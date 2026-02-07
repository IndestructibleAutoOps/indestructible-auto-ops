# SHA Storage Specification v1.0
## Era-1 Canonical Pipeline - Governance-Defined Hash Storage

---

## 📋 Document Control

| Field | Value |
|-------|-------|
| **Specification** | SHA Storage Specification |
| **Version** | 1.0.0 |
| **Era** | 1 (Evidence-Native Bootstrap) |
| **Status** | ACTIVE |
| **Canonicalization Method** | JCS (RFC 8785) + LayeredSorting |
| **Hash Algorithm** | SHA-256 |
| **Governance Level** | CRITICAL |

---

## 🎯 Core Governance Principle

> **SHA storage locations are defined by governance specifications, NOT by programmatic decisions.**

This is a **fundamental principle** of the Era-1 canonical pipeline. Without governance-defined storage:
- Hashes may scatter across artifacts without consistency
- Event streams lack integrity verification
- Hash registries cannot be generated
- Materialization complements cannot reference hashes
- Micro-closed loops cannot be established
- Era-2 migration cannot be initiated

This creates **semantic holes** in the governance layer.

---

## 📐 Three-Layer Hash Storage Architecture

### Layer 1: Artifact Hash (Entity Level)
**Purpose**: Hash of individual artifact canonical form

**Storage Location**:
```
ecosystem/.evidence/{artifact-type}/{artifact-id}.json
```

**Field Schema**:
```json
{
  "artifact_id": "uuid-v4",
  "canonical_hash": "<sha256>",
  "canonicalization_version": "1.0",
  "canonicalization_method": "JCS+LayeredSorting",
  "sha256_hash": "<sha256>",  // Legacy compatibility (Era-1 only)
  "hash_chain": {
    "self": "<sha256>",
    "parent": "<parent-sha256>",  // If part of chain
    "merkle_root": "<merkle-root>"  // If part of Merkle tree
  }
}
```

**Mandatory Fields**:
- ✅ `canonical_hash`: SHA256 of canonical form (JCS)
- ✅ `canonicalization_version`: "1.0"
- ✅ `canonicalization_method`: "JCS+LayeredSorting"
- ✅ `hash_chain.self`: Self hash

**Optional Fields** (Era-2):
- ⏸️ `hash_chain.parent`: Parent hash in lineage
- ⏸️ `hash_chain.merkle_root`: Merkle tree root
- ⏸️ `hash_chain.proof`: Merkle proof

---

### Layer 2: Event Stream Hash (Event Level)
**Purpose**: Hash of individual event for integrity verification

**Storage Location**:
```
ecosystem/.governance/event-stream.jsonl
```

**Field Schema** (EACH event line):
```json
{
  "event_id": "uuid-v4",
  "event_type": "STEP_EXECUTED | ARTIFACT_CREATED | VIOLATION_DETECTED",
  "timestamp": "ISO8601",
  "era": "1",
  
  // Hash fields (CRITICAL - MANDATORY)
  "canonical_hash": "<sha256>",
  "canonicalization_version": "1.0",
  "canonicalization_method": "JCS+LayeredSorting",
  
  // Event-specific fields
  "step_number": 1,
  "artifact_file": "ecosystem/.evidence/step-1.json",
  "artifact_hash": "<artifact-sha256>",
  
  // Hash chain
  "hash_chain": {
    "self": "<sha256>",
    "previous_event": "<previous-event-sha256>",
    "previous_artifact": "<previous-artifact-sha256>"
  }
}
```

**Mandatory Fields**:
- ✅ `canonical_hash`: SHA256 of canonical event
- ✅ `canonicalization_version`: "1.0"
- ✅ `canonicalization_method`: "JCS+LayeredSorting"
- ✅ `hash_chain.self`: Self hash
- ✅ `hash_chain.previous_event`: Previous event hash
- ✅ `hash_chain.previous_artifact`: Previous artifact hash

**Hash Chain Integrity**:
- Each event links to previous event AND previous artifact
- Enables event stream replay verification
- Supports tamper detection

---

### Layer 3: Hash Registry (Governance Level)
**Purpose**: Central hash registry for Era-1 → Era-2 migration and bidirectional mapping

**Storage Location**:
```
ecosystem/.governance/hash-registry.json
```

