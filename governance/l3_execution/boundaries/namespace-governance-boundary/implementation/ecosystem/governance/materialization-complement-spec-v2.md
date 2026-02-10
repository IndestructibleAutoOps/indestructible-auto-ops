# Materialization Complement Specification v2.0
## Era-1 Semantic Entity Binding & Proof-Carrying Artifacts

---

## 1. Core Principles

### 1.1 Governance-First Development
- **Compliance-Driven Generation**: All complements generated based on governance requirements
- **Semantic-to-Entity Binding**: Every semantic declaration must map to concrete entities
- **Missing Entity Detection**: Automatic identification of gaps between declarations and implementations
- **Complement Generation**: Creation of missing entities with proper validation

### 1.2 Proof-Carrying Artifacts (PRISM-inspired)
- **Cryptographic Proofs**: Every complement includes SHA256 hash proofs
- **Deterministic Generation**: RFC 8785 canonicalization for reproducible hashes
- **Verifiable Process**: Complete generation trace from violation to complement
- **Independent Validation**: Complements can be validated without re-execution

### 1.3 Semantic Integrity Constraints
- **Declarative Guardrails**: Semantic rules that prevent invalid complements
- **Deviation Detection**: Automatic detection of semantic drift
- **Continuous Verification**: Real-time compliance checking
- **Auto-Remediation**: Automatic fixes for simple violations

### 1.4 Era-1 to Era-2 Migration Support
- **Backward Compatibility**: Era-1 hashes remain stable in Era-2
- **Forward Extensibility**: New complement types can be added without breaking existing hashes
- **Hash Translation Table**: Bidirectional mapping between Era-1 and Era-2 hash schemes
- **Sealability**: Era-1 complements can be sealed before Era-2 migration

---

## 2. Semantic Declaration Types

### 2.1 Declaration Taxonomy

| Type | Description | Evidence Required | Complement Type |
|------|-------------|-------------------|-----------------|
| `PHASE_DECLARATION` | Phase/Stage declarations | Phase definition files, workflows | `implement_phase` |
| `ARCHITECTURE_CLAIM` | Architecture-level claims | Architecture specs, diagrams | `create_architecture_spec` |
| `TOOL_DECLARATION` | Tool existence declarations | Tool registry, source code | `register_tool` |
| `COMPLETENESS_CLAIM` | Completeness/quality claims | Validation reports, test results | `add_verification` |
| `COMPLIANCE_CLAIM` | Compliance score declarations | Compliance reports, scores | `verify_compliance` |
| `TERMINOLOGY_REFERENCE` | Undefined terminology | Terminology registry, glossary | `define_terminology` |
| `SEALING_DECLARATION` | Sealing/closure claims | Seal records, hash registries | `implement_sealing` |
| `ERA_DECLARATION` | Era transition declarations | Era definitions, migration plans | `define_era_transition` |

### 2.2 Declaration Metadata Requirements

Every semantic declaration must include:
- **Declaration ID**: Unique identifier (e.g., `DECL-20260204-001`)
- **Declaration Type**: From the taxonomy above
- **Severity**: CRITICAL, HIGH, MEDIUM, LOW
- **Source File**: File where declaration was found
- **Line Number**: Exact location
- **Declaration Text**: Exact text of the semantic declaration
- **Evidence Requirements**: List of required evidence entities
- **Complement Requirements**: List of required complement entities

---

## 3. Complement Entity Types

### 3.1 Complement Taxonomy

| Type | Purpose | Evidence Required | Template Available |
|------|---------|-------------------|-------------------|
| `implement_phase` | Implement declared phase | Phase spec, workflow definition | ✅ Yes |
| `create_architecture_spec` | Create architecture documentation | UGS, diagrams, diagrams | ✅ Yes |
| `register_tool` | Register tool in registry | Tool source, documentation, tests | ✅ Yes |
| `add_verification` | Add validation/verification code | Test files, validators | ✅ Yes |
| `verify_compliance` | Verify compliance claims | Compliance reports, scores | ✅ Yes |
| `define_terminology` | Define undefined terms | Glossary entries, definitions | ✅ Yes |
| `implement_sealing` | Implement sealing mechanism | Seal protocol, hash registry | ✅ Yes |
| `define_era_transition` | Define era transition plan | Era definitions, migration plan | ✅ Yes |

