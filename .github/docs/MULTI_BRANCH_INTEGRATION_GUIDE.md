# Multi-Branch Integration Guide

<!-- GL Layer: GL30-49 Execution Layer -->
<!-- Purpose: Practical step-by-step guide for integrating staging, test/template-branch, and research/template-branch -->

## Overview

This guide provides detailed, executable instructions for integrating three branches into the main development line:
- **staging** - Pre-production changes
- **test/template-branch** - Template testing features
- **research/template-branch** - Experimental features

**Estimated Timeline**: 10 days  
**Team Required**: 1-2 developers + 1 architect reviewer  
**Risk Level**: Medium (mitigated by sequential approach)

## Prerequisites

### System Requirements
- Python 3.11+
- Node.js 18+
- Git 2.40+
- 16GB RAM minimum
- 50GB free disk space

### Required Access
- Write access to repository
- Ability to create/review PRs
- CI/CD workflow permissions

### Pre-Integration Checklist
- [ ] All three source branches are up-to-date
- [ ] Develop branch is clean and stable
- [ ] All CI/CD workflows are passing
- [ ] Backup of current develop branch created
- [ ] Team notified of integration schedule
- [ ] Review of ADR-003, ADR-004, ADR-005 completed

## Phase 1: Pre-Integration Analysis (Days 1-2)

### Day 1: Environment Setup and Analysis

#### Step 1.1: Prepare Working Environment
```bash
# Navigate to repository
cd /path/to/machine-native-ops

# Fetch all remote branches
git fetch --all --prune

# Verify branches exist
git branch -r | grep -E '(staging|test/template-branch|research/template-branch)'

# Create analysis directory
mkdir -p integration-analysis
cd integration-analysis
```

#### Step 1.2: Create Integration Branch
```bash
# Ensure develop is clean
git checkout develop
git pull origin develop

# Verify no uncommitted changes
git status

# Create integration working branch
git checkout -b integration/multi-branch-consolidation
git push -u origin integration/multi-branch-consolidation
```

#### Step 1.3: Analyze Branch Differences
```bash
# Analyze staging branch
echo "=== Analyzing Staging Branch ===" > analysis-report.txt
git log develop..origin/staging --oneline >> analysis-report.txt
git diff --stat develop origin/staging >> analysis-report.txt
git diff --name-only develop origin/staging > staging-files.txt

# Analyze test branch
echo -e "\n=== Analyzing Test Branch ===" >> analysis-report.txt
git log develop..origin/test/template-branch --oneline >> analysis-report.txt
git diff --stat develop origin/test/template-branch >> analysis-report.txt
git diff --name-only develop origin/test/template-branch > test-files.txt

# Analyze research branch
echo -e "\n=== Analyzing Research Branch ===" >> analysis-report.txt
git log develop..origin/research/template-branch --oneline >> analysis-report.txt
git diff --stat develop origin/research/template-branch >> analysis-report.txt
git diff --name-only develop origin/research/template-branch > research-files.txt

# View summary
cat analysis-report.txt
```

### Day 2: Conflict Prediction and Planning

#### Step 2.1: Detect Potential Conflicts
```bash
# Find files modified in multiple branches
echo "=== Files Modified in Multiple Branches ===" > potential-conflicts.txt

# Compare staging and test
comm -12 <(sort staging-files.txt) <(sort test-files.txt) > staging-test-overlap.txt

# Compare staging and research
comm -12 <(sort staging-files.txt) <(sort research-files.txt) > staging-research-overlap.txt

# Compare test and research
comm -12 <(sort test-files.txt) <(sort research-files.txt) > test-research-overlap.txt

# All three branches
comm -12 <(sort staging-test-overlap.txt) <(sort staging-research-overlap.txt) > all-three-overlap.txt

# Report
echo "Files in staging + test: $(wc -l < staging-test-overlap.txt)" >> potential-conflicts.txt
echo "Files in staging + research: $(wc -l < staging-research-overlap.txt)" >> potential-conflicts.txt
echo "Files in test + research: $(wc -l < test-research-overlap.txt)" >> potential-conflicts.txt
echo "Files in all three: $(wc -l < all-three-overlap.txt)" >> potential-conflicts.txt

cat potential-conflicts.txt
cat all-three-overlap.txt
```

