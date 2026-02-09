"""
Planning Agent
Decomposes complex tasks into executable steps
"""

import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from enum import Enum


class StepStatus(Enum):
    """Step execution status"""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class ExecutionStep:
    """Single execution step"""

    def __init__(
        self,
        step_number: int,
        action: str,
        target: str,
        purpose: str,
        dependencies: Optional[List[int]] = None,
        status: StepStatus = StepStatus.PENDING,
    ):
        self.step_number = step_number
        self.action = action
        self.target = target
        self.purpose = purpose
        self.dependencies = dependencies or []
        self.status = status
        self.result = None
        self.error = None
        self.started_at = None
        self.completed_at = None

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "step_number": self.step_number,
            "action": self.action,
            "target": self.target,
            "purpose": self.purpose,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
        }


class ExecutionPlan:
    """Complete execution plan for a task"""

    def __init__(
        self,
        task_description: str,
        steps: List[ExecutionStep],
        metadata: Optional[Dict] = None,
    ):
        self.task_description = task_description
        self.steps = steps
        self.metadata = metadata or {}
        self.created_at = datetime.now(timezone.utc)
        self.plan_id = hashlib.md5(
            f"{task_description}:{self.created_at.isoformat()}".encode()
        ).hexdigest()[:16]

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "plan_id": self.plan_id,
            "task_description": self.task_description,
            "created_at": self.created_at.isoformat(),
            "steps": [step.to_dict() for step in self.steps],
            "metadata": self.metadata,
        }

    def get_step(self, step_number: int) -> Optional[ExecutionStep]:
        """Get step by number"""
        for step in self.steps:
            if step.step_number == step_number:
                return step
        return None

    def get_ready_steps(self) -> List[ExecutionStep]:
        """Get steps that are ready to execute (dependencies met)"""
        completed_steps = {
            s.step_number for s in self.steps if s.status == StepStatus.COMPLETED
        }

        ready = []
        for step in self.steps:
            if step.status == StepStatus.PENDING:
                if all(dep in completed_steps for dep in step.dependencies):
                    ready.append(step)

        return ready


