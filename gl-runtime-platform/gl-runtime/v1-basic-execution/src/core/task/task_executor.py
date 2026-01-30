"""GL Runtime V1 - Task Executor (URSS Compliant)"""
from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import sys
sys.path.insert(0, '../../../shared')

class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"

@dataclass
class Task:
    task_id: str
    definition: Dict[str, Any]
    state: TaskState = TaskState.PENDING
    result: Optional[Any] = None

class TaskExecutor:
    """V1 Task Execution Engine"""
    
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
    
    def create_task(self, task_id: str, definition: Dict[str, Any]) -> Task:
        task = Task(task_id=task_id, definition=definition)
        self._tasks[task_id] = task
        return task
    
    def execute(self, task_id: str) -> Any:
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        task.state = TaskState.RUNNING
        try:
            # Execute task logic
            result = self._run_task(task)
            task.state = TaskState.SUCCESS
            task.result = result
            return result
        except Exception as e:
            task.state = TaskState.FAILURE
            task.result = str(e)
            raise
    
    def _run_task(self, task: Task) -> Any:
        return {"executed": task.task_id, "definition": task.definition}
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)
