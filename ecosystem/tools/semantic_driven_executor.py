#!/usr/bin/env python3
"""
Semantic-Driven Governance Executor (語義驅動治理實作引擎)

Integrates violation detection, task generation, implementation checklist creation,
and comprehensive verification of implementation artifacts.

This is NOT just a validator - it's a complete governance-driven execution engine.

Usage:
    python ecosystem/tools/semantic_driven_executor.py --report reports/example.md
    python ecosystem/tools/semantic_driven_executor.py --report reports/example.md --generate-checklist
    python ecosystem/tools/semantic_driven_executor.py --report reports/example.md --verify-implementation
    python ecosystem/tools/semantic_driven_executor.py --checklist reports/implementation-checklist.json --verify-implementation
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import uuid

# Add ecosystem to path
sys.path.insert(0, str(Path(__file__).parent.parent))

class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class ItemStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VERIFIED = "verified"

class ItemType(Enum):
    TOOL = "tool"
    PHASE = "phase"
    TERMINOLOGY = "terminology"
    ARTIFACT = "artifact"
    DOCUMENT = "document"
    ENGINE = "engine"
    PLATFORM = "platform"

@dataclass
class Violation:
    """Violation from semantic validator"""
    violation_id: str
    category: str
    severity: Severity
    message: str
    line_number: int = 0
    context: str = ""
    suggested_fix: str = ""

@dataclass
class Task:
    """Task from SETC"""
    task_id: str
    name: str
    description: str
    task_type: str
    priority: str
    state: str
    estimated_effort: str
    created_from: str

@dataclass
class ImplementationItem:
    """Single implementation item requiring verification"""
    item_id: str
    name: str
    type: ItemType
    priority: Severity
    status: ItemStatus
    required_files: List[str] = field(default_factory=list)
    required_events: List[str] = field(default_factory=list)
    required_artifacts: List[int] = field(default_factory=list)
    requires_hash: bool = False
    requires_sealing: bool = False
    
    # Verification results
    file_exists: bool = False
    event_stream_ok: bool = False
    artifact_ok: bool = False
    hash_ok: bool = False
    sealing_ok: bool = False
    
    # Metadata
    violation_id: Optional[str] = None
    task_id: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""
    notes: str = ""

@dataclass
class ImplementationChecklist:
    """Complete implementation checklist"""
    checklist_id: str
    report_file: str
    violations: List[Violation] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    items: List[ImplementationItem] = field(default_factory=list)
    
    # Metrics
    semantic_compliance: float = 0.0
    completion_rate: float = 0.0
    verification_rate: float = 0.0
    overall_score: float = 0.0
    
    created_at: str = ""
    updated_at: str = ""
    
    def get_completion_rate(self) -> float:
        """Calculate completion rate"""
        if not self.items:
            return 0.0
        completed = sum(1 for item in self.items if item.status in [ItemStatus.COMPLETED, ItemStatus.VERIFIED])
        return (completed / len(self.items)) * 100
    
    def get_verification_rate(self) -> float:
        """Calculate verification pass rate"""
        if not self.items:
            return 0.0
        verified = sum(1 for item in self.items 
                      if all([item.file_exists, item.event_stream_ok, item.artifact_ok]))
        return (verified / len(self.items)) * 100
    
    def get_overall_score(self) -> float:
        """Calculate overall governance score"""
        return (
            self.semantic_compliance * 0.4 +
            self.completion_rate * 0.3 +
            self.verification_rate * 0.3
        )

class VerificationEngine:
    """Verification engine for implementation artifacts"""
    
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = workspace
        self.governance_dir = os.path.join(workspace, ".governance")
        self.evidence_dir = os.path.join(workspace, ".evidence")
        self.event_stream_file = os.path.join(self.governance_dir, "event-stream.jsonl")
        self.core_hash_file = os.path.join(self.governance_dir, "core-hash.json")
        
    def verify_file_exists(self, file_path: str) -> bool:
        """Verify if a file exists"""
        full_path = os.path.join(self.workspace, file_path)
        return os.path.exists(full_path) and os.path.isfile(full_path)
    
    def verify_event_stream(self, event_type: str) -> bool:
        """Verify if event exists in event stream"""
        if not os.path.exists(self.event_stream_file):
            return False
        
        try:
            with open(self.event_stream_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        event = json.loads(line)
                        if event.get('event_type') == event_type:
                            return True
            return False
        except Exception as e:
            print(f"[WARNING] Failed to verify event stream: {e}")
            return False
    
    def verify_artifact(self, step: int) -> bool:
        """Verify if artifact exists"""
        artifact_file = os.path.join(self.evidence_dir, f"step-{step}.json")
        return os.path.exists(artifact_file) and os.path.isfile(artifact_file)
    
    def verify_hash(self, artifact_path: str) -> bool:
        """Verify if artifact contains SHA256 hash"""
        try:
            with open(artifact_path, 'r', encoding='utf-8') as f:
                artifact = json.load(f)
            return 'artifact_hash' in artifact and artifact['artifact_hash']
        except Exception as e:
            print(f"[WARNING] Failed to verify hash: {e}")
            return False
    
    def verify_sealing(self, item_id: str) -> bool:
        """Verify if item is sealed in core-hash.json"""
        if not os.path.exists(self.core_hash_file):
            return False  # Era-1 doesn't require sealing
        
        try:
            with open(self.core_hash_file, 'r', encoding='utf-8') as f:
                core_hash = json.load(f)
            return item_id in core_hash.get('sealed_artifacts', {})
        except Exception as e:
            print(f"[WARNING] Failed to verify sealing: {e}")
            return False
    
    def verify_item(self, item: ImplementationItem) -> Dict[str, bool]:
        """Verify all requirements for an item"""
        results = {
            'file_exists': True,
            'event_stream_ok': True,
            'artifact_ok': True,
            'hash_ok': True,
            'sealing_ok': True
        }
        
        # Verify required files
        if item.required_files:
            results['file_exists'] = all(
                self.verify_file_exists(f) for f in item.required_files
            )
        
        # Verify required events
        if item.required_events:
            results['event_stream_ok'] = all(
                self.verify_event_stream(evt) for evt in item.required_events
            )
        
        # Verify required artifacts
        if item.required_artifacts:
            results['artifact_ok'] = all(
                self.verify_artifact(step) for step in item.required_artifacts
            )
        
        # Verify hash if required
        if item.requires_hash and item.required_artifacts:
            results['hash_ok'] = all(
                self.verify_hash(os.path.join(self.evidence_dir, f"step-{step}.json"))
                for step in item.required_artifacts
            )
        
        # Verify sealing if required
        if item.requires_sealing:
            results['sealing_ok'] = self.verify_sealing(item.item_id)
        else:
            # Era-1 doesn't require sealing
            results['sealing_ok'] = True
        
        return results

class SemanticDrivenExecutor:
    """Main semantic-driven governance executor"""
    
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = workspace
        self.verifier = VerificationEngine(workspace)
        self.checklists_dir = os.path.join(workspace, ".governance", "checklists")
        os.makedirs(self.checklists_dir, exist_ok=True)
        os.makedirs(self.verifier.evidence_dir, exist_ok=True)
        os.makedirs(self.verifier.governance_dir, exist_ok=True)
    
    def generate_implementation_checklist(
        self, 
        violations: List[Violation],
        tasks: List[Task],
        report_file: str
    ) -> ImplementationChecklist:
        """Generate implementation checklist from violations and tasks"""
        
        checklist = ImplementationChecklist(
            checklist_id=f"CHECKLIST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            report_file=report_file,
            violations=violations,
            tasks=tasks,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # Convert violations to implementation items
        item_counter = 0
        
        for violation in violations:
            item_counter += 1
            item = self._violation_to_item(violation, item_counter)
            checklist.items.append(item)
        
        # Link tasks to items
        for task in tasks:
            matching_items = [
                item for item in checklist.items
                if item.violation_id and task.created_from and item.violation_id in task.created_from
            ]
            for item in matching_items:
                item.task_id = task.task_id
        
        # Calculate initial metrics
        checklist.semantic_compliance = self._calculate_semantic_compliance(violations)
        checklist.completion_rate = checklist.get_completion_rate()
        checklist.verification_rate = checklist.get_verification_rate()
        checklist.overall_score = checklist.get_overall_score()
        
        return checklist
    
    def _violation_to_item(self, violation: Violation, counter: int) -> ImplementationItem:
        """Convert violation to implementation item"""
        
        item_id = f"ITEM-{datetime.now().strftime('%Y%m%d')}-{counter:03d}"
        
        # Determine item type and requirements based on violation category
        if violation.category == "tool_references":
            item_type = ItemType.TOOL
            # Extract tool name from message
            tool_name_match = re.search(r'[\'"]?[\w_]+\.py[\'"]?', violation.message)
            tool_name = tool_name_match.group(0) if tool_name_match else "unknown_tool"
            
            required_files = [f"ecosystem/tools/{tool_name}"]
            required_events = ["TOOL_REGISTERED"]
            requires_hash = False
            requires_sealing = False
            
        elif violation.category == "phase_declarations":
            item_type = ItemType.PHASE
            required_files = []
            required_events = ["PHASE_IMPLEMENTED"]
            requires_hash = False
            requires_sealing = False
            
        elif violation.category == "terminology":
            item_type = ItemType.TERMINOLOGY
            required_files = ["ecosystem/governance/terminology.yaml"]
            required_events = ["TERMINOLOGY_DEFINED"]
            requires_hash = False
            requires_sealing = False
            
        elif violation.category == "architecture_level":
            item_type = ItemType.PLATFORM
            required_files = []
            required_events = ["PLATFORM_IMPLEMENTED"]
            requires_hash = False
            requires_sealing = False
            
        elif violation.category == "compliance_claims":
            item_type = ItemType.DOCUMENT
            required_files = []
            required_events = ["REPORT_GENERATED"]
            requires_hash = False
            requires_sealing = False
            
        else:
            item_type = ItemType.DOCUMENT
            required_files = []
            required_events = ["VIOLATION_FIXED"]
            requires_hash = False
            requires_sealing = False
        
        return ImplementationItem(
            item_id=item_id,
            name=f"Fix: {violation.message[:50]}...",
            type=item_type,
            priority=violation.severity,
            status=ItemStatus.PENDING,
            required_files=required_files,
            required_events=required_events,
            requires_hash=requires_hash,
            requires_sealing=requires_sealing,
            violation_id=violation.violation_id,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            notes=violation.suggested_fix
        )
    
    def verify_implementation(self, checklist: ImplementationChecklist) -> ImplementationChecklist:
        """Verify all items in checklist"""
        
        for item in checklist.items:
            # Run verification
            results = self.verifier.verify_item(item)
            
            # Update item with results
            item.file_exists = results['file_exists']
            item.event_stream_ok = results['event_stream_ok']
            item.artifact_ok = results['artifact_ok']
            item.hash_ok = results['hash_ok']
            item.sealing_ok = results['sealing_ok']
            
            # Update status based on verification
            all_ok = all([
                item.file_exists,
                item.event_stream_ok,
                item.artifact_ok,
                item.hash_ok,
                item.sealing_ok
            ])
            
            if all_ok:
                item.status = ItemStatus.VERIFIED
            elif any([item.file_exists, item.event_stream_ok]):
                item.status = ItemStatus.COMPLETED
            else:
                item.status = ItemStatus.PENDING
            
            item.updated_at = datetime.now().isoformat()
        
        # Recalculate metrics
        checklist.completion_rate = checklist.get_completion_rate()
        checklist.verification_rate = checklist.get_verification_rate()
        checklist.overall_score = checklist.get_overall_score()
        checklist.updated_at = datetime.now().isoformat()
        
        return checklist
    
    def _calculate_semantic_compliance(self, violations: List[Violation]) -> float:
        """Calculate semantic compliance score"""
        if not violations:
            return 100.0
        
        # Weight by severity
        severity_weights = {
            Severity.CRITICAL: 10,
            Severity.HIGH: 5,
            Severity.MEDIUM: 2,
            Severity.LOW: 1
        }
        
        total_weight = sum(severity_weights.get(v.severity, 1) for v in violations)
        max_possible_weight = len(violations) * 10  # Assume all CRITICAL as worst case
        
        return max(0, 100 - (total_weight / max_possible_weight * 100))
    
    def _serialize_item(self, item: ImplementationItem) -> Dict:
        """Serialize ImplementationItem to dict"""
        return {
            'item_id': item.item_id,
            'name': item.name,
            'type': item.type.value if isinstance(item.type, ItemType) else item.type if isinstance(item.type, ItemType) else item.type,
            'priority': item.priority.value if isinstance(item.priority, Severity) else item.priority if isinstance(item.priority, Severity) else item.priority,
            'status': item.status.value if isinstance(item.status, ItemStatus) else item.status if isinstance(item.status, ItemStatus) else item.status,
            'required_files': item.required_files,
            'required_events': item.required_events,
            'required_artifacts': item.required_artifacts,
            'requires_hash': item.requires_hash,
            'requires_sealing': item.requires_sealing,
            'file_exists': item.file_exists,
            'event_stream_ok': item.event_stream_ok,
            'artifact_ok': item.artifact_ok,
            'hash_ok': item.hash_ok,
            'sealing_ok': item.sealing_ok,
            'violation_id': item.violation_id,
            'task_id': item.task_id,
            'created_at': item.created_at,
            'updated_at': item.updated_at,
            'notes': item.notes
        }
    
    def save_checklist(self, checklist: ImplementationChecklist, output_file: str = None) -> str:
        """Save checklist to file"""
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            output_file = os.path.join(
                self.checklists_dir, 
                f"checklist-{checklist.checklist_id}.json"
            )
        
        # Convert to serializable format
        checklist_dict = {
            'checklist_id': checklist.checklist_id,
            'report_file': checklist.report_file,
            'violations': [asdict(v) for v in checklist.violations],
            'tasks': [asdict(t) for t in checklist.tasks],
            'items': [self._serialize_item(item) for item in checklist.items],
            'semantic_compliance': checklist.semantic_compliance,
            'completion_rate': checklist.completion_rate,
            'verification_rate': checklist.verification_rate,
            'overall_score': checklist.overall_score,
            'created_at': checklist.created_at,
            'updated_at': checklist.updated_at
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(checklist_dict, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def _deserialize_item(self, item_dict: Dict) -> ImplementationItem:
        """Deserialize dict to ImplementationItem"""
        return ImplementationItem(
            item_id=item_dict['item_id'],
            name=item_dict['name'],
            type=ItemType(item_dict['type']) if isinstance(item_dict['type'], str) else item_dict['type'],
            priority=Severity(item_dict['priority']) if isinstance(item_dict['priority'], str) else item_dict['priority'],
            status=ItemStatus(item_dict['status']) if isinstance(item_dict['status'], str) else item_dict['status'],
            required_files=item_dict.get('required_files', []),
            required_events=item_dict.get('required_events', []),
            required_artifacts=item_dict.get('required_artifacts', []),
            requires_hash=item_dict.get('requires_hash', False),
            requires_sealing=item_dict.get('requires_sealing', False),
            file_exists=item_dict.get('file_exists', False),
            event_stream_ok=item_dict.get('event_stream_ok', False),
            artifact_ok=item_dict.get('artifact_ok', False),
            hash_ok=item_dict.get('hash_ok', False),
            sealing_ok=item_dict.get('sealing_ok', False),
            violation_id=item_dict.get('violation_id'),
            task_id=item_dict.get('task_id'),
            created_at=item_dict.get('created_at', ''),
            updated_at=item_dict.get('updated_at', ''),
            notes=item_dict.get('notes', '')
        )
    
    def load_checklist(self, checklist_file: str) -> ImplementationChecklist:
        """Load checklist from file"""
        
        with open(checklist_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        violations = [Violation(**v) for v in data.get('violations', [])]
        tasks = [Task(**t) for t in data.get('tasks', [])]
        items = [self._deserialize_item(item) for item in data.get('items', [])]
        
        return ImplementationChecklist(
            checklist_id=data['checklist_id'],
            report_file=data['report_file'],
            violations=violations,
            tasks=tasks,
            items=items,
            semantic_compliance=data['semantic_compliance'],
            completion_rate=data['completion_rate'],
            verification_rate=data['verification_rate'],
            overall_score=data['overall_score'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
    
    def generate_markdown_report(self, checklist: ImplementationChecklist) -> str:
        """Generate markdown report from checklist"""
        
        lines = []
        lines.append("# Implementation Checklist Report\n")
        lines.append(f"**Report:** `{checklist.report_file}`\n")
        lines.append(f"**Generated:** {checklist.created_at}\n")
        lines.append("---\n")
        
        # Summary
        lines.append("## Summary\n")
        lines.append(f"- **Violations:** {len(checklist.violations)}")
        lines.append(f"- **Tasks:** {len(checklist.tasks)}")
        lines.append(f"- **Implementation Items:** {len(checklist.items)}")
        lines.append(f"- **Semantic Compliance:** {checklist.semantic_compliance:.1f}/100")
        lines.append(f"- **Completion Rate:** {checklist.completion_rate:.1f}%")
        lines.append(f"- **Verification Rate:** {checklist.verification_rate:.1f}%")
        lines.append(f"- **Overall Score:** {checklist.overall_score:.1f}/100\n")
        
        # Status by severity
        lines.append("## Status by Severity\n")
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
            items = [i for i in checklist.items if i.priority == severity]
            if items:
                completed = sum(1 for i in items if i.status in [ItemStatus.COMPLETED, ItemStatus.VERIFIED])
                lines.append(f"### {severity.value}")
                lines.append(f"- Total: {len(items)}")
                lines.append(f"- Completed: {completed}")
                lines.append(f"- Pending: {len(items) - completed}\n")
        
        # Implementation Items
        lines.append("## Implementation Items\n")
        
        # Group by status
        pending_items = [i for i in checklist.items if i.status == ItemStatus.PENDING]
        in_progress_items = [i for i in checklist.items if i.status == ItemStatus.IN_PROGRESS]
        completed_items = [i for i in checklist.items if i.status == ItemStatus.COMPLETED]
        verified_items = [i for i in checklist.items if i.status == ItemStatus.VERIFIED]
        
        if pending_items:
            lines.append("### ⏸️ Pending Items\n")
            for item in pending_items:
                lines.append(f"#### {item.item_id}: {item.name}")
                lines.append(f"- **Type:** {item.type.value if isinstance(item.type, ItemType) else item.type}")
                lines.append(f"- **Priority:** {item.priority.value if isinstance(item.priority, Severity) else item.priority}")
                lines.append(f"- **Required Files:** {', '.join(item.required_files) if item.required_files else 'None'}")
                lines.append(f"- **Notes:** {item.notes}\n")
        
        if in_progress_items:
            lines.append("### 🔄 In Progress Items\n")
            for item in in_progress_items:
                lines.append(f"#### {item.item_id}: {item.name}")
                lines.append(f"- **Type:** {item.type.value if isinstance(item.type, ItemType) else item.type}")
                lines.append(f"- **Priority:** {item.priority.value if isinstance(item.priority, Severity) else item.priority}\n")
        
        if completed_items:
            lines.append("### ✅ Completed Items\n")
            for item in completed_items:
                lines.append(f"#### {item.item_id}: {item.name}")
                lines.append(f"- **Type:** {item.type.value if isinstance(item.type, ItemType) else item.type}")
                lines.append(f"- File Exists: {'✅' if item.file_exists else '❌'}")
                lines.append(f"- Event Stream: {'✅' if item.event_stream_ok else '❌'}")
                lines.append(f"- Artifact: {'✅' if item.artifact_ok else '❌'}")
                lines.append(f"- Hash: {'✅' if item.hash_ok else '❌'}\n")
        
        if verified_items:
            lines.append("### 🎯 Verified Items\n")
            for item in verified_items:
                lines.append(f"#### {item.item_id}: {item.name}")
                lines.append(f"- **Type:** {item.type.value if isinstance(item.type, ItemType) else item.type}")
                lines.append(f"- File Exists: ✅")
                lines.append(f"- Event Stream: ✅")
                lines.append(f"- Artifact: ✅")
                lines.append(f"- Hash: ✅")
                lines.append(f"- Sealing: {'✅' if item.sealing_ok else '⏸️ (Era-1)'}\n")
        
        # Verification Matrix
        lines.append("## Verification Matrix\n")
        lines.append("| Item ID | Type | Priority | Status | File | Events | Artifact | Hash | Sealing |")
        lines.append("|---------|------|----------|--------|------|--------|----------|------|---------|")
        for item in checklist.items:
            status_symbol = {
                ItemStatus.PENDING: "⏸️",
                ItemStatus.IN_PROGRESS: "🔄",
                ItemStatus.COMPLETED: "✅",
                ItemStatus.VERIFIED: "🎯"
            }.get(item.status, "❓")
            
            lines.append(
                f"| {item.item_id} | {item.type.value if isinstance(item.type, ItemType) else item.type} | {item.priority.value if isinstance(item.priority, Severity) else item.priority} | "
                f"{status_symbol} | {'✅' if item.file_exists else '❌'} | "
                f"{'✅' if item.event_stream_ok else '❌'} | "
                f"{'✅' if item.artifact_ok else '❌'} | "
                f"{'✅' if item.hash_ok else '❌'} | "
                f"{'✅' if item.sealing_ok else '⏸️'} |"
            )
        lines.append("\n")
        
        # Recommendations
        lines.append("## Recommendations\n")
        
        critical_pending = [i for i in checklist.items 
                           if i.priority == Severity.CRITICAL and i.status == ItemStatus.PENDING]
        if critical_pending:
            lines.append("### 🔴 Critical Priority")
            lines.append(f"**{len(critical_pending)} critical items pending:**\n")
            for item in critical_pending[:5]:  # Show first 5
                lines.append(f"- {item.item_id}: {item.name}")
            if len(critical_pending) > 5:
                lines.append(f"- ... and {len(critical_pending) - 5} more\n")
        
        return "\n".join(lines)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Semantic-Driven Governance Executor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate checklist from report
  python semantic_driven_executor.py --report reports/example.md --generate-checklist
  
  # Verify existing implementation
  python semantic_driven_executor.py --checklist .governance/checklists/checklist-XXX.json --verify-implementation
  
  # Full workflow
  python semantic_driven_executor.py --report reports/example.md --generate-checklist --verify-implementation --output reports/implementation-report.md
        """
    )
    
    parser.add_argument("--report", help="Report file to analyze")
    parser.add_argument("--checklist", help="Existing checklist file to verify")
    parser.add_argument("--violations", help="Violations file (JSON)")
    parser.add_argument("--tasks", help="Tasks file (JSON)")
    parser.add_argument("--generate-checklist", action="store_true", help="Generate implementation checklist")
    parser.add_argument("--verify-implementation", action="store_true", help="Verify implementation artifacts")
    parser.add_argument("--output", help="Output report file")
    parser.add_argument("--workspace", default="/workspace", help="Workspace directory")
    
    args = parser.parse_args()
    
    executor = SemanticDrivenExecutor(args.workspace)
    
    if args.checklist and os.path.exists(args.checklist):
        print(f"\n🔍 Loading checklist: {args.checklist}")
        checklist = executor.load_checklist(args.checklist)
        print(f"✅ Loaded {len(checklist.items)} items")
    
    elif args.violations and args.tasks:
        print(f"\n🔍 Loading violations and tasks...")
        
        with open(args.violations, 'r') as f:
            violations_data = json.load(f)
        with open(args.tasks, 'r') as f:
            tasks_data = json.load(f)
        
        violations = [Violation(**v) for v in violations_data]
        tasks = [Task(**t) for t in tasks_data]
        
        checklist = executor.generate_implementation_checklist(
            violations, tasks, 
            args.report or "unknown"
        )
        print(f"✅ Generated checklist with {len(checklist.items)} items")
    
    else:
        print("❌ Please provide either --checklist or both --violations and --tasks")
        parser.print_help()
        sys.exit(1)
    
    if args.verify_implementation:
        print(f"\n🔍 Verifying implementation artifacts...")
        checklist = executor.verify_implementation(checklist)
        print(f"✅ Verification complete")
        print(f"   Completion Rate: {checklist.completion_rate:.1f}%")
        print(f"   Verification Rate: {checklist.verification_rate:.1f}%")
        print(f"   Overall Score: {checklist.overall_score:.1f}/100")
    
    if args.output:
        # Save JSON
        json_file = executor.save_checklist(checklist, args.output + ".json")
        print(f"✅ Saved checklist to {json_file}")
        
        # Generate markdown report
        markdown_report = executor.generate_markdown_report(checklist)
        md_file = args.output
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_report)
        print(f"✅ Saved markdown report to {md_file}")
    else:
        # Print summary
        print(f"\n{'='*80}")
        print(f"📊 Checklist Summary")
        print(f"{'='*80}")
        print(f"Report: {checklist.report_file}")
        print(f"Items: {len(checklist.items)}")
        print(f"Semantic Compliance: {checklist.semantic_compliance:.1f}/100")
        print(f"Completion Rate: {checklist.completion_rate:.1f}%")
        print(f"Verification Rate: {checklist.verification_rate:.1f}%")
        print(f"Overall Score: {checklist.overall_score:.1f}/100")
        print(f"{'='*80}\n")

if __name__ == "__main__":
    main()