# GL Runtime V1 - Basic Execution Layer

## 概述
V1 是 GL Runtime 架構的基礎執行層，遵循 URSS (Unified Structure Specification)。

## 核心能力
- Task Execution (任務執行)
- Task State Management (狀態管理)
- Task I/O (輸入輸出)

## 目錄結構
```
v1-basic-execution/
├── manifest.json
├── docs/
│   ├── overview/
│   ├── specs/
│   ├── api/
│   └── adr/
├── src/core/
│   ├── task/task_executor.py
│   ├── state/state_machine.py
│   ├── io/io_handler.py
│   └── runtime/
└── tests/
```

## 治理
- Governance Level: 0 (No Governance)
- 依賴: 無

## 使用
```python
from src.core.task.task_executor import TaskExecutor
executor = TaskExecutor()
task = executor.create_task("task-1", {"action": "process"})
result = executor.execute("task-1")
```
