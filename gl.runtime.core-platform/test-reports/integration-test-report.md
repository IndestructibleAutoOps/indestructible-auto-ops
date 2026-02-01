# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: integration-test-report
# @GL-charter-version: 4.0.0
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

# Integration Test Report

**Generated:** 2026-01-29T05:06:42.112Z
**Version:** 21.0.0

## Summary

| Metric | Value |
|--------|-------|
| Total Suites | 4 |
| Total Tests | 12 |
| Passed | 10 |
| Failed | 2 |
| Skipped | 0 |
| Pass Rate | 83.3% |
| Duration | 3ms |
| Status | ⚠️ PARTIAL |

**Integration Tests: 10/12 passed (83.3%) in 3ms**

## Test Suites

### V19 Fabric ↔ Code Intelligence Layer

| Metric | Value |
|--------|-------|
| Tests | 3 |
| Passed | 2 |
| Failed | 1 |
| Duration | 1ms |
| Status | ⚠️ |

#### Test Details

- ✅ **1.1 Verify Fabric Continuum Integration file exists** (1ms)
- ❌ **1.2 Verify integration exports required classes** (0ms)
  - Error: Missing export: CapabilitySchemaRegistry
- ✅ **1.3 Verify Fabric Continuum Integration types** (0ms)

### V20 Continuum ↔ Code Intelligence Layer

| Metric | Value |
|--------|-------|
| Tests | 3 |
| Passed | 2 |
| Failed | 1 |
| Duration | 0ms |
| Status | ⚠️ |

#### Test Details

- ✅ **2.1 Verify Infinite Continuum module structure** (0ms)
- ❌ **2.2 Verify Continuum exports all required systems** (0ms)
  - Error: Missing export: KnowledgeAccretionSystem
- ✅ **2.3 Verify Continuum integration in Fabric Continuum file** (0ms)

### Pipeline ↔ Connector Integration

| Metric | Value |
|--------|-------|
| Tests | 3 |
| Passed | 3 |
| Failed | 0 |
| Duration | 0ms |
| Status | ✅ |

#### Test Details

- ✅ **3.1 Verify Git Connector exists and exports** (0ms)
- ✅ **3.2 Verify Infinite Continuum Server exists** (0ms)
- ✅ **3.3 Verify Server imports Infinite Continuum** (0ms)

### End-to-End Workflows

| Metric | Value |
|--------|-------|
| Tests | 3 |
| Passed | 3 |
| Failed | 0 |
| Duration | 0ms |
| Status | ✅ |

#### Test Details

- ✅ **4.1 Verify Capability Generation flow components** (0ms)
- ✅ **4.2 Verify Pattern Matching flow components** (0ms)
- ✅ **4.3 Verify Deployment Weaver flow components** (0ms)

