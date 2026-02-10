# GL Platform Training Handbook

**Version**: 5.0.0  
**Target Audience**: Platform Engineers, DevOps Engineers, SREs, Developers  
**@GL-governed** | **@GL-layer: GL90-95 (Training Layer)**

## Welcome to GL Platform

The GL (Governance Layers) Platform v5.0 is a comprehensive governance, security, observability, and automation platform designed to ensure compliance, reliability, and operational excellence across Kubernetes and CI/CD workflows.

## Table of Contents

1. [Platform Overview](#platform-overview)
2. [Architecture](#architecture)
3. [Key Features](#key-features)
4. [Getting Started](#getting-started)
5. [Daily Operations](#daily-operations)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

---

## Platform Overview

### What is GL Platform?

GL Platform is a governance-as-code solution that enforces policies, monitors compliance, automates remediation, and provides comprehensive observability across your infrastructure.

### Core Principles

- **Policy as Code**: All governance rules are version-controlled and auditable
- **Shift Left**: Catches issues before they reach production
- **Self-Healing**: Automatically fixes common issues
- **Observability First**: Full visibility into system health and compliance

### Governance Layers (GL)

The platform is organized into 99 governance layers, each handling specific concerns:

- **GL00-09**: Foundation and Infrastructure
- **GL10-29**: Security and Compliance
- **GL30-49**: Observability and Monitoring
- **GL50-69**: Automation and Orchestration
- **GL70-89**: Naming and Configuration
- **GL90-99**: Integration and Migration

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     GL Platform Architecture                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   GitHub     │  │  Kubernetes  │  │  Prometheus  │       │
│  │  Workflows   │  │   Cluster    │  │   Metrics    │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                 │
│         └─────────────────┼─────────────────┘                 │
│                           │                                   │
│                    ┌──────▼──────┐                            │
│                    │ GL Platform │                            │
│                    │   Engine    │                            │
│                    └──────┬──────┘                            │
│         ┌──────────────────┼──────────────────┐               │
│         │                  │                  │               │
│  ┌──────▼──────┐  ┌───────▼──────┐  ┌────────▼──────┐      │
│  │   Policy    │  │  Observability│  │   Automation │      │
│  │   Engine    │  │   Engine     │  │    Engine    │      │
│  └──────┬──────┘  └───────┬──────┘  └────────┬──────┘      │
│         │                  │                  │               │
│  ┌──────▼──────┐  ┌───────▼──────┐  ┌────────▼──────┐      │
│  │   Slack     │  │   PagerDuty  │  │   Grafana    │      │
│  │  Notifications│  │  Escalation │  │  Dashboards  │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Resource Creation**: Users create/modify resources (K8s manifests, GitHub PRs)
2. **Policy Validation**: OPA/Conftest validates against governance policies
3. **Observability**: Metrics and logs collected by Prometheus
4. **Alerting**: Alertmanager routes alerts to Slack/PagerDuty
5. **Auto-Fix**: Issues automatically fixed where possible
6. **Reporting**: Compliance reports generated and stored

---

## Key Features

### 1. Naming Governance

**Purpose**: Enforce consistent naming conventions across all resources

**Pattern**:
```
{environment}-{service-name}-{resource-type}-v{major}.{minor}.{patch}(-{qualifier})

Example: dev-payment-api-svc-v1.2.3-blue
```

**Benefits**:
- Easy resource identification
- Automated sorting and filtering
- Clear environment separation
- Version tracking

**How to Use**:
```bash
# Suggest compliant name
./scripts/naming/suggest-name.mjs deployment payment-api

# Validate existing resources
./scripts/discovery/naming-audit.sh
```

### 2. Security Scanning

**Purpose**: Automated security scanning for IaC and Kubernetes resources

**Tools**:
- **Checkov**: IaC security and compliance
- **kube-bench**: CIS Kubernetes benchmarks
- **Gitleaks**: Secret detection
- **Kubeaudit**: Kubernetes security audit

**How it Works**:
- Scans run on every PR
- Results posted as PR comments
- Auto-fix for common issues
- Security issues block merges

### 3. Supply Chain Security

**Purpose**: Ensure integrity and provenance of software artifacts

**Features**:
- **SBOM**: Software Bill of Materials generation
- **SLSA**: Supply chain Levels for Software Artifacts
- **Cosign**: Artifact signing and verification
- **Attestations**: Policy attestations

**Key Commands**:
```bash
# Generate SBOM
syft your-image:tag -o spdx-json > sbom.json

# Sign artifact
cosign sign --key cosign.key your-image:tag

# Verify signature
cosign verify --key cosign.pub your-image:tag
```

### 4. Observability

**Purpose**: Full visibility into system health and compliance

**Components**:
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Alertmanager**: Alert routing and management
- **Prometheus Rules**: Alert definitions

**Key Dashboards**:
- Naming Compliance Dashboard
- Ops SLA Overview Dashboard
- Security Dashboard
- Performance Dashboard

**How to Access**:
- Grafana: [EXTERNAL_URL_REMOVED]
- Prometheus: [EXTERNAL_URL_REMOVED]
- Alertmanager: [EXTERNAL_URL_REMOVED]

### 5. Auto-Fix Automation

**Purpose**: Automatically fix common issues

**Capabilities**:
- Update dependencies
- Fix linting issues
- Update base images
- Fix security vulnerabilities (low severity)
- Format code

**How it Works**:
1. Issue detected by CI/CD pipeline
2. Auto-fix bot analyzes issue
3. Creates PR with fix
4. PR validated and tested
5. Auto-merged if tests pass

---

## Getting Started

### For Platform Engineers

#### Setup Your Environment

```bash
# Clone repository
git clone [EXTERNAL_URL_REMOVED]
cd machine-native-ops

# Install required tools
# kubectl (Kubernetes CLI)
# gh (GitHub CLI)
# jq (JSON processor)
# yq (YAML processor)

# Verify installation
kubectl version --client
gh auth status
jq --version
```

#### Initial Configuration

1. **Configure Integrations**
   ```bash
   # Slack
   cp integrations/slack/config.example.yaml integrations/slack/config.yaml
   # Edit with your webhook URL

   # PagerDuty
   cp integrations/pagerduty/config.example.yaml integrations/pagerduty/config.yaml
   # Edit with your integration key

   # Prometheus
   cp integrations/prometheus/config.example.yaml integrations/prometheus/config.yaml
   # Edit with your Prometheus URL
   ```

2. **Deploy Platform Components**
   ```bash
   # Apply Alertmanager configuration
   kubectl apply -f deploy/platform/alertmanager/config.yaml

   # Deploy Prometheus rules
   kubectl apply -f observability/alerts/prometheus-rules/

   # Import Grafana dashboards
   # (Via Grafana UI or API)
   ```

3. **Run Initial Discovery**
   ```bash
   # Discover all cluster resources
   ./scripts/discovery/cluster-discovery.sh

   # Run naming audit
   ./scripts/discovery/naming-audit.sh
   ```

### For Developers

#### Understanding Naming Conventions

Before creating resources, understand the naming pattern:

| Component | Value | Example |
|-----------|-------|---------|
| Environment | `dev`/`staging`/`prod` | `dev` |
| Service Name | `[a-z0-9-]+` | `payment-api` |
| Resource Type | `deploy`/`svc`/`ing`/`cm`/`secret` | `svc` |
| Version | `v{major}.{minor}.{patch}` | `v1.2.3` |
| Qualifier (optional) | `[A-Za-z0-9]+` | `blue` |

**Full Example**: `dev-payment-api-svc-v1.2.3-blue`

#### Creating Compliant Resources

1. **Use Name Suggestion Tool**
   ```bash
   ./scripts/naming/suggest-name.mjs deployment payment-api
   # Output: dev-payment-api-deploy-v1.0.0
   ```

2. **Create Resource with Compliant Name**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: dev-payment-api-deploy-v1.0.0
     namespace: default
   spec:
     # ... rest of deployment spec
   ```

3. **Validate Before Commit**
   ```bash
   # Run Conftest
   conftest test -p .config/conftest/policies/ k8s/

   # Run Checkov
   checkov -f k8s/deployment.yaml
   ```

#### Submitting PRs

1. **Create feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes and commit**
   ```bash
   git add .
   git commit -m "feat: add payment-api deployment"
   ```

3. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   gh pr create --title "Add Payment API" --body "Implementation details..."
   ```

4. **Wait for CI checks**
   - Conftest validation
   - Checkov security scan
   - Naming convention check
   - Supply chain verification

5. **Address any failures**
   - Review PR comments
   - Fix issues
   - Push fixes

6. **Merge when approved**
   - Ensure all checks pass
   - Get approval from maintainers
   - Merge PR

---

## Daily Operations

### Morning Checklist

- [ ] Check Grafana dashboards for overnight issues
- [ ] Review Slack alerts from `#gov-platform-critical`
- [ ] Check PagerDuty for any incidents
- [ ] Review auto-fix PRs created overnight
- [ ] Verify CI/CD pipeline health

### Monitoring Metrics

#### Key Metrics to Watch

1. **Naming Compliance Rate**
   - Target: 100%
   - Alert if: < 95%
   - Dashboard: Naming Compliance

2. **Auto-Fix Success Rate**
   - Target: > 90%
   - Alert if: < 80%
   - Dashboard: Ops SLA Overview

3. **Security Scan Pass Rate**
   - Target: 100%
   - Alert if: < 95%
   - Dashboard: Security Overview

4. **Pipeline Success Rate**
   - Target: > 95%
   - Alert if: < 90%
   - Dashboard: CI/CD Overview

#### Accessing Metrics

```bash
# Query Prometheus directly
kubectl port-forward svc/prometheus-operated 9090:9090 -n gov-platform
# Open [EXTERNAL_URL_REMOVED]

# View alerts
kubectl get prometheusrule -A
kubectl get prometheus -A
```

### Handling Alerts

#### Alert Priority Levels

| Priority | Response Time | Escalation |
|----------|--------------|------------|
| P0 | 5 minutes | Immediate |
| P1 | 15 minutes | 30 minutes |
| P2 | 1 hour | 4 hours |
| P3 | 4 hours | Next business day |

#### Alert Response Workflow

1. **Receive Alert** (Slack/PagerDuty)
2. **Acknowledge** (within SLA)
3. **Investigate**
   - Check Grafana dashboards
   - Review logs
   - Check recent changes
4. **Remediate**
   - Apply fix
   - Verify resolution
5. **Document**
   - Update runbook
   - Create ticket if needed
6. **Close Alert**

### Running Audits

#### Daily Naming Audit

```bash
# Quick check
./scripts/discovery/naming-audit.sh

# Full report
./scripts/discovery/naming-audit.sh \
  --output-format json \
  --output-file audit-$(date +%Y%m%d).json
```

#### Weekly Security Audit

```bash
# Run all security scans
./github/workflows/checkov-scan.yaml
./github/workflows/kube-bench-scan.yaml
./github/workflows/gitleaks-scan.yaml

# Review results
# Check GitHub Actions tab
# Review security PR comments
```

#### Monthly Compliance Review

```bash
# Generate SLA report
./scripts/naming/report-sla.mjs \
  --period month \
  --output-file sla-report-$(date +%Y%m).json

# Review compliance trends
# Check Grafana dashboards
# Prepare executive summary
```

---

## Troubleshooting

### Common Issues

#### Issue: Naming Validation Fails

**Symptoms**:
- Conftest fails on PR
- Alert: "NamingConventionViolation"

**Diagnosis**:
```bash
# Check naming audit
./scripts/discovery/naming-audit.sh --namespace your-namespace

# View violation details
kubectl get prometheusrule -A
```

**Solution**:
1. Use name suggestion tool:
   ```bash
   ./scripts/naming/suggest-name.mjs deployment your-service
   ```
2. Update resource name to compliant pattern
3. Re-run validation
4. Update PR

#### Issue: Alerts Not Received

**Symptoms**:
- No Slack notifications
- No PagerDuty escalations

**Diagnosis**:
```bash
# Check Alertmanager logs
kubectl logs -l app=alertmanager -n gov-platform

# Check Alertmanager configuration
kubectl get configmap alertmanager-config -n gov-platform -o yaml

# Test webhook
curl -X POST YOUR_WEBHOOK_URL -d '{"text":"test"}'
```

**Solution**:
1. Verify webhook/integration keys are correct
2. Check Alertmanager configuration
3. Restart Alertmanager if needed:
   ```bash
   kubectl rollout restart deployment alertmanager -n gov-platform
   ```

#### Issue: Auto-Fix PR Fails

**Symptoms**:
- Auto-fix PR created but tests fail
- PR cannot be merged

**Diagnosis**:
```bash
# Check PR logs
gh pr view PR_NUMBER --json checks

# View workflow logs
gh run list --workflow=auto-fix-bot.yaml
```

**Solution**:
1. Review test failure logs
2. Manually fix the issue
3. Update PR
4. Re-run tests

#### Issue: Grafana Dashboard Shows No Data

**Symptoms**:
- Dashboard panels show "No Data"
- Metrics not appearing

**Diagnosis**:
```bash
# Check Prometheus targets
kubectl get prometheus -A

# Check if metrics are being scraped
kubectl port-forward svc/prometheus-operated 9090:9090 -n gov-platform
# Access [EXTERNAL_URL_REMOVED]
```

**Solution**:
1. Verify Prometheus data source in Grafana
2. Check if targets are up
3. Verify ServiceMonitors are configured
4. Check pod labels match ServiceMonitor selector

---

## Best Practices

### For Platform Engineers

1. **Always use version control**
   - All configuration changes in Git
   - Document changes in commit messages
   - Use PRs for all changes

2. **Test before applying**
   - Use `--dry-run` for Kubernetes changes
   - Test policies in staging first
   - Validate configurations

3. **Monitor everything**
   - Set up alerts for all critical metrics
   - Review dashboards daily
   - Act on alerts promptly

4. **Document procedures**
   - Keep runbooks up to date
   - Document incident responses
   - Share knowledge with team

### For Developers

1. **Follow naming conventions**
   - Use name suggestion tool
   - Validate before committing
   - Ask questions if unsure

2. **Write clean code**
   - Follow linting rules
   - Add unit tests
   - Document complex logic

3. **Review PRs thoroughly**
   - Check all CI tests pass
   - Review security scan results
   - Test changes locally

4. **Be responsive**
   - Address PR feedback promptly
   - Respond to alerts quickly
   - Communicate issues early

### Security Best Practices

1. **Never commit secrets**
   - Use Kubernetes secrets
   - Use environment variables
   - Rotate credentials regularly

2. **Apply least privilege**
   - Use RBAC for access control
   - Limit GitHub token permissions
   - Review access regularly

3. **Keep dependencies updated**
   - Use Dependabot for automatic updates
   - Review security advisories
   - Test updates thoroughly

4. **Audit regularly**
   - Review access logs
   - Check for anomalies
   - Report suspicious activity

---

## Additional Resources

### Documentation

- [GL Unified Architecture Governance Framework v5.0](./GL-UNIFIED-CHARTER.md)
- [Platform Migration Guide](./migration/PLATFORM-MIGRATION-GUIDE.md)
- [Naming Migration Playbook](./runbooks/naming-migration-playbook.md)
- [Security Policies](../.config/policy/)

### Tools and Scripts

- [Naming Suggestion Tool](../scripts/naming/suggest-name.mjs)
- [SLA Report Generator](../scripts/naming/report-sla.mjs)
- [Cluster Discovery](../scripts/discovery/cluster-discovery.sh)
- [Naming Audit](../scripts/discovery/naming-audit.sh)

### Communication Channels

- `#gov-platform-critical` - Critical alerts
- `#gov-platform-high` - High priority alerts
- `#gov-platform-medium` - Medium priority alerts
- `#gov-platform-support` - Support and questions
- `#gov-platform-announcements` - Platform announcements

---

## Appendix: Quick Reference

### Essential Commands

```bash
# Discovery
./scripts/discovery/cluster-discovery.sh
./scripts/discovery/naming-audit.sh

# Naming
./scripts/naming/suggest-name.mjs <type> <name>

# Reports
./scripts/naming/report-sla.mjs --period week

# Git Operations
gh pr create
gh pr view
gh run list

# Kubernetes
kubectl get all -A
kubectl logs -f pod/name
kubectl describe pod/name

# Monitoring
kubectl port-forward svc/prometheus-operated 9090:9090 -n gov-platform
kubectl get prometheusrule -A
kubectl get alertmanager -A
```

### Key File Locations

- Integration configs: `integrations/*/config.yaml`
- Naming policies: `.config/policy/opa/naming.rego`
- Alert rules: `observability/alerts/prometheus-rules/`
- Dashboards: `observability/dashboards/`
- Discovery scripts: `scripts/discovery/`
- Workflows: `.github/workflows/`

### Support Contacts

- Platform Team: platform-team@company.com
- On-call SRE: Use PagerDuty escalation
- Security Team: security@company.com

---

**End of Training Handbook**

@GL-charter-version: 5.0.0 | @GL-audit-trail: Created for GL Platform v5.0 deployment