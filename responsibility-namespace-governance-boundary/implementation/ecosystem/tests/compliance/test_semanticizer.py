#!/usr/bin/env python3
"""
Test Suite for Semanticizer - Language-Neutral Semantic Tokenization

Tests the semanticizer's ability to:
1. Detect language correctly
2. Extract semantic tokens from multi-language input
3. Generate consistent semantic tokens for same semantics
4. Create language maps for cross-language sealing

Author: IndestructibleAutoOps
Version: 1.0
Date: 2024-02-05
"""

import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from tools.semanticizer import (
    Semanticizer,
    SemanticTokenAST,
    Language,
    SemanticAction,
    SemanticResult,
)


class TestSemanticizer(unittest.TestCase):
    """Test cases for Semanticizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.semanticizer = Semanticizer()

    def test_language_detection_chinese(self):
        """Test language detection for Chinese"""
        text = "我們重新啟動了 nginx"
        lang = self.semanticizer.detect_language(text)
        self.assertEqual(lang, Language.ZH)

    def test_language_detection_english(self):
        """Test language detection for English"""
        text = "We restarted nginx"
        lang = self.semanticizer.detect_language(text)
        self.assertEqual(lang, Language.EN)

    def test_language_detection_japanese(self):
        """Test language detection for Japanese"""
        text = "nginx を再起動しました"
        lang = self.semanticizer.detect_language(text)
        self.assertEqual(lang, Language.JA)

    def test_language_detection_korean(self):
        """Test language detection for Korean"""
        text = "nginx 를 재시작했습니다"
        lang = self.semanticizer.detect_language(text)
        self.assertEqual(lang, Language.KO)

    def test_semanticize_chinese(self):
        """Test semanticizing Chinese text"""
        text = "我們重新啟動了 nginx"
        ast = self.semanticizer.semanticize(text, lang="zh")

        self.assertEqual(ast.action, "restart_service")
        self.assertEqual(ast.target, "nginx")
        self.assertEqual(ast.result, "success")
        self.assertEqual(ast.metadata["original_lang"], "zh")
        self.assertEqual(ast.metadata["original_text"], text)

    def test_semanticize_english(self):
        """Test semanticizing English text"""
        text = "We restarted nginx"
        ast = self.semanticizer.semanticize(text, lang="en")

        self.assertEqual(ast.action, "restart_service")
        self.assertEqual(ast.target, "nginx")
        self.assertEqual(ast.result, "success")
        self.assertEqual(ast.metadata["original_lang"], "en")

    def test_semanticize_auto_detect(self):
        """Test semanticizing with auto language detection"""
        text = "我們重新啟動了 nginx"
        ast = self.semanticizer.semanticize(text)

        self.assertEqual(ast.action, "restart_service")
        self.assertEqual(ast.target, "nginx")
        self.assertEqual(ast.metadata["detected_lang"], "zh")

    def test_cross_language_semantic_equivalence(self):
        """Test that same semantics produce consistent tokens"""
        zh_text = "我們重新啟動了 nginx"
        en_text = "We restarted nginx"

        zh_ast = self.semanticizer.semanticize(zh_text, lang="zh")
        en_ast = self.semanticizer.semanticize(en_text, lang="en")

        # Core semantic fields should be the same
        self.assertEqual(zh_ast.action, en_ast.action)
        self.assertEqual(zh_ast.target, en_ast.target)

    def test_extract_result_success(self):
        """Test result extraction for success"""
        text = "我們成功修復了 nginx"
        result = self.semanticizer.extract_result(text, Language.ZH)

        self.assertEqual(result, SemanticResult.SUCCESS)

    def test_extract_result_failure(self):
        """Test result extraction for failure"""
        text = "修復失敗"
        result = self.semanticizer.extract_result(text, Language.ZH)

        self.assertEqual(result, SemanticResult.FAILURE)

    def test_create_language_map(self):
        """Test language map creation"""
        text_zh = "我們重新啟動了 nginx"
        ast = self.semanticizer.semanticize(text_zh, lang="zh")

        translations = {
            "zh": text_zh,
            "en": "We restarted nginx",
            "ja": "nginx を再起動しました",
        }

        lang_map = self.semanticizer.create_language_map(ast, translations)

        self.assertIn("semantic_tokens", lang_map)
        self.assertIn("languages", lang_map)
        self.assertEqual(lang_map["languages"]["zh"]["text"], text_zh)
        self.assertEqual(lang_map["languages"]["en"]["text"], translations["en"])

    def test_semantic_token_to_json(self):
        """Test converting semantic token to JSON"""
        text = "我們重新啟動了 nginx"
        ast = self.semanticizer.semanticize(text, lang="zh")

        json_str = ast.to_json()
        json_obj = json.loads(json_str)

        self.assertEqual(json_obj["action"], "restart_service")
        self.assertEqual(json_obj["target"], "nginx")

    def test_semantic_token_to_dict(self):
        """Test converting semantic token to dictionary"""
        text = "我們重新啟動了 nginx"
        ast = self.semanticizer.semanticize(text, lang="zh")

        obj = ast.to_dict()

        self.assertIsInstance(obj, dict)
        self.assertEqual(obj["action"], "restart_service")
        self.assertEqual(obj["target"], "nginx")


class TestCrossLanguageHash(unittest.TestCase):
    """Test cross-language hash consistency"""

    def setUp(self):
        """Set up test fixtures"""
        from tools.canonicalizer import Canonicalizer

        self.semanticizer = Semanticizer()
        self.canonicalizer = Canonicalizer()

    def test_cross_language_hash_consistency(self):
        """Test that same semantics produce same hash"""
        zh_text = "我們重新啟動了 nginx"
        en_text = "We restarted nginx"

        zh_ast = self.semanticizer.semanticize(zh_text, lang="zh")
        en_ast = self.semanticizer.semanticize(en_text, lang="en")

        # Canonicalize and hash
        zh_canonical, zh_hash = self.canonicalizer.canonicalize_and_hash(
            zh_ast.to_dict()
        )
        en_canonical, en_hash = self.canonicalizer.canonicalize_and_hash(
            en_ast.to_dict()
        )

        # Hashes should be the same for same semantics
        self.assertEqual(zh_hash, en_hash)

    def test_language_neutral_hash(self):
        """Test that hash is language-neutral"""
        texts = {
            "zh": "我們重新啟動了 nginx",
            "en": "We restarted nginx",
            "ja": "nginx を再起動しました",
        }

        hashes = []
        for lang, text in texts.items():
            ast = self.semanticizer.semanticize(text, lang=lang)
            _, hash_value = self.canonicalizer.canonicalize_and_hash(ast.to_dict())
            hashes.append(hash_value)

        # All hashes should be identical
        self.assertEqual(len(set(hashes)), 1)


if __name__ == "__main__":
    unittest.main()
