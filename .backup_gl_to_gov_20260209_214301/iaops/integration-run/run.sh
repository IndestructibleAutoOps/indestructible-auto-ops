#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="$ROOT/configs/indestructibleautoops.pipeline.yaml"
PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")/project" && pwd)"

indestructibleautoops clean --state-dir "$PROJECT/.indestructibleautoops" >/dev/null 2>&1 || true

echo "[plan] generating plan"
indestructibleautoops plan --config "$CONFIG" --project "$PROJECT"

echo "[repair] applying patches, verifying, and sealing"
indestructibleautoops run --config "$CONFIG" --project "$PROJECT" --mode repair

echo "[verify] read-only verification"
indestructibleautoops verify --config "$CONFIG" --project "$PROJECT"
