# Agent Memory & Cache System

Complete memory management and caching solution for AI agents, featuring semantic search, intelligent compaction, and vector-based retrieval.

## Features

### Core Capabilities

- **Unified Memory Management**: Single API for short-term (context) and long-term memory
- **Semantic Search**: Vector-based similarity search using Redis Stack
- **Intelligent Caching**: Multi-level caching with semantic similarity
- **Memory Compaction**: Automatic memory size reduction with multiple strategies
- **Multi-Provider Embeddings**: Support for OpenAI, Azure, Cohere, Ollama, and local models
- **LLM Integration**: Transparent caching for OpenAI, Anthropic, and other LLM providers

### Key Components

| Component | Description |
|-----------|-------------|
| `MemoryManager` | Unified interface for all memory operations |
| `RedisMemoryBackend` | Persistent storage with vector search |
| `SemanticCacheV2` | Enhanced caching with adaptive TTL |
| `EmbeddingService` | Multi-provider text embeddings |
| `VectorSearchExecutor` | High-performance semantic search |
| `MemoryCompactor` | Intelligent memory compaction |

## Quick Start

### Installation

```bash
# Install dependencies
pip install redis[hiredis] openai cohere-async

# For local embeddings
pip install sentence-transformers

# For Ollama
pip install aiohttp
```

### Basic Usage

```python
import asyncio
from adk.core.memory_manager import MemoryManager, MemoryType

async def main():
    # Initialize memory manager
    memory_manager = MemoryManager(
        backend="redis",
        enable_vector_search=True,
        embedding_provider="openai",
        embedding_model="text-embedding-ada-002",
    )
    await memory_manager.initialize()

    # Add a memory
    entry_id = await memory_manager.add(
        content="The user prefers Python over JavaScript",
        memory_type=MemoryType.LONG_TERM,
        importance=0.9,
    )

    # Search semantically
    results = await memory_manager.semantic_search(
        query="programming preferences",
        top_k=5,
    )

    for result in results:
        print(f"[{result.score:.2f}] {result.content}")

asyncio.run(main())
```

## Documentation

| Document | Description |
|----------|-------------|
| [API Guide](docs/memory-api-guide.md) | Comprehensive API documentation |
| [Deployment Guide](docs/deployment-guide.md) | Production deployment instructions |
| [Architecture Overview](docs/architecture-overview.md) | System design and architecture |
| [Usage Examples](docs/examples.md) | Practical code examples |

## Architecture

```
Application Layer
    ↓
Memory Manager (unified API)
    ↓
┌─────────────┬─────────────┬─────────────┐
│   Cache     │   Vector    │  Storage    │
│   Layer     │   Search    │   Layer     │
└─────────────┴─────────────┴─────────────┘
    ↓
Redis Stack (Storage + Vector Search)
```

## Components

### Memory Manager

Central coordinator for all memory operations:

```python
from adk.core.memory_manager import MemoryManager

manager = MemoryManager(
    backend="redis",
    enable_vector_search=True,
)

# Add memory
entry_id = await manager.add(content="...")

# Query memory
results = await manager.semantic_search(query="...")

# Compact memory
report = await manager.compact_memories()
```

### Semantic Cache

Intelligent LLM response caching:

```python
from adk.plugins.memory_plugins.semantic_cache_v2 import (
    SemanticCacheV2,
    SemanticCacheConfigV2,
)

cache = SemanticCacheV2(
    redis_client=redis,
    embedding_service=embedding,
)

# Get or compute
response, was_cached = await cache.get_or_compute(
    query="...",
    compute_fn=lambda: generate_response(),
)
```

### Vector Search

Semantic search over embeddings:

```python
from adk.plugins.memory_plugins.vector_search import SemanticMemorySearch

search = SemanticMemorySearch(
    redis_client=redis,
    embedding_service=embedding,
)

results = await search.search(
    query="user preferences",
    top_k=10,
)
```

### Memory Compactor

Intelligent memory size reduction:

```python
from adk.plugins.memory_plugins.memory_compactor import (
    MemoryCompactor,
    CompactionConfig,
)

compactor = MemoryCompactor(
    embedding_service=embedding,
    config=CompactionConfig(
        strategy="hybrid",
        level="moderate",
    ),
)

report = await compactor.compact(snapshot)
```

## Configuration

### Environment Variables

```bash
# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Embedding Service
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_API_KEY=sk-...

# Cache
CACHE_ENABLED=true
CACHE_STRATEGY=hybrid
CACHE_SIMILARITY_THRESHOLD=0.85

# Compaction
COMPACTION_ENABLED=true
COMPACTION_STRATEGY=hybrid
```

### Configuration File

```yaml
memory:
  backend: redis
  enable_vector_search: true

redis:
  host: ${REDIS_HOST}
  port: ${REDIS_PORT}
  prefix: memory:

vector_search:
  enabled: true
  dimension: 1536
  algorithm: HNSW

cache:
  enabled: true
  strategy: hybrid
  similarity_threshold: 0.85
  max_entries: 10000

compactor:
  enabled: true
  strategy: hybrid
  level: moderate
```

## Deployment

### Docker Compose

```bash
cd infrastructure/redis-stack
docker compose up -d
```

### Kubernetes

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/app-deployment.yaml
```

See [Deployment Guide](docs/deployment-guide.md) for details.

## Performance

| Operation | Latency | Throughput |
|-----------|---------|------------|
| Exact cache lookup | < 1ms | 10,000+ QPS |
| Semantic cache lookup | 5-50ms | 500+ QPS |
| Memory storage | 1-10ms | 1,000+ QPS |
| Vector search | 10-100ms | 100+ QPS |

## Best Practices

1. **Use appropriate memory types**
   - `SHORT_TERM` for context window
   - `LONG_TERM` for persistent knowledge

2. **Set importance scores**
   - Higher scores for critical information
   - Scores affect compaction decisions

3. **Use metadata effectively**
   - Add tags and categories
   - Enable efficient filtering

4. **Enable caching**
   - Use `HYBRID` strategy for most cases
   - Adjust similarity threshold based on needs

5. **Schedule compaction**
   - Run regularly to manage memory growth
   - Use `MODERATE` level for balanced performance

## Testing

```bash
# Run unit tests
pytest ns-root/namespaces-adk/adk/core/tests/

# Run with coverage
pytest --cov=adk/plugins/memory_plugins

# Run specific test suite
pytest test_vector_search.py -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is part of the MachineNativeOps agent development kit.

## Related Projects

- [Agent Development Kit (ADK)](../ns-root/namespaces-adk/README.md)
- [Redis Stack](https://redis.io/docs/stack/)
- [OpenAI API](https://platform.openai.com/docs)

## Support

For issues and questions, please open an issue on GitHub.

## Changelog

### P5 (Latest)
- Added comprehensive documentation
- Added API guide, deployment guide, architecture overview
- Added usage examples and best practices

### P4
- Added MemoryCompactor with multiple strategies
- Added automatic memory compaction
- Integration with MemoryManager

### P3
- Added SemanticCacheV2 with enhanced features
- Added CacheMiddleware for LLM integration
- Event handlers for monitoring

### P2
- Added VectorIndexManager for Redis Stack
- Added EmbeddingService with multi-provider support
- Added VectorSearchExecutor

### P1
- Added RedisMemoryBackend
- Added SemanticCache (V1)
- Basic infrastructure

## GL Governance Markers

```
@gl-layer GL-00-NAMESPACE
@gl-module research/agent-memory-cache
@gl-semantic-anchor GL-00-RESEARCH_AGENT_MEMORY_CACHE
@gl-evidence-required false
GL Unified Charter Activated
```