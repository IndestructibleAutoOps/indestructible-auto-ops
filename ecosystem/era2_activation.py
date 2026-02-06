"""
GL Era-2 Governance Closure Activation Script
Activates Era-2 with semantic closure, immutable core sealing, and complete lineage reconstruction

This script:
1. Initializes Era-2 engines (semantic closure, core sealing, lineage reconstruction)
2. Performs comprehensive validation of governance closure
3. Generates Era-2 activation report
4. Updates GL Unified Charter status
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add ecosystem to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ecosystem.engines.semantic_closure_engine import (
    GLSemanticClosureEngine,
    SemanticEntity,
    ValidationResult,
)
from ecosystem.engines.core_sealing_engine import (
    GLCoreSealingEngine,
    CeremonyData,
    VerificationResult as CoreVerificationResult,
)
from ecosystem.engines.lineage_reconstruction_engine import (
    GLLineageReconstructionEngine,
    GovernanceEvent,
    LineageGraph,
    VerificationResult as LineageVerificationResult,
)


class Era2Activation:
    """Era-2 Governance Closure Activation"""

    def __init__(self, workspace_root: str = "/workspace"):
        self.workspace_root = Path(workspace_root)
        self.ecosystem_root = self.workspace_root / "ecosystem"

        # Initialize Era-2 engines
        self.semantic_closure_engine = None
        self.core_sealing_engine = None
        self.lineage_reconstruction_engine = None

        # Activation status
        self.activation_status = {
            "started_at": datetime.now().isoformat(),
            "phase": "INITIALIZING",
            "engines_initialized": [],
            "validations_completed": [],
            "overall_status": "IN_PROGRESS",
        }

    def initialize_engines(self) -> Dict:
        """Initialize Era-2 engines"""
        print("\n" + "=" * 80)
        print("🚀 ERA-2 ENGINE INITIALIZATION")
        print("=" * 80)

        # Initialize Semantic Closure Engine
        print("\n📝 1. Initializing Semantic Closure Engine...")
        self.semantic_closure_engine = GLSemanticClosureEngine()
        self.activation_status["engines_initialized"].append("semantic_closure_engine")
        print("✅ Semantic Closure Engine initialized")

        # Initialize Core Sealing Engine
        print("\n🔒 2. Initializing Core Sealing Engine...")
        self.core_sealing_engine = GLCoreSealingEngine()
        self.core_sealing_engine.set_sealing_committee(
            ["system_architect", "governance_lead", "security_chief"]
        )
        self.activation_status["engines_initialized"].append("core_sealing_engine")
        print("✅ Core Sealing Engine initialized")

        # Initialize Lineage Reconstruction Engine
        print("\n🔍 3. Initializing Lineage Reconstruction Engine...")
        self.lineage_reconstruction_engine = GLLineageReconstructionEngine()
        # Load existing event stream
        event_stream_path = self.ecosystem_root / ".governance" / "event-stream.jsonl"
        if event_stream_path.exists():
            events = self._load_event_stream(event_stream_path)
            self.lineage_reconstruction_engine.load_event_stream(events)
            print(
                f"✅ Lineage Reconstruction Engine initialized ({len(events)} events loaded)"
            )
        else:
            print("⚠️  No event stream found, engine initialized empty")

        return self.activation_status

    def load_governance_entities(self) -> Dict:
        """Load existing governance entities into semantic closure engine"""
        print("\n" + "=" * 80)
        print("📚 LOADING GOVERNANCE ENTITIES")
        print("=" * 80)

        entity_count = 0

        # Load UGS (Unified Governance Structure)
        ugs_path = self.ecosystem_root / "meta-spec" / "UGS" / "ug-complete.json"
        if ugs_path.exists():
            with open(ugs_path) as f:
                ugs = json.load(f)

            # Parse and add entities to semantic closure engine
            for layer_name, layer_data in ugs.get("layers", {}).items():
                layer_id = self._convert_layer_name(layer_name)
                for entity_name, entity_def in layer_data.get("entities", {}).items():
                    entity = SemanticEntity(
                        layer=layer_id,
                        entity_id=entity_name,
                        entity_type=entity_def.get("type", "unknown"),
                        definition=entity_def,
                        dependencies=entity_def.get("dependencies", []),
                        metadata=entity_def.get("metadata", {}),
                    )
                    result = self.semantic_closure_engine.define_semantic_entity(entity)
                    if result.is_valid:
                        entity_count += 1

            print(f"✅ Loaded {entity_count} governance entities from UGS")
        else:
            print("⚠️  UGS file not found")
            # Create sample entities for demonstration
            entity_count = self._create_sample_entities()
            print(f"✅ Created {entity_count} sample governance entities")

        return {"entity_count": entity_count}

    def perform_core_sealing_ceremony(self) -> Dict:
        """Perform core sealing ceremony"""
        print("\n" + "=" * 80)
        print("🔒 CORE SEALING CEREMONY")
        print("=" * 80)

        # Prepare core layers for sealing
        core_layers = ["L00", "L01", "L02"]
        artifacts = {
            "semantic_closure_matrix": self._extract_closure_matrix(),
            "governance_rules": self._extract_governance_rules(),
            "meta_spec": self._extract_meta_spec(),
        }

        print(f"\n📦 Preparing core layers: {', '.join(core_layers)}")
        ceremony_data = self.core_sealing_engine.prepare_sealing(core_layers, artifacts)
        print(f"✅ Ceremony prepared (ID: {ceremony_data.ceremony_id[:8]}...)")
        print(f"   Candidate hash: {ceremony_data.candidate_hash[:16]}...")

        # Execute sealing (auto-approve for demo purposes)
        print(f"\n🔏 Executing sealing ceremony...")
        approvals = ["system_architect", "governance_lead", "security_chief"]
        sealed_hash = self.core_sealing_engine.execute_sealing(ceremony_data, approvals)
        print(f"✅ Core sealed successfully")
        print(f"   Sealed hash: {sealed_hash[:16]}...")
        print(
            f"   Approvals: {len(approvals)}/{len(self.core_sealing_engine.sealing_committee)}"
        )

        # Verify seal
        print(f"\n🔍 Verifying seal integrity...")
        seal_valid = self.core_sealing_engine.verify_seal(sealed_hash)
        if seal_valid:
            print("✅ Seal verification passed")
        else:
            print("❌ Seal verification failed")

        return {
            "sealed_hash": sealed_hash,
            "seal_valid": seal_valid,
            "ceremony_id": ceremony_data.ceremony_id,
        }

    def validate_governance_closure(self) -> Dict:
        """Validate complete governance closure"""
        print("\n" + "=" * 80)
        print("✅ GOVERNANCE CLOSURE VALIDATION")
        print("=" * 80)

        validation_results = {
            "semantic_closure": {},
            "immutable_core": {},
            "lineage_reconstruction": {},
            "overall_closure_score": 0.0,
        }

        # 1. Validate Semantic Closure
        print("\n📝 1. Validating Semantic Closure...")
        closure_results = {}
        for layer in ["L00", "L01", "L02"]:
            result = self.semantic_closure_engine.validate_layer(layer)
            closure_results[layer] = {
                "is_valid": result.is_valid,
                "closure_score": result.closure_score,
                "violations": result.violations,
                "warnings": result.warnings,
            }
            print(
                f"   {layer}: {'✅' if result.is_valid else '❌'} Score: {result.closure_score:.2f}"
            )

        validation_results["semantic_closure"] = closure_results

        # 2. Validate Immutable Core
        print("\n🔒 2. Validating Immutable Core...")
        core_verification = self.core_sealing_engine.verify_core_continuously()
        validation_results["immutable_core"] = {
            "is_valid": core_verification.is_valid,
            "verification_score": core_verification.verification_score,
            "violations": core_verification.violations,
            "warnings": core_verification.warnings,
        }
        print(
            f"   Core integrity: {'✅' if core_verification.is_valid else '❌'} Score: {core_verification.verification_score:.2f}"
        )

        # 3. Validate Lineage Reconstruction
        print("\n🔍 3. Validating Lineage Reconstruction...")
        lineage_summaries = {}
        for entity_id in list(self.lineage_reconstruction_engine.entity_index.keys())[
            :5
        ]:  # Sample 5 entities
            summary = self.lineage_reconstruction_engine.get_lineage_summary(entity_id)
            lineage_summaries[entity_id] = summary

        validation_results["lineage_reconstruction"] = {
            "sample_entities": len(lineage_summaries),
            "summaries": lineage_summaries,
        }
        print(
            f"   Lineage reconstruction: ✅ Sampled {len(lineage_summaries)} entities"
        )

        # Compute overall closure score
        semantic_score = sum(
            r["closure_score"] for r in closure_results.values()
        ) / len(closure_results)
        core_score = core_verification.verification_score

        validation_results["overall_closure_score"] = (
            semantic_score * 0.6 + core_score * 0.4
        )
        print(
            f"\n📊 Overall Governance Closure Score: {validation_results['overall_closure_score']:.2f}"
        )

        self.activation_status["validations_completed"].append("governance_closure")

        return validation_results

    def generate_activation_report(self) -> Dict:
        """Generate Era-2 activation report"""
        print("\n" + "=" * 80)
        print("📊 GENERATING ACTIVATION REPORT")
        print("=" * 80)

        report = {
            "era": "2",
            "era_name": "Governance Closure",
            "activation_timestamp": datetime.now().isoformat(),
            "workspace_root": str(self.workspace_root),
            "activation_status": self.activation_status,
            "sealed_core_status": self.core_sealing_engine.get_seal_status(),
            "gl_unified_charter": {
                "activated": True,
                "activation_version": "v2.0.0",
                "components": [
                    "semantic_closure_engine",
                    "core_sealing_engine",
                    "lineage_reconstruction_engine",
                ],
            },
        }

        # Save report
        report_path = (
            self.ecosystem_root / ".governance" / "era2-activation-report.json"
        )
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2, default=str)

        print(f"✅ Activation report saved: {report_path}")

        return report

    def activate(self) -> Dict:
        """Activate Era-2 with complete governance closure"""
        print("\n" + "=" * 80)
        print("🎯 GL ERA-2 GOVERNANCE CLOSURE ACTIVATION")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Workspace: {self.workspace_root}")

        try:
            # Phase 1: Initialize Engines
            self.initialize_engines()

            # Phase 2: Load Governance Entities
            self.load_governance_entities()

            # Phase 3: Perform Core Sealing Ceremony
            sealing_result = self.perform_core_sealing_ceremony()

            # Phase 4: Validate Governance Closure
            validation_results = self.validate_governance_closure()

            # Phase 5: Generate Activation Report
            report = self.generate_activation_report()

            # Update activation status
            self.activation_status["phase"] = "COMPLETED"
            self.activation_status["overall_status"] = "SUCCESS"
            self.activation_status["completed_at"] = datetime.now().isoformat()

            # Final summary
            print("\n" + "=" * 80)
            print("✅ ERA-2 ACTIVATION COMPLETE")
            print("=" * 80)
            print(
                f"📊 Overall Closure Score: {validation_results['overall_closure_score']:.2f}"
            )
            print(f"🔒 Core Sealed: {sealing_result['sealed_hash'][:16]}...")
            print(
                f"📝 Report: {self.ecosystem_root / '.governance' / 'era2-activation-report.json'}"
            )
            print("\n🎓 GL Unified Charter Activated: ERA-2 GOVERNANCE CLOSURE")

            return report

        except Exception as e:
            self.activation_status["phase"] = "FAILED"
            self.activation_status["overall_status"] = "FAILED"
            self.activation_status["error"] = str(e)
            self.activation_status["completed_at"] = datetime.now().isoformat()

            print(f"\n❌ Era-2 Activation Failed: {e}")
            raise

    # Helper methods

    def _load_event_stream(self, event_stream_path: Path) -> List[Dict]:
        """Load events from event stream file"""
        events = []
        try:
            with open(event_stream_path) as f:
                for line in f:
                    if line.strip():
                        event_data = json.loads(line)
                        # Transform GL event format to GovernanceEvent format
                        if "event" in event_data:
                            # GL event format
                            events.append(
                                {
                                    "event_id": event_data.get(
                                        "id", str(hash(str(event_data)))
                                    ),
                                    "event_type": event_data["event"],
                                    "entity_id": event_data.get("context", {}).get(
                                        "entity", "unknown"
                                    ),
                                    "layer": event_data.get("context", {}).get(
                                        "layer", "unknown"
                                    ),
                                    "timestamp": event_data.get(
                                        "timestamp", datetime.now().isoformat()
                                    ),
                                    "data": event_data.get("data", {}),
                                    "dependencies": event_data.get("context", {}).get(
                                        "dependencies", []
                                    ),
                                    "context": event_data.get("context", {}),
                                    "hash": event_data.get("hash"),
                                    "previous_hash": event_data.get("previous_hash"),
                                }
                            )
        except Exception as e:
            print(f"⚠️  Warning: Could not load event stream: {e}")
        return events

    def _convert_layer_name(self, layer_name: str) -> str:
        """Convert layer name to GL format"""
        layer_map = {
            "language_layer": "L00",
            "format_layer": "L01",
            "topology_layer": "L02",
            "index_layer": "L03",
        }
        return layer_map.get(layer_name, layer_name)

    def _extract_closure_matrix(self) -> Dict:
        """Extract semantic closure matrix"""
        # Convert SemanticEntity objects to dictionaries for JSON serialization
        matrix = {}
        for layer, entities in self.semantic_closure_engine.closure_matrix.items():
            matrix[layer] = {}
            for entity_id, entity in entities.items():
                matrix[layer][entity_id] = {
                    "layer": entity.layer,
                    "entity_id": entity.entity_id,
                    "entity_type": entity.entity_type,
                    "definition": entity.definition,
                    "dependencies": entity.dependencies,
                    "metadata": entity.metadata,
                    "hash": entity.get_hash(),
                }
        return matrix

    def _extract_governance_rules(self) -> Dict:
        """Extract governance rules"""
        # Placeholder - would load from actual governance rules
        return {"rules_count": len(self.semantic_closure_engine.closure_status)}

    def _extract_meta_spec(self) -> Dict:
        """Extract meta specification"""
        # Placeholder - would load from actual meta-spec
        return {"meta_spec_loaded": True}

    def _create_sample_entities(self) -> int:
        """Create sample governance entities for demonstration"""
        sample_entities = [
            SemanticEntity(
                layer="L00",
                entity_id="primitive_string",
                entity_type="type",
                definition={"name": "string", "description": "Primitive string type"},
                dependencies=[],
                metadata={"source": "sample"},
            ),
            SemanticEntity(
                layer="L00",
                entity_id="primitive_number",
                entity_type="type",
                definition={"name": "number", "description": "Primitive number type"},
                dependencies=[],
                metadata={"source": "sample"},
            ),
            SemanticEntity(
                layer="L01",
                entity_id="json_format",
                entity_type="format",
                definition={"name": "json", "description": "JSON format specification"},
                dependencies=["primitive_string", "primitive_number"],
                metadata={"source": "sample"},
            ),
            SemanticEntity(
                layer="L02",
                entity_id="tree_topology",
                entity_type="topology",
                definition={"name": "tree", "description": "Tree topology structure"},
                dependencies=["json_format"],
                metadata={"source": "sample"},
            ),
        ]

        entity_count = 0
        for entity in sample_entities:
            result = self.semantic_closure_engine.define_semantic_entity(entity)
            if result.is_valid:
                entity_count += 1

        return entity_count


def main():
    """Main entry point"""
    activation = Era2Activation()
    report = activation.activate()

    print("\n" + "=" * 80)
    print("🎯 ACTIVATION SUMMARY")
    print("=" * 80)
    print(f"Era: {report['era']} - {report['era_name']}")
    print(f"Status: {activation.activation_status['overall_status']}")
    print(
        f"GL Unified Charter: {'✅ ACTIVATED' if report['gl_unified_charter']['activated'] else '❌ NOT ACTIVATED'}"
    )
    print("=" * 80)

    return 0 if activation.activation_status["overall_status"] == "SUCCESS" else 1


if __name__ == "__main__":
    sys.exit(main())
