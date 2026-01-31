# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: python-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

# @GL-governed
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GL Code Intelligence & Security Layer - Usage Tracker
Version 21.0.0

Tracks usage patterns of capabilities for evolution analysis.
"""

import json
import time
from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class UsageEvent:
    """Represents a single usage event"""
    capability_id: str
    capability_name: str
    timestamp: str
    execution_time_ms: float
    success: bool
    input_size: int
    output_size: int
    user_id: str
    context: Dict[str, Any]

class UsageTracker:
    """Tracks usage of capabilities for evolution analysis"""
    
    def __init__(self, storage_path: str = "./usage-data.json"):
        self.storage_path = storage_path
        self.usage_events: List[UsageEvent] = []
        self._load_usage_data()
    
    def track_usage(
        self,
        capability_id: str,
        capability_name: str,
        execution_time_ms: float,
        success: bool,
        input_size: int = 0,
        output_size: int = 0,
        user_id: str = "anonymous",
        context: Dict[str, Any] = None
    ):
        """Track a usage event"""
        event = UsageEvent(
            capability_id=capability_id,
            capability_name=capability_name,
            timestamp=datetime.now().isoformat(),
            execution_time_ms=execution_time_ms,
            success=success,
            input_size=input_size,
            output_size=output_size,
            user_id=user_id,
            context=context or {}
        )
        
        self.usage_events.append(event)
        self._save_usage_data()
    
    def get_capability_stats(self, capability_id: str) -> Dict[str, Any]:
        """Get statistics for a specific capability"""
        capability_events = [
            e for e in self.usage_events if e.capability_id == capability_id
        ]
        
        if not capability_events:
            return {}
        
        total_executions = len(capability_events)
        successful_executions = sum(1 for e in capability_events if e.success)
        avg_execution_time = sum(e.execution_time_ms for e in capability_events) / total_executions
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "success_rate": successful_executions / total_executions,
            "avg_execution_time_ms": avg_execution_time,
            "last_used": capability_events[-1].timestamp
        }
    
    def _load_usage_data(self):
        """Load usage data from storage"""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                self.usage_events = [UsageEvent(**e) for e in data]
        except FileNotFoundError:
            self.usage_events = []
    
    def _save_usage_data(self):
        """Save usage data to storage"""
        with open(self.storage_path, 'w') as f:
            json.dump([asdict(e) for e in self.usage_events], f, indent=2)


if __name__ == "__main__":
    tracker = UsageTracker()
    tracker.track_usage(
        capability_id="sql-injection-detector",
        capability_name="SQL Injection Detector",
        execution_time_ms=500,
        success=True,
        input_size=1000,
        output_size=500
    )
    print("Usage tracked successfully")