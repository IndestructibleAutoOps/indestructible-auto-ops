"""
Arbitration Rule Engine
Applies rules to make conflict resolution decisions
"""
# MNGA-002: Import organization needs review
import os
import yaml
from typing import List, Dict, Optional, Callable
from datetime import datetime
from .arbitrator import ArbitrationDecision, Decision


class ArbitrationRuleEngine:
    """Rule-based decision engine for arbitration"""
    
    # Define rules
    RULES = {
        # Rule 1: High priority module API - prefer internal
        "HIGH_PRIORITY_MODULE_API": {
            "condition": lambda internal, external: (
                internal.get("confidence", 0.0) > 0.8 and
                internal.get("metadata", {}).get("module") in [
                    "gl-platform-services",
                    "gl-execution-runtime",
                    "gl-governance"
                ]
            ),
            "decision": Decision.INTERNAL,
            "reason": "Core module API - using internal implementation ensures compatibility",
            "severity": "CRITICAL"
        },
        
        # Rule 2: Security vulnerability fix - prefer external
        "SECURITY_VULNERABILITY_FIX": {
            "condition": lambda internal, external: (
                external.get("metadata", {}).get("category") == "security" and
                external.get("metadata", {}).get("type") == "vulnerability_fix"
            ),
            "decision": Decision.EXTERNAL,
            "reason": "Security vulnerability fix - adopting external best practices for security",
            "action": "highlight_security_impact",
            "severity": "CRITICAL"
        },
        
        # Rule 3: Dependency version update - require hybrid
        "DEPENDENCY_VERSION_UPDATE": {
            "condition": lambda internal, external: (
                internal.get("metadata", {}).get("type") == "dependency" and
                external.get("metadata", {}).get("type") == "dependency" and
                internal.get("metadata", {}).get("version") != external.get("metadata", {}).get("version")
            ),
            "decision": Decision.HYBRID,
            "reason": "Dependency version update requires compatibility assessment",
            "requirement": "require_human_review",
            "severity": "HIGH"
        },
        
        # Rule 4: Code style - prefer internal
        "CODE_STYLE_PREFERENCE": {
            "condition": lambda internal, external: (
                internal.get("metadata", {}).get("type") == "style" and
                internal.get("confidence", 0.0) > 0.7
            ),
            "decision": Decision.INTERNAL,
            "reason": "Code style - following project conventions for consistency",
            "severity": "LOW"
        },
        
        # Rule 5: Environment compatibility - prefer internal
        "ENVIRONMENT_COMPATIBILITY": {
            "condition": lambda internal, external: (
                internal.get("metadata", {}).get("environment") == "production" and
                external.get("metadata", {}).get("environment") != "production"
            ),
            "decision": Decision.INTERNAL,
            "reason": "Environment compatibility - using production-tested implementation",
            "severity": "HIGH"
        },
        
        # Rule 6: Breaking API changes - reject or require review
        "BREAKING_API_CHANGE": {
            "condition": lambda internal, external: (
                external.get("metadata", {}).get("breaking_change", False) and
                internal.get("confidence", 0.0) > 0.6
            ),
            "decision": Decision.INTERNAL,
            "reason": "Breaking API change detected - maintaining backward compatibility",
            "requirement": "require_migration_plan",
            "severity": "CRITICAL"
        },
        
        # Rule 7: Low confidence both - reject
        "LOW_CONFIDENCE_BOTH": {
            "condition": lambda internal, external: (
                internal.get("confidence", 0.0) < 0.6 and
                external.get("confidence", 0.0) < 0.6
            ),
            "decision": Decision.REJECT,
            "reason": "Low confidence from both sources - insufficient information for decision",
            "action": "request_human_intervention",
            "severity": "HIGH"
        }
    }
    
    def __init__(self, rules_path: Optional[str] = None):
        """Initialize rule engine"""
        self.rules = self._load_rules(rules_path)
        
    def _load_rules(self, rules_path: Optional[str]) -> Dict:
        """Load rules from file or directory or use defaults"""
        if rules_path and os.path.exists(rules_path):
            if os.path.isdir(rules_path):
                # Load all YAML files from directory
                import glob
                for rule_file in glob.glob(os.path.join(rules_path, "*.yaml")):
                    with open(rule_file, 'r') as f:
                        custom_rules = yaml.safe_load(f)
                        if custom_rules:
                            self.RULES.update(custom_rules)
            else:
                # Load single file
                with open(rules_path, 'r') as f:
                    custom_rules = yaml.safe_load(f)
                    if custom_rules:
                        self.RULES.update(custom_rules)
        return self.RULES
    
    def apply_rules(self, internal_result: Dict, 
                   external_result: Dict) -> Optional[ArbitrationDecision]:
        """
        Apply rules to make decision
        
        Args:
            internal_result: Internal reasoning result
            external_result: External reasoning result
            
        Returns:
            ArbitrationDecision if a rule matches, None otherwise
        """
        for rule_name, rule in self.rules.items():
            try:
                if rule["condition"](internal_result, external_result):
                    return ArbitrationDecision(
                        decision=rule["decision"],
                        reason=rule["reason"],
                        internal_confidence=internal_result.get("confidence", 0.0),
                        external_confidence=external_result.get("confidence", 0.0),
                        rule_used=rule_name,
                        severity=rule.get("severity", "MEDIUM")
                    )
            except Exception as e:
                # Log error but continue to next rule
                print(f"Warning: Rule {rule_name} failed: {e}")
                continue
        
        return None
    
    def add_rule(self, name: str, condition: Callable, 
                decision: Decision, reason: str, 
                severity: str = "MEDIUM", **kwargs):
        """
        Add a new rule
        
        Args:
            name: Rule name
            condition: Lambda function for rule condition
            decision: Decision to make if condition matches
            reason: Reason for decision
            severity: Severity level
            **kwargs: Additional rule properties
        """
        rule = {
            "condition": condition,
            "decision": decision,
            "reason": reason,
            "severity": severity
        }
        rule.update(kwargs)
        self.rules[name] = rule
    
    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name"""
        if name in self.rules:
            del self.rules[name]
            return True
        return False
    
    def get_rule(self, name: str) -> Optional[Dict]:
        """Get a rule by name"""
        return self.rules.get(name)
    
    def list_rules(self) -> List[str]:
        """List all rule names"""
        return list(self.rules.keys())
    
    def export_rules(self, output_path: str):
        """Export rules to YAML file"""
        export_data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "version": "1.0.0",
                "rule_count": len(self.rules)
            },
            "rules": {}
        }
        
        for name, rule in self.rules.items():
            # Can't serialize lambda functions, so we store rule metadata
            export_data["rules"][name] = {
                "decision": rule["decision"].value,
                "reason": rule["reason"],
                "severity": rule.get("severity", "MEDIUM"),
                "note": "Condition function not serializable - needs manual redefinition"
            }
        
        with open(output_path, 'w') as f:
            yaml.dump(export_data, f, default_flow_style=False)
        
        print(f"Rules exported to {output_path}")


if __name__ == "__main__":
    # Test rule engine
    engine = ArbitrationRuleEngine()
    
    print(f"Loaded {len(engine.list_rules())} rules:")
    for rule_name in engine.list_rules():
        print(f"  - {rule_name}")
    
    # Test rule application
    internal = {
        "answer": "Use internal API",
        "confidence": 0.92,
        "metadata": {
            "module": "gl-execution-runtime",
            "type": "api"
        }
    }
    
    external = {
        "answer": "Use external best practice",
        "confidence": 0.85,
        "metadata": {
            "type": "api"
        }
    }
    
    decision = engine.apply_rules(internal, external)
    
    if decision:
        print(f"\nRule matched: {decision.rule_used}")
        print(f"Decision: {decision.decision.value}")
        print(f"Reason: {decision.reason}")
    else:
        print("\nNo rules matched")
    
    # Export rules
    engine.export_rules("/workspace/machine-native-ops/ecosystem/reasoning/dual_path/arbitration/rules_export.yaml")