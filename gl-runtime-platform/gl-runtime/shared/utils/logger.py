# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""GL Runtime Shared - Logger"""
import logging
from datetime import datetime

class GLLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(f"gl-runtime.{name}")
        self.logger.setLevel(logging.DEBUG)
    
    def info(self, msg: str) -> None:
        self.logger.info(f"[{datetime.utcnow().isoformat()}] {msg}")
    
    def error(self, msg: str) -> None:
        self.logger.error(f"[{datetime.utcnow().isoformat()}] {msg}")
    
    def audit(self, action: str, details: dict) -> None:
        self.logger.info(f"[AUDIT] {action}: {details}")
