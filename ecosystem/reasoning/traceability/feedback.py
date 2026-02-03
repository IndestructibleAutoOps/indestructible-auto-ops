"""
Feedback Loop System
Collects user feedback and analyzes patterns for optimization
"""
import os
import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter, defaultdict


class UserFeedback:
    """User feedback on arbitration decision"""
    
    FEEDBACK_TYPES = {
        "ACCEPT": "User accepted the suggestion",
        "REJECT": "User rejected the suggestion",
        "MODIFY": "User modified the suggestion",
        "IGNORE": "User ignored the suggestion",
        "REQUEST_CLARIFICATION": "User requested more information"
    }
    
    def __init__(self, case_id: str, feedback_type: str, 
                 reason: Optional[str] = None, user_id: Optional[str] = None,
                 modified_content: Optional[str] = None):
        self.case_id = case_id
        self.feedback_type = feedback_type
        self.reason = reason
        self.user_id = user_id
        self.modified_content = modified_content
        self.timestamp = datetime.now(timezone.utc).isoformat()
        
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "case_id": self.case_id,
            "feedback_type": self.feedback_type,
            "reason": self.reason,
            "user_id": self.user_id,
            "modified_content": self.modified_content,
            "timestamp": self.timestamp
        }


class FeedbackLoop:
    """
    Feedback collection and analysis system
    """
    
    def __init__(self, feedback_dir: str = "ecosystem/data/feedback"):
        """Initialize feedback loop system"""
        self.feedback_dir = feedback_dir
        Path(feedback_dir).mkdir(parents=True, exist_ok=True)
        
    def record_feedback(self, case_id: str, arbitration_decision: Dict,
                       feedback: UserFeedback) -> Dict:
        """
        Record user feedback on arbitration decision
        
        Args:
            case_id: Case identifier
            arbitration_decision: Original arbitration decision
            feedback: User feedback
            
        Returns:
            Audit log entry
        """
        feedback_data = {
            "case_id": case_id,
            "arbitration_decision": {
                "decision": arbitration_decision.get("decision"),
                "internal_confidence": arbitration_decision.get("internal_confidence"),
                "external_confidence": arbitration_decision.get("external_confidence"),
                "rule_used": arbitration_decision.get("rule_used")
            },
            "feedback": feedback.to_dict(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Save to file
        filename = f"feedback_{case_id}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.feedback_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, indent=2, ensure_ascii=False)
        
        return {
            "timestamp": feedback_data["timestamp"],
            "actor": feedback.user_id,
            "action": f"feedback:{feedback.feedback_type}",
            "resource": f"case:{case_id}",
            "result": {
                "success": True,
                "feedback_type": feedback.feedback_type
            }
        }
    
    def analyze_feedback_patterns(self, 
                                  time_range_days: int = 30) -> Dict:
        """
        Analyze feedback patterns over time
        
        Args:
            time_range_days: Number of days to analyze
            
        Returns:
            Analysis results
        """
        feedback_files = list(Path(self.feedback_dir).glob("feedback_*.json"))
        
        # Filter by time range
        cutoff_date = datetime.now(timezone.utc).timestamp() - (time_range_days * 86400)
        recent_feedback = []
        
        for filepath in feedback_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                timestamp = datetime.fromisoformat(data["timestamp"]).timestamp()
                if timestamp > cutoff_date:
                    recent_feedback.append(data)
        
        if not recent_feedback:
            return {
                "time_range_days": time_range_days,
                "total_feedback": 0,
                "message": "No feedback data available"
            }
        
        # Calculate metrics
        total_feedback = len(recent_feedback)
        feedback_types = Counter(f["feedback"]["feedback_type"] for f in recent_feedback)
        
        accept_count = feedback_types.get("ACCEPT", 0)
        acceptance_rate = accept_count / total_feedback if total_feedback > 0 else 0
        
        # Analyze rejection reasons
        rejection_reasons = Counter()
        rule_performance = defaultdict(lambda: {"accepted": 0, "rejected": 0})
        
        for f in recent_feedback:
            if f["feedback"]["feedback_type"] == "REJECT":
                reason = f["feedback"].get("reason", "unspecified")
                rejection_reasons[reason] += 1
            
            rule = f["arbitration_decision"].get("rule_used")
            if rule:
                if f["feedback"]["feedback_type"] == "ACCEPT":
                    rule_performance[rule]["accepted"] += 1
                elif f["feedback"]["feedback_type"] == "REJECT":
                    rule_performance[rule]["rejected"] += 1
        
        # Generate insights
        insights = []
        
        if acceptance_rate < 0.7:
            insights.append({
                "type": "WARNING",
                "message": f"Acceptance rate ({acceptance_rate:.2%}) below 70% threshold",
                "suggestion": "Review arbitration rules and confidence thresholds"
            })
        
        if rejection_reasons:
            top_reason = rejection_reasons.most_common(1)[0]
            insights.append({
                "type": "INFO",
                "message": f"Top rejection reason: '{top_reason[0]}' ({top_reason[1]} times)",
                "suggestion": "Consider adjusting rules to address this common issue"
            })
        
        return {
            "time_range_days": time_range_days,
            "total_feedback": total_feedback,
            "acceptance_rate": acceptance_rate,
            "feedback_distribution": dict(feedback_types),
            "rejection_reasons": dict(rejection_reasons),
            "rule_performance": dict(rule_performance),
            "insights": insights,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    def optimize_thresholds(self, min_samples: int = 10) -> Dict:
        """
        Analyze feedback to suggest optimal confidence thresholds
        
        Args:
            min_samples: Minimum samples required for analysis
            
        Returns:
            Threshold recommendations
        """
        feedback_files = list(Path(self.feedback_dir).glob("feedback_*.json"))
        
        # Group by internal confidence
        internal_confidence_groups = defaultdict(list)
        external_confidence_groups = defaultdict(list)
        
        for filepath in feedback_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                internal_conf = data["arbitration_decision"].get("internal_confidence", 0)
                external_conf = data["arbitration_decision"].get("external_confidence", 0)
                accepted = data["feedback"]["feedback_type"] == "ACCEPT"
                
                # Group by confidence ranges (0.1 increments)
                internal_group = int(internal_conf * 10)
                external_group = int(external_conf * 10)
                
                internal_confidence_groups[internal_group].append(accepted)
                external_confidence_groups[external_group].append(accepted)
        
        # Find optimal thresholds
        internal_threshold = self._find_optimal_threshold(
            internal_confidence_groups, min_samples
        )
        external_threshold = self._find_optimal_threshold(
            external_confidence_groups, min_samples
        )
        
        return {
            "recommendations": {
                "internal_confidence_threshold": internal_threshold,
                "external_confidence_threshold": external_threshold
            },
            "analysis": {
                "internal_groups": {k/10: sum(v)/len(v) if len(v) >= min_samples else None 
                                   for k, v in internal_confidence_groups.items()},
                "external_groups": {k/10: sum(v)/len(v) if len(v) >= min_samples else None 
                                   for k, v in external_confidence_groups.items()}
            },
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    def _find_optimal_threshold(self, confidence_groups: Dict, 
                                min_samples: int) -> float:
        """Find confidence threshold that maximizes acceptance rate"""
        best_threshold = 0.8  # Default
        best_rate = 0.0
        
        for group, outcomes in confidence_groups.items():
            if len(outcomes) >= min_samples:
                rate = sum(outcomes) / len(outcomes)
                threshold = group / 10.0
                
                if rate > best_rate:
                    best_rate = rate
                    best_threshold = threshold
        
        return best_threshold
    
    def suggest_rule_adjustments(self, 
                                 min_performance_diff: float = 0.3) -> List[Dict]:
        """
        Suggest rule adjustments based on performance
        
        Args:
            min_performance_diff: Minimum performance difference to suggest adjustment
            
        Returns:
            List of suggested adjustments
        """
        analysis = self.analyze_feedback_patterns(time_range_days=90)
        rule_performance = analysis.get("rule_performance", {})
        
        suggestions = []
        
        for rule, perf in rule_performance.items():
            total = perf["accepted"] + perf["rejected"]
            if total > 0:
                acceptance_rate = perf["accepted"] / total
                
                if acceptance_rate < (1.0 - min_performance_diff):
                    suggestions.append({
                        "rule": rule,
                        "current_performance": {
                            "acceptance_rate": acceptance_rate,
                            "accepted": perf["accepted"],
                            "rejected": perf["rejected"]
                        },
                        "suggestion": "Consider adjusting rule conditions or priority",
                        "action": "review_rule"
                    })
        
        return suggestions
    
    def export_feedback_report(self, output_path: str):
        """Export comprehensive feedback report"""
        analysis = self.analyze_feedback_patterns()
        thresholds = self.optimize_thresholds()
        adjustments = self.suggest_rule_adjustments()
        
        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "analysis": analysis,
            "threshold_recommendations": thresholds,
            "rule_adjustment_suggestions": adjustments
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Feedback report exported to {output_path}")


if __name__ == "__main__":
    # Test feedback loop
    feedback_loop = FeedbackLoop()
    
    # Record mock feedback
    feedback = UserFeedback(
        case_id="test_case_001",
        feedback_type="ACCEPT",
        reason="Helpful suggestion",
        user_id="user_123"
    )
    
    arbitration_decision = {
        "decision": "INTERNAL",
        "internal_confidence": 0.92,
        "external_confidence": 0.85,
        "rule_used": "HIGH_PRIORITY_MODULE_API"
    }
    
    audit = feedback_loop.record_feedback("test_case_001", arbitration_decision, feedback)
    print("Feedback recorded:")
    print(json.dumps(audit, indent=2))
    
    # Analyze patterns
    patterns = feedback_loop.analyze_feedback_patterns(time_range_days=30)
    print(f"\n\nFeedback Analysis:")
    print(json.dumps(patterns, indent=2))
    
    # Export report
    feedback_loop.export_feedback_report(
        "/workspace/machine-native-ops/ecosystem/reports/feedback_analysis.json"
    )