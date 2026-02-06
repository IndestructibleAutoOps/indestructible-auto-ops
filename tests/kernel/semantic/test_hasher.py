"""
Semantic Hasher Tests
GL Level: GL50
Namespace: /tests/kernel/semantic
"""

import pytest
from governance.kernel.semantic.hasher import SemanticHasher
from governance.kernel.semantic.tokenizer import SemanticTokenizer


class TestSemanticHasher:
    """語意 Hasher 測試"""

    def setup_method(self):
        """Setup test fixtures"""
        self.tokenizer = SemanticTokenizer()
        self.hasher = SemanticHasher()

    def test_same_semantic_produces_same_hash(self):
        """測試相同語意產生相同 hash（語言中立性）"""
        text_zh = "創建用戶 alice@example.com"
        text_en = "create user alice@example.com"

        hash_zh = self.hasher.hash(text_zh)
        hash_en = self.hasher.hash(text_en)

        # Same semantic should produce same hash
        assert hash_zh == hash_en

    def test_different_semantic_produces_different_hash(self):
        """測試不同語意產生不同 hash"""
        text1 = "create user alice@example.com"
        text2 = "delete user alice@example.com"

        hash1 = self.hasher.hash(text1)
        hash2 = self.hasher.hash(text2)

        # Different semantic should produce different hash
        assert hash1 != hash2

    def test_hash_format(self):
        """測試 hash 格式"""
        text = "create user alice@example.com"
        hash_value = self.hasher.hash(text)

        # Should be a hex string
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64  # SHA256 produces 64 hex characters
        assert all(c in "0123456789abcdef" for c in hash_value.lower())

    def test_case_insensitivity(self):
        """測試大小寫不敏感性"""
        text1 = "create user alice@example.com"
        text2 = "CREATE USER ALICE@EXAMPLE.COM"

        hash1 = self.hasher.hash(text1)
        hash2 = self.hasher.hash(text2)

        # Should produce same hash (case-insensitive)
        assert hash1 == hash2

    def test_empty_string_hash(self):
        """測試空字串 hash"""
        hash_value = self.hasher.hash("")

        # Should still produce a valid hash
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64

    def test_whitespace_normalization(self):
        """測試空白字元正規化"""
        text1 = "create user alice"
        text2 = "create   user    alice"
        text3 = "create user alice   "

        hash1 = self.hasher.hash(text1)
        hash2 = self.hasher.hash(text2)
        hash3 = self.hasher.hash(text3)

        # Should produce same hash (whitespace normalized)
        assert hash1 == hash2 == hash3

    def test_hash_with_tokens(self):
        """測試使用 tokens 產生 hash"""
        text = "create user alice@example.com"
        tokens = self.tokenizer.tokenize(text)

        hash_with_text = self.hasher.hash(text)
        hash_with_tokens = self.hasher.hash_tokens(tokens)

        # Should produce same hash
        assert hash_with_text == hash_with_tokens

    def test_hash_deterministic(self):
        """測試 hash 確定性（多次計算產生相同結果）"""
        text = "create user alice@example.com"

        hash1 = self.hasher.hash(text)
        hash2 = self.hasher.hash(text)
        hash3 = self.hasher.hash(text)

        # Should produce identical hash every time
        assert hash1 == hash2 == hash3

    def test_complex_sentence_hash(self):
        """測試複雜句子 hash"""
        text_zh = "如果用戶存在則創建訂單否則更新用戶"
        text_en = "if user exists then create order else update user"

        hash_zh = self.hasher.hash(text_zh)
        hash_en = self.hasher.hash(text_en)

        # Same semantic logic should produce same hash
        assert hash_zh == hash_en
