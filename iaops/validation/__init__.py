"""
Enterprise Strict Engineering Validation System
企业级严格工程验证系统

Core modules:
- validator: Base data structures and severity definitions
- regression_detector: Numeric and structural regression detection
- whitelist_manager: Whitelist rule management with audit trail
- strict_validator: Main validation engine with pipeline orchestration
- file_validator: Source file integrity checker
- performance_validator: Performance regression detector
"""

from .regression_detector import RegressionDetector
from .strict_validator import StrictValidator, ValidationEngine
from .validator import (
    Severity,
    ValidationConfig,
    ValidationIssue,
    ValidationResult,
    ValidatorResult,
)
from .whitelist_manager import WhitelistManager, WhitelistRule

__all__ = [
    "Severity",
    "ValidationIssue",
    "ValidatorResult",
    "ValidationResult",
    "ValidationConfig",
    "RegressionDetector",
    "WhitelistManager",
    "WhitelistRule",
    "StrictValidator",
    "ValidationEngine",
]

__version__ = "1.0.0"
