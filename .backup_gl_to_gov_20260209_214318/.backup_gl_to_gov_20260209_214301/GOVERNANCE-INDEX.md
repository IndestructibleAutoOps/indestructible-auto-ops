# Governance Directory Index

**IndestructibleAutoOps Governance Architecture**  
**Version**: 1.0.0  
**Last Updated**: 2026-02-07  
**Status**: ✅ Production Ready

---

## Overview

This index provides navigation to all governance directories in the IndestructibleAutoOps repository. The governance structure follows Machine Native Governance Architecture (MNGA) principles with strict GL (Governance Layers) compliance.

---

## 🏗️ Core Governance Architectures

### [`mnga-governance/`](./mnga-governance/)
**Machine Native Governance Architecture**  
**GL Layer**: GL00-09 (Strategic)  
**Purpose**: Core governance architecture for machine-native operations

**Subdirectories**:
- `core/` - Core MNGA specifications and charter
- `enforcement/` - Enforcement rules and validation
- `validation/` - Validation frameworks and schemas
- `contracts/` - Governance contracts and SLAs

**Key Files**:
- `core/NG00000-ZERO-TOLERANCE-POLICY.yaml` - Zero tolerance policy
- `core/core-governance-spec.yaml` - Core governance specification

---

### [`mno-governance/`](./mno-governance/)
**Machine Native Ops Governance**  
**GL Layer**: GL10-29 (Operational)  
**Purpose**: Operational governance for machine-native infrastructure

**Subdirectories**:
- `operations/` - Operational policies and procedures
- `lifecycle/` - Lifecycle management specifications
- `automation/` - Automation policies and guardrails
- `monitoring/` - Operational monitoring specifications

**Key Files**:
- `operations/NG00201-lifecycle-standard.yaml` - Lifecycle standards
- `core/enforcement-rules.yaml` - Enforcement rules

---

### [`gqs-governance/`](./gqs-governance/)
**Governance Quantum Stack**  
**GL Layer**: GL90-99 (Meta)  
**Purpose**: Quantum governance with superposition states and validation

**Subdirectories**:
- `layers/` - GQS L0-L7 layer specifications
- `contracts/` - Quantum governance contracts
- `validation/` - Quantum validation and proof generation
- `closure/` - Governance closure mechanisms

**Key Files**:
- `contracts/gqs-layers.yaml` - GQS layer definitions (L0-L7)
- `layers/governance_closure_spec.yaml` - Closure specifications

---

## 🎯 G-Attribute Governance Directories

### [`gates-governance/`](./gates-governance/)
**Operation Control Gates** (5 attributes)  
**Purpose**: Operation checkpoints with enforcement rules

**Attributes**: `gates`, `gate_fidelity`, `gatekeeper`, `gateway`, `gateways`

**Subdirectories**:
- `checkpoints/` - Operation checkpoint definitions
- `enforcement/` - Gate enforcement rules
- `policies/` - Gate policies and approval workflows

**Key Files**:
- `core/operation-gate.yaml` - Main gate definitions
- `checkpoints/self-auditor-config.yaml` - Audit gates
- `checkpoints/gates.yaml` - Research workflow gates

---

### [`guardrails-governance/`](./guardrails-governance/)
**Safety and Compliance Boundaries** (4 attributes)  
**Purpose**: AI safety boundaries and compliance checks

**Attributes**: `guardrails`, `guards`, `gdpr_compliance`, `gdpr`

**Subdirectories**:
- `safety/` - Safety guardrails specifications
- `compliance/` - Compliance requirements and checks
- `policies/` - Guardrail policies and actions

**Key Files**:
- `safety/ai-constitution.yaml` - AI safety constitution

---

### [`global-governance/`](./global-governance/)
**System-wide Configuration** (5 attributes)  
**Purpose**: Global system configuration and policies

**Attributes**: `global`, `global_config`, `global_policy`, `global_aliases`, `global_best_practices`

**Subdirectories**:
- `config/` - Global configuration specifications
- `policies/` - System-wide policies
- `aliases/` - Global naming aliases

**Key Files**:
- `config/global-aliases.yaml` - Global aliases
- `policies/language-policy.yaml` - Language policy

---

### [`gateway-governance/`](./gateway-governance/)
**API and Network Gateway** (4 attributes)  
**Purpose**: API gateway and network routing specifications

**Attributes**: `gateway`, `gateways`

**Subdirectories**:
- `routing/` - Gateway routing specifications
- `security/` - Gateway security configurations
- `monitoring/` - Gateway monitoring and metrics

**Key Files**:
- `routing/gateway-config.yaml` - Gateway configuration

---

### [`gap-governance/`](./gap-governance/)
**Gap Analysis and Planning** (6 attributes)  
**Purpose**: Gap analysis and remediation tracking

**Attributes**: `gap`, `gaps`, `gap_analysis`, `gap_description`, `gap_tolerance`, `gap_action`

**Subdirectories**:
- `analysis/` - Gap analysis specifications
- `remediation/` - Gap remediation plans
- `tracking/` - Gap tracking and metrics

**Key Files**:
- `analysis/gap-list.md` - Gap list template

---

### [`generation-governance/`](./generation-governance/)
**Artifact Generation** (15+ attributes)  
**Purpose**: Artifact generation and metadata tracking

**Attributes**: `generate`, `generated`, `generated_at`, `generated_by`, `generation_timestamp`, etc.

