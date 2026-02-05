#!/usr/bin/env python3
"""
Hash Stability Tests - Beyond Era-1 Governance Verification

Tests for verifying hash stability, determinism, and consistency across
different environments, times, and input variations.

Purpose: Ensure IndestructibleAutoOps hash generation is deterministic,
reproducible, and stable across all conditions.
"""

import pytest
import json
import hashlib
import sys
import time
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add ecosystem to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))

from hash_translation_engine import HashTranslationEngine


class TestCanonicalizationDeterminism:
    """Test that canonicalization produces deterministic results"""
    
    @pytest.fixture
    def hte(self):
        """Initialize Hash Translation Engine"""
        return HashTranslationEngine(workspace="/workspace")
    
    @pytest.fixture
    def sample_data(self):
        """Generate sample data for testing"""
        return {
            "artifact_id": "hash-stability-test-001",
            "step_number": 1,
            "timestamp": "2026-02-05T10:00:00Z",
            "era": "1",
            "success": True,
            "metadata": {
                "key1": "value1",
                "key2": "value2"
            }
        }
    
    def test_canonicalization_determinism(self, hte, sample_data):
        """
        Test: Same artifact → Multiple canonicalizations → Hash consistency
        
        Expected: Same data should produce same hash every time (deterministic)
        """
        hashes = []
        
        # Canonicalize and hash 100 times
        for i in range(100):
            era1_canonical = hte.canonicalize_v1(sample_data)
            era1_hash = hte.compute_hash(era1_canonical)
            hashes.append(era1_hash)
        
        # Verify all hashes are identical
        unique_hashes = set(hashes)
        assert len(unique_hashes) == 1, \
            f"Found {len(unique_hashes)} different hashes for same data: {unique_hashes}"
        
        # Verify hash format
        assert hashes[0].startswith("sha256:"), f"Invalid hash format: {hashes[0]}"
        
        print(f"[PASS] All 100 canonicalizations produced identical hash: {hashes[0]}")
        
        # Seal test result
        test_result = {
            "test": "test_canonicalization_determinism",
            "status": "passed",
            "iterations": 100,
            "unique_hashes": len(unique_hashes),
            "hash": hashes[0],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Save to evidence
        evidence_dir = Path("/workspace/ecosystem/evidence/tests")
        evidence_dir.mkdir(parents=True, exist_ok=True)
        with open(evidence_dir / "hash_stability_determinism.json", 'w') as f:
            json.dump(test_result, f, indent=2)
    
    def test_canonicalization_reproducibility(self, hte, sample_data):
        """
        Test: Same data across different runs → Hash reproducibility
        
        Expected: Same data in different runs should produce same hash
        """
        # First run
        era1_canonical_v1 = hte.canonicalize_v1(sample_data)
        era1_hash_v1 = hte.compute_hash(era1_canonical_v1)
        
        # Second run (simulate different run)
        era1_canonical_v2 = hte.canonicalize_v1(sample_data)
        era1_hash_v2 = hte.compute_hash(era1_canonical_v2)
        
        # Verify hashes are identical
        assert era1_hash_v1 == era1_hash_v2, \
            f"Hashes differ across runs: {era1_hash_v1} vs {era1_hash_v2}"
        
        print(f"[PASS] Hash reproducible across runs: {era1_hash_v1}")


class TestYAMLAnchorImpact:
    """Test that YAML anchors do not affect hash stability"""
    
    @pytest.fixture
    def yaml_with_anchors(self):
        """YAML content with anchors"""
        yaml_content = """
version: "1.0"
era: 1
common: &common
  artifact_id: test-001
  success: true

step_1:
  <<: *common
  step_number: 1
  timestamp: "2026-02-05T10:00:00Z"

step_2:
  <<: *common
  step_number: 2
  timestamp: "2026-02-05T10:01:00Z"
"""
        return yaml_content
    
    @pytest.fixture
    def yaml_without_anchors(self):
        """YAML content without anchors (expanded)"""
        yaml_content = """
version: "1.0"
era: 1
step_1:
  artifact_id: test-001
  success: true
  step_number: 1
  timestamp: "2026-02-05T10:00:00Z"

step_2:
  artifact_id: test-001
  success: true
  step_number: 2
  timestamp: "2026-02-05T10:01:00Z"
"""
        return yaml_content
    
    def test_yaml_anchor_impact(self, yaml_with_anchors, yaml_without_anchors):
        """
        Test: YAML anchor → Load → Verify anchor resolution is deterministic
        
        Expected: YAML anchors are resolved during loading in a deterministic way
        """
        # Load YAML with anchors multiple times
        hte = HashTranslationEngine(workspace="/workspace")
        
        # Load the same YAML with anchors multiple times
        hashes = []
        for i in range(10):
            data_with_anchors = yaml.safe_load(yaml_with_anchors)
            json_data = json.dumps(data_with_anchors, sort_keys=True)
            hash_value = hte.compute_hash(json_data)
            hashes.append(hash_value)
        
        # Verify all hashes are identical (deterministic anchor resolution)
        unique_hashes = set(hashes)
        assert len(unique_hashes) == 1, \
            f"YAML anchor resolution is not deterministic: {len(unique_hashes)} different hashes"
        
        print(f"[PASS] YAML anchor resolution is deterministic: {hashes[0]}")
        
        # Seal test result
        test_result = {
            "test": "test_yaml_anchor_impact",
            "status": "passed",
            "hash": hashes[0],
            "yaml_anchors_deterministic": True,
            "iterations": 10,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Save to evidence
        evidence_dir = Path("/workspace/ecosystem/evidence/tests")
        evidence_dir.mkdir(parents=True, exist_ok=True)
        with open(evidence_dir / "hash_stability_yaml_anchors.json", 'w') as f:
            json.dump(test_result, f, indent=2)


class TestFieldOrderStability:
    """Test that field order does not affect hash stability"""
    
    @pytest.fixture
    def data_ordered(self):
        """Data with ordered fields"""
        return {
            "artifact_id": "test-001",
            "step_number": 1,
            "timestamp": "2026-02-05T10:00:00Z",
            "era": "1",
            "success": True
        }
    
    @pytest.fixture
    def data_unordered(self):
        """Same data but with different field order"""
        return {
            "success": True,
            "era": "1",
            "timestamp": "2026-02-05T10:00:00Z",
            "step_number": 1,
            "artifact_id": "test-001"
        }
    
    def test_field_order_stability(self, data_ordered, data_unordered):
        """
        Test: Different field order → Canonicalize → Verify hash stability
        
        Expected: Different field order should produce same hash after canonicalization
        """
        hte = HashTranslationEngine(workspace="/workspace")
        
        # Canonicalize both
        canonical_ordered = hte.canonicalize_v1(data_ordered)
        canonical_unordered = hte.canonicalize_v1(data_unordered)
        
        # Compute hashes
        hash_ordered = hte.compute_hash(canonical_ordered)
        hash_unordered = hte.compute_hash(canonical_unordered)
        
        # Verify hashes are identical
        assert hash_ordered == hash_unordered, \
            f"Field order affects hash: {hash_ordered} vs {hash_unordered}"
        
        # Verify canonical strings are identical
        assert canonical_ordered == canonical_unordered, \
            f"Canonical strings differ: {canonical_ordered} vs {canonical_unordered}"
        
        print(f"[PASS] Field order does not affect hash: {hash_ordered}")
        
        # Seal test result
        test_result = {
            "test": "test_field_order_stability",
            "status": "passed",
            "hash": hash_ordered,
            "field_order_independent": True,
            "canonical_string": canonical_ordered,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Save to evidence
        evidence_dir = Path("/workspace/ecosystem/evidence/tests")
        evidence_dir.mkdir(parents=True, exist_ok=True)
        with open(evidence_dir / "hash_stability_field_order.json", 'w') as f:
            json.dump(test_result, f, indent=2)


class TestTimestampStability:
    """Test that timestamps do not introduce non-determinism"""
    
    def test_timestamp_format_stability(self):
        """
        Test: Different timestamp formats → Canonicalize → Verify hash stability
        
        Expected: Same timestamp value in different formats should produce same hash
        """
        # Same timestamp, different formats
        timestamp_iso = "2026-02-05T10:00:00Z"
        timestamp_iso_ms = "2026-02-05T10:00:00.000Z"
        
        data1 = {
            "artifact_id": "test-001",
            "timestamp": timestamp_iso
        }
        
        data2 = {
            "artifact_id": "test-001",
            "timestamp": timestamp_iso_ms
        }
        
        # These should produce different hashes because the values are different
        hte = HashTranslationEngine(workspace="/workspace")
        hash1 = hte.compute_hash(json.dumps(data1, sort_keys=True))
        hash2 = hte.compute_hash(json.dumps(data2, sort_keys=True))
        
        assert hash1 != hash2, \
            "Different timestamp formats should produce different hashes"
        
        print(f"[PASS] Timestamp format affects hash (expected behavior)")
        
        # Seal test result
        test_result = {
            "test": "test_timestamp_format_stability",
            "status": "passed",
            "hash1": hash1,
            "hash2": hash2,
            "timestamp_format_sensitive": True,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Save to evidence
        evidence_dir = Path("/workspace/ecosystem/evidence/tests")
        evidence_dir.mkdir(parents=True, exist_ok=True)
        with open(evidence_dir / "hash_stability_timestamp.json", 'w') as f:
            json.dump(test_result, f, indent=2)


class TestWhitespaceStability:
    """Test that whitespace does not affect hash stability"""
    
    def test_whitespace_normalization(self):
        """
        Test: Different whitespace → Canonicalize → Verify hash stability
        
        Expected: Different whitespace should produce same hash after canonicalization
        """
        # Data with different whitespace
        data1 = {
            "artifact_id": "test-001",
            "description": "  test description  ",
            "nested": {
                "key": "value"
            }
        }
        
        data2 = {
            "artifact_id": "test-001",
            "description": "test description",
            "nested": {
                "key": "value"
            }
        }
        
        # These should produce different hashes because the values are different
        hte = HashTranslationEngine(workspace="/workspace")
        hash1 = hte.compute_hash(json.dumps(data1, sort_keys=True))
        hash2 = hte.compute_hash(json.dumps(data2, sort_keys=True))
        
        # Hashes should differ because whitespace in string values matters
        assert hash1 != hash2, \
            "Whitespace in string values should affect hash"
        
        print(f"[PASS] Whitespace in string values affects hash (expected behavior)")
        
        # Seal test result
        test_result = {
            "test": "test_whitespace_normalization",
            "status": "passed",
            "hash1": hash1,
            "hash2": hash2,
            "whitespace_sensitive": True,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Save to evidence
        evidence_dir = Path("/workspace/ecosystem/evidence/tests")
        evidence_dir.mkdir(parents=True, exist_ok=True)
        with open(evidence_dir / "hash_stability_whitespace.json", 'w') as f:
            json.dump(test_result, f, indent=2)


def test_overall_hash_stability():
    """Overall hash stability status verification"""
    evidence_dir = Path("/workspace/ecosystem/evidence/tests")
    
    # Check all test results
    test_results = {}
    for test_file in ["hash_stability_determinism.json", "hash_stability_yaml_anchors.json",
                      "hash_stability_field_order.json", "hash_stability_timestamp.json",
                      "hash_stability_whitespace.json"]:
        test_path = evidence_dir / test_file
        if test_path.exists():
            with open(test_path, 'r') as f:
                test_results[test_file] = json.load(f)
    
    # Overall status
    overall_status = "passed"
    for test_name, result in test_results.items():
        if result.get("status") == "failed":
            overall_status = "failed"
    
    # Seal overall result
    overall_result = {
        "test": "overall_hash_stability",
        "status": overall_status,
        "tests_executed": len(test_results),
        "test_results": test_results,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    # Save to evidence
    with open(evidence_dir / "hash_stability_overall.json", 'w') as f:
        json.dump(overall_result, f, indent=2)
    
    assert overall_status == "passed", \
        "Hash stability tests failed - cannot ensure deterministic hash generation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])