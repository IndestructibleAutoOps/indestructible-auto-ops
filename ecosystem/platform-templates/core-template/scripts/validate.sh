#!/bin/bash
#
# Core Platform Validation Script
# 驗證腳本 - 檢查平台配置和狀態
#
# GL Governance Layer: GL10-29 (Operational Layer)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLATFORM_ROOT="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "Core Platform Validation"
echo "============================================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

# 1. Configuration validation
echo "1. Validating configuration files..."

if [ -f "$PLATFORM_ROOT/configs/platform-config.yaml" ]; then
    echo -e "${GREEN}[✓] platform-config.yaml exists${NC}"
    
    # Validate YAML syntax
    if python3 -c "import yaml; yaml.safe_load(open('$PLATFORM_ROOT/configs/platform-config.yaml'))" 2>/dev/null; then
        echo -e "${GREEN}[✓] platform-config.yaml is valid YAML${NC}"
    else
        echo -e "${RED}[✗] platform-config.yaml has syntax errors${NC}"
        ((ERRORS++))
    fi
else
    echo -e "${RED}[✗] platform-config.yaml not found${NC}"
    ((ERRORS++))
fi

if [ -f "$PLATFORM_ROOT/configs/services-config.yaml" ]; then
    echo -e "${GREEN}[✓] services-config.yaml exists${NC}"
else
    echo -e "${YELLOW}[!] services-config.yaml not found${NC}"
    ((WARNINGS++))
fi

# 2. Directory structure validation
echo ""
echo "2. Validating directory structure..."

REQUIRED_DIRS=("configs" "scripts" "examples")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$PLATFORM_ROOT/$dir" ]; then
        echo -e "${GREEN}[✓] $dir/ exists${NC}"
    else
        echo -e "${RED}[✗] $dir/ missing${NC}"
        ((ERRORS++))
    fi
done

# 3. Script validation
echo ""
echo "3. Validating scripts..."

REQUIRED_SCRIPTS=("setup.sh" "deploy.sh" "status.sh" "cleanup.sh")
for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [ -f "$PLATFORM_ROOT/scripts/$script" ]; then
        if [ -x "$PLATFORM_ROOT/scripts/$script" ]; then
            echo -e "${GREEN}[✓] $script is executable${NC}"
        else
            echo -e "${YELLOW}[!] $script is not executable${NC}"
            chmod +x "$PLATFORM_ROOT/scripts/$script"
            echo -e "${GREEN}[✓] Made $script executable${NC}"
        fi
    else
        echo -e "${RED}[✗] $script not found${NC}"
        ((ERRORS++))
    fi
done

# 4. Python dependencies validation
echo ""
echo "4. Validating Python dependencies..."

REQUIRED_PACKAGES=("yaml")
for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        echo -e "${GREEN}[✓] $package available${NC}"
    else
        echo -e "${RED}[✗] $package not available${NC}"
        ((ERRORS++))
    fi
done

# 5. Environment validation
echo ""
echo "5. Validating environment..."

if [ -f "$PLATFORM_ROOT/.env" ]; then
    echo -e "${GREEN}[✓] .env file exists${NC}"
    
    # Check required variables
    source "$PLATFORM_ROOT/.env"
    
    if [ -n "$PLATFORM_NAME" ]; then
        echo -e "${GREEN}[✓] PLATFORM_NAME set: $PLATFORM_NAME${NC}"
    else
        echo -e "${YELLOW}[!] PLATFORM_NAME not set${NC}"
        ((WARNINGS++))
    fi
    
    if [ -n "$JWT_SECRET" ]; then
        echo -e "${GREEN}[✓] JWT_SECRET set${NC}"
    else
        echo -e "${YELLOW}[!] JWT_SECRET not set${NC}"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}[!] .env file not found (run setup.sh first)${NC}"
    ((WARNINGS++))
fi

# 6. Ecosystem integration validation
echo ""
echo "6. Validating ecosystem integration..."

ECOSYSTEM_ROOT="$PLATFORM_ROOT/../.."
if [ -d "$ECOSYSTEM_ROOT/coordination" ]; then
    echo -e "${GREEN}[✓] Ecosystem coordination modules found${NC}"
else
    echo -e "${YELLOW}[!] Ecosystem coordination modules not found${NC}"
    ((WARNINGS++))
fi

# 7. Summary
echo ""
echo "============================================================"
echo "Validation Summary"
echo "============================================================"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ All validations passed!${NC}"
    echo ""
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Validation completed with $WARNINGS warnings${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Validation failed with $ERRORS errors and $WARNINGS warnings${NC}"
    echo ""
    exit 1
fi
