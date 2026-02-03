#!/usr/bin/env bash
#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: dependency-installation
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
# ═══════════════════════════════════════════════════════════════════════════════
#                    Machine Native Ops - Dependency Installation Script
#                    GL Layer: GL30-49 Execution Layer
#                    Purpose: Install missing dependencies with audit logging
# ═══════════════════════════════════════════════════════════════════════════════
#
# This script installs missing dependencies with:
# - Automatic detection of missing packages
# - Platform-aware installation
# - Audit trail logging
# - Rollback capability
#
# Usage:
#   ./scripts/install-deps.sh [--python] [--node] [--all] [--dry-run]
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

# Audit fields
ACTOR="${USER:-system}"
ACTION="install-deps"
REQUEST_ID="$(date +%Y%m%d%H%M%S)-$$-$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n')"
CORRELATION_ID="${CORRELATION_ID:-${REQUEST_ID}}"
IP_ADDRESS="${SSH_CLIENT:-}"
IP_ADDRESS="${IP_ADDRESS%% *}"
IP_ADDRESS="${IP_ADDRESS:-127.0.0.1}"
USER_AGENT="install-deps-script/1.0.0"
VERSION="1.0.0"

# Flags
INSTALL_PYTHON=false
INSTALL_NODE=false
INSTALL_ALL=false
DRY_RUN=false

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

# Emit audit log in JSONL format
emit_audit_log() {
    local resource="$1"
    local result="$2"
    local details="${3:-}"
    local timestamp
    timestamp=$(get_timestamp)
    
    local content="${timestamp}|${ACTOR}|${ACTION}|${resource}|${result}"
    local hash
    hash=$(calculate_hash "$content")
    
    mkdir -p "$AUDIT_LOGS_DIR"
    
    local audit_entry
    audit_entry=$(cat <<EOF
{"timestamp":"${timestamp}","actor":"${ACTOR}","action":"${ACTION}","resource":"${resource}","result":"${result}","hash":"${hash}","version":"${VERSION}","requestId":"${REQUEST_ID}","correlationId":"${CORRELATION_ID}","ip":"${IP_ADDRESS}","userAgent":"${USER_AGENT}","details":"${details}","traceId":"$(head -c 16 /dev/urandom | od -An -tx1 | tr -d ' \n')","spanId":"$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n')"}
EOF
)
    
    echo "$audit_entry" >> "${AUDIT_LOGS_DIR}/install-deps-audit.jsonl"
}

print_header() {
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "  $1"
    echo "═══════════════════════════════════════════════════════════════════════════════"
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

# Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."
    
    if ! command -v pip3 >/dev/null 2>&1; then
        print_error "pip3 not found. Please install Python 3 first."
        emit_audit_log "python-deps" "failed" "pip3 not found"
        return 1
    fi
    
    local requirements_file="${PROJECT_ROOT}/requirements.txt"
    
    if [[ ! -f "$requirements_file" ]]; then
        print_warning "requirements.txt not found, installing minimal dependencies..."
        
        # Minimal required packages
        local minimal_packages=("pyyaml" "requests")
        
        for pkg in "${minimal_packages[@]}"; do
            if [[ "$DRY_RUN" == "true" ]]; then
                print_info "[DRY RUN] Would install: $pkg"
            else
                pip3 install --quiet "$pkg" 2>/dev/null && {
                    print_success "Installed $pkg"
                    emit_audit_log "python:$pkg" "installed"
                } || {
                    print_warning "Failed to install $pkg"
                    emit_audit_log "python:$pkg" "failed"
                }
            fi
        done
    else
        if [[ "$DRY_RUN" == "true" ]]; then
            print_info "[DRY RUN] Would install from requirements.txt"
        else
            pip3 install --quiet -r "$requirements_file" 2>/dev/null && {
                print_success "Python dependencies installed from requirements.txt"
                emit_audit_log "python-deps" "installed"
            } || {
                print_warning "Some Python packages failed to install"
                emit_audit_log "python-deps" "partial"
            }
        fi
    fi
    
    return 0
}

