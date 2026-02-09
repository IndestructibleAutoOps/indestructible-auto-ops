# GL Observability Layer Specification

## 8. 可觀測性層（Observability Layer）

### 8.1 Layer Overview

The Observability Layer defines naming conventions for monitoring, logging, tracing, and alerting resources. This layer ensures consistent identification and management of observability artifacts across the platform, enabling effective system monitoring and incident response.

### 8.2 Metric Naming

**Pattern**: `gl.observability.metric`

**Format**: `gl.{domain}.{type}-metric`

**Naming Rules**:
- Must use metric identifier: `-metric`
- Domain identifies metric scope
- Type identifies metric type: `counter|gauge|histogram|summary`

**Examples**:
```yaml
# Valid
gl.runtime.requests-counter-metric
gl.api.latency-gauge-metric
gl.data.processing-histogram-metric

# Invalid
metric
requests-counter
latency-metric
```

**Purpose**: System performance and operational metrics

### 8.3 Log Naming

**Pattern**: `gl.observability.log`

**Format**: `gl.{domain}.{type}-log`

**Naming Rules**:
- Must use log identifier: `-log`
- Domain identifies log scope
- Type identifies log type: `access|error|debug|audit|system`

**Examples**:
```yaml
# Valid
gl.runtime.access-log
gl.api.error-log
gl.data.audit-log

# Invalid
log
access-log
error
```

**Purpose**: System logs for debugging and auditing

### 8.4 Trace Naming

**Pattern**: `gl.observability.trace`

**Format**: `gl.{domain}.{type}-trace`

**Naming Rules**:
- Must use trace identifier: `-trace`
- Domain identifies trace scope
- Type identifies trace type: `request|workflow|transaction`

**Examples**:
```yaml
# Valid
gl.runtime.request-trace
gl.api.workflow-trace
gl.data.transaction-trace

# Invalid
trace
request-trace
workflow
```

**Purpose**: Distributed tracing for request flow analysis

### 8.5 Dashboard Naming

**Pattern**: `gl.observability.dashboard`

**Format**: `gl.{platform}.{scope}-dashboard`

**Naming Rules**:
- Must use dashboard identifier: `-dashboard`
- Platform identifies the platform component
- Scope identifies dashboard scope: `overview|performance|error|resource`

**Examples**:
```yaml
# Valid
gl.runtime.overview-dashboard
gl.api.performance-dashboard
gl.data.error-dashboard

# Invalid
dashboard
overview-dashboard
runtime-dashboard
```

**Purpose**: Visual monitoring dashboards

### 8.6 Alert Naming

**Pattern**: `gl.observability.alert`

**Format**: `gl.{platform}.{severity}-alert`

**Naming Rules**:
- Must use alert identifier: `-alert`
- Platform identifies the platform component
- Severity identifies alert level: `critical|warning|info`

**Examples**:
```yaml
# Valid
gl.runtime.critical-alert
gl.api.warning-alert
gl.data.info-alert

# Invalid
alert
critical-alert
runtime-alert
```

**Purpose**: Alert definitions and notification rules

### 8.7 Rule Naming

**Pattern**: `gl.observability.rule`

**Format**: `gl.{platform}.{type}-rule`

**Naming Rules**:
- Must use rule identifier: `-rule`
- Platform identifies the platform component
- Type identifies rule type: `aggregation|threshold|anomaly`

**Examples**:
```yaml
# Valid
gl.runtime.aggregation-rule
gl.api.threshold-rule
gl.data.anomaly-rule

# Invalid
rule
aggregation-rule
runtime-rule
```

**Purpose**: Alerting and processing rules

### 8.8 Namespace Naming

**Pattern**: `gl.observability.namespace`

**Format**: `gl.{platform}.{environment}-namespace`

**Naming Rules**:
- Must use namespace identifier: `-namespace`
- Platform identifies the platform component
- Environment identifies deployment environment

**Examples**:
```yaml
# Valid
gl.runtime.prod-namespace
gl.api.staging-namespace
gl.data.test-namespace

# Invalid
namespace
prod-namespace
runtime
```

**Purpose**: Logical grouping for observability resources

### 8.9 Collector Naming

**Pattern**: `gl.observability.collector`

