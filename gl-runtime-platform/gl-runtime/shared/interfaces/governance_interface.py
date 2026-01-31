# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: gl_platform_universegl_platform_universe.governance-core
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL90_99-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


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
