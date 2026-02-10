# Canonical Hash Chain Tests Specification v1.0

## Executive Summary

This specification defines the governance requirements for **Canonical Hash Chain Tests** - verifying that every self-healing decision produces canonicalized input, output, and decision trace with hash-based evidence chain sealing.

**Core Principle:** Decisions are not "made", they are "sealed" - ensuring complete auditability and tamper-proof evidence.

---

## 1. Test Purpose

Validate that every self-healing decision produces:

- ✅ **Canonicalized input** - Deterministic JSON representation
- ✅ **Canonicalized output** - Deterministic JSON representation
- ✅ **Canonicalized decision trace** - Deterministic JSON representation
- ✅ **Hash-based evidence chain** - SHA256 hashes for all three
- ✅ **Replayability** - Can reproduce identical results
- ✅ **Tamper-proof** - Any modification is detectable

---

## 2. Canonicalization Rules

### 2.1 JSON Canonicalization (RFC 8785)

**Rules:**
1. **Key sorting**: All object keys sorted lexicographically
2. **Whitespace**: No unnecessary whitespace
3. **Encoding**: UTF-8
4. **Escaping**: Standard JSON escaping
5. **Volatile fields**: Remove or normalize fields like:
   - `timestamp`
   - `uuid`
   - `trace_id`
   - `request_id`
   - `correlation_id`

### 2.2 Example

**Original Input:**
```json
{
  "timestamp": "2026-02-05T10:54:33Z",
  "metrics": {"cpu": 0.75, "memory": 0.82},
  "trace_id": "abc-123"
}
```

**Canonicalized Input:**
```json
{"metrics":{"cpu":0.75,"memory":0.82}}
```

---

## 3. Test Steps (Canonical Flow)

| Step | Description |
|------|-------------|
| 1️⃣ | Trigger self-healing event |
| 2️⃣ | Extract canonicalized input |
| 3️⃣ | Extract canonicalized output |
| 4️⃣ | Extract canonicalized decision trace |
| 5️⃣ | Compute SHA256 hashes |
| 6️⃣ | Write to `.evidence/YYYYMMDD-HHMMSS/` |
| 7️⃣ | Verify replayability |
| 8️⃣ | Verify tamper-proof |

---

## 4. Evidence Directory Structure

```
.evidence/
└── canonical-hash-chain/
    └── 20260205-1054/
        ├── canonical_input.json
        ├── canonical_output.json
        ├── canonical_trace.json
        ├── hash_input.txt
        ├── hash_output.txt
        ├── hash_trace.txt
        ├── merkle_root.txt
        ├── replay_verification_report.json
        └── tamper_check_report.json
```

---

## 5. Artifact Formats

### 5.1 Canonical Input
```json
{
  "event_type": "service_anomaly",
  "service_name": "api-gateway",
  "severity": "CRITICAL",
  "metrics": {
    "cpu_usage": 0.85,
    "memory_usage": 0.92,
    "request_rate": 1250.5,
    "error_rate": 0.05
  },
  "logs": [
    {
      "level": "ERROR",
      "message": "Service timeout",
      "component": "api-gateway"
    }
  ]
}
```

### 5.2 Canonical Output
```json
{
  "action": "restart_container",
  "action_parameters": {
    "service": "api-gateway",
    "container": "api-gateway-1",
    "grace_period_seconds": 30
  },
  "execution_status": "success",
  "duration_ms": 5000
}
```

### 5.3 Canonical Decision Trace
```json
{
  "steps": [
    {
      "step": 1,
      "action": "analyze_metrics",
      "input": {"metrics": {}},
      "output": {"status": "analyzed"},
      "duration_ms": 10,
      "confidence": 0.95
    },
    {
      "step": 2,
      "action": "diagnose_issue",
      "input": {"symptoms": ["high_latency", "timeout"]},
      "output": {"issue": "service_timeout", "severity": "CRITICAL"},
      "duration_ms": 25,
      "confidence": 0.92
    },
    {
      "step": 3,
      "action": "execute_restart",
      "input": {"service": "api-gateway"},
      "output": {"success": true},
      "duration_ms": 5010,
      "confidence": 0.98
    }
  ]
}
```

### 5.4 Hash Files
```
sha256:abc123def456...
```

### 5.5 Replay Verification Report
```json
{
  "test_id": "uuid-v4",
  "timestamp": "ISO8601",
  "era": 1,
  "replay_success": true,
  "input_hash_match": true,
  "output_hash_match": true,
  "trace_hash_match": true,
  "replay_engine_version": "v2.3.1",
  "replay_timestamp": "ISO8601",
  "canonical_hash": "sha256:..."
}
```

