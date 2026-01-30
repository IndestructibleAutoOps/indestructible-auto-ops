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
