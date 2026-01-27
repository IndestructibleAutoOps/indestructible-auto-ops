"""
Redis Memory Backend: Production-ready memory storage with Redis.

This module provides a Redis-based implementation of the MemoryBackend
abstract class, supporting vector search, TTL-based expiration, and
various eviction policies.

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
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

# Note: Requires redis[hiredis] package
# pip install redis[hiredis]

try:
    import redis.asyncio as redis
    from redis.commands.search.field import NumericField, TextField, VectorField
    from redis.commands.search.indexDefinition import IndexDefinition, IndexType
    from redis.commands.search.query import Query

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


# =============================================================================
# Data Models (from memory_manager.py)
# =============================================================================


class MemoryType(Enum):
    """Types of memory storage."""

    SHORT_TERM = "short_term"  # Context window
    LONG_TERM = "long_term"  # Persistent storage
    VECTOR = "vector"  # Vector database for semantic search


@dataclass
class MemoryEntry:
    """A memory entry."""

    id: str = ""
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    memory_type: MemoryType = MemoryType.LONG_TERM
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    importance: float = 1.0  # 0.0 to 1.0
    access_count: int = 0

    def __post_init__(self):
        if not self.id:
            import uuid

            self.id = str(uuid.uuid4())


@dataclass
class MemoryQuery:
    """A memory query."""

    query_text: str = ""
    embedding: Optional[List[float]] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    memory_type: Optional[MemoryType] = None
    limit: int = 10
    threshold: float = 0.7
    metadata_filter: Optional[Dict[str, Any]] = None


class MemoryBackend(ABC):
    """Abstract base class for memory backends."""

    @abstractmethod
    async def add(self, entry: MemoryEntry) -> str:
        """Add a memory entry."""
        pass

    @abstractmethod
    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get a memory entry by ID."""
        pass

    @abstractmethod
    async def update(self, entry_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory entry."""
        pass

    @abstractmethod
    async def delete(self, entry_id: str) -> bool:
        """Delete a memory entry."""
        pass

    @abstractmethod
    async def query(self, query: MemoryQuery) -> List[MemoryEntry]:
        """Query memory entries."""
        pass

    @abstractmethod
    async def summarize(self, session_id: str, max_tokens: int = 1000) -> str:
        """Summarize memory for a session."""
        pass


# =============================================================================
# Redis Memory Backend Implementation
# =============================================================================


class RedisMemoryBackend(MemoryBackend):
    """
    Redis-based memory backend with vector search support.

    Features:
    - Fast in-memory storage with persistence
    - Vector similarity search for semantic retrieval
    - TTL-based automatic expiration
    - LRU/LFU eviction policies
    - Pub/Sub for real-time updates

    Requirements:
    - Redis Stack (with RediSearch and RedisJSON modules)
    - pip install redis[hiredis]

    Example:
        backend = RedisMemoryBackend(
            host="localhost",
            port=6379,
            vector_dim=1536,
        )
        await backend.initialize()

        # Add memory
        entry = MemoryEntry(
            content="User prefers direct flights",
            memory_type=MemoryType.LONG_TERM,
            user_id="user123",
        )
        entry_id = await backend.add(entry)

        # Query with vector search
        results = await backend.query(MemoryQuery(
            query_text="flight preferences",
            embedding=[...],  # Query embedding
            user_id="user123",
            limit=5,
        ))
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        prefix: str = "memory:",
        vector_dim: int = 1536,  # OpenAI embedding dimension
        default_ttl: int = 86400,  # 24 hours
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

        # Test connection
        await self._client.ping()
        self._logger.info(f"Connected to Redis at {self.host}:{self.port}")

        # Create vector search index
        await self._create_index()

    async def _create_index(self) -> None:
        """Create RediSearch index for memory entries."""
        index_name = f"{self.prefix}idx"

        try:
            # Check if index exists
            await self._client.ft(index_name).info()
            self._logger.info(f"Index {index_name} already exists")
        except redis.ResponseError:
            # Create index
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

            await self._client.ft(index_name).create_index(
                schema,
                definition=definition,
            )
            self._logger.info(f"Created index {index_name}")

    async def add(self, entry: MemoryEntry) -> str:
        """Add a memory entry to Redis."""
        key = f"{self.prefix}{entry.id}"

        # Serialize entry
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

        # Store as JSON
        await self._client.json().set(key, "$", data)

        # Set TTL based on memory type
        ttl = self._get_ttl(entry.memory_type, entry.importance)
        if ttl:
            await self._client.expire(key, ttl)

        self._logger.debug(f"Added memory entry: {entry.id}")
        return entry.id

    def _get_ttl(self, memory_type: MemoryType, importance: float) -> Optional[int]:
        """Calculate TTL based on memory type and importance."""
        if memory_type == MemoryType.SHORT_TERM:
            # Short-term: 1-4 hours based on importance
            return int(3600 * (1 + 3 * importance))
        elif memory_type == MemoryType.LONG_TERM:
            # Long-term: 1-30 days based on importance
            return int(86400 * (1 + 29 * importance))
        else:
            # Vector: use default TTL
            return self.default_ttl

    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get a memory entry by ID."""
        key = f"{self.prefix}{entry_id}"
        data = await self._client.json().get(key)

        if not data:
            return None

        # Increment access count
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

        # Update fields
        updates["updated_at"] = datetime.now().timestamp()

        for field_name, value in updates.items():
            await self._client.json().set(key, f"$.{field_name}", value)

        self._logger.debug(f"Updated memory entry: {entry_id}")
        return True

    async def delete(self, entry_id: str) -> bool:
        """Delete a memory entry."""
        key = f"{self.prefix}{entry_id}"
        result = await self._client.delete(key)
        if result > 0:
            self._logger.debug(f"Deleted memory entry: {entry_id}")
        return result > 0

    async def query(self, memory_query: MemoryQuery) -> List[MemoryEntry]:
        """Query memory entries with optional vector search."""
        index_name = f"{self.prefix}idx"

        # Build query
        query_parts = []

        if memory_query.session_id:
            query_parts.append(f"@session_id:{{{memory_query.session_id}}}")
        if memory_query.user_id:
            query_parts.append(f"@user_id:{{{memory_query.user_id}}}")
        if memory_query.memory_type:
            query_parts.append(f"@memory_type:{{{memory_query.memory_type.value}}}")

        # Text search
        if memory_query.query_text and not memory_query.embedding:
            # Escape special characters
            escaped_text = memory_query.query_text.replace("-", "\\-")
            query_parts.append(f"@content:{escaped_text}")

        query_str = " ".join(query_parts) if query_parts else "*"

        # Vector search if embedding provided
        if memory_query.embedding:
            query = (
                Query(
                    f"({query_str})=>[KNN {memory_query.limit} @embedding $vec AS score]"
                )
                .sort_by("score")
                .return_fields(
                    "id",
                    "content",
                    "session_id",
                    "user_id",
                    "memory_type",
                    "importance",
                    "created_at",
                    "score",
                )
                .dialect(2)
            )
            params = {"vec": self._encode_vector(memory_query.embedding)}
        else:
            query = (
                Query(query_str)
                .sort_by("created_at", asc=False)
                .paging(0, memory_query.limit)
            )
            params = {}

        # Execute query
        try:
            results = await self._client.ft(index_name).search(query, params)
        except redis.ResponseError as e:
            self._logger.error(f"Query error: {e}")
            return []

        # Convert to MemoryEntry objects
        entries = []
        for doc in results.docs:
            # Extract key from doc.id (format: "memory:uuid")
            entry_id = doc.id.replace(self.prefix, "")
            data = await self._client.json().get(f"{self.prefix}{entry_id}")
            if data:
                entry = self._deserialize_entry(data)
                entries.append(entry)

        self._logger.debug(f"Query returned {len(entries)} results")
        return entries

    def _encode_vector(self, vector: List[float]) -> bytes:
        """Encode vector for Redis search."""
        return struct.pack(f"{len(vector)}f", *vector)

    async def summarize(self, session_id: str, max_tokens: int = 1000) -> str:
        """Summarize memory for a session."""
        # Query all entries for session
        entries = await self.query(
            MemoryQuery(
                query_text="",
                session_id=session_id,
                limit=100,
            )
        )

        if not entries:
            return ""

        # Sort by importance and recency
        entries.sort(key=lambda e: (e.importance, e.created_at), reverse=True)

        # Build summary (in production, use LLM)
        summary_parts = []
        total_tokens = 0

        for entry in entries:
            entry_tokens = len(entry.content.split())
            if total_tokens + entry_tokens > max_tokens:
                break
            summary_parts.append(entry.content)
            total_tokens += entry_tokens

        return " ".join(summary_parts)

    async def get_stats(self) -> Dict[str, Any]:
        """Get memory backend statistics."""
        # Count entries by type
        stats = {
            "total_entries": 0,
            "short_term_entries": 0,
            "long_term_entries": 0,
            "vector_entries": 0,
        }

        pattern = f"{self.prefix}*"
        async for key in self._client.scan_iter(pattern):
            if key.endswith(":idx"):
                continue
            stats["total_entries"] += 1

            data = await self._client.json().get(key, "$.memory_type")
            if data:
                memory_type = data[0] if isinstance(data, list) else data
                if memory_type == "short_term":
                    stats["short_term_entries"] += 1
                elif memory_type == "long_term":
                    stats["long_term_entries"] += 1
                elif memory_type == "vector":
                    stats["vector_entries"] += 1

        # Get Redis info
        info = await self._client.info("memory")
        stats["redis_memory_used"] = info.get("used_memory_human", "N/A")

        return stats

    async def close(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._logger.info("Redis connection closed")


# =============================================================================
# Usage Example
# =============================================================================

if __name__ == "__main__":
    import asyncio

    async def main():
        # Initialize backend
        backend = RedisMemoryBackend(
            host="localhost",
            port=6379,
            vector_dim=1536,
        )

        try:
            await backend.initialize()

            # Add a memory entry
            entry = MemoryEntry(
                content="User prefers direct flights to London",
                memory_type=MemoryType.LONG_TERM,
                user_id="user123",
                session_id="session456",
                importance=0.8,
            )
            entry_id = await backend.add(entry)
            print(f"Added entry: {entry_id}")

            # Query memories
            results = await backend.query(
                MemoryQuery(
                    query_text="flight",
                    user_id="user123",
                    limit=5,
                )
            )
            print(f"Found {len(results)} results")

            # Get stats
            stats = await backend.get_stats()
            print(f"Stats: {stats}")

        finally:
            await backend.close()

    asyncio.run(main())