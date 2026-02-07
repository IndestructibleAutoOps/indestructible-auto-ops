#!/usr/bin/env python3
"""
Semantic Entity Task Converter (SETC)

Transforms semantic violations into actionable implementation tasks.
Governance-driven specification to implementation conversion system.

Usage:
    python semantic_entity_task_converter.py --violation-file violations.json
    python semantic_entity_task_converter.py --from-validator output.txt
    python semantic_entity_task_converter.py --report reports/example.md
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class TaskType(Enum):
    """Types of implementation tasks"""

    CREATE_TOOL = "create_tool"
    REGISTER_TOOL = "register_tool"
    IMPLEMENT_PHASE = "implement_phase"
    CREATE_PLATFORM = "create_platform"
    COMPLETE_IMPLEMENTATION = "complete_implementation"
    DEFINE_TERMINOLOGY = "define_terminology"
    FIX_SEMANTIC_VIOLATION = "fix_semantic_violation"


class TaskState(Enum):
    """States of implementation tasks"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VERIFIED = "verified"
    INTEGRATED = "integrated"


class Priority(Enum):
    """Priority levels for tasks"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    """Implementation task data model"""

    task_id: str
    name: str
    description: str
    task_type: TaskType
    priority: Priority
    state: TaskState
    created_at: str
    created_from: str
    violation_id: Optional[str]
    estimated_effort: str
    actual_effort: Optional[str]
    assignee: Optional[str]
    completed_at: Optional[str]
    artifacts: List[str]
    dependencies: List[str]
    metadata: Dict[str, Any]


@dataclass
class Violation:
    """Semantic violation data model"""

    violation_id: str
    violation_type: str
    severity: str
    message: str
    location: str
    context: Dict[str, Any]


class SemanticEntityTaskConverter:
    """Main converter class"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._load_default_config()
        self.tasks: List[Task] = []
        self.violations: List[Violation] = []
        self.task_counter = 0  # Track task IDs

        # Ensure output directories exist
        self._ensure_directories()

    def _load_default_config(self) -> Dict:
        """Load default configuration"""
        return {
            "output_dir": ".governance/tasks",
            "template_dir": "ecosystem/governance/templates",
            "tools_dir": "ecosystem/tools",
            "artifacts_dir": "ecosystem/governance/artifacts",
            "events_dir": "ecosystem/governance/events",
            "auto_create_tasks": True,
            "auto_generate_artifacts": True,
            "track_implementation": True,
            "notify_assignees": False,
        }

    def _ensure_directories(self):
        """Ensure all required directories exist"""
        dirs = [
            self.config["output_dir"],
            self.config["tools_dir"],
            self.config["artifacts_dir"],
            self.config["events_dir"],
            Path(self.config["template_dir"]) / "tool_stubs",
            Path(self.config["template_dir"]) / "artifact_schemas",
            Path(self.config["template_dir"]) / "event_schemas",
        ]

        for d in dirs:
            Path(d).mkdir(parents=True, exist_ok=True)

    def parse_semantic_validator_output(self, file_path: str) -> List[Violation]:
        """Parse semantic validator output file"""
        violations = []
        path = Path(file_path)

        if not path.exists():
            print(f"[ERROR] File not found: {file_path}")
            return violations

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse violations from semantic validator output
        # Pattern: [SEVERITY] violation_type: message
        violation_pattern = r"\[(CRITICAL|HIGH|MEDIUM|LOW)\]\s+(\w+):\s*(.+?)(?=\n|$)"

        for i, match in enumerate(
            re.finditer(violation_pattern, content, re.MULTILINE)
        ):
            severity = match.group(1)
            violation_type = match.group(2)
            message = match.group(3).strip()

            violation = Violation(
                violation_id=f"VIOL-{datetime.now().strftime('%Y%m%d')}-{i+1:03d}",
                violation_type=violation_type,
                severity=severity,
                message=message,
                location=f"{file_path}",
                context={},
            )
            violations.append(violation)

        print(f"[INFO] Parsed {len(violations)} violations from {file_path}")
        return violations

    def convert_violations_to_tasks(self, violations: List[Violation]) -> List[Task]:
        """Convert violations to implementation tasks"""
        tasks = []

        for violation in violations:
            task = self._create_task_from_violation(violation)
            if task:
                tasks.append(task)

        print(f"[INFO] Converted {len(tasks)} violations to tasks")
        return tasks

    def _create_task_from_violation(self, violation: Violation) -> Optional[Task]:
        """Create a task from a violation"""
        task_type = self._determine_task_type(violation)
        priority = self._determine_priority(violation)

        # Extract meaningful name from violation message
        task_name = self._extract_task_name(violation)

        self.task_counter += 1
        task = Task(
            task_id=f"TASK-{datetime.now().strftime('%Y%m%d')}-{self.task_counter:03d}",
            name=task_name,
            description=violation.message,
            task_type=task_type,
            priority=priority,
            state=TaskState.PENDING,
            created_at=datetime.now().isoformat(),
            created_from="semantic_entity_task_converter",
            violation_id=violation.violation_id,
            estimated_effort=self._estimate_effort(violation, task_type),
            actual_effort=None,
            assignee=None,
            completed_at=None,
            artifacts=self._determine_artifacts(violation, task_type),
            dependencies=[],
            metadata={
                "violation_type": violation.violation_type,
                "severity": violation.severity,
                "source_location": violation.location,
            },
        )

        return task

    def _determine_task_type(self, violation: Violation) -> TaskType:
        """Determine task type from violation"""
        violation_type = violation.violation_type.lower()

        if (
            "fictional_capability" in violation_type
            or "undefined_tool" in violation_type
        ):
            return TaskType.CREATE_TOOL
        elif "missing_tool" in violation_type or "tool_references" in violation_type:
            return TaskType.REGISTER_TOOL
        elif "phase_declarations" in violation_type:
            return TaskType.IMPLEMENT_PHASE
        elif (
            "architecture_level" in violation_type
            and "platform" in violation.message.lower()
        ):
            return TaskType.CREATE_PLATFORM
        elif "incomplete" in violation_type:
            return TaskType.COMPLETE_IMPLEMENTATION
        elif "terminology" in violation_type:
            return TaskType.DEFINE_TERMINOLOGY
        else:
            return TaskType.FIX_SEMANTIC_VIOLATION

    def _determine_priority(self, violation: Violation) -> Priority:
        """Determine priority from violation severity"""
        severity_map = {
            "CRITICAL": Priority.CRITICAL,
            "HIGH": Priority.HIGH,
            "MEDIUM": Priority.MEDIUM,
            "LOW": Priority.LOW,
        }
        return severity_map.get(violation.severity, Priority.MEDIUM)

    def _extract_task_name(self, violation: Violation) -> str:
        """Extract meaningful task name from violation"""
        # Try to extract a tool/component name from the message
        message = violation.message

        # Look for patterns like "create X", "implement X", etc.
        patterns = [
            r"(?:create|implement|build|develop)\s+([\w_]+\.?py)",
            r"(?:缺少|缺失|未定義)\s*[:：]?\s*([\w_]+)",
            r"([\w_]+\.py)\s*(?:未註冊|undefined)",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return f"Create or register {match.group(1)}"

        # Default: generate a generic name
        return f"Fix {violation.violation_type}: {message[:50]}"

    def _estimate_effort(self, violation: Violation, task_type: TaskType) -> str:
        """Estimate effort based on violation and task type"""
        base_efforts = {
            TaskType.CREATE_TOOL: "4 hours",
            TaskType.REGISTER_TOOL: "1 hour",
            TaskType.IMPLEMENT_PHASE: "8 hours",
            TaskType.CREATE_PLATFORM: "16 hours",
            TaskType.COMPLETE_IMPLEMENTATION: "2 hours",
            TaskType.DEFINE_TERMINOLOGY: "2 hours",
            TaskType.FIX_SEMANTIC_VIOLATION: "4 hours",
        }

        effort = base_efforts.get(task_type, "4 hours")

        # Adjust based on severity
        if violation.severity == "CRITICAL":
            # Keep base effort for critical
            pass
        elif violation.severity == "HIGH":
            effort = effort.replace("hours", "hours")  # Keep same
        elif violation.severity in ["MEDIUM", "LOW"]:
            effort = effort.replace("hours", "hours")  # Keep same

        return effort

    def _determine_artifacts(
        self, violation: Violation, task_type: TaskType
    ) -> List[str]:
        """Determine required artifacts for the task"""
        artifacts = []

        if task_type == TaskType.CREATE_TOOL:
            tool_name = self._extract_tool_name(violation)
            artifacts = [
                f"ecosystem/tools/{tool_name}.py",
                f"ecosystem/tools/{tool_name}_test.py",
                f"ecosystem/governance/artifacts/{tool_name}_artifact_schema.yaml",
                f"ecosystem/governance/events/{tool_name}_event_schema.yaml",
                "ecosystem/governance/tools-registry.yaml (update)",
            ]
        elif task_type == TaskType.REGISTER_TOOL:
            artifacts = ["ecosystem/governance/tools-registry.yaml (update)"]
        elif task_type == TaskType.IMPLEMENT_PHASE:
            artifacts = [
                "ecosystem/phases/[phase_name]/",
                "ecosystem/governance/artifacts/phase_artifact_schema.yaml",
            ]
        elif task_type == TaskType.DEFINE_TERMINOLOGY:
            artifacts = ["ecosystem/governance/terminology.yaml (update)"]

        return artifacts

    def _extract_tool_name(self, violation: Violation) -> str:
        """Extract tool name from violation"""
        message = violation.message

        # Look for .py filenames
        match = re.search(r"([\w_]+\.py)", message)
        if match:
            return match.group(1).replace(".py", "")

        # Generate default name
        return "new_tool"

    def generate_artifacts(self, task: Task):
        """Generate implementation artifacts for a task"""
        if task.task_type == TaskType.CREATE_TOOL:
            self._generate_tool_implementation(task)
            self._generate_tool_definition(task)
            self._generate_artifact_schema(task)
            self._generate_event_schema(task)

    def _generate_tool_implementation(self, task: Task):
        """Generate tool implementation stub"""
        tool_name = self._extract_tool_name_from_task(task)
        output_file = Path(self.config["tools_dir"]) / f"{tool_name}.py"

        stub_content = f'''"""
{tool_name.replace('_', ' ').title()} Tool

Auto-generated from semantic violation: {task.violation_id}
Task: {task.task_id}
Generated: {task.created_at}

Description: {task.description}
Estimated Effort: {task.estimated_effort}
"""

from pathlib import Path
from typing import Dict, Any, Optional


class {self._to_class_name(tool_name)}:
    """{tool_name.replace('_', ' ').title()} implementation"""
    
    def __init__(self):
        self.name = "{tool_name}"
        self.version = "1.0.0"
        self.category = "governance"
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool
        
        Args:
            input_data: Tool input data
            
        Returns:
            Tool output data
        """
        # TODO: Implement this method
        raise NotImplementedError("Method execute() not yet implemented")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input data
        
        Args:
            input_data: Input data to validate
            
        Returns:
            True if valid, False otherwise
        """
        # TODO: Implement validation logic
        return True
    
    def generate_evidence(self, operation: str, input_data: Any, output_data: Any) -> Dict[str, Any]:
        """
        Generate evidence for governance tracking
        
        Args:
            operation: Operation performed
            input_data: Input data
            output_data: Output data
            
        Returns:
            Evidence data
        """
        # TODO: Implement evidence generation
        return {{
            "tool": self.name,
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }}


if __name__ == "__main__":
    tool = {self._to_class_name(tool_name)}()
    print(f"Tool: {{tool.name}} v{{tool.version}}")
    print(f"Category: {{tool.category}}")
'''

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(stub_content)

        print(f"[INFO] Generated tool stub: {output_file}")

    def _generate_tool_definition(self, task: Task):
        """Generate tool definition JSON"""
        tool_name = self._extract_tool_name_from_task(task)
        output_file = (
            Path(self.config["artifacts_dir"]) / f"{tool_name}_definition.json"
        )

        definition = {
            "name": tool_name,
            "category": "governance",
            "era": "1",
            "purpose": task.description,
            "input_schema": "input_data",
            "output_schema": "output_data",
            "evidence_generation": "true",
            "immutable": "false",
            "description": f"Auto-generated from task {task.task_id}",
            "file_path": f"ecosystem/tools/{tool_name}.py",
            "status": "pending",
            "task_id": task.task_id,
            "created_at": task.created_at,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(definition, f, indent=2)

        print(f"[INFO] Generated tool definition: {output_file}")

    def _generate_artifact_schema(self, task: Task):
        """Generate artifact schema YAML"""
        tool_name = self._extract_tool_name_from_task(task)
        output_file = (
            Path(self.config["artifacts_dir"]) / f"{tool_name}_artifact_schema.yaml"
        )

        schema = f"""# Artifact Schema for {tool_name}
# Auto-generated from task {task.task_id}

name: "{tool_name}_artifact"
version: "1.0.0"
schema_type: "artifact"
created_from: "{task.task_id}"

fields:
  - name: "artifact_id"
    type: "string"
    required: true
    description: "Unique artifact identifier"
  
  - name: "tool_name"
    type: "string"
    required: true
    description: "Name of the tool that generated this artifact"
  
  - name: "timestamp"
    type: "datetime"
    required: true
    description: "When the artifact was created"
  
  - name: "operation"
    type: "string"
    required: true
    description: "Operation performed"
  
  - name: "input_hash"
    type: "string"
    required: false
    description: "SHA256 hash of input data"
  
  - name: "output_hash"
    type: "string"
    required: false
    description: "SHA256 hash of output data"
  
  - name: "status"
    type: "string"
    required: true
    enum: ["success", "failure", "partial"]
    description: "Artifact status"
  
  - name: "metadata"
    type: "object"
    required: false
    description: "Additional metadata"
"""

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(schema)

        print(f"[INFO] Generated artifact schema: {output_file}")

    def _generate_event_schema(self, task: Task):
        """Generate event schema YAML"""
        tool_name = self._extract_tool_name_from_task(task)
        output_file = Path(self.config["events_dir"]) / f"{tool_name}_event_schema.yaml"

        schema = f"""# Event Schema for {tool_name}
# Auto-generated from task {task.task_id}

name: "{tool_name}_event"
version: "1.0.0"
schema_type: "event"
created_from: "{task.task_id}"

fields:
  - name: "event_id"
    type: "string"
    required: true
    description: "Unique event identifier (UUID)"
  
  - name: "event_type"
    type: "string"
    required: true
    description: "Type of event (e.g., TOOL_EXECUTED, TASK_COMPLETED)"
  
  - name: "timestamp"
    type: "datetime"
    required: true
    description: "When the event occurred"
  
  - name: "tool_name"
    type: "string"
    required: true
    description: "Name of the tool"
  
  - name: "task_id"
    type: "string"
    required: false
    description: "Associated task ID"
  
  - name: "status"
    type: "string"
    required: true
    enum: ["started", "completed", "failed", "cancelled"]
    description: "Event status"
  
  - name: "duration_ms"
    type: "integer"
    required: false
    description: "Duration in milliseconds"
  
  - name: "error"
    type: "string"
    required: false
    description: "Error message if failed"
  
  - name: "metadata"
    type: "object"
    required: false
    description: "Additional event metadata"
"""

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(schema)

        print(f"[INFO] Generated event schema: {output_file}")

    def _extract_tool_name_from_task(self, task: Task) -> str:
        """Extract tool name from task"""
        # Try to find .py in artifacts
        for artifact in task.artifacts:
            if artifact.endswith(".py") and not artifact.endswith("_test.py"):
                return Path(artifact).stem

        # Fallback
        return "new_tool"

    def _to_class_name(self, name: str) -> str:
        """Convert snake_case to CamelCase"""
        return "".join(word.capitalize() for word in name.split("_"))

    def save_tasks(self, tasks: List[Task]):
        """Save tasks to task database"""
        tasks_dir = Path(self.config["output_dir"])

        for task in tasks:
            task_file = tasks_dir / f"{task.task_id}.json"

            task_dict = asdict(task)
            task_dict["task_type"] = task.task_type.value
            task_dict["priority"] = task.priority.value
            task_dict["state"] = task.state.value

            with open(task_file, "w", encoding="utf-8") as f:
                json.dump(task_dict, f, indent=2)

            print(f"[INFO] Saved task: {task_file}")

    def generate_report(self, tasks: List[Task]) -> str:
        """Generate implementation report"""
        total_tasks = len(tasks)
        completed = sum(1 for t in tasks if t.state == TaskState.COMPLETED)
        pending = sum(1 for t in tasks if t.state == TaskState.PENDING)
        in_progress = sum(1 for t in tasks if t.state == TaskState.IN_PROGRESS)

        report = f"""
================================================================================
Semantic Entity Task Converter - Implementation Report
================================================================================

Generated: {datetime.now().isoformat()}

================================================================================
📊 Summary
================================================================================

Total Tasks Generated: {total_tasks}
  - Completed: {completed}
  - In Progress: {in_progress}
  - Pending: {pending}

Task Types:
"""

        # Count by type
        type_counts = {}
        for task in tasks:
            ttype = task.task_type.value
            type_counts[ttype] = type_counts.get(ttype, 0) + 1

        for ttype, count in sorted(type_counts.items()):
            report += f"  - {ttype}: {count}\n"

        report += f"""
Priority Distribution:
"""

        # Count by priority
        priority_counts = {}
        for task in tasks:
            prio = task.priority.value
            priority_counts[prio] = priority_counts.get(prio, 0) + 1

        for prio, count in sorted(priority_counts.items()):
            report += f"  - {prio}: {count}\n"

        report += f"""
================================================================================
📋 Task List
================================================================================

"""

        for i, task in enumerate(tasks, 1):
            report += f"{i}. [{task.priority.value}] {task.task_id}: {task.name}\n"
            report += f"   State: {task.state.value}\n"
            report += f"   Type: {task.task_type.value}\n"
            report += f"   Estimated: {task.estimated_effort}\n"
            report += f"   Artifacts: {len(task.artifacts)}\n"
            report += "\n"

        report += f"""
================================================================================
Next Steps
================================================================================

1. Review generated tasks in {self.config['output_dir']}/
2. Prioritize tasks based on priority and dependencies
3. Implement tools following generated stubs
4. Update tool registry upon completion
5. Verify implementations against original semantic requirements

================================================================================
End of Report
================================================================================
"""

        return report


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Semantic Entity Task Converter - Convert semantic violations to implementation tasks"
    )

    parser.add_argument(
        "--violation-file", type=str, help="Path to violations JSON file"
    )

    parser.add_argument(
        "--from-validator",
        type=str,
        help="Parse violations from semantic validator output file",
    )

    parser.add_argument(
        "--report",
        type=str,
        help="Generate tasks from semantic violations in a report file",
    )

    parser.add_argument(
        "--workspace", type=str, default="/workspace", help="Workspace directory"
    )

    parser.add_argument(
        "--generate-artifacts",
        action="store_true",
        help="Generate implementation artifacts (stubs, schemas)",
    )

    parser.add_argument(
        "--report-file", type=str, default=None, help="Output report file path"
    )

    args = parser.parse_args()

    # Initialize converter
    converter = SemanticEntityTaskConverter()

    violations = []

    # Load violations from different sources
    if args.violation_file:
        # Load from JSON file
        with open(args.violation_file, "r") as f:
            violations_data = json.load(f)
            for v_data in violations_data:
                violations.append(Violation(**v_data))

    elif args.from_validator:
        # Parse from semantic validator output
        violations = converter.parse_semantic_validator_output(args.from_validator)

    elif args.report:
        # Parse violations from report file
        violations = converter.parse_semantic_validator_output(args.report)

    else:
        print(
            "[ERROR] Please specify a violation source with --violation-file, --from-validator, or --report"
        )
        sys.exit(1)

    if not violations:
        print("[WARNING] No violations found. No tasks to generate.")
        return

    # Convert violations to tasks
    tasks = converter.convert_violations_to_tasks(violations)

    if not tasks:
        print("[WARNING] No tasks generated from violations.")
        return

    # Generate artifacts if requested
    if args.generate_artifacts:
        for task in tasks:
            converter.generate_artifacts(task)

    # Save tasks
    converter.save_tasks(tasks)

    # Generate report
    report = converter.generate_report(tasks)

    if args.report_file:
        with open(args.report_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[INFO] Report saved to: {args.report_file}")
    else:
        print(report)

    print(f"\n[SUCCESS] Generated {len(tasks)} tasks from {len(violations)} violations")


if __name__ == "__main__":
    main()
