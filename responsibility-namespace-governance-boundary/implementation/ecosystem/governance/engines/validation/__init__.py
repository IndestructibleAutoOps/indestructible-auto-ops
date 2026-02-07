# @GL-semantic: org.mnga.engines.validation@1.0.0
# @GL-audit-trail: enabled
"""
Validation Engine - Validate governance specifications
"""

from .validation_engine import ValidationEngine, ValidationResult, ValidationError

__all__ = ["ValidationEngine", "ValidationResult", "ValidationError"]
