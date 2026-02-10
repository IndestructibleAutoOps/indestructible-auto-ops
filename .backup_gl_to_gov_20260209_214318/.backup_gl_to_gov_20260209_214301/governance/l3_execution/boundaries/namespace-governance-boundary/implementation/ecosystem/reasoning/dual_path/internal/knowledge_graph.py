"""Knowledge graph placeholder for MNGA internal reasoning path."""


class KnowledgeGraph:
    """Stub knowledge graph container."""

    def query(self, expression: str) -> list:
        return []
"""Compatibility wrapper for the internal knowledge graph implementation."""

try:
    from .._loader import load_impl

    _impl = load_impl(
        "internal/knowledge_graph.py",
        "ecosystem.reasoning.dual_path.internal.knowledge_graph.impl",
    )
    KnowledgeGraph = _impl.KnowledgeGraph
except Exception:  # pragma: no cover - fallback when implementation is missing

    class KnowledgeGraph:
        """Fallback knowledge graph that returns empty responses."""

        def __init__(self, *args, **kwargs):
            self.unavailable = True

        def query(self, pattern: str):
            return []


__all__ = ["KnowledgeGraph"]
