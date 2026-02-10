#!/usr/bin/env bash
#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: enforcement-execution
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
# ═══════════════════════════════════════════════════════════════════════════════
#                    Machine Native Ops - Start Enforcement Script
#                    GL Layer: GL30-49 Execution Layer
#                    Purpose: Run ecosystem enforcement with retry mechanism
# ═══════════════════════════════════════════════════════════════════════════════
#
# This script provides:
# - Automatic retry mechanism (max 3 retries)
# - Dependency verification
# - Layered error codes
# - Alert notification on failure
# - Audit report generation
#
# Exit Codes:
#   0   - Success
#   1   - Warning (non-blocking violations)
#   2   - Blocking error (critical violations)
#   127 - System exception (missing dependencies)
#
# Usage:
#   ./scripts/start_enforcement.sh [--audit] [--auto-fix] [--dry-run]
#
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LOGS_DIR="${PROJECT_ROOT}/logs"
AUDIT_DIR="${LOGS_DIR}/audit_$(date +%Y%m%d_%H%M%S)"
CONFIG_PATH="${CONFIG_PATH:-${PROJECT_ROOT}/ecosystem/governance/governance-monitor-config.yaml}"
LOG_LEVEL="${LOG_LEVEL:-INFO}"

# Retry configuration
MAX_RETRIES=3
RETRY_DELAY=10

# Flags
AUDIT_MODE=false
AUTO_FIX=false
DRY_RUN=false

# Exit codes
EXIT_SUCCESS=0
EXIT_WARNING=1
EXIT_BLOCKING=2
EXIT_SYSTEM_ERROR=127

# ─────────────────────────────────────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────────────────────────────────────

# RFC3339 UTC timestamp
get_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
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

# Check dependencies
check_dependencies() {
    print_info "Checking dependencies..."
    
    local missing=()
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        missing+=("python3")
    fi
    
    # Check required Python packages
    if ! python3 -c "import yaml" 2>/dev/null; then
        missing+=("pyyaml")
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        print_error "Missing dependencies: ${missing[*]}"
        echo ""
        echo "  To install missing dependencies:"
        echo "    pip3 install ${missing[*]}"
        echo "  Or:"
        echo "    ./scripts/install-deps.sh"
        return $EXIT_SYSTEM_ERROR
    fi
    
    print_success "All dependencies available"
    return $EXIT_SUCCESS
}

# Send alert notification
send_alert() {
    local message="$1"
    local channel="${2:---slack-channel=#alerts}"
    
    # Log the alert
    echo "[ALERT] $(get_timestamp) | $message" >> "${LOGS_DIR}/alerts.log"
    
    # In production, this would send to Slack/PagerDuty/etc.
    print_warning "ALERT: $message"
    
    # Example: curl -X POST -d "{\"text\": \"$message\"}" $SLACK_WEBHOOK_URL
}

# Generate audit report
generate_audit_report() {
    local status="$1"
    local violations="$2"
    local timestamp
    timestamp=$(get_timestamp)
    
    mkdir -p "$AUDIT_DIR"
    
    local report_file="${AUDIT_DIR}/audit_report-${timestamp}.json"
    
    cat > "$report_file" <<EOF
{
    "timestamp": "${timestamp}",
    "status": "${status}",
    "version": "1.0.0",
    "executor": "start_enforcement.sh",
    "config_path": "${CONFIG_PATH}",
    "log_level": "${LOG_LEVEL}",
    "violations": ${violations},
    "metadata": {
        "project_root": "${PROJECT_ROOT}",
        "audit_dir": "${AUDIT_DIR}",
        "retry_count": "${retry_counter:-0}",
        "max_retries": "${MAX_RETRIES}"
    }
}
EOF
    
    print_success "Audit report generated: $report_file"
    echo "$report_file"
}

