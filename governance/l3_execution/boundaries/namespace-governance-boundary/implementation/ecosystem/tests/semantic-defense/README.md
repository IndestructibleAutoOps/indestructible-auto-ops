# Era-1 Semantic Defense System Test Suite

## Overview

This test suite implements the **Semantic Defense System** for Era-1, designed to make the system:
- **Uncheatable**: Semantic declarations cannot be faked or hidden
- **Undrifting**: Hash values remain stable across environments
- **Unnarratable**: Fuzzy language and narrative wrappers are rejected

## Test Categories

### 1. Semantic Corruption Tests (`test-semantic-corruption/`)
**Purpose**: Detect semantic corruption from fuzzy language, narrative wrappers, and declaration mismatches

**Test Cases**:
- TC-1.1: Fuzzy Language Detection
- TC-1.2: Narrative Wrapper Detection
- TC-1.3: Semantic Declaration Mismatch

**Severity**: CRITICAL/HIGH

---

### 2. Hash Divergence Tests (`test-hash-divergence/`)
**Purpose**: Ensure canonicalization produces consistent hashes across environments

**Test Cases**:
- TC-2.1: Windows vs Linux Hash Consistency
- TC-2.2: Python Version Hash Consistency
- TC-2.3: Locale Hash Consistency
- TC-2.4: Line Ending Hash Consistency

**Severity**: CRITICAL/HIGH

---

### 3. YAML Failure Tests (`test-yaml-failure/`)
**Purpose**: Validate YAML → JSON → JCS pipeline

**Test Cases**:
- TC-3.1: YAML Anchor Expansion
- TC-3.2: YAML Alias Resolution
- TC-3.3: YAML Tag Conversion
- TC-3.4: Multi-file YAML

**Severity**: HIGH/MEDIUM

---

### 4. Event Stream Missing Field Tests (`test-event-missing-field/`)
**Purpose**: Ensure event stream integrity

**Test Cases**:
- TC-4.1: Missing Timestamp
- TC-4.2: Missing UUID
- TC-4.3: Missing Event Type
- TC-4.4: Missing Payload

**Severity**: CRITICAL

---

### 5. Tool Registry Missing Tests (`test-tool-registry/`)
**Purpose**: Ensure all tools are registered

**Test Cases**:
- TC-5.1: Unregistered Tool Call
- TC-5.2: Missing Tool Metadata
- TC-5.3: Version Mismatch

**Severity**: CRITICAL/HIGH

---

### 6. Complement Missing Tests (`test-complement-missing/`)
**Purpose**: Ensure semantic declarations have corresponding complements

**Test Cases**:
- TC-6.1: "Completed" Without Complement
- TC-6.2: "Integrated" Without Artifact
- TC-6.3: "Passed" Without Evidence

**Severity**: CRITICAL

---

### 7. Canonicalization Invariant Tests (`test-canonicalization-invariant/`)
**Purpose**: Ensure canonicalization is irreversible and consistent

**Test Cases**:
- TC-7.1: JCS → Layered Sorting
- TC-7.2: Layered Sorting → JCS
- TC-7.3: Repeated Canonicalization

**Severity**: CRITICAL

---

### 8. Layered Sorting Invariant Tests (`test-layered-sorting/`)
**Purpose**: Ensure layered sorting doesn't break canonical hash

**Test Cases**:
- TC-8.1: L1/L2/L3 Field Reordering
- TC-8.2: L2 Field Addition
- TC-8.3: L3 Field Expansion

**Severity**: CRITICAL/HIGH/MEDIUM

---

### 9. Pipeline Interrupted Tests (`test-pipeline-interrupted/`)
**Purpose**: Ensure safe pipeline interruption handling

**Test Cases**:
- TC-9.1: Canonicalization Failure
- TC-9.2: Hash Calculation Failure
- TC-9.3: Event Stream Write Failure
- TC-9.4: Artifact Generation Failure

**Severity**: CRITICAL

---

## Running Tests

### Run All Tests
```bash
cd ecosystem/tests/semantic_defense
pytest -v
```

### Run Specific Test Category
```bash
pytest -v test-semantic-corruption/
```

### Run Specific Test Case
```bash
pytest -v test-semantic-corruption/test_semantic_corruption.py::TestSemanticCorruption::test_tc_1_1_fuzzy_language_detection
```

### Run with Coverage
```bash
pytest --cov=semantic_defense --cov-report=html
```

### Generate HTML Report
```bash
pytest --html=report.html --self-contained-html
```

