"""
GL Runtime V2 - 語義分析器
基礎語義分析模組
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SemanticToken:
    value: str
    token_type: str
    metadata: Dict[str, Any]


class SemanticAnalyzer:
    """基礎語義分析器"""
    
    def __init__(self):
        self._tokens: List[SemanticToken] = []
    
    def analyze(self, content: Any) -> List[SemanticToken]:
        """執行語義分析"""
        if isinstance(content, str):
            return self._analyze_text(content)
        elif isinstance(content, dict):
            return self._analyze_structure(content)
        return []
    
    def _analyze_text(self, text: str) -> List[SemanticToken]:
        """文本語義分析"""
        tokens = []
        for word in text.split():
            tokens.append(SemanticToken(
                value=word,
                token_type="text",
                metadata={"length": len(word)}
            ))
        return tokens
    
    def _analyze_structure(self, data: dict) -> List[SemanticToken]:
        """結構語義分析"""
        tokens = []
        for key, value in data.items():
            tokens.append(SemanticToken(
                value=str(value),
                token_type="structure",
                metadata={"key": key, "type": type(value).__name__}
            ))
        return tokens
