#!/usr/bin/env python3
"""
GL Platform Consolidation Tool
自動整合根目錄的 GL 平台到統一架構
"""

import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List

# 平台遷移映射表
CONSOLIDATION_MAP = {
    # GL00-09: 企業架構層
    "gl00-09-enterprise-architecture": {
        "gl-enterprise-architecture": "specifications/",
        "gl-governance-architecture-platform": "governance/",
    },
    # GL10-19: 平台服務層
    "gl10-19-platform-services": {
        "gl-platform-core-platform": "core/",
        "gl-platform-services": "services/",
    },
    # GL20-29: 數據處理層
    "gl20-29-data-processing": {
        "gl-data-processing": "processing/",
        "gl-data-processing-platform": "processing-platform/",
        "gl-search-elasticsearch-platform": "search/",
    },
    # GL30-49: 運行時執行層
    "gl30-49-runtime-execution": {
        "gl-execution-runtime": "execution/",
        "gl-runtime-engine-platform": "engine/",
        "gl-runtime-execution-platform": "execution-platform/",
        "gl-runtime-services-platform": "services/",
    },
    # GL50-59: 監控可觀測性層
    "gl50-59-monitoring-observability": {
        "gl-monitoring-observability-platform": "monitoring/",
        "gl-monitoring-system-platform": "system/",
        "gl-observability": "observability/",
    },
    # GL60-80: 治理合規層
    "gl60-80-governance-compliance": {
        "gl-governance-compliance": "compliance/",
        "gl-governance-compliance-platform": "compliance-platform/",
    },
    # GL81-83: 擴展服務層
    "gl81-83-extension-services": {
        "gl-extension-services": "extensions/",
        "gl-extension-services-platform": "extensions-platform/",
        "gl-integration-hub-platform": "integrations/",
    },
    # GL90-99: 元規範層
    "gl90-99-meta-specifications": {
        "gl-meta-specifications": "specifications/",
        "gl-meta-specifications-platform": "specifications-platform/",
        "gl-semantic-core-platform": "semantic-core/",
    },
}

# 專項平台遷移到 platforms/
SPECIAL_PLATFORMS = {
    "gl-automation-instant-platform": "platforms/automation/instant/",
    "gl-automation-organizer-platform": "platforms/automation/organizer/",
    "gl-quantum-computing-platform": "platforms/quantum/",
    "gl-infrastructure-foundation-platform": "platforms/infrastructure/",
}


