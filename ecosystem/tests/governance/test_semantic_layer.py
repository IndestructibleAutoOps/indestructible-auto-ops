#!/usr/bin/env python3
"""
Test Suite for Semantic Layer - Language-Neutral Hashing

Tests the semantic layer's ability to:
1. Tokenize multi-language text correctly
2. Build semantic AST
3. Compute language-neutral hashes
4. Seal multi-language evidence
5. Canonicalize semantic expressions

Author: IndestructibleAutoOps
Version: 1.0
Date: 2024-02-05
"""

import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from governance.kernel.semantic import (
    SemanticTokenizer,
    SemanticAST,
    SemanticHasher,
    MultiLanguageEvidenceSealer,
    SemanticCanonicalizer,
    TokenType,
    NodeType
)


class TestSemanticTokenizer(unittest.TestCase):
    """Test semantic tokenizer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tokenizer = SemanticTokenizer()
    
    def test_tokenize_chinese(self):
        """Test tokenizing Chinese text"""
        text = "創建用戶 alice@example.com"
        tokens = self.tokenizer.tokenize(text, language="zh")
        
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenType.ACTION)
        self.assertEqual(tokens[0].canonical, "create")
        self.assertEqual(tokens[1].type, TokenType.ENTITY)
        self.assertEqual(tokens[1].canonical, "user")
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[2].canonical, "alice@example.com")
    
    def test_tokenize_english(self):
        """Test tokenizing English text"""
        text = "create user alice@example.com"
        tokens = self.tokenizer.tokenize(text, language="en")
        
        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].type, TokenType.ACTION)
        self.assertEqual(tokens[0].canonical, "create")
        self.assertEqual(tokens[1].type, TokenType.ENTITY)
        self.assertEqual(tokens[1].canonical, "user")
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[2].canonical, "alice@example.com")
    
    def test_cross_language_equivalence(self):
        """Test that same semantics produce same tokens"""
        zh_text = "創建用戶 alice@example.com"
        en_text = "create user alice@example.com"
        
        zh_tokens = self.tokenizer.tokenize(zh_text, language="zh")
        en_tokens = self.tokenizer.tokenize(en_text, language="en")
        
        # Canonical values must be the same
        zh_canonicals = [t.canonical for t in zh_tokens]
        en_canonicals = [t.canonical for t in en_tokens]
        
        self.assertEqual(zh_canonicals, en_canonicals)
        self.assertEqual(zh_canonicals, ["create", "user", "alice@example.com"])
    
    def test_detokenize_chinese(self):
        """Test detokenizing to Chinese"""
        from governance.kernel.semantic import SemanticToken
        
        tokens = [
            SemanticToken(type=TokenType.ACTION, value="create", canonical="create"),
            SemanticToken(type=TokenType.ENTITY, value="user", canonical="user"),
            SemanticToken(type=TokenType.IDENTIFIER, value="alice@example.com", canonical="alice@example.com")
        ]
        
        result = self.tokenizer.detokenize(tokens, "zh")
        self.assertIn("創建", result)
        self.assertIn("用戶", result)
        self.assertIn("alice@example.com", result)


class TestSemanticAST(unittest.TestCase):
    """Test semantic AST"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tokenizer = SemanticTokenizer()
        self.ast_builder = SemanticAST()
    
    def test_build_ast(self):
        """Test building AST from tokens"""
        text = "create user alice"
        tokens = self.tokenizer.tokenize(text, language="en")
        ast = self.ast_builder.build(tokens)
        
        self.assertIsNotNone(ast.root)
        self.assertEqual(ast.root.node_type, NodeType.SEQUENCE)
        self.assertEqual(len(ast.root.children), 3)
    
    def test_canonical_json(self):
        """Test canonical JSON generation"""
        text = "create user alice"
        tokens = self.tokenizer.tokenize(text, language="en")
        ast = self.ast_builder.build(tokens)
        
        canonical = ast.to_canonical_json()
        
        # Verify JSON is valid
        ast_dict = json.loads(canonical)
        self.assertEqual(ast_dict["node_type"], "sequence")
        
        # Verify deterministic (same input produces same output)
        canonical2 = ast.to_canonical_json()
        self.assertEqual(canonical, canonical2)
    
    def test_ast_hash(self):
        """Test AST hash computation"""
        text = "create user alice"
        tokens = self.tokenizer.tokenize(text, language="en")
        ast = self.ast_builder.build(tokens)
        
        hash_value = ast.hash()
        
        # Hash format: "sha256:..."
        self.assertTrue(hash_value.startswith("sha256:"))
        self.assertEqual(len(hash_value.split(":")[1]), 64)  # SHA256 is 64 hex chars


