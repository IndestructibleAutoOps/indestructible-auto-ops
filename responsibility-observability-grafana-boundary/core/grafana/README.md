# Grafana Monitoring for NG Governance System

This directory contains Grafana dashboards and provisioning configuration for monitoring the NG Governance System.

## 📊 Dashboard Overview

### 1. NG Governance System Dashboard (`ng-governance-dashboard.json`)
**Purpose:** High-level overview of the entire NG governance system

**Panels:**
- **NG Semantic Binding Success Rate** - Tracks the success rate of semantic binding operations
- **Parametric Convergence Lipschitz Constant** - Real-time gauge showing convergence stability
- **Fallback Validation Success Rate** - Monitors fallback decision validation success
- **Embedding Space Consistency** - Tracks consistency of the embedding space over time
- **Service Status** (3 panels) - Health status for:
  - NG Semantic Binding Service
  - Parametric Convergence Service
  - Fallback Validator Service
- **Error Rate by Component** - Stacked bar chart of errors by component
- **Parameter Change Magnitude** - Tracks parameter changes in the convergence system

**Time Range:** Last 1 hour  
**Refresh Rate:** 30 seconds

---

### 2. Parametric Convergence Monitoring (`parametric-convergence-dashboard.json`)
**Purpose:** Deep dive into parametric convergence metrics

**Panels:**
- **Lipschitz Constant** - Gauge showing current Lipschitz constant (L < 1.0 = convergent)
- **Predicted Convergence Time** - Estimated iterations to convergence
- **Parameter Change Magnitude** - Time series of parameter updates
- **Loss Function Over Time** - Optimization loss trajectory
- **Gradient Norm Over Time** - Gradient magnitude tracking
- **Adaptive Learning Rate** - Learning rate adjustments over time

**Time Range:** Last 6 hours  
**Refresh Rate:** 30 seconds

---

### 3. Fallback Validation Monitoring (`fallback-validation-dashboard.json`)
**Purpose:** Monitor fallback decision validation system

