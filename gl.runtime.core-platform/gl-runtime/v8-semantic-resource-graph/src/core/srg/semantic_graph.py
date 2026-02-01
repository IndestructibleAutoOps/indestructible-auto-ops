# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""V8 SRG - 語義資源圖"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

@dataclass
class SemanticNode:
    id: str
    type: str
    properties: Dict[str, Any] = field(default_factory=dict)
    relations: List[str] = field(default_factory=list)

@dataclass  
class SemanticRelation:
    source: str
    target: str
    relation_type: str
    weight: float = 1.0

class SemanticResourceGraph:
    def __init__(self):
        self.nodes: Dict[str, SemanticNode] = {}
        self.relations: List[SemanticRelation] = []
        self.type_index: Dict[str, List[str]] = {}
    
    def add_node(self, node_id: str, node_type: str, properties: Dict = None) -> SemanticNode:
        node = SemanticNode(node_id, node_type, properties or {})
        self.nodes[node_id] = node
        self.type_index.setdefault(node_type, []).append(node_id)
        return node
    
    def add_relation(self, source: str, target: str, rel_type: str, weight: float = 1.0):
        relation = SemanticRelation(source, target, rel_type, weight)
        self.relations.append(relation)
        if source in self.nodes:
            self.nodes[source].relations.append(target)
    
    def query(self, node_type: str = None, properties: Dict = None) -> List[SemanticNode]:
        results = list(self.nodes.values())
        if node_type:
            results = [n for n in results if n.type == node_type]
        if properties:
            results = [n for n in results if all(n.properties.get(k) == v for k, v in properties.items())]
        return results
    
    def get_neighbors(self, node_id: str, rel_type: str = None) -> List[str]:
        neighbors = []
        for rel in self.relations:
            if rel.source == node_id and (rel_type is None or rel.relation_type == rel_type):
                neighbors.append(rel.target)
        return neighbors
