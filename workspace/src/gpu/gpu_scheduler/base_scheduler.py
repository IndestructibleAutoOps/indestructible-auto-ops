"""
GL50-59: CUDA / GPU Acceleration Layer
GL51: GPU Scheduler Module - Base Scheduler
"""

import queue
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class GPUTask:
    """Represents a GPU task"""

    def __init__(self, task_config: dict[str, Any]):
        self.task_id = task_config.get('task_id', f"TASK-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        self.task_type = task_config.get('task_type', 'unknown')
        self.priority = task_config.get('priority', 1)  # 1 = lowest, 10 = highest
        self.kernel_name = task_config.get('kernel_name', '')
        self.input_data = task_config.get('input_data', {})
        self.status = 'PENDING'
        self.result = None
        self.error = None
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary"""
        return {
            'task_id': self.task_id,
            'task_type': self.task_type,
            'priority': self.priority,
            'kernel_name': self.kernel_name,
            'status': self.status,
            'result': self.result,
            'error': self.error,
            'created_at': self.created_at
        }


class BaseGPUScheduler(ABC):
    """Base class for GPU scheduler"""

    def __init__(self, scheduler_config: dict[str, Any]):
        self.scheduler_config = scheduler_config
        self.scheduler_metadata = {
            'scheduler_id': f"SCHEDULER-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'gpu_count': scheduler_config.get('gpu_count', 1),
            'created_at': datetime.now().isoformat()
        }
        self.task_queue = queue.PriorityQueue()
        self.active_tasks = {}
        self.completed_tasks = {}

    @abstractmethod
    def schedule_task(self, task: GPUTask) -> bool:
        """Schedule a task"""
        pass

    @abstractmethod
    def execute_next_task(self) -> dict[str, Any] | None:
        """Execute the next task"""
        pass

    def add_task(self, task: GPUTask) -> bool:
        """Add a task to the queue"""
        self.task_queue.put((11 - task.priority, task))  # Invert priority for queue
        return True

    def get_queue_status(self) -> dict[str, Any]:
        """Get queue status"""
        return {
            'pending_tasks': self.task_queue.qsize(),
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks)
        }


class PriorityScheduler(BaseGPUScheduler):
    """Priority-based GPU scheduler"""

    def __init__(self, scheduler_config: dict[str, Any]):
        super().__init__(scheduler_config)
        self.max_concurrent_tasks = scheduler_config.get('max_concurrent_tasks', 1)

    def schedule_task(self, task: GPUTask) -> bool:
        """Schedule a task with priority"""

        # Check if we can schedule more tasks
        if len(self.active_tasks) >= self.max_concurrent_tasks:
            return False

        self.active_tasks[task.task_id] = task
        task.status = 'SCHEDULED'

        return True

    def execute_next_task(self) -> dict[str, Any] | None:
        """Execute the next highest priority task"""

        if self.task_queue.empty():
            return None

        priority, task = self.task_queue.get()

        # Schedule the task
        if self.schedule_task(task):
            task.status = 'RUNNING'

            # Simulate task execution
            result = {
                'task_id': task.task_id,
                'status': 'SUCCESS',
                'result': f"Task {task.task_id} completed",
                'execution_time_ms': 0
            }

            task.status = 'COMPLETED'
            task.result = result
            self.completed_tasks[task.task_id] = task
            del self.active_tasks[task.task_id]

            return result

        return None


class ResourceManager:
    """Manage GPU resources"""

    def __init__(self, resource_config: dict[str, Any]):
        self.resource_config = resource_config
        self.gpu_resources = {}

        # Initialize GPU resources
        gpu_count = resource_config.get('gpu_count', 1)
        for i in range(gpu_count):
            self.gpu_resources[f"GPU-{i}"] = {
                'gpu_id': f"GPU-{i}",
                'memory_total_mb': 8192,
                'memory_used_mb': 0,
                'utilization': 0.0,
                'status': 'AVAILABLE'
            }

    def allocate_gpu(self, memory_required: int) -> str | None:
        """Allocate GPU resources"""

        for gpu_id, gpu_info in self.gpu_resources.items():
            if gpu_info['status'] == 'AVAILABLE':
                available_memory = gpu_info['memory_total_mb'] - gpu_info['memory_used_mb']

                if available_memory >= memory_required:
                    gpu_info['memory_used_mb'] += memory_required
                    gpu_info['status'] = 'IN_USE'
                    return gpu_id

        return None

    def release_gpu(self, gpu_id: str, memory_released: int) -> bool:
        """Release GPU resources"""

        if gpu_id in self.gpu_resources:
            self.gpu_resources[gpu_id]['memory_used_mb'] -= memory_released

            if self.gpu_resources[gpu_id]['memory_used_mb'] <= 0:
                self.gpu_resources[gpu_id]['status'] = 'AVAILABLE'

            return True

        return False

    def get_resource_status(self) -> dict[str, Any]:
        """Get resource status"""
        return {
            'gpu_resources': self.gpu_resources,
            'total_gpus': len(self.gpu_resources),
            'available_gpus': len([g for g in self.gpu_resources.values() if g['status'] == 'AVAILABLE']),
            'in_use_gpus': len([g for g in self.gpu_resources.values() if g['status'] == 'IN_USE'])
        }


class GPUScheduler:
    """Main GPU scheduler orchestrator"""

    def __init__(self, scheduler_config: dict[str, Any]):
        self.scheduler_config = scheduler_config
        self.scheduler = PriorityScheduler(scheduler_config)
        self.resource_manager = ResourceManager(scheduler_config)
        self.is_running = False

    def start(self) -> None:
        """Start the scheduler"""
        self.is_running = True

    def stop(self) -> None:
        """Stop the scheduler"""
        self.is_running = False

    def submit_task(self, task_config: dict[str, Any]) -> str:
        """Submit a task for execution"""

        task = GPUTask(task_config)
        self.scheduler.add_task(task)

        return task.task_id

    def process_tasks(self) -> list[dict[str, Any]]:
        """Process pending tasks"""

        results = []

        while self.scheduler.task_queue.qsize() > 0:
            result = self.scheduler.execute_next_task()
            if result:
                results.append(result)

        return results

    def get_status(self) -> dict[str, Any]:
        """Get scheduler status"""
        return {
            'scheduler_status': 'RUNNING' if self.is_running else 'STOPPED',
            'queue_status': self.scheduler.get_queue_status(),
            'resource_status': self.resource_manager.get_resource_status()
        }


# Export module info
__all__ = [
    'GPUTask',
    'BaseGPUScheduler',
    'PriorityScheduler',
    'ResourceManager',
    'GPUScheduler'
]
