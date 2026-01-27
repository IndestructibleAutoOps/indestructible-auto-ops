"""
Vector Search: High-performance semantic search with Redis Stack.

This module provides vector search capabilities including query building,
execution, and result processing.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module research/agent-memory-cache/implementation
@gl-semantic-anchor GL-00-IMPL_VECTOR_SEARCH
@gl-evidence-required false
GL Unified Charter Activated
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

try:
    from redis.commands.search.query import Query
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


logger = logging.getLogger(__name__)


# =============================================================================
# Data Models
# =============================================================================


class FilterOperator(Enum):
    """Operators for filter conditions."""
    EQ = "=="
    NEQ = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    IN = "@"
    CONTAINS = "*"


@dataclass
class FilterCondition:
    """Filter condition for vector search."""
    field: str
    operator: Union[FilterOperator, str]
    value: Any
    
    def __post_init__(self):
        if isinstance(self.operator, str):
            self.operator = FilterOperator(self.operator)
    
    def to_redis_query(self) -> str:
        """Convert to Redis search query syntax."""
        op = self.operator.value
        
        if self.operator == FilterOperator.IN:
            if isinstance(self.value, (list, tuple)):
                values = "|".join(str(v) for v in self.value)
                return f"@{self.field}:{{{values}}}"
            return f"@{self.field}:{{{self.value}}}"
        
        if self.operator == FilterOperator.CONTAINS:
            return f"@{self.field}:{self.value}"
        
        if self.operator in [FilterOperator.GT, FilterOperator.GTE, 
                           FilterOperator.LT, FilterOperator.LTE]:
            return f"@{self.field}:[{self.value} +inf]"
        
        return f"@{self.field}:{op}{self.value}"


@dataclass
class VectorSearchQuery:
    """Vector search query configuration."""
    vector: List[float]
    top_k: int = 10
    min_score: float = 0.0
    
    # Filters
    filters: List[FilterCondition] = field(default_factory=list)
    return_fields: List[str] = field(default_factory=list)
    
    # Query options
    dialect: int = 2
    hybrid_search: bool = False
    hybrid_alpha: float = 0.5
    
    def __post_init__(self):
        if not self.return_fields:
            self.return_fields = ["content", "importance", "timestamp"]
    
    def add_filter(self, field: str, operator: Union[FilterOperator, str], value: Any):
        """Add a filter condition."""
        self.filters.append(FilterCondition(field, operator, value))
    
    def build_redis_query(self) -> str:
        """Build Redis search query string."""
        # Build filter query
        filter_parts = []
        for condition in self.filters:
            filter_parts.append(condition.to_redis_query())
        
        filter_query = " ".join(filter_parts) if filter_parts else "*"
        
        # For hybrid search, include full-text search
        if self.hybrid_search and self.filters:
            return f"({filter_query})=>[KNN {self.top_k} @vector $vector AS score]"
        else:
            return f"=>[KNN {self.top_k} @vector $vector AS score]"


@dataclass
class SearchResult:
    """Vector search result."""
    id: str
    score: float
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_redis_result(cls, result: Any) -> "SearchResult":
        """Create SearchResult from Redis result."""
        doc_id = result.id
        payload = result.payload
        score = result.get("score", 0.0)
        
        # Extract content
        content = payload.get("content", "")
        
        # Extract metadata
        metadata = {
            "importance": float(payload.get("importance", 0)),
            "timestamp": float(payload.get("timestamp", 0)),
        }
        
        for key, value in payload.items():
            if key.startswith("metadata_"):
                metadata[key[9:]] = value
        
        return cls(
            id=doc_id,
            score=score,
            content=content,
            metadata=metadata
        )


# =============================================================================
# Vector Search Executor
# =============================================================================


class VectorSearchExecutor:
    """Executes vector search queries."""
    
    def __init__(
        self,
        redis_client,
        index_name: str,
        vector_field: str = "vector"
    ):
        """
        Initialize vector search executor.
        
        Args:
            redis_client: Redis client instance
            index_name: Name of vector index
            vector_field: Name of vector field
        """
        self.client = redis_client
        self.index_name = index_name
        self.vector_field = vector_field
    
    def search(
        self,
        query: VectorSearchQuery,
        vector_as_bytes: bool = True
    ) -> List[SearchResult]:
        """
        Execute vector search.
        
        Args:
            query: Vector search query
            vector_as_bytes: Whether vector is in bytes format
            
        Returns:
            List of search results
        """
        if not REDIS_AVAILABLE:
            raise ImportError("Redis package is required")
        
        try:
            # Build Redis query
            redis_query = query.build_redis_query()
            
            # Create Query object
            q = Query(redis_query)
            q.return_fields(*query.return_fields)
            q.return_fields("score")
            q.paging(0, query.top_k)
            q.dialect(query.dialect)
            
            # Convert vector to bytes if needed
            if vector_as_bytes:
                import struct
                vector_bytes = struct.pack(f"{len(query.vector)}f", *query.vector)
            else:
                vector_bytes = query.vector
            
            # Execute search
            results = self.client.ft(self.index_name).search(
                q,
                query_params={"vector": vector_bytes}
            )
            
            # Process results
            search_results = []
            for doc in results.docs:
                result = SearchResult(
                    id=doc.id,
                    score=float(doc.get("score", 0.0)),
                    content=doc.get("content", ""),
                    metadata={
                        "importance": float(doc.get("importance", 0)),
                        "timestamp": float(doc.get("timestamp", 0)),
                    }
                )
                
                # Filter by min_score
                if result.score >= query.min_score:
                    search_results.append(result)
            
            logger.debug(f"Search returned {len(search_results)} results")
            return search_results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            raise
    
    def search_similar(
        self,
        vector: List[float],
        top_k: int = 10,
        min_score: float = 0.0,
        filters: Optional[List[FilterCondition]] = None
    ) -> List[SearchResult]:
        """
        Search for similar vectors.
        
        Args:
            vector: Query vector
            top_k: Number of results to return
            min_score: Minimum similarity score
            filters: Optional filter conditions
            
        Returns:
            List of search results
        """
        query = VectorSearchQuery(
            vector=vector,
            top_k=top_k,
            min_score=min_score,
            filters=filters or []
        )
        
        return self.search(query)


# =============================================================================
# Semantic Memory Search
# =============================================================================


class SemanticMemorySearch:
    """High-level semantic search interface for memories."""
    
    def __init__(
        self,
        redis_client,
        index_name: str = "memory-index",
        embedding_service=None
    ):
        """
        Initialize semantic memory search.
        
        Args:
            redis_client: Redis client instance
            index_name: Name of memory index
            embedding_service: Embedding service for query vectors
        """
        self.client = redis_client
        self.index_name = index_name
        self.embedding_service = embedding_service
        self.executor = VectorSearchExecutor(redis_client, index_name)
    
    async def search(
        self,
        query_text: str,
        top_k: int = 5,
        min_score: float = 0.0,
        memory_type: Optional[str] = None,
        min_importance: Optional[float] = None
    ) -> List[SearchResult]:
        """
        Search memories semantically.
        
        Args:
            query_text: Query text
            top_k: Number of results
            min_score: Minimum similarity score
            memory_type: Filter by memory type
            min_importance: Minimum importance threshold
            
        Returns:
            List of search results
        """
        # Generate query vector
        if self.embedding_service:
            result = await self.embedding_service.embed(query_text)
            vector = result.embedding
        else:
            raise ValueError("Embedding service is required for semantic search")
        
        # Build filters
        filters = []
        if memory_type:
            filters.append(
                FilterCondition("metadata_type", FilterOperator.EQ, memory_type)
            )
        if min_importance is not None:
            filters.append(
                FilterCondition("importance", FilterOperator.GTE, min_importance)
            )
        
        # Execute search
        return self.executor.search_similar(
            vector=vector,
            top_k=top_k,
            min_score=min_score,
            filters=filters
        )
    
    async def find_similar_memories(
        self,
        content: str,
        threshold: float = 0.85,
        top_k: int = 10
    ) -> List[SearchResult]:
        """
        Find memories similar to given content.
        
        Args:
            content: Content to find similar memories for
            threshold: Similarity threshold
            top_k: Maximum number of results
            
        Returns:
            List of similar memories
        """
        return await self.search(
            query_text=content,
            top_k=top_k,
            min_score=threshold
        )


# =============================================================================
# Factory Functions
# =============================================================================


def create_vector_search_executor(
    redis_client,
    index_name: str,
    vector_field: str = "vector"
) -> VectorSearchExecutor:
    """
    Create vector search executor.
    
    Args:
        redis_client: Redis client instance
        index_name: Name of vector index
        vector_field: Name of vector field
        
    Returns:
        VectorSearchExecutor instance
    """
    return VectorSearchExecutor(redis_client, index_name, vector_field)


# =============================================================================
# Example Usage
# =============================================================================


async def example_usage():
    """Example usage of vector search."""
    
    import redis
    from embedding_service import EmbeddingService
    
    # Connect to Redis
    client = redis.Redis(host="localhost", port=6379)
    
    # Create embedding service
    embedding_svc = EmbeddingService(provider="openai", api_key="your-key")
    
    # Create semantic search
    semantic_search = SemanticMemorySearch(
        redis_client=client,
        embedding_service=embedding_svc
    )
    
    # Search memories
    results = await semantic_search.search(
        query_text="programming preferences",
        top_k=5,
        min_score=0.7
    )
    
    for result in results:
        print(f"[{result.score:.2f}] {result.content}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())