#!/usr/bin/env python3
"""
命名規範遷移腳本
"""

import re
from pathlib import Path


class GovNamingMigration:
    def __init__(self, project_root: str, dry_run: bool = True):
        self.project_root = Path(project_root)
        self.dry_run = dry_run
        self.DEPRECATED_PREFIXES = ["ng_", "gl_"]
        self.REPLACEMENT_PREFIX = "gov_"

    def generate_new_name(self, old_name: str) -> str:
        new_name = old_name
        for prefix in self.DEPRECATED_PREFIXES:
            if new_name.startswith(prefix):
                new_name = new_name[len(prefix):]
                break
        if not new_name.startswith("gov_"):
            new_name = self.REPLACEMENT_PREFIX + new_name
        return new_name

    def scan_deprecated(self):
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
