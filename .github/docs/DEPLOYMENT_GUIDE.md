# GL Unified Charter Activated
# Complete Deployment Guide

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- kubectl 1.25+ (for Kubernetes)
- Helm 3.0+ (optional)
- 8GB RAM minimum
- 50GB disk space

## Quick Start

### Docker Compose (Development)

```bash
# Clone repository
git clone https://github.com/MachineNativeOps/machine-native-ops.git
cd machine-native-ops

# Set environment variables
export REDIS_PASSWORD="your-secure-password"
export GRAFANA_ADMIN_PASSWORD="admin-password"
export EMBEDDING_API_KEY="your-api-key"

# Start services
docker-compose up -d

# Verify deployment
docker-compose ps
```

### Kubernetes (Production)

```bash
# Set up secrets
export REDIS_PASSWORD="your-secure-password"
export GRAFANA_ADMIN_PASSWORD="admin-password"
export EMBEDDING_API_KEY="your-api-key"

# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Apply secrets
envsubst < kubernetes/secrets.yaml | kubectl apply -f -

# Deploy infrastructure
kubectl apply -f kubernetes/redis-deployment.yaml
kubectl apply -f kubernetes/monitoring-deployment.yaml

# Deploy application
kubectl apply -f kubernetes/deployment.yaml

# Verify
kubectl get all -n cache-system
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Load Balancer                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Ingress / Gateway                         │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Pod 1      │    │   Pod 2      │    │   Pod 3      │
│  Memory      │    │  Memory      │    │  Memory      │
│  Cache       │    │  Cache       │    │  Cache       │
└──────────────┘    └──────────────┘    └──────────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Redis Cluster (3 replicas)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Monitoring Stack                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │Prometheus│  │ Grafana  │  │  Jaeger  │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Options

### Option 1: Docker Compose

**Use for**: Development, testing, small-scale production

**Pros**:
- Simple setup
- All-in-one deployment
- Easy to debug

**Cons**:
- Limited scalability
- Single point of failure
- No auto-scaling

### Option 2: Kubernetes

**Use for**: Production, large-scale, high availability

**Pros**:
- Auto-scaling
- Self-healing
- High availability
- Rolling updates

**Cons**:
- Complex setup
- Higher resource requirements
- Steeper learning curve

## Configuration

### Environment Variables

Create `.env` file:

```bash
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-secure-password
REDIS_TLS_ENABLED=true

# Application Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
API_PORT=8080

# Embedding Service
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_API_KEY=your-api-key

# Monitoring
GRAFANA_ADMIN_PASSWORD=admin-password
PROMETHEUS_ENABLED=true

# Security
JWT_SECRET=your-jwt-secret
ENCRYPTION_KEY=your-encryption-key
```

### Multi-Layer Cache Configuration

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
```

## Health Checks

### Docker Compose

```bash
# Check all services
docker-compose ps

# Check logs
docker-compose logs -f memory-cache

# Health check
curl http://localhost:8080/health
```

### Kubernetes

```bash
# Check pod status
kubectl get pods -n cache-system

# Check pod health
kubectl describe pod <pod-name> -n cache-system

# Check logs
kubectl logs -f <pod-name> -n cache-system

# Health check
kubectl exec -n cache-system <pod-name> -- curl localhost:8080/health
```

## Scaling

### Horizontal Scaling (Docker Compose)

```yaml
# docker-compose.yaml
services:
  memory-cache:
    deploy:
      replicas: 3
```

### Horizontal Pod Autoscaler (Kubernetes)

```yaml
# Already configured in deployment.yaml
# Auto-scales based on CPU and memory usage
minReplicas: 3
maxReplicas: 10
```

### Vertical Scaling

```yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "1000m"
  limits:
    memory: "2Gi"
    cpu: "2000m"
```

## Monitoring

### Accessing Dashboards

- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **Jaeger**: http://localhost:16686
- **Redis Insight**: http://localhost:8001

### Key Metrics

Monitor these metrics:

```yaml
Cache Performance:
  - cache_hit_rate (target: >80%)
  - cache_latency_p99 (target: <100ms)
  - cache_memory_usage (target: <80%)

Redis Health:
  - redis_memory_used
  - redis_connected_clients
  - redis_commands_per_second

Application Health:
  - http_requests_total
  - http_request_duration_seconds
  - error_rate
```

## Backup & Recovery

### Redis Backup

```bash
# Create backup
kubectl exec -n cache-system redis-0 -- redis-cli BGSAVE

# Copy backup file
kubectl cp cache-system/redis-0:/data/dump.rdb ./backup/dump.rdb
```

### Restore

```bash
# Copy backup file
kubectl cp ./backup/dump.rdb cache-system/redis-0:/data/dump.rdb

# Restart Redis
kubectl rollout restart statefulset/redis -n cache-system
```

## Security

### TLS Configuration

```yaml
# Enable TLS in redis.conf
tls-port 6379
tls-cert-file /etc/redis/certs/redis-server.crt
tls-key-file /etc/redis/certs/redis-server.key
tls-ca-cert-file /etc/redis/certs/ca.crt
tls-auth-clients yes
```

### RBAC Configuration

```yaml
security:
  rbac:
    enabled: true
    default_role: "cache_reader"
```

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cache-network-policy
spec:
  podSelector:
    matchLabels:
      app: memory-cache
  policyTypes:
  - Ingress
  - Egress
```

## Troubleshooting

### Common Issues

#### Redis Connection Failed

```bash
# Check Redis pod status
kubectl get pods -n cache-system -l app=redis

# Check Redis logs
kubectl logs -n cache-system redis-0

# Test connection
kubectl exec -n cache-system <pod-name> -- redis-cli -h redis-service ping
```

#### High Memory Usage

```bash
# Check pod memory
kubectl top pods -n cache-system

# Check cache stats
curl http://localhost:8080/stats

# Reduce cache size in config
```

#### Low Cache Hit Rate

```bash
# Check hit rate
curl http://localhost:8080/stats/layers

# Adjust TTL values
# Increase cache size
# Review access patterns
```

## Maintenance

### Rolling Updates

```bash
# Update image
kubectl set image deployment/memory-cache \
  memory-cache=machine-native-ops/memory-cache:v2.0.0 \
  -n cache-system

# Watch rollout
kubectl rollout status deployment/memory-cache -n cache-system
```

### Resource Cleanup

```bash
# Clean up old pods
kubectl delete pods -n cache-system --field-selector=status.phase=Succeeded

# Clean up old logs
kubectl logs --all-containers=true -n cache-system --tail=-1 > logs.txt
```

## Upgrade Guide

### Version Upgrade

```bash
# 1. Backup current configuration
kubectl get configmap -n cache-system -o yaml > backup-config.yaml

# 2. Update deployment
kubectl apply -f kubernetes/deployment.yaml

# 3. Verify health
kubectl rollout status deployment/memory-cache -n cache-system

# 4. Monitor metrics
curl http://localhost:8080/health
```

### Database Migration

```bash
# Export data
kubectl exec -n cache-system redis-0 -- redis-cli --rdb /data/backup.rdb

# Import to new cluster
kubectl exec -n new-redis-0 -- redis-cli --pipe < backup.rdb
```

## Production Checklist

- [ ] All secrets configured
- [ ] TLS/SSL enabled
- [ ] RBAC configured
- [ ] Monitoring enabled
- [ ] Alerts configured
- [ ] Backup schedule set
- [ ] Resource limits set
- [ ] HPA configured
- [ ] Network policies applied
- [ ] Security scanning completed
- [ ] Load testing performed
- [ ] Documentation reviewed