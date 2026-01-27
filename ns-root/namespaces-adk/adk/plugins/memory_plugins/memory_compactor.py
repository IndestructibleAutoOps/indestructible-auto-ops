"""
Memory Compactor: Intelligent memory summarization and compaction for agents.

Features:
- Multi-strategy memory compaction (LLM-based, statistical, semantic clustering)
- Importance-based prioritization
- Temporal windowing for recent context
- Deduplication of similar memories
- Configurable compaction policies
- Integration with vector search for semantic analysis

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins/memory_plugins
@gl-semantic-anchor GL-00-PLUGINS_MEMORYPL_COMPACTOR
@gl-evidence-required false
GL Unified Charter Activated
"""

import asyncio
import hashlib
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .embedding_service import EmbeddingService
from .vector_search import VectorSearchQueryBuilder, FilterCondition, FilterOperator


class CompactionStrategy(Enum):
    """Memory compaction strategies."""
    LLM_SUMMARIZATION = "llm_summarization"
    STATISTICAL = "statistical"
    SEMANTIC_CLUSTERING = "semantic_clustering"
    TEMPORAL_WINDOWING = "temporal_windowing"
    IMPORTANCE_PRIORITY = "importance_priority"
    HYBRID = "hybrid"


class CompactionLevel(Enum):
    """Compaction intensity levels."""
    LIGHT = "light"  # 25% reduction
    MODERATE = "moderate"  # 50% reduction
    AGGRESSIVE = "aggressive"  # 75% reduction
    EXTREME = "extreme"  # 90% reduction


@dataclass
class CompactionConfig:
    """Configuration for memory compaction."""
    strategy: CompactionStrategy = CompactionStrategy.HYBRID
    level: CompactionLevel = CompactionLevel.MODERATE
    
    # Temporal settings
    keep_recent_hours: int = 24
    keep_important_days: int = 7
    
    # Importance settings
    min_importance: float = 0.3
    importance_decay_hours: int = 48
    
    # Deduplication settings
    dedup_similarity_threshold: float = 0.95
    min_duplicates: int = 2
    
    # Clustering settings
    cluster_min_size: int = 3
    cluster_similarity_threshold: float = 0.7
    
    # LLM summarization settings
    summary_max_tokens: int = 500
    summary_min_tokens: int = 50
    batch_size: int = 10
    
    # Retention settings
    retain_top_n: int = 100
    retain_min_per_session: int = 5


