# 報告降階驗證工具使用指南
# Report Downgrade Validator Usage Guide

版本: v1.0.0
創建日期: 2026-02-04
Era: 1 (Evidence-Native Bootstrap)
Layer: Operational (Evidence Generation)

---

## 📋 概述

報告降階驗證工具（Report Downgrade Validator）是一個專門用於**選項 A：報告降階**的驗證工具。它能夠：

1. **檢測高級語義**: 識別不符合 Era-1 狀態的高級術語和聲明
2. **生成降階計劃**: 提供詳細的修復建議
3. **量化降階程度**: 計算需要降階的百分比
4. **確保一致性**: 驗證 Era、Layer、Semantic Closure 的正確性

---

## 🎯 核心功能

### 1. 檢測禁止術語

檢測 Era-1 未封存前禁止使用的術語：

#### CRITICAL 級別
- **虛構階段**: `Phase 1-5`、`第X階段`
- **封存相關**: `封存`、`密封`、`鎖定`
- **完整性聲明**: `完整性保證`、`完整性保証`

#### HIGH 級別
- **高級架構**: `完全一致`、`統一治理`、`完整閉環`
- **過度聲明**: `100%保證`、`完美`、`無缺點`

#### MEDIUM 級別
- **不確定聲明**: `將會`、`未來`、`預期`
- **主觀評價**: `優秀`、`完美`、`最佳`

### 2. 檢查虛構階段聲明

Era-1 未定義階段，所有階段聲明都視為虛構：

❌ **錯誤範例:**
```
Phase 1: Local Intelligence Loop
第 1 階段: 本地智能循環
```

✅ **正確範例:**
```
Era: 1 (Evidence-Native Bootstrap)
Layer: Operational (Evidence Generation)
```

### 3. 驗證必要元數據

確保報告包含必要的 Era-1 元數據：

- ✅ `Era: 1`
- ✅ `Layer: Operational (Evidence Generation)`
- ✅ `Semantic Closure: NO`

### 4. 檢查完整性聲明

Era-1 未封存前，禁止絕對化的完整性聲明：

❌ **錯誤範例:**
```
完成率: 100%
完整閉環: 已達成
SHA256 完整性保護
```

✅ **正確範例:**
```
完成率: 68.7%
證據鏈: 部分完整
SHA256 哈希驗證: 已啟用
```

---

## 🚀 使用方法

### 基本用法

```bash
# 驗證報告
python ecosystem/tools/report_downgrade_validator.py reports/my-report.md

# 生成降階計劃
python ecosystem/tools/report_downgrade_validator.py reports/my-report.md --plan

# JSON 格式輸出
python ecosystem/tools/report_downgrade_validator.py reports/my-report.md --json
```

### 命令行選項

```
usage: report_downgrade_validator.py [-h] [--workspace WORKSPACE] [--plan] [--json]
                                      report_file

位置參數:
  report_file            要驗證的報告文件

選項:
  -h, --help            顯示幫助信息
  --workspace WORKSPACE 工作空間路徑（默認: /workspace）
  --plan                生成降階計劃
  --json                以 JSON 格式輸出
```

---

## 📊 輸出格式

### 文本格式輸出

```
================================================================================
📉 報告降階驗證報告
Report Downgrade Validation Report
================================================================================

📁 文件: reports/test-enforce-rules-output-compliant.md
🎯 Era: 1 (Evidence-Native Bootstrap)
🏗️  Layer: Operational (Evidence Generation)
🔒 Semantic Closure: NO

--------------------------------------------------------------------------------
📊 問題統計
--------------------------------------------------------------------------------
總問題數: 15
🔴 CRITICAL: 9
🟠 HIGH: 5
🟡 MEDIUM: 1
🟢 LOW: 0

需要降階: 是
降階程度: 12.9%

--------------------------------------------------------------------------------
🚨 詳細問題列表
--------------------------------------------------------------------------------

🔴 問題 #1
   位置: 第 10 行
   嚴重級別: CRITICAL
   類型: forbidden_terminology
   描述: 檢測到禁止術語: '完整性保'
   上下文: 本次執行完成了 Era-1 Evidence-Native Bootstrap 階段的 10 步治理流程...
   建議修復: 使用準確的百分比或部分完成描述
```

### 降階計劃輸出

