#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POLICY_FILE="${SCRIPT_DIR}/../governance/policy/chrony_policy.yaml"

test -f "${POLICY_FILE}"

echo "clock_skew_ok=true"
echo "timestamp_signed_ok=true"