#### Step 2.2: Create Integration Plan
```bash
# Create detailed integration plan
cat > integration-plan.md << 'EOF'
# Multi-Branch Integration Plan

## Timeline
- Days 1-2: Analysis (CURRENT)
- Days 3-4: Staging integration
- Days 5-6: Test branch integration
- Days 7-8: Research branch integration
- Days 9-10: Final validation and review

## High-Risk Files (Review Required)
- [ ] List files from all-three-overlap.txt here
- [ ] Add core engine files
- [ ] Add GL governance files

## Validation Checkpoints
- [ ] Post-staging validation
- [ ] Post-test validation
- [ ] Post-research validation
- [ ] Final validation

## Team Assignments
- Integration Lead: TBD
- Architect Reviewer: TBD
- GL Governance Reviewer: TBD
- QA Validator: TBD

## Communication Plan
- Daily standup: 10:00 AM
- Status updates: Slack #integration-2026-01
- Escalation path: Lead → Architect → CTO
EOF

# Open for editing
${EDITOR:-vim} integration-plan.md
```

## Phase 2: Sequential Integration (Days 3-8)

### Days 3-4: Staging Branch Integration

#### Step 3.1: Merge Staging Branch
```bash
# Ensure on integration branch
git checkout integration/multi-branch-consolidation

# Merge staging (no fast-forward to preserve history)
git merge --no-ff --no-commit origin/staging

# Check for conflicts
if git diff --name-only --diff-filter=U | grep .; then
  echo "⚠️  Conflicts detected - manual resolution required"
  git diff --name-only --diff-filter=U > staging-conflicts.txt
  cat staging-conflicts.txt
else
  echo "✅ No conflicts - clean merge"
fi
```

#### Step 3.2: Resolve Staging Conflicts
```bash
# For each conflict in staging-conflicts.txt
# Apply conflict resolution matrix (ADR-005)

# Example: Core engine conflict (P1 - Manual Review)
# git mergetool $CONFLICT_FILE
# Review and choose appropriate version

# Example: Documentation conflict (P3 - Merge All)
# Manually combine content from both versions

# Example: Configuration conflict (P4 - Prefer Staging)
git checkout --theirs config/production.yaml

# Mark conflicts as resolved
git add .
```

#### Step 3.3: Validate Staging Integration
```bash
# GL Validation Gate 1: Semantic Validation
echo "=== GL Gate 1: Semantic Validation ==="
python scripts/gl/validate-semantics.py
if [ $? -ne 0 ]; then
  echo "❌ Semantic validation FAILED - fix required"
  exit 1
fi
echo "✅ Gate 1 PASSED"

# GL Validation Gate 2: Quantum Validation
echo "=== GL Gate 2: Quantum Validation ==="
python scripts/gl/quantum-validate.py
if [ $? -ne 0 ]; then
  echo "❌ Quantum validation FAILED - fix required"
  exit 1
fi
echo "✅ Gate 2 PASSED"

# GL Validation Gate 3: Compliance Check
echo "=== GL Gate 3: Compliance Check ==="
npm run check:gl-compliance
if [ $? -ne 0 ]; then
  echo "❌ GL compliance FAILED - fix required"
  exit 1
fi
echo "✅ Gate 3 PASSED"

# Run test suite
echo "=== Running Test Suite ==="
make test
if [ $? -ne 0 ]; then
  echo "❌ Tests FAILED - fix required"
  exit 1
fi
echo "✅ All tests PASSED"
```

#### Step 3.4: Commit Staging Integration
```bash
# If all validations passed
git commit -m "feat(integration): merge staging branch

- Integrated pre-production changes from staging
- Resolved X conflicts using ADR-005 priority matrix
- All GL validation gates passed
- Test suite: 100% pass rate

Validation Results:
- GL Semantic: ✅ PASSED
- GL Quantum: ✅ PASSED
- GL Compliance: ✅ 100%
- Tests: ✅ XXX/XXX passed

Reviewed-by: [Name]
GL-Validated: Yes"

# Push to remote
git push origin integration/multi-branch-consolidation

# Tag this checkpoint
git tag -a integration-checkpoint-1-staging -m "Checkpoint: Staging integrated"
git push origin integration-checkpoint-1-staging
```

