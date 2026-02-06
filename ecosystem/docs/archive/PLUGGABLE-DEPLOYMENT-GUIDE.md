# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Architecture Governance Framework Activated
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Architecture Governance Framework Activated
# Pluggable Deployment Guide
## Universal Deployment for Any Environment

---

## Overview

The pluggable deployment architecture enables you to deploy Machine Native Ops to **any environment** without modifying code. Simply:

1. Choose your provider (AWS, GCP, Azure, Kubernetes, Docker Compose, etc.)
2. Configure your environment via YAML files
3. Deploy using the universal deployment manager

---

## Quick Start

### Option 1: Automatic Deployment (Auto-Detect)

```python
from adk.plugins.deployment import UniversalDeploymentManager

# Auto-detect environment and deploy
manager = UniversalDeploymentManager(
    auto_detect=True,
    environment='production'
)

result = await manager.deploy()
print(result.to_dict())
```

### Option 2: Specify Provider

```python
from adk.plugins.deployment import UniversalDeploymentManager

# Deploy to AWS
manager = UniversalDeploymentManager(
    provider='aws',
    environment='production'
)

result = await manager.deploy()
print(result.to_dict())
```

### Option 3: Use Configuration File

```python
from adk.plugins.deployment import UniversalDeploymentManager

# Deploy using custom configuration
manager = UniversalDeploymentManager(
    provider='kubernetes',
    environment='staging',
    config_file='config/custom/my-config.yaml'
)

result = await manager.deploy()
print(result.to_dict())
```

---

## Supported Providers

### Cloud Providers

| Provider | Status | Key Features |
|----------|--------|--------------|
| **AWS** | ✅ Full Support | EKS, RDS, S3, ELB, Route53, CloudWatch |
| **GCP** | ✅ Full Support | GKE, Cloud SQL, Cloud Storage, Monitoring |
| **Azure** | ✅ Full Support | AKS, Azure SQL, Storage Accounts, Monitor |
| **DigitalOcean** | 🚧 Coming Soon | DOKS, Managed Databases, Spaces |
| **Linode** | 🚧 Coming Soon | LKE, Managed Databases, Object Storage |

### Container Platforms

| Provider | Status | Key Features |
|----------|--------|--------------|
| **Kubernetes** | ✅ Full Support | Deployments, Services, ConfigMaps, Secrets, RBAC |
| **Docker Compose** | ✅ Full Support | Services, Networks, Volumes, Health Checks |
| **Nomad** | 🚧 Coming Soon | Jobs, Services, Consul integration |
| **ECS** | 🚧 Coming Soon | Task definitions, Services, Load Balancers |
| **ACI** | 🚧 Coming Soon | Container instances, VNet integration |

---

## Configuration Architecture

### Configuration Hierarchy

Configuration is loaded in the following order (later configs override earlier ones):

1. **Base Configuration** (`config/base/`)
   - Provider-agnostic defaults
   - Application settings
   - Resource defaults
   - Security defaults

2. **Provider Configuration** (`config/providers/{provider}/`)
   - Provider-specific infrastructure
   - Resource mappings
   - Service configurations

3. **Environment Configuration** (`config/environments/{env}/`)
   - Environment-specific settings
   - Scaling policies
   - Feature flags

4. **Provider + Environment** (`config/providers/{provider}/environments/{env}/`)
   - Provider-specific environment settings
   - Regional configurations

5. **Custom Configuration** (Optional)
   - User-provided config file
   - Override any setting

6. **Environment Variables**
   - Format: `PROVIDER__SECTION__KEY`
   - Example: `AWS__INFRASTRUCTURE__VPC__CIDR=10.1.0.0/16`

### Example Directory Structure

```
config/
├── base/
│   ├── application.yaml
│   ├── services.yaml
│   ├── monitoring.yaml
│   └── security.yaml
├── providers/
│   ├── aws/
│   │   ├── infrastructure.yaml
│   │   ├── databases.yaml
│   │   ├── storage.yaml
│   │   └── environments/
│   │       ├── staging.yaml
│   │       └── production.yaml
│   ├── gcp/
│   │   └── infrastructure.yaml
│   ├── azure/
│   │   └── infrastructure.yaml
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   └── services.yaml
│   └── docker-compose/
│       └── services.yaml
└── environments/
    ├── staging.yaml
    └── production.yaml
```

---

## Deployment Examples

### Deploy to AWS

#### 1. Configure AWS Credentials

```bash
# Option 1: AWS CLI profile
aws configure --profile my-aws-profile

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

# Option 3: Configuration file
export AWS_PROFILE=my-aws-profile
```

#### 2. Configure Provider

Create `config/providers/aws/infrastructure.yaml`:

```yaml
provider:
  type: aws
  region: us-east-1
  profile: my-aws-profile  # Optional

infrastructure:
  vpc:
    enabled: true
    cidr: "10.0.0.0/16"
    subnets:
      public:
        count: 2
      private:
        count: 3
  
  kubernetes:
    enabled: true
    name: "machine-native-ops"
    version: "1.28"
    node_groups:
      main:
        min_size: 3
        max_size: 10
        instance_types:
          - "t3.medium"
```

