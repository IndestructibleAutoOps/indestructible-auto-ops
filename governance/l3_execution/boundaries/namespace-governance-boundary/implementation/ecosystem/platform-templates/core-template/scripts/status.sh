#!/bin/bash
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: platform-templates
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
#
# Core Platform Status Script
# 狀態腳本 - 檢查平台運行狀態
#
# GL Governance Layer: GL10-29 (Operational Layer)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLATFORM_ROOT="$(dirname "$SCRIPT_DIR")"

# Load environment
if [ -f "$PLATFORM_ROOT/.env" ]; then
    source "$PLATFORM_ROOT/.env"
fi

echo "============================================================"
echo "Core Platform Status"
echo "============================================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Platform info
echo "Platform: ${PLATFORM_NAME:-unknown}"
echo "Location: $PLATFORM_ROOT"
echo ""

# Service status
echo "Services Status:"
echo "----------------"

# Service Discovery
if lsof -Pi :8500 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "  Service Discovery (8500): ${GREEN}RUNNING${NC}"
else
    echo -e "  Service Discovery (8500): ${RED}STOPPED${NC}"
fi

# API Gateway
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "  API Gateway (8000):       ${GREEN}RUNNING${NC}"
else
    echo -e "  API Gateway (8000):       ${RED}STOPPED${NC}"
fi

# Message Bus
if lsof -Pi :5672 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "  Message Bus (5672):       ${GREEN}RUNNING${NC}"
else
    echo -e "  Message Bus (5672):       ${RED}STOPPED${NC}"
fi

# Data Sync
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "  Data Sync (8080):         ${GREEN}RUNNING${NC}"
else
    echo -e "  Data Sync (8080):         ${RED}STOPPED${NC}"
fi

# Resource usage
echo ""
echo "Resource Usage:"
echo "---------------"

# Disk usage
if [ -d "$PLATFORM_ROOT/data" ]; then
    DATA_SIZE=$(du -sh "$PLATFORM_ROOT/data" 2>/dev/null | cut -f1)
    echo "  Data directory: $DATA_SIZE"
fi

if [ -d "$PLATFORM_ROOT/logs" ]; then
    LOGS_SIZE=$(du -sh "$PLATFORM_ROOT/logs" 2>/dev/null | cut -f1)
    echo "  Logs directory: $LOGS_SIZE"
fi

# Recent logs
echo ""
echo "Recent Logs (last 5 entries):"
echo "-----------------------------"

if [ -f "$PLATFORM_ROOT/logs/platform.log" ]; then
    tail -5 "$PLATFORM_ROOT/logs/platform.log" 2>/dev/null || echo "  No logs available"
else
    echo "  No log file found"
fi

echo ""
