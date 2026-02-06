# GL-LanguageNeutralHash Specification v1.0

## Executive Summary

This specification defines a language-neutral canonical hash system for IndestructibleAutoOps, ensuring that semantic meaning—not linguistic expression—is the basis for cryptographic hashing. This enables cross-language governance sealing, multilingual replay verification, and semantic consistency validation.

---

## Core Principle

> ✅ **Semantic Hash Independence**: Hash MUST be bound to semantic tokens/AST, NOT to language expression.

### Problem Statement

When hash is bound to Chinese language context:
- Same semantics but different language → inconsistent hashes
- Multi-language replay validation failures
- Cannot cross-language seal and verify (e.g., English auditors cannot verify Chinese hashes)

---

## Architecture Design

```
[中文輸入] ─┐
[日文輸入] ─┤
[英文輸入] ─┘
      │
      ▼
[語意轉換器 Semanticizer] → [英文語意 Token / AST] → [canonicalize + hash] → [封存]
      │
      ├──→ [多語言輸出（可選）]
      └──→ [語言對照表（Language Map）]
```

---

## Component Specifications

### 1. Semanticizer (語意轉換器)

**Purpose**: Convert natural language input from any language to English semantic tokens/AST.

**Interface**:
```python
def semanticize(text: str, lang: str = "zh") -> SemanticTokenAST:
    """
    Convert natural language to English semantic tokens.
    
    Args:
        text: Input text in any supported language
        lang: Source language code (zh, en, ja, ko, de, fr)
    
    Returns:
        SemanticTokenAST: Abstract syntax tree of semantic tokens
    """
```

**Semantic Token Format**:
```json
{
  "action": "restart_service",
  "target": "nginx",
  "timestamp": "2024-02-05T03:35:54Z",
  "actor": "self_healing_system",
  "result": "success",
  "metadata": {
    "original_lang": "zh",
    "original_text": "我們重新啟動了 nginx"
  }
}
```

**Supported Actions**:
- `restart_service`
- `deploy_artifact`
- `patch_vulnerability`
- `rollback_deployment`
- `scale_component`
- `configure_system`
- `validate_compliance`
- `execute_remediation`

**Supported Targets**:
- Service names (nginx, redis, postgres, etc.)
- Component names (frontend, backend, database, etc.)
- Environment names (production, staging, development)

---

### 2. Canonicalizer

**Purpose**: Convert semantic tokens to canonical form using RFC 8785 JCS + Enhanced Layered Sorting.

**Canonicalization Rules**:

**Layer 1: Core Fields (Immutable)**
- action
- target
- timestamp (ISO8601)
- actor
- result

**Layer 2: Optional Fields (Extensible)**
- metadata.*
- parameters.*

**Layer 3: Extension Fields (Infinitely Extensible)**
- custom_fields.*
- context.*

**Volatile Fields Excluded**:
- uuid
- trace_id
- request_id
- correlation_id
- event_id
- generated_at
- execution_time_ms

---

### 3. Language Map (語言對照表)

**Purpose**: Store all language versions with semantic token mapping.

**Format**: `language_map.json`
```json
{
  "hash": "a8f9c3b1d2e3f4...",
  "canonical_hash": "sha256:a8f9c3b1d2e3f4...",
  "semantic_tokens": {
    "action": "restart_service",
    "target": "nginx",
    "timestamp": "2024-02-05T03:35:54Z",
    "actor": "self_healing_system",
    "result": "success"
  },
  "languages": {
    "zh": {
      "text": "我們重新啟動了 nginx",
      "canonical_text": "我們重新啟動了 nginx"
    },
    "en": {
      "text": "We restarted nginx",
      "canonical_text": "We restarted nginx"
    },
    "ja": {
      "text": "nginx を再起動しました",
      "canonical_text": "nginx を再起動しました"
    }
  },
  "evidence_chain": {
    "canonical_semantic_file": "canonical_input.semantic.json",
    "hash_file": "hash_semantic.txt"
  }
}
```

---

### 4. Hash Computation

**Algorithm**: SHA256

