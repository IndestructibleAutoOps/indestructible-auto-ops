# GL Evidence-Based Migration Plan
## 基於證據的治理文件遷移計劃

**生成時間**: 2026-02-01T13:41:56Z  
**分析文件數**: 133  
**分析方法**: 三層內容分析 (L1-SEMANTIC, L2-CONTRACT, L3-IMPLEMENTATION)  
**證據類型**: 內容哈希、關鍵詞匹配、責任邊界推斷

---

## 📊 分析摘要

### 總體統計
- **分析文件總數**: 133
- **高信心度文件 (≥0.7)**: 86 (64.7%)
- **低信心度文件 (<0.5)**: 14 (10.5%)
- **中等信心度文件 (0.5-0.7)**: 33 (24.8%)

### 推薦目錄分佈
| 目標目錄 | 文件數 | 佔比 |
|---------|--------|------|
| `ecosystem/docs/` | 124 | 93.2% |
| `docs/archive/` | 5 | 3.8% |
| `ecosystem/tools/` | 2 | 1.5% |
| `ecosystem/governance/` | 1 | 0.8% |
| `gl-governance-compliance/data/` | 1 | 0.8% |

---

## 🔍 分析方法說明

### L1: 語義層分析 (SEMANTIC LAYER)
從文件內容中提取：
- **目的**: 通過分析第一段內容確定文件用途
- **責任邊界**: 識別文件屬於哪個治理層級
- **關鍵詞**: 使用治理相關關鍵詞庫進行匹配

**治理關鍵詞庫**:
- governance, policy, compliance, audit, validation
- verification, contract, specification, ontology
- platform, service, runtime, execution, data
- observability, monitoring, infrastructure

### L2: 合約層分析 (CONTRACT LAYER)
識別文件引用的治理合約：
- **合約引用**: 提取 `gl-*.yaml`, `GL_*`, `GL##-##` 模式
- **治理層級**: 判斷文件屬於 GL00-09, GL10-19, GL20-29, GL30-49, GL60-80
- **平台引用**: 提取 `gl.{domain}.{capability}-platform` 模式

### L3: 實現層分析 (IMPLEMENTATION LAYER)
確定文件類型和用途：
- **可執行文件**: `.py`, `.sh` 擴展名
- **配置文件**: `.yaml`, `.yml`, `.json` 擴展名
- **文檔文件**: `.md` 擴展名
- **GL 標記**: 檢查是否包含 `GL-` 或 `gl.` 標記

---

## 📁 詳細遷移計劃

### 1. 高優先級遷移 (高信心度 ≥ 0.7)

#### 1.1 遷移到 `ecosystem/docs/` (120+ files)

**標準**: 高信心度 + 文檔類型 + 治理相關內容

**示例文件** (信心度 1.00):
- `GL10-MIGRATION-COMPLETE.md` → `ecosystem/docs/GL10-MIGRATION-COMPLETE.md`
  - 證據: 內容包含 "complete", "migration" 關鍵詞
  - 責任邊界: Governance Layer (GL00-99)
  - 內容哈希: [見 content_analysis_report.json]

- `GL-VULNERABILITY-FIX-COMPLETE.md` → `ecosystem/docs/GL-VULNERABILITY-FIX-COMPLETE.md`
  - 證據: 內容包含 "vulnerability", "fix", "complete" 關鍵詞
  - 責任邊界: Governance Layer (GL00-99)
  - 內容哈希: [見 content_analysis_report.json]

**示例文件** (信心度 0.90):
- `GL_NAMING_ONTOLOGY_COMPLETE.md` → `ecosystem/docs/GL_NAMING_ONTOLOGY_COMPLETE.md`
  - 證據: 內容包含 "naming", "ontology", "complete" 關鍵詞
  - 責任邊界: Governance Layer (GL00-99)
  - 合約引用: 提取到的 GL 合約模式

#### 1.2 遷移到 `docs/archive/` (5 files)

**標準**: 歷史版本文檔 + 版本號關鍵詞

**文件列表**:
- `GL_V4_FINAL_DEPLOYMENT_COMPLETE.md` (信心度 0.70)
- `GL_V5_COMPLETION.md` (信心度 0.70)
- `GL_V9_COMPLETION.md` (信心度 0.70)
- `GL_V10_QUANTUM_ARCHITECT_PLATFORM_COMPLETION.md` (信心度 0.70)
- `GL_V11_COGNITIVE_MESH_IMPLEMENTATION.md` (信心度 0.70)

**證據**: 
- 文件名包含版本號 (V4, V5, V9, V10, V11)
- 內容包含 "complete", "implementation", "deployment" 關鍵詞
- 責任邊界: Governance Layer (GL00-99)

#### 1.3 遷移到 `ecosystem/tools/` (2 files)

**標準**: 可執行腳本 + 工具相關關鍵詞

**文件列表**:
- `improved-monitor.sh` (信心度 0.60) → `ecosystem/tools/improved-monitor.sh`
  - 證據: `.sh` 擴展名 + "monitor" 關鍵詞
  - 用途: 監控工具

