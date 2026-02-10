# GL Dependency Layer Specification

## Dependency Layer - 依賴層

### Layer Overview

The Dependency Layer defines naming conventions for dependency resources including modules, packages, services, and their relationships. This layer ensures consistent dependency management across the platform, enabling effective modularity, decoupling, and dependency tracking.

### 1. Module Naming

**Pattern**: `gl.dependency.module`

**Format**: `gl.{platform}.{name}-module`

**Naming Rules**:
- Must use module identifier: `-module`
- Platform identifies the platform or system
- Name identifies the module name: `core|api|data|auth|cache|logging|config`

**Examples**:
```yaml
# Valid
gl.runtime.core-module
gl.api.data-module
gl.security.auth-module
gl.data.cache-module

# Invalid
module
core-module
runtime-module
```

**Purpose**: Modular code organization and encapsulation

### 2. Package Naming

**Pattern**: `gl.dependency.package`

**Format**: `gl.{language}.{type}-package`

**Naming Rules**:
- Must use package identifier: `-package`
- Language identifies the programming language
- Type identifies package type: `library|framework|sdk|tool|utility`

**Examples**:
```yaml
# Valid
gl.python.library-package
gl.javascript.framework-package
gl.go.sdk-package
gl.java.tool-package

# Invalid
package
library-package
python-package
```

**Purpose**: External package and library dependencies

### 3. Service Dependency Naming

**Pattern**: `gl.dependency.service`

**Format**: `gl.{platform}.{name}-service-dependency`

**Naming Rules**:
- Must use service dependency identifier: `-service-dependency`
- Platform identifies the platform
- Name identifies the dependent service

**Examples**:
```yaml
# Valid
gl.runtime.database-service-dependency
gl.api.auth-service-dependency
gl.data.cache-service-dependency
gl.security.log-service-dependency

# Invalid
service-dependency
database-service-dependency
runtime-service
```

**Purpose**: Service-to-service dependency relationships

### 4. Library Dependency Naming

**Pattern**: `gl.dependency.library`

**Format**: `gl.{language}.{name}-library-dependency`

**Naming Rules**:
- Must use library dependency identifier: `-library-dependency`
- Language identifies the programming language
- Name identifies the library name

**Examples**:
```yaml
# Valid
gl.python.requests-library-dependency
gl.javascript.express-library-dependency
gl.go.gin-library-dependency
gl.java.spring-library-dependency

# Invalid
library-dependency
requests-library-dependency
python-library
```

**Purpose**: External library dependencies

### 5. Framework Dependency Naming

**Pattern**: `gl.dependency.framework`

**Format**: `gl.{language}.{name}-framework-dependency`

**Naming Rules**:
- Must use framework dependency identifier: `-framework-dependency`
- Language identifies the programming language
- Name identifies the framework name

**Examples**:
```yaml
# Valid
gl.python.django-framework-dependency
gl.javascript.react-framework-dependency
gl.go.echo-framework-dependency
gl.java.spring-boot-framework-dependency

# Invalid
framework-dependency
django-framework-dependency
python-framework
```

**Purpose**: Framework dependencies

### 6. SDK Dependency Naming

**Pattern**: `gl.dependency.sdk`

**Format**: `gl.{provider}.{service}-sdk-dependency`

**Naming Rules**:
- Must use SDK dependency identifier: `-sdk-dependency`
- Provider identifies the cloud provider or vendor
- Service identifies the SDK service

**Examples**:
```yaml
# Valid
gl.aws.s3-sdk-dependency
gl.azure.storage-sdk-dependency
gl.gcp.pubsub-sdk-dependency
gl.auth.cognito-sdk-dependency

# Invalid
sdk-dependency
s3-sdk-dependency
aws-sdk
```

**Purpose**: SDK dependencies for cloud services

### 7. Plugin Dependency Naming

**Pattern**: `gl.dependency.plugin`

**Format**: `gl.{system}.{name}-plugin-dependency`

**Naming Rules**:
- Must use plugin dependency identifier: `-plugin-dependency`
- System identifies the plugin system
- Name identifies the plugin name

**Examples**:
```yaml
# Valid
gl.kubernetes.ingress-plugin-dependency
gl.prometheus.exporter-plugin-dependency
gl.logging.fluentd-plugin-dependency
gl.security.waf-plugin-dependency

# Invalid
plugin-dependency
ingress-plugin-dependency
kubernetes-plugin
```

