# FHS 整合驗證機制

## 概述

為確保 100% 正確的 FHS 整合，避免污染系統，我們實施了**六層驗證機制**。

## 驗證層次

### 第一層：預檢查 (Pre-flight Checks)

在開始任何整合操作前，系統會驗證：

1. ✅ **組件存在性** - 確認組件目錄存在於 `workspace/tools/`
2. ✅ **成熟度閾值** - 確認組件分數 ≥ 80 分
3. ✅ **Git 狀態** - 檢查是否有未提交的變更（警告但不阻止）
4. ✅ **FHS 目錄完整性** - 確認所有必需的 FHS 目錄存在

**失敗行為**：如果任何關鍵檢查失敗，立即中止整合。

### 第二層：路徑驗證 (Path Validation)

驗證所有目標路徑符合 FHS 標準：

1. ✅ **FHS 目錄檢查** - 只允許 `bin/`, `sbin/`, `lib/`, `etc/`
2. ✅ **子目錄結構** - `lib/` 和 `etc/` 下必須有組件子目錄
3. ✅ **命名規範** - 所有命令必須以 `mno-` 開頭
4. ✅ **文件類型** - 確保文件類型與目標目錄匹配

**範例**：
```
✓ 正確: bin/mno-repo-scan
✗ 錯誤: bin/scan (缺少 mno- 前綴)

✓ 正確: lib/repository-understanding/phase1.py
✗ 錯誤: lib/phase1.py (缺少組件子目錄)
```

### 第三層：衝突檢測 (Conflict Detection)

防止覆蓋現有文件（除非是同一組件的更新）：

1. ✅ **文件存在性檢查** - 檢測目標路徑是否已被佔用
2. ✅ **組件識別** - 允許同一組件的文件覆蓋
3. ✅ **衝突報告** - 列出所有潛在衝突

**失敗行為**：如果檢測到衝突，立即中止並報告衝突文件。

### 第四層：FHS 合規性檢查 (FHS Compliance)

確保完全符合 FHS 標準：

1. ✅ **命名規範** - 強制 `mno-*` 命名模式
2. ✅ **目錄結構** - 驗證 `lib/{component}/` 和 `etc/{component}/` 結構
3. ✅ **文件權限** - 確保正確的文件權限（命令 755，配置 644）
4. ✅ **文件類型匹配** - 確保文件放在正確的目錄

### 第五層：安全性檢查 (Security Checks)

防止惡意或錯誤的路徑操作：

1. ✅ **禁止路徑** - 不允許寫入 `/`, `/usr`, `/opt` 等系統目錄
2. ✅ **路徑跳脫檢測** - 防止 `../` 跳出倉庫
3. ✅ **關鍵文件保護** - 不允許覆蓋 `bin/sh`, `etc/passwd` 等關鍵文件
4. ✅ **倉庫邊界** - 所有路徑必須在倉庫內

**安全規則**：
```
✗ 禁止: /usr/bin/command (系統目錄)
✗ 禁止: ../../../etc/passwd (路徑跳脫)
✗ 禁止: bin/sh (關鍵系統文件)
✓ 允許: bin/mno-custom (倉庫內的正確路徑)
```

### 第六層：完整性檢查 (Integrity Checks)

確保整合的完整性和可追溯性：

1. ✅ **文件完整遷移** - 所有必要文件都包含在計劃中
2. ✅ **文檔生成** - 確保生成遷移文檔
3. ✅ **回滾能力** - 確保保留 workspace 中的原始文件
4. ✅ **追溯性** - 可追溯每個文件的來源

## 使用驗證器

### 自動驗證（推薦）

驗證已自動整合到 `fhs_integrator.py` 中：

```bash
# 驗證會自動執行
python3 workspace/tools/fhs-integration/fhs_integrator.py repository-understanding --dry-run

# 如果驗證失敗，整合會自動中止
```

### 手動驗證

也可以單獨運行驗證器：

```bash
python3 workspace/tools/fhs-integration/fhs_validator.py repository-understanding
```

### 驗證報告

驗證器會生成詳細報告：