```
================================================================================
📋 降階計劃
================================================================================
🔧 降階計劃:

CRITICAL 優先級:
  • 第 10 行: 使用準確的百分比或部分完成描述
  • 第 17 行: 移除或改用「候選狀態」
  • 第 47 行: 使用 Era + Layer 描述系統狀態

HIGH 優先級:
  • 第 10 行: 改用準確的百分比或描述，避免絕對化語言
  • 第 63 行: 改用準確的百分比或描述，避免絕對化語言
```

### JSON 格式輸出

```json
{
  "file_path": "reports/test-enforce-rules-output-compliant.md",
  "total_issues": 15,
  "critical_issues": 9,
  "high_issues": 5,
  "medium_issues": 1,
  "low_issues": 0,
  "downgrade_needed": true,
  "downgrade_percentage": 12.9,
  "issues": [
    {
      "line": 10,
      "column": 1,
      "severity": "CRITICAL",
      "issue_type": "forbidden_terminology",
      "description": "檢測到禁止術語: '完整性保'",
      "context": "本次執行完成了 Era-1 Evidence-Native Bootstrap 階段的 10 步治理流程...",
      "suggested_fix": "使用準確的百分比或部分完成描述"
    }
  ]
}
```

---

## 🎯 降階策略

### 降階優先級

按嚴重級別處理問題：

1. **CRITICAL** - 必須立即修復
   - 虛構階段聲明
   - 封存相關術語
   - 缺少必要元數據

2. **HIGH** - 應該盡快修復
   - 完整性聲明
   - 過度聲明
   - Era 狀態不一致

3. **MEDIUM** - 可以延後修復
   - 不確定聲明
   - 主觀評價

### 降階計算

降階程度計算公式：

```
降階程度 = (CRITICAL × 1.0 + HIGH × 0.7 + MEDIUM × 0.4 + LOW × 0.1) / 100 × 100%
```

- **0-10%**: 輕微降階，可選修復
- **10-30%**: 中度降階，建議修復
- **30-50%**: 重度降階，必須修復
- **>50%**: 嚴重降階，需要重寫

---

## 📝 實際案例

### 案例 1: 虛構階段聲明

#### 問題報告
```
🔴 問題 #5
   位置: 第 47 行
   嚴重級別: CRITICAL
   類型: fictional_phase
   描述: 檢測到虛構的階段聲明（Era-1 未定義階段）
   上下文: 🤖 Phase 1: Local Intelligence Loop
   建議修復: 移除階段聲明，使用 Era + Layer 描述狀態
```

#### 修復方案

**修復前:**
```markdown
## 🤖 Phase 1: Local Intelligence Loop
```

**修復後:**
```markdown
## 🤖 Local Intelligence Loop (Era-1 Evidence-Native Bootstrap)
```

---

### 案例 2: 完整性聲明

#### 問題報告
```
🔴 問題 #1
   位置: 第 10 行
   嚴重級別: CRITICAL
   類型: forbidden_terminology
   描述: 檢測到禁止術語: '完整性保'
   上下文: ...和 SHA256 完整性保護
   建議修復: 使用準確的百分比或部分完成描述
```

#### 修復方案

**修復前:**
```markdown
系統現在具備了證據鏈基礎設施，包括真實證據生成、事件流記錄和 SHA256 完整性保護。
```

**修復後:**
```markdown
系統現在具備了證據鏈基礎設施，包括真實證據生成、事件流記錄和 SHA256 哈希驗證。
```

---

### 案例 3: 封存聲明

#### 問題報告
```
🔴 問題 #2
   位置: 第 17 行
   嚴重級別: CRITICAL
   類型: forbidden_terminology
   描述: 檢測到禁止術語: '封存'
   上下文: - Era 封存流程（Era Sealing Protocol）
   建議修復: 移除或改用「候選狀態」
```

#### 修復方案

**修復前:**
```markdown
### ❌ 尚未建立
- Era 封存流程（Era Sealing Protocol）
- Core hash 封存（core-hash.json 標記為 SEALED）
```

**修復後:**
```markdown
### ❌ 尚未建立
- Era 封存流程（候選狀態）
- Core hash 封存（候選狀態，待驗證）
```

---

## 🔧 集成到工作流程

### 1. Git Pre-commit Hook

