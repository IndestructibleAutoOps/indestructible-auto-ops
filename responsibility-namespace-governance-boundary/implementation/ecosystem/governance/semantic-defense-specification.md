# Era-1 Semantic Defense System Specification v1.0

## 🛡️ Core Philosophy

> **Era-1 的測試不是為了「全部通過」，而是為了「逼出語義錯誤、破壞 hash、破壞 pipeline、破壞補件」，讓系統變得不可欺騙、不可漂移、不可敘事化。**

---

## 📋 Table of Contents

1. [Semantic Defense Overview](#semantic-defense-overview)
2. [Test Taxonomy](#test-taxonomy)
3. [Test Specifications](#test-specifications)
4. [Enforcement Rules](#enforcement-rules)
5. [Complement Generation](#complement-generation)
6. [Failure Handling](#failure-handling)

---

## 🔍 Semantic Defense Overview

### Purpose

The Era-1 Semantic Defense System ensures:
- **Uncheatable**: Semantic declarations cannot be faked or hidden
- **Undrifting**: Hash values remain stable across environments
- **Unnarratable**: Fuzzy language and narrative wrappers are rejected

### Defense Layers

```
┌─────────────────────────────────────────────────────┐
│         Governance Layer (Semantic Defense)          │
├─────────────────────────────────────────────────────┤
│  Semantic Corruption Detection                     │
│  Hash Divergence Detection                          │
│  YAML Structure Validation                          │
│  Event Stream Integrity                             │
│  Tool Registry Enforcement                          │
│  Complement Existence Verification                  │
│  Canonicalization Consistency                       │
│  Layered Sorting Invariance                         │
│  Pipeline Failure Safety                            │
└─────────────────────────────────────────────────────┘
```

---

## 🧪 Test Taxonomy

### Test Categories

| Category | Tests | Purpose |
|----------|-------|---------|
| **Semantic Integrity** | 1, 6 | Detect semantic corruption and missing complements |
| **Hash Consistency** | 2, 7, 8 | Ensure hash stability and canonicalization invariance |
| **Structural Validation** | 3, 4, 5 | Validate YAML, event stream, and tool registry |
| **Pipeline Safety** | 9 | Ensure safe pipeline interruption handling |

---

## 📝 Test Specifications

### Test 1: 語義破壞測試 (Semantic Corruption Tests)

#### Purpose
確保語義聲明與實體之間的對應不會被敘事、包裝、模糊語氣破壞。

#### Test Cases

**TC-1.1: Fuzzy Language Detection**
- **Input**: Report containing "大致完成" (roughly complete)
- **Expected**: System detects semantic shift
- **Action**: Generate complement, block sealing
- **Severity**: HIGH

**TC-1.2: Narrative Wrapper Detection**
- **Input**: Tool output with narrative wrapping
- **Expected**: System rejects narrative language
- **Action**: Generate complement, require factual output
- **Severity**: HIGH

**TC-1.3: Semantic Declaration Mismatch**
- **Input**: "status": "COMPLETED" but evidence incomplete
- **Expected**: System detects mismatch
- **Action**: Generate complement, block sealing
- **Severity**: CRITICAL

#### Enforcement Rules
```yaml
rule: SEM_CORRUPTION
severity: CRITICAL
action: BLOCK
complement_required: true
conditions:
  - fuzzy_language_detected
  - narrative_wrapper_detected
  - declaration_mismatch
```

---

### Test 2: Hash 不一致測試 (Cross-Environment Hash Divergence Tests)

#### Purpose
確保 canonicalization pipeline 在不同環境產生一致 hash。

#### Test Cases

**TC-2.1: Windows vs Linux**
- **Input**: Same artifact on Windows and Linux
- **Expected**: Hashes identical
- **Action**: If divergent → report canonicalization failure
- **Severity**: CRITICAL

**TC-2.2: Python Version Differences**
- **Input**: Same artifact on Python 3.8, 3.9, 3.10, 3.11
- **Expected**: Hashes identical
- **Action**: If divergent → report canonicalization failure
- **Severity**: CRITICAL

**TC-2.3: Locale Differences**
- **Input**: Same artifact with different locales (en_US, zh_TW, ja_JP)
- **Expected**: Hashes identical
- **Action**: If divergent → report canonicalization failure
- **Severity**: HIGH

**TC-2.4: Line Ending Differences**
- **Input**: Same artifact with LF vs CRLF
- **Expected**: Hashes identical
- **Action**: If divergent → report canonicalization failure
- **Severity**: HIGH

#### Enforcement Rules
```yaml
rule: HASH_DIVGENCE
severity: CRITICAL
action: BLOCK
complement_required: true
conditions:
  - windows_linux_divergence
  - python_version_divergence
  - locale_divergence
  - line_ending_divergence
```

---

### Test 3: YAML Anchors 破壞測試 (YAML Anchor/Tag Failure Tests)

#### Purpose
確保 YAML → JSON → JCS pipeline 能正確處理 YAML 特性。

#### Test Cases

**TC-3.1: YAML Anchor Expansion**
- **Input**: YAML with anchors (`&anchor`, `*ref`)
- **Expected**: Anchors expanded, canonical JSON correct
- **Action**: If failed → report YAML parsing failure
- **Severity**: HIGH

**TC-3.2: YAML Alias Resolution**
- **Input**: YAML with aliases
- **Expected**: Aliases resolved correctly
- **Action**: If failed → report YAML parsing failure
- **Severity**: HIGH

**TC-3.3: YAML Tag Conversion**
- **Input**: YAML with custom tags (`!custom`)
- **Expected**: Tags converted to JSON-compatible format
- **Action**: If failed → report YAML parsing failure
- **Severity**: MEDIUM

**TC-3.4: Multi-file YAML**
- **Input**: YAML with `---` document separators
- **Expected**: Each document processed independently
- **Action**: If failed → report YAML parsing failure
- **Severity**: MEDIUM

#### Enforcement Rules
```yaml
rule: YAML_FAILURE
severity: HIGH
action: BLOCK
complement_required: true
conditions:
  - anchor_expansion_failed
  - alias_resolution_failed
  - tag_conversion_failed
  - multifile_parsing_failed
```

---

### Test 4: Event Stream 缺欄位測試 (Event Stream Missing Field Tests)

#### Purpose
確保事件流缺欄位時不會 silently pass。

#### Test Cases

**TC-4.1: Missing Timestamp**
- **Input**: Event without `timestamp` field
- **Expected**: System rejects event
- **Action**: Generate complement, report incomplete event
- **Severity**: CRITICAL

**TC-4.2: Missing UUID**
- **Input**: Event without `event_id` field
- **Expected**: System rejects event
- **Action**: Generate complement, report incomplete event
- **Severity**: CRITICAL

**TC-4.3: Missing Event Type**
- **Input**: Event without `event_type` field
- **Expected**: System rejects event
- **Action**: Generate complement, report incomplete event
- **Severity**: CRITICAL

**TC-4.4: Missing Payload**
- **Input**: Event without required payload fields
- **Expected**: System rejects event
- **Action**: Generate complement, report incomplete event
- **Severity**: HIGH

#### Enforcement Rules
```yaml
rule: EVENT_MISSING_FIELD
severity: CRITICAL
action: BLOCK
complement_required: true
conditions:
  - missing_timestamp
  - missing_uuid
  - missing_event_type
  - missing_payload
```

---

### Test 5: 工具 Registry 缺定義測試 (Tool Registry Integrity Tests)

#### Purpose
確保所有工具都必須在 registry 中註冊。

#### Test Cases

**TC-5.1: Unregistered Tool Call**
- **Input**: Call to tool not in registry
- **Expected**: System blocks execution
- **Action**: Generate complement, report tool missing
- **Severity**: CRITICAL

**TC-5.2: Missing Tool Metadata**
- **Input**: Tool in registry but metadata incomplete
- **Expected**: System blocks execution
- **Action**: Generate complement, report metadata missing
- **Severity**: HIGH

**TC-5.3: Version Mismatch**
- **Input**: Tool version mismatch with registry
- **Expected**: System blocks execution
- **Action**: Generate complement, report version conflict
- **Severity**: MEDIUM

#### Enforcement Rules
```yaml
rule: TOOL_REGISTRY_MISSING
severity: CRITICAL
action: BLOCK
complement_required: true
conditions:
  - tool_not_registered
  - tool_metadata_missing
  - version_mismatch
```

---

### Test 6: 補件缺失測試 (Complement Missing Tests)

#### Purpose
確保語義聲明一定要對應補件。

#### Test Cases

**TC-6.1: "Completed" Without Complement**
- **Input**: "status": "COMPLETED" but no complement file
- **Expected**: System detects semantic inconsistency
- **Action**: Generate complement, block sealing
- **Severity**: CRITICAL

**TC-6.2: "Integrated" Without Artifact**
- **Input**: "status": "INTEGRATED" but no artifact
- **Expected**: System detects semantic inconsistency
- **Action**: Generate complement, block sealing
- **Severity**: CRITICAL

**TC-6.3: "Passed" Without Evidence**
- **Input**: "status": "PASSED" but no evidence
- **Expected**: System detects semantic inconsistency
- **Action**: Generate complement, block sealing
- **Severity**: CRITICAL

#### Enforcement Rules
```yaml
rule: COMPLEMENT_MISSING
severity: CRITICAL
action: BLOCK
complement_required: true
conditions:
  - completed_without_complement
  - integrated_without_artifact
  - passed_without_evidence
```

---

### Test 7: Canonicalization 逆序測試 (Reverse Canonicalization Tests)

#### Purpose
確保 canonicalization 是不可逆的（格式層不受語義層干擾）。

#### Test Cases

**TC-7.1: JCS → Layered Sorting**
- **Input**: First apply JCS, then layered sorting
- **Expected**: Final hash consistent
- **Action**: If divergent → report canonicalization failure
- **Severity**: CRITICAL

**TC-7.2: Layered Sorting → JCS**
- **Input**: First apply layered sorting, then JCS
- **Expected**: Final hash consistent
- **Action**: If divergent → report canonicalization failure
- **Severity**: CRITICAL

**TC-7.3: Repeated Canonicalization**
- **Input**: Canonicalize multiple times
- **Expected**: Hash always identical
- **Action**: If divergent → report canonicalization failure
- **Severity**: HIGH

#### Enforcement Rules
```yaml
rule: CANONICALIZATION_INVARIANT
severity: CRITICAL
action: BLOCK
complement_required: true
conditions:
  - jcs_layered_ordering_divergence
  - repeated_canonicalization_divergence
```

---

### Test 8: 分層排序語義衝突測試 (Layered Sorting Conflict Tests)

#### Purpose
確保分層排序不會破壞 canonical hash。

#### Test Cases

**TC-8.1: L1/L2/L3 Field Reordering**
- **Input**: Randomize L1/L2/L3 field order
- **Expected**: Canonical hash unchanged
- **Action**: If changed → report sorting failure
- **Severity**: CRITICAL

**TC-8.2: L2 Field Addition**
- **Input**: Add new fields to L2
- **Expected**: Canonical hash unchanged
- **Action**: If changed → report sorting failure
- **Severity**: HIGH

**TC-8.3: L3 Field Expansion**
- **Input**: Add many fields to L3
- **Expected**: Canonical hash unchanged
- **Action**: If changed → report sorting failure
- **Severity**: MEDIUM

#### Enforcement Rules
```yaml
rule: LAYERED_SORTING_INVARIANT
severity: CRITICAL
action: BLOCK
complement_required: true
conditions:
  - field_reordering_changes_hash
  - l2_addition_changes_hash
  - l3_expansion_changes_hash
```

---

### Test 9: Pipeline 中斷測試 (Pipeline Interruption Tests)

#### Purpose
確保 pipeline 任一階段失敗時，整個流程會安全中止。

#### Test Cases

**TC-9.1: Canonicalization Failure**
- **Input**: Force canonicalization to fail
- **Expected**: Pipeline stops safely
- **Action**: Generate complement, block sealing
- **Severity**: CRITICAL

**TC-9.2: Hash Calculation Failure**
- **Input**: Force hash calculation to fail
- **Expected**: Pipeline stops safely
- **Action**: Generate complement, block sealing
- **Severity**: CRITICAL

**TC-9.3: Event Stream Write Failure**
- **Input**: Force event stream write to fail
- **Expected**: Pipeline stops safely
- **Action**: Generate complement, block sealing
- **Severity**: CRITICAL

**TC-9.4: Artifact Generation Failure**
- **Input**: Force artifact generation to fail
- **Expected**: Pipeline stops safely
- **Action**: Generate complement, block sealing
- **Severity**: CRITICAL

#### Enforcement Rules
```yaml
rule: PIPELINE_INTERRUPTED
severity: CRITICAL
action: BLOCK
complement_required: true
conditions:
  - canonicalization_failed
  - hash_calculation_failed
  - event_stream_write_failed
  - artifact_generation_failed
```

---

## ⚖️ Enforcement Rules

### Severity Levels

| Severity | Action | Impact |
|----------|--------|--------|
| **CRITICAL** | BLOCK | Stops pipeline, requires complement |
| **HIGH** | WARN | Continues with warning, requires complement |
| **MEDIUM** | LOG | Logs issue, optional complement |
| **LOW** | INFO | Informational only |

### Enforcement Matrix

| Test | Severity | Action | Complement Required |
|------|----------|--------|---------------------|
| 1. Semantic Corruption | CRITICAL | BLOCK | ✅ |
| 2. Hash Divergence | CRITICAL | BLOCK | ✅ |
| 3. YAML Failure | HIGH | BLOCK | ✅ |
| 4. Event Missing Field | CRITICAL | BLOCK | ✅ |
| 5. Tool Registry Missing | CRITICAL | BLOCK | ✅ |
| 6. Complement Missing | CRITICAL | BLOCK | ✅ |
| 7. Canonicalization Invariant | CRITICAL | BLOCK | ✅ |
| 8. Layered Sorting Invariant | CRITICAL | BLOCK | ✅ |
| 9. Pipeline Interrupted | CRITICAL | BLOCK | ✅ |

---

## 📦 Complement Generation

### Complement Templates

**TC-1: Semantic Corruption Complement**
```json
{
  "complement_type": "semantic_corruption",
  "test_case": "TC-1.X",
  "detected_issue": "fuzzy_language_detected",
  "evidence": {
    "fuzzy_phrases": ["大致完成", "應該沒問題"],
    "location": "report.md:42"
  },
  "remediation": {
    "action": "replace_with_factual_language",
    "required": "明確聲明狀態 (COMPLETED/IN_PROGRESS/FAILED)"
  }
}
```

**TC-2: Hash Divergence Complement**
```json
{
  "complement_type": "hash_divergence",
  "test_case": "TC-2.X",
  "detected_issue": "windows_linux_divergence",
  "evidence": {
    "windows_hash": "abc123",
    "linux_hash": "def456",
    "artifact": "step-1.json"
  },
  "remediation": {
    "action": "fix_canonicalization_pipeline",
    "required": "確保所有環境產生相同 hash"
  }
}
```

---

## 🚨 Failure Handling

### Pipeline Failure Recovery

```
1. Detect Failure
   ↓
2. Generate Complement
   ↓
3. Block Sealing
   ↓
4. Log Failure
   ↓
5. Require Manual Review
   ↓
6. Re-test After Fix
   ↓
7. Un-block Sealing
```

### Failure States

| State | Description | Action Required |
|-------|-------------|-----------------|
| **FAILED** | Test failed | Generate complement, block |
| **RETRY** | Temporary failure | Retry with limit |
| **MANUAL** | Requires review | Manual intervention |
| **PASSED** | Test passed | Continue pipeline |

---

## 🎯 Success Criteria

### Era-1 Semantic Defense System Ready When:

- [x] All 9 test categories defined
- [x] Test cases specified for each category
- [x] Enforcement rules established
- [x] Complement templates created
- [x] Failure handling defined
- [ ] Test implementation completed
- [ ] Test execution automated
- [ ] CI/CD integration
- [ ] Full coverage achieved

---

## 📊 Test Coverage Matrix

| Test Category | Test Cases | Implemented | Automated | Coverage |
|---------------|------------|-------------|-----------|----------|
| Semantic Corruption | 3 | ⏸️ | ⏸️ | 0% |
| Hash Divergence | 4 | ⏸️ | ⏸️ | 0% |
| YAML Failure | 4 | ⏸️ | ⏸️ | 0% |
| Event Missing Field | 4 | ⏸️ | ⏸️ | 0% |
| Tool Registry Missing | 3 | ⏸️ | ⏸️ | 0% |
| Complement Missing | 3 | ⏸️ | ⏸️ | 0% |
| Canonicalization Invariant | 3 | ⏸️ | ⏸️ | 0% |
| Layered Sorting Invariant | 3 | ⏸️ | ⏸️ | 0% |
| Pipeline Interrupted | 4 | ⏸️ | ⏸️ | 0% |
| **Total** | **31** | **0** | **0** | **0%** |

---

## 🔮 Future Extensions

### Era-2 Tests (Planned)
- Merkle tree integrity tests
- Bidirectional hash mapping tests
- Semantic closure validation tests
- Era sealing protocol tests

### Advanced Tests (Planned)
- Differential privacy tests
- Provenance tracking tests
- Temporal consistency tests
- Cross-era migration tests

---

## 📚 References

1. **RFC 8785**: JSON Canonicalization Scheme (JCS)
2. **W3C Verifiable Credentials**: Data Integrity specification
3. **Merkle Trees**: Cryptographic data structures
4. **Chain of Custody**: Digital evidence preservation
5. **Git Content-Addressable Storage**: Hash-based storage

---

**Specification Version**: 1.0.0
**Last Updated**: 2026-02-04
**Governance Level**: CRITICAL
**Era**: 1 (Evidence-Native Bootstrap)
**Status**: READY FOR IMPLEMENTATION