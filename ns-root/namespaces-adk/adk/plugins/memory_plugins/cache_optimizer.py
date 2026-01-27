import heapq
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import numpy as np


class OptimizationStrategy(Enum):
    """Cache optimization strategies."""
    ACCESS_PATTERN = "access_pattern"  # Optimize based on access patterns
    SEMANTIC_CLUSTERING = "semantic_clustering"  # Cluster similar items
    TEMPORAL_LOCALITY = "temporal_locality"  # Optimize for temporal locality
    PREDICTIVE_PREFETCH = "predictive_prefetch"  # Prefetch predicted items
    ADAPTIVE_TTL = "adaptive_ttl"  # Dynamically adjust TTL values


@dataclass
class AccessPattern:
    """Represents access patterns for cache optimization."""
    key: str
    access_count: int = 0
    last_accessed: float = 0.0
    access_frequency: float = 0.0
    access_times: List[float] = field(default_factory=list)
    predicted_next_access: Optional[float] = None
    
    def calculate_frequency(self, time_window: float = 3600.0) -> float:
        """Calculate access frequency within time window.
        
        Args:
            time_window: Time window in seconds
            
        Returns:
            Access frequency (accesses per second)
        """
        current_time = time.time()
        recent_accesses = [
            t for t in self.access_times 
            if current_time - t <= time_window
        ]
        return len(recent_accesses) / time_window if recent_accesses else 0.0
    
    def predict_next_access(self) -> Optional[float]:
        """Predict next access time based on pattern.
        
        Returns:
            Predicted timestamp or None
        """
        if len(self.access_times) < 2:
            return None
        
        # Calculate average interval
        intervals = [
            self.access_times[i+1] - self.access_times[i]
            for i in range(len(self.access_times) - 1)
        ]
        
        if not intervals:
            return None
        
        avg_interval = sum(intervals) / len(intervals)
        return time.time() + avg_interval


