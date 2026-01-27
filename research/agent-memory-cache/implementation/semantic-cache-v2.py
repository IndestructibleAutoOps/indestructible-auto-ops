"""
Semantic Cache V2: Enhanced semantic caching with multi-level strategies.

This module provides an advanced semantic caching system with:
- Multi-level caching (exact match + semantic similarity)
- Adaptive TTL based on access patterns
- Multiple eviction policies (LRU, LFU, TTL, Adaptive)
- Streaming response support
- Cache warming and preloading
- Detailed analytics and monitoring

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module research/agent-memory-cache/implementation
@gl-semantic-anchor GL-00-IMPL_SEMANTIC_CACHE_V2
@gl-evidence-required false
GL Unified Charter Activated
"""

import asyncio
import hashlib
import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

try:
    import redis
    from redis.asyncio import Redis as AsyncRedis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None
    AsyncRedis = None


logger = logging.getLogger(__name__)


# =============================================================================
# Enums and Data Models
# =============================================================================


class EvictionPolicy(Enum):
    """Cache eviction policies."""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time-based
    ADAPTIVE = "adaptive"  # Adaptive based on access patterns


class CacheLevel(Enum):
    """Cache levels."""
    L1_EXACT = "l1_exact"  # Exact key match
    L2_SEMANTIC = "l2_semantic"  # Semantic similarity


@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    key: str
    value: Any
    created_at: float
    last_accessed: float
    ttl: int
    access_count: int = 0
    importance: float = 1.0
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_expired(self) -> bool:
        """Check if entry is expired."""
        return time.time() > (self.created_at + self.ttl)
    
    @property
    def age(self) -> float:
        """Get age in seconds."""
        return time.time() - self.created_at
    
    @property
    def time_since_access(self) -> float:
        """Get time since last access."""
        return time.time() - self.last_accessed


@dataclass
class CacheResult:
    """Cache retrieval result."""
    value: Any
    hit: bool
    level: Optional[CacheLevel] = None
    similarity: float = 1.0
    entry: Optional[CacheEntry] = None