class PlanningAgent:
    """
    Planning agent for task decomposition and execution orchestration
    """

    def __init__(self):
        """Initialize planning agent"""
        self.available_actions = [
            "read_file",
            "write_file",
            "search_code",
            "analyze_patterns",
            "generate_code",
            "run_tests",
            "query_database",
            "update_docs",
            "trigger_build",
        ]

    def plan_task(
        self, task_description: str, context: Optional[Dict] = None
    ) -> ExecutionPlan:
        """
        Decompose a complex task into executable steps

        Args:
            task_description: Description of the task to complete
            context: Additional context about the task

        Returns:
            ExecutionPlan with decomposed steps
        """
        # Parse task description to understand intent
        task_type = self._classify_task(task_description)

        # Generate steps based on task type
        steps = self._generate_steps(task_type, task_description, context)

        # Create execution plan
        plan = ExecutionPlan(
            task_description=task_description,
            steps=steps,
            metadata={
                "task_type": task_type,
                "context": context,
                "estimated_duration": self._estimate_duration(steps),
            },
        )

        return plan

    def _classify_task(self, description: str) -> str:
        """Classify task type based on description"""
        description_lower = description.lower()

        if "add" in description_lower and "log" in description_lower:
            return "add_logging"
        elif "refactor" in description_lower or "restructure" in description_lower:
            return "refactor"
        elif "test" in description_lower:
            return "testing"
        elif "deploy" in description_lower:
            return "deployment"
        elif "api" in description_lower or "endpoint" in description_lower:
            return "api_development"
        elif "documentation" in description_lower or "docs" in description_lower:
            return "documentation"
        else:
            return "general"

    def _generate_steps(
        self, task_type: str, description: str, context: Optional[Dict]
    ) -> List[ExecutionStep]:
        """Generate execution steps based on task type"""

        if task_type == "add_logging":
            return [
                ExecutionStep(
                    step_number=1,
                    action="read_code",
                    target="gov-execution-runtime/src/worker.py",
                    purpose="Analyze existing code structure",
                    dependencies=[],
                ),
                ExecutionStep(
                    step_number=2,
                    action="search_patterns",
                    target="audit log implementation",
                    purpose="Find existing audit log patterns",
                    dependencies=[1],
                ),
                ExecutionStep(
                    step_number=3,
                    action="generate_code",
                    target="gov-execution-runtime/src/audit_logger.py",
                    purpose="Create audit logger module",
                    dependencies=[2],
                ),
                ExecutionStep(
                    step_number=4,
                    action="generate_code",
                    target="gov-execution-runtime/src/worker.py",
                    purpose="Integrate audit logging into worker",
                    dependencies=[3],
                ),
                ExecutionStep(
                    step_number=5,
                    action="run_tests",
                    target="gov-execution-runtime/tests/test_audit.py",
                    purpose="Verify audit logging functionality",
                    dependencies=[4],
                ),
                ExecutionStep(
                    step_number=6,
                    action="update_docs",
                    target="docs/audit_logging.md",
                    purpose="Update documentation",
                    dependencies=[5],
                ),
            ]

        elif task_type == "refactor":
            return [
                ExecutionStep(
                    step_number=1,
                    action="read_file",
                    target=".",
                    purpose="Read project structure",
                    dependencies=[],
                ),
                ExecutionStep(
                    step_number=2,
                    action="analyze_patterns",
                    target="code patterns",
                    purpose="Analyze code patterns and dependencies",
                    dependencies=[1],
                ),
                ExecutionStep(
                    step_number=3,
                    action="generate_code",
                    target=".",
                    purpose="Generate refactored code",
                    dependencies=[2],
                ),
                ExecutionStep(
                    step_number=4,
                    action="run_tests",
                    target=".",
                    purpose="Run tests to verify refactoring",
                    dependencies=[3],
                ),
            ]

        else:  # general task
            return [
                ExecutionStep(
                    step_number=1,
                    action="analyze_patterns",
                    target=".",
                    purpose="Analyze current state",
                    dependencies=[],
                ),
                ExecutionStep(
                    step_number=2,
                    action="generate_code",
                    target=".",
                    purpose="Generate solution",
                    dependencies=[1],
                ),
                ExecutionStep(
                    step_number=3,
                    action="run_tests",
                    target=".",
                    purpose="Verify solution",
                    dependencies=[2],
                ),
            ]

    def _estimate_duration(self, steps: List[ExecutionStep]) -> str:
        """Estimate total execution duration"""
        # Mock estimation
        duration_per_step = 30  # seconds
        total_seconds = len(steps) * duration_per_step

        if total_seconds < 60:
            return f"{total_seconds}s"
        elif total_seconds < 3600:
            return f"{total_seconds // 60}m"
        else:
            return f"{total_seconds // 3600}h"

    def execute_step(self, step: ExecutionStep, tools_registry: Dict) -> Dict:
        """
        Execute a single step

        Args:
            step: Execution step to execute
            tools_registry: Available tools

        Returns:
            Execution result
        """
        step.status = StepStatus.IN_PROGRESS
        step.started_at = datetime.now(timezone.utc)

        try:
            # Mock execution - in production would call actual tools
            result = {
                "success": True,
                "output": f"Executed {step.action} on {step.target}",
                "metrics": {"duration_seconds": 1.5, "memory_used_mb": 128},
            }

            step.result = result
            step.status = StepStatus.COMPLETED

        except Exception as e:
            step.status = StepStatus.FAILED
            step.error = str(e)
            result = {"success": False, "error": str(e)}

        step.completed_at = datetime.now(timezone.utc)
        return result

    def execute_plan(self, plan: ExecutionPlan, tools_registry: Dict) -> Dict:
        """
        Execute entire plan

        Args:
            plan: Execution plan
            tools_registry: Available tools

        Returns:
            Execution summary
        """
        results = {
            "plan_id": plan.plan_id,
            "task": plan.task_description,
            "total_steps": len(plan.steps),
            "completed": 0,
            "failed": 0,
            "skipped": 0,
            "start_time": datetime.now(timezone.utc).isoformat(),
            "steps": [],
        }

        while True:
            # Get ready steps
            ready_steps = plan.get_ready_steps()

            if not ready_steps:
                # Check if all steps are completed or failed
                pending = [s for s in plan.steps if s.status == StepStatus.PENDING]
                if not pending:
                    break
                else:
                    # Circular dependency or unresolved dependency
                    break

            # Execute ready steps (could be parallelized)
            for step in ready_steps:
                result = self.execute_step(step, tools_registry)
                results["steps"].append(
                    {
                        "step_number": step.step_number,
                        "action": step.action,
                        "status": step.status.value,
                        "result": result,
                    }
                )

                if step.status == StepStatus.COMPLETED:
                    results["completed"] += 1
                elif step.status == StepStatus.FAILED:
                    results["failed"] += 1

        results["end_time"] = datetime.now(timezone.utc).isoformat()
        results["success"] = results["failed"] == 0

        return results


if __name__ == "__main__":
    # Test planning agent
    agent = PlanningAgent()

    # Plan a task
    plan = agent.plan_task(
        task_description="Add audit logging to worker module",
        context={"module": "gov-execution-runtime", "log_level": "INFO"},
    )

    print("Execution Plan:")
    print(json.dumps(plan.to_dict(), indent=2))

    # Execute plan (mock)
    tools_registry = {}
    execution_results = agent.execute_plan(plan, tools_registry)

    print("\n\nExecution Results:")
    print(json.dumps(execution_results, indent=2))
