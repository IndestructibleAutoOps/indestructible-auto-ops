#!/usr/bin/env python3
"""
NG 閉環迴圈編排器
Cycle Orchestrator - Full Closed-Loop Lifecycle

統一管理閉環的完整生命週期：
  lock_state -> verify -> execute -> evaluate_cost -> decide -> audit -> (next | terminate)

這是所有閉環組件的頂層協調器。
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .state_lock import StateLockChain, CycleParameters
from .verification_gates import VerificationGateSystem
from .decision_engine import (
    DecisionEngine,
    ExternalConstraints,
    InternalSignals,
    CycleDecision,
)
from .cost_evaluator import CostEvaluator, CycleCost, CycleBenefit
from .audit_trail import AuditTrail, AuditEventType, AuditSeverity


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CycleConfig:
    """迴圈配置"""
    max_cycles: int = 100
    time_budget_seconds: float = 3600.0
    resource_budget_units: float = 1000.0
    error_limit: int = 10
    assumptions: List[str] = field(default_factory=list)
    storage_dir: Optional[str] = None


@dataclass
class CycleContext:
    """迴圈上下文（每輪傳遞）"""
    cycle_id: str
    sequence: int
    parameters: List[CycleParameters]
    metrics: Dict[str, Any]
    assumptions_verified: bool
    work_result: Any = None


class CycleOrchestrator:
    """
    閉環迴圈編排器

    完整流程：
    1. 初始化（鎖定假設和約束）
    2. 迴圈開始：鎖定初始狀態
    3. 驗證門檢查
    4. 執行工作（由使用者定義的 work_fn）
    5. 記錄成本和收益
    6. 決策引擎判定
    7. 審計記錄
    8. 繼續或終止
    """

    def __init__(self, config: CycleConfig):
        self._config = config
        storage = Path(config.storage_dir) if config.storage_dir else None

        self._state_chain = StateLockChain(
            storage_path=storage / "state_chain.json" if storage else None
        )
        self._gates = VerificationGateSystem()
        self._decision = DecisionEngine(error_limit=config.error_limit)
        self._cost = CostEvaluator()
        self._audit = AuditTrail(
            storage_path=storage / "audit_trail.json" if storage else None,
            actor="cycle_orchestrator",
        )

        self._current_cycle: int = 0
        self._time_start: Optional[float] = None
        self._resource_consumed: float = 0.0
        self._terminated: bool = False
        self._termination_report: Optional[Dict[str, Any]] = None

    def run(
        self,
        initial_parameters: List[CycleParameters],
        external_constraints: Dict[str, Any],
        work_fn: Callable[[CycleContext], Dict[str, Any]],
        metrics_fn: Callable[[int, Any], Dict[str, Any]],
        cost_fn: Callable[[int, Any], CycleCost],
        benefit_fn: Callable[[int, Any], CycleBenefit],
    ) -> Dict[str, Any]:
        """
        執行完整閉環迴圈。

        Args:
            initial_parameters: 初始參數
            external_constraints: 外部約束
            work_fn: 每輪執行的工作函數 (CycleContext) -> result_dict
            metrics_fn: 產生度量的函數 (cycle_num, work_result) -> metrics
            cost_fn: 產生成本的函數 (cycle_num, work_result) -> CycleCost
            benefit_fn: 產生收益的函數 (cycle_num, work_result) -> CycleBenefit

        Returns:
            完整的閉環執行報告
        """
        import time

        self._time_start = time.monotonic()
        self._terminated = False

        self._audit.record(
            AuditEventType.CYCLE_STARTED,
            "INIT",
            {
                "config": {
                    "max_cycles": self._config.max_cycles,
                    "time_budget": self._config.time_budget_seconds,
                    "resource_budget": self._config.resource_budget_units,
                    "assumptions": self._config.assumptions,
                },
                "external_constraints": external_constraints,
            },
        )

        while not self._terminated and self._current_cycle < self._config.max_cycles:
            cycle_id = f"CYC-{self._current_cycle:04d}"
            elapsed = time.monotonic() - self._time_start

            # --- Step 1: Lock State ---
            lock = self._state_chain.lock_initial_state(
                cycle_id=cycle_id,
                parameters=initial_parameters,
                assumptions=self._config.assumptions,
                external_constraints=external_constraints,
            )

            self._audit.record(
                AuditEventType.STATE_LOCKED,
                cycle_id,
                {"state_hash": lock.state_hash, "sequence": lock.sequence},
            )

            # --- Step 2: Verification Gates ---
            # First cycle requires explicit assumption verification
            assumptions_verified = len(self._config.assumptions) > 0

            # Get metrics from previous work or initial state
            if self._current_cycle == 0:
                current_metrics = {"hash_divergence": 0.0, "validation_rate": 1.0,
                                   "performance_variance": 0.0, "proof_chain_coverage": 1.0}
            else:
                current_metrics = metrics_fn(self._current_cycle, None)

            gate_result = self._gates.evaluate_all(
                metrics=current_metrics,
                assumptions_verified=assumptions_verified,
            )

            self._audit.record(
                AuditEventType.VERIFICATION_COMPLETED,
                cycle_id,
                gate_result["summary"],
                severity=AuditSeverity.WARNING if gate_result["blocked"] else AuditSeverity.INFO,
            )

            # --- Step 3: Decision (pre-work) ---
            ext = ExternalConstraints(
                business_objective_met=external_constraints.get("business_objective_met", False),
                time_budget_seconds=self._config.time_budget_seconds,
                time_elapsed_seconds=elapsed,
                resource_budget_units=self._config.resource_budget_units,
                resource_consumed_units=self._resource_consumed,
                max_cycles=self._config.max_cycles,
                current_cycle=self._current_cycle,
                manual_stop_requested=external_constraints.get("manual_stop", False),
            )

            internal = InternalSignals(
                metric_stability=current_metrics.get("metric_stability", 0.5),
                insight_novelty=current_metrics.get("insight_novelty", 0.5),
                error_rate_trend=current_metrics.get("error_rate_trend", 0.0),
                resource_efficiency=current_metrics.get("resource_efficiency", 0.5),
                verification_pass_rate=gate_result["summary"]["passed"] / max(gate_result["summary"]["total_gates"], 1),
                cumulative_error=current_metrics.get("cumulative_error", 0.0),
            )

            decision = self._decision.make_decision(
                cycle_id=cycle_id,
                external=ext,
                internal=internal,
                verification_blocked=gate_result["blocked"],
            )

            self._audit.record(
                AuditEventType.DECISION_MADE,
                cycle_id,
                decision.to_dict(),
                severity=AuditSeverity.WARNING if decision.decision.value.startswith("terminate") else AuditSeverity.INFO,
            )

            if decision.decision.value.startswith("terminate"):
                self._terminated = True
                self._audit.record(
                    AuditEventType.CYCLE_TERMINATED,
                    cycle_id,
                    {"reason": decision.reason, "decision": decision.decision.value},
                )
                break

            # --- Step 4: Execute Work ---
            ctx = CycleContext(
                cycle_id=cycle_id,
                sequence=self._current_cycle,
                parameters=initial_parameters,
                metrics=current_metrics,
                assumptions_verified=assumptions_verified,
            )

            try:
                work_result = work_fn(ctx)
                ctx.work_result = work_result
            except Exception as exc:
                self._audit.record(
                    AuditEventType.ERROR_OCCURRED,
                    cycle_id,
                    {"error": str(exc), "type": type(exc).__name__},
                    severity=AuditSeverity.ERROR,
                )
                work_result = {"error": str(exc)}

            # --- Step 5: Cost & Benefit ---
            cost = cost_fn(self._current_cycle, work_result)
            benefit = benefit_fn(self._current_cycle, work_result)
            snapshot = self._cost.record_cycle(cost, benefit)

            self._resource_consumed += cost.total

            self._audit.record(
                AuditEventType.COST_RECORDED,
                cycle_id,
                snapshot.to_dict(),
            )

            # --- Step 6: Apply adjustments if any ---
            if decision.adjustments:
                self._audit.record(
                    AuditEventType.ADJUSTMENT_APPLIED,
                    cycle_id,
                    decision.adjustments,
                )

            self._audit.record(
                AuditEventType.CYCLE_COMPLETED,
                cycle_id,
                {
                    "sequence": self._current_cycle,
                    "cost": cost.total,
                    "benefit_score": benefit.benefit_score,
                    "roi": snapshot.roi,
                },
            )

            self._current_cycle += 1

        # --- Final Report ---
        chain_integrity = self._state_chain.verify_chain_integrity()
        audit_integrity = self._audit.verify_integrity()

        self._audit.record(
            AuditEventType.CHAIN_VALIDATED,
            f"CYC-{self._current_cycle:04d}",
            {
                "state_chain_valid": chain_integrity["valid"],
                "audit_chain_valid": audit_integrity["valid"],
            },
        )

        self._termination_report = {
            "status": "TERMINATED" if self._terminated else "MAX_CYCLES_REACHED",
            "termination_reason": self._decision.termination_reason,
            "cycles_completed": self._current_cycle,
            "state_chain_integrity": chain_integrity,
            "audit_chain_integrity": audit_integrity,
            "cost_summary": self._cost.get_summary(),
            "decision_history_length": len(self._decision.history),
            "verification_history_length": len(self._gates.get_history()),
            "timestamp": _utc_now(),
        }

        if self._config.storage_dir:
            report_path = Path(self._config.storage_dir) / "closed_loop_report.json"
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(self._termination_report, f, indent=2, ensure_ascii=False)

        return self._termination_report

    @property
    def report(self) -> Optional[Dict[str, Any]]:
        return self._termination_report

    @property
    def state_chain(self) -> StateLockChain:
        return self._state_chain

    @property
    def audit(self) -> AuditTrail:
        return self._audit

    @property
    def cost_evaluator(self) -> CostEvaluator:
        return self._cost
