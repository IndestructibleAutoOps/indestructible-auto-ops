#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Service Discovery System
============================
服務發現系統 - 自動服務註冊和發現

GL Governance Layer: GL10-29 (Operational Layer)
"""

from .service_registry import (
    ServiceRegistry,
    ServiceInstance,
    ServiceMetadata,
    HealthCheck,
    ServiceStatus,
    HealthStatus
)

from .service_agent import ServiceAgent

from .service_client import (
    ServiceClient,
    LoadBalancingStrategy,
    RoundRobinStrategy,
    RandomStrategy,
    HealthBasedStrategy,
    WeightedStrategy,
    LeastConnectionsStrategy
)

__all__ = [
    # Registry
    'ServiceRegistry',
    'ServiceInstance',
    'ServiceMetadata',
    'HealthCheck',
    'ServiceStatus',
    'HealthStatus',
    
    # Agent
    'ServiceAgent',
    
    # Client
    'ServiceClient',
    'LoadBalancingStrategy',
    'RoundRobinStrategy',
    'RandomStrategy',
    'HealthBasedStrategy',
    'WeightedStrategy',
    'LeastConnectionsStrategy',
]

__version__ = '1.0.0'
