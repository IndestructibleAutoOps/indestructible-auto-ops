# Workflow Migration Notes

## Disabled Workflows

### issue-pr-automation.yml → issue-pr-automation.yml.disabled

**Reason**: Replaced by comprehensive automation system to prevent conflicts.

**Date**: 2026-01-26

**Replaced by**:
- `issue-automation.yml` - Auto-labeling, welcome messages, slash commands, auto-assignment
- `pr-issue-linker.yml` - PR-to-issue linking
- `issue-triage.yml` - Stale management, critical issue alerts
- `security-issue-handler.yml` - Security issue escalation
- `gl-compliance-issues.yml` - GL compliance scanning

**Migration Path**:
The old workflow used `SillyLittleTech/AutomationSuite@0.1` which listened to the same events as the new workflows (issues: opened, edited, closed, reopened, labeled, unlabeled; pull_request: opened, edited, closed, reopened, labeled, unlabeled, synchronize). This could cause:
- Duplicate labels
- Duplicate comments
- Conflicting status updates
- Race conditions

The new system provides more granular control, better error handling, and integrates with GL governance requirements.

**Rollback Instructions**:
If needed, restore by running:
```bash
git mv .github/workflows/issue-pr-automation.yml.disabled .github/workflows/issue-pr-automation.yml
```

And disable the new workflows:
- issue-automation.yml
- pr-issue-linker.yml
