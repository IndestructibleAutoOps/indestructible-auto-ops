import asyncio
import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import OrderedDict
import numpy as np


class EvictionPolicy(Enum):
    """Cache eviction policies."""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time To Live
    ADAPTIVE = "adaptive"  # Adaptive based on access patterns


class CacheLevel(Enum):
    """Cache level types."""
    EXACT = "exact"  # Exact match cache
    SEMANTIC = "semantic"  # Semantic similarity cache


@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    key: str
    value: Any
    embedding: Optional[List[float]] = None
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    ttl: Optional[int] = None
    size: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CacheStats:
    """Cache statistics."""
    hits: int = 0
    misses: int = 0
    writes: int = 0
    evictions: int = 0
    total_size: int = 0
    hit_rate: float = 0.0
    
    def update_hit_rate(self) -> None:
        """Update hit rate calculation."""
        total = self.hits + self.misses
        self.hit_rate = self.hits / total if total > 0 else 0.0


class SemanticCacheV2:
    """Enhanced semantic cache with multi-level caching and adaptive features.
    
    This cache provides:
    - Multi-level caching (exact match + semantic similarity)
    - Adaptive TTL based on access patterns
    - Multiple eviction policies (LRU, LFU, TTL, Adaptive)
    - Streaming response support
    - Cache warming and preloading
    - Detailed analytics and monitoring
    
    Features:
    1. Exact Match Cache: Fast exact key-based lookups
    2. Semantic Cache: Vector similarity-based lookups
    3. Adaptive TTL: Automatically adjusts TTL based on access frequency
    4. Multiple Eviction Policies: Configurable eviction strategies
    5. Streaming Support: Handle streaming responses efficiently
    6. Cache Warming: Preload frequently accessed items
    7. Analytics: Detailed statistics and metrics
    
    Usage:
        cache = SemanticCacheV2(
            cache_client=redis_client,
            embedding_service=embedding_service,
            max_size=10000,
            default_ttl=3600
        )
        
        # Set value
        cache.set("query1", "response1")
        
        # Get value
        value = cache.get("query1")
        
        # Semantic search
        similar = cache.find_similar("query2", threshold=0.85)
    """
    
    def __init__(
        self,
        cache_client: Any,
        embedding_service: Any,
        max_size: int = 10000,
        default_ttl: int = 3600,
        semantic_threshold: float = 0.85,
        eviction_policy: EvictionPolicy = EvictionPolicy.LRU,
        enable_exact_cache: bool = True,
        enable_semantic_cache: bool = True
    ):
        """Initialize semantic cache.
        
        Args:
            cache_client: Backend cache client (Redis, etc.)
            embedding_service: EmbeddingService instance
            max_size: Maximum number of entries
            default_ttl: Default TTL in seconds
            semantic_threshold: Similarity threshold for semantic matching
            eviction_policy: Eviction policy to use
            enable_exact_cache: Enable exact match cache
            enable_semantic_cache: Enable semantic similarity cache
        """
        self.cache_client = cache_client
        self.embedding_service = embedding_service
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.semantic_threshold = semantic_threshold
        self.eviction_policy = eviction_policy
        self.enable_exact_cache = enable_exact_cache
        self.enable_semantic_cache = enable_semantic_cache
        
        self.stats = CacheStats()
        self._exact_cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._semantic_index: Dict[str, List[float]] = {}
        self._access_history: List[Tuple[str, float]] = []
    
    def _generate_key(self, key: str) -> str:
        """Generate cache key.
        
        Args:
            key: Original key
            
        Returns:
            Hashed cache key
        """
        return hashlib.md5(key.encode()).hexdigest()
    
    def _serialize_value(self, value: Any) -> str:
        """Serialize value to string.
        
        Args:
            value: Value to serialize
            
        Returns:
            Serialized string
        """
        return json.dumps(value)
    
    def _deserialize_value(self, value: str) -> Any:
        """Deserialize value from string.
        
        Args:
            value: Serialized string
            
        Returns:
            Deserialized value
        """
        return json.loads(value)
    
    def _calculate_adaptive_ttl(self, entry: CacheEntry) -> int:
        """Calculate adaptive TTL based on access patterns.
        
        Args:
            entry: Cache entry
            
        Returns:
            Adaptive TTL value
        """
        if entry.access_count == 0:
            return self.default_ttl
        
        # More frequent access = longer TTL
        multiplier = min(3.0, 1.0 + (entry.access_count / 10.0))
        return int(self.default_ttl * multiplier)
    
    def _evict_entries(self, count: int = 1) -> None:
        """Evict entries based on configured policy.
        
        Args:
            count: Number of entries to evict
        """
        if self.eviction_policy == EvictionPolicy.LRU:
            self._evict_lru(count)
        elif self.eviction_policy == EvictionPolicy.LFU:
            self._evict_lfu(count)
        elif self.eviction_policy == EvictionPolicy.TTL:
            self._evict_ttl(count)
        elif self.eviction_policy == EvictionPolicy.ADAPTIVE:
            self._evict_adaptive(count)
    
    def _evict_lru(self, count: int) -> None:
        """Evict least recently used entries.
        
        Args:
            count: Number of entries to evict
        """
        evicted = 0
        while evicted < count and self._exact_cache:
            key, entry = self._exact_cache.popitem(last=False)
            self._remove_from_backend(key)
            evicted += 1
            self.stats.evictions += 1
    
    def _evict_lfu(self, count: int) -> None:
        """Evict least frequently used entries.
        
        Args:
            count: Number of entries to evict
        """
        # Sort by access count
        sorted_entries = sorted(
            self._exact_cache.items(),
            key=lambda x: x[1].access_count
        )
        
        evicted = 0
        for key, entry in sorted_entries[:count]:
            del self._exact_cache[key]
            self._remove_from_backend(key)
            evicted += 1
            self.stats.evictions += 1
    
    def _evict_ttl(self, count: int) -> None:
        """Evict entries with expired TTL.
        
        Args:
            count: Number of entries to evict
        """
        current_time = time.time()
        expired = []
        
        for key, entry in self._exact_cache.items():
            if entry.ttl and (current_time - entry.created_at) > entry.ttl:
                expired.append(key)
        
        for key in expired[:count]:
            del self._exact_cache[key]
            self._remove_from_backend(key)
            self.stats.evictions += 1
    
    def _evict_adaptive(self, count: int) -> None:
        """Evict entries using adaptive policy.
        
        Args:
            count: Number of entries to evict
        """
        # Combine LRU and LFU
        scored_entries = []
        current_time = time.time()
        
        for key, entry in self._exact_cache.items():
            # Calculate score: higher = more valuable to keep
            recency = (current_time - entry.last_accessed)
            frequency = entry.access_count
            
            score = frequency * 1000 - recency
            scored_entries.append((key, score))
        
        # Sort by score (lowest first)
        scored_entries.sort(key=lambda x: x[1])
        
        evicted = 0
        for key, score in scored_entries[:count]:
            del self._exact_cache[key]
            self._remove_from_backend(key)
            evicted += 1
            self.stats.evictions += 1
    
    def _remove_from_backend(self, key: str) -> None:
        """Remove entry from backend storage.
        
        Args:
            key: Cache key
        """
        try:
            self.cache_client.delete(key)
            
            # Remove from semantic index
            if key in self._semantic_index:
                del self._semantic_index[key]
        except Exception as e:
            print(f"Error removing from backend: {e}")
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None, 
            metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Set a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Optional TTL override
            metadata: Optional metadata
            
        Returns:
            True if successful
        """
        # Check cache size
        if len(self._exact_cache) >= self.max_size:
            self._evict_entries(1)
        
        # Generate embedding for semantic cache
        embedding = None
        if self.enable_semantic_cache and self.embedding_service:
            embedding_result = self.embedding_service.embed(str(key))
            embedding = embedding_result.embedding
        
        # Create cache entry
        entry = CacheEntry(
            key=key,
            value=value,
            embedding=embedding,
            ttl=ttl or self.default_ttl,
            metadata=metadata or {}
        )
        
        # Calculate size
        entry.size = len(self._serialize_value(value))
        
        # Store in exact cache
        self._exact_cache[key] = entry
        
        # Store in semantic index
        if embedding:
            self._semantic_index[key] = embedding
        
        # Store in backend
        try:
            cache_key = self._generate_key(key)
            serialized = self._serialize_value(value)
            
            # Use adaptive TTL
            effective_ttl = self._calculate_adaptive_ttl(entry)
            self.cache_client.setex(cache_key, effective_ttl, serialized)
            
            self.stats.writes += 1
            self.stats.total_size += entry.size
            
            return True
            
        except Exception as e:
            print(f"Error setting cache entry: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        # Check exact cache first
        if key in self._exact_cache:
            entry = self._exact_cache[key]
            
            # Update access tracking
            entry.last_accessed = time.time()
            entry.access_count += 1
            
            # Move to end for LRU
            self._exact_cache.move_to_end(key)
            
            self.stats.hits += 1
            self.stats.update_hit_rate()
            
            return entry.value
        
        # Try backend
        try:
            cache_key = self._generate_key(key)
            cached = self.cache_client.get(cache_key)
            
            if cached:
                value = self._deserialize_value(cached)
                
                # Reconstruct entry
                entry = CacheEntry(
                    key=key,
                    value=value,
                    last_accessed=time.time(),
                    access_count=1
                )
                
                self._exact_cache[key] = entry
                self.stats.hits += 1
                self.stats.update_hit_rate()
                
                return value
            
        except Exception as e:
            print(f"Error getting from cache: {e}")
        
        # Not found
        self.stats.misses += 1
        self.stats.update_hit_rate()
        
        return None
    
    def find_similar(self, query: str, threshold: Optional[float] = None, 
                     limit: int = 5) -> List[Tuple[str, Any, float]]:
        """Find semantically similar cached entries.
        
        Args:
            query: Query string
            threshold: Similarity threshold (overrides default)
            limit: Maximum number of results
            
        Returns:
            List of (key, value, similarity_score) tuples
        """
        if not self.enable_semantic_cache or not self.embedding_service:
            return []
        
        # Generate query embedding
        embedding_result = self.embedding_service.embed(query)
        query_embedding = np.array(embedding_result.embedding)
        
        # Calculate similarities
        similarities = []
        effective_threshold = threshold or self.semantic_threshold
        
        for key, cached_embedding in self._semantic_index.items():
            cached_emb = np.array(cached_embedding)
            
            # Cosine similarity
            similarity = np.dot(query_embedding, cached_emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(cached_emb)
            )
            
            if similarity >= effective_threshold:
                entry = self._exact_cache.get(key)
                if entry:
                    similarities.append((key, entry.value, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[2], reverse=True)
        
        return similarities[:limit]
    
    def delete(self, key: str) -> bool:
        """Delete a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        if key in self._exact_cache:
            entry = self._exact_cache[key]
            self.stats.total_size -= entry.size
            del self._exact_cache[key]
            
            # Remove from semantic index
            if key in self._semantic_index:
                del self._semantic_index[key]
        
        # Remove from backend
        try:
            cache_key = self._generate_key(key)
            self.cache_client.delete(cache_key)
            return True
        except Exception as e:
            print(f"Error deleting from cache: {e}")
            return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self._exact_cache.clear()
        self._semantic_index.clear()
        self._access_history.clear()
        self.stats = CacheStats()
        
        try:
            pattern = self._generate_key("*")
            for key in self.cache_client.scan_iter(match=pattern):
                self.cache_client.delete(key)
        except Exception as e:
            print(f"Error clearing cache: {e}")
    
    def warm_cache(self, entries: List[Tuple[str, Any]]) -> None:
        """Warm cache with preloaded entries.
        
        Args:
            entries: List of (key, value) tuples
        """
        for key, value in entries:
            self.set(key, value)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        return {
            "hits": self.stats.hits,
            "misses": self.stats.misses,
            "writes": self.stats.writes,
            "evictions": self.stats.evictions,
            "hit_rate": self.stats.hit_rate,
            "total_entries": len(self._exact_cache),
            "total_size": self.stats.total_size,
            "max_size": self.max_size,
            "eviction_policy": self.eviction_policy.value,
            "default_ttl": self.default_ttl,
            "semantic_threshold": self.semantic_threshold
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of cache.
        
        Returns:
            Health status dictionary
        """
        try:
            # Test cache operation
            test_key = "health_check"
            test_value = "ok"
            
            self.set(test_key, test_value)
            result = self.get(test_key)
            self.delete(test_key)
            
            return {
                "status": "healthy",
                "cache_connected": result == test_value,
                "entries": len(self._exact_cache),
                "hit_rate": self.stats.hit_rate
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }