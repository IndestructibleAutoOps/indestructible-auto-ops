# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# GL Unified Charter Activated
# Phase 1 Infrastructure Integration Guide

**Last Updated**: 2026-01-18  
**Status**: Active Integration  
**Phase**: Phase 1 - Foundation Strengthening

---

## Overview

This guide provides step-by-step instructions for integrating and using the Phase 1 infrastructure components that were added from the `feat/rename-repository-to-mno` branch.

## Quick Start

### 1. Validate Infrastructure

Run the validation script to ensure all components are properly configured:

```bash
./scripts/validate-infrastructure.sh
```

This validates:
- ✅ Module manifests and schema
- ✅ Module registry and dependencies
- ✅ OPA/Rego governance policies
- ✅ Supply chain security configuration
- ✅ Documentation completeness

### 2. Review Module Organization

Explore the module structure:

```bash
tree controlplane/baseline/modules/
```

**Modules Available**:
- `01-core` - Core Engine & Infrastructure (L1-L2)
- `02-intelligence` - Intelligence Engine (L2-L3)
- `03-governance` - Governance System (L3-L4)
- `04-autonomous` - Autonomous Systems (L4-L5, in development)
- `05-observability` - Observability System (L4-L5)
- `06-security` - Security & Supply Chain (Global Layer, VETO)

### 3. Review Governance Policies

View available policies:

```bash
ls -la controlplane/governance/policies/*.rego
cat controlplane/governance/policies/readme.md
```

**Policies Available**:
- `naming.rego` - Kebab-case naming enforcement
- `semantic.rego` - Semantic consistency (≥80 health score)
- `security.rego` - Security and supply chain requirements
- `autonomy.rego` - Autonomy level progression rules

---

## Detailed Integration Steps

### Module Integration

#### Step 1: Review Module Manifests

Each module has a manifest file that defines its purpose, interfaces, and dependencies:

```bash
# View a module manifest
cat controlplane/baseline/modules/01-core/module-manifest.yaml
```

**Manifest Structure**:
```yaml
module_id: "01-core"
module_name: "Core Engine & Infrastructure"
autonomy_level: "L1-L2"
namespace: "mno-core"
dependencies: []
interfaces:
  - name: "ServiceRegistry"
    type: "service"
    endpoints: [...]
status: "active"
version: "1.0.0"
components: [...]
```

#### Step 2: Update Module Registry

When adding new components, update the module registry:

```bash
# Edit the registry
vim controlplane/baseline/modules/REGISTRY.yaml

# Validate changes
./scripts/validate-infrastructure.sh
```

#### Step 3: Map Components to Modules

Identify where existing components should be mapped:

```python
# Example: Map a component to a module
# In your component's metadata, add:
metadata:
  module: "01-core"
  namespace: "mno-core"
  autonomy_level: "L1"
```

---

### Policy Integration

#### Step 1: Install OPA (Open Policy Agent)

```bash
# Using the official install script
curl -L -o opa [EXTERNAL_URL_REMOVED]
chmod +x opa
sudo mv opa /usr/local/bin/

# Verify installation
opa version
```

#### Step 2: Test Policies

Test policies with sample data:

```bash
# Test naming policy
echo '{"resource": {"type": "file", "name": "test-file.yaml"}}' | \
  opa eval -d controlplane/governance/policies/naming.rego \
  'data.mno.governance.policies.naming.allow' -I

# Test semantic policy
echo '{"module": {"namespace": "mno-core", "semantic_mappings": ["mno-core-engine"], "semantic_health": 85}}' | \
  opa eval -d controlplane/governance/policies/semantic.rego \
  'data.mno.governance.policies.semantic.allow' -I
```

#### Step 3: Integrate Policies into CI/CD

The infrastructure validation workflow (`.github/workflows/infrastructure-validation.yml`) automatically validates policies on every push.

To add policy enforcement to other workflows:

```yaml
- name: Policy Check
  run: |
    opa check controlplane/governance/policies/*.rego
```

---

### Supply Chain Security Integration

#### Step 1: Install Supply Chain Tools

Run the automated setup script:

```bash
./scripts/supply-chain-tools-setup.sh
```

This installs:
- **syft** - SBOM generation
- **slsa-github-generator** - Provenance generation
- **cosign** - Artifact signing
- **trivy** - Vulnerability scanning

#### Step 2: Configure OIDC for Artifact Signing

In your GitHub repository settings:
1. Go to Settings → Security → Secrets and variables → Actions
2. Enable "Allow GitHub Actions to create and approve pull requests"
3. Configure OIDC provider (automatic with GitHub Actions)

#### Step 3: Enable Supply Chain Workflow

The workflow is already configured in `.github/workflows/supply-chain-security.yml`.

To trigger it:
```bash
# Push to main or develop
git push origin main

# Or trigger manually
gh workflow run supply-chain-security.yml
```

#### Step 4: Review SBOM and Provenance

After workflow runs, artifacts are available:
- SBOM files in `workspace/artifacts/sbom/`
- Provenance attestations uploaded to Rekor
- Signed artifacts with Cosign

---

## Integration with Existing Systems

### Integrating with Existing Workflows

Add infrastructure validation to existing workflows:

