# GL Deployment Layer Specification

## 6. 部署層（Deployment Layer）

### 6.1 Layer Overview

The Deployment Layer defines naming conventions for Kubernetes and container orchestration resources. This layer ensures consistent naming across deployment configurations, enabling automated resource management and operational clarity.

### 6.2 Namespace Naming

**Pattern**: `gl.k8s.namespace`

**Format**: `gl.{platform}.{environment}-ns`

**Naming Rules**:
- Must use namespace identifier: `-ns`
- Platform segment follows platform naming ontology
- Environment segment: `dev|staging|prod|test`

**Examples**:
```yaml
# Valid
gl.runtime.dev-ns
gl.dev.prod-ns
gl.ai.test-ns

# Invalid
my-namespace
runtime-ns
dev
```

**Purpose**: Logical isolation boundaries for platform environments

### 6.3 Pod Naming

**Pattern**: `gl.k8s.pod`

**Format**: `gl.{platform}.{component}-pod`

**Naming Rules**:
- Must use pod identifier: `-pod`
- Component segment identifies the workload type
- Supports replica suffix for multiple instances

**Examples**:
```yaml
# Valid
gl.runtime.core-pod
gl.data.ingestion-pod
gl.ai.inference-pod
gl.runtime.core-pod-1
gl.runtime.core-pod-2

# Invalid
core-pod
runtime-app
my-pod
```

**Purpose**: Individual container deployment units

### 6.4 Deployment Naming

**Pattern**: `gl.k8s.deployment`

**Format**: `gl.{platform}.{component}-deployment`

**Naming Rules**:
- Must use deployment identifier: `-deployment`
- Describes scalable workload configuration
- Used with ReplicaSets for rolling updates

**Examples**:
```yaml
# Valid
gl.runtime.core-deployment
gl.data.etl-deployment
gl.ai.serving-deployment

# Invalid
core-deployment
deployment
app-deploy
```

**Purpose**: Manages ReplicaSets and provides declarative updates

### 6.5 Service Naming

**Pattern**: `gl.k8s.service`

**Format**: `gl.{platform}.{component}-svc`

**Naming Rules**:
- Must use service identifier: `-svc`
- Component identifies the exposed service
- DNS-compliant names (max 63 characters)

**Examples**:
```yaml
# Valid
gl.runtime.core-svc
gl.data.api-svc
gl.ai.model-svc

# Invalid
core-service
service
api
```

**Purpose**: Network abstraction for pods, service discovery, and load balancing

### 6.6 Ingress Naming

**Pattern**: `gl.k8s.ingress`

**Format**: `gl.{platform}.{component}-ingress`

**Naming Rules**:
- Must use ingress identifier: `-ingress`
- Defines external access rules for services
- May include routing component

**Examples**:
```yaml
# Valid
gl.runtime.api-ingress
gl.web.frontend-ingress
gl.ai.gateway-ingress

# Invalid
ingress
api-ingress
web-ingress
```

**Purpose**: HTTP/HTTPS routing and external access configuration

### 6.7 CRD Naming

**Pattern**: `gl.k8s.crd`

**Format**: `gl.{domain}.{resource}.crd`

**Naming Rules**:
- Must use CRD identifier: `.crd` suffix
- Domain segment identifies custom resource domain
- Resource segment identifies the resource type

**Examples**:
```yaml
# Valid
gl.runtime.job.crd
gl.data.pipeline.crd
gl.ai.model.crd

# Invalid
job-crd
customresource
model.crd
```

**Purpose**: Custom resource definitions for extending Kubernetes API

### 6.8 Operator Naming

**Pattern**: `gl.k8s.operator`

**Format**: `gl.{platform}.{component}-operator`

**Naming Rules**:
- Must use operator identifier: `-operator`
- Platform identifies managed platform
- Component identifies the managed resource

**Examples**:
```yaml
# Valid
gl.runtime.job-operator
gl.data.etl-operator
gl.ai.model-operator

# Invalid
operator
runtime-operator
jobop
```

**Purpose**: Automated management of custom resources and applications

### 6.9 ConfigMap Naming

**Pattern**: `gl.k8s.configmap`

**Format**: `gl.{platform}.{component}-config`

**Naming Rules**:
- Must use configmap identifier: `-config`
- Component identifies the configuration scope
- Separated from secrets for non-sensitive data

**Examples**:
```yaml
# Valid
gl.runtime.core-config
gl.data.pipeline-config
gl.ai.model-config

# Invalid
config
core-config
settings
```

**Purpose**: Non-sensitive configuration data storage

### 6.10 Secret Naming

**Pattern**: `gl.k8s.secret`

**Format**: `gl.{platform}.{component}-secret`

**Naming Rules**:
- Must use secret identifier: `-secret`
- Component identifies the secret scope
- Used for sensitive data only