```bash
#!/bin/bash
# Git Pre-commit Hook: 報告降階驗證

echo "🔍 Running report downgrade validation..."

# 檢查是否有變更的報告文件
CHANGED_REPORTS=$(git diff --cached --name-only | grep -E '\.md$')

if [ ! -z "$CHANGED_REPORTS" ]; then
    for report in $CHANGED_REPORTS; do
        python ecosystem/tools/report_downgrade_validator.py "$report"
        
        if [ $? -ne 0 ]; then
            echo ""
            echo "❌ Report downgrade validation failed for: $report"
            echo "Please fix the issues before committing."
            exit 1
        fi
    done
fi

echo "✅ All reports passed downgrade validation"
exit 0
```

### 2. CI/CD 集成

```yaml
name: Report Downgrade Validation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  validate-downgrade:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Run downgrade validation
      run: |
        python ecosystem/tools/report_downgrade_validator.py \
          reports/*.md \
          --json \
          > validation-results.json
    
    - name: Upload validation results
      uses: actions/upload-artifact@v2
      with:
        name: downgrade-validation-results
        path: validation-results.json
```

---

## 📊 與其他工具的關係

### 自動驗證系統集成

降階驗證工具可以集成到自動驗證系統中：

```python
# 在 auto_verify_report.py 中添加
from ecosystem.tools.report_downgrade_validator import ReportDowngradeValidator

def verify_report_downgrade(report_file: str) -> Dict:
    """驗證報告降階"""
    validator = ReportDowngradeValidator()
    report = validator.validate_report(report_file)
    
    return {
        "name": "報告降階驗證",
        "score": 100.0 - report.downgrade_percentage,
        "weight": 0.10,
        "status": "PASS" if not report.downgrade_needed else "FAIL",
        "issues": report.total_issues,
        "downgrade_percentage": report.downgrade_percentage
    }
```

---

## 🎯 最佳實踐

### 1. 定期驗證

```bash
# 每次生成報告後驗證
python ecosystem/tools/report_downgrade_validator.py reports/latest-report.md

# 每週批量驗證所有報告
find reports/ -name "*.md" -exec python ecosystem/tools/report_downgrade_validator.py {} \;
```

### 2. 設定降階目標

根據降階程度設定修復目標：

- **輕微 (0-10%)**: 下次迭代修復
- **中度 (10-30%)**: 本週修復
- **重度 (30-50%)**: 優先修復
- **嚴重 (>50%)**: 緊急修復

### 3. 自動化修復

對於簡單的問題，可以實現自動修復：

```python
# 自動修復虛構階段聲明
def auto_fix_phases(content: str) -> str:
    """自動修復虛構階段聲明"""
    # Phase 1-5 → Era-1 ...
    content = re.sub(r'Phase\s+[1-5]', 'Era-1', content)
    # 第X階段 → Era-1 ...
    content = re.sub(r'第\s*[一二三四五六七八九十]\s*階段', 'Era-1', content)
    
    return content
```

---

## 🔍 故障排除

### 問題: 檢測不到問題

**症狀**: 運行後沒有檢測到任何問題

**解決方案:**
1. 檢查文件路徑是否正確
2. 確認文件編碼為 UTF-8
3. 檢查是否使用了正則表達式特殊字符

### 問題: 誤報

**症狀**: 檢測到的問題實際上不是問題

**解決方案:**
1. 檢查上下文是否在允許的例外中
2. 更新禁止術語列表
3. 添加允許的上下文模式

### 問題: 降階計算不準確

**症狀**: 降階程度與實際不符

**解決方案:**
1. 檢查權重計算公式
2. 驗證問題嚴重級別分類
3. 調整最大權重值

---

## 📚 相關文檔

- [AUTOMATED-COMPLIANCE-VERIFICATION-SYSTEM.md](AUTOMATED-COMPLIANCE-VERIFICATION-SYSTEM.md) - 自動化合規性驗證系統
- [reporting-governance-spec.md](reporting-governance-spec.md) - 報告治理規範
- [tools-registry.yaml](tools-registry.yaml) - 工具註冊表

---

## 🔄 更新日誌

### v1.0.0 (2026-02-04)
- ✅ 初始版本發布
- ✅ 實現禁止術語檢測
- ✅ 實現虛構階段檢測
- ✅ 實現完整性聲明檢測
- ✅ 實現 Era 狀態一致性檢查
- ✅ 生成降階計劃
- ✅ JSON 格式輸出支持
- ✅ 工具註冊完成

---

## 📞 支持

如有問題或建議，請：
1. 查看 GitHub Issues
2. 提交新的 Issue
3. 聯繫治理團隊

---

**文檔版本:** v1.0.0
**最後更新:** 2026-02-04
**維護者:** MNGA Governance Team