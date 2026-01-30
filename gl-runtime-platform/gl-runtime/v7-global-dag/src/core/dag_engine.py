"""V7 Global DAG - 全局有向無環圖引擎"""
from typing import Dict, List, Set, Optional
from collections import defaultdict

class DAGNode:
    def __init__(self, node_id: str, data: any = None):
        self.id = node_id
        self.data = data
        self.edges: List[str] = []

class GlobalDAG:
    def __init__(self):
        self.nodes: Dict[str, DAGNode] = {}
        self.adjacency: Dict[str, List[str]] = defaultdict(list)
    
    def add_node(self, node_id: str, data: any = None) -> DAGNode:
        node = DAGNode(node_id, data)
        self.nodes[node_id] = node
        return node
    
    def add_edge(self, from_id: str, to_id: str) -> bool:
        if self._would_create_cycle(from_id, to_id):
            return False
        self.adjacency[from_id].append(to_id)
        self.nodes[from_id].edges.append(to_id)
        return True
    
    def traverse(self, start_id: str) -> List[str]:
        visited, result = set(), []
        def dfs(node_id):
            if node_id in visited: return
            visited.add(node_id)
            result.append(node_id)
            for neighbor in self.adjacency[node_id]:
                dfs(neighbor)
        dfs(start_id)
        return result
    
    def get_roots(self) -> List[str]:
        children = set(n for edges in self.adjacency.values() for n in edges)
        return [n for n in self.nodes if n not in children]
    
    def _would_create_cycle(self, from_id: str, to_id: str) -> bool:
        visited = set()
        def can_reach(current, target):
            if current == target: return True
            if current in visited: return False
            visited.add(current)
            return any(can_reach(n, target) for n in self.adjacency[current])
        return can_reach(to_id, from_id)
