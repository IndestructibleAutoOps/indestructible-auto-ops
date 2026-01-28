# Deployment Guide: Infrastructure Validation Hotfix

## Overview
This guide provides step-by-step instructions for deploying the hotfix to resolve intermittent CI/CD failures in the infrastructure validation workflow.

**What's in This PR:**
- Validation scripts in the `scripts/` directory (copied from `engine/scripts-legacy/`)
- Documentation updates (DEPLOYMENT_GUIDE.md, QUICK_REFERENCE.md, BUG_FIX_COMPLETION_REPORT.md)

**What Was Added Previously:**
- The `.github/workflows/infrastructure-validation.yml` workflow file (commit 600a8a4)

This PR completes the infrastructure validation fix by adding the required scripts that the workflow references.

## Prerequisites
- Git access to MachineNativeOps/machine-native-ops repository
- GitHub Personal Access Token with repo permissions
- Local copy of the repository

## Deployment Steps

### Step 1: Verify Local Changes
```bash
cd machine-native-ops
git status
```

Expected output should show:
- New directory: `scripts/` (with validation scripts)
- New file: `scripts/validate-infrastructure.sh`
- New file: `scripts/validate-module-manifests.py`
- New file: `scripts/validate-module-registry.py`
- New file: `scripts/generate-governance-dashboard.py`
- New file: `scripts/generate-dag-visualization.py`
- Modified: `DEPLOYMENT_GUIDE.md` (this file)
- Modified: `QUICK_REFERENCE.md`
- Modified: `BUG_FIX_COMPLETION_REPORT.md`

Note: The `.github/workflows/infrastructure-validation.yml` file was added in a previous commit (600a8a4) and is not modified by this PR.

### Step 2: Review Changes
```bash
# View the main validation script
cat scripts/validate-infrastructure.sh

# List all new scripts
ls -la scripts/

# View the bug fix summary
cat BUG_FIX_COMPLETION_REPORT.md

# Review the workflow file (added in previous commit 600a8a4)
cat .github/workflows/infrastructure-validation.yml
```

### Step 3: Test Locally (Optional)
```bash
# Ensure dependencies are installed
pip install pyyaml jsonschema

# Run validation script
./scripts/validate-infrastructure.sh

# Expected: All validations should pass with ✅ indicators
```

### Step 4: Push Branch to Remote
```bash
# Ensure you're authenticated with GitHub before pushing:
# - Recommended: use GitHub CLI (`gh auth login`) or
# - Use Git credential helper with HTTPS, or
# - Use SSH keys configured for your GitHub account.

# Option A: HTTPS remote (credentials managed by gh or Git credential helper)
git remote set-url origin https://github.com/MachineNativeOps/machine-native-ops.git
git push origin hotfix/infrastructure-validation-dependencies

# Option B: SSH remote
# git remote set-url origin git@github.com:MachineNativeOps/machine-native-ops.git
# git push origin hotfix/infrastructure-validation-dependencies
```

### Step 5: Create Pull Request
Option A - Using GitHub CLI:
```bash
gh pr create \
  --title "fix(ci): complete infrastructure validation fix by adding required scripts" \
  --body "Add validation scripts to complete the infrastructure validation hotfix. See BUG_FIX_COMPLETION_REPORT.md for details." \
  --base main \
  --head hotfix/infrastructure-validation-dependencies
```

Option B - Manual via GitHub Web UI:
1. Navigate to: https://github.com/MachineNativeOps/machine-native-ops
2. Click "Compare & pull request" for the hotfix branch
3. Use the following PR description:

```
## Summary
Complete the infrastructure validation hotfix by adding the required validation scripts.

## Problem
The workflow file `.github/workflows/infrastructure-validation.yml` (added in commit 600a8a4) references scripts in the `scripts/` directory, but these scripts were not present in the repository.

## Solution
- Add validation scripts to `scripts/` directory (copied from `engine/scripts-legacy/`)
- Scripts include: validate-infrastructure.sh, validate-module-manifests.py, validate-module-registry.py, generate-governance-dashboard.py, and generate-dag-visualization.py
- Update documentation to accurately reflect the changes in this PR
- Provide deployment guide and quick reference for the infrastructure validation fix

## Files Added
- `scripts/validate-infrastructure.sh` - Main validation script
- `scripts/validate-module-manifests.py` - Module manifest validator
- `scripts/validate-module-registry.py` - Module registry validator  
- `scripts/generate-governance-dashboard.py` - Dashboard generator
- `scripts/generate-dag-visualization.py` - DAG visualization generator

## Documentation
See BUG_FIX_COMPLETION_REPORT.md and DEPLOYMENT_GUIDE.md for complete details.

GL Unified Charter Activated
```

### Step 6: Review and Approval
1. Assign reviewers from the MachineNativeOps team
2. Request at least 1 approval before merging
3. Ensure all CI/CD checks pass in the PR

### Step 7: Merge to Main
Once approved:
```bash
# Using GitHub CLI
gh pr merge hotfix/infrastructure-validation-dependencies --merge

# OR merge via GitHub Web UI with "Create a merge commit" option
```

### Step 8: Verify Deployment
After merging:
1. Navigate to: https://github.com/MachineNativeOps/machine-native-ops/actions
2. Check that the `infrastructure-validation` workflow runs successfully
3. Verify no "YAML syntax error" false positives occur
4. Monitor subsequent workflow runs for stability

## Monitoring Checklist

### Immediate (24 hours)
- [ ] Verify GitHub Actions workflow passes on main branch
- [ ] Check for any regression in validation results
- [ ] Confirm no intermittent failures occur

### Short-term (1 week)
- [ ] Monitor workflow success rate (target: >95%)
- [ ] Track frequency of validation failures
- [ ] Review error logs for any new issues

### Long-term (1 month)
- [ ] Analyze trend in CI/CD reliability
- [ ] Document any additional improvements needed
- [ ] Update runbooks based on learnings

## Rollback Plan

If issues arise after deployment:

### Option 1: Revert the Commit
```bash
git revert <commit-hash>
git push origin main
```

### Option 2: Revert to Previous Version
```bash
git checkout main
git reset --hard <previous-commit-hash>
git push --force origin main
```

### Option 3: Quick Fix via Workflow
Temporarily modify the workflow to use previous validation logic while investigating.

## Troubleshooting

### Issue: Push Fails with Authentication Error
**Solution**: Verify your GitHub token has `repo` permissions and hasn't expired.

### Issue: Validation Still Fails After Deployment
**Solution**: 
1. Check that pyyaml is installed: `python3 -c "import yaml"`
2. Review logs in GitHub Actions
3. Verify YAML files are actually valid

### Issue: CI/CD Pipeline Slower Than Expected
**Solution**: The retry logic adds minimal overhead (~10-15 seconds). If significantly slower, check for other issues.

## Success Criteria

The deployment is considered successful when:
- ✅ GitHub Actions workflow passes consistently (>95% success rate)
- ✅ No false "YAML syntax error" messages
- ✅ All module manifests, policies, and dependencies validate correctly
- ✅ Error messages are clear and actionable
- ✅ Logs are comprehensive and timestamped

## Additional Resources

- **Bug Fix Summary**: BUG_FIX_COMPLETION_REPORT.md
- **Validation Script**: scripts/validate-infrastructure.sh
- **Workflow File**: .github/workflows/infrastructure-validation.yml
- **GitHub Actions**: https://github.com/MachineNativeOps/machine-native-ops/actions

## Contact

For questions or issues during deployment:
- Review the bug fix summary document
- Check GitHub Actions logs for detailed error messages
- Consult with the MachineNativeOps team

---

**GL Unified Charter Activated**
**Version**: 1.0
**Last Updated**: 2026-01-26