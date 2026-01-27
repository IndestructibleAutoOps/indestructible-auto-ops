"""
Semantic Cache: LLM response caching with semantic similarity.

This module provides a semantic caching layer that stores and retrieves
LLM responses based on query similarity, reducing API calls and costs.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins/memory_plugins
@gl-semantic-anchor GL-00-PLUGINS_MEMORYPL_SEMCACHE
@gl-evidence-required false
GL Unified Charter Activated
"""

import hashlib
import logging
import struct
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple

try:
    import redis.asyncio as redis
    from redis.commands.search.field import NumericField, TextField, VectorField
    from redis.commands.search.indexDefinition import IndexDefinition, IndexType
    from redis.commands.search.query import Query

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


# =============================================================================
# Protocols and Data Models
# =============================================================================


class EmbeddingModel(Protocol):
    """Protocol for embedding model interface."""

    async def encode(self, text: str) -> List[float]:
        """Encode text to embedding vector."""
        ...


@dataclass
class CacheEntry:
    """A semantic cache entry."""

    id: str = ""
    query: str = ""
    response: str = ""
    embedding: List[float] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    ttl: int = 3600

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.sha256(self.query.encode()).hexdigest()[:16]


@dataclass
class CacheConfig:
    """Configuration for semantic cache."""

    # Redis settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 1  # Use separate DB for cache
    redis_password: Optional[str] = None

    # Cache settings
    prefix: str = "semcache:"
    similarity_threshold: float = 0.85
    default_ttl: int = 3600  # 1 hour
    max_entries: int = 10000
    vector_dim: int = 1536

    # Eviction settings
    eviction_policy: str = "lru"  # "lru", "lfu", or "ttl"
    eviction_batch_size: int = 100

    # TTL adaptation settings
    enable_adaptive_ttl: bool = True
    ttl_boost_threshold: int = 10  # Access count to boost TTL
    ttl_boost_multiplier: float = 1.5
    max_ttl: int = 604800  # 7 days


# =============================================================================
# Semantic Cache Implementation
# =============================================================================