**Purpose**: Plugin and extension dependencies

### 8. Binary Dependency Naming

**Pattern**: `gl.dependency.binary`

**Format**: `gl.{tool}.{name}-binary-dependency`

**Naming Rules**:
- Must use binary dependency identifier: `-binary-dependency`
- Tool identifies the tool or utility
- Name identifies the binary name

**Examples**:
```yaml
# Valid
gl.build.docker-binary-dependency
gl.dev.node-binary-dependency
gl.ops.kubectl-binary-dependency
gl.security.openssl-binary-dependency

# Invalid
binary-dependency
docker-binary-dependency
build-binary
```

**Purpose**: Binary and executable dependencies

### 9. Container Image Dependency Naming

**Pattern**: `gl.dependency.container-image`

**Format**: `gl.{platform}.{name}-container-image-dependency`

**Naming Rules**:
- Must use container image identifier: `-container-image-dependency`
- Platform identifies the platform or service
- Name identifies the image name

**Examples**:
```yaml
# Valid
gl.runtime.nginx-container-image-dependency
gl.api.redis-container-image-dependency
gl.data.postgres-container-image-dependency
gl.security.vault-container-image-dependency

# Invalid
container-image-dependency
nginx-container-image-dependency
runtime-container
```

**Purpose**: Container image dependencies

### 10. Helm Chart Dependency Naming

**Pattern**: `gl.dependency.helm-chart`

**Format**: `gl.{platform}.{name}-helm-chart-dependency`

**Naming Rules**:
- Must use Helm chart identifier: `-helm-chart-dependency`
- Platform identifies the platform or service
- Name identifies the chart name

**Examples**:
```yaml
# Valid
gl.runtime.ingress-helm-chart-dependency
gl.api.monitoring-helm-chart-dependency
gl.data.database-helm-chart-dependency
gl.security.cert-manager-helm-chart-dependency

# Invalid
helm-chart-dependency
ingress-helm-chart-dependency
runtime-helm-chart
```

**Purpose**: Helm chart dependencies

### 11. Terraform Module Dependency Naming

**Pattern**: `gl.dependency.terraform-module`

**Format**: `gl.{provider}.{resource}-terraform-module-dependency`

**Naming Rules**:
- Must use Terraform module identifier: `-terraform-module-dependency`
- Provider identifies the cloud provider
- Resource identifies the resource type

**Examples**:
```yaml
# Valid
gl.aws.vpc-terraform-module-dependency
gl.azure.network-terraform-module-dependency
gl.gcp.storage-terraform-module-dependency
gl.kubernetes.deployment-terraform-module-dependency

# Invalid
terraform-module-dependency
vpc-terraform-module-dependency
aws-terraform-module
```

**Purpose**: Terraform module dependencies

### 12. Dependency Graph Naming

**Pattern**: `gl.dependency.graph`

**Format**: `gl.{scope}.{level}-dependency-graph`

**Naming Rules**:
- Must use dependency graph identifier: `-dependency-graph`
- Scope identifies the graph scope
- Level identifies graph level: `module|service|platform|global`

**Examples**:
```yaml
# Valid
gl.runtime.module-dependency-graph
gl.api.service-dependency-graph
gl.data.platform-dependency-graph
gl.security.global-dependency-graph

# Invalid
dependency-graph
module-dependency-graph
runtime-dependency
```

**Purpose**: Dependency graph and relationship mapping

### 13. Dependency Layer Integration

### Cross-Layer Dependencies
- **Depends on**: All layers (manages dependencies for all resources)
- **Provides**: Dependency management conventions
- **Works with**: Governance Layer for dependency policies

### Naming Hierarchy
```
gl.dependency/
├── code/
│   ├── gl.dependency.module
│   ├── gl.dependency.package
│   └── gl.dependency.library
├── services/
│   ├── gl.dependency.service
│   └── gl.dependency.sdk
├── infrastructure/
│   ├── gl.dependency.framework
│   ├── gl.dependency.plugin
│   ├── gl.dependency.binary
│   └── gl.dependency.container-image
├── iac/
│   ├── gl.dependency.helm-chart
│   └── gl.dependency.terraform-module
└── analysis/
    └── gl.dependency.graph
```

### Validation Rules

