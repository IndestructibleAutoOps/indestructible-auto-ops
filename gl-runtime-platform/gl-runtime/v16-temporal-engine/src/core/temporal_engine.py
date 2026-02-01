# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: general-component
# @GL-audit-trail: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/audit-trails/GL30_49-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""V16 Temporal Engine - 時序引擎"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import time

@dataclass
class TemporalEvent:
    id: str
    timestamp: float
    data: Any
    causal_links: List[str]

class TemporalEngine:
    def __init__(self):
        self.timeline: List[TemporalEvent] = []
        self.branches: Dict[str, List[TemporalEvent]] = {"main": []}
        self.current_branch = "main"
        self.checkpoints: Dict[str, int] = {}
    
    def record_event(self, event_id: str, data: Any, causal_links: List[str] = None) -> TemporalEvent:
        event = TemporalEvent(event_id, time.time(), data, causal_links or [])
        self.timeline.append(event)
        self.branches[self.current_branch].append(event)
        return event
    
    def create_checkpoint(self, name: str):
        self.checkpoints[name] = len(self.timeline)
    
    def restore_checkpoint(self, name: str) -> bool:
        if name not in self.checkpoints: return False
        idx = self.checkpoints[name]
        self.timeline = self.timeline[:idx]
        return True
    
    def create_branch(self, name: str, from_checkpoint: str = None):
        if from_checkpoint and from_checkpoint in self.checkpoints:
            idx = self.checkpoints[from_checkpoint]
            self.branches[name] = self.timeline[:idx].copy()
        else:
            self.branches[name] = self.timeline.copy()
        self.current_branch = name
    
    def query_temporal_range(self, start: float, end: float) -> List[TemporalEvent]:
        return [e for e in self.timeline if start <= e.timestamp <= end]
    
    def get_causal_chain(self, event_id: str) -> List[TemporalEvent]:
        chain = []
        event_map = {e.id: e for e in self.timeline}
        def trace(eid):
            if eid not in event_map: return
            event = event_map[eid]
            chain.append(event)
            for link in event.causal_links:
                trace(link)
        trace(event_id)
        return chain