### 3.2 Complement Metadata Requirements

Every complement must include:
- **Complement ID**: Unique identifier (e.g., `COMP-20260204-001`)
- **Complement Type**: From the taxonomy above
- **Declaration ID**: Links to the semantic declaration
- **Priority**: CRITICAL, HIGH, MEDIUM, LOW
- **Status**: PENDING, IN_PROGRESS, COMPLETED, VERIFIED, SEALED
- **Estimated Effort**: Hours required for completion
- **Template File**: Path to template file
- **Target File**: Path where complement should be created
- **Evidence Files**: List of evidence files generated
- **Verification Status**: PENDING, PASSED, FAILED

---

## 4. Complement Generation Workflow

### 4.1 Five-Stage Process

```
┌─────────────────┐
│  Stage 1: Scan  │ Scan reports for semantic declarations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Stage 2: Match  │ Match declarations to existing entities
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Stage 3: Detect │ Detect missing entities
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Stage 4: Generate│ Generate complement templates
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Stage 5: Verify │ Verify complement completeness
└─────────────────┘
```

### 4.2 Stage Details

**Stage 1: Scan**
- Input: Report files (*.md) in `/workspace/reports/`
- Output: List of semantic declarations
- Process:
  1. Parse all report files
  2. Extract semantic declarations using pattern matching
  3. Classify declarations by type
  4. Assign severity based on context

**Stage 2: Match**
- Input: Semantic declarations from Stage 1
- Output: Declaration-to-entity mappings
- Process:
  1. For each declaration, search for matching entities
  2. Search in: `/workspace/ecosystem/`, `/workspace/`
  3. Match criteria: file paths, naming patterns, content
  4. Record matches with confidence scores

**Stage 3: Detect**
- Input: Declaration-to-entity mappings from Stage 2
- Output: List of missing entities
- Process:
  1. Identify declarations with no matching entities
  2. Identify declarations with low-confidence matches
  3. Determine complement type for each missing entity
  4. Assign priority based on declaration severity

**Stage 4: Generate**
- Input: Missing entities from Stage 3
- Output: Complement templates and reports
- Process:
  1. For each missing entity, load appropriate template
  2. Fill template with context-specific information
  3. Generate complement file in appropriate location
  4. Apply RFC 8785 canonicalization
  5. Generate SHA256 hash for each complement
  6. Write complement to hash registry

**Stage 5: Verify**
- Input: Generated complements from Stage 4
- Output: Verification report
- Process:
  1. Validate complement structure
  2. Verify semantic alignment with original declaration
  3. Check compliance with governance rules
  4. Generate verification score
  5. Write verification to event stream

---

## 5. Proof-Carrying Complements

### 5.1 Complement Structure

```json
{
  "complement_id": "COMP-20260204-001",
  "complement_type": "implement_phase",
  "declaration_id": "DECL-20260204-001",
  "declaration_text": "Phase 1: Semantic Definition",
  "priority": "CRITICAL",
  "status": "PENDING",
  "generated_at": "2026-02-04T22:30:00Z",
  "template_used": "templates/phase-template.md",
  "target_file": "ecosystem/governance/phases/phase-1-semantic-definition.md",
  "evidence_files": [],
  "verification_status": "PENDING",
  "sha256_hash": "abc123...",
  "canonicalization_version": "1.0",
  "canonicalization_method": "JCS+LayeredSorting",
  "proof_chain": {
    "self": "abc123...",
    "declaration": "def456...",
    "template": "ghi789..."
  }
}
```

### 5.2 Hash Chain Architecture

