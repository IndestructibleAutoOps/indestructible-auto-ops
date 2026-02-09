#!/usr/bin/env python3
"""
NG 閉環成本評估器
Real-Time Cost Evaluator

v2 核心原則：
- 只計算已實現的收益（非預測）
- 每個迴圈結束即時計算
- 不依賴未來不確定性
- 信心度基於已實現數據
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CycleCost:
    """單個迴圈的成本"""
    cycle_id: str
    compute_cost: float = 0.0
    time_cost_seconds: float = 0.0
    human_effort_hours: float = 0.0
    opportunity_cost: float = 0.0

    @property
    def total(self) -> float:
        return self.compute_cost + self.opportunity_cost


@dataclass
class CycleBenefit:
    """單個迴圈的已實現收益"""
    cycle_id: str
    insights_documented: int = 0
    problems_resolved: int = 0
    assumptions_eliminated: int = 0
    efficiency_gain_measured: float = 0.0
    error_rate_reduction: float = 0.0

    @property
    def benefit_score(self) -> float:
        """量化收益分數（基於已實現）"""
        return (
            self.insights_documented * 10.0
            + self.problems_resolved * 50.0
            + self.assumptions_eliminated * 20.0
            + self.efficiency_gain_measured * 100.0
            + self.error_rate_reduction * 200.0
        )


@dataclass
class CostBenefitSnapshot:
    """成本效益快照（不可變）"""
    cycle_id: str
    cumulative_cost: float
    cumulative_benefit_score: float
    roi: float
    marginal_roi: float  # 本輪邊際 ROI
    trend: str  # "improving", "stable", "declining"
    confidence: float  # 基於已實現數據的信心度
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = _utc_now()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CostEvaluator:
    """
    閉環實時成本評估器

    只計算已實現數據，不做預測。
    """

    def __init__(self):
        self._costs: List[CycleCost] = []
        self._benefits: List[CycleBenefit] = []
        self._snapshots: List[CostBenefitSnapshot] = []

    def record_cycle(self, cost: CycleCost, benefit: CycleBenefit) -> CostBenefitSnapshot:
        """
        記錄一個迴圈的成本和收益，產生快照。

        Args:
            cost: 本輪成本
            benefit: 本輪已實現收益

        Returns:
            不可變的成本效益快照
        """
        self._costs.append(cost)
        self._benefits.append(benefit)

        cumulative_cost = sum(c.total for c in self._costs)
        cumulative_benefit = sum(b.benefit_score for b in self._benefits)

        roi = (cumulative_benefit - cumulative_cost) / cumulative_cost if cumulative_cost > 0 else 0.0

        # 邊際 ROI（本輪）
        marginal_roi = (benefit.benefit_score - cost.total) / cost.total if cost.total > 0 else 0.0

        # 趨勢判定（基於最近 3 輪邊際 ROI）
        trend = self._compute_trend()

        # 信心度（基於數據量）
        n = len(self._costs)
        confidence = min(0.99, 0.5 + 0.1 * n)  # 隨數據量增長

        snapshot = CostBenefitSnapshot(
            cycle_id=cost.cycle_id,
            cumulative_cost=cumulative_cost,
            cumulative_benefit_score=cumulative_benefit,
            roi=roi,
            marginal_roi=marginal_roi,
            trend=trend,
            confidence=confidence,
        )

        self._snapshots.append(snapshot)
        return snapshot

    def get_summary(self) -> Dict[str, Any]:
        """取得完整摘要"""
        if not self._snapshots:
            return {"status": "no_data", "cycles": 0}

        latest = self._snapshots[-1]
        return {
            "status": "POSITIVE" if latest.roi > 0 else "NEGATIVE",
            "cycles_completed": len(self._snapshots),
            "cumulative_cost": latest.cumulative_cost,
            "cumulative_benefit": latest.cumulative_benefit_score,
            "current_roi": latest.roi,
            "marginal_roi": latest.marginal_roi,
            "trend": latest.trend,
            "confidence": latest.confidence,
            "recommendation": self._recommend(latest),
            "timestamp": latest.timestamp,
        }

    def get_history(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self._snapshots]

    def _compute_trend(self) -> str:
        """基於最近 3 輪邊際 ROI 計算趨勢"""
        if len(self._snapshots) < 2:
            return "insufficient_data"

        recent = self._snapshots[-3:] if len(self._snapshots) >= 3 else self._snapshots
        rois = [s.marginal_roi for s in recent]

        if len(rois) < 2:
            return "insufficient_data"

        avg_change = sum(rois[i] - rois[i - 1] for i in range(1, len(rois))) / (len(rois) - 1)

        if avg_change > 0.05:
            return "improving"
        elif avg_change < -0.05:
            return "declining"
        else:
            return "stable"

    @staticmethod
    def _recommend(snapshot: CostBenefitSnapshot) -> str:
        if snapshot.roi > 0.5 and snapshot.trend == "improving":
            return "STRONG_CONTINUE"
        if snapshot.roi > 0 and snapshot.trend != "declining":
            return "CONTINUE"
        if snapshot.roi > 0 and snapshot.trend == "declining":
            return "CONTINUE_WITH_CAUTION"
        if snapshot.roi <= 0 and snapshot.trend == "declining":
            return "CONSIDER_STOPPING"
        return "MONITOR"
