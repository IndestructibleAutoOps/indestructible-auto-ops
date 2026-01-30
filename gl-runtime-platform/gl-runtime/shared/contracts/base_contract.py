"""基礎合約定義"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseContract(ABC):
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def enforce(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass
