#!/usr/bin/env python3
"""
NG 閉環決策引擎
Decision Engine - External-Constraint-Driven

v2 核心原則：
- 終止條件由外部約束驅動（非內部收斂分數）
- 內部指標僅作為警告信號
- 優先級：外部約束 > 內部警告 > 手動決策
- 無回滾，只有前向自適應調整
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class TerminationReason(Enum):
    """終止原因"""
    OBJECTIVE_MET = "business_objective_met"
    TIME_EXHAUSTED = "time_budget_exhausted"
    RESOURCE_EXHAUSTED = "resource_budget_exhausted"
    MANUAL_STOP = "manual_decision"
    MAX_CYCLES = "max_cycles_reached"
    ERROR_LIMIT = "error_limit_reached"


class ContinuationMode(Enum):
    """繼續模式"""
    STANDARD = "standard"
    ADJUSTED = "adjusted"       # 帶參數調整
    DEGRADED = "degraded"       # 降級模式


class CycleDecision(Enum):
    """迴圈決策"""
    TERMINATE_SUCCESS = "terminate_success"
    TERMINATE_TIMEOUT = "terminate_timeout"
    TERMINATE_RESOURCE_LIMIT = "terminate_resource_limit"
    TERMINATE_ERROR_LIMIT = "terminate_error_limit"
    TERMINATE_MAX_CYCLES = "terminate_max_cycles"
    TERMINATE_MANUAL = "terminate_manual"
    CONTINUE_STANDARD = "continue_standard"
    CONTINUE_ADJUSTED = "continue_adjusted"
    CONTINUE_DEGRADED = "continue_degraded"


@dataclass
class ExternalConstraints:
    """外部約束（不可協商）"""
    business_objective_met: bool = False
    time_budget_seconds: float = 3600.0
    time_elapsed_seconds: float = 0.0
    resource_budget_units: float = 1000.0
    resource_consumed_units: float = 0.0
    max_cycles: int = 100
    current_cycle: int = 0
    manual_stop_requested: bool = False

    @property
    def time_remaining(self) -> float:
        return max(0.0, self.time_budget_seconds - self.time_elapsed_seconds)

    @property
    def resource_remaining(self) -> float:
        return max(0.0, self.resource_budget_units - self.resource_consumed_units)

    @property
    def time_exhausted(self) -> bool:
        return self.time_elapsed_seconds >= self.time_budget_seconds

    @property
    def resource_exhausted(self) -> bool:
        return self.resource_consumed_units >= self.resource_budget_units

    @property
    def max_cycles_reached(self) -> bool:
        return self.current_cycle >= self.max_cycles


@dataclass
class InternalSignals:
    """內部信號（僅警告用，非決策用）"""
    metric_stability: float = 0.0
    insight_novelty: float = 0.0
    error_rate_trend: float = 0.0
    resource_efficiency: float = 0.0
    verification_pass_rate: float = 0.0
    cumulative_error: float = 0.0

    @property
    def convergence_indicator(self) -> float:
        """
        收斂指標（僅供參考，不用於決策）
        """
        return (
            0.25 * self.metric_stability
            + 0.25 * (1.0 - self.insight_novelty)
            + 0.25 * (1.0 - self.error_rate_trend)
            + 0.25 * self.resource_efficiency
        )

    @property
    def warnings(self) -> List[str]:
        w: List[str] = []
        if self.metric_stability < 0.5:
            w.append(f"Low metric stability: {self.metric_stability:.2f}")
        if self.error_rate_trend > 0.5:
            w.append(f"Rising error trend: {self.error_rate_trend:.2f}")
        if self.resource_efficiency < 0.3:
            w.append(f"Low resource efficiency: {self.resource_efficiency:.2f}")
        if self.cumulative_error > 0.03:
            w.append(f"Cumulative error exceeds 3%: {self.cumulative_error:.4f}")
        return w


@dataclass
class DecisionRecord:
    """決策記錄（不可變）"""
    cycle_id: str
    decision: CycleDecision
    reason: str
    external_constraints: Dict[str, Any]
    internal_signals: Dict[str, Any]
    warnings: List[str]
    adjustments: Dict[str, Any]
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = _utc_now()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["decision"] = self.decision.value
        return d


class DecisionEngine:
    """
    閉環決策引擎

    決策優先級：
    1. 外部約束（不可協商）
    2. 錯誤限制
    3. 內部警告（記錄但不決策）
    4. 繼續或手動決策
    """

    def __init__(self, error_limit: int = 10):
        self._history: List[DecisionRecord] = []
        self._error_count: int = 0
        self._error_limit: int = error_limit

    def make_decision(
        self,
        cycle_id: str,
        external: ExternalConstraints,
        internal: InternalSignals,
        verification_blocked: bool = False,
    ) -> DecisionRecord:
        """
        做出迴圈繼續/終止決策。

        Args:
            cycle_id: 當前迴圈 ID
            external: 外部約束
            internal: 內部信號
            verification_blocked: 驗證門是否阻斷

        Returns:
            不可變的決策記錄
        """
        warnings = internal.warnings

        # === 優先級 1: 外部約束（不可協商）===
        if external.business_objective_met:
            return self._record(cycle_id, CycleDecision.TERMINATE_SUCCESS,
                                "Business objective met", external, internal, warnings)

        if external.manual_stop_requested:
            return self._record(cycle_id, CycleDecision.TERMINATE_MANUAL,
                                "Manual stop requested", external, internal, warnings)

        if external.time_exhausted:
            return self._record(cycle_id, CycleDecision.TERMINATE_TIMEOUT,
                                f"Time budget exhausted ({external.time_budget_seconds}s)",
                                external, internal, warnings)

        if external.resource_exhausted:
            return self._record(cycle_id, CycleDecision.TERMINATE_RESOURCE_LIMIT,
                                f"Resource budget exhausted ({external.resource_budget_units} units)",
                                external, internal, warnings)

        if external.max_cycles_reached:
            return self._record(cycle_id, CycleDecision.TERMINATE_MAX_CYCLES,
                                f"Max cycles reached ({external.max_cycles})",
                                external, internal, warnings)

        # === 優先級 2: 驗證門阻斷 ===
        if verification_blocked:
            self._error_count += 1
            if self._error_count >= self._error_limit:
                return self._record(cycle_id, CycleDecision.TERMINATE_ERROR_LIMIT,
                                    f"Error limit reached ({self._error_limit})",
                                    external, internal, warnings)
            return self._record(cycle_id, CycleDecision.CONTINUE_DEGRADED,
                                "Verification blocked, degraded mode",
                                external, internal, warnings,
                                adjustments={"mode": "degraded", "error_count": self._error_count})

        # === 優先級 3: 自適應調整 ===
        adjustments: Dict[str, Any] = {}

        if internal.cumulative_error > 0.03:
            adjustments["reduce_scope"] = True
            warnings.append("Adjusting: reducing scope due to error accumulation")

        if internal.resource_efficiency < 0.3:
            adjustments["optimize_resources"] = True
            warnings.append("Adjusting: optimizing resource allocation")

        if adjustments:
            return self._record(cycle_id, CycleDecision.CONTINUE_ADJUSTED,
                                "Continuing with adjustments",
                                external, internal, warnings, adjustments)

        # === 默認: 標準繼續 ===
        return self._record(cycle_id, CycleDecision.CONTINUE_STANDARD,
                            "All constraints satisfied, continuing",
                            external, internal, warnings)

    @property
    def history(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self._history]

    @property
    def is_terminated(self) -> bool:
        if not self._history:
            return False
        return self._history[-1].decision.value.startswith("terminate")

    @property
    def termination_reason(self) -> Optional[str]:
        if self.is_terminated:
            return self._history[-1].reason
        return None

    def _record(
        self,
        cycle_id: str,
        decision: CycleDecision,
        reason: str,
        external: ExternalConstraints,
        internal: InternalSignals,
        warnings: List[str],
        adjustments: Optional[Dict[str, Any]] = None,
    ) -> DecisionRecord:
        record = DecisionRecord(
            cycle_id=cycle_id,
            decision=decision,
            reason=reason,
            external_constraints=asdict(external),
            internal_signals=asdict(internal),
            warnings=list(warnings),
            adjustments=adjustments or {},
        )
        self._history.append(record)
        return record