**Format**: `gl.{platform}.{type}-collector`

**Naming Rules**:
- Must use collector identifier: `-collector`
- Platform identifies the platform component
- Type identifies collector type: `metrics|logs|traces`

**Examples**:
```yaml
# Valid
gl.runtime.metrics-collector
gl.api.logs-collector
gl.data.traces-collector

# Invalid
collector
metrics-collector
runtime-collector
```

**Purpose**: Data collection and aggregation

### 8.10 Exporter Naming

**Pattern**: `gl.observability.exporter`

**Format**: `gl.{platform}.{type}-exporter`

**Naming Rules**:
- Must use exporter identifier: `-exporter`
- Platform identifies the platform component
- Type identifies exporter type: `prometheus|elasticsearch|opentelemetry`

**Examples**:
```yaml
# Valid
gl.runtime.prometheus-exporter
gl.api.elasticsearch-exporter
gl.data.opentelemetry-exporter

# Invalid
exporter
prometheus-exporter
runtime-exporter
```

**Purpose**: Data export to external systems

### 8.11 Span Naming

**Pattern**: `gl.observability.span`

**Format**: `gl.{domain}.{operation}-span`

**Naming Rules**:
- Must use span identifier: `-span`
- Domain identifies span scope
- Operation identifies span operation

**Examples**:
```yaml
# Valid
gl.runtime.http-request-span
gl.api.database-query-span
gl.data.processing-span

# Invalid
span
http-request-span
operation
```

**Purpose**: Distributed tracing spans

### 8.12 Event Naming

**Pattern**: `gl.observability.event`

**Format**: `gl.{domain}.{type}-event`

**Naming Rules**:
- Must use event identifier: `-event`
- Domain identifies event scope
- Type identifies event type: `business|system|audit`

**Examples**:
```yaml
# Valid
gl.runtime.business-event
gl.api.system-event
gl.data.audit-event

# Invalid
event
business-event
system-event
```

**Purpose**: Event tracking and monitoring

### 8.13 Profile Naming

**Pattern**: `gl.observability.profile`

**Format**: `gl.{platform}.{type}-profile`

**Naming Rules**:
- Must use profile identifier: `-profile`
- Platform identifies the platform component
- Type identifies profile type: `cpu|memory|heap`

**Examples**:
```yaml
# Valid
gl.runtime.cpu-profile
gl.api.memory-profile
gl.data.heap-profile

# Invalid
profile
cpu-profile
runtime-profile
```

**Purpose**: Performance profiling data

### 8.14 Annotation Naming

**Pattern**: `gl.observability.annotation`

**Format**: `gl.{domain}.{type}-annotation`

**Naming Rules**:
- Must use annotation identifier: `-annotation`
- Domain identifies annotation scope
- Type identifies annotation type: `custom|metric|tag`

**Examples**:
```yaml
# Valid
gl.runtime.custom-annotation
gl.api.metric-annotation
gl.data.tag-annotation

# Invalid
annotation
custom-annotation
tag
```

**Purpose**: Metadata annotations for observability

### 8.15 Health Check Naming

**Pattern**: `gl.observability.health-check`

**Format**: `gl.{platform}.{component}-health-check`

**Naming Rules**:
- Must use health check identifier: `-health-check`
- Platform identifies the platform component
- Component identifies checked component

**Examples**:
```yaml
# Valid
gl.runtime.service-health-check
gl.api.database-health-check
gl.data.cache-health-check

# Invalid
health-check
service-health-check
health
```

**Purpose**: System health and availability monitoring

### 8.16 Status Check Naming

**Pattern**: `gl.observability.status-check`

**Format**: `gl.{platform}.{type}-status-check`

**Naming Rules**:
- Must use status check identifier: `-status-check`
- Platform identifies the platform component
- Type identifies check type: `readiness|liveness|startup`

**Examples**:
```yaml
# Valid
gl.runtime.readiness-status-check
gl.api.liveness-status-check
gl.data.startup-status-check

# Invalid
status-check
readiness-check
status
```

**Purpose**: Container and service status monitoring

### 8.17 Probe Naming

**Pattern**: `gl.observability.probe`

**Format**: `gl.{platform}.{type}-probe`

