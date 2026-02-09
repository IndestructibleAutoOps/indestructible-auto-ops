"""Compatibility wrapper for the arbitration rule engine."""

try:
    from .._loader import load_impl

    _impl = load_impl(
        "arbitration/rule_engine.py",
        "ecosystem.reasoning.dual_path.arbitration.rule_engine.impl",
    )
    RuleEngine = _impl.RuleEngine
except Exception:  # pragma: no cover - fallback when implementation is missing

    class RuleEngine:
        """Fallback rule engine with no rules."""

        def __init__(self, *args, **kwargs):
            self.unavailable = True

        def evaluate(self, *_args, **_kwargs):
            return []


__all__ = ["RuleEngine"]
