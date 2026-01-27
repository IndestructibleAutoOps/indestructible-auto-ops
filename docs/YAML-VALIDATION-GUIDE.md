# YAML 驗證系統指南

## 概述

GL (Governance Layer) 項目現在擁有完整的 YAML 驗證系統，確保所有 YAML 文件的語法正確性和結構完整性。

## 組件

### 1. YAML 驗證工具 (`tools/yaml_validator.sh`)

獨立的驗證工具，可手動執行或集成到 CI/CD 流程中。

**功能：**
- 檢查 YAML 語法正確性
- 驗證文件結構完整性
- 檢查必需字段
- 驗證版本號格式 (semver)
- 生成詳細的驗證報告

**使用方法：**
```bash
./tools/yaml_validator.sh
```

**輸出：**
- 彩色終端輸出，顯示驗證狀態
- 統計信息：掃描文件數、有效文件數、警告文件數、無效文件數
- 詳細的錯誤和警告信息

### 2. Git Hooks

#### Pre-commit Hook (`hooks/pre-commit-yaml-validation.sh`)

在提交前驗證所有變更的 YAML 文件。

**功能：**
- 只驗證即將提交的 YAML 文件
- 語法檢查和結構驗證
- GL 特定驗證（基於層級）
- 可通過 `--no-verify` 跳過

**安裝：**
```bash
cp hooks/pre-commit-yaml-validation.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

#### Pre-push Hook (`hooks/pre-push-yaml-validation.sh`)

在推送前執行完整的 YAML 驗證。

**功能：**
- 驗證所有 GL YAML 變更
- 深度層級特定驗證
- 交叉引用檢查
- 可通過 `--no-verify` 跳過

**安裝：**
```bash
cp hooks/pre-push-yaml-validation.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

### 3. YAML 修復腳本

#### convert_markdown_to_yaml.py

將包含 Markdown 標記的 YAML 文件轉換為純 YAML。

**功能：**
- 移除 Markdown 標題 (`#`)
- 移除加粗標記 (`**`)
- 移除代碼塊標記 (```yaml)
- 提取純 YAML 內容

**使用方法：**
```bash
python3 scripts/convert_markdown_to_yaml.py <yaml_file>
```

#### clean_yaml_files.py

批量清理 YAML 文件。

**功能：**
- 移除所有 Markdown 標記
- 移除多餘的文檔分隔符
- 保留第一個有效的 YAML 文檔

**使用方法：**
```bash
python3 scripts/clean_yaml_files.py
```

#### fix_yaml_indentation.py

修復 YAML 縮排問題。

**功能：**
- 修正列表項目的縮排
- 統一空行處理
- 確保一致的縮排格式

**使用方法：**
```bash
python3 scripts/fix_yaml_indentation.py <yaml_file>
```

#### fix_yaml_structure.py

修復 YAML 結構問題。

**功能：**
- 處理嵌套列表和映射
- 修正層級關係
- 統一縮排規則

**使用方法：**
```bash
python3 scripts/fix_yaml_structure.py <yaml_file>
```

## 驗證流程

### 1. 開發階段

```bash
# 開發完成後，手動驗證
./tools/yaml_validator.sh
```

### 2. 提交階段

```bash
# Git 自動執行 pre-commit hook
git add .
git commit
# 如果有錯誤，會阻止提交
```

### 3. 推送階段

```bash
# Git 自動執行 pre-push hook
git push origin feature/gl00-09-enhanced-artifacts
# 如果有錯誤，會阻止推送
```

## 驗證規則

### 基本規則

1. **語法正確性**
   - 所有 YAML 文件必須符合 YAML 1.2 規範
   - 縮排必須一致（建議使用 2 個空格）
   - 鍵值對格式正確

2. **結構完整性**
   - 根節點必須是字典
   - 必需字段必須存在
   - 數據類型正確

3. **GL 特定規則**
   - 文件必須包含 `apiVersion` 和 `kind` 字段
   - 版本號必須符合 semver 格式 (x.y.z)
   - 描述字段必須是字符串類型

### 層級特定驗證

#### GL00 (戰略層)
- 必需字段：`version`, `description`, `scope`
- 必須包含戰略目標或視聲明

#### GL10-GL90 (其他層級)
- 必須是非空字典
- 必須包含層級特定的元數據

## 常見問題

### 1. 如何跳過驗證？

```bash
# 跳過 pre-commit hook
git commit --no-verify

# 跳過 pre-push hook
git push --no-verify
```

⚠️ **警告：** 不建議跳過驗證，這可能導致無效的 YAML 文件進入倉庫。

### 2. 如何處理驗證失敗？

1. 查看錯誤信息
2. 使用修復腳本修復問題
3. 重新驗證
4. 提交或推送

### 3. 如何添加自定義驗證規則？

編輯 `tools/yaml_validator.sh`，在 Python 代碼中添加自定義驗證邏輯。

## 當前狀態

### 驗證統計

- **總文件數**: 73
- **有效文件**: 73 (100%)
- **警告文件**: 0
- **無效文件**: 0

### 已修復的問題

- 移除了所有 Markdown 標記
- 清理了所有文檔分隔符
- 修正了縮排和結構問題
- 統一了文件格式

## 未來改進

1. **擴展驗證規則**
   - 添加更多 GL 層級特定驗證
   - 實現交叉引用驗證
   - 添加語義驗證

2. **自動化修復**
   - 自動檢測並修復常見問題
   - 智能縮排修復
   - 自動格式化

3. **CI/CD 集成**
   - GitHub Actions 工作流
   - 自動化測試
   - 持續驗證

## 維護

### 更新驗證規則

編輯 `tools/yaml_validator.sh` 中的 Python 代碼部分。

### 更新 Git Hooks

修改 `hooks/` 目錄下的腳本，然後重新安裝到 `.git/hooks/`。

### 添加新的修復腳本

創建新的 Python 腳本到 `scripts/` 目錄，確保遵循現有的命名和格式約定。

## 聯繫

如有問題或建議，請通過以下方式聯繫：
- GitHub Issues: https://github.com/MachineNativeOps/machine-native-ops/issues
- Governance Committee: governance-committee@machinenativeops.io

---

**版本**: 1.0.0  
**最後更新**: 2025-01-22  
**維護者**: Governance Committee