**Naming Rules**:
- Must use probe identifier: `-probe`
- Platform identifies the platform component
- Type identifies probe type: `http|tcp|exec`

**Examples**:
```yaml
# Valid
gl.runtime.http-probe
gl.api.tcp-probe
gl.data.exec-probe

# Invalid
probe
http-probe
tcp
```

**Purpose**: Health probe configurations

### 8.18 Recorder Naming

**Pattern**: `gl.observability.recorder`

**Format**: `gl.{platform}.{type}-recorder`

**Naming Rules**:
- Must use recorder identifier: `-recorder`
- Platform identifies the platform component
- Type identifies recorder type: `video|audio|screenshot`

**Examples**:
```yaml
# Valid
gl.runtime.video-recorder
gl.api.audio-recorder
gl.data.screenshot-recorder

# Invalid
recorder
video-recorder
rec
```

**Purpose**: Session recording and playback

### 8.19 Snapshot Naming

**Pattern**: `gl.observability.snapshot`

**Format**: `gl.{platform}.{type}-snapshot`

**Naming Rules**:
- Must use snapshot identifier: `-snapshot`
- Platform identifies the platform component
- Type identifies snapshot type: `heap|thread|state`

**Examples**:
```yaml
# Valid
gl.runtime.heap-snapshot
gl.api.thread-snapshot
gl.data.state-snapshot

# Invalid
snapshot
heap-snapshot
state
```

**Purpose**: System state captures

### 8.20 Query Naming

**Pattern**: `gl.observability.query`

**Format**: `gl.{domain}.{type}-query`

**Naming Rules**:
- Must use query identifier: `-query`
- Domain identifies query scope
- Type identifies query type: `aggregation|filter|time-series`

**Examples**:
```yaml
# Valid
gl.runtime.aggregation-query
gl.api.filter-query
gl.data.time-series-query

# Invalid
query
aggregation-query
filter
```

**Purpose**: Query definitions for data analysis

### 8.21 Observability Layer Integration

### 8.21.1 Layer Dependencies
- Depends on: Deployment Layer (for monitoring context)
- Provides: Observability data for all layers
- Works with: Security Layer for audit logs

### 8.21.2 Naming Hierarchy
```
gl.observability/
├── metrics/
│   ├── gl.observability.metric
│   └── gl.observability.collector
├── logs/
│   ├── gl.observability.log
│   └── gl.observability.exporter
├── traces/
│   ├── gl.observability.trace
│   └── gl.observability.span
├── dashboards/
│   └── gl.observability.dashboard
├── alerts/
│   ├── gl.observability.alert
│   └── gl.observability.rule
├── monitoring/
│   ├── gl.observability.health-check
│   ├── gl.observability.status-check
│   └── gl.observability.probe
└── analysis/
    ├── gl.observability.profile
    ├── gl.observability.snapshot
    └── gl.observability.query
```

### 8.21.3 Cross-Layer Integration
- **Observability → Platform**: Platform component monitoring
- **Observability → Deployment**: K8s resource monitoring
- **Observability → Security**: Security event logging
- **Observability → Data**: Data pipeline monitoring

## 8.22 Best Practices

### 8.22.1 Golden Signals Monitoring
```yaml
# Four golden signals
gl.observability.latency-metric
gl.observability.traffic-metric
gl.observability.errors-metric
gl.observability.saturation-metric
```

### 8.22.2 Distributed Tracing
```yaml
# End-to-end request tracing
gl.observability.request-trace
  ├── gl.observability.http-request-span
  ├── gl.observability.database-query-span
  └── gl.observability.processing-span
```

### 8.22.3 Structured Logging
```yaml
# Standardized log formats
gl.runtime.access-log
gl.api.error-log
gl.data.audit-log
gl.runtime.debug-log
```

### 8.22.4 Alert Hierarchy
```yaml
# Alert severity levels
gl.runtime.critical-alert
gl.api.warning-alert
gl.data.info-alert
```

## 8.23 Validation Rules

### Rule OL-001: Metric Type Validation
- **Severity**: CRITICAL
- **Check**: Metrics must specify type (counter/gauge/histogram/summary)
- **Pattern**: `^gl\..+\.counter|gauge|histogram|summary-metric$`

