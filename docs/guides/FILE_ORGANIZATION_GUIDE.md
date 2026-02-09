# Git 專案檔案整理檢查指南

## 📋 目錄
1. [執行步驟](#執行步驟)
2. [檔案分類標準](#檔案分類標準)
3. [檢查指令](#檢查指令)
4. [識別問題檔案](#識別問題檔案)
5. [整理方法](#整理方法)
6. [防範措施](#防範措施)

---

## 🚀 執行步驟

### 步驟 1：確認分支狀態
```bash
# 查看當前分支
git branch --show-current

# 如果不在 main 分支，切換過去
git checkout main
# 或
git switch main
```

### 步驟 2：列出所有檔案位置
```bash
# 列出專案中所有文檔和配置檔案（排除 .git 和 node_modules）
find . -type f \( -name "*.md" -o -name "*.txt" -o -name "*.yaml" -o -name "*.yml" \
  -o -name "*.json" -o -name "*.toml" -o -name "*.cfg" -o -name "*.ini" -o -name "*.conf" \
  -o -name "*.sh" -o -name "Makefile" -o -name "*.mk" \) \
  ! -path "./.git/*" ! -path "*/node_modules/*" | sort

# 保存檔案清單到檔案
find . -type f \( -name "*.md" -o -name "*.txt" -o -name "*.yaml" -o -name "*.yml" \
  -o -name "*.json" -o -name "*.toml" -o -name "*.cfg" -o -name "*.ini" -o -name "*.conf" \
  -o -name "*.sh" -o -name "Makefile" -o -name "*.mk" \) \
  ! -path "./.git/*" ! -path "*/node_modules/*" | sort > file_inventory.txt
```

### 步驟 3：檢查根目錄檔案
```bash
# 查看根目錄的文檔和配置檔案
find . -maxdepth 1 -type f \( -name "*.md" -o -name "*.txt" -o -name "*.yaml" -o -name "*.yml" \
  -o -name "*.json" -o -name "*.toml" -o -name "*.cfg" -o -name "*.ini" -o -name "*.conf" \) | sort

# 統計根目錄檔案數量
find . -maxdepth 1 -type f \( -name "*.md" -o -name "*.txt" -o -name "*.yaml" -o -name "*.yml" \
  -o -name "*.json" -o -name "*.toml" -o -name "*.cfg" -o -name "*.ini" -o -name "*.conf" \) | wc -l
```

---

## 📁 檔案分類標準

### ✅ 應該在根目錄的檔案
**核心配置檔案：**
- `README.md` - 專案說明
- `CHANGELOG.md` - 變更日誌
- `CONTRIBUTING.md` - 貢獻指南
- `LICENSE` - 授權檔案
- `.gitignore` - Git 忽略規則
- `Makefile` - Make 構建檔案
- `pyproject.toml` - Python 專案配置
- `package.json` - Node.js 專案配置
- `go.mod` - Go 專案配置
- `requirements.txt` - Python 依賴
- `docker-compose.yaml` - Docker 編排
- `Dockerfile` - Docker 映像定義
- `.env.example` - 環境變數範本

**核心文檔：**
- `ARCHITECTURE.md` - 架構文檔
- `DEPLOYMENT-GUIDE.md` - 部署指南
- `DEVELOPMENT-STRATEGY.md` - 開發策略
- `PROJECT-STATUS.md` - 專案狀態

### 📂 應該集中管理的檔案類型

#### 1. 文檔檔案（*.md）
**應存放位置：** `docs/` 或 `.github/docs/`
```bash
# 檢查散落的文檔
find . -name "*.md" ! -path "./docs/*" ! -path "./.github/*" ! -path "./README.md" \
  ! -path "./.git/*" ! -path "*/node_modules/*"
```

**文檔分類建議：**
- `docs/architecture/` - 架構設計
- `docs/guides/` - 使用指南
- `docs/api/` - API 文檔
- `docs/troubleshooting/` - 疑難排解
- `docs/reports/` - 報告和分析
- `.github/docs/` - GitHub 相關文檔

#### 2. 配置檔案（*.yaml, *.yml, *.json, *.toml）
**應存放位置：** `config/` 或 `.config/`
```bash
# 檢查散落的配置檔案
find . -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" \) \
  ! -path "./config/*" ! -path "./.config/*" ! -path "./.github/*" \
  ! -path "*/node_modules/*" ! -path "./.git/*" | sort
```

**配置分類建議：**
- `config/environments/` - 環境配置
- `config/governance/` - 治理規則
- `config/monitoring/` - 監控配置
- `config/deployment/` - 部署配置
- `config/security/` - 安全配置

#### 3. 腳本檔案（*.sh）
**應存放位置：** `scripts/` 或 `.github/scripts/`
```bash
# 檢查散落的腳本
find . -name "*.sh" ! -path "./scripts/*" ! -path "./.github/*" \
  ! -path "./.git/*" ! -path "*/node_modules/*"
```

#### 4. 報告和分析檔案
**應存放位置：** `reports/`, `analysis/`, 或 `.github/reports/`
```bash
# 檢查散落的報告
find . -type f \( -name "*report*.md" -o -name "*report*.json" -o -name "*analysis*.md" -o -name "*summary*.md" \) \
  ! -path "./reports/*" ! -path "./.github/*" ! -path "./docs/*" \
  ! -path "./.git/*" ! -path "*/node_modules/*"
```

#### 5. 測試相關檔案
**應存放位置：** `tests/`
```bash
# 檢查散落的測試檔案
find . -name "*test*.md" -o -name "*test*.json" ! -path "./tests/*" \
  ! -path "./.git/*" ! -path "*/node_modules/*"
```

---

## 🔍 檢查指令

### 綜合檢查腳本
```bash
#!/bin/bash
# 檔案整理檢查腳本

echo "=== Git 專案檔案整理檢查 ==="
echo ""

# 1. 根目錄檔案檢查
echo "【1】根目錄檔案檢查："
echo "   .md 檔案："
find . -maxdepth 1 -name "*.md" | sort
echo "   配置檔案："
find . -maxdepth 1 -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" \) | sort
echo "   腳本檔案："
find . -maxdepth 1 -name "*.sh" -o -name "Makefile" | sort
echo ""

# 2. 散落的文檔
echo "【2】散落在根目錄以外的文檔："
find . -name "*.md" ! -path "./docs/*" ! -path "./.github/*" \
  ! -path "./README.md" ! -path "./.git/*" ! -path "*/node_modules/*" | sort
echo ""

# 3. 散落的配置檔案
echo "【3】散落在根目錄和標準目錄以外的配置檔案："
find . -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" \) \
  ! -path "./config/*" ! -path "./.config/*" ! -path "./.github/*" \
  ! -path "./.git/*" ! -path "*/node_modules/*" ! -path "./enterprise-governance/*" | sort
echo ""

# 4. 散落的腳本
echo "【4】散落在標準目錄以外的腳本："
find . -name "*.sh" ! -path "./scripts/*" ! -path "./.github/*" \
  ! -path "./.git/*" ! -path "*/node_modules/*" | sort
echo ""

# 5. 報告檔案
echo "【5】散落的報告檔案："
find . -type f \( -name "*report*.md" -o -name "*report*.json" -o -name "*summary*.md" \) \
  ! -path "./reports/*" ! -path "./.github/*" ! -path "./docs/*" \
  ! -path "./.git/*" ! -path "*/node_modules/*" | sort
echo ""

# 6. 統計摘要
echo "【6】統計摘要："
echo "   根目錄 .md 檔案數量：$(find . -maxdepth 1 -name "*.md" | wc -l)"
echo "   根目錄配置檔案數量：$(find . -maxdepth 1 -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" \) | wc -l)"
echo "   散落的 .md 檔案：$(find . -name "*.md" ! -path "./docs/*" ! -path "./.github/*" ! -path "./README.md" ! -path "./.git/*" ! -path "*/node_modules/*" | wc -l)"
echo "   散落的配置檔案：$(find . -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" \) ! -path "./config/*" ! -path "./.config/*" ! -path "./.github/*" ! -path "./.git/*" ! -path "*/node_modules/*" ! -path "./enterprise-governance/*" | wc -l)"
echo ""

echo "=== 檢查完成 ==="
```

### 執行檢查腳本
```bash
# 儲存腳本
cat > check_file_organization.sh << 'EOF'
#!/bin/bash
# (上面的腳本內容)
EOF

# 賦予執行權限
chmod +x check_file_organization.sh

# 執行檢查
./check_file_organization.sh
```

---

## ⚠️ 識別問題檔案

### 問題檔案識別規則

#### 1. 根目錄過多檔案
```bash
# 如果根目錄有超過 10 個 .md 檔案，可能需要整理
ROOT_MD_COUNT=$(find . -maxdepth 1 -name "*.md" | wc -l)
if [ $ROOT_MD_COUNT -gt 10 ]; then
    echo "警告：根目錄有 $ROOT_MD_COUNT 個 .md 檔案，建議整理到 docs/ 目錄"
fi
```

#### 2. 重複的配置檔案
```bash
# 檢查重複的檔案名稱
find . -name "*.yaml" -o -name "*.yml" -o -name "*.json" | \
  sed 's|.*/||' | sort | uniq -d
```

#### 3. 臨時檔案
```bash
# 檢查臨時或備份檔案
find . -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*~" -o -name "*.backup" \) \
  ! -path "./.git/*" ! -path "*/node_modules/*"
```

#### 4. 不符合命名規範的檔案
```bash
# 檢查包含空格或特殊字元的檔案名稱
find . -name "* *" -o -name "*\:*" -o -name "*\?*" -o -name "*\**" \
  ! -path "./.git/*" ! -path "*/node_modules/*"
```

---

## 🛠️ 整理方法

### 方法 1：使用 Git mv（推薦）
```bash
# 移動文檔
git mv 文件名.md docs/architecture/文件名.md

# 移動配置
git mv 配置.yaml config/environments/配置.yaml

# 批次移動
find . -maxdepth 1 -name "*report*.md" -exec git mv {} docs/reports/ \;
```

### 方法 2：建立目錄結構後移動
```bash
# 1. 建立目錄結構
mkdir -p docs/{architecture,guides,api,troubleshooting,reports}
mkdir -p config/{environments,governance,monitoring,deployment,security}
mkdir -p scripts/{setup,deployment,maintenance}
mkdir -p reports/{analysis,compliance,security,performance}
mkdir -p .github/{docs,reports,scripts}

# 2. 移動檔案
# 移動架構文檔
git mv ARCHITECTURE.md docs/architecture/
git mv *ARCHITECTURE*.md docs/architecture/
git mv *DEPLOYMENT*.md docs/deployment/

# 移動報告
git mv *report*.md docs/reports/
git mv *summary*.md docs/reports/
git mv *analysis*.md docs/reports/analysis/

# 移動配置
git mv *.yaml config/environments/
git mv *.json config/
git mv governance.yaml config/governance/

# 移動腳本
git mv *.sh scripts/
```

### 方法 3：自動整理腳本
```bash
#!/bin/bash
# 自動整理腳本

echo "開始整理檔案..."

# 建立目錄結構
mkdir -p docs/{architecture,guides,api,troubleshooting,reports,analysis}
mkdir -p config/{environments,governance,monitoring,deployment,security}
mkdir -p scripts/{setup,deployment,maintenance}
mkdir -p reports/{analysis,compliance,security,performance}
mkdir -p .github/{docs,reports,scripts}

# 移動架構相關文檔
for file in ARCHITECTURE*.md *ARCHITECTURE*.md; do
    if [ -f "$file" ]; then
        git mv "$file" docs/architecture/
    fi
done

# 移動部署相關文檔
for file in DEPLOYMENT*.md *DEPLOYMENT*.md; do
    if [ -f "$file" ]; then
        git mv "$file" docs/deployment/
    fi
done

# 移動報告相關文檔
for file in *report*.md *summary*.md *analysis*.md; do
    if [ -f "$file" ]; then
        git mv "$file" docs/reports/
    fi
done

# 移動指南相關文檔
for file in *GUIDE*.md *guide*.md; do
    if [ -f "$file" ]; then
        git mv "$file" docs/guides/
    fi
done

# 移動配置檔案
for file in *.yaml *.yml; do
    if [ -f "$file" ] && [ "$file" != "docker-compose.yaml" ]; then
        git mv "$file" config/
    fi
done

echo "整理完成！"
echo "請檢查變更並提交："
echo "  git status"
echo "  git commit -m 'chore: reorganize project structure'"
```

### 方法 4：使用 find 和 xargs 批次處理
```bash
# 移動所有根目錄的報告文檔
find . -maxdepth 1 -name "*report*.md" | xargs -I {} git mv {} docs/reports/

# 移動所有根目錄的架構文檔
find . -maxdepth 1 -name "*architecture*.md" -o -name "*ARCHITECTURE*.md" | \
  xargs -I {} git mv {} docs/architecture/

# 移動所有根目錄的 JSON 配置（除了 pyproject.json）
find . -maxdepth 1 -name "*.json" ! -name "pyproject*.json" | \
  xargs -I {} git mv {} config/
```

---

## 🛡️ 防範措施

### 1. 更新 .gitignore
```bash
# 添加到 .gitignore
# 臨時檔案
*.tmp
*.bak
*.backup
*~
*.swp

# 報告和日誌
reports/*.json
logs/*.log
*.log

# IDE 檔案
.vscode/
.idea/
*.sublime-*
```

### 2. 設置 Git Hooks
```bash
#!/bin/bash
# .git/hooks/pre-commit

# 檢查根目錄是否有多餘的檔案
ROOT_MD_COUNT=$(find . -maxdepth 1 -name "*.md" | wc -l)
if [ $ROOT_MD_COUNT -gt 15 ]; then
    echo "警告：根目錄有 $ROOT_MD_COUNT 個 .md 檔案"
    echo "請考慮將部分文檔移到 docs/ 目錄"
    echo "若確認要提交，請使用 --no-verify 繞過檢查"
    exit 1
fi

# 檢查臨時檔案
if find . -name "*.tmp" -o -name "*.bak" | grep -q .; then
    echo "警告：發現臨時檔案 (*.tmp, *.bak)"
    echo "請清理後再提交"
    exit 1
fi
```

### 3. 建立 README 指導原則
在專案根目錄的 README.md 中添加檔案組織說明：
```markdown
## 專案結構

```
.
├── README.md                 # 專案說明
├── CONTRIBUTING.md           # 貢獻指南
├── CHANGELOG.md              # 變更日誌
├── docs/                     # 文檔目錄
│   ├── architecture/         # 架構文檔
│   ├── guides/               # 使用指南
│   ├── reports/              # 報告和分析
│   └── api/                  # API 文檔
├── config/                   # 配置檔案
│   ├── environments/         # 環境配置
│   ├── governance/           # 治理規則
│   └── monitoring/           # 監控配置
├── scripts/                  # 腳本工具
│   ├── setup/                # 安裝腳本
│   ├── deployment/           # 部署腳本
│   └── maintenance/          # 維護腳本
└── reports/                  # 報告和輸出
    ├── analysis/             # 分析報告
    ├── compliance/           # 合規報告
    └── security/             # 安全報告
```

## 檔案組織原則

1. **根目錄保持簡潔**：只保留核心配置和說明檔案
2. **文檔集中管理**：所有文檔放在 `docs/` 目錄
3. **配置檔案分類**：按功能和環境分類配置
4. **腳本工具化**：所有腳本放在 `scripts/` 目錄
5. **報告定期清理**：舊報告歸檔或刪除

## 貢獻前檢查

在提交 PR 前，請確保：
- [ ] 根目錄檔案數量合理（<15 個 .md 檔案）
- [ ] 新增檔案已放在正確的目錄
- [ ] 沒有臨時檔案或備份檔案
- [ ] 檔案命名符合規範（使用連字符，不用空格）
```

### 4. 定期維護腳本
```bash
#!/bin/bash
# 定期維護腳本（每周或每月執行）

echo "執行專案維護..."

# 1. 清理臨時檔案
find . -name "*.tmp" -delete
find . -name "*.bak" -delete
find . -name "*~" -delete

# 2. 檢查重複檔案
echo "檢查重複檔案..."
find . -name "*.md" | sed 's|.*/||' | sort | uniq -d > duplicate_files.txt

# 3. 更新文檔索引
echo "更新文檔索引..."
find docs/ -name "*.md" | sort > docs/INDEX.md

# 4. 生成檔案清單
echo "生成檔案清單..."
find . -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.json" \) \
  ! -path "./.git/*" ! -path "*/node_modules/*" | sort > file_inventory.txt

echo "維護完成！"
```

### 5. 文件命名規範
建立文件命名規範文檔：

```markdown
# 文件命名規範

## Markdown 文件
- 使用小寫字母和連字符：`deployment-guide.md`
- 避免使用空格和特殊字元
- 使用描述性名稱：`api-authentication.md` 而非 `doc1.md`

## 配置文件
- 環境配置：`dev.yaml`, `staging.yaml`, `prod.yaml`
- 功能配置：`monitoring.yaml`, `security.yaml`
- 版本控制：添加版本號：`api-v2.yaml`

## 腳本文件
- 使用小寫字母和連字符：`deploy.sh`, `setup.sh`
- 添加版本號：`migrate-v1.0.0.sh`
```

---

## 📊 檢查結果判讀

### 健康指標
```bash
# 理想狀態
- 根目錄 .md 檔案：<10 個
- 根目錄配置檔案：<5 個
- 散落的文檔：0 個
- 散落的配置：0 個
- 臨時檔案：0 個
- 重複檔案：0 個
```

### 警告指標
```bash
# 需要注意
- 根目錄 .md 檔案：10-20 個
- 根目錄配置檔案：5-10 個
- 散落的文檔：1-10 個
- 臨時檔案：1-5 個
```

### 危險指標
```bash
# 需要立即整理
- 根目錄 .md 檔案：>20 個
- 根目錄配置檔案：>10 個
- 散落的文檔：>10 個
- 臨時檔案：>5 個
- 發現重複檔案
```

---

## 🎯 快速檢查清單

```bash
# 一鍵檢查所有指標
echo "=== 專案檔案健康檢查 ==="
echo ""

ROOT_MD=$(find . -maxdepth 1 -name "*.md" | wc -l)
ROOT_CONFIG=$(find . -maxdepth 1 -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" \) | wc -l)
SCATTERED_MD=$(find . -name "*.md" ! -path "./docs/*" ! -path "./.github/*" ! -path "./README.md" ! -path "./.git/*" ! -path "*/node_modules/*" | wc -l)
SCATTERED_CONFIG=$(find . -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" \) ! -path "./config/*" ! -path "./.config/*" ! -path "./.github/*" ! -path "./.git/*" ! -path "*/node_modules/*" ! -path "./enterprise-governance/*" | wc -l)
TEMP_FILES=$(find . -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*~" \) ! -path "./.git/*" ! -path "*/node_modules/*" | wc -l)

echo "根目錄 .md 檔案：$ROOT_MD"
echo "根目錄配置檔案：$ROOT_CONFIG"
echo "散落的文檔：$SCATTERED_MD"
echo "散落的配置：$SCATTERED_CONFIG"
echo "臨時檔案：$TEMP_FILES"
echo ""

# 評估健康狀態
SCORE=0
[ $ROOT_MD -lt 10 ] && ((SCORE+=25))
[ $ROOT_CONFIG -lt 5 ] && ((SCORE+=25))
[ $SCATTERED_MD -lt 5 ] && ((SCORE+=25))
[ $TEMP_FILES -eq 0 ] && ((SCORE+=25))

echo "專案健康分數：$SCORE/100"
if [ $SCORE -ge 90 ]; then
    echo "狀態：✅ 優秀"
elif [ $SCORE -ge 70 ]; then
    echo "狀態：⚠️ 良好，建議優化"
else
    echo "狀態：❌ 需要整理"
fi

echo "=== 檢查完成 ==="
```

---

## 💡 最佳實踐建議

1. **定期檢查**：每周或每月執行一次檔案整理檢查
2. **持續維護**：每次新增檔案時，確保放在正確位置
3. **文檔化**：記錄檔案組織結構和命名規範
4. **自動化**：使用 Git Hooks 自動檢查
5. **團隊協作**：確保團隊成員了解並遵守規範
6. **版本控制**：使用 Git mv 而不是 mv，保留歷史記錄
7. **備份**：在整理前創建分支備份

---

## 🔗 相關資源

- [Git 官方文檔](https://git-scm.com/doc)
- [專案結構最佳實踐](https://github.com/goldbergyoni/nodebestpractices)
- [檔案命名規範](https://github.com/airbnb/javascript)

---

**文檔版本：** 1.0  
**最後更新：** 2024-02-08  
**維護者：** 專案團隊