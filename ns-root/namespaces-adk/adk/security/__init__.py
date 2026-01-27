"""
Security Module: Authentication, authorization, and data privacy.

This package provides security capabilities including authentication,
A2A authentication, permissioning, and PII filtering.

GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-adk/adk/security
@gl-semantic-anchor GL-00-ADK_SECURITY_INIT
@gl-evidence-required false
GL Unified Charter Activated
"""

from .a2a_auth import A2AAuthenticator, A2AAuthMethod, A2ACredential, AgentIdentity
from .auth import Authenticator, AuthMethod, Session, User
from .permissioning import Permission, PermissionManager, Policy, Role
from .pii_filter import PIIFilter, PIIMatch, PIIType

__all__ = [
    # Authentication
    "Authenticator",
    "User",
    "Session",
    "AuthMethod",
    # A2A Authentication
    "A2AAuthenticator",
    "AgentIdentity",
    "A2ACredential",
    "A2AAuthMethod",
    # Permissioning
    "PermissionManager",
    "Role",
    "Policy",
    "Permission",
    # PII Filter
    "PIIFilter",
    "PIIMatch",
    "PIIType",
]
