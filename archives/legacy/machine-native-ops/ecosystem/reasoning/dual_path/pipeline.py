"""
Reasoning Pipeline
Main orchestration for dual-path retrieval + arbitration system

@GL-semantic: reasoning-pipeline
@GL-audit-trail: enabled
"""

import uuid
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime

from .base_retrieval import RetrievalContext, RetrievalResult
from .internal.retrieval import InternalRetrievalEngine
from .external.retrieval import ExternalRetrievalEngine
from .arbitration import Arbitrator, ArbitrationDecision
from ..traceability.traceability import TraceabilityEngine
from ..traceability.feedback import FeedbackSystem


@dataclass
class ReasoningResponse:
    """Response from reasoning pipeline"""
    request_id: str
    correlation_id: str
    final_answer: str
    decision: Dict[str, Any]
    confidence: float
    reasoning_explanation: str
    evidence_links: List[str]
    risk_assessment: str
    source_counts: Dict[str, int]
    timestamp: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "final_answer": self.final_answer,
            "decision": self.decision,
            "confidence": f"{self.confidence:.3f}",
            "reasoning_explanation": self.reasoning_explanation,
            "evidence_links": self.evidence_links,
            "risk_assessment": self.risk_assessment,
            "source_counts": self.source_counts,
            "timestamp": self.timestamp
        }


