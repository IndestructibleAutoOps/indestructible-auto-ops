#!/usr/bin/env python3
"""
GL Self Auditor
==============
Audits governance operations and generates audit reports.

Critical Features:
- Forbidden phrase detection
- Evidence coverage calculation
- Operation auditing
- Violation trend analysis
- Audit report generation
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Define GovernanceResult here to avoid import issues
class GovernanceResult:
    def __init__(self, operation_id: str, status: str, violations: list, 
                 evidence_collected: list, quality_gates: dict, timestamp: str):
        self.operation_id = operation_id
        self.status = status
        self.violations = violations
        self.evidence_collected = evidence_collected
        self.quality_gates = quality_gates
        self.timestamp = timestamp

@dataclass
class AuditReport:
    """Audit report for governance operations"""
    audit_id: str
    operation_id: str
    audit_timestamp: str
    violations_found: int
    evidence_coverage: float
    quality_gate_results: Dict[str, bool]
    forbidden_phrases: List[Dict]
    recommendations: List[str]
    status: str  # "COMPLIANT", "NON_COMPLIANT", "WARNING"

class SelfAuditor:
    """
    Self-auditing engine that validates governance operations.
    
    Key responsibilities:
    - Detect forbidden phrases in reports
    - Calculate evidence coverage
    - Audit operations against contracts
    - Generate audit reports
    - Track violation trends
    """
    
    # Forbidden phrases with severity levels
    FORBIDDEN_PHRASES = {
        "CRITICAL": [
            "100% 完成",
            "完全符合",
            "已全部实现"
        ],
        "HIGH": [
            "应该是",
            "可能是",
            "我认为"
        ],
        "MEDIUM": [
            "基本上",
            "差不多",
            "应该"
        ],
        "LOW": [
            "可能",
            "也许",
            "大概"
        ]
    }
    
    # Approved replacements
    APPROVED_REPLACEMENTS = {
        "100% 完成": "基于已实现的功能集",
        "完全符合": "在[方面]与标准对齐",
        "已全部实现": "已实现[具体功能列表]",
        "应该是": "根据[证据]，建议",
        "可能是": "基于[证据]，推测",
        "我认为": "基于[证据]，分析表明"
    }
    
    def __init__(self, base_path: str = "/workspace/machine-native-ops"):
        self.base_path = Path(base_path)
        self.audit_logs_dir = self.base_path / "ecosystem" / "logs" / "audit-logs"
        self.audit_logs_dir.mkdir(parents=True, exist_ok=True)
    
    def audit(self, contract: Dict, result: GovernanceResult) -> AuditReport:
        """
        Audit a governance operation result.
        
        Args:
            contract: Governance contract used for validation
            result: GovernanceResult from validation
        
        Returns:
            AuditReport with audit findings and recommendations
        """
        audit_id = self._generate_audit_id()
        
        # Check for forbidden phrases
        forbidden_phrases = self._detect_forbidden_phrases(contract, result)
        
        # Calculate evidence coverage
        evidence_coverage = self._calculate_evidence_coverage(result)
        
        # Validate quality gates
        quality_gate_results = result.quality_gates
        
        # Determine audit status
        status = self._determine_audit_status(
            result.status,
            forbidden_phrases,
            quality_gate_results
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            result.violations,
            forbidden_phrases,
            quality_gate_results
        )
        
        audit_report = AuditReport(
            audit_id=audit_id,
            operation_id=result.operation_id,
            audit_timestamp=datetime.now().isoformat(),
            violations_found=len(result.violations) + len(forbidden_phrases),
            evidence_coverage=evidence_coverage,
            quality_gate_results=quality_gate_results,
            forbidden_phrases=forbidden_phrases,
            recommendations=recommendations,
            status=status
        )
        
        # Save audit report
        self._save_audit_report(audit_report)
        
        return audit_report
    
    def check_forbidden_phrases(self, text: str) -> List[Dict]:
        """
        Check text for forbidden phrases.
        
        Args:
            text: Text to check
        
        Returns:
            List of forbidden phrase detections with severity and position
        """
        detections = []
        
        for severity, phrases in self.FORBIDDEN_PHRASES.items():
            for phrase in phrases:
                if phrase in text:
                    # Find all occurrences
                    start = 0
                    while True:
                        pos = text.find(phrase, start)
                        if pos == -1:
                            break
                        
                        # Get context (20 chars before and after)
                        context_start = max(0, pos - 20)
                        context_end = min(len(text), pos + len(phrase) + 20)
                        context = text[context_start:context_end]
                        
                        detections.append({
                            "phrase": phrase,
                            "severity": severity,
                            "position": pos,
                            "context": context,
                            "replacement": self.APPROVED_REPLACEMENTS.get(phrase, "")
                        })
                        
                        start = pos + 1
        
        return detections
    
    def audit_operation(self, operation_id: str, operation_data: Dict) -> AuditReport:
        """
        Audit a complete operation.
        
        Args:
            operation_id: Operation identifier
            operation_data: Operation data including content and metadata
        
        Returns:
            AuditReport with full audit findings
        """
        # Check forbidden phrases in content
        content = operation_data.get("content", "")
        forbidden_phrases = self.check_forbidden_phrases(content)
        
        # Calculate evidence coverage
        evidence_links = operation_data.get("evidence_links", [])
        total_statements = operation_data.get("total_statements", len(evidence_links) + 1)
        evidence_coverage = len(evidence_links) / max(total_statements, 1)
        
        # Determine status
        critical_phrases = [p for p in forbidden_phrases if p.get("severity") == "CRITICAL"]
        status = "NON_COMPLIANT" if critical_phrases else "WARNING" if forbidden_phrases else "COMPLIANT"
        
        return AuditReport(
            audit_id=self._generate_audit_id(),
            operation_id=operation_id,
            audit_timestamp=datetime.now().isoformat(),
            violations_found=len(forbidden_phrases),
            evidence_coverage=evidence_coverage,
            quality_gate_results={},
            forbidden_phrases=forbidden_phrases,
            recommendations=self._generate_replacements(forbidden_phrases),
            status=status
        )
    
    def generate_audit_report(self, audit_report: AuditReport) -> str:
        """
        Generate a human-readable audit report.
        
        Args:
            audit_report: AuditReport object
        
        Returns:
            Formatted audit report as string
        """
        report = []
        report.append("=" * 80)
        report.append(f"Audit Report: {audit_report.audit_id}")
        report.append("=" * 80)
        report.append(f"Operation ID: {audit_report.operation_id}")
        report.append(f"Audit Timestamp: {audit_report.audit_timestamp}")
        report.append(f"Status: {audit_report.status}")
        report.append("")
        report.append(f"Violations Found: {audit_report.violations_found}")
        report.append(f"Evidence Coverage: {audit_report.evidence_coverage:.2%}")
        report.append("")
        
        if audit_report.forbidden_phrases:
            report.append("Forbidden Phrases:")
            for phrase in audit_report.forbidden_phrases:
                report.append(f"  [{phrase['severity']}] {phrase['phrase']}")
                report.append(f"    Context: ...{phrase['context']}...")
                if phrase['replacement']:
                    report.append(f"    Replacement: {phrase['replacement']}")
                report.append("")
        
        if audit_report.quality_gate_results:
            report.append("Quality Gate Results:")
            for gate, passed in audit_report.quality_gate_results.items():
                status_icon = "✅" if passed else "❌"
                report.append(f"  {status_icon} {gate}: {'PASS' if passed else 'FAIL'}")
            report.append("")
        
        if audit_report.recommendations:
            report.append("Recommendations:")
            for i, rec in enumerate(audit_report.recommendations, 1):
                report.append(f"  {i}. {rec}")
            report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def report(self, report: AuditReport):
        """
        Save and emit audit report.
        
        Args:
            report: AuditReport to save
        """
        self._save_audit_report(report)
        self._emit_governance_event(report)
    
    def _generate_audit_id(self) -> str:
        """Generate unique audit ID"""
        return f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def _detect_forbidden_phrases(self, contract: Dict, result: GovernanceResult) -> List[Dict]:
        """Detect forbidden phrases in contract and result"""
        forbidden = []
        
        # Check contract
        contract_str = json.dumps(contract, ensure_ascii=False)
        contract_phrases = self.check_forbidden_phrases(contract_str)
        forbidden.extend(contract_phrases)
        
        # Check result
        result_str = json.dumps(result.violations, ensure_ascii=False)
        result_phrases = self.check_forbidden_phrases(result_str)
        forbidden.extend(result_phrases)
        
        return forbidden
    
    def _calculate_evidence_coverage(self, result: GovernanceResult) -> float:
        """Calculate evidence coverage percentage"""
        if not result.evidence_collected:
            return 0.0
        
        # Simplified: count evidence types vs expected
        expected_types = 3  # source_file, contract_reference, validation_output
        actual_types = len(set(e.get("type") for e in result.evidence_collected))
        
        return actual_types / expected_types
    
    def _determine_audit_status(self, result_status: str, forbidden_phrases: List, quality_gates: Dict) -> str:
        """Determine overall audit status"""
        critical_forbidden = [p for p in forbidden_phrases if p.get("severity") == "CRITICAL"]
        failed_gates = [k for k, v in quality_gates.items() if not v]
        
        if result_status == "FAIL" or critical_forbidden or failed_gates:
            return "NON_COMPLIANT"
        
        if forbidden_phrases or result_status == "WARNING":
            return "WARNING"
        
        return "COMPLIANT"
    
    def _generate_recommendations(self, violations: List, forbidden_phrases: List, quality_gates: Dict) -> List[str]:
        """Generate audit recommendations"""
        recommendations = []
        
        if violations:
            recommendations.append("Review and fix governance violations")
        
        if forbidden_phrases:
            recommendations.append("Replace forbidden phrases with approved alternatives")
        
        failed_gates = [k for k, v in quality_gates.items() if not v]
        if failed_gates:
            recommendations.append(f"Fix failed quality gates: {', '.join(failed_gates)}")
        
        if not recommendations:
            recommendations.append("Operation is compliant with governance requirements")
        
        return recommendations
    
    def _generate_replacements(self, forbidden_phrases: List) -> List[str]:
        """Generate replacement recommendations"""
        replacements = []
        
        for phrase in forbidden_phrases:
            replacement = phrase.get("replacement")
            if replacement:
                replacements.append(
                    f"Replace '{phrase['phrase']}' with '{replacement}'"
                )
        
        return replacements
    
    def _save_audit_report(self, audit_report: AuditReport):
        """Save audit report to file"""
        report_dir = self.audit_logs_dir / datetime.now().strftime("%Y-%m")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = report_dir / f"{audit_report.audit_id}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(audit_report.__dict__, f, ensure_ascii=False, indent=2)
        
        # Also save human-readable version
        text_file = report_file.with_suffix('.txt')
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_audit_report(audit_report))
    
    def _emit_governance_event(self, audit_report: AuditReport):
        """Emit governance event for audit completion"""
        event = {
            "event_type": "audit_completed",
            "audit_id": audit_report.audit_id,
            "operation_id": audit_report.operation_id,
            "status": audit_report.status,
            "timestamp": audit_report.audit_timestamp,
            "violations": audit_report.violations_found
        }
        
        # Save to audit log
        audit_log = self.audit_logs_dir / "audit_events.log"
        with open(audit_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event) + "\n")