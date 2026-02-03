#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL API Gateway System
=====================
API 網關系統 - 統一API入口

GL Governance Layer: GL10-29 (Operational Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
from .router import Router, Route, RouteMatchType
from .authenticator import Authenticator, AuthToken
from .rate_limiter import RateLimiter, TokenBucket, RateLimitConfig
from .gateway import Gateway

__all__ = [
    # Router
    'Router',
    'Route',
    'RouteMatchType',
    
    # Authenticator
    'Authenticator',
    'AuthToken',
    
    # Rate Limiter
    'RateLimiter',
    'TokenBucket',
    'RateLimitConfig',
    
    # Gateway
    'Gateway',
]

__version__ = '1.0.0'
