# NG Governance System - Monitoring Setup Guide

Complete guide for setting up and deploying the monitoring infrastructure for the NG Governance System.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Detailed Setup](#detailed-setup)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- Docker 20.10+
- Docker Compose 2.0+
- At least 4GB RAM available
- 20GB free disk space

### Optional Software
- Git (for cloning the repository)
- kubectl (for Kubernetes deployment)

### System Requirements
- **CPU:** 2 cores minimum, 4 cores recommended
- **RAM:** 4GB minimum, 8GB recommended
- **Disk:** 20GB minimum for 30-day data retention
- **Network:** Ports 3000 (Grafana) and 9090 (Prometheus) must be available

---

## Quick Start

### 1. Clone and Navigate

```bash
cd /path/to/machine-native-ops/monitoring
```

### 2. Start Monitoring Stack

```bash
docker-compose up -d
```

### 3. Access Dashboards

- **Grafana:** http://localhost:3000
  - Username: `admin`
  - Password: `admin`
- **Prometheus:** http://localhost:9090

### 4. Verify Services

```bash
docker-compose ps
```

Expected output:
```
NAME                COMMAND                  SERVICE             STATUS
grafana             "/run.sh"                grafana             running (healthy)
node-exporter       "/bin/node_exporter"     node-exporter       running
prometheus          "/bin/prometheus"        prometheus          running
```

---

## Detailed Setup

### Step 1: Configure Prometheus

Edit `monitoring/prometheus.yml` to configure scrape targets:

```yaml
scrape_configs:
  # NG Semantic Binding Service
  - job_name: 'ng-semantic-binding'
    static_configs:
      - targets: ['ng-semantic-binding:8080']
        labels:
          service: 'ng-semantic-binding'
    metrics_path: '/metrics'
    scrape_interval: 15s
```

### Step 2: Configure Grafana Datasource

Edit `monitoring/grafana/provisioning/datasources.yaml`:

```yaml
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

### Step 3: Configure Alert Rules

Edit `monitoring/alert-rules.yml` to define alert conditions:

```yaml
groups:
  - name: ng_governance_alerts
    interval: 30s
    rules:
      - alert: HighSemanticBindingFailureRate
        expr: ng:semantic_binding:success_rate:5m < 0.95
        for: 5m
```

### Step 4: Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service health
docker-compose ps
```

### Step 5: Initialize Grafana

1. Open http://localhost:3000
2. Login with `admin/admin`
3. Change password on first login
4. Navigate to Dashboards → NG Governance folder
5. Verify dashboards are loading

---

## Configuration

### Prometheus Configuration

#### Data Retention

Edit `monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 30s
  evaluation_interval: 30s
  # Add retention settings
  # storage.tsdb.retention.time: 30d
```

#### Custom Scrape Jobs

Add new scrape jobs to `scrape_configs`:

```yaml
- job_name: 'custom-service'
  static_configs:
    - targets: ['custom-service:8080']
        labels:
          environment: 'production'
```

### Grafana Configuration

#### Authentication

Edit `docker-compose.yml`:

```yaml
environment:
  - GF_SECURITY_ADMIN_USER=admin
  - GF_SECURITY_ADMIN_PASSWORD=your_secure_password
```

#### Dashboard Auto-Provisioning

Dashboards are automatically provisioned from:
- `monitoring/grafana/dashboards/` directory
- Configuration: `monitoring/grafana/provisioning/dashboards.yaml`

Update interval: 10 seconds

### Alerting Configuration

#### Enable Alertmanager (Optional)

Create `alertmanager.yml`:

```yaml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'

receivers:
  - name: 'web.hook'
    webhook_configs:
      - url: 'http://your-webhook-url'
```

Add to Prometheus configuration:

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

---

## Verification

### 1. Verify Prometheus

```bash
# Check Prometheus is running
curl http://localhost:9090/-/healthy

# Check metrics are being scraped
curl http://localhost:9090/api/v1/targets

# Query specific metric
curl 'http://localhost:9090/api/v1/query?query=up'
```

### 2. Verify Grafana

```bash
# Check Grafana is running
curl http://localhost:3000/api/health

# Check datasource connection
curl http://localhost:3000/api/datasources
```

### 3. Verify Dashboard Data

In Grafana UI:
1. Open NG Governance System Dashboard
2. Check each panel shows data
3. Verify time range includes recent data
4. Check query inspector for errors

### 4. Verify Alert Rules

```bash
# Check alert rules are loaded
curl http://localhost:9090/api/v1/rules

# Check active alerts
curl http://localhost:9090/api/v1/alerts
```

---

## Troubleshooting

### Grafana Issues

#### Dashboards Not Loading

**Symptoms:** Dashboards show "No Data"

**Solutions:**
1. Check Prometheus is receiving metrics:
   ```bash
   curl http://localhost:9090/api/v1/label/__name__/values
   ```

2. Verify datasource connection in Grafana:
   - Configuration → Data Sources → Prometheus → Test

3. Check dashboard JSON syntax:
   ```bash
   cat monitoring/grafana/dashboards/*.json | jq .
   ```

4. Review Grafana logs:
   ```bash
   docker logs grafana
   ```

#### Authentication Issues

**Symptoms:** Cannot login to Grafana

**Solutions:**
1. Reset admin password:
   ```bash
   docker exec -it grafana grafana-cli admin reset-admin-password newpassword
   ```

2. Check environment variables in docker-compose.yml

3. Restart Grafana:
   ```bash
   docker-compose restart grafana
   ```

### Prometheus Issues

#### No Metrics Collected

**Symptoms:** Prometheus shows "0/0 up" for targets

**Solutions:**
1. Check target services are running:
   ```bash
   docker ps | grep ng-semantic-binding
   ```

2. Verify network connectivity:
   ```bash
   docker exec prometheus ping ng-semantic-binding
   ```

3. Check Prometheus configuration:
   ```bash
   docker exec prometheus promtool check config /etc/prometheus/prometheus.yml
   ```

4. Review Prometheus logs:
   ```bash
   docker logs prometheus
   ```

#### High Memory Usage

**Symptoms:** Prometheus consuming too much RAM

**Solutions:**
1. Reduce data retention:
   ```yaml
   global:
     storage.tsdb.retention.time: 7d
   ```

2. Reduce scrape interval:
   ```yaml
   global:
     scrape_interval: 60s
   ```

3. Add resource limits in docker-compose.yml:
   ```yaml
   prometheus:
     deploy:
       resources:
         limits:
           memory: 2G
   ```

### Network Issues

#### Services Cannot Communicate

**Symptoms:** "Connection refused" errors

**Solutions:**
1. Verify all services are on the same network:
   ```bash
   docker network inspect monitoring
   ```

2. Check service names in configuration match container names

3. Verify ports are not in use:
   ```bash
   netstat -tulpn | grep -E '3000|9090'
   ```

### Performance Issues

#### Slow Dashboard Load Times

**Symptoms:** Dashboards take long to load

**Solutions:**
1. Reduce dashboard refresh rate in UI
2. Shorten time range
3. Simplify queries
4. Add data retention to reduce query time

#### High CPU Usage

**Symptoms:** System sluggish, high CPU

**Solutions:**
1. Reduce scrape interval
2. Reduce number of metrics scraped
3. Add sampling to queries
4. Increase hardware resources

---

## Advanced Configuration

### Kubernetes Deployment

For Kubernetes deployments, use Helm charts:

```bash
# Add Prometheus Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack

# Install Grafana dashboards
kubectl apply -f k8s/grafana-dashboards/
```

### Custom Metrics Exporters

Create custom Prometheus exporter:

```python
from prometheus_client import start_http_server, Gauge
import time

# Define metrics
semantic_binding_success = Gauge('ng_semantic_binding_success', 'Semantic binding success rate')

# Expose metrics
start_http_server(8080)

# Update metrics
while True:
    semantic_binding_success.set(0.95)
    time.sleep(30)
```

### Backup and Restore

#### Backup Configuration

```bash
# Backup Prometheus data
docker exec prometheus tar -czf /tmp/prometheus-backup.tar.gz /prometheus
docker cp prometheus:/tmp/prometheus-backup.tar.gz ./backups/

# Backup Grafana data
docker exec grafana tar -czf /tmp/grafana-backup.tar.gz /var/lib/grafana
docker cp grafana:/tmp/grafana-backup.tar.gz ./backups/
```

#### Restore Configuration

```bash
# Restore Prometheus data
docker cp ./backups/prometheus-backup.tar.gz prometheus:/tmp/
docker exec prometheus tar -xzf /tmp/prometheus-backup.tar.gz -C /

# Restore Grafana data
docker cp ./backups/grafana-backup.tar.gz grafana:/tmp/
docker exec grafana tar -xzf /tmp/grafana-backup.tar.gz -C /
```

---

## Monitoring Best Practices

1. **Set Up Alerts Early:** Configure alert rules before deployment
2. **Test Queries:** Verify Prometheus queries in the UI before adding to dashboards
3. **Monitor the Monitor:** Set up alerts for monitoring system itself
4. **Document Custom Metrics:** Keep a registry of custom metrics and their meanings
5. **Regular Backups:** Schedule regular backups of configuration and data
6. **Review Retention:** Adjust data retention based on storage capacity
7. **Test Failover:** Regularly test alerting and failover procedures

---

## Additional Resources

- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Prometheus Query Examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)

---

## Support

For issues or questions:
1. Check this guide first
2. Review logs: `docker-compose logs`
3. Check service status: `docker-compose ps`
4. Consult official documentation
5. Open an issue in the project repository

---

**Last Updated:** 2025-02-06  
**Version:** 1.0  
**Maintained by:** NG Governance Team