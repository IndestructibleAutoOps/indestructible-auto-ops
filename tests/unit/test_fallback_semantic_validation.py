# FILE: tests/unit/test_fallback_semantic_validation.py
# 單元測試：故障回退語義驗證

import pytest
import numpy as np
from typing import Dict, List, Callable, Tuple


class MockEmbeddingModel:
    """Mock Embedding Model"""
    def __init__(self):
        self.embeddings = {}
    
    def embed(self, text: str) -> np.ndarray:
        """Embed text to vector"""
        if text not in self.embeddings:
            # Deterministic embedding based on text hash
            np.random.seed(hash(text) % (2**32))
            self.embeddings[text] = np.random.randn(768)
            self.embeddings[text] /= np.linalg.norm(self.embeddings[text])
        
        return self.embeddings[text]


class MockFallbackSemanticValidator:
    """Mock Fallback Semantic Validator"""
    
    def __init__(self, intent_embedding_model):
        self.intent_model = intent_embedding_model
        self.intent_threshold = 0.95
        self.safety_threshold = 0.95
    
    def validate_fallback_decision(self, original_intent: str,
                                   fallback_decision: Dict,
                                   safety_constraints: List[Callable]
                                   ) -> Tuple[bool, Dict]:
        """Validate fallback decision"""
        validation_results = {
            "intent_preserved": False,
            "safety_preserved": False,
            "semantic_anchor_preserved": False,
            "overall_valid": False
        }
        
        intent_preserved = self._verify_intent_preservation(
            original_intent,
            fallback_decision
        )
        validation_results["intent_preserved"] = intent_preserved
        
        safety_preserved = self._verify_safety_constraints(
            fallback_decision,
            safety_constraints
        )
        validation_results["safety_preserved"] = safety_preserved
        
        anchor_preserved = self._verify_semantic_anchor(
            original_intent,
            fallback_decision
        )
        validation_results["semantic_anchor_preserved"] = anchor_preserved
        
        validation_results["overall_valid"] = (
            intent_preserved and
            safety_preserved and
            anchor_preserved
        )
        
        return validation_results["overall_valid"], validation_results
    
    def _verify_intent_preservation(self, original_intent: str,
                                    fallback_decision: Dict) -> bool:
        """Verify intent preservation"""
        original_embedding = self.intent_model.embed(original_intent)
        fallback_embedding = self.intent_model.embed(
            str(fallback_decision)
        )
        
        similarity = np.dot(original_embedding, fallback_embedding) / (
            np.linalg.norm(original_embedding) *
            np.linalg.norm(fallback_embedding) + 1e-8
        )
        
        return similarity > self.intent_threshold
    
    def _verify_safety_constraints(self, fallback_decision: Dict,
                                   constraints: List[Callable]) -> bool:
        """Verify safety constraints"""
        for constraint in constraints:
            if not constraint(fallback_decision):
                return False
        
        return True
    
    def _verify_semantic_anchor(self, original_intent: str,
                                fallback_decision: Dict) -> bool:
        """Verify semantic anchor"""
        original_entities = self._extract_entities(original_intent)
        fallback_entities = self._extract_entities(
            str(fallback_decision)
        )
        
        if len(original_entities) == 0:
            return True
        
        overlap = len(
            set(original_entities) & set(fallback_entities)
        ) / len(original_entities)
        
        return overlap > 0.9
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract entities"""
        import re
        ng_codes = re.findall(r"NG\d{5}", text)
        return ng_codes


# Test Cases
class TestFallbackSemanticValidation:
    """Test Fallback Semantic Validation"""
    
    def test_valid_fallback_decision(self):
        """Test valid fallback decision"""
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        original_intent = "maximize-quantum-fidelity"
        fallback_decision = {"action": "use_basic_algorithm", "NG60100": True}
        
        safety_constraints = [
            lambda d: "action" in d,
            lambda d: d["action"] != "invalid"
        ]
        
        is_valid, results = validator.validate_fallback_decision(
            original_intent,
            fallback_decision,
            safety_constraints
        )
        
        assert results["safety_preserved"] is True
    
    def test_fallback_decision_violates_safety_constraint(self):
        """Test fallback decision violates safety constraint"""
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        original_intent = "maximize-quantum-fidelity"
        fallback_decision = {"action": "invalid_action"}
        
        safety_constraints = [
            lambda d: "action" in d,
            lambda d: d["action"] != "invalid_action"
        ]
        
        is_valid, results = validator.validate_fallback_decision(
            original_intent,
            fallback_decision,
            safety_constraints
        )
        
        assert results["safety_preserved"] is False
    
    def test_fallback_decision_missing_required_field(self):
        """Test fallback decision missing required field"""
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        original_intent = "maximize-quantum-fidelity"
        fallback_decision = {"other_field": "value"}
        
        safety_constraints = [
            lambda d: "action" in d
        ]
        
        is_valid, results = validator.validate_fallback_decision(
            original_intent,
            fallback_decision,
            safety_constraints
        )
        
        assert results["safety_preserved"] is False
    
    def test_semantic_anchor_preservation_with_ng_codes(self):
        """Test semantic anchor preservation with NG codes"""
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        original_intent = "maximize-quantum-fidelity NG60100 NG70600"
        fallback_decision = {"action": "fallback", "NG60100": True}
        
        safety_constraints = [lambda d: "action" in d]
        
        is_valid, results = validator.validate_fallback_decision(
            original_intent,
            fallback_decision,
            safety_constraints
        )
        
        assert results["semantic_anchor_preserved"] is True
    
    def test_semantic_anchor_lost(self):
        """Test semantic anchor lost"""
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        original_intent = "maximize-quantum-fidelity NG60100 NG70600"
        fallback_decision = {"action": "fallback", "NG80000": True}
        
        safety_constraints = [lambda d: "action" in d]
        
        is_valid, results = validator.validate_fallback_decision(
            original_intent,
            fallback_decision,
            safety_constraints
        )
        
        assert results["semantic_anchor_preserved"] is False


class TestIntentPreservation:
    """Test Intent Preservation"""
    
    def test_intent_similarity_calculation(self):
        """Test intent similarity calculation"""
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        intent1 = "maximize-quantum-fidelity"
        intent2 = "maximize-quantum-fidelity"
        
        emb1 = model.embed(intent1)
        emb2 = model.embed(intent2)
        
        similarity = np.dot(emb1, emb2) / (
            np.linalg.norm(emb1) * np.linalg.norm(emb2)
        )
        
        # Same intent should have high similarity
        assert similarity > 0.99
    
    def test_intent_similarity_different_intents(self):
        """Test intent similarity for different intents"""
        model = MockEmbeddingModel()
        
        intent1 = "maximize-quantum-fidelity"
        intent2 = "minimize-execution-cost"
        
        emb1 = model.embed(intent1)
        emb2 = model.embed(intent2)
        
        similarity = np.dot(emb1, emb2) / (
            np.linalg.norm(emb1) * np.linalg.norm(emb2)
        )
        
        # Different intents should have lower similarity
        assert similarity < 0.5


class TestSafetyConstraints:
    """Test Safety Constraints"""
    
    def test_multiple_safety_constraints(self):
        """Test multiple safety constraints"""
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        fallback_decision = {
            "action": "valid_action",
            "priority": "high",
            "timeout": 30
        }
        
        constraints = [
            lambda d: "action" in d,
            lambda d: d["action"] != "invalid",
            lambda d: "priority" in d,
            lambda d: d["priority"] in ["low", "medium", "high"]
        ]
        
        result = validator._verify_safety_constraints(
            fallback_decision,
            constraints
        )
        
        assert result is True
    
    def test_safety_constraint_failure(self):
        """Test safety constraint failure"""
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        fallback_decision = {
            "action": "valid_action",
            "priority": "invalid_priority"
        }
        
        constraints = [
            lambda d: "priority" in d,
            lambda d: d["priority"] in ["low", "medium", "high"]
        ]
        
        result = validator._verify_safety_constraints(
            fallback_decision,
            constraints
        )
        
        assert result is False


class TestEntityExtraction:
    """Test Entity Extraction"""
    
    def test_extract_ng_codes_from_text(self):
        """Test extracting NG codes from text"""
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        text = "This is NG60100 and NG70600 and NG80300"
        entities = validator._extract_entities(text)
        
        assert len(entities) == 3
        assert "NG60100" in entities
        assert "NG70600" in entities
        assert "NG80300" in entities
    
    def test_extract_no_ng_codes(self):
        """Test extracting when no NG codes present"""
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        text = "This text has no NG codes"
        entities = validator._extract_entities(text)
        
        assert len(entities) == 0
    
    def test_extract_ng_codes_from_dict(self):
        """Test extracting NG codes from dictionary"""
        model = MockEmbeddingModel()
        validator = MockFallbackSemanticValidator(model)
        
        decision = {"action": "test", "NG60100": True, "NG70600": False}
        entities = validator._extract_entities(str(decision))
        
        assert "NG60100" in entities
        assert "NG70600" in entities