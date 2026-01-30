"""GL Runtime V0 Pro - 本地原生平台"""
class NativePlatform:
    def __init__(self):
        self._services = {}
        self._initialized = False
    
    def initialize(self) -> bool:
        self._initialized = True
        return True
    
    def register_service(self, name: str, service) -> None:
        self._services[name] = service
    
    def get_status(self) -> dict:
        return {"initialized": self._initialized, "services": len(self._services)}
