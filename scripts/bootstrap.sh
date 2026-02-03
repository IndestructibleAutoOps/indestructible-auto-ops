#!/usr/bin/env bash
#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: bootstrap-execution
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
# ═══════════════════════════════════════════════════════════════════════════════
#                    Machine Native Ops - Bootstrap Script
#                    GL Layer: GL30-49 Execution Layer
#                    Purpose: Minimal project bootstrap with audit logging
# ═══════════════════════════════════════════════════════════════════════════════
#
# This script bootstraps the Machine Native Ops environment with:
# - Dependency verification and installation
# - Environment variable validation
# - Audit trail initialization
# - Placeholder generation for missing components
#
# Usage:
#   ./scripts/bootstrap.sh [--quick] [--force] [--audit]
#
# Options:
#   --quick   Skip optional validations for faster startup
#   --force   Force reinstallation of dependencies
#   --audit   Enable detailed audit logging
#
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOGS_DIR="${PROJECT_ROOT}/ecosystem/logs"
AUDIT_LOGS_DIR="${LOGS_DIR}/audit-logs"
ENV_FILE="${PROJECT_ROOT}/.env"
ENV_EXAMPLE="${PROJECT_ROOT}/.env.example"

# Audit fields
ACTOR="${USER:-system}"
ACTION="bootstrap"
REQUEST_ID="$(date +%Y%m%d%H%M%S)-$$-$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n')"
CORRELATION_ID="${CORRELATION_ID:-${REQUEST_ID}}"
IP_ADDRESS="${SSH_CLIENT:-}"
IP_ADDRESS="${IP_ADDRESS%% *}"
IP_ADDRESS="${IP_ADDRESS:-127.0.0.1}"
USER_AGENT="bootstrap-script/1.0.0"
VERSION="1.0.0"

# Flags
QUICK_MODE=false
FORCE_MODE=false
AUDIT_MODE=false

# ─────────────────────────────────────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────────────────────────────────────

# RFC3339 UTC timestamp
get_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# Calculate SHA256 hash
calculate_hash() {
    local content="$1"
    echo -n "$content" | sha256sum | cut -d' ' -f1
}

# Emit audit log in JSONL format (OpenTelemetry compatible)
emit_audit_log() {
    local resource="$1"
    local result="$2"
    local details="${3:-}"
    local timestamp
    timestamp=$(get_timestamp)
    
    # Create content for hash
    local content="${timestamp}|${ACTOR}|${ACTION}|${resource}|${result}"
    local hash
    hash=$(calculate_hash "$content")
    
    # Ensure audit logs directory exists
    mkdir -p "$AUDIT_LOGS_DIR"
    
    # JSONL audit log entry (OpenTelemetry compatible)
    local audit_entry
    audit_entry=$(cat <<EOF
{"timestamp":"${timestamp}","actor":"${ACTOR}","action":"${ACTION}","resource":"${resource}","result":"${result}","hash":"${hash}","version":"${VERSION}","requestId":"${REQUEST_ID}","correlationId":"${CORRELATION_ID}","ip":"${IP_ADDRESS}","userAgent":"${USER_AGENT}","details":"${details}","traceId":"$(head -c 16 /dev/urandom | od -An -tx1 | tr -d ' \n')","spanId":"$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n')"}
EOF
)
    
    # Append to audit log
    echo "$audit_entry" >> "${AUDIT_LOGS_DIR}/bootstrap-audit.jsonl"
    
    if [[ "$AUDIT_MODE" == "true" ]]; then
        echo "[AUDIT] $timestamp | $ACTOR | $ACTION | $resource | $result"
    fi
}

# Print colored output
print_header() {
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  $1"
    echo "═══════════════════════════════════════════════════════════════════════════════"
}

print_step() {
    echo ""
    echo "▶ $1"
}

print_success() {
    echo "  ✅ $1"
}

print_warning() {
    echo "  ⚠️  $1"
}

print_error() {
    echo "  ❌ $1"
}

