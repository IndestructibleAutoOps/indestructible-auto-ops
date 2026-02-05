"""
GL Lineage Reconstruction Engine
Implements complete lineage reconstruction from event stream

Based on Research:
- Azure Event Sourcing pattern
- Netflix evidence chain principles
- Meta policy enforcement audit trails
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
from collections import defaultdict


@dataclass
class GovernanceEvent:
    """Represents a governance event in the event stream"""
    event_id: str
    event_type: str
    entity_id: str
    layer: str
    timestamp: str
    data: Dict
    dependencies: List[str]
    context: Dict
    hash: Optional[str] = None
    previous_hash: Optional[str] = None
    
    def compute_hash(self) -> str:
        """Compute event hash"""
        event_data = {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "entity_id": self.entity_id,
            "layer": self.layer,
            "timestamp": self.timestamp,
            "data": self.data,
            "dependencies": sorted(self.dependencies)
        }
        event_json = json.dumps(event_data, sort_keys=True)
        return hashlib.sha256(event_json.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "entity_id": self.entity_id,
            "layer": self.layer,
            "timestamp": self.timestamp,
            "data": self.data,
            "dependencies": self.dependencies,
            "context": self.context,
            "hash": self.hash,
            "previous_hash": self.previous_hash
        }


@dataclass
class LineageNode:
    """Represents a node in the lineage graph"""
    event: GovernanceEvent
    ancestors: Set[str]
    descendants: Set[str]
    depth: int
    
    def add_ancestor(self, event_id: str):
        """Add ancestor to lineage node"""
        self.ancestors.add(event_id)
    
    def add_descendant(self, event_id: str):
        """Add descendant to lineage node"""
        self.descendants.add(event_id)


@dataclass
class LineageGraph:
    """Represents complete lineage graph for an entity"""
    entity_id: str
    nodes: Dict[str, LineageNode]
    root_events: List[str]
    leaf_events: List[str]
    reconstructed_at: datetime
    
    def get_events_chronological(self) -> List[GovernanceEvent]:
        """Get all events in chronological order"""
        events = [node.event for node in self.nodes.values()]
        events.sort(key=lambda e: e.timestamp)
        return events
    
    def get_lineage_depth(self) -> int:
        """Get maximum lineage depth"""
        return max((node.depth for node in self.nodes.values()), default=0)
    
    def get_closure_score(self) -> float:
        """Get lineage closure score"""
        if not self.nodes:
            return 0.0
        
        # Check if all dependencies are resolved
        resolved_count = 0
        for node in self.nodes.values():
            if all(dep in self.nodes for dep in node.event.dependencies):
                resolved_count += 1
        
        return resolved_count / len(self.nodes)


@dataclass
class DecisionTrace:
    """Represents trace of a governance decision"""
    decision_id: str
    events: List[GovernanceEvent]
    dependencies: List[str]
    impacts: List[str]
    traced_at: datetime
    
    def get_trace_length(self) -> int:
        """Get trace length"""
        return len(self.events)
    
    def get_upstream_events(self) -> List[GovernanceEvent]:
        """Get upstream events (dependencies)"""
        return self.events[:-1]
    
    def get_downstream_events(self) -> List[GovernanceEvent]:
        """Get downstream events (impacts)"""
        return self.events[1:]


@dataclass
class VerificationResult:
    """Result of evidence chain verification"""
    is_valid: bool
    verification_score: float
    violations: List[str]
    warnings: List[str]
    verified_at: datetime
    entity_id: str
    
    def add_violation(self, message: str):
        """Add violation to result"""
        self.violations.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        """Add warning to result"""
        self.warnings.append(message)


class GLLineageReconstructionEngine:
    """
    GL Lineage Reconstruction Engine
    Reconstructs complete lineage from event stream
    """
    
    def __init__(self, event_stream_path: str = None):
        self.event_stream: List[GovernanceEvent] = []
        self.event_index: Dict[str, GovernanceEvent] = {}
        self.entity_index: Dict[str, List[str]] = defaultdict(list)
        self.layer_index: Dict[str, List[str]] = defaultdict(list)
        self.reconstruction_cache: Dict[str, LineageGraph] = {}
    
    def load_event_stream(self, events: List[Dict]):
        """
        Load events from event stream
        Builds indexes for efficient querying
        """
        for event_data in events:
            event = GovernanceEvent(
                event_id=event_data["event_id"],
                event_type=event_data["event_type"],
                entity_id=event_data["entity_id"],
                layer=event_data["layer"],
                timestamp=event_data["timestamp"],
                data=event_data.get("data", {}),
                dependencies=event_data.get("dependencies", []),
                context=event_data.get("context", {})
            )
            event.hash = event.compute_hash()
            event.previous_hash = event_data.get("previous_hash")
            
            self.event_stream.append(event)
            self.event_index[event.event_id] = event
            self.entity_index[event.entity_id].append(event.event_id)
            self.layer_index[event.layer].append(event.event_id)
        
        # Sort event stream by timestamp
        self.event_stream.sort(key=lambda e: e.timestamp)
    
    def reconstruct_lineage(self, entity_id: str, from_timestamp: str = None) -> LineageGraph:
        """
        Reconstruct complete lineage for entity
        Returns full lineage graph from creation to current state
        """
        # Check cache
        cache_key = f"{entity_id}:{from_timestamp or 'all'}"
        if cache_key in self.reconstruction_cache:
            return self.reconstruction_cache[cache_key]
        
        # Get all events for entity
        entity_events = self._get_entity_events(entity_id, from_timestamp)
        
        if not entity_events:
            raise ValueError(f"No events found for entity {entity_id}")
        
        # Build lineage graph
        lineage_graph = LineageGraph(
            entity_id=entity_id,
            nodes={},
            root_events=[],
            leaf_events=[],
            reconstructed_at=datetime.now()
        )
        
        # Build dependency graph
        event_dependencies = defaultdict(set)
        event_dependents = defaultdict(set)
        
        for event in entity_events:
            for dep in event.dependencies:
                event_dependencies[event.event_id].add(dep)
                event_dependents[dep].add(event.event_id)
        
        # Build nodes and compute depth
        visited = set()
        
        def build_node(event_id: str, depth: int = 0) -> LineageNode:
            """Recursively build lineage node"""
            if event_id in visited:
                return lineage_graph.nodes.get(event_id)
            
            visited.add(event_id)
            event = self.event_index.get(event_id)
            if not event:
                return None
            
            # Build ancestors (dependencies)
            ancestors = set()
            for dep in event_dependencies[event_id]:
                ancestor_node = build_node(dep, depth + 1)
                if ancestor_node:
                    ancestors.add(dep)
            
            # Create node
            node = LineageNode(
                event=event,
                ancestors=ancestors,
                descendants=set(event_dependents[event_id]),
                depth=depth
            )
            
            lineage_graph.nodes[event_id] = node
            
            # Track root and leaf events
            if not ancestors:
                if event_id not in lineage_graph.root_events:
                    lineage_graph.root_events.append(event_id)
            if not node.descendants:
                if event_id not in lineage_graph.leaf_events:
                    lineage_graph.leaf_events.append(event_id)
            
            return node
        
        # Build all nodes
        for event in entity_events:
            if event.event_id not in visited:
                build_node(event.event_id)
        
        # Verify lineage integrity
        if not self._verify_lineage_integrity(lineage_graph):
            raise ValueError("Lineage integrity verification failed")
        
        # Cache result
        self.reconstruction_cache[cache_key] = lineage_graph
        
        return lineage_graph
    
    def trace_governance_decision(self, decision_id: str) -> DecisionTrace:
        """
        Trace governance decision through complete evidence chain
        Returns full trace of decision including upstream and downstream events
        """
        # Find decision event
        decision_event = self._find_event_by_id(decision_id)
        if not decision_event:
            raise ValueError(f"Decision event {decision_id} not found")
        
        # Build trace
        trace = DecisionTrace(
            decision_id=decision_id,
            events=[decision_event],
            dependencies=[],
            impacts=[],
            traced_at=datetime.now()
        )
        
        # Trace upstream dependencies
        visited_upstream = set()
        def trace_upstream(event_id: str):
            """Recursively trace upstream dependencies"""
            if event_id in visited_upstream:
                return
            visited_upstream.add(event_id)
            
            event = self.event_index.get(event_id)
            if event:
                for dep in event.dependencies:
                    dep_event = self.event_index.get(dep)
                    if dep_event and dep_event.event_id not in visited_upstream:
                        trace.dependencies.insert(0, dep_event.event_id)
                        trace.events.insert(0, dep_event)
                        trace_upstream(dep_event.event_id)
        
        trace_upstream(decision_id)
        
        # Trace downstream impacts
        visited_downstream = set()
        def trace_downstream(event_id: str):
            """Recursively trace downstream impacts"""
            if event_id in visited_downstream:
                return
            visited_downstream.add(event_id)
            
            # Find events that depend on this event
            for event in self.event_stream:
                if event_id in event.dependencies and event.event_id not in visited_downstream:
                    trace.impacts.append(event.event_id)
                    trace.events.append(event)
                    trace_downstream(event.event_id)
        
        trace_downstream(decision_id)
        
        return trace
    
    def verify_evidence_chain(self, entity_id: str) -> VerificationResult:
        """
        Verify evidence chain integrity
        Checks hash chain, temporal consistency, and dependency closure
        """
        result = VerificationResult(
            is_valid=True,
            verification_score=0.0,
            violations=[],
            warnings=[],
            verified_at=datetime.now(),
            entity_id=entity_id
        )
        
        # Get events for entity
        entity_events = self._get_entity_events(entity_id)
        
        if not entity_events:
            result.add_warning(f"No events found for entity {entity_id}")
            return result
        
        # Verify hash chain
        hash_chain_valid = self._verify_hash_chain(entity_events)
        if not hash_chain_valid:
            result.add_violation("Hash chain broken")
        
        # Verify temporal consistency
        temporal_valid = self._verify_temporal_consistency(entity_events)
        if not temporal_valid:
            result.add_violation("Temporal consistency violation detected")
        
        # Verify dependency closure
        dep_valid = self._verify_dependency_closure(entity_events)
        if not dep_valid:
            result.add_violation("Dependency closure violation detected")
        
        # Verify event integrity
        integrity_valid = self._verify_event_integrity(entity_events)
        if not integrity_valid:
            result.add_violation("Event integrity violation detected")
        
        # Compute verification score
        result.verification_score = self._compute_verification_score(result)
        
        return result
    
    def get_lineage_summary(self, entity_id: str) -> Dict:
        """
        Get summary of entity lineage
        Returns key metrics about lineage
        """
        # Get lineage graph
        try:
            lineage = self.reconstruct_lineage(entity_id)
        except ValueError:
            return {
                "entity_id": entity_id,
                "status": "NO_LINEAGE",
                "event_count": 0,
                "depth": 0,
                "closure_score": 0.0
            }
        
        return {
            "entity_id": entity_id,
            "status": "LINEAGE_EXISTS",
            "event_count": len(lineage.nodes),
            "depth": lineage.get_lineage_depth(),
            "closure_score": lineage.get_closure_score(),
            "root_events": len(lineage.root_events),
            "leaf_events": len(lineage.leaf_events),
            "reconstructed_at": lineage.reconstructed_at.isoformat()
        }
    
    # Private methods
    
    def _get_entity_events(self, entity_id: str, from_timestamp: str = None) -> List[GovernanceEvent]:
        """Get all events for entity"""
        event_ids = self.entity_index.get(entity_id, [])
        events = [self.event_index[eid] for eid in event_ids]
        
        # Filter by timestamp if specified
        if from_timestamp:
            events = [e for e in events if e.timestamp >= from_timestamp]
        
        return events
    
    def _find_event_by_id(self, event_id: str) -> Optional[GovernanceEvent]:
        """Find event by ID"""
        return self.event_index.get(event_id)
    
    def _verify_lineage_integrity(self, lineage: LineageGraph) -> bool:
        """Verify lineage graph integrity"""
        # Check for circular dependencies
        for event_id, node in lineage.nodes.items():
            if event_id in node.ancestors:
                return False
        
        # Check that all ancestors exist
        for node in lineage.nodes.values():
            for ancestor_id in node.ancestors:
                if ancestor_id not in lineage.nodes:
                    return False
        
        # Check that all descendants exist
        for node in lineage.nodes.values():
            for descendant_id in node.descendants:
                if descendant_id not in lineage.nodes:
                    return False
        
        return True
    
    def _verify_hash_chain(self, events: List[GovernanceEvent]) -> bool:
        """Verify hash chain continuity"""
        for i in range(1, len(events)):
            if events[i].previous_hash and events[i].previous_hash != events[i-1].hash:
                return False
        return True
    
    def _verify_temporal_consistency(self, events: List[GovernanceEvent]) -> bool:
        """Verify temporal consistency"""
        # Check timestamps are monotonically increasing
        for i in range(1, len(events)):
            if events[i].timestamp < events[i-1].timestamp:
                return False
        
        # Check that dependencies have earlier timestamps
        for event in events:
            for dep_id in event.dependencies:
                dep_event = self.event_index.get(dep_id)
                if dep_event and dep_event.timestamp > event.timestamp:
                    return False
        
        return True
    
    def _verify_dependency_closure(self, events: List[GovernanceEvent]) -> bool:
        """Verify dependency closure"""
        # Check that all dependencies exist
        for event in events:
            for dep_id in event.dependencies:
                if dep_id not in self.event_index:
                    return False
        
        return True
    
    def _verify_event_integrity(self, events: List[GovernanceEvent]) -> bool:
        """Verify event hash integrity"""
        for event in events:
            computed_hash = event.compute_hash()
            if event.hash != computed_hash:
                return False
        return True
    
    def _compute_verification_score(self, result: VerificationResult) -> float:
        """Compute verification score"""
        total_checks = 4  # hash chain, temporal, dependency, integrity
        passed_checks = total_checks - len(result.violations)
        return passed_checks / total_checks