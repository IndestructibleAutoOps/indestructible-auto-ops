# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""V11 Mesh Cognition - 網格認知系統"""
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
import hashlib

@dataclass
class CognitionNode:
    id: str
    knowledge: Dict
    connections: Set[str]
    
    def __post_init__(self):
        self.connections = self.connections or set()

class CognitionMesh:
    def __init__(self):
        self.nodes: Dict[str, CognitionNode] = {}
        self.shared_memory: Dict[str, any] = {}
        self.inference_cache: Dict[str, any] = {}
    
    def add_cognition_node(self, node_id: str, knowledge: Dict) -> CognitionNode:
        node = CognitionNode(node_id, knowledge, set())
        self.nodes[node_id] = node
        return node
    
    def connect(self, node_a: str, node_b: str):
        if node_a in self.nodes and node_b in self.nodes:
            self.nodes[node_a].connections.add(node_b)
            self.nodes[node_b].connections.add(node_a)
    
    def propagate_knowledge(self, source: str, knowledge_key: str) -> Dict[str, bool]:
        if source not in self.nodes: return {}
        propagation_result = {}
        visited = set()
        queue = [source]
        while queue:
            current = queue.pop(0)
            if current in visited: continue
            visited.add(current)
            node = self.nodes[current]
            if knowledge_key in node.knowledge:
                propagation_result[current] = True
                for neighbor in node.connections:
                    if neighbor not in visited:
                        self.nodes[neighbor].knowledge[knowledge_key] = node.knowledge[knowledge_key]
                        queue.append(neighbor)
        return propagation_result
    
    def collective_inference(self, query: str) -> Dict:
        cache_key = hashlib.md5(query.encode()).hexdigest()
        if cache_key in self.inference_cache:
            return self.inference_cache[cache_key]
        
        aggregated = {}
        for node in self.nodes.values():
            for key, value in node.knowledge.items():
                if query.lower() in key.lower():
                    aggregated[f"{node.id}:{key}"] = value
        
        result = {"query": query, "matches": aggregated, "node_count": len(self.nodes)}
        self.inference_cache[cache_key] = result
        return result
