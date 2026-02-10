"""
回归检测核心算法
Regression Detection Core Algorithm

Provides:
- RegressionDetector: Detects numeric and structural regressions
  - detect_numeric: Numeric metric regression (performance / general)
  - detect_structural: Structural change detection (key diff / type change)
  - detect_trend: Multi-point trend regression detection
"""

from .validator import Severity, ValidationConfig, ValidationIssue


class RegressionDetector:
    """
    回归检测器
    支持数值型指标退化检测、结构变化检测和趋势退化检测
    """

    def __init__(self, config: ValidationConfig):
        self.config = config

    # ── 数值型回归检测 ──────────────────────────────────────────

    def detect_numeric(
        self,
        current: float,
        baseline: float,
        metric_type: str = "general",
        metric_name: str = "unknown",
    ) -> ValidationIssue | None:
        """
        检测数值型指标退化
        :param current: 当前指标值
        :param baseline: 基线指标值
        :param metric_type: 指标类型 (performance / general)
        :param metric_name: 指标名称
        :return: ValidationIssue 或 None
        """
        if baseline is None or current is None:
            return None

        if baseline == 0:
            if current != 0:
                return ValidationIssue(
                    issue_id=f"{metric_type}_regression_{metric_name}",
                    description=f"基线为零但当前值为 {current}",
                    severity=Severity.WARNING,
                    details={
                        "metric_name": metric_name,
                        "baseline": baseline,
                        "current": current,
                    },
                    category=metric_type,
                    source=metric_name,
                )
            return None

        if metric_type == "performance":
            return self._test_performance_regression(current, baseline, metric_name)
        return self._test_general_regression(current, baseline, metric_name)

    def _test_performance_regression(
        self, current: float, baseline: float, metric_name: str
    ) -> ValidationIssue | None:
        """
        检查性能退化（值越大表示退化，如延迟、响应时间）
        超过阈值则报告 CRITICAL
        """
        threshold = self.config.performance_threshold
        if current > baseline * (1 + threshold):
            regression_pct = ((current - baseline) / baseline) * 100
            return ValidationIssue(
                issue_id=f"performance_regression_{metric_name}",
                description=f"性能退化: {metric_name} 增加 {regression_pct:.2f}% "
                f"(基线: {baseline:.4f}, 当前: {current:.4f})",
                severity=Severity.CRITICAL,
                details={
                    "metric_name": metric_name,
                    "threshold": threshold,
                    "baseline": baseline,
                    "current": current,
                    "regression_pct": round(regression_pct, 2),
                    "direction": "increase",
                },
                category="performance",
                source=metric_name,
            )
        return None

    def _test_general_regression(
        self, current: float, baseline: float, metric_name: str
    ) -> ValidationIssue | None:
        """
        检查通用指标退化（值越小表示退化，如覆盖率、通过率）
        超过阈值则报告 CRITICAL
        """
        threshold = self.config.metric_threshold
        if current < baseline * (1 - threshold):
            regression_pct = ((baseline - current) / baseline) * 100
            return ValidationIssue(
                issue_id=f"metric_regression_{metric_name}",
                description=f"指标下降: {metric_name} 减少 {regression_pct:.2f}% "
                f"(基线: {baseline:.4f}, 当前: {current:.4f})",
                severity=Severity.CRITICAL,
                details={
                    "metric_name": metric_name,
                    "threshold": threshold,
                    "baseline": baseline,
                    "current": current,
                    "regression_pct": round(regression_pct, 2),
                    "direction": "decrease",
                },
                category="metric",
                source=metric_name,
            )
        return None

    # ── 结构变化检测 ──────────────────────────────────────────

    def detect_structural(
        self,
        current: dict,
        baseline: dict,
        context: str = "unknown",
    ) -> ValidationIssue | None:
        """
        检测结构变化退化（键差异、类型变更）
        结构变化为 BLOCKER 级别
        :param current: 当前数据结构
        :param baseline: 基线数据结构
        :param context: 上下文描述
        :return: ValidationIssue 或 None
        """
        if not baseline:
            return None

        current_keys = set(current.keys())
        baseline_keys = set(baseline.keys())

        if current_keys != baseline_keys:
            missing = baseline_keys - current_keys
            added = current_keys - baseline_keys
            return ValidationIssue(
                issue_id=f"structural_change_{context}",
                description=f"结构变化: 缺失键 {missing or '无'} | 新增键 {added or '无'}",
                severity=Severity.BLOCKER,
                details={
                    "context": context,
                    "missing_keys": sorted(list(missing)),
                    "added_keys": sorted(list(added)),
                    "baseline_key_count": len(baseline_keys),
                    "current_key_count": len(current_keys),
                },
                category="structural",
                source=context,
            )

        # 检查类型一致性
        for key in baseline_keys:
            base_val = baseline[key]
            curr_val = current.get(key)
            if curr_val is not None and not isinstance(curr_val, type(base_val)):
                return ValidationIssue(
                    issue_id=f"type_change_{context}_{key}",
                    description=f"类型变化: {key}: {type(base_val).__name__} → {type(curr_val).__name__}",
                    severity=Severity.BLOCKER,
                    details={
                        "context": context,
                        "key": key,
                        "old_type": type(base_val).__name__,
                        "new_type": type(curr_val).__name__,
                    },
                    category="structural",
                    source=f"{context}.{key}",
                )

        return None

    # ── 趋势退化检测 ──────────────────────────────────────────

    def detect_trend(
        self,
        values: list[float],
        metric_name: str = "unknown",
        window: int = 5,
        decline_threshold: float = 0.05,
    ) -> ValidationIssue | None:
        """
        多点趋势退化检测
        检查最近 window 个数据点是否呈持续下降趋势
        :param values: 历史数据点列表（时间顺序）
        :param metric_name: 指标名称
        :param window: 检测窗口大小
        :param decline_threshold: 每步下降阈值
        :return: ValidationIssue 或 None
        """
        if len(values) < window:
            return None

        recent = values[-window:]
        decline_count = 0
        for i in range(1, len(recent)):
            if recent[i - 1] > 0:
                change = (recent[i] - recent[i - 1]) / recent[i - 1]
                if change < -decline_threshold:
                    decline_count += 1

        # 如果超过 60% 的步骤都在下降，则报告趋势退化
        if decline_count >= window * 0.6:
            total_decline = ((recent[0] - recent[-1]) / recent[0]) * 100 if recent[0] > 0 else 0
            return ValidationIssue(
                issue_id=f"trend_regression_{metric_name}",
                description=f"趋势退化: {metric_name} 在最近 {window} 个数据点中"
                f"持续下降 {total_decline:.2f}%",
                severity=Severity.WARNING,
                details={
                    "metric_name": metric_name,
                    "window": window,
                    "decline_count": decline_count,
                    "total_decline_pct": round(total_decline, 2),
                    "recent_values": recent,
                },
                category="trend",
                source=metric_name,
            )

        return None

    # ── 批量检测 ──────────────────────────────────────────────

    def detect_all(
        self,
        current_metrics: dict[str, float],
        baseline_metrics: dict[str, float],
        metric_types: dict[str, str] | None = None,
    ) -> list[ValidationIssue]:
        """
        批量检测所有指标的回归
        :param current_metrics: 当前指标字典
        :param baseline_metrics: 基线指标字典
        :param metric_types: 指标类型映射 (metric_name -> performance/general)
        :return: 所有检测到的问题列表
        """
        issues = []
        metric_types = metric_types or {}

        # 结构检测
        structural_issue = self.detect_structural(
            current_metrics, baseline_metrics, context="metrics"
        )
        if structural_issue:
            issues.append(structural_issue)

        # 数值检测
        for name, current_val in current_metrics.items():
            baseline_val = baseline_metrics.get(name)
            if baseline_val is not None and isinstance(current_val, (int, float)):
                m_type = metric_types.get(name, "general")
                issue = self.detect_numeric(current_val, baseline_val, m_type, name)
                if issue:
                    issues.append(issue)

        return issues