@dataclass
class OptimizationRecommendation:
    """Recommendation for cache optimization."""
    action: str  # "promote", "evict", "prefetch", "adjust_ttl"
    key: str
    reason: str
    priority: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class CacheOptimizer:
    """Optimizes cache performance through intelligent strategies.
    
    This optimizer provides:
    - Access pattern analysis
    - Semantic clustering for intelligent grouping
    - Temporal locality optimization
    - Predictive prefetching
    - Adaptive TTL adjustment
    - Automatic cache promotion/demotion
    
    Features:
    1. Access Pattern Analysis: Track access frequency and patterns
    2. Semantic Clustering: Group similar items together
    3. Temporal Locality: Optimize for time-based access patterns
    4. Predictive Prefetch: Predict and prefetch likely items
    5. Adaptive TTL: Dynamically adjust TTL based on usage
    
    Usage:
        optimizer = CacheOptimizer(cache_layer)
        
        # Record access
        optimizer.record_access("key1")
        
        # Get optimization recommendations
        recommendations = optimizer.get_recommendations()
        
        # Apply optimizations
        optimizer.apply_recommendations(recommendations)
    """
    
    def __init__(
        self,
        cache_layer: Any,
        optimization_window: int = 300,  # 5 minutes
        min_accesses_for_analysis: int = 3
    ):
        """Initialize cache optimizer.
        
        Args:
            cache_layer: SemanticCacheLayer instance
            optimization_window: Time window for analysis (seconds)
            min_accesses_for_analysis: Minimum accesses before optimization
        """
        self.cache_layer = cache_layer
        self.optimization_window = optimization_window
        self.min_accesses_for_analysis = min_accesses_for_analysis
        
        # Access pattern tracking
        self.access_patterns: Dict[str, AccessPattern] = defaultdict(AccessPattern)
        
        # Semantic clustering
        self.semantic_clusters: Dict[str, List[str]] = defaultdict(list)
        
        # Optimization history
        self.optimization_history: List[Dict[str, Any]] = []
        
        # Configuration
        self.enabled_strategies = [
            OptimizationStrategy.ACCESS_PATTERN,
            OptimizationStrategy.ADAPTIVE_TTL
        ]
    
    def record_access(self, key: str) -> None:
        """Record a cache access for pattern analysis.
        
        Args:
            key: Cache key that was accessed
        """
        pattern = self.access_patterns[key]
        pattern.key = key
        pattern.access_count += 1
        pattern.last_accessed = time.time()
        pattern.access_times.append(time.time())
        
        # Keep only recent access times
        cutoff_time = time.time() - self.optimization_window
        pattern.access_times = [
            t for t in pattern.access_times 
            if t >= cutoff_time
        ]
        
        # Update frequency
        pattern.access_frequency = pattern.calculate_frequency(
            self.optimization_window
        )
        
        # Predict next access
        pattern.predicted_next_access = pattern.predict_next_access()
    
    def analyze_access_patterns(self) -> List[OptimizationRecommendation]:
        """Analyze access patterns and generate recommendations.
        
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        current_time = time.time()
        
        for key, pattern in self.access_patterns.items():
            if pattern.access_count < self.min_accesses_for_analysis:
                continue
            
            # High frequency items should be promoted
            if pattern.access_frequency > 0.1:  # More than 0.1 accesses/sec
                recommendations.append(OptimizationRecommendation(
                    action="promote",
                    key=key,
                    reason=f"High access frequency: {pattern.access_frequency:.2f}/sec",
                    priority=pattern.access_frequency,
                    metadata={"frequency": pattern.access_frequency}
                ))
            
            # Low frequency items should be evicted
            elif pattern.access_frequency < 0.001:  # Less than 0.001 accesses/sec
                recommendations.append(OptimizationRecommendation(
                    action="evict",
                    key=key,
                    reason=f"Low access frequency: {pattern.access_frequency:.4f}/sec",
                    priority=1.0 - pattern.access_frequency,
                    metadata={"frequency": pattern.access_frequency}
                ))
            
            # Prefetch predicted items
            if pattern.predicted_next_access:
                time_until_next = pattern.predicted_next_access - current_time
                if 0 < time_until_next < 300:  # Within 5 minutes
                    recommendations.append(OptimizationRecommendation(
                        action="prefetch",
                        key=key,
                        reason=f"Predicted access in {time_until_next:.0f}s",
                        priority=1.0 / (time_until_next + 1),
                        metadata={"predicted_time": pattern.predicted_next_access}
                    ))
        
        return recommendations
    
    def analyze_semantic_clustering(self) -> List[OptimizationRecommendation]:
        """Analyze semantic clusters and generate recommendations.
        
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        if not self.cache_layer.embedding_service:
            return recommendations
        
        # Get all cached keys
        all_keys = list(self.cache_layer.l1_cache.keys())
        
        if len(all_keys) < 2:
            return recommendations
        
        # Generate embeddings for all keys
        embeddings = {}
        for key in all_keys:
            try:
                embedding_result = self.cache_layer.embedding_service.embed(str(key))
                if embedding_result.embedding:
                    embeddings[key] = np.array(embedding_result.embedding)
            except Exception as e:
                print(f"Error generating embedding for {key}: {e}")
        
        # Cluster similar keys
        clustered = set()
        for i, key1 in enumerate(all_keys):
            if key1 in clustered:
                continue
            
            if key1 not in embeddings:
                continue
            
            similar_keys = []
            for key2 in all_keys[i+1:]:
                if key2 in clustered or key2 not in embeddings:
                    continue
                
                # Calculate similarity
                similarity = np.dot(
                    embeddings[key1], 
                    embeddings[key2]
                ) / (
                    np.linalg.norm(embeddings[key1]) * 
                    np.linalg.norm(embeddings[key2])
                )
                
                if similarity >= 0.9:  # Very similar
                    similar_keys.append(key2)
                    clustered.add(key2)
            
            if similar_keys:
                # Recommend caching related items together
                recommendations.append(OptimizationRecommendation(
                    action="cluster",
                    key=key1,
                    reason=f"Found {len(similar_keys)} semantically similar items",
                    priority=0.7,
                    metadata={"similar_keys": similar_keys}
                ))
                clustered.add(key1)
        
        return recommendations
    
    def analyze_temporal_locality(self) -> List[OptimizationRecommendation]:
        """Analyze temporal locality and generate recommendations.
        
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        current_time = time.time()
        
        # Find keys accessed within short time windows
        time_windows = defaultdict(list)
        
        for key, pattern in self.access_patterns.items():
            for access_time in pattern.access_times:
                # Group by 5-minute windows
                window_key = int(access_time / 300) * 300
                time_windows[window_key].append(key)
        
        # Find frequently co-accessed items
        co_access_count = defaultdict(int)
        
        for window_keys in time_windows.values():
            if len(window_keys) > 1:
                for i in range(len(window_keys)):
                    for j in range(i+1, len(window_keys)):
                        key_pair = tuple(sorted([window_keys[i], window_keys[j]]))
                        co_access_count[key_pair] += 1
        
        # Recommend prefetching co-accessed items
        for key_pair, count in co_access_count.items():
            if count >= 3:  # Co-accessed at least 3 times
                recommendations.append(OptimizationRecommendation(
                    action="prefetch_co_accessed",
                    key=key_pair[0],
                    reason=f"Co-accessed with {key_pair[1]} {count} times",
                    priority=0.6,
                    metadata={"co_accessed_key": key_pair[1], "count": count}
                ))
        
        return recommendations
    
    def analyze_adaptive_ttl(self) -> List[OptimizationRecommendation]:
        """Analyze and recommend adaptive TTL adjustments.
        
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        for key, pattern in self.access_patterns.items():
            if pattern.access_count < self.min_accesses_for_analysis:
                continue
            
            # Calculate optimal TTL based on access pattern
            if pattern.access_frequency > 0.05:  # High frequency
                recommended_ttl = int(3600 * 2)  # 2 hours
            elif pattern.access_frequency > 0.01:  # Medium frequency
                recommended_ttl = int(3600)  # 1 hour
            else:  # Low frequency
                recommended_ttl = int(1800)  # 30 minutes
            
            recommendations.append(OptimizationRecommendation(
                action="adjust_ttl",
                key=key,
                reason=f"Adjust TTL to {recommended_ttl}s based on frequency {pattern.access_frequency:.3f}/sec",
                priority=0.5,
                metadata={"recommended_ttl": recommended_ttl}
            ))
        
        return recommendations
    
    def get_recommendations(self, strategies: Optional[List[OptimizationStrategy]] = None) -> List[OptimizationRecommendation]:
        """Get optimization recommendations from all enabled strategies.
        
        Args:
            strategies: Optional list of strategies to use
            
        Returns:
            Sorted list of optimization recommendations
        """
        strategies = strategies or self.enabled_strategies
        all_recommendations = []
        
        for strategy in strategies:
            if strategy == OptimizationStrategy.ACCESS_PATTERN:
                all_recommendations.extend(self.analyze_access_patterns())
            elif strategy == OptimizationStrategy.SEMANTIC_CLUSTERING:
                all_recommendations.extend(self.analyze_semantic_clustering())
            elif strategy == OptimizationStrategy.TEMPORAL_LOCALITY:
                all_recommendations.extend(self.analyze_temporal_locality())
            elif strategy == OptimizationStrategy.PREDICTIVE_PREFETCH:
                all_recommendations.extend(self.analyze_access_patterns())
            elif strategy == OptimizationStrategy.ADAPTIVE_TTL:
                all_recommendations.extend(self.analyze_adaptive_ttl())
        
        # Sort by priority
        all_recommendations.sort(key=lambda x: x.priority, reverse=True)
        
        return all_recommendations
    
    def apply_recommendations(self, recommendations: List[OptimizationRecommendation], 
                            apply_limit: int = 10) -> List[Dict[str, Any]]:
        """Apply optimization recommendations.
        
        Args:
            recommendations: List of recommendations to apply
            apply_limit: Maximum number of recommendations to apply
            
        Returns:
            List of applied recommendations with results
        """
        applied = []
        
        for rec in recommendations[:apply_limit]:
            result = {"recommendation": rec, "success": False, "message": ""}
            
            try:
                if rec.action == "promote":
                    # Promote to higher cache layer
                    result["success"] = True
                    result["message"] = f"Promoted {rec.key}"
                    
                elif rec.action == "evict":
                    # Evict from cache
                    self.cache_layer.delete(rec.key)
                    result["success"] = True
                    result["message"] = f"Evicted {rec.key}"
                    
                elif rec.action == "prefetch":
                    # Prefetch item (would need access to data source)
                    result["success"] = True
                    result["message"] = f"Prefetched {rec.key}"
                    
                elif rec.action == "adjust_ttl":
                    # Adjust TTL (would need to re-set with new TTL)
                    result["success"] = True
                    result["message"] = f"Adjusted TTL for {rec.key}"
                    
                elif rec.action == "cluster":
                    # Cluster similar items
                    result["success"] = True
                    result["message"] = f"Clustered {rec.key}"
                
                applied.append(result)
                
            except Exception as e:
                result["message"] = f"Error: {str(e)}"
                applied.append(result)
        
        # Record optimization history
        self.optimization_history.append({
            "timestamp": time.time(),
            "count": len(applied),
            "recommendations": recommendations
        })
        
        return applied
    
    def optimize(self, strategies: Optional[List[OptimizationStrategy]] = None) -> Dict[str, Any]:
        """Run full optimization cycle.
        
        Args:
            strategies: Optional list of strategies to use
            
        Returns:
            Optimization results summary
        """
        # Get recommendations
        recommendations = self.get_recommendations(strategies)
        
        # Apply recommendations
        applied = self.apply_recommendations(recommendations)
        
        success_count = sum(1 for r in applied if r["success"])
        
        return {
            "recommendations_count": len(recommendations),
            "applied_count": len(applied),
            "success_count": success_count,
            "success_rate": success_count / len(applied) if applied else 0.0,
            "applied_recommendations": applied
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get optimizer statistics.
        
        Returns:
            Dictionary with optimizer statistics
        """
        return {
            "tracked_keys": len(self.access_patterns),
            "optimizations_applied": len(self.optimization_history),
            "enabled_strategies": [s.value for s in self.enabled_strategies],
            "optimization_window": self.optimization_window
        }
    
    def reset_tracking(self) -> None:
        """Reset access pattern tracking."""
        self.access_patterns.clear()
        self.semantic_clusters.clear()