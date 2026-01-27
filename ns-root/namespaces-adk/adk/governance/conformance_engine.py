"""
Conformance Engine: Enforces temporal and sequence-based policies.

This module uses finite-state machines for workflow conformance checking.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/governance
@gl-semantic-anchor GL-00-ADK_GOVERNAN_CONFORMANCEE
@gl-evidence-required false
GL Unified Charter Activated
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from ..observability.logging import Logger


@dataclass
class PolicyRule:
    """A policy rule."""

    rule_id: str
    description: str
    sequence: List[str]
    forbidden_transitions: List[tuple[str, str]]


class ConformanceEngine:
    """Enforces workflow conformance using FSMs."""

    def __init__(self):
        self.logger = Logger(name="governance.conformance")
        self._policies: Dict[str, PolicyRule] = {}
        # workflow_id -> current_state
        self._state_machines: Dict[str, str] = {}

    def add_policy(self, policy: PolicyRule) -> None:
        """Add a policy rule."""
        self._policies[policy.rule_id] = policy

    def check_conformance(
        self, workflow_id: str, current_step: str, next_step: str
    ) -> tuple[bool, Optional[str]]:
        """Check if transition conforms to policies."""
        self._state_machines.get(workflow_id, "")

        for policy in self._policies.values():
            # Check forbidden transitions
            if (current_step, next_step) in policy.forbidden_transitions:
                return False, f"Forbidden transition: {current_step} -> {next_step}"

        # Update state
        self._state_machines[workflow_id] = next_step
        return True, None

    def reset_workflow(self, workflow_id: str) -> None:
        """Reset workflow state."""
        if workflow_id in self._state_machines:
            del self._state_machines[workflow_id]
