# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# Quick Start Guide: Production Bug Investigation

## 🚀 Get Started in 5 Minutes

### 1. Setup Environment
```bash
cd machine-native-ops
export GL_TOKEN=your_token_here
export LOG_LEVEL=debug
```

### 2. Collect Logs
```bash
./scripts/collect_logs.sh
```

### 3. Analyze Patterns
```bash
python scripts/detect_patterns.py logs/bug_analysis_*
```

### 4. Review the Full Guide
Open `PRODUCTION_BUG_FIX_GUIDE.md` for comprehensive documentation.

## 📋 Essential Scripts Created

1. **`scripts/collect_logs.sh`** - Collects all logs for analysis
2. **`scripts/detect_patterns.py`** - Analyzes error patterns
3. **`lib/enhanced_logging.py`** - Comprehensive logging module
4. **`PRODUCTION_BUG_FIX_GUIDE.md`** - Complete implementation guide

## ⚠️ Security Reminder

**ROTATE YOUR GITHUB TOKEN IMMEDIATELY!**

The token you provided is now documented. For security:
1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Revoke the current token used during setup
3. Generate a new token with minimum required permissions
4. Update your environment variable

## 🔍 Next Steps

1. **Review Repository Structure**
   - CI/CD workflows in `.github/workflows/`
   - Error handling in `lib/`
   - Monitoring configuration in `config/monitoring/`

2. **Check Recent Issues**
   ```bash
   gh issue list --repo MachineNativeOps/machine-native-ops --limit 20
   ```

3. **Review Failed Workflow Runs**
   ```bash
   gh run list --repo MachineNativeOps/machine-native-ops --limit 10
   ```

4. **Start Investigation**
   Follow the comprehensive guide in `PRODUCTION_BUG_FIX_GUIDE.md`

## 📊 Key Features of the Guide

### Phase 1: Investigation
- Log collection automation
- Pattern detection algorithms
- Local reproduction techniques

### Phase 2: Debugging
- Structured logging implementation
- Comprehensive error handling
- Race condition detection

### Phase 3: Solution
- Retry logic with exponential backoff
- Circuit breaker pattern
- Best practices checklist

### Phase 4: Deployment
- Safe hotfix deployment
- Monitoring stack setup
- Alert configuration

## 🛠️ Tools and Scripts Available

### Log Analysis
- `scripts/collect_logs.sh` - Automated log collection
- `scripts/detect_patterns.py` - Pattern detection
- Custom logging in `lib/enhanced_logging.py`

### Deployment
- `scripts/deploy_hotfix.sh` - Safe deployment
- `scripts/monitor_production.sh` - Production monitoring
- Pre-deployment checklists

### Monitoring
- Prometheus configuration
- Grafana dashboards
- Alert rules

## 📞 Need Help?

The full guide includes:
- Step-by-step instructions
- Code examples
- CLI commands
- Troubleshooting tips
- Best practices

Open `PRODUCTION_BUG_FIX_GUIDE.md` for detailed information.