```
================================================================================
FHS Integration Validation
================================================================================
Component: repository-understanding
Timestamp: 2026-01-17T06:00:00

[1/6] Pre-flight Checks...
  ✓ Component exists
  ✓ Maturity threshold
  ✓ Clean git state
  ✓ FHS bin/ exists
  ✓ FHS sbin/ exists
  ✓ FHS lib/ exists
  ✓ FHS etc/ exists

[2/6] Path Validation...
  ✓ Path: bin/mno-repo-scan
  ✓ Path: lib/repository-understanding/phase1.py

[3/6] Conflict Detection...
  ✓ No conflict: mno-repo-scan
  ✓ No conflict: phase1.py
  ✓ No conflicts detected

[4/6] FHS Compliance...
  ✓ Naming: mno-repo-scan
  ✓ Library structure
  ✓ Config structure

[5/6] Security Checks...
  ✓ No forbidden paths
  ✓ Paths within repo
  ✓ No critical file overwrites

[6/6] Integrity Checks...
  ✓ Python files → lib/
  ✓ Migration documentation
  ✓ Preserves workspace files

================================================================================
VALIDATION SUMMARY
================================================================================
Total Checks: 21
Passed: 21
Failed: 0
Errors: 0
Warnings: 0

✓ VALIDATION PASSED - Safe to proceed with integration
================================================================================
```

## 驗證失敗範例

如果驗證失敗，會看到詳細的錯誤報告：

```
================================================================================
VALIDATION SUMMARY
================================================================================
Total Checks: 21
Passed: 18
Failed: 3
Errors: 3
Warnings: 1

ERRORS:
  ✗ Invalid FHS path: usr/bin/command - Not a valid FHS directory: usr
  ✗ Command name violation: scan (must start with 'mno-')
  ✗ Conflict: bin/mno-existing already exists

WARNINGS:
  ⚠ Uncommitted changes detected in repository

✗ VALIDATION FAILED - DO NOT proceed with integration
  Fix all errors before attempting integration
================================================================================
```

## 安全保證

### 1. 不會污染系統

- ✅ 所有路徑都在倉庫內
- ✅ 不會寫入系統目錄
- ✅ 不會覆蓋關鍵文件

### 2. 符合 FHS 標準

- ✅ 標準化的 `mno-*` 命令命名
- ✅ 正確的目錄結構
- ✅ 適當的文件權限

### 3. 可追溯與回滾

- ✅ 保留原始文件在 workspace
- ✅ 生成詳細的遷移文檔
- ✅ 可以回滾到整合前狀態

### 4. 漸進式遷移

- ✅ 只有成熟的組件（80+ 分）才會被整合
- ✅ 支持乾運行模式預覽
- ✅ 驗證失敗會自動中止

## 配置選項

### 跳過驗證（不建議）

```python
integrator = FHSIntegrator(dry_run=False)
result = integrator.integrate_component(
    "component-name",
    maturity_score=85,
    skip_validation=True  # ⚠️ 危險：跳過所有安全檢查
)
```

**警告**：跳過驗證可能導致系統污染，僅在完全理解風險時使用。

### 保存驗證報告

```python
validator = FHSIntegrationValidator()
report = validator.validate_integration(component_name, plan)
validator.save_validation_report(component_name)  # 保存 JSON 報告
```

## 最佳實踐

1. **始終使用乾運行**：先用 `--dry-run` 預覽
2. **檢查驗證報告**：仔細閱讀所有錯誤和警告
3. **修復所有錯誤**：不要強制執行有錯誤的整合
4. **保存驗證報告**：用於審計和追溯
5. **測試整合結果**：整合後測試新的 `mno-*` 命令

## 故障排除

### Q: 驗證失敗："Command name violation"

A: 確保所有命令以 `mno-` 開頭。修改 `fhs_integrator.py` 中的命名邏輯。

### Q: 驗證失敗："Invalid FHS path"

A: 只允許 `bin/`, `sbin/`, `lib/`, `etc/` 四個目錄。檢查路徑是否正確。

### Q: 驗證失敗："Conflict detected"

A: 目標文件已存在。選擇不同的名稱或移除現有文件。

### Q: 如何查看詳細的驗證日誌？

A: 驗證報告保存在 `docs/fhs-integration/validation-*.json`

## 總結

這個六層驗證機制確保：

✅ **100% 安全** - 不會污染系統  
✅ **100% 合規** - 符合 FHS 標準  
✅ **100% 可追溯** - 完整的審計軌跡  
✅ **100% 可回滾** - 保留原始文件  

這是一個**進階的、經過深思熟慮的遷移機制**，而不是簡單的文件複製。
