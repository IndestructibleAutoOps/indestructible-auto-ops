# Standard Operating Procedures (SOPs)

## Overview

This document contains the standard operating procedures for the Machine Native Ops platform, covering all operational tasks from deployment to incident response.

---

## Table of Contents

1. [Deployment SOP](#deployment-sop)
2. [Monitoring SOP](#monitoring-sop)
3. [Backup and Recovery SOP](#backup-and-recovery-sop)
4. [Incident Response SOP](#incident-response-sop)
5. [Scaling SOP](#scaling-sop)
6. [Security SOP](#security-sop)
7. [Maintenance SOP](#maintenance-sop)
8. [Performance Tuning SOP](#performance-tuning-sop)

---

## Deployment SOP

### Purpose

To ensure consistent, reliable, and safe deployments of the Machine Native Ops platform to production.

### Scope

This SOP applies to all deployments to the production environment.

### Responsibilities

| Role | Responsibility |
|------|---------------|
| Release Engineer | Execute deployment process |
| Engineering Lead | Approve deployment |
| Operations Team | Monitor deployment |
| QA Team | Verify deployment success |

### Procedure

#### 1. Pre-Deployment Checklist

```bash
# 1.1 Verify all tests pass
cd /workspace/machine-native-ops
pytest tests/ -v

# 1.2 Verify code quality
pylint ns-root/
black --check ns-root/
mypy ns-root/

# 1.3 Verify security scan
bandit -r ns-root/

# 1.4 Verify build succeeds
docker build -t machine-native-ops:test .

# 1.5 Verify documentation is up to date
# Check if all changes are documented

# 1.6 Create deployment ticket
# Include:
# - Deployment summary
# - Changes being deployed
# - Rollback plan
# - Verification steps
```

#### 2. Deployment Execution

```bash
# 2.1 Create release branch
git checkout -b release/vX.Y.Z

# 2.2 Update version
# Update version in package.json, __init__.py, etc.

# 2.3 Commit and push
git add .
git commit -m "Release vX.Y.Z"
git push origin release/vX.Y.Z

# 2.4 Build and push image
docker build -t ghcr.io/machinenativeops/machine-native-ops:vX.Y.Z .
docker push ghcr.io/machinenativeops/machine-native-ops:vX.Y.Z

# 2.5 Update deployment
kubectl set image deployment/machine-native-ops \
  app=ghcr.io/machinenativeops/machine-native-ops:vX.Y.Z \
  -n production

# 2.6 Monitor rollout
kubectl rollout status deployment/machine-native-ops -n production
```

#### 3. Post-Deployment Verification

```bash
# 3.1 Check pod status
kubectl get pods -n production

# 3.2 Check pod health
kubectl exec -it deployment/machine-native-ops -n production -- \
  curl http://localhost:8000/health

# 3.3 Check application logs
kubectl logs -l app=machine-native-ops -n production --tail=100

# 3.4 Check metrics
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# Query metrics in Grafana

# 3.5 Run smoke tests
./scripts/run-smoke-tests.sh

# 3.6 Monitor for 15 minutes
# Watch Grafana dashboards
# Check error rate
# Check latency
# Check resource usage
```

#### 4. Rollback Procedure

```bash
# 4.1 Trigger rollback if deployment fails
kubectl rollout undo deployment/machine-native-ops -n production

# 4.2 Monitor rollback
kubectl rollout status deployment/machine-native-ops -n production

# 4.3 Verify rollback
kubectl get pods -n production
kubectl logs -l app=machine-native-ops -n production --tail=100

# 4.4 Document rollback
# Update deployment ticket
# Create incident ticket
# Document root cause
```

### Success Criteria

- ✅ All pods are running and healthy
- ✅ Health check endpoint returns 200 OK
- ✅ Error rate < 1%
- ✅ P95 latency < 200ms
- ✅ No critical alerts
- ✅ All smoke tests pass

### Escalation

| Issue | Escalate To | Timeline |
|-------|------------|----------|
| Deployment fails after 1 rollback attempt | Engineering Lead | Immediate |
| Multiple pods in CrashLoopBackOff | Engineering Lead | Within 5 minutes |
| Error rate > 5% for 10+ minutes | On-Call Engineer | Within 5 minutes |
| Data corruption or loss | CTO | Immediate |

---

## Monitoring SOP

### Purpose

To ensure the Machine Native Ops platform is continuously monitored and issues are detected and resolved promptly.

### Scope

This SOP applies to all monitoring activities for the production environment.

### Responsibilities

| Role | Responsibility |
|------|---------------|
| Operations Team | Monitor dashboards and alerts |
| On-Call Engineer | Respond to alerts 24/7 |
| Engineering Team | Investigate and resolve issues |
| Management Team | Review trends and capacity planning |

### Procedure

#### 1. Daily Monitoring

```bash
# 1.1 Check Grafana dashboards
# Open Grafana: http://grafana.production.machinenativeops.com
# Review:
# - Machine Native Ops Dashboard
# - Istio Mesh Dashboard
# - Backup Status Dashboard
# - Infrastructure Dashboard

# 1.2 Check Alertmanager
# Open Alertmanager: http://alertmanager.production.machinenativeops.com
# Review:
# - Active alerts
# - Alert history
# - Alert trends

# 1.3 Check application logs
kubectl logs -l app=machine-native-ops -n production --tail=500 --since=1h

# 1.4 Check infrastructure health
kubectl get nodes
kubectl get pods -A
kubectl top nodes
kubectl top pods -n production

# 1.5 Check backup status
velero backup get
kubectl get jobs -n production | grep backup
```

#### 2. Alert Response

**Critical Alerts** (respond within 5 minutes):

```bash
# 2.1 Acknowledge alert
# Open PagerDuty or Slack
# Acknowledge alert

# 2.2 Investigate
# Check Grafana dashboards
# Review application logs
# Check recent deployments
# Check dependencies

# 2.3 Mitigate
# Apply immediate fix
# Example: Scale up, restart, rollback

# 2.4 Monitor
# Watch metrics for recovery
# Verify fix is effective

# 2.5 Document
# Update incident ticket
# Document root cause
# Create follow-up tasks
```

**Warning Alerts** (respond within 30 minutes):

```bash
# Follow same procedure as critical alerts
# But with 30-minute response time
```

#### 3. Weekly Monitoring Review

```bash
# 3.1 Review weekly metrics
# Check trends in:
# - Request rate
# - Error rate
# - Latency
# - Resource usage
# - Backup success rate

# 3.2 Review alert history
# Analyze:
# - Alert frequency
# - Alert severity
# - Alert resolution time
# - False positives

# 3.3 Review infrastructure health
# Check:
# - Node health
# - Pod health
# - PVC usage
# - Network performance

# 3.4 Update monitoring configuration
# Adjust:
# - Alert thresholds
# - Dashboard queries
# - Metric retention
```

### Success Criteria

- ✅ All critical alerts acknowledged within 5 minutes
- ✅ All warning alerts acknowledged within 30 minutes
- ✅ Mean time to acknowledge (MTTA) < 5 minutes
- ✅ Mean time to resolve (MTTR) < 30 minutes
- ✅ No missed critical alerts
- ✅ Weekly monitoring review completed

### Escalation

| Issue | Escalate To | Timeline |
|-------|------------|----------|
| Alert not acknowledged after 5 minutes | On-Call Engineer | Immediately |
| Issue not resolved after 30 minutes | Engineering Lead | Within 30 minutes |
| System-wide outage | CTO | Immediately |
| Repeated alerts (false positives) | Engineering Team | Within 1 hour |

---

## Backup and Recovery SOP

### Purpose

To ensure data is regularly backed up and can be quickly restored in case of data loss or corruption.

### Scope

This SOP applies to all backup and recovery operations for the production environment.

### Responsibilities

| Role | Responsibility |
|------|---------------|
| Operations Team | Schedule and monitor backups |
| Engineering Team | Test backup and recovery |
| Database Admin | Verify database backups |
| Management Team | Review backup compliance |

### Procedure

#### 1. Backup Schedule

```bash
# 1.1 Cluster Backups (Velero)
# Daily at 2 AM UTC
velero backup create daily-cluster-backup-$(date +%Y%m%d) \
  --include-namespaces production,istio-system,monitoring \
  --wait

# Hourly incremental backups
velero backup create hourly-incremental-backup-$(date +%Y%m%d-%H%M%S) \
  --include-namespaces production \
  --wait

# 1.2 Database Backups
# PostgreSQL (every 4 hours)
# Automated via CronJob: postgres-backup
kubectl create job postgres-manual-backup-$(date +%Y%m%d-%H%M%S) \
  --from=cronjob/postgres-backup -n production

# Redis (every 30 minutes)
# Automated via CronJob: redis-backup
kubectl create job redis-manual-backup-$(date +%Y%m%d-%H%M%S) \
  --from=cronjob/redis-backup -n production
```

#### 2. Backup Verification

```bash
# 2.1 Verify backup creation
velero backup get
velero backup describe <backup-name> --details

# 2.2 Verify backup integrity
# Check backup status is "Completed"
# Check backup size is reasonable
# Check no errors in backup logs

# 2.3 Verify S3 storage
aws s3 ls s3://machinenativeops-backups/velero/backups/
aws s3 ls s3://machinenativeops-backups/postgres/
aws s3 ls s3://machinenativeops-backups/redis/

# 2.4 Test restore (dry-run)
velero restore create test-restore \
  --from-backup <backup-name> \
  --dry-run \
  --wait
```

#### 3. Backup Testing

```bash
# 3.1 Weekly backup integrity test
./scripts/test-backup-integrity.sh

# 3.2 Monthly full restore test
./scripts/test-full-restore.sh

# 3.3 Quarterly disaster recovery drill
./scripts/run-disaster-recovery-drill.sh
```

#### 4. Recovery Procedure

```bash
# 4.1 Identify backup to restore
velero backup get
# Select appropriate backup

# 4.2 Stop application
kubectl scale deployment/machine-native-ops --replicas=0 -n production

# 4.3 Restore from backup
velero restore create emergency-restore-$(date +%Y%m%d-%H%M%S) \
  --from-backup <backup-name> \
  --include-namespaces production \
  --wait

# 4.4 Verify restore
kubectl get pods -n production
kubectl get all -n production

# 4.5 Start application
kubectl scale deployment/machine-native-ops --replicas=3 -n production

# 4.6 Verify application health
kubectl exec -it deployment/machine-native-ops -n production -- \
  curl http://localhost:8000/health

# 4.7 Monitor recovery
# Watch Grafana dashboards
# Check error rate
# Check latency
# Verify data integrity
```

### Success Criteria

- ✅ Daily backups completed successfully (100%)
- ✅ Hourly backups completed successfully (100%)
- ✅ Database backups completed successfully (100%)
- ✅ Backup integrity tests pass (100%)
- ✅ Restore tests pass (100%)
- ✅ RTO < 4 hours
- ✅ RPO < 1 hour

### Escalation

| Issue | Escalate To | Timeline |
|-------|------------|----------|
| Backup fails | Engineering Lead | Within 1 hour |
| Backup verification fails | Engineering Lead | Within 2 hours |
| Restore fails | CTO | Immediately |
| Data loss detected | CTO | Immediately |

---

## Incident Response SOP

### Purpose

To provide a structured approach to handling incidents, minimizing impact, and preventing recurrence.

### Scope

This SOP applies to all incidents affecting the production environment.

### Responsibilities

| Role | Responsibility |
|------|---------------|
| On-Call Engineer | Initial incident response |
| Incident Commander | Coordinate incident response |
| Engineering Team | Investigate and resolve |
| Communications Team | Stakeholder communication |

### Procedure

#### 1. Incident Detection

```bash
# 1.1 Monitor alerts
# PagerDuty
# Slack alerts
# Grafana dashboards
# Prometheus alerts

# 1.2 Detect incident
# Define incident severity:
# - Critical: System-wide outage
# - High: Major feature unavailable
# - Medium: Degraded performance
# - Low: Minor issues
```

#### 2. Incident Response

**Phase 1: Acknowledge and Assess (0-5 minutes)**

```bash
# 2.1.1 Acknowledge incident
# Open PagerDuty incident
# Post in #incident-response Slack
# Assign to Incident Commander

# 2.1.2 Assess impact
# Check system status
# Check affected services
# Check user impact
# Estimate severity level

# 2.1.3 Communicate
# Notify stakeholders
# Update status page
# Post public message if needed
```

**Phase 2: Investigate and Mitigate (5-30 minutes)**

```bash
# 2.2.1 Investigate
# Check logs
# Check metrics
# Check recent changes
# Identify root cause

# 2.2.2 Mitigate
# Apply temporary fix
# Scale up if needed
# Rollback if needed
# Restart services if needed

# 2.2.3 Monitor
# Watch metrics
# Verify fix is working
# Check for side effects
```

**Phase 3: Resolve and Recover (30-60 minutes)**

```bash
# 2.3.1 Resolve
# Apply permanent fix
# Verify resolution
# Monitor for stability

# 2.3.2 Recover
# Restore normal operations
# Verify all services
# Check data integrity

# 2.3.3 Communicate
# Update stakeholders
# Update status page
# Close public incident
```

#### 3. Post-Incident Activities

```bash
# 3.1 Document incident
# Create incident ticket
# Document timeline
# Document root cause
# Document resolution

# 3.2 Conduct post-mortem
# Schedule post-mortem meeting
# Invite all participants
# Document lessons learned

# 3.3 Create action items
# Create tasks to prevent recurrence
# Assign owners
# Set due dates

# 3.4 Update procedures
# Update runbooks
# Update monitoring
# Update documentation
```

### Success Criteria

- ✅ Incident acknowledged within 5 minutes
- ✅ Initial assessment within 10 minutes
- ✅ Mitigation implemented within 30 minutes
- ✅ Incident resolved within 60 minutes
- ✅ Root cause identified
- ✅ Post-mortem completed within 3 days
- ✅ Action items created and tracked

### Escalation

| Issue | Escalate To | Timeline |
|-------|------------|----------|
| Critical incident not acknowledged | CTO | Within 5 minutes |
| Incident not resolved in 60 minutes | CTO | Within 60 minutes |
| System-wide outage | CTO | Immediately |
| Data loss or security breach | CTO & Security Team | Immediately |

---

## Scaling SOP

### Purpose

To ensure the system can handle increased load by scaling resources appropriately.

### Scope

This SOP applies to all scaling operations for the production environment.

### Responsibilities

| Role | Responsibility |
|------|---------------|
| Operations Team | Monitor resource usage |
| Engineering Team | Implement scaling policies |
| Management Team | Capacity planning |

### Procedure

#### 1. Scaling Triggers

```bash
# 1.1 Monitor scaling metrics
# CPU usage > 70%
# Memory usage > 80%
# Request rate > 1000 req/s
# Latency P95 > 200ms
# Queue depth > 100

# 1.2 Check auto-scaling status
kubectl get hpa -n production
kubectl describe hpa machine-native-ops-hpa -n production
```

#### 2. Manual Scaling

```bash
# 2.1 Scale up
kubectl scale deployment/machine-native-ops --replicas=10 -n production
kubectl rollout status deployment/machine-native-ops -n production

# 2.2 Scale down
kubectl scale deployment/machine-native-ops --replicas=3 -n production

# 2.3 Verify scaling
kubectl get pods -n production
kubectl top pods -n production
```

#### 3. Auto-Scaling Configuration

```bash
# 3.1 Check HPA configuration
kubectl get hpa -n production -o yaml

# 3.2 Update HPA
kubectl edit hpa machine-native-ops-hpa -n production
# Adjust:
# - minReplicas
# - maxReplicas
# - target CPU utilization
# - target memory utilization

# 3.3 Verify HPA is working
kubectl get hpa machine-native-ops-hpa -n production -w
# Watch replicas scale up/down based on load
```

### Success Criteria

- ✅ Scaling triggers detected within 1 minute
- ✅ Auto-scaling responds within 2 minutes
- ✅ New pods become healthy within 30 seconds
- ✅ System maintains performance during scaling
- ✅ No errors during scaling

### Escalation

| Issue | Escalate To | Timeline |
|-------|------------|----------|
| Auto-scaling not working | Engineering Lead | Within 15 minutes |
| Manual scaling fails | Engineering Lead | Within 10 minutes |
| System cannot scale to meet demand | CTO | Within 30 minutes |

---

## Security SOP

### Purpose

To ensure the security of the Machine Native Ops platform and protect against threats.

### Scope

This SOP applies to all security-related operations for the production environment.

### Responsibilities

| Role | Responsibility |
|------|---------------|
| Security Team | Monitor security alerts |
| Engineering Team | Apply security fixes |
| Operations Team | Implement security controls |
| Management Team | Security compliance |

### Procedure

#### 1. Security Monitoring

```bash
# 1.1 Monitor security alerts
# Check Slack #security-alerts
# Check PagerDuty security incidents
# Check security tools (Trivy, Grype)

# 1.2 Check vulnerability reports
gh api repos/MachineNativeOps/machine-native-ops/code-scanning/alerts
gh api repos/MachineNativeOps/machine-native-ops/dependabot/alerts

# 1.3 Review audit logs
kubectl logs -l app=audit-logger -n production --tail=1000
```

#### 2. Security Incident Response

```bash
# 2.1 Acknowledge security incident
# Assign to Security Team
# Escalate to CTO if critical

# 2.2 Investigate
# Review logs
# Check for unauthorized access
# Check for data exfiltration
# Identify attack vector

# 2.3 Contain
# Isolate affected systems
# Block malicious IPs
# Disable compromised accounts
# Stop affected services

# 2.4 Eradicate
# Remove malware
# Patch vulnerabilities
# Update credentials
# Clean systems

# 2.5 Recover
# Restore from clean backup
# Verify systems are clean
# Monitor for recurrence

# 2.6 Communicate
# Notify stakeholders
# Document incident
# Create post-mortem
```

#### 3. Security Hardening

```bash
# 3.1 Apply security patches
kubectl set image deployment/machine-native-ops \
  app=ghcr.io/machinenativeops/machine-native-ops:latest-security \
  -n production

# 3.2 Rotate secrets
kubectl create secret generic machine-native-ops-secrets-new \
  --from-literal=secret-key=$(openssl rand -base64 32) \
  -n production

# 3.3 Update RBAC policies
kubectl apply -f k8s/production/security-policies.yaml

# 3.4 Run security scans
trivy image ghcr.io/machinenativeops/machine-native-ops:latest
grype ghcr.io/machinenativeops/machine-native-ops:latest
```

### Success Criteria

- ✅ Security incidents acknowledged within 5 minutes
- ✅ Security incidents resolved within 4 hours
- ✅ No critical vulnerabilities unpatched for > 7 days
- ✅ All secrets rotated every 90 days
- ✅ Security scans run daily

### Escalation

| Issue | Escalate To | Timeline |
|-------|------------|----------|
| Critical security incident | CTO & Security Team | Immediately |
| High severity vulnerability | Engineering Lead | Within 24 hours |
| Unauthorized access detected | CTO & Security Team | Immediately |
| Data breach | CTO & Legal Team | Immediately |

---

## Maintenance SOP

### Purpose

To ensure regular maintenance is performed to keep the system healthy and performant.

### Scope

This SOP applies to all maintenance activities for the production environment.

### Responsibilities

| Role | Responsibility |
|------|---------------|
| Operations Team | Execute maintenance tasks |
| Engineering Team | Review and approve |
| Management Team | Schedule and communicate |

### Procedure

#### 1. Maintenance Schedule

```bash
# 1.1 Weekly Maintenance
# Every Sunday at 2 AM UTC
# - Review system health
# - Update documentation
# - Review logs
# - Check backups

# 1.2 Monthly Maintenance
# First Sunday of month at 2 AM UTC
# - Apply security patches
# - Update dependencies
# - Optimize database
# - Clean up resources

# 1.3 Quarterly Maintenance
# First Sunday of quarter at 2 AM UTC
# - Major version upgrades
# - Infrastructure upgrades
# - Full system audit
# - Disaster recovery drill
```

#### 2. Maintenance Execution

```bash
# 2.1 Pre-Maintenance
# Notify stakeholders (7 days before)
# Create maintenance ticket
# Create backup
# Document current state

# 2.2 During Maintenance
# Enable maintenance mode
# Apply updates
# Verify changes
# Monitor system

# 2.3 Post-Maintenance
# Verify system health
# Run tests
# Monitor for issues
# Document results

# 2.4 Rollback (if needed)
# If issues detected:
# Rollback changes
# Verify rollback
# Investigate issues
# Reschedule maintenance
```

#### 3. Database Maintenance

```bash
# 3.1 Vacuum database
kubectl exec -it deployment/postgres -n production -- psql \
  -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "VACUUM ANALYZE;"

# 3.2 Reindex database
kubectl exec -it deployment/postgres -n production -- psql \
  -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "REINDEX DATABASE ${POSTGRES_DB};"

# 3.3 Update statistics
kubectl exec -it deployment/postgres -n production -- psql \
  -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "ANALYZE;"
```

### Success Criteria

- ✅ Maintenance scheduled and communicated in advance
- ✅ Backup created before maintenance
- ✅ Changes applied successfully
- ✅ System verified healthy after maintenance
- ✅ No unexpected downtime
- ✅ Documentation updated

### Escalation

| Issue | Escalate To | Timeline |
|-------|------------|----------|
| Maintenance fails | Engineering Lead | Within 15 minutes |
| System down after maintenance | CTO | Immediately |
| Data loss during maintenance | CTO | Immediately |

---

## Performance Tuning SOP

### Purpose

To ensure the system performs optimally and meets performance SLAs.

### Scope

This SOP applies to all performance tuning activities for the production environment.

### Responsibilities

| Role | Responsibility |
|------|---------------|
| Engineering Team | Analyze and optimize performance |
| Operations Team | Monitor performance metrics |
| Management Team | Review performance reports |

### Procedure

#### 1. Performance Monitoring

```bash
# 1.1 Check performance metrics
# Open Grafana dashboards
# Review:
# - API response times (P50, P95, P99)
# - Error rates
# - Throughput
# - Resource usage
# - Database query times
# - Cache hit rates

# 1.2 Run performance tests
./scripts/run-performance-tests.sh

# 1.3 Analyze trends
# Compare with baselines
# Identify degradations
# Predict future capacity needs
```

#### 2. Performance Optimization

```bash
# 2.1 Database optimization
# Add indexes
kubectl exec -it deployment/postgres -n production -- psql \
  -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
  -c "CREATE INDEX idx_name ON table_name (column);"

# Optimize queries
# Update query plans
# Analyze slow queries

# 2.2 Cache optimization
# Increase cache size
# Adjust TTL
# Add cache warming

# 2.3 Application optimization
# Optimize code
# Add caching
# Optimize algorithms

# 2.4 Infrastructure optimization
# Scale resources
# Adjust resource limits
# Optimize networking
```

#### 3. Performance Testing

```bash
# 3.1 Load testing
k6 run tests/load-test.js

# 3.2 Stress testing
k6 run tests/stress-test.js

# 3.3 Endurance testing
k6 run tests/endurance-test.js

# 3.4 Memory leak testing
k6 run tests/memory-leak-test.js
```

### Success Criteria

- ✅ P95 latency < 200ms
- ✅ P99 latency < 500ms
- ✅ Error rate < 1%
- ✅ Throughput > 1000 req/s
- ✅ Cache hit rate > 90%
- ✅ Database query time P95 < 50ms

### Escalation

| Issue | Escalate To | Timeline |
|-------|------------|----------|
| Performance degradation > 20% | Engineering Lead | Within 30 minutes |
| SLA breach | CTO | Immediately |
| Cannot meet performance targets | CTO | Within 24 hours |

---

## Appendix

### Contact Information

| Role | Email | Slack | Phone |
|------|-------|-------|-------|
| On-Call Engineer | oncall@machinenativeops.com | @oncall | +1-XXX-XXX-XXXX |
| Operations Manager | ops@machinenativeops.com | #operations | +1-XXX-XXX-XXXX |
| Engineering Lead | eng@machinenativeops.com | #engineering | +1-XXX-XXX-XXXX |
| Security Team | security@machinenativeops.com | #security | +1-XXX-XXX-XXXX |
| Incident Commander | incident@machinenativeops.com | #incident-response | +1-XXX-XXX-XXXX |

### Useful Commands

```bash
# Quick health check
kubectl exec -it deployment/machine-native-ops -n production -- \
  curl http://localhost:8000/health

# Check pod status
kubectl get pods -n production

# Check logs
kubectl logs -l app=machine-native-ops -n production --tail=100

# Scale deployment
kubectl scale deployment/machine-native-ops --replicas=5 -n production

# Restart deployment
kubectl rollout restart deployment/machine-native-ops -n production

# Check backups
velero backup get

# Restore from backup
velero restore create test-restore --from-backup <backup-name> --wait

# Port forward services
kubectl port-forward -n production svc/machine-native-ops 8000:8000
kubectl port-forward -n monitoring svc/prometheus 9090:9090
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

---

**Last Updated:** 2026-01-27
**Version:** 1.0.0
**Maintained By:** Machine Native Ops Team
**Review Frequency:** Monthly
**Next Review:** 2026-02-27