### Rule DL-001: Module Naming Convention
- **Severity**: CRITICAL
- **Check**: Module names must follow `gl.{platform}.{name}-module` pattern
- **Pattern**: `^gl\..+\.core|api|data|auth|cache|logging|config-module$`

### Rule DL-002: Package Version Constraint
- **Severity**: HIGH
- **Check**: Package dependencies must specify version constraints
- **Required**: Caret (^), Tilde (~), or exact version (=)

### Rule DL-003: No Circular Dependencies
- **Severity**: CRITICAL
- **Check**: Dependency graphs must not contain cycles
- **Enforcement**: Detect and reject circular dependencies

### Rule DL-004: Service Dependency Health
- **Severity**: MEDIUM
- **Check**: Service dependencies must have health check configuration
- **Required**: Health check endpoint and timeout

### Rule DL-005: Dependency License Compliance
- **Severity**: HIGH
- **Check**: All dependencies must have license information
- **Required**: License type and compatibility check

### Rule DL-006: Security Vulnerability Scan
- **Severity**: HIGH
- **Check**: Dependencies must be scanned for vulnerabilities
- **Required**: Vulnerability report and remediation plan

### Rule DL-007: Container Image Digest
- **Severity**: CRITICAL
- **Check**: Container image dependencies must use digest-based references
- **Format**: `sha256:<digest>`

### Usage Examples

### Example 1: Complete Dependency Stack
```yaml
# Module Dependencies
apiVersion: gl.io/v1
kind: Module
metadata:
  name: gl.runtime.core-module
spec:
  type: module
  dependencies:
  - gl.api.data-module
  - gl.security.auth-module
  - gl.data.cache-module
  version: "1.0.0"

# Package Dependencies
apiVersion: gl.io/v1
kind: Package
metadata:
  name: gl.python.library-package
spec:
  type: package
  language: python
  dependencies:
  - name: requests
    version: "^2.28.0"
    license: Apache-2.0
  - name: numpy
    version: "^1.24.0"
    license: BSD-3-Clause

# Service Dependencies
apiVersion: gl.io/v1
kind: ServiceDependency
metadata:
  name: gl.runtime.database-service-dependency
spec:
  service: gl.data.postgres-service
  version: "1.0.0"
  healthCheck:
    endpoint: /health
    timeout: 5s
  fallback:
    enabled: true
    endpoint: /fallback
```

### Example 2: Dependency Graph
```yaml
apiVersion: gl.io/v1
kind: DependencyGraph
metadata:
  name: gl.runtime.service-dependency-graph
spec:
  scope: service
  nodes:
  - id: gl.runtime.core-service
    type: service
  - id: gl.api.auth-service
    type: service
  - id: gl.data.database-service
    type: service
  edges:
  - from: gl.runtime.core-service
    to: gl.api.auth-service
    type: required
  - from: gl.api.auth-service
    to: gl.data.database-service
    type: required
  - from: gl.runtime.core-service
    to: gl.data.cache-service
    type: optional
```

### Example 3: Container Image Dependencies
```yaml
apiVersion: gl.io/v1
kind: ContainerImageDependency
metadata:
  name: gl.runtime.nginx-container-image-dependency
spec:
  image: nginx:latest
  digest: sha256:abc123...
  securityScan:
    enabled: true
    severityThreshold: HIGH
  license: Apache-2.0
---
apiVersion: gl.io/v1
kind: ContainerImageDependency
metadata:
  name: gl.api.redis-container-image-dependency
spec:
  image: redis:7.0-alpine
  digest: sha256:def456...
  securityScan:
    enabled: true
    severityThreshold: MEDIUM
  license: BSD-3-Clause
```

### Example 4: Helm Chart Dependencies
```yaml
apiVersion: gl.io/v1
kind: HelmChartDependency
metadata:
  name: gl.runtime.ingress-helm-chart-dependency
spec:
  chart: ingress-nginx
  repository: https://kubernetes.github.io/ingress-nginx
  version: "4.5.0"
  values:
    controller:
      service:
        type: LoadBalancer
  securityScan:
    enabled: true
---
apiVersion: gl.io/v1
kind: HelmChartDependency
metadata:
  name: gl.data.database-helm-chart-dependency
spec:
  chart: postgresql
  repository: https://charts.bitnami.com/bitnami
  version: "12.1.0"
  values:
    auth:
      postgresPassword: secret
  securityScan:
    enabled: true
```

