#!/bin/bash
#
# Enterprise Governance Framework - Minimal Start Script
# Starts only core services for development/testing
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
VENV_DIR="$PROJECT_ROOT/.venv"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Starting Minimal Services${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Activate virtual environment
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
else
    echo -e "${RED}❌ Virtual environment not found${NC}"
    echo -e "Run ./scripts/bootstrap.sh first"
    exit 1
fi

# Check .env file
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found, using defaults${NC}"
fi

# Create necessary directories
mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/data/evidence"
mkdir -p "$PROJECT_ROOT/data/events"
mkdir -p "$PROJECT_ROOT/reports"

echo ""
echo -e "${GREEN}Starting core services...${NC}"
echo ""

# Start API server (in background)
echo -e "[1/3] Starting API server..."
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload > "$PROJECT_ROOT/logs/api.log" 2>&1 &
API_PID=$!
echo -e "   ✓ API server started (PID: $API_PID)"

# Start governance worker (in background)
echo -e "[2/3] Starting governance worker..."
python -m src.governance.worker > "$PROJECT_ROOT/logs/governance.log" 2>&1 &
WORKER_PID=$!
echo -e "   ✓ Governance worker started (PID: $WORKER_PID)"

# Start metrics collector (in background)
echo -e "[3/3] Starting metrics collector..."
python -m src.monitoring.metrics > "$PROJECT_ROOT/logs/metrics.log" 2>&1 &
METRICS_PID=$!
echo -e "   ✓ Metrics collector started (PID: $METRICS_PID)"

# Save PIDs for cleanup
echo "$API_PID" > "$PROJECT_ROOT/.api.pid"
echo "$WORKER_PID" > "$PROJECT_ROOT/.worker.pid"
echo "$METRICS_PID" > "$PROJECT_ROOT/.metrics.pid"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Services Started Successfully${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "API Server: http://localhost:8000"
echo "API Docs:   http://localhost:8000/docs"
echo "Metrics:    http://localhost:9090"
echo ""
echo "Logs directory: $PROJECT_ROOT/logs"
echo ""
echo "To stop services, run: ./scripts/stop.sh"
echo ""
echo "Useful commands:"
echo "  tail -f logs/api.log        # View API logs"
echo "  tail -f logs/governance.log # View governance logs"
echo "  tail -f logs/metrics.log    # View metrics logs"
echo ""

# Wait for services to be ready
sleep 3

# Health check
echo -e "Running health check..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ API server is healthy${NC}"
else
    echo -e "${YELLOW}⚠️  API server may still be starting...${NC}"
fi

echo ""
echo -e "${BLUE}Press Ctrl+C to stop all services${NC}"
echo ""

# Handle cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping services...${NC}"
    
    for pidfile in "$PROJECT_ROOT"/*.pid; do
        if [ -f "$pidfile" ]; then
            pid=$(cat "$pidfile")
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid"
                echo -e "   ✓ Stopped process (PID: $pid)"
            fi
            rm -f "$pidfile"
        fi
    done
    
    echo -e "${GREEN}All services stopped${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Keep script running
wait