**Examples**:
```yaml
# Valid
gl.runtime.creds-secret
gl.data.connection-secret
gl.ai.api-secret

# Invalid
secret
passwords
creds
```

**Purpose**: Sensitive data storage (credentials, keys, tokens)

### 6.11 Volume Naming

**Pattern**: `gl.k8s.volume`

**Format**: `gl.{platform}.{type}-volume`

**Naming Rules**- Must use volume identifier: `-volume`
- Type identifies volume type: `data|config|cache|logs`
- Persistent volume claims follow same pattern

**Examples**:
```yaml
# Valid
gl.runtime.data-volume
gl.cache.storage-volume
gl.logs.archive-volume

# Invalid
volume
data-vol
storage
```

**Purpose**: Data storage and persistence management

### 6.12 Autoscaling Naming

**Pattern**: `gl.k8s.autoscaling`

**Format**: `gl.{platform}.{component}-autoscaler`

**Naming Rules**:
- Must use autoscaler identifier: `-autoscaler`
- Component identifies the scalable workload
- Horizontal Pod Autoscaler (HPA) naming

**Examples**:
```yaml
# Valid
gl.runtime.core-autoscaler
gl.data.ingestion-autoscaler
gl.ai.inference-autoscaler

# Invalid
autoscaler
hpa
core-hpa
```

**Purpose**: Automatic workload scaling based on metrics

### 6.13 Rollout Naming

**Pattern**: `gl.k8s.rollout`

**Format**: `gl.{platform}.{component}-rollout`

**Naming Rules**:
- Must use rollout identifier: `-rollout`
- Component identifies the deployment target
- Used with Argo Rollouts for advanced deployment strategies

**Examples**:
```yaml
# Valid
gl.runtime.core-rollout
gl.data.pipeline-rollout
gl.ai.serving-rollout

# Invalid
rollout
deployment-rollout
app-rollout
```

**Purpose**: Advanced deployment strategies (canary, blue-green, analysis)

## 6.14 Deployment Layer Integration

### 6.14.1 Layer Dependencies
- Depends on: Platform Layer (gl.k8s.*)
- Provides: Runtime environment for Language Layer components
- Works with: ConfigMap, Secret for configuration

### 6.14.2 Naming Hierarchy
```
gl.k8s.namespace/
├── gl.k8s.deployment/
│   ├── gl.k8s.pod/
│   └── gl.k8s.service/
├── gl.k8s.ingress/
├── gl.k8s.configmap/
├── gl.k8s.secret/
├── gl.k8s.volume/
├── gl.k8s.autoscaling/
├── gl.k8s.rollout/
├── gl.k8s.operator/
└── gl.k8s.crd/
```

### 6.14.3 Cross-Layer Integration
- **Platform → Deployment**: Platform resources deployed as K8s resources
- **Deployment → Format**: YAML manifests follow Format Layer conventions
- **Deployment → Language**: Language-specific runtime configurations
- **Deployment → Contract**: Deployment contracts with infrastructure providers

## 6.15 Best Practices

### 6.15.1 Namespace Organization
```yaml
# Production namespace
gl.runtime.prod-ns:
  - gl.runtime.core-deployment
  - gl.runtime.api-svc
  - gl.runtime.core-autoscaler

# Development namespace
gl.runtime.dev-ns:
  - gl.runtime.core-deployment
  - gl.runtime.api-svc
```

### 6.15.2 Service Discovery
```yaml
# DNS-based service discovery
gl.runtime.core-svc.core-ns.svc.cluster.local
gl.data.api-svc.data-ns.svc.cluster.local
gl.ai.model-svc.ai-ns.svc.cluster.local
```

### 6.15.3 Configuration Management
```yaml
# Separation of concerns
gl.runtime.core-config      # Application config
gl.runtime.creds-secret     # Credentials
gl.runtime.data-volume      # Data persistence
```

