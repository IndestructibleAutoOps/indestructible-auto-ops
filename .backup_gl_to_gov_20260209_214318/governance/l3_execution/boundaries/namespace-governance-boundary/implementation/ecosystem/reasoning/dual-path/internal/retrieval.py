"""
Internal Retrieval Engine
Combines vector-based semantic search with knowledge graph queries
"""

import os
import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

# Import simple_yaml for zero-dependency YAML parsing
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from utils.simple_yaml import safe_load


class InternalRetrievalResult:
    """Internal retrieval result with metadata"""

    def __init__(
        self,
        content: str,
        source: str,
        confidence: float,
        file_path: Optional[str] = None,
        line_range: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ):
        self.content = content
        self.source = source
        self.confidence = confidence
        self.file_path = file_path
        self.line_range = line_range
        self.metadata = metadata or {}

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "content": self.content,
            "source": self.source,
            "confidence": self.confidence,
            "file_path": self.file_path,
            "line_range": self.line_range,
            "metadata": self.metadata,
            "checksum": hashlib.sha256(self.content.encode()).hexdigest()[:16],
        }


class InternalRetrievalEngine:
    """Internal knowledge retrieval engine"""

    def __init__(self, config=None):
        """Initialize internal retrieval engine"""
        # Handle both dict config and string path
        if isinstance(config, dict):
            self.config = config
        elif isinstance(config, str):
            self.config = self._load_config(config)
        elif config is None:
            self.config = self._load_config(
                "ecosystem/contracts/reasoning/dual_path_spec.yaml"
            )
        else:
            self.config = {}

        # Get internal_retrieval config or use defaults
        if "spec" in self.config and "internal_retrieval" in self.config["spec"]:
            self.internal_config = self.config["spec"]["internal_retrieval"]
        else:
            self.internal_config = {}

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        return {"spec": {"internal_retrieval": {}}}

    def _generate_checksum(self, content: str) -> str:
        """Generate SHA-256 checksum for content"""
        return hashlib.sha256(content.encode()).hexdigest()

    def retrieve(self, context) -> List:
        """Retrieve based on context (supports RetrievalContext or dict)"""
        if hasattr(context, "query"):
            # RetrievalContext object
            query = context.query
            top_k = context.max_results
            sources = context.sources
        elif isinstance(context, dict):
            # Dict context
            query = context.get("query", "")
            top_k = context.get("max_results", 5)
            sources = context.get("sources")
        else:
            raise ValueError(f"Invalid context type: {type(context)}")

        return self.search(query, top_k=top_k, sources=sources)

    def search(
        self, query: str, top_k: int = 5, sources: Optional[List[str]] = None
    ) -> List[InternalRetrievalResult]:
        """
        Search internal knowledge base

        Args:
            query: Search query
            top_k: Number of results to return
            sources: Filter by source types (code, docs, governance, history)

        Returns:
            List of InternalRetrievalResult
        """
        # Vector-based semantic search (mock implementation)
        vector_results = self._vector_search(query, top_k)

        # Knowledge graph context (mock implementation)
        graph_results = self._graph_search(query, top_k // 2)

        # Combine and rank results
        combined_results = self._combine_results(vector_results, graph_results, top_k)

        # Filter by sources if specified
        if sources:
            combined_results = [r for r in combined_results if r.source in sources]

        return combined_results[:top_k]

    def _vector_search(self, query: str, top_k: int) -> List[InternalRetrievalResult]:
        """
        Vector-based semantic search
        Mock implementation - would integrate with ChromaDB in production
        """
        # Mock results based on query keywords
        mock_results = []

        # Search code files
        if "python" in query.lower() or "async" in query.lower():
            mock_results.append(
                InternalRetrievalResult(
                    content="def process_task(task):\n    import asyncio\n    result = await asyncio.create_task(execute_task(task))\n    return result",
                    source="code",
                    confidence=0.92,
                    file_path="gov-execution-runtime/src/worker.py",
                    line_range="45-48",
                    metadata={"language": "python", "function": "process_task"},
                )
            )

        # Search documentation
        if "api" in query.lower() or "service" in query.lower():
            mock_results.append(
                InternalRetrievalResult(
                    content="Platform services provide core infrastructure for all applications",
                    source="documentation",
                    confidence=0.88,
                    file_path="ecosystem/docs/platform-services.md",
                    metadata={"doc_type": "architecture"},
                )
            )

        # Search governance contracts
        if "governance" in query.lower() or "policy" in query.lower():
            mock_results.append(
                InternalRetrievalResult(
                    content="All platforms must follow GL naming convention: gl.{domain}.{capability}-platform",
                    source="governance",
                    confidence=0.95,
                    file_path="ecosystem/contracts/governance/gov-platforms.yaml",
                    metadata={"version": "v3.0.0", "section": "platform-definition"},
                )
            )

        return mock_results[:top_k]

    def _graph_search(self, query: str, top_k: int) -> List[InternalRetrievalResult]:
        """
        Knowledge graph search
        Mock implementation - would integrate with Neo4j in production
        """
        # Mock results based on query context
        mock_results = []

        # Find related symbols and dependencies
        if "worker" in query.lower():
            mock_results.append(
                InternalRetrievalResult(
                    content="process_task calls execute_task which depends on task_queue",
                    source="knowledge_graph",
                    confidence=0.85,
                    metadata={"graph_layer": "L2_call_graph", "symbol": "process_task"},
                )
            )

        return mock_results[:top_k]

    def _combine_results(
        self, vector_results: List, graph_results: List, top_k: int
    ) -> List[InternalRetrievalResult]:
        """Combine vector and graph results with deduplication"""
        seen_checksums = set()
        combined = []

        for result in vector_results + graph_results:
            checksum = self._generate_checksum(result.content)
            if checksum not in seen_checksums:
                combined.append(result)
                seen_checksums.add(checksum)

        # Sort by confidence
        combined.sort(key=lambda x: x.confidence, reverse=True)

        return combined[:top_k]

    def get_context(self, symbol: str, depth: int = 3) -> Dict:
        """
        Get context for a symbol from knowledge graph

        Args:
            symbol: Symbol name (function, class, variable)
            depth: Depth of context to retrieve

        Returns:
            Dictionary with context information
        """
        context = {
            "symbol": symbol,
            "definition": None,
            "callers": [],
            "callees": [],
            "related_concepts": [],
        }

        # Mock context retrieval
        if symbol == "process_task":
            context["definition"] = {
                "file": "gov-execution-runtime/src/worker.py",
                "lines": "45-48",
            }
            context["callers"] = [
                {"function": "main", "file": "gov-execution-runtime/src/main.py"}
            ]
            context["callees"] = [
                {
                    "function": "execute_task",
                    "file": "gov-execution-runtime/src/executor.py",
                },
                {"function": "asyncio.create_task", "external": True},
            ]
            context["related_concepts"] = ["task_queue", "async_execution"]

        return context

    def get_stats(self) -> Dict:
        """Get retrieval engine statistics"""
        return {
            "engine_type": "InternalRetrievalEngine",
            "config_loaded": bool(self.internal_config),
            "status": "operational",
        }

    def audit_log(
        self, actor: str, action: str, query: str, results_count: int
    ) -> Dict:
        """Generate audit log entry"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "actor": actor,
            "action": action,
            "resource": f"internal_retrieval:{query}",
            "result": {"results_count": results_count, "success": True},
            "version": "1.0.0",
            "requestId": self._generate_checksum(query)[:16],
            "correlationId": self._generate_checksum(f"{actor}:{action}")[:16],
        }


if __name__ == "__main__":
    # Test internal retrieval
    engine = InternalRetrievalEngine()

    # Test search
    results = engine.search("Python asyncio task processing", top_k=3)

    print("Internal Retrieval Results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Source: {result.source}")
        print(f"   Confidence: {result.confidence:.2f}")
        print(f"   File: {result.file_path}")
        print(f"   Content: {result.content[:100]}...")

    # Test context
    context = engine.get_context("process_task")
    print(f"\n\nContext for 'process_task':")
    print(f"  Callers: {context['callers']}")
    print(f"  Callees: {context['callees']}")

    # Audit log
    audit = engine.audit_log("test_user", "search", "Python asyncio", len(results))
    print(f"\n\nAudit Log:")
    print(json.dumps(audit, indent=2))
