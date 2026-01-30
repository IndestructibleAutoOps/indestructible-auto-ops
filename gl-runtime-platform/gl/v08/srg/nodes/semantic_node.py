# GL Runtime V8 - Semantic Resource Graph: Nodes
# @GL-governed
# @GL-layer: V08-semantic
# @GL-semantic: srg-node-core
# @GL-dependencies: V2, V7

"""
GL Runtime V8: 語義資源圖 - 節點模組
核心功能: 語義節點定義、節點類型、節點操作
治理需求: V2 分析、V7 DAG 執行
"""

from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid
import hashlib


class NodeType(Enum):
    CONCEPT = "concept"
    ENTITY = "entity"
    ACTION = "action"
    PROPERTY = "property"
    RELATION = "relation"
    CONTEXT = "context"
    INTENT = "intent"
    CONSTRAINT = "constraint"


class NodeStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DEPRECATED = "deprecated"


@dataclass
class SemanticMetadata:
    """語義元數據"""
    semantic_type: str
    confidence: float = 1.0
    source: str = "system"
    tags: Set[str] = field(default_factory=set)
    annotations: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SemanticNode:
    """GL V8 語義節點"""
    node_id: str
    node_type: NodeType
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
    metadata: Optional[SemanticMetadata] = None
    status: NodeStatus = NodeStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1
    
    # 語義特性
    embeddings: Optional[List[float]] = None
    semantic_hash: Optional[str] = None
    
    def __post_init__(self):
        if self.semantic_hash is None:
            self.semantic_hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """計算語義哈希"""
        content = f"{self.node_type.value}:{self.label}:{sorted(self.properties.items())}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def update(self, properties: Dict[str, Any]) -> None:
        """更新節點屬性"""
        self.properties.update(properties)
        self.updated_at = datetime.utcnow()
        self.version += 1
        self.semantic_hash = self._compute_hash()
    
    def add_tag(self, tag: str) -> None:
        if self.metadata:
            self.metadata.tags.add(tag)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "label": self.label,
            "properties": self.properties,
            "status": self.status.value,
            "semantic_hash": self.semantic_hash,
            "version": self.version
        }


class SemanticNodeFactory:
    """語義節點工廠"""
    
    @staticmethod
    def create(
        node_type: NodeType,
        label: str,
        properties: Optional[Dict[str, Any]] = None,
        semantic_type: str = "default",
        confidence: float = 1.0
    ) -> SemanticNode:
        return SemanticNode(
            node_id=str(uuid.uuid4()),
            node_type=node_type,
            label=label,
            properties=properties or {},
            metadata=SemanticMetadata(
                semantic_type=semantic_type,
                confidence=confidence
            )
        )
    
    @staticmethod
    def create_concept(label: str, definition: str, **kwargs) -> SemanticNode:
        return SemanticNodeFactory.create(
            NodeType.CONCEPT,
            label,
            {"definition": definition, **kwargs},
            semantic_type="concept"
        )
    
    @staticmethod
    def create_entity(label: str, entity_type: str, **kwargs) -> SemanticNode:
        return SemanticNodeFactory.create(
            NodeType.ENTITY,
            label,
            {"entity_type": entity_type, **kwargs},
            semantic_type="entity"
        )
    
    @staticmethod
    def create_action(label: str, parameters: List[str], **kwargs) -> SemanticNode:
        return SemanticNodeFactory.create(
            NodeType.ACTION,
            label,
            {"parameters": parameters, **kwargs},
            semantic_type="action"
        )


class SemanticNodeStore:
    """語義節點存儲 - 記憶體內部"""
    
    def __init__(self):
        self._nodes: Dict[str, SemanticNode] = {}
        self._index_by_type: Dict[NodeType, Set[str]] = {}
        self._index_by_label: Dict[str, Set[str]] = {}
    
    def add(self, node: SemanticNode) -> None:
        """添加節點"""
        self._nodes[node.node_id] = node
        
        # 更新索引
        if node.node_type not in self._index_by_type:
            self._index_by_type[node.node_type] = set()
        self._index_by_type[node.node_type].add(node.node_id)
        
        if node.label not in self._index_by_label:
            self._index_by_label[node.label] = set()
        self._index_by_label[node.label].add(node.node_id)
    
    def get(self, node_id: str) -> Optional[SemanticNode]:
        return self._nodes.get(node_id)
    
    def find_by_type(self, node_type: NodeType) -> List[SemanticNode]:
        ids = self._index_by_type.get(node_type, set())
        return [self._nodes[nid] for nid in ids if nid in self._nodes]
    
    def find_by_label(self, label: str) -> List[SemanticNode]:
        ids = self._index_by_label.get(label, set())
        return [self._nodes[nid] for nid in ids if nid in self._nodes]
    
    def remove(self, node_id: str) -> bool:
        if node_id in self._nodes:
            node = self._nodes[node_id]
            del self._nodes[node_id]
            
            # 清理索引
            if node.node_type in self._index_by_type:
                self._index_by_type[node.node_type].discard(node_id)
            if node.label in self._index_by_label:
                self._index_by_label[node.label].discard(node_id)
            
            return True
        return False
    
    def cleanup(self) -> None:
        """零殘留清理"""
        self._nodes.clear()
        self._index_by_type.clear()
        self._index_by_label.clear()
    
    def count(self) -> int:
        return len(self._nodes)
