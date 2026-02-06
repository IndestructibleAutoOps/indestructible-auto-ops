"""
Semantic Defense System Test Configuration
Era-1 Test Framework
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import hashlib

# Test workspace root
TEST_WORKSPACE = Path("/tmp/test_semantic_defense")


@pytest.fixture(scope="session", autouse=True)
def setup_test_workspace():
    """Setup test workspace directory"""
    TEST_WORKSPACE.mkdir(parents=True, exist_ok=True)

    yield

    # Cleanup
    if TEST_WORKSPACE.exists():
        shutil.rmtree(TEST_WORKSPACE)


@pytest.fixture
def test_workspace():
    """Create isolated test workspace"""
    workspace = TEST_WORKSPACE / f"test_{datetime.now().timestamp()}"
    workspace.mkdir(parents=True, exist_ok=True)

    # Create governance structure
    (workspace / "ecosystem" / ".governance").mkdir(parents=True, exist_ok=True)
    (workspace / "ecosystem" / ".evidence").mkdir(parents=True, exist_ok=True)
    (workspace / "complements").mkdir(parents=True, exist_ok=True)

    yield workspace

    # Cleanup
    if workspace.exists():
        shutil.rmtree(workspace)


@pytest.fixture
def sample_artifact():
    """Sample artifact for testing"""
    return {
        "artifact_id": "test-artifact-001",
        "step_number": 1,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "era": "1",
        "success": True,
        "metadata": {},
        "execution_time_ms": 100,
        "violations_count": 0,
        "artifacts_generated": [],
        "canonical_hash": "abc123def456",
        "canonicalization_version": "1.0",
        "canonicalization_method": "JCS+LayeredSorting",
        "hash_chain": {"self": "abc123def456", "parent": None, "merkle_root": None},
    }


@pytest.fixture
def sample_event():
    """Sample event for testing"""
    return {
        "event_id": "test-event-001",
        "event_type": "STEP_EXECUTED",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "era": "1",
        "step_number": 1,
        "artifact_file": "test.json",
        "success": True,
        "violations_count": 0,
        "execution_time_ms": 100,
        "phase": "Step_1",
        "canonical_hash": "xyz789uvw012",
        "canonicalization_version": "1.0",
        "canonicalization_method": "JCS+LayeredSorting",
        "hash_chain": {
            "self": "xyz789uvw012",
            "previous_event": None,
            "previous_artifact": "abc123def456",
        },
    }


@pytest.fixture
def sample_report():
    """Sample report for testing"""
    return {
        "report_id": "test-report-001",
        "title": "Test Report",
        "status": "COMPLETED",
        "summary": "Test completed successfully",
        "evidence": ["evidence-1.json"],
        "complements": [],
    }


@pytest.fixture
def fuzzy_report():
    """Report with fuzzy language"""
    return {
        "report_id": "fuzzy-report-001",
        "title": "Test Report",
        "status": "COMPLETED",
        "summary": "大致完成，應該沒問題",
        "evidence": ["evidence-1.json"],
        "complements": [],
    }


class SemanticDefenseViolation:
    """Represents a semantic defense violation"""

    def __init__(
        self,
        test_case: str,
        severity: str,
        detected_issue: str,
        evidence: Dict[str, Any],
        remediation: Dict[str, str],
    ):
        self.test_case = test_case
        self.severity = severity
        self.detected_issue = detected_issue
        self.evidence = evidence
        self.remediation = remediation
        self.timestamp = datetime.utcnow().isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_case": self.test_case,
            "severity": self.severity,
            "detected_issue": self.detected_issue,
            "evidence": self.evidence,
            "remediation": self.remediation,
            "timestamp": self.timestamp,
        }

    def to_complement(self) -> Dict[str, Any]:
        """Generate complement from violation"""
        return {
            "complement_type": "semantic_defense_violation",
            "test_case": self.test_case,
            "severity": self.severity,
            "detected_issue": self.detected_issue,
            "evidence": self.evidence,
            "remediation": self.remediation,
            "timestamp": self.timestamp,
        }


@pytest.fixture
def violation_maker():
    """Factory for creating violations"""

    def make_violation(
        test_case: str,
        severity: str = "CRITICAL",
        detected_issue: str = "test_issue",
        evidence: Dict[str, Any] = None,
        remediation: Dict[str, str] = None,
    ) -> SemanticDefenseViolation:
        if evidence is None:
            evidence = {}
        if remediation is None:
            remediation = {}

        return SemanticDefenseViolation(
            test_case=test_case,
            severity=severity,
            detected_issue=detected_issue,
            evidence=evidence,
            remediation=remediation,
        )

    return make_violation


class CanonicalizationTester:
    """Helper for testing canonicalization"""

    @staticmethod
    def compute_hash(data: Dict[str, Any]) -> str:
        """Compute SHA256 hash of JSON data"""
        json_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(json_str.encode()).hexdigest()

    @staticmethod
    def canonicalize_jcs(data: Dict[str, Any]) -> str:
        """Apply JCS canonicalization"""
        # Simplified JCS implementation
        canonical = json.dumps(
            data, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )
        return canonical

    @staticmethod
    def layered_sort(data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply layered sorting"""
        return {
            "_layer1": {
                k: v
                for k, v in sorted(data.items())
                if k in ["artifact_id", "step_number", "timestamp", "era", "success"]
            },
            "_layer2": {
                k: v
                for k, v in sorted(data.items())
                if k in ["metadata", "execution_time_ms", "violations_count"]
            },
            "_layer3": {
                k: v
                for k, v in sorted(data.items())
                if k
                not in [
                    "artifact_id",
                    "step_number",
                    "timestamp",
                    "era",
                    "success",
                    "metadata",
                    "execution_time_ms",
                    "violations_count",
                ]
            },
        }


@pytest.fixture
def canonicalization_tester():
    """Factory for canonicalization testing"""
    return CanonicalizationTester()


class EventStreamValidator:
    """Helper for validating event streams"""

    REQUIRED_FIELDS = ["event_id", "event_type", "timestamp", "era"]

    @classmethod
    def validate_event(cls, event: Dict[str, Any]) -> List[str]:
        """Validate event has all required fields"""
        missing = []
        for field in cls.REQUIRED_FIELDS:
            if field not in event:
                missing.append(field)
        return missing

    @classmethod
    def validate_event_hash(cls, event: Dict[str, Any]) -> bool:
        """Validate event hash is present and valid"""
        if "canonical_hash" not in event:
            return False
        if "hash_chain" not in event:
            return False
        if "self" not in event["hash_chain"]:
            return False
        return True


@pytest.fixture
def event_validator():
    """Factory for event validation"""
    return EventStreamValidator()
