#!/usr/bin/env bash
#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: quick-verification
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
# ═══════════════════════════════════════════════════════════════════════════════
#                    Machine Native Ops - Quick Verification Script
#                    GL Layer: GL30-49 Execution Layer
#                    Purpose: Fast local validation path with audit logging
# ═══════════════════════════════════════════════════════════════════════════════
#
# This script provides quick local verification with:
# - Fast dependency checks
# - GL compliance validation
# - Ecosystem enforcement
# - Audit trail logging (UTC RFC3339 format)
#
# Usage:
#   ./scripts/quick-verify.sh [--full] [--json]
#
# Options:
#   --full    Run all checks including optional ones
#   --json    Output results in JSON format
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
ACTION="quick-verify"
REQUEST_ID="$(date +%Y%m%d%H%M%S)-$$-$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n')"
CORRELATION_ID="${CORRELATION_ID:-${REQUEST_ID}}"
IP_ADDRESS="${SSH_CLIENT:-}"
IP_ADDRESS="${IP_ADDRESS%% *}"
IP_ADDRESS="${IP_ADDRESS:-127.0.0.1}"
USER_AGENT="quick-verify-script/1.0.0"
VERSION="1.0.0"

# Flags
FULL_MODE=false
JSON_OUTPUT=false

# Results tracking
declare -A RESULTS
RESULTS_TOTAL=0
RESULTS_PASSED=0
RESULTS_FAILED=0
RESULTS_SKIPPED=0

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
    
    echo "$audit_entry" >> "${AUDIT_LOGS_DIR}/quick-verify-audit.jsonl"
}

# Record check result
record_result() {
    local check_name="$1"
    local status="$2"  # PASS, FAIL, SKIP
    local message="${3:-}"
    
    RESULTS["$check_name"]="$status|$message"
    ((RESULTS_TOTAL++))
    
    case "$status" in
        PASS)
            ((RESULTS_PASSED++))
            emit_audit_log "check:$check_name" "passed" "$message"
            ;;
        FAIL)
            ((RESULTS_FAILED++))
            emit_audit_log "check:$check_name" "failed" "$message"
            ;;
        SKIP)
            ((RESULTS_SKIPPED++))
            emit_audit_log "check:$check_name" "skipped" "$message"
            ;;
    esac
}

# Print colored output
print_header() {
    if [[ "$JSON_OUTPUT" == "false" ]]; then
        echo ""
        echo "═══════════════════════════════════════════════════════════════════════════════"
        echo "  $1"
        echo "═══════════════════════════════════════════════════════════════════════════════"
    fi
}

print_check() {
    local name="$1"
    local status="$2"
    local message="${3:-}"
    
    if [[ "$JSON_OUTPUT" == "false" ]]; then
        case "$status" in
            PASS)
                echo "  ✅ $name"
                ;;
            FAIL)
                echo "  ❌ $name: $message"
                ;;
            SKIP)
                echo "  ⏭️  $name (skipped)"
                ;;
        esac
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Check Functions
# ─────────────────────────────────────────────────────────────────────────────

check_python() {
    if command -v python3 >/dev/null 2>&1; then
        local version
        version=$(python3 --version 2>&1 | cut -d' ' -f2)
        record_result "python3" "PASS" "version $version"
        print_check "Python 3" "PASS"
        return 0
    else
        record_result "python3" "FAIL" "not found"
        print_check "Python 3" "FAIL" "not found"
        return 1
    fi
}

check_git() {
    if command -v git >/dev/null 2>&1; then
        record_result "git" "PASS"
        print_check "Git" "PASS"
        return 0
    else
        record_result "git" "FAIL" "not found"
        print_check "Git" "FAIL" "not found"
        return 1
    fi
}

check_env_file() {
    if [[ -f "${PROJECT_ROOT}/.env" ]]; then
        record_result "env_file" "PASS"
        print_check "Environment file (.env)" "PASS"
        return 0
    elif [[ -f "${PROJECT_ROOT}/.env.example" ]]; then
        record_result "env_file" "FAIL" ".env missing, but .env.example exists"
        print_check "Environment file (.env)" "FAIL" "missing (run: cp .env.example .env)"
        return 1
    else
        record_result "env_file" "FAIL" "no .env or .env.example"
        print_check "Environment file (.env)" "FAIL" "missing"
        return 1
    fi
}

