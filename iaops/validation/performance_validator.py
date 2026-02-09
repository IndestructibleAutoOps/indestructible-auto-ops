"""
性能验证器
Performance Regression Validator

Validates:
- API response latency against baseline
- Algorithm execution time regression
- Memory usage anomaly detection
- Throughput regression detection
"""

import time
from typing import Callable, Dict, List, Optional

from .validator import Severity, ValidationConfig, ValidationIssue, ValidatorResult
from .regression_detector import RegressionDetector


class PerformanceValidator:
    """
    性能回归验证器
    检测 API 延迟、算法耗时、内存使用和吞吐量的退化
    """

    def __init__(self, config: ValidationConfig, baseline: Optional[dict] = None):
        self.config = config
        self.name = "performance_validator"
        self.baseline = baseline or {}
        self.detector = RegressionDetector(config)
        self._benchmarks: Dict[str, Callable] = {}

    def register_benchmark(self, name: str, func: Callable):
        """
        注册性能基准测试函数
        :param name: 基准测试名称
        :param func: 无参数的可调用对象，返回 float (耗时/延迟)
        """
        self._benchmarks[name] = func

    def execute(self) -> ValidatorResult:
        """执行性能验证"""
        start_time = time.time()
        issues: List[ValidationIssue] = []

        # 1. 执行已注册的基准测试
        for bench_name, bench_func in self._benchmarks.items():
            bench_issues = self._run_benchmark(bench_name, bench_func)
            issues.extend(bench_issues)

        # 2. 检查基线中的指标回归
        issues.extend(self._check_baseline_metrics())

        passed = not any(issue.is_blocking() for issue in issues)
        execution_time = time.time() - start_time

        return ValidatorResult(
            validator_name=self.name,
            passed=passed,
            issues=issues,
            execution_time=execution_time,
        )

    def _run_benchmark(
        self, name: str, func: Callable, iterations: int = 3
    ) -> List[ValidationIssue]:
        """
        运行单个基准测试并与基线对比
        :param name: 测试名称
        :param func: 测试函数
        :param iterations: 重复次数取平均
        """
        issues = []

        # 多次运行取平均值
        timings = []
        for _ in range(iterations):
            t_start = time.perf_counter()
            try:
                func()
            except Exception as e:
                issues.append(ValidationIssue(
                    issue_id=f"benchmark_error_{name}",
                    description=f"基准测试执行失败: {name} - {str(e)}",
                    severity=Severity.ERROR,
                    details={
                        "benchmark": name,
                        "error": str(e),
                        "error_type": type(e).__name__,
                    },
                    category="performance",
                    source=name,
                ))
                return issues
            t_end = time.perf_counter()
            timings.append(t_end - t_start)

        avg_time = sum(timings) / len(timings)

        # 与基线对比
        baseline_time = self.baseline.get(f"benchmark_{name}")
        if baseline_time is not None:
            issue = self.detector.detect_numeric(
                current=avg_time,
                baseline=baseline_time,
                metric_type="performance",
                metric_name=name,
            )
            if issue:
                issue.details["iterations"] = iterations
                issue.details["timings"] = [round(t, 6) for t in timings]
                issue.details["avg_time"] = round(avg_time, 6)
                issues.append(issue)

        # 更新基线
        self.baseline[f"benchmark_{name}"] = round(avg_time, 6)
        return issues

    def _check_baseline_metrics(self) -> List[ValidationIssue]:
        """检查基线中记录的性能指标"""
        issues = []
        perf_metrics = self.baseline.get("performance_metrics", {})

        for metric_name, metric_data in perf_metrics.items():
            if not isinstance(metric_data, dict):
                continue

            current = metric_data.get("current")
            baseline_val = metric_data.get("baseline")
            metric_type = metric_data.get("type", "performance")

            if current is not None and baseline_val is not None:
                issue = self.detector.detect_numeric(
                    current=current,
                    baseline=baseline_val,
                    metric_type=metric_type,
                    metric_name=metric_name,
                )
                if issue:
                    issues.append(issue)

        return issues

    def add_metric(self, name: str, current: float, baseline: float,
                   metric_type: str = "performance"):
        """
        手动添加性能指标用于验证
        :param name: 指标名称
        :param current: 当前值
        :param baseline: 基线值
        :param metric_type: 指标类型
        """
        if "performance_metrics" not in self.baseline:
            self.baseline["performance_metrics"] = {}

        self.baseline["performance_metrics"][name] = {
            "current": current,
            "baseline": baseline,
            "type": metric_type,
        }

    def get_updated_baseline(self) -> dict:
        """获取更新后的基线数据"""
        return self.baseline


class MemoryValidator:
    """
    内存使用验证器
    检测内存泄漏和异常内存增长
    """

    def __init__(self, config: ValidationConfig, baseline: Optional[dict] = None):
        self.config = config
        self.name = "memory_validator"
        self.baseline = baseline or {}
        self.detector = RegressionDetector(config)

    def execute(self) -> ValidatorResult:
        """执行内存验证"""
        start_time = time.time()
        issues: List[ValidationIssue] = []

        try:
            import resource
            current_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            baseline_mem = self.baseline.get("peak_memory")

            if baseline_mem is not None:
                # 内存增长超过 50% 视为异常
                if current_mem > baseline_mem * 1.5:
                    growth_pct = ((current_mem - baseline_mem) / baseline_mem) * 100
                    issues.append(ValidationIssue(
                        issue_id="memory_growth_anomaly",
                        description=f"内存使用异常增长: {growth_pct:.1f}% "
                                    f"(基线: {baseline_mem}KB, 当前: {current_mem}KB)",
                        severity=Severity.WARNING,
                        details={
                            "baseline_kb": baseline_mem,
                            "current_kb": current_mem,
                            "growth_pct": round(growth_pct, 1),
                        },
                        category="performance",
                        source="memory",
                    ))

            self.baseline["peak_memory"] = current_mem
        except (ImportError, AttributeError):
            pass

        passed = not any(issue.is_blocking() for issue in issues)
        execution_time = time.time() - start_time

        return ValidatorResult(
            validator_name=self.name,
            passed=passed,
            issues=issues,
            execution_time=execution_time,
        )

    def get_updated_baseline(self) -> dict:
        """获取更新后的基线数据"""
        return self.baseline