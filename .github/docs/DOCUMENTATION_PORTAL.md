# GL Unified Charter Activated
# MachineNativeOps Documentation Portal

**Welcome to the MachineNativeOps Documentation Portal**

This portal provides comprehensive documentation for the AI-native infrastructure platform with governance automation, module-based architecture, and supply chain security.

---

## 🚀 Quick Start

### New Users
1. [Introduction](../README.md) - Project overview and getting started
2. [Integration Guide](PHASE1_INTEGRATION_GUIDE.md) - Step-by-step integration instructions
3. [Architecture Overview](#architecture) - System architecture and design

### Developers
1. [Module Development](#modules) - Creating and managing modules
2. [Policy Enforcement](#governance) - Understanding governance policies
3. [CI/CD Integration](#cicd) - Integrating with CI/CD pipelines
4. [Copilot Memory Guide](COPILOT_MEMORY.md) - Configure Copilot Memory settings

### Operators
1. [Deployment Guide](DEPLOYMENT-GUIDE.md) - Production deployment
2. [Monitoring & Observability](#monitoring) - System monitoring
3. [Troubleshooting](#troubleshooting) - Common issues and solutions

---

## 📚 Documentation Structure

### Core Documentation

#### 1. Architecture & Design
- [Phase 1 Completion Report](../PHASE1_COMPLETION_REPORT.md) - Foundation strengthening summary
- [Research Verification Plan](../research_report_verification_plan.md) - Architecture verification and planning
- [Integration Status](../PHASE1_INTEGRATION_STATUS.md) - Current integration status
- [Pending Integrations Complete](../PENDING_INTEGRATIONS_COMPLETE.md) - Completed Phase 2 items
- [Inference Ecosystem Integration](architecture/inference_ecosystem_integration_Architecture.md) - AEP Engine integration guide
- [Inference Ecosystem Integration ADR](adr/ADR-001-inference-ecosystem-integration.md) - Governance decision record
- [Pull-All-Files Architecture](architecture/pull_all_files_Architecture.md) - File organizer bulk retrieval
- [Pull-All-Files ADR](adr/ADR-002-pull-all-files.md) - Governance decision record

#### 2. Modules
- [Module Registry](../controlplane/baseline/modules/REGISTRY.yaml) - Central module registry
- [Module Manifests](../controlplane/baseline/modules/) - Individual module definitions
- [01-Core Module](../controlplane/baseline/modules/01-core/module-manifest.yaml) - Core engine
- [02-Intelligence Module](../controlplane/baseline/modules/02-intelligence/module-manifest.yaml) - Intelligence engine
- [03-Governance Module](../controlplane/baseline/modules/03-governance/module-manifest.yaml) - Governance system
- [04-Autonomous Module](../controlplane/baseline/modules/04-autonomous/module-manifest.yaml) - Autonomous systems
- [05-Observability Module](../controlplane/baseline/modules/05-observability/module-manifest.yaml) - Observability
- [06-Security Module](../controlplane/baseline/modules/06-security/module-manifest.yaml) - Security & supply chain

#### 3. Governance & Policies
- [Policy Framework](../controlplane/governance/policies/README.md) - Policy-as-Code overview
- [Policy Manifest](../controlplane/governance/policies/POLICY_MANIFEST.yaml) - Central policy registry
- [Naming Policy](../controlplane/governance/policies/naming.rego) - Kebab-case enforcement
- [Semantic Policy](../controlplane/governance/policies/semantic.rego) - Semantic consistency
- [Security Policy](../controlplane/governance/policies/security.rego) - Security requirements
- [Autonomy Policy](../controlplane/governance/policies/autonomy.rego) - Autonomy level rules

#### 4. Supply Chain Security
- [Supply Chain Security Guide](supply-chain-security.md) - Implementation guide
- [SBOM Generation](supply-chain-security.md#sbom-generation) - Software Bill of Materials
- [SLSA Provenance](supply-chain-security.md#slsa-provenance) - Provenance attestations
- [Artifact Signing](supply-chain-security.md#artifact-signing) - Cosign integration
- [Vulnerability Scanning](supply-chain-security.md#vulnerability-scanning) - Trivy scanning

---

## 🎯 Live Dashboards

### Governance Metrics
- [Language Governance Dashboard](LANGUAGE_GOVERNANCE_DASHBOARD.md) - Real-time governance metrics
  - Semantic health scores (Current: 97.5%)
  - Module status distribution
  - Policy enforcement tracking
  - Health alerts and recommendations

### Dependency Analysis
- [DAG Visualization](dag-visualization/DAG_VISUALIZATION.md) - Module dependency graph
  - Mermaid diagram (GitHub-rendered)
  - ASCII tree view
  - Dependency statistics
  - Cycle detection results

### Integration Status
- [Phase 1 Integration Status](../PHASE1_INTEGRATION_STATUS.md) - Live integration tracking
  - Component completion metrics
  - Validation results
  - CI/CD workflow status
  - Next action items

### Autonomy Classification
- [Autonomy Summary](autonomy/AUTONOMY_SUMMARY.md) - Comprehensive autonomy overview
  - Module classification reports
  - Progression tracking
  - Recommendations
- [Autonomy Progress Report](autonomy/AUTONOMY_PROGRESS_REPORT.md) - Progress tracking over time
  - Historical snapshots
  - Trend analysis
  - Target progress
- [Classification Reports](autonomy/reports/) - Individual module reports
  - [01-core](autonomy/reports/01-core-classification.md)
  - [02-intelligence](autonomy/reports/02-intelligence-classification.md)
  - [03-governance](autonomy/reports/03-governance-classification.md)
  - [04-autonomous](autonomy/reports/04-autonomous-classification.md)
  - [05-observability](autonomy/reports/05-observability-classification.md)
  - [06-security](autonomy/reports/06-security-classification.md)

### Interactive Visualizations
- [Interactive DAG Visualization](dag-visualization/interactive/index.html) - D3.js powered dependency graph
  - Multiple layout options (hierarchical, force-directed, radial)
  - Click nodes for detailed information
  - Zoom and pan support
  - SVG export capability

### Policy Compliance
- [Policy Remediation Report](POLICY_REMEDIATION_REPORT.md) - Policy violation analysis
  - Naming violations
  - Semantic health issues
  - Security gaps
  - Auto-remediation suggestions

---

## 🔧 Developer Guides

### Module Development
1. [Module Manifest Schema](../controlplane/baseline/modules/module-manifest.schema.json) - JSON Schema
2. [Creating New Modules](#creating-modules) - Step-by-step guide
3. [Module Interfaces](#module-interfaces) - Interface design
4. [Dependency Management](#dependencies) - Managing module dependencies

### Policy Development
1. [OPA/Rego Basics](#opa-basics) - Introduction to OPA
2. [Writing Policies](#writing-policies) - Policy development guide
3. [Testing Policies](#testing-policies) - Policy testing strategies
4. [Policy Enforcement](#policy-enforcement) - Enforcement mechanisms

### CI/CD Integration
1. [Workflow Overview](../.github/workflows/) - Available workflows
2. [Infrastructure Validation](../.github/workflows/infrastructure-validation.yml) - Automated validation
3. [Policy Gates](../.github/workflows/policy-gate.yml) - Policy enforcement gates
4. [Supply Chain Security](../.github/workflows/supply-chain-security.yml) - SBOM & provenance

---

## 🛠️ Operations Guides

### Validation & Testing
- [Infrastructure Validation](../scripts/validate-infrastructure.sh) - Comprehensive validation script
- [Module Validation](../scripts/validate-module-manifests.py) - Module manifest validator
- [Registry Validation](../scripts/validate-module-registry.py) - Registry validator
- [Policy Validation](#policy-validation) - OPA policy testing

### Dashboard Generation
- [Governance Dashboard Generator](../scripts/generate-governance-dashboard.py) - Generate governance metrics
- [DAG Visualization Generator](../scripts/generate-dag-visualization.py) - Generate dependency graphs
- [Autonomy Classifier](../scripts/classify-autonomy.py) - Classify autonomy levels
- [Autonomy Summary Generator](../scripts/generate-autonomy-summary.py) - Generate autonomy summary reports
- [Policy Auto-Remediation](../scripts/auto-remediate-policy.py) - Auto-fix policy violations

### Troubleshooting
- [Common Issues](PHASE1_INTEGRATION_GUIDE.md#troubleshooting) - Frequently encountered problems
- [GitBook Sync Troubleshooting](GITBOOK_SYNC_TROUBLESHOOTING.md) - GitBook 同步故障排除指南 (中文)
- [GitBook Sync Troubleshooting (EN)](GITBOOK_SYNC_TROUBLESHOOTING_EN.md) - GitBook synchronization issues (English)
- [Validation Failures](#validation-failures) - Debugging validation errors
- [Policy Violations](#policy-violations) - Resolving policy violations
- [Build Issues](#build-issues) - CI/CD build problems

---

## 📊 Reference Documentation

### Frameworks & Standards
- [Autonomy Classification Framework](AUTONOMY_CLASSIFICATION_FRAMEWORK.md) - L1-L5 autonomy levels
- [Semantic Health Criteria](#semantic-health) - Semantic consistency requirements
- [Naming Conventions](#naming-conventions) - Kebab-case standards
- [Security Standards](#security-standards) - SBOM, SLSA, signing requirements

### API Reference
- [Module Manifest API](#module-manifest-api) - Module manifest structure
- [Policy API](#policy-api) - OPA policy interface
- [Registry API](#registry-api) - Module registry structure

### Tool Reference
- [Validation Tools](../scripts/) - All validation scripts
- [Generation Tools](../scripts/) - Dashboard and report generators
- [CI/CD Workflows](../.github/workflows/) - Automated workflows

---

## 🎓 Tutorials

### Getting Started
1. **[Setting Up Your Environment](#setup)**
   - Prerequisites and dependencies
   - Tool installation
   - Initial configuration

2. **[Creating Your First Module](#first-module)**
   - Module structure
   - Writing a manifest
   - Registering the module

3. **[Implementing a Policy](#first-policy)**
   - OPA/Rego basics
   - Writing rules
   - Testing and validation

### Advanced Topics
1. **[Multi-Module Applications](#multi-module)**
   - Dependency management
   - Interface design
   - Integration testing

2. **[Autonomous Systems](#autonomous-systems)**
   - L1-L5 progression
   - AI/ML integration
   - Self-healing patterns

3. **[Supply Chain Hardening](#supply-chain-hardening)**
   - SBOM generation
   - Provenance tracking
   - Signature verification

---

## 🔗 External Resources

### Standards & Specifications
- [SLSA Framework](https://slsa.dev/) - Supply chain security framework
- [OPA Documentation](https://www.openpolicyagent.org/docs/) - Open Policy Agent
- [Sigstore](https://www.sigstore.dev/) - Signing and transparency
- [SPDX](https://spdx.dev/) - Software Package Data Exchange

### Tools
- [syft](https://github.com/anchore/syft) - SBOM generation
- [Cosign](https://docs.sigstore.dev/cosign/overview/) - Container signing
- [Trivy](https://aquasecurity.github.io/trivy/) - Vulnerability scanning
- [Graphviz](https://graphviz.org/) - Graph visualization

---

## 📝 Contributing

### Documentation
- [Documentation Standards](#doc-standards) - Writing guidelines
- [Markdown Style Guide](#markdown-style) - Formatting conventions
- [Diagram Guidelines](#diagram-guidelines) - Creating diagrams

### Code Contributions
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute
- [Code Standards](#code-standards) - Coding conventions
- [PR Process](#pr-process) - Pull request workflow

---

## 🆘 Support

### Getting Help
- [Troubleshooting Guide](PHASE1_INTEGRATION_GUIDE.md#troubleshooting) - Common issues
- [FAQ](#faq) - Frequently asked questions
- [Community](#community) - Community resources

### Reporting Issues
- [Bug Reports](#bug-reports) - How to report bugs
- [Feature Requests](#feature-requests) - Requesting new features
- [Security Issues](../SECURITY.md) - Reporting security vulnerabilities

---

## 📅 Release Notes

### Current Version: Phase 1 Complete + Extensions
- ✅ Module organization (6 modules)
- ✅ Policy framework (4 policies)
- ✅ Supply chain security (SBOM, SLSA, Cosign)
- ✅ Infrastructure validation
- ✅ Policy gates in CI/CD
- ✅ Governance dashboard
- ✅ DAG visualization
- ✅ Autonomy classification framework

### Recent Updates
- 2026-01-18: Added autonomy classification framework
- 2026-01-18: Completed pending integrations (policy gates, dashboards, DAG)
- 2026-01-18: Added infrastructure validation and CI/CD workflows
- 2026-01-18: Merged Phase 1 foundation from feat/rename-repository-to-mno

---

## 📖 Quick Reference

### Common Commands

```bash
# Validate all infrastructure
./scripts/validate-infrastructure.sh

# Generate governance dashboard
python3 scripts/generate-governance-dashboard.py

# Generate DAG visualization
python3 scripts/generate-dag-visualization.py

# Classify module autonomy
python3 scripts/classify-autonomy.py --module 01-core --format markdown

# Generate autonomy summary report
python3 scripts/generate-autonomy-summary.py

# Track autonomy progress (record snapshot)
python3 scripts/autonomy-progress-tracker.py --record

# Generate autonomy progress report
python3 scripts/autonomy-progress-tracker.py --report

# Scan for policy violations
python3 scripts/auto-remediate-policy.py --policy all --report

# Auto-fix naming violations (dry-run)
python3 scripts/auto-remediate-policy.py --policy naming --fix --dry-run

# Validate module manifest
python3 scripts/validate-module-manifests.py

# Validate registry
python3 scripts/validate-module-registry.py
```

### File Locations

```
docs/                           # Documentation portal
├── DOCUMENTATION_PORTAL.md     # This file
├── PHASE1_INTEGRATION_GUIDE.md # Integration guide
├── LANGUAGE_GOVERNANCE_DASHBOARD.md # Live metrics
├── AUTONOMY_CLASSIFICATION_FRAMEWORK.md # Autonomy framework
├── POLICY_REMEDIATION_REPORT.md # Policy compliance report
├── supply-chain-security.md    # Supply chain guide
├── dag-visualization/          # DAG visualizations
└── autonomy/                   # Autonomy classification
    ├── AUTONOMY_SUMMARY.md     # Summary report
    └── reports/                # Individual module reports

controlplane/                   # Infrastructure configuration
├── baseline/modules/           # Module definitions
├── governance/policies/        # OPA policies
├── registries/                 # Registries
└── specifications/             # Specifications

scripts/                        # Automation scripts
├── validate-*.sh|py           # Validation tools
├── generate-*.py              # Generation tools
├── classify-*.py              # Classification tools
└── auto-remediate-policy.py   # Policy auto-remediation

.github/workflows/              # CI/CD workflows
├── infrastructure-validation.yml
├── policy-gate.yml
├── supply-chain-security.yml
└── scheduled-dashboard-updates.yml  # Automated dashboard updates
```

---

*This documentation portal is continuously updated. Last updated: 2026-01-18*