class TestSemanticHasher(unittest.TestCase):
    """Test semantic hasher"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.hasher = SemanticHasher()
    
    def test_language_neutral_hash(self):
        """Test that same semantics produce same hash"""
        zh_text = "創建用戶 alice@example.com"
        en_text = "create user alice@example.com"
        
        zh_hash = self.hasher.hash_text(zh_text, language="zh")
        en_hash = self.hasher.hash_text(en_text, language="en")
        
        # Hashes must be identical
        self.assertEqual(zh_hash, en_hash)
        print(f"\n✅ Language-Neutral Hash: {zh_hash}")
    
    def test_hash_from_different_phrasings(self):
        """Test that different phrasings produce different hashes"""
        text1 = "create user alice"
        text2 = "delete user alice"
        
        hash1 = self.hasher.hash_text(text1)
        hash2 = self.hasher.hash_text(text2)
        
        # Different semantics should produce different hashes
        self.assertNotEqual(hash1, hash2)
    
    def test_hash_determinism(self):
        """Test hash determinism"""
        text = "create user alice"
        
        hash1 = self.hasher.hash_text(text)
        hash2 = self.hasher.hash_text(text)
        
        # Same input must produce same hash
        self.assertEqual(hash1, hash2)


class TestMultiLanguageEvidence(unittest.TestCase):
    """Test multi-language evidence sealing"""
    
    def setUp(self):
        """Set up test fixtures"""
        import tempfile
        self.temp_dir = tempfile.mkdtemp()
        self.sealer = MultiLanguageEvidenceSealer(evidence_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_seal_multilang(self):
        """Test sealing multi-language expressions"""
        expressions = {
            "zh": "創建用戶 alice@example.com",
            "en": "create user alice@example.com"
        }
        
        result = self.sealer.seal_from_texts(expressions)
        
        self.assertIn("semantic_hash", result)
        self.assertIn("evidence_file", result)
        self.assertTrue(os.path.exists(result["evidence_file"]))
    
    def test_verify_multilang(self):
        """Test verifying multi-language expression"""
        expressions = {
            "zh": "創建用戶 alice@example.com",
            "en": "create user alice@example.com"
        }
        
        result = self.sealer.seal_from_texts(expressions)
        semantic_hash = result["semantic_hash"]
        
        # Verify Chinese expression
        is_valid_zh = self.sealer.verify_multilang(semantic_hash, expressions["zh"], "zh")
        self.assertTrue(is_valid_zh)
        
        # Verify English expression
        is_valid_en = self.sealer.verify_multilang(semantic_hash, expressions["en"], "en")
        self.assertTrue(is_valid_en)
    
    def test_load_evidence(self):
        """Test loading evidence"""
        expressions = {
            "zh": "創建用戶 alice@example.com",
            "en": "create user alice@example.com"
        }
        
        result = self.sealer.seal_from_texts(expressions)
        semantic_hash = result["semantic_hash"]
        
        # Load evidence
        evidence = self.sealer.load_evidence(semantic_hash)
        
        self.assertIsNotNone(evidence)
        self.assertEqual(evidence.semantic_hash, semantic_hash)
        self.assertEqual(len(evidence.expressions), 2)


class TestSemanticCanonicalizer(unittest.TestCase):
    """Test semantic canonicalizer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.canonicalizer = SemanticCanonicalizer()
    
    def test_canonicalize_chinese(self):
        """Test canonicalizing Chinese expressions"""
        text = "把用戶 alice 刪掉"
        canonical = self.canonicalizer.canonicalize(text, language="zh")
        
        # Should canonicalize to "delete user alice"
        self.assertIn("delete", canonical)
        self.assertIn("user", canonical)
        self.assertIn("alice", canonical)
    
    def test_canonicalize_english(self):
        """Test canonicalizing English expressions"""
        text = "remove the user named alice"
        canonical = self.canonicalizer.canonicalize(text, language="en")
        
        # Should canonicalize to "delete user alice"
        self.assertIn("delete", canonical)
        self.assertIn("user", canonical)
        self.assertIn("alice", canonical)
    
    def test_canonicalize_variants_to_same(self):
        """Test that variants canonicalize to same form"""
        variants = [
            "創建用戶 alice",
            "新增用戶 alice",
            "加入用戶 alice",
            "create user alice",
            "add user alice",
            "register user alice"
        ]
        
        canonical_forms = [self.canonicalizer.canonicalize(v) for v in variants]
        
        # All variants should canonicalize to same form
        unique_forms = set(canonical_forms)
        self.assertEqual(len(unique_forms), 1)
        self.assertIn("create", list(unique_forms)[0])


if __name__ == "__main__":
    unittest.main()