#!/usr/bin/env python3
"""Plugin System for SynergyMesh Workflow"""
import importlib
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class Plugin:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version

    def initialize(self) -> bool:
        return True

    def execute(self, context: dict[str, Any]) -> Any:
        """Execute the plugin with given context

        Args:
            context: Execution context with configuration and data

        Returns:
            Execution result
        """
        logger.info(f"Executing plugin: {self.name} v{self.version}")

        # Default implementation - subclasses should override
        return {
            "status": "success",
            "plugin": self.name,
            "version": self.version,
            "message": "Plugin executed successfully",
        }

    def cleanup(self):
        pass


class PluginRegistry:
    def __init__(self):
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin):
        self._plugins[plugin.name] = plugin
        logger.info(f"Plugin registered: {plugin.name} v{plugin.version}")

    def get(self, name: str) -> Plugin | None:
        return self._plugins.get(name)

    def list_all(self) -> list[Plugin]:
        return list(self._plugins.values())


class PluginLoader:
    def __init__(self, plugin_dirs: list[str]):
        self.plugin_dirs = plugin_dirs
        self.registry = PluginRegistry()

    def discover_plugins(self) -> list[str]:
        discovered = []
        for plugin_dir in self.plugin_dirs:
            path = Path(plugin_dir)
            if path.exists():
                for file in path.glob("*.py"):
                    if not file.name.startswith("_"):
                        discovered.append(str(file))
        return discovered

    def load_plugin(self, plugin_path: str) -> Plugin | None:
        try:
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "Plugin"):
                plugin = module.Plugin()
                self.registry.register(plugin)
                return plugin
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_path}: {e}")
        return None


class PluginSystem:
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.loader = PluginLoader(config.get("plugin_directories", []))

    def initialize(self):
        plugins = self.loader.discover_plugins()
        logger.info(f"Discovered {len(plugins)} plugins")
        for plugin_path in plugins:
            self.loader.load_plugin(plugin_path)
