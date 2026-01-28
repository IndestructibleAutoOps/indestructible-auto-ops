# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# Machine Native Ops - Documentation Index

**Quick Navigation Hub** | Last Updated: 2026-01-16

---

## 🎯 Start Here

### New to the Project?
1. **[README.md](README.md)** - Project overview and introduction
2. **[QUICKSTART.md](QUICKSTART.md)** - Get started in 3 steps
3. **[CONSOLIDATED_PROJECT_STATUS.md](CONSOLIDATED_PROJECT_STATUS.md)** - Current project status

### Need to Track Work?
1. **[CONSOLIDATED_PROJECT_STATUS.md](CONSOLIDATED_PROJECT_STATUS.md)** - Executive summary & all work items
2. **[todo.md](todo.md)** - Day-to-day task tracking
3. **[REMAINING_ISSUES_TODO.md](REMAINING_ISSUES_TODO.md)** - Security issues tracking

---

## 📚 Documentation by Category

### 🛡️ Security

**Current Work**:
- [PHASE2_EVAL_REMEDIATION_COMPLETE.md](PHASE2_EVAL_REMEDIATION_COMPLETE.md) - eval() remediation summary
- [EVAL_USAGE_COMPREHENSIVE_REPORT.md](EVAL_USAGE_COMPREHENSIVE_REPORT.md) - Detailed eval() analysis (447 lines)
- `eval_usage_analysis.json` - Machine-readable audit data (generated file)

**Reference**:
- [SECURITY.md](SECURITY.md) - Security policy and guidelines
- Security audit reports (security_audit_*.json)

### 📊 Project Status & Completion

**Current**:
- [CONSOLIDATED_PROJECT_STATUS.md](CONSOLIDATED_PROJECT_STATUS.md) - ⭐ Central hub for all project status
- [PR_2-5_REVIEW_COMPLETION_SUMMARY.md](PR_2-5_REVIEW_COMPLETION_SUMMARY.md) - PR review results
- [WORK_COMPLETION_REPORT.md](WORK_COMPLETION_REPORT.md) - Final work completion

**Archived**:
- [archive/](archive/) - Old TODO and phase reports (see archive/README.md)

### 🤖 Automation & Tools

**Usage Guides**:
- [AUTOMATION-README.md](AUTOMATION-README.md) - Complete automation guide
- [QUICKSTART.md](QUICKSTART.md) - Quick start with automation tools

**Tool Documentation**:
- Analysis tools: `fix_eval_comprehensive.py`, `code_quality_analyzer.py`
- Remediation tools: `add_eval_security_warnings.py`, `fix_*.py` scripts
- Automation: `scripts/auto-quality-check.py`, `scripts/auto-fix-issues.py`

### 🏗️ Architecture

- [ARCHITECTURE_REFACTOR_COMPLETE.md](ARCHITECTURE_REFACTOR_COMPLETE.md) - Architecture overview
- [AUTOMATED_REPOSITORY_UNDERSTANDING_SYSTEM.md](AUTOMATED_REPOSITORY_UNDERSTANDING_SYSTEM.md) - Repository system

### 📝 Task Tracking

**Active**:
- [todo.md](todo.md) - Day-to-day tasks
- [REMAINING_ISSUES_TODO.md](REMAINING_ISSUES_TODO.md) - Security issues
- [CONSOLIDATED_PROJECT_STATUS.md](CONSOLIDATED_PROJECT_STATUS.md) - All work items

**Archived**:
- [archive/old-todos/](archive/old-todos/) - Historical TODO files

---

## 🔧 Tools & Scripts

### Analysis Tools

| Tool | Purpose | Documentation |
|------|---------|---------------|
| `fix_eval_comprehensive.py` | Comprehensive eval() analysis | Run: `python3 fix_eval_comprehensive.py` |
| `code_quality_analyzer.py` | Code quality scanning | See AUTOMATION-README.md |
| `scripts/auto-quality-check.py` | Automated quality checks | See QUICKSTART.md |

### Remediation Tools

| Tool | Purpose | Status |
|------|---------|--------|
| `add_eval_security_warnings.py` | Add security warnings | ✅ Ready |
| `fix_critical_secrets.py` | Remove hardcoded secrets | ✅ Complete |
| `fix_md5_usage.py` | Replace MD5 with SHA256 | ✅ Complete |
| `scripts/auto-fix-issues.py` | Automated fixes | ✅ Ready |

