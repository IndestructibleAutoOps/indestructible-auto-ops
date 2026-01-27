# Redis Backend V2 - 完整生產級實現指南

## 概述

Redis Backend V2 是一個完整的生產級 Redis 後端實現，專為 AI Agent 記憶系統設計。它提供了高可用性、高性能和強大的容錯能力。

## 核心特性

### 1. 連接池管理
- 支持多連接池
- 可配置的最大/最小連接數
- 連接超時和重試機制

### 2. 自動重試機制
- 指數退避策略
- 線性退避策略
- 固定延遲策略
- 可配置的最大重試次數

### 3. 斷路器模式
- 自動檢測故障
- 故障閾值配置
- 自動恢復機制
- 防止級聯故障

### 4. 健康檢查
- 定期健康檢查
- 連接狀態監控
- 自動故障檢測
- 健康狀態報告

### 5. 性能監控
- 操作統計
- 成功率追蹤
- 延遲監控
- 重試次數統計

### 6. 批量操作
- Pipeline 支持
- 批量插入
- 批量更新
- 批量查詢

### 7. 事務支持
- Redis 事務
- 原子操作
- 樂觀鎖定
- 悲觀鎖定

## 架構設計

```
┌─────────────────────────────────────────────────────────┐
│                   RedisBackendV2                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ RetryHandler │  │ Circuit      │  │ Health       │  │
│  │              │  │ Breaker      │  │ Checker      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                  │                  │          │
│         └──────────────────┼──────────────────┘          │
│                            ▼                             │
│                    ┌───────────────┐                     │
│                    │ Connection    │                     │
│                    │ Pool Manager  │                     │
│                    └───────────────┘                     │
│                            ▼                             │
│                    ┌───────────────┐                     │
│                    │ Redis Client  │                     │
│                    └───────────────┘                     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Redis Stack                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │  Redis   │  │  Search  │  │  JSON    │  │  Time  │  │
│  │          │  │          │  │          │  │  Series│  │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
└─────────────────────────────────────────────────────────┘
```

## 組件說明

### RedisConfig
配置類，包含所有 Redis 相關的配置參數。

```python
from plugins.memory_plugins.redis_backend_v2 import RedisConfig

config = RedisConfig(
    host="localhost",
    port=6379,
    max_connections=50,
    circuit_breaker_enabled=True,
    health_check_enabled=True,
)
```

### CircuitBreaker
斷路器實現，防止級聯故障。

```python
breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=60.0,
)

result = await breaker.execute(operation)
```

### RetryHandler
重試處理器，提供多種重試策略。

```python
handler = RetryHandler(
    max_retries=3,
    strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
)

result = await handler.execute(operation)
```

### HealthChecker
健康檢查器，監控 Redis 連接狀態。

```python
checker = HealthChecker(
    client=redis_client,
    interval=30.0,
    enabled=True,
)

await checker.start()
is_healthy = checker.is_healthy()
```

### RedisMetrics
性能指標收集器。

```python
metrics = RedisMetrics()
# Operations are tracked automatically
print(f"Success rate: {metrics.success_rate}")
print(f"Average latency: {metrics.avg_latency_ms}")
```

## 使用示例

### 基本使用

```python
import asyncio
from plugins.memory_plugins.redis_backend_v2 import (
    RedisBackendV2,
    RedisConfig,
)
from core.memory_manager import MemoryEntry, MemoryType

async def main():
    # Create backend
    backend = RedisBackendV2(
        config=RedisConfig(
            host="localhost",
            port=6379,
            max_connections=50,
        )
    )
    
    # Initialize
    await backend.initialize()
    
    # Add entry
    entry = MemoryEntry(
        id="test1",
        content="Test memory",
        memory_type=MemoryType.LONG_TERM,
        importance=0.9,
    )
    await backend.add(entry)
    
    # Get entry
    retrieved = await backend.get("test1")
    print(f"Retrieved: {retrieved}")
    
    # Close
    await backend.close()

asyncio.run(main())
```

### 批量操作

```python
# Create multiple entries
entries = [
    MemoryEntry(
        id=f"batch_{i}",
        content=f"Batch entry {i}",
        memory_type=MemoryType.LONG_TERM,
    )
    for i in range(100)
]

# Add in batch
ids = await backend.add_batch(entries)
print(f"Added {len(ids)} entries")
```

### 向量搜索

```python
from core.memory_manager import MemoryQuery

# Query with vector embedding
query = MemoryQuery(
    embedding=[0.1, 0.2, 0.3, ...],  # Your embedding vector
    limit=10,
)

results = await backend.query(query)
for result in results:
    print(f"Score: {result.score}, Content: {result.content}")
```

### 獲取指標

```python
# Get performance metrics
metrics = backend.get_metrics()
print(f"Total operations: {metrics['total_operations']}")
print(f"Success rate: {metrics['success_rate']}")
print(f"Average latency: {metrics['avg_latency_ms']}")

# Get health status
health = backend.get_health_status()
print(f"State: {health['state']}")
print(f"Connected: {health['connected']}")
```

