# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""GL Runtime V7 - 依賴圖"""
from typing import Dict, List, Set

class DependencyGraph:
    def __init__(self):
        self._nodes: Set[str] = set()
        self._edges: Dict[str, Set[str]] = {}
    
    def add_node(self, node: str) -> None:
        self._nodes.add(node)
        if node not in self._edges:
            self._edges[node] = set()
    
    def add_edge(self, src: str, dst: str) -> None:
        self.add_node(src)
        self.add_node(dst)
        self._edges[src].add(dst)
    
    def topological_sort(self) -> List[str]:
        visited, result = set(), []
        def dfs(node):
            if node in visited: return
            visited.add(node)
            for dep in self._edges.get(node, []):
                dfs(dep)
            result.append(node)
        for node in self._nodes:
            dfs(node)
        return result[::-1]