class PlatformConsolidator:
    def __init__(
        self, workspace_root: Path, dry_run: bool = True, skip_backup: bool = False
    ):
        self.root = workspace_root
        self.dry_run = dry_run
        self.skip_backup = skip_backup
        self.moved_dirs = []
        self.errors = []

    def backup_current_state(self):
        """創建備份"""
        print("📦 Creating backup...")
        if self.skip_backup:
            print("   Skipped (backup disabled)")
            return

        if not self.dry_run:
            subprocess.run(
                ["git", "add", "-A"],
                cwd=self.root,
                check=True,
            )
            subprocess.run(
                [
                    "git",
                    "commit",
                    "-m",
                    "backup: before platform consolidation",
                    "--allow-empty",
                ],
                cwd=self.root,
            )
            tag_name = f"platform-consolidation-backup"
            subprocess.run(
                ["git", "tag", "-f", tag_name],
                cwd=self.root,
                check=True,
            )
            print(f"✅ Backup created with tag: {tag_name}")
        else:
            print("   [DRY RUN] Would create git backup")

    def create_new_structure(self):
        """創建新的目錄結構"""
        print("\n📁 Creating new directory structure...")
        for target_dir in CONSOLIDATION_MAP.keys():
            target_path = self.root / target_dir
            if not self.dry_run:
                target_path.mkdir(parents=True, exist_ok=True)
                print(f"   ✓ Created: {target_dir}")
            else:
                print(f"   [DRY RUN] Would create: {target_dir}")

        # 創建 platforms 子目錄
        for target in set(p.split("/")[0] for p in SPECIAL_PLATFORMS.values()):
            target_path = self.root / target
            if not self.dry_run:
                target_path.mkdir(parents=True, exist_ok=True)
            else:
                print(f"   [DRY RUN] Would create: {target}")

    def migrate_platforms(self):
        """遷移平台目錄"""
        print("\n🔄 Migrating platforms...")

        # 遷移到 GL 層級目錄
        for target_dir, sources in CONSOLIDATION_MAP.items():
            print(f"\n   → {target_dir}:")
            for source_name, sub_path in sources.items():
                source_path = self.root / source_name
                target_path = self.root / target_dir / sub_path

                if source_path.exists():
                    if not self.dry_run:
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(source_path), str(target_path))
                        self.moved_dirs.append(
                            (source_name, f"{target_dir}/{sub_path}")
                        )
                        print(f"     ✓ {source_name} → {sub_path}")
                    else:
                        print(f"     [DRY RUN] Would move: {source_name} → {sub_path}")
                else:
                    msg = f"     ⚠ Source not found: {source_name}"
                    print(msg)
                    self.errors.append(msg)

        # 遷移專項平台
        print("\n   → Special Platforms:")
        for source_name, target_rel in SPECIAL_PLATFORMS.items():
            source_path = self.root / source_name
            target_path = self.root / target_rel

            if source_path.exists():
                if not self.dry_run:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source_path), str(target_path))
                    self.moved_dirs.append((source_name, target_rel))
                    print(f"     ✓ {source_name} → {target_rel}")
                else:
                    print(f"     [DRY RUN] Would move: {source_name} → {target_rel}")
            else:
                msg = f"     ⚠ Source not found: {source_name}"
                print(msg)

    def generate_report(self):
        """生成遷移報告"""
        print("\n📊 Generating migration report...")

        report = {
            "timestamp": "2026-02-06",
            "dry_run": self.dry_run,
            "moved_directories": len(self.moved_dirs),
            "migrations": self.moved_dirs,
            "errors": self.errors,
            "status": "success" if not self.errors else "completed_with_warnings",
        }

        report_path = self.root / "platform-consolidation-report.json"
        if not self.dry_run:
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)
            print(f"   ✓ Report saved to: {report_path}")
        else:
            print(f"   [DRY RUN] Would save report to: {report_path}")

        return report

    def verify_migration(self):
        """驗證遷移完整性"""
        print("\n✅ Verifying migration...")

        # 檢查舊目錄是否還存在
        remaining = []
        for target_dir, sources in CONSOLIDATION_MAP.items():
            for source_name in sources.keys():
                source_path = self.root / source_name
                if source_path.exists():
                    remaining.append(source_name)

        if remaining:
            print(f"   ⚠ Warning: {len(remaining)} old directories still exist:")
            for name in remaining[:5]:
                print(f"     - {name}")
            if len(remaining) > 5:
                print(f"     ... and {len(remaining) - 5} more")
        else:
            print("   ✓ All old directories removed")

        # 檢查新目錄
        created = 0
        for target_dir in CONSOLIDATION_MAP.keys():
            target_path = self.root / target_dir
            if target_path.exists():
                created += 1

        print(f"   ✓ {created}/{len(CONSOLIDATION_MAP)} new directories verified")

    def run(self):
        """執行完整的整合流程"""
        print("=" * 60)
        print("🚀 GL Platform Consolidation Tool")
        print("=" * 60)
        print(
            f"Mode: {'DRY RUN (no changes)' if self.dry_run else 'LIVE (will make changes)'}"
        )
        print(f"Workspace: {self.root}")
        print()

        try:
            # Phase 1: 備份
            self.backup_current_state()

            # Phase 2: 創建結構
            self.create_new_structure()

            # Phase 3: 遷移
            self.migrate_platforms()

            # Phase 4: 驗證
            if not self.dry_run:
                self.verify_migration()

            # Phase 5: 報告
            report = self.generate_report()

            print("\n" + "=" * 60)
            print("✨ Consolidation Complete!")
            print("=" * 60)
            print(f"Moved directories: {report['moved_directories']}")
            print(f"Errors: {len(report['errors'])}")
            print(f"Status: {report['status']}")

            if self.dry_run:
                print("\n⚠️  This was a DRY RUN. No changes were made.")
                print("   Run with --execute to apply changes.")

            return 0

        except Exception as e:
            print(f"\n❌ Error during consolidation: {e}")
            import traceback

            traceback.print_exc()
            return 1


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Consolidate GL platforms")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the consolidation (default is dry-run)",
    )
    parser.add_argument(
        "--skip-backup",
        action="store_true",
        help="Skip creating git backup/tag before executing",
    )
    parser.add_argument(
        "--workspace",
        default="/workspace",
        help="Workspace root directory",
    )

    args = parser.parse_args()

    consolidator = PlatformConsolidator(
        workspace_root=Path(args.workspace),
        dry_run=not args.execute,
        skip_backup=args.skip_backup,
    )

    return consolidator.run()


if __name__ == "__main__":
    import sys

    sys.exit(main())
