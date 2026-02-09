#!/bin/bash
#
# Enterprise Governance Framework - Prerequisites Validation Script
# Checks all required dependencies and tools
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Prerequisites Validation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Track results
MISSING_DEPS=()
MISSING_VARS=()

# Check function
check_command() {
    if command -v "$1" &> /dev/null; then
        version=$($1 --version 2>&1 | head -n1 || echo "unknown")
        echo -e "${GREEN}✓${NC} $1: $version"
        return 0
    else
        echo -e "${RED}✗${NC} $1: NOT FOUND"
        MISSING_DEPS+=("$1")
        return 1
    fi
}

# Environment variables check
check_env_var() {
    local var_name=$1
    local file="$PROJECT_ROOT/.env"
    
    if [ -f "$file" ] && grep -q "^${var_name}=" "$file"; then
        value=$(grep "^${var_name}=" "$file" | cut -d'=' -f2 | xargs)
        if [ -n "$value" ] && [ "$value" != '""' ] && [ "$value" != "''" ]; then
            echo -e "${GREEN}✓${NC} $var_name is set"
            return 0
        else
            echo -e "${YELLOW}⚠${NC} $var_name is empty"
            MISSING_VARS+=("$var_name (empty)")
            return 1
        fi
    else
        echo -e "${YELLOW}⚠${NC} $var_name is not configured"
        MISSING_VARS+=("$var_name (missing)")
        return 1
    fi
}

# 1. Check Python
echo -e "${BLUE}[1] Python Environment${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
    PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
    
    echo -e "${GREEN}✓${NC} Python: $PYTHON_VERSION"
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
        echo -e "${GREEN}✓${NC} Python version >= 3.10"
    else
        echo -e "${RED}✗${NC} Python version must be >= 3.10"
        MISSING_DEPS+=("Python >= 3.10")
    fi
    
    # Check pip
    if command -v pip3 &> /dev/null; then
        echo -e "${GREEN}✓${NC} pip: $(pip3 --version)"
    else
        echo -e "${RED}✗${NC} pip not found"
        MISSING_DEPS+=("pip3")
    fi
else
    echo -e "${RED}✗${NC} Python 3 not found"
    MISSING_DEPS+=("python3")
fi

echo ""

# 2. Check Node.js (optional)
echo -e "${BLUE}[2] Node.js (Optional)${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node: $NODE_VERSION"
    
    if command -v npm &> /dev/null; then
        echo -e "${GREEN}✓${NC} npm: $(npm --version)"
    fi
else
    echo -e "${YELLOW}⚠${NC}  Node.js not found (optional for Node.js components)"
fi

echo ""

# 3. Check Docker (optional)
echo -e "${BLUE}[3] Docker (Optional)${NC}"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo -e "${GREEN}✓${NC} $DOCKER_VERSION"
    
    if command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}✓${NC} docker-compose: $(docker-compose --version)"
    fi
else
    echo -e "${YELLOW}⚠${NC}  Docker not found (optional for container deployment)"
fi

echo ""

# 4. Check Git
echo -e "${BLUE}[4] Git${NC}"
check_command "git"

echo ""

# 5. Check Python packages (if venv exists)
echo -e "${BLUE}[5] Python Packages${NC}"
if [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
    
    REQUIRED_PACKAGES=("pydantic" "fastapi" "sqlalchemy" "opentelemetry-api" "structlog")
    
    for pkg in "${REQUIRED_PACKAGES[@]}"; do
        if python3 -c "import $pkg" 2>/dev/null; then
            version=$(python3 -c "import $pkg; print(getattr($pkg, '__version__', 'unknown'))")
            echo -e "${GREEN}✓${NC} $pkg: $version"
        else
            echo -e "${RED}✗${NC} $pkg: NOT INSTALLED"
            MISSING_DEPS+=("python package: $pkg")
        fi
    done
else
    echo -e "${YELLOW}⚠${NC}  Virtual environment not found (run ./scripts/bootstrap.sh)"
fi

echo ""

# 6. Check Environment Variables
echo -e "${BLUE}[6] Environment Variables${NC}"
if [ -f "$PROJECT_ROOT/.env" ]; then
    # Check critical variables
    CRITICAL_VARS=("APP_NAME" "APP_ENV" "LOG_LEVEL" "DATABASE_URL" "API_PORT")
    
    for var in "${CRITICAL_VARS[@]}"; do
        check_env_var "$var"
    done
else
    echo -e "${YELLOW}⚠${NC}  .env file not found (copy from .env.example)"
    for var in APP_NAME APP_ENV LOG_LEVEL DATABASE_URL API_PORT; do
        MISSING_VARS+=("$var (no .env)")
    done
fi

echo ""

# 7. Check File Permissions
echo -e "${BLUE}[7] File Permissions${NC}"
[ -r "$PROJECT_ROOT" ] && echo -e "${GREEN}✓${NC} Project root is readable" || echo -e "${RED}✗${NC} Project root is not readable"
[ -w "$PROJECT_ROOT" ] && echo -e "${GREEN}✓${NC} Project root is writable" || echo -e "${RED}✗${NC} Project root is not writable"
[ -x "$PROJECT_ROOT" ] && echo -e "${GREEN}✓${NC} Project root is executable" || echo -e "${RED}✗${NC} Project root is not executable"

echo ""

# 8. Check Network Ports
echo -e "${BLUE}[8] Network Ports${NC}"
check_port() {
    local port=$1
    local name=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠${NC}  Port $port ($name) is in use"
    else
        echo -e "${GREEN}✓${NC} Port $port ($name) is available"
    fi
}

if command -v lsof &> /dev/null; then
    check_port 8000 "API"
    check_port 5432 "PostgreSQL"
    check_port 6379 "Redis"
    check_port 9090 "Metrics"
else
    echo -e "${YELLOW}⚠${NC}  lsof not available, skipping port checks"
fi

echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Validation Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if [ ${#MISSING_DEPS[@]} -eq 0 ] && [ ${#MISSING_VARS[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All prerequisites validated!${NC}"
    exit 0
else
    echo -e "${RED}✗ Issues found:${NC}"
    echo ""
    
    if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
        echo -e "${YELLOW}Missing Dependencies:${NC}"
        for dep in "${MISSING_DEPS[@]}"; do
            echo "  - $dep"
        done
        echo ""
        echo -e "${BLUE}To install missing dependencies, run:${NC}"
        echo "  ./scripts/install-deps.sh"
        echo ""
    fi
    
    if [ ${#MISSING_VARS[@]} -gt 0 ]; then
        echo -e "${YELLOW}Missing Environment Variables:${NC}"
        for var in "${MISSING_VARS[@]}"; do
            echo "  - $var"
        done
        echo ""
        echo -e "${BLUE}To fix environment variables, run:${NC}"
        echo "  ./scripts/fix-env.sh"
        echo ""
    fi
    
    exit 1
fi