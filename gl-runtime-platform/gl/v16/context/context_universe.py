"""GL Runtime V16 - 上下文宇宙"""
class ContextUniverse:
    def __init__(self):
        self._contexts = {}
    
    def create_context(self, name: str, data: dict) -> str:
        self._contexts[name] = data
        return name
    
    def merge_contexts(self, names: list) -> dict:
        merged = {}
        for name in names:
            merged.update(self._contexts.get(name, {}))
        return merged
