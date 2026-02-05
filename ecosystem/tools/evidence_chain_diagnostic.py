#!/usr/bin/env python3
"""
Evidence Chain Diagnostic Tool
================================

Diagnoses evidence chain vulnerabilities by checking:
1. Artifact canonical hash presence
2. Hash reproducibility
3. Event hash presence
4. Hash complement existence
5. Evidence directory completeness
6. Hash registry existence and integrity

Based on global best practices:
- Blockchain immutable audit trails (2024)
- RFC 8785 JSON Canonicalization Scheme (JCS)
- Cryptographic provenance for audit systems
- Evidence trustworthiness frameworks
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Add ecosystem to path
sys.path.insert(0, '/workspace/ecosystem')
sys.path.insert(0, '/workspace')


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class DiagnosticIssue:
    """Represents a diagnostic issue"""
    category: str
    item_id: str
    severity: Severity
    issue: str
    remediation: str
    evidence: Dict[str, Any]


@dataclass
class DiagnosticResult:
    """Overall diagnostic result"""
    timestamp: str
    total_items_checked: int
    issues: List[DiagnosticIssue]
    score: float
    can_seal: bool


class EvidenceChainDiagnostic:
    """Main diagnostic class"""
    
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = Path(workspace)
        self.evidence_dir = self.workspace / "ecosystem" / ".evidence"
        self.governance_dir = self.workspace / "ecosystem" / ".governance"
        self.event_stream_file = self.governance_dir / "event-stream.jsonl"
        self.hash_registry_file = self.governance_dir / "hash-registry.json"
        
        self.issues: List[DiagnosticIssue] = []
        self.items_checked = 0
        
    def run_full_diagnostic(self) -> DiagnosticResult:
        """Run all diagnostic checks"""
        print("🔍 Starting Evidence Chain Diagnostic...")
        print(f"📁 Evidence Directory: {self.evidence_dir}")
        print(f"📁 Governance Directory: {self.governance_dir}")
        print()
        
        # Check 1: Artifact canonical hash presence
        print("1️⃣  Checking artifact canonical hashes...")
        self._check_artifact_canonical_hashes()
        
        # Check 2: Hash reproducibility
        print("2️⃣  Checking hash reproducibility...")
        self._check_hash_reproducibility()
        
        # Check 3: Event hash presence
        print("3️⃣  Checking event hashes...")
        self._check_event_hashes()
        
        # Check 4: Hash complement existence
        print("4️⃣  Checking hash complements...")
        self._check_hash_complements()
        
        # Check 5: Evidence directory completeness
        print("5️⃣  Checking evidence directory completeness...")
        self._check_evidence_directory_completeness()
        
        # Check 6: Hash registry existence and integrity
        print("6️⃣  Checking hash registry...")
        self._check_hash_registry()
        
        # Calculate results
        score = self._calculate_score()
        can_seal = self._can_seal()
        
        print()
        print("=" * 70)
        print(f"📊 Diagnostic Complete")
        print(f"   Total Items Checked: {self.items_checked}")
        print(f"   Total Issues: {len(self.issues)}")
        print(f"   Score: {score:.1f}/100")
        print(f"   Can Seal: {'✅ YES' if can_seal else '❌ NO'}")
        print("=" * 70)
        
        # Print summary
        self._print_issue_summary()
        
        return DiagnosticResult(
            timestamp=datetime.now().isoformat(),
            total_items_checked=self.items_checked,
            issues=self.issues,
            score=score,
            can_seal=can_seal
        )
    
    def _check_artifact_canonical_hashes(self):
        """Check if all artifacts have canonical hashes"""
        if not self.evidence_dir.exists():
            self.issues.append(DiagnosticIssue(
                category="artifact",
                item_id="evidence_directory",
                severity=Severity.CRITICAL,
                issue="Evidence directory does not exist",
                remediation=f"Create directory: {self.evidence_dir}",
                evidence={"exists": False}
            ))
            return
        
        artifact_files = sorted(self.evidence_dir.glob("step-*.json"))
        self.items_checked += len(artifact_files)
        
        for artifact_file in artifact_files:
            try:
                with open(artifact_file, 'r') as f:
                    artifact = json.load(f)
                
                if 'canonical_hash' not in artifact:
                    self.issues.append(DiagnosticIssue(
                        category="artifact",
                        item_id=artifact_file.name,
                        severity=Severity.HIGH,
                        issue="Artifact missing canonical_hash field",
                        remediation="Re-run enforce.rules.py to regenerate artifact with canonical hash",
                        evidence={"file": str(artifact_file)}
                    ))
                
                if 'sha256_hash' not in artifact:
                    self.issues.append(DiagnosticIssue(
                        category="artifact",
                        item_id=artifact_file.name,
                        severity=Severity.MEDIUM,
                        issue="Artifact missing sha256_hash field",
                        remediation="Re-run enforce.rules.py to regenerate artifact",
                        evidence={"file": str(artifact_file)}
                    ))
                    
                if 'hash_chain' not in artifact:
                    self.issues.append(DiagnosticIssue(
                        category="artifact",
                        item_id=artifact_file.name,
                        severity=Severity.HIGH,
                        issue="Artifact missing hash_chain field",
                        remediation="Re-run enforce.rules.py with hash chain support",
                        evidence={"file": str(artifact_file)}
                    ))
                    
            except Exception as e:
                self.issues.append(DiagnosticIssue(
                    category="artifact",
                    item_id=artifact_file.name,
                    severity=Severity.HIGH,
                    issue=f"Failed to parse artifact: {str(e)}",
                    remediation="Check JSON syntax and encoding",
                    evidence={"file": str(artifact_file), "error": str(e)}
                ))
        
        if len(artifact_files) == 0:
            self.issues.append(DiagnosticIssue(
                category="artifact",
                item_id="no_artifacts",
                severity=Severity.CRITICAL,
                issue="No artifact files found in .evidence/ directory",
                remediation="Run enforce.rules.py to generate artifacts",
                evidence={"directory": str(self.evidence_dir)}
            ))
    
    def _check_hash_reproducibility(self):
        """Check if canonical hashes are reproducible by re-computing using JCS canonicalization"""
        # Import canonicalization tool
        try:
            from ecosystem.tools.canonicalize import canonicalize_json
        except ImportError:
            self.issues.append(DiagnosticIssue(
                category="hash",
                item_id="canonicalize_tool",
                severity=Severity.HIGH,
                issue="Canonicalization tool not available (RFC 8785 required)",
                remediation="Install rfc8785 package: pip install rfc8785",
                evidence={"error": "ImportError"}
            ))
            return
        
        artifact_files = list(self.evidence_dir.glob("step-*.json"))
        self.items_checked += len(artifact_files)
        
        for artifact_file in artifact_files:
            try:
                with open(artifact_file, 'r') as f:
                    artifact = json.load(f)
                
                stored_canonical_hash = artifact.get('canonical_hash', '')
                
                if not stored_canonical_hash:
                    self.issues.append(DiagnosticIssue(
                        category="hash",
                        item_id=artifact_file.name,
                        severity=Severity.HIGH,
                        issue="Artifact has no canonical_hash field",
                        remediation="Re-run enforce.rules.py to regenerate artifact with canonical hash",
                        evidence={"file": str(artifact_file)}
                    ))
                    continue
                
                # Recompute canonical hash using JCS
                # Note: canonical hash is computed on layered structure (_layer1, _layer2, _layer3)
                try:
                    # Create layered structure matching _create_layered_artifact
                    layered_data = {
                        "_layer1": {
                            "artifact_id": artifact.get("artifact_id"),
                            "step_number": artifact.get("step_number"),
                            "timestamp": artifact.get("timestamp"),
                            "era": artifact.get("era"),
                            "success": artifact.get("success")
                        },
                        "_layer2": {
                            "metadata": artifact.get("metadata", {}),
                            "execution_time_ms": artifact.get("execution_time_ms"),
                            "violations_count": artifact.get("violations_count", 0)
                        },
                        "_layer3": {
                            "artifacts_generated": artifact.get("artifacts_generated", [])
                        }
                    }
                    
                    canonical_str = canonicalize_json(layered_data)
                    computed_canonical_hash = hashlib.sha256(canonical_str.encode('utf-8')).hexdigest()
                    
                    if stored_canonical_hash != computed_canonical_hash:
                        self.issues.append(DiagnosticIssue(
                            category="hash",
                            item_id=artifact_file.name,
                            severity=Severity.CRITICAL,
                            issue="Canonical hash mismatch - stored hash does not match computed hash",
                            remediation="Re-run enforce.rules.py to regenerate artifact with correct canonical hash",
                            evidence={
                                "file": str(artifact_file),
                                "stored_hash": stored_canonical_hash,
                                "computed_hash": computed_canonical_hash
                            }
                        ))
                except Exception as e:
                    self.issues.append(DiagnosticIssue(
                        category="hash",
                        item_id=artifact_file.name,
                        severity=Severity.MEDIUM,
                        issue=f"Failed to canonicalize artifact: {str(e)}",
                        remediation="Check artifact structure and canonicalization tool",
                        evidence={"file": str(artifact_file), "error": str(e)}
                    ))
                    
            except Exception as e:
                self.issues.append(DiagnosticIssue(
                    category="hash",
                    item_id=artifact_file.name,
                    severity=Severity.MEDIUM,
                    issue=f"Failed to verify hash reproducibility: {str(e)}",
                    remediation="Check file encoding and format",
                    evidence={"file": str(artifact_file), "error": str(e)}
                ))
    
    def _check_event_hashes(self):
        """Check if events have canonical hashes"""
        if not self.event_stream_file.exists():
            self.issues.append(DiagnosticIssue(
                category="event",
                item_id="event-stream",
                severity=Severity.CRITICAL,
                issue="Event stream file does not exist",
                remediation="Run enforce.rules.py to generate event stream",
                evidence={"file": str(self.event_stream_file), "exists": False}
            ))
            return
        
        events_missing_hash = []
        events_missing_hash_chain = []
        events_missing_era = []
        
        with open(self.event_stream_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    event = json.loads(line.strip())
                    self.items_checked += 1
                    
                    if 'canonical_hash' not in event:
                        events_missing_hash.append(line_num)
                    
                    if 'hash_chain' not in event:
                        events_missing_hash_chain.append(line_num)
                    
                    if 'era' not in event:
                        events_missing_era.append(line_num)
                        
                except Exception as e:
                    self.issues.append(DiagnosticIssue(
                        category="event",
                        item_id=f"line_{line_num}",
                        severity=Severity.HIGH,
                        issue=f"Failed to parse event: {str(e)}",
                        remediation="Check JSON syntax and encoding",
                        evidence={"line": line_num, "error": str(e)}
                    ))
        
        if events_missing_hash:
            severity = Severity.CRITICAL if len(events_missing_hash) > 100 else Severity.HIGH
            self.issues.append(DiagnosticIssue(
                category="event",
                item_id="events_missing_hash",
                severity=severity,
                issue=f"{len(events_missing_hash)} events missing canonical_hash field",
                remediation="Run event migration script to add canonical_hash to historical events",
                evidence={"line_numbers": events_missing_hash[:10]}  # Show first 10
            ))
        
        if events_missing_hash_chain:
            severity = Severity.CRITICAL if len(events_missing_hash_chain) > 100 else Severity.HIGH
            self.issues.append(DiagnosticIssue(
                category="event",
                item_id="events_missing_hash_chain",
                severity=severity,
                issue=f"{len(events_missing_hash_chain)} events missing hash_chain field",
                remediation="Run event migration script to add hash_chain to historical events",
                evidence={"line_numbers": events_missing_hash_chain[:10]}
            ))
        
        if events_missing_era:
            self.issues.append(DiagnosticIssue(
                category="event",
                item_id="events_missing_era",
                severity=Severity.MEDIUM,
                issue=f"{len(events_missing_era)} events missing era field",
                remediation="Run event migration script to add era field to historical events",
                evidence={"line_numbers": events_missing_era[:10]}
            ))
    
    def _check_hash_complements(self):
        """Check if hashes have complements"""
        complements_dir = self.evidence_dir / "complements"
        
        if not complements_dir.exists():
            self.issues.append(DiagnosticIssue(
                category="complement",
                item_id="complements_directory",
                severity=Severity.MEDIUM,
                issue="Complements directory does not exist",
                remediation=f"Create directory: {complements_dir} and run materialization_complement_generator.py",
                evidence={"directory": str(complements_dir), "exists": False}
            ))
            return
        
        # Check if there are any complement files
        complement_files = list(complements_dir.glob("*.json"))
        
        if len(complement_files) == 0:
            self.issues.append(DiagnosticIssue(
                category="complement",
                item_id="no_complements",
                severity=Severity.MEDIUM,
                issue="No complement files found",
                remediation="Run materialization_complement_generator.py to generate complements",
                evidence={"directory": str(complements_dir)}
            ))
    
    def _check_evidence_directory_completeness(self):
        """Check if evidence directory structure is complete"""
        required_subdirs = ['artifacts', 'events', 'hashes', 'registry']
        
        for subdir in required_subdirs:
            subdir_path = self.evidence_dir / subdir
            if not subdir_path.exists():
                self.issues.append(DiagnosticIssue(
                    category="structure",
                    item_id=f"missing_{subdir}",
                    severity=Severity.MEDIUM,
                    issue=f"Missing required subdirectory: {subdir}",
                    remediation=f"Create directory: {subdir_path}",
                    evidence={"missing": str(subdir_path)}
                ))
        
        # Check if step artifacts exist
        step_artifacts = list(self.evidence_dir.glob("step-*.json"))
        if len(step_artifacts) < 10:
            self.issues.append(DiagnosticIssue(
                category="structure",
                item_id="incomplete_step_artifacts",
                severity=Severity.HIGH,
                issue=f"Only {len(step_artifacts)} step artifacts found (expected 10)",
                remediation="Run enforce.rules.py to generate all 10 step artifacts",
                evidence={"found": len(step_artifacts), "expected": 10}
            ))
    
    def _check_hash_registry(self):
        """Check if hash registry exists and is complete"""
        if not self.hash_registry_file.exists():
            self.issues.append(DiagnosticIssue(
                category="registry",
                item_id="hash_registry",
                severity=Severity.CRITICAL,
                issue="Hash registry file does not exist",
                remediation="Run enforce.rules.py to generate hash registry",
                evidence={"file": str(self.hash_registry_file), "exists": False}
            ))
            return
        
        try:
            with open(self.hash_registry_file, 'r') as f:
                registry = json.load(f)
            
            # Check for era1_to_era2 and era2_to_era1 mappings
            if not registry.get('era1_to_era2'):
                self.issues.append(DiagnosticIssue(
                    category="registry",
                    item_id="era1_to_era2",
                    severity=Severity.INFO,
                    issue="era1_to_era2 hash mapping is empty (expected for Era-1)",
                    remediation="No action needed until Era-2 migration",
                    evidence={}
                ))
            
            if not registry.get('era2_to_era1'):
                self.issues.append(DiagnosticIssue(
                    category="registry",
                    item_id="era2_to_era1",
                    severity=Severity.INFO,
                    issue="era2_to_era1 hash mapping is empty (expected for Era-1)",
                    remediation="No action needed until Era-2 migration",
                    evidence={}
                ))
            
            # Check if all artifact hashes are present
            artifacts = registry.get('artifacts', {})
            if len(artifacts) < 10:
                self.issues.append(DiagnosticIssue(
                    category="registry",
                    item_id="incomplete_artifact_hashes",
                    severity=Severity.HIGH,
                    issue=f"Only {len(artifacts)} artifact hashes in registry (expected 10)",
                    remediation="Run enforce.rules.py to regenerate hash registry",
                    evidence={"found": len(artifacts), "expected": 10}
                ))
            
        except Exception as e:
            self.issues.append(DiagnosticIssue(
                category="registry",
                item_id="parse_error",
                severity=Severity.HIGH,
                issue=f"Failed to parse hash registry: {str(e)}",
                remediation="Check JSON syntax and encoding",
                evidence={"file": str(self.hash_registry_file), "error": str(e)}
            ))
    
    def _calculate_score(self) -> float:
        """Calculate overall compliance score (0-100)"""
        if self.items_checked == 0:
            return 0.0
        
        # Count issues by severity
        critical_issues = sum(1 for i in self.issues if i.severity == Severity.CRITICAL)
        high_issues = sum(1 for i in self.issues if i.severity == Severity.HIGH)
        medium_issues = sum(1 for i in self.issues if i.severity == Severity.MEDIUM)
        low_issues = sum(1 for i in self.issues if i.severity == Severity.LOW)
        
        # Calculate penalty
        penalty = (critical_issues * 25) + (high_issues * 15) + (medium_issues * 5) + (low_issues * 1)
        
        # Calculate score
        score = max(0.0, 100.0 - penalty)
        
        return score
    
    def _can_seal(self) -> bool:
        """Determine if evidence chain can be sealed"""
        # Cannot seal if there are any CRITICAL or HIGH issues
        has_blocking_issues = any(
            i.severity in [Severity.CRITICAL, Severity.HIGH]
            for i in self.issues
        )
        
        if has_blocking_issues:
            return False
        
        # Score must be >= 90.0
        score = self._calculate_score()
        
        return score >= 90.0
    
    def _print_issue_summary(self):
        """Print summary of issues by severity"""
        if not self.issues:
            print("✅ No issues found!")
            return
        
        print()
        print("📋 Issue Summary:")
        print("-" * 70)
        
        # Group by severity
        by_severity = {
            Severity.CRITICAL: [],
            Severity.HIGH: [],
            Severity.MEDIUM: [],
            Severity.LOW: [],
            Severity.INFO: []
        }
        
        for issue in self.issues:
            by_severity[issue.severity].append(issue)
        
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]:
            issues = by_severity[severity]
            if issues:
                print(f"\n{severity.value} ({len(issues)} issues):")
                for issue in issues[:5]:  # Show first 5 of each severity
                    print(f"  - [{issue.category}] {issue.item_id}: {issue.issue}")
                if len(issues) > 5:
                    print(f"  ... and {len(issues) - 5} more")
    
    def generate_report(self, result: DiagnosticResult, output_file: str = None):
        """Generate a diagnostic report"""
        report = {
            "diagnostic_result": {
                "timestamp": result.timestamp,
                "total_items_checked": result.total_items_checked,
                "total_issues": len(result.issues),
                "score": result.score,
                "can_seal": result.can_seal
            },
            "issues": [asdict(issue) for issue in result.issues]
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"\n📄 Report saved to: {output_file}")
        
        return report


def main():
    """Main entry point"""
    diagnostic = EvidenceChainDiagnostic()
    result = diagnostic.run_full_diagnostic()
    
    # Generate JSON report
    report_file = "/workspace/reports/evidence-chain-diagnostic-report.json"
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    diagnostic.generate_report(result, report_file)
    
    # Exit with appropriate code
    sys.exit(0 if result.can_seal else 1)


if __name__ == "__main__":
    main()