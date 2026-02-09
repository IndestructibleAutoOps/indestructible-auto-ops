# @GL-semantic: org.mnga.engines.refresh@1.0.0
# @GL-audit-trail: enabled
"""
Refresh Engine - One-time refresh of governance specifications
"""

import os
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class RefreshResult:
    """Result of refresh operation"""

    success: bool
    refreshed_specs: List[str] = field(default_factory=list)
    failed_specs: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class RefreshEngine:
    """
    Refresh Engine for one-time refresh of governance specifications.

    This engine performs a one-time refresh of all governance specifications,
    updating checksums, validating structure, and ensuring consistency.
    """

    def __init__(self, workspace_root: str = "/workspace"):
        """
        Initialize Refresh Engine

        Args:
            workspace_root: Root directory of the workspace
        """
        self.workspace_root = workspace_root
        self.governance_root = os.path.join(workspace_root, "ecosystem", "governance")
        self.specs_registry_path = os.path.join(
            self.governance_root, "meta-spec", "registry", "specs.registry.json"
        )

    def refresh_all(self) -> RefreshResult:
        """
        Perform one-time refresh of all governance specifications

        Returns:
            RefreshResult with operation details
        """
        result = RefreshResult(success=True)

        print("=== Refresh Engine: Starting One-Time Refresh ===")
        print(f"Workspace: {self.workspace_root}")
        print(f"Governance Root: {self.governance_root}")
        print()

        # Step 1: Scan all specification files
        print("Step 1: Scanning specification files...")
        spec_files = self._scan_spec_files()
        print(f"Found {len(spec_files)} specification files")
        print()

        # Step 2: Update checksums for all specs
        print("Step 2: Updating checksums...")
        for spec_file in spec_files:
            try:
                self._update_checksum(spec_file)
                result.refreshed_specs.append(spec_file)
                print(f"  ✓ {spec_file}")
            except Exception as e:
                result.failed_specs.append(spec_file)
                result.errors.append(f"{spec_file}: {str(e)}")
                print(f"  ✗ {spec_file}: {str(e)}")
        print()

        # Step 3: Update specs registry
        print("Step 3: Updating specs registry...")
        try:
            self._update_registry(spec_files)
            print("  ✓ Registry updated")
        except Exception as e:
            result.errors.append(f"Registry update failed: {str(e)}")
            print(f"  ✗ Registry update failed: {str(e)}")
        print()

        # Step 4: Validate all specs
        print("Step 4: Validating specifications...")
        validation_results = self._validate_all_specs(spec_files)
        valid_count = sum(1 for r in validation_results if r["valid"])
        print(f"  Valid: {valid_count}/{len(validation_results)}")
        print()

        # Step 5: Generate summary
        print("=== Refresh Summary ===")
        print(f"Total specs: {len(spec_files)}")
        print(f"Refreshed: {len(result.refreshed_specs)}")
        print(f"Failed: {len(result.failed_specs)}")
        print(f"Valid: {valid_count}")
        print(f"Timestamp: {result.timestamp}")
        print()

        if result.failed_specs:
            result.success = False
            print("Errors:")
            for error in result.errors:
                print(f"  - {error}")

        return result

    def _scan_spec_files(self) -> List[str]:
        """
        Scan for all specification files

        Returns:
            List of specification file paths (relative to workspace)
        """
        spec_files = []

        # Define patterns for specification files
        patterns = [
            "**/*.spec.yaml",
            "**/*.spec.json",
            "**/*.schema.json",
            "**/meta*.json",
            "**/registry.json",
            "**/topology*.yaml",
            "**/semantics*.yaml",
            "**/index*.yaml",
            "**/tokens.yaml",
            "**/ast.yaml",
        ]

        for root, dirs, files in os.walk(self.governance_root):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.workspace_root)

                # Check if file matches any pattern
                for pattern in patterns:
                    if self._matches_pattern(rel_path, pattern):
                        spec_files.append(rel_path)
                        break

        return sorted(spec_files)

    def _matches_pattern(self, file_path: str, pattern: str) -> bool:
        """
        Check if file path matches pattern

        Args:
            file_path: File path to check
            pattern: Pattern to match

        Returns:
            True if matches, False otherwise
        """
        # Simple pattern matching
        if pattern.startswith("**/"):
            suffix = pattern[3:]
            return file_path.endswith(suffix)
        elif pattern.endswith("/*"):
            prefix = pattern[:-2]
            return file_path.startswith(prefix)
        else:
            return file_path == pattern

    def _update_checksum(self, file_path: str) -> None:
        """
        Update checksum for a specification file

        Args:
            file_path: Path to specification file (relative to workspace)
        """
        full_path = os.path.join(self.workspace_root, file_path)

        # Calculate SHA-256 checksum
        with open(full_path, "rb") as f:
            content = f.read()
            checksum = hashlib.sha256(content).hexdigest()

        # Update checksum in file
        if file_path.endswith(".yaml"):
            self._update_yaml_checksum(full_path, checksum)
        elif file_path.endswith(".json"):
            self._update_json_checksum(full_path, checksum)

    def _update_yaml_checksum(self, file_path: str, checksum: str) -> None:
        """
        Update checksum in YAML file

        Args:
            file_path: Path to YAML file
            checksum: New checksum value
        """
        with open(file_path, "r") as f:
            lines = f.readlines()

        updated_lines = []
        for line in lines:
            if line.strip().startswith("checksum:"):
                updated_lines.append(f"  checksum: sha256:{checksum}\n")
            else:
                updated_lines.append(line)

        with open(file_path, "w") as f:
            f.writelines(updated_lines)

    def _update_json_checksum(self, file_path: str, checksum: str) -> None:
        """
        Update checksum in JSON file

        Args:
            file_path: Path to JSON file
            checksum: New checksum value
        """
        with open(file_path, "r") as f:
            data = json.load(f)

        # Update checksum in audit_trail if present
        if "audit_trail" in data:
            data["audit_trail"]["checksum"] = f"sha256:{checksum}"

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    def _update_registry(self, spec_files: List[str]) -> None:
        """
        Update specs registry with current specifications

        Args:
            spec_files: List of specification files
        """
        registry = {
            "@GL-semantic": "org.mnga.specs.registry@1.0.0",
            "@GL-audit-trail": "enabled",
            "registry_version": "1.0.0",
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "specifications": [],
        }

        for spec_file in spec_files:
            spec_info = {
                "path": spec_file,
                "checksum": self._get_file_checksum(spec_file),
                "last_modified": self._get_file_mtime(spec_file),
            }
            registry["specifications"].append(spec_info)

        with open(self.specs_registry_path, "w") as f:
            json.dump(registry, f, indent=2)

    def _get_file_checksum(self, file_path: str) -> str:
        """
        Get checksum of file

        Args:
            file_path: Path to file (relative to workspace)

        Returns:
            SHA-256 checksum
        """
        full_path = os.path.join(self.workspace_root, file_path)
        with open(full_path, "rb") as f:
            content = f.read()
            return hashlib.sha256(content).hexdigest()

    def _get_file_mtime(self, file_path: str) -> str:
        """
        Get modification time of file

        Args:
            file_path: Path to file (relative to workspace)

        Returns:
            ISO 8601 timestamp
        """
        full_path = os.path.join(self.workspace_root, file_path)
        mtime = os.path.getmtime(full_path)
        return datetime.fromtimestamp(mtime).isoformat() + "Z"

    def _validate_all_specs(self, spec_files: List[str]) -> List[Dict[str, Any]]:
        """
        Validate all specification files

        Args:
            spec_files: List of specification files

        Returns:
            List of validation results
        """
        results = []

        for spec_file in spec_files:
            result = {"file": spec_file, "valid": True, "errors": []}

            # Check for GL-semantic marker
            if not self._has_gl_semantic(spec_file):
                result["valid"] = False
                result["errors"].append("Missing @GL-semantic marker")

            # Check for GL-audit-trail marker
            if not self._has_gl_audit_trail(spec_file):
                result["valid"] = False
                result["errors"].append("Missing @GL-audit-trail marker")

            results.append(result)

        return results

    def _has_gl_semantic(self, file_path: str) -> bool:
        """
        Check if file has GL-semantic marker

        Args:
            file_path: Path to file (relative to workspace)

        Returns:
            True if has marker, False otherwise
        """
        full_path = os.path.join(self.workspace_root, file_path)
        with open(full_path, "r") as f:
            content = f.read()
            return "@GL-semantic" in content

    def _has_gl_audit_trail(self, file_path: str) -> bool:
        """
        Check if file has GL-audit-trail marker

        Args:
            file_path: Path to file (relative to workspace)

        Returns:
            True if has marker, False otherwise
        """
        full_path = os.path.join(self.workspace_root, file_path)
        with open(full_path, "r") as f:
            content = f.read()
            return "@GL-audit-trail" in content


def main():
    """Main entry point for refresh engine"""
    engine = RefreshEngine()
    result = engine.refresh_all()

    if result.success:
        print("✓ Refresh completed successfully")
        return 0
    else:
        print("✗ Refresh completed with errors")
        return 1


if __name__ == "__main__":
    exit(main())
