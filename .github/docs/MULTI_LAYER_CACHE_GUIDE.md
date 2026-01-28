# GL Unified Charter Activated
# Multi-Layer Cache Architecture Guide

## Overview

The Multi-Layer Cache system implements a three-tier caching architecture:

- **L1 (In-Memory)**: Fast, short-term cache with LRU eviction
- **L2 (Redis)**: Distributed, medium-term cache with persistence
- **L3 (Vector Database)**: Semantic similarity cache for intelligent retrieval

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Multi-Layer Cache Manager                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Cache Strategy & Promotion              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│     L1       │    │     L2       │    │     L3       │
│  In-Memory   │◄──►│    Redis     │◄──►│   Vector DB  │
│  (LRU)       │    │  (Distributed│    │ (Semantic)   │
│  1000 items  │    │   + TTL)     │    │  Similarity  │
│  5 min TTL   │    │  1 hour TTL  │    │  24 hour TTL │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Installation

### Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f memory-cache

# Stop services
docker-compose down
```

### Kubernetes

```bash
# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Apply secrets (replace placeholders)
envsubst < kubernetes/secrets.yaml | kubectl apply -f -

# Deploy Redis
kubectl apply -f kubernetes/redis-deployment.yaml

# Deploy monitoring
kubectl apply -f kubernetes/monitoring-deployment.yaml

# Deploy application
kubectl apply -f kubernetes/deployment.yaml

# Check status
kubectl get all -n cache-system
```

## Configuration

### Basic Configuration

```python
from memory_plugins.multi_layer_cache import (
    MultiLayerCache,
    L1Cache,
    L2Cache,
    L3Cache
)

# Initialize layers
l1 = L1Cache(max_size=1000, ttl=300)
l2 = L2Cache(redis_client=redis, ttl=3600)
l3 = L3Cache(vector_manager=vector_manager, similarity_threshold=0.85)

# Create multi-layer cache
cache = MultiLayerCache(l1=l1, l2=l2, l3=l3)
```

### Configuration File

Edit `config/multi_layer_cache.yaml`:

```yaml
l1_cache:
  enabled: true
  max_size: 1000
  ttl: 300

l2_cache:
  enabled: true
  ttl: 3600

l3_cache:
  enabled: true
  similarity_threshold: 0.85
  ttl: 86400
```

## Usage

### Basic Operations

```python
# Get value (automatically checks L1 → L2 → L3)
value = await cache.get("user:123")

# Set value in all layers
await cache.set("user:123", {"name": "John", "age": 30})

# Set with embedding for L3 semantic search
await cache.set(
    "user:123",
    {"name": "John"},
    embedding=embedding_service.get_embedding("John Doe")
)

# Delete from all layers
await cache.delete("user:123")

# Clear all layers
await cache.clear()
```

### Cache Statistics

```python
# Get statistics for all layers
stats = await cache.get_stats()
print(stats)

# Output:
# {
#   'timestamp': '2026-01-27T05:40:00',
#   'layers': {
#     'L1': {'hits': 1000, 'misses': 100, 'hit_rate': 0.91},
#     'L2': {'hits': 100, 'misses': 10, 'hit_rate': 0.91},
#     'L3': {'hits': 10, 'misses': 5, 'hit_rate': 0.67}
#   },
#   'aggregate': {
#     'total_hits': 1110,
#     'total_misses': 115,
#     'overall_hit_rate': 0.91
#   }
# }
```

### Cache Warming

```python
# Pre-load cache with data
warmup_data = {
    "user:1": {"name": "Alice"},
    "user:2": {"name": "Bob"},
    # ... more data
}

embeddings = {
    "user:1": embedding_service.get_embedding("Alice"),
    "user:2": embedding_service.get_embedding("Bob"),
    # ... more embeddings
}

await cache.warm_up(warmup_data, embeddings)
```

## Cache Promotion & Demotion

The cache automatically promotes/demotes data between layers:

1. **Promotion**: When data is frequently accessed in L2, it's promoted to L1
2. **Demotion**: When data is infrequently accessed in L1, it's demoted to L2
3. **Eviction**: Least recently used items are evicted when at capacity

## Performance Optimization

### Tuning Parameters

```yaml
# Increase L1 size for higher hit rate
l1_cache:
  max_size: 2000  # Default: 1000

# Adjust TTL for your use case
l2_cache:
  ttl: 7200  # 2 hours instead of 1 hour

# Optimize similarity threshold
l3_cache:
  similarity_threshold: 0.90  # More strict matching
```

### Monitoring

Access metrics at:
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

Key metrics:
- `cache_hits_total`: Total cache hits
- `cache_misses_total`: Total cache misses
- `cache_hit_rate`: Overall hit rate
- `cache_latency_seconds`: Operation latency

## Troubleshooting

### Low Hit Rate

```bash
# Check statistics
curl http://localhost:8080/stats

# Increase L1 cache size
# Adjust TTL values
# Review access patterns
```

### Memory Issues

```bash
# Check L1 memory usage
curl http://localhost:8080/stats/l1

# Reduce L1 max_size
# Enable compression
```

### Redis Connection Issues

```bash
# Check Redis health
kubectl exec -n cache-system redis-0 -- redis-cli ping

# Check connection logs
kubectl logs -n cache-system memory-cache-xxx
```

## Best Practices

1. **Cache warming**: Pre-load frequently accessed data
2. **TTL tuning**: Adjust based on data volatility
3. **Monitoring**: Set up alerts for low hit rates
4. **Capacity planning**: Monitor memory usage trends
5. **Graceful degradation**: Configure fallback behavior