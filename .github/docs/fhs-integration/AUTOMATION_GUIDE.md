# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# GL Unified Charter Activated
# FHS Integration System - Automated Operation Guide
# FHS 整合系統 - 自動化運作指南

## 完全自動化啟動

系統現在支持三種自動化啟動方式，無需人工介入：

### 方式 1: GitHub Actions 自動化 (推薦)

系統會在以下情況自動運行：

1. **代碼推送** - 當 FHS 整合相關代碼更新時
2. **Pull Request** - PR 創建時自動驗證
3. **定時任務** - 每天 09:00 UTC 自動評估
4. **手動觸發** - 隨時可在 GitHub Actions 頁面手動運行

**配置文件**：`.github/workflows/fhs-integration-auto-init.yml`

**自動執行內容**：
- ✅ 環境檢查和依賴安裝
- ✅ 系統初始化
- ✅ 健康檢查
- ✅ 功能測試
- ✅ 組件評估
- ✅ 自動生成報告
- ✅ 檢測準備好的組件
- ✅ 創建整合計劃

**查看結果**：
1. 訪問 GitHub 倉庫
2. 點擊 "Actions" 標籤
3. 查看 "FHS Integration System Auto-Initialization" 工作流
4. 下載生成的報告（Artifacts）

### 方式 2: 自動啟動腳本

一鍵自動啟動，無需任何交互：

```bash
# 運行自動啟動腳本
bash scripts/fhs-integration/auto_startup.sh
```

**腳本會自動**：
1. 檢測並配置環境
2. 安裝必要依賴（如果缺失）
3. 初始化系統
4. 運行所有測試
5. 生成評估報告
6. 檢測準備好整合的組件

**日誌位置**：
- 主日誌：`/tmp/fhs-integration-auto-startup.log`
- 評估報告：`/tmp/fhs-assessment-YYYYMMDD-HHMMSS.txt`

**預期輸出**：
```
========================================
FHS Integration Auto-Startup
========================================

[1/5] Auto-detecting environment...
✓ Python 3 detected: 3.12.3

[2/5] Auto-installing dependencies...
✓ PyYAML already installed

[3/5] Auto-initializing system...
✓ System initialized successfully

[4/5] Running automated tests...
✓ Health check passed
✓ Operational tests passed

[5/5] Generating automated assessment...
✓ Assessment completed

========================================
✓ Auto-Startup Complete
========================================

The FHS Integration System is now running automatically!
```

### 方式 3: Systemd 服務 (Linux 系統)

設置為系統服務，開機自動啟動：

**安裝步驟**：

```bash
# 1. 複製服務文件到 systemd 目錄
sudo cp etc/systemd/fhs-integration-auto-init.service /etc/systemd/system/

# 2. 重新加載 systemd
sudo systemctl daemon-reload

# 3. 啟用服務（開機自動啟動）
sudo systemctl enable fhs-integration-auto-init.service

# 4. 立即啟動服務
sudo systemctl start fhs-integration-auto-init.service

# 5. 檢查狀態
sudo systemctl status fhs-integration-auto-init.service
```

**查看日誌**：
```bash
# 查看服務日誌
sudo journalctl -u fhs-integration-auto-init.service

# 實時查看日誌
sudo journalctl -u fhs-integration-auto-init.service -f

# 查看最近的日誌
sudo journalctl -u fhs-integration-auto-init.service -n 50
```

**服務管理**：
```bash
# 停止服務
sudo systemctl stop fhs-integration-auto-init.service

# 重啟服務
sudo systemctl restart fhs-integration-auto-init.service

# 禁用自動啟動
sudo systemctl disable fhs-integration-auto-init.service
```

## 完全自動化工作流程

### 日常自動運行

系統會自動執行以下任務：

**每天自動**：
- 09:00 UTC - GitHub Actions 自動評估所有組件
- 生成評估報告並保存為 Artifacts
- 檢測達到整合標準的組件

**每次代碼更新**：
- 自動驗證系統健康
- 運行功能測試
- 確保沒有破壞現有功能

**組件準備好時**：
- 自動檢測到成熟度 ≥ 80 分的組件
- 自動生成整合計劃（乾運行）
- 創建報告供人工審查

### 自動整合流程（需確認）

當組件準備好整合時，系統會：

