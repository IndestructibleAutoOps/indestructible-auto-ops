# Evidence Verification Logic Report

**Test Run ID**: d2009cc1-3932-486e-8d8c-aebfaa4c4f8b
**Timestamp**: 2026-02-04T23:39:41.896642

## Summary

- **Total Tests**: 7
- **Passed**: 2
- **Failed**: 4
- **Skipped**: 0
- **Overall Score**: 31.3/100

## Violations Summary

- **CRITICAL**: 840
- **HIGH**: 21
- **MEDIUM**: 0
- **LOW**: 0

## Test Results

### ✅ Fuzzy Language Detection (TC-1.1)

- **Status**: PASSED
- **Score**: 100.0/100

### ✅ Narrative Wrapper Detection (TC-1.2)

- **Status**: PASSED
- **Score**: 100.0/100

### ❌ Semantic Declaration Mismatch (TC-1.3)

- **Status**: FAILED
- **Score**: 0.0/100
- **Violations**: 10

**Violation Details**:
- **[HIGH]** Semantic declaration 'success' without corresponding event
  - Remediation: Add STEP_EXECUTED event for this artifact
- **[HIGH]** Semantic declaration 'success' without corresponding event
  - Remediation: Add STEP_EXECUTED event for this artifact
- **[HIGH]** Semantic declaration 'success' without corresponding event
  - Remediation: Add STEP_EXECUTED event for this artifact
- **[HIGH]** Semantic declaration 'success' without corresponding event
  - Remediation: Add STEP_EXECUTED event for this artifact
- **[HIGH]** Semantic declaration 'success' without corresponding event
  - Remediation: Add STEP_EXECUTED event for this artifact
- **[HIGH]** Semantic declaration 'success' without corresponding event
  - Remediation: Add STEP_EXECUTED event for this artifact
- **[HIGH]** Semantic declaration 'success' without corresponding event
  - Remediation: Add STEP_EXECUTED event for this artifact
- **[HIGH]** Semantic declaration 'success' without corresponding event
  - Remediation: Add STEP_EXECUTED event for this artifact
- **[HIGH]** Semantic declaration 'success' without corresponding event
  - Remediation: Add STEP_EXECUTED event for this artifact
- **[HIGH]** Semantic declaration 'success' without corresponding event
  - Remediation: Add STEP_EXECUTED event for this artifact

### ❌ Event Stream Completeness (TC-2.1)

- **Status**: FAILED
- **Score**: 0.0/100
- **Violations**: 461

**Violation Details**:
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload
- **[CRITICAL]** Event missing required fields
  - Remediation: Add missing fields: uuid, type, payload, canonical_hash

### ❌ Evidence Chain Verification (TC-2.2)

- **Status**: FAILED
- **Score**: 19.2/100
- **Violations**: 379

**Violation Details**:
- **[CRITICAL]** Artifact chain broken
  - Remediation: Fix hash_chain.parent field to point to previous artifact
- **[CRITICAL]** Artifact chain broken
  - Remediation: Fix hash_chain.parent field to point to previous artifact
- **[CRITICAL]** Artifact chain broken
  - Remediation: Fix hash_chain.parent field to point to previous artifact
- **[CRITICAL]** Artifact chain broken
  - Remediation: Fix hash_chain.parent field to point to previous artifact
- **[CRITICAL]** Artifact chain broken
  - Remediation: Fix hash_chain.parent field to point to previous artifact
- **[CRITICAL]** Artifact chain broken
  - Remediation: Fix hash_chain.parent field to point to previous artifact
- **[CRITICAL]** Artifact chain broken
  - Remediation: Fix hash_chain.parent field to point to previous artifact
- **[CRITICAL]** Artifact chain broken
  - Remediation: Fix hash_chain.parent field to point to previous artifact
- **[CRITICAL]** Artifact chain broken
  - Remediation: Fix hash_chain.parent field to point to previous artifact
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Event chain broken
  - Remediation: Fix hash_chain.previous_event field to point to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Event chain broken
  - Remediation: Fix hash_chain.previous_event field to point to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Event chain broken
  - Remediation: Fix hash_chain.previous_event field to point to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Event chain broken
  - Remediation: Fix hash_chain.previous_event field to point to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Event chain broken
  - Remediation: Fix hash_chain.previous_event field to point to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Event chain broken
  - Remediation: Fix hash_chain.previous_event field to point to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Event chain broken
  - Remediation: Fix hash_chain.previous_event field to point to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Event chain broken
  - Remediation: Fix hash_chain.previous_event field to point to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Event chain broken
  - Remediation: Fix hash_chain.previous_event field to point to previous event
- **[CRITICAL]** Previous event missing canonical_hash
  - Remediation: Add canonical_hash field to previous event
- **[CRITICAL]** Event chain broken
  - Remediation: Fix hash_chain.previous_event field to point to previous event

### ❌ Canonicalization Reproducibility (TC-3.1)

- **Status**: ERROR
- **Score**: 0.0/100
- **Violations**: 1

**Violation Details**:
- **[HIGH]** RFC8785 canonicalization not available
  - Remediation: Install rfc8785 package: pip install rfc8785

### ❌ Pipeline Replayability (TC-5.1)

- **Status**: FAILED
- **Score**: 0.0/100
- **Violations**: 10

**Violation Details**:
- **[HIGH]** Artifact missing generation metadata
  - Remediation: Add metadata.generated_by field to artifact
- **[HIGH]** Artifact missing generation metadata
  - Remediation: Add metadata.generated_by field to artifact
- **[HIGH]** Artifact missing generation metadata
  - Remediation: Add metadata.generated_by field to artifact
- **[HIGH]** Artifact missing generation metadata
  - Remediation: Add metadata.generated_by field to artifact
- **[HIGH]** Artifact missing generation metadata
  - Remediation: Add metadata.generated_by field to artifact
- **[HIGH]** Artifact missing generation metadata
  - Remediation: Add metadata.generated_by field to artifact
- **[HIGH]** Artifact missing generation metadata
  - Remediation: Add metadata.generated_by field to artifact
- **[HIGH]** Artifact missing generation metadata
  - Remediation: Add metadata.generated_by field to artifact
- **[HIGH]** Artifact missing generation metadata
  - Remediation: Add metadata.generated_by field to artifact
- **[HIGH]** Artifact missing generation metadata
  - Remediation: Add metadata.generated_by field to artifact

## Detailed Violations

### 1. Semantic declaration 'success' without corresponding event

- **Test ID**: TC-1.3
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "c771a453-1599-4459-870e-c26553eae425"
}
- **Affected Artifacts**: c771a453-1599-4459-870e-c26553eae425
- **Remediation**: Add STEP_EXECUTED event for this artifact

### 2. Semantic declaration 'success' without corresponding event

- **Test ID**: TC-1.3
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "c8b94f8d-3a07-438f-ad3a-cc0e986b9838"
}
- **Affected Artifacts**: c8b94f8d-3a07-438f-ad3a-cc0e986b9838
- **Remediation**: Add STEP_EXECUTED event for this artifact

### 3. Semantic declaration 'success' without corresponding event

- **Test ID**: TC-1.3
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "5c46eb1d-27f5-431d-9938-20e7b0049e31"
}
- **Affected Artifacts**: 5c46eb1d-27f5-431d-9938-20e7b0049e31
- **Remediation**: Add STEP_EXECUTED event for this artifact