class SemanticCache:
    """
    Semantic cache for LLM responses.

    Features:
    - Vector similarity-based cache lookup
    - Configurable similarity threshold
    - Adaptive TTL based on access patterns
    - LRU/LFU eviction policies
    - Cache warming and preloading
    - Comprehensive statistics

    Benefits:
    - Reduce LLM API calls by 50-90%
    - Lower latency for cached responses
    - Significant cost savings
    - Consistent responses for similar queries

    Example:
        cache = SemanticCache(
            embedding_model=my_embedding_model,
            config=CacheConfig(
                similarity_threshold=0.85,
                default_ttl=3600,
            ),
        )
        await cache.initialize()

        # Check cache
        result = await cache.get("What is the capital of France?")
        if result:
            response, score = result
            print(f"Cache hit! Score: {score}")
        else:
            # Call LLM and cache response
            response = await llm.generate("What is the capital of France?")
            await cache.set("What is the capital of France?", response)
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        config: Optional[CacheConfig] = None,
    ):
        if not REDIS_AVAILABLE:
            raise ImportError(
                "Redis package not available. Install with: pip install redis[hiredis]"
            )

        self._embedding_model = embedding_model
        self.config = config or CacheConfig()

        self._client: Optional[redis.Redis] = None
        self._logger = logging.getLogger(__name__)

        # Statistics
        self._stats = {
            "hits": 0,
            "misses": 0,
            "stores": 0,
            "evictions": 0,
            "errors": 0,
        }

    async def initialize(self) -> None:
        """Initialize Redis connection and create index."""
        self._client = redis.Redis(
            host=self.config.redis_host,
            port=self.config.redis_port,
            db=self.config.redis_db,
            password=self.config.redis_password,
            decode_responses=True,
        )

        # Test connection
        await self._client.ping()
        self._logger.info(
            f"Semantic cache connected to Redis at "
            f"{self.config.redis_host}:{self.config.redis_port}"
        )

        # Create vector search index
        await self._create_index()

    async def _create_index(self) -> None:
        """Create RediSearch index for cache entries."""
        index_name = f"{self.config.prefix}idx"

        try:
            await self._client.ft(index_name).info()
            self._logger.info(f"Cache index {index_name} already exists")
        except redis.ResponseError:
            schema = (
                TextField("$.query", as_name="query"),
                TextField("$.response", as_name="response"),
                NumericField("$.created_at", as_name="created_at"),
                NumericField("$.access_count", as_name="access_count"),
                VectorField(
                    "$.embedding",
                    "FLAT",
                    {
                        "TYPE": "FLOAT32",
                        "DIM": self.config.vector_dim,
                        "DISTANCE_METRIC": "COSINE",
                    },
                    as_name="embedding",
                ),
            )

            definition = IndexDefinition(
                prefix=[self.config.prefix],
                index_type=IndexType.JSON,
            )

            await self._client.ft(index_name).create_index(
                schema,
                definition=definition,
            )
            self._logger.info(f"Created cache index {index_name}")

    async def get(
        self,
        query: str,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> Optional[Tuple[str, float]]:
        """
        Get cached response for a query.

        Args:
            query: The query string
            metadata_filter: Optional metadata filter

        Returns:
            Tuple of (response, similarity_score) if found, None otherwise
        """
        try:
            # Generate embedding for query
            query_embedding = await self._embedding_model.encode(query)

            # Search for similar queries
            results = await self._vector_search(
                query_embedding,
                limit=5,
                metadata_filter=metadata_filter,
            )

            if not results:
                self._stats["misses"] += 1
                return None

            # Check similarity threshold
            best_match = results[0]
            similarity = 1 - best_match["distance"]  # Convert distance to similarity

            if similarity < self.config.similarity_threshold:
                self._stats["misses"] += 1
                self._logger.debug(
                    f"Cache miss: similarity {similarity:.3f} < "
                    f"threshold {self.config.similarity_threshold}"
                )
                return None

            # Update access count and TTL
            await self._update_access(best_match["id"])

            self._stats["hits"] += 1
            self._logger.debug(f"Cache hit: similarity {similarity:.3f}")
            return (best_match["response"], similarity)

        except Exception as e:
            self._stats["errors"] += 1
            self._logger.error(f"Cache get error: {e}")
            return None

    async def set(
        self,
        query: str,
        response: str,
        metadata: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None,
    ) -> str:
        """
        Store a query-response pair in cache.

        Args:
            query: The query string
            response: The LLM response
            metadata: Optional metadata
            ttl: Optional TTL in seconds

        Returns:
            Cache entry ID
        """
        try:
            # Generate embedding
            embedding = await self._embedding_model.encode(query)

            # Create entry
            entry = CacheEntry(
                query=query,
                response=response,
                embedding=embedding,
                metadata=metadata or {},
                ttl=ttl or self.config.default_ttl,
            )

            # Store in Redis
            key = f"{self.config.prefix}{entry.id}"
            data = {
                "id": entry.id,
                "query": entry.query,
                "response": entry.response,
                "embedding": entry.embedding,
                "metadata": entry.metadata,
                "created_at": entry.created_at.timestamp(),
                "access_count": 0,
            }

            await self._client.json().set(key, "$", data)
            await self._client.expire(key, entry.ttl)

            self._stats["stores"] += 1
            self._logger.debug(f"Cached response for query: {query[:50]}...")

            # Check if eviction needed
            await self._maybe_evict()

            return entry.id

        except Exception as e:
            self._stats["errors"] += 1
            self._logger.error(f"Cache set error: {e}")
            raise

    async def _vector_search(
        self,
        embedding: List[float],
        limit: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar entries using vector similarity."""
        index_name = f"{self.config.prefix}idx"

        # Build query
        query_str = "*"
        if metadata_filter:
            filter_parts = []
            for key, value in metadata_filter.items():
                filter_parts.append(f"@metadata_{key}:{{{value}}}")
            if filter_parts:
                query_str = " ".join(filter_parts)

        # Vector search
        query = (
            Query(f"({query_str})=>[KNN {limit} @embedding $vec AS distance]")
            .sort_by("distance")
            .return_fields("id", "query", "response", "distance")
            .dialect(2)
        )

        vec_bytes = struct.pack(f"{len(embedding)}f", *embedding)

        results = await self._client.ft(index_name).search(
            query,
            {"vec": vec_bytes},
        )

        return [
            {
                "id": doc.id.replace(self.config.prefix, ""),
                "query": doc.query if hasattr(doc, "query") else "",
                "response": doc.response if hasattr(doc, "response") else "",
                "distance": float(doc.distance) if hasattr(doc, "distance") else 1.0,
            }
            for doc in results.docs
        ]

    async def _update_access(self, entry_id: str) -> None:
        """Update access count and extend TTL."""
        key = f"{self.config.prefix}{entry_id}"

        # Increment access count
        await self._client.json().numincrby(key, "$.access_count", 1)

        # Adaptive TTL
        if self.config.enable_adaptive_ttl:
            access_count_data = await self._client.json().get(key, "$.access_count")
            access_count = (
                access_count_data[0]
                if isinstance(access_count_data, list)
                else access_count_data
            )

            if access_count and access_count >= self.config.ttl_boost_threshold:
                current_ttl = await self._client.ttl(key)
                if current_ttl > 0:
                    new_ttl = min(
                        int(current_ttl * self.config.ttl_boost_multiplier),
                        self.config.max_ttl,
                    )
                    await self._client.expire(key, new_ttl)
                    self._logger.debug(
                        f"Extended TTL for popular entry: {current_ttl} -> {new_ttl}"
                    )

    async def _maybe_evict(self) -> None:
        """Evict entries if cache is full."""
        # Count entries
        pattern = f"{self.config.prefix}*"
        count = 0
        async for key in self._client.scan_iter(pattern):
            if not key.endswith(":idx"):
                count += 1

        if count <= self.config.max_entries:
            return

        # Calculate entries to evict
        entries_to_evict = count - int(self.config.max_entries * 0.9)
        self._logger.info(
            f"Cache full ({count} entries), evicting {entries_to_evict} entries"
        )

        if self.config.eviction_policy == "lru":
            await self._evict_lru(entries_to_evict)
        elif self.config.eviction_policy == "lfu":
            await self._evict_lfu(entries_to_evict)
        else:
            # TTL-based eviction is handled by Redis automatically
            pass

    async def _evict_lru(self, count: int) -> None:
        """Evict least recently used entries."""
        # Get all entries sorted by created_at (as proxy for last access)
        entries = []
        pattern = f"{self.config.prefix}*"

        async for key in self._client.scan_iter(pattern):
            if key.endswith(":idx"):
                continue
            data = await self._client.json().get(key, "$.created_at")
            if data:
                created_at = data[0] if isinstance(data, list) else data
                entries.append({"key": key, "created_at": created_at})

        # Sort by created_at (oldest first)
        entries.sort(key=lambda e: e["created_at"])

        # Evict
        for entry in entries[:count]:
            await self._client.delete(entry["key"])
            self._stats["evictions"] += 1

        self._logger.info(f"Evicted {count} LRU entries")

    async def _evict_lfu(self, count: int) -> None:
        """Evict least frequently used entries."""
        entries = []
        pattern = f"{self.config.prefix}*"

        async for key in self._client.scan_iter(pattern):
            if key.endswith(":idx"):
                continue
            data = await self._client.json().get(key, "$.access_count")
            if data:
                access_count = data[0] if isinstance(data, list) else data
                entries.append({"key": key, "access_count": access_count or 0})

        # Sort by access_count (least accessed first)
        entries.sort(key=lambda e: e["access_count"])

        # Evict
        for entry in entries[:count]:
            await self._client.delete(entry["key"])
            self._stats["evictions"] += 1

        self._logger.info(f"Evicted {count} LFU entries")

    async def warm(
        self,
        entries: List[Dict[str, Any]],
        batch_size: int = 100,
    ) -> int:
        """
        Pre-warm cache with entries.

        Args:
            entries: List of {"query": str, "response": str, "metadata": dict}
            batch_size: Number of entries to process in each batch

        Returns:
            Number of entries added
        """
        count = 0
        for i in range(0, len(entries), batch_size):
            batch = entries[i : i + batch_size]
            for entry in batch:
                try:
                    await self.set(
                        query=entry["query"],
                        response=entry["response"],
                        metadata=entry.get("metadata"),
                    )
                    count += 1
                except Exception as e:
                    self._logger.error(f"Failed to warm entry: {e}")

            self._logger.info(f"Warmed {count}/{len(entries)} entries")

        return count

    async def invalidate(self, query: str) -> bool:
        """
        Invalidate a specific cache entry.

        Args:
            query: The query to invalidate

        Returns:
            True if entry was found and deleted
        """
        entry_id = hashlib.sha256(query.encode()).hexdigest()[:16]
        key = f"{self.config.prefix}{entry_id}"
        result = await self._client.delete(key)
        return result > 0

    async def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate cache entries matching a pattern.

        Args:
            pattern: Query pattern to match (uses Redis SCAN)

        Returns:
            Number of entries invalidated
        """
        count = 0
        search_pattern = f"{self.config.prefix}*"

        async for key in self._client.scan_iter(search_pattern):
            if key.endswith(":idx"):
                continue

            data = await self._client.json().get(key, "$.query")
            if data:
                query = data[0] if isinstance(data, list) else data
                if pattern.lower() in query.lower():
                    await self._client.delete(key)
                    count += 1

        return count

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total if total > 0 else 0

        return {
            **self._stats,
            "hit_rate": round(hit_rate, 4),
            "total_requests": total,
            "config": {
                "similarity_threshold": self.config.similarity_threshold,
                "default_ttl": self.config.default_ttl,
                "max_entries": self.config.max_entries,
                "eviction_policy": self.config.eviction_policy,
            },
        }

    async def clear(self) -> int:
        """Clear all cache entries."""
        pattern = f"{self.config.prefix}*"
        count = 0
        async for key in self._client.scan_iter(pattern):
            if not key.endswith(":idx"):
                await self._client.delete(key)
                count += 1

        self._logger.info(f"Cleared {count} cache entries")
        return count

    async def close(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._logger.info("Semantic cache connection closed")


# =============================================================================
# Mock Embedding Model for Testing
# =============================================================================


class MockEmbeddingModel:
    """Mock embedding model for testing."""

    def __init__(self, dim: int = 1536):
        self.dim = dim

    async def encode(self, text: str) -> List[float]:
        """Generate a deterministic embedding based on text hash."""
        import hashlib

        # Create deterministic embedding from text hash
        hash_bytes = hashlib.sha256(text.encode()).digest()
        embedding = []

        for i in range(self.dim):
            # Use hash bytes cyclically
            byte_val = hash_bytes[i % len(hash_bytes)]
            # Normalize to [-1, 1]
            embedding.append((byte_val / 127.5) - 1)

        return embedding


# =============================================================================
# Usage Example
# =============================================================================

if __name__ == "__main__":
    import asyncio

    async def main():
        # Initialize with mock embedding model
        embedding_model = MockEmbeddingModel(dim=1536)

        config = CacheConfig(
            redis_host="localhost",
            redis_port=6379,
            similarity_threshold=0.85,
            default_ttl=3600,
            max_entries=1000,
        )

        cache = SemanticCache(
            embedding_model=embedding_model,
            config=config,
        )

        try:
            await cache.initialize()

            # Store some responses
            await cache.set(
                query="What is the capital of France?",
                response="The capital of France is Paris.",
            )

            await cache.set(
                query="What is Python?",
                response="Python is a high-level programming language.",
            )

            # Try to retrieve
            result = await cache.get("What's the capital city of France?")
            if result:
                response, score = result
                print(f"Cache hit! Score: {score:.3f}")
                print(f"Response: {response}")
            else:
                print("Cache miss")

            # Get stats
            stats = cache.get_stats()
            print(f"\nCache stats: {stats}")

        finally:
            await cache.close()

    asyncio.run(main())