#### 3. Deploy

```python
from adk.plugins.deployment import UniversalDeploymentManager

manager = UniversalDeploymentManager(
    provider='aws',
    environment='production'
)

result = await manager.deploy()
print(f"Deployment successful: {result.success}")
print(f"Resources created: {result.resources}")
```

---

### Deploy to GCP

#### 1. Configure GCP Credentials

```bash
# Service account key file
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Or use gcloud CLI
gcloud auth application-default login
```

#### 2. Configure Provider

Create `config/providers/gcp/infrastructure.yaml`:

```yaml
provider:
  type: gcp
  project: my-project-id
  region: us-central1
  service_account_file: /path/to/service-account-key.json

infrastructure:
  vpc:
    enabled: true
    name: "main-vpc"
    cidr: "10.0.0.0/16"
  
  kubernetes:
    enabled: true
    name: "machine-native-ops"
    location: us-central1-a
    node_pools:
      main:
        node_count: 3
        machine_type: "n1-standard-2"
```

#### 3. Deploy

```python
from adk.plugins.deployment import UniversalDeploymentManager

manager = UniversalDeploymentManager(
    provider='gcp',
    environment='production'
)

result = await manager.deploy()
```

---

### Deploy to Kubernetes

#### 1. Configure Kubernetes

```bash
# Set kubeconfig
export KUBECONFIG=/path/to/kubeconfig.yaml

# Or use default location
~/.kube/config
```

#### 2. Configure Provider

Create `config/providers/kubernetes/deployment.yaml`:

```yaml
provider:
  type: kubernetes

deployment:
  namespace:
    name: machine-native-ops
  
  deployments:
    api-server:
      replicas: 3
      image: "machine-native-ops/api-server:1.0.0"
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 500m
          memory: 512Mi
  
  services:
    api-server:
      type: LoadBalancer
      ports:
        - port: 80
          targetPort: 8080
```

#### 3. Deploy

```python
from adk.plugins.deployment import UniversalDeploymentManager

manager = UniversalDeploymentManager(
    provider='kubernetes',
    environment='production'
)

result = await manager.deploy()
```

---

### Deploy with Docker Compose

#### 1. Configure Services

Create `config/providers/docker-compose/services.yaml`:

```yaml
provider:
  type: docker-compose

services:
  api-server:
    image: machine-native-ops/api-server:1.0.0
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://user:password@postgres:5432/db
    depends_on:
      - postgres
  
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

#### 2. Deploy

```python
from adk.plugins.deployment import UniversalDeploymentManager

manager = UniversalDeploymentManager(
    provider='docker-compose',
    environment='production'
)

result = await manager.deploy()
```

---

## Advanced Features

### Dry Run Mode

Test deployment without actually creating resources:

```python
manager = UniversalDeploymentManager(
    provider='kubernetes',
    environment='production',
    dry_run=True
)

result = await manager.deploy()
# Check what would be deployed without actually deploying
print(result.to_dict())
```

### Rollback Support

Automatically rollback on failure:

```python
manager = UniversalDeploymentManager(
    provider='aws',
    environment='production',
    auto_rollback=True
)

result = await manager.deploy()
if not result.success:
    # Auto-rollback was attempted
    print(f"Rollback completed: {result.rolled_back}")
```

### Custom Deployment Plan

Create and validate deployment plan before deploying:

```python
manager = UniversalDeploymentManager(
    provider='aws',
    environment='production'
)

# Create deployment plan
plan = await manager.create_deployment_plan()

# Review plan
print(f"Steps: {len(plan.steps)}")
print(f"Estimated duration: {plan.estimated_duration}s")

# Deploy with plan
result = await manager.deploy_with_plan(plan)
```

### Environment Detection

Automatically detect current environment:

```python
from adk.plugins.deployment import EnvironmentDetector

detector = EnvironmentDetector()
env_info = detector.detect()

print(f"Environment: {env_info.type}")
print(f"Provider: {env_info.provider}")
print(f"Region: {env_info.region}")
```

---

## Environment Variables

### AWS Configuration

```bash
# Authentication
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_SESSION_TOKEN=your_token  # Optional
AWS_PROFILE=profile_name  # Optional
AWS_DEFAULT_REGION=us-east-1

# Infrastructure overrides
AWS__INFRASTRUCTURE__VPC__CIDR=10.1.0.0/16
AWS__INFRASTRUCTURE__KUBERNETES__VERSION=1.29
```

### GCP Configuration

```bash
# Authentication
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
GOOGLE_CLOUD_PROJECT=my-project
GOOGLE_CLOUD_REGION=us-central1

