"""
Vector Search Query Builder and Executor.
Provides semantic search capabilities using Redis Stack vector search.
"""

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Union


class FilterOperator(Enum):
    """Filter operators for query building."""
    EQ = "=="
    NE = "!="
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="
    IN = "IN"
    CONTAINS = "CONTAINS"


@dataclass
class FilterCondition:
    """A single filter condition."""
    field: str
    operator: FilterOperator
    value: Union[str, int, float, list[str]]


@dataclass
class VectorSearchQuery:
    """Vector search query configuration."""
    vector: list[float]
    top_k: int = 10
    filters: list[FilterCondition] = field(default_factory=list)
    return_fields: list[str] = field(default_factory=lambda: ["content", "doc_id"])
    include_scores: bool = True
    include_vectors: bool = False
    hybrid_fields: list[str] = field(default_factory=list)  # For hybrid search
    hybrid_weight: float = 0.5  # Weight for vector vs text search


@dataclass
class SearchResult:
    """A single search result."""
    doc_id: str
    score: float
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    vector: Optional[list[float]] = None


@dataclass
class SearchResponse:
    """Search response containing results and metadata."""
    results: list[SearchResult]
    total_count: int
    query_time_ms: float
    index_name: str


class VectorSearchQueryBuilder:
    """Builder for constructing vector search queries."""

    def __init__(self):
        self._vector: Optional[list[float]] = None
        self._top_k: int = 10
        self._filters: list[FilterCondition] = []
        self._return_fields: list[str] = ["content", "doc_id"]
        self._include_scores: bool = True
        self._include_vectors: bool = False
        self._hybrid_fields: list[str] = []
        self._hybrid_weight: float = 0.5

    def with_vector(self, vector: list[float]) -> "VectorSearchQueryBuilder":
        """Set the query vector."""
        self._vector = vector
        return self

    def with_top_k(self, k: int) -> "VectorSearchQueryBuilder":
        """Set the number of results to return."""
        self._top_k = k
        return self

    def with_filter(
        self,
        field: str,
        operator: FilterOperator,
        value: Union[str, int, float, list[str]]
    ) -> "VectorSearchQueryBuilder":
        """Add a filter condition."""
        self._filters.append(FilterCondition(field, operator, value))
        return self

    def filter_eq(self, field: str, value: Union[str, int, float]) -> "VectorSearchQueryBuilder":
        """Add equality filter."""
        return self.with_filter(field, FilterOperator.EQ, value)

    def filter_ne(self, field: str, value: Union[str, int, float]) -> "VectorSearchQueryBuilder":
        """Add not-equal filter."""
        return self.with_filter(field, FilterOperator.NE, value)

    def filter_gt(self, field: str, value: Union[int, float]) -> "VectorSearchQueryBuilder":
        """Add greater-than filter."""
        return self.with_filter(field, FilterOperator.GT, value)

    def filter_gte(self, field: str, value: Union[int, float]) -> "VectorSearchQueryBuilder":
        """Add greater-than-or-equal filter."""
        return self.with_filter(field, FilterOperator.GE, value)

    def filter_lt(self, field: str, value: Union[int, float]) -> "VectorSearchQueryBuilder":
        """Add less-than filter."""
        return self.with_filter(field, FilterOperator.LT, value)

    def filter_lte(self, field: str, value: Union[int, float]) -> "VectorSearchQueryBuilder":
        """Add less-than-or-equal filter."""
        return self.with_filter(field, FilterOperator.LE, value)

    def filter_in(self, field: str, values: list[str]) -> "VectorSearchQueryBuilder":
        """Add in-list filter."""
        return self.with_filter(field, FilterOperator.IN, values)

    def filter_contains(self, field: str, value: str) -> "VectorSearchQueryBuilder":
        """Add contains filter for text fields."""
        return self.with_filter(field, FilterOperator.CONTAINS, value)

    def with_return_fields(self, fields: list[str]) -> "VectorSearchQueryBuilder":
        """Set fields to return in results."""
        self._return_fields = fields
        return self

    def with_scores(self, include: bool = True) -> "VectorSearchQueryBuilder":
        """Include similarity scores in results."""
        self._include_scores = include
        return self

    def with_vectors(self, include: bool = True) -> "VectorSearchQueryBuilder":
        """Include vectors in results."""
        self._include_vectors = include
        return self

    def with_hybrid_search(
        self,
        text_fields: list[str],
        weight: float = 0.5
    ) -> "VectorSearchQueryBuilder":
        """Enable hybrid search with text fields."""
        self._hybrid_fields = text_fields
        self._hybrid_weight = weight
        return self

    def build(self) -> VectorSearchQuery:
        """Build the search query."""
        if self._vector is None:
            raise ValueError("Query vector is required")
        
        return VectorSearchQuery(
            vector=self._vector,
            top_k=self._top_k,
            filters=self._filters,
            return_fields=self._return_fields,
            include_scores=self._include_scores,
            include_vectors=self._include_vectors,
            hybrid_fields=self._hybrid_fields,
            hybrid_weight=self._hybrid_weight
        )


