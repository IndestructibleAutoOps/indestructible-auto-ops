#!/usr/bin/env python3
import json, os, re, subprocess, sys, datetime
import yaml

def sh(*args, check=True):
    p = subprocess.run(list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"cmd_failed:{args}\n{p.stderr}")
    return p.stdout.strip()

def utc():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def parse_cfg(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def compile_patterns(pats):
    return [re.compile(p) for p in (pats or [])]

def allow_branch(name, inc, exc):
    if exc and any(r.search(name) for r in exc):
        return False
    if inc and not any(r.search(name) for r in inc):
        return False
    return True

def family_for(branch, rules):
    for r in rules:
        rgx = re.compile(r["regex"])
        m = rgx.search(branch)
        if m:
            return m.group(1)
    return branch

def safe_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default

def get_remote_branches(remote):
    out = sh("git", "for-each-ref", "--format=%(refname:strip=3)", f"refs/remotes/{remote}")
    names = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.endswith("/HEAD"):
            continue
        names.append(line)
    return sorted(set(names))

def merge_base(main_ref, br_ref):
    return sh("git", "merge-base", main_ref, br_ref)

def commit_unix(ref):
    return safe_int(sh("git", "show", "-s", "--format=%ct", ref), 0)

def ahead_behind(main_ref, br_ref):
    out = sh("git", "rev-list", "--left-right", "--count", f"{main_ref}...{br_ref}")
    left, right = out.split()
    behind = safe_int(left, 0)
    ahead = safe_int(right, 0)
    return ahead, behind

def diff_stats(main_ref, br_ref):
    out = sh("git", "diff", "--numstat", f"{main_ref}...{br_ref}")
    files = 0
    add = 0
    dele = 0
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        a, d, _ = parts[0], parts[1], parts[2]
        if a != "-" and d != "-":
            add += safe_int(a, 0)
            dele += safe_int(d, 0)
        files += 1
    return files, add + dele

def staleness_days(ref):
    sec = commit_unix(ref)
    if sec <= 0:
        return 999999
    dt = datetime.datetime.utcfromtimestamp(sec)
    return int((datetime.datetime.utcnow() - dt).total_seconds() // 86400)

def ci_signal_from_gh(branch, remote, main_branch):
    try:
        q = sh("gh","pr","list","--state","all","--head",branch,"--base",main_branch,"--json","number,state,mergeStateStatus,headRefName,baseRefName,statusCheckRollup","--jq",".[0]")
        if not q:
            return {"has_pr": False, "ci_green": 0, "merge_state": "NONE"}
        j = json.loads(q)
        rollup = j.get("statusCheckRollup") or []
        total = 0
        ok = 0
        for it in rollup:
            total += 1
            c = (it.get("conclusion") or it.get("state") or "").upper()
            if c in ("SUCCESS","NEUTRAL","SKIPPED"):
                ok += 1
        ci_green = 1 if (total > 0 and ok == total) else 0
        return {"has_pr": True, "ci_green": ci_green, "merge_state": (j.get("mergeStateStatus") or "UNKNOWN")}
    except Exception:
        return {"has_pr": False, "ci_green": 0, "merge_state": "UNKNOWN"}

def score(weights, signals):
    s = 0.0
    s += weights.get("ci_green", 0) * signals.get("ci_green", 0)
    s += weights.get("rebase_clean", 0) * signals.get("rebase_clean", 0)
    s += weights.get("test_pass", 0) * signals.get("test_pass", 0)
    s += weights.get("conflicts", 0) * signals.get("conflicts", 0)
    s += weights.get("ahead_commits", 0) * signals.get("ahead_commits", 0)
    s += weights.get("changed_files", 0) * signals.get("changed_files", 0)
    s += weights.get("diffstat_lines", 0) * signals.get("diffstat_lines", 0)
    s += weights.get("staleness_days", 0) * signals.get("staleness_days", 0)
    return s

def main():
    cfg_path = sys.argv[1]
    out_discovery = sys.argv[2]
    out_ranking = sys.argv[3]
    out_selection = sys.argv[4]

    cfg = parse_cfg(cfg_path)
    remote = (cfg.get("repo") or {}).get("remote", "origin")
    main_branch = (cfg.get("repo") or {}).get("main_branch", "main")
    main_ref = f"{remote}/{main_branch}"

    inc = compile_patterns((cfg.get("discovery") or {}).get("include_patterns"))
    exc = compile_patterns((cfg.get("discovery") or {}).get("exclude_patterns"))
    rules = ((cfg.get("grouping") or {}).get("family_prefix_rules") or [])
    weights = ((cfg.get("selection") or {}).get("score_weights") or {})
    min_score = (((cfg.get("selection") or {}).get("thresholds") or {}).get("min_score", 0))

    branches = get_remote_branches(remote)
    candidates = []
    for b in branches:
        if not allow_branch(b, inc, exc):
            continue
        br_ref = f"{remote}/{b}"
        mb = merge_base(main_ref, br_ref)
        mb_ts = commit_unix(mb)
        head_ts = commit_unix(br_ref)
        ahead, behind = ahead_behind(main_ref, br_ref)
        files, lines = diff_stats(main_ref, br_ref)
        stale = staleness_days(br_ref)
        fam = family_for(b, rules)
        ci = ci_signal_from_gh(b, remote, main_branch)
        candidates.append({
            "branch": b,
            "family": fam,
            "refs": {"main": main_ref, "branch": br_ref, "merge_base": mb},
            "time": {"merge_base_unix": mb_ts, "head_unix": head_ts, "staleness_days": stale},
            "diff": {"ahead_commits": ahead, "behind_commits": behind, "changed_files": files, "diffstat_lines": lines},
            "ci": ci
        })

    os.makedirs(os.path.dirname(out_discovery), exist_ok=True)
    with open(out_discovery, "w", encoding="utf-8") as f:
        json.dump({"time": utc(), "kind": "discovery", "remote": remote, "main": main_ref, "candidates": candidates}, f, ensure_ascii=False, indent=2)

    ranked = []
    for c in candidates:
        signals = {
            "ci_green": c["ci"].get("ci_green", 0),
            "rebase_clean": 0,
            "test_pass": 0,
            "conflicts": 0,
            "ahead_commits": c["diff"]["ahead_commits"],
            "changed_files": c["diff"]["changed_files"],
            "diffstat_lines": c["diff"]["diffstat_lines"],
            "staleness_days": c["time"]["staleness_days"],
        }
        sc = score(weights, signals)
        ranked.append({**c, "signals": signals, "score": sc})

    ranked.sort(key=lambda x: (x["time"]["merge_base_unix"], -x["score"], x["branch"]))

    with open(out_ranking, "w", encoding="utf-8") as f:
        json.dump({"time": utc(), "kind": "ranking", "weights": weights, "ranked": ranked}, f, ensure_ascii=False, indent=2)

    selected = []
    per_family_take = (cfg.get("selection") or {}).get("per_family_take", 1)
    fam_map = {}
    for item in ranked:
        fam = item["family"]
        fam_map.setdefault(fam, [])
        fam_map[fam].append(item)

    for fam, items in fam_map.items():
        items2 = sorted(items, key=lambda x: (-x["score"], x["time"]["merge_base_unix"], x["branch"]))
        take = []
        for it in items2:
            if it["score"] < min_score:
                continue
            take.append(it)
            if len(take) >= per_family_take:
                break
        selected.extend(take)

    selected.sort(key=lambda x: (x["time"]["merge_base_unix"], -x["score"], x["branch"]))

    with open(out_selection, "w", encoding="utf-8") as f:
        json.dump({"time": utc(), "kind": "selection", "min_score": min_score, "selected": selected}, f, ensure_ascii=False, indent=2)

    return 0

if __name__ == "__main__":
    sys.exit(main())
