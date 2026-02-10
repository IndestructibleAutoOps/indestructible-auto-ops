#!/usr/bin/env python3
"""
update_registry.py - Tool Registry Update with Hash Verification

Governance: GL-Tools-Registry v1.0
Era: 1 (Evidence-Native Bootstrap)
Status: OPERATIONAL

Purpose:
- Scans tools/ directory for new tools
- Computes SHA256 hash for each tool
- Updates tools/registry.json with verified tools
- Generates evidence of registry update

Evidence Chain:
- Input: tools/ directory scan
- Output: tools/registry.json (updated)
- Hash: SHA256 of registry state
- Trace: .evidence/registry/update_trace.json

Usage:
    python ecosystem/tools/update_registry.py --scan tools/ --output tools/registry.json
    python ecosystem/tools/update_registry.py --verify tools/registry.json
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import subprocess


class ToolRegistryUpdater:
    """
    Updates tool registry with hash verification and evidence generation.
    """

    def __init__(self, workspace_root: str = "/workspace"):
        self.workspace_root = Path(workspace_root)
        self.ecosystem_root = self.workspace_root / "ecosystem"
        self.tools_dir = self.ecosystem_root / "tools"
        self.evidence_dir = self.ecosystem_root / ".evidence" / "registry"

    def compute_sha256_hash(self, file_path: Path) -> str:
        """
        Computes SHA256 hash of a file.

        Args:
            file_path: Path to file

        Returns:
            SHA256 hash as hex string
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return f"sha256:{sha256_hash.hexdigest()}"

    def scan_tools(self) -> List[Dict]:
        """
        Scans tools/ directory for Python tools.

        Returns:
            List of tool metadata
        """
        tools = []

        for tool_file in self.tools_dir.rglob("*.py"):
            if tool_file.name.startswith("_") or tool_file.name == "update_registry.py":
                continue

            relative_path = tool_file.relative_to(self.workspace_root)
            tool_hash = self.compute_sha256_hash(tool_file)

            tool_info = {
                "name": tool_file.stem,
                "path": str(relative_path),
                "hash": tool_hash,
                "size": tool_file.stat().st_size,
                "modified": datetime.fromtimestamp(
                    tool_file.stat().st_mtime
                ).isoformat(),
            }

            tools.append(tool_info)

        return tools

    def load_existing_registry(self, registry_path: Path) -> Dict:
        """
        Loads existing registry.

        Args:
            registry_path: Path to registry.json

        Returns:
            Registry dictionary
        """
        if registry_path.exists():
            with open(registry_path, "r") as f:
                return json.load(f)
        return {
            "version": "1.0.0",
            "era": 1,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "governance_owner": "IndestructibleAutoOps",
            "tools": {},
            "verification_status": {
                "total_tools": 0,
                "verified_tools": 0,
                "unverified_tools": 0,
                "verification_rate": 0.0,
            },
        }

    def merge_tools(self, existing_registry: Dict, new_tools: List[Dict]) -> Dict:
        """
        Merges new tools into existing registry.

        Args:
            existing_registry: Existing registry
            new_tools: New tools from scan

        Returns:
            Updated registry
        """
        existing_tools = existing_registry.get("tools", {})

        for new_tool in new_tools:
            tool_name = new_tool["name"]

            if tool_name in existing_tools:
                existing_tools[tool_name]["hash"] = new_tool["hash"]
                existing_tools[tool_name]["modified"] = new_tool["modified"]
            else:
                existing_tools[tool_name] = {
                    "name": tool_name,
                    "version": "1.0.0",
                    "hash": new_tool["hash"],
                    "path": new_tool["path"],
                    "inputs": [],
                    "outputs": [],
                    "verified": False,
                    "verified_at": None,
                    "semantic": "Tool awaiting semantic definition",
                }

        # Update verification status
        total_tools = len(existing_tools)
        verified_tools = sum(
            1 for t in existing_tools.values() if t.get("verified", False)
        )

        existing_registry["verification_status"] = {
            "total_tools": total_tools,
            "verified_tools": verified_tools,
            "unverified_tools": total_tools - verified_tools,
            "verification_rate": (
                (verified_tools / total_tools * 100) if total_tools > 0 else 0.0
            ),
        }

        existing_registry["generated_at"] = datetime.utcnow().isoformat() + "Z"

        return existing_registry

    def write_registry(self, registry: Dict, registry_path: Path) -> str:
        """
        Writes registry to file and returns hash.

        Args:
            registry: Registry dictionary
            registry_path: Output path

        Returns:
            SHA256 hash of registry
        """
        registry_path.parent.mkdir(parents=True, exist_ok=True)

        with open(registry_path, "w") as f:
            json.dump(registry, f, indent=2, sort_keys=True)

        return self.compute_sha256_hash(registry_path)

    def generate_evidence(self, registry: Dict, registry_hash: str) -> Dict:
        """
        Generates evidence of registry update.

        Args:
            registry: Registry dictionary
            registry_hash: Hash of registry

        Returns:
            Evidence dictionary
        """
        evidence = {
            "evidence_id": f"registry-update-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "evidence_type": "registry_update",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "era": 1,
            "registry_hash": registry_hash,
            "total_tools": registry["verification_status"]["total_tools"],
            "verified_tools": registry["verification_status"]["verified_tools"],
            "verification_rate": registry["verification_status"]["verification_rate"],
            "governance_owner": "IndestructibleAutoOps",
            "compliance": (
                "PASS"
                if registry["verification_status"]["verification_rate"] >= 80.0
                else "WARNING"
            ),
        }

        # Write evidence
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        evidence_path = (
            self.evidence_dir
            / f"update_trace_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        )

        with open(evidence_path, "w") as f:
            json.dump(evidence, f, indent=2)

        return evidence

    def verify_registry(self, registry_path: Path) -> Dict:
        """
        Verifies tool registry integrity.

        Args:
            registry_path: Path to registry.json

        Returns:
            Verification result
        """
        if not registry_path.exists():
            return {"status": "FAIL", "error": "Registry file not found"}

        with open(registry_path, "r") as f:
            registry = json.load(f)

        verification_result = {
            "status": "PASS",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tools_verified": 0,
            "tools_failed": 0,
            "issues": [],
        }

        for tool_name, tool_info in registry.get("tools", {}).items():
            tool_path = self.workspace_root / tool_info["path"]

            if not tool_path.exists():
                verification_result["issues"].append(
                    {"tool": tool_name, "error": "Tool file not found"}
                )
                verification_result["tools_failed"] += 1
                continue

            current_hash = self.compute_sha256_hash(tool_path)
            registered_hash = tool_info.get("hash", "")

            if current_hash != registered_hash:
                verification_result["issues"].append(
                    {
                        "tool": tool_name,
                        "error": "Hash mismatch",
                        "registered": registered_hash,
                        "current": current_hash,
                    }
                )
                verification_result["tools_failed"] += 1
            else:
                verification_result["tools_verified"] += 1

        if verification_result["tools_failed"] > 0:
            verification_result["status"] = "FAIL"

        return verification_result

    def update(self, scan_dir: str, output_path: str) -> Dict:
        """
        Main update method.

        Args:
            scan_dir: Directory to scan
            output_path: Output registry path

        Returns:
            Update result
        """
        scan_path = Path(scan_dir)
        registry_path = Path(output_path)

        print(f"Scanning tools in {scan_path}...")
        new_tools = self.scan_tools()
        print(f"Found {len(new_tools)} tools")

        print(f"Loading existing registry from {registry_path}...")
        existing_registry = self.load_existing_registry(registry_path)

        print(f"Merging tools into registry...")
        updated_registry = self.merge_tools(existing_registry, new_tools)

        print(f"Writing registry to {registry_path}...")
        registry_hash = self.write_registry(updated_registry, registry_path)
        print(f"Registry hash: {registry_hash}")

        print(f"Generating evidence...")
        evidence = self.generate_evidence(updated_registry, registry_hash)

        result = {
            "status": "SUCCESS",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "registry_path": str(registry_path),
            "registry_hash": registry_hash,
            "total_tools": updated_registry["verification_status"]["total_tools"],
            "verified_tools": updated_registry["verification_status"]["verified_tools"],
            "verification_rate": updated_registry["verification_status"][
                "verification_rate"
            ],
            "evidence_id": evidence["evidence_id"],
            "compliance": evidence["compliance"],
        }

        print(f"\nUpdate complete:")
        print(f"  Total tools: {result['total_tools']}")
        print(f"  Verified: {result['verified_tools']}")
        print(f"  Verification rate: {result['verification_rate']:.1f}%")
        print(f"  Compliance: {result['compliance']}")

        return result


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Update tool registry with hash verification"
    )
    parser.add_argument(
        "--scan", default="ecosystem/tools", help="Directory to scan for tools"
    )
    parser.add_argument(
        "--output", default="ecosystem/tools/registry.json", help="Output registry path"
    )
    parser.add_argument(
        "--verify", action="store_true", help="Verify existing registry"
    )
    parser.add_argument(
        "--workspace", default="/workspace", help="Workspace root directory"
    )

    args = parser.parse_args()

    updater = ToolRegistryUpdater(args.workspace)

    if args.verify:
        print(f"Verifying registry: {args.output}")
        result = updater.verify_registry(Path(args.output))
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["status"] == "PASS" else 1)
    else:
        result = updater.update(args.scan, args.output)
        sys.exit(0)


if __name__ == "__main__":
    main()
