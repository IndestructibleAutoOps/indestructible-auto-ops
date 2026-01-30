# GL Runtime V1 - Task Executor
# @GL-governed
# @GL-layer: V01-execution
# @GL-semantic: task-execution-core

"""
GL Runtime V1: 基礎執行層
核心功能: 任務執行、狀態管理、I/O處理
治理需求: 無
邏輯依賴: 無
"""

from typing import Any, Dict, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import asyncio


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskResult:
    task_id: str
    status: TaskStatus
    output: Any = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Task:
    task_id: str
    name: str
    handler: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 0
    timeout: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


class TaskExecutor:
    """GL V1 核心任務執行器"""
    
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._results: Dict[str, TaskResult] = {}
        self._running = False
    
    def create_task(
        self,
        name: str,
        handler: Callable,
        *args,
        priority: int = 0,
        timeout: Optional[float] = None,
        **kwargs
    ) -> str:
        """創建新任務"""
        task_id = str(uuid.uuid4())
        task = Task(
            task_id=task_id,
            name=name,
            handler=handler,
            args=args,
            kwargs=kwargs,
            priority=priority,
            timeout=timeout
        )
        self._tasks[task_id] = task
        return task_id
    
    async def execute(self, task_id: str) -> TaskResult:
        """執行指定任務"""
        if task_id not in self._tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self._tasks[task_id]
        task.status = TaskStatus.RUNNING
        
        result = TaskResult(
            task_id=task_id,
            status=TaskStatus.RUNNING,
            started_at=datetime.utcnow()
        )
        
        try:
            if asyncio.iscoroutinefunction(task.handler):
                if task.timeout:
                    output = await asyncio.wait_for(
                        task.handler(*task.args, **task.kwargs),
                        timeout=task.timeout
                    )
                else:
                    output = await task.handler(*task.args, **task.kwargs)
            else:
                output = task.handler(*task.args, **task.kwargs)
            
            result.output = output
            result.status = TaskStatus.COMPLETED
            task.status = TaskStatus.COMPLETED
            
        except asyncio.TimeoutError:
            result.error = f"Task timed out after {task.timeout}s"
            result.status = TaskStatus.FAILED
            task.status = TaskStatus.FAILED
            
        except Exception as e:
            result.error = str(e)
            result.status = TaskStatus.FAILED
            task.status = TaskStatus.FAILED
        
        result.completed_at = datetime.utcnow()
        self._results[task_id] = result
        return result
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)
    
    def get_result(self, task_id: str) -> Optional[TaskResult]:
        return self._results.get(task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        if task_id in self._tasks:
            task = self._tasks[task_id]
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.CANCELLED
                return True
        return False
    
    def cleanup(self) -> None:
        """零殘留清理"""
        self._tasks.clear()
        self._results.clear()


# 全局執行器實例
_executor: Optional[TaskExecutor] = None


def get_executor() -> TaskExecutor:
    global _executor
    if _executor is None:
        _executor = TaskExecutor()
    return _executor


def cleanup_executor() -> None:
    global _executor
    if _executor:
        _executor.cleanup()
        _executor = None