### Days 5-6: Test Branch Integration

#### Step 5.1: Merge Test Branch
```bash
# Ensure on integration branch with staging already integrated
git checkout integration/multi-branch-consolidation
git pull origin integration/multi-branch-consolidation

# Merge test branch
git merge --no-ff --no-commit origin/test/template-branch

# Check for conflicts
if git diff --name-only --diff-filter=U | grep .; then
  echo "⚠️  Conflicts detected - manual resolution required"
  git diff --name-only --diff-filter=U > test-conflicts.txt
  cat test-conflicts.txt
else
  echo "✅ No conflicts - clean merge"
fi
```

#### Step 5.2: Resolve Test Branch Conflicts
```bash
# Apply conflict resolution matrix (ADR-005)
# Remember: P2 priority - prefer test branch for test/tooling code

# Example: Test file conflict (P2 - Prefer Test Branch)
git checkout --theirs tests/integration/template-validator.test.ts

# Example: Documentation conflict (P3 - Merge All)
# Manually combine content

# Mark resolved
git add .
```

#### Step 5.3: Validate Test Integration
```bash
# Run full validation suite (same as staging)
echo "=== Validating Test Branch Integration ==="

# GL Gate 1
python scripts/gl/validate-semantics.py || exit 1

# GL Gate 2
python scripts/gl/quantum-validate.py || exit 1

# GL Gate 3
npm run check:gl-compliance || exit 1

# Test suite
make test || exit 1

echo "✅ All validation gates PASSED"
```

#### Step 5.4: Commit Test Integration
```bash
git commit -m "feat(integration): merge test/template-branch

- Integrated template testing and validation features
- Resolved X conflicts using ADR-005 priority matrix
- All GL validation gates passed
- Enhanced test coverage

Validation Results:
- GL Semantic: ✅ PASSED
- GL Quantum: ✅ PASSED
- GL Compliance: ✅ 100%
- Tests: ✅ XXX/XXX passed

Reviewed-by: [Name]
GL-Validated: Yes"

git push origin integration/multi-branch-consolidation

# Tag checkpoint
git tag -a integration-checkpoint-2-test -m "Checkpoint: Test branch integrated"
git push origin integration-checkpoint-2-test
```

### Days 7-8: Research Branch Integration

#### Step 7.1: Merge Research Branch
```bash
# Ensure on integration branch
git checkout integration/multi-branch-consolidation
git pull origin integration/multi-branch-consolidation

# Merge research branch
git merge --no-ff --no-commit origin/research/template-branch

# Check for conflicts
if git diff --name-only --diff-filter=U | grep .; then
  echo "⚠️  Conflicts detected - manual resolution required"
  git diff --name-only --diff-filter=U > research-conflicts.txt
  cat research-conflicts.txt
else
  echo "✅ No conflicts - clean merge"
fi
```

#### Step 7.2: Resolve Research Branch Conflicts
```bash
# Apply conflict resolution matrix (ADR-005)
# Research features have lower priority than production/test code

# Carefully review experimental features
# Prefer staging/test versions for production-critical code

git add .
```

#### Step 7.3: Validate Research Integration
```bash
# Run full validation suite
echo "=== Validating Research Branch Integration ==="

python scripts/gl/validate-semantics.py || exit 1
python scripts/gl/quantum-validate.py || exit 1
npm run check:gl-compliance || exit 1
make test || exit 1

echo "✅ All validation gates PASSED"
```

