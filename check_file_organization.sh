#!/bin/bash
#
# Git 專案檔案整理檢查腳本
# 用於檢查專案中檔案的組織結構
#

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Git 專案檔案整理檢查${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 統計變數
ROOT_MD_COUNT=0
ROOT_CONFIG_COUNT=0
SCATTERED_MD_COUNT=0
SCATTERED_CONFIG_COUNT=0
TEMP_FILES_COUNT=0
DUPLICATE_FILES_COUNT=0

# 1. 檢查當前分支
echo -e "${BLUE}【1】當前分支狀態${NC}"
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "   當前分支: $CURRENT_BRANCH"
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
    echo -e "   ${GREEN}✓${NC} 在主分支上"
else
    echo -e "   ${YELLOW}⚠${NC}  不在主分支上 (當前: $CURRENT_BRANCH)"
fi
echo ""

# 2. 根目錄檔案檢查
echo -e "${BLUE}【2】根目錄檔案檢查${NC}"

# 統計根目錄的 .md 檔案
ROOT_MD_FILES=$(find . -maxdepth 1 -name "*.md" 2>/dev/null | sort)
ROOT_MD_COUNT=$(echo "$ROOT_MD_FILES" | grep -c "md" || echo 0)

if [ $ROOT_MD_COUNT -gt 0 ]; then
    echo "   .md 檔案 ($ROOT_MD_COUNT 個):"
    echo "$ROOT_MD_FILES" | sed 's|^./|      |'
    
    # 識別應該移動的檔案
    echo ""
    echo "   ${YELLOW}建議移動到 docs/ 的檔案:${NC}"
    for file in $(find . -maxdepth 1 -name "*report*.md" -o -name "*summary*.md" -o -name "*analysis*.md" -o -name "*ARCHITECTURE*.md" -o -name "*DEPLOYMENT*.md" 2>/dev/null); do
        if [ -f "$file" ]; then
            echo "      - $file"
        fi
    done
else
    echo "   ${GREEN}✓${NC} 根目錄沒有 .md 檔案"
fi
echo ""

# 統計根目錄的配置檔案
ROOT_CONFIG_FILES=$(find . -maxdepth 1 -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" -o -name "*.cfg" -o -name "*.ini" \) 2>/dev/null | sort)
ROOT_CONFIG_COUNT=$(echo "$ROOT_CONFIG_FILES" | grep -c "yaml\|yml\|json\|toml" || echo 0)

if [ $ROOT_CONFIG_COUNT -gt 0 ]; then
    echo "   配置檔案 ($ROOT_CONFIG_COUNT 個):"
    echo "$ROOT_CONFIG_FILES" | sed 's|^./|      |'
else
    echo "   ${GREEN}✓${NC} 根目錄沒有配置檔案"
fi
echo ""

# 3. 散落的文檔檢查
echo -e "${BLUE}【3】散落的文檔檢查${NC}"

SCATTERED_MD=$(find . -name "*.md" ! -path "./docs/*" ! -path "./.github/*" ! -path "./.git/*" ! -path "*/node_modules/*" ! -path "./README.md" ! -path "./enterprise-governance/*" 2>/dev/null | sort)
SCATTERED_MD_COUNT=$(echo "$SCATTERED_MD" | grep -c "md" || echo 0)

if [ $SCATTERED_MD_COUNT -gt 0 ]; then
    echo "   發現 $SCATTERED_MD_COUNT 個散落的文檔:"
    echo "$SCATTERED_MD" | head -20 | sed 's|^./|      |'
    if [ $SCATTERED_MD_COUNT -gt 20 ]; then
        echo "      ... 還有 $((SCATTERED_MD_COUNT - 20)) 個"
    fi
else
    echo "   ${GREEN}✓${NC} 沒有散落的文檔"
fi
echo ""

# 4. 散落的配置檔案檢查
echo -e "${BLUE}【4】散落的配置檔案檢查${NC}"

SCATTERED_CONFIG=$(find . -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" \) ! -path "./config/*" ! -path "./.config/*" ! -path "./.github/*" ! -path "./.git/*" ! -path "*/node_modules/*" ! -path "./enterprise-governance/*" 2>/dev/null | sort)
SCATTERED_CONFIG_COUNT=$(echo "$SCATTERED_CONFIG" | grep -c "yaml\|yml\|json\|toml" || echo 0)

if [ $SCATTERED_CONFIG_COUNT -gt 0 ]; then
    echo "   發現 $SCATTERED_CONFIG_COUNT 個散落的配置檔案:"
    echo "$SCATTERED_CONFIG" | head -20 | sed 's|^./|      |'
    if [ $SCATTERED_CONFIG_COUNT -gt 20 ]; then
        echo "      ... 還有 $((SCATTERED_CONFIG_COUNT - 20)) 個"
    fi
else
    echo "   ${GREEN}✓${NC} 沒有散落的配置檔案"
fi
echo ""

# 5. 臨時檔案檢查
echo -e "${BLUE}【5】臨時和備份檔案檢查${NC}"

TEMP_FILES=$(find . -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*~" -o -name "*.backup" -o -name "*.swp" \) ! -path "./.git/*" ! -path "*/node_modules/*" 2>/dev/null)
TEMP_FILES_COUNT=$(echo "$TEMP_FILES" | grep -c "." || echo 0)

if [ $TEMP_FILES_COUNT -gt 0 ]; then
    echo "   發現 $TEMP_FILES_COUNT 個臨時/備份檔案:"
    echo "$TEMP_FILES" | sed 's|^./|      |'
    echo "   ${YELLOW}⚠${NC}  建議清理這些檔案"
else
    echo "   ${GREEN}✓${NC} 沒有臨時/備份檔案"
fi
echo ""

# 6. 重複檔案檢查
echo -e "${BLUE}【6】重複檔案檢查${NC}"

DUPLICATE_FILENAMES=$(find . -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" -o -name "*.md" \) ! -path "./.git/*" ! -path "*/node_modules/*" 2>/dev/null | sed 's|.*/||' | sort | uniq -d)

if [ -n "$DUPLICATE_FILENAMES" ]; then
    echo "   發現重複的檔案名稱:"
    echo "$DUPLICATE_FILENAMES" | sed 's|^|      |'
    DUPLICATE_FILES_COUNT=$(echo "$DUPLICATE_FILENAMES" | wc -l)
else
    echo "   ${GREEN}✓${NC} 沒有重複的檔案名稱"
fi
echo ""

# 7. 統計摘要
echo -e "${BLUE}【7】統計摘要${NC}"
echo ""
echo "   根目錄 .md 檔案數量:     $ROOT_MD_COUNT"
echo "   根目錄配置檔案數量:       $ROOT_CONFIG_COUNT"
echo "   散落的文檔數量:          $SCATTERED_MD_COUNT"
echo "   散落的配置檔案數量:      $SCATTERED_CONFIG_COUNT"
echo "   臨時/備份檔案數量:       $TEMP_FILES_COUNT"
echo "   重複檔案名稱數量:         $DUPLICATE_FILES_COUNT"
echo ""

# 8. 健康評估
echo -e "${BLUE}【8】專案健康評估${NC}"
echo ""

# 計算健康分數
SCORE=0
MAX_SCORE=100

# 根目錄 .md 檔案評分
if [ $ROOT_MD_COUNT -lt 10 ]; then
    SCORE=$((SCORE + 25))
    echo "   ${GREEN}✓${NC} 根目錄 .md 檔案數量優秀 ($ROOT_MD_COUNT)"
elif [ $ROOT_MD_COUNT -lt 20 ]; then
    SCORE=$((SCORE + 15))
    echo "   ${YELLOW}⚠${NC}  根目錄 .md 檔案數量可接受 ($ROOT_MD_COUNT)"
else
    echo "   ${RED}✗${NC} 根目錄 .md 檔案數量過多 ($ROOT_MD_COUNT)"
fi

# 根目錄配置檔案評分
if [ $ROOT_CONFIG_COUNT -lt 5 ]; then
    SCORE=$((SCORE + 25))
    echo "   ${GREEN}✓${NC} 根目錄配置檔案數量優秀 ($ROOT_CONFIG_COUNT)"
elif [ $ROOT_CONFIG_COUNT -lt 10 ]; then
    SCORE=$((SCORE + 15))
    echo "   ${YELLOW}⚠${NC}  根目錄配置檔案數量可接受 ($ROOT_CONFIG_COUNT)"
else
    echo "   ${RED}✗${NC} 根目錄配置檔案數量過多 ($ROOT_CONFIG_COUNT)"
fi

# 散落檔案評分
if [ $SCATTERED_MD_COUNT -lt 5 ] && [ $SCATTERED_CONFIG_COUNT -lt 5 ]; then
    SCORE=$((SCORE + 25))
    echo "   ${GREEN}✓${NC} 散落檔案數量優秀"
elif [ $SCATTERED_MD_COUNT -lt 10 ] && [ $SCATTERED_CONFIG_COUNT -lt 10 ]; then
    SCORE=$((SCORE + 15))
    echo "   ${YELLOW}⚠${NC}  散落檔案數量可接受"
else
    echo "   ${RED}✗${NC} 散落檔案數量過多"
fi

# 臨時檔案評分
if [ $TEMP_FILES_COUNT -eq 0 ]; then
    SCORE=$((SCORE + 25))
    echo "   ${GREEN}✓${NC} 沒有臨時/備份檔案"
else
    echo "   ${RED}✗${NC} 發現臨時/備份檔案"
fi

echo ""
echo "   ${BLUE}專案健康分數: $SCORE/100${NC}"

if [ $SCORE -ge 90 ]; then
    echo -e "   ${GREEN}狀態: 優秀✅${NC}"
    echo "   專案結構良好，維持現狀即可。"
elif [ $SCORE -ge 70 ]; then
    echo -e "   ${YELLOW}狀態: 良好⚠️${NC}"
    echo "   專案結構可接受，建議進行少量優化。"
elif [ $SCORE -ge 50 ]; then
    echo -e "   ${YELLOW}狀態: 需要注意⚠️${NC}"
    echo "   建議整理部分檔案以改善結構。"
else
    echo -e "   ${RED}狀態: 需要整理❌${NC}"
    echo "   建議立即進行檔案整理。"
fi

echo ""

# 9. 建議操作
echo -e "${BLUE}【9】建議操作${NC}"
echo ""

if [ $ROOT_MD_COUNT -gt 15 ]; then
    echo "   1. 整理根目錄的 .md 檔案"
    echo "      將報告、分析、架構文檔移動到 docs/ 目錄"
    echo ""
fi

if [ $SCATTERED_MD_COUNT -gt 5 ]; then
    echo "   2. 集中散落的文檔"
    echo "      使用 git mv 將文檔移動到適當的目錄"
    echo ""
fi

if [ $SCATTERED_CONFIG_COUNT -gt 5 ]; then
    echo "   3. 集中散落的配置檔案"
    echo "      將配置檔案移動到 config/ 或 .config/ 目錄"
    echo ""
fi

if [ $TEMP_FILES_COUNT -gt 0 ]; then
    echo "   4. 清理臨時和備份檔案"
    echo "      刪除 .tmp, .bak, .~ 等檔案"
    echo ""
fi

if [ $DUPLICATE_FILES_COUNT -gt 0 ]; then
    echo "   5. 檢查重複檔案"
    echo "      確認重複檔案的名稱並進行適當處理"
    echo ""
fi

echo "   6. 使用提供的整理腳本"
echo "      參考 FILE_ORGANIZATION_GUIDE.md 中的腳本範例"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}檢查完成${NC}"
echo -e "${BLUE}========================================${NC}"