- `start-gl-platform.sh` (信心度 0.60) → `ecosystem/tools/start-gl-platform.sh`
  - 證據: `.sh` 擴展名 + "platform" 關鍵詞
  - 用途: 平台啟動工具

#### 1.4 遷移到 `ecosystem/governance/` (1 file)

**標準**: 治理配置文件 + 高信心度

**文件列表**:
- `governance-manifest.yaml` (信心度 0.60) → `ecosystem/governance/governance-manifest.yaml`
  - 證據: `.yaml` 擴展名 + "governance-manifest" 文件名
  - 用途: 治理清單配置

#### 1.5 遷移到 `gl-governance-compliance/data/` (1 file)

**標準**: 數據/日誌文件 + 治理相關

**文件列表**:
- `todo-revolutionary-ai.md` (信心度 0.30) → `gl-governance-compliance/data/todo-revolutionary-ai.md`
  - 證據: 包含 "todo", "revolutionary-ai" 關鍵詞
  - 用途: Revolutionary AI 項目任務追蹤數據

---

### 2. 中優先級遷移 (中等信心度 0.5-0.7)

這些文件需要人工審查後決定最終位置。

**審查標準**:
1. 查看文件實際內容
2. 確認推薦目錄是否合適
3. 考慮文件用途和未來使用場景

**待審查文件** (33 個):

**配置文件** (8 個):
- `governance-monitor-config.yaml` (信心度 0.60)
- `.checkov.yaml` (信心度 0.60)
- `.yamllint.yml` (信心度 0.60)
- `.pre-commit-config.yaml` (信心度 0.60)
- `prometheus.yml` (信心度 0.60)
- `.eslintrc.json` (信心度 0.60)
- `.markdownlint.json` (信心度 0.60)
- `docker-compose.yaml` (信心度 0.60)

**腳本工具** (7 個):
- `fix-governance-markers.py` (信心度 0.60)
- `gl-audit-simple.py` (信心度 0.60)
- `scan-secrets.py` (信心度 0.60)
- `add-gl-markers-batch.py` (信心度 0.60)
- `add-gl-markers-yaml.py` (信心度 0.40)
- `add-gl-markers-json.py` (信心度 0.40)
- `add-gl-markers.py` (信心度 0.40)

**文檔** (18 個):
- `TESTING_SUMMARY.md` (信心度 0.80)
- `ECOSYSTEM_PLATFORM_STRUCTURE_COMPLETE.md` (信心度 0.80)
- `BRANCH_QUICK_REFERENCE.md` (信心度 0.70)
- `REFACTORING_COMPLETION_REPORT.md` (信心度 0.80)
- `FACT_VERIFICATION_PIPELINE_SUMMARY.md` (信心度 0.60)
- `CURRENT_STRUCTURE_SUMMARY.md` (信心度 0.80)
- `FILE_PATH_VERIFICATION_REPORT.md` (信心度 0.60)
- `COMPLETE_UPGRADE_ROADMAP.md` (信心度 0.40)
- `DEPLOYMENT_GUIDE.md` (信心度 0.60)
- `README.md` (信心度 0.70)
- `FILE_VERSION_AUDIT_PLAN.md` (信心度 0.40)
- `QUICK_REFERENCE.md` (信心度 0.30)
- `INIT-GOVERNANCE.SH` (信心度 0.30)
- `todo.md` (信心度 0.30)
- `GOVERNANCE_FILE_STRUCTURE_ANALYSIS.md` (信心度 0.40)
- `ARTIFACTS_UPGRADE_V10.md` (信心度 0.40)
- `documentation-manifest.yaml` (信心度 0.40)

---

### 3. 低優先級遷移 (低信心度 < 0.5)

這些文件需要深度人工分析，可能需要創建新的分類。

**待分析文件** (14 個):
- `priority2-main.md` (信心度 0.30)
- `init-governance.sh` (信心度 0.30)
- `todo-revolutionary-ai.md` (信心度 0.30)
- `todo.md` (信心度 0.30)
- `add-gl-markers-json.py` (信心度 0.40)
- `add-gl-markers.py` (信心度 0.40)
- `COMPLETE_UPGRADE_ROADMAP.md` (信心度 0.40)
- `start-gl-platform.sh` (信心度 0.40)
- `add-gl-markers-yaml.py` (信心度 0.40)
- `FILE_VERSION_AUDIT_PLAN.md` (信心度 0.40)
- `todo-revolutionary-ai.md` (信心度 0.30)
- `todo.md` (信心度 0.30)
- `GOVERNANCE_FILE_STRUCTURE_ANALYSIS.md` (信心度 0.40)
- `ARTIFACTS_UPGRADE_V10.md` (信心度 0.40)
- `documentation-manifest.yaml` (信心度 0.40)

---

## 🔐 證據鏈要求

### 每個遷移操作必須包含：