### 4. Semantic declaration 'success' without corresponding event

- **Test ID**: TC-1.3
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "a4dc84a4-494d-496a-b315-b352dcca4620"
}
- **Affected Artifacts**: a4dc84a4-494d-496a-b315-b352dcca4620
- **Remediation**: Add STEP_EXECUTED event for this artifact

### 5. Semantic declaration 'success' without corresponding event

- **Test ID**: TC-1.3
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "2633a6c9-9a34-43ae-8d50-248941f1b297"
}
- **Affected Artifacts**: 2633a6c9-9a34-43ae-8d50-248941f1b297
- **Remediation**: Add STEP_EXECUTED event for this artifact

### 6. Semantic declaration 'success' without corresponding event

- **Test ID**: TC-1.3
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "0bf27f5b-e6aa-4084-a558-cf71d67b5f0b"
}
- **Affected Artifacts**: 0bf27f5b-e6aa-4084-a558-cf71d67b5f0b
- **Remediation**: Add STEP_EXECUTED event for this artifact

### 7. Semantic declaration 'success' without corresponding event

- **Test ID**: TC-1.3
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "596cce6b-d567-4027-a828-d9f919fd49c9"
}
- **Affected Artifacts**: 596cce6b-d567-4027-a828-d9f919fd49c9
- **Remediation**: Add STEP_EXECUTED event for this artifact

### 8. Semantic declaration 'success' without corresponding event

- **Test ID**: TC-1.3
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "4131ace7-f74a-4e7a-9eb4-a220dd5f7af2"
}
- **Affected Artifacts**: 4131ace7-f74a-4e7a-9eb4-a220dd5f7af2
- **Remediation**: Add STEP_EXECUTED event for this artifact

### 9. Semantic declaration 'success' without corresponding event

- **Test ID**: TC-1.3
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "1bcf919c-f1bd-4079-9a56-5c106cd8ce8a"
}
- **Affected Artifacts**: 1bcf919c-f1bd-4079-9a56-5c106cd8ce8a
- **Remediation**: Add STEP_EXECUTED event for this artifact

### 10. Semantic declaration 'success' without corresponding event

- **Test ID**: TC-1.3
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "98c852ee-0812-4f2a-bd2c-59ecd946fb32"
}
- **Affected Artifacts**: 98c852ee-0812-4f2a-bd2c-59ecd946fb32
- **Remediation**: Add STEP_EXECUTED event for this artifact

### 11. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 0,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 12. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 1,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 13. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 2,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 14. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 3,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 15. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 4,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 16. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 5,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 17. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 6,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 18. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 7,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 19. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 8,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 20. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 9,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 21. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 10,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 22. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 11,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 23. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 12,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 24. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 13,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 25. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 14,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 26. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 15,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 27. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 16,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 28. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 17,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 29. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 18,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 30. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 19,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 31. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 20,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 32. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 21,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 33. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 22,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 34. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 23,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 35. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 24,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 36. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 25,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 37. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 26,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 38. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 27,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 39. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 28,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 40. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 29,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 41. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 30,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 42. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 31,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 43. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 32,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 44. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 33,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 45. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 34,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 46. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 35,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 47. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 36,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 48. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 37,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 49. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 38,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 50. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 39,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 51. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 40,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 52. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 41,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 53. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 42,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 54. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 43,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 55. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 44,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 56. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 45,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 57. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 46,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 58. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 47,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 59. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 48,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 60. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 49,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 61. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 50,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 62. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 51,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 63. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 52,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 64. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 53,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 65. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 54,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 66. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 55,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 67. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 56,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 68. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 57,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 69. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 58,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 70. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 59,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 71. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 60,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 72. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 61,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 73. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 62,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 74. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 63,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 75. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 64,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 76. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 65,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 77. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 66,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 78. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 67,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 79. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 68,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 80. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 69,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 81. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 70,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 82. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 71,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 83. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 72,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 84. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 73,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 85. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 74,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 86. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 75,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 87. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 76,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 88. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 77,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 89. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 78,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 90. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 79,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 91. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 80,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 92. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 81,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 93. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 82,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 94. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 83,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 95. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 84,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 96. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 85,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 97. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 86,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 98. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 87,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 99. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 88,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 100. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 89,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 101. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 90,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 102. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 91,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 103. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 92,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 104. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 93,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 105. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 94,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 106. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 95,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 107. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 96,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 108. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 97,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 109. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 98,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 110. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 99,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 111. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 100,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 112. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 101,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 113. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 102,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 114. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 103,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 115. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 104,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 116. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 105,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 117. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 106,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 118. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 107,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 119. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 108,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 120. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 109,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 121. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 110,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 122. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 111,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 123. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 112,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 124. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 113,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 125. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 114,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 126. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 115,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 127. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 116,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 128. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 117,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 129. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 118,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 130. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 119,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 131. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 120,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 132. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 121,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 133. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 122,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 134. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 123,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 135. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 124,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 136. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 125,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 137. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 126,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 138. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 127,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 139. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 128,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 140. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 129,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 141. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 130,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 142. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 131,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 143. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 132,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 144. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 133,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 145. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 134,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 146. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 135,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 147. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 136,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 148. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 137,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 149. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 138,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 150. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 139,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 151. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 140,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 152. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 141,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 153. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 142,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 154. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 143,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 155. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 144,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 156. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 145,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 157. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 146,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 158. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 147,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 159. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 148,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 160. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 149,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 161. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 150,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 162. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 151,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 163. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 152,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 164. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 153,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 165. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 154,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 166. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 155,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 167. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 156,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 168. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 157,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 169. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 158,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 170. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 159,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 171. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 160,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 172. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 161,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 173. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 162,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 174. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 163,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 175. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 164,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 176. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 165,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 177. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 166,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 178. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 167,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 179. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 168,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 180. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 169,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 181. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 170,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 182. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 171,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 183. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 172,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 184. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 173,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 185. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 174,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 186. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 175,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 187. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 176,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 188. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 177,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 189. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 178,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 190. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 179,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 191. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 180,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 192. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 181,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 193. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 182,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 194. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 183,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 195. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 184,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 196. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 185,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 197. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 186,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 198. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 187,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 199. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 188,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 200. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 189,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 201. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 190,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 202. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 191,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 203. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 192,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 204. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 193,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 205. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 194,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 206. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 195,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 207. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 196,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 208. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 197,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 209. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 198,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 210. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 199,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 211. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 200,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 212. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 201,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 213. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 202,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 214. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 203,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 215. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 204,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 216. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 205,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 217. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 206,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 218. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 207,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 219. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 208,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 220. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 209,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 221. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 210,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 222. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 211,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 223. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 212,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 224. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 213,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 225. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 214,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 226. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 215,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 227. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 216,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 228. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 217,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 229. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 218,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 230. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 219,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 231. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 220,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 232. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 221,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 233. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 222,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 234. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 223,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 235. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 224,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 236. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 225,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 237. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 226,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 238. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 227,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 239. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 228,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 240. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 229,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 241. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 230,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 242. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 231,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 243. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 232,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 244. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 233,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 245. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 234,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 246. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 235,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 247. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 236,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 248. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 237,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 249. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 238,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 250. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 239,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 251. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 240,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 252. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 241,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 253. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 242,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 254. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 243,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 255. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 244,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 256. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 245,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 257. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 246,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 258. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 247,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 259. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 248,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 260. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 249,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 261. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 250,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 262. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 251,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 263. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 252,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 264. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 253,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 265. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 254,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 266. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 255,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 267. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 256,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 268. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 257,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 269. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 258,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 270. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 259,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 271. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 260,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 272. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 261,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 273. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 262,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 274. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 263,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 275. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 264,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 276. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 265,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 277. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 266,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 278. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 267,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 279. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 268,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 280. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 269,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 281. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 270,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 282. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 271,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 283. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 272,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 284. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 273,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 285. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 274,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 286. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 275,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 287. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 276,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 288. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 277,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 289. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 278,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 290. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 279,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 291. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 280,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 292. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 281,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 293. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 282,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 294. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 283,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 295. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 284,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 296. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 285,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 297. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 286,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 298. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 287,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 299. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 288,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 300. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 289,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 301. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 290,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 302. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 291,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 303. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 292,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 304. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 293,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 305. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 294,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 306. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 295,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 307. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 296,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 308. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 297,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 309. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 298,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 310. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 299,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 311. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 300,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 312. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 301,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 313. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 302,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 314. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 303,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 315. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 304,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 316. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 305,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 317. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 306,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 318. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 307,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 319. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 308,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 320. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 309,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 321. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 310,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 322. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 311,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 323. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 312,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 324. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 313,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 325. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 314,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 326. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 315,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 327. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 316,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 328. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 317,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 329. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 318,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 330. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 319,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 331. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 320,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 332. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 321,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 333. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 322,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 334. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 323,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 335. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 324,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 336. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 325,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 337. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 326,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 338. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 327,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 339. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 328,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 340. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 329,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 341. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 330,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 342. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 331,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 343. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 332,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 344. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 333,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 345. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 334,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 346. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 335,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 347. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 336,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 348. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 337,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 349. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 338,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 350. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 339,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 351. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 340,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 352. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 341,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 353. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 342,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 354. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 343,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 355. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 344,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 356. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 345,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 357. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 346,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 358. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 347,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 359. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 348,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 360. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 349,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 361. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 350,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 362. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 351,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 363. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 352,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 364. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 353,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 365. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 354,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 366. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 355,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 367. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 356,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 368. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 357,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 369. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 358,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 370. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 359,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 371. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 360,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 372. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 361,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 373. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 362,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 374. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 363,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 375. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 364,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 376. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 365,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 377. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 366,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 378. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 367,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 379. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 368,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 380. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 369,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 381. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 370,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 382. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 371,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 383. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 372,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 384. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 373,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 385. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 374,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 386. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 375,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 387. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 376,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 388. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 377,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 389. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 378,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 390. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 379,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 391. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 380,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 392. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 381,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 393. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 382,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 394. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 383,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 395. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 384,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 396. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 385,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 397. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 386,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 398. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 387,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 399. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 388,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 400. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 389,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 401. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 390,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 402. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 391,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 403. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 392,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 404. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 393,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 405. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 394,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 406. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 395,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 407. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 396,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 408. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 397,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 409. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 398,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 410. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 399,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 411. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 400,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 412. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 401,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 413. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 402,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 414. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 403,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 415. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 404,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 416. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 405,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 417. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 406,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 418. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 407,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 419. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 408,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 420. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 409,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 421. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 410,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 422. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 411,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 423. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 412,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 424. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 413,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 425. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 414,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 426. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 415,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 427. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 416,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 428. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 417,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 429. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 418,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 430. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 419,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 431. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 420,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 432. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 421,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 433. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 422,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 434. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 423,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 435. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 424,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 436. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 425,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 437. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 426,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 438. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 427,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 439. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 428,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 440. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 429,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 441. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 430,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 442. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 431,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 443. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 432,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 444. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 433,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 445. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 434,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 446. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 435,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 447. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 436,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 448. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 437,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 449. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 438,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 450. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 439,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 451. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 440,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 452. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 441,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 453. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 442,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 454. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 443,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 455. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 444,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 456. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 445,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 457. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 446,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 458. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 447,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 459. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 448,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 460. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 449,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 461. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 450,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 462. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 451,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 463. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 452,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 464. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 453,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 465. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 454,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 466. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 455,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 467. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 456,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 468. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 457,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 469. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 458,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 470. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 459,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload

### 471. Event missing required fields

- **Test ID**: TC-2.1
- **Severity**: CRITICAL
- **Evidence**: {
  "event_index": 460,
  "event_id": "UNKNOWN",
  "missing_fields": [
    "uuid",
    "type",
    "payload",
    "canonical_hash"
  ]
}
- **Remediation**: Add missing fields: uuid, type, payload, canonical_hash

### 472. Artifact chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "artifact_id": "c8b94f8d-3a07-438f-ad3a-cc0e986b9838",
  "expected_parent": "641be8127d8038326595c1791525b424ae9bd718c02ce6676da5b7133c36a9aa",
  "actual_parent": null
}
- **Affected Artifacts**: c8b94f8d-3a07-438f-ad3a-cc0e986b9838
- **Remediation**: Fix hash_chain.parent field to point to previous artifact

### 473. Artifact chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "artifact_id": "5c46eb1d-27f5-431d-9938-20e7b0049e31",
  "expected_parent": "e86ca5de3352e3d20b50f3fcb19e3ecf462323cbde45ccc25e96309a6cbb5dcf",
  "actual_parent": null
}
- **Affected Artifacts**: 5c46eb1d-27f5-431d-9938-20e7b0049e31
- **Remediation**: Fix hash_chain.parent field to point to previous artifact

### 474. Artifact chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "artifact_id": "a4dc84a4-494d-496a-b315-b352dcca4620",
  "expected_parent": "f8aad9c7011edd0b8579cdc62fb16581b49d2a86e64b4c50db39080883a0b2e6",
  "actual_parent": null
}
- **Affected Artifacts**: a4dc84a4-494d-496a-b315-b352dcca4620
- **Remediation**: Fix hash_chain.parent field to point to previous artifact

### 475. Artifact chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "artifact_id": "2633a6c9-9a34-43ae-8d50-248941f1b297",
  "expected_parent": "eaf6474b95fd485601e49d0a2c44510c2e7f0f3c02b01772013967698828b8ac",
  "actual_parent": null
}
- **Affected Artifacts**: 2633a6c9-9a34-43ae-8d50-248941f1b297
- **Remediation**: Fix hash_chain.parent field to point to previous artifact

### 476. Artifact chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "artifact_id": "0bf27f5b-e6aa-4084-a558-cf71d67b5f0b",
  "expected_parent": "2914a03bfe82050580a6b77b14d471494ad7c474bddf99b775ffa8edb6b2602e",
  "actual_parent": null
}
- **Affected Artifacts**: 0bf27f5b-e6aa-4084-a558-cf71d67b5f0b
- **Remediation**: Fix hash_chain.parent field to point to previous artifact

### 477. Artifact chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "artifact_id": "596cce6b-d567-4027-a828-d9f919fd49c9",
  "expected_parent": "4be5f7e464079168b5efcf0c4dacb46e63bc9c63ef0487c7c4e0ba0634a55194",
  "actual_parent": null
}
- **Affected Artifacts**: 596cce6b-d567-4027-a828-d9f919fd49c9
- **Remediation**: Fix hash_chain.parent field to point to previous artifact

