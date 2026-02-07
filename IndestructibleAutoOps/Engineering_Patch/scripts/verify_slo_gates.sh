#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SLO_DIR="${SCRIPT_DIR}/../governance/slo"

test -f "${SLO_DIR}/slo.yaml"
test -f "${SLO_DIR}/burnrate_rules.yaml"
test -f "${SLO_DIR}/rollback_trigger.yaml"

echo "slo_pass=true"
