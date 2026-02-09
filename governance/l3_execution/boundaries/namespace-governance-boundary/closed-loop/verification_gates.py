#!/usr/bin/env python3
"""
NG 閉環分層驗證門
Layered Verification Gates

v2 設計：分層驗證（非串聯阻斷）
- Layer 0: 假設驗證（不可繞過）
- Layer 1-N: 可配置驗證層（可失敗、可覆寫）

核心原則：
- Layer 0 永遠不可繞過（初始假設必須明確）
- 上層失敗記錄但不阻斷（除非配置為阻斷）
- 所有驗證結果形成不可變記錄
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class GateAction(Enum):
    """驗證門失敗時的動作"""
    BLOCK = "block"              # 阻斷（不可繼續）
    LOG_AND_CONTINUE = "log_and_continue"  # 記錄並繼續
    WARN_AND_CONTINUE = "warn_and_continue"  # 警告並繼續
    THROTTLE = "throttle"        # 降速繼續


class GateResult(Enum):
    """驗證門結果"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    OVERRIDDEN = "overridden"


@dataclass
class VerificationResult:
    """單個驗證門的結果"""
    gate_id: str
    layer: int
    metric_name: str
    metric_value: Any
    threshold: Any
    result: GateResult
    action_taken: GateAction
    timestamp: str = ""
    message: str = ""
    overridden_by: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = _utc_now()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["result"] = self.result.value
        d["action_taken"] = self.action_taken.value
        return d


@dataclass
class GateDefinition:
    """驗證門定義"""
    gate_id: str
    layer: int
    metric_name: str
    description: str
    threshold: Any
    comparator: str  # "eq", "gte", "lte", "gt", "lt"
    failure_action: GateAction
    can_be_bypassed: bool
    evaluator: Optional[Callable[..., Any]] = field(default=None, repr=False)


