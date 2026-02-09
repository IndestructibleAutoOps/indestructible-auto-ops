#!/bin/bash
#
# Enterprise Governance Framework - Dependencies Installation Script
# Installs all required Python and Node.js dependencies
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
PYTHON_CMD="python3"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Installing Dependencies${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 1. Check Python
echo -e "${GREEN}[1/5] Checking Python...${NC}"
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
echo -e "   ✓ Python version: $PYTHON_VERSION"

# Check Python version
PYTHON_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
    echo -e "   ✓ Python version >= 3.10"
else
    echo -e "${RED}❌ Python version must be >= 3.10${NC}"
    exit 1
fi

echo ""

# 2. Setup virtual environment
echo -e "${GREEN}[2/5] Setting up virtual environment...${NC}"
VENV_DIR="$PROJECT_ROOT/.venv"

if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo -e "   ✓ Virtual environment created"
else
    echo -e "   ✓ Virtual environment already exists"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"
echo -e "   ✓ Virtual environment activated"

echo ""

# 3. Upgrade pip and install build tools
echo -e "${GREEN}[3/5] Upgrading pip and build tools...${NC}"
pip install --upgrade pip setuptools wheel
echo -e "   ✓ pip upgraded to latest version"
echo -e "   ✓ Build tools installed"

echo ""

# 4. Install Python dependencies
echo -e "${GREEN}[4/5] Installing Python dependencies...${NC}"

if [ -f "$PROJECT_ROOT/pyproject.toml" ]; then
    echo "   Installing from pyproject.toml..."
    pip install -e "$PROJECT_ROOT"
    
    if [ $? -eq 0 ]; then
        echo -e "   ✓ Core dependencies installed"
    else
        echo -e "${RED}❌ Failed to install core dependencies${NC}"
        exit 1
    fi
    
    # Install dev dependencies
    echo "   Installing dev dependencies..."
    pip install -e "$PROJECT_ROOT[dev]"
    
    if [ $? -eq 0 ]; then
        echo -e "   ✓ Dev dependencies installed"
    else
        echo -e "${YELLOW}⚠️  Failed to install some dev dependencies${NC}"
    fi
else
    echo -e "${RED}❌ pyproject.toml not found${NC}"
    exit 1
fi

echo ""

# 5. Verify installation
echo -e "${GREEN}[5/5] Verifying installation...${NC}"

REQUIRED_PACKAGES=("pydantic" "fastapi" "uvicorn" "sqlalchemy" "opentelemetry-api" "structlog" "pytest")
ALL_INSTALLED=true

for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if $PYTHON_CMD -c "import $pkg" 2>/dev/null; then
        version=$($PYTHON_CMD -c "import $pkg; print(getattr($pkg, '__version__', 'unknown'))")
        echo -e "   ✓ $pkg ($version)"
    else
        echo -e "   ✗ $pkg NOT INSTALLED"
        ALL_INSTALLED=false
    fi
done

echo ""

# 6. Install Node.js dependencies (optional)
if [ -f "$PROJECT_ROOT/package.json" ] && command -v npm &> /dev/null; then
    echo -e "${GREEN}[6/6] Installing Node.js dependencies...${NC}"
    cd "$PROJECT_ROOT"
    npm install
    echo -e "   ✓ Node.js dependencies installed"
    echo ""
fi

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Installation Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if [ "$ALL_INSTALLED" = true ]; then
    echo -e "${GREEN}✓ All dependencies installed successfully!${NC}"
    echo ""
    echo "Virtual environment: $VENV_DIR"
    echo ""
    echo "To activate the virtual environment:"
    echo "  source $VENV_DIR/bin/activate"
    echo ""
    echo "To verify the installation:"
    echo "  ./scripts/quick-verify.sh"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Some dependencies failed to install${NC}"
    echo ""
    echo "Please check the errors above and try again."
    exit 1
fi