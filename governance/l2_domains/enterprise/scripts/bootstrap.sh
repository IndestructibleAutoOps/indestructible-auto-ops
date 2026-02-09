#!/bin/bash
#
# Enterprise Governance Framework - Bootstrap Script
# Complete environment setup and initialization
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"
PYTHON_CMD="python3"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Enterprise Governance Bootstrap${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Project Root: $PROJECT_ROOT"
echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo ""

# Step 1: Validate prerequisites
echo -e "${GREEN}[1/8] Validating prerequisites...${NC}"
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version | awk '{print $2}')
echo -e "   ✓ Python version: $PYTHON_VERSION"

if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker not found (optional)${NC}"
else
    echo -e "   ✓ Docker available"
fi

if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git not found${NC}"
    exit 1
fi
echo -e "   ✓ Git available"

# Step 2: Create virtual environment
echo ""
echo -e "${GREEN}[2/8] Setting up Python virtual environment...${NC}"
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo -e "   ✓ Virtual environment created"
else
    echo -e "   ✓ Virtual environment already exists"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Step 3: Upgrade pip and install build tools
echo ""
echo -e "${GREEN}[3/8] Installing build tools...${NC}"
pip install --upgrade pip setuptools wheel
echo -e "   ✓ Build tools installed"

# Step 4: Install Python dependencies
echo ""
echo -e "${GREEN}[4/8] Installing Python dependencies...${NC}"
pip install -e "$PROJECT_ROOT"
pip install -e "$PROJECT_ROOT[dev]"
echo -e "   ✓ Python dependencies installed"

# Step 5: Setup environment variables
echo ""
echo -e "${GREEN}[5/8] Setting up environment...${NC}"

if [ ! -f "$PROJECT_ROOT/.env" ]; then
    if [ -f "$PROJECT_ROOT/.env.example" ]; then
        cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
        echo -e "   ✓ .env created from .env.example"
        echo -e "${YELLOW}⚠️  Please review and configure .env file${NC}"
    else
        echo -e "${RED}❌ .env.example not found${NC}"
        exit 1
    fi
else
    echo -e "   ✓ .env already exists"
fi

# Step 6: Initialize directories
echo ""
echo -e "${GREEN}[6/8] Initializing directories...${NC}"
mkdir -p "$PROJECT_DIR/data/evidence"
mkdir -p "$PROJECT_DIR/data/events"
mkdir -p "$PROJECT_DIR/data/migrations"
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/reports"
echo -e "   ✓ Directories initialized"

# Step 7: Run validation
echo ""
echo -e "${GREEN}[7/8] Running validation...${NC}"
"$SCRIPT_DIR/validate-prereqs.sh"
echo -e "   ✓ Validation complete"

# Step 8: Run quick tests
echo ""
echo -e "${GREEN}[8/8] Running quick tests...${NC}"
pip install pytest pytest-cov
cd "$PROJECT_ROOT"
python -m pytest tests/test_fast.py -v --tb=short --maxfail=5 || {
    echo -e "${YELLOW}⚠️  Some tests failed, but bootstrap completed${NC}"
}

# Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Bootstrap Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Review and configure .env file"
echo "2. Run: ./scripts/start-min.sh    # Start minimal services"
echo "3. Run: ./scripts/quick-verify.sh # Verify setup"
echo "4. Run: make test                  # Run full test suite"
echo ""
echo "Virtual environment activated at: $VENV_DIR"
echo ""
echo -e "${YELLOW}To activate the virtual environment manually:${NC}"
echo "  source $VENV_DIR/bin/activate"
echo ""