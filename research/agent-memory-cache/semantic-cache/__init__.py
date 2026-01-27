"""
Agent Memory and Cache System - Semantic Cache Module

This module provides advanced semantic caching capabilities with:
- Multi-layer caching architecture (L1, L2, L3)
- Intelligent cache optimization
- Flexible cache invalidation strategies
- Comprehensive monitoring and alerting

Components:
- semantic_cache_layer: Multi-layer semantic cache system
- cache_optimizer: Intelligent cache optimization strategies
- cache_invalidator: Flexible cache invalidation with multiple strategies
- cache_monitor: Real-time monitoring, metrics, and alerting
"""

from .semantic_cache_layer import (
    SemanticCacheLayer,
    SemanticCacheResult,
    CacheLevel,
    CacheStrategy,
    LayerConfig,
    CacheLayer
)

from .cache_optimizer import (
    CacheOptimizer,
    OptimizationStrategy,
    AccessPattern,
    OptimizationRecommendation
)

from .cache_invalidator import (
    CacheInvalidator,
    InvalidationStrategy,
    InvalidationEvent,
    InvalidationRule,
    InvalidationResult
)

from .cache_monitor import (
    CacheMonitor,
    MetricType,
    Metric,
    Alert
)

__all__ = [
    # Semantic Cache Layer
    "SemanticCacheLayer",
    "SemanticCacheResult",
    "CacheLevel",
    "CacheStrategy",
    "LayerConfig",
    "CacheLayer",
    
    # Cache Optimizer
    "CacheOptimizer",
    "OptimizationStrategy",
    "AccessPattern",
    "OptimizationRecommendation",
    
    # Cache Invalidator
    "CacheInvalidator",
    "InvalidationStrategy",
    "InvalidationEvent",
    "InvalidationRule",
    "InvalidationResult",
    
    # Cache Monitor
    "CacheMonitor",
    "MetricType",
    "Metric",
    "Alert",
]

__version__ = "1.0.0"