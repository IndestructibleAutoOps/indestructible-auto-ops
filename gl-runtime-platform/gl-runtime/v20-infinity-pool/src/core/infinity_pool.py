"""V20 Infinity Pool - 無限資源池"""
from typing import Dict, List, Optional, Any, Generator
from dataclasses import dataclass
import time
from collections import deque

@dataclass
class PoolResource:
    id: str
    type: str
    data: Any
    created_at: float
    accessed_at: float
    priority: int = 0

class InfinityPool:
    def __init__(self, max_active: int = 1000):
        self.active: Dict[str, PoolResource] = {}
        self.archive: deque = deque(maxlen=10000)
        self.max_active = max_active
        self.generators: Dict[str, Generator] = {}
        self.statistics: Dict[str, int] = {"created": 0, "accessed": 0, "archived": 0}
    
    def add_resource(self, rid: str, rtype: str, data: Any, priority: int = 0) -> PoolResource:
        now = time.time()
        resource = PoolResource(rid, rtype, data, now, now, priority)
        
        if len(self.active) >= self.max_active:
            self._archive_lowest_priority()
        
        self.active[rid] = resource
        self.statistics["created"] += 1
        return resource
    
    def get_resource(self, rid: str) -> Optional[PoolResource]:
        if rid in self.active:
            self.active[rid].accessed_at = time.time()
            self.statistics["accessed"] += 1
            return self.active[rid]
        return None
    
    def register_generator(self, name: str, gen: Generator):
        self.generators[name] = gen
    
    def generate_on_demand(self, generator_name: str) -> Optional[Any]:
        if generator_name in self.generators:
            try:
                return next(self.generators[generator_name])
            except StopIteration:
                return None
        return None
    
    def _archive_lowest_priority(self):
        if not self.active: return
        lowest = min(self.active.values(), key=lambda r: (r.priority, r.accessed_at))
        self.archive.append(lowest)
        del self.active[lowest.id]
        self.statistics["archived"] += 1
    
    def query_by_type(self, rtype: str) -> List[PoolResource]:
        return [r for r in self.active.values() if r.type == rtype]
    
    def get_statistics(self) -> Dict:
        return {
            **self.statistics,
            "active_count": len(self.active),
            "archive_count": len(self.archive)
        }
