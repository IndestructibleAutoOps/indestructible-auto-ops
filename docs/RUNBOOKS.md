# Production Runbooks

## Table of Contents

1. [Incident Response](#incident-response)
2. [Operational Procedures](#operational-procedures)
3. [Emergency Procedures](#emergency-procedures)
4. [Maintenance Windows](#maintenance-windows)

---

## Incident Response

### Critical Severity Incidents

#### Alert: High Error Rate (>5%)

**Impact:** High - Users experiencing errors

**Response Time:** < 5 minutes

**Procedure:**

1. **Acknowledge Alert** (0-1 min)
   - Open PagerDuty incident
   - Post in #critical-alerts Slack channel
   - Assign to on-call engineer

2. **Assess Situation** (1-3 min)
   ```bash
   # Check error rate
   kubectl port-forward -n monitoring svc/prometheus 9090:9090
   # Query: rate(http_requests_total{status=~"5.."}[5m])
   
   # Check recent changes
   kubectl rollout history deployment/machine-native-ops -n production
   ```

3. **Identify Root Cause** (3-10 min)
   - Review application logs:
     ```bash
     kubectl logs -l app=machine-native-ops -n production --tail=500 | grep ERROR
     ```
   - Check Istio metrics:
     ```bash
     istioctl proxy-config clusters <pod-name> -n production
     ```
   - Check database connectivity:
     ```bash
     kubectl exec -it deployment/machine-native-ops -n production -- \
       psql -h postgresql.production.svc.cluster.local -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT 1"
     ```
   - Check Redis connectivity:
     ```bash
     kubectl exec -it deployment/machine-native-ops -n production -- \
       redis-cli -h redis-leader.production.svc.cluster.local ping
     ```

4. **Implement Fix** (5-15 min)
   
   **If recent deployment caused issue:**
   ```bash
   kubectl rollout undo deployment/machine-native-ops -n production
   kubectl rollout status deployment/machine-native-ops -n production
   ```
   
   **If database issue:**
   ```bash
   kubectl rollout restart deployment/postgresql -n production
   ```
   
   **If Redis issue:**
   ```bash
   kubectl rollout restart deployment/redis-leader -n production
   ```
   
   **If resource exhaustion:**
   ```bash
   kubectl top pods -n production
   kubectl scale deployment/machine-native-ops --replicas=5 -n production
   ```

5. **Verify Resolution** (15-20 min)
   - Monitor Grafana dashboards
   - Check error rate dropping below 1%
   - Verify application health:
     ```bash
     kubectl exec -it deployment/machine-native-ops -n production -- \
       curl http://localhost:8000/health
     ```

6. **Document Incident** (Post-incident)
   - Update incident ticket with timeline
   - Conduct post-mortem
   - Create action items to prevent recurrence

---

#### Alert: High Latency (P95 > 1s)

**Impact:** Medium - Slow user experience

**Response Time:** < 15 minutes

**Procedure:**

1. **Assess Latency**
   ```bash
   # Check current latency in Grafana
   # Open dashboard: machine-native-ops-prod
   # Look at "Response Time" panel
   ```

2. **Identify Bottlenecks**
   ```bash
   # Check Jaeger traces
   kubectl port-forward -n istio-system svc/jaeger-query 16686:16686
   # Open http://localhost:16686
   # Search slow operations
   ```

3. **Check Resource Usage**
   ```bash
   kubectl top pods -n production
   kubectl top nodes
   ```

4. **Implement Fixes**
   
   **If CPU high:**
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=5 -n production
   ```
   
   **If memory high:**
   ```bash
   # Restart pods to free memory
   kubectl rollout restart deployment/machine-native-ops -n production
   ```
   
   **If database slow:**
   ```bash
   # Check DB connections
   kubectl exec -it deployment/postgresql -n production -- \
     psql -h postgresql.production.svc.cluster.local -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
     -c "SELECT count(*) FROM pg_stat_activity;"
   ```

5. **Monitor Recovery**
   - Watch latency metrics in Grafana
   - Wait for P95 < 1s

---

#### Alert: Database Connection Failures

**Impact:** Critical - Application unusable

**Response Time:** < 5 minutes

**Procedure:**

1. **Check PostgreSQL Status**
   ```bash
   kubectl get pods -n production -l app=postgresql
   kubectl describe pod <postgres-pod> -n production
   kubectl logs <postgres-pod> -n production
   ```

2. **Test Connectivity**
   ```bash
   kubectl exec -it deployment/machine-native-ops -n production -- \
     psql -h postgresql.production.svc.cluster.local \
           -U ${POSTGRES_USER} \
           -d ${POSTGRES_DB} \
           -c "SELECT 1;"
   ```

3. **Check Resources**
   ```bash
   kubectl top pod <postgres-pod> -n production
   ```

4. **Restart PostgreSQL** (if needed)
   ```bash
   kubectl rollout restart deployment/postgresql -n production
   kubectl rollout status deployment/postgresql -n production
   ```

5. **Verify Connectivity**
   ```bash
   kubectl exec -it deployment/machine-native-ops -n production -- \
     psql -h postgresql.production.svc.cluster.local \
           -U ${POSTGRES_USER} \
           -d ${POSTGRES_DB} \
           -c "SELECT version();"
   ```

---

#### Alert: Pod Restarts (>5/hour)

**Impact:** Medium - Potential stability issues

**Response Time:** < 30 minutes

**Procedure:**

1. **Identify Restarting Pods**
   ```bash
   kubectl get pods -n production
   kubectl get pods -n production --sort-by='.status.containerStatuses[0].restartCount'
   ```

2. **Check Pod Logs**
   ```bash
   kubectl logs <pod-name> -n production --previous
   kubectl describe pod <pod-name> -n production
   ```

3. **Common Causes:**
   
   **OOMKilled (Out of Memory):**
   ```bash
   # Increase memory limits
   kubectl set resources deployment/machine-native-ops \
     --limits=memory=2Gi \
     --requests=memory=1Gi \
     -n production
   ```
   
   **CrashLoopBackOff (Application Error):**
   - Review application logs
   - Fix application issue
   - Redeploy
   
   **Liveness/Readiness Probe Failures:**
   ```bash
   # Adjust probe thresholds
   kubectl edit deployment machine-native-ops -n production
   # Increase initialDelaySeconds, timeoutSeconds
   ```

4. **Monitor Stability**
   - Watch restart count stabilize
   - Monitor error rate

---

### Warning Severity Incidents

#### Alert: High Memory Usage (>90%)

**Impact:** Low - Potential for OOM kills

**Response Time:** < 1 hour

**Procedure:**

1. **Check Memory Usage**
   ```bash
   kubectl top pods -n production --sort-by=memory
   ```

2. **Identify Memory Leaks**
   ```bash
   # Check memory profiles
   kubectl exec -it <pod-name> -n production -- \
     python -m memory_profiler <script>
   ```

3. **Scale Up or Optimize**
   
   **Option 1: Scale up**
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=5 -n production
   ```
   
   **Option 2: Increase limits**
   ```bash
   kubectl set resources deployment/machine-native-ops \
     --limits=memory=2Gi \
     -n production
   ```
   
   **Option 3: Fix memory leak**
   - Review code for memory leaks
   - Redeploy with fix

---

#### Alert: High CPU Usage (>90%)

**Impact:** Low - Performance degradation

**Response Time:** < 1 hour

**Procedure:**

1. **Check CPU Usage**
   ```bash
   kubectl top pods -n production --sort-by=cpu
   ```

2. **Identify CPU Intensive Processes**
   ```bash
   kubectl exec -it <pod-name> -n production -- top
   ```

3. **Scale Up or Optimize**
   
   **Option 1: Scale up**
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=5 -n production
   ```
   
   **Option 2: Increase CPU limits**
   ```bash
   kubectl set resources deployment/machine-native-ops \
     --limits=cpu=2000m \
     -n production
   ```
   
   **Option 3: Optimize code**
   - Profile CPU usage
   - Optimize algorithms
   - Redeploy with fix

---

#### Alert: Backup Failure

**Impact:** Medium - Data loss risk

**Response Time:** < 2 hours

**Procedure:**

1. **Check Velero Status**
   ```bash
   kubectl get pods -n velero
   kubectl logs -n velero deployment/velero
   ```

2. **Check Backup Status**
   ```bash
   velero backup get
   velero backup describe <failed-backup> --details
   ```

3. **Check S3 Access**
   ```bash
   aws s3 ls s3://machinenativeops-backups/
   ```

4. **Fix Common Issues**
   
   **S3 Credentials expired:**
   ```bash
   kubectl delete secret velero-s3-credentials -n velero
   kubectl create secret generic velero-s3-credentials \
     --namespace velero \
     --from-file=cloud=~/.aws/credentials
   kubectl rollout restart deployment/velero -n velero
   ```
   
   **Insufficient permissions:**
   - Update IAM role permissions
   - Apply changes
   
   **S3 bucket full:**
   - Clean up old backups
   - Increase bucket size

5. **Test Backup**
   ```bash
   velero backup create test-backup --wait
   velero backup describe test-backup --details
   ```

---

## Operational Procedures

### Deployment

#### Standard Deployment

**Frequency:** As needed

**Procedure:**

1. **Pre-Deployment Checks**
   ```bash
   # Check current health
   kubectl get pods -n production
   kubectl exec -it deployment/machine-native-ops -n production -- \
     curl http://localhost:8000/health
   
   # Check metrics
   # Open Grafana dashboard: machine-native-ops-prod
   # Verify error rate < 1%
   # Verify P95 latency < 1s
   ```

2. **Deploy New Version**
   ```bash
   # Update image
   kubectl set image deployment/machine-native-ops \
     app=ghcr.io/machinenativeops/machine-native-ops:v2.0.0 \
     -n production
   
   # Monitor rollout
   kubectl rollout status deployment/machine-native-ops -n production
   ```

3. **Post-Deployment Verification**
   ```bash
   # Check pod status
   kubectl get pods -n production
   
   # Check health
   kubectl exec -it deployment/machine-native-ops -n production -- \
     curl http://localhost:8000/health
   
   # Check metrics in Grafana
   # Monitor for 15 minutes
   ```

4. **Rollback if Needed**
   ```bash
   kubectl rollout undo deployment/machine-native-ops -n production
   kubectl rollout status deployment/machine-native-ops -n production
   ```

---

#### Canary Deployment

**Frequency:** For major releases

**Procedure:**

1. **Deploy Canary Version**
   ```bash
   # Create canary deployment
   kubectl get deployment machine-native-ops -n production -o yaml | \
     sed 's/name: machine-native-ops/name: machine-native-ops-canary/' | \
     sed 's/version: v1/version: v2/' | \
     kubectl apply -f -
   
   # Scale canary to 1 replica
   kubectl scale deployment machine-native-ops-canary --replicas=1 -n production
   ```

2. **Configure Traffic Split**
   ```bash
   kubectl apply -f - <<EOF
   apiVersion: networking.istio.io/v1alpha3
   kind: VirtualService
   metadata:
     name: machine-native-ops
     namespace: production
   spec:
     http:
     - route:
       - destination:
           host: machine-native-ops.production.svc.cluster.local
           subset: v1
         weight: 90
       - destination:
           host: machine-native-ops-canary.production.svc.cluster.local
           subset: v2
         weight: 10
   EOF
   ```

3. **Monitor Canary**
   - Check error rate in Grafana
   - Compare v1 vs v2 metrics
   - Monitor for 30 minutes

4. **Gradual Rollout**
   ```bash
   # Increase to 25% canary traffic
   # Update weights: v1=75, v2=25
   
   # Monitor for 30 minutes
   
   # Increase to 50% canary traffic
   # Update weights: v1=50, v2=50
   
   # Monitor for 30 minutes
   
   # Increase to 100% canary traffic
   # Update weights: v1=0, v2=100
   ```

5. **Complete Migration**
   ```bash
   # Delete old deployment
   kubectl delete deployment machine-native-ops -n production
   
   # Rename canary to production
   kubectl get deployment machine-native-ops-canary -n production -o yaml | \
     sed 's/name: machine-native-ops-canary/name: machine-native-ops/' | \
     kubectl apply -f -
   ```

---

### Scaling

#### Manual Scaling

**When to Use:** Planned load increases, events

**Procedure:**

1. **Scale Up**
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=10 -n production
   kubectl rollout status deployment/machine-native-ops -n production
   ```

2. **Verify Scaling**
   ```bash
   kubectl get pods -n production
   kubectl top pods -n production
   ```

3. **Scale Down** (after load decreases)
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=3 -n production
   ```

---

#### Auto-Scaling Configuration

**Procedure:**

1. **Check Current HPA**
   ```bash
   kubectl get hpa -n production
   kubectl describe hpa machine-native-ops-hpa -n production
   ```

2. **Modify HPA**
   ```bash
   kubectl edit hpa machine-native-ops-hpa -n production
   # Adjust:
   # - minReplicas
   # - maxReplicas
   # - target CPU/Memory utilization
   ```

3. **Test Auto-Scaling**
   ```bash
   # Generate load
   # Monitor HPA behavior
   kubectl get hpa machine-native-ops-hpa -n production -w
   ```

---

### Database Maintenance

#### PostgreSQL Backup

**Frequency:** Every 4 hours (automated)

**Manual Backup:**

```bash
# Create manual backup
kubectl exec -it deployment/postgres-backup -n production -- \
  /bin/sh -c "PGPASSWORD=${POSTGRES_PASSWORD} pg_dump \
    -h ${POSTGRES_HOST} \
    -p ${POSTGRES_PORT} \
    -U ${POSTGRES_USER} \
    -d ${POSTGRES_DB} \
    --format=custom \
    --compress=9 \
    --file=/backup/postgres-manual-$(date +%Y%m%d-%H%M%S).dump"

# List backups
kubectl exec -it deployment/postgres-backup -n production -- \
  ls -lh /backup/
```

---

#### PostgreSQL Restore

**Procedure:**

1. **Identify Backup**
   ```bash
   kubectl exec -it deployment/postgres-backup -n production -- \
     ls -lh /backup/
   ```

2. **Restore Backup**
   ```bash
   kubectl exec -it deployment/postgres -n production -- \
     bash -c "PGPASSWORD=${POSTGRES_PASSWORD} pg_restore \
       -h localhost \
       -U ${POSTGRES_USER} \
       -d ${POSTGRES_DB} \
       -v /backup/postgres-20240127-020000.dump"
   ```

3. **Verify Restore**
   ```bash
   kubectl exec -it deployment/postgres -n production -- \
     psql -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "\dt"
   ```

---

#### Database Vacuum

**Frequency:** Weekly

**Procedure:**

```bash
# Connect to PostgreSQL
kubectl exec -it deployment/postgres -n production -- psql \
  -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB}

# Run vacuum
VACUUM ANALYZE;

# Exit
\q
```

---

### Cache Maintenance

#### Redis Backup

**Frequency:** Every 30 minutes (automated)

**Manual Backup:**

```bash
kubectl exec -it deployment/redis-backup -n production -- \
  redis-cli -h ${REDIS_HOST} -p ${REDIS_PORT} \
  --rdb /backup/redis-manual-$(date +%Y%m%d-%H%M%S).rdb
```

---

#### Redis Flush Cache

**WARNING:** This clears all cache data

**Procedure:**

```bash
# Flush all cache
kubectl exec -it deployment/redis-leader -n production -- \
  redis-cli FLUSHALL

# Flush database 0 only
kubectl exec -it deployment/redis-leader -n production -- \
  redis-cli FLUSHDB
```

---

### Certificate Management

#### Renew TLS Certificate

**Frequency:** Before expiration (90 days)

**Procedure:**

1. **Generate New Certificate**
   ```bash
   # Use cert-manager or your CA
   # Generate new TLS certificate and key
   ```

2. **Update Kubernetes Secret**
   ```bash
   kubectl create secret tls machinenativeops-tls-cert-new \
     --cert=path/to/new-tls.crt \
     --key=path/to/new-tls.key \
     --dry-run=client -o yaml -n production | \
     kubectl apply -f -
   ```

3. **Update Istio Gateway**
   ```bash
   kubectl patch gateway machine-native-ops-gateway -n production \
     --type='json' \
     -p='[{"op": "replace", "path": "/spec/servers/0/tls/credentialName", "value":"machinenativeops-tls-cert-new"}]'
   ```

4. **Verify Certificate**
   ```bash
   # Check certificate expiration
   openssl s_client -connect api.machinenativeops.com:443 -servername api.machinenativeops.com </dev/null | openssl x509 -noout -dates
   ```

---

## Emergency Procedures

### Emergency Stop

**When to Use:** Critical security issue, data corruption risk

**Procedure:**

1. **Scale to Zero**
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=0 -n production
   ```

2. **Verify Stopped**
   ```bash
   kubectl get pods -n production
   ```

3. **Investigate Issue**
   - Review logs
   - Analyze metrics
   - Determine root cause

4. **Resume Service** (after fix)
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=3 -n production
   kubectl rollout status deployment/machine-native-ops -n production
   ```

---

### Emergency Scale-Up

**When to Use:** Unexpected traffic spike, DDoS attack

**Procedure:**

1. **Immediate Scale-Up**
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=20 -n production
   ```

2. **Enable Rate Limiting**
   ```bash
   # Update Istio virtual service
   kubectl apply -f - <<EOF
   apiVersion: networking.istio.io/v1alpha3
   kind: VirtualService
   metadata:
     name: machine-native-ops
     namespace: production
   spec:
     http:
     - match:
       - uri:
           prefix: "/"
       route:
       - destination:
           host: machine-native-ops.production.svc.cluster.local
       fault:
         abort:
           percentage:
             value: 0
         delay:
           percentage:
             value: 0
       retries:
         attempts: 0
   EOF
   ```

3. **Monitor System**
   - Watch Grafana dashboards
   - Check error rate
   - Monitor resource usage

4. **Gradual Scale-Down** (after traffic normalizes)
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=10 -n production
   # Monitor for 15 minutes
   kubectl scale deployment/machine-native-ops --replicas=3 -n production
   ```

---

### Emergency Database Failover

**When to Use:** Primary database failure

**Procedure:**

1. **Check Primary Status**
   ```bash
   kubectl get pods -n production -l app=postgresql
   kubectl logs <postgres-pod> -n production
   ```

2. **Promote Replica** (if using streaming replication)
   ```bash
   # Connect to replica
   kubectl exec -it deployment/postgres-replica -n production -- psql \
     -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB}
   
   # Promote to primary
   SELECT pg_promote();
   
   # Exit
   \q
   ```

3. **Update Application Connection**
   ```bash
   # Update environment variables or config
   kubectl set env deployment/machine-native-ops \
     POSTGRES_HOST=postgres-replica.production.svc.cluster.local \
     -n production
   
   # Rollout restart
   kubectl rollout restart deployment/machine-native-ops -n production
   ```

4. **Verify Connectivity**
   ```bash
   kubectl exec -it deployment/machine-native-ops -n production -- \
     psql -h postgres-replica.production.svc.cluster.local \
           -U ${POSTGRES_USER} \
           -d ${POSTGRES_DB} \
           -c "SELECT 1;"
   ```

---

### Emergency Restore from Backup

**When to Use:** Data corruption, accidental deletion

**Procedure:**

1. **Stop Application**
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=0 -n production
   ```

2. **Identify Backup**
   ```bash
   velero backup get
   ```

3. **Restore Backup**
   ```bash
   velero restore create emergency-restore \
     --from-backup <backup-name> \
     --include-namespaces production \
     --wait
   ```

4. **Verify Restore**
   ```bash
   kubectl get all -n production
   ```

5. **Start Application**
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=3 -n production
   kubectl rollout status deployment/machine-native-ops -n production
   ```

6. **Verify Application**
   ```bash
   kubectl exec -it deployment/machine-native-ops -n production -- \
     curl http://localhost:8000/health
   ```

---

## Maintenance Windows

### Planned Maintenance

**Frequency:** Monthly or as needed

**Preparation:**

1. **Notify Stakeholders**
   - Send email 7 days before
   - Post in Slack channels
   - Update status page

2. **Create Maintenance Ticket**
   - Document scope and duration
   - Assign owners
   - Set expectations

3. **Pre-Maintenance Checks**
   ```bash
   # Verify backups are current
   velero backup get
   velero backup describe <latest-backup> --details
   
   # Check system health
   kubectl get pods -n production
   kubectl exec -it deployment/machine-native-ops -n production -- \
     curl http://localhost:8000/health
   
   # Document current metrics
   # Take screenshots of Grafana dashboards
   ```

4. **Create Pre-Maintenance Snapshot**
   ```bash
   velero backup create pre-maintenance-$(date +%Y%m%d) \
     --include-namespaces production,istio-system,monitoring \
     --wait
   ```

---

### Maintenance Execution

**Procedure:**

1. **Enable Maintenance Mode**
   ```bash
   # Update Istio virtual service to show maintenance page
   kubectl apply -f - <<EOF
   apiVersion: networking.istio.io/v1alpha3
   kind: VirtualService
   metadata:
     name: machine-native-ops
     namespace: production
   spec:
     http:
     - match:
       - uri:
           prefix: "/"
     route:
     - destination:
         host: maintenance-page.production.svc.cluster.local
     fault:
       abort:
         httpStatus: 503
   EOF
   ```

2. **Stop Application**
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=0 -n production
   ```

3. **Perform Maintenance**
   - Apply updates
   - Fix issues
   - Run tests

4. **Start Application**
   ```bash
   kubectl scale deployment/machine-native-ops --replicas=3 -n production
   kubectl rollout status deployment/machine-native-ops -n production
   ```

5. **Disable Maintenance Mode**
   ```bash
   # Restore original virtual service
   kubectl apply -f k8s/production/virtualservice.yaml
   ```

6. **Post-Maintenance Verification**
   ```bash
   # Check pod status
   kubectl get pods -n production
   
   # Check health
   kubectl exec -it deployment/machine-native-ops -n production -- \
     curl http://localhost:8000/health
   
   # Check metrics
   # Verify error rate < 1%
   # Verify P95 latency < 1s
   
   # Monitor for 30 minutes
   ```

7. **Create Post-Maintenance Backup**
   ```bash
   velero backup create post-maintenance-$(date +%Y%m%d) \
     --include-namespaces production,istio-system,monitoring \
     --wait
   ```

8. **Document Results**
   - Update maintenance ticket
   - Send completion notification
   - Document any issues

---

### Post-Maintenance

**Procedure:**

1. **Review Logs**
   ```bash
   kubectl logs -l app=machine-native-ops -n production --tail=1000
   ```

2. **Compare Metrics**
   - Compare pre-maintenance vs post-maintenance metrics
   - Verify no degradation

3. **Update Documentation**
   - Update runbooks if needed
   - Document lessons learned

4. **Close Ticket**
   - Mark maintenance complete
   - Send summary email

---

## Appendix

### Contact Information

| Role | Email | Slack | Phone |
|------|-------|-------|-------|
| On-Call Engineer | oncall@machinenativeops.com | @oncall | +1-XXX-XXX-XXXX |
| Operations Manager | ops@machinenativeops.com | #operations | +1-XXX-XXX-XXXX |
| Engineering Lead | eng@machinenativeops.com | #engineering | +1-XXX-XXX-XXXX |
| Database Admin | dba@machinenativeops.com | #database | +1-XXX-XXX-XXXX |

### Useful Commands

```bash
# Quick health check
kubectl exec -it deployment/machine-native-ops -n production -- curl http://localhost:8000/health

# Get all pods with restarts
kubectl get pods -n production --sort-by='.status.containerStatuses[0].restartCount'

# Watch pod status
watch kubectl get pods -n production

# Get resource usage
kubectl top pods -n production
kubectl top nodes

# Get recent logs
kubectl logs -l app=machine-native-ops -n production --tail=100 --since=5m

# Check rollout status
kubectl rollout status deployment/machine-native-ops -n production

# Get Istio proxy stats
kubectl exec -it <pod-name> -n production -c istio-proxy -- curl localhost:15000/stats

# List backups
velero backup get

# Describe backup
velero backup describe <backup-name> --details

# Port forward services
kubectl port-forward -n production svc/machine-native-ops 8000:8000
kubectl port-forward -n monitoring svc/prometheus 9090:9090
kubectl port-forward -n monitoring svc/grafana 3000:3000
kubectl port-forward -n istio-system svc/jaeger-query 16686:16686
```

---

**Last Updated:** 2026-01-27
**Version:** 1.0.0
**Maintained By:** Machine Native Ops Team