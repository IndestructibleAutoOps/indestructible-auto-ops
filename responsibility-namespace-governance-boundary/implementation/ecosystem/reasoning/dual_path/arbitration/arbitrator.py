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
