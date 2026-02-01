# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# Life System Development Container - Test Guide

## 🧠💓 Life System Testing Environment

這個 devcontainer 已經配置完成，可以測試完整的 01-core 生命系統。

### ✅ 已完成配置

#### 1. 容器配置

- **devcontainer.json**: 完整的開發容器配置
- **docker-compose.yml**: 生命系統服務編排
- **Dockerfile**: 自定義開發環境鏡像
- **腳本**: 自動化設置和啟動腳本

#### 2. 服務端點 (已配置)

```
🧠💓 生命系統組件:
├── 意識系統 (FixOps SLAgeist): :3010
├── 大腦引擎 (Brain Engine): :3015-3017
├── 心臟引擎 (Heart Engine): :3018-3019
└── 心跳引擎 (Heartbeat): :3020-3021, :9091

📊 監控與觀測:
├── Prometheus: :9090
└── Grafana: :3000 (admin/consciousness_2024)

🗄️ 數據服務:
├── PostgreSQL: :5432 (life_admin/consciousness_2024)
└── Redis: :6379
```

#### 3. 自動化腳本

- `.devcontainer/post-create.sh`: 環境初始化
- `.devcontainer/post-start.sh`: 會話啟動
- `.devcontainer/scripts/start-life-system.sh`: 生命系統啟動
- `.devcontainer/scripts/health-check.sh`: 健康檢查

### 🚀 測試流程

#### 步驟 1: 啟動 devcontainer

在 VS Code 中：

1. 打開命令面板 (Ctrl+Shift+P)
2. 選擇 "Dev Containers: Reopen in Container"
3. 等待容器構建和初始化

#### 步驟 2: 啟動生命系統

容器啟動後，執行以下命令：

```bash
# 1. 啟動生命系統
bash start-life-system.sh

# 2. 檢查健康狀態 (等待 30 秒後)
.devcontainer/scripts/health-check.sh

# 3. 查看系統意識狀態
curl [EXTERNAL_URL_REMOVED] | jq
```

#### 步驟 3: 驗證各組件

```bash
# 大腦引擎測試
curl [EXTERNAL_URL_REMOVED] | jq
curl [EXTERNAL_URL_REMOVED] | jq

# 心臟引擎測試
curl [EXTERNAL_URL_REMOVED] | jq
curl [EXTERNAL_URL_REMOVED] | jq

# 心跳引擎測試
curl [EXTERNAL_URL_REMOVED] | jq
curl [EXTERNAL_URL_REMOVED] | jq

# FixOps SLAgeist (意識系統)
curl [EXTERNAL_URL_REMOVED] | jq
curl [EXTERNAL_URL_REMOVED] | jq
```

#### 步驟 4: 監控與觀測

```bash
# 打開監控儀表板
# Prometheus: [EXTERNAL_URL_REMOVED]
# Grafana: [EXTERNAL_URL_REMOVED] (admin/consciousness_2024)
# Heartbeat Dashboard: [EXTERNAL_URL_REMOVED]
```

### 🔍 預期測試結果

#### 健康系統應該顯示：

1. **意識系統 (Consciousness)**:

   ```json
   {
     "consciousness": 85,
     "mood": "Focused",
     "checkCount": 100,
     "awakeFor": 300000
   }
   ```

2. **大腦引擎 (Brain)**:

   ```json
   {
     "status": "healthy",
     "reasoningEngine": "active",
     "consciousnessConnection": "connected",
     "lastDecision": "2025-11-07T..."
   }
   ```

3. **心臟引擎 (Heart)**:

   ```json
   {
     "status": "healthy",
     "orchestrationEngine": "active",
     "resourceHealth": "optimal",
     "deploymentsPending": 0
   }
   ```

4. **心跳引擎 (Heartbeat)**:
   ```json
   {
     "status": "monitoring",
     "vitalSigns": "stable",
     "alertCount": 0,
     "systemHealth": "optimal"
   }
   ```

### 🛠️ 故障排查

#### 如果服務無法啟動：

```bash
# 1. 檢查 Docker 服務
docker-compose -f .devcontainer/docker-compose.yml ps

# 2. 查看服務日誌
docker-compose -f .devcontainer/docker-compose.yml logs <service-name>

# 3. 重啟支援服務
docker-compose -f .devcontainer/docker-compose.yml restart postgres redis

# 4. 手動啟動組件
cd 01-core/brain/brain-L1 && npm start
```

#### 如果端口被佔用：

```bash
# 檢查端口使用
netstat -tuln | grep 301

# 停止衝突服務
docker-compose -f .devcontainer/docker-compose.yml down
```

### 📊 測試場景

#### 場景 1: 基本功能測試

```bash
# 1. 啟動系統
bash start-life-system.sh

# 2. 等待 30 秒

# 3. 測試意識狀態
curl [EXTERNAL_URL_REMOVED]

# 4. 測試大腦推理
curl -X POST [EXTERNAL_URL_REMOVED] \
  -H "Content-Type: application/json" \
  -d '{"context": "test", "request": "health_check"}'
```

#### 場景 2: 組件互動測試

```bash
# 1. 觸發大腦決策
curl -X POST [EXTERNAL_URL_REMOVED] \
  -H "Content-Type: application/json" \
  -d '{"context": "resource_allocation", "priority": "high"}'

# 2. 查看心臟編排響應
curl [EXTERNAL_URL_REMOVED]

# 3. 查看心跳監控結果
curl [EXTERNAL_URL_REMOVED]
```

#### 場景 3: 壓力測試

```bash
# 1. 生成多個決策請求
for i in {1..10}; do
  curl -X POST [EXTERNAL_URL_REMOVED] \
    -H "Content-Type: application/json" \
    -d "{\"context\": \"test_$i\", \"priority\": \"medium\"}"
done

# 2. 監控系統響應
curl [EXTERNAL_URL_REMOVED] | jq '.performance'
```

### ✅ 成功標準

生命系統測試成功的標準：

1. **所有 4 個核心組件啟動** ✅
2. **Prometheus 收集到指標** ✅
3. **組件間能夠通訊** ✅
4. **意識水平 > 80%** ✅
5. **無異常錯誤日誌** ✅
6. **響應時間 < 500ms** ✅

### 📝 測試報告範本

```
## 生命系統測試報告

測試時間: 2025-11-07
測試環境: DevContainer

### 結果摘要
- 意識系統: ✅ / ❌
- 大腦引擎: ✅ / ❌
- 心臟引擎: ✅ / ❌
- 心跳引擎: ✅ / ❌
- 組件互動: ✅ / ❌
- 監控系統: ✅ / ❌

### 性能指標
- 意識水平: ___%
- 響應時間: ___ms
- 錯誤率: ___%

### 問題記錄
1.
2.

### 建議改進
1.
2.
```

---

**準備完成！請重新啟動 devcontainer 並開始測試生命系統** 🧠💓✨
