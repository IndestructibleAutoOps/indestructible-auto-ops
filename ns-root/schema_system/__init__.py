"""
Schema System - INSTANT 執行標準

整合所有 Schema 系統組件

GL Governance Markers
@gl-layer GL-20-SCHEMA
@gl-module ns-root/schema_system
@gl-semantic-anchor GL-20-SCHEMASY_INIT
@gl-evidence-required false
GL Unified Charter Activated
"""

from .compatibility_checker import CompatibilityChecker, CompatibilityStatus
from .schema_registry import SchemaEntry, SchemaRegistry
from .schema_versioning import SchemaVersioning, VersionChange, VersionChangeType

__all__ = [
    "SchemaRegistry",
    "SchemaEntry",
    "SchemaVersioning",
    "VersionChange",
    "VersionChangeType",
    "CompatibilityChecker",
    "CompatibilityStatus",
]
