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
    
    def __init__(self, base_path: str = "/workspace/machine-native-ops"):
        self.base_path = Path(base_path)
        self.contracts_dir = self.base_path / "ecosystem" / "contracts"
        self.contracts = {}
        self._load_contracts()
    
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
                
                # Check quality gates
                contract_gates = self._check_quality_gates(contract, operation)
                quality_gates.update(contract_gates)
        
        # Determine overall status
        status = self._determine_status(violations, quality_gates)
        
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
        """Check quality gates"""
        gates = {}
        quality_gates = contract.get("verify", {}).get("quality_gates", [])
        
        for gate in quality_gates:
            gate_name = gate.get("gate")
            threshold = gate.get("threshold", 0.90)
            
            # Simplified implementation
            if gate_name == "evidence_coverage":
                evidence_links = operation.get("evidence_links", [])
                total_statements = operation.get("total_statements", 1)
                coverage = len(evidence_links) / max(total_statements, 1)
                gates[gate_name] = coverage >= threshold
            
            elif gate_name == "forbidden_phrases":
                content = operation.get("content", "")
                count = content.count("100% 完成")
                gates[gate_name] = count == threshold
        
        return gates
    
    def _determine_status(self, violations: List[Dict], quality_gates: Dict) -> str:
        """Determine overall validation status"""
        critical_violations = [v for v in violations if v.get("severity") == "CRITICAL"]
        
        if critical_violations:
            return "FAIL"
        
        failed_gates = [k for k, v in quality_gates.items() if not v]
        if failed_gates:
            return "FAIL"
        
        if violations:
            return "WARNING"
        
        return "PASS"