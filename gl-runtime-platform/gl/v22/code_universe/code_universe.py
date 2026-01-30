"""GL Runtime V22 - 程式宇宙"""
class CodeUniverse:
    def __init__(self):
        self._codebase = {}
    
    def index(self, name: str, code: str) -> None:
        self._codebase[name] = code
    
    def search(self, query: str) -> list:
        return [k for k in self._codebase if query in k]
