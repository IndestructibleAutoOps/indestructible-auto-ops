# G-Attributes Quick Reference Guide

**Quick access guide to G-specification attributes in the IndestructibleAutoOps repository**

---

## Overview

This quick reference provides a categorized list of G-prefixed specification attributes found in the repository, excluding GL (Governance Layers) and GQS (Governance Quantum Stack) which are documented separately.

For detailed analysis, see: [G-SPECIFICATION-ATTRIBUTES-DISCOVERY-REPORT.md](./G-SPECIFICATION-ATTRIBUTES-DISCOVERY-REPORT.md)

---

## 🎯 Top 10 Most Important G-Attributes

| Attribute | Purpose | Primary Location |
|-----------|---------|------------------|
| **gates** | Operation control checkpoints | `ecosystem/gates/operation-gate.yaml` |
| **guardrails** | Safety boundaries | `.github/config/governance/ai-constitution.yaml` |
| **global** | System-wide configuration | `prometheus.yml`, `monitoring/*.yml` |
| **governance_owner** | Ownership metadata | Throughout governance files |
| **group** | Resource grouping | Workflow files, monitoring configs |
| **generated_at** | Generation timestamp | Generated artifacts |
| **gateway** | API/network routing | Infrastructure configs |
| **gcp** | Google Cloud Platform | `.github/config/providers/gcp/` |
| **grafana** | Monitoring dashboards | Monitoring stack configs |
| **gap** | Gap analysis | Workflow files |

---

## 📋 Complete Attribute Categories

### 1. Operation Control

```yaml
gates:                    # Operation checkpoints
gate_fidelity:           # Quantum gate fidelity
gatekeeper:              # Policy enforcement
gateway:                 # Network routing
gateways:                # Multiple gateways
```

**Example Location**: `ecosystem/gates/operation-gate.yaml`

---

### 2. Safety & Compliance

```yaml
guardrails:              # Safety boundaries
  safety:
  compliance:
guards:                  # Protection mechanisms
gdpr_compliance:         # GDPR adherence
```

**Example Location**: `.github/config/governance/ai-constitution.yaml`

---

### 3. System Configuration

```yaml
global:                  # System-wide settings
global_config:           # Global configuration
global_policy:           # System policies
global_aliases:          # Naming aliases
global_best_practices:   # Best practices
```

**Example Location**: `prometheus.yml`, `.config/alertmanager/`

---

### 4. Governance (20+ sub-attributes)

```yaml
governance_owner:         # Owner identification
governance_version:       # Version tracking
governance_stage:         # Development stage
governance_assertions:    # Validation assertions
governance_fallback:      # Fallback behavior
governance_binding_enforcement:  # Enforcement rules
governance_boundaries:    # Layer boundaries
governance_tokens:        # Token definitions
governance_chain:         # Chain of responsibility
governance_metadata:      # Additional metadata
governance_committee:     # Committee members
governance_loop:          # Governance loops
governance_loop_index:    # Loop indexing
governance_policy:        # Policy definitions
governance_baseline:      # Baseline configuration
governance_event_structure: # Event definitions
governance_requirements:  # Requirements
governance_compliance:    # Compliance status
governance_principles:    # Core principles
governance_events:        # Event tracking
governance_impact:        # Impact assessment
```

**Example Location**: `ecosystem/governance/specs/`, `.github/governance/`

---

### 5. Organizational

```yaml
group:                   # Group identifier
groups:                  # Group collections
group_by:                # Grouping criteria
group_wait:              # Wait duration
group_interval:          # Evaluation interval
```

**Example Location**: Workflow files, `monitoring/prometheus.yml`

---

### 6. Artifact Generation

```yaml
generate:                # Generation flag
generated:               # Generated marker
generated_at:            # Generation timestamp
generated_by:            # Generator identification
generation_timestamp:    # Alternative timestamp
generation_standards:    # Generation rules
generator:               # Generator configuration
generator_compatibility: # Compatibility specs
generators:              # Multiple generators
generate_charts:         # Chart generation
generate_reports:        # Report generation
generate_dag_visualization:  # DAG visualization
```

**Example Location**: Throughout specification files

---

### 7. Cloud Infrastructure

```yaml
# Google Cloud Platform
gcp:                     # GCP configuration
gcp_project:             # Project identifier
gcp_bucket:              # Storage bucket
gcp_cloud_logging:       # Logging service
gcp_compute:             # Compute resources
gcp_endpoint:            # Service endpoint
gcp_pubsub:              # Pub/Sub service
gcp_secret_manager:      # Secret management
gcp_service_account_key: # Service account
gcp_storage:             # Storage service
gke_cluster:             # Kubernetes cluster
gcs:                     # Cloud Storage

# Grafana
grafana:                 # Monitoring config
  enabled:
  adminPassword:
  datasources:
  persistence:
  service:
  dashboards:
```

**Example Location**: `.github/config/providers/gcp/`, monitoring configs

---

### 8. Analysis & Planning

```yaml
gap:                     # Gap identifier
gaps:                    # Gap collection
gap_analysis:            # Analysis results
gap_description:         # Gap details
gap_tolerance:           # Tolerance level
gap_action:              # Remediation action
```

**Example Location**: Workflow and analysis files

---

### 9. Language & Specifications

