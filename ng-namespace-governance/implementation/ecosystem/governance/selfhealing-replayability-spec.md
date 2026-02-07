# Self-Healing Decision Replayability Specification v1.0

## Executive Summary

This specification defines the governance requirements for **Self-Healing Decision Replayability** - the ability to reproduce, verify, and seal every self-healing decision with hash-based evidence.

**Core Principle:** Every self-healing decision must be replayable, verifiable, and sealable, independent of model version, environment, time, or input order.

---

## 1. Decision Archival Format

### Location
```
evidence/selfhealing/decisions/<decision_id>.json
```

### Decision Artifact Schema

```json
{
  "decision_id": "uuid-v4",
  "timestamp": "ISO8601",
  "era": 1,
  "engine_version": "semantic version",
  "engine_hash": "sha256:...",
  
  "input_snapshot": {
    "metrics": "snapshots/metrics/<uuid>.json",
    "logs": "snapshots/logs/<uuid>.json",
    "topology": "snapshots/topology/<uuid>.json",
    "alerts": "snapshots/alerts/<uuid>.json"
  },
  
  "decision": {
    "output_action": "action_type",
    "action_parameters": {},
    "execution_trace": "traces/<uuid>.json"
  },
  
  "canonical_hash": "sha256:...",
  "signature": "optional_digital_signature"
}
```

### Input Snapshot Schema

**metrics.json**
```json
{
  "timestamp": "ISO8601",
  "system_metrics": {
    "cpu_usage": 0.75,
    "memory_usage": 0.82,
    "disk_io": 0.45,
    "network_io": 0.30
  },
  "application_metrics": {
    "request_rate": 1250.5,
    "error_rate": 0.02,
    "latency_p99": 150.0
  },
  "canonical_hash": "sha256:..."
}
```

**logs.json**
```json
{
  "timestamp": "ISO8601",
  "logs": [
    {
      "level": "ERROR",
      "message": "Service timeout",
      "timestamp": "ISO8601",
      "component": "api-gateway"
    }
  ],
  "canonical_hash": "sha256:..."
}
```

**topology.json**
```json
{
  "timestamp": "ISO8601",
  "services": [
    {
      "name": "api-gateway",
      "instances": 3,
      "health": "degraded",
      "dependencies": ["auth-service", "user-service"]
    }
  ],
  "canonical_hash": "sha256:..."
}
```

**alerts.json**
```json
{
  "timestamp": "ISO8601",
  "alerts": [
    {
      "severity": "CRITICAL",
      "type": "service_timeout",
      "component": "api-gateway",
      "threshold": "30s",
      "actual": "45s"
    }
  ],
  "canonical_hash": "sha256:..."
}
```

**execution_trace.json**
```json
{
  "timestamp": "ISO8601",
  "steps": [
    {
      "step": 1,
      "action": "analyze_metrics",
      "input": {},
      "output": {},
      "duration_ms": 10
    },
    {
      "step": 2,
      "action": "diagnose_issue",
      "input": {},
      "output": {"issue": "service_timeout"},
      "duration_ms": 25
    },
    {
      "step": 3,
      "action": "execute_restart",
      "input": {"service": "api-gateway"},
      "output": {"success": true},
      "duration_ms": 5000
    }
  ],
  "canonical_hash": "sha256:..."
}
```

---

## 2. Replayability Testing Framework

### Test 1: Decision Replayability
```python
def test_decision_replayability(decision_id):
    """
    Verify that a decision can be replayed and produces identical output
    """
    # 1. Load archived decision
    decision = load_decision(decision_id)
    
    # 2. Load input snapshot
    inputs = load_input_snapshot(decision.input_snapshot)
    
    # 3. Replay in isolated environment
    replayed_output = replay_decision_engine(
        inputs=inputs,
        engine_hash=decision.engine_hash
    )
    
    # 4. Verify output matches
    assert replayed_output.action == decision.output_action
    assert replayed_output.trace == decision.execution_trace
    
    return {
        "status": "passed",
        "output_match": True,
        "trace_match": True
    }
```

### Test 2: Engine Version Drift Detection
```python
def test_engine_version_drift(decision_id, target_engine_version):
    """
    Verify that using a different engine version produces expected
    semantic drift or maintains semantic consistency
    """
    # 1. Load archived decision
    decision = load_decision(decision_id)
    
    # 2. Load input snapshot
    inputs = load_input_snapshot(decision.input_snapshot)
    
    # 3. Replay with different engine version
    replayed_output = replay_decision_engine(
        inputs=inputs,
        engine_version=target_engine_version
    )
    
    # 4. Analyze semantic drift
    drift_analysis = compare_semantics(
        original=decision.output_action,
        replayed=replayed_output.action
    )
    
    return {
        "status": "passed",
        "semantic_drift": drift_analysis.drift_detected,
        "drift_magnitude": drift_analysis.magnitude
    }
```

### Test 3: Input Order Independence
```python
def test_input_order_independence(decision_id):
    """
    Verify that reordering input snapshot fields produces identical output
    """
    # 1. Load archived decision
    decision = load_decision(decision_id)
    
    # 2. Load and shuffle input snapshot
    inputs = load_input_snapshot(decision.input_snapshot)
    shuffled_inputs = shuffle_fields(inputs)
    
    # 3. Replay with shuffled inputs
    replayed_output = replay_decision_engine(
        inputs=shuffled_inputs,
        engine_hash=decision.engine_hash
    )
    
    # 4. Verify output is identical
    assert replayed_output.action == decision.output_action
    
    return {
        "status": "passed",
        "order_independence": True
    }
```

