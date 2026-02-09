"""Index builder placeholder for MNGA internal reasoning path."""


class IndexBuilder:
    """Stub index builder."""

    def build(self, documents: list) -> None:
        return None
"""Compatibility wrapper for the internal index builder."""

try:
    from .._loader import load_impl

    _impl = load_impl(
        "internal/index_builder.py",
        "ecosystem.reasoning.dual_path.internal.index_builder.impl",
    )
    IndexBuilder = _impl.IndexBuilder
except Exception:  # pragma: no cover - fallback when implementation is missing

    class IndexBuilder:
        """Fallback index builder placeholder."""

        def __init__(self, *args, **kwargs):
            self.unavailable = True

        def build(self):
            return {"status": "unavailable"}


__all__ = ["IndexBuilder"]
