#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"${SCRIPT_DIR}/verify_policy_conflicts.sh"
"${SCRIPT_DIR}/verify_slo_gates.sh"
"${SCRIPT_DIR}/verify_drift.sh"
"${SCRIPT_DIR}/verify_time_integrity.sh"
"${SCRIPT_DIR}/verify_artifact_coverage.sh"

echo "ALL_VERIFICATIONS_PASS=true"