@dataclass
class MemorySnapshot:
    """A snapshot of memory entries."""
    entries: List[Dict[str, Any]]
    total_entries: int = 0
    total_tokens: int = 0
    oldest_timestamp: float = 0.0
    newest_timestamp: float = 0.0
    
    def __post_init__(self):
        if not self.oldest_timestamp and self.entries:
            timestamps = [e.get("created_at", time.time()) for e in self.entries]
            self.oldest_timestamp = min(timestamps)
            self.newest_timestamp = max(timestamps)
        self.total_entries = len(self.entries)
        self.total_tokens = sum(e.get("token_count", len(e.get("content", "")) // 4) for e in self.entries)


@dataclass
class CompactionReport:
    """Report of compaction operation."""
    original_entries: int
    original_tokens: int
    compacted_entries: int
    compacted_tokens: int
    reduction_ratio: float
    strategy_used: str
    time_elapsed_ms: float
    details: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def entries_removed(self) -> int:
        return self.original_entries - self.compacted_entries
    
    @property
    def tokens_saved(self) -> int:
        return self.original_tokens - self.compacted_tokens


class CompactionRule(ABC):
    """Abstract base class for compaction rules."""
    
    @abstractmethod
    async def should_compact(
        self,
        snapshot: MemorySnapshot,
        config: CompactionConfig,
    ) -> Tuple[bool, str]:
        """
        Determine if compaction should be performed.
        
        Returns:
            Tuple of (should_compact, reason)
        """
        pass


class TokenThresholdRule(CompactionRule):
    """Rule based on token count threshold."""
    
    def __init__(self, max_tokens: int = 10000):
        self.max_tokens = max_tokens
    
    async def should_compact(
        self,
        snapshot: MemorySnapshot,
        config: CompactionConfig,
    ) -> Tuple[bool, str]:
        if snapshot.total_tokens > self.max_tokens:
            return True, f"Token count ({snapshot.total_tokens}) exceeds threshold ({self.max_tokens})"
        return False, ""


class EntryCountRule(CompactionRule):
    """Rule based on entry count threshold."""
    
    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
    
    async def should_compact(
        self,
        snapshot: MemorySnapshot,
        config: CompactionConfig,
    ) -> Tuple[bool, str]:
        if snapshot.total_entries > self.max_entries:
            return True, f"Entry count ({snapshot.total_entries}) exceeds threshold ({self.max_entries})"
        return False, ""


class TimeSinceLastCompactionRule(CompactionRule):
    """Rule based on time since last compaction."""
    
    def __init__(self, min_hours: int = 24, last_compaction_time: float = 0.0):
        self.min_hours = min_hours
        self.last_compaction_time = last_compaction_time
    
    def set_last_compaction(self, timestamp: float) -> None:
        """Update the last compaction time."""
        self.last_compaction_time = timestamp
    
    async def should_compact(
        self,
        snapshot: MemorySnapshot,
        config: CompactionConfig,
    ) -> Tuple[bool, str]:
        if self.last_compaction_time == 0:
            return False, "No previous compaction"
        
        hours_since = (time.time() - self.last_compaction_time) / 3600
        if hours_since >= self.min_hours:
            return True, f"{hours_since:.1f} hours since last compaction"
        return False, ""


class MemoryCompactor:
    """
    Memory compaction engine with multiple strategies.
    
    Provides intelligent memory summarization and compaction
    to manage memory usage while preserving important information.
    """
    
    def __init__(
        self,
        embedding_service: Optional[EmbeddingService] = None,
        llm_summarizer: Optional[Callable[[List[str]], str]] = None,
        config: Optional[CompactionConfig] = None,
    ):
        """
        Initialize the memory compactor.
        
        Args:
            embedding_service: Service for semantic analysis
            llm_summarizer: Async function for LLM-based summarization
            config: Compaction configuration
        """
        self._embedding_service = embedding_service
        self._llm_summarizer = llm_summarizer
        self.config = config or CompactionConfig()
        self._logger = logging.getLogger(__name__)
        
        self._rules: List[CompactionRule] = []
        self._last_compaction_time = 0.0
        
        # Add default rules
        self.add_rule(TokenThresholdRule(max_tokens=10000))
        self.add_rule(EntryCountRule(max_entries=1000))
    
    def add_rule(self, rule: CompactionRule) -> None:
        """Add a compaction rule."""
        self._rules.append(rule)
    
    def remove_rule(self, rule_type: type) -> None:
        """Remove rules of a specific type."""
        self._rules = [r for r in self._rules if not isinstance(r, rule_type)]
    
    async def should_compact(self, snapshot: MemorySnapshot) -> Tuple[bool, str]:
        """
        Check if compaction should be performed.
        
        Args:
            snapshot: Current memory snapshot
            
        Returns:
            Tuple of (should_compact, reason)
        """
        for rule in self._rules:
            should, reason = await rule.should_compact(snapshot, self.config)
            if should:
                return True, reason
        
        return False, "No compaction rules triggered"
    
    async def compact(
        self,
        snapshot: MemorySnapshot,
    ) -> CompactionReport:
        """
        Perform memory compaction.
        
        Args:
            snapshot: Memory snapshot to compact
            
        Returns:
            Compaction report
        """
        start_time = time.time()
        
        # Check if compaction is needed
        should_compact, reason = await self.should_compact(snapshot)
        if not should_compact:
            return CompactionReport(
                original_entries=snapshot.total_entries,
                original_tokens=snapshot.total_tokens,
                compacted_entries=snapshot.total_entries,
                compacted_tokens=snapshot.total_tokens,
                reduction_ratio=0.0,
                strategy_used="none",
                time_elapsed_ms=(time.time() - start_time) * 1000,
                details={"reason": "Compaction not needed", "trigger_reason": reason},
            )
        
        # Apply compaction strategy
        strategy_method = {
            CompactionStrategy.LLM_SUMMARIZATION: self._compact_llm,
            CompactionStrategy.STATISTICAL: self._compact_statistical,
            CompactionStrategy.SEMANTIC_CLUSTERING: self._compact_semantic,
            CompactionStrategy.TEMPORAL_WINDOWING: self._compact_temporal,
            CompactionStrategy.IMPORTANCE_PRIORITY: self._compact_importance,
            CompactionStrategy.HYBRID: self._compact_hybrid,
        }[self.config.strategy]
        
        compacted_entries = await strategy_method(snapshot)
        
        # Calculate report
        compacted_snapshot = MemorySnapshot(entries=compacted_entries)
        
        report = CompactionReport(
            original_entries=snapshot.total_entries,
            original_tokens=snapshot.total_tokens,
            compacted_entries=compacted_snapshot.total_entries,
            compacted_tokens=compacted_snapshot.total_tokens,
            reduction_ratio=1.0 - (compacted_snapshot.total_entries / snapshot.total_entries),
            strategy_used=self.config.strategy.value,
            time_elapsed_ms=(time.time() - start_time) * 1000,
            details={
                "trigger_reason": reason,
                "strategy_config": {
                    "level": self.config.level.value,
                    "keep_recent_hours": self.config.keep_recent_hours,
                },
            },
        )
        
        self._last_compaction_time = time.time()
        
        return report
    
    async def _compact_llm(self, snapshot: MemorySnapshot) -> List[Dict[str, Any]]:
        """Compaction using LLM summarization."""
        if not self._llm_summarizer:
            self._logger.warning("LLM summarizer not available, falling back to statistical")
            return await self._compact_statistical(snapshot)
        
        # Group entries by session or category
        groups = self._group_entries(snapshot.entries)
        
        compacted = []
        for group_name, entries in groups.items():
            # Summarize each group
            texts = [e["content"] for e in entries]
            summary = await self._llm_summarizer(texts)
            
            # Create summary entry
            summary_entry = {
                "id": f"summary_{group_name}_{int(time.time())}",
                "content": summary,
                "type": "summary",
                "metadata": {
                    "compacted_from": len(entries),
                    "original_ids": [e["id"] for e in entries],
                    "group": group_name,
                    "strategy": "llm_summarization",
                },
                "created_at": time.time(),
                "importance": max(e.get("importance", 0.5) for e in entries),
            }
            compacted.append(summary_entry)
        
        return compacted
    
    async def _compact_statistical(self, snapshot: MemorySnapshot) -> List[Dict[str, Any]]:
        """Compaction using statistical methods."""
        # Score entries
        scored_entries = []
        now = time.time()
        
        for entry in snapshot.entries:
            score = self._calculate_importance_score(entry, now)
            scored_entries.append((score, entry))
        
        # Sort by score (highest first)
        scored_entries.sort(key=lambda x: x[0], reverse=True)
        
        # Determine target count based on level
        target_count = self._get_target_count(snapshot.total_entries)
        
        # Keep top entries
        compacted = [entry for score, entry in scored_entries[:target_count]]
        
        return compacted
    
    async def _compact_semantic(self, snapshot: MemorySnapshot) -> List[Dict[str, Any]]:
        """Compaction using semantic clustering."""
        if not self._embedding_service:
            self._logger.warning("Embedding service not available, falling back to statistical")
            return await self._compact_statistical(snapshot)
        
        # Generate embeddings for all entries
        texts = [e["content"] for e in snapshot.entries]
        embeddings = await self._embedding_service.embed_many(texts)
        
        # Cluster entries by similarity
        clusters = self._cluster_entries(snapshot.entries, embeddings)
        
        # Summarize or keep representative from each cluster
        compacted = []
        for cluster in clusters:
            if len(cluster) < self.config.cluster_min_size:
                # Keep all entries in small clusters
                compacted.extend(cluster)
            else:
                # Keep most important entry from cluster
                best = max(cluster, key=lambda e: e.get("importance", 0.5))
                compacted.append(best)
        
        return compacted
    
    async def _compact_temporal(self, snapshot: MemorySnapshot) -> List[Dict[str, Any]]:
        """Compaction using temporal windowing."""
        now = time.time()
        recent_cutoff = now - (self.config.keep_recent_hours * 3600)
        important_cutoff = now - (self.config.keep_important_days * 86400)
        
        # Keep recent entries and important old entries
        compacted = []
        for entry in snapshot.entries:
            created_at = entry.get("created_at", now)
            importance = entry.get("importance", 0.5)
            
            if created_at > recent_cutoff:
                # Recent, keep
                compacted.append(entry)
            elif importance >= self.config.min_importance and created_at > important_cutoff:
                # Important, keep
                compacted.append(entry)
        
        return compacted
    
    async def _compact_importance(self, snapshot: MemorySnapshot) -> List[Dict[str, Any]]:
        """Compaction based on importance scores."""
        now = time.time()
        
        # Score entries with time decay
        scored_entries = []
        for entry in snapshot.entries:
            base_score = entry.get("importance", 0.5)
            created_at = entry.get("created_at", now)
            age_hours = (now - created_at) / 3600
            
            # Apply decay
            decay_factor = max(0.1, 1.0 - (age_hours / self.config.importance_decay_hours))
            final_score = base_score * decay_factor
            
            scored_entries.append((final_score, entry))
        
        # Sort by score
        scored_entries.sort(key=lambda x: x[0], reverse=True)
        
        # Keep top entries
        target_count = self._get_target_count(snapshot.total_entries)
        compacted = [entry for score, entry in scored_entries[:target_count]]
        
        return compacted
    
    async def _compact_hybrid(self, snapshot: MemorySnapshot) -> List[Dict[str, Any]]:
        """Hybrid compaction combining multiple strategies."""
        # Step 1: Deduplicate similar entries
        deduplicated = await self._deduplicate(snapshot.entries)
        
        # Step 2: Apply temporal windowing
        temporal_snapshot = MemorySnapshot(entries=deduplicated)
        temporal_compacted = await self._compact_temporal(temporal_snapshot)
        
        # Step 3: Apply importance filtering
        importance_snapshot = MemorySnapshot(entries=temporal_compacted)
        importance_compacted = await self._compact_importance(importance_snapshot)
        
        # Step 4: Ensure minimum retention
        if len(importance_compacted) < self.config.retain_top_n:
            # Add back top entries from original
            sorted_by_importance = sorted(
                snapshot.entries,
                key=lambda e: e.get("importance", 0.5),
                reverse=True,
            )
            needed = self.config.retain_top_n - len(importance_compacted)
            importance_compacted.extend(sorted_by_importance[:needed])
        
        return importance_compacted
    
    async def _deduplicate(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate or highly similar entries."""
        if not self._embedding_service:
            return entries
        
        # Group by content hash (exact duplicates)
        hash_groups: Dict[str, List[Dict[str, Any]]] = {}
        for entry in entries:
            content_hash = hashlib.sha256(entry["content"].encode()).hexdigest()
            if content_hash not in hash_groups:
                hash_groups[content_hash] = []
            hash_groups[content_hash].append(entry)
        
        # Keep most important from each group
        deduplicated = []
        for group in hash_groups.values():
            if len(group) >= self.config.min_duplicates:
                # Keep most important
                best = max(group, key=lambda e: e.get("importance", 0.5))
                deduplicated.append(best)
            else:
                deduplicated.extend(group)
        
        return deduplicated
    
    def _group_entries(self, entries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group entries for summarization."""
        groups: Dict[str, List[Dict[str, Any]]] = {}
        
        for entry in entries:
            group_key = entry.get("session_id", entry.get("category", "default"))
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(entry)
        
        return groups
    
    def _cluster_entries(
        self,
        entries: List[Dict[str, Any]],
        embeddings: List[List[float]],
    ) -> List[List[Dict[str, Any]]]:
        """Cluster entries by semantic similarity."""
        if len(entries) <= self.config.cluster_min_size:
            return [[e] for e in entries]
        
        # Simple clustering: group by similarity threshold
        clusters: List[List[Dict[str, Any]]] = []
        assigned = set()
        
        for i, entry in enumerate(entries):
            if i in assigned:
                continue
            
            cluster = [entry]
            assigned.add(i)
            
            for j, other in enumerate(entries):
                if j in assigned:
                    continue
                
                # Calculate cosine similarity
                similarity = self._cosine_similarity(embeddings[i], embeddings[j])
                
                if similarity >= self.config.cluster_similarity_threshold:
                    cluster.append(other)
                    assigned.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    def _calculate_importance_score(self, entry: Dict[str, Any], now: float) -> float:
        """Calculate importance score for an entry."""
        base_importance = entry.get("importance", 0.5)
        access_count = entry.get("access_count", 0)
        created_at = entry.get("created_at", now)
        
        # Recency factor (more recent = higher score)
        age_hours = max(0.1, (now - created_at) / 3600)
        recency_factor = 1.0 / (1.0 + age_hours / 24)  # Decay over days
        
        # Access frequency factor
        access_factor = 1.0 + (access_count * 0.1)
        
        # Combined score
        score = base_importance * recency_factor * access_factor
        
        return min(1.0, score)
    
    def _get_target_count(self, original_count: int) -> int:
        """Get target count based on compaction level."""
        level_ratios = {
            CompactionLevel.LIGHT: 0.75,
            CompactionLevel.MODERATE: 0.50,
            CompactionLevel.AGGRESSIVE: 0.25,
            CompactionLevel.EXTREME: 0.10,
        }
        
        ratio = level_ratios.get(self.config.level, 0.5)
        return max(self.config.retain_top_n, int(original_count * ratio))
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between vectors."""
        import math
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(a * a for a in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


class AutomaticMemoryCompactor:
    """
    Automatic memory compactor that runs periodically.
    Monitors memory usage and compacts when needed.
    """
    
    def __init__(
        self,
        compactor: MemoryCompactor,
        check_interval_seconds: int = 3600,
        auto_compact: bool = True,
    ):
        """
        Initialize automatic compactor.
        
        Args:
            compactor: Memory compactor instance
            check_interval_seconds: How often to check for compaction
            auto_compact: Whether to automatically compact
        """
        self.compactor = compactor
        self.check_interval = check_interval_seconds
        self.auto_compact = auto_compact
        self._logger = logging.getLogger(__name__)
        self._running = False
        self._task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """Start automatic compaction."""
        if self._running:
            return
        
        self._running = True
        self._task = asyncio.create_task(self._compaction_loop())
        self._logger.info("Automatic memory compactor started")
    
    async def stop(self) -> None:
        """Stop automatic compaction."""
        if not self._running:
            return
        
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._logger.info("Automatic memory compactor stopped")
    
    async def _compaction_loop(self) -> None:
        """Main compaction loop."""
        while self._running:
            try:
                # Check if compaction is needed
                # This would require a method to get memory snapshot
                # For now, we'll just log
                await asyncio.sleep(self.check_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._logger.error(f"Compaction loop error: {e}")
                await asyncio.sleep(60)  # Wait before retrying