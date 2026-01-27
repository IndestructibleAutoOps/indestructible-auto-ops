"""
Memory Plugins: Memory backend implementations.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins/memory_plugins
@gl-semantic-anchor GL-00-PLUGINS_MEMORYPL_INIT
@gl-evidence-required false
GL Unified Charter Activated
"""

from .redis_backend import RedisMemoryBackend
from .semantic_cache import CacheConfig, SemanticCache
from .vector_index_manager import (
    VectorIndexManager,
    VectorIndexConfig,
    DistanceMetric,
    VectorAlgorithm,
    DEFAULT_MEMORY_INDEX,
    DEFAULT_CACHE_INDEX,
    DEFAULT_KNOWLEDGE_INDEX,
)
from .embedding_service import (
    EmbeddingService,
    EmbeddingConfig,
    EmbeddingProvider,
    OPENAI_ADA_002_CONFIG,
    OPENAI_3_SMALL_CONFIG,
    OPENAI_3_LARGE_CONFIG,
    COHERE_ENGLISH_CONFIG,
    COHERE_MULTILINGUAL_CONFIG,
    OLLAMA_NOMIC_CONFIG,
    SENTENCE_TRANSFORMERS_MINILM_CONFIG,
)
from .vector_search import (
    VectorSearchQueryBuilder,
    VectorSearchExecutor,
    VectorSearchQuery,
    SearchResult,
    SearchResponse,
    FilterCondition,
    FilterOperator,
    SemanticMemorySearch,
)
from .semantic_cache_v2 import (
    SemanticCacheV2,
    SemanticCacheConfigV2,
    CacheStrategy,
    EvictionPolicy,
    CacheEntry,
    CacheHit,
    CacheStats,
)
from .cache_middleware import (
    CacheMiddleware,
    CacheMiddlewareConfig,
    CacheEvent,
    CacheEventHandler,
    LoggingEventHandler,
    MetricsEventHandler,
    OpenAICacheMiddleware,
    AnthropicCacheMiddleware,
)
from .memory_compactor import (
    MemoryCompactor,
    AutomaticMemoryCompactor,
    MemorySnapshot,
    CompactionConfig,
    CompactionStrategy,
    CompactionLevel,
    CompactionReport,
    CompactionRule,
    TokenThresholdRule,
    EntryCountRule,
    TimeSinceLastCompactionRule,
)
from .cache_optimizer import CacheOptimizer
from .cache_invalidator import CacheInvalidator

__all__ = [
    # Redis Backend
    "RedisMemoryBackend",
    # Semantic Cache (V1)
    "SemanticCache",
    "CacheConfig",
    # Vector Index Manager
    "VectorIndexManager",
    "VectorIndexConfig",
    "DistanceMetric",
    "VectorAlgorithm",
    "DEFAULT_MEMORY_INDEX",
    "DEFAULT_CACHE_INDEX",
    "DEFAULT_KNOWLEDGE_INDEX",
    # Embedding Service
    "EmbeddingService",
    "EmbeddingConfig",
    "EmbeddingProvider",
    "OPENAI_ADA_002_CONFIG",
    "OPENAI_3_SMALL_CONFIG",
    "OPENAI_3_LARGE_CONFIG",
    "COHERE_ENGLISH_CONFIG",
    "COHERE_MULTILINGUAL_CONFIG",
    "OLLAMA_NOMIC_CONFIG",
    "SENTENCE_TRANSFORMERS_MINILM_CONFIG",
    # Vector Search
    "VectorSearchQueryBuilder",
    "VectorSearchExecutor",
    "VectorSearchQuery",
    "SearchResult",
    "SearchResponse",
    "FilterCondition",
    "FilterOperator",
    "SemanticMemorySearch",
    # Semantic Cache V2
    "SemanticCacheV2",
    "SemanticCacheConfigV2",
    "CacheStrategy",
    "EvictionPolicy",
    "CacheEntry",
    "CacheHit",
    "CacheStats",
    # Cache Middleware
    "CacheMiddleware",
    "CacheMiddlewareConfig",
    "CacheEvent",
    "CacheEventHandler",
    "LoggingEventHandler",
    "MetricsEventHandler",
    "OpenAICacheMiddleware",
    "AnthropicCacheMiddleware",
    # Memory Compactor
    "MemoryCompactor",
    "AutomaticMemoryCompactor",
    "MemorySnapshot",
    "CompactionConfig",
    "CompactionStrategy",
    "CompactionLevel",
    "CompactionReport",
    "CompactionRule",
    "TokenThresholdRule",
    "EntryCountRule",
    "TimeSinceLastCompactionRule",
    # Cache Optimizer
    "CacheOptimizer",
    # Cache Invalidator
    "CacheInvalidator",
]