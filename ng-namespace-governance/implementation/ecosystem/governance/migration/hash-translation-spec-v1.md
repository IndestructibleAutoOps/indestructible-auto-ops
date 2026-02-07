# Hash Translation Table Specification v1.0

## Overview

This specification defines the Hash Translation Table (HTT) protocol for Era-1 → Era-2 migration. The HTT enables Era-2 to understand, verify, and replay Era-1 governance evidence chains while maintaining semantic continuity and cryptographic integrity.

## Core Principles

### 1. Semantic Continuity
- Era-2 must be able to interpret Era-1 semantic declarations
- Hash translation must preserve semantic meaning
- Multi-semantic mapping: one Era-1 hash may map to multiple Era-2 hashes for different contexts

### 2. Cryptographic Integrity
- Era-1 hashes remain immutable and never change
- Era-2 hashes are generated according to Era-2 canonicalization spec
- Translation table is itself hashed and sealed

### 3. Bidirectional Mapping
- Era-1 → Era-2: Forward mapping for migration
- Era-2 → Era-1: Reverse mapping for verification and replay
- Both mappings are immutable and append-only

### 4. Evidence Chain Preservation
- Hash chains (artifact chain, event chain) remain unbroken across Era migration
- Translation table includes chain references (parent, child)
- Merkle tree roots maintained across Eras

## Hash Translation Table Format

### Location
```
ecosystem/governance/migration/hashtranslationtable.jsonl
```

### Format (JSONL - One JSON object per line)

```json
{
  "translation_id": "uuid-v4",
  "era1_hash": "sha256:abc123...",
  "era2_hash": "sha256:def456...",
  "source_type": "artifact|event|registry|complement|governance",
  "source_path": "relative/path/to/artifact.json",
  "source_era": "era-1",
  "target_era": "era-2",
  "translation_method": "canonical_rehash|semantic_preserve|multi_semantic",
  "translated_by": "hashtranslation_engine",
  "translated_at": "2026-02-05T08:45:00Z",
  "canonicalization_v1": {
    "version": "1.0",
    "method": "JCS+LayeredSorting",
    "hash_algorithm": "SHA256"
  },
  "canonicalization_v2": {
    "version": "2.0",
    "method": "JCS+EnhancedLayeredSorting",
    "hash_algorithm": "SHA256"
  },
  "semantic_delta": {
    "fields_added": ["era2_field"],
    "fields_removed": [],
    "fields_renamed": {},
    "semantic_changes": []
  },
  "chain_references": {
    "parent": "sha256:parent_hash...",
    "children": ["sha256:child1_hash...", "sha256:child2_hash..."],
    "merkle_root": "sha256:merkle_root..."
  },
  "verification_status": "verified|pending|failed",
  "metadata": {
    "source_artifact_id": "uuid-v4",
    "target_artifact_id": "uuid-v4",
    "preserve_semantic": true,
    "preserve_chain": true
  }
}
```

## Translation Methods

### 1. Canonical Rehash (canonical_rehash)
**Use Case:** Era-2 changes canonicalization method slightly but content remains the same
**Process:**
1. Load Era-1 artifact content
2. Apply Era-2 canonicalization rules
3. Generate Era-2 hash
4. Record both hashes in HTT

**Example:**
```json
{
  "translation_method": "canonical_rehash",
  "era1_hash": "sha256:abc123...",
  "era2_hash": "sha256:def456...",
  "reason": "JCS sorting order optimization in Era-2"
}
```

### 2. Semantic Preserve (semantic_preserve)
**Use Case:** Content changes but semantic meaning is preserved
**Process:**
1. Load Era-1 artifact
2. Apply Era-2 semantic transformations
3. Generate Era-2 hash
4. Record semantic delta in HTT

**Example:**
```json
{
  "translation_method": "semantic_preserve",
  "era1_hash": "sha256:abc123...",
  "era2_hash": "sha256:def456...",
  "semantic_delta": {
    "fields_renamed": {"era1_field": "era2_field"},
    "semantic_changes": ["renamed for clarity"]
  }
}
```

### 3. Multi-Semantic (multi_semantic)
**Use Case:** One Era-1 artifact maps to multiple Era-2 artifacts
**Process:**
1. Load Era-1 artifact
2. Generate multiple Era-2 artifacts with different contexts
3. Create one HTT entry for each Era-2 artifact
4. Link them via `translation_id` and `chain_references`