### Rule OL-002: Log Retention Policy
- **Severity**: MEDIUM
- **Check**: Logs must have retention period defined
- **Required**: Retention days and storage requirements

### Rule OL-003: Trace Span Limits
- **Severity**: MEDIUM
- **Check**: Trace spans must have reasonable limits
- **Required**: Max span count and timeout

### Rule OL-004: Alert Escalation Rules
- **Severity**: HIGH
- **Check**: Alerts must have escalation policies defined
- **Required**: Escalation path and notification channels

### Rule OL-005: Dashboard Refresh Rate
- **Severity**: LOW
- **Check**: Dashboards must have appropriate refresh rates
- **Recommended**: 1-60 seconds based on use case

## 8.24 Usage Examples

### Example 1: Complete Observability Stack
```yaml
# Metrics
apiVersion: metrics.gl.io/v1
kind: Metric
metadata:
  name: gl.runtime.requests-counter-metric
spec:
  type: counter
  help: Total number of requests
  labels:
  - method
  - path
  - status
---
apiVersion: metrics.gl.io/v1
kind: Collector
metadata:
  name: gl.runtime.metrics-collector
spec:
  type: metrics
  interval: 15s
  exporters:
  - gl.runtime.prometheus-exporter
---
# Logs
apiVersion: logging.gl.io/v1
kind: Log
metadata:
  name: gl.runtime.access-log
spec:
  type: access
  format: json
  retention: 30d
  fields:
  - timestamp
  - method
  - path
  - status
  - latency
---
apiVersion: logging.gl.io/v1
kind: Exporter
metadata:
  name: gl.runtime.elasticsearch-exporter
spec:
  type: elasticsearch
  endpoint: http://elasticsearch:9200
---
# Traces
apiVersion: tracing.gl.io/v1
kind: Trace
metadata:
  name: gl.runtime.request-trace
spec:
  type: request
  samplingRate: 0.1
  spans:
  - gl.runtime.http-request-span
  - gl.runtime.database-query-span
---
apiVersion: tracing.gl.io/v1
kind: Span
metadata:
  name: gl.runtime.http-request-span
spec:
  kind: server
  operation: GET
  attributes:
    http.method: GET
    http.url: /api/v1/data
---
# Dashboard
apiVersion: dashboard.gl.io/v1
kind: Dashboard
metadata:
  name: gl.runtime.overview-dashboard
spec:
  title: Platform Overview
  panels:
  - title: Request Rate
    metrics:
    - gl.runtime.requests-counter-metric
  - title: Error Rate
    metrics:
    - gl.runtime.errors-counter-metric
---
# Alerts
apiVersion: alerting.gl.io/v1
kind: Alert
metadata:
  name: gl.runtime.critical-alert
spec:
  severity: critical
  rules:
  - gl.runtime.threshold-rule
  notifications:
  - slack: #alerts
  - email: ops-team@example.com
```

### Example 2: Health Monitoring
```yaml
# Health Check
apiVersion: monitoring.gl.io/v1
kind: HealthCheck
metadata:
  name: gl.runtime.service-health-check
spec:
  interval: 30s
  timeout: 5s
  checks:
  - gl.runtime.http-probe
  - gl.runtime.tcp-probe
---
# Status Check
apiVersion: monitoring.gl.io/v1
kind: StatusCheck
metadata:
  name: gl.runtime.readiness-status-check
spec:
  type: readiness
  initialDelaySeconds: 5
  periodSeconds: 10
---
# Probe
apiVersion: monitoring.gl.io/v1
kind: Probe
metadata:
  name: gl.runtime.http-probe
spec:
  type: http
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```

### Example 3: Performance Analysis
```yaml
# Profile
apiVersion: analysis.gl.io/v1
kind: Profile
metadata:
  name: gl.runtime.cpu-profile
spec:
  type: cpu
  duration: 30s
  interval: 100ms
---
# Snapshot
apiVersion: analysis.gl.io/v1
kind: Snapshot
metadata:
  name: gl.runtime.heap-snapshot
spec:
  type: heap
  format: json
---
# Query
apiVersion: analysis.gl.io/v1
kind: Query
metadata:
  name: gl.runtime.aggregation-query
spec:
  type: aggregation
  query: |
    sum(rate(gl_runtime_requests_total[5m])) by (path)
```

