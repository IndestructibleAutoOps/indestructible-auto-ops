#!/usr/bin/env bash
#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: minimal-startup
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
# ═══════════════════════════════════════════════════════════════════════════════
#                    Machine Native Ops - Minimal Startup Script
#                    GL Layer: GL30-49 Execution Layer
#                    Purpose: Minimal execution with audit trail
# ═══════════════════════════════════════════════════════════════════════════════
#
# This script provides a minimal startup path with:
# - Dependency detection and missing component reporting
# - Automatic placeholder generation
# - Audit trail logging (UTC RFC3339 format)
# - OpenTelemetry/JSONL compatible logging
#
# Usage:
#   ./scripts/start-min.sh [--verify-only] [--generate-mocks]
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
ACTION="start-min"
REQUEST_ID="$(date +%Y%m%d%H%M%S)-$$-$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n')"
CORRELATION_ID="${CORRELATION_ID:-${REQUEST_ID}}"
IP_ADDRESS="${SSH_CLIENT:-}"
IP_ADDRESS="${IP_ADDRESS%% *}"
IP_ADDRESS="${IP_ADDRESS:-127.0.0.1}"
USER_AGENT="start-min-script/1.0.0"
VERSION="1.0.0"

# Flags
VERIFY_ONLY=false
GENERATE_MOCKS=false

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
    
    # JSONL audit log entry
    local audit_entry
    audit_entry=$(cat <<EOF
{"timestamp":"${timestamp}","actor":"${ACTOR}","action":"${ACTION}","resource":"${resource}","result":"${result}","hash":"${hash}","version":"${VERSION}","requestId":"${REQUEST_ID}","correlationId":"${CORRELATION_ID}","ip":"${IP_ADDRESS}","userAgent":"${USER_AGENT}","details":"${details}","traceId":"$(head -c 16 /dev/urandom | od -An -tx1 | tr -d ' \n')","spanId":"$(head -c 8 /dev/urandom | od -An -tx1 | tr -d ' \n')"}
EOF
)
    
    echo "$audit_entry" >> "${AUDIT_LOGS_DIR}/start-min-audit.jsonl"
}

# Print colored output
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

# Check minimum requirements
check_minimum_requirements() {
    local missing=()
    
    # Minimum required: python3
    if ! command -v python3 >/dev/null 2>&1; then
        missing+=("python3")
    fi
    
    # Check if git is available
    if ! command -v git >/dev/null 2>&1; then
        missing+=("git")
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        print_error "Missing minimum requirements: ${missing[*]}"
        emit_audit_log "minimum-requirements" "failed" "Missing: ${missing[*]}"
        return 1
    fi
    
    emit_audit_log "minimum-requirements" "passed"
    return 0
}

