# Production Configuration Guide

## Complete Configuration Template

This guide provides a comprehensive production configuration for the Agent Memory Cache system.

## File Structure

```
ns-root/namespaces-adk/adk/plugins/memory_plugins/config/
├── production_config.yaml      # Main production configuration
├── multi_layer_cache.yaml      # Multi-layer cache settings
├── security.yaml               # Security configuration
└── redis-config.yaml           # Redis-specific settings
```

## Configuration Files

### 1. Production Configuration (production_config.yaml)

This is the main configuration file that includes all subsystems:

```yaml
version: "1.0.0"
environment: "production"

# Redis Configuration
redis:
  host: "${REDIS_HOST:-redis-service.cache-system.svc.cluster.local}"
  port: ${REDIS_PORT:-6379}
  password: "${REDIS_PASSWORD}"
  tls_enabled: ${REDIS_TLS_ENABLED:-true}
  connection_pool:
    min_connections: ${REDIS_POOL_MIN:-5}
    max_connections: ${REDIS_POOL_MAX:-20}

# Multi-Layer Cache
multi_layer_cache:
  l1:
    enabled: true
    max_size: ${L1_MAX_SIZE:-1000}
    ttl: ${L1_TTL:-300}
  l2:
    enabled: true
    ttl: ${L2_TTL:-3600}
  l3:
    enabled: true
    similarity_threshold: ${L3_SIMILARITY_THRESHOLD:-0.85}
```

### 2. Multi-Layer Cache Configuration (multi_layer_cache.yaml)

Detailed settings for each cache layer:

```yaml
# L1 Cache Configuration (In-Memory)
l1_cache:
  enabled: true
  max_size: 1000
  ttl: 300
  eviction_policy: "lru"

# L2 Cache Configuration (Redis)
l2_cache:
  enabled: true
  ttl: 3600
  pool_size: 10
  retry_attempts: 3

# L3 Cache Configuration (Vector Database)
l3_cache:
  enabled: true
  similarity_threshold: 0.85
  ttl: 86400
  index_type: "hnsw"
```

### 3. Security Configuration (security.yaml)

TLS, RBAC, and encryption settings:

```yaml
# TLS Configuration
tls:
  enabled: true
  min_version: "TLSv1.2"
  cert_file: "/etc/redis/certs/redis-server.crt"
  key_file: "/etc/redis/certs/redis-server.key"

# RBAC Configuration
rbac:
  enabled: true
  roles:
    cache_admin:
      permissions: ["cache:*"]
    cache_operator:
      permissions: ["cache:read", "cache:write"]
```

### 4. Redis Configuration (redis-config.yaml)

Redis-specific settings for Stack with vector search:

```yaml
# Redis Stack Configuration
redis:
  port: 6379
  tls-port: 0
  protected-mode: yes
  requirepass: "${REDIS_PASSWORD}"

# Modules
modules:
  - name: search
    enabled: true
  - name: json
    enabled: true

# Memory Management
maxmemory: 4gb
maxmemory-policy: allkeys-lru
```

## Environment Variables

Production environment requires these variables:

```bash
# Required
export REDIS_PASSWORD="your-secure-password"
export REDIS_HOST="redis-service.cache-system.svc.cluster.local"
export REDIS_PORT=6379

# Optional with defaults
export L1_MAX_SIZE=1000
export L1_TTL=300
export L2_TTL=3600
export L3_TTL=86400
export L3_SIMILARITY_THRESHOLD=0.85

# Security
export JWT_SECRET="your-jwt-secret"
export ENCRYPTION_KEY="your-encryption-key"

# Monitoring
export GRAFANA_ADMIN_PASSWORD="admin-password"
export PROMETHEUS_ENABLED=true

# Logging
export LOG_LEVEL=INFO
export LOG_FORMAT=json
```

## Configuration by Environment

### Development Environment

```yaml
environment: "development"

redis:
  host: "localhost"
  port: 6379
  tls_enabled: false

multi_layer_cache:
  l1:
    max_size: 100
    ttl: 60
  l2:
    ttl: 300
  l3:
    ttl: 1800

monitoring:
  prometheus:
    enabled: false

logging:
  level: "DEBUG"
```

### Staging Environment

```yaml
environment: "staging"

redis:
  host: "staging-redis.internal"
  port: 6379
  tls_enabled: true

multi_layer_cache:
  l1:
    max_size: 500
    ttl: 180
  l2:
    ttl: 1800
  l3:
    ttl: 43200

monitoring:
  prometheus:
    enabled: true

logging:
  level: "INFO"
```

### Production Environment

```yaml
environment: "production"

redis:
  host: "${REDIS_HOST}"
  port: ${REDIS_PORT}
  tls_enabled: true

multi_layer_cache:
  l1:
    max_size: 1000
    ttl: 300
  l2:
    ttl: 3600
  l3:
    ttl: 86400

monitoring:
  prometheus:
    enabled: true

security:
  rbac:
    enabled: true
  encryption:
    enabled: true

logging:
  level: "INFO"
  format: "json"
```

## Advanced Configuration

