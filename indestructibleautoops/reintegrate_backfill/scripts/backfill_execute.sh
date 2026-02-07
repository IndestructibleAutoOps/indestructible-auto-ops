#!/usr/bin/env bash
set -euo pipefail

CFG="${CFG:-indestructibleautoops/reintegrate_backfill/config.yaml}"

REMOTE="${REMOTE:-origin}"
MAIN_BRANCH="${MAIN_BRANCH:-main}"

LOG_DIR="${LOG_DIR:-.evidence/reintegrate_backfill/logs}"
REP_DIR="${REP_DIR:-.evidence/reintegrate_backfill/reports}"

source "$(dirname "$0")/_lib.sh"

require_bin git
require_bin gh
require_bin python

git_root
ensure_clean_worktree

run bash "indestructibleautoops/reintegrate_backfill/scripts/preflight_main_latest.sh"

disc="${REP_DIR}/discovery.json"
rank="${REP_DIR}/ranking.json"
sel="${REP_DIR}/selection.json"

run python "indestructibleautoops/reintegrate_backfill/scripts/discover_rank_select.py" "${CFG}" "${disc}" "${rank}" "${sel}"

test_cmd="$(python - <<'PY'
import yaml
cfg=yaml.safe_load(open("indestructibleautoops/reintegrate_backfill/config.yaml","r",encoding="utf-8"))
print(((cfg.get("execution") or {}).get("test_command") or "").strip())
PY
)"

mode="$(python - <<'PY'
import yaml
cfg=yaml.safe_load(open("indestructibleautoops/reintegrate_backfill/config.yaml","r",encoding="utf-8"))
print(((cfg.get("execution") or {}).get("mode") or "rebase_then_merge_pr").strip())
PY
)"

auto_merge="$(python - <<'PY'
import yaml
cfg=yaml.safe_load(open("indestructibleautoops/reintegrate_backfill/config.yaml","r",encoding="utf-8"))
print("true" if ((cfg.get("execution") or {}).get("auto_merge", True)) else "false")
PY
)"

required_checks="$(python - <<'PY'
import yaml
cfg=yaml.safe_load(open("indestructibleautoops/reintegrate_backfill/config.yaml","r",encoding="utf-8"))
print("true" if ((cfg.get("execution") or {}).get("required_status_checks", True)) else "false")
PY
)"

pr_body_template="indestructibleautoops/reintegrate_backfill/templates/pr_body.txt"

result_items="[]"

python - <<'PY' > "${REP_DIR}/selected.tsv"
import json
j=json.load(open(".evidence/reintegrate_backfill/reports/selection.json","r",encoding="utf-8"))
for it in j.get("selected",[]):
  print("\t".join([
    it.get("family",""),
    it.get("branch",""),
    str(it.get("score",0)),
    json.dumps(it.get("signals",{}), ensure_ascii=False)
  ]))
PY

while IFS=$'\t' read -r family source_branch score signals_json; do
  [ -n "${source_branch}" ] || continue

  export TEST_COMMAND="${test_cmd}"
  trial_json="$(bash "indestructibleautoops/reintegrate_backfill/scripts/try_rebase_and_test.sh" "${source_branch}")"

  rebase_clean="$(python - <<PY
import json
j=json.loads('''${trial_json}''')
print(j.get("rebase_clean",0))
PY
)"
  test_pass="$(python - <<PY
import json
j=json.loads('''${trial_json}''')
print(j.get("test_pass",0))
PY
)"

  if [ "${rebase_clean}" != "1" ]; then
    continue
  fi
  if [ -n "${test_cmd}" ] && [ "${test_pass}" != "1" ]; then
    continue
  fi

  run git fetch --all --prune
  run git checkout "${MAIN_BRANCH}"
  run git pull --ff-only "${REMOTE}" "${MAIN_BRANCH}"

  work_branch="reintegrate-backfill/${source_branch//\//-}-onto-${MAIN_BRANCH}-$(date -u +%Y%m%d%H%M%S)"
  run git checkout -b "${work_branch}" "${REMOTE}/${source_branch}"

  if [ "${mode}" = "rebase_then_merge_pr" ]; then
    run git rebase "${REMOTE}/${MAIN_BRANCH}" | tee -a "${LOG_DIR}/git.log" >/dev/null || die "rebase_conflict:${source_branch}"
  fi

  run git push -u "${REMOTE}" "${work_branch}" | tee -a "${LOG_DIR}/git.log" >/dev/null

  body="$(sed \
    -e "s|{{FAMILY}}|${family}|g" \
    -e "s|{{SOURCE_BRANCH}}|${source_branch}|g" \
    -e "s|{{TARGET_BRANCH}}|${MAIN_BRANCH}|g" \
    -e "s|{{MODE}}|${mode}|g" \
    -e "s|{{SCORE}}|${score}|g" \
    -e "s|{{SIGNALS_JSON}}|${signals_json}|g" \
    "${pr_body_template}")"

  pr_title="reintegrate-backfill: ${family} (${source_branch}) -> ${MAIN_BRANCH}"
  run gh pr create --base "${MAIN_BRANCH}" --head "${work_branch}" --title "${pr_title}" --body "${body}" | tee -a "${LOG_DIR}/gh.log" >/dev/null

  pr_number="$(gh pr view --json number --jq '.number' 2>/dev/null || true)"
  [ -n "${pr_number}" ] || die "pr_create_failed:${source_branch}"

  if [ "${auto_merge}" = "true" ]; then
    if [ "${mode}" = "squash_pr" ]; then
      run gh pr merge "${pr_number}" --squash --auto | tee -a "${LOG_DIR}/gh.log" >/dev/null || true
    else
      run gh pr merge "${pr_number}" --merge --auto | tee -a "${LOG_DIR}/gh.log" >/dev/null || true
    fi
  fi

  item_json="$(python - <<PY
import json,datetime
print(json.dumps({
  "time": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
  "family": "${family}",
  "source_branch": "${source_branch}",
  "target_branch": "${MAIN_BRANCH}",
  "mode": "${mode}",
  "work_branch": "${work_branch}",
  "score": float("${score}"),
  "signals": json.loads('''${signals_json}''') if '''${signals_json}'''.strip().startswith("{") else {},
  "trial": json.loads('''${trial_json}'''),
  "pr_number": int("${pr_number}") if "${pr_number}".isdigit() else None
}, ensure_ascii=False))
PY
)"
  result_items="$(python - <<PY
import json
arr=json.loads('''${result_items}''')
arr.append(json.loads('''${item_json}'''))
print(json.dumps(arr,ensure_ascii=False))
PY
)"

  run git checkout "${MAIN_BRANCH}"
done < "${REP_DIR}/selected.tsv"

write_file "${REP_DIR}/result.json" "$(python - <<PY
import json,datetime
items=json.loads('''${result_items}''')
print(json.dumps({
  "time": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
  "kind":"backfill_result",
  "count": len(items),
  "items": items
}, ensure_ascii=False, indent=2))
PY
)"
