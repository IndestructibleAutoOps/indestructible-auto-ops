# GL 架構整合計劃報告

**生成日期**: 2026-01-21T04:04:43.516936

## 摘要

| 指標 | 數值 |
|------|------|
| total_gl_files | 83 |
| compliant_files | 65 |
| non_compliant_files | 18 |
| compliance_rate | 78.3% |
| duplicate_directories | 7 |
| total_actions | 35 |

## 重複目錄

### governance/GL-architecture ↔ workspace/governance/GL-architecture
共同檔案數: 33

### governance/layers ↔ workspace/governance/layers
共同檔案數: 15

### governance/meta-spec ↔ workspace/governance/meta-spec
共同檔案數: 5

### governance/sealed ↔ workspace/governance/sealed
共同檔案數: 3

### governance/naming-governance-v1.0.0 ↔ workspace/governance/naming-governance-v1.0.0
共同檔案數: 15

### governance/naming-governance-v1.0.0-extended ↔ workspace/governance/naming-governance-v1.0.0-extended
共同檔案數: 6

### governance/quantum-naming-v4.0.0 ↔ workspace/governance/quantum-naming-v4.0.0
共同檔案數: 8

## 不合規檔案

| 檔案路徑 | 問題 |
|----------|------|
| `GL-EXECUTION-MODE.yaml` | 建議重命名為: gl-execution-mode.yaml |
| `GL-MAINLINE-INTEGRATION.md` | 建議重命名為: gl-mainline-integration.md |
| `reports/GL_ARCHITECTURE_COMPLETION_REPORT.md` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_ARCHITECTURE_COMPLETION_REPORT.md |
| `governance/GL-architecture/GL_DIRECTORY_NAMING_SPEC.yaml` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_DIRECTORY_NAMING_SPEC.yaml; 建議重命名為: gl-directory-naming-spec.yaml |
| `governance/GL-architecture/GL_LAYERS.yaml` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_LAYERS.yaml; 建議重命名為: gl-layers.yaml |
| `governance/GL-architecture/GL_SEMANTIC_STABILIZATION.yaml` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_SEMANTIC_STABILIZATION.yaml; 建議重命名為: gl-semantic-stabilization.yaml |
| `governance/GL-architecture/GL_MAPPING.csv` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_MAPPING.csv; 建議重命名為: gl-mapping.csv |
| `governance/GL-architecture/GL_FILESYSTEM_MAPPING.yaml` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_FILESYSTEM_MAPPING.yaml; 建議重命名為: gl-filesystem-mapping.yaml |
| `governance/GL-architecture/GL_REFACTORING_EXEC_PROMPTS.md` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_REFACTORING_EXEC_PROMPTS.md; 建議重命名為: gl-refactoring-exec-prompts.md |
| `governance/GL-architecture/GL_QUICKREF.md` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_QUICKREF.md; 建議重命名為: gl-quickref.md |
| `workspace/docs/GLOBAL_TECH_REVIEW.txt` | 使用底線分隔的大寫命名，建議改為 kebab-case: GLOBAL_TECH_REVIEW.txt |
| `workspace/governance/GL-architecture/GL_DIRECTORY_NAMING_SPEC.yaml` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_DIRECTORY_NAMING_SPEC.yaml; 建議重命名為: gl-directory-naming-spec.yaml |
| `workspace/governance/GL-architecture/GL_LAYERS.yaml` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_LAYERS.yaml; 建議重命名為: gl-layers.yaml |
| `workspace/governance/GL-architecture/GL_SEMANTIC_STABILIZATION.yaml` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_SEMANTIC_STABILIZATION.yaml; 建議重命名為: gl-semantic-stabilization.yaml |
| `workspace/governance/GL-architecture/GL_MAPPING.csv` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_MAPPING.csv; 建議重命名為: gl-mapping.csv |
| `workspace/governance/GL-architecture/GL_FILESYSTEM_MAPPING.yaml` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_FILESYSTEM_MAPPING.yaml; 建議重命名為: gl-filesystem-mapping.yaml |
| `workspace/governance/GL-architecture/GL_REFACTORING_EXEC_PROMPTS.md` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_REFACTORING_EXEC_PROMPTS.md; 建議重命名為: gl-refactoring-exec-prompts.md |
| `workspace/governance/GL-architecture/GL_QUICKREF.md` | 使用底線分隔的大寫命名，建議改為 kebab-case: GL_QUICKREF.md; 建議重命名為: gl-quickref.md |

## 整合動作計劃

