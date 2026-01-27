import asyncio
import hashlib
import json
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import OrderedDict
import numpy as np


class CacheLevel(Enum):
    """Cache level hierarchy."""
    L1 = "l1"  # In-memory cache (fastest)
    L2 = "l2"  # Redis cache (fast)
    L3 = "l3"  # Vector database (semantic search)


class CacheStrategy(Enum):
    """Cache retrieval strategies."""
    EXACT_FIRST = "exact_first"  # Try exact match, then semantic
    SEMANTIC_FIRST = "semantic_first"  # Try semantic match, then exact
    PARALLEL = "parallel"  # Query both levels in parallel
    HYBRID = "hybrid"  # Combine exact and semantic results


@dataclass
class LayerConfig:
    """Configuration for a cache layer."""
    name: str
    level: CacheLevel
    enabled: bool = True
    max_size: int = 1000
    ttl: int = 3600
    priority: int = 0
    backend: Optional[Any] = None


@dataclass
class CacheLayer:
    """Represents a cache layer."""
    config: LayerConfig
    data: Dict[str, Any] = field(default_factory=dict)
    access_count: int = 0
    hit_count: int = 0
    miss_count: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate hit rate for this layer."""
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0.0


@dataclass
class SemanticCacheResult:
    """Result from semantic cache lookup."""
    key: str
    value: Any
    found: bool
    layer: Optional[CacheLevel] = None
    similarity_score: Optional[float] = None
    retrieval_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class SemanticCacheLayer:
    """Multi-layer semantic cache system for AI agent responses.
    
    This cache provides:
    - Hierarchical caching across multiple levels (L1, L2, L3)
    - Exact match and semantic similarity caching
    - Multiple retrieval strategies
    - Automatic cache promotion and demotion
    - Detailed metrics and analytics
    - Configurable eviction policies
    
    Architecture:
    - L1 Cache: In-memory dictionary for ultra-fast access
    - L2 Cache: Redis for distributed caching
    - L3 Cache: Vector database for semantic similarity search
    
    Usage:
        cache = SemanticCacheLayer(
            embedding_service=embedding_service,
            l1_max_size=1000,
            l2_client=redis_client,
            l3_client=vector_db_client
        )
        
        # Set value
        cache.set("query", "response")
        
        # Get value with semantic fallback
        result = cache.get("similar query", strategy=CacheStrategy.SEMANTIC_FIRST)
    """
    
    def __init__(
        self,
        embedding_service: Any,
        l1_max_size: int = 1000,
        l2_client: Optional[Any] = None,
        l3_client: Optional[Any] = None,
        default_ttl: int = 3600,
        semantic_threshold: float = 0.85,
        strategy: CacheStrategy = CacheStrategy.EXACT_FIRST
    ):
        """Initialize semantic cache layer.
        
        Args:
            embedding_service: EmbeddingService instance
            l1_max_size: Maximum size for L1 cache
            l2_client: Optional Redis client for L2
            l3_client: Optional vector DB client for L3
            default_ttl: Default TTL for cache entries
            semantic_threshold: Similarity threshold for semantic matching
            strategy: Default cache retrieval strategy
        """
        self.embedding_service = embedding_service
        self.l1_max_size = l1_max_size
        self.default_ttl = default_ttl
        self.semantic_threshold = semantic_threshold
        self.strategy = strategy
        
        # Initialize layers
        self.l1_cache: OrderedDict[str, Tuple[Any, float, Dict[str, Any]]] = OrderedDict()
        self.l2_client = l2_client
        self.l3_client = l3_client
        
        # Metrics
        self.total_hits = 0
        self.total_misses = 0
        self.layer_stats: Dict[CacheLevel, Dict[str, int]] = {
            CacheLevel.L1: {"hits": 0, "misses": 0},
            CacheLevel.L2: {"hits": 0, "misses": 0},
            CacheLevel.L3: {"hits": 0, "misses": 0}
        }
    
    def _generate_key(self, key: str) -> str:
        """Generate cache key.
        
        Args:
            key: Original key
            
        Returns:
            Hashed cache key
        """
        return hashlib.md5(key.encode()).hexdigest()
    
    def _serialize(self, value: Any) -> str:
        """Serialize value to string.
        
        Args:
            value: Value to serialize
            
        Returns:
            Serialized string
        """
        return json.dumps(value)
    
    def _deserialize(self, value: str) -> Any:
        """Deserialize value from string.
        
        Args:
            value: Serialized string
            
        Returns:
            Deserialized value
        """
        return json.loads(value)
    
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
        effective_ttl = ttl or self.default_ttl
        
        # Set in L1 cache
        self._set_l1(key, value, effective_ttl, metadata or {})
        
        # Set in L2 cache if available
        if self.l2_client:
            self._set_l2(key, value, effective_ttl, metadata or {})
        
        # Set in L3 cache if available
        if self.l3_client:
            self._set_l3(key, value, effective_ttl, metadata or {})
        
        return True
    
    def _set_l1(self, key: str, value: Any, ttl: int, metadata: Dict[str, Any]) -> None:
        """Set value in L1 cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: TTL in seconds
            metadata: Optional metadata
        """
        # Evict if necessary
        if len(self.l1_cache) >= self.l1_max_size:
            self.l1_cache.popitem(last=False)
        
        # Store value with timestamp
        self.l1_cache[key] = (value, time.time() + ttl, metadata)
    
    def _set_l2(self, key: str, value: Any, ttl: int, metadata: Dict[str, Any]) -> None:
        """Set value in L2 cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: TTL in seconds
            metadata: Optional metadata
        """
        try:
            cache_key = self._generate_key(key)
            payload = {
                "value": self._serialize(value),
                "metadata": metadata
            }
            self.l2_client.setex(cache_key, ttl, json.dumps(payload))
        except Exception as e:
            print(f"Error setting L2 cache: {e}")
    
    def _set_l3(self, key: str, value: Any, ttl: int, metadata: Dict[str, Any]) -> None:
        """Set value in L3 cache with embedding.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: TTL in seconds
            metadata: Optional metadata
        """
        try:
            # Generate embedding for semantic search
            embedding_result = self.embedding_service.embed(str(key))
            embedding = embedding_result.embedding
            
            if not embedding:
                return
            
            # Store in vector database
            payload = {
                "value": self._serialize(value),
                "metadata": metadata,
                "embedding": embedding
            }
            
            # Store in L3 (simplified - actual implementation depends on vector DB)
            cache_key = self._generate_key(key)
            self.l3_client.setex(cache_key, ttl, json.dumps(payload))
            
        except Exception as e:
            print(f"Error setting L3 cache: {e}")
    
    def get(self, key: str, strategy: Optional[CacheStrategy] = None) -> SemanticCacheResult:
        """Get a value from the cache using specified strategy.
        
        Args:
            key: Cache key
            strategy: Optional retrieval strategy override
            
        Returns:
            SemanticCacheResult with value and metadata
        """
        strategy = strategy or self.strategy
        start_time = time.time()
        
        if strategy == CacheStrategy.EXACT_FIRST:
            result = self._get_exact_first(key)
        elif strategy == CacheStrategy.SEMANTIC_FIRST:
            result = self._get_semantic_first(key)
        elif strategy == CacheStrategy.PARALLEL:
            result = self._get_parallel(key)
        elif strategy == CacheStrategy.HYBRID:
            result = self._get_hybrid(key)
        else:
            result = self._get_exact_first(key)
        
        result.retrieval_time_ms = (time.time() - start_time) * 1000
        
        if result.found:
            self.total_hits += 1
        else:
            self.total_misses += 1
        
        return result
    
    def _get_exact_first(self, key: str) -> SemanticCacheResult:
        """Try exact match first, then semantic.
        
        Args:
            key: Cache key
            
        Returns:
            SemanticCacheResult
        """
        # Try L1
        result = self._get_l1(key)
        if result.found:
            result.layer = CacheLevel.L1
            return result
        
        # Try L2
        result = self._get_l2(key)
        if result.found:
            result.layer = CacheLevel.L2
            # Promote to L1
            self._set_l1(key, result.value, self.default_ttl, result.metadata)
            return result
        
        # Try L3 (semantic)
        result = self._get_l3_semantic(key)
        if result.found:
            result.layer = CacheLevel.L3
            # Promote to L1 and L2
            self._set_l1(key, result.value, self.default_ttl, result.metadata)
            self._set_l2(key, result.value, self.default_ttl, result.metadata)
            return result
        
        return SemanticCacheResult(key=key, value=None, found=False)
    
    def _get_semantic_first(self, key: str) -> SemanticCacheResult:
        """Try semantic match first, then exact.
        
        Args:
            key: Cache key
            
        Returns:
            SemanticCacheResult
        """
        # Try L3 (semantic)
        result = self._get_l3_semantic(key)
        if result.found:
            result.layer = CacheLevel.L3
            # Promote to L1 and L2
            self._set_l1(key, result.value, self.default_ttl, result.metadata)
            self._set_l2(key, result.value, self.default_ttl, result.metadata)
            return result
        
        # Try L1
        result = self._get_l1(key)
        if result.found:
            result.layer = CacheLevel.L1
            return result
        
        # Try L2
        result = self._get_l2(key)
        if result.found:
            result.layer = CacheLevel.L2
            self._set_l1(key, result.value, self.default_ttl, result.metadata)
            return result
        
        return SemanticCacheResult(key=key, value=None, found=False)
    
    def _get_parallel(self, key: str) -> SemanticCacheResult:
        """Query all layers in parallel.
        
        Args:
            key: Cache key
            
        Returns:
            SemanticCacheResult
        """
        # This is a simplified implementation
        # In production, use asyncio.gather for true parallel queries
        
        # Try L1 first (fastest)
        result = self._get_l1(key)
        if result.found:
            result.layer = CacheLevel.L1
            return result
        
        # Try L2
        result = self._get_l2(key)
        if result.found:
            result.layer = CacheLevel.L2
            self._set_l1(key, result.value, self.default_ttl, result.metadata)
            return result
        
        # Try L3
        result = self._get_l3_semantic(key)
        if result.found:
            result.layer = CacheLevel.L3
            self._set_l1(key, result.value, self.default_ttl, result.metadata)
            return result
        
        return SemanticCacheResult(key=key, value=None, found=False)
    
    def _get_hybrid(self, key: str) -> SemanticCacheResult:
        """Combine exact and semantic results.
        
        Args:
            key: Cache key
            
        Returns:
            SemanticCacheResult
        """
        # Get exact match
        exact_result = self._get_exact_first(key)
        
        # Get semantic match
        semantic_result = self._get_l3_semantic(key)
        
        # If both found, choose based on similarity
        if exact_result.found and semantic_result.found:
            if semantic_result.similarity_score and semantic_result.similarity_score >= self.semantic_threshold:
                return semantic_result
            return exact_result
        elif exact_result.found:
            return exact_result
        elif semantic_result.found:
            return semantic_result
        
        return SemanticCacheResult(key=key, value=None, found=False)
    
    def _get_l1(self, key: str) -> SemanticCacheResult:
        """Get value from L1 cache.
        
        Args:
            key: Cache key
            
        Returns:
            SemanticCacheResult
        """
        if key in self.l1_cache:
            value, expiry, metadata = self.l1_cache[key]
            
            # Check expiry
            if time.time() < expiry:
                # Move to end for LRU
                self.l1_cache.move_to_end(key)
                
                self.layer_stats[CacheLevel.L1]["hits"] += 1
                return SemanticCacheResult(
                    key=key,
                    value=value,
                    found=True,
                    metadata=metadata
                )
            else:
                # Expired, remove
                del self.l1_cache[key]
        
        self.layer_stats[CacheLevel.L1]["misses"] += 1
        return SemanticCacheResult(key=key, value=None, found=False)
    
    def _get_l2(self, key: str) -> SemanticCacheResult:
        """Get value from L2 cache.
        
        Args:
            key: Cache key
            
        Returns:
            SemanticCacheResult
        """
        try:
            cache_key = self._generate_key(key)
            cached = self.l2_client.get(cache_key)
            
            if cached:
                payload = json.loads(cached)
                value = self._deserialize(payload["value"])
                metadata = payload.get("metadata", {})
                
                self.layer_stats[CacheLevel.L2]["hits"] += 1
                return SemanticCacheResult(
                    key=key,
                    value=value,
                    found=True,
                    metadata=metadata
                )
            
        except Exception as e:
            print(f"Error getting from L2 cache: {e}")
        
        self.layer_stats[CacheLevel.L2]["misses"] += 1
        return SemanticCacheResult(key=key, value=None, found=False)
    
    def _get_l3_semantic(self, key: str) -> SemanticCacheResult:
        """Get value from L3 cache using semantic similarity.
        
        Args:
            key: Cache key
            
        Returns:
            SemanticCacheResult
        """
        try:
            if not self.l3_client:
                return SemanticCacheResult(key=key, value=None, found=False)
            
            # Generate query embedding
            embedding_result = self.embedding_service.embed(str(key))
            query_embedding = np.array(embedding_result.embedding)
            
            if not embedding_result.embedding:
                return SemanticCacheResult(key=key, value=None, found=False)
            
            # Search for similar entries
            cache_key = self._generate_key(key)
            cached = self.l3_client.get(cache_key)
            
            if cached:
                payload = json.loads(cached)
                cached_embedding = np.array(payload.get("embedding", []))
                
                if len(cached_embedding) > 0:
                    # Calculate similarity
                    similarity = np.dot(query_embedding, cached_embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(cached_embedding)
                    )
                    
                    if similarity >= self.semantic_threshold:
                        value = self._deserialize(payload["value"])
                        metadata = payload.get("metadata", {})
                        
                        self.layer_stats[CacheLevel.L3]["hits"] += 1
                        return SemanticCacheResult(
                            key=key,
                            value=value,
                            found=True,
                            layer=CacheLevel.L3,
                            similarity_score=similarity,
                            metadata=metadata
                        )
            
        except Exception as e:
            print(f"Error getting from L3 cache: {e}")
        
        self.layer_stats[CacheLevel.L3]["misses"] += 1
        return SemanticCacheResult(key=key, value=None, found=False)
    
    def delete(self, key: str) -> bool:
        """Delete a value from all cache layers.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful
        """
        # Delete from L1
        if key in self.l1_cache:
            del self.l1_cache[key]
        
        # Delete from L2
        if self.l2_client:
            try:
                cache_key = self._generate_key(key)
                self.l2_client.delete(cache_key)
            except Exception as e:
                print(f"Error deleting from L2 cache: {e}")
        
        # Delete from L3
        if self.l3_client:
            try:
                cache_key = self._generate_key(key)
                self.l3_client.delete(cache_key)
            except Exception as e:
                print(f"Error deleting from L3 cache: {e}")
        
        return True
    
    def clear(self, level: Optional[CacheLevel] = None) -> None:
        """Clear cache entries.
        
        Args:
            level: Optional cache level to clear (all if None)
        """
        if level is None or level == CacheLevel.L1:
            self.l1_cache.clear()
        
        if level is None or level == CacheLevel.L2:
            if self.l2_client:
                try:
                    pattern = f"{self._generate_key('*')}"
                    for key in self.l2_client.scan_iter(match=pattern):
                        self.l2_client.delete(key)
                except Exception as e:
                    print(f"Error clearing L2 cache: {e}")
        
        if level is None or level == CacheLevel.L3:
            if self.l3_client:
                try:
                    pattern = f"{self._generate_key('*')}"
                    for key in self.l3_client.scan_iter(match=pattern):
                        self.l3_client.delete(key)
                except Exception as e:
                    print(f"Error clearing L3 cache: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_requests = self.total_hits + self.total_misses
        
        return {
            "overall": {
                "hits": self.total_hits,
                "misses": self.total_misses,
                "hit_rate": self.total_hits / total_requests if total_requests > 0 else 0.0
            },
            "layers": {
                "l1": {
                    "size": len(self.l1_cache),
                    "max_size": self.l1_max_size,
                    "hits": self.layer_stats[CacheLevel.L1]["hits"],
                    "misses": self.layer_stats[CacheLevel.L1]["misses"],
                    "hit_rate": self.layer_stats[CacheLevel.L1]["hits"] / (
                        self.layer_stats[CacheLevel.L1]["hits"] + self.layer_stats[CacheLevel.L1]["misses"]
                    ) if (self.layer_stats[CacheLevel.L1]["hits"] + self.layer_stats[CacheLevel.L1]["misses"]) > 0 else 0.0
                },
                "l2": {
                    "enabled": self.l2_client is not None,
                    "hits": self.layer_stats[CacheLevel.L2]["hits"],
                    "misses": self.layer_stats[CacheLevel.L2]["misses"],
                    "hit_rate": self.layer_stats[CacheLevel.L2]["hits"] / (
                        self.layer_stats[CacheLevel.L2]["hits"] + self.layer_stats[CacheLevel.L2]["misses"]
                    ) if (self.layer_stats[CacheLevel.L2]["hits"] + self.layer_stats[CacheLevel.L2]["misses"]) > 0 else 0.0
                },
                "l3": {
                    "enabled": self.l3_client is not None,
                    "hits": self.layer_stats[CacheLevel.L3]["hits"],
                    "misses": self.layer_stats[CacheLevel.L3]["misses"],
                    "hit_rate": self.layer_stats[CacheLevel.L3]["hits"] / (
                        self.layer_stats[CacheLevel.L3]["hits"] + self.layer_stats[CacheLevel.L3]["misses"]
                    ) if (self.layer_stats[CacheLevel.L3]["hits"] + self.layer_stats[CacheLevel.L3]["misses"]) > 0 else 0.0
                }
            },
            "configuration": {
                "default_ttl": self.default_ttl,
                "semantic_threshold": self.semantic_threshold,
                "strategy": self.strategy.value
            }
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of all cache layers.
        
        Returns:
            Health status dictionary
        """
        health = {
            "status": "healthy",
            "layers": {}
        }
        
        # Check L1
        health["layers"]["l1"] = {
            "status": "healthy",
            "size": len(self.l1_cache),
            "max_size": self.l1_max_size
        }
        
        # Check L2
        if self.l2_client:
            try:
                test_key = f"{self._generate_key('health_check')}:l2"
                self.l2_client.setex(test_key, 10, "ok")
                result = self.l2_client.get(test_key)
                self.l2_client.delete(test_key)
                health["layers"]["l2"] = {
                    "status": "healthy" if result == b"ok" else "unhealthy"
                }
            except Exception as e:
                health["layers"]["l2"] = {"status": "unhealthy", "error": str(e)}
                health["status"] = "degraded"
        else:
            health["layers"]["l2"] = {"status": "disabled"}
        
        # Check L3
        if self.l3_client:
            try:
                test_key = f"{self._generate_key('health_check')}:l3"
                self.l3_client.setex(test_key, 10, "ok")
                result = self.l3_client.get(test_key)
                self.l3_client.delete(test_key)
                health["layers"]["l3"] = {
                    "status": "healthy" if result == b"ok" else "unhealthy"
                }
            except Exception as e:
                health["layers"]["l3"] = {"status": "unhealthy", "error": str(e)}
                health["status"] = "degraded"
        else:
            health["layers"]["l3"] = {"status": "disabled"}
        
        return health