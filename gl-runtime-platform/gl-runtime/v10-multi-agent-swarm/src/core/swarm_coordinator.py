"""V10 Multi Agent Swarm - 多代理蜂群協調器"""
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
import uuid
from enum import Enum

class AgentRole(Enum):
    WORKER = "worker"
    COORDINATOR = "coordinator"
    OBSERVER = "observer"

@dataclass
class SwarmAgent:
    id: str
    role: AgentRole
    capabilities: List[str]
    state: Dict = None
    
    def __post_init__(self):
        self.state = self.state or {}

class SwarmCoordinator:
    def __init__(self):
        self.agents: Dict[str, SwarmAgent] = {}
        self.task_queue: List[Dict] = []
        self.completed_tasks: List[Dict] = []
    
    def spawn_agent(self, role: AgentRole, capabilities: List[str]) -> str:
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        self.agents[agent_id] = SwarmAgent(agent_id, role, capabilities)
        return agent_id
    
    def submit_task(self, task: Dict) -> str:
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        task["id"] = task_id
        task["status"] = "pending"
        self.task_queue.append(task)
        return task_id
    
    def allocate_tasks(self) -> Dict[str, List[str]]:
        allocation = {}
        for task in self.task_queue:
            if task["status"] != "pending": continue
            required_caps = task.get("capabilities", [])
            for agent_id, agent in self.agents.items():
                if agent.role == AgentRole.WORKER and all(c in agent.capabilities for c in required_caps):
                    allocation.setdefault(agent_id, []).append(task["id"])
                    task["status"] = "assigned"
                    task["agent"] = agent_id
                    break
        return allocation
    
    def execute_swarm(self) -> Dict:
        self.allocate_tasks()
        results = {}
        for task in self.task_queue:
            if task["status"] == "assigned":
                results[task["id"]] = {"status": "completed", "agent": task["agent"]}
                task["status"] = "completed"
                self.completed_tasks.append(task)
        return {"executed": len(results), "results": results}
