"""
主验证器集成 - 验证引擎
Strict Validation Engine with Pipeline Orchestration

Provides:
- StrictValidator: Orchestrates the full validation pipeline
- ValidationEngine: High-level API for running validators

Workflow:
1. Execute validators in pipeline order
2. Collect all validation results
3. Apply whitelist rules
4. Check for blocking issues
5. Generate and persist full report
"""

import json
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .validator import (
    Severity,
    ValidationConfig,
    ValidationIssue,
    ValidationResult,
    ValidatorResult,
)
from .regression_detector import RegressionDetector
from .whitelist_manager import WhitelistManager
from .file_validator import FileCheckValidator
from .performance_validator import PerformanceValidator, MemoryValidator


class StrictValidator:
    """
    严格验证器 - 管道式验证执行引擎

    VALIDATOR_PIPELINE 定义验证器执行顺序:
    1. file_validator: 文件完整性检查
    2. performance_validator: 性能回归检测
    3. memory_validator: 内存使用检测
    """

    VALIDATOR_PIPELINE = [
        "file_validator",
        "performance_validator",
        "memory_validator",
    ]

    def __init__(
        self,
        config: ValidationConfig,
        whitelist_manager: Optional[WhitelistManager] = None,
    ):
        self.config = config
        self.results: Dict[str, ValidatorResult] = {}
        self.whitelist_manager = whitelist_manager
        self.baseline = self._load_baseline()
        self._custom_validators: Dict[str, Callable] = {}

        # 确保输出目录存在
        config.ensure_dirs()

    def register_validator(self, name: str, validator_factory: Callable):
        """
        注册自定义验证器
        :param name: 验证器名称
        :param validator_factory: 工厂函数，接收 (config, baseline) 返回带 execute() 方法的对象
        """
        self._custom_validators[name] = validator_factory
        if name not in self.VALIDATOR_PIPELINE:
            self.VALIDATOR_PIPELINE.append(name)

    def validate(self) -> ValidationResult:
        """
        执行完整验证流程
        1. 按管道顺序执行所有验证器
        2. 应用白名单规则
        3. 生成最终报告
        """
        total_start = time.time()

        # 执行所有验证器
        for validator_name in self.VALIDATOR_PIPELINE:
            result = self._run_validator(validator_name)
            if result:
                self.results[validator_name] = result

        # 应用白名单规则
        suppressed_count = 0
        if self.whitelist_manager:
            for validator_result in self.results.values():
                validator_result.issues = self.whitelist_manager.apply_rules(
                    validator_result.issues
                )
                suppressed_count += self.whitelist_manager.suppression_count

        # 生成最终报告
        report = self._generate_report(suppressed_count)

        # 保存报告
        report_path = report.save(self.config.output_dir)

        # 保存更新后的基线
        self._save_baseline()

        total_time = time.time() - total_start
        print(f"\n⏱️  验证总耗时: {total_time:.3f}s")
        print(f"📄 报告已保存: {report_path}")

        return report

    def _run_validator(self, name: str) -> Optional[ValidatorResult]:
        """运行单个验证器"""
        start_time = time.time()

        try:
            validator = self._create_validator(name)
            if validator is None:
                return None

            result = validator.execute()
            result.execution_time = time.time() - start_time

            # 收集基线更新
            if hasattr(validator, "get_updated_baseline"):
                updated = validator.get_updated_baseline()
                if updated:
                    self.baseline[name] = updated

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            return ValidatorResult(
                validator_name=name,
                passed=False,
                issues=[
                    ValidationIssue(
                        issue_id=f"validator_error_{name}",
                        description=f"验证器执行异常: {name} - {str(e)}",
                        severity=Severity.ERROR,
                        details={
                            "validator": name,
                            "error": str(e),
                            "error_type": type(e).__name__,
                        },
                        category="system",
                        source=name,
                    )
                ],
                execution_time=execution_time,
            )

    def _create_validator(self, name: str):
        """根据名称创建验证器实例"""
        baseline_data = self.baseline.get(name, {})

        if name == "file_validator":
            return FileCheckValidator(self.config, baseline=baseline_data)
        elif name == "performance_validator":
            return PerformanceValidator(self.config, baseline=baseline_data)
        elif name == "memory_validator":
            return MemoryValidator(self.config, baseline=baseline_data)
        elif name in self._custom_validators:
            return self._custom_validators[name](self.config, baseline_data)
        else:
            return None

    def _generate_report(self, suppressed_count: int) -> ValidationResult:
        """生成验证报告"""
        has_blockers = any(
            len(v.blocking_issues) > 0 for v in self.results.values()
        )

        all_passed = all(result.passed for result in self.results.values())
        overall_passed = not has_blockers and all_passed and len(self.results) > 0

        return ValidationResult(
            timestamp=time.time(),
            config={
                "project_root": self.config.project_root,
                "strict_mode": self.config.strict_mode,
                "performance_threshold": self.config.performance_threshold,
                "metric_threshold": self.config.metric_threshold,
            },
            validators=self.results,
            overall_passed=overall_passed,
            suppressed_issues=suppressed_count,
        )

    def _load_baseline(self) -> dict:
        """加载基线数据"""
        baseline_path = Path(self.config.baseline_dir) / "baseline.json"
        if baseline_path.exists():
            try:
                with baseline_path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_baseline(self):
        """保存更新后的基线数据"""
        baseline_path = Path(self.config.baseline_dir) / "baseline.json"
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        with baseline_path.open("w", encoding="utf-8") as f:
            json.dump(self.baseline, f, indent=2, ensure_ascii=False)


class ValidationEngine:
    """
    高层验证引擎 API
    提供简化的验证执行接口
    """

    def __init__(self, config: ValidationConfig):
        self.config = config
        self.whitelist = (
            WhitelistManager(config.whitelist_path)
            if config.whitelist_path
            else None
        )
        self.validator = StrictValidator(config, whitelist_manager=self.whitelist)

    def run(self) -> ValidationResult:
        """执行完整验证并返回结果"""
        return self.validator.validate()

    def run_and_report(self) -> bool:
        """
        执行验证并打印报告
        :return: True 如果验证通过，False 如果失败
        """
        result = self.run()
        result.print_report()
        return result.overall_passed

    def run_and_exit(self):
        """
        执行验证，打印报告，并以适当的退出码退出
        - 通过: exit(0)
        - 失败: exit(1)
        """
        import sys
        passed = self.run_and_report()
        sys.exit(0 if passed else 1)

    def register_validator(self, name: str, factory: Callable):
        """注册自定义验证器"""
        self.validator.register_validator(name, factory)

    def register_benchmark(self, name: str, func: Callable):
        """注册性能基准测试"""
        # 这将在下次运行时被 performance_validator 使用
        if not hasattr(self, "_benchmarks"):
            self._benchmarks = {}
        self._benchmarks[name] = func