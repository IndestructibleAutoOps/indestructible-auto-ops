"""
Traceability Engine
Tracks complete reasoning process and provides full audit trail
"""

import os
import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path


class TraceReport:
    """Complete traceability report"""

    def __init__(
        self,
        final_answer: str,
        sources: Dict,
        arbitration_trace: Dict,
        metadata: Optional[Dict] = None,
    ):
        self.final_answer = final_answer
        self.sources = sources
        self.arbitration_trace = arbitration_trace
        self.metadata = metadata or {}
        self.generated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "metadata": {
                "generated_at": self.generated_at,
                "version": "1.0.0",
                **self.metadata,
            },
            "final_answer": self.final_answer,
            "sources": self.sources,
            "arbitration_trace": self.arbitration_trace,
        }

    def save(self, output_path: str, format: str = "json"):
        """Save trace report to file"""
        report_data = self.to_dict()

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
        elif format == "jsonl":
            with open(output_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(report_data) + "\n")
        elif format == "markdown":
            self._save_markdown(output_path)

        print(f"Trace report saved to {output_path}")

    def _save_markdown(self, output_path: str):
        """Save trace report as Markdown"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Traceability Report\n\n")
            f.write(f"**Generated:** {self.generated_at}\n\n")

            f.write("## Final Answer\n\n")
            f.write(f"{self.final_answer}\n\n")

            f.write("## Sources\n\n")

            if "internal" in self.sources:
                f.write("### Internal Sources\n\n")
                for source in self.sources["internal"].get("files", []):
                    f.write(f"- **{source['path']}:**\n")
                    f.write(f"  - Lines: {source.get('lines', 'N/A')}\n")
                    f.write(f"  - Checksum: {source.get('checksum', 'N/A')}\n\n")

                for source in self.sources["internal"].get("contracts", []):
                    f.write(f"- **{source['path']}:**\n")
                    f.write(f"  - Version: {source.get('version', 'N/A')}\n")
                    f.write(f"  - Section: {source.get('section', 'N/A')}\n\n")

            if "external" in self.sources:
                f.write("### External Sources\n\n")
                for source in self.sources["external"].get("urls", []):
                    f.write(f"- [{source['title']}]({source['url']})\n")
                    f.write(f"  - Accessed: {source.get('accessed', 'N/A')}\n")
                    f.write(f"  - Confidence: {source.get('confidence', 'N/A')}\n\n")

            f.write("## Arbitration Trace\n\n")

            if "conflicts" in self.arbitration_trace:
                f.write("### Conflicts\n\n")
                for i, conflict in enumerate(self.arbitration_trace["conflicts"], 1):
                    f.write(f"{i}. **{conflict.get('issue', 'Unknown')}**\n")
                    f.write(f"   - Internal: {conflict.get('internal', 'N/A')}\n")
                    f.write(f"   - External: {conflict.get('external', 'N/A')}\n")
                    f.write(f"   - Resolution: {conflict.get('resolution', 'N/A')}\n")
                    f.write(f"   - Reason: {conflict.get('reason', 'N/A')}\n\n")

            if "reasoning_chain" in self.arbitration_trace:
                f.write("### Reasoning Chain\n\n")
                for i, step in enumerate(self.arbitration_trace["reasoning_chain"], 1):
                    f.write(f"{i}. {step}\n")


class TraceabilityEngine:
    """Engine for generating and managing traceability reports"""

    def __init__(self, config=None):
        """Initialize traceability engine"""
        # Handle both dict config and string path
        if isinstance(config, dict):
            self.output_dir = config.get("output_dir", "ecosystem/logs/audit")
        elif isinstance(config, str):
            self.output_dir = config
        elif config is None:
            self.output_dir = "ecosystem/logs/audit"
        else:
            self.output_dir = "ecosystem/logs/audit"

        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def generate_trace(
        self,
        task_spec: str,
        internal_results: List[Dict],
        external_results: List[Dict],
        arbitration_decision: Dict,
        final_answer: str,
    ) -> TraceReport:
        """
        Generate complete traceability report

        Args:
            task_spec: Task specification
            internal_results: List of internal retrieval results
            external_results: List of external retrieval results
            arbitration_decision: Arbitration decision
            final_answer: Final answer provided to user

        Returns:
            TraceReport
        """
        # Process sources
        sources = {
            "internal": self._process_internal_sources(internal_results),
            "external": self._process_external_sources(external_results),
        }

        # Process arbitration trace
        arbitration_trace = self._process_arbitration_trace(
            internal_results, external_results, arbitration_decision
        )

        # Create report
        report = TraceReport(
            final_answer=final_answer,
            sources=sources,
            arbitration_trace=arbitration_trace,
            metadata={
                "task_spec": task_spec,
                "internal_count": len(internal_results),
                "external_count": len(external_results),
                "request_id": hashlib.md5(task_spec.encode()).hexdigest()[:16],
            },
        )

        return report

    def trace_retrieval(
        self,
        context: Dict,
        internal_results: List[Dict],
        external_results: List[Dict],
        user_id: Optional[str] = None,
    ) -> Dict:
        """Trace retrieval step

        Args:
            context: Retrieval context
            internal_results: Internal retrieval results
            external_results: External retrieval results
            user_id: Optional user identifier

        Returns:
            Retrieval trace dictionary
        """
        return {
            "context": context,
            "internal_count": len(internal_results),
            "external_count": len(external_results),
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
        }

    def trace_arbitration(
        self,
        decision: Dict,
        internal_result: Dict,
        external_result: Dict,
        user_id: Optional[str] = None,
    ) -> Dict:
        """Trace arbitration step

        Args:
            decision: Arbitration decision
            internal_result: Internal result dict
            external_result: External result dict
            user_id: Optional user identifier

        Returns:
            Arbitration trace dictionary
        """
        return {
            "decision": decision,
            "internal_confidence": internal_result.get("confidence", 0.0),
            "external_confidence": external_result.get("confidence", 0.0),
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
        }

    def trace_feedback(
        self,
        request_id: str,
        feedback_type: str,
        reason: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Dict:
        """Trace feedback submission

        Args:
            request_id: Request identifier
            feedback_type: Type of feedback
            reason: Optional reason
            user_id: Optional user identifier

        Returns:
            Feedback trace dictionary
        """
        return {
            "request_id": request_id,
            "feedback_type": feedback_type,
            "reason": reason,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
        }

    def _process_internal_sources(self, results: List[Dict]) -> Dict:
        """Process internal retrieval results"""
        files = []
        contracts = []

        for result in results:
            if result.get("file_path"):
                files.append(
                    {
                        "path": result.get("file_path"),
                        "lines": result.get("line_range"),
                        "checksum": result.get("metadata", {}).get("checksum")
                        or result.get("checksum"),
                        "snippet": result.get("content", "")[:200] + "...",
                    }
                )

            if result.get("source") == "governance":
                contracts.append(
                    {
                        "path": result.get("file_path"),
                        "version": result.get("metadata", {}).get("version"),
                        "section": result.get("metadata", {}).get("section"),
                    }
                )

        return {"files": files, "contracts": contracts}

    def _process_external_sources(self, results: List[Dict]) -> Dict:
        """Process external retrieval results"""
        urls = []

        for result in results:
            urls.append(
                {
                    "url": result.get("url"),
                    "title": result.get("title"),
                    "accessed": result.get("accessed"),
                    "confidence": result.get("confidence"),
                    "snippet": result.get("content", "")[:200] + "...",
                }
            )

        return {"urls": urls}

    def _process_arbitration_trace(
        self, internal_results: List[Dict], external_results: List[Dict], decision: Dict
    ) -> Dict:
        """Process arbitration decision trace"""
        conflicts = []
        reasoning_chain = []

        # Detect conflicts
        internal_versions = set(
            r.get("metadata", {}).get("version")
            for r in internal_results
            if r.get("metadata")
        )
        external_versions = set(
            r.get("metadata", {}).get("version")
            for r in external_results
            if r.get("metadata")
        )

        if len(internal_versions) > 0 and len(external_versions) > 0:
            version_diff = internal_versions.symmetric_difference(external_versions)
            if version_diff:
                conflicts.append(
                    {
                        "issue": "Version mismatch detected",
                        "internal": ", ".join(filter(None, internal_versions)),
                        "external": ", ".join(filter(None, external_versions)),
                        "resolution": decision.get("reason", "N/A"),
                        "reason": "Chosen based on arbitration rule",
                    }
                )

        # Build reasoning chain
        reasoning_chain.append(f"1. Analyzed {len(internal_results)} internal sources")
        reasoning_chain.append(f"2. Analyzed {len(external_results)} external sources")

        if conflicts:
            reasoning_chain.append(f"3. Detected {len(conflicts)} conflict(s)")

        reasoning_chain.append(
            f"4. Applied arbitration: {decision.get('decision', 'N/A')}"
        )
        reasoning_chain.append(f"5. Reason: {decision.get('reason', 'N/A')}")

        return {
            "conflicts": conflicts,
            "reasoning_chain": reasoning_chain,
            "decision": decision,
        }

    def save_trace(
        self,
        report: TraceReport,
        request_id: str,
        formats: List[str] = ["json", "jsonl"],
    ):
        """
        Save trace report in multiple formats

        Args:
            report: TraceReport to save
            request_id: Request identifier
            formats: List of formats to save (json, jsonl, markdown)
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

        for format in formats:
            filename = f"trace_{request_id}_{timestamp}.{format}"
            output_path = os.path.join(self.output_dir, filename)
            report.save(output_path, format)

    def query_traces(self, request_id: str) -> List[Dict]:
        """Query traces by request ID"""
        traces = []

        for file_path in Path(self.output_dir).glob(f"trace_{request_id}_*.json"):
            with open(file_path, "r", encoding="utf-8") as f:
                traces.append(json.load(f))

        return traces

    def get_stats(self) -> Dict:
        """Get traceability engine statistics"""
        return {
            "engine_type": "TraceabilityEngine",
            "output_dir": self.output_dir,
            "status": "operational",
        }

    def get_trace(self, request_id: str) -> Optional[Dict]:
        """Get trace for a specific request

        Args:
            request_id: Request identifier

        Returns:
            Trace dictionary or None
        """
        traces = self.query_traces(request_id)
        return traces[0] if traces else None

    def export_traces(self, format: str = "json") -> str:
        """Export all traces

        Args:
            format: Export format (json, jsonl, markdown)

        Returns:
            Export file path
        """
        output_file = Path(self.output_dir) / f"traces_export.{format}"
        traces = []

        # Collect all traces
        for trace_file in Path(self.output_dir).glob("trace_*.json"):
            with open(trace_file, "r", encoding="utf-8") as f:
                traces.append(json.load(f))

        # Export based on format
        if format == "json":
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(traces, f, indent=2, ensure_ascii=False)
        elif format == "jsonl":
            with open(output_file, "w", encoding="utf-8") as f:
                for trace in traces:
                    f.write(json.dumps(trace) + "\n")
        else:
            # Default to json
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(traces, f, indent=2, ensure_ascii=False)

        return str(output_file)