---

## Test Output

### Success
```
ecosystem/tests/semantic-defense/test-semantic-corruption/test_semantic_corruption.py::TestSemanticCorruption::test_tc_1_1_fuzzy_language_detection PASSED
ecosystem/tests/semantic-defense/test-semantic-corruption/test_semantic_corruption.py::TestSemanticCorruption::test_tc_1_2_narrative_wrapper_detection PASSED
...
```

### Failure (Violation Detected)
```
FAILED ecosystem/tests/semantic-defense/test-semantic-corruption/test_semantic_corruption.py::TestSemanticCorruption::test_tc_1_3_semantic_declaration_mismatch
AssertionError: Should detect semantic mismatch: COMPLETED with no evidence
```

---

## Violation Reporting

When a test detects a violation, it generates a **violation object** that includes:

```python
{
    "test_case": "TC-1.3",
    "severity": "CRITICAL",
    "detected_issue": "declaration_mismatch",
    "evidence": {
        "declared_status": "COMPLETED",
        "actual_state": "NO_EVIDENCE",
        "evidence_count": 0
    },
    "remediation": {
        "action": "align_status_with_evidence",
        "required": "狀態必須與證據一致",
        "suggestion": "提供完整證據或將狀態改為 IN_PROGRESS"
    },
    "timestamp": "2026-02-04T20:00:00Z"
}
```

Violations can be converted to complements:

```python
violation.to_complement()
```

---

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: Semantic Defense Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Semantic Defense Tests
        run: |
          cd ecosystem/tests/semantic_defense
          pytest -v --junitxml=test-results.xml
      - name: Upload Test Results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: test-results.xml
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

cd ecosystem/tests/semantic_defense
pytest -q

if [ $? -ne 0 ]; then
    echo "Semantic defense tests failed. Commit blocked."
    exit 1
fi
```

---

## Compliance Gates

### Before Era-1 Sealing
All **CRITICAL** tests must pass:
- ✅ TC-1.3: Semantic Declaration Mismatch
- ✅ TC-2.1: Windows vs Linux Hash Consistency
- ✅ TC-2.2: Python Version Hash Consistency
- ✅ TC-4.1-4.4: Event Stream Missing Fields
- ✅ TC-5.1: Unregistered Tool Call
- ✅ TC-6.1-6.3: Complement Missing
- ✅ TC-7.1-7.3: Canonicalization Invariant
- ✅ TC-8.1: L1/L2/L3 Field Reordering
- ✅ TC-9.1-9.4: Pipeline Interrupted

### Before Era-2 Migration
All tests must pass (CRITICAL, HIGH, MEDIUM)

---

## Test Coverage Goals

| Category | Target | Current | Status |
|----------|--------|---------|--------|
| Semantic Corruption | 100% | 60% | 🟡 |
| Hash Divergence | 100% | 80% | 🟢 |
| YAML Failure | 100% | 0% | 🔴 |
| Event Missing Field | 100% | 0% | 🔴 |
| Tool Registry Missing | 100% | 0% | 🔴 |
| Complement Missing | 100% | 0% | 🔴 |
| Canonicalization Invariant | 100% | 60% | 🟡 |
| Layered Sorting Invariant | 100% | 0% | 🔴 |
| Pipeline Interrupted | 100% | 0% | 🔴 |
| **Overall** | **100%** | **22%** | 🔴 |

---

## Contributing

### Adding New Test Cases

1. Create test file in appropriate category directory
2. Follow naming convention: `test_tc_{category}_{case_number}_{description}.py`
3. Use fixtures from `conftest.py`
4. Generate violations when issues detected
5. Document severity level and remediation

### Example
```python
def test_tc_X_Y_new_test_case(self, sample_artifact, violation_maker):
    """
    TC-X.Y: New Test Case
    
    Input: Description
    Expected: Expected behavior
    Action: Action to take
    Severity: CRITICAL
    """
    # Test logic here
    
    # If violation detected
    if violation_detected:
        violation = violation_maker(
            test_case="TC-X.Y",
            severity="CRITICAL",
            detected_issue="issue_name",
            evidence={},
            remediation={}
        )
```

---

## References

- [Semantic Defense Specification](../../governance/semantic-defense-specification.md)
- [Hash Storage Specification](../../governance/hash-storage-specification.md)
- [RFC 8785: JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785)

---

**Version**: 1.0.0  
**Era**: 1 (Evidence-Native Bootstrap)  
**Status**: Active Development  
**Last Updated**: 2026-02-04