#!/usr/bin/env python3
"""
完整命名規範遷移腳本
Full Naming Convention Migration Script
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Tuple


class GovNamingMigrationFull:
    def __init__(self, project_root: str, dry_run: bool = False):
        self.project_root = Path(project_root)
        self.dry_run = dry_run
        self.DEPRECATED_PREFIXES = ["ng_", "gl_"]
        self.REPLACEMENT_PREFIX = "gov_"
        self.migrations: List[Tuple[Path, Path]] = []
        self.content_updates: Dict[str, List[Tuple[str, str]]] = {}

    def generate_new_name(self, old_name: str) -> str:
        """Generate new name with gov_ prefix"""
        new_name = old_name
        for prefix in self.DEPRECATED_PREFIXES:
            if new_name.startswith(prefix):
                # Remove old prefix
                new_name = new_name[len(prefix):]
                break
        # Add gov_ prefix if not already present
        if not new_name.startswith("gov_"):
            new_name = self.REPLACEMENT_PREFIX + new_name
        return new_name

    def scan_deprecated(self) -> List[Path]:
        """Scan for files with deprecated prefixes"""
        deprecated = []
        for asset in self.project_root.rglob("*"):
            if ".git" in str(asset):
                continue
            if asset.is_file():
                for prefix in self.DEPRECATED_PREFIXES:
                    if asset.name.startswith(prefix):
                        deprecated.append(asset)
                        break
        return deprecated

    def plan_migrations(self, deprecated_files: List[Path]) -> None:
        """Plan file migrations"""
        self.migrations = []
        for old_path in deprecated_files:
            new_name = self.generate_new_name(old_path.name)
            new_path = old_path.parent / new_name
            self.migrations.append((old_path, new_path))

    def execute_migrations(self) -> int:
        """Execute file migrations"""
        success_count = 0
        print(f"\n🔄 {'[DRY RUN] ' if self.dry_run else ''}Starting migration...")

        for old_path, new_path in self.migrations:
            relative_old = old_path.relative_to(self.project_root)
            relative_new = new_path.relative_to(self.project_root)

            if self.dry_run:
                print(f"  WOULD RENAME: {relative_old} → {relative_new}")
                success_count += 1
            else:
                try:
                    if new_path.exists():
                        print(f"  ⚠️  SKIP (target exists): {relative_old}")
                        continue

                    # Rename file
                    os.rename(old_path, new_path)
                    print(f"  ✅ RENAMED: {relative_old} → {relative_new}")
                    success_count += 1
                except Exception as e:
                    print(f"  ❌ ERROR: {relative_old}: {e}")

        return success_count

    def scan_content_references(self) -> None:
        """Scan files for content references to migrated files"""
        print(f"\n🔍 Scanning for content references...")

        # Create mapping of old to new names
        name_mapping = {}
        for old_path, new_path in self.migrations:
            old_name = old_path.name
            new_name = new_path.name
            # Also track names without extension
            old_base = old_path.stem
            new_base = new_path.stem
            name_mapping[old_name] = new_name
            name_mapping[old_base] = new_base

        # Scan all text files
        text_extensions = ['.py', '.yaml', '.yml', '.json', '.md', '.txt', '.ts', '.js']
        for file_path in self.project_root.rglob("*"):
            if ".git" in str(file_path) or not file_path.is_file():
                continue
            if file_path.suffix not in text_extensions:
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for references
                updates = []
                for old_name, new_name in name_mapping.items():
                    if old_name in content and old_name != new_name:
                        updates.append((old_name, new_name))

                if updates:
                    self.content_updates[str(file_path)] = updates
            except (UnicodeDecodeError, PermissionError):
                # Skip binary or permission-denied files
                pass

    def update_content_references(self) -> int:
        """Update content references in files"""
        update_count = 0
        print(f"\n📝 {'[DRY RUN] ' if self.dry_run else ''}Updating content references...")

        for file_path, updates in self.content_updates.items():
            relative_path = Path(file_path).relative_to(self.project_root)

            if self.dry_run:
                print(f"  WOULD UPDATE: {relative_path}")
                for old, new in updates:
                    print(f"    - {old} → {new}")
                update_count += 1
            else:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Apply updates
                    for old_name, new_name in updates:
                        content = content.replace(old_name, new_name)

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    print(f"  ✅ UPDATED: {relative_path}")
                    for old, new in updates:
                        print(f"    - {old} → {new}")
                    update_count += 1
                except Exception as e:
                    print(f"  ❌ ERROR: {relative_path}: {e}")

        return update_count

    def run_full_migration(self) -> Dict[str, int]:
        """Run complete migration process"""
        print("="*60)
        print(f"🚀 Governance Naming Migration - {'DRY RUN' if self.dry_run else 'LIVE'}")
        print("="*60)

        # Step 1: Scan
        deprecated_files = self.scan_deprecated()
        print(f"\n📊 Found {len(deprecated_files)} files with deprecated prefixes")

        # Step 2: Plan
        self.plan_migrations(deprecated_files)

        # Step 3: Execute file renames
        renamed_count = self.execute_migrations()

        # Step 4: Scan content references
        self.scan_content_references()
        print(f"   Found {len(self.content_updates)} files with content references")

        # Step 5: Update content
        updated_count = self.update_content_references()

        # Summary
        print("\n" + "="*60)
        print("📈 MIGRATION SUMMARY")
        print("="*60)
        print(f"  Files renamed: {renamed_count}/{len(self.migrations)}")
        print(f"  Content files updated: {updated_count}/{len(self.content_updates)}")
        print("="*60)

        return {
            "files_renamed": renamed_count,
            "files_planned": len(self.migrations),
            "content_updated": updated_count,
            "content_found": len(self.content_updates)
        }


if __name__ == "__main__":
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "."
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv

    migrator = GovNamingMigrationFull(root, dry_run=dry_run)
    results = migrator.run_full_migration()

    if dry_run:
        print("\n💡 Run without --dry-run to execute migration")
    else:
        print("\n✅ Migration completed!")
