"""GL Runtime Shared - Governance Interface"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class IGovernance(ABC):
    @abstractmethod
    def audit(self, evidence: Dict[str, Any]) -> bool: pass
    
    @abstractmethod
    def enforce(self, rule: str, target: Any) -> bool: pass

class IFalsifiable(ABC):
    @abstractmethod
    def falsify(self, hypothesis: str) -> bool: pass
    
    @abstractmethod
    def get_evidence(self) -> List[Dict[str, Any]]: pass