# Infrastructure overrides
GCP__INFRASTRUCTURE__VPC__CIDR=10.1.0.0/16
GCP__INFRASTRUCTURE__KUBERNETES__LOCATION=us-central1-a
```

### Azure Configuration

```bash
# Authentication
AZURE_SUBSCRIPTION_ID=your_subscription_id
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret

# Infrastructure overrides
AZURE__INFRASTRUCTURE__VNET__ADDRESS_PREFIX=10.1.0.0/16
AZURE__INFRASTRUCTURE__AKS__LOCATION=eastus
```

### Kubernetes Configuration

```bash
# Cluster access
KUBECONFIG=/path/to/kubeconfig.yaml
KUBERNETES_SERVICE_HOST=cluster_endpoint
KUBERNETES_SERVICE_PORT=443

# Deployment overrides
KUBERNETES__DEPLOYMENT__NAMESPACE=my-namespace
KUBERNETES__DEPLOYMENT__REPLICAS=5
```

---

## Troubleshooting

### Common Issues

#### 1. Authentication Failed

**AWS:**
```bash
# Verify credentials
aws sts get-caller-identity

# Check profile
aws configure --list-profiles
```

**GCP:**
```bash
# Verify authentication
gcloud auth list
gcloud config list

# Test service account
gcloud auth activate-service-account --key-file=/path/to/key.json
```

**Azure:**
```bash
# Verify login
az account show
az account list --output table
```

#### 2. Configuration Not Found

```bash
# Check config file exists
ls -la config/providers/aws/infrastructure.yaml

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('config/providers/aws/infrastructure.yaml'))"
```

#### 3. Provider Not Supported

```python
from adk.plugins.deployment import ProviderAdapterFactory

# List available providers
providers = ProviderAdapterFactory.list_providers()
print(f"Available providers: {providers}")

# Check if provider is supported
if ProviderAdapterFactory.is_provider_supported('aws'):
    print("AWS is supported")
```

#### 4. Deployment Failed

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Get detailed error information
manager = UniversalDeploymentManager(provider='aws')
result = await manager.deploy()

if not result.success:
    print(f"Errors: {result.errors}")
    print(f"Warnings: {result.warnings}")
```

---

## Best Practices

### 1. Configuration Management

- Use version control for all configuration files
- Separate configurations by environment (dev, staging, prod)
- Store sensitive data in secrets, not in config files
- Use environment variables for environment-specific values

### 2. Deployment Strategy

- Always test in staging environment first
- Use dry-run mode before production deployment
- Enable auto-rollback for production
- Monitor deployment progress and logs

### 3. Security

- Rotate credentials regularly
- Use least privilege IAM roles
- Enable encryption at rest and in transit
- Enable audit logging

### 4. Resource Management

- Set appropriate resource limits
- Use auto-scaling when possible
- Clean up unused resources
- Monitor costs regularly

---

## Extending the Architecture

### Adding a New Provider

1. Create adapter class implementing `ProviderAdapter` interface:

```python
from adk.plugins.deployment.adapters import ProviderAdapter

class MyProviderAdapter(ProviderAdapter):
    PROVIDER_NAME = "my-provider"
    
    async def deploy_infrastructure(self, config: dict) -> dict:
        # Implementation
        pass
    
    # Implement other required methods
```

2. Register the adapter:

```python
from adk.plugins.deployment.adapters import ProviderAdapterFactory

ProviderAdapterFactory.register_adapter('my-provider', MyProviderAdapter)
```

3. Create configuration files:

```yaml
# config/providers/my-provider/infrastructure.yaml
provider:
  type: my-provider

infrastructure:
  # Provider-specific configuration
```

4. Use the provider:

```python
manager = UniversalDeploymentManager(provider='my-provider')
result = await manager.deploy()
```

---

## API Reference

### UniversalDeploymentManager

**Constructor:**
```python
UniversalDeploymentManager(
    provider: Optional[str] = None,
    environment: str = 'production',
    config_file: Optional[str] = None,
    auto_detect: bool = True,
    dry_run: bool = False,
    auto_rollback: bool = False
)
```

**Methods:**
- `async deploy() -> DeploymentResult` - Deploy infrastructure
- `async rollback() -> bool` - Rollback deployment
- `async create_deployment_plan() -> DeploymentPlan` - Create deployment plan
- `async deploy_with_plan(plan: DeploymentPlan) -> DeploymentResult` - Deploy with plan
- `get_deployment_status() -> DeploymentStatus` - Get deployment status

### DeploymentResult

**Fields:**
- `success: bool` - Deployment success status
- `provider: str` - Provider name
- `environment: str` - Environment name
- `resources: Dict[str, Any]` - Created resources
- `errors: List[str]` - Error messages
- `warnings: List[str]` - Warning messages
- `duration: float` - Deployment duration in seconds

---

## Support

For questions or issues:
- Check the [Architecture Design Document](./k8s/production/PLUGGABLE_ARCHITECTURE_DESIGN.md)
- Review configuration examples in `config/`
- Enable debug logging for troubleshooting

---

**Version:** 1.0.0
**Last Updated:** January 2026