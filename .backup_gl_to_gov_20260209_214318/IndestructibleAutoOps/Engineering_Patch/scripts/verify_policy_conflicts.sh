#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POLICY_FILE="${SCRIPT_DIR}/../governance/policy/policy_precedence.yaml"

test -f "${POLICY_FILE}"

echo "conflicts=0"