### Performance Tuning

```yaml
# Connection Pool Tuning
redis:
  connection_pool:
    min_connections: 5
    max_connections: 20
    timeout: 30
    retry_attempts: 3

# Cache Strategy
cache_strategy:
  retrieval_order: ["L1", "L2", "L3"]
  promotion_enabled: true
  promotion_threshold: 2
  demotion_enabled: true
  demotion_threshold: 3600

# Vector Search Optimization
vector_search:
  index_prefix: "cache"
  algorithm: "hnsw"
  ef_construction: 200
  ef_search: 40
  m: 16
```

### High Availability

```yaml
# Redis Sentinel
redis:
  sentinel_enabled: true
  sentinel_hosts:
    - "redis-sentinel-1:26379"
    - "redis-sentinel-2:26379"
    - "redis-sentinel-3:26379"
  leader_name: "myleader"

# Connection Resilience
resilience:
  circuit_breaker:
    enabled: true
    failure_threshold: 5
    recovery_timeout: 60
  retry:
    max_attempts: 3
    backoff_factor: 2
```

### Monitoring & Alerts

```yaml
monitoring:
  enabled: true
  metrics_interval: 60
  health_check_interval: 30
  alert_thresholds:
    hit_rate: 0.7
    latency_p99: 1000
    memory_usage: 0.8
    error_rate: 0.01

# Prometheus Scrape Config
prometheus:
  enabled: true
  port: 9090
  metrics_path: "/metrics"
  scrape_interval: 15s
```

## Loading Configuration

### Python

```python
import yaml
from pathlib import Path

def load_config(config_path: str = "config/production_config.yaml"):
    """Load production configuration."""
    config_file = Path(config_path)
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Substitute environment variables
    config = substitute_env_vars(config)
    return config

def substitute_env_vars(config: dict) -> dict:
    """Replace ${VAR} with environment variable values."""
    import os
    import re
    
    def replace_vars(value):
        if isinstance(value, str):
            pattern = r'\$\{([^}]+)\}'
            matches = re.findall(pattern, value)
            for match in matches:
                env_value = os.getenv(match, '')
                value = value.replace(f'${{{match}}}', env_value)
            return value
        elif isinstance(value, dict):
            return {k: replace_vars(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [replace_vars(item) for item in value]
        return value
    
    return replace_vars(config)

# Usage
config = load_config()
redis_host = config['redis']['host']
l1_max_size = config['multi_layer_cache']['l1']['max_size']
```

### Environment Variables Only

```python
import os

# Simple configuration from environment
config = {
    'redis': {
        'host': os.getenv('REDIS_HOST', 'localhost'),
        'port': int(os.getenv('REDIS_PORT', 6379)),
        'password': os.getenv('REDIS_PASSWORD')
    },
    'cache': {
        'l1_size': int(os.getenv('L1_MAX_SIZE', 1000)),
        'l1_ttl': int(os.getenv('L1_TTL', 300))
    }
}
```

## Configuration Validation

```python
from typing import Dict, Any
import logging

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate production configuration."""
    logger = logging.getLogger(__name__)
    
    # Check required fields
    required_fields = [
        ('redis', 'host'),
        ('redis', 'port'),
        ('redis', 'password'),
        ('multi_layer_cache', 'l1'),
        ('multi_layer_cache', 'l2'),
        ('multi_layer_cache', 'l3')
    ]
    
    for section, field in required_fields:
        if section not in config:
            logger.error(f"Missing section: {section}")
            return False
        if field not in config[section]:
            logger.error(f"Missing field: {section}.{field}")
            return False
    
    # Validate values
    if not (1 <= config['redis']['port'] <= 65535):
        logger.error("Invalid Redis port")
        return False
    
    if config['multi_layer_cache']['l1']['max_size'] <= 0:
        logger.error("Invalid L1 cache size")
        return False
    
    logger.info("Configuration validated successfully")
    return True
```

## Configuration Management Best Practices

1. **Version Control**: Store configuration templates in Git
2. **Secrets Management**: Use secrets for passwords and API keys
3. **Environment Separation**: Separate configs for dev/staging/prod
4. **Validation**: Validate configuration before deployment
5. **Documentation**: Document all configuration options
6. **Monitoring**: Monitor configuration changes
7. **Rollback**: Keep previous configurations for rollback

## Troubleshooting Configuration Issues

### Missing Environment Variables

```bash
# Check if variable is set
echo $REDIS_PASSWORD

# List all environment variables
env | grep -E "REDIS|CACHE|LOG"

# Set missing variable
export REDIS_PASSWORD="your-password"
```

### Invalid YAML

```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('config/production_config.yaml'))"

# Check for common issues
# - Indentation (use 2 spaces)
# - Quotes around special characters
# - No tabs in YAML files
```

### Configuration Not Applied

```bash
# Check if config file is loaded
kubectl describe pod <pod-name> -n cache-system

# Check ConfigMap
kubectl get configmap memory-cache-config -n cache-system -o yaml

# Restart pods to apply new config
kubectl rollout restart deployment/memory-cache -n cache-system
```