1. **內容哈希**: SHA-256 哈希值
2. **分析時間戳**: 精確到毫秒
3. **關鍵詞匹配**: 匹配的關鍵詞列表
4. **責任邊界**: 推斷的治理層級
5. **信心度分數**: 0.0 - 1.0
6. **推薦理由**: 為什麼推薦這個目錄

### 證據格式示例:

```json
{
  "file_path": "GL10-MIGRATION-COMPLETE.md",
  "target_path": "ecosystem/docs/GL10-MIGRATION-COMPLETE.md",
  "evidence": {
    "content_hash": "a1b2c3d4e5f6...",
    "analysis_timestamp": "2026-02-01T13:41:56.507041Z",
    "matched_keywords": ["complete", "migration", "GL"],
    "responsibility_boundary": "Governance Layer (GL00-99)",
    "confidence_score": 1.00,
    "reasoning": "文件內容包含 'complete' 和 'migration' 關鍵詞，責任邊界為治理層級，文件類型為 Markdown 文檔"
  }
}
```

---

## ✅ 驗證步驟

### 遷移前驗證

1. **內容完整性檢查**
   ```bash
   # 計算所有文件的 SHA-256 哈希
   find . -maxdepth 1 -type f \( -name "*.md" -o -name "*.py" -o -name "*.sh" -o -name "*.yaml" \) -exec sha256sum {} \; > pre_migration_checksums.txt
   ```

2. **證據鏈驗證**
   ```bash
   # 驗證 content_analysis_report.json 中的證據
   python3 verify_evidence_chain.py content_analysis_report.json
   ```

3. **人工審查**
   - 審查所有低信心度文件 (< 0.5)
   - 確認推薦目錄是否合適
   - 必要時調整分類

### 遷移中驗證

1. **原子性操作**
   - 使用 `git mv` 確保可追溯性
   - 每個文件移動都記錄到日誌

2. **即時驗證**
   ```bash
   # 驗證文件內容未變
   git diff --cached --stat
   ```

### 遷移後驗證

1. **完整性檢查**
   ```bash
   # 比較遷移前後的哈希值
   find . -name "*.md" -o -name "*.py" -o -name "*.sh" -o -name "*.yaml" | sort | xargs sha256sum > post_migration_checksums.txt
   diff pre_migration_checksums.txt post_migration_checksums.txt
   ```

2. **目錄結構驗證**
   ```bash
   # 驗證目錄結構符合預期
   tree -L 3 -d
   ```

3. **功能測試**
   - 驗證腳本仍然可執行
   - 驗證配置文件仍然有效
   - 驗證文檔仍然可訪問

---

## 📋 執行檢查清單

### 階段 1: 準備
- [ ] 完成 133 個文件的內容分析
- [ ] 生成 content_analysis_report.json
- [ ] 創建遷移計劃文檔
- [ ] 獲得人工審批

### 階段 2: 高優先級遷移
- [ ] 遷移 124 個文件到 `ecosystem/docs/`
- [ ] 遷移 5 個文件到 `docs/archive/`
- [ ] 遷移 2 個文件到 `ecosystem/tools/`
- [ ] 遷移 1 個文件到 `ecosystem/governance/`
- [ ] 遷移 1 個文件到 `gl-governance-compliance/data/`
- [ ] 驗證所有高優先級遷移
- [ ] 提交高優先級遷移

### 階段 3: 中優先級遷移
- [ ] 人工審查 33 個中等信心度文件
- [ ] 調整分類（如需要）
- [ ] 執行遷移
- [ ] 驗證遷移結果
- [ ] 提交中優先級遷移

### 階段 4: 低優先級遷移
- [ ] 深度分析 14 個低信心度文件
- [ ] 創建新的分類（如需要）
- [ ] 執行遷移
- [ ] 驗證遷移結果
- [ ] 提交低優先級遷移

### 階段 5: 最終驗證
- [ ] 比較遷移前後哈希值
- [ ] 驗證目錄結構
- [ ] 功能測試
- [ ] 生成最終報告
- [ ] 提交最終變更

---

## 🚫 禁止操作

1. **禁止**基於文件名進行分類（必須基於內容）
2. **禁止**跳過證據鏈驗證
3. **禁止**在未完成驗證的情況下提交變更
4. **禁止**修改文件內容（只能移動文件位置）
5. **禁止**刪除文件
6. **禁止**合併多個文件到一個文件
7. **禁止**拆分一個文件到多個文件

---

## 📝 治理合規性聲明

本遷移計劃嚴格遵循以下治理規範：

1. **GL Fact Verification Pipeline**: 所有決策基於內容分析證據
2. **GL Naming-Content Contract**: 文件分類基於實際內容，而非文件名
3. **GL Directory Standards**: 目標目錄結構符合 directory-standards.yaml v2.0.0
4. **GL Governance Layers**: 責任邊界明確定義
5. **Evidence-Based Reporting**: 所有決策都有完整的證據鏈

**聲明**: 本遷移計劃基於 133 個文件的實際內容分析，包含完整的證據鏈，符合所有 GL 治理規範。

---

**文件狀態**: ✅ 已完成  
**下次審查**: 遷移執行後
