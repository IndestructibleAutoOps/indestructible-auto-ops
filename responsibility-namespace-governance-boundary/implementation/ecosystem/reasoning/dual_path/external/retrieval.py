"""Compatibility wrapper for the external retrieval engine."""

try:
    from .._loader import load_impl

    _impl = load_impl(
        "external/retrieval.py", "ecosystem.reasoning.dual_path.external.retrieval.impl"
    )
    ExternalRetrievalEngine = _impl.ExternalRetrievalEngine
    ExternalRetrievalResult = getattr(_impl, "ExternalRetrievalResult", None)
except Exception:  # pragma: no cover - fallback when implementation is missing

    class ExternalRetrievalResult:
        """Minimal fallback result when implementation is unavailable."""

        def __init__(self, content: str = "", source: str = "", confidence: float = 0.0):
            self.content = content
            self.source = source
            self.confidence = confidence

    class ExternalRetrievalEngine:
        """Fallback retrieval engine that returns no results."""

        def __init__(self, *args, **kwargs):
            self.unavailable = True

        def search(self, query: str, top_k: int = 5):
            return []


__all__ = ["ExternalRetrievalEngine", "ExternalRetrievalResult"]
