"""
Namespace-ADK: Machine-Native AI Agent Runtime Layer

A comprehensive agent runtime framework that orchestrates MCP tools,
manages agent memory and context, enforces runtime governance,
and supports multi-step, auditable workflows.

Version: 1.0.0
License: Apache 2.0

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk
@gl-semantic-anchor GL-00-NAMESPAC_ADK_INIT
@gl-evidence-required false
GL Unified Charter Activated
"""

__version__ = "1.0.0"
__author__ = "MachineNativeOps"

from .core.agent_runtime import AgentRuntime
from .core.context_manager import ContextManager
from .core.error_handling import ErrorHandler
from .core.event_bus import EventBus
from .core.memory_manager import MemoryManager
from .core.plugin_manager import PluginManager
from .core.sandbox import Sandbox
from .core.workflow_orchestrator import WorkflowOrchestrator
from .governance.ari_index import ARIIndex
from .governance.audit_trail import AuditTrail
from .governance.conformance_engine import ConformanceEngine
from .governance.containment import Containment
from .governance.drift_detection import DriftDetection
from .governance.mi9_runtime import MI9Runtime
from .mcp.a2a_client import A2AClient
from .mcp.mcp_client import MCPClient
from .mcp.mcp_security import MCPSecurity
from .mcp.tool_router import ToolRouter
from .mcp.tool_schemas import ToolSchemas
from .observability.event_schema import EventSchemaDef as EventSchema
from .observability.logging import Logger
from .observability.metrics import MetricsCollector
from .observability.tracing import Tracer
from .security.a2a_auth import A2AAuthenticator
from .security.auth import Authenticator
from .security.permissioning import PermissionManager
from .security.pii_filter import PIIFilter

__all__ = [
    # Core
    "AgentRuntime",
    "WorkflowOrchestrator",
    "MemoryManager",
    "ContextManager",
    "EventBus",
    "ErrorHandler",
    "PluginManager",
    "Sandbox",
    # MCP
    "MCPClient",
    "ToolRouter",
    "ToolSchemas",
    "A2AClient",
    "MCPSecurity",
    # Governance
    "MI9Runtime",
    "ARIIndex",
    "ConformanceEngine",
    "DriftDetection",
    "Containment",
    "AuditTrail",
    # Observability
    "Logger",
    "Tracer",
    "MetricsCollector",
    "EventSchema",
    # Security
    "Authenticator",
    "A2AAuthenticator",
    "PermissionManager",
    "PIIFilter",
]