class VerificationGateSystem:
    """
    分層驗證門系統

    Layer 0: 不可繞過（假設驗證）
    Layer 1+: 可配置
    """

    def __init__(self):
        self._gates: List[GateDefinition] = []
        self._results_history: List[List[VerificationResult]] = []
        self._setup_default_gates()

    def _setup_default_gates(self) -> None:
        """設定預設驗證門"""
        # Layer 0: 假設驗證（絕對不可繞過）
        self._gates.append(GateDefinition(
            gate_id="V0_assumption_verification",
            layer=0,
            metric_name="initial_assumptions_documented",
            description="初始假設必須明確文檔化且經外部審查",
            threshold=True,
            comparator="eq",
            failure_action=GateAction.BLOCK,
            can_be_bypassed=False,
        ))

        # Layer 1: 內部一致性
        self._gates.append(GateDefinition(
            gate_id="V1_internal_consistency",
            layer=1,
            metric_name="hash_divergence",
            description="內部狀態一致性（hash 偏差）",
            threshold=0.0,
            comparator="lte",
            failure_action=GateAction.LOG_AND_CONTINUE,
            can_be_bypassed=True,
        ))

        # Layer 2: 外部可驗證性
        self._gates.append(GateDefinition(
            gate_id="V2_external_verifiability",
            layer=2,
            metric_name="validation_rate",
            description="外部驗證通過率",
            threshold=0.95,
            comparator="gte",
            failure_action=GateAction.WARN_AND_CONTINUE,
            can_be_bypassed=True,
        ))

        # Layer 3: 規模穩定性
        self._gates.append(GateDefinition(
            gate_id="V3_scale_stability",
            layer=3,
            metric_name="performance_variance",
            description="效能方差 <= 閾值",
            threshold=0.03,
            comparator="lte",
            failure_action=GateAction.THROTTLE,
            can_be_bypassed=True,
        ))

        # Layer 4: 因果鏈完整性
        self._gates.append(GateDefinition(
            gate_id="V4_causal_completeness",
            layer=4,
            metric_name="proof_chain_coverage",
            description="因果鏈覆蓋率",
            threshold=0.90,
            comparator="gte",
            failure_action=GateAction.LOG_AND_CONTINUE,
            can_be_bypassed=True,
        ))

    def add_gate(self, gate: GateDefinition) -> None:
        """新增驗證門"""
        if gate.layer == 0 and gate.can_be_bypassed:
            raise ValueError("Layer 0 gates cannot be bypassed")
        self._gates.append(gate)
        self._gates.sort(key=lambda g: (g.layer, g.gate_id))

    def evaluate_all(
        self,
        metrics: Dict[str, Any],
        assumptions_verified: bool = False,
        override_gates: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        執行所有驗證門。

        Args:
            metrics: 當前度量值 {"metric_name": value}
            assumptions_verified: 初始假設是否已驗證
            override_gates: 可覆寫的門 {"gate_id": "override_reason"}

        Returns:
            {
                "all_passed": bool,
                "blocked": bool,
                "results": [VerificationResult, ...],
                "summary": {...}
            }
        """
        override_gates = override_gates or {}
        results: List[VerificationResult] = []
        blocked = False

        # 注入假設驗證指標
        full_metrics = dict(metrics)
        full_metrics["initial_assumptions_documented"] = assumptions_verified

        for gate in self._gates:
            metric_value = full_metrics.get(gate.metric_name)

            # 度量缺失
            if metric_value is None:
                result = VerificationResult(
                    gate_id=gate.gate_id,
                    layer=gate.layer,
                    metric_name=gate.metric_name,
                    metric_value=None,
                    threshold=gate.threshold,
                    result=GateResult.FAILED,
                    action_taken=gate.failure_action,
                    message=f"Metric '{gate.metric_name}' not provided",
                )
                if not gate.can_be_bypassed:
                    blocked = True
                results.append(result)
                continue

            # 比較
            passed = self._compare(metric_value, gate.threshold, gate.comparator)

            if passed:
                result = VerificationResult(
                    gate_id=gate.gate_id,
                    layer=gate.layer,
                    metric_name=gate.metric_name,
                    metric_value=metric_value,
                    threshold=gate.threshold,
                    result=GateResult.PASSED,
                    action_taken=GateAction.LOG_AND_CONTINUE,
                    message="Gate passed",
                )
            elif gate.gate_id in override_gates:
                result = VerificationResult(
                    gate_id=gate.gate_id,
                    layer=gate.layer,
                    metric_name=gate.metric_name,
                    metric_value=metric_value,
                    threshold=gate.threshold,
                    result=GateResult.OVERRIDDEN,
                    action_taken=GateAction.LOG_AND_CONTINUE,
                    message=f"Overridden: {override_gates[gate.gate_id]}",
                    overridden_by=override_gates[gate.gate_id],
                )
            else:
                result = VerificationResult(
                    gate_id=gate.gate_id,
                    layer=gate.layer,
                    metric_name=gate.metric_name,
                    metric_value=metric_value,
                    threshold=gate.threshold,
                    result=GateResult.FAILED,
                    action_taken=gate.failure_action,
                    message=f"Failed: {gate.metric_name}={metric_value} vs threshold={gate.threshold}",
                )
                if not gate.can_be_bypassed:
                    blocked = True

            results.append(result)

        all_passed = all(r.result in (GateResult.PASSED, GateResult.OVERRIDDEN) for r in results)

        cycle_results = {
            "all_passed": all_passed,
            "blocked": blocked,
            "results": [r.to_dict() for r in results],
            "summary": {
                "total_gates": len(results),
                "passed": sum(1 for r in results if r.result == GateResult.PASSED),
                "failed": sum(1 for r in results if r.result == GateResult.FAILED),
                "overridden": sum(1 for r in results if r.result == GateResult.OVERRIDDEN),
                "blocked": blocked,
            },
            "timestamp": _utc_now(),
        }

        self._results_history.append(results)
        return cycle_results

    def get_history(self) -> List[List[Dict[str, Any]]]:
        return [[r.to_dict() for r in cycle] for cycle in self._results_history]

    @staticmethod
    def _compare(value: Any, threshold: Any, comparator: str) -> bool:
        ops = {
            "eq": lambda v, t: v == t,
            "gte": lambda v, t: v >= t,
            "lte": lambda v, t: v <= t,
            "gt": lambda v, t: v > t,
            "lt": lambda v, t: v < t,
        }
        fn = ops.get(comparator)
        if fn is None:
            raise ValueError(f"Unknown comparator: {comparator}")
        try:
            return fn(value, threshold)
        except TypeError:
            return False