### 478. Artifact chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "artifact_id": "4131ace7-f74a-4e7a-9eb4-a220dd5f7af2",
  "expected_parent": "03b38766d9d64361c34b6f478acdce7585fc82cce9822826f3961ddb00254e09",
  "actual_parent": null
}
- **Affected Artifacts**: 4131ace7-f74a-4e7a-9eb4-a220dd5f7af2
- **Remediation**: Fix hash_chain.parent field to point to previous artifact

### 479. Artifact chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "artifact_id": "1bcf919c-f1bd-4079-9a56-5c106cd8ce8a",
  "expected_parent": "00d21dd113a1cdf30da5158452fdfccb14c56b2f435c85ec7b503937253edfd1",
  "actual_parent": null
}
- **Affected Artifacts**: 1bcf919c-f1bd-4079-9a56-5c106cd8ce8a
- **Remediation**: Fix hash_chain.parent field to point to previous artifact

### 480. Artifact chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "artifact_id": "98c852ee-0812-4f2a-bd2c-59ecd946fb32",
  "expected_parent": "fed97d9ed5bdac429de4716fb61ac2f66a032695b042c847195857cf1c96c682",
  "actual_parent": null
}
- **Affected Artifacts**: 98c852ee-0812-4f2a-bd2c-59ecd946fb32
- **Remediation**: Fix hash_chain.parent field to point to previous artifact

### 481. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 0
}
- **Remediation**: Add canonical_hash field to previous event

### 482. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 1
}
- **Remediation**: Add canonical_hash field to previous event

### 483. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 2
}
- **Remediation**: Add canonical_hash field to previous event

### 484. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 3
}
- **Remediation**: Add canonical_hash field to previous event

### 485. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 4
}
- **Remediation**: Add canonical_hash field to previous event

### 486. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 5
}
- **Remediation**: Add canonical_hash field to previous event

### 487. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 6
}
- **Remediation**: Add canonical_hash field to previous event

### 488. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 7
}
- **Remediation**: Add canonical_hash field to previous event

### 489. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 8
}
- **Remediation**: Add canonical_hash field to previous event

### 490. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 9
}
- **Remediation**: Add canonical_hash field to previous event

### 491. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 10
}
- **Remediation**: Add canonical_hash field to previous event

### 492. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 11
}
- **Remediation**: Add canonical_hash field to previous event

### 493. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 12
}
- **Remediation**: Add canonical_hash field to previous event

### 494. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 13
}
- **Remediation**: Add canonical_hash field to previous event

### 495. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 14
}
- **Remediation**: Add canonical_hash field to previous event

### 496. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 15
}
- **Remediation**: Add canonical_hash field to previous event

### 497. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 16
}
- **Remediation**: Add canonical_hash field to previous event

### 498. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 17
}
- **Remediation**: Add canonical_hash field to previous event

### 499. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 18
}
- **Remediation**: Add canonical_hash field to previous event

### 500. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 19
}
- **Remediation**: Add canonical_hash field to previous event

### 501. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 20
}
- **Remediation**: Add canonical_hash field to previous event

### 502. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 21
}
- **Remediation**: Add canonical_hash field to previous event

### 503. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 22
}
- **Remediation**: Add canonical_hash field to previous event

### 504. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 23
}
- **Remediation**: Add canonical_hash field to previous event

### 505. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 24
}
- **Remediation**: Add canonical_hash field to previous event

### 506. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 25
}
- **Remediation**: Add canonical_hash field to previous event

### 507. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 26
}
- **Remediation**: Add canonical_hash field to previous event

### 508. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 27
}
- **Remediation**: Add canonical_hash field to previous event

### 509. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 28
}
- **Remediation**: Add canonical_hash field to previous event

### 510. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 29
}
- **Remediation**: Add canonical_hash field to previous event

### 511. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 30
}
- **Remediation**: Add canonical_hash field to previous event

### 512. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 31
}
- **Remediation**: Add canonical_hash field to previous event

### 513. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 32
}
- **Remediation**: Add canonical_hash field to previous event

### 514. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 33
}
- **Remediation**: Add canonical_hash field to previous event

### 515. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 34
}
- **Remediation**: Add canonical_hash field to previous event

### 516. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 35
}
- **Remediation**: Add canonical_hash field to previous event

### 517. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 36
}
- **Remediation**: Add canonical_hash field to previous event

### 518. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 37
}
- **Remediation**: Add canonical_hash field to previous event

### 519. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 38
}
- **Remediation**: Add canonical_hash field to previous event

### 520. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 39
}
- **Remediation**: Add canonical_hash field to previous event

### 521. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 40
}
- **Remediation**: Add canonical_hash field to previous event

### 522. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 41
}
- **Remediation**: Add canonical_hash field to previous event

### 523. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 42
}
- **Remediation**: Add canonical_hash field to previous event

### 524. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 43
}
- **Remediation**: Add canonical_hash field to previous event

### 525. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 44
}
- **Remediation**: Add canonical_hash field to previous event

### 526. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 45
}
- **Remediation**: Add canonical_hash field to previous event

### 527. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 46
}
- **Remediation**: Add canonical_hash field to previous event

### 528. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 47
}
- **Remediation**: Add canonical_hash field to previous event

### 529. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 48
}
- **Remediation**: Add canonical_hash field to previous event

### 530. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 49
}
- **Remediation**: Add canonical_hash field to previous event

### 531. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 50
}
- **Remediation**: Add canonical_hash field to previous event

### 532. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 51
}
- **Remediation**: Add canonical_hash field to previous event

### 533. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 52
}
- **Remediation**: Add canonical_hash field to previous event

### 534. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 53
}
- **Remediation**: Add canonical_hash field to previous event

### 535. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 54
}
- **Remediation**: Add canonical_hash field to previous event

### 536. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 55
}
- **Remediation**: Add canonical_hash field to previous event

### 537. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 56
}
- **Remediation**: Add canonical_hash field to previous event

### 538. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 57
}
- **Remediation**: Add canonical_hash field to previous event

### 539. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 58
}
- **Remediation**: Add canonical_hash field to previous event

### 540. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 59
}
- **Remediation**: Add canonical_hash field to previous event

### 541. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 60
}
- **Remediation**: Add canonical_hash field to previous event

### 542. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 61
}
- **Remediation**: Add canonical_hash field to previous event

### 543. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 62
}
- **Remediation**: Add canonical_hash field to previous event

### 544. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 63
}
- **Remediation**: Add canonical_hash field to previous event

### 545. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 64
}
- **Remediation**: Add canonical_hash field to previous event

### 546. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 65
}
- **Remediation**: Add canonical_hash field to previous event

### 547. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 66
}
- **Remediation**: Add canonical_hash field to previous event

### 548. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 67
}
- **Remediation**: Add canonical_hash field to previous event

### 549. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 68
}
- **Remediation**: Add canonical_hash field to previous event

### 550. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 69
}
- **Remediation**: Add canonical_hash field to previous event

### 551. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 70
}
- **Remediation**: Add canonical_hash field to previous event

### 552. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 71
}
- **Remediation**: Add canonical_hash field to previous event

### 553. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 72
}
- **Remediation**: Add canonical_hash field to previous event

