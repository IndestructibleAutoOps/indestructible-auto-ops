"""
Semantic Cache: LLM response caching with semantic similarity.

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
from typing import Any, Dict, List, Optional, Protocol, Tuple

try:
    import redis.asyncio as redis
    from redis.commands.search.field import NumericField, TextField, VectorField
    from redis.commands.search.indexDefinition import IndexDefinition, IndexType
    from redis.commands.search.query import Query

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class EmbeddingModel(Protocol):
    """Protocol for embedding model interface."""

    async def encode(self, text: str) -> List[float]:
        """Encode text to embedding vector."""
        ...


@dataclass
class CacheConfig:
    """Configuration for semantic cache."""

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 1
    redis_password: Optional[str] = None
    prefix: str = "semcache:"
    similarity_threshold: float = 0.85
    default_ttl: int = 3600
    max_entries: int = 10000
    vector_dim: int = 1536
    eviction_policy: str = "lru"
    enable_adaptive_ttl: bool = True
    ttl_boost_threshold: int = 10
    ttl_boost_multiplier: float = 1.5
    max_ttl: int = 604800


class SemanticCache:
    """Semantic cache for LLM responses."""

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        config: Optional[CacheConfig] = None,
    ):
        if not REDIS_AVAILABLE:
            raise ImportError("Redis package not available. Install with: pip install redis[hiredis]")

        self._embedding_model = embedding_model
        self.config = config or CacheConfig()
        self._client: Optional[redis.Redis] = None
        self._logger = logging.getLogger(__name__)
        self._stats = {"hits": 0, "misses": 0, "stores": 0, "evictions": 0, "errors": 0}

    async def initialize(self) -> None:
        """Initialize Redis connection and create index."""
        self._client = redis.Redis(
            host=self.config.redis_host,
            port=self.config.redis_port,
            db=self.config.redis_db,
            password=self.config.redis_password,
            decode_responses=True,
        )
        await self._client.ping()
        await self._create_index()

    async def _create_index(self) -> None:
        """Create RediSearch index for cache entries."""
        index_name = f"{self.config.prefix}idx"
        try:
            await self._client.ft(index_name).info()
        except redis.ResponseError:
            schema = (
                TextField("$.query", as_name="query"),
                TextField("$.response", as_name="response"),
                NumericField("$.created_at", as_name="created_at"),
                NumericField("$.access_count", as_name="access_count"),
                VectorField(
                    "$.embedding",
                    "FLAT",
                    {"TYPE": "FLOAT32", "DIM": self.config.vector_dim, "DISTANCE_METRIC": "COSINE"},
                    as_name="embedding",
                ),
            )
            definition = IndexDefinition(prefix=[self.config.prefix], index_type=IndexType.JSON)
            await self._client.ft(index_name).create_index(schema, definition=definition)

    async def get(self, query: str, metadata_filter: Optional[Dict[str, Any]] = None) -> Optional[Tuple[str, float]]:
        """Get cached response for a query."""
        try:
            query_embedding = await self._embedding_model.encode(query)
            results = await self._vector_search(query_embedding, limit=5, metadata_filter=metadata_filter)

            if not results:
                self._stats["misses"] += 1
                return None

            best_match = results[0]
            similarity = 1 - best_match["distance"]

            if similarity < self.config.similarity_threshold:
                self._stats["misses"] += 1
                return None

            await self._update_access(best_match["id"])
            self._stats["hits"] += 1
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
        """Store a query-response pair in cache."""
        try:
            embedding = await self._embedding_model.encode(query)
            entry_id = hashlib.sha256(query.encode()).hexdigest()[:16]

            data = {
                "id": entry_id,
                "query": query,
                "response": response,
                "embedding": embedding,
                "metadata": metadata or {},
                "created_at": datetime.now().timestamp(),
                "access_count": 0,
            }

            key = f"{self.config.prefix}{entry_id}"
            await self._client.json().set(key, "$", data)
            await self._client.expire(key, ttl or self.config.default_ttl)

            self._stats["stores"] += 1
            await self._maybe_evict()
            return entry_id

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
        query_str = "*"

        query = (
            Query(f"({query_str})=>[KNN {limit} @embedding $vec AS distance]")
            .sort_by("distance")
            .return_fields("id", "query", "response", "distance")
            .dialect(2)
        )

        vec_bytes = struct.pack(f"{len(embedding)}f", *embedding)
        results = await self._client.ft(index_name).search(query, {"vec": vec_bytes})

        return [
            {
                "id": doc.id.replace(self.config.prefix, ""),
                "query": getattr(doc, "query", ""),
                "response": getattr(doc, "response", ""),
                "distance": float(getattr(doc, "distance", 1.0)),
            }
            for doc in results.docs
        ]

    async def _update_access(self, entry_id: str) -> None:
        """Update access count and extend TTL."""
        key = f"{self.config.prefix}{entry_id}"
        await self._client.json().numincrby(key, "$.access_count", 1)

        if self.config.enable_adaptive_ttl:
            access_count_data = await self._client.json().get(key, "$.access_count")
            access_count = access_count_data[0] if isinstance(access_count_data, list) else access_count_data

            if access_count and access_count >= self.config.ttl_boost_threshold:
                current_ttl = await self._client.ttl(key)
                if current_ttl > 0:
                    new_ttl = min(int(current_ttl * self.config.ttl_boost_multiplier), self.config.max_ttl)
                    await self._client.expire(key, new_ttl)

    async def _maybe_evict(self) -> None:
        """Evict entries if cache is full."""
        pattern = f"{self.config.prefix}*"
        count = 0
        async for key in self._client.scan_iter(pattern):
            if not key.endswith(":idx"):
                count += 1

        if count <= self.config.max_entries:
            return

        entries_to_evict = count - int(self.config.max_entries * 0.9)
        entries = []

        async for key in self._client.scan_iter(pattern):
            if key.endswith(":idx"):
                continue
            data = await self._client.json().get(key, "$.access_count", "$.created_at")
            if data:
                entries.append({"key": key, "access_count": data.get("$.access_count", [0])[0], "created_at": data.get("$.created_at", [0])[0]})

        if self.config.eviction_policy == "lru":
            entries.sort(key=lambda e: e["created_at"])
        else:
            entries.sort(key=lambda e: e["access_count"])

        for entry in entries[:entries_to_evict]:
            await self._client.delete(entry["key"])
            self._stats["evictions"] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._stats["hits"] + self._stats["misses"]
        hit_rate = self._stats["hits"] / total if total > 0 else 0
        return {**self._stats, "hit_rate": round(hit_rate, 4), "total_requests": total}

    async def clear(self) -> int:
        """Clear all cache entries."""
        pattern = f"{self.config.prefix}*"
        count = 0
        async for key in self._client.scan_iter(pattern):
            if not key.endswith(":idx"):
                await self._client.delete(key)
                count += 1
        return count

    async def close(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()