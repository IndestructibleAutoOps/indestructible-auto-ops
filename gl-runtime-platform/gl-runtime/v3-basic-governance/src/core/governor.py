"""V3 Basic Governance - 基礎治理引擎"""
from typing import Dict, List, Optional
from shared.interfaces.governance_interface import GovernanceInterface

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
