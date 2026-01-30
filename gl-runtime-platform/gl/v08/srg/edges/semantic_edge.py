"""GL Runtime V8 - 語義邊"""
from typing import Any, Dict
from dataclasses import dataclass

@dataclass
class SemanticEdge:
    source: str
    target: str
    relation: str
    weight: float = 1.0
    metadata: Dict[str, Any] = None
