# GL Metadata Layer Specification

## Metadata Layer - 元數據層

### Layer Overview

The Metadata Layer defines naming conventions for metadata resources including labels, annotations, descriptions, versions, and timestamps. This layer ensures consistent metadata management across all platform resources, enabling effective resource discovery, indexing, and governance.

### 1. Label Naming

**Pattern**: `gl.metadata.label`

**Format**: `gl.{scope}.{key}-label`

**Naming Rules**:
- Must use label identifier: `-label`
- Scope identifies the label context
- Key identifies the label type: `environment|owner|team|tier|region|zone|component|version`

**Examples**:
```yaml
# Valid
gl.runtime.environment-label
gl.api.owner-label
gl.data.team-label
gl.security.tier-label

# Invalid
environment-label
runtime-label
label
```

**Purpose**: Resource identification and categorization

### 2. Annotation Naming

**Pattern**: `gl.metadata.annotation`

**Format**: `gl.{scope}.{type}-annotation`

**Naming Rules**:
- Must use annotation identifier: `-annotation`
- Scope identifies the annotation context
- Type identifies annotation type: `documentation|monitoring|networking|security|deployment|custom`

**Examples**:
```yaml
# Valid
gl.runtime.documentation-annotation
gl.api.monitoring-annotation
gl.data.networking-annotation
gl.security.security-annotation

# Invalid
documentation-annotation
runtime-annotation
annotation
```

**Purpose**: Non-identifying metadata for resource management

### 3. Description Naming

**Pattern**: `gl.metadata.description`

**Format**: `gl.{resource}.{purpose}-description`

**Naming Rules**:
- Must use description identifier: `-description`
- Resource identifies the described resource
- Purpose identifies description type: `summary|detailed|technical|business`

**Examples**:
```yaml
# Valid
gl.runtime.summary-description
gl.api.detailed-description
gl.data.technical-description

# Invalid
description
summary-description
runtime-description
```

**Purpose**: Human-readable resource descriptions

### 4. Version Naming

**Pattern**: `gl.metadata.version`

**Format**: `gl.{component}.{type}-version`

**Naming Rules**:
- Must use version identifier: `-version`
- Component identifies the versioned component
- Type identifies version type: `semantic|build|release|api|schema`

**Examples**:
```yaml
# Valid
gl.runtime.semantic-version
gl.api.build-version
gl.data.release-version
gl.security.api-version

# Invalid
version
semantic-version
runtime-version
```

**Purpose**: Version information and tracking

### 5. Timestamp Naming

**Pattern**: `gl.metadata.timestamp`

**Format**: `gl.{event}.{type}-timestamp`

**Naming Rules**:
- Must use timestamp identifier: `-timestamp`
- Event identifies the timestamped event
- Type identifies timestamp type: `creation|update|deletion|expiration|activation`

**Examples**:
```yaml
# Valid
gl.runtime.creation-timestamp
gl.api.update-timestamp
gl.data.deletion-timestamp
gl.security.expiration-timestamp

# Invalid
timestamp
creation-timestamp
runtime-timestamp
```

**Purpose**: Temporal metadata for lifecycle management

### 6. Tag Naming

**Pattern**: `gl.metadata.tag`

**Format**: `gl.{domain}.{category}-tag`

**Naming Rules**:
- Must use tag identifier: `-tag`
- Domain identifies the tag domain
- Category identifies tag category: `environment|cost|compliance|security|operational|business`

**Examples**:
```yaml
# Valid
gl.runtime.environment-tag
gl.api.cost-tag
gl.data.compliance-tag
gl.security.security-tag

# Invalid
tag
environment-tag
runtime-tag
```

**Purpose**: Resource categorization and grouping

### 7. Property Naming

**Pattern**: `gl.metadata.property`

**Format**: `gl.{scope}.{attribute}-property`

**Naming Rules**:
- Must use property identifier: `-property`
- Scope identifies the property context
- Attribute identifies property type: `configuration|feature|capability|constraint`

**Examples**:
```yaml
# Valid
gl.runtime.configuration-property
gl.api.feature-property
gl.data.capability-property
gl.security.constraint-property

# Invalid
property
configuration-property
runtime-property
```

**Purpose**: Resource properties and attributes

### 8. Attribute Naming

**Pattern**: `gl.metadata.attribute`

**Format**: `gl.{entity}.{type}-attribute`

**Naming Rules**:
- Must use attribute identifier: `-attribute`
- Entity identifies the attributed entity
- Type identifies attribute type: `custom|standard|extended|computed`

**Examples**:
```yaml
# Valid
gl.runtime.custom-attribute
gl.api.standard-attribute
gl.data.extended-attribute
gl.security.computed-attribute

# Invalid
attribute
custom-attribute
runtime-attribute
```

**Purpose**: Entity attributes and metadata

### 9. Reference Naming

**Pattern**: `gl.metadata.reference`

**Format**: `gl.{source}.{target}-reference`

**Naming Rules**:
- Must use reference identifier: `-reference`
- Source identifies the referencing resource
- Target identifies the referenced resource type

