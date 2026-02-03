#
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: governance
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Meta-Governance Framework
=============================
元治理框架 - 驗證器規範治理

GL Governance Layer: GL90-99 (Meta-Specification Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
from .version_manager import (
    VersionManager,
    SemanticVersion,
    VersionType,
    ReleaseType,
    VersionMetadata
)

from .change_manager import (
    ChangeManager,
    ChangeRequest,
    ImpactLevel,
    ChangeStatus
)

from .review_manager import (
    ReviewManager,
    Review,
    ReviewComment,
    ReviewLayer,
    ReviewDecision
)

from .dependency_manager import (
    DependencyManager,
    Dependency
)

from .governance_framework import GovernanceFramework

__all__ = [
    # Version Management
    'VersionManager',
    'SemanticVersion',
    'VersionType',
    'ReleaseType',
    'VersionMetadata',
    
    # Change Management
    'ChangeManager',
    'ChangeRequest',
    'ImpactLevel',
    'ChangeStatus',
    
    # Review Management
    'ReviewManager',
    'Review',
    'ReviewComment',
    'ReviewLayer',
    'ReviewDecision',
    
    # Dependency Management
    'DependencyManager',
    'Dependency',
    
    # Governance Framework
    'GovernanceFramework',
]

__version__ = '1.0.0'
