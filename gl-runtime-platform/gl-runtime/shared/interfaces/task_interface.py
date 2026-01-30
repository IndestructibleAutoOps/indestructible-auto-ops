"""GL Runtime Shared - Task Interface"""
from abc import ABC, abstractmethod
from typing import Any, Dict

class ITask(ABC):
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any: pass
    
    @abstractmethod
    def get_state(self) -> str: pass
    
    @abstractmethod
    def set_state(self, state: str) -> None: pass

class ITaskExecutor(ABC):
    @abstractmethod
    def run(self, task: ITask) -> Any: pass
