#!/bin/bash
#
# 自動檔案整理腳本
# 自動將散落的檔案移動到適當的目錄
#

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 計數器
MOVED_MD=0
MOVED_CONFIG=0
MOVED_REPORT=0
MOVED_GUIDE=0
MOVED_ARCHITECTURE=0
MOVED_SCRIPT=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}自動檔案整理${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 檢查是否在 Git 倉庫中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}錯誤：不在 Git 倉庫中${NC}"
    exit 1
fi

# 檢查是否有未提交的更改
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}警告：工作目錄有未提交的更改${NC}"
    read -p "是否繼續？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "取消操作"
        exit 0
    fi
fi

echo -e "${BLUE}步驟 1：建立目錄結構${NC}"
echo ""

# 建立目錄結構
mkdir -p docs/{architecture,deployment,guides,api,troubleshooting,reports,analysis}
mkdir -p config/{environments,governance,monitoring,deployment,security,infrastructure}
mkdir -p scripts/{setup,deployment,maintenance,utils}
mkdir -p reports/{analysis,compliance,security,performance,testing}
mkdir -p .github/{docs,reports,scripts,config}

echo -e "${GREEN}✓${NC} 目錄結構已建立"
echo ""

echo -e "${BLUE}步驟 2：整理根目錄文檔${NC}"
echo ""

# 移動架構相關文檔
for file in ARCHITECTURE*.md *ARCHITECTURE*.md *architecture*.md; do
    if [ -f "$file" ] && [ "$file" != "ARCHITECTURE.md" ]; then
        echo "   移動 $file -> docs/architecture/"
        git mv "$file" docs/architecture/ 2>/dev/null || mv "$file" docs/architecture/
        ((++MOVED_ARCHITECTURE))
    fi
done

# 移動部署相關文檔
for file in DEPLOYMENT*.md *DEPLOYMENT*.md *deployment*.md; do
    if [ -f "$file" ] && [ "$file" != "DEPLOYMENT-GUIDE.md" ]; then
        echo "   移動 $file -> docs/deployment/"
        git mv "$file" docs/deployment/ 2>/dev/null || mv "$file" docs/deployment/
        ((++MOVED_GUIDE))
    fi
done

# 移動指南相關文檔
for file in *GUIDE*.md *guide*.md *Guide*.md; do
    if [ -f "$file" ]; then
        echo "   移動 $file -> docs/guides/"
        git mv "$file" docs/guides/ 2>/dev/null || mv "$file" docs/guides/
        ((++MOVED_GUIDE))
    fi
done

# 移動報告和摘要
for file in *report*.md *summary*.md *Report*.md *Summary*.md *REPORT*.md *SUMMARY*.md; do
    if [ -f "$file" ]; then
        echo "   移動 $file -> docs/reports/"
        git mv "$file" docs/reports/ 2>/dev/null || mv "$file" docs/reports/
        ((++MOVED_REPORT))
    fi
done

# 移動分析文檔
for file in *analysis*.md *Analysis*.md *ANALYSIS*.md; do
    if [ -f "$file" ]; then
        echo "   移動 $file -> docs/analysis/"
        git mv "$file" docs/analysis/ 2>/dev/null || mv "$file" docs/analysis/
        ((++MOVED_REPORT))
    fi
done

echo -e "${GREEN}✓${NC} 文檔整理完成"
echo ""

echo -e "${BLUE}步驟 3：整理配置檔案${NC}"
echo ""