**Field Schema**:
```json
{
  "specification_version": "1.0",
  "era": "1",
  "generated_at": "ISO8601",
  "canonicalization_method": "JCS+LayeredSorting",
  
  // Hash categories
  "artifacts": {
    "step-1": "<sha256>",
    "step-2": "<sha256>",
    ...
    "step-10": "<sha256>"
  },
  
  "events": {
    "event-count": 345,
    "first-event": "<sha256>",
    "last-event": "<sha256>",
    "merkle-root": "<merkle-root>"
  },
  
  // Era migration support (Era-2)
  "era1_to_era2": {},
  "era2_to_era1": {},
  
  // Hash chains
  "hash_chains": {
    "artifact_chain": ["<sha256-1>", "<sha256-2>", ...],
    "event_chain": ["<sha256-1>", "<sha256-2>", ...]
  },
  
  // Merkle tree (Era-2 optional)
  "merkle_tree": {
    "enabled": false,
    "root": null,
    "proofs": {}
  },
  
  // Integrity verification
  "integrity": {
    "total_hashes": 10,
    "verified": true,
    "verification_timestamp": "ISO8601"
  }
}
```

**Mandatory Fields (Era-1)**:
- ✅ `artifacts.*`: All artifact hashes
- ✅ `events.event-count`: Total event count
- ✅ `events.first-event`: First event hash
- ✅ `events.last-event`: Last event hash
- ✅ `hash_chains.artifact_chain`: Ordered artifact hashes
- ✅ `hash_chains.event_chain`: Ordered event hashes
- ✅ `integrity.total_hashes`: Total hash count
- ✅ `integrity.verified`: Verification status

**Optional Fields (Era-2)**:
- ⏸️ `era1_to_era2`: Era-1 → Era-2 mapping
- ⏸️ `era2_to_era1`: Era-2 → Era-1 mapping
- ⏸️ `events.merkle-root`: Merkle tree root
- ⏸️ `merkle_tree.enabled`: Merkle tree support
- ⏸️ `merkle_tree.root`: Merkle tree root

---

## 🔄 Hash Chain Architecture

### Artifact Chain
```
step-1.json → step-2.json → step-3.json → ... → step-10.json
   ↓               ↓               ↓
   <hash-1>        <hash-2>        <hash-3>        → hash_registry.json
```

**Purpose**: Link artifacts in execution order

**Implementation**:
```python
artifact_chain = [hash1, hash2, hash3, ..., hash10]
hash_registry["hash_chains"]["artifact_chain"] = artifact_chain
```

### Event Chain
```
event-1 → event-2 → event-3 → ... → event-345
   ↓          ↓          ↓
   <hash-1>   <hash-2>   <hash-3>   → hash_registry.json
```

**Purpose**: Link events in temporal order

**Implementation**:
```python
event_chain = [event_hash1, event_hash2, ..., event_hash345]
hash_registry["hash_chains"]["event_chain"] = event_chain
```

### Combined Chain
```
Artifact Chain ↔ Event Chain ↔ Hash Registry
      ↓                  ↓               ↓
   10 artifacts      345 events      Central mapping
```

**Purpose**: Full traceability from artifacts → events → registry

---

## 📊 Hash Verification Requirements

### 1. Artifact Verification
**Check**: `canonical_hash` matches recomputed canonical form

**Procedure**:
```python
def verify_artifact_hash(artifact_file):
    artifact = load_json(artifact_file)
    
    # Canonicalize artifact (excluding hash fields)
    data = {k: v for k, v in artifact.items() 
            if k not in ["canonical_hash", "sha256_hash", "hash_chain"]}
    
    canonical_str = canonicalize_json(data)
    computed_hash = sha256(canonical_str)
    
    expected_hash = artifact["canonical_hash"]
    
    return computed_hash == expected_hash
```

**Enforcement**: CRITICAL - Block non-compliant artifacts

---

### 2. Event Stream Verification
**Check**: Each event's `canonical_hash` and `hash_chain` integrity

**Procedure**:
```python
def verify_event_stream(event_stream_file):
    events = load_jsonl(event_stream_file)
    previous_event_hash = None
    previous_artifact_hash = None
    
    for event in events:
        # Verify event hash
        event_data = {k: v for k, v in event.items() 
                      if k not in ["canonical_hash", "hash_chain"]}
        canonical_str = canonicalize_json(event_data)
        computed_hash = sha256(canonical_str)
        
        if computed_hash != event["canonical_hash"]:
            return False, f"Event hash mismatch: {event['event_id']}"
        
        # Verify hash chain
        if event["hash_chain"]["previous_event"] != previous_event_hash:
            return False, f"Event chain broken: {event['event_id']}"
        
        if event["hash_chain"]["previous_artifact"] != previous_artifact_hash:
            return False, f"Artifact chain broken: {event['event_id']}"
        
        previous_event_hash = event["hash_chain"]["self"]
        previous_artifact_hash = event.get("artifact_hash")
    
    return True, "Event stream verified"
```

**Enforcement**: CRITICAL - Block tampered event streams

---

### 3. Hash Registry Verification
**Check**: Registry integrity and consistency

