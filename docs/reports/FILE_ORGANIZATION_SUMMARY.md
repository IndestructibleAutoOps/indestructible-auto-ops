# Git 專案檔案整理完整指南 - 快速參考

## 📚 相關檔案

本專案提供了完整的檔案整理工具套件：

1. **FILE_ORGANIZATION_GUIDE.md** - 詳細的理論指南和最佳實踐
2. **check_file_organization.sh** - 檢查腳本
3. **auto_organize_files.sh** - 自動整理腳本
4. **FILE_ORGANIZATION_SUMMARY.md** - 本快速參考文檔

---

## 🚀 快速開始（5 分鐘）

### 1. 確認分支
```bash
git checkout main
# 或
git switch main
```

### 2. 執行檢查
```bash
chmod +x check_file_organization.sh
./check_file_organization.sh
```

### 3. 查看結果
檢查腳本會顯示：
- 根目錄檔案數量
- 散落的檔案
- 臨時檔案
- 健康評分（0-100）

### 4. 自動整理（如需要）
```bash
chmod +x auto_organize_files.sh
./auto_organize_files.sh
```

### 5. 提交變更
```bash
git status
git add .
git commit -m "chore: reorganize project file structure"
```

---

## 📊 健康指標解釋

### 優秀（90-100分）
- ✅ 根目錄 <10 個 .md 檔案
- ✅ 根目錄 <5 個配置檔案
- ✅ 無散落檔案
- ✅ 無臨時檔案

**行動**：維持現狀，定期檢查

### 良好（70-89分）
- ⚠️ 根目錄 10-20 個 .md 檔案
- ⚠️ 根目錄 5-10 個配置檔案
- ⚠️ 少量散落檔案

**行動**：建議進行少量優化

### 需要注意（50-69分）
- ⚠️ 根目錄 >20 個 .md 檔案
- ⚠️ 根目錄 >10 個配置檔案
- ⚠️ 多個散落檔案

**行動**：建議整理部分檔案

### 需要整理（<50分）
- ❌ 大量檔案散落
- ❌ 多個臨時檔案
- ❌ 結構混亂

**行動**：立即執行整理

---

## 📁 標準目錄結構

```
.
├── README.md                    # 專案說明（根目錄）
├── CONTRIBUTING.md              # 貢獻指南（根目錄）
├── CHANGELOG.md                 # 變更日誌（根目錄）
├── docs/                        # 文檔目錄
│   ├── architecture/            # 架構文檔
│   │   └── ARCHITECTURE.md
│   ├── deployment/              # 部署文檔
│   │   └── DEPLOYMENT-GUIDE.md
│   ├── guides/                  # 使用指南
│   │   └── DEVELOPMENT-STRATEGY.md
│   ├── reports/                 # 報告和分析
│   │   ├── PROJECT-STATUS.md
│   │   └── COMPREHENSIVE-REPORT.md
│   └── analysis/                # 分析文檔
│       └── ANALYSIS-REPORT.md
├── config/                      # 配置檔案
│   ├── environments/            # 環境配置
│   │   ├── dev.yaml
│   │   ├── staging.yaml
│   │   └── prod.yaml
│   ├── governance/              # 治理規則
│   │   └── governance.yaml
│   ├── monitoring/              # 監控配置
│   │   ├── prometheus.yml
│   │   └── grafana-dashboard.json
│   └── security/                # 安全配置
│       └── security-rules.yaml
├── scripts/                     # 腳本工具
│   ├── setup/                   # 安裝腳本
│   ├── deployment/              # 部署腳本
│   └── utils/                   # 工具腳本
└── reports/                     # 報告輸出
    ├── analysis/                # 分析報告
    ├── compliance/              # 合規報告
    └── security/                # 安全報告
```

---

## 🔍 常見問題檔案類型

### 應該在根目錄
✅ `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`  
✅ `LICENSE`, `CODE_OF_CONDUCT.md`  
✅ `Makefile`, `pyproject.toml`, `package.json`  
✅ `docker-compose.yaml`, `Dockerfile`  
✅ `.gitignore`, `.env.example`

### 應該在 docs/
❌ `ARCHITECTURE.md` → `docs/architecture/`  
❌ `DEPLOYMENT-GUIDE.md` → `docs/deployment/`  
❌ `PROJECT-STATUS.md` → `docs/reports/`  
❌ `COMPREHENSIVE-ANALYSIS.md` → `docs/analysis/`

### 應該在 config/
❌ `governance.yaml` → `config/governance/`  
❌ `prometheus.yml` → `config/monitoring/`  
❌ `security-rules.yaml` → `config/security/`

