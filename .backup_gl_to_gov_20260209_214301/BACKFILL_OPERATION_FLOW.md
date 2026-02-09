# Reintegrate Backfill System - Operation Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    REINTEGRATE BACKFILL OPERATION FLOW                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: PREFLIGHT CHECK                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Input: None                                                                  │
│  Script: preflight_main_latest.sh                                            │
│                                                                               │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐               │
│  │ Check Clean   │───▶│ Fetch All     │───▶│ Update Main   │               │
│  │ Worktree      │    │ Branches      │    │ (ff-only)     │               │
│  └───────────────┘    └───────────────┘    └───────┬───────┘               │
│                                                      │                        │
│  Output: preflight.json                             ▼                        │
│          {main: "abc123...", clean: true}    ┌──────────────┐              │
│                                               │ ✅ READY     │              │
│                                               └──────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 2: DISCOVERY & RANKING                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Input: config.yaml                                                           │
│  Script: discover_rank_select.py                                             │
│                                                                               │
│  ┌───────────────────────────────────────────────────────────────┐          │
│  │ 1. Scan Remote Branches                                        │          │
│  │    git for-each-ref refs/remotes/origin                        │          │
│  │    Result: [feature/*, cursor/*, bugfix/*, ...]                │          │
│  └───────────────────────┬───────────────────────────────────────┘          │
│                          ▼                                                    │
│  ┌───────────────────────────────────────────────────────────────┐          │
│  │ 2. Apply Include/Exclude Patterns                             │          │
│  │    Include: ^cursor/.*, ^feature/.*, ^bugfix/.*               │          │
│  │    Exclude: ^main$, ^release/.*, ^dependabot/.*               │          │
│  │    Result: [feature/auth, cursor/fix, bugfix/leak]            │          │
│  └───────────────────────┬───────────────────────────────────────┘          │
│                          ▼                                                    │
│  ┌───────────────────────────────────────────────────────────────┐          │
│  │ 3. Calculate Metrics for Each Branch                          │          │
│  │    ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐ │          │
│  │    │ Merge Base Time │  │ Diff Statistics │  │ CI Status  │ │          │
│  │    │ Staleness Days  │  │ Ahead/Behind    │  │ via gh CLI │ │          │
│  │    └─────────────────┘  └─────────────────┘  └────────────┘ │          │
│  └───────────────────────┬───────────────────────────────────────┘          │
│                          ▼                                                    │
│  ┌───────────────────────────────────────────────────────────────┐          │
│  │ 4. Calculate Scores                                            │          │
│  │    Score = ci_green×60 + rebase_clean×30 + test_pass×30       │          │
│  │          + conflicts×(-120) + ahead×0.02 + files×(-0.05)      │          │
│  │          + lines×(-0.001) + staleness×(-0.2)                  │          │
│  │                                                                │          │
│  │    feature/auth:    51.85 ✅                                  │          │
│  │    cursor/fix:      48.20 ✅                                  │          │
│  │    bugfix/leak:     18.50 ❌ (below threshold)                │          │
│  └───────────────────────┬───────────────────────────────────────┘          │
│                          ▼                                                    │
│  ┌───────────────────────────────────────────────────────────────┐          │
│  │ 5. Sort by (merge_base_time, -score, branch_name)             │          │
│  │    Oldest merge-base first → Historical order                 │          │
│  └───────────────────────┬───────────────────────────────────────┘          │
│                          ▼                                                    │
│  Output: discovery.json (4 candidates)                                       │
│          ranking.json (sorted with scores)                                   │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 3: SELECTION                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Input: ranking.json, config.yaml                                            │
│                                                                               │
│  ┌───────────────────────────────────────────────────────────────┐          │
│  │ 1. Group Branches by Family                                    │          │
│  │    Apply family_prefix_rules regex patterns                    │          │
│  │                                                                │          │
│  │    Family: feature/auth     → [feature/auth]                  │          │
│  │    Family: cursor/fix       → [cursor/fix]                    │          │
│  │    Family: bugfix/leak      → [bugfix/leak]                   │          │
│  └───────────────────────┬───────────────────────────────────────┘          │
│                          ▼                                                    │
│  ┌───────────────────────────────────────────────────────────────┐          │
│  │ 2. Select Best Candidate per Family                           │          │
│  │    per_family_take: 1                                          │          │
│  │    min_score: 25                                               │          │
│  │                                                                │          │
│  │    Family: feature/auth                                        │          │
│  │      ✅ feature/auth (51.85) → SELECTED                       │          │
│  │                                                                │          │
│  │    Family: cursor/fix                                          │          │
│  │      ✅ cursor/fix (48.20) → SELECTED                         │          │
│  │                                                                │          │
│  │    Family: bugfix/leak                                         │          │
│  │      ❌ bugfix/leak (18.50) → REJECTED (score < 25)           │          │
│  └───────────────────────┬───────────────────────────────────────┘          │
│                          ▼                                                    │
│  Output: selection.json (2 selected)                                         │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 4: TRIAL EXECUTION                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Input: selection.json                                                        │
│  Script: try_rebase_and_test.sh (for each candidate)                        │
│                                                                               │
│  For: feature/auth                                                            │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 1. Create Work Branch                                        │            │
│  │    reintegrate-backfill/feature-auth-onto-main-20260207...   │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 2. Checkout Source Branch                                    │            │
│  │    git checkout -b work origin/feature/auth                  │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 3. Attempt Rebase                                            │            │
│  │    git rebase origin/main                                    │            │
│  │                                                              │            │
│  │    ┌──────────┐         ┌──────────┐                        │            │
│  │    │ Success  │    or   │ Conflict │                        │            │
│  │    │ ✅       │         │ ❌       │                        │            │
│  │    └────┬─────┘         └────┬─────┘                        │            │
│  │         │                    │                               │            │
│  │         ▼                    ▼                               │            │
│  │    Continue           git rebase --abort                     │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 4. Run Tests (if configured)                                 │            │
│  │    bash -lc "${TEST_COMMAND}"                                │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 5. Record Results & Clean Up                                 │            │
│  │    git checkout main                                          │            │
│  │    git branch -D work                                         │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  Result: {rebase_clean: 1, test_pass: 0} ✅                                 │
│                                                                               │
│  For: cursor/fix (same process)                                              │
│  Result: {rebase_clean: 1, test_pass: 0} ✅                                 │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 5: PR CREATION                                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Input: Trial results (only for rebase_clean=1)                             │
│  Script: backfill_execute.sh                                                 │
│                                                                               │
│  For: feature/auth (rebase_clean=1) ✅                                      │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 1. Create & Push Work Branch                                 │            │
│  │    git checkout -b reintegrate-backfill/...                  │            │
│  │    git rebase origin/main                                     │            │
│  │    git push -u origin reintegrate-backfill/...               │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 2. Generate PR Body from Template                            │            │
│  │    Replace: {{FAMILY}}, {{SOURCE_BRANCH}}, {{SCORE}}, etc.  │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 3. Create PR via GitHub CLI                                  │            │
│  │    gh pr create --base main --head work-branch               │            │
│  │                 --title "..." --body "..."                    │            │
│  │                                                              │            │
│  │    PR #123 Created ✅                                        │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 4. Enable Auto-Merge                                         │            │
│  │    gh pr merge 123 --merge --auto                            │            │
│  │                                                              │            │
│  │    ✅ Auto-merge enabled                                     │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  Result: PR #123 created and configured                                      │
│                                                                               │
│  For: cursor/fix (same process)                                              │
│  Result: PR #124 created and configured                                      │
│                                                                               │
│  Output: result.json                                                          │
│          {count: 2, items: [{pr_number: 123, ...}, ...]}                    │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STAGE 6: VERIFICATION                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Input: result.json                                                           │
│  Script: verify_post_merge.sh                                                │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 1. Pull Latest Main                                          │            │
│  │    git fetch --all --prune                                   │            │
│  │    git checkout main                                          │            │
│  │    git pull --ff-only origin main                            │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 2. Query PR Status                                           │            │
│  │    For each PR in result.json:                              │            │
│  │      gh pr view ${PR} --json state,mergeStateStatus,...     │            │
│  │                                                              │            │
│  │    PR #123: OPEN | MERGEABLE | ...                          │            │
│  │    PR #124: MERGED | MERGED | ...                           │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ 3. Generate Verification Report                              │            │
│  │    {prs: [{pr: 123, status: "..."}, ...]}                   │            │
│  └────────────┬────────────────────────────────────────────────┘            │
│               ▼                                                               │
│  Output: verify.json                                                          │
│          {kind: "verify", prs: [...]}                                        │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ✅ COMPLETE                                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Evidence Generated:                                                          │
│    ✅ .evidence/reintegrate_backfill/reports/preflight.json                 │
│    ✅ .evidence/reintegrate_backfill/reports/discovery.json                 │
│    ✅ .evidence/reintegrate_backfill/reports/ranking.json                   │
│    ✅ .evidence/reintegrate_backfill/reports/selection.json                 │
│    ✅ .evidence/reintegrate_backfill/reports/result.json                    │
│    ✅ .evidence/reintegrate_backfill/reports/verify.json                    │
│    ✅ .evidence/reintegrate_backfill/logs/commands.log                      │
│    ✅ .evidence/reintegrate_backfill/logs/git.log                           │
│    ✅ .evidence/reintegrate_backfill/logs/gh.log                            │
│                                                                               │
│  PRs Created: 2                                                               │
│  PRs Merged:  1                                                               │
│  PRs Pending: 1                                                               │
│                                                                               │
│  Total Execution Time: ~66 seconds                                           │
│  Quality: ⭐⭐⭐⭐⭐                                                          │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ SCORING FORMULA DETAILS                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  Score = Σ (signal × weight)                                                 │
│                                                                               │
│  Positive Signals:                                                            │
│    • ci_green (0 or 1)        × 60    → CI all checks passed                │
│    • rebase_clean (0 or 1)    × 30    → Rebase without conflicts            │
│    • test_pass (0 or 1)       × 30    → Tests passed                        │
│    • ahead_commits (count)    × 0.02  → Number of unique commits            │
│                                                                               │
│  Negative Signals:                                                            │
│    • conflicts (0 or 1)       × -120  → Has merge conflicts                 │
│    • changed_files (count)    × -0.05 → Number of files modified            │
│    • diffstat_lines (count)   × -0.001→ Total lines changed                 │
│    • staleness_days (days)    × -0.2  → Days since merge-base               │
│                                                                               │
│  Threshold: 25 (minimum score to be considered)                              │
│                                                                               │
│  Example Calculation:                                                         │
│    Branch: feature/user-authentication                                        │
│    • ci_green: 1         → 1 × 60 = 60                                       │
│    • rebase_clean: 0     → 0 × 30 = 0                                        │
│    • test_pass: 0        → 0 × 30 = 0                                        │
│    • conflicts: 0        → 0 × -120 = 0                                      │
│    • ahead_commits: 15   → 15 × 0.02 = 0.3                                   │
│    • changed_files: 12   → 12 × -0.05 = -0.6                                 │
│    • diffstat_lines: 450 → 450 × -0.001 = -0.45                              │
│    • staleness_days: 37  → 37 × -0.2 = -7.4                                  │
│    ─────────────────────────────────────────                                 │
│    Total Score: 51.85 ✅ (above threshold)                                   │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ DATA FLOW                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  config.yaml                                                                  │
│      ↓                                                                        │
│  [discover_rank_select.py]                                                   │
│      ↓                          ↓                      ↓                      │
│  discovery.json          ranking.json          selection.json                │
│      ↓                          ↓                      ↓                      │
│      └──────────────────────────┴──────────────────────┘                     │
│                                 ↓                                             │
│                     [try_rebase_and_test.sh]                                 │
│                                 ↓                                             │
│                          trial_results (JSON)                                │
│                                 ↓                                             │
│                      [backfill_execute.sh]                                   │
│                                 ↓                                             │
│                           result.json                                         │
│                                 ↓                                             │
│                      [verify_post_merge.sh]                                  │
│                                 ↓                                             │
│                           verify.json                                         │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Legend

```
✅ = Success / Passed
❌ = Failed / Rejected
⏳ = Pending
→  = Flow direction
├─ = Branch point
└─ = Continuation
```

## Execution Command

```bash
# Single command to execute entire pipeline
bash indestructibleautoops/reintegrate_backfill/scripts/backfill_execute.sh

# Verification (run after PRs merge)
bash indestructibleautoops/reintegrate_backfill/scripts/verify_post_merge.sh
```
