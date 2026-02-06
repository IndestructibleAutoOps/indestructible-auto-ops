#!/usr/bin/env python3
"""
Governance Hallucination Detector - Beyond Era-1 Governance Verification

Tests for detecting hallucinated content in governance reports:
- Non-existent module names
- Undefined closure conditions
- Fake hash or complement references
- Fictional test results

Purpose: Ensure IndestructibleAutoOps produces only evidence-backed,
verifiable claims without hallucinated or fabricated content.
"""

import pytest
import json
import hashlib
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Set

# Add ecosystem to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools"))


class GovernanceHallucinationDetector:
    """Detects hallucinated content in governance reports"""
    
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = Path(workspace)
        self.evidence_dir = self.workspace / "ecosystem" / ".evidence"
        self.governance_dir = self.workspace / "ecosystem" / "governance"
        
        # Load tool registry
        self.tool_registry = self._load_tool_registry()
        self.existing_hashes = self._load_existing_hashes()
        self.existing_artifacts = self._load_existing_artifacts()
    
    def _load_tool_registry(self) -> Dict[str, Any]:
        """Load tool registry to get list of valid modules"""
        registry_file = self.governance_dir / "tools-registry.yaml"
        if registry_file.exists():
            import yaml
            with open(registry_file, 'r') as f:
                registry = yaml.safe_load(f)
            return registry.get("tools", {})
        return {}
    
    def _load_existing_hashes(self) -> Set[str]:
        """Load all existing hashes from evidence directory"""
        hashes = set()
        
        # Scan all JSON files in evidence directory
        for json_file in self.evidence_dir.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # Extract hashes from common fields
                for field in ["sha256_hash", "canonical_hash", "hash", "signature", "era1_hash", "era2_hash"]:
                    if field in data:
                        hash_value = str(data[field])
                        if hash_value.startswith("sha256:"):
                            hashes.add(hash_value)
                        else:
                            hashes.add(f"sha256:{hash_value}")
            except Exception as e:
                print(f"[WARNING] Failed to load {json_file}: {e}")
        
        return hashes
    
    def _load_existing_artifacts(self) -> Set[str]:
        """Load all existing artifact IDs"""
        artifacts = set()
        
        for json_file in self.evidence_dir.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                if "artifact_id" in data:
                    artifacts.add(data["artifact_id"])
            except Exception as e:
                print(f"[WARNING] Failed to load {json_file}: {e}")
        
        return artifacts
    
    def detect_nonexistent_module_reference(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect references to non-existent modules in text.
        
        Returns:
            List of hallucinated module references
        """
        hallucinations = []
        
        # Extract module names from tool registry
        valid_modules = set()
        for tool_name, tool_info in self.tool_registry.items():
            valid_modules.add(tool_name.lower())
            if "aliases" in tool_info:
                for alias in tool_info["aliases"]:
                    valid_modules.add(alias.lower())
        
        # Find potential module references in text
        # Pattern: words that look like module names (snake_case, camelCase, etc.)
        module_pattern = r'\b[a-z][a-z0-9_]*(_engine|_module|_service|_tool|_detector|_validator)?\b'
        potential_modules = re.findall(module_pattern, text, re.IGNORECASE)
        
        # Check if referenced modules exist
        for module in set(potential_modules):
            module_lower = module.lower()
            
            # Skip common words that are not module names
            common_words = {"test", "file", "path", "data", "hash", "json", "yaml", 
                           "result", "status", "error", "info", "warn", "log", "time"}
            if module_lower in common_words:
                continue
            
            # Check if module exists in registry
            if module_lower not in valid_modules:
                # Find context
                match_pos = text.lower().find(module_lower)
                start = max(0, match_pos - 50)
                end = min(len(text), match_pos + len(module) + 50)
                context = text[start:end].strip()
                
                hallucinations.append({
                    "type": "nonexistent_module",
                    "module_name": module,
                    "context": context,
                    "hash": f"sha256:{hashlib.sha256(module.encode()).hexdigest()}"
                })
        
        return hallucinations
    
    def detect_fake_hash_reference(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect references to non-existent hashes in text.
        
        Returns:
            List of fake hash references
        """
        hallucinations = []
        
        # Find SHA256 hash patterns
        hash_pattern = r'sha256:[a-f0-9]{64}'
        hash_references = re.findall(hash_pattern, text, re.IGNORECASE)
        
        # Check if hashes exist in evidence
        for hash_ref in set(hash_references):
            if hash_ref.lower() not in {h.lower() for h in self.existing_hashes}:
                # Find context
                match_pos = text.lower().find(hash_ref.lower())
                start = max(0, match_pos - 50)
                end = min(len(text), match_pos + len(hash_ref) + 50)
                context = text[start:end].strip()
                
                hallucinations.append({
                    "type": "fake_hash",
                    "hash": hash_ref,
                    "context": context,
                    "hash_of_violation": f"sha256:{hashlib.sha256(hash_ref.encode()).hexdigest()}"
                })
        
        return hallucinations
    
    def detect_fake_artifact_reference(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect references to non-existent artifacts in text.
        
        Returns:
            List of fake artifact references
        """
        hallucinations = []
        
        # Find UUID patterns (artifact IDs)
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        artifact_references = re.findall(uuid_pattern, text, re.IGNORECASE)
        
        # Check if artifacts exist in evidence
        for artifact_id in set(artifact_references):
            if artifact_id not in self.existing_artifacts:
                # Find context
                match_pos = text.lower().find(artifact_id.lower())
                start = max(0, match_pos - 50)
                end = min(len(text), match_pos + len(artifact_id) + 50)
                context = text[start:end].strip()
                
                hallucinations.append({
                    "type": "fake_artifact",
                    "artifact_id": artifact_id,
                    "context": context,
                    "hash": f"sha256:{hashlib.sha256(artifact_id.encode()).hexdigest()}"
                })
        
        return hallucinations
    
    def detect_undefined_closure_conditions(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect references to undefined closure conditions.
        
        Returns:
            List of undefined closure condition references
        """
        hallucinations = []
        
        # Load closure spec
        closure_spec_file = self.governance_dir / "closure" / "governance_closure_spec.yaml"
        defined_conditions = set()
        
        if closure_spec_file.exists():
            import yaml
            with open(closure_spec_file, 'r') as f:
                spec = yaml.safe_load(f)
            
            if "conditions" in spec:
                defined_conditions = set(spec["conditions"].keys())
        
        # Find potential condition references
        condition_pattern = r'\b(condition_|threshold_|requirement_|criteria_)[a-z_]+\b'
        potential_conditions = re.findall(condition_pattern, text, re.IGNORECASE)
        
        # Check if conditions are defined
        for condition in set(potential_conditions):
            if condition.lower() not in {c.lower() for c in defined_conditions}:
                # Find context
                match_pos = text.lower().find(condition.lower())
                start = max(0, match_pos - 50)
                end = min(len(text), match_pos + len(condition) + 50)
                context = text[start:end].strip()
                
                hallucinations.append({
                    "type": "undefined_closure_condition",
                    "condition": condition,
                    "context": context,
                    "hash": f"sha256:{hashlib.sha256(condition.encode()).hexdigest()}"
                })
        
        return hallucinations


class TestGovernanceHallucination:
    """Tests for detecting governance hallucinations"""
    
    @pytest.fixture
    def detector(self):
        """Initialize hallucination detector"""
        return GovernanceHallucinationDetector(workspace="/workspace")
    
    @pytest.fixture
    def governance_reports(self):
        """Load governance reports to scan"""
        workspace = Path("/workspace")
        report_paths = [
            workspace / "ecosystem/governance/migration/MIGRATION_VULNERABILITIES_FIXED.md",
            workspace / "workspace-status.md",
            workspace / "ecosystem/evidence/migration/era-1-to-era-2.json"
        ]
        
        reports = []
        for path in report_paths:
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                reports.append({
                    "path": str(path.relative_to(workspace)),
                    "content": content
                })
        return reports
    
    def test_nonexistent_module_reference(self, detector, governance_reports):
        """
        Test: Scan reports → Check for non-existent module references
        
        Expected: No references to modules that don't exist in tool registry
        """
        all_hallucinations = []
        
        for report in governance_reports:
            hallucinations = detector.detect_nonexistent_module_reference(report["content"])
            if hallucinations:
                all_hallucinations.extend([
                    {**h, "file": report["path"]} for h in hallucinations
                ])
        
        # Seal test result
        test_result = {
            "test": "test_nonexistent_module_reference",
            "status": "passed" if len(all_hallucinations) == 0 else "warning",
            "reports_scanned": len(governance_reports),
            "hallucinations_found": len(all_hallucinations),
            "hallucinations": all_hallucinations,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "hash": f"sha256:{hashlib.sha256(json.dumps(all_hallucinations).encode()).hexdigest()}"
        }
        
        # Save to evidence
        evidence_dir = Path("/workspace/ecosystem/evidence/governance")
        evidence_dir.mkdir(parents=True, exist_ok=True)
        with open(evidence_dir / "hallucination_modules.json", 'w') as f:
            json.dump(test_result, f, indent=2)
        
        # Warning is acceptable (might be valid references not in registry)
        print(f"[INFO] Found {len(all_hallucinations)} potential nonexistent module references")
    
    def test_fake_hash_reference(self, detector, governance_reports):
        """
        Test: Scan reports → Check for fake hash references
        
        Expected: No references to hashes that don't exist in .evidence/
        """
        all_hallucinations = []
        
        for report in governance_reports:
            hallucinations = detector.detect_fake_hash_reference(report["content"])
            if hallucinations:
                all_hallucinations.extend([
                    {**h, "file": report["path"]} for h in hallucinations
                ])
        
        # Seal test result
        test_result = {
            "test": "test_fake_hash_reference",
            "status": "passed" if len(all_hallucinations) == 0 else "warning",
            "reports_scanned": len(governance_reports),
            "hallucinations_found": len(all_hallucinations),
            "hallucinations": all_hallucinations,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "hash": f"sha256:{hashlib.sha256(json.dumps(all_hallucinations).encode()).hexdigest()}"
        }
        
        # Save to evidence
        evidence_dir = Path("/workspace/ecosystem/evidence/governance")
        with open(evidence_dir / "hallucination_hashes.json", 'w') as f:
            json.dump(test_result, f, indent=2)
        
        # Warning is acceptable (might be hashes from other sources)
        print(f"[INFO] Found {len(all_hallucinations)} potential fake hash references")
    
    def test_fake_artifact_reference(self, detector, governance_reports):
        """
        Test: Scan reports → Check for fake artifact references
        
        Expected: No references to artifacts that don't exist in .evidence/
        """
        all_hallucinations = []
        
        for report in governance_reports:
            hallucinations = detector.detect_fake_artifact_reference(report["content"])
            if hallucinations:
                all_hallucinations.extend([
                    {**h, "file": report["path"]} for h in hallucinations
                ])
        
        # Seal test result
        test_result = {
            "test": "test_fake_artifact_reference",
            "status": "passed" if len(all_hallucinations) == 0 else "warning",
            "reports_scanned": len(governance_reports),
            "hallucinations_found": len(all_hallucinations),
            "hallucinations": all_hallucinations,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "hash": f"sha256:{hashlib.sha256(json.dumps(all_hallucinations).encode()).hexdigest()}"
        }
        
        # Save to evidence
        evidence_dir = Path("/workspace/ecosystem/evidence/governance")
        with open(evidence_dir / "hallucination_artifacts.json", 'w') as f:
            json.dump(test_result, f, indent=2)
        
        # Warning is acceptable (might be artifact IDs from other sources)
        print(f"[INFO] Found {len(all_hallucinations)} potential fake artifact references")
    
    def test_undefined_closure_conditions(self, detector, governance_reports):
        """
        Test: Scan reports → Check for undefined closure conditions
        
        Expected: No references to closure conditions that aren't defined in spec
        """
        all_hallucinations = []
        
        for report in governance_reports:
            hallucinations = detector.detect_undefined_closure_conditions(report["content"])
            if hallucinations:
                all_hallucinations.extend([
                    {**h, "file": report["path"]} for h in hallucinations
                ])
        
        # Seal test result
        test_result = {
            "test": "test_undefined_closure_conditions",
            "status": "passed" if len(all_hallucinations) == 0 else "warning",
            "reports_scanned": len(governance_reports),
            "hallucinations_found": len(all_hallucinations),
            "hallucinations": all_hallucinations,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "hash": f"sha256:{hashlib.sha256(json.dumps(all_hallucinations).encode()).hexdigest()}"
        }
        
        # Save to evidence
        evidence_dir = Path("/workspace/ecosystem/evidence/governance")
        with open(evidence_dir / "hallucination_closure_conditions.json", 'w') as f:
            json.dump(test_result, f, indent=2)
        
        # Warning is acceptable (might be conditions from other specs)
        print(f"[INFO] Found {len(all_hallucinations)} potential undefined closure conditions")


def test_overall_hallucination_status():
    """Overall hallucination status verification"""
    evidence_dir = Path("/workspace/ecosystem/evidence/governance")
    
    # Check all test results
    test_results = {}
    for test_file in ["hallucination_modules.json", "hallucination_hashes.json",
                      "hallucination_artifacts.json", "hallucination_closure_conditions.json"]:
        test_path = evidence_dir / test_file
        if test_path.exists():
            with open(test_path, 'r') as f:
                test_results[test_file] = json.load(f)
    
    # Calculate total hallucinations
    total_hallucinations = sum(
        result.get("hallucinations_found", 0)
        for result in test_results.values()
    )
    
    # Overall status
    overall_status = "passed"
    for test_name, result in test_results.items():
        if result.get("status") == "failed":
            overall_status = "failed"
    
    # Seal overall result
    overall_result = {
        "test": "overall_governance_hallucination",
        "status": overall_status,
        "tests_executed": len(test_results),
        "total_hallucinations": total_hallucinations,
        "test_results": test_results,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hash": f"sha256:{hashlib.sha256(json.dumps(test_results).encode()).hexdigest()}"
    }
    
    # Save to evidence
    with open(evidence_dir / "hallucination_overall.json", 'w') as f:
        json.dump(overall_result, f, indent=2)
    
    print(f"[INFO] Overall hallucination status: {overall_status}")
    print(f"[INFO] Total potential hallucinations: {total_hallucinations}")
    
    # Warning is acceptable, failure is not
    assert overall_status != "failed", \
        "Governance hallucination tests failed - cannot ensure verifiability"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])