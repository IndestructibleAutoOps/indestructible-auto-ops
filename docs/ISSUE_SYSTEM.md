# 🤖 Automated Issue Management System

**GL Unified Charter Activated**

This document describes the comprehensive automated issue management system for the Machine Native Ops repository.

> **Note**: This system replaces the previous `issue-pr-automation.yml` workflow to provide more granular control and avoid conflicts. See `.github/workflows/MIGRATION_NOTE.md` for details.

## 📋 Table of Contents

- [Overview](#overview)
- [Issue Templates](#issue-templates)
- [Label System](#label-system)
- [Automation Workflows](#automation-workflows)
- [Commands](#commands)
- [Best Practices](#best-practices)

---

## Overview

The Machine Native Ops repository uses a fully automated issue management system that:

- 🏷️ **Auto-labels** issues based on content analysis
- 👋 **Welcomes** new contributors
- 🔗 **Links** PRs to issues automatically
- 📊 **Generates** weekly metrics reports
- ⏰ **Manages** stale issues
- 🔒 **Escalates** security issues
- 🏛️ **Enforces** GL governance compliance

---

## Issue Templates

### Available Templates

| Template | Purpose | Labels Applied |
|----------|---------|----------------|
| 🐛 Bug Report | Report bugs and unexpected behavior | `type:bug`, `status:triage` |
| ✨ Feature Request | Suggest new features | `type:feature`, `status:triage` |
| 🏛️ GL Compliance | Report governance compliance issues | `gl:compliance`, `priority:high` |
| 📋 Task | Create development tasks | `status:triage` |

### Template Features

- **Structured forms** with dropdowns and checkboxes
- **Required fields** to ensure complete information
- **Auto-labeling** based on selections
- **GL governance** integration

---

## Label System

### Priority Labels

| Label | Color | Description |
|-------|-------|-------------|
| `priority:critical` | 🔴 Red | Requires immediate attention |
| `priority:high` | 🟠 Orange | High priority issue |
| `priority:medium` | 🟡 Yellow | Medium priority issue |
| `priority:low` | 🟢 Green | Low priority issue |

### Status Labels

| Label | Color | Description |
|-------|-------|-------------|
| `status:triage` | 🟣 Purple | Needs triage and categorization |
| `status:ready` | 🟢 Green | Ready to be worked on |
| `status:in-progress` | 🔵 Blue | Currently being worked on |
| `status:review` | 🔵 Blue | Ready for review |
| `status:blocked` | 🔴 Red | Blocked by external dependency |

### Type Labels

| Label | Description |
|-------|-------------|
| `type:bug` | Bug report |
| `type:feature` | Feature request |
| `type:security` | Security vulnerability |
| `type:refactor` | Code refactoring |
| `type:test` | Testing related |
| `type:ci-cd` | CI/CD pipeline related |

### Component Labels

| Label | Description |
|-------|-------------|
| `component:engine` | AEP Engine core |
| `component:gl-gate` | GL Gate module |
| `component:governance` | Governance system |
| `component:web-app` | Web application |
| `component:cli` | CLI application |

### GL Governance Labels

| Label | Description |
|-------|-------------|
| `gl:compliance` | GL compliance related |
| `gl:charter` | GL Charter related |
| `gl:audit` | GL Audit related |

---

## Automation Workflows

### 1. Issue Automation (`issue-automation.yml`)

**Triggers**: Issue opened, edited, labeled, assigned, closed

**Features**:
- Auto-labels based on title and body content
- Welcomes first-time contributors
- Updates status labels on assignment
- Adds closing comments
- Processes slash commands

### 2. Issue Triage (`issue-triage.yml`)

**Triggers**: Daily schedule, manual dispatch

**Features**:
- Marks stale issues (30 days inactive)
- Closes stale issues (7 days after marking)
- Generates weekly metrics reports
- Auto-closes duplicate issues
- Notifies on unaddressed critical issues

### 3. PR-Issue Linker (`pr-issue-linker.yml`)

**Triggers**: PR opened, edited, synchronized

**Features**:
- Extracts issue references from PR body, title, and branch name
- Comments on linked issues
- Updates issue status to in-progress
- Closes issues on PR merge

### 4. Security Issue Handler (`security-issue-handler.yml`)

**Triggers**: Issue opened or labeled with security

**Features**:
- Auto-applies critical priority
- Adds security notice comment
- Provides security guidelines
- Defines response SLAs

### 5. GL Compliance Issues (`gl-compliance-issues.yml`)

**Triggers**: Weekly schedule, manual dispatch

**Features**:
- Scans for missing @gl-governed markers
- Scans for missing .gl-manifest.yaml files
- Validates version formats
- Creates/updates compliance report issue

---

## Commands

Use these commands in issue comments to trigger actions:

| Command | Description | Example |
|---------|-------------|---------|
| `/priority <level>` | Set priority | `/priority high` |
| `/status <status>` | Set status | `/status in-progress` |
| `/assign <user>` | Assign to user | `/assign @username` |
| `/label <label>` | Add a label | `/label type:bug` |
| `/close` | Close the issue | `/close` |
| `/close not-planned` | Close as not planned | `/close not-planned` |
| `/reopen` | Reopen the issue | `/reopen` |
| `/help` | Show help message | `/help` |

---

## Best Practices

### Creating Issues

1. **Use templates** - Always use the provided issue templates
2. **Be specific** - Provide detailed descriptions and reproduction steps
3. **Add context** - Include environment details, logs, and screenshots
4. **Check duplicates** - Search existing issues before creating new ones

### Managing Issues

1. **Triage promptly** - Review new issues within 48 hours
2. **Label correctly** - Apply appropriate priority, type, and component labels
3. **Assign owners** - Ensure issues have assignees
4. **Update status** - Keep status labels current

### GL Compliance

1. **Include GL context** - Specify affected GL layers
2. **Reference charter** - Link to relevant charter sections
3. **Track compliance** - Use gl: labels for governance issues

### Security Issues

1. **Use private advisories** - For critical vulnerabilities
2. **Don't share secrets** - Never include credentials in issues
3. **Follow SLAs** - Respond within defined timeframes

---

## Metrics & Reporting

### Weekly Metrics Report

The legacy `issue-metrics.yml` workflow generates a consolidated weekly metrics report, with its exact schedule defined in that workflow file.

The primary `issue-triage.yml` workflow generates an enhanced metrics report nightly (daily at midnight UTC) and is also available on-demand via `workflow_dispatch`, which includes:

- Total open/closed issues
- Issues opened/closed in the last 7 days
- Priority breakdown
- Type breakdown
- Status breakdown
- Average time to close
- GL compliance issues

### Stale Issue Management

- Issues are marked stale after **30 days** of inactivity
- Stale issues are closed after **7 additional days**
- PRs are marked stale after **45 days**
- PRs are closed after **14 additional days**
- Exempt labels: `priority:critical`, `priority:high`, `keep-open`, `status:in-progress`, `status:blocked`

---

## Configuration

### Customizing Automation

To customize the automation:

1. Edit workflow files in `.github/workflows/`
2. Modify label definitions via GitHub API or UI
3. Update issue templates in `.github/ISSUE_TEMPLATE/`

### Adding New Labels

```bash
# Using GitHub CLI
gh label create "label-name" --color "HEXCODE" --description "Description"
```

### Disabling Automation

To disable specific automation:

1. Remove or rename the workflow file
2. Add `if: false` to the job
3. Comment out the workflow triggers

---

## Support

For questions about the issue system:

1. 📚 Check this documentation
2. 💬 Open a discussion
3. 🐛 Report bugs using the Bug Report template

---

*GL Unified Charter Activated*
*Last Updated: 2024-01-26*