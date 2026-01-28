# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# CI 錯誤診斷與修復報告

## 🔍 問題概述

**Repository:** https://github.com/MachineNativeOps/mno-repository-understanding-system  
**分支:** main  
**問題狀態:** CI 持續整合流程失敗

## 📋 診斷結果

### 根本原因分析

經過詳細的 CI 日誌分析，我識別出以下主要問題：

#### 1. **權限問題 - 主要錯誤**

**錯誤信息:**
```
RequestError [HttpError]: Resource not accessible by integration
status: 403
message: 'Resource not accessible by integration'
```

**影響範圍:**
- AI-Driven Integration Analyzer workflow
- PR Quality Check workflow  
- 具體失敗步驟: "Create PR comment with AI analysis"

**根本原因:**
GitHub Actions 的 GitHub Token 權限不足，無法在 Pull Request 中創建評論。

#### 2. **Workflow 觸發條件問題**

**當前配置:**
```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, labeled]
    branches: [ main, develop ]
  push:
    branches: [ main, develop ]
```

**問題:**
- Workflow 在 PR 事件和 push 事件都會觸發
- 某些步驟使用了 `if: github.event_name == 'pull_request'` 條件
- 但權限配置沒有區分不同事件類型的需求

#### 3. **JavaScript 語法錯誤（次要問題）**

**發現的問題:**
```javascript
comment += `- 變更風險: ${{ steps.ai-analysis.outputs.risk }}\n`;
```

**問題說明:**
在 JavaScript 模板字串中混用了 GitHub Actions 語法，可能導致變量替換失敗。

## 🔧 修復方案

### 方案一：解決權限問題（推薦）

#### 1.1 更新 Workflow 權限配置

在 `.github/workflows/ai-integration-analyzer.yml` 和 `.github/workflows/pr-quality-check.yml` 的頂部添加權限配置：

```yaml
permissions:
  contents: read
  issues: write
  pull-requests: write
```

#### 1.2 優化 GitHub Token 使用

在需要寫入權限的步驟中明確指定 token：

```yaml
- name: Create PR comment with AI analysis
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v7
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    script: |
      // ... existing script ...
```

### 方案二：修復 JavaScript 語法

修正 workflow 中的 JavaScript 變量引用：

**修復前:**
```javascript
comment += `- 變更風險: ${{ steps.ai-analysis.outputs.risk }}\n`;
```

**修復後:**
```javascript
const riskLevel = '${{ steps.ai-analysis.outputs.risk }}';
comment += `- 變更風險: ${riskLevel}\n`;
```

### 方案三：改進錯誤處理

添加更強健的錯誤處理邏輯：

```yaml
- name: Create PR comment with AI analysis
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v7
  continue-on-error: true
  with:
    script: |
      try {
        // ... existing code ...
        github.rest.issues.createComment({
          issue_number: context.issue.number,
          owner: context.repo.owner,
          repo: context.repo.repo,
          body: comment
        });
      } catch (error) {
        console.log('Failed to create comment:', error.message);
        // Continue workflow even if comment creation fails
      }
```

## 📊 需要檢查的具體項目清單

### 1. Repository 設置檢查

- [ ] **GitHub Token 權限設置**
  - 路徑: Settings → Actions → General → Workflow permissions
  - 檢查: 是否啟用了 "Read and write permissions"

- [ ] **Branch Protection Rules**
  - 路徑: Settings → Branches → main → Edit protection rule
  - 檢查: CI 檢查是否要求過嚴格

- [ ] **Secrets 管理**
  - 路徑: Settings → Secrets and variables → Actions
  - 檢查: 所需的 secrets 是否正確配置

### 2. Workflow 配置檢查

- [ ] **權限聲明**
  ```yaml
  permissions:
    contents: read
    issues: write
    pull-requests: write
  ```

- [ ] **觸發條件**
  - 確認 workflow 觸發條件符合需求
  - 檢查分支名稱是否正確

- [ ] **依賴版本**
  - 檢查 actions/checkout@v4 版本
  - 檢查 actions/setup-python@v5 版本
  - 檢查 actions/github-script@v7 版本

### 3. 代碼質量檢查

- [ ] **JavaScript 語法**
  - 檢查 workflow 中的 JavaScript 代碼
  - 驗證變量替換語法

- [ ] **Shell 腳本語法**
  - 檢查所有 `run:` 步驟中的 shell 命令
  - 驗證環境變量使用