```yaml
name: My Existing Workflow

on: [push, pull_request]

jobs:
  infrastructure-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate infrastructure
        run: ./scripts/validate-infrastructure.sh
  
  my-existing-job:
    needs: infrastructure-check
    runs-on: ubuntu-latest
    steps:
      # ... your existing steps
```

### Integrating with Module Registry

When creating new components, register them in the module registry:

```python
# Example: Register a new component in Python
import yaml

def register_component(module_id, component_name, component_type, location):
    """Register a new component in the module manifest"""
    manifest_path = f"controlplane/baseline/modules/{module_id}/module-manifest.yaml"
    
    with open(manifest_path, 'r') as f:
        manifest = yaml.safe_load(f)
    
    # Add component
    manifest['components'].append({
        'name': component_name,
        'type': component_type,
        'location': location,
        'status': 'active'
    })
    
    with open(manifest_path, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False)

# Usage
register_component('01-core', 'MyNewService', 'service', 'lib/mno-core/my-service/')
```

---

## Validation and Testing

### Continuous Validation

The infrastructure validation workflow runs automatically on:
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main`
- Manual trigger via workflow_dispatch

### Local Validation

Before committing changes:

```bash
# Validate all infrastructure
./scripts/validate-infrastructure.sh

# Validate specific policy
opa check controlplane/governance/policies/naming.rego

# Validate module manifest
python3 -c "import yaml; yaml.safe_load(open('controlplane/baseline/modules/01-core/module-manifest.yaml'))"
```

### Testing Module Dependencies

Check for circular dependencies:

```bash
python3 << 'EOF'
import yaml

with open('controlplane/baseline/modules/REGISTRY.yaml', 'r') as f:
    registry = yaml.safe_load(f)

modules = {m['module_id']: m.get('dependencies', []) for m in registry['modules']}

# Simple cycle detection
def has_cycle(module_id, visited, rec_stack):
    visited.add(module_id)
    rec_stack.add(module_id)
    
    for dep in modules.get(module_id, []):
        if dep == 'none':
            continue
        if dep not in visited:
            if has_cycle(dep, visited, rec_stack):
                return True
        elif dep in rec_stack:
            return True
    
    rec_stack.remove(module_id)
    return False

visited = set()
for module_id in modules:
    if module_id not in visited:
        if has_cycle(module_id, visited, set()):
            print(f"❌ Circular dependency detected involving {module_id}")
            exit(1)

print("✅ No circular dependencies found")
EOF
```

---

## Troubleshooting

### Common Issues

#### 1. Validation Script Fails

**Error**: `Module manifest schema not found`

**Solution**:
```bash
# Check if schema exists
ls -la controlplane/baseline/modules/module-manifest.schema.json

# If missing, restore from git
git checkout HEAD -- controlplane/baseline/modules/module-manifest.schema.json
```

#### 2. OPA Policy Validation Fails

**Error**: `opa: command not found`

**Solution**:
```bash
# Install OPA
curl -L -o opa [EXTERNAL_URL_REMOVED]
chmod +x opa
sudo mv opa /usr/local/bin/
```

#### 3. YAML Syntax Errors

**Error**: `YAML syntax error in module manifest`

**Solution**:
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('path/to/file.yaml'))"

# Use a YAML linter
yamllint path/to/file.yaml
```

#### 4. Module Dependency Issues

**Error**: `Unknown dependency: module-xyz`

**Solution**:
1. Check if the dependency exists in the registry
2. Update the dependency name to match an existing module
3. Add the missing module to the registry

---

## Next Steps

### Phase 2 Planning

Review the research verification plan for Phase 2 tasks:

```bash
cat research_report_verification_plan.md | grep -A 20 "Phase 2"
```

**Recommended Next Steps**:
1. Implement Language Governance Dashboard
2. Create DAG visualization tools
3. Complete 04-autonomous module implementation
4. Integrate policies into deployment gates
5. Set up self-hosted runners

### Advanced Integration

**Module Interface Implementation**:
- Implement the interfaces defined in module manifests
- Create API endpoints for service interfaces
- Set up event-driven communication between modules

**Policy Refinement**:
- Add custom policies for project-specific requirements
- Create policy test suites
- Implement automated remediation for policy violations

**Supply Chain Enhancement**:
- Configure vulnerability scanning thresholds
- Set up SBOM publishing to artifact registry
- Implement signature verification in deployment pipelines

---

## Resources

### Documentation
- [Module Organization README](controlplane/baseline/modules/readme.md)
- [Policy Framework README](controlplane/governance/policies/readme.md)
- [Supply Chain Security Guide](docs/supply-chain-security.md)
- [Phase 1 Completion Report](PHASE1_COMPLETION_REPORT.md)

### Tools
- [OPA Documentation]([EXTERNAL_URL_REMOVED])
- [syft Documentation]([EXTERNAL_URL_REMOVED])
- [Cosign Documentation]([EXTERNAL_URL_REMOVED])
- [SLSA Framework]([EXTERNAL_URL_REMOVED])

### Support
- Review [FEATURE_BRANCH_MERGE_SUMMARY.md](FEATURE_BRANCH_MERGE_SUMMARY.md) for integration details
- Check [research_report_verification_plan.md](research_report_verification_plan.md) for gap analysis
- Run `./scripts/validate-infrastructure.sh` for health checks

---

**Integration Status**: ✅ Phase 1 Complete  
**Next Milestone**: Phase 2 - Advanced Integration  
**Support**: See documentation links above