**Panels:**
- **Fallback Validation Success Rate** - Overall validation success rate
- **Cross-Mode Agreement (Cohen's Kappa)** - Agreement metric between validation modes
- **Fallback Validations by Level** - Breakdown of validations by fallback level
- **Validation Failures by Reason** - Categorized failure reasons
- **Fallback Decision Validation Scores** - Time series of:
  - Intent Similarity Score
  - Safety Constraint Score
  - Semantic Anchor Score

**Time Range:** Last 6 hours  
**Refresh Rate:** 30 seconds

---

## 🚀 Deployment

### Prerequisites
- Docker and Docker Compose
- Prometheus server running
- Sufficient resources (CPU: 2 cores, RAM: 4GB recommended)

### Quick Start with Docker Compose

```bash
# Create docker-compose.yml in monitoring directory
docker-compose up -d grafana prometheus
```

### Manual Deployment

1. **Build Grafana image with dashboards:**
```bash
docker build -t grafana-ng-governance -f Dockerfile .
```

2. **Run Grafana container:**
```bash
docker run -d \
  --name grafana \
  -p 3000:3000 \
  -v $(pwd)/provisioning:/etc/grafana/provisioning \
  -v $(pwd)/dashboards:/etc/grafana/provisioning/dashboards \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  -e GF_INSTALL_PLUGINS= \
  grafana-ng-governance
```

3. **Access Grafana:**
```
URL: http://localhost:3000
Username: admin
Password: admin (change on first login)
```

---

## 📈 Prometheus Metrics Reference

### NG Semantic Binding Metrics

| Metric Name | Type | Description |
|------------|------|-------------|
| `ng:semantic_binding:success_rate:5m` | Gauge | 5-minute success rate |
| `ng:embedding_space:consistency:5m` | Gauge | Embedding space consistency |
| `ng_semantic_binding_errors_total` | Counter | Total binding errors |

### Parametric Convergence Metrics

| Metric Name | Type | Description |
|------------|------|-------------|
| `parametric_convergence_lipschitz_constant` | Gauge | Current Lipschitz constant |
| `parametric:convergence:time:prediction` | Gauge | Predicted convergence iterations |
| `parametric_parameter_change` | Gauge | Parameter change magnitude |
| `parametric_loss` | Gauge | Current loss value |
| `parametric_gradient_norm` | Gauge | Gradient norm |
| `parametric_learning_rate` | Gauge | Current learning rate |

### Fallback Validation Metrics

| Metric Name | Type | Description |
|------------|------|-------------|
| `fallback:validation:success_rate:5m` | Gauge | 5-minute success rate |
| `fallback_cross_mode_agreement_kappa` | Gauge | Cohen's Kappa score |
| `fallback_validation_by_level` | Counter | Validations by level |
| `fallback_validation_failures_by_reason` | Counter | Failures by reason |
| `fallback_intent_similarity_score` | Gauge | Intent similarity |
| `fallback_safety_constraint_score` | Gauge | Safety constraint score |
| `fallback_semantic_anchor_score` | Gauge | Semantic anchor score |

---

## 🎯 Alerting Rules

Critical alerts should be configured in Prometheus:

```yaml
# Example alert rules
groups:
  - name: ng_governance_alerts
    interval: 30s
    rules:
      - alert: HighSemanticBindingFailureRate
        expr: ng:semantic_binding:success_rate:5m < 0.95
        for: 5m
        annotations:
          summary: "High semantic binding failure rate"

      - alert: NonConvergentSystem
        expr: parametric_convergence_lipschitz_constant >= 1.0
        for: 2m
        annotations:
          summary: "System not convergent"

      - alert: LowFallbackValidationSuccess
        expr: fallback:validation:success_rate:5m < 0.9
        for: 5m
        annotations:
          summary: "Low fallback validation success rate"
```

---

## 🔧 Configuration

### Datasource Configuration

Edit `provisioning/datasources.yaml` to configure Prometheus connection:

```yaml
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090  # Adjust URL as needed
    isDefault: true
    editable: true
    jsonData:
      timeInterval: 30s
```

### Dashboard Provisioning

Edit `provisioning/dashboards.yaml` to configure dashboard provider:

```yaml
providers:
  - name: 'NG Governance Dashboards'
    orgId: 1
    folder: 'NG Governance'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
```

---

## 📝 Dashboard Customization

### Adding Custom Panels

1. Export dashboard JSON from Grafana UI
2. Modify panel configuration
3. Update JSON file in `dashboards/` directory
4. Restart Grafana or wait for automatic reload (10 seconds)

### Creating New Dashboards

1. Create new JSON file in `dashboards/` directory
2. Follow the structure of existing dashboards
3. Add to `provisioning/dashboards.yaml` if needed
4. Restart Grafana

---

## 🔍 Troubleshooting

### Dashboards Not Loading

1. Check Grafana logs:
```bash
docker logs grafana
```

2. Verify datasource connection:
```bash
curl http://prometheus:9090/api/v1/query?query=up
```

3. Check provisioning configuration:
```bash
cat /etc/grafana/provisioning/datasources/datasources.yaml
```

### No Data in Panels

1. Verify Prometheus is receiving metrics:
```bash
curl http://localhost:9090/api/v1/label/__name__/values
```

2. Check metric names match dashboards
3. Verify time range includes data
4. Check query syntax in Grafana query inspector

### Performance Issues

1. Reduce refresh rate in dashboard settings
2. Reduce time range
3. Simplify queries
4. Add data retention to Prometheus

---

## 📚 Additional Resources

- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [NG Governance System Documentation](../../README.md)
- [Alerting Configuration](../alert-rules.yml)

---

## 🤝 Contributing

When modifying dashboards:

1. Test changes in development environment first
2. Validate JSON syntax
3. Document custom metrics or panels
4. Update this README with new panels or metrics
5. Test with sample data before deployment

---

## 📄 License

Same as the main NG Governance System project.

---

**Last Updated:** 2025-02-06  
**Version:** 1.0  
**Maintained by:** NG Governance Team