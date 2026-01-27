"""
Core Runtime Modules: Agent lifecycle, orchestration, memory, and context.

This package provides the core runtime components for the agent system.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/core
@gl-semantic-anchor GL-00-ADK_CORE_INIT
@gl-evidence-required false
GL Unified Charter Activated
"""

from .agent_runtime import AgentConfig, AgentRuntime, AgentState
from .context_manager import ContextManager, ContextScope, ContextSnapshot
from .error_handling import (
    ErrorHandler,
    ErrorInfo,
    ErrorSeverity,
    ErrorType,
    RetryPolicy,
    retry,
)
from .event_bus import Event, EventBus, EventPriority, Subscription
from .memory_manager import (
    InMemoryBackend,
    MemoryBackend,
    MemoryEntry,
    MemoryManager,
    MemoryQuery,
    MemoryType,
)
from .plugin_manager import (
    Plugin,
    PluginInterface,
    PluginManager,
    PluginManifest,
    PluginType,
)
from .sandbox import (
    ResourceLimits,
    Sandbox,
    SandboxConfig,
    SandboxExecution,
    SandboxState,
    SandboxType,
)
from .workflow_orchestrator import (
    StepType,
    WorkflowDefinition,
    WorkflowExecution,
    WorkflowOrchestrator,
    WorkflowState,
    WorkflowStep,
)

__all__ = [
    # Agent Runtime
    "AgentRuntime",
    "AgentState",
    "AgentConfig",
    # Workflow Orchestrator
    "WorkflowOrchestrator",
    "WorkflowDefinition",
    "WorkflowStep",
    "WorkflowExecution",
    "WorkflowState",
    "StepType",
    # Memory Manager
    "MemoryManager",
    "MemoryEntry",
    "MemoryQuery",
    "MemoryType",
    "MemoryBackend",
    "InMemoryBackend",
    # Context Manager
    "ContextManager",
    "ContextScope",
    "ContextSnapshot",
    # Event Bus
    "EventBus",
    "Event",
    "EventPriority",
    "Subscription",
    # Error Handling
    "ErrorHandler",
    "ErrorInfo",
    "ErrorType",
    "ErrorSeverity",
    "RetryPolicy",
    "retry",
    # Plugin Manager
    "PluginManager",
    "Plugin",
    "PluginManifest",
    "PluginType",
    "PluginInterface",
    # Sandbox
    "Sandbox",
    "SandboxConfig",
    "ResourceLimits",
    "SandboxType",
    "SandboxState",
    "SandboxExecution",
]