#### Step 7.4: Commit Research Integration
```bash
git commit -m "feat(integration): merge research/template-branch

- Integrated experimental template research features
- Resolved X conflicts using ADR-005 priority matrix
- All GL validation gates passed
- Preserved production stability

Validation Results:
- GL Semantic: ✅ PASSED
- GL Quantum: ✅ PASSED
- GL Compliance: ✅ 100%
- Tests: ✅ XXX/XXX passed

Reviewed-by: [Name]
GL-Validated: Yes"

git push origin integration/multi-branch-consolidation

# Tag final checkpoint
git tag -a integration-checkpoint-3-research -m "Checkpoint: All branches integrated"
git push origin integration-checkpoint-3-research
```

## Phase 3: Final Validation and Review (Days 9-10)

### Day 9: Comprehensive Validation

#### Step 9.1: Full Test Suite
```bash
# Run complete test suite with coverage
make test

# Generate coverage report
npm run test:coverage  # if available

# Run integration tests
npm run test:integration  # if available

# Run E2E tests (if applicable)
npm run test:e2e  # if available
```

#### Step 9.2: GL Compliance Verification
```bash
# Run all GL validation scripts
echo "=== Comprehensive GL Validation ==="

# Core validations
python scripts/gl/validate-semantics.py
python scripts/gl/quantum-validate.py
python scripts/gl/validate-data-catalog.py
python scripts/gl/validate-metadata.py
python scripts/gl/validate-model-registry.py

# Generate reports
python scripts/gl/generate-evidence-chain.py
python scripts/gl/generate-audit-report.py
python scripts/gl/generate-risk-assessment.py
python scripts/gl/generate-monitoring-report.py

# Check compliance
npm run check:gl-compliance
```

#### Step 9.3: Code Quality Checks
```bash
# Run linting
npm run lint

# Run quality checks
make automation-check

# Generate quality report
make automation-report
cat AUTO-QUALITY-REPORT.md
```

#### Step 9.4: Security Scanning
```bash
# Run security scans (if available)
npm audit
# or
make security-scan

# Check for secrets
git secrets --scan

# CodeQL scan (via CI/CD)
# Monitor GitHub Actions workflow
```

### Day 10: Review and Merge

#### Step 10.1: Create Pull Request
```bash
# Push final changes
git push origin integration/multi-branch-consolidation

# Create PR (via GitHub UI or CLI)
gh pr create \
  --base develop \
  --head integration/multi-branch-consolidation \
  --title "Multi-Branch Integration: staging, test/template-branch, research/template-branch" \
  --body "$(cat << 'EOF'
## Multi-Branch Integration

This PR integrates changes from three branches:
- ✅ staging (pre-production changes)
- ✅ test/template-branch (template testing features)
- ✅ research/template-branch (experimental features)

### Integration Approach
- Sequential integration (ADR-003)
- GL-First validation (ADR-004)
- Priority-based conflict resolution (ADR-005)

### Validation Results
- GL Semantic Validation: ✅ PASSED
- GL Quantum Validation: ✅ PASSED
- GL Compliance: ✅ 100%
- Test Suite: ✅ XXX/XXX passed
- Code Quality: ✅ Grade A
- Security Scan: ✅ No vulnerabilities

### Files Changed
- Total commits: XXX
- Files changed: XXX
- Lines added: XXX
- Lines removed: XXX

### Conflicts Resolved
- Total conflicts: XXX
- P0 (GL violations): 0
- P1 (Core engine): XXX
- P2 (Tests/tools): XXX
- P3 (Documentation): XXX
- P4 (Configuration): XXX
- P5 (Scripts): XXX
- P6 (Dependencies): XXX

### Review Checklist
- [ ] Code review completed
- [ ] GL governance review completed
- [ ] Security review completed
- [ ] All CI/CD checks passed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

### Related ADRs
- ADR-003: Sequential Integration Strategy
- ADR-004: GL-First Validation Approach
- ADR-005: Conflict Resolution Priority Matrix

### Architecture Documentation
- [Multi-Branch Integration Architecture](docs/architecture/multi_branch_integration_Architecture.md)

---
Reviewed-by: [Name]
GL-Validated: Yes
Integration-Timeline: 10 days
EOF
)"
```

