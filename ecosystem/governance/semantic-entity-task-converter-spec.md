# Semantic Entity Task Converter Specification

## Overview

The Semantic Entity Task Converter (SETC) transforms semantic violations into actionable implementation tasks. Instead of deleting or ignoring semantic violations, it converts them into concrete development work.

## Core Principles

1. **Semantics → Implementation**: Preserve semantic meaning by creating real implementation
2. **Governance-Driven Specs**: Reports become executable specifications
3. **Automatic Generation**: Convert violations to tasks with minimal manual intervention
4. **Traceability**: Maintain links between violations and resulting implementations

## Conversion Process

### Step 1: Violation Detection
```yaml
violation_type: "fictional_capability"
violation_message: "報告治理系統已整合"
severity: "CRITICAL"
location: "reports/example.md:42"
```

### Step 2: Task Generation
```yaml
task_id: "TASK-001"
task_type: "tool_implementation"
task_name: "Create reporting_integrator.py"
priority: "CRITICAL"
estimated_effort: "4 hours"
dependencies: []
```

### Step 3: Artifact Generation
```yaml
artifacts:
  - tool_definition.json
  - implementation_stub.py
  - artifact_schema.yaml
  - event_schema.yaml
```

## Violation Type → Task Mapping

| Violation Type | Task Type | Output |
|----------------|-----------|--------|
| `fictional_capability` | Create Tool | `tools/[name].py` |
| `fictional_phase` | Implement Phase | `phases/[name]/` |
| `fictional_platform` | Create Platform Component | `platforms/[name]/` |
| `missing_tool` | Register/Implement Tool | Update registry + create tool |
| `incomplete_implementation` | Complete Implementation | Add missing methods |
| `undefined_terminology` | Define Terminology | Update glossary |

## Generated Artifacts

### 1. Tool Definition (tool-definition.json)
```json
{
  "name": "reporting_integrator",
  "category": "governance",
  "era": "1",
  "purpose": "Integrate reporting with governance system",
  "input_schema": "report_data",
  "output_schema": "governance_report",
  "evidence_generation": "true"
}
```

### 2. Implementation Stub (implementation_stub.py)
```python
"""
[TOOL_NAME] Implementation Stub

Auto-generated from semantic violation at [LOCATION]
Task: [TASK_ID]
Generated: [TIMESTAMP]
"""

class [ToolName]:
    def __init__(self):
        pass
    
    def execute(self, input_data):
        # TODO: Implement this method
        raise NotImplementedError
```

### 3. Artifact Schema (artifact_schema.yaml)
```yaml
name: "[ARTIFACT_NAME]"
version: "1.0.0"
schema_type: "artifact"
fields:
  - name: "task_id"
    type: "string"
  - name: "timestamp"
    type: "datetime"
  - name: "result"
    type: "object"
```

### 4. Event Schema (event_schema.yaml)
```yaml
name: "[EVENT_NAME]"
version: "1.0.0"
schema_type: "event"
fields:
  - name: "event_type"
    type: "string"
  - name: "task_id"
    type: "string"
  - name: "status"
    type: "string"
```

## Task Tracking

### Task States
1. **PENDING**: Task generated, awaiting implementation
2. **IN_PROGRESS**: Implementation started
3. **COMPLETED**: Implementation finished
4. **VERIFIED**: Verified against semantic requirement
5. **INTEGRATED**: Integrated into main system

### Task Metadata
```yaml
task_id: "TASK-001"
name: "Create reporting_integrator.py"
state: "PENDING"
created_at: "2026-02-04T11:30:00Z"
created_from: "semantic_validator"
violation_id: "VIOL-001"
estimated_effort: "4 hours"
actual_effort: null
assignee: null
completed_at: null
```

## Integration with Semantic Validator

### Workflow
```
Semantic Validator
    ↓ detects violations
Violation Analyzer
    ↓ categorizes violations
Task Generator
    ↓ creates implementation tasks
Artifact Generator
    ↓ creates stubs and schemas
Task Tracker
    ↓ tracks implementation progress
Implementation Queue
    ↓ prioritizes tasks
Developer Dashboard
```

## Configuration

### Generator Templates
Located in: `ecosystem/governance/templates/`

- `tool-stubs/` - Python tool implementation templates
- `artifact-schemas/` - Artifact schema templates
- `event-schemas/` - Event schema templates
- `task_definitions/` - Task definition templates

### Customization
```yaml
converter_config:
  output_dir: ".governance/tasks"
  template_dir: "ecosystem/governance/templates"
  auto_create_tasks: true
  auto_generate_artifacts: true
  track_implementation: true
  notify_assignees: false
```

## API

### Convert Violations to Tasks
```python
from ecosystem.tools.semantic_entity_task_converter import SemanticEntityTaskConverter

converter = SemanticEntityTaskConverter()
tasks = converter.convert_violations(violations)
converter.generate_artifacts(tasks)
converter.save_tasks(tasks)
```

### Track Task Progress
```python
task = converter.get_task("TASK-001")
task.state = "COMPLETED"
converter.update_task(task)
```

### Generate Report
```python
report = converter.generate_implementation_report()
print(f"Total tasks: {report.total_tasks}")
print(f"Completed: {report.completed_tasks}")
print(f"Pending: {report.pending_tasks}")
```

## Example Use Case

### Input: Semantic Violation
```
[CRITICAL] fictional_capability: "報告治理系統已整合"
Location: reports/system-status.md:23
```

### Output: Implementation Task
```yaml
task_id: "TASK-20260204-001"
name: "Create reporting_integrator.py"
description: "Implement reporting system integration with governance"
type: "tool_implementation"
priority: "CRITICAL"
estimated_effort: "4 hours"
artifacts:
  - tools/reporting_integrator.py
  - ecosystem/governance/tools-registry.yaml (update)
  - tools/reporting_integrator_test.py
status: "PENDING"
```

### Generated Files
1. `.governance/tasks/TASK-20260204-001.json`
2. `tools/reporting_integrator.py` (stub)
3. `tools/reporting_integrator_test.py` (stub)
4. `ecosystem/governance/tools-registry.yaml` (update)

## Benefits

1. **Semantics Preservation**: Original meaning is preserved through implementation
2. **Governance-Driven**: All work is traceable to governance requirements
3. **Automatic Generation**: Reduces manual effort in creating boilerplate
4. **Progress Tracking**: Clear visibility into implementation status
5. **Quality Assurance**: Ensures all claims have backing implementation

## Future Enhancements

1. **AI-Assisted Implementation**: Use LLMs to generate initial implementation
2. **Dependency Analysis**: Automatically detect and manage task dependencies
3. **Test Generation**: Auto-generate tests for implemented tools
4. **Documentation Generation**: Generate API docs from implementation
5. **CI/CD Integration**: Auto-validate implementations against original claims