# GL Runtime Platform 全域啟動架構文檔

## 🏗️ 整體架構設計

```
┌─────────────────────────────────────────────────────────┐
│                GL Runtime Platform 啟動系統               │
├─────────────────────────────────────────────────────────┤
│ 第1層：GitOps 與代碼治理                                 │
│ 第2層：容器與服務編排                                    │
│ 第3層：治理層啟動與驗證                                  │
│ 第4層：Multi-Agent 協作啟動                              │
│ 第5層：審計與監控啟動                                    │
└─────────────────────────────────────────────────────────┘
```

## 📁 完整文件結構

```
gl-execution-runtime/
├── tasks/
│   ├── start-runtime.yml                 # 主啟動任務定義
│   ├── governance-bootstrap.yml          # 治理層啟動任務
│   └── agent-orchestration.yml           # 代理協調任務
├── ops/
│   ├── service-health-check.sh           # 服務健康檢查
│   └── governance-verification.sh        # 治理驗證腳本
├── control-plane/
│   ├── nlp-control-api.py                # 自然語言控制平面
│   └── task-dispatcher.py                # 任務分發器
├── config/
│   ├── ports-config.yml                  # 端口配置
│   ├── services-config.yml               # 服務配置
│   └── governance-config.yml             # 治理配置
├── agents/
│   ├── service-agent/                    # 服務代理
│   ├── governance-agent/                 # 治理代理
│   └── verification-agent/               # 驗證代理
├── docs/
│   ├── agent-protocol.md                 # 代理智能體啟動協議
│   └── ARCHITECTURE.md                   # 架構文檔（本文件）
└── simple-server.js                      # 簡化版 GL Runtime Platform 服務器
```

## 🔧 端口配置

| 服務 | 端口 | 健康檢查 | 描述 |
|------|------|----------|------|
| GL Runtime Platform | 3000 | /health | 主應用服務 |
| REST API | 8080 | /health | REST API 服務 |
| NLP Control Plane | 5001 | /health | 自然語言控制平面 |
| Health Check 1 | 3001 | /health | 主健康檢查服務 |
| Health Check 2 | 3002 | /health | 備用健康檢查服務 |
| PostgreSQL | 5432 | pg_isready | 資料庫服務 |
| Redis | 6379 | ping | 事件流與緩存 |
| MinIO API | 9000 | /health | 物件存儲 API |
| MinIO Console | 9001 | - | 物件存儲控制台 |
| Prometheus | 9090 | /health | 監控服務 |

## 🚀 啟動流程

### 階段 1: GitOps 準備與驗證
1. 克隆儲存庫
2. 執行規範性驗證
3. 執行簽名驗證
4. 治理鉤子執行

### 階段 2: 核心服務啟動
1. 啟動主應用服務 (3000, 3001, 3002)
2. 啟動 REST API (8080)
3. 啟動自然語言控制平面 (5001)
4. 啟動存儲服務 (9000, 9001, 6379, 5432)
5. 啟動監控服務 (9090)

### 階段 3: 子系統框架啟動
1. 加載 api/rest 子系統
2. 加載 engine 子系統
3. 加載 gl-runtime 子系統
4. 加載所有其他子系統（共21個）

### 階段 4: 治理與事件系統
1. 啟動治理層運行時
2. 啟動審計事件流
3. 啟動驗證引擎
4. 啟動監控堆棧

### 階段 5: Multi-Agent 系統
1. 初始化代理協調器
2. 啟動治理代理
3. 啟動驗證代理
4. 啟動審計代理
5. 啟用跨代理通信

## 🧠 Multi-Agent 系統

### 代理類型

#### 核心治理代理
- **governance-agent**: 治理規則執行
- **verification-agent**: 驗證與合規檢查
- **audit-agent**: 審計事件收集
- **compliance-agent**: 合規性監控

#### 系統運維代理
- **orchestrator-agent**: 代理協調
- **health-agent**: 健康監控
- **deployment-agent**: 部署管理
- **monitoring-agent**: 性能監控

#### 功能領域代理
- **cognitive-agent**: 認知處理
- **analysis-agent**: 數據分析
- **reporting-agent**: 報告生成
- **storage-agent**: 存儲管理

## 📊 監控與觀察性

