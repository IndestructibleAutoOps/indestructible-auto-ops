"""GL Runtime V11 - 網格認知節點"""
from typing import Dict, Any

class MeshNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self._neighbors: Dict[str, 'MeshNode'] = {}
    
    def connect(self, node: 'MeshNode') -> None:
        self._neighbors[node.node_id] = node
    
    def broadcast(self, message: Any) -> None:
        for neighbor in self._neighbors.values():
            neighbor.receive(message)
    
    def receive(self, message: Any) -> None:
        pass