### 高優先級 (Priority 1)

- **MERGE**: `workspace/governance/GL-architecture`
  - 目標: `governance/GL-architecture`
  - 原因: 合併重複目錄 workspace/governance/GL-architecture 到 governance/GL-architecture
  - 風險: medium
- **DELETE**: `workspace/governance/GL-architecture`
  - 原因: 刪除已合併的重複目錄 workspace/governance/GL-architecture
  - 風險: medium
- **MERGE**: `workspace/governance/layers`
  - 目標: `governance/layers`
  - 原因: 合併重複目錄 workspace/governance/layers 到 governance/layers
  - 風險: medium
- **DELETE**: `workspace/governance/layers`
  - 原因: 刪除已合併的重複目錄 workspace/governance/layers
  - 風險: medium
- **MERGE**: `workspace/governance/meta-spec`
  - 目標: `governance/meta-spec`
  - 原因: 合併重複目錄 workspace/governance/meta-spec 到 governance/meta-spec
  - 風險: medium
- **DELETE**: `workspace/governance/meta-spec`
  - 原因: 刪除已合併的重複目錄 workspace/governance/meta-spec
  - 風險: medium
- **MERGE**: `workspace/governance/sealed`
  - 目標: `governance/sealed`
  - 原因: 合併重複目錄 workspace/governance/sealed 到 governance/sealed
  - 風險: medium
- **DELETE**: `workspace/governance/sealed`
  - 原因: 刪除已合併的重複目錄 workspace/governance/sealed
  - 風險: medium
- **MERGE**: `workspace/governance/naming-governance-v1.0.0`
  - 目標: `governance/naming-governance-v1.0.0`
  - 原因: 合併重複目錄 workspace/governance/naming-governance-v1.0.0 到 governance/naming-governance-v1.0.0
  - 風險: medium
- **DELETE**: `workspace/governance/naming-governance-v1.0.0`
  - 原因: 刪除已合併的重複目錄 workspace/governance/naming-governance-v1.0.0
  - 風險: medium
- **MERGE**: `workspace/governance/naming-governance-v1.0.0-extended`
  - 目標: `governance/naming-governance-v1.0.0-extended`
  - 原因: 合併重複目錄 workspace/governance/naming-governance-v1.0.0-extended 到 governance/naming-governance-v1.0.0-extended
  - 風險: medium
- **DELETE**: `workspace/governance/naming-governance-v1.0.0-extended`
  - 原因: 刪除已合併的重複目錄 workspace/governance/naming-governance-v1.0.0-extended
  - 風險: medium
- **MERGE**: `workspace/governance/quantum-naming-v4.0.0`
  - 目標: `governance/quantum-naming-v4.0.0`
  - 原因: 合併重複目錄 workspace/governance/quantum-naming-v4.0.0 到 governance/quantum-naming-v4.0.0
  - 風險: medium
- **DELETE**: `workspace/governance/quantum-naming-v4.0.0`
  - 原因: 刪除已合併的重複目錄 workspace/governance/quantum-naming-v4.0.0
  - 風險: medium

### 中優先級 (Priority 2)

- **RENAME**: `GL-EXECUTION-MODE.yaml`
  - 目標: `gl-execution-mode.yaml`
  - 原因: 統一命名風格: GL-EXECUTION-MODE.yaml -> gl-execution-mode.yaml
- **RENAME**: `GL-MAINLINE-INTEGRATION.md`
  - 目標: `gl-mainline-integration.md`
  - 原因: 統一命名風格: GL-MAINLINE-INTEGRATION.md -> gl-mainline-integration.md
- **RENAME**: `governance/GL-architecture/GL_DIRECTORY_NAMING_SPEC.yaml`
  - 目標: `governance/GL-architecture/gl-directory-naming-spec.yaml`
  - 原因: 統一命名風格: GL_DIRECTORY_NAMING_SPEC.yaml -> gl-directory-naming-spec.yaml
- **RENAME**: `governance/GL-architecture/GL_LAYERS.yaml`
  - 目標: `governance/GL-architecture/gl-layers.yaml`
  - 原因: 統一命名風格: GL_LAYERS.yaml -> gl-layers.yaml
- **RENAME**: `governance/GL-architecture/GL_SEMANTIC_STABILIZATION.yaml`
  - 目標: `governance/GL-architecture/gl-semantic-stabilization.yaml`
  - 原因: 統一命名風格: GL_SEMANTIC_STABILIZATION.yaml -> gl-semantic-stabilization.yaml
