# Foundation Layer Package
# GL Layer: GL00-09 Strategic Layer
#
# The Foundation Layer provides the base for all governance:
# - Language Layer (L0): Parser and validator specifications
# - Format Layer (L1): Schema and structure definitions
# - Semantic Layer (L2): Meaning and governance rules
#
# Hierarchy: Language → Format → Semantic

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""

from .language import (
    LanguageEnforcer,
    LanguageType,
    LanguageViolation,
    LanguageValidationResult,
    Severity as LanguageSeverity,
)

from .format import (
    FormatEnforcer,
    FormatType,
    FormatViolation,
    FormatValidationResult,
    Severity as FormatSeverity,
)

from .foundation_dag import (
    FoundationDAG,
    FoundationLayer,
    DAGNode,
    DAGEdge,
    UnifiedFoundationEnforcer,
)

__all__ = [
    # Language Layer
    "LanguageEnforcer",
    "LanguageType",
    "LanguageViolation",
    "LanguageValidationResult",
    "LanguageSeverity",
    # Format Layer
    "FormatEnforcer",
    "FormatType",
    "FormatViolation",
    "FormatValidationResult",
    "FormatSeverity",
    # Foundation DAG
    "FoundationDAG",
    "FoundationLayer",
    "DAGNode",
    "DAGEdge",
    "UnifiedFoundationEnforcer",
]