class VectorSearchExecutor:
    """
    Executes vector search queries against Redis Stack.
    """

    def __init__(
        self,
        redis_client: Any,
        default_index: str = "idx:memory",
        vector_field: str = "embedding"
    ):
        """
        Initialize the search executor.
        
        Args:
            redis_client: Redis client with RediSearch support
            default_index: Default index name for searches
            vector_field: Name of the vector field in documents
        """
        self._client = redis_client
        self._default_index = default_index
        self._vector_field = vector_field

    def _build_filter_string(self, filters: list[FilterCondition]) -> str:
        """Build Redis filter string from conditions."""
        if not filters:
            return "*"
        
        filter_parts = []
        for f in filters:
            if f.operator == FilterOperator.EQ:
                if isinstance(f.value, str):
                    filter_parts.append(f"@{f.field}:{{{f.value}}}")
                else:
                    filter_parts.append(f"@{f.field}:[{f.value} {f.value}]")
            elif f.operator == FilterOperator.NE:
                if isinstance(f.value, str):
                    filter_parts.append(f"-@{f.field}:{{{f.value}}}")
                else:
                    filter_parts.append(f"-@{f.field}:[{f.value} {f.value}]")
            elif f.operator == FilterOperator.GT:
                filter_parts.append(f"@{f.field}:[({f.value} +inf]")
            elif f.operator == FilterOperator.GE:
                filter_parts.append(f"@{f.field}:[{f.value} +inf]")
            elif f.operator == FilterOperator.LT:
                filter_parts.append(f"@{f.field}:[-inf ({f.value}]")
            elif f.operator == FilterOperator.LE:
                filter_parts.append(f"@{f.field}:[-inf {f.value}]")
            elif f.operator == FilterOperator.IN:
                if isinstance(f.value, list):
                    values = "|".join(str(v) for v in f.value)
                    filter_parts.append(f"@{f.field}:{{{values}}}")
            elif f.operator == FilterOperator.CONTAINS:
                filter_parts.append(f"@{f.field}:{f.value}")
        
        return " ".join(filter_parts) if filter_parts else "*"

    async def search(
        self,
        query: VectorSearchQuery,
        index_name: Optional[str] = None
    ) -> SearchResponse:
        """
        Execute a vector search query.
        
        Args:
            query: The search query
            index_name: Optional index name (uses default if not provided)
            
        Returns:
            Search response with results
        """
        import time
        start_time = time.time()
        
        idx = index_name or self._default_index
        filter_str = self._build_filter_string(query.filters)
        
        # Build return fields
        return_fields = list(query.return_fields)
        if query.include_scores:
            return_fields.append("__vector_score")
        if query.include_vectors:
            return_fields.append(self._vector_field)

        # Convert vector to bytes for Redis
        vector_bytes = self._vector_to_bytes(query.vector)
        
        # Build KNN query
        knn_query = (
            f"({filter_str})=>[KNN {query.top_k} @{self._vector_field} $vec AS __vector_score]"
        )
        
        # Execute search
        try:
            result = await self._client.ft(idx).search(
                knn_query,
                query_params={"vec": vector_bytes}
            )
        except Exception as e:
            # Fallback to raw command if search method fails
            cmd_parts = [
                "FT.SEARCH", idx, knn_query,
                "PARAMS", "2", "vec", vector_bytes,
                "RETURN", str(len(return_fields)), *return_fields,
                "SORTBY", "__vector_score",
                "DIALECT", "2"
            ]
            result = await self._client.execute_command(*cmd_parts)

        # Parse results
        results = self._parse_results(result, query)
        
        query_time = (time.time() - start_time) * 1000
        
        return SearchResponse(
            results=results,
            total_count=len(results),
            query_time_ms=query_time,
            index_name=idx
        )

    async def search_by_text(
        self,
        text: str,
        embedding_service: Any,
        top_k: int = 10,
        filters: Optional[list[FilterCondition]] = None,
        index_name: Optional[str] = None
    ) -> SearchResponse:
        """
        Search by text (generates embedding automatically).
        
        Args:
            text: Text to search for
            embedding_service: Service to generate embeddings
            top_k: Number of results
            filters: Optional filters
            index_name: Optional index name
            
        Returns:
            Search response
        """
        # Generate embedding for query text
        vector = await embedding_service.embed(text)
        
        # Build query
        builder = VectorSearchQueryBuilder().with_vector(vector).with_top_k(top_k)
        
        if filters:
            for f in filters:
                builder.with_filter(f.field, f.operator, f.value)
        
        query = builder.build()
        return await self.search(query, index_name)

    async def similarity_search(
        self,
        vector: list[float],
        top_k: int = 10,
        min_score: float = 0.0,
        index_name: Optional[str] = None
    ) -> list[SearchResult]:
        """
        Simple similarity search returning results above minimum score.
        
        Args:
            vector: Query vector
            top_k: Number of results
            min_score: Minimum similarity score (0-1)
            index_name: Optional index name
            
        Returns:
            List of search results
        """
        query = (
            VectorSearchQueryBuilder()
            .with_vector(vector)
            .with_top_k(top_k)
            .with_scores(True)
            .build()
        )
        
        response = await self.search(query, index_name)
        
        # Filter by minimum score
        return [r for r in response.results if r.score >= min_score]

    def _vector_to_bytes(self, vector: list[float]) -> bytes:
        """Convert vector to bytes for Redis."""
        import struct
        return struct.pack(f"{len(vector)}f", *vector)

    def _parse_results(
        self,
        raw_result: Any,
        query: VectorSearchQuery
    ) -> list[SearchResult]:
        """Parse raw Redis results into SearchResult objects."""
        results = []
        
        # Handle different result formats
        if hasattr(raw_result, 'docs'):
            # redis-py search result format
            for doc in raw_result.docs:
                doc_dict = doc.__dict__ if hasattr(doc, '__dict__') else dict(doc)
                
                score = 1.0 - float(doc_dict.get('__vector_score', 0))
                content = doc_dict.get('content', '')
                doc_id = doc_dict.get('doc_id', doc_dict.get('id', ''))
                
                metadata = {
                    k: v for k, v in doc_dict.items()
                    if k not in ['content', 'doc_id', 'id', '__vector_score', 'embedding']
                }
                
                vector = None
                if query.include_vectors and self._vector_field in doc_dict:
                    vector = doc_dict[self._vector_field]
                
                results.append(SearchResult(
                    doc_id=doc_id,
                    score=score,
                    content=content,
                    metadata=metadata,
                    vector=vector
                ))
        elif isinstance(raw_result, (list, tuple)):
            # Raw command result format
            total = raw_result[0] if raw_result else 0
            i = 1
            while i < len(raw_result):
                doc_id = raw_result[i] if isinstance(raw_result[i], str) else raw_result[i].decode()
                i += 1
                
                if i < len(raw_result) and isinstance(raw_result[i], (list, tuple)):
                    fields = raw_result[i]
                    doc_dict = {}
                    for j in range(0, len(fields), 2):
                        key = fields[j] if isinstance(fields[j], str) else fields[j].decode()
                        value = fields[j + 1]
                        if isinstance(value, bytes):
                            value = value.decode()
                        doc_dict[key] = value
                    
                    score = 1.0 - float(doc_dict.get('__vector_score', 0))
                    content = doc_dict.get('content', '')
                    
                    metadata = {
                        k: v for k, v in doc_dict.items()
                        if k not in ['content', '__vector_score', 'embedding']
                    }
                    
                    results.append(SearchResult(
                        doc_id=doc_id,
                        score=score,
                        content=content,
                        metadata=metadata
                    ))
                    i += 1
        
        return results