**Procedure**:
```python
def verify_hash_registry(registry_file, evidence_dir, event_stream_file):
    registry = load_json(registry_file)
    
    # Verify all artifact hashes
    for artifact_name, expected_hash in registry["artifacts"].items():
        artifact_file = evidence_dir / f"{artifact_name}.json"
        artifact = load_json(artifact_file)
        
        if artifact["canonical_hash"] != expected_hash:
            return False, f"Artifact hash mismatch: {artifact_name}"
    
    # Verify event counts
    events = load_jsonl(event_stream_file)
    if len(events) != registry["events"]["event-count"]:
        return False, f"Event count mismatch"
    
    # Verify first/last event hashes
    first_event_hash = events[0]["canonical_hash"]
    last_event_hash = events[-1]["canonical_hash"]
    
    if first_event_hash != registry["events"]["first-event"]:
        return False, f"First event hash mismatch"
    
    if last_event_hash != registry["events"]["last-event"]:
        return False, f"Last event hash mismatch"
    
    # Verify hash chains
    if registry["hash_chains"]["artifact_chain"] != get_artifact_chain(evidence_dir):
        return False, f"Artifact chain mismatch"
    
    if registry["hash_chains"]["event_chain"] != get_event_chain(events):
        return False, f"Event chain mismatch"
    
    return True, "Hash registry verified"
```

**Enforcement**: CRITICAL - Block inconsistent registries

---

## 🏗️ Implementation Requirements

### 1. Artifact Hash Generation

**When**: Every time an artifact is created or modified

**Where**: In `_generate_artifact()` method

**Requirements**:
```python
def _generate_artifact(self, step_number, result):
    # ... existing code ...
    
    # Create layered structure
    layered_data = self._create_layered_artifact(artifact_data)
    
    # Canonicalize and hash
    canonical_str = canonicalize_json(layered_data)
    canonical_hash = sha256(canonical_str)
    
    # Add hash fields (governance-defined)
    artifact_data["canonical_hash"] = canonical_hash
    artifact_data["canonicalization_version"] = "1.0"
    artifact_data["canonicalization_method"] = "JCS+LayeredSorting"
    artifact_data["sha256_hash"] = canonical_hash  # Legacy compatibility
    
    # Add hash chain (Era-1: self only)
    artifact_data["hash_chain"] = {
        "self": canonical_hash,
        "parent": None,  # Era-1: no parent
        "merkle_root": None  # Era-1: no Merkle tree
    }
    
    # ... rest of code ...
```

---

### 2. Event Hash Generation

**When**: Every time an event is written to event stream

**Where**: In `_write_step_event()` method

**Requirements**:
```python
def _write_step_event(self, step_number, artifact_file, result):
    # ... existing code ...
    
    # Get previous hashes
    previous_event_hash = self._get_last_event_hash()
    previous_artifact_hash = self._get_last_artifact_hash()
    
    # Canonicalize event
    event_data = {
        "event_id": event_id,
        "event_type": "STEP_EXECUTED",
        "timestamp": timestamp,
        "era": self.current_era(),
        "step_number": step_number,
        "artifact_file": str(artifact_file),
        "success": result.success,
        "violations_count": len(result.violations) if result.violations else 0,
        "execution_time_ms": result.execution_time_ms,
        "phase": result.phase if hasattr(result, 'phase') else f"Step_{step_number}"
    }
    
    canonical_str = canonicalize_json(event_data)
    canonical_hash = sha256(canonical_str)
    
    # Add hash fields (governance-defined)
    event_data["canonical_hash"] = canonical_hash
    event_data["canonicalization_version"] = "1.0"
    event_data["canonicalization_method"] = "JCS+LayeredSorting"
    event_data["artifact_hash"] = artifact_hash
    
    # Add hash chain
    event_data["hash_chain"] = {
        "self": canonical_hash,
        "previous_event": previous_event_hash,
        "previous_artifact": previous_artifact_hash
    }
    
    # Write event
    with open(event_stream_file, 'a') as f:
        f.write(json.dumps(event_data, ensure_ascii=False) + '\n')
    
    # ... rest of code ...
```

---

### 3. Hash Registry Generation

**When**: At the end of each 10-step execution cycle

**Where**: In `step_10_loop_back()` method

