"""
GL Runtime V2 - 結構解析器
基礎結構理解模組
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class StructureNode:
    name: str
    node_type: str
    children: List['StructureNode']
    attributes: Dict[str, Any]


class StructureParser:
    """基礎結構解析器"""
    
    def __init__(self):
        self._root: Optional[StructureNode] = None
    
    def parse(self, data: Any) -> Optional[StructureNode]:
        """解析數據結構"""
        if isinstance(data, dict):
            return self._parse_dict(data, "root")
        elif isinstance(data, list):
            return self._parse_list(data, "root")
        return None
    
    def _parse_dict(self, data: dict, name: str) -> StructureNode:
        """解析字典結構"""
        children = []
        attributes = {}
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                children.append(self._parse_dict(value, key) if isinstance(value, dict) 
                              else self._parse_list(value, key))
            else:
                attributes[key] = value
        return StructureNode(name=name, node_type="dict", children=children, attributes=attributes)
    
    def _parse_list(self, data: list, name: str) -> StructureNode:
        """解析列表結構"""
        children = []
        for i, item in enumerate(data):
            if isinstance(item, dict):
                children.append(self._parse_dict(item, f"{name}[{i}]"))
        return StructureNode(name=name, node_type="list", children=children, attributes={"length": len(data)})