- **RENAME**: `governance/GL-architecture/GL_MAPPING.csv`
  - 目標: `governance/GL-architecture/gl-mapping.csv`
  - 原因: 統一命名風格: GL_MAPPING.csv -> gl-mapping.csv
- **RENAME**: `governance/GL-architecture/GL_FILESYSTEM_MAPPING.yaml`
  - 目標: `governance/GL-architecture/gl-filesystem-mapping.yaml`
  - 原因: 統一命名風格: GL_FILESYSTEM_MAPPING.yaml -> gl-filesystem-mapping.yaml
- **RENAME**: `governance/GL-architecture/GL_REFACTORING_EXEC_PROMPTS.md`
  - 目標: `governance/GL-architecture/gl-refactoring-exec-prompts.md`
  - 原因: 統一命名風格: GL_REFACTORING_EXEC_PROMPTS.md -> gl-refactoring-exec-prompts.md
- **RENAME**: `governance/GL-architecture/GL_QUICKREF.md`
  - 目標: `governance/GL-architecture/gl-quickref.md`
  - 原因: 統一命名風格: GL_QUICKREF.md -> gl-quickref.md
- **RENAME**: `workspace/governance/GL-architecture/GL_DIRECTORY_NAMING_SPEC.yaml`
  - 目標: `workspace/governance/GL-architecture/gl-directory-naming-spec.yaml`
  - 原因: 統一命名風格: GL_DIRECTORY_NAMING_SPEC.yaml -> gl-directory-naming-spec.yaml
- **RENAME**: `workspace/governance/GL-architecture/GL_LAYERS.yaml`
  - 目標: `workspace/governance/GL-architecture/gl-layers.yaml`
  - 原因: 統一命名風格: GL_LAYERS.yaml -> gl-layers.yaml
- **RENAME**: `workspace/governance/GL-architecture/GL_SEMANTIC_STABILIZATION.yaml`
  - 目標: `workspace/governance/GL-architecture/gl-semantic-stabilization.yaml`
  - 原因: 統一命名風格: GL_SEMANTIC_STABILIZATION.yaml -> gl-semantic-stabilization.yaml
- **RENAME**: `workspace/governance/GL-architecture/GL_MAPPING.csv`
  - 目標: `workspace/governance/GL-architecture/gl-mapping.csv`
  - 原因: 統一命名風格: GL_MAPPING.csv -> gl-mapping.csv
- **RENAME**: `workspace/governance/GL-architecture/GL_FILESYSTEM_MAPPING.yaml`
  - 目標: `workspace/governance/GL-architecture/gl-filesystem-mapping.yaml`
  - 原因: 統一命名風格: GL_FILESYSTEM_MAPPING.yaml -> gl-filesystem-mapping.yaml
- **RENAME**: `workspace/governance/GL-architecture/GL_REFACTORING_EXEC_PROMPTS.md`
  - 目標: `workspace/governance/GL-architecture/gl-refactoring-exec-prompts.md`
  - 原因: 統一命名風格: GL_REFACTORING_EXEC_PROMPTS.md -> gl-refactoring-exec-prompts.md
- **RENAME**: `workspace/governance/GL-architecture/GL_QUICKREF.md`
  - 目標: `workspace/governance/GL-architecture/gl-quickref.md`
  - 原因: 統一命名風格: GL_QUICKREF.md -> gl-quickref.md

### 低優先級 (Priority 3)

- **MOVE**: `GL-UNIFIED-NAMING-CHARTER-ANALYSIS.md`
  - 目標: `governance/GL-architecture/GL-UNIFIED-NAMING-CHARTER-ANALYSIS.md`
  - 原因: 將根目錄 GL 檔案移至統一位置
- **MOVE**: `GL-EXECUTION-MODE.yaml`
  - 目標: `governance/GL-architecture/GL-EXECUTION-MODE.yaml`
  - 原因: 將根目錄 GL 檔案移至統一位置
- **MOVE**: `GL-MAINLINE-INTEGRATION.md`
  - 目標: `governance/GL-architecture/GL-MAINLINE-INTEGRATION.md`
  - 原因: 將根目錄 GL 檔案移至統一位置
- **MOVE**: `gl-analysis-scanner.py`
  - 目標: `governance/GL-architecture/gl-analysis-scanner.py`
  - 原因: 將根目錄 GL 檔案移至統一位置
- **MOVE**: `gl-analysis-report.json`
  - 目標: `governance/GL-architecture/gl-analysis-report.json`
  - 原因: 將根目錄 GL 檔案移至統一位置
