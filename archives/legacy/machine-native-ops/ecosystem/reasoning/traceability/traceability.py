"""
Traceability Engine
Tracks complete reasoning process for audit and compliance

@GL-semantic: traceability-engine
@GL-audit-trail: enabled
"""

import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class TraceRecord:
    """Single traceability record"""
    request_id: str
    correlation_id: str
    actor: str
    action: str
    resource: str
    result: str
    metadata: Dict[str, Any]
    timestamp: str
    hash: str
    evidence_links: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)
        
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
        
    def to_jsonl(self) -> str:
        """Convert to JSONL string"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
        
    def to_markdown(self) -> str:
        """Convert to Markdown string"""
        md = f"""# Trace Record

## Request Info
- **Request ID**: {self.request_id}
- **Correlation ID**: {self.correlation_id}
- **Timestamp**: {self.timestamp}

## Action Details
- **Actor**: {self.actor}
- **Action**: {self.action}
- **Resource**: {self.resource}
- **Result**: {self.result}

## Evidence
{chr(10).join(f"- {link}" for link in self.evidence_links)}

## Metadata
```json
{json.dumps(self.metadata, indent=2)}
```

## Hash
`{self.hash}`
"""
        return md


class TraceabilityEngine:
    """Traceability engine for complete audit trail"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize traceability engine
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.log_path = None
        self._traces = []
        self._stats = {
            "total_traces": 0,
            "actions": {}
        }
        self._initialize()
        
    def _initialize(self) -> None:
        """Initialize the traceability engine"""
        workspace = Path(self.config.get("workspace", "/workspace/machine-native-ops"))
        self.log_path = workspace / self.config.get(
            "log_path",
            "ecosystem/reasoning/logs"
        )
        
        # Create log directory
        self.log_path.mkdir(parents=True, exist_ok=True)
        
    def trace(
        self,
        actor: str,
        action: str,
        resource: str,
        result: str,
        metadata: Optional[Dict[str, Any]] = None,
        evidence_links: Optional[List[str]] = None,
        correlation_id: Optional[str] = None
    ) -> TraceRecord:
        """Create a trace record
        
        Args:
            actor: Who performed the action
            action: What action was performed
            resource: What resource was acted upon
            result: Result of the action
            metadata: Additional metadata
            evidence_links: Evidence links
            correlation_id: Correlation ID for grouping
            
        Returns:
            Trace record
        """
        # Generate request ID
        request_id = self._generate_request_id()
        
        # Use correlation ID if provided, otherwise use request ID
        correlation_id = correlation_id or request_id
        
        # Create trace record
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        trace_data = {
            "request_id": request_id,
            "correlation_id": correlation_id,
            "actor": actor,
            "action": action,
            "resource": resource,
            "result": result,
            "metadata": metadata or {},
            "timestamp": timestamp
        }
        
        # Calculate hash
        hash_value = self._calculate_hash(trace_data)
        trace_data["hash"] = hash_value
        
        # Add evidence links
        trace_data["evidence_links"] = evidence_links or []
        
        # Create trace record
        trace = TraceRecord(**trace_data)
        
        # Store trace
        self._traces.append(trace)
        self._stats["total_traces"] += 1
        self._stats["actions"][action] = self._stats["actions"].get(action, 0) + 1
        
        # Save trace to file
        self._save_trace(trace)
        
        return trace
        
    def trace_retrieval(
        self,
        context: Dict,
        internal_results: List[Dict],
        external_results: List[Dict],
        user_id: Optional[str] = None
    ) -> TraceRecord:
        """Trace a retrieval operation
        
        Args:
            context: Retrieval context
            internal_results: Internal retrieval results
            external_results: External retrieval results
            user_id: User ID
            
        Returns:
            Trace record
        """
        evidence_links = []
        for result in internal_results:
            evidence_links.extend(result.get("evidence_links", []))
        for result in external_results:
            evidence_links.extend(result.get("evidence_links", []))
            
        return self.trace(
            actor=user_id or "system",
            action="RETRIEVAL",
            resource=f"query: {context.get('query', 'unknown')}",
            result=f"internal: {len(internal_results)}, external: {len(external_results)}",
            metadata={
                "context": context,
                "internal_count": len(internal_results),
                "external_count": len(external_results)
            },
            evidence_links=evidence_links
        )
        
    def trace_arbitration(
        self,
        decision: str,
        confidence: float,
        reasoning: str,
        chosen_results: List[Dict],
        user_id: Optional[str] = None
    ) -> TraceRecord:
        """Trace an arbitration decision
        
        Args:
            decision: Arbitration decision
            confidence: Decision confidence
            reasoning: Decision reasoning
            chosen_results: Chosen results
            user_id: User ID
            
        Returns:
            Trace record
        """
        evidence_links = []
        for result in chosen_results:
            evidence_links.extend(result.get("evidence_links", []))
            
        return self.trace(
            actor=user_id or "arbitrator",
            action="ARBITRATION",
            resource=f"decision: {decision}",
            result=f"confidence: {confidence:.3f}, results: {len(chosen_results)}",
            metadata={
                "decision": decision,
                "confidence": confidence,
                "reasoning": reasoning,
                "results_count": len(chosen_results)
            },
            evidence_links=evidence_links
        )
        
    def trace_feedback(
        self,
        request_id: str,
        feedback_type: str,
        reason: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> TraceRecord:
        """Trace a user feedback
        
        Args:
            request_id: Original request ID
            feedback_type: Feedback type (ACCEPT/REJECT/MODIFY/IGNORE)
            reason: Feedback reason
            user_id: User ID
            
        Returns:
            Trace record
        """
        return self.trace(
            actor=user_id or "user",
            action="FEEDBACK",
            resource=f"request: {request_id}",
            result=feedback_type,
            metadata={
                "request_id": request_id,
                "feedback_type": feedback_type,
                "reason": reason
            }
        )
        
    def _generate_request_id(self) -> str:
        """Generate unique request ID
        
        Returns:
            Request ID string
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        random_str = hashlib.md5(str(hash(self)).encode()).hexdigest()[:8]
        return f"req-{timestamp}-{random_str}"
        
    def _calculate_hash(self, data: Dict) -> str:
        """Calculate SHA-256 hash of data
        
        Args:
            data: Data dictionary
            
        Returns:
            Hash string
        """
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
        
    def _save_trace(self, trace: TraceRecord) -> None:
        """Save trace to file
        
        Args:
            trace: Trace record
        """
        # Save in JSON format
        json_file = self.log_path / f"{trace.request_id}.json"
        with open(json_file, 'w') as f:
            f.write(trace.to_json())
            
        # Append to JSONL for log aggregation
        jsonl_file = self.log_path / "traces.jsonl"
        with open(jsonl_file, 'a') as f:
            f.write(trace.to_jsonl() + '\n')
            
    def get_trace(self, request_id: str) -> Optional[TraceRecord]:
        """Get trace by request ID
        
        Args:
            request_id: Request ID
            
        Returns:
            Trace record or None
        """
        for trace in self._traces:
            if trace.request_id == request_id:
                return trace
        return None
        
    def get_traces_by_correlation(self, correlation_id: str) -> List[TraceRecord]:
        """Get all traces for a correlation ID
        
        Args:
            correlation_id: Correlation ID
            
        Returns:
            List of trace records
        """
        return [t for t in self._traces if t.correlation_id == correlation_id]
        
    def export_traces(
        self,
        format: str = "json",
        output_path: Optional[str] = None
    ) -> str:
        """Export all traces
        
        Args:
            format: Export format (json, jsonl, markdown)
            output_path: Output file path
            
        Returns:
            Exported file path
        """
        if output_path is None:
            output_path = self.log_path / f"traces_export.{format}"
            
        if format == "json":
            with open(output_path, 'w') as f:
                json.dump([t.to_dict() for t in self._traces], f, indent=2)
        elif format == "jsonl":
            with open(output_path, 'w') as f:
                for trace in self._traces:
                    f.write(trace.to_jsonl() + '\n')
        elif format == "markdown":
            with open(output_path, 'w') as f:
                f.write("# Traceability Export\n\n")
                for trace in self._traces:
                    f.write(trace.to_markdown() + "\n\n---\n\n")
                    
        return str(output_path)
        
    def get_stats(self) -> Dict[str, Any]:
        """Get traceability engine statistics
        
        Returns:
            Dictionary of statistics
        """
        return {
            "engine_type": "TraceabilityEngine",
            "log_path": str(self.log_path),
            "total_traces": self._stats["total_traces"],
            "action_distribution": self._stats["actions"],
            "memory_traces": len(self._traces)
        }