**Examples**:
```yaml
# Valid
gl.runtime.deployment-reference
gl.api.service-reference
gl.data.pod-reference
gl.security.config-reference

# Invalid
reference
deployment-reference
runtime-reference
```

**Purpose**: Cross-resource references and relationships

### 10. Checksum Naming

**Pattern**: `gl.metadata.checksum`

**Format**: `gl.{resource}.{type}-checksum`

**Naming Rules**:
- Must use checksum identifier: `-checksum`
- Resource identifies the checksummed resource
- Type identifies checksum type: `sha256|md5|crc32|blake2`

**Examples**:
```yaml
# Valid
gl.runtime.sha256-checksum
gl.api.md5-checksum
gl.data.crc32-checksum
gl.security.blake2-checksum

# Invalid
checksum
sha256-checksum
runtime-checksum
```

**Purpose**: Data integrity and verification

### 11. Fingerprint Naming

**Pattern**: `gl.metadata.fingerprint`

**Format**: `gl.{component}.{type}-fingerprint`

**Naming Rules**:
- Must use fingerprint identifier: `-fingerprint`
- Component identifies the fingerprinted component
- Type identifies fingerprint type: `deployment|configuration|image|manifest`

**Examples**:
```yaml
# Valid
gl.runtime.deployment-fingerprint
gl.api.configuration-fingerprint
gl.data.image-fingerprint
gl.security.manifest-fingerprint

# Invalid
fingerprint
deployment-fingerprint
runtime-fingerprint
```

**Purpose**: Component identification and change detection

### 12. Metadata Layer Integration

### Cross-Layer Dependencies
- **Depends on**: All layers (provides metadata for all resources)
- **Provides**: Standardized metadata conventions
- **Works with**: Governance Layer for compliance metadata

### Naming Hierarchy
```
gl.metadata/
├── identification/
│   ├── gl.metadata.label
│   ├── gl.metadata.tag
│   └── gl.metadata.reference
├── documentation/
│   ├── gl.metadata.annotation
│   └── gl.metadata.description
├── lifecycle/
│   ├── gl.metadata.version
│   └── gl.metadata.timestamp
├── properties/
│   ├── gl.metadata.property
│   └── gl.metadata.attribute
└── verification/
    ├── gl.metadata.checksum
    └── gl.metadata.fingerprint
```

### Validation Rules

### Rule ML-001: Label Format
- **Severity**: CRITICAL
- **Check**: Labels must follow DNS subdomain format (max 253 chars)
- **Pattern**: `^[a-z0-9]([-a-z0-9]*[a-z0-9])?$`

### Rule ML-002: Annotation Size
- **Severity**: HIGH
- **Check**: Annotation values must be < 256KB
- **Enforcement**: Validate size before application

### Rule ML-003: Version Format
- **Severity**: CRITICAL
- **Check**: Semantic versions must follow SemVer 2.0.0
- **Pattern**: `^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$`

### Rule ML-004: Timestamp Format
- **Severity**: CRITICAL
- **Check**: Timestamps must follow ISO 8601 format
- **Format**: `YYYY-MM-DDTHH:MM:SSZ`

### Rule ML-005: Label Key Prefix
- **Severity**: MEDIUM
- **Check**: Custom labels must use `gl.{domain}/` prefix
- **Pattern**: `^gl\.[a-z]+/`

### Rule ML-006: Checksum Algorithm
- **Severity**: HIGH
- **Check**: Checksums must specify algorithm
- **Required**: sha256 (recommended), md5, crc32

### Usage Examples

### Example 1: Complete Metadata Stack
```yaml
# Labels
metadata:
  labels:
    gl.runtime.environment: production
    gl.api.owner: team-data-platform
    gl.data.team: backend-engineering
    gl.security.tier: critical

# Annotations
metadata:
  annotations:
    gl.runtime.documentation: "https://docs.gl.runtime/api"
    gl.api.monitoring: "prometheus.io/scrape: true"
    gl.data.networking: "networking.k8s.io/ingress: true"
    gl.security.compliance: "SOC2, ISO27001"

# Description
metadata:
  description: gl.runtime.summary-description

# Version
metadata:
  version: gl.runtime.semantic-version
  versionValue: "1.2.3"
  
# Timestamp
metadata:
  creationTimestamp: gl.runtime.creation-timestamp
  creationTimestampValue: "2024-01-15T10:30:00Z"
```

### Example 2: Kubernetes Metadata
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gl.runtime.core-deployment
  labels:
    gl.runtime.environment: production
    gl.runtime.component: core
    gl.api.owner: platform-team
    gl.data.team: backend
  annotations:
    gl.runtime.documentation: "https://docs.gl.runtime/deployment"
    gl.api.monitoring: "prometheus.io/port: 8080"
    gl.security.compliance: "SOC2"
  description: "GL Runtime Core Platform Deployment"
  version: "1.0.0"
spec:
  replicas: 3
  template:
    metadata:
      labels:
        gl.runtime.environment: production
        gl.runtime.component: core
      annotations:
        gl.runtime.checksum: "sha256:abc123..."
