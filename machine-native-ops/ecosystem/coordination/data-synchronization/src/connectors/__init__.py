#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Data Connectors
==================
數據連接器 - 支持多種數據源

GL Governance Layer: GL10-29 (Operational Layer)
"""

from .base_connector import BaseConnector
from .filesystem_connector import FilesystemConnector

__all__ = [
    'BaseConnector',
    'FilesystemConnector',
]
