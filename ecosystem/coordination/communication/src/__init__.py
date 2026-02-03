#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Communication System
=======================
通信系統 - 跨平台消息和事件處理

GL Governance Layer: GL10-29 (Operational Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
from .message_bus import MessageBus, Message, Subscription
from .event_dispatcher import EventDispatcher, EventHandler

__all__ = [
    # Message Bus
    'MessageBus',
    'Message',
    'Subscription',
    
    # Event Dispatcher
    'EventDispatcher',
    'EventHandler',
]

__version__ = '1.0.0'
