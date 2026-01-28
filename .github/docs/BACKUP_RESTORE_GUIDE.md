# GL Unified Charter Activated
# Backup and Recovery Guide

## Overview

This guide provides comprehensive procedures for backing up and restoring the Machine Native Ops production environment using Velero, CronJobs, and S3 storage.

---

## Table of Contents

1. [Backup Architecture](#backup-architecture)
2. [Backup Configuration](#backup-configuration)
3. [Backup Procedures](#backup-procedures)
4. [Restore Procedures](#restore-procedures)
5. [Backup Testing](#backup-testing)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

---

## Backup Architecture

### 3-2-1 Backup Rule

The backup strategy follows the industry-standard 3-2-1 rule:

- **3** copies of data (production, backup, archive)
- **2** different storage types (Kubernetes, S3)
- **1** offsite copy (S3 in different region)

### Backup Components

| Component | Purpose | Tool |
|-----------|---------|------|
| Cluster Backups | Kubernetes resources and PVs | Velero |
| Database Backups | PostgreSQL dumps | CronJob + pg_dump |
| Cache Backups | Redis RDB files | CronJob + redis-cli |
| Configuration Backups | ConfigMaps and Secrets | Velero |
| Archive Backups | Long-term retention | S3 Glacier |

### Backup Schedule

| Backup Type | Frequency | Retention | Storage |
|-------------|-----------|-----------|---------|
| Full Cluster Backup | Daily (2 AM UTC) | 30 days | S3 Standard |
| Incremental Backup | Hourly | 7 days | S3 Standard |
| PostgreSQL Backup | Every 4 hours | 30 days | S3 Standard |
| Redis Backup | Every 30 minutes | 7 days | S3 Standard |
| Configuration Backup | Every 30 minutes | 90 days | S3 Standard |
| Archive Backup | Weekly | 1 year | S3 Glacier |

---

## Backup Configuration

### Velero Configuration

#### Install Velero

```bash
# Install Velero CLI
curl -L https://github.com/vmware-tanzu/velero/releases/download/v1.12.0/velero-v1.12.0-linux-amd64.tar.gz -o velero.tar.gz
tar -xvf velero.tar.gz
sudo mv velero-v1.12.0-linux-amd64/velero /usr/local/bin/

# Create S3 bucket
aws s3api create-bucket \
  --bucket machinenativeops-backups \
  --region us-east-1 \
  --create-bucket-configuration LocationConstraint=us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket machinenativeops-backups \
  --versioning-configuration Status=Enabled

# Set lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket machinenativeops-backups \
  --lifecycle-configuration file://lifecycle-policy.json

# Create Velero secret
kubectl create secret generic velero-s3-credentials \
  --namespace velero \
  --from-file=cloud=~/.aws/credentials

# Install Velero
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket machinenativeops-backups \
  --secret-file ~/.aws/credentials \
  --use-volume-snapshots=false \
  --backup-location-config region=us-east-1 \
  --namespace velero
```

#### Configure Backup Storage Location

```yaml
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: machinenativeops-backups
    prefix: velero
  config:
    region: us-east-1
    s3Url: https://s3.amazonaws.com
    s3ForcePathStyle: "true"
  accessMode: ReadWrite
```

#### Configure Volume Snapshot Location

```yaml
apiVersion: velero.io/v1
kind: VolumeSnapshotLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  config:
    region: us-east-1
```

### Backup Schedules

#### Daily Full Cluster Backup

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-cluster-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM UTC
  template:
    includedNamespaces:
    - production
    - istio-system
    - monitoring
    - velero
    excludedResources:
    - events
    - pods
    - endpoints
    ttl: 720h  # 30 days
    storageLocation: default
    volumeSnapshotLocations:
    - default
    hooks:
      resources:
      - name: pre-backup-hook
        includedNamespaces:
        - production
        labelSelector:
          matchLabels:
            app: machine-native-ops
        pre:
          - exec:
              container: app
              command:
              - /bin/sh
              - -c
              - "echo 'Starting backup' && python -m pytest tests/backup_validation.py"
              onError: Continue
              timeout: 600s
```

#### Hourly Incremental Backup

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: hourly-incremental-backup
  namespace: velero
spec:
  schedule: "0 * * * *"  # Hourly
  template:
    includedNamespaces:
    - production
    excludedResources:
    - events
    - pods
    - endpoints
    ttl: 168h  # 7 days
    storageLocation: default
    volumeSnapshotLocations:
    - default
```

### Database Backup Configuration

#### PostgreSQL Backup CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: production
spec:
  schedule: "0 */4 * * *"  # Every 4 hours
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      backoffLimit: 3
      template:
        spec:
          containers:
          - name: postgres-backup
            image: postgres:15-alpine
            command:
            - /bin/sh
            - -c
            - |
              TIMESTAMP=$(date +%Y%m%d-%H%M%S)
              BACKUP_FILE="/backup/postgres-${TIMESTAMP}.dump"
              
              echo "Starting PostgreSQL backup at $(date)"
              PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump \
                -h "${POSTGRES_HOST}" \
                -p "${POSTGRES_PORT}" \
                -U "${POSTGRES_USER}" \
                -d "${POSTGRES_DB}" \
                --format=custom \
                --compress=9 \
                --file="${BACKUP_FILE}"
              
              BACKUP_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
              echo "Backup completed: ${BACKUP_FILE} (${BACKUP_SIZE})"
              
              # Clean up old backups (keep last 30)
              ls -t /backup/postgres-*.dump | tail -n +31 | xargs rm -f
              
              echo "Backup finished at $(date)"
            env:
            - name: POSTGRES_HOST
              value: "postgresql.production.svc.cluster.local"
            - name: POSTGRES_PORT
              value: "5432"
            - name: POSTGRES_DB
              valueFrom:
                secretKeyRef:
                  name: machine-native-ops-secrets
                  key: postgres-db
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: machine-native-ops-secrets
                  key: postgres-user
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: machine-native-ops-secrets
                  key: postgres-password
            volumeMounts:
            - name: backup
              mountPath: /backup
          volumes:
          - name: backup
            persistentVolumeClaim:
              claimName: postgres-backup-pvc
          restartPolicy: OnFailure
```

#### Redis Backup CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: redis-backup
  namespace: production
spec:
  schedule: "*/30 * * * *"  # Every 30 minutes
  successfulJobsHistoryLimit: 5
  failedJobsHistoryLimit: 5
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      backoffLimit: 3
      template:
        spec:
          containers:
          - name: redis-backup
            image: redis:7-alpine
            command:
            - /bin/sh
            - -c
            - |
              TIMESTAMP=$(date +%Y%m%d-%H%M%S)
              BACKUP_FILE="/backup/redis-${TIMESTAMP}.rdb"
              
              echo "Starting Redis backup at $(date)"
              redis-cli -h "${REDIS_HOST}" -p "${REDIS_PORT}" \
                --rdb "${BACKUP_FILE}"
              
              BACKUP_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
              echo "Backup completed: ${BACKUP_FILE} (${BACKUP_SIZE})"
              
              # Clean up old backups (keep last 50)
              ls -t /backup/redis-*.rdb | tail -n +51 | xargs rm -f
              
              echo "Backup finished at $(date)"
            env:
            - name: REDIS_HOST
              value: "redis-leader.production.svc.cluster.local"
            - name: REDIS_PORT
              value: "6379"
            volumeMounts:
            - name: backup
              mountPath: /backup
          volumes:
          - name: backup
            persistentVolumeClaim:
              claimName: redis-backup-pvc
          restartPolicy: OnFailure
```

---

## Backup Procedures

### Manual Cluster Backup

```bash
# Create on-demand backup
velero backup create manual-backup-$(date +%Y%m%d-%H%M%S) \
  --include-namespaces production,istio-system,monitoring \
  --wait

# Create backup with specific resources
velero backup create deployment-backup \
  --include-namespaces production \
  --include-resources deployments,services,configmaps \
  --selector app=machine-native-ops \
  --wait

# Create backup excluding certain resources
velero backup create partial-backup \
  --include-namespaces production \
  --exclude-resources secrets,persistentvolumes \
  --wait

# Verify backup
velero backup describe manual-backup-$(date +%Y%m%d-%H%M%S) --details
```

### Manual Database Backup

```bash
# Trigger PostgreSQL backup job
kubectl create job postgres-manual-backup-$(date +%Y%m%d-%H%M%S) \
  --from=cronjob/postgres-backup \
  -n production

# Trigger Redis backup job
kubectl create job redis-manual-backup-$(date +%Y%m%d-%H%M%S) \
  --from=cronjob/redis-backup \
  -n production

# Monitor job status
kubectl get jobs -n production
kubectl logs -l job-name=postgres-manual-backup-$(date +%Y%m%d-%H%M%S) -n production -f
```

### Backup Verification

```bash
# List all backups
velero backup get

# Check backup status
velero backup get <backup-name> -o jsonpath='{.status.phase}'

# Get backup details
velero backup describe <backup-name> --details

# Check backup size
velero backup get <backup-name> -o jsonpath='{.status.volumeSnapshots}'

# List backup files in S3
aws s3 ls s3://machinenativeops-backups/velero/backups/<backup-name>/

# Verify backup integrity
velero backup create test-backup \
  --include-namespaces production \
  --wait

# Test restore (dry-run)
velero restore create test-restore \
  --from-backup test-backup \
  --dry-run \
  --wait
```

### Backup Monitoring

```bash
# Check Velero pod status
kubectl get pods -n velero

# Check Velero logs
kubectl logs -n velero deployment/velero

# Monitor backup schedules
velero schedule get

# Check backup schedule status
velero schedule describe daily-cluster-backup

# Check recent backup jobs
kubectl get jobs -n production -l backup=true

# View backup metrics
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# Query: velero_backup_total{status="completed"}
```

---

## Restore Procedures

### Full Cluster Restore

```bash
# List available backups
velero backup get

# Restore from specific backup
velero restore create full-restore-$(date +%Y%m%d-%H%M%S) \
  --from-backup <backup-name> \
  --wait

# Restore with include namespaces
velero restore create partial-restore \
  --from-backup <backup-name> \
  --include-namespaces production \
  --wait

# Restore with exclude namespaces
velero restore create restore-without-monitoring \
  --from-backup <backup-name> \
  --exclude-namespaces monitoring,velero \
  --wait

# Check restore status
velero restore get
velero restore describe <restore-name> --details

# Monitor restore progress
watch velero restore get
```

### Single Namespace Restore

```bash
# Restore only production namespace
velero restore create production-restore \
  --from-backup <backup-name> \
  --include-namespaces production \
  --wait

# Restore with resource filters
velero restore create selective-restore \
  --from-backup <backup-name> \
  --include-namespaces production \
  --include-resources deployments,services,configmaps \
  --wait

# Restore with label selector
velero restore create app-restore \
  --from-backup <backup-name> \
  --selector app=machine-native-ops \
  --wait
```

### Database Restore

#### PostgreSQL Restore

```bash
# List available backups
kubectl exec -it deployment/postgres-backup -n production -- \
  ls -lh /backup/

# Identify backup to restore
BACKUP_FILE="postgres-20240127-020000.dump"

# Copy backup to PostgreSQL pod
kubectl cp deployment/postgres-backup:/backup/${BACKUP_FILE} \
  /tmp/${BACKUP_FILE} -n production
kubectl cp /tmp/${BACKUP_FILE} \
  deployment/postgres:/tmp/${BACKUP_FILE} -n production

# Restore database
kubectl exec -it deployment/postgres -n production -- \
  bash -c "PGPASSWORD=${POSTGRES_PASSWORD} pg_restore \
    -h localhost \
    -U ${POSTGRES_USER} \
    -d ${POSTGRES_DB} \
    -v /tmp/${BACKUP_FILE}"

# Alternative: Drop and recreate database
kubectl exec -it deployment/postgres -n production -- \
  bash -c "PGPASSWORD=${POSTGRES_PASSWORD} psql \
    -h localhost \
    -U ${POSTGRES_USER} \
    -c &quot;DROP DATABASE IF EXISTS ${POSTGRES_DB};&quot; \
    -c &quot;CREATE DATABASE ${POSTGRES_DB};&quot;"

kubectl exec -it deployment/postgres -n production -- \
  bash -c "PGPASSWORD=${POSTGRES_PASSWORD} pg_restore \
    -h localhost \
    -U ${POSTGRES_USER} \
    -d ${POSTGRES_DB} \
    -v /tmp/${BACKUP_FILE}"

# Verify restore
kubectl exec -it deployment/postgres -n production -- \
  psql -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "\dt"
```

#### Redis Restore

```bash
# List available backups
kubectl exec -it deployment/redis-backup -n production -- \
  ls -lh /backup/

# Identify backup to restore
BACKUP_FILE="redis-20240127-020000.rdb"

# Copy backup to Redis pod
kubectl cp deployment/redis-backup:/backup/${BACKUP_FILE} \
  /tmp/${BACKUP_FILE} -n production
kubectl cp /tmp/${BACKUP_FILE} \
  deployment/redis-leader:/data/dump.rdb -n production

# Restart Redis to load backup
kubectl rollout restart deployment/redis-leader -n production

# Verify restore
kubectl exec -it deployment/redis-leader -n production -- \
  redis-cli -h localhost INFO keyspace

# Check key count
kubectl exec -it deployment/redis-leader -n production -- \
  redis-cli -h localhost DBSIZE
```

### Selective Resource Restore

```bash
# Restore only specific deployments
velero restore create deployment-restore \
  --from-backup <backup-name> \
  --include-namespaces production \
  --include-resources deployments \
  --selector app=machine-native-ops \
  --wait

# Restore only ConfigMaps and Secrets
velero restore create config-restore \
  --from-backup <backup-name> \
  --include-namespaces production \
  --include-resources configmaps,secrets \
  --wait

# Restore excluding certain resources
velero restore create exclude-secrets-restore \
  --from-backup <backup-name> \
  --exclude-resources secrets \
  --wait

# Restore with namespace mapping
velero restore create namespace-mapping-restore \
  --from-backup <backup-name> \
  --namespace-mappings production:production-restored \
  --wait
```

### Disaster Recovery Restore

```bash
# Step 1: Verify cluster is healthy
kubectl get nodes
kubectl get pods -n kube-system

# Step 2: Install Velero (if not installed)
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket machinenativeops-backups \
  --secret-file ~/.aws/credentials \
  --use-volume-snapshots=false \
  --namespace velero

# Step 3: Verify backup storage location
kubectl get backupstoragelocations -n velero
velero backup-location get

# Step 4: List available backups
velero backup get

# Step 5: Restore latest backup
velero restore create disaster-recovery \
  --from-backup <latest-backup> \
  --wait

# Step 6: Verify restore status
velero restore get
velero restore describe disaster-recovery --details

# Step 7: Check restored resources
kubectl get all -n production
kubectl get pods -n production

# Step 8: Restart applications
kubectl rollout restart deployment/machine-native-ops -n production

# Step 9: Verify application health
kubectl exec -it deployment/machine-native-ops -n production -- \
  curl http://localhost:8000/health

# Step 10: Monitor application metrics
# Check Grafana dashboards
# Verify error rate < 1%
# Verify P95 latency < 1s
```

---

## Backup Testing

### Backup Integrity Test

```bash
# Create test backup
velero backup create integrity-test-backup \
  --include-namespaces production \
  --wait

# Verify backup
velero backup describe integrity-test-backup --details

# Test restore (dry-run)
velero restore create integrity-test-restore \
  --from-backup integrity-test-backup \
  --dry-run \
  --wait

# Check restore plan
velero restore describe integrity-test-restore --details

# Delete test backup
velero backup delete integrity-test-backup --confirm
```

### Database Restore Test

```bash
# Create test database
kubectl exec -it deployment/postgres -n production -- \
  psql -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
  -c "CREATE TABLE test_backup (id SERIAL PRIMARY KEY, data TEXT);"

kubectl exec -it deployment/postgres -n production -- \
  psql -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
  -c "INSERT INTO test_backup (data) VALUES ('backup-test');"

# Backup database
kubectl create job postgres-test-backup \
  --from=cronjob/postgres-backup \
  -n production

# Wait for backup to complete
kubectl wait --for=condition=complete job/postgres-test-backup -n production --timeout=300s

# Drop test table
kubectl exec -it deployment/postgres -n production -- \
  psql -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
  -c "DROP TABLE test_backup;"

# Verify table is dropped
kubectl exec -it deployment/postgres -n production -- \
  psql -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
  -c "\dt"

# Restore database
kubectl exec -it deployment/postgres -n production -- \
  bash -c "PGPASSWORD=${POSTGRES_PASSWORD} pg_restore \
    -h localhost \
    -U ${POSTGRES_USER} \
    -d ${POSTGRES_DB} \
    -v /backup/postgres-test-backup-*.dump"

# Verify table is restored
kubectl exec -it deployment/postgres -n production -- \
  psql -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
  -c "\dt"

# Clean up
kubectl exec -it deployment/postgres -n production -- \
  psql -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
  -c "DROP TABLE test_backup;"
```

### Full Disaster Recovery Test

```bash
# Pre-test: Document current state
kubectl get all -n production -o yaml > /tmp/pre-test-state.yaml

# Step 1: Create backup
velero backup create dr-test-backup \
  --include-namespaces production,istio-system,monitoring \
  --wait

# Step 2: Delete production namespace
kubectl delete namespace production --force --grace-period=0

# Step 3: Verify namespace is deleted
kubectl get namespace production
# Should return "Not found"

# Step 4: Restore from backup
velero restore create dr-test-restore \
  --from-backup dr-test-backup \
  --wait

# Step 5: Verify namespace is restored
kubectl get namespace production

# Step 6: Check all resources are restored
kubectl get all -n production

# Step 7: Verify pods are running
kubectl wait --for=condition=ready pod -l app=machine-native-ops -n production --timeout=300s

# Step 8: Verify application health
kubectl exec -it deployment/machine-native-ops -n production -- \
  curl http://localhost:8000/health

# Step 9: Compare with pre-test state
kubectl get all -n production -o yaml > /tmp/post-test-state.yaml
diff /tmp/pre-test-state.yaml /tmp/post-test-state.yaml

# Step 10: Clean up test backup
velero backup delete dr-test-backup --confirm
```

---

## Troubleshooting

### Backup Failures

#### Issue: Backup fails with "Access Denied"

**Symptoms:**
```bash
velero backup create test-backup --wait
# Error: rpc error: code = Unknown desc = Access Denied
```

**Solution:**
```bash
# Check Velero secret
kubectl get secret velero-s3-credentials -n velero -o yaml

# Update AWS credentials
kubectl delete secret velero-s3-credentials -n velero
kubectl create secret generic velero-s3-credentials \
  --namespace velero \
  --from-file=cloud=~/.aws/credentials

# Restart Velero
kubectl rollout restart deployment/velero -n velero

# Test backup again
velero backup create test-backup --wait
```

#### Issue: Backup times out

**Symptoms:**
```bash
velero backup create test-backup --wait --timeout=10m
# Error: backup timed out
```

**Solution:**
```bash
# Check Velero logs
kubectl logs -n velero deployment/velero

# Increase timeout
velero backup create test-backup --wait --timeout=30m

# Check resource usage
kubectl top pod -n velero

# If Velero is resource constrained
kubectl edit deployment velero -n velero
# Increase CPU/memory requests and limits
```

#### Issue: Partial backup (some resources excluded)

**Symptoms:**
```bash
velero backup describe test-backup --details
# Shows some resources excluded
```

**Solution:**
```bash
# Check backup details
velero backup describe test-backup --details

# Look for excluded resources
# Check if they should be excluded

# If backup configuration is wrong
kubectl edit schedule daily-cluster-backup -n velero
# Update excludedResources field

# Test backup again
velero backup create test-backup --wait
```

### Restore Failures

#### Issue: Restore fails with "Resource already exists"

**Symptoms:**
```bash
velero restore create test-restore --from-backup test-backup --wait
# Error: resource already exists
```

**Solution:**
```bash
# Check existing resources
kubectl get all -n production

# Option 1: Delete existing resources before restore
kubectl delete namespace production --force --grace-period=0

# Option 2: Use existing resources policy
velero restore create test-restore \
  --from-backup test-backup \
  --existing-resource-policy=update \
  --wait

# Option 3: Selective restore
velero restore create test-restore \
  --from-backup test-backup \
  --include-resources deployments \
  --wait
```

#### Issue: Restore fails with "Invalid namespace"

**Symptoms:**
```bash
velero restore create test-restore --from-backup test-backup --wait
# Error: namespace not found
```

**Solution:**
```bash
# Check backup namespaces
velero backup describe test-backup --details

# Create missing namespaces
kubectl create namespace production
kubectl create namespace istio-system

# Retry restore
velero restore create test-restore \
  --from-backup test-backup \
  --wait
```

#### Issue: Restore fails for database

**Symptoms:**
```bash
# PostgreSQL restore fails
kubectl exec -it deployment/postgres -n production -- \
  pg_restore -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} -v /backup/backup.dump
# Error: database is being accessed by other users
```

**Solution:**
```bash
# Stop application
kubectl scale deployment/machine-native-ops --replicas=0 -n production

# Terminate all connections
kubectl exec -it deployment/postgres -n production -- \
  psql -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
  -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${POSTGRES_DB}' AND pid <> pg_backend_pid();"

# Restore database
kubectl exec -it deployment/postgres -n production -- \
  bash -c "PGPASSWORD=${POSTGRES_PASSWORD} pg_restore \
    -h localhost \
    -U ${POSTGRES_USER} \
    -d ${POSTGRES_DB} \
    -v /backup/backup.dump"

# Start application
kubectl scale deployment/machine-native-ops --replicas=3 -n production
```

### Storage Issues

#### Issue: S3 bucket full

**Symptoms:**
```bash
velero backup create test-backup --wait
# Error: bucket is full
```

**Solution:**
```bash
# Check bucket size
aws s3 ls s3://machinenativeops-backups/ --recursive --summarize --human-readable

# Clean up old backups
velero backup delete old-backup-1 --confirm
velero backup delete old-backup-2 --confirm

# Update lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket machinenativeops-backups \
  --lifecycle-configuration file://lifecycle-policy.json

# Increase bucket size
aws s3api put-bucket-versioning \
  --bucket machinenativeops-backups \
  --versioning-configuration Status=Enabled
```

#### Issue: Persistent volume restore fails

**Symptoms:**
```bash
velero restore create test-restore --from-backup test-backup --wait
# Error: persistent volume claim not bound
```

**Solution:**
```bash
# Check PVC status
kubectl get pvc -n production

# Check PV status
kubectl get pv

# If PV is stuck
kubectl delete pvc <pvc-name> -n production

# Recreate PVC from backup
velero restore create pvc-restore \
  --from-backup test-backup \
  --include-resources persistentvolumeclaims \
  --wait
```

---

## Best Practices

### Backup Best Practices

1. **Automate Everything**
   - Use Velero schedules for automated backups
   - Use CronJobs for database backups
   - Never rely on manual backups

2. **Test Regularly**
   - Perform monthly backup integrity tests
   - Test disaster recovery quarterly
   - Document test results

3. **Monitor Backups**
   - Set up alerts for backup failures
   - Monitor backup duration and size
   - Track restore success rate

4. **Follow 3-2-1 Rule**
   - 3 copies of data
   - 2 different storage types
   - 1 offsite copy

5. **Secure Backups**
   - Encrypt backups at rest
   - Use IAM roles for S3 access
   - Rotate access keys regularly

### Restore Best Practices

1. **Document Procedures**
   - Create detailed runbooks
   - Include step-by-step instructions
   - Document common issues and solutions

2. **Test Restores**
   - Test restore procedures regularly
   - Document restore time (RTO)
   - Track data loss (RPO)

3. **Plan for Failures**
   - Have rollback procedures
   - Know when to escalate
   - Have contact information ready

4. **Communicate**
   - Notify stakeholders before restore
   - Provide updates during restore
   - Document post-restore actions

### Backup Retention Policy

| Backup Type | Retention | Reason |
|-------------|-----------|--------|
| Daily full backups | 30 days | Covers most recent issues |
| Hourly incremental backups | 7 days | Fine-grained recovery |
| PostgreSQL backups | 30 days | Database recovery point |
| Redis backups | 7 days | Cache recovery |
| Archive backups | 1 year | Compliance requirements |

### Monitoring Checklist

- [ ] Velero pod is running
- [ ] Backup schedules are active
- [ ] Backup jobs are completing successfully
- [ ] Backup size is within expected range
- [ ] S3 storage has sufficient space
- [ ] Backup duration is within SLA
- [ ] Restore tests are passing
- [ ] Alerts are configured for failures

---

## Appendix

### Useful Commands

```bash
# List all backups
velero backup get

# Describe backup
velero backup describe <backup-name> --details

# Delete backup
velero backup delete <backup-name> --confirm

# List schedules
velero schedule get

# Create schedule
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --include-namespaces production

# List restores
velero restore get

# Describe restore
velero restore describe <restore-name> --details

# Delete restore
velero restore delete <restore-name> --confirm

# Check Velero logs
kubectl logs -n velero deployment/velero

# Restart Velero
kubectl rollout restart deployment/velero -n velero

# Check S3 bucket
aws s3 ls s3://machinenativeops-backups/

# Get bucket size
aws s3 ls s3://machinenativeops-backups/ --recursive --summarize
```

### Contact Information

- **Backup Team:** backup@machinenativeops.com
- **On-Call:** +1-XXX-XXX-XXXX
- **Slack:** #backup-alerts

### Additional Resources

- [Velero Documentation](https://velero.io/docs/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [PostgreSQL Backup](https://www.postgresql.org/docs/current/backup.html)
- [Redis Persistence](https://redis.io/topics/persistence)

---

**Last Updated:** 2026-01-27
**Version:** 1.0.0
**Maintained By:** Machine Native Ops Team