**Subdirectories**:
- `standards/` - Generation standards and specifications
- `generators/` - Generator configurations
- `metadata/` - Generation metadata specifications

**Key Files**:
- `core/hash_policy.yaml` - Hash generation policy

---

### [`group-governance/`](./group-governance/)
**Resource Grouping** (5 attributes)  
**Purpose**: Resource grouping and organization

**Attributes**: `group`, `groups`, `group_by`, `group_wait`, `group_interval`

**Subdirectories**:
- `policies/` - Grouping policies and rules
- `workflows/` - Workflow grouping configurations
- `monitoring/` - Monitoring group configurations

**Key Files**:
- `monitoring/workflow-monitor.yml` - Workflow monitor configuration

---

### [`gcp-governance/`](./gcp-governance/)
**Google Cloud Platform** (12+ attributes)  
**Purpose**: GCP infrastructure specifications and configurations

**Attributes**: `gcp`, `gcp_project`, `gcp_bucket`, `gke_cluster`, `gcs`, etc.

**Subdirectories**:
- `infrastructure/` - GCP infrastructure specifications
- `monitoring/` - GCP monitoring configurations
- `security/` - GCP security specifications

**Key Files**:
- `infrastructure/gcp/` - GCP provider configurations

---

### [`grafana-governance/`](./grafana-governance/)
**Monitoring Dashboards** (1+ attributes)  
**Purpose**: Grafana dashboard and visualization specifications

**Attributes**: `grafana`

**Subdirectories**:
- `dashboards/` - Dashboard specifications
- `datasources/` - Datasource configurations
- `alerts/` - Alert configurations

**Key Files**:
- `core/grafana/` - Grafana configurations
- `core/monitoring-stack.yaml` - AWS monitoring stack

---

## 📊 Statistics

| Category | Count |
|----------|-------|
| **Total Governance Directories** | 12 |
| **Core Architectures** | 3 (MNGA, MNO, GQS) |
| **G-Attribute Domains** | 9 |
| **Total Attributes Covered** | 60+ |
| **GL Layers Represented** | GL00-09, GL10-29, GL90-99 |

---

## 🔍 Quick Navigation

### By GL Layer
- **GL00-09 (Strategic)**: [`mnga-governance/`](./mnga-governance/)
- **GL10-29 (Operational)**: [`mno-governance/`](./mno-governance/)
- **GL90-99 (Meta)**: [`gqs-governance/`](./gqs-governance/)

### By Function
- **Operation Control**: [`gates-governance/`](./gates-governance/)
- **Safety**: [`guardrails-governance/`](./guardrails-governance/)
- **Configuration**: [`global-governance/`](./global-governance/)
- **Infrastructure**: [`gateway-governance/`](./gateway-governance/), [`gcp-governance/`](./gcp-governance/)
- **Monitoring**: [`grafana-governance/`](./grafana-governance/)
- **Analysis**: [`gap-governance/`](./gap-governance/)
- **Automation**: [`generation-governance/`](./generation-governance/), [`group-governance/`](./group-governance/)

---

## 📚 Related Documentation

- [G-SPECIFICATION-README.md](./G-SPECIFICATION-README.md) - G-specification attributes guide
- [G-ATTRIBUTES-QUICK-REFERENCE.md](./G-ATTRIBUTES-QUICK-REFERENCE.md) - Quick reference
- [G-SPECIFICATION-ATTRIBUTES-DISCOVERY-REPORT.md](./G-SPECIFICATION-ATTRIBUTES-DISCOVERY-REPORT.md) - Full analysis
- [GOVERNANCE-RESTRUCTURE-SPEC.yaml](./GOVERNANCE-RESTRUCTURE-SPEC.yaml) - Restructure specification
- `governance/audit/restructure-evidence.json` - Audit trail

---

## 🔧 Tools

### Governance Restructure Executor
```bash
# View governance structure
python3 governance-restructure-executor.py

# Execute restructuring (already completed)
python3 governance-restructure-executor.py --execute
```

### Validation
```bash
# Validate GL compliance
python ecosystem/enforce.py

# Check governance boundaries
npm run validate:gl
```

---

## ✅ Compliance

This governance structure follows:
- ✅ GL (Governance Layers) semantic boundaries
- ✅ MNGA (Machine Native Governance Architecture) v1.0
- ✅ FHS+GL directory mapping standards
- ✅ Audit trail requirements
- ✅ Machine-readable specifications

---

## 🚀 Usage

### For Developers
1. Navigate to relevant governance directory
2. Review README.md for domain overview
3. Check subdirectories for specific specs
4. Follow documented policies and procedures

### For Architects
1. Review core governance architectures (MNGA, MNO, GQS)
2. Understand G-attribute governance domains
3. Ensure compliance with governance boundaries
4. Reference specifications in architecture decisions

### For Operations
1. Consult MNO governance for operational policies
2. Check gates-governance for operation checkpoints
3. Review guardrails-governance for safety boundaries
4. Monitor gap-governance for remediation tracking

---

## 📞 Support

For governance-related questions:
1. Check the relevant governance directory README
2. Review the G-specification documentation
3. Consult the GOVERNANCE-RESTRUCTURE-SPEC.yaml
4. Contact the governance committee

---

**Maintained by**: IndestructibleAutoOps  
**Governance Level**: CONSTITUTIONAL  
**Last Restructure**: 2026-02-07  
**Audit Trail**: `governance/audit/restructure-evidence.json`

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-07 | Initial governance restructure completed |

---

**Status**: ✅ Active and Compliant
