# Backend Governance Responsibility Specification
# IndestructibleAutoOps Technical Specification
# Version: 2.0.0
# Status: CANONICAL
# GL Level: GL50 (Indestructible Kernel)

## Platform Definition

**IndestructibleAutoOps** is a cloud-native AIOps platform providing autonomous infrastructure resilience through ML-driven self-healing.

**Core Philosophy**: Backend is not a "function executor", but a "Governance Gatekeeper"

```
Traditional Backend: Receive request → Execute logic → Return result
Governance Backend: Receive request → Verify governance → Seal evidence → Execute logic → Verify output → Seal decision → Return result
```

---

## GL-5L: Five-Layer Governance Responsibility Model

### Overview

```
Layer 5: 存儲層 (Repository Layer)        ← Multi-platform consistency
Layer 4: 治理層 (Governance Layer)         ← Rule enforcement
Layer 3: 封存層 (Evidence Layer)           ← Evidence chain integrity
Layer 2: 決策層 (Decision Layer)           ← Decision replay
Layer 1: 語意層 (Semantic Layer)           ← Language-neutral sealing
```

**Rule**: Upper layers depend on lower layers, lower layers MUST NOT depend on upper layers.

---

## Layer 1: 語意層 (Semantic Layer)

### Responsibility Definition

**Backend MUST be responsible for semantic sealing, not language presentation.**

All governance-critical information MUST be sealed in "language-neutral" form, ensuring:
- Same semantics in different languages produce the same hash
- Semantics can be replayed across languages
- Semantics can be replayed across AI models

---

### Responsibility 1.1: Semantic Tokenization

**Definition**: Convert natural language to semantic token sequences.

**Implementation Requirements**:

```python
# governance/kernel/semantic/tokenizer.py

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

class TokenType(Enum):
    """Semantic token types"""
    ACTION = "ACTION"           # create, delete, update, query
    ENTITY = "ENTITY"           # user, service, deployment
    IDENTIFIER = "IDENTIFIER"   # alice@example.com, nginx
    CONDITION = "CONDITION"     # if, when, unless
    VALUE = "VALUE"            # strings, numbers
    OPERATOR = "OPERATOR"       # and, or, not

@dataclass
class SemanticToken:
    """Semantic token"""
    type: TokenType
    value: str          # Original value
    canonical: str      # Canonicalized value (language-neutral)
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
                result.append(translations.get("actions", {}).get(token.canonical, token.value))
            elif token.type == TokenType.ENTITY:
                result.append(translations.get("entities", {}).get(token.canonical, token.value))
            else:
                result.append(token.value)
        
        return " ".join(result)
    
    def _detect_language(self, text: str) -> str:
        """Detect language from text"""
        import re
        
        # Chinese
        if re.search(r'[\u4e00-\u9fff]', text):
            return "zh"
        # Japanese
        elif re.search(r'[\u3040-\u309f\u30a0-\u30ff]', text):
            return "ja"
        # Korean
        elif re.search(r'[\ac00-\ud7af]', text):
            return "ko"
        # German
        elif re.search(r'[äöüß]', text):
            return "de"
        # French
        elif re.search(r'[éèêëàâôîïûùç]', text):
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
            import re
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return SemanticToken(
                    type=TokenType.ACTION,
                    value=match.group(),
                    canonical=canonical
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
            import re
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return SemanticToken(
                    type=TokenType.ENTITY,
                    value=match.group(),
                    canonical=canonical
                )
        return None
    
    def _extract_identifier(self, text: str, language: str) -> Optional[SemanticToken]:
        """Extract identifier token"""
        import re
        # Email pattern
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if email_match:
            return SemanticToken(
                type=TokenType.IDENTIFIER,
                value=email_match.group(),
                canonical=email_match.group()
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
```

**Acceptance Criteria**:

```python
# Test case
def test_semantic_tokenization():
    tokenizer = SemanticTokenizer()
    
    # Chinese input
    tokens_zh = tokenizer.tokenize("創建用戶 alice@example.com", language="zh")
    
    # English input (same semantics)
    tokens_en = tokenizer.tokenize("create user alice@example.com", language="en")
    
    # Semantic tokens must be the same
    assert [t.canonical for t in tokens_zh] == [t.canonical for t in tokens_en]
    # ['create', 'user', 'alice@example.com']
    
    # Can convert back to different language
    zh_output = tokenizer.detokenize(tokens_zh, "zh")
    en_output = tokenizer.detokenize(tokens_zh, "en")
    assert zh_output == "創建 用戶 alice@example.com"
    assert en_output == "create user alice@example.com"
```

**Status**: ⚠️ **Not Implemented** - This is the current biggest gap

---

[CONTINUE - This specification continues with all 5 layers...]