### Test 4: Canonical Hash Determinism
```python
def test_canonical_hash_determinism(decision_id):
    """
    Verify that canonical hash is deterministic across multiple computations
    """
    # 1. Load archived decision
    decision = load_decision(decision_id)
    
    # 2. Compute canonical hash 100 times
    hashes = []
    for _ in range(100):
        hash_val = compute_canonical_hash(decision)
        hashes.append(hash_val)
    
    # 3. Verify all hashes are identical
    assert len(set(hashes)) == 1
    
    return {
        "status": "passed",
        "determinism": 100.0,
        "iterations": 100
    }
```

---

## 3. Replay Engine Requirements

### Core Functions

```python
class ReplayEngine:
    def replay_decision(self, decision_id: str) -> ReplayResult:
        """
        Replay a single decision in isolated environment
        
        Returns:
            ReplayResult with output_action, execution_trace, metrics
        """
    
    def replay_batch(self, decision_ids: List[str]) -> BatchReplayResult:
        """
        Replay multiple decisions in sequence
        
        Returns:
            BatchReplayResult with individual results and aggregate metrics
        """
    
    def verify_replay(self, decision_id: str) -> VerificationResult:
        """
        Verify that replay matches original decision
        
        Returns:
            VerificationResult with match status and diff details
        """
```

### Isolation Requirements

- **Docker-based isolation**: Each replay runs in separate container
- **State isolation**: No shared state between replays
- **Resource limits**: CPU, memory, time limits enforced
- **Network isolation**: No external network access during replay

---

## 4. Sealed Test Results Format

### Location
```
evidence/tests/selfhealing/testreplayability_<decision_id>.json
```

### Test Result Schema

```json
{
  "test_id": "uuid-v4",
  "decision_id": "uuid-v4",
  "timestamp": "ISO8601",
  "era": 1,
  
  "tests": {
    "decision_replayability": {
      "status": "passed",
      "output_match": true,
      "trace_match": true,
      "duration_ms": 150
    },
    "engine_version_drift": {
      "status": "passed",
      "semantic_drift": false,
      "drift_magnitude": 0.0,
      "duration_ms": 200
    },
    "input_order_independence": {
      "status": "passed",
      "order_independence": true,
      "duration_ms": 120
    },
    "canonical_hash_determinism": {
      "status": "passed",
      "determinism": 100.0,
      "iterations": 100,
      "duration_ms": 450
    }
  },
  
  "summary": {
    "total_tests": 4,
    "passed": 4,
    "failed": 0,
    "overall_status": "passed",
    "total_duration_ms": 920
  },
  
  "canonical_hash": "sha256:...",
  "signature": "optional_digital_signature"
}
```

---

## 5. Governance Validation Rules

### YAML Specification

```yaml
version: "1.0"
era: 1
governance_owner: IndestructibleAutoOps

replay_assertions:
  - all_decisions_have_input_snapshot
  - all_decisions_have_engine_hash
  - all_decisions_are_replayable
  - all_replays_match_original_output
  - all_replays_match_original_trace
  - all_tests_are_hash_sealed
  - canonical_hash_is_deterministic
  - replay_isolated_from_environment

enforced_by:
  - replay_engine
  - test_replayability
  - test_engine_version_drift
  - test_input_order_independence
  - test_canonical_hash_determinism

canonicalization:
  method: "JCS+LayeredSorting"
  hash_algorithm: "sha256"
  layer_structure:
    - layer1: "core_fields"
    - layer2: "optional_fields"
    - layer3: "extension_fields"

sealing_requirements:
  - decision_artifact_hash_sealed
  - input_snapshot_hashes_sealed
  - execution_trace_hash_sealed
  - test_result_hash_sealed

audit_trail_requirements:
  - all_replays_logged
  - all_tests_logged
  - all_hashes_recorded
  - full_traceability_maintained

thresholds:
  replay_success_rate_min: 100.0
  output_match_rate_min: 100.0
  trace_match_rate_min: 100.0
  hash_determinism_min: 100.0
```

---

## 6. Implementation Requirements

### Must-Have Features
- ✅ Decision archival with complete input snapshot
- ✅ Engine version and hash tracking
- ✅ Replay engine with isolation
- ✅ Four replayability tests
- ✅ Sealed test results
- ✅ Hash-based verification
- ✅ Full audit trail

### Should-Have Features
- 🔄 Batch replay capability
- 🔄 Replay diff generation
- 🔄 Performance benchmarking
- 🔄 Regression detection
- 🔄 Semantic drift analysis

### Could-Have Features
- 💡 Visual replay inspector
- 💡 AI-powered drift explanation
- 💡 Automated fix suggestions
- 💡 Real-time replay monitoring

---

## 7. Era-1 to Era-2 Migration

### Era-1 Requirements
- All decisions archived with input snapshots
- Engine versions and hashes recorded
- Basic replay capability
- Hash sealing of artifacts

### Era-2 Requirements
- Full self-healing history from Era-1
- Replay across era boundaries
- Advanced semantic drift analysis
- Cross-era verification
- Hash translation table

---

## 8. Security Considerations

### Hash Integrity
- SHA256 for all hashes
- Canonicalization using JCS+LayeredSorting
- Hash chain verification

### Access Control
- Read-only access for audit
- Write access only for self-healing engine
- Signature verification for sealed artifacts

### Tamper Detection
- Immutable evidence storage
- Hash verification on read
- Chain-of-custody tracking

---

## References

1. RFC 8785 - JSON Canonicalization Scheme (JCS)
2. Deterministic Replay Systems (University of Washington)
3. Blockchain Evidence Management (IJES 2024)
4. Self-Healing Machine Learning (NeurIPS 2024)
5. Digital Evidence Preservation (IJIRSET 2024)

---

**Version History:**
- v1.0 (2026-02-05): Initial specification for Era-1 Self-Healing Replayability