**Requirements**:
```python
def _generate_hash_registry(self):
    # Collect all artifact hashes
    artifacts = {}
    for i in range(1, 11):
        artifact_file = self.evidence_dir / f"step-{i}.json"
        artifact = load_json(artifact_file)
        artifacts[f"step-{i}"] = artifact["canonical_hash"]
    
    # Collect event hashes
    events = load_jsonl(self.governance_dir / "event-stream.jsonl")
    event_hashes = [e["canonical_hash"] for e in events]
    
    # Build hash registry
    registry = {
        "specification_version": "1.0",
        "era": self.current_era(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "canonicalization_method": "JCS+LayeredSorting",
        
        "artifacts": artifacts,
        
        "events": {
            "event-count": len(events),
            "first-event": event_hashes[0],
            "last-event": event_hashes[-1],
            "merkle-root": None  # Era-1: no Merkle tree
        },
        
        "era1_to_era2": {},
        "era2_to_era1": {},
        
        "hash_chains": {
            "artifact_chain": list(artifacts.values()),
            "event_chain": event_hashes
        },
        
        "merkle_tree": {
            "enabled": false,
            "root": None,
            "proofs": {}
        },
        
        "integrity": {
            "total_hashes": len(artifacts) + len(events),
            "verified": True,
            "verification_timestamp": datetime.now(timezone.utc).isoformat()
        }
    }
    
    # Save registry
    registry_file = self.governance_dir / "hash-registry.json"
    with open(registry_file, 'w') as f:
        json.dump(registry, f, indent=2)
    
    return registry
```

---

## 🚨 Enforcement Rules

### CRITICAL Violations (BLOCK)

1. **Missing canonical_hash** in artifact
   - Artifact must have `canonical_hash` field
   - Block artifact generation

2. **Missing canonical_hash** in event
   - Event must have `canonical_hash` field
   - Block event writing

3. **Hash chain broken**
   - Each event must link to previous event
   - Block event stream writing

4. **Hash registry missing**
   - Registry must exist after execution cycle
   - Block execution completion

### HIGH Violations (WARN)

1. **Hash verification failed**
   - Computed hash != stored hash
   - Warn but allow (for debugging)

2. **Hash chain inconsistent**
   - Registry hashes don't match actual hashes
   - Warn and require manual review

### MEDIUM Violations (LOG)

1. **Legacy sha256_hash field**
   - Use `canonical_hash` instead
   - Log deprecation warning

---

## 📈 Era Migration Support

### Era-1 → Era-2 Migration

**Hash Translation Table**:
```json
{
  "era1_to_era2": {
    "abc123": "def456"
  },
  "era2_to_era1": {
    "def456": "abc123"
  }
}
```

**Migration Process**:
1. Generate Era-2 hashes with new canonicalization method
2. Build bidirectional mapping table
3. Update hash registry with Era-2 hashes
4. Maintain Era-1 hashes for backward compatibility
5. Phase out Era-1 hashes after validation

**Backward Stability**:
- Era-1 hashes MUST remain stable
- Era-2 hashes MUST NOT break Era-1 hashes
- Bidirectional mapping enables smooth migration

---

## 🔍 Verification Commands

### Verify Artifact Hash
```bash
python ecosystem/tools/verify_hash.py --artifact ecosystem/.evidence/step-1.json
```

### Verify Event Stream
```bash
python ecosystem/tools/verify_hash.py --event-stream ecosystem/.governance/event-stream.jsonl
```

### Verify Hash Registry
```bash
python ecosystem/tools/verify_hash.py --registry ecosystem/.governance/hash-registry.json
```

### Verify All
```bash
python ecosystem/tools/verify_hash.py --all
```

---

## 📚 References

1. **RFC 8785**: JSON Canonicalization Scheme (JCS)
2. **W3C Verifiable Credentials**: Data Integrity specification
3. **Merkle Trees**: Cryptographic data structure for integrity verification
4. **Git Content-Addressable Storage**: Hash-based object storage
5. **Chain of Custody**: Digital evidence preservation best practices

---

## ✅ Compliance Checklist

### Era-1 Requirements

- [x] Artifact hash storage defined
- [x] Event hash storage defined
- [x] Hash registry structure defined
- [x] Hash chain architecture defined
- [x] Verification requirements defined
- [x] Implementation requirements defined
- [x] Enforcement rules defined
- [x] Era migration support defined

### Implementation Checklist

- [ ] Update `_generate_artifact()` to include hash chain
- [ ] Update `_write_step_event()` to include canonical_hash and hash chain
- [ ] Implement `_generate_hash_registry()` method
- [ ] Implement hash verification tools
- [ ] Update governance checks to enforce hash storage
- [ ] Create hash registry generation automation
- [ ] Add hash verification to CI/CD pipeline
- [ ] Test hash chain integrity

---

## 🎯 Conclusion

This specification provides a **governance-defined SHA storage architecture** for the Era-1 canonical pipeline, ensuring:

- ✅ Consistent hash storage across artifacts, events, and registry
- ✅ Hash chain integrity for tamper detection
- ✅ Era-1 → Era-2 migration support
- ✅ Backward stability for hash values
- ✅ Forward extensibility for new hash methods
- ✅ Full traceability and auditability

**Status**: Ready for implementation
**Next Step**: Implement hash storage in enforce.rules.py

---

**Specification Version**: 1.0.0
**Last Updated**: 2026-02-04
**Governance Level**: CRITICAL
**Era**: 1 (Evidence-Native Bootstrap)