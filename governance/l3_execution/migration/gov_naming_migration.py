#!/usr/bin/env python3
"""
命名規範遷移腳本
"""

from pathlib import Path
from typing import List


class GovNamingMigration:
    # Mapping of deprecated prefixes to their replacement prefixes,
    # aligned with gov_naming_registry.yaml.
    PREFIX_MIGRATIONS = {
        "ng_": "gov_naming_",
        "gl_": "gov_",
    }
    DEPRECATED_PREFIXES = list(PREFIX_MIGRATIONS.keys())
    
    def __init__(self, project_root: str, dry_run: bool = True):
        self.project_root = Path(project_root)
        self.dry_run = dry_run

    def generate_new_name(self, old_name: str) -> str:
        """Generate a new asset name based on deprecated prefix mappings."""
        for prefix, replacement in self.PREFIX_MIGRATIONS.items():
            if old_name.startswith(prefix):
                # Strip the deprecated prefix and prepend the mapped replacement.
                remainder = old_name[len(prefix):]
                return f"{replacement}{remainder}"
        # If no deprecated prefix is found, return the original name unchanged.
        return old_name

    def scan_deprecated(self) -> List[Path]:
        """Scan for assets with deprecated prefixes."""
        deprecated = []
        for asset in self.project_root.rglob("*"):
            for prefix in self.DEPRECATED_PREFIXES:
                if asset.name.startswith(prefix):
                    deprecated.append(asset)
                    break
        return deprecated


if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    migrator = GovNamingMigration(root, dry_run=True)
    print("🔄 Naming Migration (Dry Run)")
    deprecated = migrator.scan_deprecated()
    print(f"  Found {len(deprecated)} assets to migrate")
    for asset in deprecated[:10]:
        new_name = migrator.generate_new_name(asset.name)
        print(f"    {asset.name} → {new_name}")