### 健康檢查
- 主健康檢查端點: [EXTERNAL_URL_REMOVED]
- REST API 健康檢查: [EXTERNAL_URL_REMOVED]
- 控制平面健康檢查: [EXTERNAL_URL_REMOVED]
- Prometheus 監控: [EXTERNAL_URL_REMOVED]

### 審計日誌
- 審計流: redis://localhost:6379/0
- 審計日誌: /var/log/gl-audit-*.json
- 審計保留期: 30天

### 治理報告
- 治理狀態: [EXTERNAL_URL_REMOVED]
- 系統狀態: [EXTERNAL_URL_REMOVED]
- 代理狀態: [EXTERNAL_URL_REMOVED]

## 🛡️ 治理與安全

### 治理層級
- **UNIFIED**: 統一治理層 - 全域策略與規則
- **ROOT**: 根治理層 - 系統核心規則
- **META**: 元治理層 - 執行監控與優化

### 安全措施
- TLS 1.3 通信加密
- AES-256-GCM 消息加密
- 基於令牌的身份驗證
- 基於角色的訪問控制
- 審計日誌記錄

## 🎯 自然語言控制平面

### API 端點

#### 提交任務
```bash
POST /api/control/execute
Content-Type: application/json

{
  "command": "檢查系統狀態",
  "priority": "normal",
  "governance_level": "root"
}
```

#### 獲取控制狀態
```bash
GET /api/control/status
```

#### 獲取系統狀態
```bash
GET /api/control/system/status
```

#### 獲取治理報告
```bash
GET /api/governance/report
```

### 支持的命令類型
- 啟動服務/代理/系統
- 停止服務
- 查詢狀態
- 部署應用
- 驗證合規
- 審計操作

## 📝 使用示例

### 快速啟動
```bash
# 1. 導航到項目目錄
cd /workspace/machine-native-ops/gl-execution-runtime

# 2. 執行服務健康檢查
./ops/service-health-check.sh

# 3. 執行治理驗證
./ops/governance-verification.sh

# 4. 提交自然語言任務
curl -X POST [EXTERNAL_URL_REMOVED] \
  -H "Content-Type: application/json" \
  -d '{"command": "檢查系統狀態", "priority": "normal"}'
```

### 監控系統
```bash
# 查看實時審計日誌
redis-cli MONITOR | grep gl-audit-stream

# 查看 GL Platform 健康狀態
curl [EXTERNAL_URL_REMOVED] | jq .

# 查看控制平面狀態
curl [EXTERNAL_URL_REMOVED] | jq .
```

## 🔧 配置文件

### ports-config.yml
定義所有服務的端口配置和安全規則。

### services-config.yml
定義所有服務的啟動配置、依賴關係和環境變量。

### governance-config.yml
定義治理策略、規則、審計配置和 Multi-Agent 系統配置。

## 📋 驗證清單

### 啟動前驗證
- [ ] Git 儲存庫已克隆
- [ ] 代碼規範性驗證通過
- [ ] 簽名驗證通過
- [ ] 所有依賴已安裝

### 啟動後驗證
- [ ] 所有服務端口正常
- [ ] 健康檢查通過
- [ ] 治理層已激活
- [ ] Multi-Agent 系統運行
- [ ] 審計流正常
- [ ] 監控數據收集

### 運行時驗證
- [ ] 服務健康監控
- [ ] 治理合規檢查
- [ ] 代理狀態監控
- [ ] 性能指標收集
- [ ] 審計日誌記錄

## 🚨 故障處理

### 服務故障
1. 檢查服務日誌
2. 執行健康檢查腳本
3. 重啟失敗服務
4. 檢查依賴服務

### 治理故障
1. 運行治理驗證腳本
2. 檢查治理層狀態
3. 檢查審計日誌
4. 聯系治理團隊

### 代理故障
1. 檢查代理進程
2. 檢查代理日誌
3. 重啟失敗代理
4. 檢查代理通信

## 📚 相關文檔

- [代理智能體啟動協議](./agent-protocol.md)
- [GL Platform 啟動報告](../../GL_PLATFORM_STARTUP_REPORT.md)
- [治理配置](../config/governance-config.yml)

---

**@GL-governed**  
**@GL-layer: GL90-99 Meta-Specification**  
**@GL-semantic: architecture-documentation**  
**@GL-charter-version: 1.0.0**