# Run enforcement with retry mechanism
run_enforcement() {
    local retry_counter=0
    local exit_code=$EXIT_SUCCESS
    local violations="[]"
    
    print_header "Machine Native Ops - Governance Enforcement"
    
    echo ""
    echo "  Timestamp: $(get_timestamp)"
    echo "  Config: $CONFIG_PATH"
    echo "  Log Level: $LOG_LEVEL"
    echo "  Max Retries: $MAX_RETRIES"
    echo ""
    
    # Check dependencies first
    if ! check_dependencies; then
        return $EXIT_SYSTEM_ERROR
    fi
    
    # Build command
    local cmd="python3 ${PROJECT_ROOT}/ecosystem/enforce.py"
    
    if [[ "$AUDIT_MODE" == "true" ]]; then
        cmd="$cmd --audit"
    fi
    
    if [[ "$AUTO_FIX" == "true" ]]; then
        cmd="$cmd --auto-fix"
    fi
    
    if [[ "$DRY_RUN" == "true" ]]; then
        print_info "[DRY RUN] Would execute: $cmd"
        return $EXIT_SUCCESS
    fi
    
    # Retry loop with explicit exit code checking
    print_info "Running governance enforcement..."
    
    local success=false
    while [[ $retry_counter -lt $MAX_RETRIES ]]; do
        $cmd 2>&1 | tee "${AUDIT_DIR}/enforce_output.log"
        local cmd_exit=$?
        
        if [[ $cmd_exit -eq 0 ]]; then
            success=true
            break
        fi
        
        retry_counter=$((retry_counter + 1))
        if [[ $retry_counter -lt $MAX_RETRIES ]]; then
            print_warning "Attempt $retry_counter failed (exit code: $cmd_exit). Retrying in ${RETRY_DELAY} seconds..."
            sleep $RETRY_DELAY
        fi
    done
    
    # Check final result
    if [[ "$success" != "true" ]]; then
        print_error "Enforcement failed after $MAX_RETRIES attempts"
        exit_code=$EXIT_BLOCKING
        
        # Send alert
        send_alert "Governance enforcement failed after $MAX_RETRIES retries"
    else
        print_success "Enforcement completed successfully"
        
        # Check for CRITICAL in output
        if [[ -f "${AUDIT_DIR}/enforce_output.log" ]]; then
            if grep -q "CRITICAL" "${AUDIT_DIR}/enforce_output.log"; then
                print_warning "CRITICAL violations detected"
                exit_code=$EXIT_WARNING
                
                # Extract violations using Python for proper JSON parsing
                violations=$(python3 -c "
import json
import sys
try:
    with open('${AUDIT_DIR}/enforce_output.log', 'r') as f:
        content = f.read()
        # Try to find and parse JSON
        import re
        match = re.search(r'\{.*\"violations\".*\}', content, re.DOTALL)
        if match:
            data = json.loads(match.group())
            print(json.dumps(data.get('violations', [])))
        else:
            print('[]')
except:
    print('[]')
" 2>/dev/null || echo "[]")
            fi
        fi
    fi
    
    # Generate audit report
    local report_file
    report_file=$(generate_audit_report "$exit_code" "$violations")
    
    return $exit_code
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --audit)
                AUDIT_MODE=true
                shift
                ;;
            --auto-fix)
                AUTO_FIX=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --help|-h)
                cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Run governance enforcement with retry mechanism.

Options:
    --audit       Enable detailed audit logging
    --auto-fix    Enable automatic violation remediation
    --dry-run     Show what would be executed without running
    --help        Show this help message

Environment Variables:
    CONFIG_PATH   Path to configuration file
    LOG_LEVEL     Logging level (DEBUG, INFO, WARNING, ERROR)

Exit Codes:
    0   - Success
    1   - Warning (non-blocking violations)
    2   - Blocking error (critical violations)
    127 - System exception (missing dependencies)

Examples:
    $(basename "$0")                    # Run enforcement
    $(basename "$0") --audit            # Run with audit logging
    $(basename "$0") --audit --auto-fix # Run with auto-fix enabled

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
    
    # Ensure logs directory exists
    mkdir -p "$LOGS_DIR"
    mkdir -p "$AUDIT_DIR"
    
    # Run enforcement
    local exit_code
    run_enforcement
    exit_code=$?
    
    print_header "Enforcement Complete"
    
    case $exit_code in
        $EXIT_SUCCESS)
            print_success "All governance checks passed"
            ;;
        $EXIT_WARNING)
            print_warning "Enforcement completed with warnings"
            ;;
        $EXIT_BLOCKING)
            print_error "Enforcement failed with blocking errors"
            ;;
        $EXIT_SYSTEM_ERROR)
            print_error "System error during enforcement"
            ;;
        *)
            print_error "Unknown exit code: $exit_code"
            ;;
    esac
    
    echo ""
    echo "  Audit reports: $AUDIT_DIR"
    echo "  Logs: $LOGS_DIR"
    echo ""
    
    return $exit_code
}

main "$@"
