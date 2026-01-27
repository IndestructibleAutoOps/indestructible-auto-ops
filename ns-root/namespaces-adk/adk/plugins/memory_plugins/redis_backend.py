"""
Redis Memory Backend: Production-ready memory storage with Redis Stack.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins/memory_plugins
@gl-semantic-anchor GL-00-PLUGINS_MEMORYPL_REDIS
@gl-evidence-required false
GL Unified Charter Activated
"""

import json
import logging
import struct
from datetime import datetime
from typing import Any, Dict, List, Optional

from ...core.memory_manager import (
    MemoryBackend,
    MemoryEntry,
    MemoryQuery,
    MemoryType,
)

try:
    import redis.asyncio as redis
    from redis.commands.search.field import NumericField, TextField, VectorField
    from redis.commands.search.indexDefinition import IndexDefinition, IndexType
    from redis.commands.search.query import Query

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class RedisMemoryBackend(MemoryBackend):
    """Redis-based memory backend with vector search support."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        prefix: str = "memory:",
        vector_dim: int = 1536,
        default_ttl: int = 86400,
        **kwargs,
    ):
        if not REDIS_AVAILABLE:
            raise ImportError(
                "Redis package not available. Install with: pip install redis[hiredis]"
            )

        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.prefix = prefix
        self.vector_dim = vector_dim
        self.default_ttl = default_ttl
        self._client: Optional[redis.Redis] = None
        self._logger = logging.getLogger(__name__)

    async def initialize(self) -> None:
        """Initialize Redis connection and create index."""
        self._client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=True,
        )
        await self._client.ping()
        self._logger.info(f"Connected to Redis at {self.host}:{self.port}")
        await self._create_index()

    async def _create_index(self) -> None:
        """Create RediSearch index for memory entries."""
        index_name = f"{self.prefix}idx"
        try:
            await self._client.ft(index_name).info()
        except redis.ResponseError:
            schema = (
                TextField("$.content", as_name="content"),
                TextField("$.session_id", as_name="session_id"),
                TextField("$.user_id", as_name="user_id"),
                TextField("$.memory_type", as_name="memory_type"),
                NumericField("$.importance", as_name="importance"),
                NumericField("$.created_at", as_name="created_at"),
                NumericField("$.access_count", as_name="access_count"),
                VectorField(
                    "$.embedding",
                    "FLAT",
                    {
                        "TYPE": "FLOAT32",
                        "DIM": self.vector_dim,
                        "DISTANCE_METRIC": "COSINE",
                    },
                    as_name="embedding",
                ),
            )
            definition = IndexDefinition(
                prefix=[self.prefix],
                index_type=IndexType.JSON,
            )
            await self._client.ft(index_name).create_index(schema, definition=definition)
            self._logger.info(f"Created index {index_name}")

    async def add(self, entry: MemoryEntry) -> str:
        """Add a memory entry to Redis."""
        key = f"{self.prefix}{entry.id}"
        data = {
            "id": entry.id,
            "content": entry.content,
            "metadata": entry.metadata,
            "embedding": entry.embedding,
            "memory_type": entry.memory_type.value,
            "session_id": entry.session_id,
            "user_id": entry.user_id,
            "created_at": entry.created_at.timestamp(),
            "updated_at": entry.updated_at.timestamp(),
            "importance": entry.importance,
            "access_count": entry.access_count,
        }
        await self._client.json().set(key, "$", data)
        ttl = self._get_ttl(entry.memory_type, entry.importance)
        if ttl:
            await self._client.expire(key, ttl)
        return entry.id

    def _get_ttl(self, memory_type: MemoryType, importance: float) -> Optional[int]:
        """Calculate TTL based on memory type and importance."""
        if memory_type == MemoryType.SHORT_TERM:
            return int(3600 * (1 + 3 * importance))
        elif memory_type == MemoryType.LONG_TERM:
            return int(86400 * (1 + 29 * importance))
        return self.default_ttl

    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get a memory entry by ID."""
        key = f"{self.prefix}{entry_id}"
        data = await self._client.json().get(key)
        if not data:
            return None
        await self._client.json().numincrby(key, "$.access_count", 1)
        return self._deserialize_entry(data)

    def _deserialize_entry(self, data: Dict[str, Any]) -> MemoryEntry:
        """Deserialize Redis data to MemoryEntry."""
        return MemoryEntry(
            id=data["id"],
            content=data["content"],
            metadata=data.get("metadata", {}),
            embedding=data.get("embedding"),
            memory_type=MemoryType(data["memory_type"]),
            session_id=data.get("session_id"),
            user_id=data.get("user_id"),
            created_at=datetime.fromtimestamp(data["created_at"]),
            updated_at=datetime.fromtimestamp(data["updated_at"]),
            importance=data.get("importance", 1.0),
            access_count=data.get("access_count", 0),
        )

    async def update(self, entry_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory entry."""
        key = f"{self.prefix}{entry_id}"
        if not await self._client.exists(key):
            return False
        updates["updated_at"] = datetime.now().timestamp()
        for field_name, value in updates.items():
            await self._client.json().set(key, f"$.{field_name}", value)
        return True

    async def delete(self, entry_id: str) -> bool:
        """Delete a memory entry."""
        key = f"{self.prefix}{entry_id}"
        result = await self._client.delete(key)
        return result > 0

    async def query(self, memory_query: MemoryQuery) -> List[MemoryEntry]:
        """Query memory entries with optional vector search."""
        index_name = f"{self.prefix}idx"
        query_parts = []

        if memory_query.session_id:
            query_parts.append(f"@session_id:{{{memory_query.session_id}}}")
        if memory_query.user_id:
            query_parts.append(f"@user_id:{{{memory_query.user_id}}}")
        if memory_query.memory_type:
            query_parts.append(f"@memory_type:{{{memory_query.memory_type.value}}}")
        if memory_query.query_text and not memory_query.embedding:
            escaped_text = memory_query.query_text.replace("-", "\\-")
            query_parts.append(f"@content:{escaped_text}")

        query_str = " ".join(query_parts) if query_parts else "*"

        if hasattr(memory_query, "embedding") and memory_query.embedding:
            query = (
                Query(f"({query_str})=>[KNN {memory_query.limit} @embedding $vec AS score]")
                .sort_by("score")
                .return_fields("id", "content", "session_id", "user_id", "memory_type", "importance", "created_at", "score")
                .dialect(2)
            )
            params = {"vec": struct.pack(f"{len(memory_query.embedding)}f", *memory_query.embedding)}
        else:
            query = Query(query_str).sort_by("created_at", asc=False).paging(0, memory_query.limit)
            params = {}

        try:
            results = await self._client.ft(index_name).search(query, params)
        except redis.ResponseError as e:
            self._logger.error(f"Query error: {e}")
            return []

        entries = []
        for doc in results.docs:
            entry_id = doc.id.replace(self.prefix, "")
            data = await self._client.json().get(f"{self.prefix}{entry_id}")
            if data:
                entries.append(self._deserialize_entry(data))
        return entries

    async def summarize(self, session_id: str, max_tokens: int = 1000) -> str:
        """Summarize memory for a session."""
        entries = await self.query(MemoryQuery(query_text="", session_id=session_id, limit=100))
        if not entries:
            return ""
        entries.sort(key=lambda e: (e.importance, e.created_at), reverse=True)
        summary_parts = []
        total_tokens = 0
        for entry in entries:
            entry_tokens = len(entry.content.split())
            if total_tokens + entry_tokens > max_tokens:
                break
            summary_parts.append(entry.content)
            total_tokens += entry_tokens
        return " ".join(summary_parts)

    async def close(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()