### 應該清理
❌ `*.tmp`, `*.bak`, `*~`, `*.backup`  
❌ `*.swp`, `*.swo`

---

## 🛠️ 手動整理指令

### 移動單個檔案
```bash
git mv 檔案名.md 目標目錄/
```

### 批次移動架構文檔
```bash
find . -maxdepth 1 -name "*ARCHITECTURE*.md" | \
  xargs -I {} git mv {} docs/architecture/
```

### 批次移動報告
```bash
find . -maxdepth 1 -name "*report*.md" | \
  xargs -I {} git mv {} docs/reports/
```

### 清理臨時檔案
```bash
find . -name "*.tmp" -delete
find . -name "*.bak" -delete
```

---

## ⚙️ 自動化設置

### Git Hooks

創建 `.git/hooks/pre-commit`：

```bash
#!/bin/bash
# 檢查根目錄檔案數量
ROOT_MD_COUNT=$(find . -maxdepth 1 -name "*.md" | wc -l)
if [ $ROOT_MD_COUNT -gt 15 ]; then
    echo "警告：根目錄有 $ROOT_MD_COUNT 個 .md 檔案"
    echo "請考慮整理到 docs/ 目錄"
    exit 1
fi
```

賦予執行權限：
```bash
chmod +x .git/hooks/pre-commit
```

### .gitignore 更新

添加到 `.gitignore`：

```gitignore
# 臨時檔案
*.tmp
*.bak
*.backup
*~
*.swp

# 報告和日誌
reports/*.json
logs/*.log

# IDE 檔案
.vscode/
.idea/
*.sublime-*
```

---

## 📅 定期維護

### 每週檢查
```bash
./check_file_organization.sh
```

### 每月整理
```bash
./auto_organize_files.sh
git commit -m "chore: monthly file organization cleanup"
```

### 季度審查
- 檢查目錄結構是否需要調整
- 更新文檔索引
- 清理舊的報告文件

---

## 🔗 實用指令

### 查看所有文檔
```bash
find . -name "*.md" | sort
```

### 查看所有配置
```bash
find . -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" \) | sort
```

### 統計檔案數量
```bash
find . -name "*.md" | wc -l
find . -name "*.yaml" -o -name "*.yml" | wc -l
```

### 查找大檔案
```bash
find . -type f -size +1M | sort
```

### 查找最近修改的檔案
```bash
find . -name "*.md" -mtime -7
```

---

## 💡 最佳實踐

### 1. 命名規範
- 使用小寫字母和連字符：`deployment-guide.md`
- 避免空格和特殊字元
- 使用描述性名稱

### 2. 提交訊息
```bash
# 移動檔案
git mv old.md docs/new.md
git commit -m "refactor: move old.md to docs/new.md"

# 批次整理
git add .
git commit -m "chore: reorganize project structure"
```

### 3. 分支策略
```bash
# 創建整理分支
git checkout -b chore/file-organization

# 執行整理
./auto_organize_files.sh

# 提交並合併
git commit -m "chore: reorganize project structure"
git checkout main
git merge chore/file-organization
```

### 4. 團隊協作
- 在 README 中說明檔案結構
- 在 CONTRIBUTING 中說明命名規範
- 使用 PR 模板檢查檔案位置

---

## 🎯 檢查清單

### 提交前檢查
- [ ] 根目錄檔案數量合理（<15 個 .md）
- [ ] 新增檔案在正確目錄
- [ ] 沒有臨時檔案
- [ ] 沒有重複檔案
- [ ] 檔案命名符合規範
- [ ] .gitignore 已更新

### 定期檢查
- [ ] 執行檢查腳本
- [ ] 清理臨時檔案
- [ ] 更新文檔索引
- [ ] 審查目錄結構
- [ ] 更新 .gitignore

---

## 🆘 故障排除

### 問題：檔案移動後 Git 追蹤遺失
**解決方案**：使用 `git mv` 而不是 `mv`

### 問題：腳本沒有執行權限
**解決方案**：`chmod +x script_name.sh`

### 問題：檔案被忽略
**解決方案**：檢查 `.gitignore`

### 問題：提交失敗
**解決方案**：使用 `--no-verify` 繞過 hooks

---

## 📞 支援

- 詳細指南：參考 `FILE_ORGANIZATION_GUIDE.md`
- 問題報告：在 GitHub 開 Issue
- 改進建議：提交 PR

---

**文檔版本**：1.0  
**最後更新**：2024-02-08  
**維護者**：專案團隊