---

## 📋 Common Tasks

### Check Project Status
```bash
# Read central status document
cat CONSOLIDATED_PROJECT_STATUS.md

# Check daily tasks
cat todo.md

# Check security issues
cat REMAINING_ISSUES_TODO.md
```

### Run Quality Checks
```bash
# Quick quality check
make automation-check

# Full analysis
python3 scripts/auto-quality-check.py

# View report
cat AUTO-QUALITY-REPORT.md
```

### Run Security Analysis
```bash
# Analyze eval() usage
python3 fix_eval_comprehensive.py

# View results
cat EVAL_USAGE_COMPREHENSIVE_REPORT.md
```

---

## 📊 Project Metrics (At a Glance)

### Security
- **CRITICAL**: 0 ✅
- **HIGH**: 7 ⚠️ (documented, in tool files)
- **MEDIUM**: 9 ⚠️ (next PR)
- **Compliance**: 95% ✅

### Code Quality
- **Files Scanned**: 1,370 Python, 1,128 TypeScript
- **Type Hint Coverage**: 66.5% (target: 90%)
- **Docstring Coverage**: 96.7% ✅ (target: 85%)
- **Security Compliance**: 95% ✅

### Testing
- **Sprint 1.3**: 33% complete (Day 1/3)
- **Unit Tests**: 36 passing ✅
- **Integration Tests**: Pending ⏸️

---

## 🗂️ File Organization

```
machine-native-ops/
├── CONSOLIDATED_PROJECT_STATUS.md  ← ⭐ Start here for project status
├── DOCUMENTATION_INDEX.md          ← This file (navigation)
├── todo.md                         ← Day-to-day tasks
├── REMAINING_ISSUES_TODO.md        ← Security issues
│
├── Security Reports/
│   ├── PHASE2_EVAL_REMEDIATION_COMPLETE.md
│   ├── EVAL_USAGE_COMPREHENSIVE_REPORT.md
│   └── eval_usage_analysis.json         (generated)
│
├── Completion Reports/
│   ├── PR_2-5_REVIEW_COMPLETION_SUMMARY.md
│   └── WORK_COMPLETION_REPORT.md
│
├── Tools/
│   ├── fix_eval_comprehensive.py
│   ├── add_eval_security_warnings.py
│   └── Other fix_*.py scripts
│
├── Automation/
│   ├── AUTOMATION-README.md
│   ├── QUICKSTART.md
│   └── scripts/auto-*.py
│
└── archive/                        ← Historical reference only
    ├── old-todos/
    ├── phase-reports/
    └── README.md
```

---

## 🔍 Quick Lookup

### I need to...

**Understand current project status**
→ Read [CONSOLIDATED_PROJECT_STATUS.md](CONSOLIDATED_PROJECT_STATUS.md)

**Track daily tasks**
→ Check [todo.md](todo.md)

**See security issues**
→ Review [REMAINING_ISSUES_TODO.md](REMAINING_ISSUES_TODO.md)

**Get started with the project**
→ Read [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md)

**Run quality checks**
→ See [AUTOMATION-README.md](AUTOMATION-README.md)

**Understand eval() remediation**
→ Read [PHASE2_EVAL_REMEDIATION_COMPLETE.md](PHASE2_EVAL_REMEDIATION_COMPLETE.md)

**Find old TODO files**
→ Check [archive/](archive/) (historical reference only)

**Review PR work**
→ Read [PR_2-5_REVIEW_COMPLETION_SUMMARY.md](PR_2-5_REVIEW_COMPLETION_SUMMARY.md)

---

## 📞 Support

### Documentation Issues?
1. Check this index for navigation
2. See CONSOLIDATED_PROJECT_STATUS.md for current status
3. Review relevant category sections above

### Cannot Find Something?
1. Use this index to navigate
2. Check archive/ for historical files
3. Review CONSOLIDATED_PROJECT_STATUS.md

---

## 🔄 Document Maintenance

**Last Updated**: 2026-01-16  
**Maintained By**: Development Team  
**Update Frequency**: As needed  

**To Update This Index**:
1. Add new documents to appropriate category
2. Update metrics if significant changes
3. Keep "Start Here" section current
4. Archive outdated documents

---

**Navigation**: [Top](#machine-native-ops---documentation-index) | [Status](CONSOLIDATED_PROJECT_STATUS.md) | [Tasks](todo.md) | [README](README.md)
