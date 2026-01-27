# Memory & Cache Architecture Overview

## Overview

This document provides a comprehensive overview of the Memory and Cache system architecture, including design principles, component interactions, and data flow.

## Table of Contents

- [Design Principles](#design-principles)
- [System Architecture](#system-architecture)
- [Component Overview](#component-overview)
- [Data Flow](#data-flow)
- [Integration Patterns](#integration-patterns)
- [Performance Considerations](#performance-considerations)

---

## Design Principles

### 1. Unified Interface

The system provides a single, consistent API for all memory operations regardless of the underlying storage backend.

```python
memory_manager = MemoryManager(backend="redis")
await memory_manager.add(content="...")
```

### 2. Semantic Understanding

Leverages vector embeddings to enable semantic search and similarity-based operations.

```python
results = await memory_manager.semantic_search(query="user preferences")
```

### 3. Scalability

Designed for horizontal scalability with connection pooling, batching, and distributed caching.

### 4. Performance Optimized

Multiple caching layers, adaptive TTL, and efficient indexing for low-latency operations.

### 5. Observability

Built-in metrics, logging, and tracing for monitoring and debugging.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Application Layer                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Agent A    │  │   Agent B    │  │   Agent C    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Memory Manager Layer                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Memory Mgr  │  │ Semantic S.  │  │  Compactor   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Cache & Storage Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Semantic V2  │  │  Vector Src  │  │  Redis Bknd  │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Redis Stack  │  │  Embedding   │  │   Metrics    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Overview

### 1. Memory Manager

**Purpose**: Central coordinator for all memory operations

**Key Responsibilities**:
- Unified API for memory operations
- Backend abstraction (in-memory, Redis, vector DB)
- Context window management
- Memory compaction orchestration

**Public Methods**:
```python
add(content, memory_type, session_id, user_id, importance) -> str
get(entry_id) -> MemoryEntry
query(query_text, filters) -> List[MemoryEntry]
semantic_search(query, top_k, filters) -> List[SearchResult]
compact_memories(config) -> CompactionReport
```

---

### 2. Redis Backend

**Purpose**: Persistent storage with vector search capabilities

**Key Responsibilities**:
- JSON document storage
- Vector indexing and search
- TTL and eviction
- Persistence and replication

**Data Structures**:
```redis
# Memory entry
memory:{entry_id} -> JSON
{
  "id": "mem_123",
  "content": "...",
  "embedding": [0.1, 0.2, ...],
  "metadata": {...}
}

# Vector index
idx:memory -> RediSearch Index
- Fields: content, embedding, metadata
- Algorithm: HNSW
- Distance: COSINE
```

---

### 3. Semantic Cache V2

**Purpose**: Intelligent LLM response caching

**Key Responsibilities**:
- Exact match caching
- Semantic similarity caching
- Adaptive TTL
- Multi-level eviction policies

**Cache Strategies**:
- `EXACT_ONLY`: Hash-based exact matching
- `SEMANTIC_ONLY`: Vector similarity search
- `HYBRID`: Exact match first, then semantic

---

### 4. Embedding Service

**Purpose**: Unified interface for text embeddings

**Supported Providers**:
- OpenAI
- Azure OpenAI
- Cohere
- Ollama
- Sentence Transformers

**Features**:
- Provider abstraction
- Batching support
- Built-in caching
- Fallback handling

---

### 5. Vector Search

**Purpose**: Semantic search over embeddings

**Components**:
- `VectorIndexManager`: Creates and manages vector indices
- `VectorSearchQueryBuilder`: Builds complex search queries
- `VectorSearchExecutor`: Executes vector searches
- `SemanticMemorySearch`: High-level semantic search interface

---

### 6. Memory Compactor

**Purpose**: Intelligent memory size reduction

**Strategies**:
- `LLM_SUMMARIZATION`: Summarize groups of memories
- `STATISTICAL`: Filter by importance scores
- `SEMANTIC_CLUSTERING`: Group similar memories
- `TEMPORAL_WINDOWING`: Keep recent/important memories
- `IMPORTANCE_PRIORITY`: Prioritize by importance
- `HYBRID`: Combine multiple strategies

---

### 7. Cache Middleware

**Purpose**: Transparent caching for LLM providers

**Features**:
- Decorator pattern for easy integration
- Event handlers for metrics
- Provider-specific implementations
- Request normalization

---

## Data Flow

### Adding a Memory Entry

```
1. Agent calls memory_manager.add(content)
   │
2. MemoryManager validates and creates MemoryEntry
   │
3. If vector search enabled:
   ├─ EmbeddingService.embed(content)
   │  └─ Returns [0.1, 0.2, ...]
   │
4. Backend stores entry:
   ├─ RedisBackend.add(entry)
   │  ├─ Stores JSON document
   │  └─ Stores in vector index
   │
5. Update statistics
   │
6. Emit event (if event_bus configured)
   │
7. Return entry_id
```

### Semantic Search Query

```
1. Agent calls memory_manager.semantic_search(query)
   │
2. MemoryManager calls SemanticMemorySearch.search()
   │
3. EmbeddingService.embed(query)
   ├─ Returns [0.1, 0.2, ...]
   │
4. VectorSearchExecutor.search()
   ├─ Builds RediSearch query
   ├─ Applies filters
   └─ Executes KNN search
   │
5. Retrieve matching documents from Redis
   │
6. Calculate similarity scores
   │
7. Sort and return top_k results
```

### Cache Lookup

```
1. LLM request comes in
   │
2. CacheMiddleware.intercept()
   │
3. Build cache key from request
   │
4. If HYBRID strategy:
   ├─ Try exact match (hash-based)
   │  └─ If found → Return cached response
   │
5. If no exact match:
   ├─ EmbeddingService.embed(query)
   │
6. VectorSearchExecutor.search()
   ├─ Find semantically similar cached responses
   │
7. If similarity >= threshold:
   ├─ Update access count
   ├─ Extend TTL (adaptive)
   └─ Return cached response
   │
8. If cache miss:
   ├─ Call actual LLM
   ├─ Store response in cache
   └─ Return fresh response
```

### Memory Compaction

```
1. Trigger: Timer or threshold reached
   │
2. Create MemorySnapshot from all entries
   │
3. Apply compaction strategy:
   ├─ If HYBRID:
   │  ├─ Deduplicate similar entries
   │  ├─ Apply temporal windowing
   │  ├─ Apply importance filtering
   │  └─ Ensure minimum retention
   │
4. Generate compaction report:
   ├─ original_entries
   ├─ compacted_entries
   ├─ reduction_ratio
   └─ details
   │
5. Delete removed entries from backend
   │
6. Update statistics
```

---

## Integration Patterns

### Pattern 1: Simple Memory Usage

```python
# Initialize
memory_manager = MemoryManager(backend="redis")
await memory_manager.initialize()

# Use
entry_id = await memory_manager.add(
    content="User prefers Python",
    memory_type=MemoryType.LONG_TERM,
)

results = await memory_manager.semantic_search("preferences")
```

### Pattern 2: Cached LLM Calls

```python
# Setup cache
cache = SemanticCacheV2(
    redis_client=redis,
    embedding_service=embedding,
)

middleware = CacheMiddleware(cache)

# Use decorator
@middleware.cached(model="gpt-4")
async def get_response(messages):
    return await openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
    )
```

### Pattern 3: Automatic Compaction

```python
# Setup compactor
auto_compactor = AutomaticMemoryCompactor(
    compactor=compactor,
    check_interval_seconds=3600,
)

# Start background task
await auto_compactor.start()

# System automatically compacts periodically
```

### Pattern 4: Multi-Agent Shared Memory

```python
# Each agent has its own memory manager
agent1_memory = MemoryManager(agent_id="agent1")
agent2_memory = MemoryManager(agent_id="agent2")

# But they share the same backend
shared_backend = RedisBackend(redis_client)

# Agent 1 adds memory
await agent1_memory.add(content="Shared information")

# Agent 2 can access it (if permissions allow)
results = await agent2_memory.semantic_search("shared")
```

---

## Performance Considerations

### Latency Breakdown

| Operation | Typical Latency | Optimization |
|-----------|----------------|--------------|
| Exact cache lookup | < 1ms | Hash-based lookup |
| Semantic cache lookup | 5-50ms | Vector search index |
| Embedding generation | 50-500ms | Batching + caching |
| Memory storage | 1-10ms | Pipelining |
| Vector search | 10-100ms | HNSW index tuning |

### Scaling Strategies

1. **Horizontal Scaling**
   - Deploy multiple app instances
   - Use Redis Cluster for distributed storage
   - Consistent hashing for cache distribution

2. **Vertical Scaling**
   - Increase Redis memory
   - Use larger embedding batch sizes
   - Optimize index parameters

3. **Caching Layers**
   - L1: In-memory exact match cache
   - L2: Semantic cache with vector search
   - L3: Persistent Redis storage

### Resource Planning

| Metric | Small | Medium | Large |
|--------|-------|--------|-------|
| QPS | 10 | 100 | 1000+ |
| Redis Memory | 2GB | 8GB | 32GB+ |
| App Instances | 1 | 2-3 | 5-10 |
| Embedding Rate | 10/s | 100/s | 1000/s |

---

## Security Considerations

### Data Protection

```python
# Enable Redis authentication
REDIS_PASSWORD=your-secure-password

# Use TLS for connections
REDIS_SSL=true

# Encrypt sensitive data at rest
# (Redis provides built-in encryption in some versions)
```

### Access Control

```python
# Use session-based isolation
memory_manager.add(
    content="Sensitive info",
    session_id="user_123",
    metadata={"access_level": "private"},
)

# Query with filters
results = await memory_manager.semantic_search(
    query="...",
    agent_id="agent_1",  # Filter by agent
)
```

### PII Handling

```python
# Use PII filtering
from adk.plugins.pii_filter import PIIFilter

filtered_content = PIIFilter.sanitize(content)
await memory_manager.add(content=filtered_content)
```

---

## Monitoring and Observability

### Key Metrics

```
# Cache performance
cache_hit_rate
cache_miss_rate
cache_latency_ms

# Memory usage
memory_entries_total
memory_bytes_used
memory_compaction_ratio

# Vector search
vector_search_latency_ms
vector_search_accuracy
embedding_generation_time_ms

# Infrastructure
redis_memory_used_bytes
redis_connections_active
redis_ops_per_second
```

### Logging

```python
# Structured logging
logger.info(
    "Cache hit",
    extra={
        "query_hash": "abc123",
        "similarity": 0.95,
        "tokens_saved": 150,
    }
)
```

---

## Future Enhancements

### Planned Features

1. **Distributed Vector Search**
   - Multi-node vector indexing
   - Federated search across clusters

2. **Advanced Compression**
   - Delta compression for embeddings
   - Sparse vector representations

3. **Machine Learning**
   - Adaptive importance scoring
   - Predictive caching

4. **Multi-Model Support**
   - Multiple embedding models per entry
   - Model-specific search

5. **Event-Driven Architecture**
   - Real-time memory synchronization
   - Pub/sub for memory updates