### Example 5: Terraform Module Dependencies
```yaml
apiVersion: gl.io/v1
kind: TerraformModuleDependency
metadata:
  name: gl.aws.vpc-terraform-module-dependency
spec:
  source: terraform-aws-modules/vpc/aws
  version: "3.19.0"
  variables:
    cidr: "10.0.0.0/16"
    azs: ["us-east-1a", "us-east-1b"]
  securityScan:
    enabled: true
---
apiVersion: gl.io/v1
kind: TerraformModuleDependency
metadata:
  name: gl.gcp.storage-terraform-module-dependency
spec:
  source: terraform-google-modules/storage-bucket/google
  version: "5.0.0"
  variables:
    location: US
    force_destroy: false
  securityScan:
    enabled: true
```

### Best Practices

### Dependency Management
```yaml
# Clear dependency hierarchy
dependencies:
  core:
    - gl.runtime.core-module
  services:
    - gl.api.auth-service-dependency
    - gl.data.cache-service-dependency
  infrastructure:
    - gl.aws.vpc-terraform-module-dependency
    - gl.runtime.nginx-container-image-dependency

# Version constraints
dependencies:
  - gl.python.requests-library-dependency: "^2.28.0"
  - gl.javascript.express-framework-dependency: "~4.18.0"
  - gl.go.gin-library-dependency: "1.9.1"
```

### Dependency Health
```yaml
# Service dependency health
healthChecks:
  gl.runtime.database-service-dependency:
    endpoint: /health
    interval: 30s
    timeout: 5s
    retries: 3
  gl.api.auth-service-dependency:
    endpoint: /healthz
    interval: 60s
    timeout: 10s
    retries: 3
```

### Security Scanning
```yaml
# Vulnerability scanning
security:
  enabled: true
  scanInterval: 24h
  severityThreshold: HIGH
  autoRemediation:
    enabled: true
    critical: true
    high: false
```

### Tool Integration

### Dependency Scanning
```bash
# Scan for vulnerabilities
trivy image gl.runtime.nginx:latest
snyk test gl.python.requests-library-dependency
npm audit gl.javascript.express-framework-dependency
```

### Dependency Graph Visualization
```python
# Generate dependency graph
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edge("gl.runtime.core-service", "gl.api.auth-service")
G.add_edge("gl.api.auth-service", "gl.data.database-service")

nx.draw(G, with_labels=True)
plt.savefig("dependency-graph.png")
```

### Pre-commit Hooks
```bash
#!/bin/bash
# Validate dependency naming conventions
for file in $(git diff --name-only --cached | grep -E '\.(yaml|yml|json)$'); do
  # Check module naming
  if grep -E "kind: Module" "$file" | grep -vE "name: gl\..+\.module"; then
    echo "ERROR: Invalid module naming in $file"
    exit 1
  fi
  
  # Check service dependency naming
  if grep -E "kind: ServiceDependency" "$file" | grep -vE "name: gl\..+\.service-dependency"; then
    echo "ERROR: Invalid service dependency naming in $file"
    exit 1
  fi
done
```

### Compliance Checklist

- [x] Module naming follows `gl.{platform}.{name}-module` pattern
- [x] Package naming includes `-package` identifier
- [x] Service dependency naming includes `-service-dependency` identifier
- [x] Library dependency naming includes `-library-dependency` identifier
- [x] Framework dependency naming includes `-framework-dependency` identifier
- [x] SDK dependency naming includes `-sdk-dependency` identifier
- [x] Plugin dependency naming includes `-plugin-dependency` identifier
- [x] Binary dependency naming includes `-binary-dependency` identifier
- [x] Container image naming includes `-container-image-dependency` identifier
- [x] Helm chart naming includes `-helm-chart-dependency` identifier
- [x] Terraform module naming includes `-terraform-module-dependency` identifier
- [x] Dependency graph naming includes `-dependency-graph` identifier
- [x] All dependencies have version constraints
- [x] No circular dependencies in dependency graphs
- [x] Service dependencies have health check configuration
- [x] All dependencies have license information
- [x] Dependencies are scanned for vulnerabilities
- [x] Container images use digest-based references

### References

- Dependency Management Best Practices: https://12factor.net/dependencies
- Semantic Versioning: https://semver.org/
- OWASP Dependency Check: https://owasp.org/www-project-dependency-check/
- Kubernetes Dependency Management: https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/
- Naming Convention Principles: gov-prefix-principles-engineering.md