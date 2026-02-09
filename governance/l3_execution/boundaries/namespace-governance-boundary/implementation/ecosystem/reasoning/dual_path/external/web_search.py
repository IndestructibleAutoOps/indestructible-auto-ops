"""Compatibility wrapper for the external web search module."""

try:
    from .._loader import load_impl

    _impl = load_impl(
        "external/web_search.py",
        "ecosystem.reasoning.dual_path.external.web_search.impl",
    )
    WebSearch = _impl.WebSearch
except Exception:  # pragma: no cover - fallback when implementation is missing

    class WebSearch:
        """Fallback web search placeholder."""

        def __init__(self, *args, **kwargs):
            self.unavailable = True

        def search(self, query: str):
            return []


__all__ = ["WebSearch"]
