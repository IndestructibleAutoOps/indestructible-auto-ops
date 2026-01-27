# Multi-Branch Integration - Quick Reference

<!-- GL Layer: GL30-49 Execution Layer -->
<!-- Purpose: Quick reference card for multi-branch integration -->

## 🎯 Quick Start

### Integration Order
```
staging → test/template-branch → research/template-branch
```

### Validation Gates (After Each Branch)
```bash
# Gate 1: Semantic
python scripts/gl/validate-semantics.py

# Gate 2: Quantum
python scripts/gl/quantum-validate.py

# Gate 3: Compliance
npm run check:gl-compliance && make test
```

## 📋 Integration Checklist

### Pre-Integration
- [ ] Review ADR-003, ADR-004, ADR-005
- [ ] Backup develop branch
- [ ] Notify team
- [ ] Create integration branch
- [ ] Run analysis scripts

### Per Branch Integration
- [ ] Merge branch
- [ ] Resolve conflicts (use priority matrix)
- [ ] Run GL Gate 1 (Semantic)
- [ ] Run GL Gate 2 (Quantum)
- [ ] Run GL Gate 3 (Compliance + Tests)
- [ ] Commit and tag checkpoint
- [ ] Push to remote

### Post-Integration
- [ ] Full test suite
- [ ] Comprehensive GL validation
- [ ] Code quality checks
- [ ] Security scanning
- [ ] Create PR
- [ ] Review and merge

## 🔧 Common Commands

### Setup
```bash
cd /path/to/machine-native-ops
git fetch --all
git checkout -b integration/multi-branch-consolidation develop
git push -u origin integration/multi-branch-consolidation
```

### Merge Branch
```bash
git merge --no-ff --no-commit origin/<branch-name>
```

### Check Conflicts
```bash
git diff --name-only --diff-filter=U
```

### Validate
```bash
python scripts/gl/validate-semantics.py
python scripts/gl/quantum-validate.py
npm run check:gl-compliance
make test
```

### Commit
```bash
git commit -m "feat(integration): merge <branch-name>

- Integrated changes from <branch-name>
- Resolved X conflicts using ADR-005
- All GL validation gates passed

Validation Results:
- GL Semantic: ✅ PASSED
- GL Quantum: ✅ PASSED
- GL Compliance: ✅ 100%
- Tests: ✅ XXX/XXX passed

GL-Validated: Yes"
```

### Tag Checkpoint
```bash
git tag -a integration-checkpoint-N-<branch> -m "Checkpoint: <branch> integrated"
git push origin integration-checkpoint-N-<branch>
```

## 🎲 Conflict Resolution Matrix

| Priority | Type | Resolution |
|----------|------|-----------|
| **P0** | GL Violations | 🔴 BLOCK - Fix required |
| **P1** | Core Engine | 🟡 Manual review |
| **P2** | Tests/Tools | 🟢 Prefer test branch |
| **P3** | Documentation | 🟢 Merge all |
| **P4** | Configuration | 🟢 Prefer staging |
| **P5** | Scripts | 🟢 Newest timestamp |
| **P6** | Dependencies | 🟡 Manual review, prefer staging |

### Quick Resolution Commands

```bash
# P2: Prefer test branch
git checkout origin/test/template-branch -- <file>

# P3: Merge documentation (manual)
git merge-file <file>

# P4: Prefer staging
git checkout origin/staging -- <file>

# P5: Use newest (check timestamps first)
git log -1 --format=%ct origin/staging -- <file>
git log -1 --format=%ct origin/test/template-branch -- <file>
# Use checkout on branch with higher timestamp
```

## ⚠️ Validation Thresholds

### Must Pass (Blocking)
- GL Semantic: 100% (0 violations)
- GL Quantum: ≥99.3% overall accuracy
- GL Compliance: 100%
- Test Pass Rate: 100%

### Warning Levels
- Security vulnerabilities: 0
- Code quality: Grade A
- Performance: No regression >10%

## 🚨 Emergency Rollback

### Abort Current Merge
```bash
git merge --abort
git reset --hard HEAD
```

### Revert to Checkpoint
```bash
git reset --hard integration-checkpoint-N-<branch>
```

### Revert Specific Commit
```bash
git revert <commit-hash>
```

## 📊 Progress Tracking

### Analysis Phase (Days 1-2)
- [ ] Branch analysis complete
- [ ] Conflict prediction done
- [ ] Integration plan created

### Staging Integration (Days 3-4)
- [ ] Staging merged
- [ ] Conflicts resolved
- [ ] All GL gates passed
- [ ] Committed and tagged

### Test Integration (Days 5-6)
- [ ] Test branch merged
- [ ] Conflicts resolved
- [ ] All GL gates passed
- [ ] Committed and tagged

### Research Integration (Days 7-8)
- [ ] Research branch merged
- [ ] Conflicts resolved
- [ ] All GL gates passed
- [ ] Committed and tagged

### Final Validation (Days 9-10)
- [ ] Full test suite passed
- [ ] Comprehensive GL validation
- [ ] Code quality checks passed
- [ ] Security scan clean
- [ ] PR created and reviewed
- [ ] Merged to develop

## 🔍 Troubleshooting

### GL Validation Fails
```bash
# Verbose output for debugging
python scripts/gl/validate-semantics.py --verbose
python scripts/gl/quantum-validate.py --verbose
```

### Tests Fail
```bash
# Run specific test
npm test -- --testNamePattern="test name"

# Check test logs
make test 2>&1 | tee test-failures.log
```

### Conflicts Too Complex
```bash
# Use merge tool
git mergetool

# Or prefer one version
git checkout --theirs <file>  # Use incoming
git checkout --ours <file>    # Use current
```

## 📚 Documentation Links

### Required Reading
- [Multi-Branch Integration Architecture](docs/architecture/multi_branch_integration_Architecture.md)
- [ADR-003: Sequential Integration](docs/adr/ADR-003-sequential-integration-strategy.md)
- [ADR-004: GL-First Validation](docs/adr/ADR-004-gl-first-validation.md)
- [ADR-005: Conflict Resolution](docs/adr/ADR-005-conflict-resolution-priority.md)

### Detailed Guide
- [Multi-Branch Integration Guide](docs/MULTI_BRANCH_INTEGRATION_GUIDE.md) - Full step-by-step

### Executive Summary
- [Integration Summary](MULTI_BRANCH_INTEGRATION_SUMMARY.md) - For leadership

## 🎯 Success Criteria

- ✅ All three branches merged
- ✅ GL compliance: 100%
- ✅ Test pass rate: 100%
- ✅ Code quality: Grade A
- ✅ Zero security vulnerabilities
- ✅ No performance regressions
- ✅ Documentation updated
- ✅ Team aligned

## 📞 Escalation Path

1. **Integration Lead** → Day-to-day decisions
2. **Senior Architect** → Architectural decisions
3. **GL Governance Team** → Governance issues
4. **CTO/Tech Director** → Strategic decisions

## 💡 Tips

- 🎯 **Focus**: One branch at a time
- 🔍 **Validate**: After every branch integration
- 📝 **Document**: Every conflict resolution
- 🔄 **Commit**: Frequently with clear messages
- 🚀 **Progress**: Report daily status
- 🛡️ **Safety**: Always have rollback plan

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-27  
**Author**: Senior Architect Agent  
**GL Layer**: GL30-49 Execution Layer

**Print this card and keep it handy during integration!**
