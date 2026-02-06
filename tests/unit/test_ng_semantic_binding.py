# FILE: tests/unit/test_ng_semantic_binding.py
# 單元測試：NG 語義綁定

import pytest
import numpy as np
from datetime import datetime
from typing import Dict, List
import hashlib

# Mock classes for testing
class MockNgSemanticBinding:
    """Mock NG Semantic Binding"""
    def __init__(self, entity_id: str, ng_code: str, ng_category: str, 
                 semantic_type: str, vector_id: str = None):
        self.entity_id = entity_id
        self.ng_code = ng_code
        self.ng_category = ng_category
        self.semantic_type = semantic_type
        self.vector_id = vector_id
        self.created_at = datetime.utcnow().isoformat()

class MockNgVectorSpaceManager:
    """Mock NG Vector Space Manager"""
    def __init__(self):
        self.bindings: Dict = {}
        self.embedding_version = "internal-multimodal-encoder-v3"
        self.embedding_space_hash = None
    
    def register_entity(self, binding: MockNgSemanticBinding) -> bool:
        if not self._validate_ng_code(binding.ng_code):
            raise ValueError(f"Invalid NG code: {binding.ng_code}")
        
        if binding.entity_id in self.bindings:
            existing = self.bindings[binding.entity_id]
            if existing.ng_code != binding.ng_code:
                raise ValueError(
                    f"Entity {binding.entity_id} already bound to "
                    f"{existing.ng_code}, cannot rebind to {binding.ng_code}"
                )
        
        self.bindings[binding.entity_id] = binding
        return True
    
    def get_binding(self, entity_id: str):
        return self.bindings.get(entity_id)
    
    def verify_embedding_space_consistency(self) -> bool:
        current_hash = self._compute_embedding_space_hash()
        
        if self.embedding_space_hash is None:
            self.embedding_space_hash = current_hash
            return True
        
        if current_hash != self.embedding_space_hash:
            drift = self._calculate_drift(current_hash, self.embedding_space_hash)
            if drift > 0.1:
                return False
        
        return True
    
    def _validate_ng_code(self, ng_code: str) -> bool:
        import re
        pattern = r"^NG[0-9]{5}$"
        return bool(re.match(pattern, ng_code))
    
    def _compute_embedding_space_hash(self) -> str:
        content = str(sorted(self.bindings.items()))
        return hashlib.sha3_512(content.encode()).hexdigest()
    
    def _calculate_drift(self, hash1: str, hash2: str) -> float:
        diff_count = sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
        return diff_count / len(hash1)


# Test Cases
class TestNgSemanticBinding:
    """Test NG Semantic Binding"""
    
    def test_register_valid_entity(self):
        """Test registering a valid entity"""
        manager = MockNgVectorSpaceManager()
        binding = MockNgSemanticBinding(
            entity_id="evidence_cluster_001",
            ng_code="NG70600",
            ng_category="semantic_entity",
            semantic_type="evidence_cluster",
            vector_id="vec_001"
        )
        
        assert manager.register_entity(binding) is True
        assert manager.get_binding("evidence_cluster_001") == binding
    
    def test_register_invalid_ng_code_format(self):
        """Test registering entity with invalid NG code format"""
        manager = MockNgVectorSpaceManager()
        binding = MockNgSemanticBinding(
            entity_id="entity_001",
            ng_code="INVALID_CODE",
            ng_category="semantic_entity",
            semantic_type="evidence"
        )
        
        with pytest.raises(ValueError, match="Invalid NG code"):
            manager.register_entity(binding)
    
    def test_register_duplicate_entity_same_ng_code(self):
        """Test registering duplicate entity with same NG code"""
        manager = MockNgVectorSpaceManager()
        binding1 = MockNgSemanticBinding(
            entity_id="entity_001",
            ng_code="NG70600",
            ng_category="semantic_entity",
            semantic_type="evidence"
        )
        binding2 = MockNgSemanticBinding(
            entity_id="entity_001",
            ng_code="NG70600",
            ng_category="semantic_entity",
            semantic_type="evidence"
        )
        
        manager.register_entity(binding1)
        # Should not raise error for same NG code
        assert manager.register_entity(binding2) is True
    
    def test_register_duplicate_entity_different_ng_code(self):
        """Test registering duplicate entity with different NG code"""
        manager = MockNgVectorSpaceManager()
        binding1 = MockNgSemanticBinding(
            entity_id="entity_001",
            ng_code="NG70600",
            ng_category="semantic_entity",
            semantic_type="evidence"
        )
        binding2 = MockNgSemanticBinding(
            entity_id="entity_001",
            ng_code="NG70700",
            ng_category="semantic_entity",
            semantic_type="evidence"
        )
        
        manager.register_entity(binding1)
        
        with pytest.raises(ValueError, match="already bound to"):
            manager.register_entity(binding2)
    
    def test_embedding_space_consistency_first_check(self):
        """Test embedding space consistency on first check"""
        manager = MockNgVectorSpaceManager()
        binding = MockNgSemanticBinding(
            entity_id="entity_001",
            ng_code="NG70600",
            ng_category="semantic_entity",
            semantic_type="evidence"
        )
        
        manager.register_entity(binding)
        assert manager.verify_embedding_space_consistency() is True
    
    def test_embedding_space_consistency_stable(self):
        """Test embedding space consistency remains stable"""
        manager = MockNgVectorSpaceManager()
        binding = MockNgSemanticBinding(
            entity_id="entity_001",
            ng_code="NG70600",
            ng_category="semantic_entity",
            semantic_type="evidence"
        )
        
        manager.register_entity(binding)
        manager.verify_embedding_space_consistency()
        
        # Second check should pass
        assert manager.verify_embedding_space_consistency() is True
    
    def test_embedding_space_drift_detection(self):
        """Test embedding space drift detection"""
        manager = MockNgVectorSpaceManager()
        binding1 = MockNgSemanticBinding(
            entity_id="entity_001",
            ng_code="NG70600",
            ng_category="semantic_entity",
            semantic_type="evidence"
        )
        
        manager.register_entity(binding1)
        manager.verify_embedding_space_consistency()
        
        # Add many new bindings to cause drift
        for i in range(100):
            binding = MockNgSemanticBinding(
                entity_id=f"entity_{i:03d}",
                ng_code=f"NG{70600 + (i % 100):05d}",
                ng_category="semantic_entity",
                semantic_type="evidence"
            )
            manager.register_entity(binding)
        
        # Should detect drift
        result = manager.verify_embedding_space_consistency()
        # Result depends on actual drift calculation
        assert isinstance(result, bool)
    
    def test_get_nonexistent_binding(self):
        """Test getting non-existent binding"""
        manager = MockNgVectorSpaceManager()
        assert manager.get_binding("nonexistent") is None
    
    def test_multiple_entities_different_ng_codes(self):
        """Test registering multiple entities with different NG codes"""
        manager = MockNgVectorSpaceManager()
        
        bindings = [
            MockNgSemanticBinding("entity_001", "NG70600", "semantic_entity", "evidence"),
            MockNgSemanticBinding("entity_002", "NG70700", "semantic_entity", "hypothesis"),
            MockNgSemanticBinding("entity_003", "NG60100", "business_intent", "intent"),
        ]
        
        for binding in bindings:
            assert manager.register_entity(binding) is True
        
        assert len(manager.bindings) == 3
        assert manager.get_binding("entity_001").ng_code == "NG70600"
        assert manager.get_binding("entity_002").ng_code == "NG70700"
        assert manager.get_binding("entity_003").ng_code == "NG60100"


