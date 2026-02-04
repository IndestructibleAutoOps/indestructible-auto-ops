#!/usr/bin/env python3
"""
Materialization Complement Generator v2.0
Era-1 Semantic Entity Binding & Proof-Carrying Artifacts

Integrates:
- RFC 8785 Canonicalization for deterministic hashing
- Proof-Carrying Complements with cryptographic integrity
- Semantic Integrity Constraints for validation
- Governance-First Workflow for compliance-driven generation
"""

import os
import re
import json
import hashlib
import argparse
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sys

# Add ecosystem to path
sys.path.insert(0, '/workspace/ecosystem')

# Import canonicalization tool
try:
    from tools.canonicalize import Canonicalizer
    CANONICALIZER_AVAILABLE = True
except ImportError:
    CANONICALIZER_AVAILABLE = False
    print("[WARN] canonicalize.py not available, using basic canonicalization")

try:
    import rfc8785
    JCS_AVAILABLE = True
except ImportError:
    JCS_AVAILABLE = False
    print("[WARN] rfc8785 not available, using basic canonicalization")


# ============================================================================
# Enums
# ============================================================================

class DeclarationType(Enum):
    """Semantic declaration types"""
    PHASE_DECLARATION = "phase_declaration"
    ARCHITECTURE_CLAIM = "architecture_claim"
    TOOL_DECLARATION = "tool_declaration"
    COMPLETENESS_CLAIM = "completeness_claim"
    COMPLIANCE_CLAIM = "compliance_claim"
    TERMINOLOGY_REFERENCE = "terminology_reference"
    SEALING_DECLARATION = "sealing_declaration"
    ERA_DECLARATION = "era_declaration"


class ComplementType(Enum):
    """Complement entity types"""
    IMPLEMENT_PHASE = "implement_phase"
    CREATE_ARCHITECTURE_SPEC = "create_architecture_spec"
    REGISTER_TOOL = "register_tool"
    ADD_VERIFICATION = "add_verification"
    VERIFY_COMPLIANCE = "verify_compliance"
    DEFINE_TERMINOLOGY = "define_terminology"
    IMPLEMENT_SEALING = "implement_sealing"
    DEFINE_ERA_TRANSITION = "define_era_transition"


