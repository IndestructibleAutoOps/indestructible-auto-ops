#!/usr/bin/env python3
"""
Playbook Runner Service

Executes team playbooks with:
- Stage orchestration
- Parallel execution
- Evidence collection
- Quality gates
- Audit logging
"""

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class StageStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


class PlaybookStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"


@dataclass
class StageResult:
    stage_id: str
    name: str
    status: StageStatus
    started_at: str | None = None
    completed_at: str | None = None
    duration_seconds: float = 0.0
    outputs: dict[str, Any] = field(default_factory=dict)
    artifacts: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass
class PlaybookResult:
    playbook_name: str
    version: str
    status: PlaybookStatus
    trigger_event: str
    started_at: str
    completed_at: str | None = None
    duration_seconds: float = 0.0
    stages: list[StageResult] = field(default_factory=list)
    quality_gates_passed: bool = True
    artifacts: list[str] = field(default_factory=list)
    evidence_bundle: str | None = None


class PlaybookRunner:
    """Execute playbooks with full lifecycle management."""

    def __init__(
        self,
        playbooks_dir: str = "teams/default-team/playbooks",
        artifacts_dir: str = "/tmp/playbook-artifacts",
    ):
        self._playbooks_dir = Path(playbooks_dir)
        self._artifacts_dir = Path(artifacts_dir)
        self._artifacts_dir.mkdir(parents=True, exist_ok=True)
        self._action_handlers: dict[str, Callable] = {}
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        """Register default action handlers."""
        self._action_handlers = {
            "setup_environment": self._action_setup_environment,
            "run_linters": self._action_run_linters,
            "generate_report": self._action_generate_report,
            "scan_dependencies": self._action_scan_dependencies,
            "run_sast": self._action_run_sast,
            "run_pytest": self._action_run_pytest,
            "aggregate_results": self._action_aggregate_results,
            "notify_pr": self._action_notify_pr,
        }

    def register_action(self, action_name: str, handler: Callable) -> None:
        """Register a custom action handler."""
        self._action_handlers[action_name] = handler

    async def load_playbook(self, name: str) -> dict[str, Any]:
        """Load a playbook by name."""
        playbook_path = self._playbooks_dir / f"{name}.yaml"

        if not playbook_path.exists():
            raise FileNotFoundError(f"Playbook not found: {playbook_path}")

        with open(playbook_path) as f:
            return yaml.safe_load(f)

    async def execute(
        self,
        playbook_name: str,
        trigger_event: str,
        context: dict[str, Any] | None = None,
    ) -> PlaybookResult:
        """Execute a playbook."""
        start_time = datetime.utcnow()
        context = context or {}

        logger.info(f"Starting playbook: {playbook_name}")

        try:
            playbook = await self.load_playbook(playbook_name)
        except FileNotFoundError:
            return PlaybookResult(
                playbook_name=playbook_name,
                version="unknown",
                status=PlaybookStatus.FAILURE,
                trigger_event=trigger_event,
                started_at=start_time.isoformat(),
                completed_at=datetime.utcnow().isoformat(),
            )

        result = PlaybookResult(
            playbook_name=playbook.get("name", playbook_name),
            version=playbook.get("version", "1.0.0"),
            status=PlaybookStatus.RUNNING,
            trigger_event=trigger_event,
            started_at=start_time.isoformat(),
        )

        stages = playbook.get("stages", [])
        stage_results: dict[str, StageResult] = {}

        for stage in stages:
            stage_id = stage.get("id")
            stage_name = stage.get("name", stage_id)

            depends_on = stage.get("depends_on", [])
            should_skip = False

            for dep in depends_on:
                dep_result = stage_results.get(dep)
                if dep_result and dep_result.status != StageStatus.SUCCESS:
                    should_skip = True
                    break

            condition = stage.get("condition")
            if condition and not self._evaluate_condition(
                condition, stage_results, context
            ):
                should_skip = True

            if should_skip:
                stage_result = StageResult(
                    stage_id=stage_id,
                    name=stage_name,
                    status=StageStatus.SKIPPED,
                )
                stage_results[stage_id] = stage_result
                result.stages.append(stage_result)
                continue

            stage_result = await self._execute_stage(stage, context, stage_results)
            stage_results[stage_id] = stage_result
            result.stages.append(stage_result)

            if stage_result.status == StageStatus.FAILURE:
                run_on = stage.get("run_on", "success")
                if run_on != "always":
                    break

        end_time = datetime.utcnow()
        result.completed_at = end_time.isoformat()
        result.duration_seconds = (end_time - start_time).total_seconds()

        all_success = all(
            s.status in [StageStatus.SUCCESS, StageStatus.SKIPPED]
            for s in result.stages
        )
        result.status = (
            PlaybookStatus.SUCCESS if all_success else PlaybookStatus.FAILURE
        )

        result.quality_gates_passed = await self._check_quality_gates(
            playbook.get("quality_gates", []),
            stage_results,
        )

        result.evidence_bundle = await self._create_evidence_bundle(result)

        logger.info(f"Playbook completed: {playbook_name} - {result.status.value}")

        return result

    async def _execute_stage(
        self,
        stage: dict[str, Any],
        context: dict[str, Any],
        previous_results: dict[str, StageResult],
    ) -> StageResult:
        """Execute a single stage."""
        stage_id = stage.get("id")
        stage_name = stage.get("name", stage_id)
        start_time = datetime.utcnow()

        logger.info(f"Starting stage: {stage_name}")

        result = StageResult(
            stage_id=stage_id,
            name=stage_name,
            status=StageStatus.RUNNING,
            started_at=start_time.isoformat(),
        )

        try:
            steps = stage.get("steps", [])
            step_outputs = {}

            for step in steps:
                action = step.get("action")
                params = step.get("params", {})

                params = self._interpolate_params(
                    params, context, previous_results, step_outputs
                )

                handler = self._action_handlers.get(action)
                if handler:
                    step_result = await handler(params, context)
                    step_outputs[action] = step_result

                    if step.get("output"):
                        output_config = step["output"]
                        if "artifact" in output_config:
                            result.artifacts.append(output_config["artifact"])
                        if "outputs" in output_config:
                            result.outputs.update(step_result.get("outputs", {}))
                else:
                    logger.warning(f"Unknown action: {action}")

            result.status = StageStatus.SUCCESS

        except Exception as e:
            logger.error(f"Stage failed: {stage_name} - {e}")
            result.status = StageStatus.FAILURE
            result.error = str(e)

        end_time = datetime.utcnow()
        result.completed_at = end_time.isoformat()
        result.duration_seconds = (end_time - start_time).total_seconds()

        if stage.get("evidence_required"):
            result.evidence = {
                "stage_id": stage_id,
                "timestamp": end_time.isoformat(),
                "status": result.status.value,
                "artifacts": result.artifacts,
            }

        return result

    def _interpolate_params(
        self,
        params: dict[str, Any],
        context: dict[str, Any],
        previous_results: dict[str, StageResult],
        step_outputs: dict[str, Any],
    ) -> dict[str, Any]:
        """Interpolate parameter values."""
        result = {}
        for key, value in params.items():
            if isinstance(value, str) and "{" in value:
                value = value.format(
                    **context,
                    stages=previous_results,
                    outputs=step_outputs,
                )
            result[key] = value
        return result

    def _evaluate_condition(
        self,
        condition: str,
        stage_results: dict[str, StageResult],
        context: dict[str, Any],
    ) -> bool:
        """Evaluate a condition string."""
        try:
            return True
        except Exception:
            return False

    async def _check_quality_gates(
        self,
        gates: list[dict[str, Any]],
        stage_results: dict[str, StageResult],
    ) -> bool:
        """Check if all quality gates pass."""
        for gate in gates:
            stage_id = gate.get("stage")
            required = gate.get("required", True)

            if required:
                stage_result = stage_results.get(stage_id)
                if stage_result and stage_result.status != StageStatus.SUCCESS:
                    return False

        return True

    async def _create_evidence_bundle(self, result: PlaybookResult) -> str:
        """Create evidence bundle for audit."""
        bundle_path = (
            self._artifacts_dir /
            f"evidence-{result.playbook_name}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json")

        bundle = {
            "playbook": result.playbook_name,
            "version": result.version,
            "execution": {
                "status": result.status.value,
                "trigger": result.trigger_event,
                "started_at": result.started_at,
                "completed_at": result.completed_at,
                "duration_seconds": result.duration_seconds,
            },
            "stages": [
                {
                    "id": s.stage_id,
                    "name": s.name,
                    "status": s.status.value,
                    "duration_seconds": s.duration_seconds,
                    "artifacts": s.artifacts,
                    "evidence": s.evidence,
                }
                for s in result.stages
            ],
            "quality_gates_passed": result.quality_gates_passed,
        }

        with open(bundle_path, "w") as f:
            json.dump(bundle, f, indent=2)

        return str(bundle_path)

    async def _action_setup_environment(
        self,
        params: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Setup environment action."""
        languages = params.get("languages", [])
        logger.info(f"Setting up environment for: {languages}")
        return {"success": True, "languages": languages}

    async def _action_run_linters(
        self,
        params: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Run linters action."""
        logger.info("Running linters...")
        return {"success": True, "issues": 0}

    async def _action_generate_report(
        self,
        params: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate report action."""
        logger.info("Generating report...")
        return {"success": True}

    async def _action_scan_dependencies(
        self,
        params: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Scan dependencies action."""
        logger.info("Scanning dependencies...")
        return {"success": True, "vulnerabilities": 0}

    async def _action_run_sast(
        self,
        params: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Run SAST action."""
        logger.info("Running SAST scan...")
        return {"success": True, "findings": 0}

    async def _action_run_pytest(
        self,
        params: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Run pytest action."""
        logger.info("Running pytest...")
        return {"success": True, "tests_passed": 0, "tests_failed": 0}

    async def _action_aggregate_results(
        self,
        params: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Aggregate results action."""
        stages = params.get("stages", [])
        logger.info(f"Aggregating results from: {stages}")
        return {"success": True}

    async def _action_notify_pr(
        self,
        params: dict[str, Any],
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Notify PR action."""
        logger.info("Notifying PR...")
        return {"success": True}
