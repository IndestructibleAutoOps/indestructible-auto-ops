# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""GL Runtime V1 - State Machine (URSS Compliant)"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class StateTransitionError(Exception): pass

@dataclass
class StateTransition:
    from_state: str
    to_state: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

class StateMachine:
    """V1 State Management Engine"""
    
    VALID_TRANSITIONS = {
        "pending": ["running"],
        "running": ["success", "failure", "pending"],
        "success": ["pending"],
        "failure": ["pending"]
    }
    
    def __init__(self, initial_state: str = "pending"):
        self._state = initial_state
        self._history: List[StateTransition] = []
    
    @property
    def state(self) -> str:
        return self._state
    
    def transition(self, to_state: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        if to_state not in self.VALID_TRANSITIONS.get(self._state, []):
            raise StateTransitionError(f"Invalid transition: {self._state} -> {to_state}")
        
        transition = StateTransition(
            from_state=self._state,
            to_state=to_state,
            timestamp=datetime.utcnow(),
            metadata=metadata or {}
        )
        self._history.append(transition)
        self._state = to_state
        return True
    
    def get_history(self) -> List[StateTransition]:
        return self._history.copy()
