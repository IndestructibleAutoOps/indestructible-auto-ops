"""
Semantic Cache V2: Enhanced LLM response caching with vector search integration.

Features:
- Multi-level caching (exact match + semantic similarity)
- Adaptive TTL based on access patterns
- Query clustering for cache optimization
- Streaming response support
- Cache warming and preloading
- Detailed analytics and monitoring

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins/memory_plugins
@gl-semantic-anchor GL-00-PLUGINS_MEMORYPL_SEMCACHE_V2
@gl-evidence-required false
GL Unified Charter Activated
"""

import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Tuple, Union

from .embedding_service import EmbeddingService
from .vector_index_manager import VectorIndexManager, VectorIndexConfig, DistanceMetric
from .vector_search import VectorSearchExecutor, VectorSearchQueryBuilder, FilterOperator, FilterCondition


class CacheStrategy(Enum):
    """Cache lookup strategies."""
    EXACT_ONLY = "exact_only"
    SEMANTIC_ONLY = "semantic_only"
    HYBRID = "hybrid"  # Exact first, then semantic


class EvictionPolicy(Enum):
    """Cache eviction policies."""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time-based only
    ADAPTIVE = "adaptive"  # Combined scoring


@dataclass
class SemanticCacheConfigV2:
    """Enhanced configuration for semantic cache."""
    # Redis connection
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 1
    redis_password: Optional[str] = None
    
    # Cache settings
    prefix: str = "semcache:v2:"
    index_name: str = "idx:semcache"
    
    # Similarity settings
    similarity_threshold: float = 0.85
    exact_match_boost: float = 0.1  # Bonus score for exact hash match
    
    # TTL settings
    default_ttl: int = 3600  # 1 hour
    min_ttl: int = 300  # 5 minutes
    max_ttl: int = 604800  # 7 days
    enable_adaptive_ttl: bool = True
    ttl_hit_multiplier: float = 1.2
    ttl_decay_rate: float = 0.95
    
    # Capacity settings
    max_entries: int = 10000
    eviction_batch_size: int = 100
    eviction_policy: EvictionPolicy = EvictionPolicy.ADAPTIVE
    
    # Vector settings
    vector_dim: int = 1536
    
    # Performance settings
    enable_exact_cache: bool = True
    enable_query_normalization: bool = True
    enable_response_compression: bool = False
    compression_threshold: int = 1000  # bytes
    
    # Analytics
    enable_analytics: bool = True
    analytics_sample_rate: float = 1.0


@dataclass
class CacheEntry:
    """A cache entry with metadata."""
    id: str
    query: str
    query_hash: str
    response: str
    embedding: List[float]
    model: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    ttl: int = 3600
    importance_score: float = 1.0
    tokens_saved: int = 0


@dataclass
class CacheHit:
    """Result of a cache lookup."""
    entry: CacheEntry
    similarity: float
    is_exact_match: bool
    lookup_time_ms: float


@dataclass
class CacheStats:
    """Cache statistics."""
    total_requests: int = 0
    hits: int = 0
    misses: int = 0
    exact_hits: int = 0
    semantic_hits: int = 0
    stores: int = 0
    evictions: int = 0
    errors: int = 0
    total_tokens_saved: int = 0
    avg_similarity: float = 0.0
    avg_lookup_time_ms: float = 0.0
    
    @property
    def hit_rate(self) -> float:
        return self.hits / self.total_requests if self.total_requests > 0 else 0.0


