"""Internal retrieval system placeholder for MNGA dual-path reasoning."""


class InternalRetriever:
    """Stub internal retriever for governance scaffolding."""

    def retrieve(self, query: str) -> list:
        return []


class InternalRetrievalEngine(InternalRetriever):
    """Compatibility alias expected by governance checks."""
"""Compatibility wrapper for the internal retrieval engine."""

from typing import List

try:
    from .._loader import load_impl

    _impl = load_impl(
        "internal/retrieval.py", "ecosystem.reasoning.dual_path.internal.retrieval.impl"
    )
    InternalRetrievalEngine = _impl.InternalRetrievalEngine
    InternalRetrievalResult = getattr(_impl, "InternalRetrievalResult", None)
except Exception:  # pragma: no cover - fallback when implementation is missing

    class InternalRetrievalResult:
        """Minimal fallback result when implementation is unavailable."""

        def __init__(self, content: str = "", source: str = "", confidence: float = 0.0):
            self.content = content
            self.source = source
            self.confidence = confidence

        def to_dict(self):
            return {
                "content": self.content,
                "source": self.source,
                "confidence": self.confidence,
            }

    class InternalRetrievalEngine:
        """Fallback retrieval engine that returns no results."""

        def __init__(self, *args, **kwargs):
            self.unavailable = True

        def search(self, query: str, top_k: int = 5, sources=None) -> List[InternalRetrievalResult]:
            return []

        def retrieve(self, context):
            return self.search("", top_k=0)


__all__ = ["InternalRetrievalEngine", "InternalRetrievalResult"]
