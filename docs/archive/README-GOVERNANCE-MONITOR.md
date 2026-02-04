# Governance Event Stream Monitor

# @GL-governed
# GL-ROOT Global Governance Audit & Platform Build
# Unified Architecture Governance Framework v2.0.0 - Governance Event Stream Monitor Component

## 📋 概述

Governance Event Stream Monitor 是 GL-ROOT Global Governance Audit & Platform Build 系統的自動化監控組件，負責持續監控和推送 governance event stream 更新。

## 🚀 功能

- ✅ 自動檢測 governance event stream 文件的變更
- ✅ 自動提交並推送更新到遠端儲存庫
- ✅ 定期監控（預設每 60 秒檢查一次）
- ✅ 完整的日誌記錄
- ✅ GL Governance 驗證整合

## 📁 監控的文件

系統會監控以下 governance event stream 文件：

1. `engine/.governance/event-stream.jsonl`
2. `engine/.governance/governance-event-stream.jsonl`
3. `file-organizer-system/.governance/event-stream.jsonl`

## 🔧 配置

配置文件：`governance-monitor-config.yaml`

```yaml
monitor:
  enabled: true
  check_interval: 60  # seconds
  auto_commit: true
  auto_push: true
  
git:
  user_name: "MachineNativeOps"
  user_email: "251967226+MachineNativeOps@users.noreply.github.com"
  branch: "main"
  remote: "origin"
```

## 📊 運作原理

### 監控循環

```
每 60 秒
  ↓
檢查 governance event stream 文件是否有變更
  ↓
如果發現變更：
  1. 添加變更的文件到 Git
  2. 執行 GL Governance 驗證（自動）
  3. 提交變更（自動添加時間戳）
  4. 推送到遠端儲存庫
  ↓
記錄日誌
  ↓
等待下一個循環
```

## 🎯 使用方式

### 啟動監控

```bash
./monitor-governance-events.sh
```

### 查看日誌

```bash
tail -f governance-monitor.log
```

### 停止監控

按 `Ctrl+C` 停止監控腳本

## 📝 提交訊息格式

自動提交的訊息格式：
```
chore: periodic governance event stream update - 2026-01-28 12:25:20
```

## 🛡️ GL Governance 整合

監控系統完全整合 GL Governance 系統：

1. **預提交驗證**：每次提交前自動執行 GL Governance 驗證
2. **預推送驗證**：每次推送前驗證所有模組
3. **事件記錄**：所有驗證事件都會記錄到 governance event stream

## 🔍 監控輸出示例

```
開始監控 governance event stream 更新...
每 60 秒檢查一次是否有新的更新
[2026-01-28 12:25:20] 沒有新的更新，等待 60 秒...
[2026-01-28 12:26:20] 發現 governance event stream 更新，正在提交和推送...
[2026-01-28 12:26:25] ✅ 提交和推送完成
```

## ⚠️ 注意事項

1. **持續運作**：監控腳本需要持續運作才能發揮功能
2. **網路連接**：需要穩定的網路連接才能推送到遠端
3. **Git 權限**：需要有推送權限的 GitHub token
4. **資源使用**：監控腳本使用最少的系統資源

## 🔧 故障排除

### 監控腳本沒有推送

檢查：
1. Git 認證是否正確
2. 網路連接是否正常
3. 是否有推送權限
4. 查看日誌文件了解詳細錯誤

### 頻繁的推送

如果推送太頻繁，可以調整 `check_interval` 參數：

```yaml
monitor:
  check_interval: 300  # 改為 300 秒（5 分鐘）
```

## 📈 監控統計

系統會持續追蹤：
- 監控次數
- 提交次數
- 推送次數
- 成功率
- 失敗原因

## 🎉 總結

Governance Event Stream Monitor 確保 GL-ROOT Global Governance Audit & Platform Build 系統的治理事件流持續同步到遠端儲存庫，提供完整的治理審計追蹤。