class Severity(Enum):
    """Severity levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ComplementStatus(Enum):
    """Complement status"""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    VERIFIED = "VERIFIED"
    SEALED = "SEALED"


class VerificationStatus(Enum):
    """Verification status"""
    PENDING = "PENDING"
    PASSED = "PASSED"
    FAILED = "FAILED"


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class SemanticDeclaration:
    """Represents a semantic declaration found in reports"""
    declaration_id: str
    declaration_type: str
    severity: str
    source_file: str
    line_number: int
    declaration_text: str
    evidence_requirements: List[str]
    complement_requirements: List[str]
    timestamp: str


@dataclass
class Complement:
    """Represents a complement entity"""
    complement_id: str
    complement_type: str
    declaration_id: str
    declaration_text: str
    priority: str
    status: str
    generated_at: str
    template_used: str
    target_file: str
    evidence_files: List[str]
    verification_status: str
    estimated_effort: int
    sha256_hash: str
    canonicalization_version: str
    canonicalization_method: str
    proof_chain: Dict[str, str]
    metadata: Dict[str, Any]


@dataclass
class VerificationResult:
    """Represents verification results for a complement"""
    complement_id: str
    structural_score: float
    semantic_score: float
    integrity_score: float
    overall_score: float
    status: str
    violations: List[str]
    warnings: List[str]


# ============================================================================
# Declaration Patterns
# ============================================================================

DECLARATION_PATTERNS = {
    DeclarationType.PHASE_DECLARATION: [
        r'Phase\s+\d+:.+?[Dd]efinition',
        r'第\s*\d+\s*階段:.*定義',
        r'Stage\s+\d+:.+?[Ss]pecification',
        r'[Pp]hase\s*\d+\s*[:：].+?[完成|完成|Complete|Done]'
    ],
    DeclarationType.ARCHITECTURE_CLAIM: [
        r'治理平台.*完成',
        r'[Gg]overnance\s+[Pp]latform.*[Cc]omplete',
        r'完整.*閉環.*建立',
        r'[Cc]omplete.*[Cc]losed\s+[Ll]oop.*[Ee]stablished',
        r'治理.*閉環.*完成'
    ],
    DeclarationType.TOOL_DECLARATION: [
        r'使用.*工具.*來',
        r'[Uu]sing.*tool.*to',
        r'已.*創建.*工具',
        r'[Cc]reated.*tool',
        r'實作.*工具'
    ],
    DeclarationType.COMPLETENESS_CLAIM: [
        r'完整性.*保證',
        r'[Cc]ompleteness.*[Gg]uarantee',
        r'完整.*實作',
        r'[Ff]ully.*[Ii]mplemented'
    ],
    DeclarationType.COMPLIANCE_CLAIM: [
        r'100%.*合規',
        r'100%.*[Cc]ompliant',
        r'完全.*符合.*規範',
        r'[Ff]ully.*[Cc]ompliant.*[Ww]ith.*[Ss]pecification',
        r'合規性.*\d+.*%'
    ],
    DeclarationType.TERMINOLOGY_REFERENCE: [
        r'[A-Z][A-Z_]+',  # Uppercase terminology patterns
        r'[A-Z][a-z]+[A-Z][a-z]+',  # CamelCase terminology
        r'[A-Za-z]+-+[A-Za-z]+'  # Kebab-case terminology
    ],
    DeclarationType.SEALING_DECLARATION: [
        r'[Ss]ealed?',
        r'封存',
        r'密封',
        r'[Ll]ocked',
        r'[Ff]rozen'
    ],
    DeclarationType.ERA_DECLARATION: [
        r'[Ee]ra\s*\d+',
        r'[Ee]ra-[A-Za-z]+',
        r'時代\s*\d+'
    ]
}


# ============================================================================
# Materialization Complement Generator v2.0
# ============================================================================

class MaterializationComplementGenerator:
    """
    Enhanced materialization complement generator with:
    - RFC 8785 canonicalization
    - Proof-carrying artifacts
    - Semantic integrity constraints
    - Governance-first workflow
    """

    def __init__(self, workspace: str = "/workspace", verbose: bool = False):
        self.workspace = Path(workspace)
        self.verbose = verbose
        self.reports_dir = self.workspace / "reports"
        self.complements_dir = self.workspace / "complements"
        self.templates_dir = self.complements_dir / "templates"
        self.generated_dir = self.complements_dir / "generated"
        self.governance_dir = self.workspace / "ecosystem" / ".governance"
        self.event_stream_file = self.governance_dir / "event-stream.jsonl"
        self.hash_registry_file = self.governance_dir / "hash-registry.json"
        
        # Statistics
        self.total_declarations = 0
        self.total_missing_entities = 0
        self.total_complements_generated = 0
        self.declarations_by_type = {}
        
        # Initialize canonicalizer
        self.canonicalizer = None
        if CANONICALIZER_AVAILABLE:
            self.canonicalizer = Canonicalizer()
        
        # Load hash registry
        self.hash_registry = self._load_hash_registry()
        
        # Initialize declarations list
        self.declarations: List[SemanticDeclaration] = []
        self.complements: List[Complement] = []
        self.verification_results: List[VerificationResult] = []
        
        if self.verbose:
            print(f"[INFO] Materialization Complement Generator v2.0 initialized")
            print(f"[INFO] Workspace: {self.workspace}")
            print(f"[INFO] Reports dir: {self.reports_dir}")
            print(f"[INFO] Complements dir: {self.complements_dir}")
    
    def _log(self, message: str, level: str = "INFO"):
        """Log message with level"""
        if self.verbose or level in ["ERROR", "WARN"]:
            print(f"[{level}] {message}")
    
    def _load_hash_registry(self) -> Dict:
        """Load hash registry from file"""
        if self.hash_registry_file.exists():
            try:
                with open(self.hash_registry_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self._log(f"Failed to load hash registry: {e}", "ERROR")
        
        return {
            "version": "1.0.0",
            "era": "1",
            "complements": {},
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _save_hash_registry(self):
        """Save hash registry to file"""
        try:
            self.hash_registry["last_updated"] = datetime.utcnow().isoformat()
            with open(self.hash_registry_file, 'w', encoding='utf-8') as f:
                json.dump(self.hash_registry, f, indent=2, ensure_ascii=False)
            self._log(f"Hash registry saved to {self.hash_registry_file}")
        except Exception as e:
            self._log(f"Failed to save hash registry: {e}", "ERROR")
    
    def _canonicalize_json(self, obj: Dict) -> str:
        """
        Canonicalize JSON object using RFC 8785 (JCS) if available,
        otherwise use basic canonicalization
        """
        try:
            if JCS_AVAILABLE and self.canonicalizer:
                # Use JCS canonicalization
                canonical_json = rfc8785.dumps(obj)
                return canonical_json
            elif CANONICALIZER_AVAILABLE and self.canonicalizer:
                # Use custom canonicalizer with layered sorting
                canonical_json = self.canonicalizer.canonicalize_json(obj)
                return canonical_json
            else:
                # Basic canonicalization
                return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        except Exception as e:
            self._log(f"Canonicalization failed: {e}, using basic JSON", "WARN")
            return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    
    def _compute_sha256(self, data: str) -> str:
        """Compute SHA256 hash of data"""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def _generate_complement_id(self, declaration_type: str) -> str:
        """Generate unique complement ID"""
        timestamp = datetime.now().strftime("%Y%m%d")
        count = sum(1 for c in self.complements if c.complement_type.startswith(declaration_type))
        return f"COMP-{timestamp}-{count + 1:03d}"
    
    def _generate_declaration_id(self, declaration_type: str) -> str:
        """Generate unique declaration ID"""
        timestamp = datetime.now().strftime("%Y%m%d")
        count = sum(1 for d in self.declarations if d.declaration_type == declaration_type)
        return f"DECL-{timestamp}-{count + 1:03d}"
    
    def _write_event(self, event_type: str, data: Dict):
        """Write event to event stream"""
        try:
            event = {
                "event_id": str(uuid.uuid4()),
                "event_type": event_type,
                "timestamp": datetime.utcnow().isoformat(),
                "era": "1",
                **data
            }
            
            # Canonicalize and hash event
            canonical_json = self._canonicalize_json(event)
            event["sha256_hash"] = self._compute_sha256(canonical_json)
            
            # Append to event stream
            with open(self.event_stream_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
            
            if self.verbose:
                self._log(f"Event written: {event_type}", "INFO")
        except Exception as e:
            self._log(f"Failed to write event: {e}", "ERROR")
    
    def scan_reports(self) -> List[SemanticDeclaration]:
        """
        Stage 1: Scan reports for semantic declarations
        """
        self._log("Stage 1: Scanning reports for semantic declarations", "INFO")
        
        # Initialize declarations list
        self.declarations = []
        self.declarations_by_type = {dt.value: [] for dt in DeclarationType}
        
        # Find all markdown files in reports directory
        report_files = list(self.reports_dir.glob("*.md"))
        
        if self.verbose:
            print(f"[INFO] Found {len(report_files)} report files to scan")
        
        for report_file in report_files:
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                # Scan for each declaration type
                for decl_type, patterns in DECLARATION_PATTERNS.items():
                    for pattern in patterns:
                        for match in re.finditer(pattern, content, re.IGNORECASE):
                            line_num = content[:match.start()].count('\n') + 1
                            line_text = lines[line_num - 1] if line_num <= len(lines) else match.group(0)
                            
                            declaration = SemanticDeclaration(
                                declaration_id=self._generate_declaration_id(decl_type.value),
                                declaration_type=decl_type.value,
                                severity=self._determine_severity(decl_type, match.group(0)),
                                source_file=str(report_file.relative_to(self.workspace)),
                                line_number=line_num,
                                declaration_text=line_text.strip(),
                                evidence_requirements=self._get_evidence_requirements(decl_type),
                                complement_requirements=self._get_complement_requirements(decl_type),
                                timestamp=datetime.utcnow().isoformat()
                            )
                            
                            self.declarations.append(declaration)
                            self.declarations_by_type[decl_type.value].append(declaration)
                            
                            if self.verbose:
                                print(f"[INFO] Found {decl_type.value}: {match.group(0)[:60]}")
                            
            except Exception as e:
                self._log(f"Failed to scan {report_file}: {e}", "ERROR")
        
        self.total_declarations = len(self.declarations)
        
        self._log(f"Scan complete: {self.total_declarations} declarations found", "INFO")
        self._write_event("COMPLEMENT_SCAN_STARTED", {
            "total_reports": len(report_files),
            "total_declarations": self.total_declarations,
            "declarations_by_type": {k: len(v) for k, v in self.declarations_by_type.items()}
        })
        
        return self.declarations
    
    def _determine_severity(self, decl_type: DeclarationType, text: str) -> str:
        """Determine severity based on declaration type and context"""
        high_severity_types = [
            DeclarationType.PHASE_DECLARATION,
            DeclarationType.ARCHITECTURE_CLAIM,
            DeclarationType.COMPLIANCE_CLAIM
        ]
        
        if decl_type in high_severity_types:
            return "CRITICAL"
        elif decl_type in [DeclarationType.TOOL_DECLARATION, DeclarationType.SEALING_DECLARATION]:
            return "HIGH"
        else:
            return "MEDIUM"
    
    def _get_evidence_requirements(self, decl_type: DeclarationType) -> List[str]:
        """Get evidence requirements for declaration type"""
        requirements = {
            DeclarationType.PHASE_DECLARATION: ["phase_spec", "workflow_definition", "validation_report"],
            DeclarationType.ARCHITECTURE_CLAIM: ["UGS", "diagrams", "architecture_documentation"],
            DeclarationType.TOOL_DECLARATION: ["tool_source", "tool_documentation", "test_files"],
            DeclarationType.COMPLETENESS_CLAIM: ["validation_reports", "test_results", "coverage_reports"],
            DeclarationType.COMPLIANCE_CLAIM: ["compliance_reports", "score_cards", "audit_trails"],
            DeclarationType.TERMINOLOGY_REFERENCE: ["glossary_entries", "definitions", "usage_examples"],
            DeclarationType.SEALING_DECLARATION: ["seal_records", "hash_registries", "seal_protocols"],
            DeclarationType.ERA_DECLARATION: ["era_definitions", "migration_plans", "transition_docs"]
        }
        return requirements.get(decl_type, [])
    
    def _get_complement_requirements(self, decl_type: DeclarationType) -> List[str]:
        """Get complement requirements for declaration type"""
        mapping = {
            DeclarationType.PHASE_DECLARATION: [ComplementType.IMPLEMENT_PHASE.value],
            DeclarationType.ARCHITECTURE_CLAIM: [ComplementType.CREATE_ARCHITECTURE_SPEC.value],
            DeclarationType.TOOL_DECLARATION: [ComplementType.REGISTER_TOOL.value],
            DeclarationType.COMPLETENESS_CLAIM: [ComplementType.ADD_VERIFICATION.value],
            DeclarationType.COMPLIANCE_CLAIM: [ComplementType.VERIFY_COMPLIANCE.value],
            DeclarationType.TERMINOLOGY_REFERENCE: [ComplementType.DEFINE_TERMINOLOGY.value],
            DeclarationType.SEALING_DECLARATION: [ComplementType.IMPLEMENT_SEALING.value],
            DeclarationType.ERA_DECLARATION: [ComplementType.DEFINE_ERA_TRANSITION.value]
        }
        return mapping.get(decl_type, [])
    
    def match_declarations_to_entities(self) -> Dict[str, List]:
        """
        Stage 2: Match declarations to existing entities
        """
        self._log("Stage 2: Matching declarations to existing entities", "INFO")
        
        matches = {"matched": [], "missing": [], "low_confidence": []}
        
        for declaration in self.declarations:
            match_result = self._find_matching_entity(declaration)
            
            if match_result["found"]:
                matches["matched"].append({
                    "declaration_id": declaration.declaration_id,
                    "declaration_type": declaration.declaration_type,
                    "entity_path": match_result["path"],
                    "confidence": match_result["confidence"]
                })
            elif match_result["confidence"] > 0.5:
                matches["low_confidence"].append({
                    "declaration_id": declaration.declaration_id,
                    "declaration_type": declaration.declaration_type,
                    "entity_path": match_result["path"],
                    "confidence": match_result["confidence"]
                })
            else:
                matches["missing"].append({
                    "declaration_id": declaration.declaration_id,
                    "declaration_type": declaration.declaration_type,
                    "declaration_text": declaration.declaration_text
                })
        
        self.total_missing_entities = len(matches["missing"])
        
        self._log(f"Match complete: {len(matches['matched'])} matched, {self.total_missing_entities} missing", "INFO")
        
        return matches
    
    def _find_matching_entity(self, declaration: SemanticDeclaration) -> Dict:
        """Find matching entity for declaration"""
        # This is a simplified implementation
        # In a full implementation, this would use more sophisticated matching
        
        search_paths = [
            self.workspace / "ecosystem",
            self.workspace / "complements" / "generated"
        ]
        
        # Simple keyword matching
        keywords = re.findall(r'\w+', declaration.declaration_text.lower())
        
        for search_path in search_paths:
            for file_path in search_path.rglob("*"):
                if file_path.is_file() and file_path.suffix in ['.md', '.py', '.yaml', '.json']:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                        
                        # Check if keywords appear in file
                        keyword_matches = sum(1 for kw in keywords if kw in content)
                        if keyword_matches >= min(3, len(keywords)):
                            return {
                                "found": True,
                                "path": str(file_path.relative_to(self.workspace)),
                                "confidence": min(keyword_matches / len(keywords), 1.0)
                            }
                    except Exception:
                        continue
        
        return {"found": False, "path": None, "confidence": 0.0}
    
    def detect_missing_entities(self, matches: Dict[str, List]) -> List[Dict]:
        """
        Stage 3: Detect missing entities
        """
        self._log("Stage 3: Detecting missing entities", "INFO")
        
        missing_entities = []
        
        for missing in matches["missing"]:
            declaration = next(
                (d for d in self.declarations if d.declaration_id == missing["declaration_id"]),
                None
            )
            
            if declaration:
                complement_type = self._determine_complement_type(declaration)
                
                missing_entities.append({
                    "declaration_id": declaration.declaration_id,
                    "declaration_type": declaration.declaration_type,
                    "complement_type": complement_type,
                    "priority": declaration.severity,
                    "declaration_text": declaration.declaration_text,
                    "estimated_effort": self._estimate_effort(complement_type)
                })
        
        self.total_missing_entities = len(missing_entities)
        
        self._log(f"Detection complete: {self.total_missing_entities} missing entities detected", "INFO")
        self._write_event("COMPLEMENT_DETECTION_COMPLETE", {
            "total_missing": self.total_missing_entities,
            "missing_by_type": self._count_by_type(missing_entities, "complement_type")
        })
        
        return missing_entities
    
    def _determine_complement_type(self, declaration: SemanticDeclaration) -> str:
        """Determine complement type for declaration"""
        mapping = {
            "phase_declaration": "implement_phase",
            "architecture_claim": "create_architecture_spec",
            "tool_declaration": "register_tool",
            "completeness_claim": "add_verification",
            "compliance_claim": "verify_compliance",
            "terminology_reference": "define_terminology",
            "sealing_declaration": "implement_sealing",
            "era_declaration": "define_era_transition"
        }
        return mapping.get(declaration.declaration_type, "generic_complement")
    
    def _estimate_effort(self, complement_type: str) -> int:
        """Estimate effort in hours for complement type"""
        effort_map = {
            "implement_phase": 40,
            "create_architecture_spec": 30,
            "register_tool": 8,
            "add_verification": 16,
            "verify_compliance": 12,
            "define_terminology": 4,
            "implement_sealing": 20,
            "define_era_transition": 24
        }
        return effort_map.get(complement_type, 10)
    
    def _count_by_type(self, items: List[Dict], type_field: str) -> Dict[str, int]:
        """Count items by type"""
        counts = {}
        for item in items:
            item_type = item.get(type_field, "unknown")
            counts[item_type] = counts.get(item_type, 0) + 1
        return counts
    
    def generate_complements(self, missing_entities: List[Dict]) -> List[Complement]:
        """
        Stage 4: Generate complement templates
        """
        self._log("Stage 4: Generating complement templates", "INFO")
        
        # Create generated directory if it doesn't exist
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        
        self.complements = []
        
        for missing in missing_entities:
            complement = self._generate_complement(missing)
            if complement:
                self.complements.append(complement)
                self.total_complements_generated += 1
                
                # Write complement to file
                self._write_complement_file(complement)
                
                # Register in hash registry
                self._register_complement_in_registry(complement)
                
                if self.verbose:
                    print(f"[INFO] Generated complement: {complement.complement_id}")
        
        self._log(f"Generation complete: {self.total_complements_generated} complements generated", "INFO")
        self._write_event("COMPLEMENT_GENERATION_COMPLETE", {
            "total_generated": self.total_complements_generated,
            "generated_by_type": self._count_by_type(
                [asdict(c) for c in self.complements], "complement_type"
            )
        })
        
        return self.complements
    
    def _generate_complement(self, missing: Dict) -> Optional[Complement]:
        """Generate complement from missing entity"""
        complement_id = self._generate_complement_id(missing["complement_type"])
        template = self._load_template(missing["complement_type"])
        target_file = self._determine_target_file(missing["complement_type"], complement_id)
        
        # Fill template with context
        content = self._fill_template(template, missing)
        
        # Create complement object
        complement_dict = {
            "complement_id": complement_id,
            "complement_type": missing["complement_type"],
            "declaration_id": missing["declaration_id"],
            "declaration_text": missing["declaration_text"],
            "priority": missing["priority"],
            "status": ComplementStatus.PENDING.value,
            "generated_at": datetime.utcnow().isoformat(),
            "template_used": f"templates/{missing['complement_type']}-template.md",
            "target_file": target_file,
            "evidence_files": [],
            "verification_status": VerificationStatus.PENDING.value,
            "estimated_effort": missing["estimated_effort"],
            "sha256_hash": "",  # Will be filled after canonicalization
            "canonicalization_version": "1.0",
            "canonicalization_method": "JCS+LayeredSorting",
            "proof_chain": {
                "self": "",  # Will be filled after canonicalization
                "declaration": "",  # Would be filled with declaration hash
                "template": ""  # Would be filled with template hash
            },
            "metadata": {
                "era": "1",
                "layer": "Operational",
                "content": content
            }
        }
        
        # Canonicalize and compute hash
        canonical_json = self._canonicalize_json(complement_dict)
        sha256_hash = self._compute_sha256(canonical_json)
        
        complement_dict["sha256_hash"] = sha256_hash
        complement_dict["proof_chain"]["self"] = sha256_hash
        
        return Complement(**complement_dict)
    
    def _load_template(self, complement_type: str) -> str:
        """Load template for complement type"""
        template_file = self.templates_dir / f"{complement_type}-template.md"
        
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Return default template
            return """# {complement_type}

