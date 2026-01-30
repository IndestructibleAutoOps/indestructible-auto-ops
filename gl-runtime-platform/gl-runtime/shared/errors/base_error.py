"""GL Runtime Shared - Base Error"""
from typing import Any, Dict, Optional

class GLError(Exception):
    def __init__(self, code: str, message: str, details: Optional[Dict[str, Any]] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(f"[{code}] {message}")
    
    def to_dict(self) -> Dict[str, Any]:
        return {"code": self.code, "message": self.message, "details": self.details}

class TaskError(GLError): pass
class StateError(GLError): pass
class GovernanceError(GLError): pass