class ReasoningPipeline:
    """Main reasoning pipeline orchestrating dual-path system"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize reasoning pipeline
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        
        # Initialize components
        self.internal_engine = InternalRetrievalEngine(config)
        self.external_engine = ExternalRetrievalEngine(config)
        self.arbitrator = Arbitrator(config)
        self.traceability = TraceabilityEngine(config)
        self.feedback = FeedbackSystem(config)
        
        self._stats = {
            "total_requests": 0,
            "decision_distribution": {}
        }
        
    def handle_request(
        self,
        task_spec: str,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None
    ) -> ReasoningResponse:
        """Handle a reasoning request
        
        Args:
            task_spec: Task specification or query
            context: Additional context (sources, domains, etc.)
            user_id: User ID
            
        Returns:
            Reasoning response
        """
        self._stats["total_requests"] += 1
        
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())
        
        # Create retrieval context
        retrieval_context = RetrievalContext(
            query=task_spec,
            task_type=context.get("task_type") if context else None,
            category=context.get("category") if context else None,
            module=context.get("module") if context else None,
            sources=context.get("sources") if context else None,
            domains=context.get("domains") if context else None,
            max_results=context.get("max_results", 10) if context else 10,
            min_confidence=context.get("min_confidence", 0.7) if context else 0.7,
            user_id=user_id
        )
        
        # Step 1: Internal retrieval
        internal_results = self.internal_engine.retrieve(retrieval_context)
        
        # Step 2: External retrieval
        external_results = self.external_engine.retrieve(retrieval_context)
        
        # Step 3: Trace retrieval
        retrieval_trace = self.traceability.trace_retrieval(
            context=retrieval_context.to_dict(),
            internal_results=[r.to_dict() for r in internal_results],
            external_results=[r.to_dict() for r in external_results],
            user_id=user_id
        )
        
        # Step 4: Arbitration
        decision = self.arbitrator.arbitrate(
            retrieval_context,
            internal_results,
            external_results
        )
        
        # Step 5: Trace arbitration
        arbitration_trace = self.traceability.trace_arbitration(
            decision=decision.decision,
            confidence=decision.confidence,
            reasoning=decision.reasoning,
            chosen_results=[r.to_dict() for r in decision.chosen_results],
            user_id=user_id
        )
        
        # Step 6: Generate final answer
        final_answer = self._generate_final_answer(
            task_spec,
            decision,
            internal_results,
            external_results
        )
        
        # Step 7: Build response
        response = ReasoningResponse(
            request_id=retrieval_trace.request_id,
            correlation_id=correlation_id,
            final_answer=final_answer,
            decision=decision.to_dict(),
            confidence=decision.confidence,
            reasoning_explanation=decision.reasoning,
            evidence_links=decision.evidence_links,
            risk_assessment=decision.risk_assessment,
            source_counts={
                "internal": len(internal_results),
                "external": len(external_results),
                "chosen": len(decision.chosen_results)
            },
            timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        
        # Track decision distribution
        decision_type = decision.decision
        self._stats["decision_distribution"][decision_type] = (
            self._stats["decision_distribution"].get(decision_type, 0) + 1
        )
        
        return response
        
    def _generate_final_answer(
        self,
        query: str,
        decision: ArbitrationDecision,
        internal_results: List[RetrievalResult],
        external_results: List[RetrievalResult]
    ) -> str:
        """Generate final answer from decision and results
        
        Args:
            query: Original query
            decision: Arbitration decision
            internal_results: Internal retrieval results
            external_results: External retrieval results
            
        Returns:
            Final answer string
        """
        if decision.decision == "REJECT":
            return (
                "Unable to provide a reliable answer. "
                f"Both internal and external sources have low confidence. "
                f"Internal: {sum(r.confidence for r in internal_results) / max(len(internal_results), 1):.2f}, "
                f"External: {sum(r.confidence for r in external_results) / max(len(external_results), 1):.2f}. "
                "Please rephrase your query or provide more context."
            )
            
        # Combine content from chosen results
        answer_parts = []
        answer_parts.append(f"**Decision**: {decision.decision}")
        answer_parts.append(f"**Confidence**: {decision.confidence:.2%}")
        answer_parts.append(f"**Reasoning**: {decision.reasoning}")
        answer_parts.append("\n**Answer**:\n")
        
        for i, result in enumerate(decision.chosen_results[:3], 1):
            answer_parts.append(f"\n{i}. [{result.source}] (Confidence: {result.confidence:.2%})")
            answer_parts.append(result.content.strip())
            
        # Add evidence links
        if decision.evidence_links:
            answer_parts.append("\n**Evidence**:\n")
            for link in decision.evidence_links:
                answer_parts.append(f"- {link}")
                
        return "\n".join(answer_parts)
        
    def submit_feedback(
        self,
        request_id: str,
        feedback_type: str,
        user_id: str,
        reason: Optional[str] = None
    ) -> None:
        """Submit feedback for a request
        
        Args:
            request_id: Request ID
            feedback_type: Feedback type (ACCEPT/REJECT/MODIFY/IGNORE)
            user_id: User ID
            reason: Feedback reason
        """
        # Submit to feedback system
        self.feedback.submit_feedback(
            request_id=request_id,
            feedback_type=feedback_type,
            user_id=user_id,
            reason=reason
        )
        
        # Trace feedback
        self.traceability.trace_feedback(
            request_id=request_id,
            feedback_type=feedback_type,
            reason=reason,
            user_id=user_id
        )
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get pipeline metrics
        
        Returns:
            Dictionary of metrics
        """
        total = self._stats["total_requests"]
        
        return {
            "pipeline_type": "ReasoningPipeline",
            "total_requests": total,
            "decision_distribution": {
                k: f"{v / total * 100:.1f}%" if total > 0 else "0%"
                for k, v in self._stats["decision_distribution"].items()
            },
            "internal_engine": self.internal_engine.get_stats(),
            "external_engine": self.external_engine.get_stats(),
            "arbitrator": self.arbitrator.get_stats(),
            "traceability": self.traceability.get_stats(),
            "feedback": self.feedback.get_stats()
        }
        
    def get_trace(self, request_id: str) -> Optional[Dict]:
        """Get trace for a request
        
        Args:
            request_id: Request ID
            
        Returns:
            Trace dictionary or None
        """
        trace = self.traceability.get_trace(request_id)
        return trace.to_dict() if trace else None
        
    def export_traces(self, format: str = "json") -> str:
        """Export all traces
        
        Args:
            format: Export format (json, jsonl, markdown)
            
        Returns:
            Export file path
        """
        return self.traceability.export_traces(format=format)
        
    def generate_feedback_report(self) -> str:
        """Generate feedback analysis report
        
        Returns:
            Report string
        """
        return self.feedback.generate_report()
