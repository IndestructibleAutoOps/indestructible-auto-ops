# Ecosystem 部署和使用指南

**版本**: 1.0.0  
**最後更新**: 2026-02-01  
**GL Governance Layer**: GL10-29 (Operational Layer)

---

## 📋 目錄

1. [快速開始](#快速開始)
2. [系統要求](#系統要求)
3. [安裝部署](#安裝部署)
4. [組件配置](#組件配置)
5. [使用手冊](#使用手冊)
6. [API 文檔](#api-文檔)
7. [最佳實踐](#最佳實踐)
8. [故障排除](#故障排除)

---

## 🚀 快速開始

### 5分鐘快速部署

```bash
# 1. 克隆倉庫
git clone <repository-url>
cd ecosystem

# 2. 選擇平台模板
cp -r platform-templates/core-template my-platform
cd my-platform

# 3. 配置平台
vim configs/platform-config.yaml

# 4. 設置和部署
bash scripts/setup.sh
bash scripts/deploy.sh

# 5. 驗證部署
bash scripts/validate.sh
bash scripts/status.sh
```

### 驗證安裝

```python
# test_installation.py
from platform_manager import PlatformManager

pm = PlatformManager('configs/platform-config.yaml')
status = pm.get_platform_status()
print(f"Platform: {status['platform']}")
print(f"Components: {list(status['components'].keys())}")
```

---

## 💻 系統要求

### 最小要求

- **操作系統**: Ubuntu 20.04+ / RHEL 8+ / CentOS 8+
- **CPU**: 4 cores
- **內存**: 8 GB RAM
- **存儲**: 100 GB 可用空間
- **Python**: 3.8+
- **網絡**: 內網連接

### 推薦配置

- **操作系統**: Ubuntu 22.04 LTS
- **CPU**: 8 cores
- **內存**: 16 GB RAM
- **存儲**: 500 GB SSD
- **Python**: 3.10+
- **網絡**: 千兆以太網

### 依賴軟件

```bash
# Python 包
pip install PyYAML>=6.0
pip install PyJWT>=2.0  # API Gateway
pip install requests>=2.28  # 可選，用於 HTTP 健康檢查

# 系統工具
sudo apt-get install -y python3 python3-pip
sudo apt-get install -y net-tools lsof
```

---

## 📦 安裝部署

### 方式1: 使用模板部署

#### Core Template（基礎平台）

```bash
# 複製模板
cp -r ecosystem/platform-templates/core-template ./my-core-platform
cd my-core-platform

# 配置
vim configs/platform-config.yaml

# 部署
bash scripts/setup.sh
bash scripts/deploy.sh
```

#### Cloud Template（雲平台）

```bash
# AWS
cp -r ecosystem/platform-templates/cloud-template ./my-aws-platform
cd my-aws-platform

# 配置 AWS 憑證
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
export AWS_REGION=us-east-1

# 使用 AWS 配置
cp configs/platform-config.aws.yaml configs/platform-config.yaml

# 部署（需要自定義 AWS 部署腳本）
# bash scripts/deploy-aws.sh
```

#### On-Premise Template（本地部署）

```bash
# 複製模板
cp -r ecosystem/platform-templates/on-premise-template ./my-datacenter

# 檢查前置條件
bash scripts/prerequisites.sh

# 配置
vim configs/platform-config.yaml

# 部署
bash scripts/setup.sh
bash scripts/deploy.sh
```

### 方式2: 手動部署

#### 1. 設置 Service Discovery

```python
from ecosystem.coordination.service_discovery import ServiceRegistry, ServiceAgent

config = {
    'registry': {
        'type': 'inmemory',
        'persistence': True,
        'storage_path': '/data/service-registry'
    }
}

registry = ServiceRegistry(config)
agent = ServiceAgent(registry, config)

# 註冊服務
service_id = agent.register_service(
    name='my-service',
    platform='my-platform',
    endpoint='http://localhost:8080',
    auto_health_check=True
)
```

#### 2. 設置 API Gateway

```python
from ecosystem.coordination.api_gateway import Gateway, Route

config = {
    'authentication': {
        'jwt': {
            'enabled': True,
            'secret': 'your-secret-key'
        }
    },
    'rate_limiting': {
        'enabled': True,
        'default_limit': 1000
    }
}

gateway = Gateway(config)

# 添加路由
route = Route(
    path='/api/v1/services/*',
    platform='my-platform',
    service='my-service',
    methods=['GET', 'POST']
)

gateway.add_route(route)
```

#### 3. 設置 Communication

```python
from ecosystem.coordination.communication import MessageBus, EventDispatcher

bus = MessageBus()
bus.start()

dispatcher = EventDispatcher(bus)

# 訂閱事件
def event_handler(message):
    print(f"Event: {message.event_type}, Payload: {message.payload}")

dispatcher.register_handler('user.created', event_handler)
dispatcher.subscribe_to_events('user.events', ['user.created'])

# 發布事件
dispatcher.dispatch_event(
    topic='user.events',
    event_type='user.created',
    payload={'user_id': 123}
)
```

#### 4. 設置 Data Synchronization

```python
from ecosystem.coordination.data_synchronization import SyncEngine, SyncMode

engine = SyncEngine()

# 添加數據
engine.add_data('platform-a', 'config-1', {'key': 'value'})

# 創建同步任務
job_id = engine.create_sync_job(
    dataset='my-data',
    source='platform-a',
    destinations=['platform-b'],
    mode=SyncMode.MANUAL
)

# 執行同步
engine.execute_sync_job(job_id)

# 檢查狀態
status = engine.get_job_status(job_id)
print(f"Synced: {status['items_synced']}/{status['items_total']}")
```

---

## ⚙️ 組件配置

### Service Discovery 配置

```yaml
# configs/service-discovery-config.yaml
service_discovery:
  enabled: true
  registry_type: inmemory  # inmemory, consul, etcd
  
  health_check:
    enabled: true
    default_interval: 30
    default_timeout: 5
  
  load_balancing:
    default_strategy: health-based
```

### API Gateway 配置

```yaml
# configs/gateway-config.yaml
api_gateway:
  enabled: true
  port: 8000
  
  authentication:
    jwt:
      enabled: true
      secret: "${JWT_SECRET}"
      expiration: 3600
  
  rate_limiting:
    enabled: true
    default_limit: 1000
    per_route:
      "/api/v1/public/*": 2000
      "/api/v1/admin/*": 100
```

### Communication 配置

```yaml
# configs/communication-config.yaml
communication:
  message_bus:
    enabled: true
    type: inmemory  # inmemory, rabbitmq, kafka
    max_queue_size: 10000
  
  event_dispatcher:
    enabled: true
    worker_threads: 4
```

### Data Sync 配置

```yaml
# configs/sync-config.yaml
data_sync:
  enabled: true
  mode: scheduled  # real-time, scheduled, manual
  
  conflict_resolution:
    default_strategy: last-write-wins  # merge, custom
  
  scheduler:
    default_interval: 3600
    schedules:
      - name: config-sync
        source: platform-main
        destinations: [platform-backup]
        interval: 1800
```

---

## 📖 使用手冊

### 服務發現

#### 註冊服務

```python
from platform_manager import PlatformManager

pm = PlatformManager('configs/platform-config.yaml')

# 註冊服務
service_id = pm.register_service(
    name='my-api',
    endpoint='http://localhost:8080',
    service_type='api',
    version='1.0.0',
    tags=['production', 'api'],
    health_check={
        'type': 'http',
        'path': '/health',
        'interval': 30
    }
)

print(f"Service registered: {service_id}")
```

#### 發現服務

```python
# 發現所有服務
services = pm.discover_services()

# 按類型過濾
api_services = pm.discover_services(service_type='api')

# 按平台過濾
platform_services = pm.discover_services(platform='my-platform')

# 只獲取健康的服務
healthy_services = pm.discover_services(only_healthy=True)
```

### API Gateway

#### 配置路由

```python
# 添加路由
pm.add_route(
    path='/api/v1/users/*',
    service='user-service',
    methods=['GET', 'POST', 'PUT', 'DELETE'],
    authentication='required',
    timeout=30
)

# 公開路由（無需認證）
pm.add_route(
    path='/api/v1/public/*',
    service='public-api',
    methods=['GET'],
    authentication='none'
)
```

#### 生成認證令牌

```python
from ecosystem.coordination.api_gateway import Gateway

gateway = Gateway(config)

# 生成 JWT
token = gateway.authenticator.generate_jwt(
    user_id='user123',
    username='john',
    roles=['user', 'admin']
)

print(f"Token: {token}")
```

### 消息通信

#### 發布事件

```python
# 發布事件
pm.publish_event(
    topic='platform.events',
    event_type='service.started',
    payload={
        'service': 'my-service',
        'timestamp': time.time()
    }
)
```

#### 訂閱事件

```python
# 訂閱事件
def handle_service_event(message):
    print(f"Service event: {message.payload}")

pm.subscribe_events('platform.events', handle_service_event)
```

### 數據同步

#### 手動同步

```python
# 添加數據
pm.sync_engine.add_data('source', 'item-1', {'data': 'value'})

# 同步數據
job_id = pm.sync_data(
    source='source',
    destinations=['dest-1', 'dest-2'],
    dataset='my-dataset'
)

# 檢查狀態
status = pm.sync_engine.get_job_status(job_id)
print(f"Status: {status['status']}")
print(f"Synced: {status['items_synced']}/{status['items_total']}")
```

#### 自動調度同步

```python
from ecosystem.coordination.data_synchronization import SyncScheduler

def sync_callback(dataset, source, destinations):
    # 執行同步
    job_id = pm.sync_data(source, destinations, dataset)
    return job_id

scheduler = SyncScheduler(sync_callback, config)

# 添加調度
scheduler.add_schedule(
    name='hourly-backup',
    source='platform-main',
    destinations=['platform-backup'],
    interval=3600,  # 1 hour
    enabled=True
)

# 啟動調度器
scheduler.start()
```

---

## 📚 API 文檔

### Service Discovery API

#### 註冊服務
```python
agent.register_service(
    name: str,              # 服務名稱
    platform: str,          # 平台名稱
    endpoint: str,          # 服務端點
    service_type: str,      # 服務類型（可選）
    version: str,           # 版本（默認 "1.0.0"）
    tags: List[str],        # 標籤（可選）
    health_check: HealthCheck,  # 健康檢查（可選）
    auto_health_check: bool     # 自動健康檢查（默認 True）
) -> str  # 返回服務ID
```

#### 發現服務
```python
client.discover_services(
    name: str,              # 服務名稱（可選）
    platform: str,          # 平台名稱（可選）
    service_type: str,      # 服務類型（可選）
    tags: List[str],        # 標籤（可選）
    only_healthy: bool      # 只返回健康服務（默認 True）
) -> List[ServiceInstance]
```

### API Gateway API

#### 添加路由
```python
gateway.add_route(Route(
    path: str,              # 路由路徑
    platform: str,          # 平台名稱
    service: str,           # 服務名稱
    methods: List[str],     # HTTP 方法
    timeout: int,           # 超時時間（秒）
    authentication: str     # 認證要求: required/optional/none
)) -> bool
```

#### 處理請求
```python
gateway.handle_request(
    method: str,            # HTTP 方法
    path: str,              # 請求路徑
    headers: Dict,          # 請求頭（可選）
    body: Dict,             # 請求體（可選）
    client_ip: str          # 客戶端IP（可選）
) -> Tuple[int, Dict, Dict]  # (status, headers, body)
```

### Communication API

#### 發布消息
```python
message_bus.publish(
    topic: str,             # 主題
    event_type: str,        # 事件類型
    payload: Dict,          # 消息負載
    source: str             # 消息來源（可選）
) -> str  # 返回消息ID
```

#### 訂閱消息
```python
message_bus.subscribe(
    topic: str,             # 主題
    handler: Callable,      # 消息處理函數
    filter_func: Callable   # 過濾函數（可選）
) -> str  # 返回訂閱ID
```

### Data Sync API

#### 創建同步任務
```python
sync_engine.create_sync_job(
    dataset: str,           # 數據集名稱
    source: str,            # 源位置
    destinations: List[str], # 目標位置列表
    mode: SyncMode          # 同步模式
) -> str  # 返回任務ID
```

#### 執行同步
```python
sync_engine.execute_sync_job(
    job_id: str             # 任務ID
) -> bool  # 成功返回 True
```

---

## 🎯 最佳實踐

### 1. 服務命名

```python
# 推薦格式
name = f"{platform}-{service-type}-{instance}"

# 示例
"aws-compute-service-01"
"gcp-storage-service-west"
"onprem-api-gateway-main"
```

### 2. 健康檢查

```python
# 始終配置健康檢查
health_check = {
    'type': 'http',
    'path': '/health',
    'interval': 30,
    'timeout': 5
}

# 為關鍵服務使用更頻繁的檢查
critical_health_check = {
    'type': 'http',
    'path': '/health',
    'interval': 10,  # 10秒
    'timeout': 3
}
```

### 3. 負載均衡

```python
# 使用健康優先策略
client = ServiceClient(registry, {
    'load_balancing': {
        'default_strategy': 'health-based'
    }
})

# 對於特定場景使用不同策略
instance = client.get_service_instance(
    name='my-service',
    strategy='least-connections'  # 最少連接
)
```

### 4. 速率限制

```yaml
# 為不同路由設置不同限制
rate_limiting:
  enabled: true
  default_limit: 1000
  per_route:
    "/api/v1/public/*": 5000   # 公開API更高限制
    "/api/v1/admin/*": 100      # 管理API更嚴格限制
```

### 5. 數據同步策略

```python
# 實時同步：關鍵配置
engine.create_sync_job(
    dataset='critical-config',
    source='main',
    destinations=['backup', 'replica'],
    mode=SyncMode.REAL_TIME
)

# 定時同步：大數據集
engine.create_sync_job(
    dataset='analytics-data',
    source='warehouse',
    destinations=['archive'],
    mode=SyncMode.SCHEDULED
)
```

### 6. 事件驅動架構

```python
# 使用事件解耦服務
# Service A 發布事件
dispatcher.dispatch_event(
    'orders',
    'order.created',
    {'order_id': 123}
)

# Service B、C、D 各自處理
# 無需互相知道
```

---

## 🐛 故障排除

### 問題1: 服務無法註冊

**症狀**: `register_service()` 返回 None

**解決方案**:
```bash
# 檢查服務發現是否運行
lsof -i :8500

# 檢查配置
cat configs/platform-config.yaml | grep service_discovery

# 重啟服務發現
python3 -c "from platform_manager import PlatformManager; pm = PlatformManager('configs/platform-config.yaml')"
```

### 問題2: API Gateway 返回 503

**症狀**: Gateway 請求返回 Service Unavailable

**解決方案**:
```python
# 檢查服務健康狀態
services = pm.discover_services(name='my-service')
for s in services:
    print(f"{s.id}: {s.health_status}")

# 手動更新健康狀態
pm.registry.update_health_status(service_id, HealthStatus.HEALTHY)
```

### 問題3: 消息未收到

**症狀**: 訂閱者未收到消息

**解決方案**:
```python
# 檢查消息總線狀態
stats = pm.message_bus.get_stats()
print(f"Published: {stats['published']}, Delivered: {stats['delivered']}")

# 檢查訂閱
topics = pm.message_bus.list_topics()
print(f"Topics: {topics}")

# 確保消息總線已啟動
pm.message_bus.start()
```

### 問題4: 數據同步失敗

**症狀**: 同步任務狀態為 failed

**解決方案**:
```python
# 檢查任務詳情
status = pm.sync_engine.get_job_status(job_id)
print(f"Error: {status['error']}")
print(f"Failed items: {status['items_failed']}")

# 檢查源數據是否存在
items = pm.sync_engine.list_data('source-location')
print(f"Source items: {len(items)}")
```

### 問題5: 速率限制過於嚴格

**症狀**: 收到 429 Too Many Requests

**解決方案**:
```python
# 調整限制
pm.gateway.rate_limiter.set_route_limit(
    route='/api/v1/myroute/*',
    limit=5000,  # 增加限制
    burst=500
)

# 或重置客戶端限制
pm.gateway.rate_limiter.reset_client_limits('client-id')
```

---

## 📊 監控和維護

### 查看統計信息

```python
# 平台整體狀態
status = pm.get_platform_status()
print(json.dumps(status, indent=2))

# 各組件統計
print(f"Services: {pm.registry.get_statistics()}")
print(f"Gateway: {pm.gateway.get_stats()}")
print(f"Message Bus: {pm.message_bus.get_stats()}")
print(f"Data Sync: {pm.sync_engine.get_stats()}")
```

### 日誌查看

```bash
# 查看平台日誌
tail -f logs/platform.log

# 查看服務日誌
tail -f logs/services/my-service.log

# 查看錯誤日誌
tail -f logs/error/error.log
```

### 性能監控

```bash
# 使用 Prometheus（如果啟用）
curl http://localhost:9090/metrics

# 查看服務健康
curl http://localhost:8500/health

# 查看 Gateway 統計
curl http://localhost:8000/metrics
```

---

## 🔐 安全建議

### 1. 認證

```yaml
# 生產環境必須啟用認證
authentication:
  enabled: true
  jwt:
    secret: "${JWT_SECRET}"  # 使用環境變量
```

### 2. TLS

```yaml
# 啟用 TLS
security:
  tls:
    enabled: true
    cert_file: /etc/certs/server.crt
    key_file: /etc/certs/server.key
```

### 3. 網絡隔離

```bash
# 配置防火牆
sudo ufw allow from 10.0.0.0/8 to any port 8000:8500
sudo ufw deny 8000:8500
```

### 4. 定期更新

```bash
# 更新依賴
pip install --upgrade PyYAML PyJWT requests

# 更新配置
git pull
bash scripts/deploy.sh
```

---

## 📝 附錄

### A. 端口列表

| 服務 | 端口 | 用途 |
|------|------|------|
| Service Discovery | 8500 | 服務註冊和發現 |
| API Gateway | 8000 | API 統一入口 |
| Message Bus | 5672 | 消息通信 |
| Data Sync | 8080 | 數據同步 API |
| Prometheus | 9090 | 監控指標 |

### B. 環境變量

```bash
# 必需
export PLATFORM_NAME=my-platform
export JWT_SECRET=your-secret-key

# 可選
export LOG_LEVEL=INFO
export REGISTRY_TYPE=inmemory
export SYNC_MODE=scheduled
```

### C. 文件路徑

```
/data/platform/           # 平台數據
/data/logs/              # 日誌
/data/sync/              # 同步數據
/etc/platform/           # 配置
/etc/platform/certs/     # 證書
```

---

**文檔版本**: 1.0.0  
**適用於**: Ecosystem v1.0.0  
**維護者**: GL Cloud Agent  
**最後更新**: 2026-02-01
