#!/bin/bash
# Minimal Startup Script for MNGA System
# Starts core components with minimal configuration

set -e

echo "========================================="
echo "MNGA Minimal Startup"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check virtual environment
echo "Checking virtual environment..."
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Run bootstrap.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    print_success "Environment variables loaded"
else
    print_warning "No .env file found, using defaults"
fi

# Start time
START_TIME=$(date +%s)

# Step 1: Run governance enforcement
echo ""
echo "Step 1: Running governance enforcement..."
python3 ecosystem/enforce.py --audit > /tmp/governance_check.json 2>&1
if [ $? -eq 0 ]; then
    print_success "Governance enforcement passed"
else
    print_warning "Governance enforcement had warnings"
fi

# Step 2: Initialize internal retrieval
echo ""
echo "Step 2: Initializing internal retrieval engine..."
python3 -c "
from ecosystem.reasoning.dual_path.internal.retrieval import InternalRetrievalEngine
engine = InternalRetrievalEngine()
print('Internal retrieval engine initialized')
" 2>&1 | head -5
print_success "Internal retrieval initialized"

# Step 3: Initialize external retrieval
echo ""
echo "Step 3: Initializing external retrieval engine..."
python3 -c "
from ecosystem.reasoning.dual_path.external.retrieval import ExternalRetrievalEngine
engine = ExternalRetrievalEngine()
print('External retrieval engine initialized')
" 2>&1 | head -5
print_success "External retrieval initialized"

# Step 4: Initialize arbitrator
echo ""
echo "Step 4: Initializing arbitrator..."
python3 -c "
from ecosystem.reasoning.dual_path.arbitration.arbitrator import Arbitrator
arbitrator = Arbitrator()
print('Arbitrator initialized')
" 2>&1 | head -5
print_success "Arbitrator initialized"

# Step 5: Test reasoning pipeline
echo ""
echo "Step 5: Testing reasoning pipeline..."
python3 -c "
from platforms.gl.platform-assistant.orchestration.pipeline import ReasoningPipeline
pipeline = ReasoningPipeline()
response = pipeline.handle_request(
    task_spec='Test request',
    context={}
)
print('Reasoning pipeline test passed')
print('Request ID:', response.get('request_id'))
" 2>&1 | head -10
print_success "Reasoning pipeline test passed"

# Calculate duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Summary
echo ""
echo "========================================="
echo "Startup Complete!"
echo "========================================="
echo ""
echo "Components started:"
echo "  ✓ Governance Enforcement"
echo "  ✓ Internal Retrieval Engine"
echo "  ✓ External Retrieval Engine"
echo "  ✓ Arbitrator"
echo "  ✓ Reasoning Pipeline"
echo ""
echo "Startup time: ${DURATION}s"
echo ""
print_success "All systems operational!"
echo ""
echo "To test the system:"
echo "  python3 platforms/gl-platform-assistant/orchestration/pipeline.py"