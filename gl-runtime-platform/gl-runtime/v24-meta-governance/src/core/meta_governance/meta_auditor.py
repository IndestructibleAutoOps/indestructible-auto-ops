# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: gl_platform_universegl_platform_universe.governance-core
# @GL-audit-trail: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/audit-trails/GL90_99-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""GL Runtime V24 - Meta Auditor (URSS Compliant)"""
from typing import Any, Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MetaAuditResult:
    rule_name: str
    is_valid: bool
    is_falsifiable: bool
    is_consistent: bool
    evidence: Dict[str, Any]

class MetaAuditor:
    """
    V24 Meta Auditor
    審計治理規則本身
    確保治理層的自洽性
    """
    
    def __init__(self):
        self._audits: List[MetaAuditResult] = []
    
    def audit_rule(self, rule_name: str, rule_definition: Dict[str, Any]) -> MetaAuditResult:
        """審計單個治理規則"""
        result = MetaAuditResult(
            rule_name=rule_name,
            is_valid=self._validate_rule(rule_definition),
            is_falsifiable=self._check_falsifiable(rule_definition),
            is_consistent=self._check_consistency(rule_definition),
            evidence={"rule": rule_definition, "timestamp": datetime.utcnow().isoformat()}
        )
        self._audits.append(result)
        return result
    
    def _validate_rule(self, rule: Dict[str, Any]) -> bool:
        required_fields = ["applies_to", "requires", "evidence"]
        return all(f in rule for f in required_fields)
    
    def _check_falsifiable(self, rule: Dict[str, Any]) -> bool:
        return "falsifiable_by" in rule and len(rule.get("falsifiable_by", [])) > 0
    
    def _check_consistency(self, rule: Dict[str, Any]) -> bool:
        forbids = rule.get("forbids", [])
        requires = rule.get("requires", [])
        return not any(f in requires for f in forbids)
    
    def get_audit_history(self) -> List[MetaAuditResult]:
        return self._audits.copy()