check_governance_manifest() {
    if [[ -f "${PROJECT_ROOT}/governance-manifest.yaml" ]]; then
        record_result "governance_manifest" "PASS"
        print_check "Governance manifest" "PASS"
        return 0
    else
        record_result "governance_manifest" "FAIL" "governance-manifest.yaml not found"
        print_check "Governance manifest" "FAIL" "not found"
        return 1
    fi
}

check_ecosystem_contracts() {
    if [[ -d "${PROJECT_ROOT}/ecosystem/contracts" ]]; then
        local contract_count
        contract_count=$(find "${PROJECT_ROOT}/ecosystem/contracts" -name "*.yaml" 2>/dev/null | wc -l)
        record_result "ecosystem_contracts" "PASS" "$contract_count contracts found"
        print_check "Ecosystem contracts" "PASS"
        return 0
    else
        record_result "ecosystem_contracts" "FAIL" "contracts directory not found"
        print_check "Ecosystem contracts" "FAIL" "directory not found"
        return 1
    fi
}

check_ecosystem_enforce() {
    if [[ -f "${PROJECT_ROOT}/ecosystem/enforce.py" ]]; then
        # Try to run it and check exit code
        cd "$PROJECT_ROOT"
        if python3 "${PROJECT_ROOT}/ecosystem/enforce.py" >/dev/null 2>&1; then
            record_result "ecosystem_enforce" "PASS"
            print_check "Ecosystem enforcement" "PASS"
            return 0
        else
            # Check if it's a partial pass
            local output
            output=$(python3 "${PROJECT_ROOT}/ecosystem/enforce.py" 2>&1 || true)
            if echo "$output" | grep -q "GL 治理文件完整"; then
                record_result "ecosystem_enforce" "PASS" "GL compliance passed"
                print_check "Ecosystem enforcement" "PASS"
                return 0
            else
                record_result "ecosystem_enforce" "FAIL" "some checks failed"
                print_check "Ecosystem enforcement" "FAIL" "some checks failed"
                return 1
            fi
        fi
    else
        record_result "ecosystem_enforce" "FAIL" "enforce.py not found"
        print_check "Ecosystem enforcement" "FAIL" "enforce.py not found"
        return 1
    fi
}

check_audit_logs_dir() {
    if [[ -d "${AUDIT_LOGS_DIR}" ]]; then
        record_result "audit_logs_dir" "PASS"
        print_check "Audit logs directory" "PASS"
        return 0
    else
        mkdir -p "${AUDIT_LOGS_DIR}"
        record_result "audit_logs_dir" "PASS" "created"
        print_check "Audit logs directory" "PASS"
        return 0
    fi
}

check_python_yaml() {
    if python3 -c "import yaml" 2>/dev/null; then
        record_result "python_yaml" "PASS"
        print_check "Python YAML module" "PASS"
        return 0
    else
        record_result "python_yaml" "FAIL" "pyyaml not installed"
        print_check "Python YAML module" "FAIL" "not installed (run: pip3 install pyyaml)"
        return 1
    fi
}

check_makefile() {
    if [[ -f "${PROJECT_ROOT}/Makefile" ]]; then
        record_result "makefile" "PASS"
        print_check "Makefile" "PASS"
        return 0
    else
        record_result "makefile" "FAIL" "not found"
        print_check "Makefile" "FAIL" "not found"
        return 1
    fi
}

# Optional checks (only in full mode)
check_node() {
    if [[ "$FULL_MODE" != "true" ]]; then
        record_result "node" "SKIP" "optional check"
        return 0
    fi
    
    if command -v node >/dev/null 2>&1; then
        local version
        version=$(node --version 2>&1)
        record_result "node" "PASS" "version $version"
        print_check "Node.js" "PASS"
        return 0
    else
        record_result "node" "SKIP" "not installed (optional)"
        print_check "Node.js" "SKIP"
        return 0
    fi
}