if __name__ == "__main__":
    # Test traceability engine
    engine = TraceabilityEngine()

    # Mock data
    internal_results = [
        {
            "content": "def process_task(task): pass",
            "file_path": "src/worker.py",
            "line_range": "45-48",
            "metadata": {"checksum": "abc123", "version": "3.8"},
        }
    ]

    external_results = [
        {
            "content": "asyncio.create_task() documentation",
            "url": "https://docs.python.org/3/library/asyncio.html",
            "title": "Python asyncio",
            "confidence": 0.95,
            "accessed": datetime.now(timezone.utc).isoformat(),
            "metadata": {"version": "3.11"},
        }
    ]

    arbitration_decision = {
        "decision": "INTERNAL",
        "reason": "Production environment compatibility",
        "internal_confidence": 0.92,
        "external_confidence": 0.95,
    }

    final_answer = "Use internal implementation for production compatibility"

    # Generate trace report
    report = engine.generate_trace(
        task_spec="How to implement async task processing?",
        internal_results=internal_results,
        external_results=external_results,
        arbitration_decision=arbitration_decision,
        final_answer=final_answer,
    )

    # Save report
    request_id = hashlib.md5("async task processing".encode()).hexdigest()[:16]
    engine.save_trace(report, request_id, formats=["json", "markdown"])

    print("Traceability report generated successfully")
