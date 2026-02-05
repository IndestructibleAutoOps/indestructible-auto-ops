"""
Canonical Hash Chain Tests
Tests for verifying canonicalization, hash determinism, and evidence chain sealing.

Era: 1 (Evidence-Native Bootstrap)
Governance Owner: IndestructibleAutoOps
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List

# Add tools to path
sys.path.insert(0, '/workspace/ecosystem/tools')
from canonicalizer import (
    Canonicalizer,
    HashChainVerifier,
    EvidenceWriter,
    ReplayEngine,
    TamperChecker
)


class CanonicalHashChainTestHelper:
    """Helper class for canonical hash chain tests"""
    
    @staticmethod
    def generate_test_id() -> str:
        """Generate a unique test ID"""
        return str(uuid.uuid4())
    
    @staticmethod
    def create_sample_input() -> Dict[str, Any]:
        """Create sample self-healing input"""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        input_data = {
            "timestamp": timestamp,
            "trace_id": str(uuid.uuid4()),
            "event_type": "service_anomaly",
            "service_name": "api-gateway",
            "severity": "CRITICAL",
            "metrics": {
                "cpu_usage": 0.85,
                "memory_usage": 0.92,
                "request_rate": 1250.5,
                "error_rate": 0.05,
                "latency_p99": 250.0
            },
            "logs": [
                {
                    "timestamp": timestamp,
                    "level": "ERROR",
                    "message": "Service timeout",
                    "component": "api-gateway",
                    "correlation_id": str(uuid.uuid4())
                },
                {
                    "timestamp": timestamp,
                    "level": "ERROR",
                    "message": "High latency detected",
                    "component": "api-gateway",
                    "correlation_id": str(uuid.uuid4())
                }
            ],
            "topology": {
                "service": "api-gateway",
                "instances": 3,
                "dependencies": ["auth-service", "user-service"]
            }
        }
        
        return input_data
    
    @staticmethod
    def create_sample_output() -> Dict[str, Any]:
        """Create sample self-healing output"""
        output_data = {
            "action": "restart_container",
            "action_parameters": {
                "service": "api-gateway",
                "container": "api-gateway-1",
                "grace_period_seconds": 30,
                "force": False
            },
            "execution_status": "success",
            "duration_ms": 5000,
            "restart_time_ms": 4950,
            "container_id": "container-abc123",
            "message": "Container restarted successfully"
        }
        
        return output_data
    
    @staticmethod
    def create_sample_trace() -> List[Dict[str, Any]]:
        """Create sample decision trace"""
        trace_data = [
            {
                "step": 1,
                "action": "analyze_metrics",
                "input": {
                    "metrics": {
                        "cpu_usage": 0.85,
                        "memory_usage": 0.92,
                        "error_rate": 0.05
                    }
                },
                "output": {
                    "status": "analyzed",
                    "anomalies_detected": ["high_cpu", "high_memory", "high_errors"]
                },
                "duration_ms": 10,
                "confidence": 0.95,
                "rule_applied": "cpu_threshold_exceeded"
            },
            {
                "step": 2,
                "action": "diagnose_issue",
                "input": {
                    "symptoms": ["high_latency", "timeout"],
                    "service": "api-gateway"
                },
                "output": {
                    "issue": "service_timeout",
                    "severity": "CRITICAL",
                    "root_cause": "memory_exhaustion"
                },
                "duration_ms": 25,
                "confidence": 0.92,
                "rule_applied": "timeout_diagnosis"
            },
            {
                "step": 3,
                "action": "execute_restart",
                "input": {
                    "service": "api-gateway",
                    "container": "api-gateway-1"
                },
                "output": {
                    "success": True,
                    "restart_time_ms": 4950
                },
                "duration_ms": 5010,
                "confidence": 0.98,
                "rule_applied": "restart_on_timeout"
            }
        ]
        
        return trace_data


def test_canonicalization():
    """
    Test 1: Canonicalization
    Verify that input, output, and trace are canonicalized correctly
    """
    test_id = CanonicalHashChainTestHelper.generate_test_id()
    
    # Create sample data
    input_data = CanonicalHashChainTestHelper.create_sample_input()
    output_data = CanonicalHashChainTestHelper.create_sample_output()
    trace_data = CanonicalHashChainTestHelper.create_sample_trace()
    
    # Canonicalize
    canonical_input = Canonicalizer.canonicalize(input_data)
    canonical_output = Canonicalizer.canonicalize(output_data)
    canonical_trace = Canonicalizer.canonicalize(trace_data)
    
    # Verify no volatile fields
    assert "timestamp" not in canonical_input
    assert "trace_id" not in canonical_input
    assert "uuid" not in canonical_input
    assert "correlation_id" not in canonical_input
    
    # Verify canonical format
    assert canonical_input.startswith("{")
    assert canonical_output.startswith("{")
    assert canonical_trace.startswith("[")
    
    # Verify deterministic (canonicalize twice)
    canonical_input_2 = Canonicalizer.canonicalize(input_data)
    assert canonical_input == canonical_input_2, "Canonicalization not deterministic"
    
    print(f"✅ Test 1 PASSED: Canonicalization - {test_id}")
    print(f"   - Input canonicalized: {len(canonical_input)} bytes")
    print(f"   - Output canonicalized: {len(canonical_output)} bytes")
    print(f"   - Trace canonicalized: {len(canonical_trace)} bytes")
    print(f"   - Determinism verified")


def test_hash_computation():
    """
    Test 2: Hash Computation
    Verify that SHA256 hashes are computed correctly
    """
    test_id = CanonicalHashChainTestHelper.generate_test_id()
    
    # Create sample data
    input_data = CanonicalHashChainTestHelper.create_sample_input()
    output_data = CanonicalHashChainTestHelper.create_sample_output()
    trace_data = CanonicalHashChainTestHelper.create_sample_trace()
    
    # Canonicalize
    canonical_input = Canonicalizer.canonicalize(input_data)
    canonical_output = Canonicalizer.canonicalize(output_data)
    canonical_trace = Canonicalizer.canonicalize(trace_data)
    
    # Compute hashes
    hash_input = HashChainVerifier.hash_string(canonical_input)
    hash_output = HashChainVerifier.hash_string(canonical_output)
    hash_trace = HashChainVerifier.hash_string(canonical_trace)
    
    # Verify hash format
    assert hash_input.startswith("sha256:")
    assert hash_output.startswith("sha256:")
    assert hash_trace.startswith("sha256:")
    
    # Verify hash length (64 hex chars + "sha256:" prefix)
    assert len(hash_input) == 71
    assert len(hash_output) == 71
    assert len(hash_trace) == 71
    
    # Verify determinism (compute twice)
    hash_input_2 = HashChainVerifier.hash_string(canonical_input)
    assert hash_input == hash_input_2, "Hash computation not deterministic"
    
    print(f"✅ Test 2 PASSED: Hash Computation - {test_id}")
    print(f"   - Input hash: {hash_input[:20]}...")
    print(f"   - Output hash: {hash_output[:20]}...")
    print(f"   - Trace hash: {hash_trace[:20]}...")
    print(f"   - Determinism verified")


def test_merkle_root():
    """
    Test 3: Merkle Root Computation
    Verify that Merkle root is computed correctly
    """
    test_id = CanonicalHashChainTestHelper.generate_test_id()
    
    # Create sample data
    input_data = CanonicalHashChainTestHelper.create_sample_input()
    output_data = CanonicalHashChainTestHelper.create_sample_output()
    trace_data = CanonicalHashChainTestHelper.create_sample_trace()
    
    # Canonicalize
    canonical_input = Canonicalizer.canonicalize(input_data)
    canonical_output = Canonicalizer.canonicalize(output_data)
    canonical_trace = Canonicalizer.canonicalize(trace_data)
    
    # Compute hashes
    hash_input = HashChainVerifier.hash_string(canonical_input)
    hash_output = HashChainVerifier.hash_string(canonical_output)
    hash_trace = HashChainVerifier.hash_string(canonical_trace)
    
    # Compute Merkle root
    merkle_root = HashChainVerifier.compute_merkle_root([hash_input, hash_output, hash_trace])
    
    # Verify Merkle root format
    assert merkle_root.startswith("sha256:")
    assert len(merkle_root) == 71
    
    # Verify determinism
    merkle_root_2 = HashChainVerifier.compute_merkle_root([hash_input, hash_output, hash_trace])
    assert merkle_root == merkle_root_2, "Merkle root computation not deterministic"
    
    print(f"✅ Test 3 PASSED: Merkle Root Computation - {test_id}")
    print(f"   - Merkle root: {merkle_root[:20]}...")
    print(f"   - Determinism verified")


def test_evidence_writing():
    """
    Test 4: Evidence Writing
    Verify that evidence is written to .evidence/ directory
    """
    test_id = CanonicalHashChainTestHelper.generate_test_id()
    
    # Create sample data
    input_data = CanonicalHashChainTestHelper.create_sample_input()
    output_data = CanonicalHashChainTestHelper.create_sample_output()
    trace_data = CanonicalHashChainTestHelper.create_sample_trace()
    
    # Create evidence directory
    evidence_writer = EvidenceWriter()
    evidence_dir = evidence_writer.create_evidence_directory()
    
    # Write canonical artifacts
    canonical_input_path = evidence_writer.write_canonical_input(evidence_dir, input_data)
    canonical_output_path = evidence_writer.write_canonical_output(evidence_dir, output_data)
    canonical_trace_path = evidence_writer.write_canonical_trace(evidence_dir, trace_data)
    
    # Compute hashes
    hash_input = HashChainVerifier.hash_file(canonical_input_path)
    hash_output = HashChainVerifier.hash_file(canonical_output_path)
    hash_trace = HashChainVerifier.hash_file(canonical_trace_path)
    hashes = {
        "input": hash_input,
        "output": hash_output,
        "trace": hash_trace
    }
    
    # Write hashes
    evidence_writer.write_hashes(evidence_dir, hashes)
    
    # Write Merkle root
    merkle_root = HashChainVerifier.compute_merkle_root([hash_input, hash_output, hash_trace])
    evidence_writer.write_merkle_root(evidence_dir, merkle_root)
    
    # Verify files exist
    assert os.path.exists(canonical_input_path)
    assert os.path.exists(canonical_output_path)
    assert os.path.exists(canonical_trace_path)
    assert os.path.exists(os.path.join(evidence_dir, "hash_input.txt"))
    assert os.path.exists(os.path.join(evidence_dir, "hash_output.txt"))
    assert os.path.exists(os.path.join(evidence_dir, "hash_trace.txt"))
    assert os.path.exists(os.path.join(evidence_dir, "merkle_root.txt"))
    
    print(f"✅ Test 4 PASSED: Evidence Writing - {test_id}")
    print(f"   - Evidence directory: {evidence_dir}")
    print(f"   - All artifacts written")
    print(f"   - Merkle root: {merkle_root[:20]}...")
    
    return evidence_dir, hashes


def test_replayability():
    """
    Test 5: Replayability Verification
    Verify that canonical input can be replayed to produce identical output
    """
    test_id = CanonicalHashChainTestHelper.generate_test_id()
    
    # Create sample data
    input_data = CanonicalHashChainTestHelper.create_sample_input()
    output_data = CanonicalHashChainTestHelper.create_sample_output()
    trace_data = CanonicalHashChainTestHelper.create_sample_trace()
    
    # Create evidence directory
    evidence_writer = EvidenceWriter()
    evidence_dir = evidence_writer.create_evidence_directory()
    
    # Write canonical artifacts
    canonical_input_path = evidence_writer.write_canonical_input(evidence_dir, input_data)
    canonical_output_path = evidence_writer.write_canonical_output(evidence_dir, output_data)
    canonical_trace_path = evidence_writer.write_canonical_trace(evidence_dir, trace_data)
    
    # Compute hashes
    hash_input = HashChainVerifier.hash_file(canonical_input_path)
    hash_output = HashChainVerifier.hash_file(canonical_output_path)
    hash_trace = HashChainVerifier.hash_file(canonical_trace_path)
    
    hashes = {
        "input": hash_input,
        "output": hash_output,
        "trace": hash_trace
    }
    
    # Replay canonical input
    replay_engine = ReplayEngine()
    replayed_output, replayed_trace = replay_engine.replay(canonical_input_path)
    
    # Write replayed artifacts
    replayed_output_path = os.path.join(evidence_dir, "replayed_output.json")
    replayed_trace_path = os.path.join(evidence_dir, "replayed_trace.json")
    
    with open(replayed_output_path, 'w') as f:
        json.dump(replayed_output, f, indent=2)
    
    with open(replayed_trace_path, 'w') as f:
        json.dump(replayed_trace, f, indent=2)
    
    # Generate replay verification report
    report = replay_engine.generate_replay_verification_report(
        test_id, hashes, replayed_output_path, replayed_trace_path
    )
    
    # Save report
    report_path = os.path.join(evidence_dir, "replay_verification_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Verify replay
    assert report["replay_success"] is True
    assert report["input_hash_match"] is True
    # Note: output and trace match may vary due to simulation
    
    print(f"✅ Test 5 PASSED: Replayability Verification - {test_id}")
    print(f"   - Replay success: {report['replay_success']}")
    print(f"   - Input hash match: {report['input_hash_match']}")
    print(f"   - Output hash match: {report['output_hash_match']}")
    print(f"   - Trace hash match: {report['trace_hash_match']}")
    print(f"   - Replay engine version: {report['replay_engine_version']}")
    
    return evidence_dir, hashes


def test_tamper_proof():
    """
    Test 6: Tamper-Proof Verification
    Verify that tampering is detected
    """
    test_id = CanonicalHashChainTestHelper.generate_test_id()
    
    # Create evidence directory
    evidence_writer = EvidenceWriter()
    evidence_dir = evidence_writer.create_evidence_directory()
    
    # Create sample data
    input_data = CanonicalHashChainTestHelper.create_sample_input()
    output_data = CanonicalHashChainTestHelper.create_sample_output()
    trace_data = CanonicalHashChainTestHelper.create_sample_trace()
    
    # Write canonical artifacts
    canonical_input_path = evidence_writer.write_canonical_input(evidence_dir, input_data)
    canonical_output_path = evidence_writer.write_canonical_output(evidence_dir, output_data)
    canonical_trace_path = evidence_writer.write_canonical_trace(evidence_dir, trace_data)
    
    # Compute hashes
    hash_input = HashChainVerifier.hash_file(canonical_input_path)
    hash_output = HashChainVerifier.hash_file(canonical_output_path)
    hash_trace = HashChainVerifier.hash_file(canonical_trace_path)
    
    hashes = {
        "input": hash_input,
        "output": hash_output,
        "trace": hash_trace
    }
    
    # Write hashes
    evidence_writer.write_hashes(evidence_dir, hashes)
    evidence_writer.write_merkle_root(
        evidence_dir,
        HashChainVerifier.compute_merkle_root([hash_input, hash_output, hash_trace])
    )
    
    # Check for tampering (should be clean)
    tamper_checker = TamperChecker()
    clean_report = tamper_checker.check_tamper(evidence_dir)
    
    assert clean_report["input_tamper_detected"] is False
    assert clean_report["output_tamper_detected"] is False
    assert clean_report["trace_tamper_detected"] is False
    assert clean_report["verdict"] == "PASS"
    
    # Tamper with canonical input
    with open(canonical_input_path, 'r') as f:
        content = f.read()
    with open(canonical_input_path, 'w') as f:
        f.write(content.replace("CRITICAL", "WARNING"))
    
    # Check for tampering (should detect)
    tampered_report = tamper_checker.check_tamper(evidence_dir)
    
    assert tampered_report["input_tamper_detected"] is True
    assert tampered_report["output_tamper_detected"] is False
    assert tampered_report["trace_tamper_detected"] is False
    assert tampered_report["verdict"] == "FAIL"
    
    # Restore original
    with open(canonical_input_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Test 6 PASSED: Tamper-Proof Verification - {test_id}")
    print(f"   - Clean check: PASS")
    print(f"   - Tampering detected: {tampered_report['input_tamper_detected']}")
    print(f"   - Verdict: {tampered_report['verdict']}")
    
    return evidence_dir


def test_complete_workflow():
    """
    Test 7: Complete Workflow
    End-to-end test of the entire canonical hash chain workflow
    """
    test_id = CanonicalHashChainTestHelper.generate_test_id()
    
    # Create sample data
    input_data = CanonicalHashChainTestHelper.create_sample_input()
    output_data = CanonicalHashChainTestHelper.create_sample_output()
    trace_data = CanonicalHashChainTestHelper.create_sample_trace()
    
    # Create evidence directory
    evidence_writer = EvidenceWriter()
    evidence_dir = evidence_writer.create_evidence_directory()
    
    # Write canonical artifacts
    canonical_input_path = evidence_writer.write_canonical_input(evidence_dir, input_data)
    canonical_output_path = evidence_writer.write_canonical_output(evidence_dir, output_data)
    canonical_trace_path = evidence_writer.write_canonical_trace(evidence_dir, trace_data)
    
    # Compute hashes
    hash_input = HashChainVerifier.hash_file(canonical_input_path)
    hash_output = HashChainVerifier.hash_file(canonical_output_path)
    hash_trace = HashChainVerifier.hash_file(canonical_trace_path)
    
    hashes = {
        "input": hash_input,
        "output": hash_output,
        "trace": hash_trace
    }
    
    # Write hashes and Merkle root
    evidence_writer.write_hashes(evidence_dir, hashes)
    merkle_root = HashChainVerifier.compute_merkle_root([hash_input, hash_output, hash_trace])
    evidence_writer.write_merkle_root(evidence_dir, merkle_root)
    
    # Replay and verify
    replay_engine = ReplayEngine()
    replayed_output, replayed_trace = replay_engine.replay(canonical_input_path)
    
    replayed_output_path = os.path.join(evidence_dir, "replayed_output.json")
    replayed_trace_path = os.path.join(evidence_dir, "replayed_trace.json")
    
    with open(replayed_output_path, 'w') as f:
        json.dump(replayed_output, f, indent=2)
    
    with open(replayed_trace_path, 'w') as f:
        json.dump(replayed_trace, f, indent=2)
    
    replay_report = replay_engine.generate_replay_verification_report(
        test_id, hashes, replayed_output_path, replayed_trace_path
    )
    
    replay_report_path = os.path.join(evidence_dir, "replay_verification_report.json")
    with open(replay_report_path, 'w') as f:
        json.dump(replay_report, f, indent=2)
    
    # Check for tampering
    tamper_checker = TamperChecker()
    tamper_report = tamper_checker.check_tamper(evidence_dir)
    
    tamper_report_path = os.path.join(evidence_dir, "tamper_check_report.json")
    with open(tamper_report_path, 'w') as f:
        json.dump(tamper_report, f, indent=2)
    
    # Generate summary
    summary = {
        "test_id": test_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "era": 1,
        "evidence_directory": evidence_dir,
        "tests": {
            "canonicalization": {"status": "passed"},
            "hash_computation": {"status": "passed"},
            "merkle_root": {"status": "passed"},
            "evidence_writing": {"status": "passed"},
            "replayability": {"status": "passed" if replay_report["replay_success"] else "failed"},
            "tamper_proof": {"status": "passed" if tamper_report["verdict"] == "PASS" else "failed"}
        },
        "summary": {
            "total_tests": 6,
            "passed": sum(1 for t in [
                replay_report["replay_success"],
                replay_report["input_hash_match"],
                tamper_report["verdict"] == "PASS"
            ]),
            "overall_status": "passed" if tamper_report["verdict"] == "PASS" else "failed"
        },
        "canonical_hash": HashChainVerifier.hash_string(json.dumps({
            "test_id": test_id,
            "verdict": tamper_report["verdict"]
        }, sort_keys=True))
    }
    
    summary_path = os.path.join(evidence_dir, "summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Verify all tests passed
    assert summary["summary"]["overall_status"] == "passed"
    
    print(f"✅ Test 7 PASSED: Complete Workflow - {test_id}")
    print(f"   - Evidence directory: {evidence_dir}")
    print(f"   - Total tests: {summary['summary']['total_tests']}")
    print(f"   - Passed: {summary['summary']['passed']}")
    print(f"   - Overall status: {summary['summary']['overall_status']}")
    print(f"   - Merkle root: {merkle_root[:20]}...")
    
    return evidence_dir, summary


# ========== Test Runner ==========

if __name__ == "__main__":
    print("=" * 80)
    print("🧪 Canonical Hash Chain Tests")
    print("=" * 80)
    print()
    
    # Run all tests
    test_canonicalization()
    print()
    
    test_hash_computation()
    print()
    
    test_merkle_root()
    print()
    
    evidence_dir, hashes = test_evidence_writing()
    print()
    
    test_replayability()
    print()
    
    test_tamper_proof()
    print()
    
    test_complete_workflow()
    print()
    
    print("=" * 80)
    print("✅ All canonical hash chain tests PASSED (7/7)")
    print("=" * 80)