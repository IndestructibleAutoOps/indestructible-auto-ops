"""
共享常數模組
"""

from .system_constants import (
    BRIDGE_PROTOCOLS,
    CONFIG_FILES,
    DEFAULT_TIMEOUT,
    ISLAND_TYPES,
    SUPPORTED_MODES,
    SYSTEM_NAME,
    VERSION,
)

__all__ = [
    "VERSION",
    "SYSTEM_NAME",
    "SUPPORTED_MODES",
    "ISLAND_TYPES",
    "BRIDGE_PROTOCOLS",
    "DEFAULT_TIMEOUT",
    "CONFIG_FILES",
]
