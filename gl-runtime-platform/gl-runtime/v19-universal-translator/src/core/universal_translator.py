"""V19 Universal Translator - 通用翻譯器"""
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass

@dataclass
class TranslationRule:
    source_format: str
    target_format: str
    transformer: Callable

class UniversalTranslator:
    def __init__(self):
        self.rules: Dict[str, TranslationRule] = {}
        self.format_registry: Dict[str, Dict] = {}
        self.translation_cache: Dict[str, Any] = {}
    
    def register_format(self, name: str, schema: Dict):
        self.format_registry[name] = schema
    
    def add_rule(self, source: str, target: str, transformer: Callable):
        key = f"{source}->{target}"
        self.rules[key] = TranslationRule(source, target, transformer)
    
    def translate(self, data: Any, source_format: str, target_format: str) -> Any:
        cache_key = f"{hash(str(data))}:{source_format}->{target_format}"
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]
        
        direct_key = f"{source_format}->{target_format}"
        if direct_key in self.rules:
            result = self.rules[direct_key].transformer(data)
            self.translation_cache[cache_key] = result
            return result
        
        # Try to find path
        path = self._find_translation_path(source_format, target_format)
        if path:
            current = data
            for i in range(len(path) - 1):
                key = f"{path[i]}->{path[i+1]}"
                current = self.rules[key].transformer(current)
            self.translation_cache[cache_key] = current
            return current
        
        return None
    
    def _find_translation_path(self, source: str, target: str) -> Optional[List[str]]:
        visited = set()
        queue = [[source]]
        while queue:
            path = queue.pop(0)
            current = path[-1]
            if current == target:
                return path
            if current in visited:
                continue
            visited.add(current)
            for key in self.rules:
                src, tgt = key.split("->")
                if src == current and tgt not in visited:
                    queue.append(path + [tgt])
        return None
    
    def can_translate(self, source: str, target: str) -> bool:
        return self._find_translation_path(source, target) is not None
