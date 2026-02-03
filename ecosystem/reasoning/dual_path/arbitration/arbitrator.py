"""
Core Arbitrator
Makes decisions between internal and external reasoning results
"""
import os
import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import yaml
from enum import Enum


class Decision(Enum):
    """Arbitration decision types"""
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
    HYBRID = "HYBRID"
    REJECT = "REJECT"


class ArbitrationDecision:
    """Result of arbitration process"""
    
    def __init__(self, decision: Decision, reason: str, 
                 internal_confidence: float, external_confidence: float,
                 rule_used: Optional[str] = None, severity: str = "MEDIUM",
                 final_answer: Optional[str] = None):
        self.decision = decision
        self.reason = reason
        self.internal_confidence = internal_confidence
        self.external_confidence = external_confidence
        self.rule_used = rule_used
        self.severity = severity
        self.final_answer = final_answer
        
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "decision": self.decision.value,
            "reason": self.reason,
            "internal_confidence": self.internal_confidence,
            "external_confidence": self.external_confidence,
            "rule_used": self.rule_used,
            "severity": self.severity,
            "final_answer": self.final_answer,
            "confidence_delta": abs(self.internal_confidence - self.external_confidence)
        }


class Arbitrator:
    """Core arbitrator for dual-path reasoning"""
    
    def __init__(self, config_path: str = "ecosystem/contracts/reasoning/dual_path_spec.yaml"):
        """Initialize arbitrator"""
        self.config = self._load_config(config_path)
        self.arbitration_config = self.config["spec"]["arbitration"]
        
        # Import rule engine with rules_path from config if available
        from .rule_engine import ArbitrationRuleEngine
        rules_path = self.arbitration_config.get("rules_path")
        self.rule_engine = ArbitrationRuleEngine(rules_path=rules_path) if rules_path else ArbitrationRuleEngine()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {"spec": {"arbitration": {}}}
    
    def arbitrate(self, task_spec: str, 
                  internal_result: Dict, 
                  external_result: Dict) -> ArbitrationDecision:
        """
        Make arbitration decision between internal and external results
        
        Args:
            task_spec: Task specification/description
            internal_result: Internal reasoning result
            external_result: External reasoning result
            
        Returns:
            ArbitrationDecision
        """
        # Extract key information
        internal_confidence = internal_result.get("confidence", 0.0)
        external_confidence = external_result.get("confidence", 0.0)
        internal_answer = internal_result.get("answer", "")
        external_answer = external_result.get("answer", "")
        
        # Check for conflicts
        conflicts = self._detect_conflicts(internal_result, external_result)
        
        # Apply rule engine
        rule_decision = self.rule_engine.apply_rules(internal_result, external_result)
        
        if rule_decision:
            return rule_decision
        
        # Default confidence-based strategy
        return self._confidence_based_arbitration(
            task_spec, internal_result, external_result, conflicts
        )
    
    def _detect_conflicts(self, internal: Dict, external: Dict) -> List[Dict]:
        """Detect conflicts between internal and external results"""
        conflicts = []
        
        # Version conflict
        internal_version = internal.get("metadata", {}).get("version")
        external_version = external.get("metadata", {}).get("version")
        
        if internal_version and external_version and internal_version != external_version:
            conflicts.append({
                "type": "version_mismatch",
                "internal": internal_version,
                "external": external_version,
                "severity": "HIGH"
            })
        
        # Approach conflict
        internal_approach = internal.get("metadata", {}).get("approach")
        external_approach = external.get("metadata", {}).get("approach")
        
        if internal_approach and external_approach and internal_approach != external_approach:
            conflicts.append({
                "type": "approach_mismatch",
                "internal": internal_approach,
                "external": external_approach,
                "severity": "MEDIUM"
            })
        
        return conflicts
    
    def _confidence_based_arbitration(self, task_spec: str,
                                       internal: Dict, 
                                       external: Dict,
                                       conflicts: List[Dict]) -> ArbitrationDecision:
        """
        Default confidence-based arbitration strategy
        """
        internal_confidence = internal.get("confidence", 0.0)
        external_confidence = external.get("confidence", 0.0)
        
        # Confidence thresholds from config
        thresholds = self.arbitration_config.get("confidence_threshold", {})
        internal_threshold = thresholds.get("internal", 0.8)
        external_threshold = thresholds.get("external", 0.85)
        hybrid_threshold = thresholds.get("hybrid", 0.75)
        
        # Decision logic
        if internal_confidence >= internal_threshold and external_confidence < hybrid_threshold:
            # High internal confidence, low external -> Use internal
            decision = Decision.INTERNAL
            reason = f"Internal confidence ({internal_confidence:.2f}) exceeds threshold ({internal_threshold}), external confidence too low"
            final_answer = internal.get("answer", "")
            
        elif external_confidence >= external_threshold and internal_confidence < hybrid_threshold:
            # High external confidence, low internal -> Use external
            decision = Decision.EXTERNAL
            reason = f"External confidence ({external_confidence:.2f}) exceeds threshold ({external_threshold}), internal confidence too low"
            final_answer = external.get("answer", "")
            
        elif abs(internal_confidence - external_confidence) < 0.1:
            # Similar confidence -> Hybrid approach
            decision = Decision.HYBRID
            reason = f"Similar confidence levels (internal: {internal_confidence:.2f}, external: {external_confidence:.2f}), using hybrid approach"
            final_answer = self._merge_answers(internal, external)
            
        else:
            # Use the higher confidence
            if internal_confidence > external_confidence:
                decision = Decision.INTERNAL
                reason = f"Internal confidence ({internal_confidence:.2f}) higher than external ({external_confidence:.2f})"
                final_answer = internal.get("answer", "")
            else:
                decision = Decision.EXTERNAL
                reason = f"External confidence ({external_confidence:.2f}) higher than internal ({internal_confidence:.2f})"
                final_answer = external.get("answer", "")
        
        # Adjust for conflicts
        if conflicts:
            high_severity_conflicts = [c for c in conflicts if c.get("severity") == "HIGH"]
            if high_severity_conflicts:
                reason += f". Note: High-severity conflicts detected - {len(conflicts)} conflict(s)"
        
        return ArbitrationDecision(
            decision=decision,
            reason=reason,
            internal_confidence=internal_confidence,
            external_confidence=external_confidence,
            final_answer=final_answer,
            severity="HIGH" if conflicts else "MEDIUM"
        )
    
    def _merge_answers(self, internal: Dict, external: Dict) -> str:
        """Merge internal and external answers for hybrid decision"""
        internal_answer = internal.get("answer", "")
        external_answer = external.get("answer", "")
        
        merged = f"""# Hybrid Recommendation

## Internal Approach
{internal_answer}

## External Best Practices
{external_answer}

## Combined Recommendation
Based on both sources, consider the following:
1. Follow internal patterns for compatibility with your codebase
2. Incorporate external best practices where applicable
3. Test thoroughly in a staging environment
"""
        return merged
    
    def explain_decision(self, decision: ArbitrationDecision, 
                        task_spec: str) -> Dict:
        """
        Provide detailed explanation of arbitration decision
        
        Args:
            decision: Arbitration decision to explain
            task_spec: Original task specification
            
        Returns:
            Dictionary with detailed explanation
        """
        explanation = {
            "task_spec": task_spec,
            "decision": decision.decision.value,
            "reason": decision.reason,
            "confidence_analysis": {
                "internal": decision.internal_confidence,
                "external": decision.external_confidence,
                "delta": abs(decision.internal_confidence - decision.external_confidence),
                "winner": "internal" if decision.internal_confidence > decision.external_confidence else "external"
            },
            "rule_applied": decision.rule_used,
            "severity": decision.severity,
            "final_answer": decision.final_answer,
            "recommendations": []
        }
        
        # Add recommendations based on decision
        if decision.decision == Decision.INTERNAL:
            explanation["recommendations"].append(
                "Internal solution prioritized for codebase consistency"
            )
        elif decision.decision == Decision.EXTERNAL:
            explanation["recommendations"].append(
                "External solution adopted for best practices alignment"
            )
        elif decision.decision == Decision.HYBRID:
            explanation["recommendations"].append(
                "Hybrid approach combines internal patterns with external best practices"
            )
        
        return explanation
    
    def audit_log(self, actor: str, task_spec: str, 
                  internal_result: Dict, external_result: Dict,
                  decision: ArbitrationDecision) -> Dict:
        """Generate audit log entry"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "actor": actor,
            "action": "arbitrate",
            "resource": f"arbitration:{hashlib.md5(task_spec.encode()).hexdigest()[:16]}",
            "task_spec": task_spec,
            "internal_result": {
                "confidence": internal_result.get("confidence"),
                "answer": internal_result.get("answer", "")[:100] + "..."
            },
            "external_result": {
                "confidence": external_result.get("confidence"),
                "answer": external_result.get("answer", "")[:100] + "..."
            },
            "decision": decision.to_dict(),
            "result": {
                "success": True,
                "decision": decision.decision.value
            },
            "version": "1.0.0",
            "requestId": hashlib.md5(f"{actor}:{task_spec}".encode()).hexdigest()[:16],
            "correlationId": hashlib.md5(f"arbitrate:{task_spec}".encode()).hexdigest()[:16]
        }


if __name__ == "__main__":
    # Test arbitrator
    arbitrator = Arbitrator()
    
    # Test arbitration
    internal_result = {
        "answer": "Use asyncio.create_task() based on existing code patterns",
        "confidence": 0.92,
        "metadata": {
            "version": "3.8",
            "approach": "internal_pattern"
        }
    }
    
    external_result = {
        "answer": "Use asyncio.create_task() or asyncio.gather() for better performance",
        "confidence": 0.95,
        "metadata": {
            "version": "3.11",
            "approach": "best_practice"
        }
    }
    
    decision = arbitrator.arbitrate(
        task_spec="How to implement async task processing in Python?",
        internal_result=internal_result,
        external_result=external_result
    )
    
    print("Arbitration Decision:")
    print(json.dumps(decision.to_dict(), indent=2))
    
    # Get explanation
    explanation = arbitrator.explain_decision(decision, "Async task processing")
    print("\n\nExplanation:")
    print(json.dumps(explanation, indent=2))