```yaml
grammar:                 # Language grammar
  tokens:
  syntax:
Go:                      # Go language config
  version:
  modules:
```

**Example Location**: `ecosystem/governance/ugs/l00-language/ldl.spec.yaml`

---

### 10. Performance & Resources

```yaml
gc_overhead_target:      # GC overhead limit
gc_pause_target:         # GC pause time target
gid:                     # Unix group ID
granularity:             # Granularity level
graph:                   # Graph configuration
grpc:                    # gRPC settings
```

**Example Location**: Performance configuration files

---

## 🔍 Finding Attributes by Use Case

### Security & Compliance
- `guardrails` - Safety enforcement
- `gdpr_compliance` - Data protection
- `gates` - Security gates
- `gatekeeper` - Policy enforcement

### Infrastructure
- `gcp`, `gcp_*` - Google Cloud Platform
- `grafana` - Monitoring
- `gateway`, `gateways` - Network routing
- `gke_cluster`, `gcs` - GCP services

### Governance
- `governance_owner` - Ownership
- `governance_version` - Versioning
- `governance_compliance` - Compliance
- `governance_metadata` - Metadata

### Development
- `generate_*` - Code/artifact generation
- `generated_at`, `generated_by` - Generation tracking
- `grammar` - Language definitions
- `Go` - Go language settings

---

## 📖 Annotation Tags

### @GL-* Tags (11 variants)

```yaml
# @GL-governed              # Governance control marker
# @GL-layer: GQS-L0         # Layer specification
# @GL-semantic: primitive    # Semantic classification
# @GL-audit-trail: path.json # Audit reference
# @GL-boundary: strict       # Boundary definition
# @GL-charter-version: 1.0   # Charter version
# @GL-evidence-chain: hash   # Evidence reference
# @GL-internal-only          # Internal use marker
# @GL-ownership: team        # Ownership
# @GL-revision: 42           # Revision number
# @GL-status: verified       # Status indicator
```

**Usage**: Header comments in YAML files

---

## 🗂️ File Locations

### Primary Configuration Files

```
ecosystem/
├── gates/
│   ├── operation-gate.yaml       # Main gate definitions
│   └── self-auditor-config.yaml  # Audit gates
├── governance/
│   └── specs/
│       └── governance_layer_boundaries.yaml
└── contracts/
    └── governance/
        └── gqs-layers.yaml       # GQS definitions

.github/
├── config/
│   ├── governance/
│   │   └── ai-constitution.yaml  # Guardrails
│   └── providers/
│       ├── gcp/                  # GCP configs
│       ├── aws/                  # AWS configs
│       └── azure/                # Azure configs
└── governance/
    └── architecture/
        └── gl-*.yaml             # GL architecture

governance/
└── workflows/
    └── research-loop/
        └── gates.yaml            # Research gates
```

---

## 🔗 Related Systems

### Integration with GL (Governance Layers)
- Many `governance_*` attributes are GL-specific
- `gl_version`, `gl_semantic_naming`, `gl_anchor` throughout

### Integration with GQS (Governance Quantum Stack)
- GQS defined in `ecosystem/contracts/governance/gqs-layers.yaml`
- Seven layers: `gqs_l0` through `gqs_l7`
- Quantum superposition states

---

## 📊 Usage Statistics

| Category | Attributes | Files |
|----------|-----------|-------|
| Governance | 20+ | 500+ |
| Global | 5+ | 150+ |
| Gates | 5+ | 20+ |
| Generation | 15+ | 100+ |
| GCP | 12+ | 10+ |
| Group | 5+ | 80+ |
| Grafana | 1 | 15+ |
| Gap | 6+ | 30+ |

---

## 🎓 Best Practices

### When to Use Each Attribute

1. **gates**: Use for operation checkpoints requiring approval or validation
2. **guardrails**: Use for safety boundaries in AI/ML operations
3. **global**: Use for system-wide configuration that affects all components
4. **governance_***: Use for governance metadata and tracking
5. **group**: Use for organizing related resources or workflow concurrency
6. **generate_***: Use for controlling artifact generation
7. **gateway**: Use for network routing and API gateway configuration

### Naming Conventions

- Use `snake_case` for all attributes
- Prefix governance sub-attributes with `governance_`
- Use plurals for collections: `gates:`, `groups:`, `generators:`
- Include timestamps: `generated_at`, `generation_timestamp`

---

## 🔄 Quick Command Reference

### Search for G-attributes
```bash
# Find all g/G keys in YAML files
grep -rh "^\s*[gG][a-z_]*:" --include="*.yaml" . | sort -u

# Find annotation tags
grep -rh "@G[A-Z]" --include="*.yaml" . | sort -u

# Find files with gates
find . -name "*gate*" -type f

# Count files with G-terms
find . -type f -name "*.yaml" -exec grep -l "gates\|guardrails\|governance" {} \; | wc -l
```

---

## 📞 Support

For detailed information:
- See [G-SPECIFICATION-ATTRIBUTES-DISCOVERY-REPORT.md](./G-SPECIFICATION-ATTRIBUTES-DISCOVERY-REPORT.md)
- Check individual configuration files
- Refer to `.github/copilot-instructions.md` for governance guidelines

---

**Last Updated**: 2026-02-07  
**Version**: 1.0  
**Status**: ✅ Complete