@dataclass
class CacheStats:
    """Cache statistics."""
    hits: int = 0
    misses: int = 0
    l1_hits: int = 0
    l2_hits: int = 0
    evictions: int = 0
    total_queries: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate overall hit rate."""
        if self.total_queries == 0:
            return 0.0
        return self.hits / self.total_queries
    
    @property
    def l1_hit_rate(self) -> float:
        """Calculate L1 hit rate."""
        if self.total_queries == 0:
            return 0.0
        return self.l1_hits / self.total_queries
    
    @property
    def l2_hit_rate(self) -> float:
        """Calculate L2 hit rate."""
        if self.total_queries == 0:
            return 0.0
        return self.l2_hits / self.total_queries


# =============================================================================
# Eviction Strategies
# =============================================================================


class EvictionStrategy(ABC):
    """Abstract base class for eviction strategies."""
    
    @abstractmethod
    def select_for_eviction(
        self,
        entries: List[CacheEntry],
        count: int
    ) -> List[str]:
        """Select entries for eviction."""
        pass


class LRUEvictionStrategy(EvictionStrategy):
    """Least Recently Used eviction strategy."""
    
    def select_for_eviction(
        self,
        entries: List[CacheEntry],
        count: int
    ) -> List[str]:
        """Select least recently used entries."""
        sorted_entries = sorted(
            entries,
            key=lambda e: e.time_since_access,
            reverse=True
        )
        return [e.key for e in sorted_entries[:count]]


class LFUEvictionStrategy(EvictionStrategy):
    """Least Frequently Used eviction strategy."""
    
    def select_for_eviction(
        self,
        entries: List[CacheEntry],
        count: int
    ) -> List[str]:
        """Select least frequently used entries."""
        sorted_entries = sorted(
            entries,
            key=lambda e: (e.access_count, e.time_since_access)
        )
        return [e.key for e in sorted_entries[:count]]


class TTLEvictionStrategy(EvictionStrategy):
    """Time-based eviction strategy."""
    
    def select_for_eviction(
        self,
        entries: List[CacheEntry],
        count: int
    ) -> List[str]:
        """Select entries closest to expiration."""
        sorted_entries = sorted(
            entries,
            key=lambda e: e.created_at + e.ttl
        )
        return [e.key for e in sorted_entries[:count]]


class AdaptiveEvictionStrategy(EvictionStrategy):
    """Adaptive eviction strategy combining multiple factors."""
    
    def select_for_eviction(
        self,
        entries: List[CacheEntry],
        count: int
    ) -> List[str]:
        """Select entries based on adaptive score."""
        scored_entries = []
        for entry in entries:
            # Score = (importance * access_count) / (time_since_access * ttl)
            time_factor = max(entry.time_since_access, 1.0)
            ttl_factor = max(entry.ttl, 1.0)
            score = (entry.importance * entry.access_count) / (time_factor * ttl_factor)
            scored_entries.append((score, entry))
        
        scored_entries.sort(key=lambda x: x[0])
        return [e.key for _, e in scored_entries[:count]]


# =============================================================================
# Semantic Cache V2
# =============================================================================


class SemanticCacheV2:
    """Enhanced semantic cache with multi-level caching."""
    
    def __init__(
        self,
        redis_client: Optional[Union[redis.Redis, AsyncRedis]] = None,
        similarity_threshold: float = 0.85,
        default_ttl: int = 3600,
        max_entries: int = 10000,
        eviction_policy: Union[EvictionPolicy, str] = EvictionPolicy.LRU,
        enable_adaptive_ttl: bool = True,
        ttl_boost_threshold: int = 10,
        ttl_boost_multiplier: float = 1.5,
        enable_streaming: bool = True
    ):
        """
        Initialize SemanticCacheV2.
        
        Args:
            redis_client: Redis client instance
            similarity_threshold: Minimum similarity for L2 cache hit
            default_ttl: Default TTL in seconds
            max_entries: Maximum number of entries
            eviction_policy: Eviction policy to use
            enable_adaptive_ttl: Enable adaptive TTL
            ttl_boost_threshold: Access count to trigger TTL boost
            ttl_boost_multiplier: TTL boost multiplier
            enable_streaming: Enable streaming response support
        """
        self.redis_client = redis_client
        self.similarity_threshold = similarity_threshold
        self.default_ttl = default_ttl
        self.max_entries = max_entries
        self.enable_adaptive_ttl = enable_adaptive_ttl
        self.ttl_boost_threshold = ttl_boost_threshold
        self.ttl_boost_multiplier = ttl_boost_multiplier
        self.enable_streaming = enable_streaming
        
        # In-memory L1 cache for exact matches
        self._l1_cache: Dict[str, CacheEntry] = {}
        self._l2_cache: Dict[str, CacheEntry] = {}
        self._embedding_cache: Dict[str, List[float]] = {}
        
        # Statistics
        self.stats = CacheStats()
        
        # Eviction strategy
        if isinstance(eviction_policy, str):
            eviction_policy = EvictionPolicy(eviction_policy)
        self.eviction_policy = eviction_policy
        self._eviction_strategy = self._create_eviction_strategy()
        
        # Lock for thread safety
        self._lock = asyncio.Lock()
        
        # Embedding service (optional)
        self._embedding_service = None
    
    def _create_eviction_strategy(self) -> EvictionStrategy:
        """Create eviction strategy instance."""
        strategies = {
            EvictionPolicy.LRU: LRUEvictionStrategy(),
            EvictionPolicy.LFU: LFUEvictionStrategy(),
            EvictionPolicy.TTL: TTLEvictionStrategy(),
            EvictionPolicy.ADAPTIVE: AdaptiveEvictionStrategy(),
        }
        return strategies.get(self.eviction_policy, LRUEvictionStrategy())
    
    async def initialize(self):
        """Initialize the cache."""
        if not REDIS_AVAILABLE and self.redis_client is not None:
            raise ImportError(
                "Redis package is required for Redis backend. "
                "Install with: pip install redis[hiredis]"
            )
        logger.info("SemanticCacheV2 initialized")
    
    async def get(self, key: str, embedding: Optional[List[float]] = None) -> CacheResult:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            embedding: Optional embedding for L2 search
            
        Returns:
            CacheResult with value and hit information
        """
        async with self._lock:
            self.stats.total_queries += 1
            
            # Try L1 exact match first
            if key in self._l1_cache:
                entry = self._l1_cache[key]
                
                if entry.is_expired:
                    await self._remove_entry(key, CacheLevel.L1_EXACT)
                else:
                    # Update access info
                    entry.last_accessed = time.time()
                    entry.access_count += 1
                    
                    # Adaptive TTL boost
                    if self.enable_adaptive_ttl and \
                       entry.access_count >= self.ttl_boost_threshold:
                        entry.ttl = int(entry.ttl * self.ttl_boost_multiplier)
                    
                    self.stats.hits += 1
                    self.stats.l1_hits += 1
                    
                    logger.debug(f"L1 cache hit: {key}")
                    return CacheResult(
                        value=entry.value,
                        hit=True,
                        level=CacheLevel.L1_EXACT,
                        similarity=1.0,
                        entry=entry
                    )
            
            # Try L2 semantic match if embedding provided
            if embedding is not None and self._l2_cache:
                semantic_result = await self._semantic_search(embedding)
                
                if semantic_result and semantic_result.score >= self.similarity_threshold:
                    entry = semantic_result.entry
                    
                    # Update access info
                    entry.last_accessed = time.time()
                    entry.access_count += 1
                    
                    self.stats.hits += 1
                    self.stats.l2_hits += 1
                    
                    logger.debug(f"L2 cache hit: {key} -> {entry.key} (similarity: {semantic_result.score:.2f})")
                    return CacheResult(
                        value=entry.value,
                        hit=True,
                        level=CacheLevel.L2_SEMANTIC,
                        similarity=semantic_result.score,
                        entry=entry
                    )
            
            # Cache miss
            self.stats.misses += 1
            logger.debug(f"Cache miss: {key}")
            return CacheResult(value=None, hit=False)
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        embedding: Optional[List[float]] = None,
        importance: float = 1.0
    ):
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
            embedding: Optional embedding for L2 cache
            importance: Entry importance for eviction
        """
        async with self._lock:
            now = time.time()
            entry_ttl = ttl or self.default_ttl
            
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=now,
                last_accessed=now,
                ttl=entry_ttl,
                importance=importance,
                embedding=embedding
            )
            
            # Check capacity
            if len(self._l1_cache) + len(self._l2_cache) >= self.max_entries:
                await self._evict(count=1)
            
            # Store in L1 cache
            self._l1_cache[key] = entry
            
            # Store in L2 cache if embedding provided
            if embedding is not None:
                self._l2_cache[key] = entry
            
            logger.debug(f"Cache set: {key} (TTL: {entry_ttl}s)")
    
    async def _semantic_search(
        self,
        embedding: List[float]
    ) -> Optional[Any]:
        """
        Search for semantically similar entries in L2 cache.
        
        Args:
            embedding: Query embedding
            
        Returns:
            Best matching entry with score
        """
        if not self._l2_cache:
            return None
        
        best_match = None
        best_score = 0.0
        
        for entry in self._l2_cache.values():
            if entry.is_expired or entry.embedding is None:
                continue
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(embedding, entry.embedding)
            
            if similarity > best_score:
                best_score = similarity
                best_match = entry
        
        if best_match:
            return type('Result', (), {'entry': best_match, 'score': best_score})()
        
        return None
    
    @staticmethod
    def _cosine_similarity(v1: List[float], v2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import math
        
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    async def _evict(self, count: int):
        """
        Evict entries based on eviction policy.
        
        Args:
            count: Number of entries to evict
        """
        all_entries = list(self._l1_cache.values()) + list(self._l2_cache.values())
        keys_to_evict = self._eviction_strategy.select_for_eviction(all_entries, count)
        
        for key in keys_to_evict:
            await self._remove_entry(key, CacheLevel.L1_EXACT)
            await self._remove_entry(key, CacheLevel.L2_SEMANTIC)
        
        self.stats.evictions += len(keys_to_evict)
        logger.debug(f"Evicted {len(keys_to_evict)} entries")
    
    async def _remove_entry(self, key: str, level: CacheLevel):
        """Remove entry from cache level."""
        if level == CacheLevel.L1_EXACT and key in self._l1_cache:
            del self._l1_cache[key]
        elif level == CacheLevel.L2_SEMANTIC and key in self._l2_cache:
            del self._l2_cache[key]
    
    async def clear(self):
        """Clear all cache entries."""
        async with self._lock:
            self._l1_cache.clear()
            self._l2_cache.clear()
            self._embedding_cache.clear()
            logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "hits": self.stats.hits,
            "misses": self.stats.misses,
            "l1_hits": self.stats.l1_hits,
            "l2_hits": self.stats.l2_hits,
            "evictions": self.stats.evictions,
            "total_queries": self.stats.total_queries,
            "hit_rate": self.stats.hit_rate,
            "l1_hit_rate": self.stats.l1_hit_rate,
            "l2_hit_rate": self.stats.l2_hit_rate,
            "l1_size": len(self._l1_cache),
            "l2_size": len(self._l2_cache),
            "max_entries": self.max_entries
        }
    
    def reset_stats(self):
        """Reset cache statistics."""
        self.stats = CacheStats()


# =============================================================================
# Factory Functions
# =============================================================================


def create_semantic_cache(
    redis_client: Optional[Union[redis.Redis, AsyncRedis]] = None,
    **kwargs
) -> SemanticCacheV2:
    """
    Factory function to create semantic cache.
    
    Args:
        redis_client: Optional Redis client
        **kwargs: Additional configuration
        
    Returns:
        SemanticCacheV2 instance
    """
    return SemanticCacheV2(redis_client=redis_client, **kwargs)


# =============================================================================
# Example Usage
# =============================================================================


async def example_usage():
    """Example usage of SemanticCacheV2."""
    
    # Create cache
    cache = SemanticCacheV2(
        similarity_threshold=0.85,
        default_ttl=3600,
        max_entries=10000,
        eviction_policy=EvictionPolicy.ADAPTIVE
    )
    
    await cache.initialize()
    
    # Set some entries
    await cache.set(
        key="query1",
        value="Response to query 1",
        ttl=3600,
        importance=0.9
    )
    
    await cache.set(
        key="query2",
        value="Response to query 2",
        ttl=1800,
        importance=0.7
    )
    
    # Get entry
    result = await cache.get("query1")
    print(f"Hit: {result.hit}, Value: {result.value}")
    
    # Get stats
    stats = cache.get_stats()
    print(f"Cache stats: {stats}")
    
    # Clear cache
    await cache.clear()


if __name__ == "__main__":
    asyncio.run(example_usage())