## 配置選項

### 連接配置

| 參數 | 類型 | 默認值 | 說明 |
|------|------|--------|------|
| host | str | localhost | Redis 主機地址 |
| port | int | 6379 | Redis 端口 |
| db | int | 0 | Redis 數據庫編號 |
| password | str | None | Redis 密碼 |
| username | str | None | Redis 用戶名 |

### 連接池配置

| 參數 | 類型 | 默認值 | 說明 |
|------|------|--------|------|
| max_connections | int | 50 | 最大連接數 |
| min_connections | int | 5 | 最小連接數 |
| connection_timeout | int | 10 | 連接超時（秒） |
| socket_timeout | int | 10 | Socket 超時（秒） |

### 重試配置

| 參數 | 類型 | 默認值 | 說明 |
|------|------|--------|------|
| max_retries | int | 3 | 最大重試次數 |
| strategy | RetryStrategy | EXPONENTIAL_BACKOFF | 重試策略 |
| delay | float | 0.1 | 初始延遲（秒） |
| max_delay | float | 10.0 | 最大延遲（秒） |

### 斷路器配置

| 參數 | 類型 | 默認值 | 說明 |
|------|------|--------|------|
| enabled | bool | True | 是否啟用 |
| failure_threshold | int | 5 | 故障閾值 |
| recovery_timeout | float | 60.0 | 恢復超時（秒） |

### 健康檢查配置

| 參數 | 類型 | 默認值 | 說明 |
|------|------|--------|------|
| enabled | bool | True | 是否啟用 |
| interval | float | 30.0 | 檢查間隔（秒） |

## 性能優化建議

### 1. 連接池大小
- 開發環境: 10-20 連接
- 生產環境: 50-100 連接
- 高負載環境: 100-200 連接

### 2. 批量操作
- 使用批量操作而非單個操作
- 批量大小: 100-1000
- 使用 Pipeline 減少網絡往返

### 3. 索引優化
- 為常用查詢字段創建索引
- 選擇合適的向量算法（FLAT vs HNSW）
- 調整 HNSW 參數（M, ef_construction, ef_runtime）

### 4. TTL 策略
- 短期記憶: 1-4 小時
- 長期記憶: 1-30 天
- 向量索引: 7-30 天

### 5. 監控和告警
- 監控成功率和延遲
- 設置斷路器告警
- 追蹤重試次數

## 故障排查

### 連接失敗
```
錯誤: ConnectionError: Error connecting to Redis

解決方案:
1. 檢查 Redis 服務是否運行
2. 驗證主機和端口配置
3. 檢查防火牆規則
4. 確認認證信息
```

### 斷路器開啟
```
錯誤: Circuit breaker is open

解決方案:
1. 等待恢復超時時間
2. 檢查 Redis 服務健康狀態
3. 調整故障閾值
4. 增加重試次數
```

### 性能問題
```
問題: 高延遲或低吞吐量

解決方案:
1. 增加連接池大小
2. 使用批量操作
3. 優化查詢和索引
4. 啟用 Pipeline
5. 檢查 Redis 服務器資源
```

## 測試

運行測試套件:

```bash
# 運行所有測試
pytest ns-root/namespaces-adk/adk/core/tests/test_redis_backend_v2.py -v

# 運行特定測試類
pytest ns-root/namespaces-adk/adk/core/tests/test_redis_backend_v2.py::TestRedisBackendV2 -v

# 運行帶覆蓋率報告的測試
pytest --cov=ns-root/namespaces-adk/adk/plugins/memory_plugins/redis_backend_v2 \
      --cov-report=html
```

## 部署

### Docker 部署

```yaml
# docker-compose.yml
services:
  redis:
    image: redis/redis-stack:latest
    ports:
      - "6379:6379"
      - "8001:8001"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --maxmemory 2gb
```

### Kubernetes 部署

參考 `infrastructure/redis-stack/` 目錄中的 Kubernetes 配置文件。

## 最佳實踐

1. **始終使用連接池** - 避免為每個操作創建新連接
2. **啟用斷路器** - 防止級聯故障
3. **監控指標** - 追蹤性能和健康狀態
4. **使用批量操作** - 提高吞吐量
5. **設置合理的 TTL** - 防止內存泄漏
6. **實現重試邏輯** - 處理臨時故障
7. **定期備份** - 保護數據安全
8. **使用管道** - 減少網絡往返

## 參考資料

- [Redis 官方文檔](https://redis.io/docs/)
- [Redis Stack 文檔](https://redis.io/docs/stack/)
- [Redis Python 客戶端](https://redis.readthedocs.io/)
- [斷路器模式](https://martinfowler.com/bliki/CircuitBreaker.html)

## 貢獻

歡迎貢獻！請提交 Pull Request 或創建 Issue。

## 許可證

本項目採用 MIT 許可證。