# 移動 YAML 配置（保留核心配置在根目錄）
for file in *.yaml *.yml; do
    if [ -f "$file" ]; then
        # 保留核心配置在根目錄
        if [[ "$file" =~ ^(docker-compose|Makefile|\.gitignore|README|CHANGELOG|CONTRIBUTING|CODE-OF-CONDUCT|LICENSE) ]]; then
            continue
        fi
        
        # 根據檔案名稱分類
        if [[ "$file" =~ (governance|GL|governance|policy|rule) ]]; then
            echo "   移動 $file -> config/governance/"
            git mv "$file" config/governance/ 2>/dev/null || mv "$file" config/governance/
        elif [[ "$file" =~ (monitoring|prometheus|grafana|alert|metric) ]]; then
            echo "   移動 $file -> config/monitoring/"
            git mv "$file" config/monitoring/ 2>/dev/null || mv "$file" config/monitoring/
        elif [[ "$file" =~ (security|auth|rbac|permission) ]]; then
            echo "   移動 $file -> config/security/"
            git mv "$file" config/security/ 2>/dev/null || mv "$file" config/security/
        elif [[ "$file" =~ (deploy|deployment|k8s|kubernetes|helm) ]]; then
            echo "   移動 $file -> config/deployment/"
            git mv "$file" config/deployment/ 2>/dev/null || mv "$file" config/deployment/
        else
            echo "   移動 $file -> config/environments/"
            git mv "$file" config/environments/ 2>/dev/null || mv "$file" config/environments/
        fi
        ((++MOVED_CONFIG))
    fi
done

# 移動 JSON 配置
for file in *.json; do
    if [ -f "$file" ]; then
        # 保留核心配置在根目錄
        if [[ "$file" =~ ^(package|pyproject) ]]; then
            continue
        fi
        
        echo "   移動 $file -> config/"
        git mv "$file" config/ 2>/dev/null || mv "$file" config/
        ((++MOVED_CONFIG))
    fi
done

echo -e "${GREEN}✓${NC} 配置檔案整理完成"
echo ""

echo -e "${BLUE}步驟 4：整理腳本檔案${NC}"
echo ""

# 移動腳本檔案
for file in *.sh; do
    if [ -f "$file" ]; then
        echo "   移動 $file -> scripts/utils/"
        git mv "$file" scripts/utils/ 2>/dev/null || mv "$file" scripts/utils/
        ((++MOVED_SCRIPT))
    fi
done

echo -e "${GREEN}✓${NC} 腳本檔案整理完成"
echo ""

echo -e "${BLUE}步驟 5：清理臨時檔案${NC}"
echo ""

# 清理臨時檔案
TEMP_FILES=$(find . -maxdepth 2 -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*~" -o -name "*.backup" -o -name "*.swp" \) ! -path "./.git/*" 2>/dev/null)

if [ -n "$TEMP_FILES" ]; then
    echo "   發現臨時檔案，正在刪除..."
    echo "$TEMP_FILES" | xargs rm -f
    echo -e "${GREEN}✓${NC} 臨時檔案已清理"
else
    echo -e "${GREEN}✓${NC} 沒有發現臨時檔案"
fi
echo ""

echo -e "${BLUE}步驟 6：更新索引檔案${NC}"
echo ""

# 創建或更新文檔索引
cat > docs/INDEX.md << EOF
# 文檔索引

本目錄包含所有專案文檔。

## 架構文檔
- [架構文檔目錄](architecture/)

## 部署文檔
- [部署文檔目錄](deployment/)

## 使用指南
- [指南文檔目錄](guides/)

## 報告
- [專案報告目錄](reports/)

## 分析
- [分析文檔目錄](analysis/)

---
最後更新：$(date +%Y-%m-%d)
EOF

echo -e "${GREEN}✓${NC} 文檔索引已更新"
echo ""

# 顯示摘要
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}整理摘要${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "   移動的架構文檔:      $MOVED_ARCHITECTURE"
echo "   移動的指南文檔:      $MOVED_GUIDE"
echo "   移動的報告文檔:      $MOVED_REPORT"
echo "   移動的配置檔案:      $MOVED_CONFIG"
echo "   移動的腳本檔案:      $MOVED_SCRIPT"
echo "   總共移動檔案:        $((MOVED_ARCHITECTURE + MOVED_GUIDE + MOVED_REPORT + MOVED_CONFIG + MOVED_SCRIPT))"
echo ""

echo -e "${BLUE}下一步操作：${NC}"
echo ""
echo "   1. 檢查移動的檔案："
echo "      git status"
echo ""
echo "   2. 查看變更："
echo "      git diff --cached"
echo ""
echo "   3. 提交變更："
echo "      git commit -m 'chore: reorganize project file structure'"
echo ""
echo "   4. 驗證整理結果："
echo "      ./scripts/utils/check_file_organization.sh"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}整理完成！${NC}"
echo -e "${BLUE}========================================${NC}"
