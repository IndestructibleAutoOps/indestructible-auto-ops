#!/bin/bash
#
# Enterprise Governance Framework - Environment Fix Script
# Checks and fixes missing environment variables
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
ENV_FILE="$PROJECT_ROOT/.env"
ENV_EXAMPLE="$PROJECT_ROOT/.env.example"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Environment Configuration Fix${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if .env.example exists
if [ ! -f "$ENV_EXAMPLE" ]; then
    echo -e "${RED}❌ .env.example not found${NC}"
    exit 1
fi

# Create .env if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo "Creating .env from .env.example..."
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    echo -e "${GREEN}✓ .env created${NC}"
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

echo ""
echo -e "${BLUE}Checking environment variables...${NC}"
echo ""

# Variables to check and their default values
declare -A CRITICAL_VARS=(
    ["APP_NAME"]="Enterprise-Governance-Framework"
    ["APP_VERSION"]="1.0.0"
    ["APP_ENV"]="development"
    ["DEBUG"]="true"
    ["LOG_LEVEL"]="INFO"
    ["API_HOST"]="0.0.0.0"
    ["API_PORT"]="8000"
    ["API_WORKERS"]="4"
)

declare -A OPTIONAL_VARS=(
    ["DATABASE_URL"]="postgresql://iaops:change_me@localhost:5432/indestructibleautoops"
    ["REDIS_URL"]="redis://localhost:6379/0"
    ["GOVERNANCE_ENABLED"]="true"
    ["EVIDENCE_DIR"]="./data/evidence"
)

# Function to set variable in .env
set_env_var() {
    local var_name=$1
    local var_value=$2
    
    if grep -q "^${var_name}=" "$ENV_FILE"; then
        # Variable exists, update it
        sed -i "s/^${var_name}=.*/${var_name}=${var_value}/" "$ENV_FILE"
    else
        # Variable doesn't exist, append it
        echo "${var_name}=${var_value}" >> "$ENV_FILE"
    fi
}

# Check and set critical variables
echo -e "${YELLOW}[1] Critical Variables${NC}"
for var_name in "${!CRITICAL_VARS[@]}"; do
    current_value=$(grep "^${var_name}=" "$ENV_FILE" | cut -d'=' -f2- | xargs || echo "")
    
    if [ -z "$current_value" ] || [ "$current_value" = '""' ] || [ "$current_value" = "''" ]; then
        echo -e "   ${YELLOW}Setting${NC} $var_name = ${CRITICAL_VARS[$var_name]}"
        set_env_var "$var_name" "${CRITICAL_VARS[$var_name]}"
    else
        echo -e "   ${GREEN}✓${NC} $var_name = $current_value"
    fi
done

echo ""

# Check optional variables
echo -e "${YELLOW}[2] Optional Variables${NC}"
for var_name in "${!OPTIONAL_VARS[@]}"; do
    current_value=$(grep "^${var_name}=" "$ENV_FILE" | cut -d'=' -f2- | xargs || echo "")
    
    if [ -z "$current_value" ] || [ "$current_value" = '""' ] || [ "$current_value" = "''" ]; then
        echo -e "   ${YELLOW}Setting${NC} $var_name = ${OPTIONAL_VARS[$var_name]}"
        set_env_var "$var_name" "${OPTIONAL_VARS[$var_name]}"
    else
        echo -e "   ${GREEN}✓${NC} $var_name = $current_value"
    fi
done

echo ""

# Generate random secrets
echo -e "${YELLOW}[3] Security Secrets${NC}"

# Generate JWT secret
if ! grep -q "^JWT_SECRET=" "$ENV_FILE" || grep -q "^JWT_SECRET=your-super-secret" "$ENV_FILE"; then
    JWT_SECRET=$(openssl rand -hex 32 2>/dev/null || echo "change-this-jwt-secret-$(date +%s)")
    set_env_var "JWT_SECRET" "$JWT_SECRET"
    echo -e "   ${GREEN}✓${NC} JWT_SECRET generated"
else
    echo -e "   ${GREEN}✓${NC} JWT_SECRET already set"
fi

# Generate API key secret
if ! grep -q "^API_KEY_SECRET=" "$ENV_FILE" || grep -q "^API_KEY_SECRET=your-api-key-secret" "$ENV_FILE"; then
    API_KEY_SECRET=$(openssl rand -hex 32 2>/dev/null || echo "change-this-api-key-secret-$(date +%s)")
    set_env_var "API_KEY_SECRET" "$API_KEY_SECRET"
    echo -e "   ${GREEN}✓${NC} API_KEY_SECRET generated"
else
    echo -e "   ${GREEN}✓${NC} API_KEY_SECRET already set"
fi

echo ""

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Environment Configuration Complete${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}✓ .env file is ready${NC}"
echo ""
echo "Location: $ENV_FILE"
echo ""
echo -e "${YELLOW}Important:${NC}"
echo "1. Review the .env file and update any values as needed"
echo "2. Update sensitive values (API keys, tokens, passwords)"
echo "3. Set the correct environment (APP_ENV: development/staging/production)"
echo ""
echo "Next steps:"
echo "  ./scripts/validate-prereqs.sh  # Validate configuration"
echo "  ./scripts/quick-verify.sh     # Quick verification"
echo "  ./scripts/start-min.sh        # Start services"
echo ""