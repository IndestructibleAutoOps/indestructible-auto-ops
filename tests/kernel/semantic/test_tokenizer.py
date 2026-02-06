"""
Semantic Tokenizer Tests
GL Level: GL50
Namespace: /tests/kernel/semantic
"""

import pytest
from governance.kernel.semantic.tokenizer import (
    SemanticTokenizer,
    SemanticToken,
    TokenType,
)


class TestSemanticTokenizer:
    """語意 Tokenizer 測試"""

    def setup_method(self):
        """Setup test fixtures"""
        self.tokenizer = SemanticTokenizer()

    def test_basic_tokenization_chinese(self):
        """測試基礎中文 tokenization"""
        text = "創建用戶 alice@example.com"
        tokens = self.tokenizer.tokenize(text)

        assert len(tokens) >= 3

        # Check action token
        action_token = next((t for t in tokens if t.type == TokenType.ACTION), None)
        assert action_token is not None
        assert action_token.canonical == "create"

        # Check entity token
        entity_token = next((t for t in tokens if t.type == TokenType.ENTITY), None)
        assert entity_token is not None
        assert entity_token.canonical == "user"

        # Check identifier token
        identifier_token = next(
            (t for t in tokens if t.type == TokenType.IDENTIFIER), None
        )
        assert identifier_token is not None
        assert "alice@example.com" in identifier_token.value.lower()

    def test_basic_tokenization_english(self):
        """測試基礎英文 tokenization"""
        text = "create user alice@example.com"
        tokens = self.tokenizer.tokenize(text)

        assert len(tokens) >= 3

        # Check action token
        action_token = next((t for t in tokens if t.type == TokenType.ACTION), None)
        assert action_token is not None
        assert action_token.canonical == "create"

        # Check entity token
        entity_token = next((t for t in tokens if t.type == TokenType.ENTITY), None)
        assert entity_token is not None
        assert entity_token.canonical == "user"

    def test_language_neutrality(self):
        """測試語言中立性（相同語意產生相同 canonical）"""
        text_zh = "創建用戶 alice@example.com"
        text_en = "create user alice@example.com"

        tokens_zh = self.tokenizer.tokenize(text_zh)
        tokens_en = self.tokenizer.tokenize(text_en)

        # Extract canonical tokens
        canonical_zh = [t.canonical for t in tokens_zh]
        canonical_en = [t.canonical for t in tokens_en]

        # Canonical tokens should be the same
        assert canonical_zh == canonical_en
        assert "create" in canonical_zh
        assert "user" in canonical_zh

    def test_detokenization_chinese(self):
        """測試反向 tokenization（中文）"""
        text_en = "create user alice@example.com"
        tokens = self.tokenizer.tokenize(text_en)

        # Convert to Chinese
        text_zh = self.tokenizer.detokenize(tokens, target_language="zh")

        # Should contain Chinese words
        assert "創建" in text_zh or "建立" in text_zh
        assert "用戶" in text_zh or "使用者" in text_zh

    def test_detokenization_english(self):
        """測試反向 tokenization（英文）"""
        text_zh = "創建用戶 alice@example.com"
        tokens = self.tokenizer.tokenize(text_zh)

        # Convert to English
        text_en = self.tokenizer.detokenize(tokens, target_language="en")

        # Should contain English words
        assert "create" in text_en.lower()
        assert "user" in text_en.lower()

    def test_multiple_actions(self):
        """測試多個動作"""
        text_zh = "創建用戶 alice 然後 刪除用戶 bob"
        tokens = self.tokenizer.tokenize(text_zh)

        actions = [t for t in tokens if t.type == TokenType.ACTION]
        assert len(actions) >= 2

        canonicals = [a.canonical for a in actions]
        assert "create" in canonicals
        assert "delete" in canonicals

    def test_empty_input(self):
        """測試空輸入"""
        tokens = self.tokenizer.tokenize("")
        assert tokens == []

    def test_whitespace_only(self):
        """測試只有空白字元的輸入"""
        tokens = self.tokenizer.tokenize("   \t\n  ")
        assert tokens == []

    def test_email_identification(self):
        """測試 Email 識別"""
        text = "create user alice@example.com"
        tokens = self.tokenizer.tokenize(text)

        email_token = next(
            (t for t in tokens if t.type == TokenType.IDENTIFIER and "@" in t.value),
            None,
        )
        assert email_token is not None
        assert "alice@example.com" in email_token.value.lower()

    def test_url_identification(self):
        """測試 URL 識別"""
        text = "create service https://api.example.com"
        tokens = self.tokenizer.tokenize(text)

        url_token = next(
            (t for t in tokens if t.type == TokenType.IDENTIFIER and "http" in t.value),
            None,
        )
        assert url_token is not None
        assert "api.example.com" in url_token.value.lower()

    def test_numeric_value(self):
        """測試數字值"""
        text = "create service nginx replicas 3"
        tokens = self.tokenizer.tokenize(text)

        value_tokens = [t for t in tokens if t.type == TokenType.VALUE]
        assert len(value_tokens) >= 1
        assert "3" in [t.value for t in value_tokens]

    def test_condition_extraction(self):
        """測試條件提取"""
        text = "如果用戶存在則創建"
        tokens = self.tokenizer.tokenize(text)

        condition_token = next(
            (t for t in tokens if t.type == TokenType.CONDITION), None
        )
        assert condition_token is not None
        assert condition_token.canonical == "if"


class TestSemanticToken:
    """SemanticToken 測試"""

    def test_to_dict(self):
        """測試轉換為字典"""
        token = SemanticToken(
            type=TokenType.ACTION,
            value="創建",
            canonical="create",
            metadata={"language": "zh"},
        )

        token_dict = token.to_dict()

        assert token_dict["type"] == TokenType.ACTION
        assert token_dict["value"] == "創建"
        assert token_dict["canonical"] == "create"
        assert token_dict["metadata"]["language"] == "zh"

    def test_from_dict(self):
        """測試從字典創建"""
        token_dict = {
            "type": "ACTION",
            "value": "創建",
            "canonical": "create",
            "metadata": {"language": "zh"},
        }

        token = SemanticToken.from_dict(token_dict)

        assert token.type == TokenType.ACTION
        assert token.value == "創建"
        assert token.canonical == "create"
        assert token.metadata["language"] == "zh"
