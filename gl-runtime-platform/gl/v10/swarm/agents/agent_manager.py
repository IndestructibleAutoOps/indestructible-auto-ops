"""GL Runtime V10 - 代理管理器"""
from typing import Dict, Any

class AgentManager:
    def __init__(self):
        self._agents: Dict[str, Any] = {}
    
    def register(self, agent_id: str, agent: Any) -> None:
        self._agents[agent_id] = agent
    
    def get_agent(self, agent_id: str) -> Any:
        return self._agents.get(agent_id)
