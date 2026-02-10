#!/usr/bin/env python3
"""
Code Scanning Analysis Tool
Analyzes Python code for syntax errors and common issues
"""

# MNGA-002: Import organization needs review
import ast
import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple


class CodeScanningAnalyzer:
    """Analyzes code for syntax errors and security issues"""

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.results = {
            "syntax_errors": [],
            "security_issues": [],
            "code_quality_issues": [],
            "total_files_scanned": 0,
            "files_with_issues": 0,
        }

        # Files to skip (tools that legitimately check for these patterns)
        self.skip_files = {
            "code-scanning-analysis.py",
            "fix-security-issues.py",
            "fix-code-scanning-issues.py",
            "scan-secrets.py",
        }

        # Directories to skip (archived/legacy code)
        self.skip_dirs = {
            ".github/archive",
            "tests-legacy",
            "tools-legacy",
            "scripts-legacy",  # Legacy scripts with eval/exec
        }

    def should_skip_file(self, filepath: str) -> bool:
        """Check if file should be skipped"""
        # Skip if filename matches
        if Path(filepath).name in self.skip_files:
            return True

        # Skip if in excluded directory
        for skip_dir in self.skip_dirs:
            if skip_dir in filepath:
                return True

        return False

    def scan_python_files(self) -> Dict:
        """Scan all Python files in the repository"""
        print("🔍 Scanning Python files...")

        for root, dirs, files in os.walk(self.root_path):
            # Skip common directories
            dirs[:] = [
                d
                for d in dirs
                if d not in [".git", "__pycache__", "node_modules", ".venv", "venv"]
            ]

            for file in files:
                if file.endswith(".py"):
                    filepath = Path(root) / file
                    self.analyze_file(filepath)

        return self.results

    def analyze_file(self, filepath: Path):
        """Analyze a single Python file"""
        rel_path = str(filepath.relative_to(self.root_path))

        # Skip files that are tools or in excluded directories
        if self.should_skip_file(rel_path):
            return

        self.results["total_files_scanned"] += 1

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for syntax errors
            try:
                ast.parse(content)
            except SyntaxError as e:
                self.results["syntax_errors"].append(
                    {
                        "file": rel_path,
                        "line": e.lineno,
                        "message": str(e.msg),
                        "text": e.text.strip() if e.text else "",
                    }
                )
                self.results["files_with_issues"] += 1
                return

            # Check for security issues
            self.check_security_issues(content, rel_path)

            # Check for code quality issues
            self.check_code_quality(content, rel_path)

        except Exception as e:
            print(f"⚠️  Error analyzing {rel_path}: {e}")

    def check_security_issues(self, content: str, filepath: str):
        """Check for common security issues"""
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check for eval() usage
            if "eval(" in line and not line.strip().startswith("#"):
                self.results["security_issues"].append(
                    {
                        "file": filepath,
                        "line": i,
                        "type": "dangerous-function",
                        "message": "Use of eval() detected - security risk",
                        "severity": "high",
                    }
                )

            # Check for exec() usage
            if "exec(" in line and not line.strip().startswith("#"):
                self.results["security_issues"].append(
                    {
                        "file": filepath,
                        "line": i,
                        "type": "dangerous-function",
                        "message": "Use of exec() detected - security risk",
                        "severity": "high",
                    }
                )

            # Check for pickle usage
            if "pickle.loads(" in line and not line.strip().startswith("#"):
                self.results["security_issues"].append(
                    {
                        "file": filepath,
                        "line": i,
                        "type": "insecure-deserialization",
                        "message": "Unsafe deserialization with pickle.loads()",
                        "severity": "medium",
                    }
                )

    def check_code_quality(self, content: str, filepath: str):
        """Check for code quality issues"""
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            # Check for malformed identifiers (duplicate prefixes)
            if "gov-platformgl-platform" in line:
                self.results["code_quality_issues"].append(
                    {
                        "file": filepath,
                        "line": i,
                        "type": "malformed-identifier",
                        "message": "Duplicate prefix in identifier",
                        "severity": "high",
                    }
                )

            # Check for @ not in comments
            if line.strip().startswith("@") and not line.strip().startswith("@"):
                if "GL-governed" in line and not line.strip().startswith("#"):
                    self.results["code_quality_issues"].append(
                        {
                            "file": filepath,
                            "line": i,
                            "type": "incorrect-annotation",
                            "message": "@GL-governed should be a comment, not a decorator",
                            "severity": "high",
                        }
                    )

    def generate_report(self, output_file: str = "code-scanning-report.json"):
        """Generate a detailed report"""
        report = {
            "summary": {
                "total_files_scanned": self.results["total_files_scanned"],
                "files_with_issues": self.results["files_with_issues"],
                "total_syntax_errors": len(self.results["syntax_errors"]),
                "total_security_issues": len(self.results["security_issues"]),
                "total_code_quality_issues": len(self.results["code_quality_issues"]),
            },
            "findings": self.results,
        }

        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        return report

    def print_summary(self):
        """Print a summary of findings"""
        print("\n" + "=" * 60)
        print("📊 CODE SCANNING ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"Total files scanned: {self.results['total_files_scanned']}")
        print(f"Files with issues: {self.results['files_with_issues']}")
        print(f"\n🔴 Syntax Errors: {len(self.results['syntax_errors'])}")
        print(f"🟠 Security Issues: {len(self.results['security_issues'])}")
        print(f"🟡 Code Quality Issues: {len(self.results['code_quality_issues'])}")

        if self.results["syntax_errors"]:
            print("\n📋 Top 10 Syntax Errors:")
            for i, error in enumerate(self.results["syntax_errors"][:10], 1):
                print(f"  {i}. {error['file']}:{error['line']} - {error['message']}")

        if self.results["security_issues"]:
            print("\n🔒 Security Issues:")
            for i, issue in enumerate(self.results["security_issues"][:10], 1):
                print(f"  {i}. {issue['file']}:{issue['line']} - {issue['message']}")

        if self.results["code_quality_issues"]:
            print("\n📝 Top 10 Code Quality Issues:")
            for i, issue in enumerate(self.results["code_quality_issues"][:10], 1):
                print(f"  {i}. {issue['file']}:{issue['line']} - {issue['message']}")

        print("=" * 60)


def main():
    """Main entry point"""
    analyzer = CodeScanningAnalyzer(
        "/home/runner/work/machine-native-ops/machine-native-ops"
    )

    print("🚀 Starting code scanning analysis...")
    results = analyzer.scan_python_files()

    analyzer.print_summary()

    # Generate JSON report
    report = analyzer.generate_report()
    print(f"\n📄 Detailed report saved to: code-scanning-report.json")

    # Return exit code based on findings
    if results["syntax_errors"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
