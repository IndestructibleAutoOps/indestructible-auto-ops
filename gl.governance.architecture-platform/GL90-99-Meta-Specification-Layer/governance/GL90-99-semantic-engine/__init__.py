# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: python-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-enterprise-architecture/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-enterprise-architecture/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

"""
GL Semantic Core Engine
A fully functional semantic engine that transforms YAML specifications into
computable, reasonaable, indexable, and foldable semantic structures.

Phases Implemented:
- Phase 2: Semantic Folding (語意折疊)
- Phase 3: Semantic Parameterization (語意參數化)
- Phase 4: Semantic Indexing (語意索引)
- Phase 5: Semantic Optimization (語意性能優化)
- Phase 6: Semantic Engine Integration (語意引擎化)
"""

from .gl_platform_universe.gl_platform_universe.governance.semantic_engine import SemanticEngine
from .semantic_models import (
    SemanticNode, 
    SemanticNodeType, 
    SemanticEdge, 
    SemanticGraph, 
    SemanticIndex
)
from .semantic_folding import SemanticFoldingEngine
from .semantic_parameterization import SemanticParameterizationEngine
from .semantic_indexing import SemanticIndexingEngine
from .semantic_inference import SemanticInferenceEngine

__version__ = "1.0.0"
__author__ = "GL Semantic Core Platform"

__all__ = [
    'SemanticEngine',
    'SemanticNode',
    'SemanticNodeType',
    'SemanticEdge',
    'SemanticGraph',
    'SemanticIndex',
    'SemanticFoldingEngine',
    'SemanticParameterizationEngine',
    'SemanticIndexingEngine',
    'SemanticInferenceEngine',
]