class SemanticMemorySearch:
    """
    High-level semantic memory search interface.
    Combines embedding service and vector search for easy memory retrieval.
    """

    def __init__(
        self,
        redis_client: Any,
        embedding_service: Any,
        index_name: str = "idx:memory"
    ):
        """
        Initialize semantic memory search.
        
        Args:
            redis_client: Redis client
            embedding_service: Embedding service
            index_name: Index name for memory storage
        """
        self._executor = VectorSearchExecutor(redis_client, index_name)
        self._embedding_service = embedding_service
        self._index_name = index_name

    async def search(
        self,
        query: str,
        top_k: int = 10,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        min_importance: Optional[float] = None,
        time_range: Optional[tuple[float, float]] = None
    ) -> list[SearchResult]:
        """
        Search memories semantically.
        
        Args:
            query: Search query text
            top_k: Number of results
            agent_id: Filter by agent ID
            session_id: Filter by session ID
            memory_type: Filter by memory type
            min_importance: Minimum importance score
            time_range: Tuple of (start_timestamp, end_timestamp)
            
        Returns:
            List of matching memories
        """
        # Build filters
        filters = []
        
        if agent_id:
            filters.append(FilterCondition("agent_id", FilterOperator.EQ, agent_id))
        if session_id:
            filters.append(FilterCondition("session_id", FilterOperator.EQ, session_id))
        if memory_type:
            filters.append(FilterCondition("type", FilterOperator.EQ, memory_type))
        if min_importance is not None:
            filters.append(FilterCondition("importance", FilterOperator.GE, min_importance))
        if time_range:
            filters.append(FilterCondition("timestamp", FilterOperator.GE, time_range[0]))
            filters.append(FilterCondition("timestamp", FilterOperator.LE, time_range[1]))

        # Execute search
        response = await self._executor.search_by_text(
            text=query,
            embedding_service=self._embedding_service,
            top_k=top_k,
            filters=filters,
            index_name=self._index_name
        )
        
        return response.results

    async def find_similar(
        self,
        content: str,
        top_k: int = 5,
        exclude_self: bool = True
    ) -> list[SearchResult]:
        """
        Find memories similar to given content.
        
        Args:
            content: Content to find similar memories for
            top_k: Number of results
            exclude_self: Whether to exclude exact matches
            
        Returns:
            List of similar memories
        """
        results = await self.search(content, top_k=top_k + (1 if exclude_self else 0))
        
        if exclude_self and results:
            # Remove exact match if present
            results = [r for r in results if r.score < 0.99][:top_k]
        
        return results

    async def get_context(
        self,
        query: str,
        max_tokens: int = 2000,
        agent_id: Optional[str] = None
    ) -> str:
        """
        Get relevant context for a query, formatted for LLM consumption.
        
        Args:
            query: Query to get context for
            max_tokens: Maximum tokens in context
            agent_id: Filter by agent ID
            
        Returns:
            Formatted context string
        """
        results = await self.search(query, top_k=20, agent_id=agent_id)
        
        context_parts = []
        estimated_tokens = 0
        
        for result in results:
            content = result.content
            # Rough token estimation (4 chars per token)
            content_tokens = len(content) // 4
            
            if estimated_tokens + content_tokens > max_tokens:
                break
            
            context_parts.append(f"[Score: {result.score:.2f}] {content}")
            estimated_tokens += content_tokens
        
        return "\n\n".join(context_parts)