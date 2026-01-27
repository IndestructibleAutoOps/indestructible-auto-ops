# Autonomy Classification Summary

**Generated**: 2026-01-18 10:55 UTC  
**Total Modules**: 6  
**Active Modules**: 5  
**Average Semantic Health**: 97.5%

---

## 📊 Executive Summary

This report provides a comprehensive overview of autonomy classifications across all MachineNativeOps modules. The autonomy framework defines five levels (L1-L5) plus a Global Layer for cross-cutting concerns.

### Key Metrics

| Metric | Value |
|--------|-------|
| Total Modules | 6 |
| Active Modules | 5 |
| In Development | 1 |
| Average Semantic Health | 97.5% |

### Autonomy Level Distribution

| Level | Count | Modules |
|-------|-------|---------|
| L1 | 0 | - |
| L2 | 0 | - |
| L3 | 0 | - |
| L4 | 0 | - |
| L5 | 0 | - |
| Global Layer | 1 | 06-security |

---

## 📋 Module Details

### 01-core: Core Infrastructure

| Attribute | Value |
|-----------|-------|
| Current Level | **L1-L2** |
| Expected Range | L1 - L2 |
| Compliance | ⚠️ Below Expected |
| Semantic Health | 100% |
| Status | 🟢 active |
| Dependencies | None |

### 02-intelligence: Intelligence Layer

| Attribute | Value |
|-----------|-------|
| Current Level | **L2-L3** |
| Expected Range | L2 - L3 |
| Compliance | ⚠️ Below Expected |
| Semantic Health | 100% |
| Status | 🟢 active |
| Dependencies | 01-core |

### 03-governance: Governance Framework

| Attribute | Value |
|-----------|-------|
| Current Level | **L3-L4** |
| Expected Range | L3 - L4 |
| Compliance | ⚠️ Below Expected |
| Semantic Health | 100% |
| Status | 🟢 active |
| Dependencies | 01-core, 02-intelligence |

### 04-autonomous: Autonomous Operations

| Attribute | Value |
|-----------|-------|
| Current Level | **L4-L5** |
| Expected Range | L4 - L5 |
| Compliance | ⚠️ Below Expected |
| Semantic Health | 85% |
| Status | 🟡 in-development |
| Dependencies | 01-core, 02-intelligence, 03-governance |

### 05-observability: Observability Platform

| Attribute | Value |
|-----------|-------|
| Current Level | **L4-L5** |
| Expected Range | L4 - L5 |
| Compliance | ⚠️ Below Expected |
| Semantic Health | 100% |
| Status | 🟢 active |
| Dependencies | 01-core, 02-intelligence, 03-governance |

### 06-security: Security & Compliance

| Attribute | Value |
|-----------|-------|
| Current Level | **Global Layer** |
| Expected Range | Global Layer - Global Layer |
| Compliance | ✅ Within Range |
| Semantic Health | 100% |
| Status | 🟢 active |
| Dependencies | 01-core, 03-governance, 05-observability |

---

## 🎯 Recommendations

### Priority Actions

3. **Upgrade 01-core Autonomy**: Current level (L1-L2) is below expected minimum (L1). Implement required capabilities for level progression.

3. **Upgrade 02-intelligence Autonomy**: Current level (L2-L3) is below expected minimum (L2). Implement required capabilities for level progression.

3. **Upgrade 03-governance Autonomy**: Current level (L3-L4) is below expected minimum (L3). Implement required capabilities for level progression.

1. **Complete 04-autonomous**: Module is in development status. Prioritize completion to enable full autonomy assessment.

2. **Improve 04-autonomous Semantic Health**: Current score (85%) is below target (90%). Review semantic mappings and namespace consistency.

### Long-term Goals

1. **Achieve L5 for 04-autonomous**: Enable full autonomous operations
2. **Maintain 95%+ Semantic Health**: Across all modules
3. **Zero Circular Dependencies**: Maintain clean dependency graph
4. **100% Policy Compliance**: All modules pass policy gates

---

## 📈 Progression Tracking

### Target State (6 months)

| Module | Current | Target | Gap |
|--------|---------|--------|-----|
| 01-core | L1-L2 | L2 | +2 levels |
| 02-intelligence | L2-L3 | L3 | +3 levels |
| 03-governance | L3-L4 | L4 | +4 levels |
| 04-autonomous | L4-L5 | L5 | +5 levels |
| 05-observability | L4-L5 | L5 | +5 levels |
| 06-security | Global Layer | Global Layer | ✅ At target |

---

## 📁 Classification Reports

Individual classification reports are available in `docs/autonomy/reports/`:

- [01-core-classification.md](reports/01-core-classification.md) - ✅ Available
- [02-intelligence-classification.md](reports/02-intelligence-classification.md) - ✅ Available
- [03-governance-classification.md](reports/03-governance-classification.md) - ✅ Available
- [04-autonomous-classification.md](reports/04-autonomous-classification.md) - ✅ Available
- [05-observability-classification.md](reports/05-observability-classification.md) - ✅ Available
- [06-security-classification.md](reports/06-security-classification.md) - ✅ Available

---

## 🔗 Related Documentation

- [Autonomy Classification Framework](../AUTONOMY_CLASSIFICATION_FRAMEWORK.md)
- [Language Governance Dashboard](../LANGUAGE_GOVERNANCE_DASHBOARD.md)
- [DAG Visualization](../dag-visualization/DAG_VISUALIZATION.md)
- [Documentation Portal](../DOCUMENTATION_PORTAL.md)

---

*This report is automatically generated. Last update: 2026-01-18 10:55 UTC*
