#!/usr/bin/env python3
"""
Core Hash Generator (核心雜湊生成器)

Generates SHA256 hashes for all governance artifacts and creates
a core-hash.json file for sealing purposes.

Usage:
    python ecosystem/tools/generate_core_hash.py --artifacts .evidence/*.json
    python ecosystem/tools/generate_core_hash.py --artifacts .evidence/*.json --output .governance/core-hash.json
    python ecosystem/tools/generate_core_hash.py --verify .governance/core-hash.json
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class CoreHashGenerator:
    """Generates and verifies core hashes for governance artifacts"""

    def __init__(self, workspace: str = "/workspace"):
        self.workspace = workspace
        self.governance_dir = os.path.join(workspace, ".governance")
        self.evidence_dir = os.path.join(workspace, ".evidence")

        # Ensure directories exist
        os.makedirs(self.governance_dir, exist_ok=True)
        os.makedirs(self.evidence_dir, exist_ok=True)

    def generate_file_hash(self, file_path: str) -> str:
        """Generate SHA256 hash for a single file"""
        sha256_hash = hashlib.sha256()

        try:
            with open(file_path, "rb") as f:
                # Read file in chunks for memory efficiency
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"❌ Error hashing {file_path}: {e}")
            return ""

    def generate_artifact_hashes(
        self, artifact_patterns: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        """Generate hashes for multiple artifacts"""
        sealed_artifacts = {}

        for pattern in artifact_patterns:
            # Expand glob patterns
            full_pattern = os.path.join(self.workspace, pattern)
            artifacts = Path(self.workspace).glob(pattern)

            for artifact_path in sorted(artifacts):
                if artifact_path.is_file():
                    file_hash = self.generate_file_hash(str(artifact_path))

                    if file_hash:
                        relative_path = os.path.relpath(
                            str(artifact_path), self.workspace
                        )
                        sealed_artifacts[artifact_path.name] = {
                            "hash": file_hash,
                            "path": relative_path,
                            "size": os.path.getsize(str(artifact_path)),
                            "hash_preview": file_hash[:16] + "...",
                        }
                        print(f"✅ Sealed {artifact_path.name}: {file_hash[:16]}...")

        return sealed_artifacts

    def generate_core_hash(
        self,
        artifact_patterns: List[str] = None,
        output_file: str = None,
        pipeline_id: str = None,
        overall_score: float = None,
    ) -> Dict[str, Any]:
        """Generate complete core hash data structure"""

        if artifact_patterns is None:
            # Default to all step artifacts
            artifact_patterns = [
                ".evidence/step-*.json",
                ".governance/event-stream.jsonl",
                "ecosystem/enforce.py",
                "ecosystem/enforce.rules.py",
            ]

        # Generate hashes for all artifacts
        sealed_artifacts = self.generate_artifact_hashes(artifact_patterns)

        # Build core hash data structure
        core_hash_data = {
            "version": "1.0.0",
            "era": "1",
            "sealed_at": datetime.now().isoformat(),
            "workspace": self.workspace,
            # Metadata
            "metadata": {
                "pipeline_id": pipeline_id or "manual",
                "overall_score": overall_score,
                "total_artifacts": len(sealed_artifacts),
            },
            # Sealed artifacts
            "sealed_artifacts": sealed_artifacts,
            # Hash of this core hash file itself (will be filled after saving)
            "self_hash": "",
        }

        # Save to file
        if output_file is None:
            output_file = os.path.join(self.governance_dir, "core-hash.json")

        # Save to JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(core_hash_data, f, indent=2, ensure_ascii=False)

        # Generate self hash
        self_hash = self.generate_file_hash(output_file)

        # Update with self hash
        core_hash_data["self_hash"] = self_hash

        # Save again with self hash
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(core_hash_data, f, indent=2, ensure_ascii=False)

        return core_hash_data

    def verify_core_hash(self, core_hash_file: str) -> Dict[str, Any]:
        """Verify that sealed artifacts still match their hashes"""

        verification_result = {
            "verified": True,
            "verified_at": datetime.now().isoformat(),
            "artifacts_verified": 0,
            "artifacts_failed": 0,
            "failed_artifacts": [],
        }

        # Load core hash file
        try:
            with open(core_hash_file, "r", encoding="utf-8") as f:
                core_hash_data = json.load(f)
        except Exception as e:
            print(f"❌ Error loading core hash file: {e}")
            verification_result["verified"] = False
            verification_result["error"] = str(e)
            return verification_result

        # Verify each artifact
        for artifact_name, artifact_info in core_hash_data.get(
            "sealed_artifacts", {}
        ).items():
            original_hash = artifact_info.get("hash")
            artifact_path = os.path.join(self.workspace, artifact_info.get("path"))

            if not os.path.exists(artifact_path):
                print(f"❌ Artifact not found: {artifact_name}")
                verification_result["verified"] = False
                verification_result["artifacts_failed"] += 1
                verification_result["failed_artifacts"].append(
                    {"name": artifact_name, "reason": "not_found"}
                )
                continue

            # Generate current hash
            current_hash = self.generate_file_hash(artifact_path)

            if current_hash == original_hash:
                print(f"✅ {artifact_name}: hash verified")
                verification_result["artifacts_verified"] += 1
            else:
                print(f"❌ {artifact_name}: hash mismatch!")
                print(f"   Expected: {original_hash[:16]}...")
                print(f"   Current:  {current_hash[:16]}...")
                verification_result["verified"] = False
                verification_result["artifacts_failed"] += 1
                verification_result["failed_artifacts"].append(
                    {
                        "name": artifact_name,
                        "reason": "hash_mismatch",
                        "expected": original_hash,
                        "current": current_hash,
                    }
                )

        # Verify self hash
        self_hash_original = core_hash_data.get("self_hash")
        self_hash_current = self.generate_file_hash(core_hash_file)

        if self_hash_current == self_hash_original:
            print(f"✅ Self hash verified: {self_hash_current[:16]}...")
        else:
            print(f"⚠️ Self hash mismatch (expected after modification)")

        return verification_result

    def print_summary(self, core_hash_data: Dict[str, Any]):
        """Print a summary of the core hash"""
        print("\n" + "=" * 80)
        print("🔐 Core Hash Summary")
        print("=" * 80)
        print(f"Version: {core_hash_data.get('version')}")
        print(f"Era: {core_hash_data.get('era')}")
        print(f"Sealed At: {core_hash_data.get('sealed_at')}")
        print(f"Workspace: {core_hash_data.get('workspace')}")
        print()

        metadata = core_hash_data.get("metadata", {})
        print("Metadata:")
        print(f"  Pipeline ID: {metadata.get('pipeline_id')}")
        print(f"  Overall Score: {metadata.get('overall_score')}")
        print(f"  Total Artifacts: {metadata.get('total_artifacts')}")
        print()

        print("Sealed Artifacts:")
        for name, info in core_hash_data.get("sealed_artifacts", {}).items():
            print(f"  {name}:")
            print(f"    Hash: {info.get('hash_preview')}")
            print(f"    Path: {info.get('path')}")
            print(f"    Size: {info.get('size')} bytes")
        print()

        print(f"Self Hash: {core_hash_data.get('self_hash', '')[:16]}...")
        print("=" * 80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Core Hash Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate core hash for all step artifacts
  python generate_core_hash.py --artifacts ".evidence/step-*.json"
  
  # Generate with custom output
  python generate_core_hash.py --artifacts ".evidence/*.json" --output core-hash.json
  
  # Verify existing core hash
  python generate_core_hash.py --verify .governance/core-hash.json
  
  # Generate with metadata
  python generate_core_hash.py --artifacts ".evidence/*.json" --pipeline-id ci-123 --overall-score 95.0
        """,
    )

    parser.add_argument(
        "--artifacts",
        nargs="+",
        help="Artifact patterns to hash (e.g., '.evidence/*.json')",
    )
    parser.add_argument(
        "--output",
        help="Output file for core hash (default: .governance/core-hash.json)",
    )
    parser.add_argument("--workspace", default="/workspace", help="Workspace directory")
    parser.add_argument("--pipeline-id", help="Pipeline ID for metadata")
    parser.add_argument(
        "--overall-score", type=float, help="Overall compliance score for metadata"
    )
    parser.add_argument("--verify", help="Verify existing core hash file")

    args = parser.parse_args()

    generator = CoreHashGenerator(args.workspace)

    if args.verify:
        # Verify mode
        print(f"\n🔍 Verifying core hash: {args.verify}\n")
        result = generator.verify_core_hash(args.verify)

        print("\n" + "=" * 80)
        print("Verification Result")
        print("=" * 80)
        print(f"Verified: {'✅ YES' if result['verified'] else '❌ NO'}")
        print(f"Verified At: {result['verified_at']}")
        print(f"Artifacts Verified: {result['artifacts_verified']}")
        print(f"Artifacts Failed: {result['artifacts_failed']}")

        if result.get("failed_artifacts"):
            print("\nFailed Artifacts:")
            for failed in result["failed_artifacts"]:
                print(f"  - {failed['name']}: {failed['reason']}")

        print("=" * 80)

        sys.exit(0 if result["verified"] else 1)

    else:
        # Generate mode
        artifacts = args.artifacts or [".evidence/step-*.json"]

        print(f"\n🔐 Generating core hash...")
        print(f"   Artifacts: {', '.join(artifacts)}")
        print(f"   Pipeline ID: {args.pipeline_id or 'manual'}")
        print(f"   Overall Score: {args.overall_score or 'N/A'}")
        print()

        core_hash_data = generator.generate_core_hash(
            artifact_patterns=artifacts,
            output_file=args.output,
            pipeline_id=args.pipeline_id,
            overall_score=args.overall_score,
        )

        # Print summary
        generator.print_summary(core_hash_data)

        output_file = args.output or os.path.join(
            generator.governance_dir, "core-hash.json"
        )
        print(f"✅ Core hash saved to: {output_file}\n")


if __name__ == "__main__":
    main()
