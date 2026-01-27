# Memory & Cache Deployment Guide

## Overview

This guide provides instructions for deploying the Memory and Cache components in production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Redis Stack Setup](#redis-stack-setup)
- [Environment Configuration](#environment-configuration)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Monitoring Setup](#monitoring-setup)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Software Requirements

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11+
- Redis 7.2+ (for production)

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Redis | 2GB RAM | 8GB+ RAM |
| Application | 1 CPU, 1GB RAM | 4 CPU, 4GB RAM |
| Storage | 10GB | 50GB+ SSD |

---

## Redis Stack Setup

### Option 1: Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  redis-stack:
    image: redis/redis-stack:7.2.0-v9
    container_name: memory-redis
    ports:
      - "6379:6379"
      - "8001:8001"  # RedisInsight UI
    volumes:
      - redis_data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf
    command: >
      redis-server
      --loadmodule /opt/redis-stack/lib/redisearch.so
      --loadmodule /opt/redis-stack/lib/redisjson.so
      --loadmodule /opt/redis-stack/lib/redistimeseries.so
    environment:
      - REDIS_MAX_MEMORY=4gb
      - REDIS_MAX_MEMORY_POLICY=allkeys-lru
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

volumes:
  redis_data:
    driver: local
```

Start Redis Stack:

```bash
docker-compose up -d
```

Access RedisInsight at `http://localhost:8001`

### Option 2: Native Installation

```bash
# Download Redis Stack
wget https://redis.io/download/redis-stack-server-7.2.0-v9-linux-x64.tar.gz

# Extract
tar -xzf redis-stack-server-7.2.0-v9-linux-x64.tar.gz

# Run
cd redis-stack-server-7.2.0-v9-linux-x64
./redis-stack-server --port 6379
```

### Option 3: Redis Cloud

1. Sign up at [Redis Cloud](https://redis.com/try-free/)
2. Create a new database
3. Enable Redis Stack modules
4. Get connection string

---

## Environment Configuration

### Environment Variables

Create `.env` file:

```bash
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your-redis-password
REDIS_PREFIX=memory:

# Vector Search Configuration
ENABLE_VECTOR_SEARCH=true
VECTOR_DIM=1536
VECTOR_INDEX_NAME=idx:memory

# Embedding Service Configuration
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_API_KEY=your-openai-api-key
EMBEDDING_API_BASE=https://api.openai.com/v1
EMBEDDING_CACHE_TTL=86400
EMBEDDING_BATCH_SIZE=100

# Cache Configuration
CACHE_ENABLED=true
CACHE_STRATEGY=hybrid
CACHE_SIMILARITY_THRESHOLD=0.85
CACHE_DEFAULT_TTL=3600
CACHE_MAX_ENTRIES=10000
CACHE_EV POLICY=adaptive

# Memory Compactor Configuration
COMPACTION_ENABLED=true
COMPACTION_STRATEGY=hybrid
COMPACTION_LEVEL=moderate
COMPACTION_CHECK_INTERVAL_HOURS=24

# Application Configuration
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Configuration File

Create `config/memory_config.yaml`:

```yaml
memory:
  backend: redis
  enable_vector_search: true

redis:
  host: ${REDIS_HOST}
  port: ${REDIS_PORT}
  db: ${REDIS_DB}
  password: ${REDIS_PASSWORD}
  prefix: ${REDIS_PREFIX}
  pool_size: 50
  socket_timeout: 5
  socket_connect_timeout: 5
  retry_on_timeout: true

vector_search:
  enabled: ${ENABLE_VECTOR_SEARCH}
  dimension: ${VECTOR_DIM}
  index_name: ${VECTOR_INDEX_NAME}
  distance_metric: COSINE
  algorithm: HNSW

embedding:
  provider: ${EMBEDDING_PROVIDER}
  model: ${EMBEDDING_MODEL}
  api_key: ${EMBEDDING_API_KEY}
  api_base: ${EMBEDDING_API_BASE}
  cache_ttl: ${EMBEDDING_CACHE_TTL}
  batch_size: ${EMBEDDING_BATCH_SIZE}
  max_retries: 3
  timeout: 30.0

cache:
  enabled: ${CACHE_ENABLED}
  strategy: ${CACHE_STRATEGY}
  similarity_threshold: ${CACHE_SIMILARITY_THRESHOLD}
  default_ttl: ${CACHE_DEFAULT_TTL}
  max_entries: ${CACHE_MAX_ENTRIES}
  eviction_policy: ${CACHE_EV POLICY}
  enable_adaptive_ttl: true

compactor:
  enabled: ${COMPACTION_ENABLED}
  strategy: ${COMPACTION_STRATEGY}
  level: ${COMPACTION_LEVEL}
  check_interval_seconds: ${COMPACTION_CHECK_INTERVAL_HOURS}
  keep_recent_hours: 24
  keep_important_days: 7
  min_importance: 0.3
```

---

## Docker Deployment

### Build Application Image

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
# Build image
docker build -t memory-app:latest .

# Run container
docker run -d \
  --name memory-app \
  --env-file .env \
  -p 8000:8000 \
  memory-app:latest
```

### Docker Compose (Full Stack)

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  redis:
    image: redis/redis-stack:7.2.0-v9
    container_name: memory-redis
    ports:
      - "6379:6379"
      - "8001:8001"
    volumes:
      - redis_data:/data
    environment:
      - REDIS_MAX_MEMORY=4gb
      - REDIS_MAX_MEMORY_POLICY=allkeys-lru
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: memory-app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      redis:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    restart: unless-stopped

volumes:
  redis_data:
  prometheus_data:
  grafana_data:
```

Deploy:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Kubernetes Deployment

### Namespace and ConfigMap

Create `k8s/namespace.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: memory-system
```

Create `k8s/configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: memory-config
  namespace: memory-system
data:
  memory_config.yaml: |
    memory:
      backend: redis
      enable_vector_search: true
    redis:
      host: redis-service
      port: 6379
      prefix: memory:
    vector_search:
      enabled: true
      dimension: 1536
```

### Redis Deployment

Create `k8s/redis-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: memory-system
spec:
  serviceName: redis-service
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis/redis-stack:7.2.0-v9
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-data
          mountPath: /data
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        command:
        - redis-server
        - --loadmodule /opt/redis-stack/lib/redisearch.so
        - --loadmodule /opt/redis-stack/lib/redisjson.so
        - --maxmemory 3gb
        - --maxmemory-policy allkeys-lru
        livenessProbe:
          exec:
            command:
            - redis-cli
            - ping
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - redis-cli
            - ping
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: memory-system
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
  namespace: memory-system
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

### Application Deployment

Create `k8s/app-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: memory-app
  namespace: memory-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: memory-app
  template:
    metadata:
      labels:
        app: memory-app
    spec:
      containers:
      - name: app
        image: memory-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_HOST
          value: "redis-service"
        - name: REDIS_PORT
          value: "6379"
        - name: LOG_LEVEL
          value: "INFO"
        - name: ENVIRONMENT
          value: "production"
        envFrom:
        - secretRef:
            name: memory-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: memory-app-service
  namespace: memory-system
spec:
  selector:
    app: memory-app
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Secrets

Create `k8s/secret.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: memory-secrets
  namespace: memory-system
type: Opaque
stringData:
  REDIS_PASSWORD: your-redis-password
  EMBEDDING_API_KEY: your-openai-api-key
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets
kubectl apply -f k8s/secret.yaml

# Deploy Redis
kubectl apply -f k8s/redis-deployment.yaml

# Deploy application
kubectl apply -f k8s/app-deployment.yaml

# Check status
kubectl get pods -n memory-system
kubectl get services -n memory-system

# View logs
kubectl logs -f deployment/memory-app -n memory-system
```

---

## Monitoring Setup

### Prometheus Configuration

Create `monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'memory-app'
    static_configs:
      - targets: ['app:8000']
    metrics_path: '/metrics'

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

### Grafana Dashboard

Key metrics to monitor:

- Memory cache hit rate
- Vector search query latency
- Embedding service performance
- Redis memory usage
- Compaction efficiency

Create dashboard at `monitoring/grafana/dashboards/memory-dashboard.json`:

```json
{
  "dashboard": {
    "title": "Memory System Dashboard",
    "panels": [
      {
        "title": "Cache Hit Rate",
        "targets": [
          {
            "expr": "cache_hit_rate"
          }
        ]
      },
      {
        "title": "Vector Search Latency",
        "targets": [
          {
            "expr": "vector_search_latency_ms"
          }
        ]
      },
      {
        "title": "Redis Memory Usage",
        "targets": [
          {
            "expr": "redis_memory_used_bytes"
          }
        ]
      }
    ]
  }
}
```

### Health Checks

Create `monitoring/health.sh`:

```bash
#!/bin/bash

# Check Redis
redis-cli -h localhost -p 6379 ping

# Check application health
curl -f http://localhost:8000/health || exit 1

# Check metrics endpoint
curl -f http://localhost:8000/metrics || exit 1

echo "All health checks passed"
```

---

## Troubleshooting

### Common Issues

#### Redis Connection Failed

```bash
# Check Redis is running
docker ps | grep redis

# Check Redis logs
docker logs memory-redis

# Test connection
redis-cli -h localhost -p 6379 ping
```

#### High Memory Usage

```bash
# Check Redis memory usage
redis-cli INFO memory

# Monitor memory growth
redis-cli --stat

# Adjust max memory policy
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

#### Slow Vector Search

```bash
# Check index info
redis-cli FT.INFO idx:memory

# Rebuild index if needed
redis-cli FT.DROPINDEX idx:memory DD
# Then recreate index
```

#### Cache Low Hit Rate

```bash
# Check cache statistics
curl http://localhost:8000/metrics | grep cache

# Adjust similarity threshold
# Lower threshold = more cache hits but lower precision
```

### Log Analysis

```bash
# View application logs
tail -f logs/app.log

# Filter for errors
grep ERROR logs/app.log

# Monitor performance
grep "Latency:" logs/app.log
```

### Performance Optimization

```bash
# Enable connection pooling
export REDIS_POOL_SIZE=50

# Increase batch size for embeddings
export EMBEDDING_BATCH_SIZE=200

# Use compression for large payloads
export REDIS_COMPRESSION=true
```

---

## Scaling Considerations

### Horizontal Scaling

- Deploy multiple application instances behind a load balancer
- Use Redis Cluster for distributed storage
- Implement consistent hashing for cache distribution

### Vertical Scaling

- Increase Redis memory allocation
- Use larger instance types for application
- Optimize embedding batch sizes

### Database Optimization

```bash
# Configure Redis persistence
redis-cli CONFIG SET save "900 1 300 10 60 10000"

# Enable AOF persistence
redis-cli CONFIG SET appendonly yes

# Optimize for SSD
redis-cli CONFIG SET io-threads 4
```

---

## Backup and Recovery

### Redis Backup

```bash
# Create snapshot
redis-cli BGSAVE

# Copy RDB file
cp /var/lib/redis/dump.rdb /backup/dump_$(date +%Y%m%d).rdb

# Restore
redis-cli --rdb /backup/dump_20231201.rdb
```

### Kubernetes Backup

```bash
# Backup Redis volume
kubectl exec -n memory-system redis-0 -- redis-cli BGSAVE
kubectl exec -n memory-system redis-0 -- cat /data/dump.rdb > backup.rdb

# Restore
kubectl cp backup.rdb memory-system/redis-0:/data/dump.rdb
kubectl exec -n memory-system redis-0 -- redis-cli SHUTDOWN NOSAVE
kubectl exec -n memory-system redis-0 -- redis-server
```