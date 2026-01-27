"""
Memory Manager: Unified management of short-term and long-term memory.

This module provides unified memory operations for agents, supporting
both context window (short-term) and persistent (long-term) memory backends.

GL Layer: GL30-49 (Execution Layer)
GL Purpose: Memory management and context persistence

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/core
@gl-semantic-anchor GL-00-ADK_CORE_MEMORYMANAGE
@gl-evidence-required false
GL Unified Charter Activated
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from ..observability.logging import Logger
from .event_bus import EventBus


class MemoryType(Enum):
    """Types of memory storage."""

    SHORT_TERM = "short_term"  # Context window
    LONG_TERM = "long_term"  # Persistent storage
    VECTOR = "vector"  # Vector database for semantic search


@dataclass
class MemoryEntry:
    """A memory entry."""

    id: str
    content: str
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

    query_text: str
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


class InMemoryBackend(MemoryBackend):
    """In-memory backend for testing and development."""

    def __init__(self):
        self._storage: Dict[str, MemoryEntry] = {}
        self._logger = logging.getLogger(__name__)

    async def add(self, entry: MemoryEntry) -> str:
        self._storage[entry.id] = entry
        return entry.id

    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        return self._storage.get(entry_id)

    async def update(self, entry_id: str, updates: Dict[str, Any]) -> bool:
        entry = self._storage.get(entry_id)
        if not entry:
            return False
        for key, value in updates.items():
            setattr(entry, key, value)
        entry.updated_at = datetime.now()
        return True

    async def delete(self, entry_id: str) -> bool:
        if entry_id in self._storage:
            del self._storage[entry_id]
            return True
        return False

    async def query(self, memory_query: MemoryQuery) -> List[MemoryEntry]:
        # Simple text-based query (in production, use vector similarity)
        results = []
        query_lower = memory_query.query_text.lower()

        for entry in self._storage.values():
            # Apply filters
            if memory_query.session_id and entry.session_id != memory_query.session_id:
                continue
            if memory_query.user_id and entry.user_id != memory_query.user_id:
                continue
            if (
                memory_query.memory_type
                and entry.memory_type != memory_query.memory_type
            ):
                continue

            # Simple text match
            if query_lower in entry.content.lower():
                results.append(entry)
                if len(results) >= memory_query.limit:
                    break

        return results

    async def summarize(self, session_id: str, max_tokens: int = 1000) -> str:
        # Simple summarization (in production, use LLM)
        entries = [e for e in self._storage.values() if e.session_id == session_id]
        if not entries:
            return ""

        # Sort by importance and recency
        entries.sort(key=lambda e: (e.importance, e.created_at), reverse=True)

        # Build summary
        summary_parts = []
        total_tokens = 0

        for entry in entries:
            entry_tokens = len(entry.content.split())
            if total_tokens + entry_tokens > max_tokens:
                break
            summary_parts.append(entry.content)
            total_tokens += entry_tokens

        return " ".join(summary_parts)


class MemoryManager:
    """
    Unified memory manager for agents.

    Provides:
    - Unified API for short-term and long-term memory
    - Context window management
    - Memory compaction and summarization
    - Plugin support for different backends
    - PII filtering integration
    """

    def __init__(
        self,
        backend: str = "in_memory",
        event_bus: Optional[EventBus] = None,
        **backend_config,
    ):
        self.backend_type = backend
        self.event_bus = event_bus
        self.backend_config = backend_config

        self.logger = Logger(name="memory.manager")

        # Initialize backend
        self.backend: Optional[MemoryBackend] = None

        # Context window cache
        self._context_cache: Dict[str, List[MemoryEntry]] = {}
        self._context_max_size: int = backend_config.get("context_max_size", 50)

        # Statistics
        self._stats = {
            "total_entries": 0,
            "total_queries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
        }

    async def initialize(self) -> None:
        """Initialize the memory manager and backend."""
        self.logger.info(
            f"Initializing memory manager with backend: {self.backend_type}"
        )

        if self.backend_type == "in_memory":
            self.backend = InMemoryBackend()
        elif self.backend_type == "redis":
            from ..plugins.memory_plugins.redis_backend import RedisMemoryBackend

            self.backend = RedisMemoryBackend(
                host=self.backend_config.get("redis_host", "localhost"),
                port=self.backend_config.get("redis_port", 6379),
                db=self.backend_config.get("redis_db", 0),
                password=self.backend_config.get("redis_password"),
                prefix=self.backend_config.get("redis_prefix", "memory:"),
                vector_dim=self.backend_config.get("vector_dim", 1536),
            )
            await self.backend.initialize()
            
            # Initialize vector search components if enabled
            if self.backend_config.get("enable_vector_search", False):
                await self._initialize_vector_search()
        elif self.backend_type == "vector":
            # Initialize vector-only backend with semantic search
            await self._initialize_vector_search()
        else:
            raise ValueError(f"Unknown backend type: {self.backend_type}")

        self.logger.info("Memory manager initialized")

    async def _initialize_vector_search(self) -> None:
        """Initialize vector search components."""
        from ..plugins.memory_plugins.vector_index_manager import (
            VectorIndexManager,
            DEFAULT_MEMORY_INDEX,
        )
        from ..plugins.memory_plugins.embedding_service import (
            EmbeddingService,
            EmbeddingConfig,
            EmbeddingProvider,
        )
        from ..plugins.memory_plugins.vector_search import (
            VectorSearchExecutor,
            SemanticMemorySearch,
        )

        # Get Redis client from backend if available
        redis_client = getattr(self.backend, "_client", None)
        if not redis_client:
            self.logger.warning("Vector search requires Redis backend")
            return

        # Initialize vector index manager
        self._vector_index_manager = VectorIndexManager(redis_client)
        
        # Create default memory index
        index_config = self.backend_config.get("vector_index_config", DEFAULT_MEMORY_INDEX)
        await self._vector_index_manager.create_index(index_config)

        # Initialize embedding service
        embedding_provider = self.backend_config.get(
            "embedding_provider", EmbeddingProvider.OPENAI
        )
        embedding_model = self.backend_config.get(
            "embedding_model", "text-embedding-ada-002"
        )
        embedding_dim = self.backend_config.get("vector_dim", 1536)
        
        embedding_config = EmbeddingConfig(
            provider=embedding_provider,
            model=embedding_model,
            dimension=embedding_dim,
            api_key=self.backend_config.get("embedding_api_key"),
            api_base=self.backend_config.get("embedding_api_base"),
        )
        
        self._embedding_service = EmbeddingService(
            config=embedding_config,
            cache_client=redis_client,
            cache_ttl=self.backend_config.get("embedding_cache_ttl", 86400),
        )

        # Initialize vector search executor
        self._vector_search_executor = VectorSearchExecutor(
            redis_client=redis_client,
            default_index=index_config.name,
            vector_field="embedding",
        )

        # Initialize semantic memory search
        self._semantic_search = SemanticMemorySearch(
            redis_client=redis_client,
            embedding_service=self._embedding_service,
            index_name=index_config.name,
        )

        self.logger.info("Vector search components initialized")

    async def shutdown(self) -> None:
        """Shutdown the memory manager."""
        self.logger.info("Memory manager shutdown")

    async def add(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.LONG_TERM,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        importance: float = 1.0,
    ) -> str:
        """
        Add a memory entry.

        Args:
            content: Memory content
            memory_type: Type of memory
            session_id: Session ID
            user_id: User ID
            metadata: Additional metadata
            importance: Importance score (0.0 to 1.0)

        Returns:
            Entry ID
        """
        entry = MemoryEntry(
            content=content,
            memory_type=memory_type,
            session_id=session_id,
            user_id=user_id,
            metadata=metadata or {},
            importance=importance,
        )

        entry_id = await self.backend.add(entry)
        self._stats["total_entries"] += 1

        # Update context cache
        if session_id and memory_type == MemoryType.SHORT_TERM:
            self._update_context_cache(session_id, entry)

        # Emit event
        if self.event_bus:
            await self.event_bus.publish(
                "memory.added",
                {
                    "entry_id": entry_id,
                    "memory_type": memory_type.value,
                    "session_id": session_id,
                    "user_id": user_id,
                },
            )

        self.logger.debug(f"Added memory entry: {entry_id}")
        return entry_id

    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get a memory entry by ID."""
        entry = await self.backend.get(entry_id)
        if entry:
            entry.access_count += 1
        return entry

    async def update(
        self,
        entry_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Update a memory entry."""
        updates = {}
        if content:
            updates["content"] = content
        if metadata:
            updates["metadata"] = metadata

        success = await self.backend.update(entry_id, updates)

        if success and self.event_bus:
            await self.event_bus.publish("memory.updated", {"entry_id": entry_id})

        return success

    async def delete(self, entry_id: str) -> bool:
        """Delete a memory entry."""
        success = await self.backend.delete(entry_id)

        if success and self.event_bus:
            await self.event_bus.publish("memory.deleted", {"entry_id": entry_id})

        return success

    async def query(
        self,
        query_text: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        memory_type: Optional[MemoryType] = None,
        limit: int = 10,
        threshold: float = 0.7,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[MemoryEntry]:
        """
        Query memory entries.

        Args:
            query_text: Query text
            session_id: Session ID filter
            user_id: User ID filter
            memory_type: Memory type filter
            limit: Maximum number of results
            threshold: Similarity threshold (for vector search)
            metadata_filter: Metadata filter

        Returns:
            List of matching memory entries
        """
        self._stats["total_queries"] += 1

        memory_query = MemoryQuery(
            query_text=query_text,
            session_id=session_id,
            user_id=user_id,
            memory_type=memory_type,
            limit=limit,
            threshold=threshold,
            metadata_filter=metadata_filter,
        )

        results = await self.backend.query(memory_query)

        # Update access counts
        for entry in results:
            entry.access_count += 1

        self.logger.debug(f"Query returned {len(results)} results")
        return results

    async def get_context(self, session_id: str, max_tokens: int = 2000) -> str:
        """
        Get context window for a session.

        Args:
            session_id: Session ID
            max_tokens: Maximum tokens

        Returns:
            Context string
        """
        # Check cache
        if session_id in self._context_cache:
            self._stats["cache_hits"] += 1
            entries = self._context_cache[session_id]
        else:
            self._stats["cache_misses"] += 1
            # Query for short-term memory
            entries = await self.query(
                query_text="",
                session_id=session_id,
                memory_type=MemoryType.SHORT_TERM,
                limit=100,
            )
            self._context_cache[session_id] = entries

        # Build context string
        context_parts = []
        total_tokens = 0

        for entry in entries:
            entry_tokens = len(entry.content.split())
            if total_tokens + entry_tokens > max_tokens:
                break
            context_parts.append(entry.content)
            total_tokens += entry_tokens

        return "\n\n".join(context_parts)

    async def semantic_search(
        self,
        query: str,
        top_k: int = 10,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        min_importance: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search over memories using vector similarity.

        Args:
            query: Search query text
            top_k: Number of results to return
            agent_id: Filter by agent ID
            session_id: Filter by session ID
            memory_type: Filter by memory type
            min_importance: Minimum importance score

        Returns:
            List of search results with scores
        """
        if not hasattr(self, "_semantic_search") or self._semantic_search is None:
            self.logger.warning("Semantic search not initialized, falling back to text query")
            entries = await self.query(query_text=query, session_id=session_id, limit=top_k)
            return [{"doc_id": e.id, "content": e.content, "score": 1.0} for e in entries]

        results = await self._semantic_search.search(
            query=query,
            top_k=top_k,
            agent_id=agent_id,
            session_id=session_id,
            memory_type=memory_type,
            min_importance=min_importance,
        )

        return [
            {
                "doc_id": r.doc_id,
                "content": r.content,
                "score": r.score,
                "metadata": r.metadata,
            }
            for r in results
        ]

    async def get_semantic_context(
        self,
        query: str,
        max_tokens: int = 2000,
        agent_id: Optional[str] = None,
    ) -> str:
        """
        Get semantically relevant context for a query.

        Args:
            query: Query to get context for
            max_tokens: Maximum tokens in context
            agent_id: Filter by agent ID

        Returns:
            Formatted context string
        """
        if not hasattr(self, "_semantic_search") or self._semantic_search is None:
            return await self.compact_context(agent_id or "", max_tokens)

        return await self._semantic_search.get_context(
            query=query,
            max_tokens=max_tokens,
            agent_id=agent_id,
        )

    async def add_with_embedding(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.LONG_TERM,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        importance: float = 1.0,
    ) -> str:
        """
        Add a memory entry with automatic embedding generation.

        Args:
            content: Memory content
            memory_type: Type of memory
            session_id: Session ID
            user_id: User ID
            agent_id: Agent ID
            metadata: Additional metadata
            importance: Importance score (0.0 to 1.0)

        Returns:
            Entry ID
        """
        import time

        # Generate embedding if service is available
        embedding = None
        if hasattr(self, "_embedding_service") and self._embedding_service is not None:
            embedding = await self._embedding_service.embed(content)

        # Create entry
        entry = MemoryEntry(
            content=content,
            memory_type=memory_type,
            session_id=session_id,
            user_id=user_id,
            metadata=metadata or {},
            importance=importance,
            embedding=embedding,
        )

        # Add to backend
        entry_id = await self.backend.add(entry)
        self._stats["total_entries"] += 1

        # Store in vector index if available
        if (
            hasattr(self, "_vector_index_manager")
            and self._vector_index_manager is not None
            and embedding is not None
        ):
            await self._vector_index_manager.store_document(
                index_name="idx:memory",
                doc_id=entry_id,
                content=content,
                embedding=embedding,
                metadata={
                    "type": memory_type.value,
                    "session_id": session_id or "",
                    "agent_id": agent_id or "",
                    "user_id": user_id or "",
                    "importance": importance,
                    "timestamp": time.time(),
                    **(metadata or {}),
                },
            )

        # Update context cache
        if session_id and memory_type == MemoryType.SHORT_TERM:
            self._update_context_cache(session_id, entry)

        # Emit event
        if self.event_bus:
            await self.event_bus.publish(
                "memory.added",
                {
                    "entry_id": entry_id,
                    "memory_type": memory_type.value,
                    "session_id": session_id,
                    "user_id": user_id,
                    "has_embedding": embedding is not None,
                },
            )

        self.logger.debug(f"Added memory entry with embedding: {entry_id}")
        return entry_id

    async def find_similar_memories(
        self,
        content: str,
        top_k: int = 5,
        exclude_self: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Find memories similar to given content.

        Args:
            content: Content to find similar memories for
            top_k: Number of results
            exclude_self: Whether to exclude exact matches

        Returns:
            List of similar memories with scores
        """
        if not hasattr(self, "_semantic_search") or self._semantic_search is None:
            return []

        results = await self._semantic_search.find_similar(
            content=content,
            top_k=top_k,
            exclude_self=exclude_self,
        )

        return [
            {
                "doc_id": r.doc_id,
                "content": r.content,
                "score": r.score,
                "metadata": r.metadata,
            }
            for r in results
        ]

    def get_embedding_stats(self) -> Dict[str, Any]:
        """Get embedding service statistics."""
        if hasattr(self, "_embedding_service") and self._embedding_service is not None:
            return self._embedding_service.get_stats()
        return {}

    async def compact_context(self, session_id: str, max_tokens: int = 1000) -> str:
        """
        Compact context window by summarizing older entries.

        Args:
            session_id: Session ID
            max_tokens: Maximum tokens for summary

        Returns:
            Compacted context string
        """
        if self.backend:
            return await self.backend.summarize(session_id, max_tokens)
        return ""

    async def compact_memories(
        self,
        compaction_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Perform intelligent memory compaction using MemoryCompactor.
        
        Args:
            compaction_config: Optional configuration for compaction
            
        Returns:
            Compaction report
        """
        try:
            from .memory_compactor import (
                MemoryCompactor,
                MemorySnapshot,
                CompactionConfig,
                CompactionStrategy,
                CompactionLevel,
            )
        except ImportError:
            self.logger.warning("MemoryCompactor not available")
            return {"error": "MemoryCompactor not available"}
        
        # Get all memory entries
        entries = await self.query(query_text="", limit=10000)
        
        # Convert to snapshot format
        memory_entries = [
            {
                "id": e.id,
                "content": e.content,
                "created_at": e.created_at.timestamp() if e.created_at else time.time(),
                "importance": e.importance,
                "access_count": e.access_count,
                "session_id": e.session_id or "",
                "type": e.memory_type.value if e.memory_type else "unknown",
                "metadata": e.metadata,
            }
            for e in entries
        ]
        
        snapshot = MemorySnapshot(entries=memory_entries)
        
        # Configure compactor
        config = CompactionConfig(
            strategy=CompactionStrategy.HYBRID,
            level=CompactionLevel.MODERATE,
        )
        
        # Override with provided config
        if compaction_config:
            for key, value in compaction_config.items():
                if hasattr(config, key):
                    setattr(config, key, value)
        
        # Create and run compactor
        compactor = MemoryCompactor(
            embedding_service=getattr(self, "_embedding_service", None),
            llm_summarizer=getattr(self, "_llm_summarizer", None),
            config=config,
        )
        
        report = await compactor.compact(snapshot)
        
        # Delete entries that were removed
        if report.entries_removed > 0:
            compacted_ids = {e["id"] for e in snapshot.entries if e not in [e for e in 
                [entry for entry in memory_entries if entry not in []]]}
            
            # Get compacted snapshot entries
            compacted_snapshot = MemorySnapshot(entries=[])
            if hasattr(compactor, "_compact_hybrid"):
                compacted_entries = await compactor._compact_hybrid(snapshot)
                compacted_snapshot = MemorySnapshot(entries=compacted_entries)
            
            # Delete removed entries
            for entry in memory_entries:
                if not any(
                    ce.get("id") == entry["id"] 
                    for ce in compacted_snapshot.entries
                ):
                    await self.delete(entry["id"])
        
        self.logger.info(
            f"Memory compaction: {report.entries_removed} entries removed, "
            f"{report.tokens_saved} tokens saved ({report.reduction_ratio:.1%} reduction)"
        )
        
        return {
            "entries_before": report.original_entries,
            "entries_after": report.compacted_entries,
            "entries_removed": report.entries_removed,
            "tokens_saved": report.tokens_saved,
            "reduction_ratio": report.reduction_ratio,
            "strategy": report.strategy_used,
            "time_ms": report.time_elapsed_ms,
        }

    def _update_context_cache(self, session_id: str, entry: MemoryEntry) -> None:
        """Update context cache with new entry."""
        if session_id not in self._context_cache:
            self._context_cache[session_id] = []

        cache = self._context_cache[session_id]
        cache.append(entry)

        # Maintain max size
        if len(cache) > self._context_max_size:
            # Remove oldest entries
            cache.sort(key=lambda e: e.created_at)
            self._context_cache[session_id] = cache[-self._context_max_size:]

    async def clear_session(self, session_id: str) -> int:
        """
        Clear all memory for a session.

        Args:
            session_id: Session ID

        Returns:
            Number of entries deleted
        """
        # Query all entries for session
        entries = await self.query(query_text="", session_id=session_id, limit=1000)

        # Delete all entries
        count = 0
        for entry in entries:
            if await self.delete(entry.id):
                count += 1

        # Clear context cache
        if session_id in self._context_cache:
            del self._context_cache[session_id]

        return count

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        return {
            **self._stats,
            "backend_type": self.backend_type,
            "context_cache_size": len(self._context_cache),
        }
