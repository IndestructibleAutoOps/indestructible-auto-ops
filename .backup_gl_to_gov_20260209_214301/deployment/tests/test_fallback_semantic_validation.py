"""
测试故障回退语义验证
"""
import pytest
import numpy as np
from typing import Dict, List, Tuple


class FallbackSemanticValidator:
    """故障回退的语义验证"""
    
    def __init__(self, intent_embedding_model):
        self.intent_model = intent_embedding_model
        self.intent_threshold = 0.95
        self.safety_threshold = 0.95
    
    def validate_fallback_decision(
        self,
        original_intent: str,
        fallback_decision: Dict,
        safety_constraints: List
    ) -> Tuple[bool, Dict]:
        """验证回退决策"""
        validation_results = {
            "intent_preserved": False,
            "safety_preserved": False,
            "semantic_anchor_preserved": False,
            "overall_valid": False
        }
        
        # 1. 验证意图保留
        intent_preserved = self._verify_intent_preservation(
            original_intent,
            fallback_decision
        )
        validation_results["intent_preserved"] = intent_preserved
        
        # 2. 验证安全约束
        safety_preserved = self._verify_safety_constraints(
            fallback_decision,
            safety_constraints
        )
        validation_results["safety_preserved"] = safety_preserved
        
        # 3. 验证语义锚点
        anchor_preserved = self._verify_semantic_anchor(
            original_intent,
            fallback_decision
        )
        validation_results["semantic_anchor_preserved"] = anchor_preserved
        
        # 整体验证
        validation_results["overall_valid"] = (
            intent_preserved and
            safety_preserved and
            anchor_preserved
        )
        
        return validation_results["overall_valid"], validation_results
    
    def _verify_intent_preservation(
        self,
        original_intent: str,
        fallback_decision: Dict
    ) -> bool:
        """验证意图保留"""
        original_embedding = self.intent_model.embed(original_intent)
        fallback_embedding = self.intent_model.embed(
            str(fallback_decision)
        )
        
        similarity = np.dot(original_embedding, fallback_embedding) / (
            np.linalg.norm(original_embedding) *
            np.linalg.norm(fallback_embedding)
        )
        
        return similarity > self.intent_threshold
    
    def _verify_safety_constraints(
        self,
        fallback_decision: Dict,
        constraints: List
    ) -> bool:
        """验证安全约束"""
        for constraint in constraints:
            if not constraint(fallback_decision):
                return False
        
        return True
    
    def _verify_semantic_anchor(
        self,
        original_intent: str,
        fallback_decision: Dict
    ) -> float:
        """验证语义锚点"""
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
        """提取实体"""
        import re
        ng_codes = re.findall(r"NG\d{5}", text)
        return ng_codes


# ============ 测试用例 ============

class MockEmbeddingModel:
    """模拟意图嵌入模型"""
    def __init__(self, similarity=0.97):
        self.similarity = similarity
    
    def embed(self, text):
        # 返回归一化向量
        vec = np.random.randn(512)
        return vec / np.linalg.norm(vec)


def test_fallback_semantic_validation():
    """测试故障回退语义验证"""
    validator = FallbackSemanticValidator(MockEmbeddingModel())
    
    original_intent = "maximize-quantum-fidelity NG60100"
    fallback_decision = {"action": "use_basic_algorithm", "ng_code": "NG60100"}
    
    safety_constraints = [
        lambda d: "action" in d,
        lambda d: d["action"] != "invalid"
    ]
    
    is_valid, results = validator.validate_fallback_decision(
        original_intent,
        fallback_decision,
        safety_constraints
    )
    
    assert results["safety_preserved"]
    assert results["overall_valid"]


def test_intent_preservation_failure():
    """测试意图保留失败"""
    validator = FallbackSemanticValidator(MockEmbeddingModel())
    
    original_intent = "maximize-quantum-fidelity NG60100"
    fallback_decision = {"action": "totally_different_action"}
    
    safety_constraints = [lambda d: True]
    
    is_valid, results = validator.validate_fallback_decision(
        original_intent,
        fallback_decision,
        safety_constraints
    )
    
    assert not results["intent_preserved"]
    assert not results["overall_valid"]


def test_safety_constraint_failure():
    """测试安全约束失败"""
    validator = FallbackSemanticValidator(MockEmbeddingModel())
    
    original_intent = "maximize-quantum-fidelity NG60100"
    fallback_decision = {"action": "invalid"}
    
    safety_constraints = [
        lambda d: d["action"] != "invalid"
    ]
    
    is_valid, results = validator.validate_fallback_decision(
        original_intent,
        fallback_decision,
        safety_constraints
    )
    
    assert not results["safety_preserved"]
    assert not results["overall_valid"]


def test_semantic_anchor_preservation():
    """测试语义锚点保留"""
    validator = FallbackSemanticValidator(MockEmbeddingModel())
    
    original_intent = "optimize NG60100 and NG70200"
    fallback_decision = {
        "action": "use_basic_algorithm",
        "ng_codes": ["NG60100", "NG70200"]
    }
    
    safety_constraints = [lambda d: True]
    
    is_valid, results = validator.validate_fallback_decision(
        original_intent,
        fallback_decision,
        safety_constraints
    )
    
    assert results["semantic_anchor_preserved"]


def test_semantic_anchor_missing():
    """测试语义锚点缺失"""
    validator = FallbackSemanticValidator(MockEmbeddingModel())
    
    original_intent = "optimize NG60100 and NG70200"
    fallback_decision = {"action": "use_basic_algorithm"}
    
    safety_constraints = [lambda d: True]
    
    is_valid, results = validator.validate_fallback_decision(
        original_intent,
        fallback_decision,
        safety_constraints
    )
    
    assert not results["semantic_anchor_preserved"]


def test_entity_extraction():
    """测试实体提取"""
    validator = FallbackSemanticValidator(MockEmbeddingModel())
    
    text = "This involves NG60100, NG70200, and NG80300"
    entities = validator._extract_entities(text)
    
    assert "NG60100" in entities
    assert "NG70200" in entities
    assert "NG80300" in entities
    assert len(entities) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=.", "--cov-report=html"])