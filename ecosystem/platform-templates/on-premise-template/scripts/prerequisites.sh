#!/bin/bash
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: platform-templates
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
#
# On-Premise Platform Prerequisites Check
# 前置檢查腳本 - 驗證系統要求
#
# GL Governance Layer: GL10-29 (Operational Layer)

set -e

echo "============================================================"
echo "On-Premise Platform - Prerequisites Check"
echo "============================================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

# 1. Operating System
echo "1. Checking Operating System..."

OS_NAME=$(cat /etc/os-release | grep "^NAME=" | cut -d= -f2 | tr -d '"')
OS_VERSION=$(cat /etc/os-release | grep "^VERSION_ID=" | cut -d= -f2 | tr -d '"')

echo "  OS: $OS_NAME $OS_VERSION"

if [[ "$OS_NAME" =~ Ubuntu|Debian|RHEL|CentOS|Rocky ]]; then
    echo -e "${GREEN}[✓] Supported OS${NC}"
else
    echo -e "${YELLOW}[!] OS not officially supported${NC}"
    ((WARNINGS++))
fi

# 2. CPU
echo ""
echo "2. Checking CPU..."

CPU_CORES=$(nproc)
echo "  CPU Cores: $CPU_CORES"

if [ $CPU_CORES -ge 4 ]; then
    echo -e "${GREEN}[✓] CPU cores sufficient${NC}"
else
    echo -e "${RED}[✗] Minimum 4 CPU cores required${NC}"
    ((ERRORS++))
fi

# 3. Memory
echo ""
echo "3. Checking Memory..."

TOTAL_MEM=$(free -g | awk '/^Mem:/{print $2}')
echo "  Total Memory: ${TOTAL_MEM}GB"

if [ $TOTAL_MEM -ge 8 ]; then
    echo -e "${GREEN}[✓] Memory sufficient${NC}"
else
    echo -e "${RED}[✗] Minimum 8GB memory required${NC}"
    ((ERRORS++))
fi

# 4. Disk Space
echo ""
echo "4. Checking Disk Space..."

DISK_AVAIL=$(df -BG / | tail -1 | awk '{print $4}' | sed 's/G//')
echo "  Available Space: ${DISK_AVAIL}GB"

if [ $DISK_AVAIL -ge 100 ]; then
    echo -e "${GREEN}[✓] Disk space sufficient${NC}"
else
    echo -e "${YELLOW}[!] Recommended 100GB+ available space${NC}"
    ((WARNINGS++))
fi

# 5. Network
echo ""
echo "5. Checking Network..."

# Check network interfaces
INTERFACES=$(ip -o link show | awk -F': ' '{print $2}' | grep -v lo | wc -l)
echo "  Network Interfaces: $INTERFACES"

if [ $INTERFACES -ge 1 ]; then
    echo -e "${GREEN}[✓] Network interface available${NC}"
else
    echo -e "${RED}[✗] No network interface found${NC}"
    ((ERRORS++))
fi

# 6. Required Ports
echo ""
echo "6. Checking Required Ports..."

REQUIRED_PORTS=(8000 8080 8500 5672 9090)
for port in "${REQUIRED_PORTS[@]}"; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}[!] Port $port already in use${NC}"
        ((WARNINGS++))
    else
        echo -e "${GREEN}[✓] Port $port available${NC}"
    fi
done

# 7. Python
echo ""
echo "7. Checking Python..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo "  Python Version: $PYTHON_VERSION"
    
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ $PYTHON_MAJOR -eq 3 ] && [ $PYTHON_MINOR -ge 8 ]; then
        echo -e "${GREEN}[✓] Python 3.8+ available${NC}"
    else
        echo -e "${RED}[✗] Python 3.8+ required${NC}"
        ((ERRORS++))
    fi
else
    echo -e "${RED}[✗] Python 3 not found${NC}"
    ((ERRORS++))
fi

# 8. Summary
echo ""
echo "============================================================"
echo "Prerequisites Check Summary"
echo "============================================================"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ All prerequisites met!${NC}"
    echo ""
    echo "System is ready for platform deployment."
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Prerequisites met with $WARNINGS warnings${NC}"
    echo ""
    echo "System is ready, but review warnings above."
    exit 0
else
    echo -e "${RED}❌ Prerequisites check failed: $ERRORS errors, $WARNINGS warnings${NC}"
    echo ""
    echo "Please resolve the errors before deploying."
    exit 1
fi
