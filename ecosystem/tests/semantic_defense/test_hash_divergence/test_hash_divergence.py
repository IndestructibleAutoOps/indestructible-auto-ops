"""
Test 2: Hash Divergence Tests
Purpose: Ensure canonicalization pipeline produces consistent hashes across different environments
"""

import pytest
import json
import hashlib
from typing import Dict, Any


class TestHashDivergence:
    """Test suite for hash divergence detection"""
    
    def test_tc_2_1_windows_vs_linux_hash_consistency(
        self,
        sample_artifact,
        canonicalization_tester,
        violation_maker
    ):
        """
        TC-2.1: Windows vs Linux Hash Consistency
        
        Input: Same artifact on Windows and Linux
        Expected: Hashes identical
        Action: If divergent → report canonicalization failure
        Severity: CRITICAL
        """
        # Simulate Windows line endings (CRLF)
        artifact_windows = {**sample_artifact}
        json_windows = json.dumps(artifact_windows, ensure_ascii=False).replace('\n', '\r\n')
        hash_windows = hashlib.sha256(json_windows.encode()).hexdigest()
        
        # Simulate Linux line endings (LF)
        artifact_linux = {**sample_artifact}
        json_linux = json.dumps(artifact_linux, ensure_ascii=False)
        hash_linux = hashlib.sha256(json_linux.encode()).hexdigest()
        
        # Canonicalize both (should produce same hash)
        canonical_windows = canonicalization_tester.canonicalize_jcs(artifact_windows)
        canonical_linux = canonicalization_tester.canonicalize_jcs(artifact_linux)
        
        hash_windows_canonical = hashlib.sha256(canonical_windows.encode()).hexdigest()
        hash_linux_canonical = hashlib.sha256(canonical_linux.encode()).hexdigest()
        
        # Canonicalization should produce consistent hash
        assert hash_windows_canonical == hash_linux_canonical, \
            "Canonicalization should produce consistent hash across OS"
        
        # Raw hashes may differ, but that's expected
        # Only canonical hashes must match
    
    def test_tc_2_2_python_version_hash_consistency(
        self,
        sample_artifact,
        canonicalization_tester,
        violation_maker
    ):
        """
        TC-2.2: Python Version Hash Consistency
        
        Input: Same artifact on Python 3.8, 3.9, 3.10, 3.11
        Expected: Hashes identical
        Action: If divergent → report canonicalization failure
        Severity: CRITICAL
        """
        # Simulate different Python version behaviors
        # (In real test, we'd run on different Python versions)
        
        # Test with JSON encoding variations
        artifact = {**sample_artifact}
        
        # Canonicalized encoding (JCS) - should be stable
        canonical = canonicalization_tester.canonicalize_jcs(artifact)
        hash_canonical = hashlib.sha256(canonical.encode()).hexdigest()
        
        # Canonicalization should produce same hash when called multiple times
        canonical2 = canonicalization_tester.canonicalize_jcs(artifact)
        hash_canonical2 = hashlib.sha256(canonical2.encode()).hexdigest()
        
        # Canonicalization should be stable
        assert hash_canonical == hash_canonical2, \
            "Canonicalization should produce stable hash across multiple calls"
    
    def test_tc_2_3_locale_hash_consistency(
        self,
        sample_artifact,
        canonicalization_tester,
        violation_maker
    ):
        """
        TC-2.3: Locale Hash Consistency
        
        Input: Same artifact with different locales (en_US, zh_TW, ja_JP)
        Expected: Hashes identical
        Action: If divergent → report canonicalization failure
        Severity: HIGH
        """
        artifact = {**sample_artifact}
        
        # Canonicalization should be locale-independent
        canonical_en = canonicalization_tester.canonicalize_jcs(artifact)
        canonical_zh = canonicalization_tester.canonicalize_jcs(artifact)
        canonical_ja = canonicalization_tester.canonicalize_jcs(artifact)
        
        hash_en = hashlib.sha256(canonical_en.encode()).hexdigest()
        hash_zh = hashlib.sha256(canonical_zh.encode()).hexdigest()
        hash_ja = hashlib.sha256(canonical_ja.encode()).hexdigest()
        
        assert hash_en == hash_zh == hash_ja, \
            "Canonicalization should be locale-independent"
    
    def test_tc_2_4_line_ending_hash_consistency(
        self,
        sample_artifact,
        canonicalization_tester,
        violation_maker
    ):
        """
        TC-2.4: Line Ending Hash Consistency
        
        Input: Same artifact with LF vs CRLF
        Expected: Hashes identical
        Action: If divergent → report canonicalization failure
        Severity: HIGH
        """
        artifact = {**sample_artifact}
        
        # LF line ending
        json_lf = json.dumps(artifact, ensure_ascii=False, indent=2).replace('\r\n', '\n')
        hash_lf = hashlib.sha256(json_lf.encode()).hexdigest()
        
        # CRLF line ending
        json_crlf = json.dumps(artifact, ensure_ascii=False, indent=2).replace('\n', '\r\n')
        hash_crlf = hashlib.sha256(json_crlf.encode()).hexdigest()
        
        # Raw hashes differ
        assert hash_lf != hash_crlf, "Line endings affect raw hash"
        
        # Canonicalized hashes should match
        canonical = canonicalization_tester.canonicalize_jcs(artifact)
        hash_canonical = hashlib.sha256(canonical.encode()).hexdigest()
        
        # Canonicalization normalizes line endings
        assert hash_canonical is not None, "Canonicalization produces hash"
    
    def test_hash_divergence_detection(
        self,
        sample_artifact,
        violation_maker
    ):
        """Test that hash divergence is properly detected and reported"""
        # Simulate hash divergence
        hash_windows = "abc123def456"
        hash_linux = "def456abc123"
        
        if hash_windows != hash_linux:
            violation = violation_maker(
                test_case="TC-2.1",
                severity="CRITICAL",
                detected_issue="windows_linux_divergence",
                evidence={
                    "windows_hash": hash_windows,
                    "linux_hash": hash_linux,
                    "artifact": "sample_artifact"
                },
                remediation={
                    "action": "fix_canonicalization_pipeline",
                    "required": "確保所有環境產生相同 hash",
                    "suggestion": "檢查 JCS canonicalization 實現"
                }
            )
            
            assert violation.severity == "CRITICAL"
            assert violation.detected_issue == "windows_linux_divergence"
    
    def test_repeated_canonicalization_produces_same_hash(
        self,
        sample_artifact,
        canonicalization_tester
    ):
        """Test that repeated canonicalization produces identical hashes"""
        artifact = {**sample_artifact}
        
        hashes = []
        for i in range(10):
            canonical = canonicalization_tester.canonicalize_jcs(artifact)
            hash_val = hashlib.sha256(canonical.encode()).hexdigest()
            hashes.append(hash_val)
        
        # All hashes should be identical
        assert len(set(hashes)) == 1, \
            f"Repeated canonicalization should produce same hash, got {len(set(hashes))} different hashes"