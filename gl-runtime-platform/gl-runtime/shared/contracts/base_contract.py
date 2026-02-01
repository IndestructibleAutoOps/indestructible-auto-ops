# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


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
