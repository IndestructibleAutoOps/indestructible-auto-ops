"""
Semantic Canonicalizer Tests
GL Level: GL50
Namespace: /tests/kernel/semantic
"""

import pytest
from governance.kernel.semantic.canonicalizer import SemanticCanonicalizer
from governance.kernel.semantic.tokenizer import SemanticTokenizer


class TestSemanticCanonicalizer:
    """語意正規化器測試"""

    def setup_method(self):
        """Setup test fixtures"""
        self.tokenizer = SemanticTokenizer()
        self.canonicalizer = SemanticCanonicalizer()

    def test_canonicalize_action(self):
        """測試動作正規化"""
        variants = ["創建", "建立", "新增", "create", "add"]

        canonicals = []
        for variant in variants:
            tokens = self.tokenizer.tokenize(variant)
            canonical = self.canonicalizer.canonicalize_tokens(tokens)
            canonicals.append(canonical)

        # All should produce the same canonical representation
        assert len(set(canonicals)) == 1

    def test_canonicalize_entity(self):
        """測試實體正規化"""
        variants = ["用戶", "使用者", "user"]

        canonicals = []
        for variant in variants:
            tokens = self.tokenizer.tokenize(variant)
            canonical = self.canonicalizer.canonicalize_tokens(tokens)
            canonicals.append(canonical)

        # All should produce the same canonical representation
        assert len(set(canonicals)) == 1

    def test_canonicalize_sentence(self):
        """測試句子正規化"""
        text_zh = "創建用戶 alice@example.com"
        text_en = "create user alice@example.com"

        canonical_zh = self.canonicalizer.canonicalize(text_zh)
        canonical_en = self.canonicalizer.canonicalize(text_en)

        # Should produce same canonical representation
        assert canonical_zh == canonical_en

    def test_canonical_format(self):
        """測試正規化格式"""
        text = "create user alice@example.com"
        canonical = self.canonicalizer.canonicalize(text)

        # Should be a structured representation
        assert isinstance(canonical, str)
        assert "action" in canonical.lower() or "canonical" in canonical.lower()

    def test_case_normalization(self):
        """測試大小寫正規化"""
        text1 = "CREATE USER ALICE"
        text2 = "create user alice"

        canonical1 = self.canonicalizer.canonicalize(text1)
        canonical2 = self.canonicalizer.canonicalize(text2)

        # Should produce same canonical (case normalized)
        assert canonical1 == canonical2

    def test_whitespace_normalization(self):
        """測試空白字元正規化"""
        text1 = "create user alice"
        text2 = "create   user    alice"

        canonical1 = self.canonicalizer.canonicalize(text1)
        canonical2 = self.canonicalizer.canonicalize(text2)

        # Should produce same canonical (whitespace normalized)
        assert canonical1 == canonical2

    def test_empty_input(self):
        """測試空輸入"""
        canonical = self.canonicalizer.canonicalize("")

        # Should still produce a canonical representation
        assert isinstance(canonical, str)

    def test_deterministic_canonicalization(self):
        """測試正規化確定性"""
        text = "create user alice@example.com"

        canonical1 = self.canonicalizer.canonicalize(text)
        canonical2 = self.canonicalizer.canonicalize(text)
        canonical3 = self.canonicalizer.canonicalize(text)

        # Should produce identical result every time
        assert canonical1 == canonical2 == canonical3
