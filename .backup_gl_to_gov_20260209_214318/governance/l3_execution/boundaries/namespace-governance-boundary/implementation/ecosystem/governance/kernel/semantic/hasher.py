#!/usr/bin/env python3
"""
Semantic Hasher - Language-Neutral Hash Computation

Computes semantic hashes from natural language text, ensuring same semantics
produce same hash across different languages.

Author: IndestructibleAutoOps
Version: 1.0
Date: 2024-02-05
"""

import json
from typing import Dict, Any, Optional

from .tokenizer import SemanticTokenizer, SemanticToken
from .ast_builder import SemanticAST, ASTNode


class SemanticHasher:
    """Semantic Hasher"""

    def __init__(self):
        self.tokenizer = SemanticTokenizer()
        self.ast_builder = SemanticAST()

    def hash_text(self, text: str, language: str = "auto") -> str:
        """
        Hash text semantically

        Process:
        1. Tokenize → semantic tokens
        2. Build AST → semantic AST
        3. Canonicalize → RFC 8785 JSON
        4. Hash → SHA256

        Args:
            text: Text to hash
            language: Language code (auto-detect if "auto")

        Returns:
            Hash as "sha256:..." format
        """
        # Step 1: Tokenize
        tokens = self.tokenizer.tokenize(text, language)

        # Step 2: Build AST
        self.ast_builder.build(tokens)

        # Step 3: Canonicalize
        canonical_json = self.ast_builder.to_canonical_json()

        # Step 4: Hash
        hash_value = self.ast_builder.hash()

        return hash_value

    def hash_tokens(self, tokens: list[SemanticToken]) -> str:
        """
        Hash semantic tokens

        Args:
            tokens: List of semantic tokens

        Returns:
            Hash as "sha256:..." format
        """
        self.ast_builder.build(tokens)
        return self.ast_builder.hash()

    def hash_dict(
        self, obj: Dict[str, Any], exclude_fields: Optional[list] = None
    ) -> str:
        """
        Hash dictionary semantically

        Args:
            obj: Dictionary to hash
            exclude_fields: Fields to exclude from hash

        Returns:
            Hash as "sha256:..." format
        """
        exclude_fields = exclude_fields or []

        # Remove excluded fields
        clean_obj = {k: v for k, v in obj.items() if k not in exclude_fields}

        # Canonicalize
        canonical_json = json.dumps(
            clean_obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )

        # Hash
        import hashlib

        hash_value = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

        return f"sha256:{hash_value}"

    def compare_hash(self, hash1: str, hash2: str) -> bool:
        """
        Compare two hashes

        Args:
            hash1: First hash
            hash2: Second hash

        Returns:
            True if hashes are equal
        """
        return hash1 == hash2

    def get_semantic_signature(self, text: str, language: str = "auto") -> str:
        """
        Get semantic signature (compact representation)

        Args:
            text: Text to analyze
            language: Language code

        Returns:
            Compact signature string
        """
        tokens = self.tokenizer.tokenize(text, language)
        self.ast_builder.build(tokens)
        return self.ast_builder.get_semantic_signature()
