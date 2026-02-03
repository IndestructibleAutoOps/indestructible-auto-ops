#!/bin/bash
# @GL-governed
# @GL-layer: GQS-L7
# @GL-semantic: bootstrap
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json

---
# Bootstrap Script for Governance System
# 治理系統引導腳本
#
# Purpose: 初始化治理環境，安裝依賴，設置配置
# Version: 1.0.0

set -euo pipefail

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日誌函數
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 檢查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 檢查依賴
check_dependencies() {
    log_info "Checking dependencies..."
    
    local missing_deps=()
    
    # 必需依賴
    local required_deps=(
        "git"
        "python3"
        "pip"
        "curl"
        "wget"
    )
    
    # 可選依賴
    local optional_deps=(
        "docker"
        "kubectl"
        "conftest"
        "opa"
        "jq"
    )
    
    # 檢查必需依賴
    for dep in "${required_deps[@]}"; do
        if ! command_exists "$dep"; then
            missing_deps+=("$dep")
        fi
    done
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_error "Please install them before continuing"
        exit 1
    fi
    
    # 檢查可選依賴
    local missing_optional=()
    for dep in "${optional_deps[@]}"; do
        if ! command_exists "$dep"; then
            missing_optional+=("$dep")
        fi
    done
    
    if [ ${#missing_optional[@]} -gt 0 ]; then
        log_warning "Missing optional dependencies: ${missing_optional[*]}"
        log_warning "They will be installed automatically if possible"
    fi
    
    log_success "All required dependencies are installed"
}

# 安裝 Python 依賴
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        # 基礎依賴
        pip install pyyaml jsonschema python-dateutil requests pyjwt
    fi
    
    log_success "Python dependencies installed"
}

# 安裝 Conftest
install_conftest() {
    if command_exists conftest; then
        log_info "Conftest already installed: $(conftest --version)"
        return
    fi
    
    log_info "Installing Conftest..."
    
    local conftest_version="v0.49.0"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget "https://github.com/open-policy-agent/conftest/releases/download/${conftest_version}/conftest_${conftest_version}_Linux_x86_64.tar.gz"
        tar xzf "conftest_${conftest_version}_Linux_x86_64.tar.gz"
        sudo mv conftest /usr/local/bin/
        rm "conftest_${conftest_version}_Linux_x86_64.tar.gz"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew tap open-policy-agent/tap
        brew install conftest
    else
        log_warning "Cannot auto-install Conftest on $OSTYPE"
        log_warning "Please install it manually: https://github.com/open-policy-agent/conftest"
    fi
    
    if command_exists conftest; then
        log_success "Conftest installed: $(conftest --version)"
    fi
}

# 安裝 OPA
install_opa() {
    if command_exists opa; then
        log_info "OPA already installed: $(opa version --format json | jq -r '.version')"
        return
    fi
    
    log_info "Installing OPA..."
    
    local opa_version="v0.61.0"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget "https://openpolicyagent.org/downloads/${opa_version}/opa_linux_amd64"
        sudo mv opa_linux_amd64 /usr/local/bin/opa
        sudo chmod +x /usr/local/bin/opa
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install opa
    else
        log_warning "Cannot auto-install OPA on $OSTYPE"
        log_warning "Please install it manually: https://www.openpolicyagent.org/docs/latest/"
    fi
    
    if command_exists opa; then
        log_success "OPA installed: $(opa version --format json | jq -r '.version')"
    fi
}

# 初始化治理數據庫
init_governance_db() {
    log_info "Initializing governance database..."
    
    local db_dir="ecosystem/governance"
    
    # 創建必要的目錄
    mkdir -p "$db_dir/states"
    mkdir -p "$db_dir/validation"
    mkdir -p "$db_dir/verification"
    mkdir -p "$db_dir/proofs"
    mkdir -p "$db_dir/execution-logs"
    mkdir -p "$db_dir/violations"
    mkdir -p "$db_dir/fixes"
    mkdir -p "$db_dir/reports"
    mkdir -p "$db_dir/artifacts"
    mkdir -p "$db_dir/audit-logs"
    
    # 初始化審計數據庫
    if [ ! -f "$db_dir/audit.db" ]; then
        log_info "Creating audit database..."
        python3 -c "
import sqlite3
from datetime import datetime

db_path = 'ecosystem/governance/audit.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS governance_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT UNIQUE NOT NULL,
    timestamp TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    resource TEXT NOT NULL,
    result TEXT NOT NULL,
    hash TEXT NOT NULL,
    version TEXT NOT NULL,
    request_id TEXT,
    correlation_id TEXT,
    ip TEXT,
    user_agent TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS semantic_violations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    violation_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    classification TEXT NOT NULL,
    message TEXT NOT NULL,
    remediation TEXT,
    timestamp TEXT NOT NULL,
    resolved BOOLEAN DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS audit_trail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    resource TEXT NOT NULL,
    result TEXT NOT NULL,
    hash TEXT NOT NULL,
    version TEXT NOT NULL,
    request_id TEXT,
    correlation_id TEXT,
    ip TEXT,
    user_agent TEXT
)
''')

conn.commit()
conn.close()
print('Audit database created successfully')
"
        log_success "Audit database created"
    fi
    
    log_success "Governance database initialized"
}

# 生成 .env.example
generate_env_example() {
    log_info "Generating .env.example..."
    
    cat > .env.example << 'EOF'
# Governance System Environment Variables
# 治理系統環境變量

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=owner/repo
GITHUB_BRANCH=main

# Governance Configuration
GOVERNANCE_MODE=strict
EVIDENCE_COVERAGE_THRESHOLD=0.95
AUTO_FIX_ENABLED=true
AUTO_MERGE_ENABLED=false

# Database Configuration
AUDIT_DB_PATH=ecosystem/governance/audit.db
STATE_DB_PATH=ecosystem/governance/state.db

# OPA Configuration
OPA_SERVER_URL=http://localhost:8181
OPA_BUNDLE_DIR=ecosystem/contracts/policies/

# Conftest Configuration
CONFTEST_POLICY_DIR=ecosystem/contracts/policies/
CONFTEST_TIMEOUT=30s

# SLA Configuration
SLA_RESPONSE_TIME_THRESHOLD=300
SLA_FIX_RATE_THRESHOLD=0.95
SLA_VIOLATION_ALERT=true

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_OUTPUT=stdout
EOF
    
    log_success ".env.example generated"
}

# 生成啟動報告
generate_bootstrap_report() {
    log_info "Generating bootstrap report..."
    
    local report_file="ecosystem/governance/bootstrap-report-$(date +%Y%m%d-%H%M%S).json"
    
    cat > "$report_file" << EOF
{
  "bootstrap_timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "bootstrap_version": "1.0.0",
  "governance_model": "Governance Quantum Stack (GQS)",
  "gqs_version": "1.0.0",
  "dependencies": {
    "python": "$(python3 --version)",
    "pip": "$(pip --version)",
    "git": "$(git --version)"
  },
  "installed_tools": {
    "conftest": "$(command_exists conftest && conftest --version || echo 'not installed')",
    "opa": "$(command_exists opa && opa version --format json | jq -r '.version' || echo 'not installed')",
    "docker": "$(command_exists docker && docker --version || echo 'not installed')",
    "kubectl": "$(command_exists kubectl && kubectl version --client || echo 'not installed')"
  },
  "directories_created": [
    "ecosystem/governance/states",
    "ecosystem/governance/validation",
    "ecosystem/governance/verification",
    "ecosystem/governance/proofs",
    "ecosystem/governance/execution-logs",
    "ecosystem/governance/violations",
    "ecosystem/governance/fixes",
    "ecosystem/governance/reports",
    "ecosystem/governance/artifacts",
    "ecosystem/governance/audit-logs"
  ],
  "databases_initialized": [
    "ecosystem/governance/audit.db"
  ],
  "configuration_files": [
    ".env.example",
    "ecosystem/contracts/policies/conftest.yaml",
    "ecosystem/contracts/policies/naming-policy.rego"
  ],
  "next_steps": [
    "1. Copy .env.example to .env and configure your environment variables",
    "2. Run 'make test-fast' to verify the installation",
    "3. Run 'scripts/start-min.sh' to start the minimal governance system",
    "4. Review the governance policies in ecosystem/contracts/policies/"
  ]
}
EOF
    
    log_success "Bootstrap report generated: $report_file"
}

# 主函數
main() {
    log_info "=========================================="
    log_info "Governance System Bootstrap"
    log_info "Governance Quantum Stack (GQS) v1.0.0"
    log_info "=========================================="
    
    # 檢查依賴
    check_dependencies
    
    # 安裝 Python 依賴
    install_python_deps
    
    # 安裝工具
    install_conftest
    install_opa
    
    # 初始化治理數據庫
    init_governance_db
    
    # 生成配置文件
    generate_env_example
    
    # 生成報告
    generate_bootstrap_report
    
    log_success "=========================================="
    log_success "Bootstrap completed successfully!"
    log_success "=========================================="
    
    echo ""
    log_info "Next steps:"
    echo "  1. Copy .env.example to .env and configure your environment variables"
    echo "  2. Run 'make test-fast' to verify the installation"
    echo "  3. Run 'scripts/start-min.sh' to start the minimal governance system"
    echo ""
}

# 運行主函數
main "$@"