# Core Platform Template

核心平台模板 - 用於創建基礎平台實例

**GL Governance Layer**: GL10-29 (Operational Layer)  
**Template Type**: Core  
**Version**: 1.0.0

---

## 📋 概述

Core Template 提供了創建新平台所需的所有基礎組件和配置。這是最基本的平台模板，適用於：

- 開發和測試環境
- 小型部署
- 平台原型
- 學習和實驗

---

## 🎯 包含的組件

### 1. 服務發現
- Service Registry 集成
- 自動服務註冊
- 健康檢查配置

### 2. API 網關
- 路由配置
- 認證設置
- 速率限制

### 3. 通信系統
- Message Bus 配置
- 事件分發
- 訂閱管理

### 4. 數據同步
- 同步引擎配置
- 衝突解決策略
- 調度設置

---

## 🚀 快速開始

### 1. 創建新平台

```bash
# 複製模板
cp -r ecosystem/platform-templates/core-template my-new-platform

# 進入平台目錄
cd my-new-platform

# 配置平台
vim configs/platform-config.yaml
```

### 2. 配置平台

編輯 `configs/platform-config.yaml`:

```yaml
platform:
  name: my-platform
  version: "1.0.0"
  type: core
  environment: development
```

### 3. 設置平台

```bash
# 運行設置腳本
bash scripts/setup.sh

# 驗證設置
bash scripts/validate.sh
```

### 4. 部署平台

```bash
# 部署平台服務
bash scripts/deploy.sh

# 檢查狀態
bash scripts/status.sh
```

---

## 📁 目錄結構

```
core-template/
├── README.md                    # 本文件
├── configs/
│   ├── platform-config.yaml    # 平台主配置
│   ├── services-config.yaml    # 服務配置
│   └── registry-config.yaml    # 註冊表配置
├── scripts/
│   ├── setup.sh                # 設置腳本
│   ├── deploy.sh               # 部署腳本
│   ├── validate.sh             # 驗證腳本
│   ├── status.sh               # 狀態檢查
│   └── cleanup.sh              # 清理腳本
├── examples/
│   ├── register_service.py     # 服務註冊示例
│   ├── api_gateway_example.py  # API 網關示例
│   └── sync_data.py            # 數據同步示例
└── platform_manager.py         # 平台管理工具
```

---

## ⚙️ 配置說明

### platform-config.yaml

主要配置文件，定義平台的基本屬性：

```yaml
platform:
  name: my-platform              # 平台名稱
  version: "1.0.0"               # 版本
  type: core                     # 類型
  environment: development       # 環境
  
  governance:
    enabled: true
    layers:
      - gl-enterprise-architecture
      - gl-boundary-enforcement
```

### services-config.yaml

服務配置，定義平台運行的服務：

```yaml
services:
  service-discovery:
    enabled: true
    port: 8500
  
  api-gateway:
    enabled: true
    port: 8000
  
  message-bus:
    enabled: true
    port: 5672
```

---

## 🔧 腳本說明

### setup.sh

初始化平台環境：
- 檢查依賴
- 創建目錄結構
- 生成配置文件
- 初始化數據庫

### deploy.sh

部署平台服務：
- 啟動服務發現
- 啟動 API 網關
- 啟動消息總線
- 註冊平台

### validate.sh

驗證平台配置：
- 檢查配置文件
- 驗證服務可達性
- 測試連接
- 生成報告

### status.sh

檢查平台狀態：
- 服務運行狀態
- 健康檢查結果
- 資源使用情況
- 錯誤日誌

### cleanup.sh

清理平台：
- 停止所有服務
- 清理臨時文件
- 移除註冊信息
- 備份數據

---

## 📝 使用示例

### 註冊服務

```python
from platform_manager import PlatformManager

# 創建平台管理器
pm = PlatformManager('configs/platform-config.yaml')

# 註冊服務
service_id = pm.register_service(
    name='my-service',
    endpoint='http://localhost:8080',
    health_check={'type': 'http', 'path': '/health'}
)

print(f"Service registered: {service_id}")
```

### 配置 API 路由

```python
# 添加路由
pm.add_route(
    path='/api/v1/my-service/*',
    service='my-service',
    methods=['GET', 'POST'],
    authentication='required'
)
```

### 同步數據

```python
# 創建同步任務
job_id = pm.sync_data(
    source='platform-a',
    destinations=['platform-b', 'platform-c'],
    dataset='config-data'
)
```

---

## 🔍 最佳實踐

### 1. 命名規範

- 平台名稱：`gl.{category}.{name}-platform`
- 服務名稱：`{platform}-{service}-{instance}`
- 數據集名稱：`{platform}-{type}-{name}`

### 2. 配置管理

- 使用環境變量覆蓋配置
- 敏感信息使用 secrets
- 版本控制配置文件

### 3. 監控和日誌

- 啟用健康檢查
- 配置日誌級別
- 設置告警規則

### 4. 安全

- 啟用認證和授權
- 使用 TLS 加密
- 定期更新密鑰

---

## 🐛 故障排除

### 服務無法啟動

```bash
# 檢查日誌
tail -f logs/platform.log

# 驗證配置
bash scripts/validate.sh

# 重新部署
bash scripts/cleanup.sh
bash scripts/deploy.sh
```

### 服務發現失敗

```bash
# 檢查服務發現狀態
curl http://localhost:8500/health

# 重新註冊服務
python examples/register_service.py
```

### 數據同步問題

```bash
# 檢查同步狀態
python -c "from platform_manager import PlatformManager; \
pm = PlatformManager('configs/platform-config.yaml'); \
print(pm.get_sync_stats())"
```

---

## 📚 參考文檔

- [Ecosystem 架構文檔](../../ECOSYSTEM_STATUS_ANALYSIS.md)
- [Service Discovery 文檔](../../coordination/service-discovery/README.md)
- [API Gateway 文檔](../../coordination/api-gateway/README.md)
- [Communication 文檔](../../coordination/communication/README.md)
- [Data Sync 文檔](../../coordination/data-synchronization/README.md)

---

## 🆘 獲取幫助

- 查看文檔：`docs/`
- 運行示例：`examples/`
- 檢查日誌：`logs/`
- 提交問題：GitHub Issues

---

**GL Compliance**: Yes  
**Layer**: GL10-29 (Platform Services)  
**Status**: Active  
**Template Version**: 1.0.0
