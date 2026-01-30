# @GL-governed
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GL Code Intelligence & Security Layer - Adaptation Engine
Version 21.0.0

Adapts capabilities based on usage patterns and performance data.
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class AdaptationAction:
    """Represents an adaptation action"""
    action_type: str
    target_capability_id: str
    description: str
    priority: int
    parameters: Dict[str, Any]

class AdaptationEngine:
    """Adapts capabilities based on usage data"""
    
    def __init__(self, usage_tracker):
        self.usage_tracker = usage_tracker
        self.adaptation_history: List[AdaptationAction] = []
    
    def analyze_and_adapt(self) -> List[AdaptationAction]:
        """Analyze usage data and generate adaptation actions"""
        actions = []
        
        # Get all capability stats
        capability_stats = {}
        for event in self.usage_tracker.usage_events:
            if event.capability_id not in capability_stats:
                capability_stats[event.capability_id] = self.usage_tracker.get_capability_stats(
                    event.capability_id
                )
        
        # Analyze each capability
        for capability_id, stats in capability_stats.items():
            actions.extend(self._analyze_capability(capability_id, stats))
        
        self.adaptation_history.extend(actions)
        return actions
    
    def _analyze_capability(self, capability_id: str, stats: Dict[str, Any]) -> List[AdaptationAction]:
        """Analyze a single capability and generate adaptation actions"""
        actions = []
        
        # Check for performance issues
        if stats.get("avg_execution_time_ms", 0) > 2000:
            actions.append(AdaptationAction(
                action_type="optimize-performance",
                target_capability_id=capability_id,
                description=f"Optimize performance (avg: {stats['avg_execution_time_ms']:.0f}ms)",
                priority=2,
                parameters={"target_time_ms": 1000}
            ))
        
        # Check for success rate issues
        if stats.get("success_rate", 1.0) < 0.95:
            actions.append(AdaptationAction(
                action_type="improve-reliability",
                target_capability_id=capability_id,
                description=f"Improve reliability (success rate: {stats['success_rate']:.2%})",
                priority=1,
                parameters={"target_success_rate": 0.98}
            ))
        
        # Check for usage patterns
        if stats.get("total_executions", 0) > 100:
            actions.append(AdaptationAction(
                action_type="optimize-for-scale",
                target_capability_id=capability_id,
                description="Optimize for high-usage scenarios",
                priority=2,
                parameters={"usage_level": "high"}
            ))
        
        return actions
    
    def apply_adaptation(self, action: AdaptationAction) -> bool:
        """Apply an adaptation action"""
        # This would integrate with the actual capability system
        # For now, we just log the action
        print(f"Applying adaptation: {action.action_type} to {action.target_capability_id}")
        return True


if __name__ == "__main__":
    from usage_tracker import UsageTracker
    tracker = UsageTracker()
    engine = AdaptationEngine(tracker)
    actions = engine.analyze_and_adapt()
    print(f"Generated {len(actions)} adaptation actions")