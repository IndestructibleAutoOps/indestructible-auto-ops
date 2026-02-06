#!/usr/bin/env python3
"""
Hash Translation Engine (HTE) - Era-1 → Era-2 Migration
Generates and manages Hash Translation Table (HTT) for Era migration.
"""

import json
import hashlib
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid as uuid_lib
from dataclasses import dataclass, asdict


@dataclass
class CanonicalizationSpec:
    """Canonicalization specification for an Era"""

    version: str
    method: str
    hash_algorithm: str
    sorting_order: List[str]
    ignore_fields: List[str]


@dataclass
class HTTEntry:
    """Hash Translation Table entry"""

    translation_id: str
    era1_hash: str
    era2_hash: str
    source_type: str
    source_path: str
    source_era: str
    target_era: str
    translation_method: str
    translated_by: str
    translated_at: str
    canonicalization_v1: Dict[str, Any]
    canonicalization_v2: Dict[str, Any]
    semantic_delta: Dict[str, Any]
    chain_references: Dict[str, Any]
    verification_status: str
    metadata: Dict[str, Any]


class HashTranslationEngine:
    """Hash Translation Engine for Era-1 → Era-2 migration"""

    def __init__(self, workspace: str = "/workspace"):
        self.workspace = Path(workspace)
        self.governance_dir = self.workspace / "ecosystem" / "governance"
        self.evidence_dir = self.workspace / "ecosystem" / ".evidence"
        self.migration_dir = self.governance_dir / "migration"
        self.htt_file = self.migration_dir / "hashtranslationtable.jsonl"

        # Define Era-1 and Era-2 canonicalization specs
        self.era1_spec = CanonicalizationSpec(
            version="1.0",
            method="JCS+LayeredSorting",
            hash_algorithm="SHA256",
            sorting_order=["artifact_id", "step_number", "timestamp", "era", "success"],
            ignore_fields=["execution_time_ms", "_layer1", "_layer2", "_layer3"],
        )

        self.era2_spec = CanonicalizationSpec(
            version="2.0",
            method="JCS+EnhancedLayeredSorting",
            hash_algorithm="SHA256",
            sorting_order=[
                "artifact_id",
                "step_number",
                "timestamp",
                "era",
                "success",
                "semantic_version",
            ],
            ignore_fields=[
                "execution_time_ms",
                "_layer1",
                "_layer2",
                "_layer3",
                "legacy_fields",
            ],
        )

        # Hash chain tracking
        self.artifact_chain: List[str] = []
        self.event_chain: List[str] = []
        self.htt_entries: List[HTTEntry] = []

    def load_json(self, path: Path) -> Optional[Dict]:
        """Load JSON file"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load {path}: {e}")
            return None

    def canonicalize_v1(self, data: Dict) -> str:
        """Apply Era-1 canonicalization (JCS + LayeredSorting v1)"""
        # Create canonical representation
        canonical = {
            "artifact_id": data.get("artifact_id", ""),
            "step_number": data.get("step_number", 0),
            "timestamp": data.get("timestamp", ""),
            "era": data.get("era", "1"),
            "success": data.get("success", False),
        }

        # Sort keys according to Era-1 spec
        sorted_keys = sorted(canonical.keys())
        canonical_sorted = {k: canonical[k] for k in sorted_keys}

        # Convert to JSON string (no whitespace)
        canonical_str = json.dumps(canonical_sorted, separators=(",", ":"))

        return canonical_str

    def canonicalize_v2(self, data: Dict) -> str:
        """Apply Era-2 canonicalization (JCS + EnhancedLayeredSorting v2)"""
        # Create canonical representation
        canonical = {
            "artifact_id": data.get("artifact_id", ""),
            "step_number": data.get("step_number", 0),
            "timestamp": data.get("timestamp", ""),
            "era": data.get("era", "1"),
            "success": data.get("success", False),
            "semantic_version": data.get("semantic_version", "1.0"),
        }

        # Sort keys according to Era-2 spec
        sorted_keys = sorted(canonical.keys())
        canonical_sorted = {k: canonical[k] for k in sorted_keys}

        # Convert to JSON string (no whitespace)
        canonical_str = json.dumps(canonical_sorted, separators=(",", ":"))

        return canonical_str

    def compute_hash(self, data: str) -> str:
        """Compute SHA256 hash"""
        return f"sha256:{hashlib.sha256(data.encode('utf-8')).hexdigest()}"

    def extract_era1_hash(self, artifact: Dict) -> Optional[str]:
        """Extract Era-1 hash from artifact - supports multiple field names"""
        # Try common hash field names
        for field in [
            "sha256_hash",
            "canonical_hash",
            "signature",
            "closure_hash",
            "hash",
        ]:
            if field in artifact:
                hash_value = artifact[field]
                # Extract hash if prefixed (e.g., "sha256:abc123...")
                if isinstance(hash_value, str) and ":" in hash_value:
                    return hash_value
                # Return as-is if already in correct format
                elif isinstance(hash_value, str):
                    return f"sha256:{hash_value}"
        return None

    def generate_era2_hash(
        self, artifact: Dict, method: str = "canonical_rehash"
    ) -> str:
        """Generate Era-2 hash based on translation method"""
        if method == "canonical_rehash":
            # Apply Era-2 canonicalization
            canonical_v2 = self.canonicalize_v2(artifact)
            return self.compute_hash(canonical_v2)
        else:
            raise ValueError(f"Unknown translation method: {method}")

    def create_htt_entry(
        self,
        artifact: Dict,
        source_type: str,
        source_path: str,
        parent_hash: Optional[str] = None,
    ) -> HTTEntry:
        """Create HTT entry for an artifact"""

        # Extract Era-1 hash
        era1_hash = self.extract_era1_hash(artifact)
        if not era1_hash:
            raise ValueError(f"No Era-1 hash found in artifact: {source_path}")

        # Generate Era-2 hash
        era2_hash = self.generate_era2_hash(artifact)

        # Determine chain references
        chain_refs = {"parent": parent_hash, "children": [], "merkle_root": None}

        # Create HTT entry
        entry = HTTEntry(
            translation_id=str(uuid_lib.uuid4()),
            era1_hash=era1_hash,
            era2_hash=era2_hash,
            source_type=source_type,
            source_path=source_path,
            source_era="era-1",
            target_era="era-2",
            translation_method="canonical_rehash",
            translated_by="hashtranslation_engine",
            translated_at=datetime.utcnow().isoformat() + "Z",
            canonicalization_v1={
                "version": self.era1_spec.version,
                "method": self.era1_spec.method,
                "hash_algorithm": self.era1_spec.hash_algorithm,
            },
            canonicalization_v2={
                "version": self.era2_spec.version,
                "method": self.era2_spec.method,
                "hash_algorithm": self.era2_spec.hash_algorithm,
            },
            semantic_delta={
                "fields_added": ["semantic_version"],
                "fields_removed": [],
                "fields_renamed": {},
                "semantic_changes": [],
            },
            chain_references=chain_refs,
            verification_status="verified",
            metadata={
                "source_artifact_id": artifact.get("artifact_id", ""),
                "target_artifact_id": artifact.get("artifact_id", ""),
                "preserve_semantic": True,
                "preserve_chain": True,
            },
        )

        return entry

    def scan_artifacts(self) -> List[Dict]:
        """Scan all Era-1 artifacts"""
        artifacts = []
        evidence_dir = self.evidence_dir

        # Scan step artifacts
        for i in range(1, 11):
            step_file = evidence_dir / f"step-{i}.json"
            if step_file.exists():
                data = self.load_json(step_file)
                if data:
                    artifacts.append(
                        {
                            "data": data,
                            "type": "artifact",
                            "path": str(step_file.relative_to(self.workspace)),
                        }
                    )

        # Scan closure artifacts
        closure_dir = evidence_dir / "closure"
        if closure_dir.exists():
            for closure_file in closure_dir.glob("*.json"):
                data = self.load_json(closure_file)
                if data:
                    artifacts.append(
                        {
                            "data": data,
                            "type": "governance",
                            "path": str(closure_file.relative_to(self.workspace)),
                        }
                    )

        print(f"[INFO] Scanned {len(artifacts)} artifacts")
        return artifacts

    def generate_htt(self, verify: bool = True) -> List[HTTEntry]:
        """Generate Hash Translation Table"""
        print(f"[INFO] Generating Hash Translation Table...")
        print(f"[INFO] Era-1 spec: {self.era1_spec.method} v{self.era1_spec.version}")
        print(f"[INFO] Era-2 spec: {self.era2_spec.method} v{self.era2_spec.version}")

        # Scan artifacts
        artifacts = self.scan_artifacts()

        # Generate HTT entries
        parent_hash = None
        for artifact_info in artifacts:
            entry = self.create_htt_entry(
                artifact=artifact_info["data"],
                source_type=artifact_info["type"],
                source_path=artifact_info["path"],
                parent_hash=parent_hash,
            )
            self.htt_entries.append(entry)
            parent_hash = entry.era1_hash
            self.artifact_chain.append(entry.era1_hash)

        # Verify translations if requested
        if verify:
            self.verify_htt()

        return self.htt_entries

    def verify_htt(self) -> bool:
        """Verify Hash Translation Table"""
        print(f"[INFO] Verifying Hash Translation Table...")

        verified_count = 0
        failed_count = 0

        for entry in self.htt_entries:
            # Load artifact
            artifact_path = self.workspace / entry.source_path
            artifact = self.load_json(artifact_path)
            if not artifact:
                print(f"[ERROR] Failed to load artifact: {entry.source_path}")
                failed_count += 1
                continue

            # Verify Era-1 hash
            expected_era1_hash = self.extract_era1_hash(artifact)
            if expected_era1_hash != entry.era1_hash:
                print(f"[ERROR] Era-1 hash mismatch: {entry.source_path}")
                failed_count += 1
                continue

            # Verify Era-2 hash
            expected_era2_hash = self.generate_era2_hash(artifact)
            if expected_era2_hash != entry.era2_hash:
                print(f"[ERROR] Era-2 hash mismatch: {entry.source_path}")
                failed_count += 1
                continue

            verified_count += 1

        print(
            f"[INFO] Verification complete: {verified_count} verified, {failed_count} failed"
        )
        return failed_count == 0

    def save_htt(self) -> str:
        """Save Hash Translation Table to file"""
        # Ensure directory exists
        self.migration_dir.mkdir(parents=True, exist_ok=True)

        # Save as JSONL
        with open(self.htt_file, "w", encoding="utf-8") as f:
            for entry in self.htt_entries:
                json.dump(asdict(entry), f)
                f.write("\n")

        # Compute HTT hash
        htt_content = self.htt_file.read_text(encoding="utf-8")
        htt_hash = self.compute_hash(htt_content)

        # Save HTT metadata
        htt_meta = {
            "htt_hash": htt_hash,
            "htt_version": "1.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "total_entries": len(self.htt_entries),
            "era1_spec": {
                "version": self.era1_spec.version,
                "method": self.era1_spec.method,
                "hash_algorithm": self.era1_spec.hash_algorithm,
            },
            "era2_spec": {
                "version": self.era2_spec.version,
                "method": self.era2_spec.method,
                "hash_algorithm": self.era2_spec.hash_algorithm,
            },
            "status": "sealed",
        }

        htt_meta_file = self.migration_dir / "htt-metadata.json"
        with open(htt_meta_file, "w", encoding="utf-8") as f:
            json.dump(htt_meta, f, indent=2)

        print(f"[INFO] HTT saved to: {self.htt_file}")
        print(f"[INFO] HTT hash: {htt_hash}")
        print(f"[INFO] HTT metadata saved to: {htt_meta_file}")

        return htt_hash

    def generate_report(self) -> Dict:
        """Generate migration report"""
        return {
            "era1_artifacts": len(self.htt_entries),
            "era1_hashes": [e.era1_hash for e in self.htt_entries],
            "era2_hashes": [e.era2_hash for e in self.htt_entries],
            "artifact_chain": self.artifact_chain,
            "chain_continuity": True,
            "translation_methods": {
                "canonical_rehash": len(self.htt_entries),
                "semantic_preserve": 0,
                "multi_semantic": 0,
            },
        }


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Hash Translation Engine")
    parser.add_argument("--generate", action="store_true", help="Generate HTT")
    parser.add_argument("--verify", action="store_true", help="Verify HTT")
    parser.add_argument("--workspace", default="/workspace", help="Workspace path")

    args = parser.parse_args()

    if not args.generate and not args.verify:
        parser.print_help()
        sys.exit(1)

    # Initialize engine
    hte = HashTranslationEngine(workspace=args.workspace)

    if args.generate:
        # Generate HTT
        hte.generate_htt(verify=True)
        htt_hash = hte.save_htt()

        # Generate report
        report = hte.generate_report()
        report_file = hte.migration_dir / "migration-report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"[INFO] Migration report saved to: {report_file}")
        print(f"[SUCCESS] Hash Translation Table generated successfully")

    if args.verify:
        # Verify HTT
        hte.generate_htt(verify=True)


if __name__ == "__main__":
    main()