### Example 4: Distributed Tracing
```yaml
# Trace
apiVersion: tracing.gl.io/v1
kind: Trace
metadata:
  name: gl.api.workflow-trace
spec:
  type: workflow
  samplingRate: 1.0
  tags:
  - workflow_id
  - user_id
---
# Spans
apiVersion: tracing.gl.io/v1
kind: Span
metadata:
  name: gl.api.http-request-span
spec:
  kind: client
  operation: POST
  parent: gl.api.workflow-trace
  attributes:
    http.method: POST
    http.url: /api/v1/workflow
---
apiVersion: tracing.gl.io/v1
kind: Span
metadata:
  name: gl.api.database-query-span
spec:
  kind: server
  operation: SELECT
  parent: gl.api.http-request-span
  attributes:
    db.statement: SELECT * FROM users
    db.system: postgresql
```

## 8.25 Compliance Checklist

- [x] Metric naming follows `gl.{domain}.{type}-metric` pattern
- [x] Log naming includes `-log` identifier
- [x] Trace naming includes `-trace` identifier
- [x] Dashboard naming includes `-dashboard` identifier
- [x] Alert naming includes `-alert` identifier with severity
- [x] Rule naming includes `-rule` identifier
- [x] Collector naming includes `-collector` identifier
- [x] Exporter naming includes `-exporter` identifier
- [x] Span naming includes `-span` identifier
- [x] Event naming includes `-event` identifier
- [x] Profile naming includes `-profile` identifier
- [x] Health check naming includes `-health-check` identifier
- [x] Status check naming includes `-status-check` identifier
- [x] Probe naming includes `-probe` identifier
- [x] Recorder naming includes `-recorder` identifier
- [x] Snapshot naming includes `-snapshot` identifier
- [x] Query naming includes `-query` identifier
- [x] All metrics follow golden signals
- [x] Trace spans have reasonable limits
- [x] Alerts have escalation policies

## 8.26 Tool Integration

### 8.26.1 Prometheus Monitoring
```yaml
# Prometheus configuration
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
- job_name: 'gov-runtime'
  static_configs:
  - targets: ['gl.runtime:8080']
  metrics_path: /metrics
```

### 8.26.2 Grafana Dashboards
```json
{
  "title": "gl.runtime.overview-dashboard",
  "panels": [
    {
      "title": "Request Rate",
      "targets": [
        {
          "expr": "rate(gl_runtime_requests_total[5m])"
        }
      ]
    }
  ]
}
```

### 8.26.3 Jaeger Tracing
```yaml
# Jaeger collector configuration
collector:
  zipkin:
    host-port: 0.0.0.0:9411

storage:
  elasticsearch:
    servers: gl.runtime.elasticsearch:9200
```

### 8.26.4 Pre-commit Hooks
```bash
#!/bin/bash
# Validate observability naming conventions
for file in $(git diff --name-only --cached | grep -E '\.(yaml|yml)$'); do
  # Check metric naming
  if grep -E "kind: Metric" "$file" | grep -vE "name: gl\..+-.+metric"; then
    echo "ERROR: Invalid metric naming in $file"
    exit 1
  fi
  
  # Check alert naming
  if grep -E "kind: Alert" "$file" | grep -vE "name: gl\..+-.+alert"; then
    echo "ERROR: Invalid alert naming in $file"
    exit 1
  fi
done
```

### 8.26.5 Log Analysis
```bash
# Query logs
grep "ERROR" gl.runtime.access-log | wc -l

# Analyze metrics
curl -s http://gl.runtime:9090/api/v1/query?query=gl_runtime_requests_total

# Trace analysis
curl -s http://jaeger:16686/api/traces | jq '.data[]'
```

## 8.27 References

- Observability Best Practices: https://sre.google/sre-book/monitoring-distributed-systems/
- Prometheus Documentation: https://prometheus.io/docs/
- Grafana Dashboards: https://grafana.com/docs/
- OpenTelemetry: https://opentelemetry.io/
- Naming Convention Principles: gov-prefix-principles-engineering.md
- Deployment Layer: gov-deployment-layer-specification.md