# Detect missing dependencies and report
detect_missing_dependencies() {
    local missing_deps=()
    local missing_env=()
    
    # Check Python packages
    local python_packages=("yaml" "json" "pathlib")
    for pkg in "${python_packages[@]}"; do
        if ! python3 -c "import $pkg" 2>/dev/null; then
            if [[ "$pkg" == "yaml" ]]; then
                missing_deps+=("pyyaml")
            fi
        fi
    done
    
    # Check environment file
    if [[ ! -f "${PROJECT_ROOT}/.env" ]]; then
        missing_env+=(".env file")
    fi
    
    # Report missing items
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        print_warning "Missing dependencies: ${missing_deps[*]}"
        emit_audit_log "dependencies" "missing" "${missing_deps[*]}"
        
        # Generate fix script suggestion
        echo ""
        echo "  To fix missing dependencies, run:"
        echo "    pip3 install ${missing_deps[*]}"
        echo "  Or:"
        echo "    ./scripts/install-deps.sh"
        echo ""
    fi
    
    if [[ ${#missing_env[@]} -gt 0 ]]; then
        print_warning "Missing environment configuration"
        emit_audit_log "environment" "missing"
        
        echo ""
        echo "  To fix missing environment, run:"
        echo "    cp .env.example .env"
        echo "  Or:"
        echo "    ./scripts/fix-env.sh"
        echo ""
    fi
    
    # Return status
    if [[ ${#missing_deps[@]} -gt 0 ]] || [[ ${#missing_env[@]} -gt 0 ]]; then
        return 1
    fi
    
    return 0
}

# Generate mock services
generate_mock_services() {
    print_info "Generating mock services..."
    
    local mocks_dir="${PROJECT_ROOT}/ecosystem/mocks"
    mkdir -p "${mocks_dir}/api"
    mkdir -p "${mocks_dir}/data"
    mkdir -p "${mocks_dir}/services"
    
    # Generate mock API responses
    cat > "${mocks_dir}/api/health.json" <<'EOF'
{
    "status": "healthy",
    "timestamp": "2026-02-03T00:00:00Z",
    "version": "1.0.0-mock",
    "services": {
        "database": "mock",
        "cache": "mock",
        "queue": "mock"
    }
}
EOF
    
    # Generate mock data
    cat > "${mocks_dir}/data/sample-users.json" <<'EOF'
[
    {"id": 1, "name": "Test User 1", "email": "user1@test.local"},
    {"id": 2, "name": "Test User 2", "email": "user2@test.local"},
    {"id": 3, "name": "Test User 3", "email": "user3@test.local"}
]
EOF
    
    # Generate mock service
    cat > "${mocks_dir}/services/mock_service.py" <<'EOF'
#!/usr/bin/env python3
"""
Mock Service for Local Development
===================================
GL Layer: GL30-49 Execution Layer

This mock service simulates external dependencies for local development.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class MockService:
    """Mock service implementation."""
    
    def __init__(self, mock_data_dir: Optional[str] = None):
        """Initialize mock service."""
        self.mock_data_dir = Path(mock_data_dir or Path(__file__).parent.parent / "data")
    
    def get_health(self) -> Dict[str, Any]:
        """Get mock health status."""
        return {
            "status": "healthy",
            "mock": True,
            "version": "1.0.0-mock"
        }
    
    def get_users(self) -> list:
        """Get mock users."""
        users_file = self.mock_data_dir / "sample-users.json"
        if users_file.exists():
            with open(users_file) as f:
                return json.load(f)
        return []
    
    def simulate_response(self, endpoint: str, method: str = "GET") -> Dict[str, Any]:
        """Simulate an API response."""
        return {
            "success": True,
            "endpoint": endpoint,
            "method": method,
            "mock": True,
            "data": {}
        }


def get_mock_service() -> MockService:
    """Get mock service instance."""
    return MockService()


if __name__ == "__main__":
    service = get_mock_service()
    print(json.dumps(service.get_health(), indent=2))
EOF
    
    print_success "Mock services generated in ecosystem/mocks/"
    emit_audit_log "mock-services" "generated"
}

# Run minimal ecosystem verification
run_minimal_verification() {
    print_info "Running minimal ecosystem verification..."
    
    cd "$PROJECT_ROOT"
    
    # Check GL compliance
    if [[ -f "${PROJECT_ROOT}/ecosystem/enforce.py" ]]; then
        print_info "Running ecosystem enforcement check..."
        python3 "${PROJECT_ROOT}/ecosystem/enforce.py" 2>&1 || {
            print_warning "Ecosystem enforcement check had issues (non-fatal)"
            emit_audit_log "ecosystem-enforce" "warning"
        }
    else
        print_warning "ecosystem/enforce.py not found"
        emit_audit_log "ecosystem-enforce" "missing"
    fi
    
    emit_audit_log "minimal-verification" "completed"
    return 0
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --verify-only)
                VERIFY_ONLY=true
                shift
                ;;
            --generate-mocks)
                GENERATE_MOCKS=true
                shift
                ;;
            --help|-h)
                cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Minimal startup for Machine Native Ops.

Options:
    --verify-only     Only verify environment, don't start anything
    --generate-mocks  Generate mock services for local development
    --help            Show this help message

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
    
    print_header "Machine Native Ops - Minimal Startup"
    
    echo ""
    echo "  Request ID: $REQUEST_ID"
    echo "  Timestamp: $(get_timestamp)"
    echo ""
    
    emit_audit_log "start-min" "started"
    
    # Check minimum requirements
    if ! check_minimum_requirements; then
        print_error "Minimum requirements not met"
        exit 1
    fi
    print_success "Minimum requirements satisfied"
    
    # Detect and report missing dependencies
    if ! detect_missing_dependencies; then
        print_warning "Some dependencies are missing (see above for fix instructions)"
        
        if [[ "$GENERATE_MOCKS" == "true" ]]; then
            generate_mock_services
        fi
        
        if [[ "$VERIFY_ONLY" != "true" ]]; then
            echo ""
            print_info "Continuing with available components..."
        fi
    else
        print_success "All dependencies available"
    fi
    
    # Generate mocks if requested
    if [[ "$GENERATE_MOCKS" == "true" ]]; then
        generate_mock_services
    fi
    
    # Run minimal verification
    if [[ "$VERIFY_ONLY" == "true" ]]; then
        run_minimal_verification
        print_header "Verification Complete"
        emit_audit_log "start-min" "verification-completed"
    else
        print_header "Minimal Startup Complete"
        emit_audit_log "start-min" "completed"
        
        echo ""
        echo "  Environment is ready for development."
        echo ""
        echo "  Quick commands:"
        echo "    make test-fast          # Run quick tests"
        echo "    ./scripts/quick-verify.sh   # Verify setup"
        echo "    python ecosystem/enforce.py # Run governance checks"
        echo ""
    fi
    
    return 0
}

main "$@"
