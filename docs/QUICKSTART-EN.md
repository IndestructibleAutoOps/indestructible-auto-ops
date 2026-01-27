# 🚀 Automation Tools Quick Start Guide

<!-- GL Layer: GL90-99 Meta-Specification Layer -->
<!-- Purpose: Quick start guide for automation tools -->

## Quick Start (3 Steps)

### 1️⃣ Initialize (Run Once)

```bash
make automation-init
```

Or directly:

```bash
bash scripts/init-automation.sh
```

This will:
- ✅ Install all Python dependencies (detect-secrets, black, ruff, mypy, etc.)
- ✅ Create configuration files (.secrets.baseline, .env.example)
- ✅ Run initial quality check
- ✅ Generate initialization report

### 2️⃣ Run Quality Check

```bash
make automation-check
```

Or:

```bash
python scripts/auto-quality-check.py
```

### 3️⃣ View Report

```bash
make automation-report
```

Or:

```bash
cat AUTO-QUALITY-REPORT.md
```

---

## 📋 All Available Commands

### Makefile Commands (Recommended)

| Command | Description |
|---------|-------------|
| `make automation-init` | Initialize automation tools |
| `make automation-check` | Run quality checks |
| `make automation-fix` | Auto-fix issues |
| `make automation-fix-preview` | Preview fixes (dry run) |
| `make automation-verify` | Verify installation status |
| `make automation-report` | View quality report |
| `make automation-help` | Show help |

### Direct Script Execution

```bash
# Initialize
bash scripts/init-automation.sh

# Quality check
python scripts/auto-quality-check.py

# Auto-fix (preview)
python scripts/auto-fix-issues.py --dry-run

# Auto-fix (actual execution)
python scripts/auto-fix-issues.py

# Verify status
bash scripts/verify-automation.sh
```

---

## 📊 Generated Reports

The following files will be generated after execution:

| File | Description |
|------|-------------|
| `AUTO-QUALITY-REPORT.md` | Human-readable quality report |
| `auto-quality-report.json` | Detailed JSON report |
| `AUTOMATION-INIT-REPORT.md` | Initialization completion report |
| `.secrets.baseline` | detect-secrets baseline file |
| `.env.example` | Environment variable template |

---

## 🔍 Check Items

The automation tool checks 8 items:

1. **Security** - Scan hardcoded secrets in code
2. **Python Type Hints** - Type coverage statistics (target 90%+)
3. **TypeScript Quality** - File statistics
4. **Code Duplication** - Detect duplicate modules
5. **Docstring Coverage** - String coverage (target 85%+)
6. **Non-ASCII Filenames** - Cross-platform compatibility
7. **console.log** - Detect improper logging usage
8. **eval() Usage** - Security risk detection

---

## 🔧 Auto-Fix Features

`auto-fix-issues.py` can automatically fix:

- ✅ Code formatting (Black)
- ✅ Import sorting (isort)
- ✅ .gitignore updates
- ✅ .env.example creation

---

## 🤖 CI/CD Integration

Every Push or Pull Request, GitHub Actions will automatically:

1. Run security scan
2. Check Python quality
3. Check TypeScript quality
4. Detect code duplication
5. Check Docstring coverage
6. Run tests and generate coverage report
7. Generate comprehensive quality report
8. Publish results in PR

Configuration file: `.github/workflows/pr-quality-check.yml`

---

## 📖 Detailed Documentation

- [AUTOMATION-README.md](./AUTOMATION-README.md) - Complete usage guide
- [AUTOMATION-INIT-REPORT.md](./AUTOMATION-INIT-REPORT.md) - Initialization report
- [PR-1-REVIEW-REPORT.md](./PR-1-REVIEW-REPORT.md) - Detailed review report
- [PR-1-CODE-EXAMPLES.md](./PR-1-CODE-EXAMPLES.md) - Code examples
- [PR-1-ACTION-PLAN.md](./PR-1-ACTION-PLAN.md) - Improvement plan

---

## 🚙 Troubleshooting

### Issue: Python Dependencies Not Found

```bash
pip install detect-secrets bandit black ruff mypy isort pytest pytest-cov interrogate pylint
```

### Issue: Permission Denied

```bash
chmod +x scripts/*.sh scripts/*.py
```

### Issue: Need to Re-initialize

```bash
make automation-init
```

---

## 💡 Usage Tips

### Daily Workflow

```bash
# 1. Check before starting work
make automation-check

# 2. View areas that need improvement
make automation-report

# 3. Let tools auto-fix simple issues
make automation-fix-preview  # Preview first
make automation-fix          # Actually execute

# 4. Manually fix other issues
# ... edit code ...

# 5. Check again
make automation-check
```

### Integrate into Git Hooks

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "🔍 Running quality checks..."
python scripts/auto-quality-check.py || true
python scripts/auto-fix-issues.py
```

---

## ✅ Verify Installation

Confirm everything is working:

```bash
make automation-verify
```

You should see all checks pass:

```
✓ Python 3 installed
✓ detect-secrets installed
✓ black installed
...
✅ All checks passed! Automation tools ready.
```

---

## 🎯 Next Steps

1. ✅ Run `make automation-init` to initialize
2. 📊 Check `AUTO-QUALITY-REPORT.md` to understand current quality
3. 🔧 Use `make automation-fix` for auto-fixes
4. 📖 Read [PR-1-ACTION-PLAN.md](./PR-1-ACTION-PLAN.md) for improvement plan
5. 🚀 Start improving code quality!

---

**Last Updated**: 2026-01-16  
**Maintained by**: DevOps Team