1. **自動檢測** - 識別成熟度 ≥ 80 分的組件
2. **自動驗證** - 運行六層驗證機制
3. **生成計劃** - 創建詳細的整合計劃
4. **等待確認** - 需要人工審查並確認執行

**手動確認整合**：
```bash
# 查看整合計劃
cat /tmp/integration-plan.txt

# 或從 GitHub Actions Artifacts 下載

# 確認後執行整合
python3 workspace/tools/fhs-integration/fhs_automation_leader.py --auto-integrate --execute
```

## 自動化監控

### GitHub Actions 監控

**自動通知**：
- ✅ 成功：工作流通過時顯示綠色勾號
- ❌ 失敗：工作流失敗時發送通知

**報告下載**：
1. 進入 GitHub Actions
2. 選擇工作流運行
3. 下載 Artifacts：
   - `fhs-assessment-report` - 評估報告
   - `fhs-integration-plan` - 整合計劃（如有）

### 本地監控

**檢查系統狀態**：
```bash
# 快速健康檢查
bash scripts/fhs-integration/health_check.sh

# 查看最近的評估
ls -lt /tmp/fhs-assessment-*.txt | head -1
cat $(ls -t /tmp/fhs-assessment-*.txt | head -1)
```

**查看日誌**：
```bash
# 查看自動啟動日誌
tail -f /tmp/fhs-integration-auto-startup.log

# 查看 systemd 日誌（如使用服務）
sudo journalctl -u fhs-integration-auto-init.service -f
```

## 自動化配置

### 調整自動評估時間

編輯 `.github/workflows/fhs-integration-auto-init.yml`：

```yaml
schedule:
  # 修改 cron 表達式調整時間
  # 例如：每天 14:00 UTC
  - cron: '0 14 * * *'
  
  # 或每週一 09:00 UTC
  - cron: '0 9 * * 1'
```

### 調整整合閾值

編輯 `workspace/tools/fhs-integration/maturity-criteria.yaml`：

```yaml
# 修改生產就緒閾值
production:
  score: 81-100  # 調整為 85-100 以更嚴格
```

### 自定義自動化行為

編輯 `scripts/fhs-integration/auto_startup.sh`：

```bash
# 添加自定義步驟
# 例如：自動發送郵件通知

# 在階段 5 後添加：
if [ -f "$ASSESSMENT_OUTPUT" ]; then
    # 發送郵件（需配置郵件服務）
    mail -s "FHS Assessment Report" admin@example.com < "$ASSESSMENT_OUTPUT"
fi
```

## 故障自動恢復

### GitHub Actions 自動重試

工作流失敗時會自動：
- 記錄錯誤信息
- 創建錯誤報告
- 在下次觸發時重試

### Systemd 自動重啟

服務失敗時會自動：
- 等待 10 秒
- 自動重啟服務
- 記錄到系統日誌

### 手動觸發恢復

```bash
# 重新運行自動啟動
bash scripts/fhs-integration/auto_startup.sh

# 或通過 systemd
sudo systemctl restart fhs-integration-auto-init.service

# 或在 GitHub Actions 手動觸發
```

## 最佳實踐

### 完全自動化設置

1. ✅ 啟用 GitHub Actions 自動化
2. ✅ 在服務器上安裝 systemd 服務
3. ✅ 設置通知（郵件、Slack 等）
4. ✅ 定期檢查 Artifacts 和日誌
5. ✅ 組件達標時及時審查整合計劃

### 安全的自動化

- ✅ 自動評估和驗證
- ✅ 自動生成整合計劃
- ⚠️ 需要人工確認才執行實際整合
- ✅ 保留所有日誌和報告供審計

### 監控建議

- **每天**：檢查 GitHub Actions 狀態
- **每週**：審查評估報告
- **每月**：審查是否有組件準備好整合

## 總結

FHS 整合系統現在完全自動化：

✅ **自動啟動** - 無需手動初始化  
✅ **自動測試** - 持續驗證系統健康  
✅ **自動評估** - 定期評估所有組件  
✅ **自動檢測** - 識別準備好的組件  
✅ **自動報告** - 生成詳細報告  
✅ **自動恢復** - 失敗時自動重試  

**唯一需要人工介入的是**：審查並確認實際的 FHS 整合操作，以確保安全。

系統現在可以在無人值守的情況下持續運行並監控組件成熟度！