### 554. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 73
}
- **Remediation**: Add canonical_hash field to previous event

### 555. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 74
}
- **Remediation**: Add canonical_hash field to previous event

### 556. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 75
}
- **Remediation**: Add canonical_hash field to previous event

### 557. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 76
}
- **Remediation**: Add canonical_hash field to previous event

### 558. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 77
}
- **Remediation**: Add canonical_hash field to previous event

### 559. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 78
}
- **Remediation**: Add canonical_hash field to previous event

### 560. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 79
}
- **Remediation**: Add canonical_hash field to previous event

### 561. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 80
}
- **Remediation**: Add canonical_hash field to previous event

### 562. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 81
}
- **Remediation**: Add canonical_hash field to previous event

### 563. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 82
}
- **Remediation**: Add canonical_hash field to previous event

### 564. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 83
}
- **Remediation**: Add canonical_hash field to previous event

### 565. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 84
}
- **Remediation**: Add canonical_hash field to previous event

### 566. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 85
}
- **Remediation**: Add canonical_hash field to previous event

### 567. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 86
}
- **Remediation**: Add canonical_hash field to previous event

### 568. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 87
}
- **Remediation**: Add canonical_hash field to previous event

### 569. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 88
}
- **Remediation**: Add canonical_hash field to previous event

### 570. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 89
}
- **Remediation**: Add canonical_hash field to previous event

### 571. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 90
}
- **Remediation**: Add canonical_hash field to previous event

### 572. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 91
}
- **Remediation**: Add canonical_hash field to previous event

### 573. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 92
}
- **Remediation**: Add canonical_hash field to previous event

### 574. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 93
}
- **Remediation**: Add canonical_hash field to previous event

### 575. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 94
}
- **Remediation**: Add canonical_hash field to previous event

### 576. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 95
}
- **Remediation**: Add canonical_hash field to previous event

### 577. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 96
}
- **Remediation**: Add canonical_hash field to previous event

### 578. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 97
}
- **Remediation**: Add canonical_hash field to previous event

### 579. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 98
}
- **Remediation**: Add canonical_hash field to previous event

### 580. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 99
}
- **Remediation**: Add canonical_hash field to previous event

### 581. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 100
}
- **Remediation**: Add canonical_hash field to previous event

### 582. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 101
}
- **Remediation**: Add canonical_hash field to previous event

### 583. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 102
}
- **Remediation**: Add canonical_hash field to previous event

### 584. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 103
}
- **Remediation**: Add canonical_hash field to previous event

### 585. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 104
}
- **Remediation**: Add canonical_hash field to previous event

### 586. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 105
}
- **Remediation**: Add canonical_hash field to previous event

### 587. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 106
}
- **Remediation**: Add canonical_hash field to previous event

### 588. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 107
}
- **Remediation**: Add canonical_hash field to previous event

### 589. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 108
}
- **Remediation**: Add canonical_hash field to previous event

### 590. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 109
}
- **Remediation**: Add canonical_hash field to previous event

### 591. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 110
}
- **Remediation**: Add canonical_hash field to previous event

### 592. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 111
}
- **Remediation**: Add canonical_hash field to previous event

### 593. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 112
}
- **Remediation**: Add canonical_hash field to previous event

### 594. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 113
}
- **Remediation**: Add canonical_hash field to previous event

### 595. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 114
}
- **Remediation**: Add canonical_hash field to previous event

### 596. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 115
}
- **Remediation**: Add canonical_hash field to previous event

### 597. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 116
}
- **Remediation**: Add canonical_hash field to previous event

### 598. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 117
}
- **Remediation**: Add canonical_hash field to previous event

### 599. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 118
}
- **Remediation**: Add canonical_hash field to previous event

### 600. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 119
}
- **Remediation**: Add canonical_hash field to previous event

### 601. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 120
}
- **Remediation**: Add canonical_hash field to previous event

### 602. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 121
}
- **Remediation**: Add canonical_hash field to previous event

### 603. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 122
}
- **Remediation**: Add canonical_hash field to previous event

### 604. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 123
}
- **Remediation**: Add canonical_hash field to previous event

### 605. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 124
}
- **Remediation**: Add canonical_hash field to previous event

### 606. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 125
}
- **Remediation**: Add canonical_hash field to previous event

### 607. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 126
}
- **Remediation**: Add canonical_hash field to previous event

### 608. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 127
}
- **Remediation**: Add canonical_hash field to previous event

### 609. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 128
}
- **Remediation**: Add canonical_hash field to previous event

### 610. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 129
}
- **Remediation**: Add canonical_hash field to previous event

### 611. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 130
}
- **Remediation**: Add canonical_hash field to previous event

### 612. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 131
}
- **Remediation**: Add canonical_hash field to previous event

### 613. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 132
}
- **Remediation**: Add canonical_hash field to previous event

### 614. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 133
}
- **Remediation**: Add canonical_hash field to previous event

### 615. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 134
}
- **Remediation**: Add canonical_hash field to previous event

### 616. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 135
}
- **Remediation**: Add canonical_hash field to previous event

### 617. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 136
}
- **Remediation**: Add canonical_hash field to previous event

### 618. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 137
}
- **Remediation**: Add canonical_hash field to previous event

### 619. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 138
}
- **Remediation**: Add canonical_hash field to previous event

### 620. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 139
}
- **Remediation**: Add canonical_hash field to previous event

### 621. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 140
}
- **Remediation**: Add canonical_hash field to previous event

### 622. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 141
}
- **Remediation**: Add canonical_hash field to previous event

### 623. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 142
}
- **Remediation**: Add canonical_hash field to previous event

### 624. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 143
}
- **Remediation**: Add canonical_hash field to previous event

### 625. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 144
}
- **Remediation**: Add canonical_hash field to previous event

### 626. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 145
}
- **Remediation**: Add canonical_hash field to previous event

### 627. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 146
}
- **Remediation**: Add canonical_hash field to previous event

### 628. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 147
}
- **Remediation**: Add canonical_hash field to previous event

### 629. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 148
}
- **Remediation**: Add canonical_hash field to previous event

### 630. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 149
}
- **Remediation**: Add canonical_hash field to previous event

### 631. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 150
}
- **Remediation**: Add canonical_hash field to previous event

### 632. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 151
}
- **Remediation**: Add canonical_hash field to previous event

### 633. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 152
}
- **Remediation**: Add canonical_hash field to previous event

### 634. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 153
}
- **Remediation**: Add canonical_hash field to previous event

### 635. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 154
}
- **Remediation**: Add canonical_hash field to previous event

### 636. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 155
}
- **Remediation**: Add canonical_hash field to previous event

### 637. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 156
}
- **Remediation**: Add canonical_hash field to previous event

### 638. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 157
}
- **Remediation**: Add canonical_hash field to previous event

### 639. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 158
}
- **Remediation**: Add canonical_hash field to previous event

### 640. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 159
}
- **Remediation**: Add canonical_hash field to previous event

### 641. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 160
}
- **Remediation**: Add canonical_hash field to previous event

### 642. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 161
}
- **Remediation**: Add canonical_hash field to previous event

### 643. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 162
}
- **Remediation**: Add canonical_hash field to previous event

### 644. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 163
}
- **Remediation**: Add canonical_hash field to previous event

