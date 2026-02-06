"""
GL Semantic Closure Engine
Implements semantic closure validation across L00-L99 governance layers

Based on Research:
- TOGAF Architecture Continuum for layer transitions
- Zachman Framework 6x6 semantic matrix
- Netflix steady state validation principles
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json

# Removed dependencies on ecosystem.core for standalone operation
# These will be integrated with existing GL components when available


@dataclass
class SemanticEntity:
    """Represents a semantic entity in a governance layer"""

    layer: str
    entity_id: str
    entity_type: str
    definition: Dict
    dependencies: List[str]
    metadata: Dict

    def get_hash(self) -> str:
        """Compute semantic entity hash"""
        entity_data = {
            "layer": self.layer,
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "definition": self.definition,
            "dependencies": sorted(self.dependencies),
        }
        return hashlib.sha256(
            json.dumps(entity_data, sort_keys=True).encode()
        ).hexdigest()


@dataclass
class ValidationResult:
    """Represents validation result"""

    is_valid: bool
    closure_score: float
    violations: List[str]
    warnings: List[str]
    validated_at: datetime
    layer: str

    def add_violation(self, message: str):
        """Add violation to result"""
        self.violations.append(message)
        self.is_valid = False

    def add_warning(self, message: str):
        """Add warning to result"""
        self.warnings.append(message)


class GLSemanticClosureEngine:
    """
    GL Semantic Closure Engine
    Validates semantic closure across governance layers L00-L99
    """

    def __init__(self, semantic_graph=None):
        self.semantic_graph = semantic_graph  # Optional for future integration
        self.closure_matrix: Dict[str, Dict[str, SemanticEntity]] = {}
        self.closure_status: Dict[str, float] = {}
        self.drift_history: List[Dict] = []

    def define_semantic_entity(self, entity: SemanticEntity) -> ValidationResult:
        """
        Define semantic entity in governance layer
        Validates semantic closure before accepting definition
        """
        result = ValidationResult(
            is_valid=True,
            closure_score=0.0,
            violations=[],
            warnings=[],
            validated_at=datetime.now(),
            layer=entity.layer,
        )

        # Check if entity already exists
        entity_key = f"{entity.layer}:{entity.entity_id}"
        if entity_key in self.closure_matrix.get(entity.layer, {}):
            result.add_warning(
                f"Entity {entity.entity_id} already exists in layer {entity.layer}"
            )

        # Verify semantic closure
        closure_check = self._verify_closure(entity)
        if not closure_check["is_closed"]:
            result.add_violation(
                f"Entity {entity.entity_id} violates semantic closure: {closure_check['reason']}"
            )

        # Check dependency validity
        dep_check = self._verify_dependencies(entity)
        if not dep_check["valid"]:
            result.add_violation(f"Invalid dependencies: {dep_check['reason']}")

        # If valid, add to closure matrix
        if result.is_valid:
            if entity.layer not in self.closure_matrix:
                self.closure_matrix[entity.layer] = {}
            self.closure_matrix[entity.layer][entity.entity_id] = entity
            self._update_closure_status(entity.layer)

        return result

    def validate_layer(self, layer: str) -> ValidationResult:
        """
        Validate semantic closure for entire governance layer
        Returns True if layer achieves complete semantic closure
        """
        result = ValidationResult(
            is_valid=True,
            closure_score=0.0,
            violations=[],
            warnings=[],
            validated_at=datetime.now(),
            layer=layer,
        )

        # Check if layer exists
        if layer not in self.closure_matrix:
            result.add_violation(f"Layer {layer} has no defined entities")
            return result

        # Validate each entity
        entities = self.closure_matrix[layer]
        for entity_id, entity in entities.items():
            entity_check = self._verify_closure(entity)
            if not entity_check["is_closed"]:
                result.add_violation(
                    f"Entity {entity_id} not closed: {entity_check['reason']}"
                )

        # Check for orphaned references
        orphaned = self._find_orphaned_references(layer)
        if orphaned:
            result.add_violation(f"Orphaned references found: {orphaned}")

        # Check for circular dependencies
        circular = self._find_circular_dependencies(layer)
        if circular:
            result.add_violation(f"Circular dependencies detected: {circular}")

        # Check for semantic conflicts
        conflicts = self._find_semantic_conflicts(layer)
        if conflicts:
            result.add_warning(f"Semantic conflicts found: {conflicts}")

        # Compute closure score
        result.closure_score = self._compute_closure_score(layer)

        return result

    def validate_layer_transition(
        self, from_layer: str, to_layer: str
    ) -> ValidationResult:
        """
        Validate semantic closure during layer transition
        Ensures no semantic violations when moving between layers
        """
        result = ValidationResult(
            is_valid=True,
            closure_score=0.0,
            violations=[],
            warnings=[],
            validated_at=datetime.now(),
            layer=f"{from_layer}→{to_layer}",
        )

        # Validate from layer
        from_check = self.validate_layer(from_layer)
        if not from_check.is_valid:
            result.add_violation(
                f"From layer {from_layer} not valid: {from_check.violations}"
            )

        # Validate to layer
        to_check = self.validate_layer(to_layer)
        if not to_check.is_valid:
            result.add_violation(
                f"To layer {to_layer} not valid: {to_check.violations}"
            )

        # Check if to_layer references only from_layer or lower
        violations = self._check_layer_dependencies(from_layer, to_layer)
        for violation in violations:
            result.add_violation(violation)

        # Check semantic consistency
        if not self._check_semantic_consistency(from_layer, to_layer):
            result.add_violation("Semantic inconsistency detected between layers")

        # Compute transition closure score
        result.closure_score = self._compute_transition_score(from_layer, to_layer)

        return result

    def detect_semantic_drift(self, layer: str) -> List[Dict]:
        """
        Detect semantic drift in governance layer
        Returns list of entities with semantic violations
        """
        drift_events = []

        # Get current entities
        entities = self.closure_matrix.get(layer, {})

        # Check each entity for drift
        for entity_id, entity in entities.items():
            # Check dependency drift
            dep_drift = self._check_dependency_drift(entity)
            if dep_drift:
                drift_events.append(
                    {
                        "entity_id": entity_id,
                        "drift_type": "dependency",
                        "details": dep_drift,
                    }
                )

            # Check definition drift
            def_drift = self._check_definition_drift(entity)
            if def_drift:
                drift_events.append(
                    {
                        "entity_id": entity_id,
                        "drift_type": "definition",
                        "details": def_drift,
                    }
                )

        # Record drift history
        if drift_events:
            self.drift_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "layer": layer,
                    "drift_count": len(drift_events),
                    "drift_events": drift_events,
                }
            )

        return drift_events

    def get_closure_score(self, layer: str) -> float:
        """
        Get semantic closure score for governance layer
        Returns 0.0 to 1.0 where 1.0 is complete closure
        """
        return self.closure_status.get(layer, 0.0)

    # Private methods

    def _verify_closure(self, entity: SemanticEntity) -> Dict:
        """Verify if entity achieves semantic closure"""
        # Check if all dependencies are defined
        for dep in entity.dependencies:
            dep_key = f"{entity.layer}:{dep}"
            if dep_key not in self.closure_matrix.get(entity.layer, {}):
                # Check lower layers
                found = False
                for lower_layer in self._get_lower_layers(entity.layer):
                    dep_key = f"{lower_layer}:{dep}"
                    if dep_key in self.closure_matrix.get(lower_layer, {}):
                        found = True
                        break
                if not found:
                    return {
                        "is_closed": False,
                        "reason": f"Dependency {dep} not found in any layer",
                    }

        return {"is_closed": True, "reason": ""}

    def _verify_dependencies(self, entity: SemanticEntity) -> Dict:
        """Verify entity dependencies are valid"""
        # Check for self-reference
        if entity.entity_id in entity.dependencies:
            return {"valid": False, "reason": "Self-reference detected"}

        # Check for circular reference (immediate)
        for dep in entity.dependencies:
            dep_entity = self._get_entity(entity.layer, dep)
            if dep_entity and entity.entity_id in dep_entity.dependencies:
                return {"valid": False, "reason": f"Circular reference with {dep}"}

        return {"valid": True, "reason": ""}

    def _find_orphaned_references(self, layer: str) -> List[str]:
        """Find references to non-existent entities"""
        orphans = []
        entities = self.closure_matrix.get(layer, {})

        for entity_id, entity in entities.items():
            for dep in entity.dependencies:
                dep_key = f"{layer}:{dep}"
                if dep_key not in entities:
                    orphans.append(f"{entity_id} → {dep}")

        return orphans

    def _find_circular_dependencies(self, layer: str) -> List[str]:
        """Find circular dependencies in layer"""
        cycles = []
        entities = self.closure_matrix.get(layer, {})

        # Build dependency graph
        graph = {}
        for entity_id, entity in entities.items():
            graph[entity_id] = entity.dependencies

        # Detect cycles using DFS
        visited = set()
        rec_stack = set()

        def detect_cycles(node, path):
            if node in rec_stack:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return True
            if node in visited:
                return False

            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph.get(node, []):
                if detect_cycles(neighbor, path + [node]):
                    return True

            rec_stack.remove(node)
            return False

        for entity_id in graph:
            if entity_id not in visited:
                detect_cycles(entity_id, [])

        return cycles

    def _find_semantic_conflicts(self, layer: str) -> List[str]:
        """Find semantic conflicts in layer"""
        conflicts = []
        entities = self.closure_matrix.get(layer, {})

        # Check for duplicate definitions
        entity_hashes = {}
        for entity_id, entity in entities.items():
            entity_hash = entity.get_hash()
            if entity_hash in entity_hashes:
                conflicts.append(
                    f"Duplicate definition: {entity_id} and {entity_hashes[entity_hash]}"
                )
            else:
                entity_hashes[entity_hash] = entity_id

        return conflicts

    def _check_layer_dependencies(self, from_layer: str, to_layer: str) -> List[str]:
        """Check if to_layer references only from_layer or lower"""
        violations = []
        to_entities = self.closure_matrix.get(to_layer, {})

        for entity_id, entity in to_entities.items():
            for dep in entity.dependencies:
                # Check if dependency is in a higher layer
                dep_layer = self._find_entity_layer(dep)
                if dep_layer and self._is_higher_layer(dep_layer, from_layer):
                    violations.append(
                        f"{to_layer}:{entity_id} references {dep_layer}:{dep} (higher layer)"
                    )

        return violations

    def _check_semantic_consistency(self, from_layer: str, to_layer: str) -> bool:
        """Check semantic consistency between layers"""
        # Check if definitions are consistent
        # This is a simplified check - real implementation would be more sophisticated

        # Get shared entities (entities defined in both layers)
        from_entities = self.closure_matrix.get(from_layer, {})
        to_entities = self.closure_matrix.get(to_layer, {})

        shared = set(from_entities.keys()) & set(to_entities.keys())

        for entity_id in shared:
            from_entity = from_entities[entity_id]
            to_entity = to_entities[entity_id]

            # Check if definitions are compatible
            if from_entity.definition != to_entity.definition:
                return False

        return True

    def _compute_closure_score(self, layer: str) -> float:
        """Compute semantic closure score for layer"""
        entities = self.closure_matrix.get(layer, {})
        if not entities:
            return 0.0

        # Count entities that are closed
        closed_count = 0
        for entity_id, entity in entities.items():
            if self._verify_closure(entity)["is_closed"]:
                closed_count += 1

        return closed_count / len(entities)

    def _compute_transition_score(self, from_layer: str, to_layer: str) -> float:
        """Compute transition closure score"""
        from_score = self.get_closure_score(from_layer)
        to_score = self.get_closure_score(to_layer)

        # Transition score is weighted average
        return from_score * 0.3 + to_score * 0.7

    def _update_closure_status(self, layer: str):
        """Update closure status for layer"""
        self.closure_status[layer] = self._compute_closure_score(layer)

    def _get_entity(self, layer: str, entity_id: str) -> Optional[SemanticEntity]:
        """Get entity from closure matrix"""
        return self.closure_matrix.get(layer, {}).get(entity_id)

    def _get_lower_layers(self, layer: str) -> List[str]:
        """Get layers lower than given layer"""
        # Simplified - assumes L00 < L01 < ... < L99
        layer_num = int(layer[1:])
        return [f"L{str(i).zfill(2)}" for i in range(layer_num)]

    def _is_higher_layer(self, layer1: str, layer2: str) -> bool:
        """Check if layer1 is higher than layer2"""
        layer1_num = int(layer1[1:])
        layer2_num = int(layer2[1:])
        return layer1_num > layer2_num

    def _find_entity_layer(self, entity_id: str) -> Optional[str]:
        """Find which layer defines an entity"""
        for layer, entities in self.closure_matrix.items():
            if entity_id in entities:
                return layer
        return None

    def _check_dependency_drift(self, entity: SemanticEntity) -> Optional[Dict]:
        """Check if entity dependencies have drifted"""
        # Simplified check - real implementation would compare with previous state
        return None

    def _check_definition_drift(self, entity: SemanticEntity) -> Optional[Dict]:
        """Check if entity definition has drifted"""
        # Simplified check - real implementation would compare with previous state
        return None
