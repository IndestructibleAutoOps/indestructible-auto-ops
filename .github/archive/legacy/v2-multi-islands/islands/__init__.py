# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: archive-tools
# @GL-audit-trail: ../../engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
"""
島嶼模組

包含所有語言島嶼的實作。
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
from .base_island import BaseIsland, IslandStatus
from .go_island import GoIsland
from .java_island import JavaIsland
from .python_island import PythonIsland
from .rust_island import RustIsland
from .typescript_island import TypeScriptIsland

__all__ = [
    "BaseIsland",
    "IslandStatus",
    "RustIsland",
    "GoIsland",
    "TypeScriptIsland",
    "PythonIsland",
    "JavaIsland",
]