### 645. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 164
}
- **Remediation**: Add canonical_hash field to previous event

### 646. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 165
}
- **Remediation**: Add canonical_hash field to previous event

### 647. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 166
}
- **Remediation**: Add canonical_hash field to previous event

### 648. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 167
}
- **Remediation**: Add canonical_hash field to previous event

### 649. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 168
}
- **Remediation**: Add canonical_hash field to previous event

### 650. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 169
}
- **Remediation**: Add canonical_hash field to previous event

### 651. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 170
}
- **Remediation**: Add canonical_hash field to previous event

### 652. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 171
}
- **Remediation**: Add canonical_hash field to previous event

### 653. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 172
}
- **Remediation**: Add canonical_hash field to previous event

### 654. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 173
}
- **Remediation**: Add canonical_hash field to previous event

### 655. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 174
}
- **Remediation**: Add canonical_hash field to previous event

### 656. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 175
}
- **Remediation**: Add canonical_hash field to previous event

### 657. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 176
}
- **Remediation**: Add canonical_hash field to previous event

### 658. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 177
}
- **Remediation**: Add canonical_hash field to previous event

### 659. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 178
}
- **Remediation**: Add canonical_hash field to previous event

### 660. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 179
}
- **Remediation**: Add canonical_hash field to previous event

### 661. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 180
}
- **Remediation**: Add canonical_hash field to previous event

### 662. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 181
}
- **Remediation**: Add canonical_hash field to previous event

### 663. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 182
}
- **Remediation**: Add canonical_hash field to previous event

### 664. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 183
}
- **Remediation**: Add canonical_hash field to previous event

### 665. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 184
}
- **Remediation**: Add canonical_hash field to previous event

### 666. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 185
}
- **Remediation**: Add canonical_hash field to previous event

### 667. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 186
}
- **Remediation**: Add canonical_hash field to previous event

### 668. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 187
}
- **Remediation**: Add canonical_hash field to previous event

### 669. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 188
}
- **Remediation**: Add canonical_hash field to previous event

### 670. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 189
}
- **Remediation**: Add canonical_hash field to previous event

### 671. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 190
}
- **Remediation**: Add canonical_hash field to previous event

### 672. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 191
}
- **Remediation**: Add canonical_hash field to previous event

### 673. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 192
}
- **Remediation**: Add canonical_hash field to previous event

### 674. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 193
}
- **Remediation**: Add canonical_hash field to previous event

### 675. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 194
}
- **Remediation**: Add canonical_hash field to previous event

### 676. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 195
}
- **Remediation**: Add canonical_hash field to previous event

### 677. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 196
}
- **Remediation**: Add canonical_hash field to previous event

### 678. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 197
}
- **Remediation**: Add canonical_hash field to previous event

### 679. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 198
}
- **Remediation**: Add canonical_hash field to previous event

### 680. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 199
}
- **Remediation**: Add canonical_hash field to previous event

### 681. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 200
}
- **Remediation**: Add canonical_hash field to previous event

### 682. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 201
}
- **Remediation**: Add canonical_hash field to previous event

### 683. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 202
}
- **Remediation**: Add canonical_hash field to previous event

### 684. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 203
}
- **Remediation**: Add canonical_hash field to previous event

### 685. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 204
}
- **Remediation**: Add canonical_hash field to previous event

### 686. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 205
}
- **Remediation**: Add canonical_hash field to previous event

### 687. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 206
}
- **Remediation**: Add canonical_hash field to previous event

### 688. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 207
}
- **Remediation**: Add canonical_hash field to previous event

### 689. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 208
}
- **Remediation**: Add canonical_hash field to previous event

### 690. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 209
}
- **Remediation**: Add canonical_hash field to previous event

### 691. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 210
}
- **Remediation**: Add canonical_hash field to previous event

### 692. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 211
}
- **Remediation**: Add canonical_hash field to previous event

### 693. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 212
}
- **Remediation**: Add canonical_hash field to previous event

### 694. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 213
}
- **Remediation**: Add canonical_hash field to previous event

### 695. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 214
}
- **Remediation**: Add canonical_hash field to previous event

### 696. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 215
}
- **Remediation**: Add canonical_hash field to previous event

### 697. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 216
}
- **Remediation**: Add canonical_hash field to previous event

### 698. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 217
}
- **Remediation**: Add canonical_hash field to previous event

### 699. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 218
}
- **Remediation**: Add canonical_hash field to previous event

### 700. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 219
}
- **Remediation**: Add canonical_hash field to previous event

### 701. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 220
}
- **Remediation**: Add canonical_hash field to previous event

### 702. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 221
}
- **Remediation**: Add canonical_hash field to previous event

### 703. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 222
}
- **Remediation**: Add canonical_hash field to previous event

### 704. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 223
}
- **Remediation**: Add canonical_hash field to previous event

### 705. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 224
}
- **Remediation**: Add canonical_hash field to previous event

### 706. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 225
}
- **Remediation**: Add canonical_hash field to previous event

### 707. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 226
}
- **Remediation**: Add canonical_hash field to previous event

### 708. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 227
}
- **Remediation**: Add canonical_hash field to previous event

### 709. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 228
}
- **Remediation**: Add canonical_hash field to previous event

### 710. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 229
}
- **Remediation**: Add canonical_hash field to previous event

### 711. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 230
}
- **Remediation**: Add canonical_hash field to previous event

### 712. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 231
}
- **Remediation**: Add canonical_hash field to previous event

### 713. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 232
}
- **Remediation**: Add canonical_hash field to previous event

### 714. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 233
}
- **Remediation**: Add canonical_hash field to previous event

### 715. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 234
}
- **Remediation**: Add canonical_hash field to previous event

### 716. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 235
}
- **Remediation**: Add canonical_hash field to previous event

### 717. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 236
}
- **Remediation**: Add canonical_hash field to previous event

### 718. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 237
}
- **Remediation**: Add canonical_hash field to previous event

### 719. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 238
}
- **Remediation**: Add canonical_hash field to previous event

### 720. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 239
}
- **Remediation**: Add canonical_hash field to previous event

### 721. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 240
}
- **Remediation**: Add canonical_hash field to previous event

### 722. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 241
}
- **Remediation**: Add canonical_hash field to previous event

### 723. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 242
}
- **Remediation**: Add canonical_hash field to previous event

### 724. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 243
}
- **Remediation**: Add canonical_hash field to previous event

### 725. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 244
}
- **Remediation**: Add canonical_hash field to previous event

### 726. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 245
}
- **Remediation**: Add canonical_hash field to previous event

### 727. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 246
}
- **Remediation**: Add canonical_hash field to previous event

### 728. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 247
}
- **Remediation**: Add canonical_hash field to previous event

### 729. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 248
}
- **Remediation**: Add canonical_hash field to previous event

### 730. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 249
}
- **Remediation**: Add canonical_hash field to previous event

### 731. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 250
}
- **Remediation**: Add canonical_hash field to previous event

### 732. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 251
}
- **Remediation**: Add canonical_hash field to previous event

### 733. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 252
}
- **Remediation**: Add canonical_hash field to previous event

### 734. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 253
}
- **Remediation**: Add canonical_hash field to previous event

### 735. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 254
}
- **Remediation**: Add canonical_hash field to previous event

### 736. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 255
}
- **Remediation**: Add canonical_hash field to previous event

