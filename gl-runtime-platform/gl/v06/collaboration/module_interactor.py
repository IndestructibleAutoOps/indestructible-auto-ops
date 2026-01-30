"""GL Runtime V6 - 模組交互器"""
from typing import Any, Dict

class ModuleInteractor:
    def __init__(self):
        self._modules: Dict[str, Any] = {}
    
    def register_module(self, name: str, module: Any) -> None:
        self._modules[name] = module
    
    def interact(self, source: str, target: str, message: Any) -> Any:
        return {"from": source, "to": target, "message": message}
