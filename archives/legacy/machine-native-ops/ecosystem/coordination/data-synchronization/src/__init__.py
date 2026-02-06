#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Data Synchronization System
===============================
數據同步系統 - 跨平台數據同步

GL Governance Layer: GL10-29 (Operational Layer)
"""

from .sync_engine import SyncEngine, SyncJob, SyncMode, SyncStatus, DataItem
from .conflict_resolver import ConflictResolver, Conflict
from .sync_scheduler import SyncScheduler, Schedule
from .connectors import BaseConnector, FilesystemConnector

__all__ = [
    # Sync Engine
    'SyncEngine',
    'SyncJob',
    'SyncMode',
    'SyncStatus',
    'DataItem',
    
    # Conflict Resolver
    'ConflictResolver',
    'Conflict',
    
    # Scheduler
    'SyncScheduler',
    'Schedule',
    
    # Connectors
    'BaseConnector',
    'FilesystemConnector',
]

__version__ = '1.0.0'