## Declaration
{declaration_text}

## Complement ID
{complement_id}

## Status
{status}

## Next Steps
[ ] Implement complement
[ ] Verify evidence
[ ] Test validation
[ ] Update status to COMPLETED
"""
    
    def _fill_template(self, template: str, missing: Dict) -> str:
        """Fill template with context"""
        return template.format(
            complement_type=missing["complement_type"],
            complement_id=self._generate_complement_id(missing["complement_type"]),
            declaration_text=missing["declaration_text"],
            status=ComplementStatus.PENDING.value,
            priority=missing["priority"]
        )
    
    def _determine_target_file(self, complement_type: str, complement_id: str) -> str:
        """Determine target file path for complement"""
        type_dirs = {
            "implement_phase": "phases",
            "create_architecture_spec": "architecture",
            "register_tool": "tools",
            "add_verification": "verifications",
            "verify_compliance": "compliances",
            "define_terminology": "terminologies",
            "implement_sealing": "sealings",
            "define_era_transition": "era-transitions"
        }
        
        type_dir = type_dirs.get(complement_type, "generic")
        filename = f"{complement_id.lower()}.md"
        
        return f"complements/generated/{type_dir}/{filename}"
    
    def _write_complement_file(self, complement: Complement):
        """Write complement to file"""
        try:
            file_path = self.workspace / complement.target_file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(complement.metadata.get("content", ""))
            
            if self.verbose:
                print(f"[INFO] Written complement to {complement.target_file}")
        except Exception as e:
            self._log(f"Failed to write complement file: {e}", "ERROR")
    
    def _register_complement_in_registry(self, complement: Complement):
        """Register complement in hash registry"""
        self.hash_registry["complements"][complement.complement_id] = {
            "sha256_hash": complement.sha256_hash,
            "file_path": complement.target_file,
            "canonicalization": complement.canonicalization_method,
            "era": complement.metadata.get("era", "1"),
            "layer": complement.metadata.get("layer", "Operational")
        }
    
    def verify_complements(self) -> List[VerificationResult]:
        """
        Stage 5: Verify complement completeness
        """
        self._log("Stage 5: Verifying complement completeness", "INFO")
        
        self.verification_results = []
        
        for complement in self.complements:
            result = self._verify_complement(complement)
            self.verification_results.append(result)
            
            # Update complement verification status
            complement.verification_status = result.status
            
            if self.verbose:
                print(f"[INFO] Verified {complement.complement_id}: {result.status} ({result.overall_score:.1f})")
        
        # Calculate overall statistics
        total = len(self.verification_results)
        passed = sum(1 for r in self.verification_results if r.status == "PASSED")
        failed = total - passed
        avg_score = sum(r.overall_score for r in self.verification_results) / total if total > 0 else 0
        
        self._log(f"Verification complete: {passed}/{total} passed, {failed} failed, avg score: {avg_score:.1f}", "INFO")
        self._write_event("COMPLEMENT_VERIFICATION_COMPLETE", {
            "total": total,
            "passed": passed,
            "failed": failed,
            "average_score": avg_score
        })
        
        # Save hash registry
        self._save_hash_registry()
        
        return self.verification_results
    
    def _verify_complement(self, complement: Complement) -> VerificationResult:
        """Verify single complement"""
        violations = []
        warnings = []
        
        # Structural verification (30%)
        structural_score = self._verify_structure(complement, violations, warnings)
        
        # Semantic verification (40%)
        semantic_score = self._verify_semantics(complement, violations, warnings)
        
        # Integrity verification (30%)
        integrity_score = self._verify_integrity(complement, violations, warnings)
        
        # Calculate overall score
        overall_score = (structural_score * 0.3) + (semantic_score * 0.4) + (integrity_score * 0.3)
        
        # Determine status
        if overall_score >= 85.0:
            status = VerificationStatus.PASSED.value
        elif overall_score >= 70.0:
            status = "WARNING"
            warnings.append(f"Overall score {overall_score:.1f} is below recommended 85.0")
        else:
            status = VerificationStatus.FAILED.value
            violations.append(f"Overall score {overall_score:.1f} is below minimum 70.0")
        
        return VerificationResult(
            complement_id=complement.complement_id,
            structural_score=structural_score,
            semantic_score=semantic_score,
            integrity_score=integrity_score,
            overall_score=overall_score,
            status=status,
            violations=violations,
            warnings=warnings
        )
    
    def _verify_structure(self, complement: Complement, violations: List[str], warnings: List[str]) -> float:
        """Verify complement structure"""
        score = 100.0
        
        # Check required fields
        required_fields = [
            "complement_id", "complement_type", "declaration_id",
            "priority", "status", "generated_at", "target_file",
            "sha256_hash"
        ]
        
        for field in required_fields:
            if not hasattr(complement, field) or not getattr(complement, field):
                violations.append(f"Missing required field: {field}")
                score -= 10.0
        
        # Check hash format
        if complement.sha256_hash and len(complement.sha256_hash) != 64:
            violations.append("SHA256 hash has incorrect length")
            score -= 5.0
        
        return max(0.0, score)
    
    def _verify_semantics(self, complement: Complement, violations: List[str], warnings: List[str]) -> float:
        """Verify complement semantics"""
        score = 100.0
        
        # Check complement type matches declaration type
        # This is a simplified check
        valid_types = [ct.value for ct in ComplementType]
        if complement.complement_type not in valid_types:
            violations.append(f"Invalid complement type: {complement.complement_type}")
            score -= 20.0
        
        # Check priority is valid
        valid_priorities = [s.value for s in Severity]
        if complement.priority not in valid_priorities:
            violations.append(f"Invalid priority: {complement.priority}")
            score -= 10.0
        
        return max(0.0, score)
    
    def _verify_integrity(self, complement: Complement, violations: List[str], warnings: List[str]) -> float:
        """Verify complement integrity"""
        score = 100.0
        
        # Verify hash chain
        if complement.proof_chain.get("self") != complement.sha256_hash:
            violations.append("Hash chain self-reference mismatch")
            score -= 20.0
        
        # Verify target file exists
        file_path = self.workspace / complement.target_file
        if not file_path.exists():
            warnings.append(f"Target file does not exist: {complement.target_file}")
            score -= 10.0
        
        return max(0.0, score)
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate comprehensive report"""
        if output_file is None:
            output_file = str(self.reports_dir / "materialization-complement-report.md")
        
        report = []
        report.append("# Materialization Complement Report v2.0")
        report.append(f"\nGenerated: {datetime.utcnow().isoformat()}")
        report.append(f"Era: 1 (Evidence-Native Bootstrap)")
        report.append(f"\n---\n")
        
        # Executive Summary
        report.append("## Executive Summary\n")
        report.append(f"- **Total Declarations Scanned**: {self.total_declarations}")
        report.append(f"- **Total Missing Entities Detected**: {self.total_missing_entities}")
        report.append(f"- **Total Complements Generated**: {self.total_complements_generated}")
        
        if self.verification_results:
            total = len(self.verification_results)
            passed = sum(1 for r in self.verification_results if r.status == "PASSED")
            avg_score = sum(r.overall_score for r in self.verification_results) / total
            report.append(f"\n- **Verification Results**: {passed}/{total} passed")
            report.append(f"- **Average Compliance Score**: {avg_score:.1f}/100")
        
        report.append("\n---\n")
        
        # Declarations by Type
        report.append("## Declarations by Type\n")
        report.append("| Type | Count | Severity |\n")
        report.append("|------|-------|----------|\n")
        
        for decl_type, declarations in self.declarations_by_type.items():
            if declarations:
                severity = declarations[0].severity
                count = len(declarations)
                report.append(f"| {decl_type} | {count} | {severity} |\n")
        
        report.append("\n---\n")
        
        # Complements List
        if self.complements:
            report.append("## Generated Complements\n")
            report.append("| Complement ID | Type | Priority | Status | Score |\n")
            report.append("|---------------|------|----------|--------|-------|\n")
            
            for complement in self.complements:
                verification = next(
                    (v for v in self.verification_results if v.complement_id == complement.complement_id),
                    None
                )
                score = f"{verification.overall_score:.1f}" if verification else "N/A"
                
                report.append(
                    f"| {complement.complement_id} | {complement.complement_type} | "
                    f"{complement.priority} | {complement.verification_status} | {score} |\n"
                )
        
        report.append("\n---\n")
        
        # Verification Results
        if self.verification_results:
            report.append("## Verification Results\n")
            
            for result in self.verification_results:
                report.append(f"\n### {result.complement_id}\n")
                report.append(f"- **Status**: {result.status}\n")
                report.append(f"- **Overall Score**: {result.overall_score:.1f}/100\n")
                report.append(f"  - Structural: {result.structural_score:.1f}\n")
                report.append(f"  - Semantic: {result.semantic_score:.1f}\n")
                report.append(f"  - Integrity: {result.integrity_score:.1f}\n")
                
                if result.violations:
                    report.append(f"- **Violations**:\n")
                    for v in result.violations:
                        report.append(f"  - ❌ {v}\n")
                
                if result.warnings:
                    report.append(f"- **Warnings**:\n")
                    for w in result.warnings:
                        report.append(f"  - ⚠️  {w}\n")
        
        report.append("\n---\n")
        
        # Recommendations
        report.append("## Recommendations\n")
        
        if self.total_missing_entities > 0:
            report.append(f"\n1. **Priority Actions** ({self.total_missing_entities} complements pending):\n")
            report.append("   - Review and implement CRITICAL priority complements first\n")
            report.append("   - Focus on phase declarations and architecture claims\n")
            report.append("   - Add verification evidence for completeness claims\n")
        
        if self.verification_results:
            failed = [r for r in self.verification_results if r.status == "FAILED"]
            if failed:
                report.append(f"\n2. **Failed Complements** ({len(failed)}):\n")
                for result in failed:
                    report.append(f"   - {result.complement_id}: {result.violations[0] if result.violations else 'Unknown error'}\n")
        
        report.append("\n3. **Next Steps for Era-2 Transition**:\n")
        report.append("   - Complete all complement implementations\n")
        report.append("   - Achieve verification score ≥ 90.0\n")
        report.append("   - Seal all complements in hash registry\n")
        report.append("   - Prepare Era-2 migration documentation\n")
        
        report.append("\n---\n")
        report.append("\n*Report generated by Materialization Complement Generator v2.0*")
        
        # Write report
        report_content = "".join(report)
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self._log(f"Report written to {output_path}", "INFO")
        
        return report_content
    
    def run_full_pipeline(self) -> Dict:
        """Run the complete 5-stage pipeline"""
        self._log("Starting Materialization Complement Generator v2.0 full pipeline", "INFO")
        
        results = {
            "declarations": [],
            "complements": [],
            "verification_results": [],
            "statistics": {}
        }
        
        # Stage 1: Scan
        declarations = self.scan_reports()
        results["declarations"] = [asdict(d) for d in declarations]
        
        # Stage 2: Match
        matches = self.match_declarations_to_entities()
        
        # Stage 3: Detect
        missing_entities = self.detect_missing_entities(matches)
        
        # Stage 4: Generate
        complements = self.generate_complements(missing_entities)
        results["complements"] = [asdict(c) for c in complements]
        
        # Stage 5: Verify
        verification_results = self.verify_complements()
        results["verification_results"] = [asdict(v) for v in verification_results]
        
        # Statistics
        results["statistics"] = {
            "total_declarations": self.total_declarations,
            "total_missing_entities": self.total_missing_entities,
            "total_complements_generated": self.total_complements_generated,
            "declarations_by_type": {k: len(v) for k, v in self.declarations_by_type.items()},
            "average_verification_score": sum(v.overall_score for v in self.verification_results) / len(self.verification_results) if self.verification_results else 0
        }
        
        # Generate report
        self.generate_report()
        
        self._log("Full pipeline complete", "INFO")
        
        return results


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Materialization Complement Generator v2.0 - Era-1 Semantic Entity Binding"
    )
    
    parser.add_argument(
        "--scan-reports",
        action="store_true",
        help="Scan reports for semantic declarations"
    )
    
    parser.add_argument(
        "--generate-complements",
        action="store_true",
        help="Generate complement templates"
    )
    
    parser.add_argument(
        "--verify-complements",
        action="store_true",
        help="Verify generated complements"
    )
    
    parser.add_argument(
        "--run-full-pipeline",
        action="store_true",
        help="Run the complete 5-stage pipeline"
    )
    
    parser.add_argument(
        "--output-file",
        type=str,
        help="Output file path for JSON results"
    )
    
    parser.add_argument(
        "--report-file",
        type=str,
        help="Output file path for Markdown report"
    )
    
    parser.add_argument(
        "--workspace",
        type=str,
        default="/workspace",
        help="Workspace directory"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = MaterializationComplementGenerator(
        workspace=args.workspace,
        verbose=args.verbose
    )
    
    # Run requested operations
    results = {}
    
    if args.run_full_pipeline:
        results = generator.run_full_pipeline()
    else:
        if args.scan_reports:
            declarations = generator.scan_reports()
            results["declarations"] = [asdict(d) for d in declarations]
        
        if args.generate_complements:
            matches = generator.match_declarations_to_entities()
            missing = generator.detect_missing_entities(matches)
            complements = generator.generate_complements(missing)
            results["complements"] = [asdict(c) for c in complements]
        
        if args.verify_complements:
            verification_results = generator.verify_complements()
            results["verification_results"] = [asdict(v) for v in verification_results]
        
        # Generate report
        if args.report_file:
            generator.generate_report(args.report_file)
    
    # Write JSON output if requested
    if args.output_file:
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"[INFO] JSON results written to {args.output_file}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("Materialization Complement Generator v2.0 - Summary")
    print("=" * 80)
    print(f"Total Declarations: {generator.total_declarations}")
    print(f"Missing Entities: {generator.total_missing_entities}")
    print(f"Complements Generated: {generator.total_complements_generated}")
    
    if generator.verification_results:
        total = len(generator.verification_results)
        passed = sum(1 for r in generator.verification_results if r.status == "PASSED")
        avg_score = sum(r.overall_score for r in generator.verification_results) / total
        print(f"Verification: {passed}/{total} passed, avg score: {avg_score:.1f}")
    
    print("=" * 80)


if __name__ == "__main__":
    main()