```
Declaration Hash
     │
     ├─→ Complement Hash
     │       │
     │       ├─→ Template Hash
     │       │
     │       └─→ Evidence Hashes
     │
     └─→ Verification Hash
```

### 5.3 Canonicalization Requirements

- **Method**: RFC 8785 (JCS) + Layered Sorting Protocol
- **Layer 1 (Core)**: Fields that never change (id, type, declaration_id, priority)
- **Layer 2 (Optional)**: Fields that can be added (metadata, estimated_effort)
- **Layer 3 (Extension)**: Fields that can be infinitely expanded (custom_fields)
- **Sorting**: L1 before L2, L2 before L3
- **Encoding**: UTF-8

---

## 6. Semantic Integrity Constraints

### 6.1 Constraint Categories

**Type Constraints**
- Complement type must match declaration type
- Template must exist for complement type
- Target file path must follow naming conventions

**Evidence Constraints**
- All required evidence must be present
- Evidence must be valid and accessible
- Evidence hashes must match content

**Compliance Constraints**
- Complement must comply with governance rules
- Must pass naming convention checks
- Must pass security checks

**Semantic Constraints**
- Complement must align with original declaration
- Must not contradict governance specifications
- Must not introduce new semantic violations

### 6.2 Violation Handling

| Severity | Action | Auto-Fix | Human Review |
|----------|--------|----------|--------------|
| CRITICAL | BLOCK | ❌ | ✅ Yes |
| HIGH | BLOCK | ⚠️ Partial | ✅ Yes |
| MEDIUM | WARN | ✅ Yes | ⚠️ Optional |
| LOW | LOG | ✅ Yes | ❌ No |

---

## 7. Era-1 to Era-2 Migration

### 7.1 Backward Compatibility

**Era-1 Hash Stability**
- All Era-1 complement hashes remain stable in Era-2
- Hash registry maintains Era-1 entries
- New Era-2 hashes added alongside Era-1 hashes

**Hash Translation Table**
```json
{
  "era_1_hash": "abc123...",
  "era_2_hash": "xyz789...",
  "translation_timestamp": "2026-02-04T22:30:00Z",
  "migration_reason": "era_2_transition"
}
```

### 7.2 Forward Extensibility

**New Complement Types**
- Can be added in Era-2 without breaking Era-1 hashes
- Layer 3 (Extension) fields support infinite expansion
- New layers can be added (Layer 4, 5, ...) with proper versioning

**New Metadata Fields**
- Can be added to existing complements
- Do not affect Layer 1 (Core) hashes
- Documented in complement specification updates

---

## 8. Verification & Validation

### 8.1 Complement Verification

**Structural Verification**
- JSON schema validation
- Required field presence
- Field type correctness
- Hash format validation

**Semantic Verification**
- Declaration-to-complement alignment
- Compliance with governance rules
- Semantic consistency checks

**Integrity Verification**
- Hash chain verification
- Canonicalization correctness
- Evidence hash verification

### 8.2 Compliance Scoring

```
Complement Compliance Score = (Structural * 30%) + (Semantic * 40%) + (Integrity * 30%)

Where:
- Structural: 0-100 based on schema validation
- Semantic: 0-100 based on semantic alignment
- Integrity: 0-100 based on hash verification
```

**Thresholds:**
- **PASS**: ≥85.0 - Complement is valid and can be sealed
- **WARNING**: 70.0-84.9 - Complement valid but needs review
- **FAIL**: <70.0 - Complement invalid, must be regenerated

---

## 9. CLI Interface

### 9.1 Commands

```bash
# Scan reports and generate complements
python ecosystem/tools/materialization_complement_generator.py \
  --scan-reports \
  --generate-complements \
  --verify-complements \
  --verbose

# Scan only (no generation)
python ecosystem/tools/materialization_complement_generator.py \
  --scan-reports \
  --output-file reports/scan-results.json

# Generate specific complement type
python ecosystem/tools/materialization_complement_generator.py \
  --complement-type implement_phase \
  --declaration-id DECL-20260204-001

# Verify existing complements
python ecosystem/tools/materialization_complement_generator.py \
  --verify-complements \
  --complements-dir complements/

# Generate report
python ecosystem/tools/materialization_complement_generator.py \
  --generate-report \
  --report-file reports/complement-report.md
```

