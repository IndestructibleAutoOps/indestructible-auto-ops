"""
Semantic Layer - Language-Neutral Semantic Tokenization

This module provides language-neutral semantic tokenization, AST building,
hash computation, and multi-language evidence sealing for governance systems.

Author: IndestructibleAutoOps
Version: 1.0
Date: 2024-02-05
"""

from .tokenizer import SemanticTokenizer, SemanticToken, TokenType
from .ast_builder import SemanticAST, ASTNode, NodeType
from .hasher import SemanticHasher
from .multilang_evidence import MultiLanguageEvidence, MultiLanguageEvidenceSealer
from .canonicalizer import SemanticCanonicalizer

__all__ = [
    # Tokenizer
    'SemanticTokenizer',
    'SemanticToken',
    'TokenType',
    # AST Builder
    'SemanticAST',
    'ASTNode',
    'NodeType',
    # Hasher
    'SemanticHasher',
    # Multi-Language Evidence
    'MultiLanguageEvidence',
    'MultiLanguageEvidenceSealer',
    # Canonicalizer
    'SemanticCanonicalizer',
]

__version__ = '1.0.0'