### 737. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 256
}
- **Remediation**: Add canonical_hash field to previous event

### 738. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 257
}
- **Remediation**: Add canonical_hash field to previous event

### 739. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 258
}
- **Remediation**: Add canonical_hash field to previous event

### 740. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 259
}
- **Remediation**: Add canonical_hash field to previous event

### 741. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 260
}
- **Remediation**: Add canonical_hash field to previous event

### 742. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 261
}
- **Remediation**: Add canonical_hash field to previous event

### 743. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 262
}
- **Remediation**: Add canonical_hash field to previous event

### 744. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 263
}
- **Remediation**: Add canonical_hash field to previous event

### 745. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 264
}
- **Remediation**: Add canonical_hash field to previous event

### 746. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 265
}
- **Remediation**: Add canonical_hash field to previous event

### 747. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 266
}
- **Remediation**: Add canonical_hash field to previous event

### 748. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 267
}
- **Remediation**: Add canonical_hash field to previous event

### 749. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 268
}
- **Remediation**: Add canonical_hash field to previous event

### 750. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 269
}
- **Remediation**: Add canonical_hash field to previous event

### 751. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 270
}
- **Remediation**: Add canonical_hash field to previous event

### 752. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 271
}
- **Remediation**: Add canonical_hash field to previous event

### 753. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 272
}
- **Remediation**: Add canonical_hash field to previous event

### 754. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 273
}
- **Remediation**: Add canonical_hash field to previous event

### 755. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 274
}
- **Remediation**: Add canonical_hash field to previous event

### 756. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 275
}
- **Remediation**: Add canonical_hash field to previous event

### 757. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 276
}
- **Remediation**: Add canonical_hash field to previous event

### 758. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 277
}
- **Remediation**: Add canonical_hash field to previous event

### 759. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 278
}
- **Remediation**: Add canonical_hash field to previous event

### 760. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 279
}
- **Remediation**: Add canonical_hash field to previous event

### 761. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 280
}
- **Remediation**: Add canonical_hash field to previous event

### 762. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 281
}
- **Remediation**: Add canonical_hash field to previous event

### 763. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 282
}
- **Remediation**: Add canonical_hash field to previous event

### 764. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 283
}
- **Remediation**: Add canonical_hash field to previous event

### 765. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 284
}
- **Remediation**: Add canonical_hash field to previous event

### 766. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 285
}
- **Remediation**: Add canonical_hash field to previous event

### 767. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 286
}
- **Remediation**: Add canonical_hash field to previous event

### 768. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 287
}
- **Remediation**: Add canonical_hash field to previous event

### 769. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 288
}
- **Remediation**: Add canonical_hash field to previous event

### 770. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 289
}
- **Remediation**: Add canonical_hash field to previous event

### 771. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 290
}
- **Remediation**: Add canonical_hash field to previous event

### 772. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 291
}
- **Remediation**: Add canonical_hash field to previous event

### 773. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 292
}
- **Remediation**: Add canonical_hash field to previous event

### 774. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 293
}
- **Remediation**: Add canonical_hash field to previous event

### 775. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 294
}
- **Remediation**: Add canonical_hash field to previous event

### 776. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 295
}
- **Remediation**: Add canonical_hash field to previous event

### 777. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 296
}
- **Remediation**: Add canonical_hash field to previous event

### 778. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 297
}
- **Remediation**: Add canonical_hash field to previous event

### 779. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 298
}
- **Remediation**: Add canonical_hash field to previous event

### 780. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 299
}
- **Remediation**: Add canonical_hash field to previous event

### 781. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 300
}
- **Remediation**: Add canonical_hash field to previous event

### 782. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 301
}
- **Remediation**: Add canonical_hash field to previous event

### 783. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 302
}
- **Remediation**: Add canonical_hash field to previous event

### 784. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 303
}
- **Remediation**: Add canonical_hash field to previous event

### 785. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 304
}
- **Remediation**: Add canonical_hash field to previous event

### 786. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 305
}
- **Remediation**: Add canonical_hash field to previous event

### 787. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 306
}
- **Remediation**: Add canonical_hash field to previous event

### 788. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 307
}
- **Remediation**: Add canonical_hash field to previous event

### 789. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 308
}
- **Remediation**: Add canonical_hash field to previous event

### 790. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 309
}
- **Remediation**: Add canonical_hash field to previous event

### 791. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 310
}
- **Remediation**: Add canonical_hash field to previous event

### 792. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 311
}
- **Remediation**: Add canonical_hash field to previous event

### 793. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 312
}
- **Remediation**: Add canonical_hash field to previous event

### 794. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 313
}
- **Remediation**: Add canonical_hash field to previous event

### 795. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 314
}
- **Remediation**: Add canonical_hash field to previous event

### 796. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 315
}
- **Remediation**: Add canonical_hash field to previous event

### 797. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 316
}
- **Remediation**: Add canonical_hash field to previous event

### 798. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 317
}
- **Remediation**: Add canonical_hash field to previous event

### 799. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 318
}
- **Remediation**: Add canonical_hash field to previous event

### 800. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 319
}
- **Remediation**: Add canonical_hash field to previous event

### 801. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 320
}
- **Remediation**: Add canonical_hash field to previous event

### 802. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 321
}
- **Remediation**: Add canonical_hash field to previous event

### 803. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 322
}
- **Remediation**: Add canonical_hash field to previous event

### 804. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 323
}
- **Remediation**: Add canonical_hash field to previous event

### 805. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 324
}
- **Remediation**: Add canonical_hash field to previous event

### 806. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 325
}
- **Remediation**: Add canonical_hash field to previous event

### 807. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 326
}
- **Remediation**: Add canonical_hash field to previous event

### 808. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 327
}
- **Remediation**: Add canonical_hash field to previous event

### 809. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 328
}
- **Remediation**: Add canonical_hash field to previous event

### 810. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 329
}
- **Remediation**: Add canonical_hash field to previous event

### 811. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 330
}
- **Remediation**: Add canonical_hash field to previous event

### 812. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 331
}
- **Remediation**: Add canonical_hash field to previous event

### 813. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 332
}
- **Remediation**: Add canonical_hash field to previous event

### 814. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 333
}
- **Remediation**: Add canonical_hash field to previous event

### 815. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 334
}
- **Remediation**: Add canonical_hash field to previous event

### 816. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 335
}
- **Remediation**: Add canonical_hash field to previous event

### 817. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 336
}
- **Remediation**: Add canonical_hash field to previous event

### 818. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 337
}
- **Remediation**: Add canonical_hash field to previous event

### 819. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 338
}
- **Remediation**: Add canonical_hash field to previous event

### 820. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 339
}
- **Remediation**: Add canonical_hash field to previous event

### 821. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 340
}
- **Remediation**: Add canonical_hash field to previous event

### 822. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 341
}
- **Remediation**: Add canonical_hash field to previous event

### 823. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 342
}
- **Remediation**: Add canonical_hash field to previous event

### 824. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 343
}
- **Remediation**: Add canonical_hash field to previous event

### 825. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 344
}
- **Remediation**: Add canonical_hash field to previous event

### 826. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 345
}
- **Remediation**: Add canonical_hash field to previous event

### 827. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 346
}
- **Remediation**: Add canonical_hash field to previous event