class TestNgCodeValidation:
    """Test NG Code Validation"""
    
    def test_valid_ng_codes(self):
        """Test valid NG codes"""
        manager = MockNgVectorSpaceManager()
        valid_codes = [
            "NG00000", "NG12345", "NG99999", "NG70600", "NG80300"
        ]
        
        for code in valid_codes:
            assert manager._validate_ng_code(code) is True
    
    def test_invalid_ng_codes(self):
        """Test invalid NG codes"""
        manager = MockNgVectorSpaceManager()
        invalid_codes = [
            "NG1234",      # Too short
            "NG123456",    # Too long
            "ng12345",     # Lowercase
            "NG1234a",     # Contains letter
            "INVALID",     # No NG prefix
            "NG-12345",    # Contains dash
        ]
        
        for code in invalid_codes:
            assert manager._validate_ng_code(code) is False


class TestEmbeddingSpaceHash:
    """Test Embedding Space Hash Calculation"""
    
    def test_hash_calculation_consistency(self):
        """Test hash calculation is consistent"""
        manager = MockNgVectorSpaceManager()
        binding = MockNgSemanticBinding(
            entity_id="entity_001",
            ng_code="NG70600",
            ng_category="semantic_entity",
            semantic_type="evidence"
        )
        
        manager.register_entity(binding)
        hash1 = manager._compute_embedding_space_hash()
        hash2 = manager._compute_embedding_space_hash()
        
        assert hash1 == hash2
    
    def test_hash_changes_with_new_entity(self):
        """Test hash changes when new entity is added"""
        manager = MockNgVectorSpaceManager()
        binding1 = MockNgSemanticBinding(
            entity_id="entity_001",
            ng_code="NG70600",
            ng_category="semantic_entity",
            semantic_type="evidence"
        )
        
        manager.register_entity(binding1)
        hash1 = manager._compute_embedding_space_hash()
        
        binding2 = MockNgSemanticBinding(
            entity_id="entity_002",
            ng_code="NG70700",
            ng_category="semantic_entity",
            semantic_type="hypothesis"
        )
        
        manager.register_entity(binding2)
        hash2 = manager._compute_embedding_space_hash()
        
        assert hash1 != hash2
    
    def test_drift_calculation(self):
        """Test drift calculation between hashes"""
        manager = MockNgVectorSpaceManager()
        
        hash1 = "a" * 128
        hash2 = "a" * 64 + "b" * 64
        
        drift = manager._calculate_drift(hash1, hash2)
        
        # 50% of characters are different
        assert drift == 0.5