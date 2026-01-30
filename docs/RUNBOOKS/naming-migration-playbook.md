# Naming Convention Migration Playbook

## Overview

This playbook guides the systematic migration of existing resources to comply with the GL Unified Charter v5.0 naming conventions.

**@GL-governed**
**@GL-layer: GL10-29**
**@GL-semantic: naming-migration-playbook**
**@GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json**

---

## Table of Contents

1. [Discovery Phase](#discovery-phase)
2. [Planning Phase](#planning-phase)
3. [Dry-run Phase](#dry-run-phase)
4. [Staged Rename Phase](#staged-rename-phase)
5. [Cutover Phase](#cutover-phase)
6. [Rollback Phase](#rollback-phase)
7. [Verification Phase](#verification-phase)

---

## 1. Discovery Phase

### Objective
Identify all resources that violate naming conventions across all environments.

### Tools
- `kubectl get all --all-namespaces -o json`
- `find . -name "*.yaml" | xargs grep -l`
- Conftest policy validation
- Custom discovery scripts

### Procedure

```bash
# 1. Scan all Kubernetes resources
kubectl get all --all-namespaces -o json > k8s-resources-discovery.json

# 2. Run naming policy validation
conftest test \
  --policy .config/conftest/policies/naming_policy.rego \
  --all-namespaces \
  --output json \
  k8s-resources-discovery.json > naming-violations.json

# 3. Generate violation report
node scripts/naming/discover-violations.js \
  --input k8s-resources-discovery.json \
  --output artifacts/reports/naming/violations-report.json \
  --format json

# 4. Categorize violations by severity
jq '.violations | group_by(.severity) | map({severity: .[0].severity, count: length})' \
  naming-violations.json > violations-by-severity.json
```

### Output
- Complete list of non-compliant resources
- Violation categorization by severity and type
- Impact analysis of each violation

### Discovery Template

| Resource Type | Current Name | Issue | Suggested Name | Environment | Priority |
|---------------|--------------|-------|-----------------|-------------|----------|
| Deployment | myapp-deployment | Missing environment prefix | dev-myapp-deploy-v1.0.0 | dev | P1 |
| Service | api-svc | Missing version | dev-api-svc-v1.0.0 | dev | P2 |
| ConfigMap | config | Generic name | dev-myapp-cm-v1.0.0 | dev | P3 |

---

## 2. Planning Phase

### Objective
Create a detailed migration plan with risk assessment and acceptance criteria.

### Migration Plan Template

```yaml
# migration-plan.yaml
apiVersion: migration.machinenativeops.io/v1
kind: NamingMigrationPlan
metadata:
  name: naming-migration-plan-001
spec:
  phases:
    - name: discovery
      duration: 1d
      tasks:
        - scan-all-resources
        - categorize-violations
        - generate-reports
    
    - name: planning
      duration: 2d
      tasks:
        - create-migration-schedule
        - assess-risks
        - define-rollback-strategy
    
    - name: dry-run
      duration: 1d
      tasks:
        - validate-naming-changes
        - test-applications
        - generate-diff-reports
    
    - name: staged-migration
      duration: 3d
      environments:
        - dev
        - staging
      tasks:
        - migrate-dev-resources
        - validate-dev-migration
        - migrate-staging-resources
    
    - name: production-cutover
      duration: 2h
      maintenance-window: "02:00-04:00 UTC"
      tasks:
        - migrate-prod-resources
        - validate-prod-migration
        - update-dns-and-load-balancers
        - monitor-system-health
  
  rollback:
    enabled: true
    timeout: 20m
    triggers:
      - critical-failure
      - sli-breach
  
  acceptance-criteria:
    - naming-compliance-rate: "99%+"
    - zero-downtime: true
    - all-tests-passing: true
    - metrics-healthy: true
```

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Application downtime due to name changes | Medium | High | Use rolling updates, maintain DNS |
| Configuration drift | Low | Medium | Use GitOps, validate configs |
| Rollback failure | Low | High | Pre-test rollback procedures |
| DNS/Endpoint issues | Medium | High | Use TTL, gradual cutover |

---

## 3. Dry-run Phase

### Objective
Validate all changes without affecting production.

### Procedure

```bash
# 1. Generate proposed changes
node scripts/naming/generate-changes.js \
  --plan migration-plan.yaml \
  --output artifacts/reports/naming/proposed-changes.json

# 2. Validate changes
kubectl apply --dry-run=server -f artifacts/reports/naming/proposed-changes.yaml

# 3. Generate diff report
kubectl diff -f artifacts/reports/naming/proposed-changes.yaml \
  > artifacts/reports/naming/diff-report.txt

# 4. Test applications locally
kubectl port-forward svc/dev-myapp-svc-v1.0.0 8080:80
curl http://localhost:8080/health

# 5. Validate YAML syntax
yamllint artifacts/reports/naming/proposed-changes.yaml

# 6. Run conftest validation
conftest test \
  --policy .config/conftest/policies/ \
  artifacts/reports/naming/proposed-changes.yaml
```

### Validation Checklist

- [ ] All proposed names follow the naming pattern
- [ ] No duplicate names in any namespace
- [ ] All applications function correctly with new names
- [ ] DNS and service discovery work with new names
- [ ] ConfigMap and Secret references are updated
- [ ] No breaking changes in environment variables
- [ ] Rolling update strategy tested
- [ ] Rollback procedure verified

---

## 4. Staged Rename Phase

### Objective
Migrate resources incrementally, starting with non-critical resources.

### Migration Stages

#### Stage 1: Non-Critical Resources (Day 1)

```bash
# Migrate ConfigMaps and Secrets
for resource in $(jq -r '.resources[] | select(.type=="ConfigMap" or .type=="Secret") | .name' proposed-changes.json); do
  kubectl rename cm $resource ${resource}-v1.0.0
  kubectl rename secret $resource ${resource}-v1.0.0
done
```

#### Stage 2: Services (Day 1-2)

```bash
# Migrate Services with rolling update
for service in $(jq -r '.resources[] | select(.type=="Service") | .name' proposed-changes.json); do
  kubectl patch svc $service -p '{"metadata":{"name":"'${service}-v1.0.0'"}}'
done
```

#### Stage 3: Deployments (Day 2-3)

```bash
# Migrate Deployments with rolling update
for deployment in $(jq -r '.resources[] | select(.type=="Deployment") | .name' proposed-changes.json); do
  kubectl patch deployment $deployment \
    -p '{"metadata":{"name":"'${deployment}-v1.0.0'"}}' \
    --record
  kubectl rollout status deployment/${deployment}-v1.0.0
done
```

### Monitoring During Migration

```bash
# Monitor application health
watch -n 5 'kubectl get pods -o wide | grep -v Running'

# Check logs for errors
kubectl logs -f -l app=myapp-v1.0.0 --tail=100

# Monitor metrics
kubectl top pods -l app=myapp-v1.0.0
```

---

## 5. Cutover Phase

### Objective
Switch traffic to renamed resources with minimal disruption.

### Maintenance Window
- **Window**: 02:00-04:00 UTC (2 hours)
- **Notification**: 24 hours advance notice
- **Fallback**: Immediate rollback if issues detected

### Procedure

```bash
# 1. Stop external traffic
kubectl annotate ingress dev-myapp-ing-v1.0.0 \
  nginx.ingress.kubernetes.io/canary="true" \
  nginx.ingress.kubernetes.io/canary-weight="0"

# 2. Update Ingress to point to new Service
kubectl patch ingress dev-myapp-ing-v1.0.0 \
  -p '{"spec":{"rules":[{"http":{"paths":[{"path":"/","backend":{"service":{"name":"dev-myapp-svc-v1.0.0","port":{"number":80}}}}]}}]}}'

# 3. Verify new endpoints
curl -H "Host: myapp.example.com" http://ingress-controller/health

# 4. Gradually increase traffic
for weight in 10 20 50 100; do
  kubectl annotate ingress dev-myapp-ing-v1.0.0 \
    nginx.ingress.kubernetes.io/canary-weight="$weight"
  sleep 300  # Wait 5 minutes between steps
  
  # Validate health
  if ! curl -f http://ingress-controller/health; then
    echo "Health check failed at weight $weight"
    # Trigger rollback
    ./scripts/naming/rollback.sh
    exit 1
  fi
done

# 5. Monitor for 30 minutes
./scripts/naming/monitor-cutover.sh --duration 30m
```

### DNS Updates

```bash
# 1. Update DNS records (if applicable)
# Point myapp.example.com to new load balancer

# 2. Update TTL to 60s for quick propagation
# Change TTL from 3600s to 60s

# 3. Verify DNS propagation
dig myapp.example.com +short

# 4. Monitor DNS queries
tcpdump -i any -n port 53
```

---

## 6. Rollback Phase

### Objective
Revert to previous state if issues are detected.

### Rollback Triggers

- Critical application failures
- SLI breaches (availability < 99%, latency > 500ms)
- Database connection errors
- Authentication failures
- High error rates (> 5%)

### Rollback Procedure

```bash
#!/bin/bash
# scripts/naming/rollback.sh

set -e

BACKUP_DIR="artifacts/backups/naming/$(date +%Y%m%d-%H%M%S)"

echo "Starting rollback..."

# 1. Restore from backup if available
if [ -d "$BACKUP_DIR" ]; then
  echo "Restoring from backup: $BACKUP_DIR"
  kubectl apply -f $BACKUP_DIR/
else
  echo "No backup available, manual rollback required"
  exit 1
fi

# 2. Restore Service names
for service in $(cat rollback-services.txt); do
  kubectl patch svc ${service}-v1.0.0 \
    -p '{"metadata":{"name":"'${service}'"}}'
done

# 3. Restore Deployment names
for deployment in $(cat rollback-deployments.txt); do
  kubectl patch deployment ${deployment}-v1.0.0 \
    -p '{"metadata":{"name":"'${deployment}'"}}' \
    --record
done

# 4. Restore Ingress configuration
kubectl apply -f artifacts/rollback/ingress.yaml

# 5. Restore DNS records (if applicable)
# Execute DNS API calls to restore original records

# 6. Verify rollback
./scripts/naming/verify-rollback.sh

echo "Rollback completed successfully"
```

### Rollback Verification

```bash
# Verify all old names are restored
kubectl get all --all-namespaces -o json | jq '.items[] | select(.metadata.name | test(".*-v1.0.0$")) | "Still using new names: " + .metadata.name'

# Verify applications are accessible
curl http://myapp.example.com/health

# Verify metrics are healthy
kubectl top pods -l app=myapp

# Verify no errors in logs
kubectl logs -l app=myapp --tail=100 | grep -i error
```

---

## 7. Verification Phase

### Objective
Confirm migration success and generate final report.

### Verification Checklist

#### Naming Compliance
- [ ] All resources follow naming pattern
- [ ] No naming violations detected by conftest
- [ ] All required labels present

#### Application Health
- [ ] All pods running
- [ ] All services accessible
- [ ] Health checks passing
- [ ] No errors in logs

#### System Metrics
- [ ] Availability >= 99%
- [ ] Latency <= 500ms
- [ ] Error rate <= 1%
- [ ] CPU/Memory utilization normal

#### DNS & Networking
- [ ] DNS resolution correct
- [ ] Load balancer healthy
- [ ] Ingress routing correct
- [ ] Network policies valid

#### Monitoring & Observability
- [ ] Prometheus metrics reporting
- [ ] Grafana dashboards updated
- [ ] Alert rules working
- [ ] Logs being collected

### Generate Final Report

```bash
# Generate migration completion report
node scripts/naming/generate-report.js \
  --migration-id naming-migration-001 \
  --output artifacts/reports/naming/migration-completion-report.md \
  --format markdown
```

### Final Report Template

```markdown
# Naming Convention Migration Report

## Summary

- **Migration ID**: naming-migration-001
- **Date**: 2024-01-30
- **Duration**: 3 days
- **Resources Migrated**: 150
- **Compliance Rate**: 99.3%
- **Downtime**: 0 minutes

## Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Naming Compliance | 45% | 99.3% | +54.3% |
| NCR Count | 82 | 1 | -81 |
| Availability | 99.5% | 99.8% | +0.3% |
| Avg Latency | 450ms | 420ms | -30ms |

## Resources Migrated

- Deployments: 50
- Services: 30
- ConfigMaps: 40
- Secrets: 20
- Ingresses: 10

## Issues Encountered

1. **Issue**: DNS propagation delay
   - **Resolution**: Reduced TTL to 60s before migration
   - **Impact**: Minimal

2. **Issue**: Some ConfigMaps had hard-coded service names
   - **Resolution**: Updated application code to use environment variables
   - **Impact**: Required code changes

## Lessons Learned

1. Pre-testing rollback procedures is critical
2. Gradual traffic cutover reduces risk
3. Comprehensive monitoring during migration is essential

## Next Steps

1. Update documentation to reflect new naming
2. Update CI/CD pipelines to enforce naming policies
3. Schedule periodic compliance audits
```

---

## Acceptance Criteria

Migration is considered successful when:

1. **Naming Compliance**: ≥99% of resources follow naming conventions
2. **Zero Downtime**: No measurable downtime during migration
3. **Application Health**: All applications functioning correctly
4. **Metrics Healthy**: All SLIs within acceptable ranges
5. **Rollback Verified**: Rollback procedure tested and documented
6. **Documentation Updated**: All docs reflect new naming

---

## Appendix

### Useful Commands

```bash
# List all resources with naming violations
kubectl get all --all-namespaces -o json | \
  jq '.items[] | select(.metadata.name | test(".*") | not) | "\(.kind): \(.metadata.name)"'

# Generate renaming script
kubectl get all --all-namespaces -o json | \
  jq -r '.items[] | "kubectl rename \(.kind | ascii_downcase) \(.metadata.name) \(.metadata.name)-v1.0.0"' > rename-script.sh

# Check for hard-coded service names
grep -r "myapp-service" apps/

# Validate naming before applying
conftest test --policy .config/conftest/policies/ proposed-changes.yaml
```

### Contacts

- **Migration Owner**: @migration-owner
- **Platform Team**: @platform-team
- **DevOps Team**: @devops-team
- **Emergency Contact**: +1-xxx-xxx-xxxx

---

**Document Version**: 1.0.0  
**Last Updated**: 2024-01-30  
**Approved By**: GL Governance Committee