### 5.6 Tamper Check Report
```json
{
  "test_id": "uuid-v4",
  "timestamp": "ISO8601",
  "era": 1,
  "input_tamper_detected": false,
  "output_tamper_detected": false,
  "trace_tamper_detected": false,
  "verifier": "gov-hash-verifier v1.0",
  "verdict": "PASS",
  "details": [],
  "canonical_hash": "sha256:..."
}
```

---

## 6. Hash Chain Structure

### 6.1 Individual Hashes
```
hash_input = SHA256(canonical_input.json)
hash_output = SHA256(canonical_output.json)
hash_trace = SHA256(canonical_trace.json)
```

### 6.2 Merkle Root
```
hash_leaf_1 = SHA256(hash_input)
hash_leaf_2 = SHA256(hash_output)
hash_leaf_3 = SHA256(hash_trace)
hash_parent_1 = SHA256(hash_leaf_1 || hash_leaf_2)
merkle_root = SHA256(hash_parent_1 || hash_leaf_3)
```

### 6.3 Hash Chain
```
hash_chain = [
  { "artifact": "canonical_input.json", "hash": "sha256:..." },
  { "artifact": "canonical_output.json", "hash": "sha256:..." },
  { "artifact": "canonical_trace.json", "hash": "sha256:..." },
  { "merkle_root": "sha256:..." }
]
```

---

## 7. Replayability Verification

### 7.1 Process
1. Load canonical input
2. Run through replay engine
3. Generate replayed output and trace
4. Compute hashes of replayed artifacts
5. Compare with original hashes

### 7.2 Success Criteria
- `replay_success`: true
- `input_hash_match`: true
- `output_hash_match`: true
- `trace_hash_match`: true

---

## 8. Tamper-Proof Verification

### 8.1 Process
1. Load canonical artifacts
2. Compute current hashes
3. Compare with stored hashes
4. Verify hash chain integrity
5. Verify Merkle root

### 8.2 Failure Detection
- `input_tamper_detected`: true if hash mismatch
- `output_tamper_detected`: true if hash mismatch
- `trace_tamper_detected`: true if hash mismatch
- `verdict`: "FAIL" if any tampering detected

---

## 9. Governance Assertions

### Required Assertions
- `all_inputs_canonicalized`
- `all_outputs_canonicalized`
- `all_traces_canonicalized`
- `all_hashes_computed`
- `all_hashes_stored`
- `replayability_verified`
- `tamper_proof_verified`
- `hash_chain_intact`
- `merkle_root_valid`

---

## 10. Era-1 Requirements

### Mandatory
- ✅ Canonicalization framework operational
- ✅ Hash computation operational (SHA256)
- ✅ Evidence writing operational
- ✅ Replayability verification operational
- ✅ Tamper-proof verification operational
- ✅ Hash chain integrity verified
- ✅ Merkle root computation operational

### Optional (Era-2)
- 🔄 Advanced canonicalization (custom rules)
- 🔄 Multiple hash algorithms support
- 🔄 Blockchain-based sealing
- 🔄 Real-time tamper detection

---

## 11. Security Considerations

### Hash Integrity
- SHA256 for all hashes
- Canonicalization using RFC 8785
- Hash chain verification
- Merkle tree validation

### Tamper Detection
- Immutable append-only storage
- Hash verification on read
- Chain-of-custody tracking
- Merkle root verification

### Access Control
- Read-only access for audit
- Write access only for governance engine
- Admin access for governance owner

---

## 12. Best Practices

Based on global research:

1. **RFC 8785 - JSON Canonicalization Scheme (JCS)**
   - Standardized JSON canonicalization
   - Deterministic hash computation
   - Interoperability across systems

2. **Immutable Audit Log Architecture**
   - Append-only storage
   - Tamper-evident design
   - Complete audit trail

3. **Merkle Tree Data Integrity**
   - Efficient verification
   - Scalable architecture
   - Tamper-proof hashing

4. **Blockchain Evidence Management**
   - Hash chain integrity
   - Immutable evidence
   - Cryptographic verification

---

## 13. Performance Requirements

- Canonicalization: < 100ms per artifact
- Hash computation: < 50ms per artifact
- Evidence writing: < 200ms total
- Replay verification: < 500ms total
- Tamper check: < 100ms total

---

## References

1. RFC 8785 - JSON Canonicalization Scheme (JCS)
2. Immutable Audit Log Architecture - 2024 Research
3. Merkle Tree Data Integrity - 2024 Research
4. Blockchain Evidence Management - 2024 Research
5. SHA256 Cryptographic Standard

---

**Version History:**
- v1.0 (2026-02-05): Initial specification for Era-1 Canonical Hash Chain Tests