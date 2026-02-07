#!/usr/bin/env bash
set -euo pipefail

REMOTE="${REMOTE:-origin}"
MAIN_BRANCH="${MAIN_BRANCH:-main}"

LOG_DIR="${LOG_DIR:-.evidence/reintegrate_backfill/logs}"
REP_DIR="${REP_DIR:-.evidence/reintegrate_backfill/reports}"

source "$(dirname "$0")/_lib.sh"

require_bin git
git_root
ensure_clean_worktree

run git fetch --all --prune
run git checkout "${MAIN_BRANCH}"
run git pull --ff-only "${REMOTE}" "${MAIN_BRANCH}"

write_file "${REP_DIR}/preflight.json" "$(python - <<PY
import json,datetime,subprocess
def sh(*a):
  return subprocess.check_output(list(a), text=True).strip()
print(json.dumps({
  "time": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
  "kind": "preflight",
  "main": "${REMOTE}/${MAIN_BRANCH}",
  "head": sh("git","rev-parse","HEAD"),
  "clean": True
}, ensure_ascii=False, indent=2))
PY
)"