- [ ] **Python 代碼**
  - 檢查 Python 腳本語法
  - 驗證依賴包版本

### 4. 測試配置檢查

- [ ] **測試框架**
  - 確認 pytest 配置正確
  - 檢查測試文件路徑

- [ ] **測試依賴**
  - 驗證 requirements.txt 或 pyproject.toml
  - 檢查測試數據文件是否存在

## 🛠️ 診斷 CI 錯誤的命令和步驟

### 本地診斷命令

```bash
# 1. 檢查 workflow 語法
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ai-integration-analyzer.yml'))"

# 2. 檢查 shell 腳本語法
bash -n .github/workflows/*.yml

# 3. 驗證 Python 代碼
python3 -m py_compile scripts/**/*.py

# 4. 檢查依賴
pip check

# 5. 運行本地測試
pytest tests/ -v

# 6. 檢查代碼格式
black --check .
ruff check .
```

### GitHub CLI 診斷命令

```bash
# 查看最近的 workflow runs
gh run list --repo MachineNativeOps/machine-native-ops --limit 10

# 查看特定 run 的詳細信息
gh run view <run-id> --repo MachineNativeOps/machine-native-ops

# 查看失敗的日誌
gh run view <run-id> --repo MachineNativeOps/machine-native-ops --log-failed

# 重新運行失敗的 workflow
gh run rerun <run-id> --repo MachineNativeOps/machine-native-ops

# 查看 workflow 配置
gh api /repos/MachineNativeOps/mno-repository-understanding-system/actions/workflows

# 檢查 repository 設置
gh api /repos/MachineNativeOps/machine-native-ops
```

## 🎯 常見 CI 錯誤修復建議

### 1. 權限相關錯誤

**錯誤:** `Resource not accessible by integration`  
**修復:** 添加適當的 `permissions` 設置到 workflow

### 2. 依賴相關錯誤

**錯誤:** `ModuleNotFoundError` 或 `ImportError`  
**修復:** 檢查 requirements.txt，確保所有依賴已正確安裝

### 3. 測試失敗

**錯誤:** 測試用例失敗  
**修復:** 
- 本地運行測試重現問題
- 檢查測試數據和環境變量
- 更新測試用例或修復代碼

### 4. 時間相關錯誤

**錯誤:** `timeout` 或 `execution time exceeded`  
**修復:**
- 優化腳本性能
- 增加 timeout 設置
- 分割長時間運行的任務

### 5. 路徑相關錯誤

**錯誤:** `FileNotFoundError` 或路徑不正確  
**修復:**
- 使用絕對路徑或相對於項目根目錄的路徑
- 檢查文件是否存在
- 使用 `$GITHUB_WORKSPACE` 環境變量

### 6. 環境變量相關錯誤

**錯誤:** 環境變量未定義或值錯誤  
**修復:**
- 在 workflow 中定義環境變量
- 使用 `env:` 部分
- 從 secrets 中讀取敏感信息

## 📝 實施建議

### 優先級排序

1. **高優先級** - 權限問題（影響所有 PR 功能）
2. **中優先級** - JavaScript 語法修復（影響分析功能）
3. **低優先級** - 錯誤處理改進（改善穩定性）

### 實施步驟

1. **立即修復權限問題**
   - 更新 workflow 權限配置
   - 測試 PR 創建評論功能

2. **修復 JavaScript 語法**
   - 更新 workflow 中的 JavaScript 代碼
   - 本地測試驗證

3. **添加錯誤處理**
   - 改進 workflow 的錯誤處理
   - 添加更詳細的日誌

4. **監控和驗證**
   - 觀察後續 CI 執行狀態
   - 驗證所有功能正常運作

## 🔄 後續監控

修復後需要監控的關鍵指標：

- ✅ Workflow 成功率
- ✅ PR 評論創建成功率
- ✅ 代碼質量檢查通過率
- ✅ 安全掃描結果
- ✅ 執行時間

## 📞 技術支持

如果問題仍然存在，建議：

1. 檢查 GitHub Actions 設置頁面
2. 查看 GitHub Status 頁面確認服務狀態
3. 查閱 GitHub Actions 文檔
4. 在 GitHub Community 尋求幫助

---

**報告生成時間:** 2026-01-17  
**診斷工具:** MNO AI Agent  
**Repository:** MachineNativeOps/machine-native-ops