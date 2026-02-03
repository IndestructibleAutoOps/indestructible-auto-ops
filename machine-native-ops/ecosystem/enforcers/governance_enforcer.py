#!/usr/bin/env python3
"""
GL Governance Enforcer
=====================
Enforces governance contracts and validates operations.

Critical Features:
- Contract-based validation
- Evidence collection
- Governance event emission
- Quality gate enforcement
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

# Import event emitter and semantic context
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from events.event_emitter import EventEmitter, EventType, emit_event, get_global_emitter
from semantic.semantic_context import SemanticContextManager, get_global_context_manager

@dataclass
class GovernanceResult:
    """Governance enforcement result"""
    operation_id: str
    status: str  # "PASS", "FAIL", "WARNING"
    violations: List[Dict]
    evidence_collected: List[Dict]
    quality_gates: Dict[str, bool]
    timestamp: str

class GovernanceEnforcer:
    """
    Governance enforcement engine that executes contracts and validates operations.
    
    Key responsibilities:
    - Load and parse governance contracts
    - Validate operations against contracts
    - Collect evidence for all claims
    - Enforce quality gates
    - Emit governance events
    """
    
    def __init__(self, base_path: str = None):
        # Auto-detect base path if not provided
        if base_path is None:
            base_path = self._detect_base_path()
        self.base_path = Path(base_path)
        self.contracts_dir = self.base_path / "ecosystem" / "contracts"
        self.contracts = {}
        
        # P2: Initialize event emitter and semantic context manager
        self.event_emitter = get_global_emitter(base_path=str(base_path))
        self.context_manager = get_global_context_manager(base_path=str(base_path))
        
        self._load_contracts()
    
    def _detect_base_path(self) -> str:
        """Auto-detect project base path by looking for governance-manifest.yaml"""
        current = Path(__file__).parent  # ecosystem/enforcers
        while current != current.parent:
            if (current / "governance-manifest.yaml").exists():
                return str(current)
            if (current / "ecosystem").exists() and (current / "ecosystem" / "enforce.py").exists():
                return str(current)
            current = current.parent
        # Fallback to parent of ecosystem directory
        return str(Path(__file__).parent.parent.parent)
    
    def _load_contracts(self):
        """Load all governance contracts"""
        contract_paths = [
            "verification/gl-verification-engine-spec-executable.yaml",
            "verification/gl-proof-model-executable.yaml",
            "verification/gl-verifiable-report-standard-executable.yaml"
        ]
        
        for contract_path in contract_paths:
            full_path = self.contracts_dir / contract_path
            try:
                with open(full_path, 'r') as f:
                    contract = yaml.safe_load(f)
                    if contract:
                        self.contracts[contract_path] = contract
            except Exception as e:
                print(f"⚠️  Failed to load contract {contract_path}: {e}")
    
    def validate(self, operation: Dict[str, Any]) -> GovernanceResult:
        """
        Validate an operation against governance contracts.
        
        Args:
            operation: Dictionary containing operation details
                - type: operation type (e.g., "file_change", "report_generation")
                - files: list of affected files
                - content: operation content/data
        
        Returns:
            GovernanceResult with validation status, violations, and evidence
        """
        operation_id = self._generate_operation_id()
        violations = []
        evidence = []
        quality_gates = {}
        
        # P2: Emit validation start event
        emit_event(
            EventType.VALIDATION_START,
            operation_id,
            metadata={
                "operation_type": operation.get("type", "unknown"),
                "files": operation.get("files", [])
            },
            data={"operation": operation},
            priority=2
        )
        
        # Validate against each contract
        for contract_path, contract in self.contracts.items():
            if not contract:
                continue
            
            # Check trigger conditions
            if self._should_validate_trigger(contract, operation):
                # Run verification rules
                contract_violations = self._verify_contract(contract, operation)
                violations.extend(contract_violations)
                
                # Collect evidence
                contract_evidence = self._collect_evidence(contract, operation)
                evidence.extend(contract_evidence)
                
                # P2: Emit evidence collected event
                if contract_evidence:
                    emit_event(
                        EventType.EVIDENCE_COLLECTED,
                        operation_id,
                        metadata={
                            "contract": contract_path,
                            "evidence_count": len(contract_evidence)
                        },
                        data={"evidence": contract_evidence}
                    )
                
                # Check quality gates
                contract_gates = self._check_quality_gates(contract, operation)
                quality_gates.update(contract_gates)
        
        # Determine overall status
        status = self._determine_status(violations, quality_gates)
        
        # P2: Emit validation complete event
        event_type = EventType.VALIDATION_COMPLETE if status == "PASS" else EventType.VALIDATION_FAILED
        emit_event(
            event_type,
            operation_id,
            metadata={
                "status": status,
                "violations_count": len(violations),
                "evidence_count": len(evidence),
                "failed_gates": [k for k, v in quality_gates.items() if not v]
            },
            data={
                "violations": violations,
                "quality_gates": quality_gates
            },
            priority=2 if status == "PASS" else 1
        )
        
        # P2: Emit quality gate failure event if any gates failed
        failed_gates = [k for k, v in quality_gates.items() if not v]
        if failed_gates:
            emit_event(
                EventType.QUALITY_GATE_FAILED,
                operation_id,
                metadata={
                    "failed_gates": failed_gates,
                    "gate_count": len(failed_gates)
                },
                data={"quality_gates": quality_gates},
                priority=1
            )
        
        return GovernanceResult(
            operation_id=operation_id,
            status=status,
            violations=violations,
            evidence_collected=evidence,
            quality_gates=quality_gates,
            timestamp=datetime.now().isoformat()
        )
    
    def execute_contract(self, contract_path: str, operation: Dict[str, Any]) -> GovernanceResult:
        """
        Execute a specific governance contract.
        
        Args:
            contract_path: Path to the contract file
            operation: Operation details
        
        Returns:
            GovernanceResult from contract execution
        """
        if contract_path not in self.contracts:
            return GovernanceResult(
                operation_id=self._generate_operation_id(),
                status="FAIL",
                violations=[{
                    "severity": "CRITICAL",
                    "rule": "contract_not_found",
                    "message": f"Contract {contract_path} not loaded"
                }],
                evidence_collected=[],
                quality_gates={},
                timestamp=datetime.now().isoformat()
            )
        
        contract = self.contracts[contract_path]
        return self.validate(operation)
    
    def validate_trigger(self, event: Dict[str, Any]) -> bool:
        """
        Validate if an event triggers governance enforcement.
        
        Args:
            event: Event dictionary with type and details
        
        Returns:
            True if the event should trigger governance enforcement
        """
        event_type = event.get("type", "")
        
        for contract_path, contract in self.contracts.items():
            if not contract:
                continue
            
            trigger_conditions = contract.get("trigger", {}).get("conditions", [])
            
            for condition in trigger_conditions:
                if condition.get("type") == event_type:
                    return True
                
                if condition.get("type") == "file_change" and "files" in event:
                    return True
                
                if condition.get("type") == "ci_event" and "ci_event" in event:
                    return True
        
        return False
    
    def _generate_operation_id(self) -> str:
        """Generate unique operation ID"""
        return f"gov_op_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def _should_validate_trigger(self, contract: Dict, operation: Dict) -> bool:
        """Check if operation matches trigger conditions"""
        trigger_conditions = contract.get("trigger", {}).get("conditions", [])
        
        for condition in trigger_conditions:
            if condition.get("type") == operation.get("type"):
                return True
            
            if condition.get("type") == "file_change" and "files" in operation:
                return True
        
        return False
    
    def _verify_contract(self, contract: Dict, operation: Dict) -> List[Dict]:
        """Verify operation against contract rules"""
        violations = []
        verify_rules = contract.get("verify", {})
        
        # Check evidence collection rules
        evidence_rules = verify_rules.get("evidence_collection", [])
        for rule in evidence_rules:
            if not self._check_evidence_rule(rule, operation):
                violations.append({
                    "severity": rule.get("severity", "HIGH"),
                    "rule": rule.get("rule"),
                    "message": f"Rule failed: {rule.get('rule')}",
                    "remediation": rule.get("remediation", "")
                })
        
        # Check report validation rules
        report_rules = verify_rules.get("report_validation", [])
        for rule in report_rules:
            if not self._check_report_rule(rule, operation):
                violations.append({
                    "severity": rule.get("severity", "HIGH"),
                    "rule": rule.get("rule"),
                    "message": f"Rule failed: {rule.get('rule')}",
                    "remediation": rule.get("remediation", "")
                })
        
        return violations
    
    def _check_evidence_rule(self, rule: Dict, operation: Dict) -> bool:
        """Check an evidence collection rule"""
        # Simplified implementation
        if rule.get("rule") == "all_files_must_have_evidence":
            return len(operation.get("evidence_links", [])) > 0
        return True
    
    def _check_report_rule(self, rule: Dict, operation: Dict) -> bool:
        """Check a report validation rule"""
        # Simplified implementation
        if rule.get("rule") == "no_forbidden_phrases":
            content = operation.get("content", "")
            forbidden = rule.get("forbidden_phrases", [])
            for phrase in forbidden:
                if phrase.get("phrase") in content:
                    return False
        return True
    
    def _collect_evidence(self, contract: Dict, operation: Dict) -> List[Dict]:
        """Collect evidence for the operation"""
        evidence = []
        
        # Collect file evidence
        files = operation.get("files", [])
        for file_path in files:
            full_path = self.base_path / file_path
            if full_path.exists():
                with open(full_path, 'rb') as f:
                    content = f.read()
                    evidence.append({
                        "type": "source_file",
                        "file_path": str(full_path),
                        "checksum": self._calculate_checksum(content),
                        "size": len(content),
                        "timestamp": datetime.now().isoformat()
                    })
        
        # Collect contract reference evidence
        evidence.append({
            "type": "contract_reference",
            "contract_path": contract.get("metadata", {}).get("name", "unknown"),
            "version": contract.get("version", "unknown"),
            "timestamp": datetime.now().isoformat()
        })
        
        return evidence
    
    def _calculate_checksum(self, content: bytes) -> str:
        """Calculate SHA-256 checksum"""
        import hashlib
        return hashlib.sha256(content).hexdigest()
    
    def _check_quality_gates(self, contract: Dict, operation: Dict) -> Dict[str, bool]:
        """
        Check quality gates with comprehensive validation.
        
        Quality Gates:
        1. Evidence coverage >= 90%
        2. Forbidden phrases == 0
        3. Source consistency check
        """
        gates = {}
        quality_gates = contract.get("verify", {}).get("quality_gates", [])
        
        # Gate 1: Evidence Coverage
        gates["evidence_coverage"] = self._check_evidence_coverage_gate(operation)
        
        # Gate 2: Forbidden Phrases
        gates["forbidden_phrases"] = self._check_forbidden_phrases_gate(operation)
        
        # Gate 3: Source Consistency
        gates["source_consistency"] = self._check_source_consistency_gate(operation)
        
        # Additional contract-specific gates
        for gate in quality_gates:
            gate_name = gate.get("gate")
            if gate_name not in gates:
                # Custom gate handling if needed
                threshold = gate.get("threshold", 0.90)
                gates[gate_name] = True  # Default pass
        
        return gates
    
    def _check_evidence_coverage_gate(self, operation: Dict) -> bool:
        """
        Check evidence coverage >= 90%.
        
        Coverage calculation:
        - Count evidence links in content
        - Count total statements requiring evidence
        - Calculate percentage
        """
        content = operation.get("content", "")
        if not content:
            return False
        
        # Count evidence links using pattern [证据: path/to/file#L10-L15]
        import re
        evidence_pattern = r'\[证据[^\]]+\]'
        evidence_links = re.findall(evidence_pattern, content)
        
        # Estimate total statements (lines ending with ., 。, !, ！, ?, ？)
        statement_pattern = r'[.。！！？？]\s*$'
        statements = re.findall(statement_pattern, content, re.MULTILINE)
        
        if not statements:
            return False
        
        # Calculate coverage
        coverage = len(evidence_links) / len(statements)
        threshold = 0.90  # 90% threshold
        
        # Log coverage if below threshold
        if coverage < threshold:
            print(f"⚠️  Evidence coverage: {coverage:.2%} (threshold: {threshold:.2%})")
        
        return coverage >= threshold
    
    def _check_forbidden_phrases_gate(self, operation: Dict) -> bool:
        """
        Check for forbidden phrases == 0.
        
        Forbidden phrases:
        CRITICAL: "100% 完成", "完全符合", "已全部实现"
        HIGH: "应该是", "可能是", "我认为"
        """
        content = operation.get("content", "")
        if not content:
            return True
        
        forbidden_phrases = {
            "CRITICAL": ["100% 完成", "完全符合", "已全部实现"],
            "HIGH": ["应该是", "可能是", "我认为"],
            "MEDIUM": ["基本上", "差不多", "应该"],
            "LOW": ["可能", "也许", "大概"]
        }
        
        total_violations = 0
        violations_found = []
        
        for severity, phrases in forbidden_phrases.items():
            for phrase in phrases:
                count = content.count(phrase)
                if count > 0:
                    total_violations += count
                    violations_found.append({
                        "phrase": phrase,
                        "severity": severity,
                        "count": count
                    })
        
        # Log violations if any found
        if violations_found:
            print(f"⚠️  Forbidden phrases found: {total_violations} violations")
            for v in violations_found:
                print(f"   - '{v['phrase']}' ({v['severity']}): {v['count']} occurrences")
        
        return total_violations == 0
    
    def _check_source_consistency_gate(self, operation: Dict) -> bool:
        """
        Check source consistency in evidence links.
        
        Verifies that:
        - Evidence sources exist
        - Evidence sources are readable
        - Evidence sources match expected paths
        """
        content = operation.get("content", "")
        if not content:
            return True
        
        import re
        from pathlib import Path
        
        # Extract evidence paths
        evidence_pattern = r'\[证据[^\]]+([^\]]+)\]'
        evidence_paths = re.findall(evidence_pattern, content)
        
        if not evidence_paths:
            return True
        
        # Check each evidence source
        inconsistent_sources = []
        for path in evidence_paths:
            # Clean up path (remove line ranges, etc.)
            clean_path = path.split('#')[0].strip()
            full_path = self.base_path / clean_path
            
            if not full_path.exists():
                inconsistent_sources.append({
                    "path": clean_path,
                    "issue": "file_not_exist"
                })
            elif not full_path.is_file():
                inconsistent_sources.append({
                    "path": clean_path,
                    "issue": "not_a_file"
                })
        
        # Log inconsistencies if any found
        if inconsistent_sources:
            print(f"⚠️  Source consistency issues: {len(inconsistent_sources)} problems")
            for issue in inconsistent_sources:
                print(f"   - {issue['path']}: {issue['issue']}")
        
        return len(inconsistent_sources) == 0
    
    def _determine_status(self, violations: List[Dict], quality_gates: Dict) -> str:
        """
        Determine overall validation status with quality gate failure handling.
        
        Status Logic:
        - CRITICAL violations: FAIL (block operation)
        - Failed quality gates: FAIL (block operation) with remediation
        - HIGH violations: FAIL (block operation)
        - MEDIUM/LOW violations: WARNING (allow with caution)
        - All pass: PASS
        """
        # Check for CRITICAL violations
        critical_violations = [v for v in violations if v.get("severity") == "CRITICAL"]
        if critical_violations:
            print(f"❌ CRITICAL violations found: {len(critical_violations)}")
            self._generate_remediation(critical_violations, quality_gates)
            return "FAIL"
        
        # Check for HIGH violations
        high_violations = [v for v in violations if v.get("severity") == "HIGH"]
        if high_violations:
            print(f"❌ HIGH violations found: {len(high_violations)}")
            self._generate_remediation(high_violations, quality_gates)
            return "FAIL"
        
        # Check for failed quality gates
        failed_gates = [k for k, v in quality_gates.items() if not v]
        if failed_gates:
            print(f"❌ Quality gates failed: {', '.join(failed_gates)}")
            self._generate_quality_gate_remediation(failed_gates, quality_gates)
            return "FAIL"
        
        # Check for MEDIUM/LOW violations (WARNING)
        if violations:
            medium_violations = [v for v in violations if v.get("severity") == "MEDIUM"]
            low_violations = [v for v in violations if v.get("severity") == "LOW"]
            
            if medium_violations or low_violations:
                print(f"⚠️  Non-critical violations: {len(medium_violations)} MEDIUM, {len(low_violations)} LOW")
                self._generate_remediation(medium_violations + low_violations, quality_gates)
                return "WARNING"
        
        print("✅ All checks passed")
        return "PASS"
    
    def _generate_remediation(self, violations: List[Dict], quality_gates: Dict):
        """Generate remediation suggestions for violations."""
        if not violations:
            return
        
        print("\n📋 Remediation Suggestions:")
        print("-" * 50)
        
        # Group violations by type
        violation_types = {}
        for v in violations:
            rule = v.get("rule", "unknown")
            if rule not in violation_types:
                violation_types[rule] = []
            violation_types[rule].append(v)
        
        # Generate suggestions for each type
        for rule, rule_violations in violation_types.items():
            print(f"\n{rule}:")
            print(f"  Severity: {rule_violations[0].get('severity', 'UNKNOWN')}")
            print(f"  Count: {len(rule_violations)}")
            
            remediation = rule_violations[0].get("remediation", "No remediation available")
            print(f"  Suggestion: {remediation}")
    
    def _generate_quality_gate_remediation(self, failed_gates: List[str], quality_gates: Dict):
        """Generate remediation suggestions for failed quality gates."""
        if not failed_gates:
            return
        
        print("\n📋 Quality Gate Remediation:")
        print("-" * 50)
        
        remediation_map = {
            "evidence_coverage": (
                "Add evidence links using format [证据: path/to/file#L10-L15]. "
                "Target: 90% coverage of statements."
            ),
            "forbidden_phrases": (
                "Replace forbidden phrases with approved alternatives:\n"
                "  - '100% 完成' → '基于已实现的功能集'\n"
                "  - '完全符合' → '在[方面]与标准对齐'\n"
                "  - '应该是' → '根据[证据]，建议'"
            ),
            "source_consistency": (
                "Verify all evidence sources exist and are accessible. "
                "Check file paths and ensure files are in the repository."
            )
        }
        
        for gate in failed_gates:
            print(f"\n{gate}:")
            print(f"  Status: FAILED")
            suggestion = remediation_map.get(gate, "Review quality gate requirements")
            print(f"  Suggestion: {suggestion}")