# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# GL Unified Charter Activated
# 🚀 自動化工具快速開始指南

<!-- GL Layer: GL90-99 Meta-Specification Layer -->
<!-- Purpose: Quick start guide for automation tools -->

## 快速開始（3 步驟）

### 1️⃣ 初始化（僅需執行一次）

```bash
make automation-init
```

或直接執行：

```bash
bash scripts/init-automation.sh
```

這會：
- ✅ 安裝所有 Python 依賴（detect-secrets, black, ruff, mypy 等）
- ✅ 建立配置檔案（.secrets.baseline, .env.example）
- ✅ 執行初始品質檢查
- ✅ 生成初始報告

### 2️⃣ 執行品質檢查

```bash
make automation-check
```

或：

```bash
python scripts/auto-quality-check.py
```

### 3️⃣ 查看報告

```bash
make automation-report
```

或：

```bash
cat AUTO-QUALITY-REPORT.md
```

---

## 📋 所有可用命令

### Makefile 命令（推薦）

| 命令 | 說明 |
|------|------|
| `make automation-init` | 初始化自動化工具 |
| `make automation-check` | 執行品質檢查 |
| `make automation-fix` | 自動修復問題 |
| `make automation-fix-preview` | 預覽修復（不實際修改） |
| `make automation-verify` | 驗證安裝狀態 |
| `make automation-report` | 查看品質報告 |
| `make automation-help` | 顯示說明 |

### 直接執行腳本

```bash
# 初始化
bash scripts/init-automation.sh

# 品質檢查
python scripts/auto-quality-check.py

# 自動修復（預覽）
python scripts/auto-fix-issues.py --dry-run

# 自動修復（實際執行）
python scripts/auto-fix-issues.py

# 驗證狀態
bash scripts/verify-automation.sh
```

---

## 📊 生成的報告

執行後會產生以下檔案：

| 檔案 | 說明 |
|------|------|
| `AUTO-QUALITY-REPORT.md` | 人類可讀的品質報告 |
| `auto-quality-report.json` | JSON 格式的詳細報告 |
| `AUTOMATION-INIT-REPORT.md` | 初始化完成報告 |
| `.secrets.baseline` | detect-secrets 基準檔案 |
| `.env.example` | 環境變數範本 |

---

## 🔍 檢查項目

自動化工具會檢查以下 8 個項目：

1. **安全性** - 掃描硬編碼的秘密
2. **Python 型別提示** - 覆蓋率統計（目標 90%+）
3. **TypeScript 品質** - 檔案統計
4. **程式碼重複** - 檢測重複模組
5. **Docstring 覆蓋率** - 文件字串覆蓋（目標 85%+）
6. **非 ASCII 檔名** - 跨平台相容性
7. **console.log** - 檢測不當的日誌使用
8. **eval() 使用** - 安全性風險檢測

---

## 🔧 自動修復功能

`auto-fix-issues.py` 可以自動修復：

- ✅ 程式碼格式化（Black）
- ✅ Import 排序（isort）
- ✅ .gitignore 更新
- ✅ .env.example 建立

---

## 🤖 CI/CD 整合

每次 Push 或 Pull Request 時，GitHub Actions 會自動：

1. 執行安全掃描
2. 檢查 Python 品質
3. 檢查 TypeScript 品質
4. 檢測程式碼重複
5. 檢查 Docstring 覆蓋率
6. 執行測試並生成覆蓋率報告
7. 生成綜合品質報告
8. 在 PR 中發布結果

配置檔案：`.github/workflows/pr-quality-check.yml`

---

## 📖 詳細文件

- [AUTOMATION-README.md](./AUTOMATION-README.md) - 完整使用指南
- [AUTOMATION-INIT-REPORT.md](./AUTOMATION-INIT-REPORT.md) - 初始化報告
- [PR-1-REVIEW-REPORT.md](./PR-1-REVIEW-REPORT.md) - 詳細審查報告
- [PR-1-CODE-EXAMPLES.md](./PR-1-CODE-EXAMPLES.md) - 程式碼範例
- [PR-1-ACTION-PLAN.md](./PR-1-ACTION-PLAN.md) - 改進計劃

---

## 🆘 故障排除

### 問題：找不到 Python 依賴

```bash
pip install detect-secrets bandit black ruff mypy isort pytest pytest-cov interrogate pylint
```

### 問題：權限錯誤

```bash
chmod +x scripts/*.sh scripts/*.py
```

### 問題：需要重新初始化

```bash
make automation-init
```

---

## 💡 使用技巧

### 每日工作流程

```bash
# 1. 開始工作前檢查
make automation-check

# 2. 查看需要改進的地方
make automation-report

# 3. 讓工具自動修復簡單問題
make automation-fix-preview  # 先預覽
make automation-fix          # 實際執行

# 4. 手動修復其他問題
# ... 編輯程式碼 ...

# 5. 再次檢查
make automation-check
```

### 整合到 Git Hooks

在 `.git/hooks/pre-commit` 中添加：

```bash
#!/bin/bash
echo "🔍 Running quality checks..."
python scripts/auto-quality-check.py || true
python scripts/auto-fix-issues.py
```

---

## ✅ 驗證安裝

確認一切正常運作：

```bash
make automation-verify
```

應該看到所有檢查都通過：

```
✓ Python 3 已安裝
✓ detect-secrets 已安裝
✓ black 已安裝
...
✅ 所有檢查通過！自動化工具已就緒。
```

---

## 🎯 下一步

1. ✅ 執行 `make automation-init` 初始化
2. 📊 查看 `AUTO-QUALITY-REPORT.md` 了解當前品質
3. 🔧 使用 `make automation-fix` 自動修復
4. 📖 閱讀 [PR-1-ACTION-PLAN.md](./PR-1-ACTION-PLAN.md) 了解改進計劃
5. 🚀 開始改進程式碼品質！

---

**更新時間**: 2026-01-16  
**維護者**: DevOps 團隊
