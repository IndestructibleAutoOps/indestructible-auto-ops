"""Arbitrator placeholder for MNGA dual-path reasoning arbitration."""


class Arbitrator:
    """Stub arbitrator selecting between internal and external results."""

    def choose(self, internal_result, external_result):
        return internal_result if internal_result is not None else external_result
"""Compatibility wrapper for the arbitration engine."""

try:
    from .._loader import load_impl

    _impl = load_impl(
        "arbitration/arbitrator.py",
        "ecosystem.reasoning.dual_path.arbitration.arbitrator.impl",
    )
    Arbitrator = _impl.Arbitrator
    ArbitrationDecision = getattr(_impl, "ArbitrationDecision", None)
    Decision = getattr(_impl, "Decision", None)
except Exception:  # pragma: no cover - fallback when implementation is missing

    class ArbitrationDecision:
        """Fallback decision payload."""

        def __init__(self, decision: str = "unknown", reason: str = ""):
            self.decision = decision
            self.reason = reason

    class Arbitrator:
        """Fallback arbitrator that returns neutral decisions."""

        def __init__(self, *args, **kwargs):
            self.unavailable = True

        def decide(self, internal_score: float = 0.0, external_score: float = 0.0):
            return ArbitrationDecision(decision="neutral", reason="unavailable")

    Decision = ArbitrationDecision


__all__ = ["Arbitrator", "ArbitrationDecision", "Decision"]
