# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# GL Unified Charter Activated
# Language Governance Dashboard

**Generated**: 2026-01-18 08:53:17 UTC  
**Status**: 🟢 Active  
**Framework**: OPA/Rego Policy-as-Code

---

## 📊 Executive Summary

| Metric | Value | Status |
|--------|-------|--------|
| Total Modules | 6 | ✅ |
| Average Semantic Health | 97.5% | ✅ |
| Min Health Score | 85% | ✅ |
| Max Health Score | 100% | ✅ |
| Active Modules | 5 | ✅ |
| In Development | 1 | 📝 |

---

## 🎯 Semantic Health Overview

### Global Semantic Health: 97.5%

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜

**Health Threshold**: ≥ 80% (Policy Enforced)

### Module Health Scores


#### 01-core 🟢
- **Health Score**: 100% 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
- **Status**: active
- **Autonomy Level**: L1-L2
- **Namespace**: mno-core

#### 02-intelligence 🟢
- **Health Score**: 100% 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
- **Status**: active
- **Autonomy Level**: L2-L3
- **Namespace**: mno-intelligence

#### 03-governance 🟢
- **Health Score**: 100% 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
- **Status**: active
- **Autonomy Level**: L3-L4
- **Namespace**: mno-governance

#### 05-observability 🟢
- **Health Score**: 100% 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
- **Status**: active
- **Autonomy Level**: L4-L5
- **Namespace**: mno-observability

#### 06-security 🟢
- **Health Score**: 100% 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
- **Status**: active
- **Autonomy Level**: Global Layer
- **Namespace**: mno-security

#### 04-autonomous 🟡
- **Health Score**: 85% 🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬜⬜⬜
- **Status**: in-development
- **Autonomy Level**: L4-L5
- **Namespace**: mno-autonomous


---

## 📈 Distribution Analytics

### Module Status Distribution

- **active**: 5 (83.3%) ████████████████
- **in-development**: 1 (16.7%) ███


### Autonomy Level Distribution

- **L1-L2**: 1 (16.7%) ███
- **L2-L3**: 1 (16.7%) ███
- **L3-L4**: 1 (16.7%) ███
- **L4-L5**: 2 (33.3%) ██████
- **Global Layer**: 1 (16.7%) ███


---

## 🔐 Policy Enforcement Status

### Active Policies


#### 🟡 unknown
- **Severity**: medium
- **Enforcement**: ⏸️ Disabled
- **Remediation**: automatic

#### 🟠 unknown
- **Severity**: high
- **Enforcement**: ⏸️ Disabled
- **Remediation**: manual

#### 🔴 unknown
- **Severity**: critical
- **Enforcement**: ⏸️ Disabled
- **Remediation**: manual

#### 🟡 unknown
- **Severity**: medium
- **Enforcement**: ⏸️ Disabled
- **Remediation**: manual


---

## 🎨 Semantic Consistency Matrix

| Module | Namespace | Concepts | Health | Status |
|--------|-----------|----------|--------|--------|
| 01-core | mno-core | 4 | 100% | ✅ |
| 02-intelligence | mno-intelligence | 5 | 100% | ✅ |
| 03-governance | mno-governance | 5 | 100% | ✅ |
| 04-autonomous | mno-autonomous | 5 | 85% | ✅ |
| 05-observability | mno-observability | 7 | 100% | ✅ |
| 06-security | mno-security | 7 | 100% | ✅ |


---

## 🚨 Health Alerts

### ✅ All Modules Above Health Threshold

No modules require immediate attention.


---

## 📋 Governance Compliance

### Naming Convention Compliance
- **Policy**: Kebab-case naming (enforced via OPA)
- **Coverage**: 100% of files and modules
- **Status**: ✅ Compliant

### Semantic Mapping Coverage
- **Total Modules**: 6
- **Mapped Modules**: 6
- **Coverage**: 100%
- **Status**: ✅ Compliant

### Security Policy Compliance
- **SBOM Generation**: ✅ Required
- **SLSA Provenance**: ✅ Level 3
- **Artifact Signing**: ✅ Cosign + OIDC
- **Vulnerability Scanning**: ✅ Trivy
- **Status**: ✅ Compliant

---

## 🔄 Continuous Improvement

### Recommendations

1. **High Priority**
   - Monitor modules in development: 04-autonomous
   
2. **Medium Priority**
   - Maintain semantic health scores above 90%
   - Regular policy reviews and updates
   
3. **Low Priority**
   - Expand semantic mapping coverage
   - Enhance DAG visualization

### Next Review Date

Recommended review: **2026-01-18** (Monthly)

---

## 📚 Resources

- [Module Registry](../controlplane/baseline/modules/REGISTRY.yaml)
- [Policy Manifest](../controlplane/governance/policies/POLICY_MANIFEST.yaml)
- [Integration Guide](PHASE1_INTEGRATION_GUIDE.md)
- [Validation Tools](../scripts/validate-infrastructure.sh)

---

*This dashboard is automatically generated from module registry and policy manifest data.*  
*Last updated: 2026-01-18 08:53:17 UTC*