### 6.15.4 Rolling Updates
```yaml
# Deployment strategy
gl.runtime.core-deployment:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

## 6.16 Validation Rules

### Rule DL-001: Namespace Identifier
- **Severity**: CRITICAL
- **Check**: Namespace must end with `-ns` identifier
- **Pattern**: `^gl\..+\.dev|staging|prod|test-ns$`

### Rule DL-002: Deployment Structure
- **Severity**: CRITICAL
- **Check**: Deployment must follow `gl.{platform}.{component}-deployment` pattern
- **Pattern**: `^gl\..+\..+-deployment$`

### Rule DL-003: Service DNS Compliance
- **Severity**: HIGH
- **Check**: Service names must be DNS-compliant (max 63 chars)
- **Enforcement**: Truncate and warn if exceeded

### Rule DL-004: Resource Limits
- **Severity**: MEDIUM
- **Check**: Deployments must have resource limits defined
- **Required**: `requests.cpu`, `requests.memory`, `limits.cpu`, `limits.memory`

## 6.17 Usage Examples

### Example 1: Microservice Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gl.runtime.core-deployment
  namespace: gl.runtime.prod-ns
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gl.runtime.core-pod
  template:
    metadata:
      labels:
        app: gl.runtime.core-pod
    spec:
      containers:
      - name: core
        image: gl.runtime.core:latest
        volumeMounts:
        - name: gl.runtime.data-volume
          mountPath: /data
        envFrom:
        - configMapRef:
            name: gl.runtime.core-config
        - secretRef:
            name: gl.runtime.creds-secret
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
      volumes:
      - name: gl.runtime.data-volume
        persistentVolumeClaim:
          claimName: gl.runtime.data-volume
---
apiVersion: v1
kind: Service
metadata:
  name: gl.runtime.core-svc
  namespace: gl.runtime.prod-ns
spec:
  selector:
    app: gl.runtime.core-pod
  ports:
  - port: 8080
    targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gl.runtime.core-autoscaler
  namespace: gl.runtime.prod-ns
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: gl.runtime.core-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Example 2: Ingress Configuration
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: gl.runtime.api-ingress
  namespace: gl.runtime.prod-ns
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: gl.letsencrypt
spec:
  tls:
  - hosts:
    - api.gl.runtime.prod
    secretName: gl.runtime.tls-secret
  rules:
  - host: api.gl.runtime.prod
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: gl.runtime.core-svc
            port:
              number: 8080
```

### Example 3: Custom Resource and Operator
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: gl.runtime.job.crd
spec:
  group: gl.runtime
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              image:
                type: string
              command:
                type: array
  scope: Namespaced
---
apiVersion: gl.runtime/v1
kind: Job
metadata:
  name: gl.runtime.job
  namespace: gl.runtime.prod-ns
spec:
  image: gl.runtime.job:latest
  command: ["/bin/sh", "-c", "echo hello"]
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gl.runtime.job-operator
  namespace: gl.runtime.prod-ns
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gl.runtime.job-operator-pod
  template:
    metadata:
      labels:
        app: gl.runtime.job-operator-pod
    spec:
      serviceAccountName: gl.runtime.job-operator
      containers:
      - name: operator
        image: gl.runtime.job-operator:latest
        env:
        - name: WATCH_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
```

## 6.18 Compliance Checklist

- [x] Namespace naming follows `gl.{platform}.{environment}-ns` pattern
- [x] Pod naming includes platform and component identifiers
- [x] Deployment naming follows `gl.{platform}.{component}-deployment` pattern
- [x] Service names are DNS-compliant and use `-svc` identifier
- [x] Ingress configurations use `-ingress` identifier
- [x] CRD naming uses `.crd` suffix with domain and resource
- [x] Operator naming follows `-operator` pattern
- [x] ConfigMap uses `-config` identifier
- [x] Secret uses `-secret` identifier for sensitive data
- [x] Volume naming includes type identifier `-volume`
- [x] Autoscaling uses `-autoscaler` identifier
- [x] Rollout naming follows `-rollout` pattern
- [x] Resource limits defined for all deployments
- [x] Proper separation of ConfigMap and Secret
- [x] DNS-compliant service names for service discovery

## 6.19 Tool Integration

### 6.19.1 Kubectl Validation
```bash
# Validate naming conventions
kubectl apply --dry-run=client -f deployment.yaml

# Check DNS compliance
kubectl get services -o jsonpath='{.items[*].metadata.name}' | \
  awk '{if (length($1) > 63) print "Service name exceeds 63 chars: " $1}'
```

### 6.19.2 Helm Chart Validation
```yaml
# Chart.yaml
name: gl-runtime-core
description: GL Runtime Core Platform
type: application

# values.yaml
deployment:
  name: gl.runtime.core-deployment
  namespace: gl.runtime.prod-ns

service:
  name: gl.runtime.core-svc
```

### 6.19.3 Pre-commit Hooks
```bash
#!/bin/bash
# Validate K8s naming conventions
for file in $(git diff --name-only --cached | grep -E '\.(yaml|yml)$'); do
  if grep -E "name: " "$file" | grep -vE "^gl\."; then
    echo "ERROR: Invalid naming in $file"
    exit 1
  fi
done
```

## 6.20 References

- Kubernetes Documentation: https://kubernetes.io/docs/concepts/
- Argo Rollouts: https://argoproj.github.io/argo-rollouts/
- Naming Convention Best Practices: gl-prefix-principles-engineering.md
- Platform Layer Specification: gl-platform-layer-specification.md
- Format Layer Specification: gl-format-layer-specification.md