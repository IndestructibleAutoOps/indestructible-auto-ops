# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""GL Runtime V10 - 代理管理器"""
from typing import Dict, Any

class AgentManager:
    def __init__(self):
        self._agents: Dict[str, Any] = {}
    
    def register(self, agent_id: str, agent: Any) -> None:
        self._agents[agent_id] = agent
    
    def get_agent(self, agent_id: str) -> Any:
        return self._agents.get(agent_id)
