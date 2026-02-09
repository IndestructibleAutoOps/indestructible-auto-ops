# GL CI/CD Layer Specification

## CI/CD Layer - CI/CD 層

### Layer Overview

The CI/CD Layer defines naming conventions for CI/CD resources including workflows, jobs, steps, and deployments. This layer ensures consistent CI/CD management across the platform, enabling effective automation, deployment strategies, and release management.

### 1. Workflow Naming

**Pattern**: `gl.ci-cd.workflow`

**Format**: `gl.{project}.{type}-workflow`

**Naming Rules**:
- Must use workflow identifier: `-workflow`
- Project identifies the CI/CD project
- Type identifies the workflow type: `ci|cd|release|deploy|rollback`

**Examples**:
```yaml
# Valid
gl.runtime.ci-workflow
gl.data.cd-workflow
gl.security.release-workflow

# Invalid
ci-workflow
runtime-workflow
workflow
```

**Purpose**: CI/CD workflow definitions

### 2. Job Naming

**Pattern**: `gl.ci-cd.job`

**Format**: `gl.{workflow}.{task}-job`

**Naming Rules**:
- Must use job identifier: `-job`
- Workflow identifies the CI/CD workflow
- Task identifies the job task

**Examples**:
```yaml
# Valid
gl.runtime.build-job
gl.data.test-job
gl.security.deploy-job

# Invalid
build-job
runtime-job
job
```

**Purpose**: CI/CD job definitions

### 3. Step Naming

**Pattern**: `gl.ci-cd.step`

**Format**: `gl.{job}.{action}-step`

**Naming Rules**:
- Must use step identifier: `-step`
- Job identifies the CI/CD job
- Action identifies the step action

**Examples**:
```yaml
# Valid
gl.runtime.checkout-step
gl.data.build-step
gl.security.deploy-step

# Invalid
checkout-step
runtime-step
step
```

**Purpose**: CI/CD step definitions

### 4. Deployment Naming

**Pattern**: `gl.ci-cd.deployment`

**Format**: `gl.{environment}.{app}-deployment`

**Naming Rules**:
- Must use deployment identifier: `-deployment`
- Environment identifies the deployment environment
- App identifies the deployed application

**Examples**:
```yaml
# Valid
gl.runtime.prod-deployment
gl.data.staging-deployment
gl.security.dev-deployment

# Invalid
prod-deployment
runtime-deployment
deployment
```

**Purpose**: CI/CD deployment definitions

### 5. Release Naming

**Pattern**: `gl.ci-cd.release`

**Format**: `gl.{app}.{version}-release`

**Naming Rules**:
- Must use release identifier: `-release`
- App identifies the released application
- Version identifies the release version

**Examples**:
```yaml
# Valid
gl.runtime.1.2.3-release
gl.data.2.0.0-release
gl.security.1.5.0-release

# Invalid
1.2.3-release
runtime-release
release
```

**Purpose**: CI/CD release definitions

### 6. Rollback Naming

**Pattern**: `gl.ci-cd.rollback`

**Format**: `gl.{app}.{version}-rollback`

**Naming Rules**:
- Must use rollback identifier: `-rollback`
- App identifies the rolled back application
- Version identifies the rollback version

**Examples**:
```yaml
# Valid
gl.runtime.1.2.2-rollback
gl.data.1.9.0-rollback
gl.security.1.4.0-rollback

# Invalid
1.2.2-rollback
runtime-rollback
rollback
```

**Purpose**: CI/CD rollback definitions

### 7. Environment Naming

**Pattern**: `gl.ci-cd.environment`

**Format**: `gl.{project}.{type}-environment`

**Naming Rules**:
- Must use environment identifier: `-environment`
- Project identifies the CI/CD project
- Type identifies the environment type: `dev|staging|prod|test`

**Examples**:
```yaml
# Valid
gl.runtime.dev-environment
gl.data.staging-environment
gl.security.prod-environment

# Invalid
dev-environment
runtime-environment
environment
```

