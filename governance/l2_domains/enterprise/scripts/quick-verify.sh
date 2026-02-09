#!/bin/bash
#
# Enterprise Governance Framework - Quick Verification Script
# Performs fast integrity checks (<30 seconds)
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
echo -e "${BLUE}Quick Verification${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Verification results
PASS=0
FAIL=0
WARN=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARN++))
}

# 1. Check project structure
echo -e "${BLUE}[1] Project Structure${NC}"
[ -d "$PROJECT_ROOT/src" ] && check_pass "src directory exists" || check_fail "src directory missing"
[ -d "$PROJECT_ROOT/tests" ] && check_pass "tests directory exists" || check_fail "tests directory missing"
[ -d "$PROJECT_ROOT/scripts" ] && check_pass "scripts directory exists" || check_fail "scripts directory missing"
[ -f "$PROJECT_ROOT/pyproject.toml" ] && check_pass "pyproject.toml exists" || check_fail "pyproject.toml missing"
[ -f "$PROJECT_ROOT/package.json" ] && check_pass "package.json exists" || check_fail "package.json missing"

echo ""

# 2. Check configuration
echo -e "${BLUE}[2] Configuration Files${NC}"
[ -f "$PROJECT_ROOT/.env.example" ] && check_pass ".env.example exists" || check_fail ".env.example missing"
[ -f "$PROJECT_ROOT/.env" ] && check_pass ".env configured" || check_warn ".env not configured (copy from .env.example)"
[ -f "$PROJECT_ROOT/docker-compose.yaml" ] && check_pass "docker-compose.yaml exists" || check_fail "docker-compose.yaml missing"
[ -f "$PROJECT_ROOT/Dockerfile" ] && check_pass "Dockerfile exists" || check_fail "Dockerfile missing"

echo ""

# 3. Check Python environment
echo -e "${BLUE}[3] Python Environment${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    check_pass "Python installed: $PYTHON_VERSION"
else
    check_fail "Python 3 not found"
fi

if [ -d "$PROJECT_ROOT/.venv" ]; then
    check_pass "Virtual environment exists"
else
    check_warn "Virtual environment not found (run ./scripts/bootstrap.sh)"
fi

echo ""

# 4. Check core modules
echo -e "${BLUE}[4] Core Modules${NC}"
[ -f "$PROJECT_ROOT/src/audit/logger.py" ] && check_pass "Audit logger module exists" || check_fail "Audit logger module missing"
[ -f "$PROJECT_ROOT/src/governance/enforcer.py" ] && check_pass "Governance enforcer module exists" || check_fail "Governance enforcer module missing"

echo ""

# 5. Check test files
echo -e "${BLUE}[5] Test Files${NC}"
[ -f "$PROJECT_ROOT/tests/test_fast.py" ] && check_pass "Fast test suite exists" || check_fail "Fast test suite missing"

echo ""

# 6. Check data directories
echo -e "${BLUE}[6] Data Directories${NC}"
[ -d "$PROJECT_ROOT/data/evidence" ] && check_pass "Evidence directory exists" || check_warn "Evidence directory missing (will be created)"
[ -d "$PROJECT_ROOT/data/events" ] && check_pass "Events directory exists" || check_warn "Events directory missing (will be created)"

echo ""

# 7. Quick import test (if venv exists)
echo -e "${BLUE}[7] Module Import Test${NC}"
if [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
    if python3 -c "from src.audit.logger import AuditLogger" 2>/dev/null; then
        check_pass "Audit logger imports successfully"
    else
        check_fail "Audit logger import failed"
    fi
    
    if python3 -c "from src.governance.enforcer import GovernanceEnforcer" 2>/dev/null; then
        check_pass "Governance enforcer imports successfully"
    else
        check_fail "Governance enforcer import failed"
    fi
else
    check_warn "Skip import test (venv not available)"
fi

echo ""

# 8. Run fast tests
echo -e "${BLUE}[8] Run Fast Tests${NC}"
if [ -d "$PROJECT_ROOT/.venv" ]; then
    cd "$PROJECT_ROOT"
    if python3 -m pytest tests/test_fast.py -v --tb=short -q 2>&1 | grep -q "passed"; then
        check_pass "Fast tests pass"
    else
        check_fail "Fast tests failed"
    fi
else
    check_warn "Skip tests (venv not available)"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Verification Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${YELLOW}Warnings: $WARN${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ All critical checks passed!${NC}"
    echo ""
    echo "You can now:"
    echo "  ./scripts/start-min.sh    # Start services"
    echo "  make test                 # Run full test suite"
    exit 0
else
    echo -e "${RED}✗ Some checks failed${NC}"
    echo ""
    echo "Please fix the failures above or run:"
    echo "  ./scripts/bootstrap.sh    # Setup environment"
    exit 1
fi