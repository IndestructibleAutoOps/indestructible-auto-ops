# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""V17 Reality Bridge - 現實橋接器"""
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum

class RealityDomain(Enum):
    PHYSICAL = "physical"
    DIGITAL = "digital"
    ABSTRACT = "abstract"
    HYBRID = "hybrid"

@dataclass
class RealityAnchor:
    id: str
    domain: RealityDomain
    coordinates: Dict[str, float]
    properties: Dict[str, Any]

class RealityBridge:
    def __init__(self):
        self.anchors: Dict[str, RealityAnchor] = {}
        self.bridges: List[Dict] = []
        self.transformers: Dict[str, Callable] = {}
    
    def create_anchor(self, anchor_id: str, domain: RealityDomain, 
                      coords: Dict[str, float], props: Dict = None) -> RealityAnchor:
        anchor = RealityAnchor(anchor_id, domain, coords, props or {})
        self.anchors[anchor_id] = anchor
        return anchor
    
    def bridge_anchors(self, anchor_a: str, anchor_b: str, 
                       bidirectional: bool = True) -> Dict:
        if anchor_a not in self.anchors or anchor_b not in self.anchors:
            return {"error": "anchor_not_found"}
        bridge = {
            "from": anchor_a, "to": anchor_b,
            "domains": (self.anchors[anchor_a].domain, self.anchors[anchor_b].domain),
            "bidirectional": bidirectional
        }
        self.bridges.append(bridge)
        return bridge
    
    def register_transformer(self, from_domain: RealityDomain, 
                            to_domain: RealityDomain, fn: Callable):
        key = f"{from_domain.value}->{to_domain.value}"
        self.transformers[key] = fn
    
    def transfer(self, data: Any, from_anchor: str, to_anchor: str) -> Any:
        if from_anchor not in self.anchors or to_anchor not in self.anchors:
            return None
        from_domain = self.anchors[from_anchor].domain
        to_domain = self.anchors[to_anchor].domain
        key = f"{from_domain.value}->{to_domain.value}"
        if key in self.transformers:
            return self.transformers[key](data)
        return data  # No transformation needed
    
    def get_connected_anchors(self, anchor_id: str) -> List[str]:
        connected = []
        for bridge in self.bridges:
            if bridge["from"] == anchor_id:
                connected.append(bridge["to"])
            elif bridge["bidirectional"] and bridge["to"] == anchor_id:
                connected.append(bridge["from"])
        return connected
