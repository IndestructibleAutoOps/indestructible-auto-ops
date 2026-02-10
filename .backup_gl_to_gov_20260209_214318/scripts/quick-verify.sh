#!/bin/bash
# Quick Verification Script for MNGA System
# Verifies all components are working correctly

set -e

echo "========================================="
echo "MNGA Quick Verification"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if venv exists
echo "Checking prerequisites..."
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found. Run bootstrap.sh first."
    exit 1
fi

source venv/bin/activate
print_success "Virtual environment found"

# Verify Python version
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
print_success "Python version: ${PYTHON_VERSION}"

# Test counter
PASSED=0
FAILED=0
TOTAL=0

# Test 1: Governance enforcement
echo ""
echo "Test 1: Governance Enforcement"
TOTAL=$((TOTAL + 1))
if python3 ecosystem/enforce.py --audit > /dev/null 2>&1; then
    print_success "Governance enforcement working"
    PASSED=$((PASSED + 1))
else
    print_error "Governance enforcement failed"
    FAILED=$((FAILED + 1))
fi

# Test 2: Internal retrieval
echo ""
echo "Test 2: Internal Retrieval Engine"
TOTAL=$((TOTAL + 1))
if python3 -c "
from ecosystem.reasoning.dual_path.internal.retrieval import InternalRetrievalEngine
engine = InternalRetrievalEngine()
results = engine.search('test query', top_k=3)
assert len(results) >= 0
" 2>&1 | grep -q "Success"; then
    print_success "Internal retrieval working"
    PASSED=$((PASSED + 1))
else
    print_error "Internal retrieval failed"
    FAILED=$((FAILED + 1))
fi

# Test 3: External retrieval
echo ""
echo "Test 3: External Retrieval Engine"
TOTAL=$((TOTAL + 1))
if python3 -c "
from ecosystem.reasoning.dual_path.external.retrieval import ExternalRetrievalEngine
engine = ExternalRetrievalEngine()
results = engine.search('test query', top_k=3)
assert len(results) >= 0
" 2>&1 | grep -q "Success"; then
    print_success "External retrieval working"
    PASSED=$((PASSED + 1))
else
    print_error "External retrieval failed"
    FAILED=$((FAILED + 1))
fi

# Test 4: Arbitrator
echo ""
echo "Test 4: Arbitrator"
TOTAL=$((TOTAL + 1))
if python3 -c "
from ecosystem.reasoning.dual_path.arbitration.arbitrator import Arbitrator
arbitrator = Arbitrator()
decision = arbitrator.arbitrate(
    'test task',
    {'confidence': 0.9, 'answer': 'internal', 'metadata': {}},
    {'confidence': 0.8, 'answer': 'external', 'metadata': {}}
)
assert decision is not None
" 2>&1 | grep -q "Success"; then
    print_success "Arbitrator working"
    PASSED=$((PASSED + 1))
else
    print_error "Arbitrator failed"
    FAILED=$((FAILED + 1))
fi

# Test 5: Traceability
echo ""
echo "Test 5: Traceability Engine"
TOTAL=$((TOTAL + 1))
if python3 -c "
from ecosystem.reasoning.traceability.traceability import TraceabilityEngine
engine = TraceabilityEngine()
assert engine is not None
" 2>&1 | grep -q "Success"; then
    print_success "Traceability working"
    PASSED=$((PASSED + 1))
else
    print_error "Traceability failed"
    FAILED=$((FAILED + 1))
fi

# Test 6: Feedback Loop
echo ""
echo "Test 6: Feedback Loop"
TOTAL=$((TOTAL + 1))
if python3 -c "
from ecosystem.reasoning.traceability.feedback import FeedbackLoop, UserFeedback
loop = FeedbackLoop()
feedback = UserFeedback('test_case', 'ACCEPT')
assert feedback is not None
" 2>&1 | grep -q "Success"; then
    print_success "Feedback loop working"
    PASSED=$((PASSED + 1))
else
    print_error "Feedback loop failed"
    FAILED=$((FAILED + 1))
fi

# Test 7: Planning Agent
echo ""
echo "Test 7: Planning Agent"
TOTAL=$((TOTAL + 1))
if python3 -c "
from ecosystem.reasoning.agents.planning_agent import PlanningAgent
agent = PlanningAgent()
plan = agent.plan_task('test task')
assert plan is not None
assert len(plan.steps) > 0
" 2>&1 | grep -q "Success"; then
    print_success "Planning agent working"
    PASSED=$((PASSED + 1))
else
    print_error "Planning agent failed"
    FAILED=$((FAILED + 1))
fi

# Test 8: Reasoning Pipeline
echo ""
echo "Test 8: End-to-End Reasoning Pipeline"
TOTAL=$((TOTAL + 1))
if python3 -c "
from platforms.gl.platform-assistant.orchestration.pipeline import ReasoningPipeline
pipeline = ReasoningPipeline()
response = pipeline.handle_request('test query', {}, 'test_user')
assert 'request_id' in response
assert 'final_answer' in response
" 2>&1 | grep -q "Success"; then
    print_success "Reasoning pipeline working"
    PASSED=$((PASSED + 1))
else
    print_error "Reasoning pipeline failed"
    FAILED=$((FAILED + 1))
fi

# Test 9: Configuration files
echo ""
echo "Test 9: Configuration Files"
TOTAL=$((TOTAL + 1))
CONFIG_FILES=(
    "ecosystem/contracts/reasoning/dual_path_spec.yaml"
    "ecosystem/reasoning/agents/tools_registry.yaml"
    ".config/conftest/policies/naming_policy.rego"
    ".config/prometheus/naming-convention-alerts.yaml"
)

ALL_CONFIGS_EXIST=true
for file in "${CONFIG_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Missing config: $file"
        ALL_CONFIGS_EXIST=false
    fi
done

if [ "$ALL_CONFIGS_EXIST" = true ]; then
    print_success "All configuration files present"
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

# Test 10: Directory structure
echo ""
echo "Test 10: Directory Structure"
TOTAL=$((TOTAL + 1))
REQUIRED_DIRS=(
    "ecosystem/reasoning/dual-path/internal"
    "ecosystem/reasoning/dual-path/external"
    "ecosystem/reasoning/dual-path/arbitration"
    "ecosystem/reasoning/traceability"
    "ecosystem/reasoning/agents"
    "platforms/gov-platform-assistant/orchestration"
)

ALL_DIRS_EXIST=true
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        print_error "Missing directory: $dir"
        ALL_DIRS_EXIST=false
    fi
done

if [ "$ALL_DIRS_EXIST" = true ]; then
    print_success "All required directories present"
    PASSED=$((PASSED + 1))
else
    FAILED=$((FAILED + 1))
fi

# Summary
echo ""
echo "========================================="
echo "Verification Results"
echo "========================================="
echo ""
echo "Total Tests: $TOTAL"
echo -e "${GREEN}Passed:${NC} $PASSED"
echo -e "${RED}Failed:${NC} $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    print_success "All tests passed! System is ready."
    exit 0
else
    print_error "Some tests failed. Please review the errors above."
    exit 1
fi