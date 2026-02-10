#!/usr/bin/env bash
set -euo pipefail

REMOTE="${REMOTE:-origin}"
MAIN_BRANCH="${MAIN_BRANCH:-main}"
SOURCE_BRANCH="${1:-}"

TEST_COMMAND="${TEST_COMMAND:-}"
LOG_DIR="${LOG_DIR:-.evidence/reintegrate_backfill/logs}"

source "$(dirname "$0")/_lib.sh"

require_bin git
git_root
ensure_clean_worktree

[ -n "${SOURCE_BRANCH}" ] || die "missing_source_branch"

run git fetch --all --prune
run git checkout "${MAIN_BRANCH}"
run git pull --ff-only "${REMOTE}" "${MAIN_BRANCH}"

run git show-ref --verify --quiet "refs/remotes/${REMOTE}/${SOURCE_BRANCH}" || die "remote_branch_not_found:${REMOTE}/${SOURCE_BRANCH}"

work_branch="reintegrate-backfill/${SOURCE_BRANCH//\//-}-onto-${MAIN_BRANCH}-$(date -u +%Y%m%d%H%M%S)"
run git checkout -b "${work_branch}" "${REMOTE}/${SOURCE_BRANCH}"

rebase_ok=1
if ! git rebase "${REMOTE}/${MAIN_BRANCH}" >> "${LOG_DIR}/git.log" 2>&1; then
  rebase_ok=0
  git rebase --abort >> "${LOG_DIR}/git.log" 2>&1 || true
fi

test_ok=0
if [ "${rebase_ok}" = "1" ] && [ -n "${TEST_COMMAND}" ]; then
  if bash -lc "${TEST_COMMAND}" >> "${LOG_DIR}/git.log" 2>&1; then
    test_ok=1
  else
    test_ok=0
  fi
fi

printf "%s" "$(python - <<PY
import json,datetime
print(json.dumps({
  "time": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
  "kind": "trial",
  "source_branch": "${SOURCE_BRANCH}",
  "work_branch": "${work_branch}",
  "rebase_clean": int(${rebase_ok}),
  "test_pass": int(${test_ok}),
  "test_command": "${TEST_COMMAND}"
}, ensure_ascii=False))
PY
)"
run git checkout "${MAIN_BRANCH}"
run git branch -D "${work_branch}" >/dev/null 2>&1 || true
