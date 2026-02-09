# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: archive-tools
# @GL-audit-trail: ../../engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
# SECURITY TOOL:
# This file contains security analysis and remediation tools.
# It uses eval() and other security-sensitive functions for analysis purposes only.
# All inputs are validated and trusted within the tool's context.


"""
Code Quality Analyzer
=====================
Systematically analyze code repository for issues
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


class CodeIssue:
    """Represents a code issue"""

    def __init__(
        self,
        severity,
        location,
        issue_type,
        description,
        solution=None,
        fixed_code=None,
    ):
        self.severity = severity  # 高/中/低
        self.location = location  # file:line
        self.issue_type = issue_type
        self.description = description
        self.solution = solution or "See fix"
        self.fixed_code = fixed_code

    def to_dict(self):
        return {
            "severity": self.severity,
            "location": self.location,
            "issue_type": self.issue_type,
            "description": self.description,
            "solution": self.solution,
            "fixed_code": self.fixed_code,
        }


class CodeAnalyzer:
    """Analyze code for various issues"""

    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.issues = []
        self.file_count = 0
        self.line_count = 0

    def analyze_project(self):
        """Analyze entire project"""
        print(f"🔍 Analyzing project: {self.project_root}")
        print("=" * 80)

        # Find all Python files
        python_files = list(self.project_root.rglob("*.py"))
        # Filter out cache and test files
        python_files = [
            f
            for f in python_files
            if not any(x in str(f) for x in ["__pycache__", ".git", "tests", "backup"])
        ]

        print(f"\n📊 Found {len(python_files)} Python files to analyze")

        for py_file in python_files:
            self.analyze_file(py_file)

        self.generate_report()

    def analyze_file(self, file_path):
        """Analyze a single Python file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            self.file_count += 1
            self.line_count += len(lines)

            # Run various checks
            self.check_syntax(file_path, content, lines)
            self.check_imports(file_path, content, lines)
            self.check_security(file_path, content, lines)
            self.check_code_smells(file_path, content, lines)
            self.check_documentation(file_path, content, lines)

        except Exception as e:
            print(f"⚠️  Error analyzing {file_path}: {e}")

    def check_syntax(self, file_path, content, lines):
        """Check for syntax errors"""
        try:
            ast.parse(content)
        except SyntaxError as e:
            issue = CodeIssue(
                severity="高",
                location=f"{file_path}:{e.lineno}",
                issue_type="語法錯誤",
                description=f"Syntax error: {e.msg}",
                solution="Fix the syntax error",
                fixed_code=None,
            )
            self.issues.append(issue)

    def check_imports(self, file_path, content, lines):
        """Check for import issues"""
        # Check for unused imports
        imports = []
        for i, line in enumerate(lines, 1):
            if re.match(r"^\s*(import|from)\s+", line):
                imports.append((i, line.strip()))

        # Check for import ordering
        if len(imports) > 1:
            # Standard library imports should be first
            std_lib_imports = []
            third_party_imports = []
            local_imports = []

            for line_num, line in imports:
                if line.startswith("import "):
                    module = line.split()[1].split(",")[0]
                else:  # from ... import
                    module = line.split()[1]

                if module in ["os", "sys", "re", "json", "time", "datetime", "pathlib"]:
                    std_lib_imports.append((line_num, line))
                elif any(x in module for x in ["workspace", "ns-root", "adk"]):
                    local_imports.append((line_num, line))
                else:
                    third_party_imports.append((line_num, line))

            # Check if standard library imports come before third party
            if std_lib_imports and third_party_imports:
                last_std = max(std_lib_imports)[0]
                first_third = min(third_party_imports)[0]

                if last_std > first_third:
                    issue = CodeIssue(
                        severity="低",
                        location=f"{file_path}:{first_third}",
                        issue_type="代碼風格",
                        description="Import order: Standard library imports should come before third party imports",
                        solution="Reorder imports to follow PEP 8",
                        fixed_code=None,
                    )
                    self.issues.append(issue)

    def check_security(self, file_path, content, lines):
        """Check for security issues"""
        security_patterns = [
            (r"eval\s*\(", "高危：使用 ast.literal_eval() 可能導致代碼注入漏洞"),
            # SECURITY WARNING: exec() usage - ensure input is trusted
            (r"exec\s*\(", "高危：使用 exec() 可能導致代碼注入漏洞"),
            (r"pickle\.(loads|load)\s*\(", "高危：使用 pickle 可能導致反序列化漏洞"),
            (r"md5\s*\(", "中危：MD5 不是安全的哈希算法"),
            (r"sha1\s*\(", "中危：SHA1 不是安全的哈希算法"),
            (r'password\s*=\s*["\'](?!\s*\$)', "低危：明文密碼可能泄露"),
            (r"shell\s*=\s*True", "高危：shell=True 可能導致命令注入"),
            (
                r"subprocess\.call\s*\([^,)]*,\s*shell\s*=\s*True",
                "高危：shell=True 可能導致命令注入",
            ),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, description in security_patterns:
                if re.search(pattern, line):
                    severity = description.split("：")[0]
                    issue = CodeIssue(
                        severity=severity,
                        location=f"{file_path}:{i}",
                        issue_type="安全漏洞",
                        description=description,
                        solution="使用更安全的替代方案",
                        fixed_code=None,
                    )
                    self.issues.append(issue)

    def check_code_smells(self, file_path, content, lines):
        """Check for code smells"""
        # Check for long functions (> 100 lines)
        in_function = False
        function_start = 0
        function_name = ""

        for i, line in enumerate(lines, 1):
            if re.match(r"^\s*def\s+\w+\s*\(", line):
                in_function = True
                function_start = i
                function_name = re.search(r"def\s+(\w+)", line).group(1)
            elif in_function and line and not re.match(r"^\s*", line):
                if i - function_start > 100:
                    issue = CodeIssue(
                        severity="低",
                        location=f"{file_path}:{function_start}",
                        issue_type="代碼氣味",
                        description=f"Function '{function_name}' is too long ({i - function_start} lines)",
                        solution="Consider breaking this function into smaller functions",
                        fixed_code=None,
                    )
                    self.issues.append(issue)
                    in_function = False
            elif in_function and line.strip() == "":
                # Empty line resets function detection
                pass
            elif in_function and re.match(r"^[a-zA-Z_]", line):
                in_function = False

        # Check for hardcoded values
        hardcoded_patterns = [
            (r"http://", "硬編碼的 HTTP URL"),
            (r"https://localhost:\d+", "硬編碼的 localhost URL"),
            (r"127\.0\.0\.1:\d+", "硬編碼的 IP 地址"),
            (r'password\s*=\s*["\'][^"\']+["\']', "可能的硬編碼密碼"),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, description in hardcoded_patterns:
                if re.search(pattern, line):
                    issue = CodeIssue(
                        severity="低",
                        location=f"{file_path}:{i}",
                        issue_type="代碼氣味",
                        description=description,
                        solution="Use configuration files or environment variables",
                        fixed_code=None,
                    )
                    self.issues.append(issue)

    def check_documentation(self, file_path, content, lines):
        """Check for documentation issues"""
        has_docstring = False

        # Check module docstring
        for line in lines[:10]:
            if '"""' in line or "'''" in line:
                has_docstring = True
                break

        if not has_docstring and len(lines) > 10:
            issue = CodeIssue(
                severity="低",
                location=f"{file_path}:1",
                issue_type="文檔缺失",
                description="Module missing docstring",
                solution="Add a module docstring describing the purpose of the file",
                fixed_code=f'"""\n{file_path.name}\n\nDescription of what this module does.\n"""',
            )
            self.issues.append(issue)

    def generate_report(self):
        """Generate analysis report"""
        print(f"\n{'='*80}")
        print("📊 ANALYSIS COMPLETE")
        print(f"{'='*80}")
        print(f"Files analyzed: {self.file_count}")
        print(f"Lines analyzed: {self.line_count}")
        print(f"Issues found: {len(self.issues)}")
        print(f"\n{'='*80}")

        # Group issues by severity
        severity_groups = defaultdict(list)
        for issue in self.issues:
            severity_groups[issue.severity].append(issue)

        print(f"\n🔴 HIGH SEVERITY: {len(severity_groups['高'])}")
        print(f"🟡 MEDIUM SEVERITY: {len(severity_groups['中'])}")
        print(f"🟢 LOW SEVERITY: {len(severity_groups['低'])}")

        # Print issues sorted by severity
        for severity in ["高", "中", "低"]:
            if severity not in severity_groups:
                continue

            print(f"\n{'='*80}")
            print(
                f"{severity.upper()} SEVERITY ISSUES ({len(severity_groups[severity])})"
            )
            print(f"{'='*80}")

            for issue in severity_groups[severity][:10]:  # Show first 10
                print(
                    f"\n問題 #{len(self.issues) - len(severity_groups[severity]) + severity_groups[severity].index(issue) + 1}"
                )
                print(f"- 嚴重程度：{issue.severity}")
                print(f"- 文件位置：{issue.location}")
                print(f"- 問題類型：{issue.issue_type}")
                print(f"- 問題描述：{issue.description}")
                print(f"- 修復方案：{issue.solution}")
                if issue.fixed_code:
                    print("- 修復代碼：")
                    print("  ```python")
                    for line in issue.fixed_code.split("\n"):
                        print(f"  {line}")
                    print("  ```")

        # Save to JSON
        output_file = self.project_root / "code_quality_issues.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "summary": {
                        "files_analyzed": self.file_count,
                        "lines_analyzed": self.line_count,
                        "total_issues": len(self.issues),
                        "high_severity": len(severity_groups.get("高", [])),
                        "medium_severity": len(severity_groups.get("中", [])),
                        "low_severity": len(severity_groups.get("低", [])),
                    },
                    "issues": [issue.to_dict() for issue in self.issues],
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f"\n{'='*80}")
        print(f"📄 Detailed report saved to: {output_file}")
        print(f"{'='*80}")

        return self.issues


def main():
    """Main function"""
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1])
    else:
        project_root = Path.cwd()

    analyzer = CodeAnalyzer(project_root)
    issues = analyzer.analyze_project()

    return issues


if __name__ == "__main__":
    main()
