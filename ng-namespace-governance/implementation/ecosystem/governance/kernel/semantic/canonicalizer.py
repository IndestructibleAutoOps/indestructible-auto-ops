#!/usr/bin/env python3
"""
Semantic Canonicalizer - Semantic Expression Normalization

Normalizes different phrasing variations into standard semantic forms,
ensuring consistent representation across different expressions.

Author: IndestructibleAutoOps
Version: 1.0
Date: 2024-02-05
"""

from typing import Dict, List, Set, Any
import re

from .tokenizer import SemanticTokenizer, SemanticToken, TokenType


class SemanticCanonicalizer:
    """Semantic canonicalization engine"""

    def __init__(self):
        self.tokenizer = SemanticTokenizer()
        self.canonicalization_rules = self._load_canonicalization_rules()

    def canonicalize(self, text: str, language: str = "auto") -> str:
        """
        Canonicalize semantic expression

        Example:
        Input: "把用戶 alice 刪掉"
        Output: "delete user alice"

        Input: "remove the user named alice"
        Output: "delete user alice"

        Args:
            text: Text to canonicalize
            language: Language code (auto-detect if "auto")

        Returns:
            Canonicalized expression (in English)
        """
        detected_lang = (
            language if language != "auto" else self.tokenizer._detect_language(text)
        )

        # Tokenize
        tokens = self.tokenizer.tokenize(text, detected_lang)

        # Apply canonicalization rules
        canonical_tokens = self._apply_canonicalization_rules(tokens, detected_lang)

        # Detokenize to English
        canonical_expression = self.tokenizer.detokenize(canonical_tokens, "en")

        return canonical_expression

    def _apply_canonicalization_rules(
        self, tokens: List[SemanticToken], language: str
    ) -> List[SemanticToken]:
        """
        Apply canonicalization rules

        Rules example:
        - "刪掉" / "移除" / "remove" → "delete"
        - "新增" / "加入" / "add" → "create"
        - "修改" / "更新" / "update" → "modify"

        Args:
            tokens: List of semantic tokens
            language: Language code

        Returns:
            Canonicalized tokens
        """
        canonical_tokens = []

        for token in tokens:
            if token.type == TokenType.ACTION:
                # Apply action canonicalization
                canonical_action = self._canonicalize_action(token.canonical, language)
                canonical_tokens.append(
                    SemanticToken(
                        type=token.type, value=token.value, canonical=canonical_action
                    )
                )
            elif token.type == TokenType.ENTITY:
                # Apply entity canonicalization
                canonical_entity = self._canonicalize_entity(token.canonical, language)
                canonical_tokens.append(
                    SemanticToken(
                        type=token.type, value=token.value, canonical=canonical_entity
                    )
                )
            else:
                # Keep other tokens as-is
                canonical_tokens.append(token)

        return canonical_tokens

    def _canonicalize_action(self, action: str, language: str) -> str:
        """Canonicalize action"""
        action_map = {
            "add": "create",
            "insert": "create",
            "register": "create",
            "establish": "create",
            "remove": "delete",
            "drop": "delete",
            "erase": "delete",
            "revoke": "delete",
            "modify": "update",
            "change": "update",
            "adjust": "update",
            "edit": "update",
            "search": "query",
            "find": "query",
            "lookup": "query",
            "retrieve": "query",
        }
        return action_map.get(action.lower(), action)

    def _canonicalize_entity(self, entity: str, language: str) -> str:
        """Canonicalize entity"""
        entity_map = {
            "account": "user",
            "member": "user",
            "component": "service",
            "db": "database",
        }
        return entity_map.get(entity.lower(), entity)

    def _load_canonicalization_rules(self) -> Dict[str, Any]:
        """Load canonicalization rules"""
        return {
            "action_aliases": {
                "create": [
                    "add",
                    "insert",
                    "register",
                    "establish",
                    "產生",
                    "建立",
                    "新增",
                    "加入",
                ],
                "delete": [
                    "remove",
                    "drop",
                    "erase",
                    "revoke",
                    "刪除",
                    "移除",
                    "刪掉",
                    "撤銷",
                ],
                "update": [
                    "modify",
                    "change",
                    "adjust",
                    "edit",
                    "更新",
                    "修改",
                    "變更",
                    "調整",
                ],
                "query": [
                    "search",
                    "find",
                    "lookup",
                    "retrieve",
                    "查詢",
                    "搜索",
                    "尋找",
                    "查找",
                ],
            },
            "entity_aliases": {
                "user": ["account", "member", "用戶", "使用者", "帳號", "賬戶"],
                "service": ["component", "服務", "服務項"],
                "deployment": ["release", "部署", "發布", "上線"],
                "database": ["db", "數據庫", "資料庫"],
            },
        }

    def get_canonical_variants(self, canonical: str, token_type: TokenType) -> Set[str]:
        """
        Get all variants of a canonical token

        Args:
            canonical: Canonical value
            token_type: Token type

        Returns:
            Set of all variants
        """
        variants = {canonical}

        if token_type == TokenType.ACTION:
            variants.update(
                self.canonicalization_rules.get("action_aliases", {}).get(canonical, [])
            )
        elif token_type == TokenType.ENTITY:
            variants.update(
                self.canonicalization_rules.get("entity_aliases", {}).get(canonical, [])
            )

        return variants