```

### Example 3: Version and Timestamp Management
```yaml
# Semantic Versioning
apiVersion: gl.io/v1
kind: Version
metadata:
  name: gl.runtime.semantic-version
spec:
  major: 1
  minor: 2
  patch: 3
  prerelease: "beta.1"
  build: "20240115"
  
# Timestamp Tracking
apiVersion: gl.io/v1
kind: Timestamp
metadata:
  name: gl.runtime.creation-timestamp
spec:
  type: creation
  value: "2024-01-15T10:30:00Z"
  timezone: UTC
  
apiVersion: gl.io/v1
kind: Timestamp
metadata:
  name: gl.runtime.update-timestamp
spec:
  type: update
  value: "2024-01-15T11:00:00Z"
  timezone: UTC
```

### Example 4: Checksum and Fingerprint
```yaml
# Checksum Verification
apiVersion: gl.io/v1
kind: Checksum
metadata:
  name: gl.runtime.sha256-checksum
spec:
  type: sha256
  value: "a1b2c3d4e5f6..."
  resource: gl.runtime.core-deployment
  
# Deployment Fingerprint
apiVersion: gl.io/v1
kind: Fingerprint
metadata:
  name: gl.runtime.deployment-fingerprint
spec:
  type: deployment
  value: "fp1234567890abcdef"
  algorithm: blake2
  computedAt: "2024-01-15T10:30:00Z"
```

### Best Practices

### Label Organization
```yaml
# Standard label structure
labels:
  # Environment
  gl.runtime.environment: production
  
  # Ownership
  gl.api.owner: platform-team
  gl.data.team: backend
  
  # Classification
  gl.security.tier: critical
  gl.data.classification: confidential
  
  # Technical
  gl.runtime.component: core
  gl.api.version: "1.0.0"
```

### Annotation Standards
```yaml
# Standard annotation structure
annotations:
  # Documentation
  gl.runtime.documentation: "https://docs.gl.runtime"
  
  # Monitoring
  gl.api.monitoring: "enabled"
  gl.data.metrics: "prometheus"
  
  # Networking
  gl.network.ingress: "true"
  gl.network.service: "true"
  
  # Security
  gl.security.compliance: "SOC2, ISO27001"
  gl.security.audit: "true"
```

### Version Management
```yaml
# Semantic versioning strategy
versions:
  - gl.runtime.semantic-version: "1.0.0"
  - gl.api.build-version: "20240115"
  - gl.data.release-version: "v1.2.3"
  - gl.security.api-version: "v2"
```

### Tool Integration

### Kubernetes Labels and Annotations
```bash
# Apply labels
kubectl label pod gl.runtime.core-pod gl.runtime.environment=production

# Apply annotations
kubectl annotate deployment gl.runtime.core-deployment \
  gl.runtime.documentation="https://docs.gl.runtime"

# Query by labels
kubectl get pods -l gl.runtime.environment=production
```

### Metadata Validation
```python
# Python validation script
def validate_label(key: str, value: str) -> bool:
    """Validate Kubernetes label"""
    if len(key) > 253:
        return False
    if len(value) > 63:
        return False
    return True

def validate_annotation(key: str, value: str) -> bool:
    """Validate Kubernetes annotation"""
    if len(key) > 253:
        return False
    if len(value) > 262144:  # 256KB
        return False
    return True
```

### Pre-commit Hooks
```bash
#!/bin/bash
# Validate metadata naming conventions
for file in $(git diff --name-only --cached | grep -E '\.(yaml|yml)$'); do
  # Check label naming
  if grep -E "labels:" "$file" | grep -vE "gl\..+:"; then
    echo "ERROR: Invalid label naming in $file"
    exit 1
  fi
  
  # Check annotation naming
  if grep -E "annotations:" "$file" | grep -vE "gl\..+:"; then
    echo "ERROR: Invalid annotation naming in $file"
    exit 1
  fi
done
```

### Compliance Checklist

- [x] Label naming follows `gl.{scope}.{key}-label` pattern
- [x] Annotation naming includes `-annotation` identifier
- [x] Description naming includes `-description` identifier
- [x] Version naming includes `-version` identifier
- [x] Timestamp naming includes `-timestamp` identifier
- [x] Tag naming includes `-tag` identifier
- [x] Property naming includes `-property` identifier
- [x] Attribute naming includes `-attribute` identifier
- [x] Reference naming includes `-reference` identifier
- [x] Checksum naming includes `-checksum` identifier
- [x] Fingerprint naming includes `-fingerprint` identifier
- [x] Labels follow DNS subdomain format
- [x] Annotations respect size limits
- [x] Versions follow SemVer 2.0.0
- [x] Timestamps use ISO 8601 format
- [x] Custom labels use `gl.{domain}/` prefix

### References

- Kubernetes Labels and Annotations: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
- SemVer 2.0.0: https://semver.org/
- ISO 8601: https://www.iso.org/standard/40874.html
- Metadata Best Practices: CNCF Metadata Standards
- Naming Convention Principles: gl-prefix-principles-engineering.md