**Process**:
```bash
# Step 1: Semanticize
python semanticizer.py "我們重新啟動了 nginx" --lang zh > semantic_tokens.json

# Step 2: Canonicalize
python canonicalizer.py semantic_tokens.json --semantic > canonical_input.semantic.json

# Step 3: Hash
sha256sum canonical_input.semantic.json > hash_semantic.txt
```

**Hash Chain**:
```json
{
  "hash_input": "a8f9c3...",
  "hash_output": "b7d2e4...",
  "hash_trace": "c1e3f5...",
  "merkle_root": "d4f6e7..."
}
```

---

## Acceptance Criteria (GL-LanguageNeutralHashSpec)

| 項目 | 驗證方式 |
|------|----------|
| 同語意不同語言 → 相同 hash | 中文與英文版本的 semantic.json hash 相同 |
| hash 與語言無關 | hash 僅來自 semantic 層，不含語言特徵 |
| 可重播、可驗證 | 任一語言輸入 → semanticize → hash → replay 驗證一致性 |
| 可封存語言對照表 | language_map.json 封存於 .evidence/ |
| 支援多語言翻譯封存 | zh, en, ja, ko, de, fr（可擴充） |

---

## Governance Assertions

### GL-LNH-001: Semantic Token Determinism
- All semantic tokens MUST be deterministic
- Same semantic content MUST produce identical tokens regardless of source language

### GL-LNH-002: Hash Semantic Binding
- Hash MUST be computed ONLY on canonical semantic representation
- Hash MUST NOT include language-specific features

### GL-LNH-003: Language Map Completeness
- All language versions MUST be stored in language_map.json
- Original language MUST be preserved in metadata

### GL-LNH-004: Cross-Language Replay
- Replay engine MUST accept input in ANY supported language
- Replay MUST produce identical hash to original semantic hash

### GL-LNH-005: Evidence Chain Integrity
- language_map.json MUST reference canonical semantic file
- Hash MUST be stored in both hash_semantic.txt and language_map.json

---

## File Structure

```
.evidence/
├── canonical-hash-chain/
│   └── 20260205-1104/
│       ├── canonical_input.zh.json
│       ├── canonical_input.en.json
│       ├── canonical_input.semantic.json
│       ├── language_map.json
│       ├── hash_semantic.txt
│       ├── hash_chain.json
│       └── merkle_root.txt
```

---

## Integration Points

### 1. Integration with enforce.rules.py
```python
# In _generate_artifact method
def _generate_artifact_with_language_neutral_hash(self, input_data, lang="zh"):
    # Semanticize
    semantic_tokens = semanticize(input_data, lang)
    
    # Canonicalize
    canonical = canonicalize_semantic(semantic_tokens)
    
    # Hash
    hash_value = sha256(canonical.encode()).hexdigest()
    
    # Generate language map
    language_map = {
        "semantic_tokens": semantic_tokens,
        "languages": {lang: input_data},
        "hash": hash_value
    }
    
    return hash_value, language_map
```

### 2. Integration with canonicalizer.py
```python
def canonicalize_semantic(obj):
    # Remove volatile fields
    clean_obj = remove_volatile_fields(obj)
    
    # Apply layered sorting
    sorted_obj = apply_layered_sorting(clean_obj)
    
    # Serialize with RFC 8785
    return json.dumps(sorted_obj, indent=2, sort_keys=True)
```

---

## Supported Languages

| Code | Language | Status |
|------|----------|--------|
| zh | Chinese (Simplified) | ✅ Primary |
| en | English | ✅ Semantic Anchor |
| ja | Japanese | ✅ Supported |
| ko | Korean | ✅ Supported |
| de | German | ✅ Supported |
| fr | French | ✅ Supported |

**Extensibility**: Language support can be added without breaking existing hashes.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-02-05 | Initial specification |

---

## References

- RFC 8785 - JSON Canonicalization Scheme (JCS)
- Multilingual Tokenization Advances - Emergent Mind (2024)
- Abstract Syntax Tree for Semantic Control (ICLR 2025)
- Blockchain Evidence Integrity Verification (2024)