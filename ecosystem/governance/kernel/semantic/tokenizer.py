#!/usr/bin/env python3
"""
Semantic Tokenizer - Language-Neutral Semantic Tokenization Engine

Converts natural language to semantic token sequences, enabling language-neutral
hash computation and cross-language governance sealing.

Author: IndestructibleAutoOps
Version: 1.0
Date: 2024-02-05
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class TokenType(Enum):
    """Semantic token types"""

    ACTION = "ACTION"  # create, delete, update, query
    ENTITY = "ENTITY"  # user, service, deployment
    IDENTIFIER = "IDENTIFIER"  # alice@example.com, nginx
    CONDITION = "CONDITION"  # if, when, unless
    VALUE = "VALUE"  # strings, numbers
    OPERATOR = "OPERATOR"  # and, or, not


@dataclass
class SemanticToken:
    """Semantic token"""

    type: TokenType
    value: str  # Original value
    canonical: str  # Canonicalized value (language-neutral)
    metadata: Dict[str, Any] = field(default_factory=dict)


class SemanticTokenizer:
    """Semantic Tokenization Engine"""

    def __init__(self):
        self.language_patterns = self._load_language_patterns()

    def tokenize(self, text: str, language: str = "auto") -> List[SemanticToken]:
        """
        Convert text to semantic tokens

        Example:
        Input: "創建用戶 alice@example.com"
        Output: [
          SemanticToken(type=ACTION, value="創建", canonical="create"),
          SemanticToken(type=ENTITY, value="用戶", canonical="user"),
          SemanticToken(type=IDENTIFIER, value="alice@example.com", canonical="alice@example.com")
        ]
        """
        detected_lang = language if language != "auto" else self._detect_language(text)
        tokens = []

        # Extract action
        action_token = self._extract_action(text, detected_lang)
        if action_token:
            tokens.append(action_token)

        # Extract entity
        entity_token = self._extract_entity(text, detected_lang)
        if entity_token:
            tokens.append(entity_token)

        # Extract identifier
        identifier_token = self._extract_identifier(text, detected_lang)
        if identifier_token:
            tokens.append(identifier_token)

        return tokens

    def detokenize(self, tokens: List[SemanticToken], target_language: str) -> str:
        """
        Convert semantic tokens back to target language

        Example:
        Input: [ACTION: create, ENTITY: user, IDENTIFIER: alice@example.com]
        Output (zh): "創建用戶 alice@example.com"
        Output (en): "create user alice@example.com"
        """
        translations = self._load_translations(target_language)
        result = []

        for token in tokens:
            if token.type == TokenType.ACTION:
                result.append(
                    translations.get("actions", {}).get(token.canonical, token.value)
                )
            elif token.type == TokenType.ENTITY:
                result.append(
                    translations.get("entities", {}).get(token.canonical, token.value)
                )
            else:
                result.append(token.value)

        return " ".join(result)

    def _detect_language(self, text: str) -> str:
        """Detect language from text"""
        # Japanese
        # Note: Japanese often includes Kanji (CJK range); detect Kana first.
        if re.search(r"[\u3040-\u309f\u30a0-\u30ff]", text):
            return "ja"
        # Korean
        elif re.search(r"[\uac00-\ud7af]", text):
            return "ko"
        # Chinese
        elif re.search(r"[\u4e00-\u9fff]", text):
            return "zh"
        # German
        elif re.search(r"[äöüß]", text):
            return "de"
        # French
        elif re.search(r"[éèêëàâôîïûùç]", text):
            return "fr"
        # English (default)
        else:
            return "en"

    def _extract_action(self, text: str, language: str) -> Optional[SemanticToken]:
        """Extract action token"""
        action_patterns = {
            "zh": {
                "create": r"(創建|新增|加入|建立|產生)",
                "delete": r"(刪除|移除|刪掉|撤銷)",
                "update": r"(更新|修改|變更|調整)",
                "query": r"(查詢|搜索|尋找|查找)",
            },
            "en": {
                "create": r"(create|add|insert|register|establish|generate)",
                "delete": r"(delete|remove|drop|erase|revoke)",
                "update": r"(update|modify|change|adjust|edit)",
                "query": r"(query|search|find|lookup|retrieve)",
            },
        }

        patterns = action_patterns.get(language, action_patterns["en"])
        for canonical, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return SemanticToken(
                    type=TokenType.ACTION, value=match.group(), canonical=canonical
                )
        return None

    def _extract_entity(self, text: str, language: str) -> Optional[SemanticToken]:
        """Extract entity token"""
        entity_patterns = {
            "zh": {
                "user": r"(用戶|使用者|帳號|賬戶)",
                "service": r"(服務|服務項)",
                "deployment": r"(部署|發布|上線)",
                "database": r"(數據庫|資料庫)",
            },
            "en": {
                "user": r"(user|account|member)",
                "service": r"(service|component)",
                "deployment": r"(deployment|release)",
                "database": r"(database|db)",
            },
        }

        patterns = entity_patterns.get(language, entity_patterns["en"])
        for canonical, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return SemanticToken(
                    type=TokenType.ENTITY, value=match.group(), canonical=canonical
                )
        return None

    def _extract_identifier(self, text: str, language: str) -> Optional[SemanticToken]:
        """Extract identifier token"""
        # Email pattern
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        if email_match:
            return SemanticToken(
                type=TokenType.IDENTIFIER,
                value=email_match.group(),
                canonical=email_match.group(),
            )

        # Prefer ASCII identifiers (names, service ids) over trailing CJK tokens.
        # Example: "把用戶 alice 刪掉" should extract "alice" (not "刪掉").
        ascii_identifiers = re.findall(r"\b[a-zA-Z0-9][a-zA-Z0-9._-]*\b", text)
        for identifier in reversed(ascii_identifiers):
            if identifier.lower() not in {"user", "service", "deployment", "database", "db"}:
                return SemanticToken(
                    type=TokenType.IDENTIFIER, value=identifier, canonical=identifier
                )

        return None

    def _load_language_patterns(self) -> Dict[str, Any]:
        """Load language patterns"""
        return {}

    def _load_translations(self, target_language: str) -> Dict[str, Any]:
        """Load translations for target language"""
        translations = {
            "zh": {
                "actions": {
                    "create": "創建",
                    "delete": "刪除",
                    "update": "更新",
                    "query": "查詢",
                },
                "entities": {
                    "user": "用戶",
                    "service": "服務",
                    "deployment": "部署",
                    "database": "數據庫",
                },
            },
            "en": {
                "actions": {
                    "create": "create",
                    "delete": "delete",
                    "update": "update",
                    "query": "query",
                },
                "entities": {
                    "user": "user",
                    "service": "service",
                    "deployment": "deployment",
                    "database": "database",
                },
            },
        }
        return translations.get(target_language, translations["en"])
