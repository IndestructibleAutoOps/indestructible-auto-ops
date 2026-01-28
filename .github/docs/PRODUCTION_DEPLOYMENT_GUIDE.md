# GL Unified Charter Activated
# Enterprise Production Deployment Guide

## Overview

This guide provides comprehensive procedures for deploying and managing the Machine Native Ops platform in production using enterprise-grade infrastructure including Istio service mesh, distributed tracing, backup systems, and monitoring.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Infrastructure Overview](#infrastructure-overview)
3. [Deployment Procedures](#deployment-procedures)
4. [Istio Service Mesh](#istio-service-mesh)
5. [Distributed Tracing](#distributed-tracing)
6. [Backup and Recovery](#backup-and-recovery)
7. [Monitoring and Alerting](#monitoring-and-alerting)
8. [Troubleshooting](#troubleshooting)
9. [Runbooks](#runbooks)

---

## Prerequisites

### Required Tools

- **kubectl** v1.28+
- **helm** v3.0+
- **istioctl** v1.19+
- **velero** v1.12+
- **aws cli** v2.0+

### Required Access

- Kubernetes cluster admin access
- AWS IAM permissions for S3
- GitHub container registry access
- SSL/TLS certificates

### Environment Variables

```bash
# AWS Credentials
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"

# Kubernetes Context
export KUBECONFIG="~/.kube/config-production"

# Application Secrets
export POSTGRES_DB="machinenativeops"
export POSTGRES_USER="mno_admin"
export POSTGRES_PASSWORD=$(openssl rand -base64 32)
export SECRET_KEY=$(openssl rand -base64 32)

# Notification Channels
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export PAGERDUTY_SERVICE_KEY="your-pagerduty-key"
export PAGERDUTY_URL="https://events.pagerduty.com/v2/enqueue"
```

---

## Infrastructure Overview

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Load Balancer (ALB)                 │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Istio Ingress Gateway                      │
│         (TLS Termination, Routing, mTLS)               │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│          Machine Native Ops Pods (3 replicas)           │
│    (Istio Sidecar, App Container, Tracing)             │
└──────┬───────────────────────────────────────┬──────────┘
       │                                       │
┌──────▼──────┐                        ┌──────▼──────┐
│   Redis     │                        │ PostgreSQL  │
│   (Cache)   │                        │ (Database)  │
└─────────────┘                        └─────────────┘
                                                     │
┌────────────────────────────────────────────────────▼────────────┐
│                   Monitoring Stack                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │Prometheus│  │ Grafana  │  │ AlertMgr │  │    Jaeger    │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │
└───────────────────────────────────────────────────────────────┘
                                                     │
┌────────────────────────────────────────────────────▼────────────┐
│                   Backup Stack                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                       │
│  │  Velero  │  │S3 Backup │  │ CronJobs │                       │
│  └──────────┘  └──────────┘  └──────────┘                       │
└───────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| Service Mesh | Traffic management, mTLS, observability | Istio |
| API Gateway | External access, routing, security | Istio Gateway |
| Application | Core platform services | Kubernetes Deployments |
| Caching | High-performance cache | Redis |
| Database | Persistent data storage | PostgreSQL |
| Tracing | Distributed tracing | Jaeger |
| Metrics | Monitoring and alerting | Prometheus |
| Visualization | Dashboards and monitoring | Grafana |
| Alerting | Alert routing and notifications | Alertmanager |
| Backup | Disaster recovery | Velero + S3 |

---

## Deployment Procedures

### Initial Deployment

#### Step 1: Create Namespaces

```bash
# Create production namespace
kubectl create namespace production

# Create monitoring namespace
kubectl create namespace monitoring

# Create velero namespace
kubectl create namespace velero
```

#### Step 2: Install Istio

```bash
# Download Istio
curl -L https://istio.io/downloadIstio | sh -
cd istio-*

# Install Istio with production profile
istioctl install --set profile=default -y

# Enable Istio injection on production namespace
kubectl label namespace production istio-injection=enabled
```

#### Step 3: Deploy Application

```bash
# Apply production namespace with RBAC
kubectl apply -f k8s/production/namespace.yaml

# Apply Istio-enabled deployment
kubectl apply -f k8s/production/deployment-istio.yaml

# Apply Istio virtual service and gateway
kubectl apply -f k8s/production/virtualservice.yaml
kubectl apply -f k8s/production/gateway.yaml

# Apply security policies
kubectl apply -f k8s/production/security-policies.yaml
```

#### Step 4: Configure Tracing

```bash
# Apply Jaeger configuration
kubectl apply -f k8s/production/jaeger-config.yaml

# Apply tracing middleware config
kubectl apply -f k8s/production/tracing-middleware-config.yaml
```

#### Step 5: Configure Backup

```bash
# Create S3 bucket
aws s3api create-bucket \
  --bucket machinenativeops-backups \
  --region us-east-1 \
  --create-bucket-configuration LocationConstraint=us-east-1

# Apply Velero configuration
kubectl apply -f k8s/production/velero-config.yaml

# Install Velero
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket machinenativeops-backups \
  --secret-file ~/.aws/credentials \
  --use-volume-snapshots=false \
  --namespace velero
```

#### Step 6: Configure Monitoring

```bash
# Apply Prometheus configuration
kubectl apply -f k8s/production/prometheus-config.yaml

# Apply Grafana dashboards
kubectl apply -f k8s/production/grafana-dashboards.yaml

# Apply Alertmanager configuration
kubectl apply -f k8s/production/alertmanager-config.yaml

# Deploy monitoring stack (if using Helm)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set grafana.adminPassword=$(openssl rand -base64 12)
```

#### Step 7: Verify Deployment

```bash
# Check pod status
kubectl get pods -n production

# Check services
kubectl get svc -n production

# Check Istio components
kubectl get pods -n istio-system

# Test application health
kubectl exec -it deployment/machine-native-ops -n production -- curl http://localhost:8000/health

# Check Istio gateway
kubectl get gateway -n production

# Check virtual services
kubectl get virtualservice -n production
```

### Rolling Update

```bash
# Update deployment with new image
kubectl set image deployment/machine-native-ops \
  app=ghcr.io/machinenativeops/machine-native-ops:v2.0.0 \
  -n production

# Monitor rollout status
kubectl rollout status deployment/machine-native-ops -n production

# Check rollout history
kubectl rollout history deployment/machine-native-ops -n production

# Rollback if needed
kubectl rollout undo deployment/machine-native-ops -n production
```

### Canary Deployment

```bash
# Deploy canary version
kubectl patch deployment machine-native-ops -n production \
  -p '{"spec":{"template":{"metadata":{"labels":{"version":"v2"}}}}}'

# Update virtual service to split traffic
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: machine-native-ops
  namespace: production
spec:
  hosts:
  - "api.machinenativeops.com"
  gateways:
  - machine-native-ops-gateway
  http:
  - route:
    - destination:
        host: machine-native-ops.production.svc.cluster.local
        subset: v1
      weight: 90
    - destination:
        host: machine-native-ops.production.svc.cluster.local
        subset: v2
      weight: 10
EOF

# Monitor canary metrics
# (Check Grafana dashboards)

# Gradually increase canary traffic
# (Update weights: 50/50, then 100% v2)
```

---

## Istio Service Mesh

### Traffic Management

#### Circuit Breaking

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: machine-native-ops
  namespace: production
spec:
  host: machine-native-ops.production.svc.cluster.local
  trafficPolicy:
    circuitBreaker:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

#### Retries

```yaml
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
    retries:
      attempts: 3
      perTryTimeout: 10s
      retryOn: 5xx,connect-failure,refused-stream
```

#### Load Balancing

```yaml
trafficPolicy:
  loadBalancer:
    simple: LEAST_CONN
```

### Security

#### mTLS Enforcement

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: machine-native-ops-mtls
  namespace: production
spec:
  selector:
    matchLabels:
      app: machine-native-ops
  mtls:
    mode: STRICT
```

#### Authorization Policies

```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: machine-native-ops-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: machine-native-ops
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/production/sa/machine-native-ops
```

### Observability

#### View Traffic Metrics

```bash
# Enable Prometheus metrics
kubectl apply -f k8s/istio/metrics.yaml

# Query metrics
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# Open http://localhost:9090

# Common queries:
# - Request rate: sum(rate(istio_requests_total[5m])) by (destination_service)
# - Success rate: sum(rate(istio_requests_total{response_code!~"5.."}[5m])) / sum(rate(istio_requests_total[5m]))
# - Latency: histogram_quantile(0.95, sum(rate(istio_request_duration_milliseconds_bucket[5m])) by (le))
```

---

## Distributed Tracing

### Jaeger Configuration

#### Install Jaeger

```bash
# Install Elasticsearch Operator
kubectl apply -f https://download.elastic.co/downloads/eck/2.9.0/crds.yaml

# Install Elasticsearch
kubectl apply -f k8s/jaeger/elasticsearch.yaml

# Install Jaeger
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm install jaeger jaegertracing/jaeger \
  --namespace istio-system \
  --values k8s/jaeger/values.yaml
```

#### Configure Tracing in Application

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger import JaegerExporter

# Configure tracing
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger-agent.istio-system.svc.cluster.local",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

# Get tracer
tracer = trace.get_tracer(__name__)

# Use in code
with tracer.start_as_current_span("operation_name") as span:
    span.set_attribute("key", "value")
    # Your code here
```

### View Traces

```bash
# Port forward to Jaeger UI
kubectl port-forward -n istio-system svc/jaeger-query 16686:16686

# Open http://localhost:16686

# Search traces by:
# - Service name
# - Operation name
# - Tags
# - Time range

# Analyze trace spans:
# - Check latency per span
# - Identify bottlenecks
# - Verify service dependencies
```

---

## Backup and Recovery

### Backup Configuration

#### Velero Schedules

```yaml
# Daily full cluster backup
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
    ttl: 720h  # 30 days

# Hourly incremental backup
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
    ttl: 168h  # 7 days
```

#### Database Backups

```yaml
# PostgreSQL backup (every 4 hours)
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: production
spec:
  schedule: "0 */4 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: postgres-backup
            image: postgres:15-alpine
            command:
            - /bin/sh
            - -c
            - |
              PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump \
                -h "${POSTGRES_HOST}" \
                -U "${POSTGRES_USER}" \
                -d "${POSTGRES_DB}" \
                --format=custom \
                --compress=9 \
                --file=/backup/postgres-$(date +%Y%m%d-%H%M%S).dump
```

### Backup Verification

```bash
# List backups
velero backup get

# Describe backup
velero backup describe <backup-name> --details

# Check backup status
velero backup get <backup-name> -o jsonpath='{.status.phase}'

# Validate backup
velero backup create test-backup \
  --include-namespaces production \
  --wait

# Test restore
velero restore create test-restore \
  --from-backup test-backup \
  --wait
```

### Restore Procedures

#### Full Cluster Restore

```bash
# List available backups
velero backup get

# Restore from backup
velero restore create prod-restore \
  --from-backup <backup-name> \
  --include-namespaces production,istio-system,monitoring \
  --wait

# Check restore status
velero restore get
velero restore describe prod-restore --details
```

#### Single Namespace Restore

```bash
# Restore only production namespace
velero restore create prod-namespace-restore \
  --from-backup <backup-name> \
  --include-namespaces production \
  --wait
```

#### Database Restore

```bash
# Restore PostgreSQL backup
kubectl exec -it deployment/postgres -n production -- bash
PGPASSWORD="${POSTGRES_PASSWORD}" pg_restore \
  -h "${POSTGRES_HOST}" \
  -U "${POSTGRES_USER}" \
  -d "${POSTGRES_DB}" \
  -v /backup/postgres-20240127-020000.dump

# Exit pod
exit
```

---

## Monitoring and Alerting

### Prometheus Configuration

#### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `http_requests_total` | Total HTTP requests | - |
| `http_request_duration_seconds` | Request latency | P95 > 1s |
| `container_cpu_usage_seconds_total` | CPU usage | > 90% |
| `container_memory_usage_bytes` | Memory usage | > 90% |
| `istio_requests_total` | Istio mesh requests | - |
| `istio_request_duration_milliseconds` | Istio latency | P95 > 1000ms |

#### Alert Rules

```yaml
# High error rate
- alert: HighErrorRate
  expr: |
    rate(http_requests_total{job="machine-native-ops",status=~"5.."}[5m]) /
    rate(http_requests_total{job="machine-native-ops"}[5m]) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "High error rate detected"
    description: "Error rate is {{ $value | humanizePercentage }}"

# High latency
- alert: HighLatency
  expr: |
    histogram_quantile(0.95,
      rate(http_request_duration_seconds_bucket{job="machine-native-ops"}[5m])
    ) > 1
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High latency detected"
    description: "P95 latency is {{ $value }}s"
```

### Grafana Dashboards

#### Access Dashboards

```bash
# Port forward to Grafana
kubectl port-forward -n monitoring svc/grafana 3000:3000

# Open http://localhost:3000
# Default credentials: admin / admin (change on first login)

# Import dashboards:
# - Machine Native Ops - Production (uid: machine-native-ops-prod)
# - Istio Mesh - Production (uid: istio-mesh-prod)
# - Backup Status - Production (uid: backup-status-prod)
```

### Alertmanager Configuration

#### Notification Channels

```yaml
receivers:
- name: 'critical-alerts'
  slack_configs:
  - channel: '#critical-alerts'
    send_resolved: true
  pagerduty_configs:
  - service_key: '${PAGERDUTY_SERVICE_KEY}'

- name: 'machine-native-ops-alerts'
  slack_configs:
  - channel: '#machine-native-ops'
    send_resolved: true
  email_configs:
  - to: 'ops@machinenativeops.com'
```

---

## Troubleshooting

### Common Issues

#### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n production

# Describe pod
kubectl describe pod <pod-name> -n production

# Check pod logs
kubectl logs <pod-name> -n production

# Check events
kubectl get events -n production --sort-by='.lastTimestamp'

# Common causes:
# - Image pull errors (check image name and registry access)
# - Resource limits (increase CPU/memory)
# - Missing secrets/configmaps
# - Node issues (check node status)
```

#### High Error Rates

```bash
# Check error logs
kubectl logs -l app=machine-native-ops -n production --tail=100

# Check Istio metrics
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# Query: rate(http_requests_total{status=~"5.."}[5m])

# Check circuit breaker status
istioctl proxy-config clusters <pod-name> -n production -o json | jq '.[] | select(.name | contains("machine-native-ops")) | .circuitBreakers'

# Check destination rules
kubectl get destinationrule -n production
```

#### Database Connection Issues

```bash
# Check PostgreSQL status
kubectl get pods -n production -l app=postgresql

# Check PostgreSQL logs
kubectl logs -l app=postgresql -n production

# Test connection
kubectl exec -it deployment/machine-native-ops -n production -- \
  psql -h postgresql.production.svc.cluster.local \
        -U ${POSTGRES_USER} \
        -d ${POSTGRES_DB} \
        -c "SELECT 1"

# Check network policies
kubectl get networkpolicy -n production
```

#### Backup Failures

```bash
# Check Velero logs
kubectl logs -n velero deployment/velero

# Check backup status
velero backup get

# Describe failed backup
velero backup describe <backup-name> --details

# Check S3 access
aws s3 ls s3://machinenativeops-backups/velero/

# Test Velero
velero backup create test-backup --wait
```

### Debugging Tools

#### Istio Debug

```bash
# Check Istio proxy configuration
istioctl proxy-config routes <pod-name> -n production
istioctl proxy-config clusters <pod-name> -n production
istioctl proxy-config listeners <pod-name> -n production

# Check Istio proxy logs
kubectl logs <pod-name> -n production -c istio-proxy

# Check mesh status
istioctl analyze

# View envoy config dump
kubectl exec -it <pod-name> -n production -c istio-proxy -- \
  curl localhost:15000/config_dump
```

#### Network Debug

```bash
# Test DNS resolution
kubectl exec -it deployment/machine-native-ops -n production -- \
  nslookup postgresql.production.svc.cluster.local

# Test network connectivity
kubectl exec -it deployment/machine-native-ops -n production -- \
  curl -v http://postgresql.production.svc.cluster.local:5432

# Check network policies
kubectl get networkpolicy -n production -o yaml

# Check service endpoints
kubectl get endpoints -n production
```

---

## Runbooks

### Incident Response

#### High Error Rate Alert

**Severity:** Critical

**Steps:**
1. Acknowledge alert in PagerDuty/Slack
2. Check Grafana dashboard for error patterns
3. Review application logs:
   ```bash
   kubectl logs -l app=machine-native-ops -n production --tail=500
   ```
4. Check recent deployments:
   ```bash
   kubectl rollout history deployment/machine-native-ops -n production
   ```
5. If recent deployment caused issues, rollback:
   ```bash
   kubectl rollout undo deployment/machine-native-ops -n production
   ```
6. Monitor recovery in Grafana
7. Document incident in post-mortem

#### Database Connection Alert

**Severity:** Critical

**Steps:**
1. Check PostgreSQL pod status:
   ```bash
   kubectl get pods -n production -l app=postgresql
   ```
2. Check PostgreSQL logs:
   ```bash
   kubectl logs -l app=postgresql -n production
   ```
3. Check resource usage:
   ```bash
   kubectl top pod -n production -l app=postgresql
   ```
4. Test connection:
   ```bash
   kubectl exec -it deployment/machine-native-ops -n production -- \
     psql -h postgresql.production.svc.cluster.local \
           -U ${POSTGRES_USER} \
           -d ${POSTGRES_DB}
   ```
5. If pod is crashed, restart:
   ```bash
   kubectl rollout restart deployment/postgresql -n production
   ```
6. Monitor recovery

#### Backup Failure Alert

**Severity:** Warning

**Steps:**
1. Check Velero logs:
   ```bash
   kubectl logs -n velero deployment/velero
   ```
2. Check backup status:
   ```bash
   velero backup get
   velero backup describe <failed-backup> --details
   ```
3. Check S3 access:
   ```bash
   aws s3 ls s3://machinenativeops-backups/
   ```
4. If S3 access issue, update credentials:
   ```bash
   kubectl delete secret velero-s3-credentials -n velero
   kubectl create secret generic velero-s3-credentials \
     --namespace velero \
     --from-file=cloud=~/.aws/credentials
   ```
5. Test backup:
   ```bash
   velero backup create test-backup --wait
   ```

### Maintenance Procedures

#### Rolling Restart

```bash
# Restart all pods gracefully
kubectl rollout restart deployment/machine-native-ops -n production

# Monitor rollout
kubectl rollout status deployment/machine-native-ops -n production
```

#### Scale Up/Down

```bash
# Scale up to 5 replicas
kubectl scale deployment/machine-native-ops --replicas=5 -n production

# Scale down to 3 replicas
kubectl scale deployment/machine-native-ops --replicas=3 -n production
```

#### Certificate Rotation

```bash
# Create new TLS certificate
kubectl create secret tls machinenativeops-tls-cert-new \
  --cert=path/to/tls.crt \
  --key=path/to/tls.key \
  -n production

# Update gateway
kubectl patch gateway machine-native-ops-gateway -n production \
  -p '{"spec":{"servers":[{"tls":{"credentialName":"machinenativeops-tls-cert-new"}}]}}'
```

### Disaster Recovery

#### Full Cluster Recovery

```bash
# 1. Restore cluster from Velero backup
velero restore create disaster-recovery \
  --from-backup <latest-backup> \
  --wait

# 2. Verify all resources restored
kubectl get all -n production

# 3. Check application health
kubectl exec -it deployment/machine-native-ops -n production -- \
  curl http://localhost:8000/health

# 4. Verify monitoring stack
kubectl get pods -n monitoring

# 5. Verify backup schedules
velero schedule get
```

---

## Appendix

### Useful Commands

```bash
# Get pod resource usage
kubectl top pods -n production

# Get node resource usage
kubectl top nodes

# Watch pod status
watch kubectl get pods -n production

# Get logs from all pods
kubectl logs -l app=machine-native-ops -n production --all-containers=true

# Port forward to service
kubectl port-forward svc/machine-native-ops 8000:8000 -n production

# Exec into pod
kubectl exec -it <pod-name> -n production -- bash

# Copy files to/from pod
kubectl cp /local/file <pod-name>:/remote/file -n production
kubectl cp <pod-name>:/remote/file /local/file -n production

# Get Istio proxy stats
kubectl exec -it <pod-name> -n production -c istio-proxy -- \
  curl localhost:15000/stats

# Get Istio mesh config
istioctl proxy-config clusters <pod-name> -n production
```

### Contact Information

- **Operations Team:** ops@machinenativeops.com
- **On-Call:** +1-XXX-XXX-XXXX
- **Slack:** #operations, #alerts, #machine-native-ops

### Additional Resources

- [Istio Documentation](https://istio.io/latest/docs/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [Velero Documentation](https://velero.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

---

**Last Updated:** 2026-01-27
**Version:** 1.0.0
**Maintained By:** Machine Native Ops Team