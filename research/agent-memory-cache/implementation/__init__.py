"""
Agent Memory and Cache System - Implementation Module

This module provides complete implementations for AI agent memory management
and semantic caching systems.

Components:
- vector_index_manager: Vector index management for semantic search
- embedding_service: Multi-provider embedding generation
- vector_search: Vector similarity search functionality
- cache_middleware: LLM API response caching
- semantic_cache_v2: Enhanced semantic cache with adaptive features
"""

from .vector_index_manager import (
    VectorIndexManager,
    Document,
    IndexConfig,
    DistanceMetric,
    IndexAlgorithm
)

from .embedding_service import (
    EmbeddingService,
    EmbeddingConfig,
    EmbeddingProvider,
    EmbeddingResult
)

from .vector_search import (
    VectorSearch,
    SearchQuery,
    SearchResult,
    SearchStrategy
)

from .cache_middleware import (
    CacheMiddleware,
    CacheConfig,
    CacheStrategy,
    EventHandler,
    LoggingEventHandler,
    MetricsEventHandler,
    CacheEvent
)

from .semantic_cache_v2 import (
    SemanticCacheV2,
    CacheEntry,
    CacheStats,
    EvictionPolicy,
    CacheLevel
)

__all__ = [
    # Vector Index Manager
    "VectorIndexManager",
    "Document",
    "IndexConfig",
    "DistanceMetric",
    "IndexAlgorithm",
    
    # Embedding Service
    "EmbeddingService",
    "EmbeddingConfig",
    "EmbeddingProvider",
    "EmbeddingResult",
    
    # Vector Search
    "VectorSearch",
    "SearchQuery",
    "SearchResult",
    "SearchStrategy",
    
    # Cache Middleware
    "CacheMiddleware",
    "CacheConfig",
    "CacheStrategy",
    "EventHandler",
    "LoggingEventHandler",
    "MetricsEventHandler",
    "CacheEvent",
    
    # Semantic Cache V2
    "SemanticCacheV2",
    "CacheEntry",
    "CacheStats",
    "EvictionPolicy",
    "CacheLevel",
]

__version__ = "2.0.0"