"""
Arbitration Engine
Makes decisions between internal and external retrieval results

@GL-semantic: arbitration-engine
@GL-audit-trail: enabled
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ..base_retrieval import RetrievalResult, RetrievalContext


@dataclass
class ArbitrationDecision:
    """Result from arbitration process"""
    decision: str  # INTERNAL, EXTERNAL, HYBRID, REJECT
    confidence: float  # 0.0 to 1.0
    reasoning: str
    evidence_links: List[str]
    risk_assessment: str
    chosen_results: List[RetrievalResult]
    timestamp: str
    rule_applied: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "decision": self.decision,
            "confidence": f"{self.confidence:.3f}",
            "reasoning": self.reasoning,
            "evidence_links": self.evidence_links,
            "risk_assessment": self.risk_assessment,
            "chosen_results": [r.to_dict() for r in self.chosen_results],
            "timestamp": self.timestamp,
            "rule_applied": self.rule_applied
        }


class Arbitrator:
    """Arbitration engine for dual-path decision making"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize arbitrator
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.rules = self._load_default_rules()
        self._stats = {
            "total_arbitrations": 0,
            "decisions": {
                "INTERNAL": 0,
                "EXTERNAL": 0,
                "HYBRID": 0,
                "REJECT": 0
            },
            "rules_applied": {}
        }
        self._initialize()
        
    def _initialize(self) -> None:
        """Initialize the arbitrator"""
        # Initialization complete
        pass
        
    def _load_default_rules(self) -> Dict:
        """Load default arbitration rules
        
        Returns:
            Dictionary of rules
        """
        return {
            "SEC001": {
                "rule_id": "SEC001",
                "name": "SECURITY_VULNERABILITY_FIX",
                "priority": "CRITICAL",
                "decision": "EXTERNAL",
                "confidence_threshold": 0.75,
                "description": "For security vulnerability fixes, always prefer external sources",
                "conditions": [
                    {"field": "category", "operator": "equals", "value": "security"},
                    {"field": "task_type", "operator": "equals", "value": "vulnerability_fix"}
                ],
                "reasoning": "External security sources provide the most up-to-date security patches",
                "@evidence": ["external: security-advisory-db#L1-L50"]
            },
            "SEC002": {
                "rule_id": "SEC002",
                "name": "HIGH_PRIORITY_MODULE_API",
                "priority": "HIGH",
                "decision": "INTERNAL",
                "confidence_threshold": 0.8,
                "description": "For core GL platform modules, prefer internal sources",
                "conditions": [
                    {"field": "module", "operator": "in", "values": ["gl-platform-services", "gl-execution-runtime", "gl-meta-specifications"]},
                    {"field": "internal_confidence", "operator": "greater_than", "value": 0.8}
                ],
                "reasoning": "Core GL modules have well-documented internal APIs",
                "@evidence": ["internal: gl-platform-services/api#L1-L100"]
            },
            "DEP001": {
                "rule_id": "DEP001",
                "name": "DEPENDENCY_VERSION_UPDATE",
                "priority": "MEDIUM",
                "decision": "HYBRID",
                "confidence_threshold": 0.7,
                "description": "For dependency version updates, use hybrid approach",
                "conditions": [
                    {"field": "task_type", "operator": "equals", "value": "dependency_update"}
                ],
                "reasoning": "Dependency updates need both internal compatibility and external version info",
                "@evidence": ["internal: version-checker#L1-L50", "external: pypi.org/package#L1-L100"]
            }
        }
        
    def arbitrate(
        self,
        context: RetrievalContext,
        internal_results: List[RetrievalResult],
        external_results: List[RetrievalResult]
    ) -> ArbitrationDecision:
        """Make arbitration decision
        
        Args:
            context: Retrieval context
            internal_results: Internal retrieval results
            external_results: External retrieval results
            
        Returns:
            Arbitration decision
        """
        self._stats["total_arbitrations"] += 1
        
        # Step 1: Apply rule engine (highest priority)
        rule_decision = self._apply_rule_engine(context, internal_results, external_results)
        if rule_decision:
            self._stats["decisions"][rule_decision.decision] += 1
            if rule_decision.rule_applied:
                self._stats["rules_applied"][rule_decision.rule_applied] = (
                    self._stats["rules_applied"].get(rule_decision.rule_applied, 0) + 1
                )
            return rule_decision
            
        # Step 2: Use confidence-based strategy (fallback)
        confidence_decision = self._apply_confidence_strategy(
            context, internal_results, external_results
        )
        self._stats["decisions"][confidence_decision.decision] += 1
        return confidence_decision
        
    def _apply_rule_engine(
        self,
        context: RetrievalContext,
        internal_results: List[RetrievalResult],
        external_results: List[RetrievalResult]
    ) -> Optional[ArbitrationDecision]:
        """Apply rule engine for arbitration
        
        Args:
            context: Retrieval context
            internal_results: Internal retrieval results
            external_results: External retrieval results
            
        Returns:
            Arbitration decision or None if no rule matches
        """
        # Calculate average confidences
        avg_internal_conf = (
            sum(r.confidence for r in internal_results) / len(internal_results)
            if internal_results else 0.0
        )
        avg_external_conf = (
            sum(r.confidence for r in external_results) / len(external_results)
            if external_results else 0.0
        )
        
        # Check each rule
        for rule_id, rule in self.rules.items():
            if self._matches_rule(rule, context, avg_internal_conf):
                decision_type = rule["decision"]
                
                # Check confidence threshold
                threshold = rule.get("confidence_threshold", 0.7)
                if decision_type == "INTERNAL" and avg_internal_conf < threshold:
                    continue
                if decision_type == "EXTERNAL" and avg_external_conf < threshold:
                    continue
                if decision_type == "HYBRID" and max(avg_internal_conf, avg_external_conf) < threshold:
                    continue
                    
                # Apply decision
                chosen_results = self._select_results_by_decision(
                    decision_type, internal_results, external_results
                )
                
                return ArbitrationDecision(
                    decision=decision_type,
                    confidence=max(avg_internal_conf, avg_external_conf),
                    reasoning=rule["reasoning"],
                    evidence_links=rule.get("@evidence", []),
                    risk_assessment=self._assess_risk(decision_type, avg_internal_conf, avg_external_conf),
                    chosen_results=chosen_results,
                    timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    rule_applied=rule_id
                )
                
        return None
        
    def _matches_rule(
        self,
        rule: Dict,
        context: RetrievalContext,
        internal_confidence: float
    ) -> bool:
        """Check if rule matches the context
        
        Args:
            rule: Rule definition
            context: Retrieval context
            internal_confidence: Average internal confidence
            
        Returns:
            True if rule matches
        """
        for condition in rule.get("conditions", []):
            field = condition["field"]
            operator = condition["operator"]
            value = condition.get("value")
            values = condition.get("values")
            
            # Get field value from context
            field_value = getattr(context, field, None)
            if field_value is None and field == "internal_confidence":
                field_value = internal_confidence
                
            # Apply operator
            if operator == "equals":
                if str(field_value) != str(value):
                    return False
            elif operator == "in":
                if field_value not in values:
                    return False
            elif operator == "starts_with":
                if not str(field_value).startswith(value):
                    return False
            elif operator == "greater_than":
                if float(field_value) <= float(value):
                    return False
                    
        return True
        
    def _apply_confidence_strategy(
        self,
        context: RetrievalContext,
        internal_results: List[RetrievalResult],
        external_results: List[RetrievalResult]
    ) -> ArbitrationDecision:
        """Apply confidence-based arbitration strategy
        
        Args:
            context: Retrieval context
            internal_results: Internal retrieval results
            external_results: External retrieval results
            
        Returns:
            Arbitration decision
        """
        # Get thresholds from config
        internal_threshold = self.config.get("confidence_threshold", {}).get("internal", 0.8)
        external_threshold = self.config.get("confidence_threshold", {}).get("external", 0.85)
        hybrid_threshold = self.config.get("confidence_threshold", {}).get("hybrid", 0.75)
        reject_threshold = self.config.get("confidence_threshold", {}).get("reject", 0.6)
        
        # Calculate average confidences
        avg_internal_conf = (
            sum(r.confidence for r in internal_results) / len(internal_results)
            if internal_results else 0.0
        )
        avg_external_conf = (
            sum(r.confidence for r in external_results) / len(external_results)
            if external_results else 0.0
        )
        
        # Decision logic
        if max(avg_internal_conf, avg_external_conf) < reject_threshold:
            # Reject if both are below threshold
            decision = "REJECT"
            chosen_results = []
            reasoning = f"Both internal ({avg_internal_conf:.2f}) and external ({avg_external_conf:.2f}) confidence below reject threshold ({reject_threshold})"
            
        elif avg_external_conf >= external_threshold:
            # Use external if high confidence
            decision = "EXTERNAL"
            chosen_results = external_results
            reasoning = f"External confidence ({avg_external_conf:.2f}) above threshold ({external_threshold})"
            
        elif avg_internal_conf >= internal_threshold:
            # Use internal if high confidence
            decision = "INTERNAL"
            chosen_results = internal_results
            reasoning = f"Internal confidence ({avg_internal_conf:.2f}) above threshold ({internal_threshold})"
            
        elif abs(avg_internal_conf - avg_external_conf) < 0.1:
            # Use hybrid if confidences are similar
            decision = "HYBRID"
            chosen_results = internal_results + external_results
            chosen_results.sort(key=lambda x: x.confidence, reverse=True)
            reasoning = f"Internal ({avg_internal_conf:.2f}) and external ({avg_external_conf:.2f}) confidence similar (< 0.1 diff)"
            
        else:
            # Choose the higher confidence
            decision = "INTERNAL" if avg_internal_conf > avg_external_conf else "EXTERNAL"
            chosen_results = internal_results if decision == "INTERNAL" else external_results
            reasoning = f"{decision} has higher confidence ({max(avg_internal_conf, avg_external_conf):.2f})"
            
        return ArbitrationDecision(
            decision=decision,
            confidence=max(avg_internal_conf, avg_external_conf),
            reasoning=reasoning,
            evidence_links=[
                f"internal_conf: {avg_internal_conf:.3f}",
                f"external_conf: {avg_external_conf:.3f}"
            ],
            risk_assessment=self._assess_risk(decision, avg_internal_conf, avg_external_conf),
            chosen_results=chosen_results,
            timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        
    def _select_results_by_decision(
        self,
        decision: str,
        internal_results: List[RetrievalResult],
        external_results: List[RetrievalResult]
    ) -> List[RetrievalResult]:
        """Select results based on decision type
        
        Args:
            decision: Decision type
            internal_results: Internal retrieval results
            external_results: External retrieval results
            
        Returns:
            Selected results
        """
        if decision == "INTERNAL":
            return internal_results
        elif decision == "EXTERNAL":
            return external_results
        elif decision == "HYBRID":
            # Merge and sort by confidence
            merged = internal_results + external_results
            merged.sort(key=lambda x: x.confidence, reverse=True)
            return merged
        elif decision == "REJECT":
            return []
        return []
        
    def _assess_risk(
        self,
        decision: str,
        internal_conf: float,
        external_conf: float
    ) -> str:
        """Assess risk level of decision
        
        Args:
            decision: Decision type
            internal_conf: Internal confidence
            external_conf: External confidence
            
        Returns:
            Risk assessment string
        """
        max_conf = max(internal_conf, external_conf)
        
        if max_conf >= 0.9:
            return "LOW - High confidence result"
        elif max_conf >= 0.8:
            return "LOW - Good confidence result"
        elif max_conf >= 0.7:
            return "MEDIUM - Moderate confidence, consider review"
        elif max_conf >= 0.6:
            return "MEDIUM - Low confidence, manual review recommended"
        else:
            return "HIGH - Very low confidence, human intervention required"
            
    def get_stats(self) -> Dict[str, Any]:
        """Get arbitrator statistics
        
        Returns:
            Dictionary of statistics
        """
        total = self._stats["total_arbitrations"]
        return {
            "arbitrator_type": "Arbitrator",
            "total_arbitrations": total,
            "decision_distribution": {
                k: f"{v / total * 100:.1f}%" if total > 0 else "0%"
                for k, v in self._stats["decisions"].items()
            },
            "rules_applied": self._stats["rules_applied"],
            "rules_loaded": len(self.rules)
        }