### 828. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 347
}
- **Remediation**: Add canonical_hash field to previous event

### 829. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 348
}
- **Remediation**: Add canonical_hash field to previous event

### 830. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 349
}
- **Remediation**: Add canonical_hash field to previous event

### 831. Event chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "expected_previous": "91c736ab2cef76cfea2d3653ac7072bd44a3c4bb453986b352d2909b478b24c5",
  "actual_previous": null
}
- **Remediation**: Fix hash_chain.previous_event field to point to previous event

### 832. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 360
}
- **Remediation**: Add canonical_hash field to previous event

### 833. Event chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "expected_previous": "e5f24c30707f41a31fea94bcec5c69d649ca6d9633e4a3cb1e734d2b22a1c1c4",
  "actual_previous": null
}
- **Remediation**: Fix hash_chain.previous_event field to point to previous event

### 834. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 371
}
- **Remediation**: Add canonical_hash field to previous event

### 835. Event chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "expected_previous": "832c3aca5297cb1f005aa889da865c9c1ca5a44eeb0fbab4e43bcb8e4e581ad4",
  "actual_previous": null
}
- **Remediation**: Fix hash_chain.previous_event field to point to previous event

### 836. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 382
}
- **Remediation**: Add canonical_hash field to previous event

### 837. Event chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "expected_previous": "43eded6302b9105b946e9574f038c7d54b07874beaf0215cdfd41b9be8f542a9",
  "actual_previous": null
}
- **Remediation**: Fix hash_chain.previous_event field to point to previous event

### 838. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 393
}
- **Remediation**: Add canonical_hash field to previous event

### 839. Event chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "expected_previous": "5d793148fef93163462e6ad3d0a48c4a9ddb2fcded060906fd59042334f88977",
  "actual_previous": null
}
- **Remediation**: Fix hash_chain.previous_event field to point to previous event

### 840. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 404
}
- **Remediation**: Add canonical_hash field to previous event

### 841. Event chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "expected_previous": "b717032080e6941aea9d96779d841701618c2c97649c223534df6ac0292d99bb",
  "actual_previous": null
}
- **Remediation**: Fix hash_chain.previous_event field to point to previous event

### 842. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 415
}
- **Remediation**: Add canonical_hash field to previous event

### 843. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 416
}
- **Remediation**: Add canonical_hash field to previous event

### 844. Event chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "expected_previous": "8b2ee955efa27ed5a55e6795eabea47fb2ce4506b18bd50742027e522a443900",
  "actual_previous": null
}
- **Remediation**: Fix hash_chain.previous_event field to point to previous event

### 845. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 427
}
- **Remediation**: Add canonical_hash field to previous event

### 846. Event chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "expected_previous": "d77077aed674e2f1cac0e405a06849df616e97a5264b36966189d632756049ba",
  "actual_previous": null
}
- **Remediation**: Fix hash_chain.previous_event field to point to previous event

### 847. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 438
}
- **Remediation**: Add canonical_hash field to previous event

### 848. Event chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "expected_previous": "b0ccdba807fd81339dbdc3e2eaf016c6c9bb1bb2c35bf5f63d777e6509e6cc82",
  "actual_previous": null
}
- **Remediation**: Fix hash_chain.previous_event field to point to previous event

### 849. Previous event missing canonical_hash

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "previous_event_index": 449
}
- **Remediation**: Add canonical_hash field to previous event

### 850. Event chain broken

- **Test ID**: TC-2.2
- **Severity**: CRITICAL
- **Evidence**: {
  "event_id": "UNKNOWN",
  "expected_previous": "27c4f87f47b5d3e6efd5089715470b774f0ff9d03c1df27ba338a99bc584a56d",
  "actual_previous": null
}
- **Remediation**: Fix hash_chain.previous_event field to point to previous event

### 851. RFC8785 canonicalization not available

- **Test ID**: TC-3.1
- **Severity**: HIGH
- **Evidence**: {}
- **Remediation**: Install rfc8785 package: pip install rfc8785

### 852. Artifact missing generation metadata

- **Test ID**: TC-5.1
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "c771a453-1599-4459-870e-c26553eae425"
}
- **Affected Artifacts**: c771a453-1599-4459-870e-c26553eae425
- **Remediation**: Add metadata.generated_by field to artifact

### 853. Artifact missing generation metadata

- **Test ID**: TC-5.1
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "c8b94f8d-3a07-438f-ad3a-cc0e986b9838"
}
- **Affected Artifacts**: c8b94f8d-3a07-438f-ad3a-cc0e986b9838
- **Remediation**: Add metadata.generated_by field to artifact

### 854. Artifact missing generation metadata

- **Test ID**: TC-5.1
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "5c46eb1d-27f5-431d-9938-20e7b0049e31"
}
- **Affected Artifacts**: 5c46eb1d-27f5-431d-9938-20e7b0049e31
- **Remediation**: Add metadata.generated_by field to artifact

### 855. Artifact missing generation metadata

- **Test ID**: TC-5.1
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "a4dc84a4-494d-496a-b315-b352dcca4620"
}
- **Affected Artifacts**: a4dc84a4-494d-496a-b315-b352dcca4620
- **Remediation**: Add metadata.generated_by field to artifact

### 856. Artifact missing generation metadata

- **Test ID**: TC-5.1
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "2633a6c9-9a34-43ae-8d50-248941f1b297"
}
- **Affected Artifacts**: 2633a6c9-9a34-43ae-8d50-248941f1b297
- **Remediation**: Add metadata.generated_by field to artifact

### 857. Artifact missing generation metadata

- **Test ID**: TC-5.1
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "0bf27f5b-e6aa-4084-a558-cf71d67b5f0b"
}
- **Affected Artifacts**: 0bf27f5b-e6aa-4084-a558-cf71d67b5f0b
- **Remediation**: Add metadata.generated_by field to artifact

### 858. Artifact missing generation metadata

- **Test ID**: TC-5.1
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "596cce6b-d567-4027-a828-d9f919fd49c9"
}
- **Affected Artifacts**: 596cce6b-d567-4027-a828-d9f919fd49c9
- **Remediation**: Add metadata.generated_by field to artifact

### 859. Artifact missing generation metadata

- **Test ID**: TC-5.1
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "4131ace7-f74a-4e7a-9eb4-a220dd5f7af2"
}
- **Affected Artifacts**: 4131ace7-f74a-4e7a-9eb4-a220dd5f7af2
- **Remediation**: Add metadata.generated_by field to artifact

### 860. Artifact missing generation metadata

- **Test ID**: TC-5.1
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "1bcf919c-f1bd-4079-9a56-5c106cd8ce8a"
}
- **Affected Artifacts**: 1bcf919c-f1bd-4079-9a56-5c106cd8ce8a
- **Remediation**: Add metadata.generated_by field to artifact

### 861. Artifact missing generation metadata

- **Test ID**: TC-5.1
- **Severity**: HIGH
- **Evidence**: {
  "artifact_id": "98c852ee-0812-4f2a-bd2c-59ecd946fb32"
}
- **Affected Artifacts**: 98c852ee-0812-4f2a-bd2c-59ecd946fb32
- **Remediation**: Add metadata.generated_by field to artifact

## Conclusion

❌ **CRITICAL VIOLATIONS DETECTED** - System is not ready for Era-1 sealing.