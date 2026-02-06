#!/usr/bin/env python3
"""
Semantic AST Builder - Abstract Syntax Tree for Semantic Tokens

Builds a canonical AST from semantic tokens, enabling language-neutral
hash computation and semantic consistency validation.

Author: IndestructibleAutoOps
Version: 1.0
Date: 2024-02-05
"""

import json
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

from .tokenizer import SemanticToken, TokenType


class NodeType(Enum):
    """AST node types"""

    ACTION = "action"
    ENTITY = "entity"
    IDENTIFIER = "identifier"
    SEQUENCE = "sequence"
    CONDITION = "condition"
    OPERATOR = "operator"


@dataclass
class ASTNode:
    """AST node"""

    node_type: NodeType
    canonical_value: str
    children: List["ASTNode"] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self, include_metadata: bool = True) -> Dict[str, Any]:
        """Convert to dictionary.

        For language-neutral hashing, canonical JSON should exclude language-specific
        metadata (e.g. original_value). Callers can include metadata for debugging.
        """
        result = {
            "node_type": self.node_type.value,
            "canonical_value": self.canonical_value,
            "children": [child.to_dict(include_metadata=include_metadata) for child in self.children],
        }
        if include_metadata and self.metadata:
            result["metadata"] = self.metadata
        return result

    def add_child(self, child: "ASTNode"):
        """Add child node"""
        self.children.append(child)

    def is_leaf(self) -> bool:
        """Check if node is leaf (no children)"""
        return len(self.children) == 0


class SemanticAST:
    """Semantic Abstract Syntax Tree"""

    def __init__(self):
        self.root = None

    def build(self, tokens: List[SemanticToken]) -> "SemanticAST":
        """
        Build AST from semantic tokens

        Args:
            tokens: List of semantic tokens

        Returns:
            Self for method chaining
        """
        # Create sequence node as root
        self.root = ASTNode(
            node_type=NodeType.SEQUENCE,
            canonical_value="sequence",
            metadata={"token_count": len(tokens)},
        )

        # Add tokens as children
        for token in tokens:
            node = self._token_to_node(token)
            if node:
                self.root.add_child(node)

        return self

    def _token_to_node(self, token: SemanticToken) -> Optional[ASTNode]:
        """Convert semantic token to AST node"""
        node_type_map = {
            TokenType.ACTION: NodeType.ACTION,
            TokenType.ENTITY: NodeType.ENTITY,
            TokenType.IDENTIFIER: NodeType.IDENTIFIER,
            TokenType.CONDITION: NodeType.CONDITION,
            TokenType.OPERATOR: NodeType.OPERATOR,
        }

        node_type = node_type_map.get(token.type)
        if not node_type:
            return None

        return ASTNode(
            node_type=node_type,
            canonical_value=token.canonical,
            metadata={"original_value": token.value, "original_type": token.type.value},
        )

    def to_canonical_json(self) -> str:
        """
        Convert to canonical JSON (RFC 8785)
        Ensures same semantics produce same JSON

        Returns:
            Canonical JSON string
        """
        if self.root is None:
            return "{}"

        # Exclude metadata from canonical JSON to ensure language-neutral hashing.
        ast_dict = self.root.to_dict(include_metadata=False)
        return json.dumps(
            ast_dict, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )

    def hash(self) -> str:
        """
        Compute semantic hash (SHA256)
        Based on canonical JSON

        Returns:
            Hash as "sha256:..." format
        """
        canonical = self.to_canonical_json()
        hash_value = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return f"sha256:{hash_value}"

    def get_semantic_signature(self) -> str:
        """
        Get semantic signature (compact representation)

        Returns:
            Compact signature string
        """
        if self.root is None:
            return ""

        def visit(node: ASTNode) -> str:
            if node.is_leaf():
                return f"{node.node_type.value}:{node.canonical_value}"
            children_sig = "|".join(visit(child) for child in node.children)
            return f"{node.node_type.value}[{children_sig}]"

        return visit(self.root)