class SemanticCacheV2:
    """
    Enhanced semantic cache with vector search integration.
    
    Provides:
    - Exact hash matching for identical queries
    - Semantic similarity search for similar queries
    - Adaptive TTL based on access patterns
    - Multiple eviction policies
    - Streaming response support
    - Comprehensive analytics
    """

    def __init__(
        self,
        redis_client: Any,
        embedding_service: EmbeddingService,
        config: Optional[SemanticCacheConfigV2] = None,
    ):
        """
        Initialize the semantic cache.
        
        Args:
            redis_client: Async Redis client
            embedding_service: Service for generating embeddings
            config: Cache configuration
        """
        self._client = redis_client
        self._embedding_service = embedding_service
        self.config = config or SemanticCacheConfigV2()
        self._logger = logging.getLogger(__name__)
        
        # Initialize components
        self._index_manager: Optional[VectorIndexManager] = None
        self._search_executor: Optional[VectorSearchExecutor] = None
        
        # Statistics
        self._stats = CacheStats()
        self._similarity_samples: List[float] = []
        self._lookup_time_samples: List[float] = []
        
        # Locks for thread safety
        self._init_lock = asyncio.Lock()
        self._eviction_lock = asyncio.Lock()
        
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize cache components and create index."""
        async with self._init_lock:
            if self._initialized:
                return
            
            # Initialize vector index manager
            self._index_manager = VectorIndexManager(self._client)
            
            # Create cache index
            index_config = VectorIndexConfig(
                name=self.config.index_name,
                prefix=self.config.prefix,
                dimension=self.config.vector_dim,
                distance_metric=DistanceMetric.COSINE,
                text_fields=["query", "response", "model"],
                tag_fields=["query_hash"],
                numeric_fields=["created_at", "last_accessed", "access_count", "ttl", "importance_score"],
            )
            
            await self._index_manager.create_index(index_config)
            
            # Initialize search executor
            self._search_executor = VectorSearchExecutor(
                redis_client=self._client,
                default_index=self.config.index_name,
                vector_field="embedding",
            )
            
            self._initialized = True
            self._logger.info("SemanticCacheV2 initialized")

    async def get(
        self,
        query: str,
        model: Optional[str] = None,
        strategy: CacheStrategy = CacheStrategy.HYBRID,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> Optional[CacheHit]:
        """
        Get cached response for a query.
        
        Args:
            query: The query to look up
            model: Optional model filter
            strategy: Cache lookup strategy
            metadata_filter: Additional metadata filters
            
        Returns:
            CacheHit if found, None otherwise
        """
        if not self._initialized:
            await self.initialize()
        
        start_time = time.time()
        self._stats.total_requests += 1
        
        try:
            # Normalize query if enabled
            normalized_query = self._normalize_query(query) if self.config.enable_query_normalization else query
            query_hash = self._hash_query(normalized_query)
            
            # Try exact match first if using hybrid strategy
            if strategy in (CacheStrategy.EXACT_ONLY, CacheStrategy.HYBRID) and self.config.enable_exact_cache:
                exact_result = await self._exact_lookup(query_hash)
                if exact_result:
                    lookup_time = (time.time() - start_time) * 1000
                    self._stats.hits += 1
                    self._stats.exact_hits += 1
                    await self._update_access(exact_result)
                    
                    return CacheHit(
                        entry=exact_result,
                        similarity=1.0,
                        is_exact_match=True,
                        lookup_time_ms=lookup_time,
                    )
            
            # Semantic search
            if strategy in (CacheStrategy.SEMANTIC_ONLY, CacheStrategy.HYBRID):
                semantic_result = await self._semantic_lookup(
                    query=normalized_query,
                    model=model,
                    metadata_filter=metadata_filter,
                )
                
                if semantic_result:
                    entry, similarity = semantic_result
                    lookup_time = (time.time() - start_time) * 1000
                    self._stats.hits += 1
                    self._stats.semantic_hits += 1
                    await self._update_access(entry)
                    
                    # Track analytics
                    self._track_similarity(similarity)
                    self._track_lookup_time(lookup_time)
                    
                    return CacheHit(
                        entry=entry,
                        similarity=similarity,
                        is_exact_match=False,
                        lookup_time_ms=lookup_time,
                    )
            
            # Cache miss
            self._stats.misses += 1
            return None
            
        except Exception as e:
            self._stats.errors += 1
            self._logger.error(f"Cache get error: {e}")
            return None

    async def set(
        self,
        query: str,
        response: str,
        model: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None,
        tokens_used: int = 0,
    ) -> str:
        """
        Store a query-response pair in cache.
        
        Args:
            query: The query
            response: The response to cache
            model: Model identifier
            metadata: Additional metadata
            ttl: Time-to-live in seconds
            tokens_used: Number of tokens in response
            
        Returns:
            Cache entry ID
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            # Normalize and hash query
            normalized_query = self._normalize_query(query) if self.config.enable_query_normalization else query
            query_hash = self._hash_query(normalized_query)
            
            # Generate embedding
            embedding = await self._embedding_service.embed(normalized_query)
            
            # Create entry
            entry_id = f"{query_hash[:8]}_{int(time.time() * 1000) % 100000}"
            entry_ttl = ttl or self.config.default_ttl
            
            entry = CacheEntry(
                id=entry_id,
                query=query,
                query_hash=query_hash,
                response=response,
                embedding=embedding,
                model=model,
                metadata=metadata or {},
                ttl=entry_ttl,
                tokens_saved=tokens_used,
            )
            
            # Store in Redis
            await self._store_entry(entry)
            
            # Update stats
            self._stats.stores += 1
            self._stats.total_tokens_saved += tokens_used
            
            # Check if eviction needed
            await self._maybe_evict()
            
            return entry_id
            
        except Exception as e:
            self._stats.errors += 1
            self._logger.error(f"Cache set error: {e}")
            raise

    async def invalidate(
        self,
        query: Optional[str] = None,
        entry_id: Optional[str] = None,
        model: Optional[str] = None,
    ) -> int:
        """
        Invalidate cache entries.
        
        Args:
            query: Invalidate by query (exact match)
            entry_id: Invalidate by entry ID
            model: Invalidate all entries for a model
            
        Returns:
            Number of entries invalidated
        """
        count = 0
        
        if entry_id:
            key = f"{self.config.prefix}{entry_id}"
            if await self._client.delete(key):
                count += 1
        
        if query:
            query_hash = self._hash_query(self._normalize_query(query))
            async for key in self._client.scan_iter(f"{self.config.prefix}*"):
                try:
                    data = await self._client.json().get(key, "$.query_hash")
                    if data and data[0] == query_hash:
                        await self._client.delete(key)
                        count += 1
                except Exception:
                    continue
        
        if model:
            async for key in self._client.scan_iter(f"{self.config.prefix}*"):
                try:
                    data = await self._client.json().get(key, "$.model")
                    if data and data[0] == model:
                        await self._client.delete(key)
                        count += 1
                except Exception:
                    continue
        
        return count

    async def warm(
        self,
        queries: List[Tuple[str, str]],
        model: str = "",
        ttl: Optional[int] = None,
    ) -> int:
        """
        Warm the cache with pre-computed query-response pairs.
        
        Args:
            queries: List of (query, response) tuples
            model: Model identifier
            ttl: Time-to-live for warmed entries
            
        Returns:
            Number of entries added
        """
        count = 0
        for query, response in queries:
            try:
                await self.set(query, response, model=model, ttl=ttl)
                count += 1
            except Exception as e:
                self._logger.warning(f"Failed to warm cache entry: {e}")
        return count

    async def get_or_compute(
        self,
        query: str,
        compute_fn: Callable[[], Any],
        model: str = "",
        ttl: Optional[int] = None,
        strategy: CacheStrategy = CacheStrategy.HYBRID,
    ) -> Tuple[str, bool]:
        """
        Get from cache or compute and store.
        
        Args:
            query: The query
            compute_fn: Async function to compute response if not cached
            model: Model identifier
            ttl: Time-to-live
            strategy: Cache lookup strategy
            
        Returns:
            Tuple of (response, was_cached)
        """
        # Try cache first
        hit = await self.get(query, model=model, strategy=strategy)
        if hit:
            return hit.entry.response, True
        
        # Compute response
        if asyncio.iscoroutinefunction(compute_fn):
            response = await compute_fn()
        else:
            response = compute_fn()
        
        # Store in cache
        await self.set(query, response, model=model, ttl=ttl)
        
        return response, False

    async def stream_get_or_compute(
        self,
        query: str,
        compute_fn: Callable[[], AsyncIterator[str]],
        model: str = "",
        ttl: Optional[int] = None,
    ) -> AsyncIterator[str]:
        """
        Get from cache or compute with streaming support.
        
        Args:
            query: The query
            compute_fn: Async generator function for streaming response
            model: Model identifier
            ttl: Time-to-live
            
        Yields:
            Response chunks
        """
        # Try cache first
        hit = await self.get(query, model=model)
        if hit:
            yield hit.entry.response
            return
        
        # Stream and collect response
        chunks: List[str] = []
        async for chunk in compute_fn():
            chunks.append(chunk)
            yield chunk
        
        # Store complete response
        full_response = "".join(chunks)
        await self.set(query, full_response, model=model, ttl=ttl)

    async def _exact_lookup(self, query_hash: str) -> Optional[CacheEntry]:
        """Look up entry by exact query hash."""
        async for key in self._client.scan_iter(f"{self.config.prefix}*"):
            try:
                data = await self._client.json().get(key)
                if data and data.get("query_hash") == query_hash:
                    return self._dict_to_entry(data)
            except Exception:
                continue
        return None

    async def _semantic_lookup(
        self,
        query: str,
        model: Optional[str] = None,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> Optional[Tuple[CacheEntry, float]]:
        """Look up entry by semantic similarity."""
        # Generate query embedding
        embedding = await self._embedding_service.embed(query)
        
        # Build search query
        builder = VectorSearchQueryBuilder().with_vector(embedding).with_top_k(5)
        
        if model:
            builder.filter_eq("model", model)
        
        search_query = builder.build()
        
        # Execute search
        response = await self._search_executor.search(search_query, self.config.index_name)
        
        if not response.results:
            return None
        
        # Check similarity threshold
        best = response.results[0]
        if best.score < self.config.similarity_threshold:
            return None
        
        # Get full entry
        key = f"{self.config.prefix}{best.doc_id}"
        data = await self._client.json().get(key)
        if not data:
            return None
        
        entry = self._dict_to_entry(data)
        return entry, best.score

    async def _store_entry(self, entry: CacheEntry) -> None:
        """Store a cache entry in Redis."""
        key = f"{self.config.prefix}{entry.id}"
        
        data = {
            "id": entry.id,
            "query": entry.query,
            "query_hash": entry.query_hash,
            "response": entry.response,
            "embedding": entry.embedding,
            "model": entry.model,
            "metadata": entry.metadata,
            "created_at": entry.created_at,
            "last_accessed": entry.last_accessed,
            "access_count": entry.access_count,
            "ttl": entry.ttl,
            "importance_score": entry.importance_score,
            "tokens_saved": entry.tokens_saved,
        }
        
        await self._client.json().set(key, "$", data)
        await self._client.expire(key, entry.ttl)

    async def _update_access(self, entry: CacheEntry) -> None:
        """Update access statistics for an entry."""
        key = f"{self.config.prefix}{entry.id}"
        
        try:
            # Update access count and time
            await self._client.json().numincrby(key, "$.access_count", 1)
            await self._client.json().set(key, "$.last_accessed", time.time())
            
            # Adaptive TTL
            if self.config.enable_adaptive_ttl:
                current_ttl = await self._client.ttl(key)
                if current_ttl > 0:
                    new_ttl = min(
                        int(current_ttl * self.config.ttl_hit_multiplier),
                        self.config.max_ttl
                    )
                    await self._client.expire(key, new_ttl)
        except Exception as e:
            self._logger.warning(f"Failed to update access: {e}")

    async def _maybe_evict(self) -> None:
        """Evict entries if cache is over capacity."""
        async with self._eviction_lock:
            # Count entries
            count = 0
            async for _ in self._client.scan_iter(f"{self.config.prefix}*"):
                count += 1
            
            if count <= self.config.max_entries:
                return
            
            # Collect entries for eviction scoring
            entries: List[Dict[str, Any]] = []
            async for key in self._client.scan_iter(f"{self.config.prefix}*"):
                try:
                    data = await self._client.json().get(key)
                    if data:
                        data["_key"] = key
                        entries.append(data)
                except Exception:
                    continue
            
            # Score and sort entries
            entries_to_evict = count - int(self.config.max_entries * 0.9)
            scored_entries = self._score_entries_for_eviction(entries)
            
            # Evict lowest scored entries
            for entry in scored_entries[:entries_to_evict]:
                await self._client.delete(entry["_key"])
                self._stats.evictions += 1

    def _score_entries_for_eviction(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score entries for eviction (lower score = evict first)."""
        now = time.time()
        
        for entry in entries:
            if self.config.eviction_policy == EvictionPolicy.LRU:
                score = entry.get("last_accessed", 0)
            elif self.config.eviction_policy == EvictionPolicy.LFU:
                score = entry.get("access_count", 0)
            elif self.config.eviction_policy == EvictionPolicy.TTL:
                score = entry.get("created_at", 0) + entry.get("ttl", 0)
            else:  # ADAPTIVE
                recency = (now - entry.get("last_accessed", now)) / 3600  # hours
                frequency = entry.get("access_count", 0)
                importance = entry.get("importance_score", 1.0)
                tokens = entry.get("tokens_saved", 0)
                
                # Combined score: higher is better (less likely to evict)
                score = (frequency * 10 + tokens * 0.01 + importance * 5) / (1 + recency)
            
            entry["_eviction_score"] = score
        
        return sorted(entries, key=lambda e: e.get("_eviction_score", 0))

    def _normalize_query(self, query: str) -> str:
        """Normalize query for consistent matching."""
        # Basic normalization
        normalized = query.strip().lower()
        # Remove extra whitespace
        normalized = " ".join(normalized.split())
        return normalized

    def _hash_query(self, query: str) -> str:
        """Generate hash for exact matching."""
        return hashlib.sha256(query.encode()).hexdigest()

    def _dict_to_entry(self, data: Dict[str, Any]) -> CacheEntry:
        """Convert dictionary to CacheEntry."""
        return CacheEntry(
            id=data.get("id", ""),
            query=data.get("query", ""),
            query_hash=data.get("query_hash", ""),
            response=data.get("response", ""),
            embedding=data.get("embedding", []),
            model=data.get("model", ""),
            metadata=data.get("metadata", {}),
            created_at=data.get("created_at", time.time()),
            last_accessed=data.get("last_accessed", time.time()),
            access_count=data.get("access_count", 0),
            ttl=data.get("ttl", self.config.default_ttl),
            importance_score=data.get("importance_score", 1.0),
            tokens_saved=data.get("tokens_saved", 0),
        )

    def _track_similarity(self, similarity: float) -> None:
        """Track similarity for analytics."""
        if not self.config.enable_analytics:
            return
        self._similarity_samples.append(similarity)
        if len(self._similarity_samples) > 1000:
            self._similarity_samples = self._similarity_samples[-500:]
        self._stats.avg_similarity = sum(self._similarity_samples) / len(self._similarity_samples)

    def _track_lookup_time(self, time_ms: float) -> None:
        """Track lookup time for analytics."""
        if not self.config.enable_analytics:
            return
        self._lookup_time_samples.append(time_ms)
        if len(self._lookup_time_samples) > 1000:
            self._lookup_time_samples = self._lookup_time_samples[-500:]
        self._stats.avg_lookup_time_ms = sum(self._lookup_time_samples) / len(self._lookup_time_samples)

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "total_requests": self._stats.total_requests,
            "hits": self._stats.hits,
            "misses": self._stats.misses,
            "exact_hits": self._stats.exact_hits,
            "semantic_hits": self._stats.semantic_hits,
            "hit_rate": round(self._stats.hit_rate, 4),
            "stores": self._stats.stores,
            "evictions": self._stats.evictions,
            "errors": self._stats.errors,
            "total_tokens_saved": self._stats.total_tokens_saved,
            "avg_similarity": round(self._stats.avg_similarity, 4),
            "avg_lookup_time_ms": round(self._stats.avg_lookup_time_ms, 2),
        }

    async def clear(self) -> int:
        """Clear all cache entries."""
        count = 0
        async for key in self._client.scan_iter(f"{self.config.prefix}*"):
            await self._client.delete(key)
            count += 1
        
        # Reset stats
        self._stats = CacheStats()
        self._similarity_samples.clear()
        self._lookup_time_samples.clear()
        
        return count

    async def close(self) -> None:
        """Close cache connections."""
        self._initialized = False