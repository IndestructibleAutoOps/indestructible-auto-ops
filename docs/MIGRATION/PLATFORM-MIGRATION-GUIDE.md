# GL Platform Migration Guide

**Version**: 5.0.0  
**Last Updated**: 2024-01-30  
**@GL-governed** | **@GL-layer: GL90-95 (Migration Layer)**

## Overview

This guide provides step-by-step instructions for migrating to the GL (Governance Layers) Platform v5.0. The platform implements comprehensive governance, security, observability, and automation capabilities for Kubernetes and CI/CD workflows.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Migration Phases](#migration-phases)
3. [Integration Setup](#integration-setup)
4. [Naming Convention Migration](#naming-convention-migration)
5. [Validation & Testing](#validation--testing)
6. [Rollback Procedures](#rollback-procedures)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Access

- Kubernetes cluster admin access
- GitHub repository admin access
- Ability to create secrets and configure integrations

### Required Tools

```bash
# Verify tool installation
kubectl version --client
git --version
jq --version
```

### Pre-Migration Checklist

- [ ] Read and understand GL Unified Charter v5.0
- [ ] Review naming convention policies
- [ ] Identify critical workloads requiring special handling
- [ ] Schedule maintenance window for cutover
- [ ] Notify stakeholders of migration activities
- [ ] Create rollback plan

---

## Migration Phases

### Phase 1: Integration Configuration

#### 1.1 Slack Integration

1. **Create Slack App**
   - Navigate to https://api.slack.com/apps
   - Create new app: "GL Platform Bot"
   - Enable incoming webhooks
   - Copy webhook URL

2. **Configure Integration**
   ```bash
   cd gl-repo
   cp integrations/slack/config.example.yaml integrations/slack/config.yaml
   # Edit config.yaml with your webhook URL and channel names
   ```

3. **Test Integration**
   ```bash
   # Send test message (optional script or manual test)
   curl -X POST -H 'Content-type: application/json' \
     --data '{"text":"GL Platform Integration Test"}' \
     YOUR_WEBHOOK_URL
   ```

#### 1.2 PagerDuty Integration

1. **Create PagerDuty Service**
   - Navigate to PagerDuty dashboard
   - Create service: "GL Platform"
   - Create escalation policies
   - Generate integration key

2. **Configure Integration**
   ```bash
   cp integrations/pagerduty/config.example.yaml integrations/pagerduty/config.yaml
   # Edit config.yaml with your integration key
   ```

#### 1.3 Prometheus Integration

1. **Configure Data Source**
   - Ensure Prometheus is installed in cluster
   - Verify Prometheus API accessibility
   - Configure remote write if using Thanos

2. **Apply Configuration**
   ```bash
   cp integrations/prometheus/config.example.yaml integrations/prometheus/config.yaml
   kubectl apply -f integrations/prometheus/config.yaml
   ```

### Phase 2: Alertmanager Deployment

1. **Deploy Alertmanager**
   ```bash
   kubectl apply -f deploy/platform/alertmanager/config.yaml
   ```

2. **Verify Deployment**
   ```bash
   kubectl get pods -n gl-platform
   kubectl get configmap alertmanager-config -n gl-platform -o yaml
   ```

3. **Test Alert Routing**
   - Trigger test alert
   - Verify Slack notification
   - Verify PagerDuty escalation

### Phase 3: Initial Discovery

1. **Run Cluster Discovery**
   ```bash
   ./scripts/discovery/cluster-discovery.sh
   ```

2. **Review Results**
   - Check naming compliance rate
   - Identify non-compliant resources
   - Document security issues

3. **Run Naming Audit**
   ```bash
   ./scripts/discovery/naming-audit.sh --output-file audit-results.json
   ```

4. **Generate Migration Plan**
   - Create spreadsheet of resources to rename
   - Prioritize by impact and dependencies
   - Schedule rename operations

### Phase 4: Naming Convention Migration

#### 4.1 Discovery Phase

```bash
# Get list of non-compliant resources
./scripts/discovery/naming-audit.sh --output-format json | \
  jq '.violations[]' > non-compliant-resources.json
```

#### 4.2 Planning Phase

For each non-compliant resource:

1. Identify dependencies (services, ingress, configmaps)
2. Document current configuration
3. Plan rename order (dependencies first)
4. Estimate downtime requirements

#### 4.3 Dry-Run Phase

```bash
# Test rename without applying changes
kubectl get deployment old-name -n namespace -o yaml | \
  sed 's/old-name/new-name/g' | \
  kubectl apply --dry-run=server -f -
```

#### 4.4 Staged Rename

1. **Create new resources with compliant names**
   ```bash
   kubectl get deployment old-name -n namespace -o yaml | \
     sed 's/old-name/new-name/g' | \
     kubectl apply -f -
   ```

2. **Wait for new resources to be ready**
   ```bash
   kubectl rollout status deployment new-name -n namespace
   ```

3. **Update dependent resources**
   - Update services to point to new deployment
   - Update ingress rules
   - Update configmap references

4. **Remove old resources**
   ```bash
   kubectl delete deployment old-name -n namespace
   ```

#### 4.5 Cutover Phase

1. **DNS updates** (if applicable)
2. **Load balancer updates**
3. **Service endpoint updates**
4. **Verify application health**

### Phase 5: Validation

1. **Run Naming Audit**
   ```bash
   ./scripts/discovery/naming-audit.sh
   ```

2. **Verify 100% Compliance**

3. **Test Alerting**
   - Trigger test alerts for each priority level
   - Verify notifications received
   - Verify escalation logic

4. **Test Auto-Fix**
   - Create test violations
   - Verify auto-fix triggers
   - Verify PR creation

---

## Integration Setup

### Slack Channel Setup

Create the following channels:

- `#gl-platform-critical` - P0/P1 alerts
- `#gl-platform-high` - P2 alerts
- `#gl-platform-medium` - P3 alerts
- `#gl-platform-low` - Informational alerts
- `#gl-platform-naming` - Naming convention violations
- `#gl-platform-security` - Security alerts
- `#gl-platform-compliance` - Compliance reports

### PagerDuty Service Setup

Create services:

1. **GL Platform Critical** - Escalation policy: 5m → 10m → 15m → 30m
2. **GL Platform High** - Escalation policy: 15m → 30m
3. **GL Platform Standard** - Escalation policy: 60m

### Grafana Dashboard Import

1. Navigate to Grafana
2. Import dashboards:
   - `observability/dashboards/naming-compliance.json`
   - `observability/dashboards/ops-sla-overview.json`
3. Configure Prometheus data source
4. Set up refresh intervals

---

## Naming Convention Migration

### Standard Naming Pattern

```
{environment}-{service-name}-{resource-type}-v{major}.{minor}.{patch}(-{qualifier})

Examples:
- dev-payment-api-svc-v1.2.3-blue
- prod-user-auth-deploy-v2.0.0
- staging-redis-cache-cm-v1.0.0
```

### Resource Type Shortcodes

| Resource | Shortcode |
|----------|-----------|
| Deployment | `deploy` |
| Service | `svc` |
| Ingress | `ing` |
| ConfigMap | `cm` |
| Secret | `secret` |
| StatefulSet | `sts` |
| DaemonSet | `ds` |
| PVC | `pvc` |

### Migration Script Template

```bash
#!/bin/bash

RESOURCE_TYPE="deployment"
NAMESPACE="default"
OLD_NAME="old-deployment-name"
NEW_NAME="dev-service-name-deploy-v1.0.0"

# Step 1: Export current configuration
kubectl get $RESOURCE_TYPE $OLD_NAME -n $NAMESPACE -o yaml > ${OLD_NAME}.yaml

# Step 2: Create new resource
sed "s/$OLD_NAME/$NEW_NAME/g" ${OLD_NAME}.yaml | kubectl apply -f -

# Step 3: Wait for readiness
kubectl rollout status $RESOURCE_TYPE $NEW_NAME -n $NAMESPACE

# Step 4: Update dependent resources
# (manual or scripted based on dependencies)

# Step 5: Delete old resource
kubectl delete $RESOURCE_TYPE $OLD_NAME -n $NAMESPACE
```

---

## Validation & Testing

### Post-Migration Validation Checklist

- [ ] All naming audit results show 100% compliance
- [ ] Alertmanager routing works correctly
- [ ] Slack notifications received for test alerts
- [ ] PagerDuty escalation verified
- [ ] Grafana dashboards display data
- [ ] Auto-fix workflow creates PRs
- [ ] CI/CD pipeline runs successfully
- [ ] All services operational
- [ ] No duplicate resources exist

### Performance Validation

```bash
# Check pod restarts
kubectl get pods -A | awk '{print $4}' | grep -v RESTARTS

# Check error rates
kubectl logs -l app=gl-platform --tail=100 | grep -i error

# Check alert firing rates
# Access Prometheus UI: http://prometheus.machinenativeops.io
```

---

## Rollback Procedures

### Naming Rollback

If naming migration causes issues:

1. **Identify problematic resources**
   ```bash
   ./scripts/discovery/naming-audit.sh --namespace namespace
   ```

2. **Rollback individual resources**
   ```bash
   # Delete new resource
   kubectl delete deployment new-name -n namespace
   
   # Restore old resource
   kubectl apply -f ${OLD_NAME}.yaml
   ```

3. **Update dependent resources** to point back to old names

### Integration Rollback

If integration issues occur:

1. **Disable problematic integration**
   - Edit integration config file
   - Set `enabled: false`
   - Apply configuration

2. **Restore previous Alertmanager config**
   ```bash
   kubectl rollout restart deployment alertmanager -n gl-platform
   ```

3. **Verify notifications stopped**

### Complete Rollback

If critical issues require full rollback:

1. **Rollback GitHub PR**
   ```bash
   gh pr close PR_NUMBER --comment "Rolling back due to critical issues"
   ```

2. **Restore previous deployment**
   ```bash
   kubectl rollout undo deployment/deployment-name -n namespace
   ```

3. **Restore previous configuration**
   ```bash
   git revert COMMIT_HASH
   git push origin main
   ```

---

## Troubleshooting

### Common Issues

#### Issue: Naming audit shows false positives

**Solution**: 
- Review naming patterns in `scripts/discovery/naming-audit.sh`
- Update regex patterns if needed
- Test with `--verbose` flag

#### Issue: Alertmanager not sending notifications

**Solution**:
```bash
# Check Alertmanager logs
kubectl logs -l app=alertmanager -n gl-platform

# Verify configuration
kubectl get configmap alertmanager-config -n gl-platform -o yaml

# Test webhook connectivity
curl -X POST YOUR_WEBHOOK_URL -d '{"text":"test"}'
```

#### Issue: Auto-fix not creating PRs

**Solution**:
- Verify GitHub token permissions
- Check workflow logs in GitHub Actions
- Verify branch protection rules allow auto-merge

#### Issue: Grafana dashboards not showing data

**Solution**:
- Verify Prometheus data source connection
- Check query syntax in dashboard JSON
- Verify metrics are being scraped:
  ```bash
  kubectl port-forward svc/prometheus-operated 9090:9090 -n gl-platform
  # Access http://localhost:9090 and check targets
  ```

### Getting Help

- Review GL Platform documentation
- Check GitHub issues
- Contact platform team via `#gl-platform-support`
- Run discovery scripts for diagnostic information

---

## Additional Resources

- [GL Unified Charter v5.0](./GL-UNIFIED-CHARTER.md)
- [Naming Migration Playbook](./RUNBOOKS/naming-migration-playbook.md)
- [Security Policies](../.config/policy/)
- [Observability Guide](../observability/README.md)

---

## Appendix: Quick Reference

### Essential Commands

```bash
# Run discovery
./scripts/discovery/cluster-discovery.sh

# Run naming audit
./scripts/discovery/naming-audit.sh

# Suggest compliant name
./scripts/naming/suggest-name.mjs deployment my-app

# Generate SLA report
./scripts/naming/report-sla.mjs

# Check workflow status
gh run list --workflow=ci.yaml

# View alerts
kubectl get prometheusrule -A
```

### Key File Locations

- Integration configs: `integrations/*/config.yaml`
- Naming policies: `.config/policy/opa/naming.rego`
- Alert rules: `observability/alerts/prometheus-rules/`
- Dashboards: `observability/dashboards/`
- Discovery scripts: `scripts/discovery/`

---

**End of Migration Guide**

@GL-charter-version: 5.0.0 | @GL-audit-trail: Created for GL Platform v5.0 deployment