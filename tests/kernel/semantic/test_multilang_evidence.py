"""
Multi-Language Evidence Tests
GL Level: GL50
Namespace: /tests/kernel/semantic
"""

import pytest
from governance.kernel.semantic.multilang_evidence import MultiLanguageEvidence
from governance.kernel.semantic.tokenizer import SemanticTokenizer


class TestMultiLanguageEvidence:
    """多語言證據測試"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.tokenizer = SemanticTokenizer()
        self.evidence = MultiLanguageEvidence()
    
    def test_create_evidence_pair(self):
        """測試創建多語言證據對"""
        text_zh = "創建用戶 alice@example.com"
        text_en = "create user alice@example.com"
        
        evidence_pair = self.evidence.create_evidence_pair(
            text_zh=text_zh,
            text_en=text_en
        )
        
        assert evidence_pair is not None
        assert "zh" in evidence_pair
        assert "en" in evidence_pair
        assert "semantic_hash" in evidence_pair
    
    def test_evidence_consistency(self):
        """測試證據一致性（相同語意產生相同 hash）"""
        text_zh = "創建用戶 alice@example.com"
        text_en = "create user alice@example.com"
        
        evidence = self.evidence.create_evidence_pair(
            text_zh=text_zh,
            text_en=text_en
        )
        
        # Same semantic hash for both languages
        assert evidence["zh"]["semantic_hash"] == evidence["en"]["semantic_hash"]
    
    def test_evidence_serialization(self):
        """測試證據序列化"""
        text_zh = "創建用戶 alice@example.com"
        text_en = "create user alice@example.com"
        
        evidence = self.evidence.create_evidence_pair(
            text_zh=text_zh,
            text_en=text_en
        )
        
        # Should be serializable to JSON
        import json
        try:
            json_str = json.dumps(evidence)
            assert json_str is not None
        except Exception as e:
            pytest.fail(f"Failed to serialize evidence: {e}")
    
    def test_evidence_integrity(self):
        """測試證據完整性"""
        text_zh = "創建用戶 alice@example.com"
        text_en = "create user alice@example.com"
        
        evidence = self.evidence.create_evidence_pair(
            text_zh=text_zh,
            text_en=text_en
        )
        
        # Should have all required fields
        assert "zh" in evidence
        assert "en" in evidence
        assert "semantic_hash" in evidence
        assert "timestamp" in evidence
        assert "evidence_id" in evidence
    
    def test_multiple_languages(self):
        """測試多種語言證據"""
        texts = {
            "zh": "創建用戶 alice@example.com",
            "en": "create user alice@example.com",
            # 可以添加更多語言
        }
        
        evidence = self.evidence.create_multi_language_evidence(texts)
        
        assert evidence is not None
        assert len(evidence["translations"]) == len(texts)
    
    def test_evidence_from_tokens(self):
        """測試從 tokens 創建證據"""
        text_zh = "創建用戶 alice@example.com"
        text_en = "create user alice@example.com"
        
        tokens_zh = self.tokenizer.tokenize(text_zh)
        tokens_en = self.tokenizer.tokenize(text_en)
        
        evidence = self.evidence.create_evidence_from_tokens(
            tokens_zh=tokens_zh,
            tokens_en=tokens_en
        )
        
        assert evidence is not None
        assert "semantic_hash" in evidence
        assert "tokens" in evidence
    
    def test_evidence_reconstruction(self):
        """測試證據重建"""
        text_zh = "創建用戶 alice@example.com"
        text_en = "create user alice@example.com"
        
        evidence = self.evidence.create_evidence_pair(
            text_zh=text_zh,
            text_en=text_en
        )
        
        # Should be able to reconstruct from evidence
        reconstructed = self.evidence.reconstruct_from_evidence(evidence)
        
        assert reconstructed is not None
        assert "zh" in reconstructed
        assert "en" in reconstructed
    
    def test_evidence_hash_consistency(self):
        """測試證據 hash 一致性"""
        text_zh = "創建用戶 alice@example.com"
        text_en = "create user alice@example.com"
        
        evidence1 = self.evidence.create_evidence_pair(
            text_zh=text_zh,
            text_en=text_en
        )
        
        evidence2 = self.evidence.create_evidence_pair(
            text_zh=text_zh,
            text_en=text_en
        )
        
        # Same input should produce same evidence hash
        assert evidence1["semantic_hash"] == evidence2["semantic_hash"]
    
    def test_evidence_uniqueness(self):
        """測試證據唯一性（不同語意產生不同 hash）"""
        text1_zh = "創建用戶 alice@example.com"
        text1_en = "create user alice@example.com"
        
        text2_zh = "刪除用戶 alice@example.com"
        text2_en = "delete user alice@example.com"
        
        evidence1 = self.evidence.create_evidence_pair(
            text_zh=text1_zh,
            text_en=text1_en
        )
        
        evidence2 = self.evidence.create_evidence_pair(
            text_zh=text2_zh,
            text_en=text2_en
        )
        
        # Different semantic should produce different hash
        assert evidence1["semantic_hash"] != evidence2["semantic_hash"]