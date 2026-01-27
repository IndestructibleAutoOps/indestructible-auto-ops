"""
Plugins: Plugin system for extensibility.

This package provides plugin infrastructure for tools, memory,
workflows, and SDK integrations.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/plugins
@gl-semantic-anchor GL-00-ADK_PLUGINS_INIT
@gl-evidence-required false
GL Unified Charter Activated
"""

from ..core.plugin_manager import (
    Plugin,
    PluginInterface,
    PluginManager,
    PluginManifest,
    PluginType,
)

__all__ = [
    "PluginManager",
    "Plugin",
    "PluginManifest",
    "PluginType",
    "PluginInterface",
]
