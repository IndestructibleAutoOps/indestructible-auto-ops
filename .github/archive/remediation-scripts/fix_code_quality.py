# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: archive-tools
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
"""
Automated Code Quality Fixes

This script fixes low-severity code quality issues using:
- isort: Import ordering
- autopep8: Code style fixes
- black: Code formatting
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class CodeQualityFixer:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.fixed_files = []
        self.errors = []

    def run_command(self, cmd: List[str], description: str) -> Tuple[bool, str]:
        """Run a command and return success status and output."""
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.project_root
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)

    def fix_import_order(self, file_path: Path) -> bool:
        """Fix import ordering using isort."""
        cmd = ["isort", str(file_path)]
        success, output = self.run_command(cmd, f"Fixing imports in {file_path}")
        if success:
            self.fixed_files.append(("import_order", file_path))
        return success

    def fix_code_style(self, file_path: Path) -> bool:
        """Fix code style using autopep8."""
        cmd = ["autopep8", "--in-place", "--aggressive", str(file_path)]
        success, output = self.run_command(cmd, f"Fixing style in {file_path}")
        if success:
            self.fixed_files.append(("code_style", file_path))
        return success

    def format_code(self, file_path: Path) -> bool:
        """Format code using black."""
        cmd = ["black", str(file_path)]
        success, output = self.run_command(cmd, f"Formatting {file_path}")
        if success:
            self.fixed_files.append(("formatting", file_path))
        return success

    def get_python_files(self) -> List[Path]:
        """Get all Python files in the project."""
        python_files = []
        for pattern in ["**/*.py"]:
            python_files.extend(self.project_root.rglob(pattern))

        # Exclude cache and venv directories
        excluded_dirs = {"__pycache__", ".git", "venv", ".venv", "node_modules"}
        return [
            f
            for f in python_files
            if not any(excluded_dir in f.parts for excluded_dir in excluded_dirs)
        ]

    def fix_all_files(self, dry_run: bool = False) -> dict:
        """Fix all Python files in the project."""
        python_files = self.get_python_files()
        total_files = len(python_files)

        print(f"🔍 Found {total_files} Python files to process")
        print("=" * 60)

        results = {
            "total": total_files,
            "fixed_imports": 0,
            "fixed_style": 0,
            "formatted": 0,
            "errors": 0,
        }

        for i, file_path in enumerate(python_files, 1):
            print(
                f"\n[{i}/{total_files}] Processing: {file_path.relative_to(self.project_root)}"
            )

            if dry_run:
                print("  [DRY RUN] Would fix this file")
                continue

            try:
                # Fix import order
                if self.fix_import_order(file_path):
                    results["fixed_imports"] += 1
                    print("  ✅ Imports fixed")

                # Fix code style
                if self.fix_code_style(file_path):
                    results["fixed_style"] += 1
                    print("  ✅ Style fixed")

                # Format code
                if self.format_code(file_path):
                    results["formatted"] += 1
                    print("  ✅ Formatted")

            except Exception as e:
                results["errors"] += 1
                self.errors.append((str(file_path), str(e)))
                print(f"  ❌ Error: {e}")

        return results

    def generate_report(self, results: dict) -> str:
        """Generate a summary report."""
        report = []
        report.append("=" * 60)
        report.append("CODE QUALITY FIX SUMMARY")
        report.append("=" * 60)
        report.append(f"Total files processed: {results['total']}")
        report.append(f"Imports fixed: {results['fixed_imports']}")
        report.append(f"Style fixes: {results['fixed_style']}")
        report.append(f"Files formatted: {results['formatted']}")
        report.append(f"Errors: {results['errors']}")

        if self.errors:
            report.append("\n❌ Errors encountered:")
            for file_path, error in self.errors:
                report.append(f"  - {file_path}: {error}")

        return "\n".join(report)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Automated code quality fixes for machine-native-ops"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes",
    )
    parser.add_argument(
        "--limit", type=int, help="Limit number of files to process (for testing)"
    )

    args = parser.parse_args()

    # Get project root
    project_root = Path.cwd()
    print(f"📁 Project root: {project_root}")
    print("🔧 Starting code quality fixes...")
    print()

    fixer = CodeQualityFixer(project_root)

    if args.limit:
        # For testing, limit to a subset of files
        python_files = fixer.get_python_files()[: args.limit]
        print(f"🧪 Test mode: Processing {args.limit} files")
        print()

        results = {
            "total": args.limit,
            "fixed_imports": 0,
            "fixed_style": 0,
            "formatted": 0,
            "errors": 0,
        }

        for file_path in python_files:
            print(f"Processing: {file_path.relative_to(project_root)}")
            if not args.dry_run:
                if fixer.fix_import_order(file_path):
                    results["fixed_imports"] += 1
                if fixer.fix_code_style(file_path):
                    results["fixed_style"] += 1
                if fixer.format_code(file_path):
                    results["formatted"] += 1
    else:
        results = fixer.fix_all_files(dry_run=args.dry_run)

    print("\n" + fixer.generate_report(results))

    if results["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