print_info() {
    echo "  ℹ️  $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check and install system dependencies
check_system_dependencies() {
    print_step "Checking system dependencies..."
    
    local missing=()
    
    # Required tools
    local required_tools=("python3" "pip3" "git")
    
    for tool in "${required_tools[@]}"; do
        if command_exists "$tool"; then
            print_success "$tool is available"
            emit_audit_log "dependency:$tool" "available"
        else
            missing+=("$tool")
            print_error "$tool is missing"
            emit_audit_log "dependency:$tool" "missing"
        fi
    done
    
    # Optional tools
    local optional_tools=("node" "npm" "make")
    
    for tool in "${optional_tools[@]}"; do
        if command_exists "$tool"; then
            print_success "$tool is available (optional)"
            emit_audit_log "dependency:$tool" "available"
        else
            print_warning "$tool is not available (optional)"
            emit_audit_log "dependency:$tool" "missing-optional"
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        print_error "Missing required dependencies: ${missing[*]}"
        print_info "Please install the missing dependencies and try again."
        emit_audit_log "system-dependencies" "failed" "Missing: ${missing[*]}"
        return 1
    fi
    
    emit_audit_log "system-dependencies" "passed"
    return 0
}

# Check Python dependencies
check_python_dependencies() {
    print_step "Checking Python dependencies..."
    
    local requirements_file="${PROJECT_ROOT}/requirements.txt"
    
    if [[ ! -f "$requirements_file" ]]; then
        print_warning "requirements.txt not found, skipping Python dependencies check"
        emit_audit_log "python-dependencies" "skipped" "requirements.txt not found"
        return 0
    fi
    
    # Install Python dependencies
    if [[ "$FORCE_MODE" == "true" ]] || ! python3 -c "import yaml" 2>/dev/null; then
        print_info "Installing Python dependencies..."
        pip3 install --quiet -r "$requirements_file" 2>/dev/null || {
            print_warning "Some Python packages failed to install"
            emit_audit_log "python-dependencies" "partial"
        }
    fi
    
    print_success "Python dependencies checked"
    emit_audit_log "python-dependencies" "passed"
    return 0
}

# Check Node.js dependencies
check_node_dependencies() {
    print_step "Checking Node.js dependencies..."
    
    local package_json="${PROJECT_ROOT}/package.json"
    
    if [[ ! -f "$package_json" ]]; then
        print_warning "package.json not found, skipping Node.js dependencies check"
        emit_audit_log "node-dependencies" "skipped" "package.json not found"
        return 0
    fi
    
    if ! command_exists npm; then
        print_warning "npm not available, skipping Node.js dependencies"
        emit_audit_log "node-dependencies" "skipped" "npm not available"
        return 0
    fi
    
    # Check if node_modules exists
    if [[ ! -d "${PROJECT_ROOT}/node_modules" ]] || [[ "$FORCE_MODE" == "true" ]]; then
        print_info "Installing Node.js dependencies..."
        cd "$PROJECT_ROOT"
        npm install --quiet 2>/dev/null || {
            print_warning "npm install encountered issues"
            emit_audit_log "node-dependencies" "partial"
        }
    fi
    
    print_success "Node.js dependencies checked"
    emit_audit_log "node-dependencies" "passed"
    return 0
}

# Check environment variables
check_environment_variables() {
    print_step "Checking environment variables..."
    
    # Required environment variables
    local required_vars=()
    local optional_vars=("APP_ENV" "APP_DEBUG" "APP_LOG_LEVEL")
    local missing_required=()
    local missing_optional=()
    
    # Check if .env exists
    if [[ ! -f "$ENV_FILE" ]]; then
        print_warning ".env file not found"
        
        # Generate .env from .env.example if available
        if [[ -f "$ENV_EXAMPLE" ]]; then
            print_info "Generating .env from .env.example..."
            cp "$ENV_EXAMPLE" "$ENV_FILE"
            emit_audit_log "env-file" "generated" "Created from .env.example"
            print_success ".env file generated from template"
        else
            print_warning "No .env.example found, environment may not be properly configured"
            emit_audit_log "env-file" "missing" "No .env or .env.example found"
        fi
    fi
    
    # Load .env if it exists
    if [[ -f "$ENV_FILE" ]]; then
        set -a
        # shellcheck source=/dev/null
        source "$ENV_FILE" 2>/dev/null || true
        set +a
    fi
    
    # Check required variables
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            missing_required+=("$var")
            emit_audit_log "env:$var" "missing-required"
        else
            emit_audit_log "env:$var" "present"
        fi
    done
    
    # Check optional variables
    for var in "${optional_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            missing_optional+=("$var")
            emit_audit_log "env:$var" "missing-optional"
        else
            emit_audit_log "env:$var" "present"
        fi
    done
    
    if [[ ${#missing_required[@]} -gt 0 ]]; then
        print_error "Missing required environment variables: ${missing_required[*]}"
        print_info "Run: ./scripts/fix-env.sh to generate placeholder values"
        emit_audit_log "environment-variables" "failed"
        return 1
    fi
    
    if [[ ${#missing_optional[@]} -gt 0 ]]; then
        print_warning "Missing optional environment variables: ${missing_optional[*]}"
    fi
    
    print_success "Environment variables checked"
    emit_audit_log "environment-variables" "passed"
    return 0
}

# Initialize audit trail
init_audit_trail() {
    print_step "Initializing audit trail..."
    
    # Create logs directories
    mkdir -p "$AUDIT_LOGS_DIR"
    
    # Create audit trail database directory
    local db_dir="${AUDIT_LOGS_DIR}"
    
    # Initialize audit metadata
    local init_metadata
    init_metadata=$(cat <<EOF
{
    "initialized_at": "$(get_timestamp)",
    "version": "${VERSION}",
    "actor": "${ACTOR}",
    "requestId": "${REQUEST_ID}",
    "correlationId": "${CORRELATION_ID}"
}
EOF
)
    
    echo "$init_metadata" > "${AUDIT_LOGS_DIR}/audit-metadata.json"
    
    print_success "Audit trail initialized"
    emit_audit_log "audit-trail" "initialized"
    return 0
}

# Validate GL governance compliance
check_gl_compliance() {
    print_step "Checking GL governance compliance..."
    
    if [[ "$QUICK_MODE" == "true" ]]; then
        print_info "Skipping GL compliance check (quick mode)"
        emit_audit_log "gl-compliance" "skipped"
        return 0
    fi
    
    local governance_manifest="${PROJECT_ROOT}/governance-manifest.yaml"
    local contracts_dir="${PROJECT_ROOT}/ecosystem/contracts"
    
    local checks_passed=0
    local checks_total=0
    
    # Check governance manifest
    ((checks_total++))
    if [[ -f "$governance_manifest" ]]; then
        print_success "governance-manifest.yaml exists"
        ((checks_passed++))
        emit_audit_log "gl:governance-manifest" "present"
    else
        print_warning "governance-manifest.yaml not found"
        emit_audit_log "gl:governance-manifest" "missing"
    fi
    
    # Check contracts directory
    ((checks_total++))
    if [[ -d "$contracts_dir" ]]; then
        print_success "ecosystem/contracts directory exists"
        ((checks_passed++))
        emit_audit_log "gl:contracts" "present"
    else
        print_warning "ecosystem/contracts directory not found"
        emit_audit_log "gl:contracts" "missing"
    fi
    
    print_info "GL compliance: $checks_passed/$checks_total checks passed"
    
    if [[ $checks_passed -lt $checks_total ]]; then
        emit_audit_log "gl-compliance" "partial"
        return 0  # Non-fatal
    fi
    
    emit_audit_log "gl-compliance" "passed"
    return 0
}

# Generate placeholder files if missing
generate_placeholders() {
    print_step "Checking for missing placeholders..."
    
    local generated=0
    
    # Check and generate mock service placeholder
    local mock_services_dir="${PROJECT_ROOT}/ecosystem/mocks"
    if [[ ! -d "$mock_services_dir" ]]; then
        mkdir -p "$mock_services_dir"
        
        # Create mock service placeholder
        cat > "${mock_services_dir}/README.md" <<'EOF'
# Mock Services

This directory contains mock services for local development and testing.

## Structure

```
mocks/
├── api/           # Mock API responses
├── data/          # Fake data generators
└── services/      # Mock service implementations
```

## Usage

Mock services are automatically loaded when `DEV_MOCK_EXTERNAL_SERVICES=true`
is set in `.env`.

EOF
        ((generated++))
        emit_audit_log "placeholder:mock-services" "generated"
    fi
    
    if [[ $generated -gt 0 ]]; then
        print_success "Generated $generated placeholder(s)"
    else
        print_info "No placeholders needed"
    fi
    
    emit_audit_log "placeholders" "checked"
    return 0
}

# Print usage
print_usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Bootstrap the Machine Native Ops environment.

Options:
    --quick     Skip optional validations for faster startup
    --force     Force reinstallation of dependencies
    --audit     Enable detailed audit logging
    --help      Show this help message

Examples:
    $(basename "$0")                # Standard bootstrap
    $(basename "$0") --quick        # Quick bootstrap (minimal checks)
    $(basename "$0") --force        # Force reinstall all dependencies
    $(basename "$0") --audit        # Bootstrap with verbose audit logging

EOF
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --quick)
                QUICK_MODE=true
                shift
                ;;
            --force)
                FORCE_MODE=true
                shift
                ;;
            --audit)
                AUDIT_MODE=true
                shift
                ;;
            --help|-h)
                print_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done
}

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

main() {
    parse_args "$@"
    
    print_header "Machine Native Ops - Bootstrap"
    
    echo ""
    echo "  Request ID: $REQUEST_ID"
    echo "  Actor: $ACTOR"
    echo "  Timestamp: $(get_timestamp)"
    echo ""
    
    emit_audit_log "bootstrap" "started"
    
    local exit_code=0
    
    # Initialize audit trail first
    init_audit_trail || exit_code=1
    
    # Check system dependencies
    check_system_dependencies || exit_code=1
    
    # Check Python dependencies
    check_python_dependencies || exit_code=1
    
    # Check Node.js dependencies
    if [[ "$QUICK_MODE" != "true" ]]; then
        check_node_dependencies || true  # Non-fatal
    fi
    
    # Check environment variables
    check_environment_variables || exit_code=1
    
    # Check GL compliance
    check_gl_compliance || true  # Non-fatal
    
    # Generate placeholders
    generate_placeholders || true  # Non-fatal
    
    print_header "Bootstrap Complete"
    
    if [[ $exit_code -eq 0 ]]; then
        print_success "All required checks passed"
        emit_audit_log "bootstrap" "completed"
        echo ""
        echo "  Next steps:"
        echo "    1. Review .env configuration"
        echo "    2. Run './scripts/quick-verify.sh' to validate setup"
        echo "    3. Run 'make test-fast' for quick tests"
        echo ""
    else
        print_error "Some required checks failed"
        emit_audit_log "bootstrap" "failed"
        echo ""
        echo "  Fix the issues above and run bootstrap again."
        echo "  For environment issues: ./scripts/fix-env.sh"
        echo "  For dependency issues: ./scripts/install-deps.sh"
        echo ""
    fi
    
    return $exit_code
}

main "$@"