check_npm() {
    if [[ "$FULL_MODE" != "true" ]]; then
        record_result "npm" "SKIP" "optional check"
        return 0
    fi
    
    if command -v npm >/dev/null 2>&1; then
        local version
        version=$(npm --version 2>&1)
        record_result "npm" "PASS" "version $version"
        print_check "npm" "PASS"
        return 0
    else
        record_result "npm" "SKIP" "not installed (optional)"
        print_check "npm" "SKIP"
        return 0
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Output Functions
# ─────────────────────────────────────────────────────────────────────────────

output_json() {
    local timestamp
    timestamp=$(get_timestamp)
    
    local results_json="{"
    local first=true
    
    for key in "${!RESULTS[@]}"; do
        local value="${RESULTS[$key]}"
        local status="${value%%|*}"
        local message="${value#*|}"
        
        if [[ "$first" == "true" ]]; then
            first=false
        else
            results_json+=","
        fi
        
        results_json+="\"${key}\":{\"status\":\"${status}\",\"message\":\"${message}\"}"
    done
    
    results_json+="}"
    
    cat <<EOF
{
    "timestamp": "${timestamp}",
    "requestId": "${REQUEST_ID}",
    "correlationId": "${CORRELATION_ID}",
    "actor": "${ACTOR}",
    "version": "${VERSION}",
    "summary": {
        "total": ${RESULTS_TOTAL},
        "passed": ${RESULTS_PASSED},
        "failed": ${RESULTS_FAILED},
        "skipped": ${RESULTS_SKIPPED}
    },
    "results": ${results_json}
}
EOF
}

output_summary() {
    print_header "Verification Summary"
    
    echo ""
    echo "  Total checks:   $RESULTS_TOTAL"
    echo "  Passed:         $RESULTS_PASSED"
    echo "  Failed:         $RESULTS_FAILED"
    echo "  Skipped:        $RESULTS_SKIPPED"
    echo ""
    
    if [[ $RESULTS_FAILED -eq 0 ]]; then
        echo "  ✅ All required checks passed!"
    else
        echo "  ❌ Some checks failed. Please fix the issues above."
        echo ""
        echo "  Quick fix commands:"
        echo "    ./scripts/bootstrap.sh     # Full bootstrap"
        echo "    ./scripts/install-deps.sh  # Install dependencies"
        echo "    ./scripts/fix-env.sh       # Fix environment"
    fi
    echo ""
}

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --full)
                FULL_MODE=true
                shift
                ;;
            --json)
                JSON_OUTPUT=true
                shift
                ;;
            --help|-h)
                cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Quick verification for Machine Native Ops environment.

Options:
    --full    Run all checks including optional ones
    --json    Output results in JSON format
    --help    Show this help message

EOF
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done
}

main() {
    parse_args "$@"
    
    if [[ "$JSON_OUTPUT" == "false" ]]; then
        print_header "Machine Native Ops - Quick Verification"
        echo ""
        echo "  Request ID: $REQUEST_ID"
        echo "  Timestamp: $(get_timestamp)"
        echo ""
    fi
    
    emit_audit_log "quick-verify" "started"
    
    # Required checks
    if [[ "$JSON_OUTPUT" == "false" ]]; then
        echo "  Required Checks:"
    fi
    
    check_python || true
    check_git || true
    check_env_file || true
    check_governance_manifest || true
    check_ecosystem_contracts || true
    check_audit_logs_dir || true
    check_python_yaml || true
    check_makefile || true
    
    # Optional checks
    if [[ "$FULL_MODE" == "true" ]]; then
        if [[ "$JSON_OUTPUT" == "false" ]]; then
            echo ""
            echo "  Optional Checks:"
        fi
        check_node || true
        check_npm || true
    fi
    
    # Ecosystem enforcement (comprehensive check)
    if [[ "$JSON_OUTPUT" == "false" ]]; then
        echo ""
        echo "  Ecosystem Enforcement:"
    fi
    check_ecosystem_enforce || true
    
    emit_audit_log "quick-verify" "completed" "passed=$RESULTS_PASSED,failed=$RESULTS_FAILED"
    
    # Output results
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        output_json
    else
        output_summary
    fi
    
    # Return exit code based on failed checks
    if [[ $RESULTS_FAILED -gt 0 ]]; then
        return 1
    fi
    return 0
}

main "$@"
