# Reintegrate Backfill System - Testing Plan

## Test Checklist

### ✅ Phase 1: Static Validation (Completed)

- [x] Directory structure exists
- [x] All required files present
- [x] Scripts have executable permissions
- [x] YAML syntax is valid
- [x] Shell script syntax is valid
- [x] Python script syntax is valid
- [x] Template placeholders exist
- [x] Evidence directories created

### 🔄 Phase 2: Integration Testing (Manual)

To manually test the system, follow these steps:

#### Prerequisites Check

```bash
# Verify required tools
command -v git >/dev/null 2>&1 && echo "✅ git" || echo "❌ git missing"
command -v gh >/dev/null 2>&1 && echo "✅ gh" || echo "❌ gh missing"
command -v python3 >/dev/null 2>&1 && echo "✅ python3" || echo "❌ python3 missing"
python3 -c "import yaml" 2>/dev/null && echo "✅ PyYAML" || echo "❌ PyYAML missing"

# Verify git status
git status --short | grep -q "^" && echo "❌ Working tree dirty" || echo "✅ Working tree clean"
```

#### Test 1: Configuration Loading

```bash
# Test config.yaml parsing
python3 << 'EOF'
import yaml
cfg = yaml.safe_load(open('indestructibleautoops/reintegrate_backfill/config.yaml'))
print(f"✅ Config loaded: {cfg['repo']['main_branch']} @ {cfg['repo']['remote']}")
EOF
```

#### Test 2: Library Functions

```bash
# Test _lib.sh functions
bash -c '
source indestructibleautoops/reintegrate_backfill/scripts/_lib.sh
echo "Testing library functions..."
echo "✅ ts: $(ts)"
echo "✅ LOG_DIR: ${LOG_DIR}"
echo "✅ REP_DIR: ${REP_DIR}"
'
```

#### Test 3: Discover Script (Dry Run)

This requires a clean git state and proper GitHub CLI authentication:

```bash
# Note: This will fetch all branches and analyze them
# It won't make any changes, just generate reports

# Only run if you want to test with real data:
# bash indestructibleautoops/reintegrate_backfill/scripts/preflight_main_latest.sh

# To test discovery without execution:
# python3 indestructibleautoops/reintegrate_backfill/scripts/discover_rank_select.py \
#   indestructibleautoops/reintegrate_backfill/config.yaml \
#   .evidence/reintegrate_backfill/reports/test_discovery.json \
#   .evidence/reintegrate_backfill/reports/test_ranking.json \
#   .evidence/reintegrate_backfill/reports/test_selection.json
```

#### Test 4: Template Rendering

```bash
# Test template variable substitution
bash -c '
template="indestructibleautoops/reintegrate_backfill/templates/pr_body.txt"
body=$(sed \
  -e "s|{{FAMILY}}|test-family|g" \
  -e "s|{{SOURCE_BRANCH}}|feature/test-branch|g" \
  -e "s|{{TARGET_BRANCH}}|main|g" \
  -e "s|{{MODE}}|rebase_then_merge_pr|g" \
  -e "s|{{SCORE}}|85.5|g" \
  -e "s|{{SIGNALS_JSON}}|{\"ci_green\":1}|g" \
  "$template")
echo "$body"
echo "✅ Template rendered successfully"
'
```

### 🚀 Phase 3: End-to-End Testing (Production-like)

⚠️ **WARNING**: These tests will create PRs in the repository. Only run in a test environment.

#### Full Execution Test

```bash
# This will:
# 1. Check git state
# 2. Discover branches
# 3. Rank and select candidates
# 4. Try rebase for each candidate
# 5. Create PRs for successful candidates
# 6. Optionally auto-merge

# bash indestructibleautoops/reintegrate_backfill/scripts/backfill_execute.sh
```

#### Post-Merge Verification

```bash
# This will:
# 1. Pull latest main
# 2. Check PR states from result.json
# 3. Generate verify.json report

# bash indestructibleautoops/reintegrate_backfill/scripts/verify_post_merge.sh
```

### 📊 Expected Outputs

After successful execution, check these files:

```
.evidence/reintegrate_backfill/
├── reports/
│   ├── preflight.json       # ✅ Preflight checks passed
│   ├── discovery.json       # 📋 All discovered branches
│   ├── ranking.json         # 📊 Ranked with scores
│   ├── selection.json       # ⭐ Selected candidates
│   ├── result.json          # ✅ Execution results
│   └── verify.json          # 🔍 Verification status
└── logs/
    ├── commands.log         # 📝 All executed commands
    ├── git.log             # 🔧 Git operations
    └── gh.log              # 🐙 GitHub CLI operations
```

### 🔍 Validation Commands

```bash
# Check reports exist and are valid JSON
for file in .evidence/reintegrate_backfill/reports/*.json; do
  [ -f "$file" ] && python3 -m json.tool "$file" > /dev/null 2>&1 \
    && echo "✅ $(basename $file)" \
    || echo "❌ $(basename $file)"
done

# Check log files exist
for file in .evidence/reintegrate_backfill/logs/*.log; do
  [ -f "$file" ] \
    && echo "✅ $(basename $file) ($(wc -l < $file) lines)" \
    || echo "❌ $(basename $file)"
done
```

### 🛠️ Debugging Tips

1. **Check logs first**: Always look at `.evidence/reintegrate_backfill/logs/commands.log` for execution flow
2. **Validate config**: Ensure `config.yaml` patterns match your branch naming
3. **Test patterns**: Use Python regex testing:
   ```python
   import re
   pattern = re.compile(r"^(cursor/[^/]+)")
   print(pattern.search("cursor/fix-bug"))  # Should match
   ```
4. **Check git state**: Ensure working tree is clean before execution
5. **Verify GitHub CLI**: Run `gh auth status` to check authentication

### 🔄 Rollback Procedures

If something goes wrong:

```bash
# 1. List PRs created by the system
gh pr list --label "reintegrate-backfill" --json number,headRefName,state

# 2. Close a PR and delete its branch
gh pr close <PR_NUMBER> --delete-branch

# 3. Delete a pushed work branch
git push origin :reintegrate-backfill/<branch-name>

# 4. Return to main branch
git checkout main
git pull --ff-only origin main
```

## Test Status

- **Static Validation**: ✅ PASSED (2026-02-07)
- **Integration Testing**: ⏳ PENDING (requires manual execution)
- **End-to-End Testing**: ⏳ PENDING (requires test environment)

## Notes

- All Phase 1 tests passed successfully
- System is ready for Phase 2 integration testing
- Phase 3 should only be run in a controlled test environment
- Review configuration before production use
