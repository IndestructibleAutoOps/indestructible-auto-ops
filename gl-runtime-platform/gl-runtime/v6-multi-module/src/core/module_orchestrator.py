# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""V6 Multi Module - 多模組協調器"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import uuid

@dataclass
class Module:
    id: str
    name: str
    dependencies: List[str]
    status: str = "idle"

class ModuleOrchestrator:
    def __init__(self):
        self.modules: Dict[str, Module] = {}
        self.execution_graph = {}
    
    def register_module(self, name: str, dependencies: List[str] = None) -> str:
        module_id = str(uuid.uuid4())[:8]
        self.modules[module_id] = Module(module_id, name, dependencies or [])
        return module_id
    
    def execute_pipeline(self, module_ids: List[str]) -> Dict:
        execution_order = self._topological_sort(module_ids)
        results = {}
        for mid in execution_order:
            results[mid] = self._execute_module(mid)
        return {"order": execution_order, "results": results}
    
    def _topological_sort(self, module_ids: List[str]) -> List[str]:
        visited, order = set(), []
        def dfs(mid):
            if mid in visited: return
            visited.add(mid)
            for dep in self.modules.get(mid, Module("", "", [])).dependencies:
                if dep in self.modules: dfs(dep)
            order.append(mid)
        for mid in module_ids: dfs(mid)
        return order
    
    def _execute_module(self, module_id: str) -> Dict:
        module = self.modules.get(module_id)
        if module:
            module.status = "completed"
            return {"module": module.name, "status": "success"}
        return {"error": "module_not_found"}
