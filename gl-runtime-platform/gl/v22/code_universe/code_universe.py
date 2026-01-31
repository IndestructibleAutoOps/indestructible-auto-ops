# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""GL Runtime V22 - 程式宇宙"""
class CodeUniverse:
    def __init__(self):
        self._codebase = {}
    
    def index(self, name: str, code: str) -> None:
        self._codebase[name] = code
    
    def search(self, query: str) -> list:
        return [k for k in self._codebase if query in k]