### 9.2 Output Formats

**JSON Format**
```json
{
  "scan_results": {
    "total_declarations": 150,
    "total_missing_entities": 75,
    "declaration_types": { ... }
  },
  "complements": [
    {
      "complement_id": "COMP-20260204-001",
      "complement_type": "implement_phase",
      ...
    }
  ],
  "verification_results": {
    "total_complements": 75,
    "passed": 70,
    "failed": 5,
    "compliance_score": 93.3
  }
}
```

**Markdown Format**
- Human-readable report
- Summary statistics
- Declaration breakdown by type
- Complement list with status
- Verification results
- Recommendations

---

## 10. Integration Points

### 10.1 Workflow Integration

```
┌─────────────────┐
│ enforce.py      │ 18/18 checks PASS
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ enforce.rules.py│ 10-step closed loop
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ materialization_        │ Scan reports → Generate
│ complement_generator.py │ complements → Verify
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│ semantic_       │ Validate complements
│ validator.py    │ (semantic alignment)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ verify_         │ Verify evidence
│ compliance.py   │ (file, events, artifacts)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ generate_       │ Seal complements
│ core_hash.py    │ (SHA256 hash registry)
└─────────────────┘
```

### 10.2 Event Stream Integration

All complement generation events written to:
- `ecosystem/.governance/event-stream.jsonl`
- Event types:
  - `COMPLEMENT_SCAN_STARTED`
  - `DECLARATION_DETECTED`
  - `COMPLEMENT_GENERATED`
  - `COMPLEMENT_VERIFIED`
  - `COMPLEMENT_SEALED`

### 10.3 Hash Registry Integration

All complements registered in:
- `ecosystem/.governance/hash-registry.json`
- Structure:
```json
{
  "complements": {
    "COMP-20260204-001": {
      "sha256_hash": "abc123...",
      "file_path": "complements/phase-1.md",
      "canonicalization": "JCS+LayeredSorting",
      "era": "1"
    }
  }
}
```

---

## 11. Appendix A: Declaration Patterns

### 11.1 Phase Declaration Patterns

```regex
Phase\s+\d+:.+?Definition
第\s*\d+\s*階段:.*定義
Stage\s+\d+:.+?Specification
```

### 11.2 Architecture Claim Patterns

```regex
治理平台.*完成
Governance Platform.*Complete
完整.*閉環.*建立
Complete.*Closed Loop.*Established
```

### 11.3 Tool Declaration Patterns

```regex
使用.*工具.*來.*
Using.*tool.*to.*
已.*創建.*工具
Created.*tool
```

### 11.4 Compliance Claim Patterns

```regex
100%.*合規
100%.*Compliant
完全.*符合.*規範
Fully.*Compliant.*With.*Specification
```

---

## 12. Appendix B: Template Locations

### 12.1 Template Directory Structure

```
complements/
├── templates/
│   ├── phase-template.md
│   ├── architecture-spec-template.md
│   ├── tool-registration-template.md
│   ├── verification-template.md
│   ├── compliance-template.md
│   ├── terminology-template.md
│   ├── sealing-template.md
│   └── era-transition-template.md
├── generated/
│   ├── phases/
│   ├── architecture/
│   ├── tools/
│   ├── verifications/
│   ├── compliances/
│   ├── terminologies/
│   ├── sealings/
│   └── era-transitions/
└── reports/
    ├── complement-scan-report.md
    ├── complement-generation-report.md
    └── complement-verification-report.md
```

---

## 13. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-03 | Initial specification |
| 2.0.0 | 2026-02-04 | Added RFC 8785 canonicalization, proof-carrying artifacts, semantic integrity constraints |

---

**End of Specification v2.0**