#!/usr/bin/env bash
set -euo pipefail
python3 -m pip install -e . >/dev/null
indestructibleautoops run --config configs/indestructibleautoops.pipeline.yaml --project examples/dirty_project --mode plan
indestructibleautoops run --config configs/indestructibleautoops.pipeline.yaml --project examples/dirty_project --mode verify || true
indestructibleautoops run --config configs/indestructibleautoops.pipeline.yaml --project examples/dirty_project --mode seal