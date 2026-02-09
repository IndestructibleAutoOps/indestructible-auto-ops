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
from collections.abc import Callable
from pathlib import Path

from .file_validator import FileCheckValidator
from .performance_validator import MemoryValidator, PerformanceValidator
from .validator import (
    Severity,
    ValidationConfig,
    ValidationIssue,
    ValidationResult,
    ValidatorResult,
)
from .whitelist_manager import WhitelistManager


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
        whitelist_manager: WhitelistManager | None = None,
    ):
        self.config = config
        self.results: dict[str, ValidatorResult] = {}
        self.whitelist_manager = whitelist_manager
        self.baseline = self._load_baseline()
        self._custom_validators: dict[str, Callable] = {}

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

                # 重新计算 passed 状态：如果白名单抑制后没有阻塞性问题，则通过
                if not validator_result.issues:
                    validator_result.passed = True
                else:
                    has_blocking = any(issue.is_blocking() for issue in validator_result.issues)
                    validator_result.passed = not has_blocking

            # 保存白名单规则（包含审计日志）一次
            self.whitelist_manager.save_rules()

        # 生成最终报告
        report = self._generate_report(suppressed_count)

        # 保存报告
        report_path = report.save(self.config.output_dir)

        # 只在验证通过时保存基线，避免将失败/退化的运行作为新基线
        if report.overall_passed:
            self._save_baseline()
        else:
            print("⚠️  验证未通过，基线数据未更新")

        total_time = time.time() - total_start
        print(f"\n⏱️  验证总耗时: {total_time:.3f}s")
        print(f"📄 报告已保存: {report_path}")

        return report

    def _run_validator(self, name: str) -> ValidatorResult | None:
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
        """生成验证报告（基于白名单后的最终问题列表）"""
        # 检查是否存在阻塞性问题（白名单后）
        has_blockers = any(
            any(issue.is_blocking() for issue in v.issues) for v in self.results.values()
        )

        # 整体通过需要：无阻塞性问题 + 至少有一个验证器运行
        overall_passed = not has_blockers and len(self.results) > 0

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
            except (OSError, json.JSONDecodeError):
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
        self.whitelist = WhitelistManager(config.whitelist_path) if config.whitelist_path else None
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

    def register_benchmark(self, name: str, func: Callable) -> None:
        """注册性能基准测试（当前为兼容性保留的空操作）。

        注意：
            历史上该方法尝试在 ValidationEngine 上存储自定义基准，
            但这些数据并不会被 StrictValidator 或 PerformanceValidator 使用。
            为避免误导与静态分析告警，该方法目前不再持久化任何状态。

            如需添加自定义基准测试，请直接在 PerformanceValidator 中配置。
        """
        # 当前实现为安全的空操作，不存储任何状态
        pass