**Example:**
```json
{
  "translation_id": "multi-001",
  "translation_method": "multi_semantic",
  "era1_hash": "sha256:abc123...",
  "era2_hash": "sha256:def456...",
  "context": "audit_context",
  "related_translations": ["multi-002", "multi-003"]
}
```

## Chain Preservation

### Artifact Chain
```json
{
  "chain_type": "artifact_chain",
  "era1_chain": ["sha256:step1...", "sha256:step2...", ...],
  "era2_chain": ["sha256:step1_v2...", "sha256:step2_v2...", ...],
  "chain_continuity": true
}
```

### Event Chain
```json
{
  "chain_type": "event_chain",
  "era1_chain": ["sha256:event1...", "sha256:event2...", ...],
  "era2_chain": ["sha256:event1_v2...", "sha256:event2_v2...", ...],
  "chain_continuity": true
}
```

## Verification Requirements

### 1. Forward Translation Verification
```python
def verify_forward_translation(era1_hash, era2_hash):
    # Load Era-1 artifact
    artifact = load_era1_artifact(era1_hash)
    
    # Apply Era-2 canonicalization
    era2_canonical = apply_era2_canonicalization(artifact)
    
    # Generate expected Era-2 hash
    expected_hash = sha256(era2_canonical)
    
    # Compare
    return expected_hash == era2_hash
```

### 2. Reverse Translation Verification
```python
def verify_reverse_translation(era2_hash, era1_hash):
    # Load Era-2 artifact
    artifact = load_era2_artifact(era2_hash)
    
    # Apply Era-1 canonicalization (reverse mapping)
    era1_canonical = apply_era1_canonicalization_reverse(artifact)
    
    # Generate expected Era-1 hash
    expected_hash = sha256(era1_canonical)
    
    # Compare
    return expected_hash == era1_hash
```

### 3. Chain Continuity Verification
```python
def verify_chain_continuity(htt_entries):
    # Verify parent-child relationships
    for entry in htt_entries:
        if entry['chain_references']['parent']:
            parent = find_entry_by_hash(entry['era1_hash'])
            if not parent:
                return False
    return True
```

## HTT Integrity

### HTT Hash
The HTT itself is hashed after generation:
```json
{
  "htt_hash": "sha256:htt_hash...",
  "htt_version": "1.0",
  "generated_at": "2026-02-05T08:46:00Z",
  "total_entries": 537,
  "status": "sealed"
}
```

### HTT Verification
```bash
# Verify HTT integrity
python ecosystem/tools/hash_translation_engine.py --verify-htt
```

## Migration Protocol

### Phase 1: HTT Generation
1. Scan all Era-1 artifacts
2. Generate Era-2 hashes
3. Create HTT entries
4. Verify bidirectional mappings
5. Hash and seal HTT

### Phase 2: Pilot Migration
1. Select pilot modules
2. Migrate using HTT
3. Verify semantic continuity
4. Verify hash chain continuity
4. Run parallel with Era-1

### Phase 3: Full Migration
1. Migrate all modules
2. Verify all translations
3. Verify all chains
4. Seal Era-1
5. Activate Era-2

## Security Considerations

### 1. HTT Tamper-Evidence
- HTT is append-only
- Any modification changes HTT hash
- HTT hash is recorded in Era-1 closure artifact

### 2. Verifiability
- All translations are verifiable via re-hashing
- Bidirectional mapping enables cross-verification
- Chain references enable完整性驗證

### 3. Rollback Capability
- HTT enables Era-1 → Era-2 rollback if needed
- Preserve Era-1 hashes for reference
- Store translation metadata

## Era Compatibility Matrix

| Feature | Era-1 | Era-2 | Translation |
|---------|-------|-------|-------------|
| Canonicalization | JCS+LayeredSorting v1 | JCS+EnhancedLayeredSorting v2 | canonical_rehash |
| Hash Algorithm | SHA256 | SHA256 | direct |
| Semantic Model | v1 | v2 | semantic_preserve |
| Evidence Format | JSON v1 | JSON v2 | format_preserve |
| Chain Structure | Linear | Linear + Branching | chain_extend |

## References

1. NIST SP 1800-38C - Post-Quantum Cryptography Migration
2. NIST IR 8387 - Digital Evidence Preservation
3. RFC 8785 - JSON Canonicalization Scheme (JCS)
4. Blockchain Cross-Chain Protocols - Hash Translation Patterns
5. Semantic Model Version Control - Multi-Era Compatibility

## Version History

- **v1.0** (2026-02-05): Initial specification for Era-1 → Era-2 migration