**Purpose**: CI/CD environment definitions

### 8. Pipeline Naming

**Pattern**: `gl.ci-cd.pipeline`

**Format**: `gl.{project}.{type}-pipeline`

**Naming Rules**:
- Must use pipeline identifier: `-pipeline`
- Project identifies the CI/CD project
- Type identifies the pipeline type: `build|test|deploy|monitor`

**Examples**:
```yaml
# Valid
gl.runtime.build-pipeline
gl.data.test-pipeline
gl.security.deploy-pipeline

# Invalid
build-pipeline
runtime-pipeline
pipeline
```

**Purpose**: CI/CD pipeline definitions

### 9. Promotion Naming

**Pattern**: `gl.ci-cd.promotion`

**Format**: `gl.{app}.{from-to}-promotion`

**Naming Rules**:
- Must use promotion identifier: `-promotion`
- App identifies the promoted application
- From-to identifies the promotion path

**Examples**:
```yaml
# Valid
gl.runtime.staging-to-prod-promotion
gl.data.dev-to-staging-promotion
gl.security.test-to-prod-promotion

# Invalid
staging-to-prod-promotion
runtime-promotion
promotion
```

**Purpose**: CI/CD promotion definitions

### 10. CI/CD Layer Integration

### Cross-Layer Dependencies
- **Depends on**: Build Layer (for CI/CD builds)
- **Provides**: CI/CD conventions
- **Works with**: Deployment Layer for deployment
- **Works with**: Testing Layer for CI/CD tests

### Naming Hierarchy
```
gl.ci-cd/
├── workflows/
│   ├── gl.ci-cd.workflow
│   └── gl.ci-cd.job
├── steps/
│   └── gl.ci-cd.step
├── deployments/
│   ├── gl.ci-cd.deployment
│   └── gl.ci-cd.release
├── rollback/
│   └── gl.ci-cd.rollback
├── environments/
│   └── gl.ci-cd.environment
├── pipelines/
│   └── gl.ci-cd.pipeline
└── promotions/
    └── gl.ci-cd.promotion
```

### Validation Rules

### Rule CL-001: Workflow Naming Convention
- **Severity**: CRITICAL
- **Check**: Workflows must follow `gl.{project}.{type}-workflow` pattern
- **Pattern**: `^gl\..+\.ci|cd|release|deploy|rollback-workflow$`

### Rule CL-002: Job Isolation
- **Severity**: HIGH
- **Check**: Jobs must be isolated
- **Required**: Separate containers or VMs

### Rule CL-003: Deployment Approval
- **Severity**: HIGH
- **Check**: Production deployments must be approved
- **Required**: Approval workflow and approvers

### Rule CL-004: Rollback Safety
- **Severity**: CRITICAL
- **Check**: Rollbacks must be tested
- **Required**: Rollback validation

### Rule CL-005: Environment Separation
- **Severity**: HIGH
- **Check**: Environments must be separated
- **Required: Separate infrastructure

### Rule CL-006: Promotion Gates
- **Severity**: MEDIUM
- **Check**: Promotions must have gates
- **Required**: Quality gates and success criteria

### Usage Examples

### Example 1: Complete CI/CD Stack
```yaml
# CI Workflow
apiVersion: gl.io/v1
kind: Workflow
metadata:
  name: gl.runtime.ci-workflow
spec:
  type: ci
  project: gl.runtime
  trigger:
    - push
    - pull_request
  jobs:
  - gl.runtime.build-job
  - gl.runtime.test-job

# CD Workflow
apiVersion: gl.io/v1
kind: Workflow
metadata:
  name: gl.runtime.cd-workflow
spec:
  type: cd
  project: gl.runtime
  trigger:
    - manual
  jobs:
  - gl.runtime.deploy-job
  - gl.runtime.verify-job

# Job
apiVersion: gl.io/v1
kind: Job
metadata:
  name: gl.runtime.build-job
spec:
  workflow: gl.runtime.ci-workflow
  steps:
  - gl.runtime.checkout-step
  - gl.runtime.build-step
  - gl.runtime.test-step
  timeout: 3600s
  retries: 2
```

