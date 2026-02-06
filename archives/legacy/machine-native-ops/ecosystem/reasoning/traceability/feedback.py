"""
Feedback System
Collects and analyzes user feedback for system improvement

@GL-semantic: feedback-system
@GL-audit-trail: enabled
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass


@dataclass
class FeedbackRecord:
    """User feedback record"""
    request_id: str
    feedback_type: str  # ACCEPT, REJECT, MODIFY, IGNORE
    reason: Optional[str]
    user_id: str
    timestamp: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "request_id": self.request_id,
            "feedback_type": self.feedback_type,
            "reason": self.reason,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }


class FeedbackSystem:
    """Feedback collection and analysis system"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize feedback system
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.storage_path = None
        self._feedback = []
        self._stats = {
            "total_feedback": 0,
            "acceptance_rate": 0.0,
            "rejection_rate": 0.0,
            "feedback_types": {
                "ACCEPT": 0,
                "REJECT": 0,
                "MODIFY": 0,
                "IGNORE": 0
            }
        }
        self._initialize()
        
    def _initialize(self) -> None:
        """Initialize the feedback system"""
        workspace = Path(self.config.get("workspace", "/workspace/machine-native-ops"))
        self.storage_path = workspace / self.config.get(
            "storage_path",
            "ecosystem/reasoning/data/feedback"
        )
        
        # Create storage directory
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing feedback
        self._load_feedback()
        
    def _load_feedback(self) -> None:
        """Load existing feedback from storage"""
        feedback_file = self.storage_path / "feedback.json"
        if feedback_file.exists():
            with open(feedback_file, 'r') as f:
                feedback_data = json.load(f)
                self._feedback = [FeedbackRecord(**f) for f in feedback_data]
                self._recalculate_stats()
                
    def _save_feedback(self) -> None:
        """Save feedback to storage"""
        feedback_file = self.storage_path / "feedback.json"
        feedback_data = [f.to_dict() for f in self._feedback]
        with open(feedback_file, 'w') as f:
            json.dump(feedback_data, f, indent=2)
            
    def _recalculate_stats(self) -> None:
        """Recalculate statistics"""
        total = len(self._feedback)
        if total == 0:
            return
            
        self._stats["total_feedback"] = total
        self._stats["feedback_types"] = {
            "ACCEPT": 0,
            "REJECT": 0,
            "MODIFY": 0,
            "IGNORE": 0
        }
        
        for feedback in self._feedback:
            self._stats["feedback_types"][feedback.feedback_type] += 1
            
        accept_count = self._stats["feedback_types"]["ACCEPT"]
        reject_count = self._stats["feedback_types"]["REJECT"]
        
        self._stats["acceptance_rate"] = accept_count / total if total > 0 else 0.0
        self._stats["rejection_rate"] = reject_count / total if total > 0 else 0.0
        
    def submit_feedback(
        self,
        request_id: str,
        feedback_type: str,
        user_id: str,
        reason: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> FeedbackRecord:
        """Submit user feedback
        
        Args:
            request_id: Original request ID
            feedback_type: Feedback type (ACCEPT/REJECT/MODIFY/IGNORE)
            user_id: User ID
            reason: Feedback reason
            metadata: Additional metadata
            
        Returns:
            Feedback record
        """
        # Validate feedback type
        valid_types = ["ACCEPT", "REJECT", "MODIFY", "IGNORE"]
        if feedback_type not in valid_types:
            raise ValueError(f"Invalid feedback type. Must be one of: {valid_types}")
            
        # Create feedback record
        feedback = FeedbackRecord(
            request_id=request_id,
            feedback_type=feedback_type,
            reason=reason,
            user_id=user_id,
            timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            metadata=metadata or {}
        )
        
        # Store feedback
        self._feedback.append(feedback)
        self._recalculate_stats()
        self._save_feedback()
        
        return feedback
        
    def get_feedback(self, request_id: str) -> Optional[FeedbackRecord]:
        """Get feedback by request ID
        
        Args:
            request_id: Request ID
            
        Returns:
            Feedback record or None
        """
        for feedback in self._feedback:
            if feedback.request_id == request_id:
                return feedback
        return None
        
    def get_feedback_by_type(self, feedback_type: str) -> List[FeedbackRecord]:
        """Get all feedback of a specific type
        
        Args:
            feedback_type: Feedback type
            
        Returns:
            List of feedback records
        """
        return [f for f in self._feedback if f.feedback_type == feedback_type]
        
    def analyze_rejection_reasons(self) -> Dict[str, int]:
        """Analyze rejection reasons
        
        Returns:
            Dictionary of reason counts
        """
        rejections = self.get_feedback_by_type("REJECT")
        reasons = {}
        
        for feedback in rejections:
            if feedback.reason:
                reason = feedback.reason.strip()
                reasons[reason] = reasons.get(reason, 0) + 1
                
        return reasons
        
    def get_acceptance_rate(self, user_id: Optional[str] = None) -> float:
        """Get acceptance rate
        
        Args:
            user_id: Optional user ID filter
            
        Returns:
            Acceptance rate (0.0 to 1.0)
        """
        feedback_list = self._feedback
        if user_id:
            feedback_list = [f for f in self._feedback if f.user_id == user_id]
            
        if not feedback_list:
            return 0.0
            
        accepts = len([f for f in feedback_list if f.feedback_type == "ACCEPT"])
        return accepts / len(feedback_list)
        
    def get_stats(self) -> Dict[str, Any]:
        """Get feedback system statistics
        
        Returns:
            Dictionary of statistics
        """
        return {
            "system_type": "FeedbackSystem",
            "storage_path": str(self.storage_path),
            **self._stats
        }
        
    def generate_report(self) -> str:
        """Generate feedback analysis report
        
        Returns:
            Report string
        """
        rejection_reasons = self.analyze_rejection_reasons()
        
        report = f"""# Feedback Analysis Report

## Overview
- Total Feedback: {self._stats['total_feedback']}
- Acceptance Rate: {self._stats['acceptance_rate']:.1%}
- Rejection Rate: {self._stats['rejection_rate']:.1%}

## Feedback Distribution
- ACCEPT: {self._stats['feedback_types']['ACCEPT']}
- REJECT: {self._stats['feedback_types']['REJECT']}
- MODIFY: {self._stats['feedback_types']['MODIFY']}
- IGNORE: {self._stats['feedback_types']['IGNORE']}

## Rejection Reasons Analysis
"""
        
        for reason, count in rejection_reasons.items():
            report += f"- {reason}: {count}\n"
            
        return report
