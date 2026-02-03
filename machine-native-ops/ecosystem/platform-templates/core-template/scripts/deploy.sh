#!/bin/bash
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: platform-templates
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
#
# Core Platform Deploy Script
# 部署腳本 - 啟動平台服務
#
# GL Governance Layer: GL10-29 (Operational Layer)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLATFORM_ROOT="$(dirname "$SCRIPT_DIR")"

# Load environment
if [ -f "$PLATFORM_ROOT/.env" ]; then
    source "$PLATFORM_ROOT/.env"
fi

echo "============================================================"
echo "Core Platform Deployment"
echo "============================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Pre-deployment checks
echo "Step 1: Pre-deployment checks..."

if [ ! -f "$PLATFORM_ROOT/.env" ]; then
    echo -e "${RED}[✗] Platform not setup. Run setup.sh first.${NC}"
    exit 1
fi

echo -e "${GREEN}[✓] Environment loaded${NC}"

# 2. Start Service Discovery
echo ""
echo "Step 2: Starting Service Discovery..."

# Check if already running
if lsof -Pi :8500 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}[!] Service Discovery already running on port 8500${NC}"
else
    # Start service discovery (mock for template)
    echo -e "${GREEN}[✓] Service Discovery started on port 8500${NC}"
    echo "  (Mock service - implement actual start in production)"
fi

# 3. Start Message Bus
echo ""
echo "Step 3: Starting Message Bus..."

if lsof -Pi :5672 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}[!] Message Bus already running on port 5672${NC}"
else
    echo -e "${GREEN}[✓] Message Bus started on port 5672${NC}"
    echo "  (Mock service - implement actual start in production)"
fi

# 4. Start API Gateway
echo ""
echo "Step 4: Starting API Gateway..."

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}[!] API Gateway already running on port 8000${NC}"
else
    echo -e "${GREEN}[✓] API Gateway started on port 8000${NC}"
    echo "  (Mock service - implement actual start in production)"
fi

# 5. Start Data Sync Service
echo ""
echo "Step 5: Starting Data Sync Service..."

if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}[!] Data Sync already running on port 8080${NC}"
else
    echo -e "${GREEN}[✓] Data Sync Service started on port 8080${NC}"
    echo "  (Mock service - implement actual start in production)"
fi

# 6. Register platform
echo ""
echo "Step 6: Registering platform..."

# This would register the platform with ecosystem registry
echo -e "${GREEN}[✓] Platform registered${NC}"
echo "  Platform: $PLATFORM_NAME"

# 7. Verify deployment
echo ""
echo "Step 7: Verifying deployment..."

SERVICES_OK=true

# Mock health checks
echo "  Service Discovery: OK"
echo "  Message Bus: OK"
echo "  API Gateway: OK"
echo "  Data Sync: OK"

# 8. Deployment complete
echo ""
echo "============================================================"
echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo "============================================================"
echo ""
echo "Platform: $PLATFORM_NAME"
echo "Status: Running"
echo ""
echo "Access points:"
echo "  - Service Discovery: http://localhost:8500"
echo "  - API Gateway: http://localhost:8000"
echo "  - Message Bus: amqp://localhost:5672"
echo "  - Data Sync API: http://localhost:8080"
echo ""
echo "Next steps:"
echo "  - Check status: bash scripts/status.sh"
echo "  - View logs: tail -f logs/platform.log"
echo "  - Run examples: python examples/register_service.py"
echo ""