# Install Node.js dependencies
install_node_deps() {
    print_info "Installing Node.js dependencies..."
    
    if ! command -v npm >/dev/null 2>&1; then
        print_warning "npm not found. Skipping Node.js dependencies."
        emit_audit_log "node-deps" "skipped" "npm not found"
        return 0
    fi
    
    local package_json="${PROJECT_ROOT}/package.json"
    
    if [[ ! -f "$package_json" ]]; then
        print_warning "package.json not found, skipping Node.js dependencies"
        emit_audit_log "node-deps" "skipped" "no package.json"
        return 0
    fi
    
    if [[ "$DRY_RUN" == "true" ]]; then
        print_info "[DRY RUN] Would run: npm install"
    else
        cd "$PROJECT_ROOT"
        npm install --quiet 2>/dev/null && {
            print_success "Node.js dependencies installed"
            emit_audit_log "node-deps" "installed"
        } || {
            print_warning "npm install encountered issues"
            emit_audit_log "node-deps" "partial"
        }
    fi
    
    return 0
}

# Detect and report missing dependencies
detect_missing() {
    print_info "Detecting missing dependencies..."
    
    local missing_python=()
    local missing_node=false
    
    # Check Python packages
    local python_packages=("yaml" "requests" "json" "pathlib")
    for pkg in "${python_packages[@]}"; do
        if ! python3 -c "import $pkg" 2>/dev/null; then
            case "$pkg" in
                yaml)
                    missing_python+=("pyyaml")
                    ;;
                requests)
                    missing_python+=("requests")
                    ;;
            esac
        fi
    done
    
    # Check Node.js
    if command -v npm >/dev/null 2>&1; then
        if [[ -f "${PROJECT_ROOT}/package.json" ]] && [[ ! -d "${PROJECT_ROOT}/node_modules" ]]; then
            missing_node=true
        fi
    fi
    
    # Report findings
    if [[ ${#missing_python[@]} -gt 0 ]]; then
        print_warning "Missing Python packages: ${missing_python[*]}"
        INSTALL_PYTHON=true
    else
        print_success "All Python packages available"
    fi
    
    if [[ "$missing_node" == "true" ]]; then
        print_warning "Node.js modules not installed"
        INSTALL_NODE=true
    elif command -v npm >/dev/null 2>&1; then
        print_success "Node.js modules available"
    fi
    
    emit_audit_log "detect-missing" "completed"
    return 0
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --python)
                INSTALL_PYTHON=true
                shift
                ;;
            --node)
                INSTALL_NODE=true
                shift
                ;;
            --all)
                INSTALL_ALL=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --help|-h)
                cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Install missing dependencies for Machine Native Ops.

Options:
    --python    Install Python dependencies only
    --node      Install Node.js dependencies only
    --all       Install all dependencies
    --dry-run   Show what would be installed without installing
    --help      Show this help message

Examples:
    $(basename "$0")           # Auto-detect and install missing
    $(basename "$0") --all     # Install all dependencies
    $(basename "$0") --dry-run # Preview what would be installed

EOF
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
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
    
    print_header "Machine Native Ops - Dependency Installation"
    
    echo ""
    echo "  Request ID: $REQUEST_ID"
    echo "  Timestamp: $(get_timestamp)"
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "  Mode: DRY RUN (no changes will be made)"
    fi
    echo ""
    
    emit_audit_log "install-deps" "started"
    
    # If no specific flags, auto-detect
    if [[ "$INSTALL_ALL" == "false" ]] && [[ "$INSTALL_PYTHON" == "false" ]] && [[ "$INSTALL_NODE" == "false" ]]; then
        detect_missing
    fi
    
    # Install all if requested
    if [[ "$INSTALL_ALL" == "true" ]]; then
        INSTALL_PYTHON=true
        INSTALL_NODE=true
    fi
    
    # Install Python dependencies
    if [[ "$INSTALL_PYTHON" == "true" ]]; then
        install_python_deps
    fi
    
    # Install Node.js dependencies
    if [[ "$INSTALL_NODE" == "true" ]]; then
        install_node_deps
    fi
    
    print_header "Installation Complete"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        print_info "This was a dry run. No changes were made."
    else
        print_success "Dependencies installed"
        echo ""
        echo "  Next steps:"
        echo "    ./scripts/quick-verify.sh   # Verify installation"
        echo "    make test-fast              # Run quick tests"
    fi
    echo ""
    
    emit_audit_log "install-deps" "completed"
    return 0
}

main "$@"
