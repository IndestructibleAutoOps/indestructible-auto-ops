"""V25 Ecosystem Integration - 生態系統整合器"""
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import time

@dataclass
class EcosystemNode:
    id: str
    type: str
    version: str
    capabilities: List[str]
    dependencies: List[str]
    state: Dict[str, Any] = field(default_factory=dict)

@dataclass
class IntegrationLink:
    source: str
    target: str
    protocol: str
    bandwidth: float
    latency: float

class EcosystemIntegrator:
    def __init__(self):
        self.nodes: Dict[str, EcosystemNode] = {}
        self.links: List[IntegrationLink] = []
        self.protocols: Dict[str, Callable] = {}
        self.health_status: Dict[str, str] = {}
    
    def register_node(self, node_id: str, node_type: str, version: str,
                     capabilities: List[str], dependencies: List[str] = None) -> EcosystemNode:
        node = EcosystemNode(node_id, node_type, version, capabilities, dependencies or [])
        self.nodes[node_id] = node
        self.health_status[node_id] = "healthy"
        return node
    
    def create_link(self, source: str, target: str, protocol: str,
                   bandwidth: float = 1.0, latency: float = 0.0) -> Optional[IntegrationLink]:
        if source not in self.nodes or target not in self.nodes:
            return None
        link = IntegrationLink(source, target, protocol, bandwidth, latency)
        self.links.append(link)
        return link
    
    def register_protocol(self, name: str, handler: Callable):
        self.protocols[name] = handler
    
    def integrate(self, source: str, target: str, data: Any) -> Dict:
        link = next((l for l in self.links if l.source == source and l.target == target), None)
        if not link:
            return {"error": "no_link"}
        
        if link.protocol in self.protocols:
            result = self.protocols[link.protocol](data)
            return {"status": "success", "result": result, "latency": link.latency}
        return {"status": "success", "data": data, "latency": link.latency}
    
    def check_dependencies(self, node_id: str) -> Dict[str, bool]:
        if node_id not in self.nodes:
            return {}
        node = self.nodes[node_id]
        return {dep: dep in self.nodes and self.health_status.get(dep) == "healthy" 
                for dep in node.dependencies}
    
    def get_ecosystem_topology(self) -> Dict:
        return {
            "nodes": [{"id": n.id, "type": n.type, "version": n.version} 
                     for n in self.nodes.values()],
            "links": [{"source": l.source, "target": l.target, "protocol": l.protocol}
                     for l in self.links],
            "health": self.health_status
        }
    
    def broadcast(self, data: Any, capability_filter: str = None) -> Dict[str, Any]:
        results = {}
        for node in self.nodes.values():
            if capability_filter and capability_filter not in node.capabilities:
                continue
            results[node.id] = {"received": True, "timestamp": time.time()}
        return results
