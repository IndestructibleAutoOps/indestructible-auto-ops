"""
Memory Compactor: Intelligent memory summarization and compression.

This module provides memory compaction capabilities including LLM-driven
summarization, importance decay, semantic deduplication, and sleep-time
memory consolidation.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins/memory_plugins
@gl-semantic-anchor GL-00-PLUGINS_MEMORYPL_COMPACT
@gl-evidence-required false
GL Unified Charter Activated
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol


# =============================================================================
# Protocols and Data Models
# =============================================================================


class MemoryType(Enum):
    """Types of memory storage."""

    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    VECTOR = "vector"


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
    importance: float = 1.0
    access_count: int = 0


class LLMClient(Protocol):
    """Protocol for LLM client interface."""

    async def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate text from prompt."""
        ...


class MemoryManagerProtocol(Protocol):
    """Protocol for memory manager interface."""

    async def add(
        self,
        content: str,
        memory_type: MemoryType,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        importance: float = 1.0,
    ) -> str:
        ...

    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        ...

    async def update(
        self,
        entry_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        ...

    async def delete(self, entry_id: str) -> bool:
        ...

    async def query(
        self,
        query_text: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        memory_type: Optional[MemoryType] = None,
        limit: int = 10,
    ) -> List[MemoryEntry]:
        ...

    async def get_context(self, session_id: str, max_tokens: int = 2000) -> str:
        ...


# =============================================================================
# Configuration
# =============================================================================


@dataclass
class CompactionConfig:
    """Configuration for memory compaction."""

    # Context window settings
    max_context_tokens: int = 4000
    summarization_threshold: int = 3000

    # Eviction settings
    eviction_ratio: float = 0.7  # Evict 70% of messages when compacting

    # Importance decay settings
    importance_decay_rate: float = 0.1  # Daily decay rate
    min_importance_threshold: float = 0.1
    access_boost_factor: float = 0.01  # Boost per access
    max_access_boost: float = 0.3

    # Deduplication settings
    deduplication_threshold: float = 0.95

    # Summarization settings
    summary_max_tokens: int = 500
    summary_importance: float = 0.8

    # Scheduling settings
    auto_compact_enabled: bool = True
    compact_interval_hours: int = 6
    decay_interval_hours: int = 24


@dataclass
class CompactionResult:
    """Result of a compaction operation."""

    success: bool = True
    operation: str = ""
    session_id: Optional[str] = None
    entries_processed: int = 0
    entries_affected: int = 0
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


# =============================================================================
# Memory Compactor Implementation
# =============================================================================


class MemoryCompactor:
    """
    Intelligent memory compaction and summarization.

    Features:
    - LLM-driven summarization of conversation history
    - Recursive summarization for long histories
    - Importance-based memory decay
    - Semantic deduplication
    - Memory consolidation during idle time (sleep-time compute)

    The compactor helps maintain efficient memory usage while preserving
    important information through intelligent compression strategies.

    Example:
        compactor = MemoryCompactor(
            memory_manager=memory_manager,
            llm_client=llm_client,
            config=CompactionConfig(
                max_context_tokens=4000,
                summarization_threshold=3000,
            ),
        )

        # Compact a session's memory
        result = await compactor.compact_session("session123")

        # Run full consolidation (during idle time)
        result = await compactor.consolidate("session123")
    """

    def __init__(
        self,
        memory_manager: MemoryManagerProtocol,
        llm_client: Optional[LLMClient] = None,
        config: Optional[CompactionConfig] = None,
    ):
        self.memory_manager = memory_manager
        self.llm_client = llm_client
        self.config = config or CompactionConfig()

        self._logger = logging.getLogger(__name__)

        # Statistics
        self._stats = {
            "compactions": 0,
            "summaries_created": 0,
            "entries_evicted": 0,
            "duplicates_removed": 0,
            "importance_updates": 0,
        }

    async def compact_session(
        self,
        session_id: str,
        force: bool = False,
    ) -> CompactionResult:
        """
        Compact memory for a session.

        This method:
        1. Checks if compaction is needed based on context size
        2. Summarizes older entries using LLM
        3. Stores summary as long-term memory
        4. Deletes summarized short-term entries

        Args:
            session_id: Session ID to compact
            force: Force compaction even if below threshold

        Returns:
            CompactionResult with details of the operation
        """
        self._logger.info(f"Starting compaction for session: {session_id}")

        try:
            # Get current context size
            context = await self.memory_manager.get_context(
                session_id,
                max_tokens=self.config.max_context_tokens * 2,
            )

            current_tokens = len(context.split())

            # Check if compaction needed
            if not force and current_tokens < self.config.summarization_threshold:
                return CompactionResult(
                    success=True,
                    operation="compact_session",
                    session_id=session_id,
                    details={
                        "compacted": False,
                        "reason": "below_threshold",
                        "current_tokens": current_tokens,
                        "threshold": self.config.summarization_threshold,
                    },
                )

            # Get all short-term memories for session
            entries = await self.memory_manager.query(
                query_text="",
                session_id=session_id,
                memory_type=MemoryType.SHORT_TERM,
                limit=1000,
            )

            if not entries:
                return CompactionResult(
                    success=True,
                    operation="compact_session",
                    session_id=session_id,
                    details={"compacted": False, "reason": "no_entries"},
                )

            # Sort by creation time
            entries.sort(key=lambda e: e.created_at)

            # Calculate eviction point
            eviction_count = int(len(entries) * self.config.eviction_ratio)
            entries_to_summarize = entries[:eviction_count]
            entries_to_keep = entries[eviction_count:]

            # Generate summary
            summary = await self._summarize_entries(entries_to_summarize)

            # Store summary as long-term memory
            summary_id = await self.memory_manager.add(
                content=summary,
                memory_type=MemoryType.LONG_TERM,
                session_id=session_id,
                metadata={
                    "type": "session_summary",
                    "summarized_count": len(entries_to_summarize),
                    "summarized_at": datetime.now().isoformat(),
                    "original_token_count": current_tokens,
                },
                importance=self.config.summary_importance,
            )

            # Delete summarized entries
            deleted_count = 0
            for entry in entries_to_summarize:
                if await self.memory_manager.delete(entry.id):
                    deleted_count += 1

            self._stats["compactions"] += 1
            self._stats["summaries_created"] += 1
            self._stats["entries_evicted"] += deleted_count

            return CompactionResult(
                success=True,
                operation="compact_session",
                session_id=session_id,
                entries_processed=len(entries),
                entries_affected=deleted_count,
                details={
                    "compacted": True,
                    "summary_id": summary_id,
                    "entries_summarized": len(entries_to_summarize),
                    "entries_deleted": deleted_count,
                    "entries_kept": len(entries_to_keep),
                    "original_tokens": current_tokens,
                    "summary_tokens": len(summary.split()),
                },
            )

        except Exception as e:
            self._logger.error(f"Compaction failed: {e}")
            return CompactionResult(
                success=False,
                operation="compact_session",
                session_id=session_id,
                error=str(e),
            )

    async def _summarize_entries(
        self,
        entries: List[MemoryEntry],
    ) -> str:
        """Summarize a list of memory entries using LLM."""
        # Build conversation text
        conversation = "\n\n".join(
            [
                f"[{entry.created_at.strftime('%Y-%m-%d %H:%M')}] {entry.content}"
                for entry in entries
            ]
        )

        # If no LLM client, use simple concatenation
        if not self.llm_client:
            self._logger.warning("No LLM client available, using simple summarization")
            return self._simple_summarize(entries)

        # Generate summary using LLM
        prompt = f"""Summarize the following conversation history, preserving:
1. Key decisions and outcomes
2. Important facts and preferences mentioned
3. Action items and commitments
4. Any errors or issues encountered

Be concise but comprehensive. Focus on information that would be useful for future interactions.

Conversation:
{conversation}

Summary:"""

        try:
            response = await self.llm_client.generate(
                prompt, max_tokens=self.config.summary_max_tokens
            )
            return response.strip()
        except Exception as e:
            self._logger.error(f"LLM summarization failed: {e}")
            return self._simple_summarize(entries)

    def _simple_summarize(self, entries: List[MemoryEntry]) -> str:
        """Simple summarization without LLM."""
        # Sort by importance
        sorted_entries = sorted(entries, key=lambda e: e.importance, reverse=True)

        # Take top entries up to token limit
        summary_parts = []
        total_tokens = 0

        for entry in sorted_entries:
            entry_tokens = len(entry.content.split())
            if total_tokens + entry_tokens > self.config.summary_max_tokens:
                break
            summary_parts.append(entry.content)
            total_tokens += entry_tokens

        return " | ".join(summary_parts)

    async def decay_importance(
        self,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> CompactionResult:
        """
        Apply importance decay to memories.

        Importance decays over time but is boosted by access frequency.
        Memories below the minimum threshold are deleted.

        Args:
            session_id: Optional session ID to limit decay
            user_id: Optional user ID to limit decay

        Returns:
            CompactionResult with decay statistics
        """
        self._logger.info("Starting importance decay")

        try:
            # Query all long-term memories
            entries = await self.memory_manager.query(
                query_text="",
                session_id=session_id,
                user_id=user_id,
                memory_type=MemoryType.LONG_TERM,
                limit=10000,
            )

            updated_count = 0
            deleted_count = 0

            for entry in entries:
                # Calculate age in days
                age_days = (datetime.now() - entry.created_at).days

                # Apply exponential decay
                decay_factor = (1 - self.config.importance_decay_rate) ** age_days
                new_importance = entry.importance * decay_factor

                # Boost importance based on access count
                access_boost = min(
                    entry.access_count * self.config.access_boost_factor,
                    self.config.max_access_boost,
                )
                new_importance = min(new_importance + access_boost, 1.0)

                if new_importance < self.config.min_importance_threshold:
                    # Delete low-importance memories
                    if await self.memory_manager.delete(entry.id):
                        deleted_count += 1
                        self._logger.debug(
                            f"Deleted low-importance entry: {entry.id} "
                            f"(importance: {new_importance:.3f})"
                        )
                elif abs(new_importance - entry.importance) > 0.01:
                    # Update importance if changed significantly
                    if await self.memory_manager.update(
                        entry.id,
                        metadata={
                            **entry.metadata,
                            "importance": new_importance,
                            "last_decay": datetime.now().isoformat(),
                        },
                    ):
                        updated_count += 1

            self._stats["importance_updates"] += updated_count
            self._stats["entries_evicted"] += deleted_count

            return CompactionResult(
                success=True,
                operation="decay_importance",
                session_id=session_id,
                entries_processed=len(entries),
                entries_affected=updated_count + deleted_count,
                details={
                    "entries_updated": updated_count,
                    "entries_deleted": deleted_count,
                    "decay_rate": self.config.importance_decay_rate,
                },
            )

        except Exception as e:
            self._logger.error(f"Importance decay failed: {e}")
            return CompactionResult(
                success=False,
                operation="decay_importance",
                session_id=session_id,
                error=str(e),
            )

    async def deduplicate(
        self,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> CompactionResult:
        """
        Remove semantically duplicate memories.

        Uses cosine similarity between embeddings to identify duplicates.
        Keeps the entry with higher importance or more recent creation.

        Args:
            session_id: Optional session ID to limit deduplication
            user_id: Optional user ID to limit deduplication

        Returns:
            CompactionResult with deduplication statistics
        """
        self._logger.info("Starting deduplication")

        try:
            # Query all memories with embeddings
            entries = await self.memory_manager.query(
                query_text="",
                session_id=session_id,
                user_id=user_id,
                memory_type=MemoryType.VECTOR,
                limit=10000,
            )

            # Filter entries with embeddings
            entries_with_embeddings = [e for e in entries if e.embedding]

            if len(entries_with_embeddings) < 2:
                return CompactionResult(
                    success=True,
                    operation="deduplicate",
                    session_id=session_id,
                    details={
                        "duplicates_found": 0,
                        "duplicates_removed": 0,
                        "reason": "insufficient_entries",
                    },
                )

            # Find duplicates using cosine similarity
            duplicates = []
            processed = set()

            for i, entry1 in enumerate(entries_with_embeddings):
                if entry1.id in processed:
                    continue

                for entry2 in entries_with_embeddings[i + 1 :]:
                    if entry2.id in processed:
                        continue

                    similarity = self._cosine_similarity(
                        entry1.embedding,
                        entry2.embedding,
                    )

                    if similarity >= self.config.deduplication_threshold:
                        # Determine which to keep
                        if entry1.importance > entry2.importance:
                            to_delete = entry2
                        elif entry1.importance < entry2.importance:
                            to_delete = entry1
                        elif entry1.created_at > entry2.created_at:
                            to_delete = entry2
                        else:
                            to_delete = entry1

                        duplicates.append(to_delete.id)
                        processed.add(to_delete.id)

                        self._logger.debug(
                            f"Found duplicate: {to_delete.id} "
                            f"(similarity: {similarity:.3f})"
                        )

            # Remove duplicates
            removed_count = 0
            for entry_id in duplicates:
                if await self.memory_manager.delete(entry_id):
                    removed_count += 1

            self._stats["duplicates_removed"] += removed_count

            return CompactionResult(
                success=True,
                operation="deduplicate",
                session_id=session_id,
                entries_processed=len(entries_with_embeddings),
                entries_affected=removed_count,
                details={
                    "duplicates_found": len(duplicates),
                    "duplicates_removed": removed_count,
                    "similarity_threshold": self.config.deduplication_threshold,
                },
            )

        except Exception as e:
            self._logger.error(f"Deduplication failed: {e}")
            return CompactionResult(
                success=False,
                operation="deduplicate",
                session_id=session_id,
                error=str(e),
            )

    def _cosine_similarity(
        self,
        vec1: List[float],
        vec2: List[float],
    ) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    async def consolidate(
        self,
        session_id: str,
    ) -> CompactionResult:
        """
        Consolidate memories during idle time (sleep-time compute).

        This method performs comprehensive memory maintenance:
        1. Compacts short-term memory
        2. Applies importance decay
        3. Removes duplicates
        4. Extracts and stores key facts (if LLM available)

        Best called during periods of low activity to improve
        memory quality without impacting response latency.

        Args:
            session_id: Session ID to consolidate

        Returns:
            CompactionResult with consolidation statistics
        """
        self._logger.info(f"Starting consolidation for session: {session_id}")

        results = {
            "session_id": session_id,
            "consolidated_at": datetime.now().isoformat(),
            "operations": [],
        }

        try:
            # Step 1: Compact short-term memory
            compaction_result = await self.compact_session(session_id)
            results["operations"].append(
                {
                    "operation": "compact_session",
                    "success": compaction_result.success,
                    "details": compaction_result.details,
                }
            )

            # Step 2: Apply importance decay
            decay_result = await self.decay_importance(session_id)
            results["operations"].append(
                {
                    "operation": "decay_importance",
                    "success": decay_result.success,
                    "details": decay_result.details,
                }
            )

            # Step 3: Remove duplicates
            dedup_result = await self.deduplicate(session_id)
            results["operations"].append(
                {
                    "operation": "deduplicate",
                    "success": dedup_result.success,
                    "details": dedup_result.details,
                }
            )

            # Calculate totals
            total_affected = (
                compaction_result.entries_affected
                + decay_result.entries_affected
                + dedup_result.entries_affected
            )

            all_success = all(
                r.success for r in [compaction_result, decay_result, dedup_result]
            )

            return CompactionResult(
                success=all_success,
                operation="consolidate",
                session_id=session_id,
                entries_affected=total_affected,
                details=results,
            )

        except Exception as e:
            self._logger.error(f"Consolidation failed: {e}")
            return CompactionResult(
                success=False,
                operation="consolidate",
                session_id=session_id,
                error=str(e),
                details=results,
            )

    def get_stats(self) -> Dict[str, Any]:
        """Get compactor statistics."""
        return {
            **self._stats,
            "config": {
                "max_context_tokens": self.config.max_context_tokens,
                "summarization_threshold": self.config.summarization_threshold,
                "eviction_ratio": self.config.eviction_ratio,
                "importance_decay_rate": self.config.importance_decay_rate,
                "deduplication_threshold": self.config.deduplication_threshold,
            },
        }


# =============================================================================
# Mock Classes for Testing
# =============================================================================


class MockLLMClient:
    """Mock LLM client for testing."""

    async def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate a mock summary."""
        return "This is a mock summary of the conversation history."


class MockMemoryManager:
    """Mock memory manager for testing."""

    def __init__(self):
        self._storage: Dict[str, MemoryEntry] = {}

    async def add(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.LONG_TERM,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        importance: float = 1.0,
    ) -> str:
        import uuid

        entry_id = str(uuid.uuid4())
        entry = MemoryEntry(
            id=entry_id,
            content=content,
            memory_type=memory_type,
            session_id=session_id,
            user_id=user_id,
            metadata=metadata or {},
            importance=importance,
        )
        self._storage[entry_id] = entry
        return entry_id

    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        return self._storage.get(entry_id)

    async def update(
        self,
        entry_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        if entry_id not in self._storage:
            return False
        entry = self._storage[entry_id]
        if content:
            entry.content = content
        if metadata:
            entry.metadata.update(metadata)
        return True

    async def delete(self, entry_id: str) -> bool:
        if entry_id in self._storage:
            del self._storage[entry_id]
            return True
        return False

    async def query(
        self,
        query_text: str,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        memory_type: Optional[MemoryType] = None,
        limit: int = 10,
    ) -> List[MemoryEntry]:
        results = []
        for entry in self._storage.values():
            if session_id and entry.session_id != session_id:
                continue
            if user_id and entry.user_id != user_id:
                continue
            if memory_type and entry.memory_type != memory_type:
                continue
            results.append(entry)
            if len(results) >= limit:
                break
        return results

    async def get_context(self, session_id: str, max_tokens: int = 2000) -> str:
        entries = await self.query("", session_id=session_id)
        return " ".join(e.content for e in entries)


# =============================================================================
# Usage Example
# =============================================================================

if __name__ == "__main__":
    import asyncio

    async def main():
        # Initialize with mock components
        memory_manager = MockMemoryManager()
        llm_client = MockLLMClient()

        compactor = MemoryCompactor(
            memory_manager=memory_manager,
            llm_client=llm_client,
            config=CompactionConfig(
                max_context_tokens=4000,
                summarization_threshold=100,  # Low threshold for testing
                eviction_ratio=0.7,
            ),
        )

        # Add some test memories
        session_id = "test_session"
        for i in range(10):
            await memory_manager.add(
                content=f"This is test message {i} with some content.",
                memory_type=MemoryType.SHORT_TERM,
                session_id=session_id,
                importance=0.5 + (i * 0.05),
            )

        print(f"Added {len(memory_manager._storage)} entries")

        # Run compaction
        result = await compactor.compact_session(session_id, force=True)
        print(f"\nCompaction result: {result}")

        # Run consolidation
        result = await compactor.consolidate(session_id)
        print(f"\nConsolidation result: {result}")

        # Get stats
        stats = compactor.get_stats()
        print(f"\nCompactor stats: {stats}")

    asyncio.run(main())