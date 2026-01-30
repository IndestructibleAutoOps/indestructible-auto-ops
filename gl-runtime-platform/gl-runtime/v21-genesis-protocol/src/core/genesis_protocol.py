"""V21 Genesis Protocol - 創世協議"""
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import time
import uuid

@dataclass
class GenesisBlueprint:
    id: str
    name: str
    parameters: Dict[str, Any]
    constraints: List[Dict]
    creation_rules: List[Callable]

@dataclass
class GenesisEntity:
    id: str
    blueprint_id: str
    state: Dict[str, Any]
    born_at: float
    lineage: List[str] = field(default_factory=list)

class GenesisProtocol:
    def __init__(self):
        self.blueprints: Dict[str, GenesisBlueprint] = {}
        self.entities: Dict[str, GenesisEntity] = {}
        self.creation_log: List[Dict] = []
    
    def define_blueprint(self, name: str, parameters: Dict, 
                        constraints: List[Dict] = None) -> GenesisBlueprint:
        bp_id = f"bp_{uuid.uuid4().hex[:8]}"
        blueprint = GenesisBlueprint(bp_id, name, parameters, constraints or [], [])
        self.blueprints[bp_id] = blueprint
        return blueprint
    
    def add_creation_rule(self, blueprint_id: str, rule: Callable):
        if blueprint_id in self.blueprints:
            self.blueprints[blueprint_id].creation_rules.append(rule)
    
    def create_entity(self, blueprint_id: str, overrides: Dict = None, 
                     parent_id: str = None) -> Optional[GenesisEntity]:
        if blueprint_id not in self.blueprints:
            return None
        
        blueprint = self.blueprints[blueprint_id]
        
        # Check constraints
        params = {**blueprint.parameters, **(overrides or {})}
        for constraint in blueprint.constraints:
            if not self._check_constraint(constraint, params):
                return None
        
        # Apply creation rules
        state = params.copy()
        for rule in blueprint.creation_rules:
            state = rule(state)
        
        # Create entity
        entity_id = f"entity_{uuid.uuid4().hex[:8]}"
        lineage = []
        if parent_id and parent_id in self.entities:
            lineage = self.entities[parent_id].lineage + [parent_id]
        
        entity = GenesisEntity(entity_id, blueprint_id, state, time.time(), lineage)
        self.entities[entity_id] = entity
        self.creation_log.append({
            "entity_id": entity_id, "blueprint": blueprint.name,
            "parent": parent_id, "timestamp": time.time()
        })
        return entity
    
    def _check_constraint(self, constraint: Dict, params: Dict) -> bool:
        ctype = constraint.get("type", "range")
        key = constraint.get("key")
        if key not in params:
            return True
        value = params[key]
        if ctype == "range":
            return constraint.get("min", float("-inf")) <= value <= constraint.get("max", float("inf"))
        elif ctype == "enum":
            return value in constraint.get("values", [])
        return True
    
    def get_lineage(self, entity_id: str) -> List[GenesisEntity]:
        if entity_id not in self.entities:
            return []
        return [self.entities[eid] for eid in self.entities[entity_id].lineage 
                if eid in self.entities]