### Example 2: Deployment and Release
```yaml
# Deployment
apiVersion: gl.io/v1
kind: Deployment
metadata:
  name: gl.runtime.prod-deployment
spec:
  environment: prod
  app: gl.runtime
  version: "1.2.3"
  strategy: rolling
  replicas: 3
  approval:
    required: true
    approvers:
    - devops-lead
    - product-owner

# Release
apiVersion: gl.io/v1
kind: Release
metadata:
  name: gl.runtime.1.2.3-release
spec:
  app: gl.runtime
  version: "1.2.3"
  environment: prod
  artifacts:
  - gl.runtime.binary-artifact
  - gl.runtime.docker-artifact
  changelog: |
    - Add new feature
    - Bug fixes
  releaseDate: "2024-01-15T00:00:00Z"
```

### Example 3: Rollback and Promotion
```yaml
# Rollback
apiVersion: gl.io/v1
kind: Rollback
metadata:
  name: gl.runtime.1.2.2-rollback
spec:
  app: gl.runtime
  version: "1.2.2"
  environment: prod
  reason: "Critical bug in 1.2.3"
  rollbackDate: "2024-01-15T12:00:00Z"
  approvedBy: devops-lead

# Promotion
apiVersion: gl.io/v1
kind: Promotion
metadata:
  name: gl.runtime.staging-to-prod-promotion
spec:
  app: gl.runtime
  from: staging
  to: prod
  version: "1.2.3"
  gates:
  - name: staging-tests
    status: passed
  - name: approval
    status: approved
  promotionDate: "2024-01-15T00:00:00Z"
```

### Best Practices

### Workflow Organization
```yaml
# Standard CI/CD workflows
workflows:
  ci:
    - gl.runtime.ci-workflow
    - gl.data.ci-workflow
  cd:
    - gl.runtime.cd-workflow
    - gl.data.cd-workflow
  release:
    - gl.runtime.release-workflow
    - gl.security.release-workflow
```

### Deployment Strategy
```yaml
# Deployment strategies
deployments:
  rolling:
    - gl.runtime.prod-deployment
  blue-green:
    - gl.data.prod-deployment
  canary:
    - gl.security.prod-deployment
```

### Tool Integration

### CI/CD Execution
```bash
# Run workflow
gl ci-cd workflow run gl.runtime.ci-workflow

# List workflows
gl ci-cd workflow list

# Get workflow status
gl ci-cd workflow status gl.runtime.ci-workflow
```

### Deployment Management
```python
# Python deployment management
def deploy(app, environment, version):
    """Deploy application"""
    deployment = Deployment(
        name=f"{app}.{environment}-deployment",
        app=app,
        environment=environment,
        version=version
    )
    deployment.create()
    deployment.wait_for_ready()
```

### Compliance Checklist

- [x] Workflow naming follows `gl.{project}.{type}-workflow` pattern
- [x] Job naming includes `-job` identifier
- [x] Step naming includes `-step` identifier
- [x] Deployment naming includes `-deployment` identifier
- [x] Release naming includes `-release` identifier
- [x] Rollback naming includes `-rollback` identifier
- [x] Environment naming includes `-environment` identifier
- [x] Pipeline naming includes `-pipeline` identifier
- [x] Promotion naming includes `-promotion` identifier
- [x] All workflows follow naming conventions
- [x] Jobs are isolated
- [x] Production deployments are approved
- [x] Rollbacks are tested
- [x] Environments are separated
- [x] Promotions have gates

### References

- CI/CD Best Practices: https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment
- Deployment Strategies: https://martinfowler.com/bliki/CanaryRelease.html
- GitHub Actions: https://docs.github.com/en/actions
- Naming Convention Principles: gl-prefix-principles-engineering.md