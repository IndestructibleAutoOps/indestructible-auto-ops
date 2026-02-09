#!/usr/bin/env bash
set -euo pipefail

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

run git fetch --all --prune
run git checkout "${MAIN_BRANCH}"
run git pull --ff-only "${REMOTE}" "${MAIN_BRANCH}"

python - <<'PY' > "${REP_DIR}/verify.tsv"
import json
j=json.load(open(".evidence/reintegrate_backfill/reports/result.json","r",encoding="utf-8"))
for it in j.get("items",[]):
  pr=it.get("pr_number")
  if pr:
    print(str(pr))
PY

states=[]
while read -r pr; do
  [ -n "${pr}" ] || continue
  st="$(gh pr view "${pr}" --json state,mergeStateStatus,baseRefName,headRefName --jq '.state+"|"+.mergeStateStatus+"|"+.baseRefName+"|"+.headRefName' 2>/dev/null || true)"
  printf "%s\t%s\n" "${pr}" "${st}" | tee -a "${LOG_DIR}/gh.log" >/dev/null
  states_json="$(python - <<PY
import json
pr="${pr}"
st="${st}"
print(json.dumps({"pr": int(pr), "status": st}, ensure_ascii=False))
PY
)"
  states="$(python - <<PY
import json
arr=json.loads('''${states:-[]}''') if '''${states:-[]}'''.strip().startswith("[") else []
arr.append(json.loads('''${states_json}'''))
print(json.dumps(arr,ensure_ascii=False))
PY
)"
done < "${REP_DIR}/verify.tsv"

write_file "${REP_DIR}/verify.json" "$(python - <<PY
import json,datetime
arr=json.loads('''${states:-[]}''') if '''${states:-[]}'''.strip().startswith("[") else []
print(json.dumps({
  "time": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
  "kind":"verify",
  "main":"${REMOTE}/${MAIN_BRANCH}",
  "prs": arr
}, ensure_ascii=False, indent=2))
PY
)"
