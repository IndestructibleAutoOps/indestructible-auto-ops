# Migration Playbook

<!--
@GL-governed
@GL-layer: GL30-49
@GL-semantic: migration-playbook
@GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
-->

## Overview

This playbook provides step-by-step guidance for executing migrations within the Machine Native Ops Monorepo. It covers discovery, planning, execution, and rollback procedures.

## Table of Contents

1. [Migration Types](#migration-types)
2. [Pre-Migration Checklist](#pre-migration-checklist)
3. [Phase 1: Discovery](#phase-1-discovery)
4. [Phase 2: Planning](#phase-2-planning)
5. [Phase 3: Dry-Run](#phase-3-dry-run)
6. [Phase 4: Cutover](#phase-4-cutover)
7. [Phase 5: Rollback](#phase-5-rollback)
8. [Post-Migration Validation](#post-migration-validation)

---

## Migration Types

| Type | Description | Response Action | Estimated Time |
|------|-------------|-----------------|----------------|
| Security Patch | CVE/vulnerability fix | Auto PR fix | < 1 hour |
| Naming Conflict | Governance violation | Auto-rename | < 30 min |
| Architecture Change | Breaking change | Migration Playbook | 2-4 hours |
| Dependency Update | Major version bump | Semi-automated | 1-2 hours |
| Platform Migration | Cross-platform move | Full playbook | 4-8 hours |

---

## Pre-Migration Checklist

Before starting any migration:

- [ ] Backup current state
- [ ] Review change impact assessment
- [ ] Verify rollback procedure
- [ ] Notify stakeholders
- [ ] Check maintenance window
- [ ] Ensure monitoring is active
- [ ] Document baseline metrics

```bash
# Create baseline snapshot
./scripts/bootstrap.sh --backup
kubectl get all -A -o json > baseline-$(date +%Y%m%d_%H%M%S).json
```

---

## Phase 1: Discovery

### 1.1 Inventory Current Resources

```bash
# Export current state
kubectl get all -A -o json > current-state.json

# List all deployments
kubectl get deployments -A -o wide

# Export ConfigMaps and Secrets
kubectl get configmaps -A -o yaml > configmaps-backup.yaml
kubectl get secrets -A -o yaml > secrets-backup.yaml
```

### 1.2 Dependency Analysis

```bash
# Run dependency scan
python ecosystem/enforce.py --audit

# Generate SBOM
cyclonedx-py requirements requirements.txt --format json -o sbom.json

# Check for vulnerabilities
pip-audit --output json > vulnerability-report.json
```

### 1.3 Impact Assessment

```python
# ecosystem/migration/impact_analyzer.py
"""
Impact assessment for migration planning
"""

def assess_migration_impact(resource_type: str, changes: list) -> dict:
    """
    Assess impact of proposed migration changes.
    
    Returns:
        {
            "risk_level": "low|medium|high|critical",
            "affected_services": [...],
            "estimated_downtime": "0m|5m|30m|2h",
            "rollback_complexity": "simple|moderate|complex"
        }
    """
    impact = {
        "risk_level": "low",
        "affected_services": [],
        "estimated_downtime": "0m",
        "rollback_complexity": "simple"
    }
    
    # Assess based on resource type
    if resource_type == "Deployment":
        impact["risk_level"] = "medium"
        impact["estimated_downtime"] = "5m"
    elif resource_type == "StatefulSet":
        impact["risk_level"] = "high"
        impact["estimated_downtime"] = "30m"
        impact["rollback_complexity"] = "moderate"
    
    return impact
```

---

## Phase 2: Planning

### 2.1 Create Migration Plan

```yaml
# migration-plan.yaml
apiVersion: migration.machine-native-ops.io/v1
kind: MigrationPlan
metadata:
  name: example-migration
  annotations:
    gl-layer: GL30-49
    gl-semantic: migration
spec:
  description: "Migration to new naming convention"
  
  phases:
    - name: discovery
      duration: "30m"
      tasks:
        - inventory_resources
        - analyze_dependencies
        - assess_impact
    
    - name: preparation
      duration: "1h"
      tasks:
        - create_backups
        - notify_stakeholders
        - prepare_rollback
    
    - name: dry-run
      duration: "30m"
      tasks:
        - validate_changes
        - test_rollback
    
    - name: execution
      duration: "2h"
      tasks:
        - apply_changes
        - validate_health
        - update_documentation
    
    - name: verification
      duration: "30m"
      tasks:
        - run_tests
        - check_metrics
        - confirm_success
  
  rollback:
    maxDuration: "20m"
    automaticTriggers:
      - healthCheckFailure
      - errorRateThreshold: 5%
    
  notifications:
    slack: "#platform-migrations"
    email: ["platform-team@example.com"]
```

### 2.2 Estimate Resources

| Resource | Required | Available | Status |
|----------|----------|-----------|--------|
| Engineers | 2 | 3 | ✅ |
| Time (hours) | 4 | 8 | ✅ |
| Downtime window | 30m | 2h | ✅ |
| Rollback time | 20m | 20m | ✅ |

---

## Phase 3: Dry-Run

### 3.1 Validate Changes

```bash
# Kubernetes dry-run
kubectl apply --dry-run=server -f manifests/

# Kpt live apply dry-run
kpt live apply --dry-run

# Run policy validation
conftest test manifests/ -p policies/
```

### 3.2 Test Rollback Procedure

```bash
# Create test environment
kubectl create namespace migration-test

# Apply changes to test
kubectl apply -f manifests/ -n migration-test

# Verify functionality
./scripts/quick-verify.sh --namespace migration-test

# Test rollback
kubectl rollout undo deployment/app -n migration-test

# Cleanup test
kubectl delete namespace migration-test
```

### 3.3 Validation Checklist

- [ ] Dry-run completed without errors
- [ ] Policy validation passed
- [ ] Test rollback successful
- [ ] Estimated time within window
- [ ] Team sign-off obtained

---

## Phase 4: Cutover

### 4.1 Pre-Cutover Steps

```bash
# Final backup
kubectl get all -A -o yaml > pre-cutover-backup.yaml

# Set maintenance mode
kubectl annotate deployment/app maintenance=true

# Scale down non-critical services (optional)
kubectl scale deployment/batch-processor --replicas=0
```

### 4.2 Execute Migration

```bash
#!/bin/bash
# migration-execute.sh

set -euo pipefail

echo "Starting migration at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Apply changes
kubectl apply -f manifests/ --record

# Wait for rollout
kubectl rollout status deployment/app --timeout=5m

# Verify health
for i in {1..10}; do
    if kubectl exec -it deploy/app -- curl -s localhost:8080/health | grep -q "ok"; then
        echo "Health check passed"
        break
    fi
    sleep 10
done

# Remove maintenance mode
kubectl annotate deployment/app maintenance-

echo "Migration completed at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### 4.3 Blue-Green Deployment (Alternative)

```bash
# Deploy new version alongside old
kubectl apply -f manifests/app-v2.yaml

# Wait for new version
kubectl rollout status deployment/app-v2 --timeout=5m

# Switch traffic
kubectl patch service/app -p '{"spec":{"selector":{"version":"v2"}}}'

# Verify traffic routing
kubectl get endpoints app

# Remove old version after verification
kubectl delete deployment/app-v1
```

### 4.4 Monitoring During Cutover

```bash
# Watch deployment status
watch -n 5 kubectl get pods

# Monitor logs
kubectl logs -f deployment/app --since=1m

# Check metrics
curl -s localhost:9090/api/v1/query?query=up | jq .
```

---

## Phase 5: Rollback

### 5.1 Automatic Rollback Triggers

Rollback automatically triggers when:
- Health check fails 3 consecutive times
- Error rate exceeds 5%
- P95 latency exceeds 2x baseline
- Manual trigger via ops team

### 5.2 Rollback Procedure

```bash
#!/bin/bash
# rollback.sh

set -euo pipefail

echo "ROLLBACK INITIATED at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Undo deployment
kubectl rollout undo deployment/app

# Wait for rollback
kubectl rollout status deployment/app --timeout=5m

# Restore from backup if needed
if [ "$1" == "--full" ]; then
    kubectl apply -f pre-cutover-backup.yaml
fi

# Verify rollback
kubectl exec -it deploy/app -- curl -s localhost:8080/health

# Notify team
echo "ROLLBACK COMPLETE at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### 5.3 Rollback SLA

| Metric | Target | Max |
|--------|--------|-----|
| Detection time | < 2 min | 5 min |
| Rollback initiation | < 1 min | 2 min |
| Rollback completion | < 10 min | 20 min |
| **Total recovery time** | **< 13 min** | **≤ 20 min** |

---

## Post-Migration Validation

### Validation Checklist

- [ ] All pods running and healthy
- [ ] No error spikes in logs
- [ ] Metrics within baseline tolerance
- [ ] Integration tests passing
- [ ] User acceptance verified
- [ ] Documentation updated
- [ ] Runbook updated if needed

### Metrics to Monitor

```promql
# Error rate
sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# Latency P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Availability
(1 - sum(rate(http_requests_total{code=~"5.."}[1h])) / sum(rate(http_requests_total[1h]))) * 100
```

### Sign-Off

| Role | Name | Sign-Off | Date |
|------|------|----------|------|
| Migration Lead | | ☐ | |
| Platform Engineer | | ☐ | |
| QA Lead | | ☐ | |
| Product Owner | | ☐ | |

---

## Appendix

### A. Common Issues and Resolutions

| Issue | Cause | Resolution |
|-------|-------|------------|
| Pod CrashLoopBackOff | Image pull failed | Check image registry credentials |
| Service unavailable | Endpoint not ready | Wait for pod readiness |
| ConfigMap not found | Missing dependency | Apply ConfigMap first |
| Permission denied | RBAC misconfigured | Update ClusterRole |

### B. Emergency Contacts

| Team | Slack | PagerDuty |
|------|-------|-----------|
| Platform | #platform-oncall | platform-pd |
| Security | #security-oncall | security-pd |
| SRE | #sre-oncall | sre-pd |

### C. Related Documents

- [Governance Policy Guide](./governance-policy.md)
- [Incident Response Playbook](./incident-response.md)
- [Architecture Decision Records](../adr/)

---

*Last Updated: 2026-02-03*
*Version: 1.0.0*
*Owner: Platform Team*
