# Ecosystem 快速參考指南

**版本**: 1.0.0  
**快速查閱**: 常用命令和代碼片段

---

## 🚀 快速命令

### 平台管理

```bash
# 創建新平台
cp -r ecosystem/platform-templates/core-template my-platform
cd my-platform

# 設置平台
bash scripts/setup.sh

# 部署平台
bash scripts/deploy.sh

# 檢查狀態
bash scripts/status.sh

# 清理
bash scripts/cleanup.sh
```

### Registry 管理

```bash
# 平台註冊
python3 ecosystem/tools/registry/platform_registry_manager.py \
  register --name gl.example.my-platform --type core

# 列出平台
python3 ecosystem/tools/registry/platform_registry_manager.py list

# 服務註冊
python3 ecosystem/tools/registry/service_registry_manager.py \
  register --name my-service --platform my-platform \
  --type api --endpoint http://localhost:8080

# 生成報告
python3 ecosystem/tools/registry/platform_registry_manager.py report
```

---

## 💻 Python 代碼片段

### 完整設置

```python
from platform_manager import PlatformManager

# 初始化平台
pm = PlatformManager('configs/platform-config.yaml')

# 註冊服務
service_id = pm.register_service(
    name='my-service',
    endpoint='http://localhost:8080',
    health_check={'type': 'http', 'path': '/health'}
)

# 配置路由
pm.add_route(
    path='/api/v1/service/*',
    service='my-service',
    methods=['GET', 'POST']
)

# 訂閱事件
pm.subscribe_events('events', lambda msg: print(msg.payload))

# 發布事件
pm.publish_event('events', 'service.ready', {'service': 'my-service'})

# 同步數據
pm.sync_data('source', ['dest'], 'my-data')

# 查看狀態
print(pm.get_platform_status())
```

### Service Discovery

```python
from ecosystem.coordination.service_discovery import (
    ServiceRegistry, ServiceAgent, ServiceClient
)

# 創建
registry = ServiceRegistry()
agent = ServiceAgent(registry)
client = ServiceClient(registry)

# 註冊
sid = agent.register_service('svc', 'platform', 'http://localhost:8080')

# 發現
services = client.discover_services(name='svc')

# 調用
response = client.call_service('svc', 'GET', '/api/data')
```

### API Gateway

```python
from ecosystem.coordination.api_gateway import Gateway, Route

# 創建
gateway = Gateway(config)

# 路由
gateway.add_route(Route(
    path='/api/*', platform='p', service='s', methods=['GET']
))

# 處理
status, headers, body = gateway.handle_request('GET', '/api/test')

# 認證
token = gateway.authenticator.generate_jwt('uid', 'user', ['role'])
```

### Communication

```python
from ecosystem.coordination.communication import MessageBus, EventDispatcher

# 創建
bus = MessageBus()
bus.start()
dispatcher = EventDispatcher(bus)

# 發布
bus.publish('topic', 'event.type', {'data': 'value'})

# 訂閱
bus.subscribe('topic', lambda msg: print(msg.payload))

# 事件分發
dispatcher.register_handler('event.type', handler_func)
dispatcher.dispatch_event('topic', 'event.type', {})
```

### Data Sync

```python
from ecosystem.coordination.data_synchronization import SyncEngine, SyncMode

# 創建
engine = SyncEngine()

# 添加數據
engine.add_data('location', 'item-id', {'data': 'value'})

# 同步
job_id = engine.create_sync_job('dataset', 'src', ['dest'], SyncMode.MANUAL)
engine.execute_sync_job(job_id)

# 狀態
status = engine.get_job_status(job_id)
```

---

## 📋 配置模板

### 最小配置

```yaml
platform:
  name: gl.example.minimal-platform
  type: core
  
service_discovery:
  enabled: true
  
api_gateway:
  enabled: true
  port: 8000
```

### 完整配置

```yaml
platform:
  name: gl.example.full-platform
  type: core
  environment: production
  governance:
    enabled: true
    layers: [gl-enterprise-architecture]
  capabilities: [service-discovery, api-gateway, messaging, data-sync]

service_discovery:
  enabled: true
  registry_type: inmemory
  health_check: {enabled: true, interval: 30}

api_gateway:
  enabled: true
  port: 8000
  authentication: {jwt: {enabled: true, secret: "${JWT_SECRET}"}}
  rate_limiting: {enabled: true, default_limit: 1000}

communication:
  enabled: true
  message_bus: {type: inmemory}

data_sync:
  enabled: true
  mode: scheduled
  scheduler: {default_interval: 3600}

monitoring:
  enabled: true
  metrics: {port: 9090}
  logging: {level: INFO}
```

---

## 🔍 常用查詢

### 查找服務

```python
# 按名稱
services = client.discover_services(name='user-service')

# 按平台
services = client.discover_services(platform='aws-platform')

# 按類型
services = client.discover_services(service_type='api')

# 組合條件
services = client.discover_services(
    platform='aws', 
    service_type='compute',
    only_healthy=True
)
```

### 獲取統計

```python
# Service Discovery
registry.get_statistics()
# {'total_services': 10, 'healthy_services': 8, ...}

# API Gateway
gateway.get_stats()
# {'routes': 5, 'rate_limiter': {...}}

# Message Bus
bus.get_stats()
# {'published': 100, 'delivered': 95, ...}

# Data Sync
engine.get_stats()
# {'total_jobs': 5, 'sync_count': 4, ...}
```

---

## ⚡ 性能優化

### 負載均衡

```python
# 使用加權策略提高性能
config = {
    'load_balancing': {
        'default_strategy': 'weighted'
    }
}
```

### 批量同步

```python
# 增加批量大小
config = {
    'sync_engine': {
        'batch_size': 5000  # 默認 1000
    }
}
```

### 消息隊列

```python
# 增加隊列容量
config = {
    'message_bus': {
        'max_queue_size': 50000  # 默認 10000
    }
}
```

---

## 🎓 學習資源

### 示例程序

1. `platform-templates/core-template/examples/register_service.py`
2. `platform-templates/core-template/examples/api_gateway_example.py`
3. `platform-templates/core-template/examples/messaging_example.py`
4. `platform-templates/core-template/examples/sync_data.py`

### 測試套件

1. `coordination/service-discovery/tests/test_service_discovery.py`
2. `coordination/api-gateway/tests/test_api_gateway.py`
3. `coordination/communication/tests/test_communication.py`
4. `coordination/data-synchronization/tests/test_data_sync.py`
5. `tests/test_ecosystem_integration.py`

### 文檔

1. `DEPLOYMENT_GUIDE.md` - 部署指南
2. `ECOSYSTEM_STATUS_ANALYSIS.md` - 架構分析
3. `PHASE1_COMPLETION_REPORT.md` - Phase 1 報告
4. `PHASE1_AND_2_COMPLETION.md` - Phase 1 & 2 報告

---

**快速參考**: 常用操作和代碼片段  
**版本**: 1.0.0  
**最後更新**: 2026-02-01
