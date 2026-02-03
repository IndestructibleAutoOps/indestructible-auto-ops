#!/bin/bash
# Bootstrap Script for MNGA Dual-Path Retrieval System
# Installs dependencies and initializes the environment

set -e

echo "========================================="
echo "MNGA Bootstrap Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    MINGW*)     MACHINE=Windows;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

print_success "Detected OS: ${MACHINE}"

# Check Python version
echo ""
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    print_success "Python found: ${PYTHON_VERSION}"
    
    # Check if version is >= 3.11
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [[ $PYTHON_MAJOR -lt 3 || ($PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 11) ]]; then
        print_error "Python 3.11 or higher is required"
        exit 1
    fi
else
    print_error "Python 3 not found. Please install Python 3.11 or higher"
    exit 1
fi

# Check if pip is available
echo ""
echo "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 found"
else
    print_error "pip3 not found"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip -q
print_success "pip upgraded"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    print_success "Dependencies installed"
else
    print_warning "requirements.txt not found, installing minimal dependencies"
    pip install pyyaml requests -q
fi

# Install additional dependencies for reasoning system
echo ""
echo "Installing reasoning system dependencies..."
pip install -q -r requirements.txt
print_success "Reasoning system dependencies installed"

# Create necessary directories
echo ""
echo "Creating directory structure..."
directories=(
    "ecosystem/logs/audit"
    "ecosystem/logs/reasoning"
    "ecosystem/data/feedback"
    "ecosystem/indexes/internal/code_vectors"
    "ecosystem/indexes/internal/docs_index"
    "ecosystem/indexes/external/cache"
    "artifacts/modules"
    "artifacts/reports/naming"
    "artifacts/reports/audit"
    "artifacts/reports/auto-fix"
)

for dir in "${directories[@]}"; do
    mkdir -p "$dir"
    print_success "Created: $dir"
done

# Create .env.example if it doesn't exist
echo ""
echo "Creating environment configuration..."
if [ ! -f ".env.example" ]; then
    cat > .env.example << 'EOF'
# MNGA Configuration
MNGA_ENV=development
MNGA_LOG_LEVEL=INFO

# Internal Retrieval
INTERNAL_EMBEDDING_MODEL=text-embedding-3-small
INTERNAL_VECTOR_DB_TYPE=chromadb
INTERNAL_VECTOR_DB_PATH=ecosystem/indexes/internal/code_vectors

# Knowledge Graph
GRAPH_DB_URI=bolt://localhost:7687
GRAPH_DB_USER=neo4j
GRAPH_DB_PASSWORD=your_password_here

# External Retrieval
EXTERNAL_SEARCH_PROVIDER=bing
EXTERNAL_SEARCH_API_KEY=your_api_key_here
EXTERNAL_SEARCH_MAX_RESULTS=10

# LLM Configuration
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_API_KEY=your_api_key_here
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# Arbitration
ARBITRATION_INTERNAL_THRESHOLD=0.8
ARBITRATION_EXTERNAL_THRESHOLD=0.85
ARBITRATION_HYBRID_THRESHOLD=0.75

# Traceability
TRACEABILITY_ENABLED=true
TRACEABILITY_OUTPUT_FORMAT=json
TRACEABILITY_RETENTION_DAYS=90

# Feedback
FEEDBACK_ENABLED=true
FEEDBACK_ANALYSIS_DAYS=30

# Monitoring
PROMETHEUS_ENABLED=false
PROMETHEUS_PORT=9090
GRAFANA_ENABLED=false
GRAFANA_PORT=3000
EOF
    print_success "Created .env.example"
else
    print_warning ".env.example already exists"
fi

# Create .env from .env.example if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning "Created .env from .env.example. Please update with actual values."
fi

# Create minimal requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    cat > requirements.txt << 'EOF'
# Core dependencies
PyYAML>=6.0
requests>=2.31.0

# LLM clients
openai>=1.0.0
anthropic>=0.18.0

# Vector database
chromadb>=0.4.0

# Graph database
neo4j>=5.0.0

# Code analysis
tree-sitter>=0.20.0
tree-sitter-python>=0.20.0

# Graph operations
networkx>=3.2.0

# Data processing
pandas>=2.0.0
numpy>=1.24.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0

# Utilities
python-dotenv>=1.0.0
EOF
    print_success "Created requirements.txt"
fi

# Run governance enforcement to verify setup
echo ""
echo "Running governance enforcement check..."
if [ -f "ecosystem/enforce.py" ]; then
    python3 ecosystem/enforce.py || {
        print_error "Governance enforcement check failed"
        exit 1
    }
    print_success "Governance enforcement check passed"
else
    print_warning "ecosystem/enforce.py not found, skipping enforcement check"
fi

# Initialize knowledge graph
echo ""
echo "Initializing knowledge graph..."
if [ -f "ecosystem/reasoning/dual_path/internal/knowledge_graph.py" ]; then
    python3 ecosystem/reasoning/dual_path/internal/knowledge_graph.py || {
        print_warning "Knowledge graph initialization skipped (requires Neo4j)"
    }
    print_success "Knowledge graph initialization attempted"
else
    print_warning "Knowledge graph module not found"
fi

# Summary
echo ""
echo "========================================="
echo "Bootstrap Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run minimal start: ./scripts/start-min.sh"
echo "4. Run quick verify: ./scripts/quick-verify.sh"
echo ""
print_success "Bootstrap completed successfully!"