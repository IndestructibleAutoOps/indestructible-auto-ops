#!/usr/bin/env bash
set -euo pipefail

LOG_DIR="${LOG_DIR:-.evidence/reintegrate_backfill/logs}"
REP_DIR="${REP_DIR:-.evidence/reintegrate_backfill/reports}"
mkdir -p "${LOG_DIR}" "${REP_DIR}"

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }

log_cmd() { printf "[%s] %s\n" "$(ts)" "$*" | tee -a "${LOG_DIR}/commands.log" >/dev/null; }

run() { log_cmd "$*"; "$@" 2>&1 | tee -a "${LOG_DIR}/commands.log" >/dev/null; }

die() { printf "{\"time\":\"%s\",\"level\":\"error\",\"message\":%q}\n" "$(ts)" "$*" >&2; exit 1; }

require_bin() { command -v "$1" >/dev/null 2>&1 || die "missing_binary:$1"; }

git_root() { git rev-parse --show-toplevel >/dev/null 2>&1 || die "not_a_git_repo"; }

ensure_clean_worktree() {
  git update-index -q --refresh
  if ! git diff --quiet || ! git diff --cached --quiet; then
    die "dirty_worktree"
  fi
}

write_file() { local p="$1"; shift; mkdir -p "$(dirname "$p")"; printf "%s" "$*" > "$p"; }
