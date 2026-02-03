# Cloud Platform Instance Layer

## 🧱 Module Purpose

platform-cloud defines **how platforms use cloud** and **how platforms are deployed on cloud**.

It is responsible for:
- Platform deployment strategies (per environment / per instance)
- Platform topology and configuration on cloud
- How platforms consume ecosystem-cloud contracts
- Platform instance settings (dev/stage/prod/customer)

platform-cloud **does not define cloud provider capabilities** - that's ecosystem-cloud's responsibility.

---

## 🧩 Semantic Anchor

**CLOUDPLATFORMINSTANCE** - Defines how platforms use cloud infrastructure

---

## 🎯 Key Responsibilities

### 1. Platform Deployment Strategies

Each platform instance has its own:
- Configuration
- Cloud provider
- Region
- Quotas and feature flags

### 2. Platform Topology on Cloud

Defines:
- VPC architecture
- Subnet layout
- Load balancers
- Database clusters
- Message queues
- CDN endpoints

### 3. Platform Configuration

Each instance has:
- environment.yaml (environment-specific settings)
- platform.yaml (platform-specific settings)
- deployment.yaml (deployment configuration)
- services.yaml (service definitions)

### 4. Contract Consumption

platform-cloud uses ecosystem-cloud contracts by:
- Specifying cloud provider (AWS/Azure/GCP)
- Selecting appropriate adapters
- Defining resource requirements
- Setting up networking and security

---

## 🏗 Directory Structure

```
platform-cloud/
├── dev/                   # Development environment
│   ├── environment.yaml
│   ├── platform.yaml
│   ├── deployment.yaml
│   ├── services.yaml
│   └── networking.yaml
├── staging/               # Staging environment
│   └── [same structure as dev]
├── prod/                  # Production environment
│   └── [same structure as dev]
├── customer-a/            # Customer A specific platform instance
│   └── [same structure as dev]
├── customer-b/            # Customer B specific platform instance
│   └── [same structure as dev]
├── customer-c/            # Customer C specific platform instance
│   └── [same structure as dev]
└── templates/
    ├── base/
    ├── dev/
    ├── staging/
    ├── prod/
    └── customer/
```

---

## 📋 Configuration Files

### environment.yaml
```yaml
platform:
  name: platform-instance-name
  instance_type: dev/staging/prod/customer
  owner: team@company.com
  cost_center: cc-12345

cloud:
  provider: aws
  region: us-east-1
  account_id: 123456789012

ecosystem_cloud:
  storage_adapter: aws
  compute_adapter: aws
  queue_adapter: aws
  secrets_adapter: aws
  logging_adapter: aws

networking:
  vpc_cidr: 10.0.0.0/16
  subnet_cidr_bits: 8
  availability_zones: [us-east-1a, us-east-1b]

monitoring:
  enabled: true
  metrics_collection: true
  alerting: true
  dashboard: cloudwatch-ops-dashboard

limits:
  max_instances: 10
  max_storage_gb: 1000
  max_databases: 5
```

### platform.yaml
```yaml
services:
  api_gateway:
    enabled: true
    instance_type: t3.medium
    min_instances: 2
    max_instances: 10
    target_cpu_percent: 70
  
  data_processing:
    enabled: true
    instance_type: t3.large
    min_instances: 1
    max_instances: 5
    target_cpu_percent: 80
  
  observability:
    enabled: true
    instance_type: t3.small
    min_instances: 1
    max_instances: 3
    target_cpu_percent: 60
```

### deployment.yaml
```yaml
deployment:
  strategy: blue_green
  health_check_path: /health
  health_check_interval_seconds: 30
  health_check_timeout_seconds: 10
  
  rollback:
    enabled: true
    on_health_check_failure: true
    on_deployment_failure: true
  
  notifications:
    slack:
      enabled: true
      webhook_url: ${SLACK_WEBHOOK_URL}
    email:
      enabled: true
      recipients: team@company.com
```

---

## 🔧 Platform Creation

To create a new platform instance:

```bash
# Create directory structure
cp -r platform-cloud/templates/dev platform-cloud/new-platform

# Customize configuration
vim platform-cloud/new-platform/environment.yaml
vim platform-cloud/new-platform/platform.yaml
vim platform-cloud/new-platform/deployment.yaml

# Validate configuration
python ecosystem/tools/validate_platform.py platform-cloud/new-platform

# Deploy platform
python ecosystem/tools/deploy_platform.py platform-cloud/new-platform
```

---

## 🎯 Governance

All platform instances must:

1. **Pass validation** - Configuration must be valid
2. **Comply with contracts** - Use only valid adapters
3. **Follow naming conventions** - Follow GL naming ontology
4. **Include documentation** - README.md in each platform instance
5. **Use templates** - Start from templates, don't create from scratch

---

## 📊 Platform Instance Status

| Platform | Status | Provider | Region | Last Deployed |
|----------|--------|----------|--------|---------------|
| dev | ACTIVE | AWS | us-east-1 | 2024-02-02 |
| staging | ACTIVE | AWS | us-east-1 | 2024-02-01 |
| prod | ACTIVE | AWS | us-east-1 | 2024-01-30 |
| customer-a | ACTIVE | AWS | us-west-2 | 2024-01-28 |
| customer-b | PENDING | Azure | eastus | N/A |
| customer-c | PENDING | GCP | us-central1 | N/A |

---

## 🔗 Relationships

### ecosystem-cloud → platform-cloud
ecosystem-cloud provides:
- Cloud provider contracts (storage, compute, queue, secrets, logging)
- Cloud adapters (AWS, Azure, GCP, on-premise)
- Platform templates for cloud resources

platform-cloud consumes:
- Cloud provider contracts for service definitions
- Cloud adapters for actual resource provisioning
- Platform templates for common infrastructure

### Separate Evolutions
- **ecosystem-cloud evolution**: Update contracts → Update adapters → Test → Deploy
- **platform-cloud evolution**: Update templates → Update configs → Test → Deploy

Two evolution paths **do not interfere** with each other.

---

## 🚨 Forbidden

platform-cloud **CANNOT** contain:

- ❌ Cloud provider contracts (that's ecosystem-cloud)
- ❌ Cloud provider adapters (that's ecosystem-cloud)
- ❌ Cloud provider SDKs (use ecosystem-cloud adapters instead)
- ❌ Business logic (belongs to services)
- ❌ Non-cloud-specific contracts (use core contracts/)

---

## ✅ Allowed

platform-cloud **CAN** contain:

- ✅ Platform deployment strategies
- ✅ Platform topology definitions
- ✅ Platform instance configurations
- ✅ Platform-specific settings
- ✅ Platform deployment scripts

---

## 🎯 Final Statement

> ecosystem-cloud defines cloud provider capabilities; platform-cloud defines how platforms use cloud.  
> Both must be side-by-side, not mixed, not cross-contained.  
> ecosystem-cloud = cloud abstraction; platform-cloud = platform deployment.