#### Step 10.2: Address Review Feedback
```bash
# Make any requested changes
# Re-run validations
# Push updates

git add .
git commit -m "fix: address PR review feedback"
git push origin integration/multi-branch-consolidation
```

#### Step 10.3: Final Merge
```bash
# After PR approval, merge to develop
# Use GitHub UI or:
gh pr merge integration/multi-branch-consolidation \
  --merge \
  --delete-branch

# Verify merge
git checkout develop
git pull origin develop

# Tag release
git tag -a integration-v1.0.0 -m "Multi-branch integration complete"
git push origin integration-v1.0.0
```

## Rollback Procedures

### Emergency Rollback
If critical issues discovered after integration:

```bash
# Option 1: Revert to checkpoint
git checkout develop
git reset --hard integration-checkpoint-2-test  # or checkpoint-1-staging
git push --force origin develop  # DANGER: Use with caution

# Option 2: Revert specific commits
git revert <commit-hash>
git push origin develop

# Option 3: Create fix-forward branch
git checkout -b fix/integration-issues develop
# Fix issues
# Create new PR
```

### Validation Failure Rollback
If validation fails during integration:

```bash
# Abort current merge
git merge --abort

# Return to last good state
git reset --hard HEAD

# Or return to specific checkpoint
git reset --hard integration-checkpoint-1-staging

# Analyze failure
# Fix issues
# Retry integration
```

## Troubleshooting

### Common Issues

#### Issue: GL Semantic Validation Fails
```bash
# Solution: Check semantic boundaries
python scripts/gl/validate-semantics.py --verbose

# Review GL layer violations
# Fix violations before proceeding
```

#### Issue: Merge Conflicts Too Complex
```bash
# Solution: Use merge tool
git mergetool

# Or manually edit conflict markers
${EDITOR:-vim} $CONFLICT_FILE

# Or prefer one version entirely
git checkout --theirs $CONFLICT_FILE  # Use incoming
git checkout --ours $CONFLICT_FILE    # Use current
```

#### Issue: Tests Failing After Merge
```bash
# Solution: Identify failing tests
make test 2>&1 | tee test-failures.log

# Run specific test
npm test -- --testNamePattern="specific test name"

# Debug and fix
# Re-run validation
```

#### Issue: Performance Regression
```bash
# Solution: Run benchmarks
npm run benchmark  # if available

# Profile code
# Identify bottleneck
# Optimize or revert change
```

## Post-Integration Tasks

### Update Documentation
- [ ] Update CHANGELOG.md with integration summary
- [ ] Update README.md if features changed
- [ ] Update API documentation if applicable
- [ ] Archive integration analysis documents

### Communication
- [ ] Notify team of successful integration
- [ ] Update project status dashboard
- [ ] Schedule retrospective meeting
- [ ] Document lessons learned

### Cleanup
- [ ] Delete integration working branch (after merge)
- [ ] Archive conflict resolution logs
- [ ] Update project management tools
- [ ] Close related issues/tickets

## Success Criteria

Integration is successful when:
- ✅ All three branches merged without critical issues
- ✅ GL compliance: 100%
- ✅ Test pass rate: 100%
- ✅ Code quality: Grade A or better
- ✅ No new security vulnerabilities
- ✅ No performance regressions
- ✅ Documentation updated
- ✅ Team aligned on changes

## References

### Architecture Documentation
- [Multi-Branch Integration Architecture](docs/architecture/multi_branch_integration_Architecture.md)

### ADRs
- [ADR-003: Sequential Integration Strategy](docs/adr/ADR-003-sequential-integration-strategy.md)
- [ADR-004: GL-First Validation Approach](docs/adr/ADR-004-gl-first-validation.md)
- [ADR-005: Conflict Resolution Priority Matrix](docs/adr/ADR-005-conflict-resolution-priority.md)

### GL Documentation
- [GL Status Report](GL-STATUS-REPORT.md)
- [Governance Manifest](governance-manifest.yaml)
- [Branch Strategy Guide](BRANCH_STRATEGY.md)

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-27  
**Author**: Senior Architect Agent  
**GL Layer**: GL30-49 Execution Layer
