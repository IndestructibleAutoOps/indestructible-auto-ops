"""
测试 NG 语义绑定层
"""
import pytest
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional
import hashlib
from datetime import datetime


@dataclass
class NgSemanticBinding:
    """NG 语义绑定"""
    entity_id: str
    ng_code: str
    ng_category: str
    semantic_type: str
    vector_id: Optional[str] = None
    metadata: Dict = None
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()


class NgVectorSpaceManager:
    """NG 向量空间管理器"""
    
    def __init__(self):
        self.bindings: Dict[str, NgSemanticBinding] = {}
        self.embedding_version = "internal-multimodal-encoder-v3"
        self.embedding_space_hash = None
    
    def register_entity(self, binding: NgSemanticBinding) -> bool:
        """注册实体与 NG 编码的绑定"""
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
    
    def get_binding(self, entity_id: str) -> Optional[NgSemanticBinding]:
        """获取实体的 NG 绑定"""
        return self.bindings.get(entity_id)
    
    def verify_embedding_space_consistency(self) -> bool:
        """验证嵌入空间一致性"""
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
        """验证 NG 编码格式"""
        import re
        pattern = r"^NG[0-9]{5}$"
        return bool(re.match(pattern, ng_code))
    
    def _compute_embedding_space_hash(self) -> str:
        """计算嵌入空间哈希"""
        content = str(sorted(self.bindings.items()))
        return hashlib.sha3_512(content.encode()).hexdigest()
    
    def _calculate_drift(self, hash1: str, hash2: str) -> float:
        """计算哈希漂移"""
        diff_count = sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
        return diff_count / len(hash1)


# ============ 测试用例 ============

def test_ng_semantic_binding():
    """测试 NG 语义绑定"""
    manager = NgVectorSpaceManager()
    
    # 注册实体
    binding = NgSemanticBinding(
        entity_id="evidence_cluster_001",
        ng_code="NG70600",
        ng_category="semantic_entity",
        semantic_type="evidence_cluster",
        vector_id="vec_001"
    )
    
    assert manager.register_entity(binding)
    assert manager.get_binding("evidence_cluster_001") == binding
    
    # 验证嵌入空间一致性
    assert manager.verify_embedding_space_consistency()


def test_ng_binding_conflict_detection():
    """测试 NG 绑定冲突检测"""
    manager = NgVectorSpaceManager()
    
    binding1 = NgSemanticBinding(
        entity_id="entity_001",
        ng_code="NG70600",
        ng_category="semantic_entity",
        semantic_type="evidence"
    )
    
    binding2 = NgSemanticBinding(
        entity_id="entity_001",
        ng_code="NG70700",  # 不同的 NG 编码
        ng_category="semantic_entity",
        semantic_type="evidence"
    )
    
    manager.register_entity(binding1)
    
    # 应该抛出异常
    with pytest.raises(ValueError):
        manager.register_entity(binding2)


def test_invalid_ng_code():
    """测试无效 NG 编码"""
    manager = NgVectorSpaceManager()
    
    binding = NgSemanticBinding(
        entity_id="entity_001",
        ng_code="INVALID_CODE",  # 无效格式
        ng_category="semantic_entity",
        semantic_type="evidence"
    )
    
    with pytest.raises(ValueError):
        manager.register_entity(binding)


def test_embedding_space_drift_detection():
    """测试嵌入空间漂移检测"""
    manager = NgVectorSpaceManager()
    
    # 注册初始绑定
    binding = NgSemanticBinding(
        entity_id="entity_001",
        ng_code="NG70600",
        ng_category="semantic_entity",
        semantic_type="evidence"
    )
    manager.register_entity(binding)
    
    # 初始验证应该通过
    assert manager.verify_embedding_space_consistency()
    
    # 添加新绑定（模拟漂移）
    new_binding = NgSemanticBinding(
        entity_id="entity_002",
        ng_code="NG70700",
        ng_category="semantic_entity",
        semantic_type="evidence"
    )
    manager.register_entity(new_binding)
    
    # 验证仍然应该通过（漂移小）
    assert manager.verify_embedding_space_consistency()


def test_get_nonexistent_binding():
    """测试获取不存在的绑定"""
    manager = NgVectorSpaceManager()
    
    binding = manager.get_binding("nonexistent")
    assert binding is None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=.", "--cov-report=html"])