# Memory & Cache API Guide

## Overview

This guide provides comprehensive documentation for the Memory and Cache components in the Agent Development Kit (ADK).

## Table of Contents

- [Memory Manager](#memory-manager)
- [Redis Backend](#redis-backend)
- [Semantic Cache](#semantic-cache)
- [Vector Search](#vector-search)
- [Embedding Service](#embedding-service)
- [Memory Compactor](#memory-compactor)

---

## Memory Manager

### Overview

The `MemoryManager` provides a unified interface for managing both short-term (context window) and long-term memory for AI agents.

### Initialization

```python
from adk.core.memory_manager import MemoryManager, MemoryType

# Initialize with Redis backend
memory_manager = MemoryManager(
    backend="redis",
    redis_host="localhost",
    redis_port=6379,
    enable_vector_search=True,
    embedding_provider="openai",
    embedding_model="text-embedding-ada-002",
    vector_dim=1536,
)

await memory_manager.initialize()
```

### Basic Operations

#### Adding Memories

```python
# Add a memory entry
entry_id = await memory_manager.add(
    content="The user prefers Python over JavaScript",
    memory_type=MemoryType.LONG_TERM,
    session_id="session_123",
    user_id="user_456",
    importance=0.8,
    metadata={"category": "preference"},
)

# Add with automatic embedding
entry_id = await memory_manager.add_with_embedding(
    content="Important information to remember",
    memory_type=MemoryType.LONG_TERM,
    agent_id="agent_1",
    importance=0.9,
)
```

#### Retrieving Memories

```python
# Get by ID
entry = await memory_manager.get(entry_id)

# Query memories
entries = await memory_manager.query(
    query_text="programming preferences",
    session_id="session_123",
    limit=10,
)

# Semantic search
results = await memory_manager.semantic_search(
    query="user likes Python",
    top_k=5,
    agent_id="agent_1",
)

# Get context for LLM
context = await memory_manager.get_semantic_context(
    query="current task",
    max_tokens=2000,
    agent_id="agent_1",
)
```

#### Updating and Deleting

```python
# Update a memory
await memory_manager.update(
    entry_id=entry_id,
    content="Updated content",
    metadata={"status": "verified"},
)

# Delete a memory
await memory_manager.delete(entry_id)

# Clear entire session
count = await memory_manager.clear_session("session_123")
```

### Advanced Features

#### Semantic Search

```python
from adk.plugins.memory_plugins.vector_search import FilterOperator, FilterCondition

# Build complex queries
builder = VectorSearchQueryBuilder()
builder.filter_eq("type", "preference")
builder.filter_gte("importance", 0.5)

query = builder.build()
results = await memory_manager._vector_search_executor.search(query)
```

#### Memory Compaction

```python
# Compact memories intelligently
report = await memory_manager.compact_memories(
    compaction_config={
        "strategy": "hybrid",
        "level": "moderate",
        "keep_recent_hours": 24,
    }
)

print(f"Removed {report['entries_removed']} entries")
print(f"Saved {report['tokens_saved']} tokens")
```

---

## Redis Backend

### Overview

The `RedisMemoryBackend` provides persistent memory storage using Redis Stack with vector search capabilities.

### Configuration

```python
from adk.plugins.memory_plugins.redis_backend import RedisConfig, RedisMemoryBackend

config = RedisConfig(
    host="localhost",
    port=6379,
    db=0,
    prefix="memory:",
    vector_dim=1536,
)

backend = RedisMemoryBackend(config)
await backend.initialize()
```

### Usage

```python
# Add entry
entry_id = await backend.add(
    id="mem_123",
    content="Memory content",
    metadata={"key": "value"},
)

# Get entry
entry = await backend.get("mem_123")

# Vector search
results = await backend.vector_search(
    query_vector=[0.1, 0.2, ...],
    limit=10,
    filters={"type": "preference"},
)
```

---

## Semantic Cache

### Overview

The `SemanticCache` provides intelligent LLM response caching based on semantic similarity.

### V2 Cache (Enhanced)

```python
from adk.plugins.memory_plugins.semantic_cache_v2 import (
    SemanticCacheV2,
    SemanticCacheConfigV2,
    CacheStrategy,
    EvictionPolicy,
)

# Configure cache
config = SemanticCacheConfigV2(
    similarity_threshold=0.85,
    default_ttl=3600,
    max_entries=10000,
    eviction_policy=EvictionPolicy.ADAPTIVE,
    enable_adaptive_ttl=True,
)

# Initialize with Redis and embedding service
cache = SemanticCacheV2(
    redis_client=redis_client,
    embedding_service=embedding_service,
    config=config,
)

await cache.initialize()
```

### Cache Operations

```python
# Get cached response
hit = await cache.get(
    query="What is Python?",
    model="gpt-4",
    strategy=CacheStrategy.HYBRID,
)

if hit:
    print(f"Cache hit: {hit.entry.response}")
    print(f"Similarity: {hit.similarity}")
else:
    print("Cache miss, compute response")

# Store response
await cache.set(
    query="What is Python?",
    response="Python is a programming language...",
    model="gpt-4",
    tokens_used=150,
)

# Get or compute pattern
response, was_cached = await cache.get_or_compute(
    query="What is Python?",
    compute_fn=lambda: generate_response(),
    model="gpt-4",
)

# Warm cache
await cache.warm([
    ("Q1", "A1"),
    ("Q2", "A2"),
])
```

### Cache Middleware

```python
from adk.plugins.memory_plugins.cache_middleware import (
    CacheMiddleware,
    CacheMiddlewareConfig,
    MetricsEventHandler,
)

# Create middleware
middleware = CacheMiddleware(
    cache=semantic_cache,
    config=CacheMiddlewareConfig(
        enabled=True,
        strategy=CacheStrategy.HYBRID,
        log_cache_events=True,
    ),
)

# Add metrics handler
metrics = MetricsEventHandler()
middleware.add_event_handler(metrics)

# Wrap LLM calls
@middleware.cached(model="gpt-4")
async def generate_response(messages):
    return await openai_client.chat.completions.create(
        model="gpt-4",
        messages=messages,
    )

# Or use wrap_completion
response = await middleware.wrap_completion(
    completion_fn=openai_client.chat.completions.create,
    messages=[{"role": "user", "content": "Hello"}],
    model="gpt-4",
)

# Get metrics
stats = metrics.get_metrics()
print(f"Hit rate: {stats['hit_rate']:.2%}")
```

---

## Vector Search

### Overview

Vector search enables semantic memory retrieval using similarity search over embeddings.

### Vector Index Manager

```python
from adk.plugins.memory_plugins.vector_index_manager import (
    VectorIndexManager,
    VectorIndexConfig,
    DistanceMetric,
    VectorAlgorithm,
)

# Create index manager
index_manager = VectorIndexManager(redis_client)

# Define index configuration
config = VectorIndexConfig(
    name="idx:memory",
    prefix="memory:",
    dimension=1536,
    distance_metric=DistanceMetric.COSINE,
    algorithm=VectorAlgorithm.HNSW,
    text_fields=["content", "summary"],
    tag_fields=["type", "agent_id"],
    numeric_fields=["timestamp", "importance"],
)

# Create index
await index_manager.create_index(config)

# Store document
key = await index_manager.store_document(
    index_name="idx:memory",
    doc_id="doc_123",
    content="Document content",
    embedding=[0.1, 0.2, ...],
    metadata={"type": "knowledge"},
)
```

### Vector Search Executor

```python
from adk.plugins.memory_plugins.vector_search import (
    VectorSearchQueryBuilder,
    VectorSearchExecutor,
    FilterOperator,
)

# Build query
builder = VectorSearchQueryBuilder()
builder.with_vector(query_embedding)
builder.filter_eq("agent_id", "agent_1")
builder.filter_gte("importance", 0.5)
builder.filter_in("type", ["episodic", "semantic"])

query = builder.build()

# Execute search
executor = VectorSearchExecutor(redis_client, "idx:memory")
response = await executor.search(query)

for result in response.results:
    print(f"ID: {result.doc_id}")
    print(f"Score: {result.score}")
    print(f"Content: {result.content}")
```

### Semantic Memory Search

```python
from adk.plugins.memory_plugins.vector_search import SemanticMemorySearch

# Create semantic search
search = SemanticMemorySearch(
    redis_client=redis_client,
    embedding_service=embedding_service,
    index_name="idx:memory",
)

# Search memories
results = await search.search(
    query="user preferences",
    top_k=10,
    agent_id="agent_1",
    session_id="session_123",
    min_importance=0.5,
)

# Get context for LLM
context = await search.get_context(
    query="current task",
    max_tokens=2000,
    agent_id="agent_1",
)

# Find similar memories
similar = await search.find_similar(
    content="Python is preferred",
    top_k=5,
    exclude_self=True,
)
```

---

## Embedding Service

### Overview

The `EmbeddingService` provides a unified interface for generating text embeddings from multiple providers.

### Supported Providers

```python
from adk.plugins.memory_plugins.embedding_service import (
    EmbeddingService,
    EmbeddingConfig,
    EmbeddingProvider,
)
```

| Provider | Config Example |
|----------|---------------|
| OpenAI | `EmbeddingConfig(provider=EmbeddingProvider.OPENAI, model="text-embedding-ada-002", api_key="...")` |
| Azure OpenAI | `EmbeddingConfig(provider=EmbeddingProvider.AZURE_OPENAI, model="deployment-name", api_key="...", api_base="...", api_version="...")` |
| Cohere | `EmbeddingConfig(provider=EmbeddingProvider.COHERE, model="embed-english-v3.0", api_key="...")` |
| Ollama | `EmbeddingConfig(provider=EmbeddingProvider.OLLAMA, model="nomic-embed-text", api_base="http://localhost:11434")` |
| Sentence Transformers | `EmbeddingConfig(provider=EmbeddingProvider.SENTENCE_TRANSFORMERS, model="all-MiniLM-L6-v2")` |

### Usage

```python
# Initialize service
config = EmbeddingConfig(
    provider=EmbeddingProvider.OPENAI,
    model="text-embedding-ada-002",
    dimension=1536,
    api_key="your-api-key",
)

service = EmbeddingService(
    config=config,
    cache_client=redis_client,  # Optional Redis cache
    cache_ttl=86400,  # 24 hours
)

# Generate embedding for single text
embedding = await service.embed("Hello, world!")
print(f"Dimension: {len(embedding)}")

# Generate embeddings for multiple texts
embeddings = await service.embed_many([
    "First text",
    "Second text",
    "Third text",
])

# Get statistics
stats = service.get_stats()
print(f"Total requests: {stats['total_requests']}")
print(f"Cache hit rate: {stats['cache_hits'] / stats['total_requests']}")
```

---

## Memory Compactor

### Overview

The `MemoryCompactor` intelligently reduces memory usage while preserving important information.

### Configuration

```python
from adk.plugins.memory_plugins.memory_compactor import (
    MemoryCompactor,
    CompactionConfig,
    CompactionStrategy,
    CompactionLevel,
)

config = CompactionConfig(
    strategy=CompactionStrategy.HYBRID,
    level=CompactionLevel.MODERATE,
    keep_recent_hours=24,
    keep_important_days=7,
    min_importance=0.3,
)

compactor = MemoryCompactor(
    embedding_service=embedding_service,
    llm_summarizer=summarization_fn,  # Optional LLM function
    config=config,
)
```

### Compaction Strategies

| Strategy | Description |
|----------|-------------|
| `LLM_SUMMARIZATION` | Uses LLM to summarize groups of memories |
| `STATISTICAL` | Filters based on importance scores |
| `SEMANTIC_CLUSTERING` | Groups similar memories and keeps representatives |
| `TEMPORAL_WINDOWING` | Keeps recent and important old memories |
| `IMPORTANCE_PRIORITY` | Prioritizes by importance with time decay |
| `HYBRID` | Combines multiple strategies |

### Usage

```python
from adk.plugins.memory_plugins.memory_compactor import MemorySnapshot

# Create snapshot
entries = [
    {"id": "1", "content": "...", "created_at": 1234567890, "importance": 0.8},
    # ... more entries
]
snapshot = MemorySnapshot(entries=entries)

# Run compaction
report = await compactor.compact(snapshot)

print(f"Before: {report.original_entries} entries")
print(f"After: {report.compacted_entries} entries")
print(f"Removed: {report.entries_removed} entries")
print(f"Reduction: {report.reduction_ratio:.1%}")
```

### Automatic Compaction

```python
from adk.plugins.memory_plugins.memory_compactor import AutomaticMemoryCompactor

# Create automatic compactor
auto_compactor = AutomaticMemoryCompactor(
    compactor=compactor,
    check_interval_seconds=3600,  # Check every hour
    auto_compact=True,
)

# Start
await auto_compactor.start()

# Stop
await auto_compactor.stop()
```

### Compaction Rules

```python
from adk.plugins.memory_plugins.memory_compactor import (
    TokenThresholdRule,
    EntryCountRule,
    TimeSinceLastCompactionRule,
)

# Add custom rules
compactor.add_rule(TokenThresholdRule(max_tokens=5000))
compactor.add_rule(EntryCountRule(max_entries=500))
compactor.add_rule(TimeSinceLastCompactionRule(min_hours=12))
```

---

## Best Practices

### Memory Management

1. **Use appropriate memory types**: Use `SHORT_TERM` for context, `LONG_TERM` for persistent memories
2. **Set importance scores**: Higher importance for critical information
3. **Use metadata**: Add tags and categories for better filtering
4. **Compact regularly**: Schedule periodic compaction to manage memory growth

### Caching

1. **Choose appropriate strategy**: Use `HYBRID` for most use cases
2. **Set sensible TTL**: Balance between freshness and performance
3. **Monitor hit rates**: Adjust similarity threshold based on usage
4. **Use adaptive TTL**: Automatically extends cache for frequently accessed items

### Vector Search

1. **Index efficiently**: Use appropriate algorithm (HNSW for large datasets)
2. **Use filters**: Apply filters before vector search for better performance
3. **Batch embeddings**: Generate embeddings in batches when possible
4. **Cache embeddings**: Use embedding service caching for repeated queries

---

## Performance Tuning

### Redis Configuration

```python
# For high-throughput scenarios
redis_config = RedisConfig(
    host="localhost",
    port=6379,
    # Enable connection pooling
    max_connections=50,
    # Use persistent connections
    connection_pool=True,
    # Enable compression for large payloads
    compression=True,
)
```

### Embedding Service

```python
# Optimize for performance
config = EmbeddingConfig(
    provider=EmbeddingProvider.OPENAI,
    batch_size=100,  # Larger batches for API calls
    max_retries=3,
    timeout=30.0,
)
```

### Cache Configuration

```python
# High-performance caching
cache_config = SemanticCacheConfigV2(
    similarity_threshold=0.9,  # Higher for better precision
    enable_exact_cache=True,  # Always enable exact matching
    eviction_policy=EvictionPolicy.ADAPTIVE,
)
```

---

## Error Handling

```python
try:
    # Memory operations
    entry_id = await memory_manager.add(content="...")
    entry = await memory_manager.get(entry_id)
except Exception as e:
    logger.error(f"Memory error: {e}")
    # Handle error appropriately

try:
    # Cache operations
    hit = await cache.get(query="...")
    if not hit:
        # Fallback to computation
        response = await compute()
except Exception as e:
    logger.error(f"Cache error: {e}")
    # Continue without cache
```

---

## Monitoring and Metrics

### Memory Manager Stats

```python
stats = memory_manager.get_stats()
print(f"Total entries: {stats['total_entries']}")
print(f"Total queries: {stats['total_queries']}")
print(f"Cache hit rate: {stats['hit_rate']}")
```

### Cache Stats

```python
stats = cache.get_stats()
print(f"Hit rate: {stats['hit_rate']:.2%}")
print(f"Exact hits: {stats['exact_hits']}")
print(f"Semantic hits: {stats['semantic_hits']}")
print(f"Tokens saved: {stats['total_tokens_saved']}")
```

### Embedding Service Stats

```python
stats = embedding_service.get_stats()
print(f"Total requests: {stats['total_requests']}")
print(f"Cache hit rate: {stats['cache_hits'] / stats['total_requests']}")
```