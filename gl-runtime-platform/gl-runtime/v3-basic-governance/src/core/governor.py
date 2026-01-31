# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: gl_platform_universegl_platform_universe.governance-core
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL90_99-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""V3 Basic Governance - 基礎治理引擎"""
from typing import Dict, List, Optional
from shared.interfaces.gl_platform_universegl_platform_universe.governance_interface import GovernanceInterface

class Governor(GovernanceInterface):
    def __init__(self):
        self.rules = []
        self.violations = []
    
    def validate(self, context: dict) -> bool:
        for rule in self.rules:
            if not self._check_rule(rule, context):
                self.violations.append({"rule": rule["name"], "context": context})
                return False
        return True
    
    def enforce(self, action: dict) -> dict:
        if self.validate(action):
            return {"status": "allowed", "action": action}
        return {"status": "blocked", "violations": self.violations}
    
    def add_rule(self, rule: Dict):
        self.rules.append(rule)
    
    def _check_rule(self, rule: Dict, context: Dict) -> bool:
        rule_type = rule.get("type", "allow")
        condition = rule.get("condition", lambda x: True)
        return condition(context) if callable(condition) else True
