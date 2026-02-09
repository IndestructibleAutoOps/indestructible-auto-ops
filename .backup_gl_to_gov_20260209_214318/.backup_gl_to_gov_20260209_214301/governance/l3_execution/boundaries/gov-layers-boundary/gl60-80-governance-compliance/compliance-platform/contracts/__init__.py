# @GL-layer: GL60-80
# @GL-governed
"""
GL Governance Compliance - Contracts Module

This module provides GL contract validation, policy evaluation,
and quality gate enforcement.
"""

from .gov_contract import GLContract, GLContractException
from .gov_policy import GLPolicy, PolicyCondition
from .gov_validator import GLContractValidator, ValidationResult, ValidationError
from .gl_quality_gate import GLQualityGate, QualityGateStatus
from .gl_audit_event import GLAuditEvent

__all__ = [
    'GLContract',
    'GLContractException',
    'GLPolicy',
    'PolicyCondition',
    'GLContractValidator',
    'ValidationResult',
    'ValidationError',
    'GLQualityGate',
    'QualityGateStatus',
    'GLAuditEvent'
]

__version__ = '1.0.0'