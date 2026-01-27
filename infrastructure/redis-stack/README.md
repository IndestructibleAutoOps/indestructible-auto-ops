# Redis Stack Infrastructure

## Quick Start

```bash
cd infrastructure/redis-stack
docker-compose up -d
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| Redis | 6379 | Redis server with vector search |
| RedisInsight | 8001 | Web UI for Redis management |

## Verify

```bash
docker exec adk-redis-stack redis-cli ping
```

## Stop

```bash
docker-compose down
```

## Data Persistence

Data is stored in `redis_data` volume.