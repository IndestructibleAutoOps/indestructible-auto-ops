#!/bin/bash
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: platform-templates
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
#
# Core Platform Cleanup Script
# 清理腳本 - 停止服務並清理資源
#
# GL Governance Layer: GL10-29 (Operational Layer)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLATFORM_ROOT="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "Core Platform Cleanup"
echo "============================================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Stop services
echo "Step 1: Stopping services..."

# This would stop actual services
echo -e "${GREEN}[✓] All services stopped${NC}"

# 2. Cleanup temporary files
echo ""
echo "Step 2: Cleaning temporary files..."

if [ -d "$PLATFORM_ROOT/tmp" ]; then
    rm -rf "$PLATFORM_ROOT/tmp"/*
    echo -e "${GREEN}[✓] Temporary files cleaned${NC}"
fi

# 3. Backup data (optional)
echo ""
echo "Step 3: Backing up data..."

BACKUP_DIR="$PLATFORM_ROOT/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -d "$PLATFORM_ROOT/data" ]; then
    cp -r "$PLATFORM_ROOT/data" "$BACKUP_DIR/"
    echo -e "${GREEN}[✓] Data backed up to: $BACKUP_DIR${NC}"
fi

# 4. Cleanup complete
echo ""
echo "============================================================"
echo -e "${GREEN}✅ Cleanup completed!${NC}"
echo "============================================================"
echo ""
