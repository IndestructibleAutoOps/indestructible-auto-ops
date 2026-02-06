#!/usr/bin/env python3
"""
MNGA 命名規範強制執行器
GL20-29 Naming Convention Enforcer

完整實現多層次命名檢查：
1. 目錄命名 (kebab-case)
2. 文件命名 (依類型區分)
3. 代碼內部命名 (類別/函數/變數)
4. GL 語義錨點命名
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class NamingViolation:
    """命名違規記錄"""

    rule_id: str
    category: str  # directory, file, code, gl_semantic
    path: str
    name: str
    expected_style: str
    actual_style: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    message: str
    suggestion: str
    line_number: Optional[int] = None
    auto_fixable: bool = False


@dataclass
class NamingReport:
    """命名檢查報告"""

    total_items_scanned: int = 0
    directories_scanned: int = 0
    files_scanned: int = 0
    code_elements_scanned: int = 0
    violations: List[NamingViolation] = field(default_factory=list)
    by_severity: Dict[str, int] = field(default_factory=dict)
    by_category: Dict[str, int] = field(default_factory=dict)
    execution_time_ms: int = 0


class NamingEnforcer:
    """命名規範強制執行器"""

    def __init__(self, workspace_path: Path):
        self.workspace = workspace_path
        self.violations: List[NamingViolation] = []

        # 命名模式定義
        self.patterns = {
            "kebab-case": re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$"),
            "snake_case": re.compile(r"^[a-z][a-z0-9_]*$"),
            "UPPER_SNAKE_CASE": re.compile(r"^[A-Z][A-Z0-9_]*$"),
            "PascalCase": re.compile(r"^[A-Z][a-zA-Z0-9]*$"),
            "camelCase": re.compile(r"^[a-z][a-zA-Z0-9]*$"),
        }

        # 排除目錄
        self.excluded_dirs = {
            ".git",
            "__pycache__",
            "node_modules",
            ".venv",
            "venv",
            ".idea",
            ".vscode",
            ".pytest_cache",
            ".mypy_cache",
            "dist",
            "build",
            "egg-info",
            ".eggs",
            ".tox",
            "htmlcov",
            ".coverage",
            "outputs",
            ".governance",
        }

        # 特殊目錄例外（不檢查命名）
        self.special_dir_exceptions = {
            ".github",  # GitHub 標準目錄
            "PULL_REQUEST_TEMPLATE",  # GitHub PR 模板目錄
            "ISSUE_TEMPLATE",  # GitHub Issue 模板目錄
            "(tabs)",  # Next.js/Expo 路由目錄
            "(auth)",  # Next.js/Expo 路由目錄
            "(app)",  # Next.js/Expo 路由目錄
            "RUNBOOKS",  # 文檔標準目錄
            "TRAINING",  # 文檔標準目錄
            "MIGRATION",  # 文檔標準目錄
        }

        # GL 語義目錄模式（允許大寫開頭）
        self.gl_semantic_pattern = re.compile(r"^GL\d{2}(-\d{2})?(-[A-Za-z-]+)?$")

        # 排除文件
        self.excluded_files = {
            ".gitignore",
            ".gitattributes",
            ".dockerignore",
            "Dockerfile",
            "Makefile",
            "LICENSE",
            "CODEOWNERS",
            ".env",
            ".env.example",
            ".editorconfig",
            "requirements.txt",
            "setup.py",
            "setup.cfg",
            "pyproject.toml",
            "poetry.lock",
            "Pipfile",
            "Pipfile.lock",
            "package.json",
            "package-lock.json",
            "yarn.lock",
            "tsconfig.json",
            "webpack.config.js",
            "babel.config.js",
            ".eslintrc",
            ".prettierrc",
            ".babelrc",
        }

        # Python 包目錄 (允許 snake_case)
        self.python_package_indicators = {"__init__.py"}

    def check_style(self, name: str, expected_style: str) -> bool:
        """檢查名稱是否符合指定風格"""
        if expected_style not in self.patterns:
            return True
        return bool(self.patterns[expected_style].match(name))

    def detect_style(self, name: str) -> str:
        """檢測名稱的實際風格"""
        for style, pattern in self.patterns.items():
            if pattern.match(name):
                return style

        if "_" in name and name.islower():
            return "snake_case (invalid)"
        if "-" in name:
            return "kebab-case (invalid)"
        if name[0].isupper():
            return "PascalCase (invalid)"
        return "unknown"

    def suggest_fix(self, name: str, target_style: str) -> str:
        """建議修復名稱"""
        # 移除擴展名
        base_name = name
        ext = ""
        if "." in name:
            parts = name.rsplit(".", 1)
            if len(parts[1]) <= 5:  # 合理的擴展名長度
                base_name, ext = parts
                ext = "." + ext

        # 轉換風格
        if target_style == "kebab-case":
            # 將下劃線和駝峰轉為 kebab-case
            result = re.sub(r"([a-z])([A-Z])", r"\1-\2", base_name)
            result = result.replace("_", "-").lower()
        elif target_style == "snake_case":
            # 將連字符和駝峰轉為 snake_case
            result = re.sub(r"([a-z])([A-Z])", r"\1_\2", base_name)
            result = result.replace("-", "_").lower()
        elif target_style == "PascalCase":
            # 轉為 PascalCase
            words = re.split(r"[-_]", base_name)
            result = "".join(word.capitalize() for word in words)
        elif target_style == "UPPER_SNAKE_CASE":
            result = re.sub(r"([a-z])([A-Z])", r"\1_\2", base_name)
            result = result.replace("-", "_").upper()
        else:
            result = base_name

        return result + ext

    def is_python_package(self, dir_path: Path) -> bool:
        """檢查目錄是否是 Python 包"""
        return (dir_path / "__init__.py").exists()

    def should_exclude_dir(self, dir_path: Path) -> bool:
        """檢查是否應排除目錄"""
        name = dir_path.name

        # 排除隱藏目錄和特殊目錄
        if name.startswith(".") and name not in {".github", ".governance"}:
            return True
        if name in self.excluded_dirs:
            return True
        if name.endswith(".egg-info"):
            return True

        # 檢查路徑中是否包含排除目錄
        for part in dir_path.parts:
            if part in self.excluded_dirs:
                return True

        return False

    def should_exclude_file(self, file_path: Path) -> bool:
        """檢查是否應排除文件"""
        name = file_path.name

        if name in self.excluded_files:
            return True
        if name.startswith("."):
            return True

        # 檢查路徑中是否包含排除目錄
        for part in file_path.parts:
            if part in self.excluded_dirs:
                return True

        return False

    def check_directory_naming(self) -> List[NamingViolation]:
        """檢查目錄命名規範"""
        violations = []

        for dir_path in self.workspace.rglob("*"):
            if not dir_path.is_dir():
                continue
            if self.should_exclude_dir(dir_path):
                continue

            name = dir_path.name
            rel_path = str(dir_path.relative_to(self.workspace))

            # 特殊目錄例外
            if name in self.special_dir_exceptions:
                continue

            # GL 語義目錄例外（允許 GL00-99 格式）
            if self.gl_semantic_pattern.match(name):
                continue

            # Python 包目錄允許 snake_case
            if self.is_python_package(dir_path):
                if not (
                    self.check_style(name, "snake_case")
                    or self.check_style(name, "kebab-case")
                    or name.isalnum()
                ):
                    violations.append(
                        NamingViolation(
                            rule_id="GL20-DIR-002",
                            category="directory",
                            path=rel_path,
                            name=name,
                            expected_style="snake_case (Python package)",
                            actual_style=self.detect_style(name),
                            severity="MEDIUM",
                            message=f"Python 包目錄 '{name}' 命名不規範",
                            suggestion=self.suggest_fix(name, "snake_case"),
                            auto_fixable=False,  # Python 包重命名需要更新 import
                        )
                    )
                continue

            # 一般目錄應使用 kebab-case
            if not self.check_style(name, "kebab-case"):
                # 檢查是否使用了下劃線
                if "_" in name:
                    violations.append(
                        NamingViolation(
                            rule_id="GL20-DIR-001",
                            category="directory",
                            path=rel_path,
                            name=name,
                            expected_style="kebab-case",
                            actual_style=self.detect_style(name),
                            severity="MEDIUM",
                            message=f"目錄 '{name}' 使用下劃線，應使用連字符 (kebab-case)",
                            suggestion=self.suggest_fix(name, "kebab-case"),
                            auto_fixable=True,
                        )
                    )
                elif not name[0].islower():
                    violations.append(
                        NamingViolation(
                            rule_id="GL20-DIR-003",
                            category="directory",
                            path=rel_path,
                            name=name,
                            expected_style="kebab-case",
                            actual_style=self.detect_style(name),
                            severity="LOW",
                            message=f"目錄 '{name}' 應以小寫字母開頭",
                            suggestion=self.suggest_fix(name, "kebab-case"),
                            auto_fixable=True,
                        )
                    )

        return violations

    def check_file_naming(self) -> List[NamingViolation]:
        """檢查文件命名規範"""
        violations = []

        for file_path in self.workspace.rglob("*"):
            if not file_path.is_file():
                continue
            if self.should_exclude_file(file_path):
                continue

            name = file_path.name
            rel_path = str(file_path.relative_to(self.workspace))
            suffix = file_path.suffix.lower()
            stem = file_path.stem

            # Python 文件應使用 snake_case
            if suffix == ".py":
                # 排除特殊文件
                if name.startswith("__") and name.endswith("__.py"):
                    continue

                if not self.check_style(stem, "snake_case"):
                    # 檢查是否使用了連字符
                    if "-" in stem:
                        violations.append(
                            NamingViolation(
                                rule_id="GL20-FILE-001",
                                category="file",
                                path=rel_path,
                                name=name,
                                expected_style="snake_case",
                                actual_style=self.detect_style(stem),
                                severity="HIGH",
                                message=f"Python 文件 '{name}' 使用連字符，應使用下劃線 (snake_case)",
                                suggestion=self.suggest_fix(name, "snake_case"),
                                auto_fixable=True,
                            )
                        )
                    elif stem[0].isupper():
                        violations.append(
                            NamingViolation(
                                rule_id="GL20-FILE-002",
                                category="file",
                                path=rel_path,
                                name=name,
                                expected_style="snake_case",
                                actual_style=self.detect_style(stem),
                                severity="MEDIUM",
                                message=f"Python 文件 '{name}' 應以小寫字母開頭",
                                suggestion=self.suggest_fix(name, "snake_case"),
                                auto_fixable=True,
                            )
                        )

            # 配置文件應使用 kebab-case
            elif suffix in {".yaml", ".yml", ".json", ".toml"}:
                # 排除特殊配置文件
                if name in self.excluded_files:
                    continue
                # GL 語義文件有特殊格式
                if stem.startswith("GL") and re.match(r"^GL\d{2}", stem):
                    continue

                if not self.check_style(stem, "kebab-case"):
                    if "_" in stem:
                        violations.append(
                            NamingViolation(
                                rule_id="GL20-FILE-003",
                                category="file",
                                path=rel_path,
                                name=name,
                                expected_style="kebab-case",
                                actual_style=self.detect_style(stem),
                                severity="MEDIUM",
                                message=f"配置文件 '{name}' 使用下劃線，應使用連字符 (kebab-case)",
                                suggestion=self.suggest_fix(name, "kebab-case"),
                                auto_fixable=True,
                            )
                        )

            # Markdown 文件
            elif suffix == ".md":
                # 允許全大寫 (README, CHANGELOG) 或 kebab-case
                if not (
                    self.check_style(stem, "kebab-case")
                    or stem.isupper()
                    or stem
                    in {"README", "CHANGELOG", "CONTRIBUTING", "LICENSE", "SECURITY"}
                ):
                    if "_" in stem:
                        violations.append(
                            NamingViolation(
                                rule_id="GL20-FILE-004",
                                category="file",
                                path=rel_path,
                                name=name,
                                expected_style="kebab-case or UPPER_CASE",
                                actual_style=self.detect_style(stem),
                                severity="LOW",
                                message=f"Markdown 文件 '{name}' 命名不規範",
                                suggestion=self.suggest_fix(name, "kebab-case"),
                                auto_fixable=True,
                            )
                        )

            # Shell 腳本
            elif suffix == ".sh":
                if not self.check_style(stem, "kebab-case"):
                    if "_" in stem:
                        violations.append(
                            NamingViolation(
                                rule_id="GL20-FILE-005",
                                category="file",
                                path=rel_path,
                                name=name,
                                expected_style="kebab-case",
                                actual_style=self.detect_style(stem),
                                severity="LOW",
                                message=f"Shell 腳本 '{name}' 應使用 kebab-case",
                                suggestion=self.suggest_fix(name, "kebab-case"),
                                auto_fixable=True,
                            )
                        )

        return violations

    def check_python_code_naming(self, file_path: Path) -> List[NamingViolation]:
        """檢查 Python 代碼內部命名"""
        violations = []
        rel_path = str(file_path.relative_to(self.workspace))

        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content)
        except (SyntaxError, UnicodeDecodeError):
            return violations

        for node in ast.walk(tree):
            # 檢查類別命名
            if isinstance(node, ast.ClassDef):
                name = node.name
                if not self.check_style(name, "PascalCase"):
                    violations.append(
                        NamingViolation(
                            rule_id="GL20-CODE-001",
                            category="code",
                            path=rel_path,
                            name=name,
                            expected_style="PascalCase",
                            actual_style=self.detect_style(name),
                            severity="HIGH",
                            message=f"類別 '{name}' 應使用 PascalCase",
                            suggestion=self.suggest_fix(name, "PascalCase"),
                            line_number=node.lineno,
                            auto_fixable=False,
                        )
                    )

            # 檢查函數命名
            elif isinstance(node, ast.FunctionDef):
                name = node.name
                # 排除魔術方法和私有方法
                if name.startswith("__") and name.endswith("__"):
                    continue
                if not self.check_style(name, "snake_case"):
                    # 允許私有方法 _name
                    if name.startswith("_") and self.check_style(
                        name[1:], "snake_case"
                    ):
                        continue
                    violations.append(
                        NamingViolation(
                            rule_id="GL20-CODE-002",
                            category="code",
                            path=rel_path,
                            name=name,
                            expected_style="snake_case",
                            actual_style=self.detect_style(name),
                            severity="MEDIUM",
                            message=f"函數 '{name}' 應使用 snake_case",
                            suggestion=self.suggest_fix(name, "snake_case"),
                            line_number=node.lineno,
                            auto_fixable=False,
                        )
                    )

            # 檢查常數命名 (模組級別的全大寫賦值)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        # 如果看起來像常數 (全大寫)
                        if name.isupper() and not self.check_style(
                            name, "UPPER_SNAKE_CASE"
                        ):
                            violations.append(
                                NamingViolation(
                                    rule_id="GL20-CODE-003",
                                    category="code",
                                    path=rel_path,
                                    name=name,
                                    expected_style="UPPER_SNAKE_CASE",
                                    actual_style=self.detect_style(name),
                                    severity="LOW",
                                    message=f"常數 '{name}' 應使用 UPPER_SNAKE_CASE",
                                    suggestion=self.suggest_fix(
                                        name, "UPPER_SNAKE_CASE"
                                    ),
                                    line_number=node.lineno,
                                    auto_fixable=False,
                                )
                            )

        return violations

    def check_all_python_code(self) -> List[NamingViolation]:
        """檢查所有 Python 文件的代碼命名"""
        violations = []

        for file_path in self.workspace.rglob("*.py"):
            if self.should_exclude_file(file_path):
                continue
            violations.extend(self.check_python_code_naming(file_path))

        return violations

    def run_full_check(self) -> NamingReport:
        """執行完整命名檢查"""
        start_time = datetime.now()
        report = NamingReport()

        # 1. 目錄命名檢查
        dir_violations = self.check_directory_naming()
        report.violations.extend(dir_violations)
        report.directories_scanned = sum(
            1 for _ in self.workspace.rglob("*") if _.is_dir()
        )

        # 2. 文件命名檢查
        file_violations = self.check_file_naming()
        report.violations.extend(file_violations)
        report.files_scanned = sum(1 for _ in self.workspace.rglob("*") if _.is_file())

        # 3. 代碼命名檢查 (可選，較慢)
        # code_violations = self.check_all_python_code()
        # report.violations.extend(code_violations)

        # 統計
        report.total_items_scanned = report.directories_scanned + report.files_scanned

        for v in report.violations:
            report.by_severity[v.severity] = report.by_severity.get(v.severity, 0) + 1
            report.by_category[v.category] = report.by_category.get(v.category, 0) + 1

        report.execution_time_ms = int(
            (datetime.now() - start_time).total_seconds() * 1000
        )

        return report

    def generate_fix_script(self, violations: List[NamingViolation]) -> str:
        """生成修復腳本"""
        lines = [
            "#!/bin/bash",
            "# MNGA Naming Convention Fix Script",
            "# Generated automatically",
            "",
            "set -e",
            "",
        ]

        # 按路徑深度排序 (深的先處理)
        fixable = [v for v in violations if v.auto_fixable]
        fixable.sort(key=lambda v: v.path.count("/"), reverse=True)

        for v in fixable:
            old_path = v.path
            if v.category == "directory":
                new_name = v.suggestion
                parent = str(Path(old_path).parent)
                new_path = f"{parent}/{new_name}" if parent != "." else new_name
                lines.append(f"# {v.message}")
                lines.append(
                    f'git mv "{old_path}" "{new_path}" 2>/dev/null || mv "{old_path}" "{new_path}"'
                )
                lines.append("")
            elif v.category == "file":
                new_name = v.suggestion
                parent = str(Path(old_path).parent)
                new_path = f"{parent}/{new_name}" if parent != "." else new_name
                lines.append(f"# {v.message}")
                lines.append(
                    f'git mv "{old_path}" "{new_path}" 2>/dev/null || mv "{old_path}" "{new_path}"'
                )
                lines.append("")

        lines.append('echo "Fix complete!"')
        return "\n".join(lines)


def main():
    """主函數"""
    import argparse

    parser = argparse.ArgumentParser(description="MNGA Naming Convention Enforcer")
    parser.add_argument("--workspace", "-w", default=".", help="Workspace path")
    parser.add_argument("--output", "-o", help="Output report file")
    parser.add_argument("--fix-script", help="Generate fix script")
    parser.add_argument(
        "--check-code", action="store_true", help="Also check code naming"
    )
    parser.add_argument(
        "--severity",
        choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        default="LOW",
        help="Minimum severity to report",
    )

    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    enforcer = NamingEnforcer(workspace)

    print(f"\n{'='*70}")
    print(f"{'MNGA 命名規範檢查器':^70}")
    print(f"{'='*70}\n")

    report = enforcer.run_full_check()

    if args.check_code:
        code_violations = enforcer.check_all_python_code()
        report.violations.extend(code_violations)
        for v in code_violations:
            report.by_severity[v.severity] = report.by_severity.get(v.severity, 0) + 1
            report.by_category[v.category] = report.by_category.get(v.category, 0) + 1

    # 過濾嚴重性
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    min_severity = severity_order.get(args.severity, 3)
    filtered_violations = [
        v
        for v in report.violations
        if severity_order.get(v.severity, 3) <= min_severity
    ]

    # 輸出結果
    print(f"掃描項目: {report.total_items_scanned}")
    print(f"  - 目錄: {report.directories_scanned}")
    print(f"  - 文件: {report.files_scanned}")
    print(f"執行時間: {report.execution_time_ms}ms")
    print(f"\n發現違規: {len(filtered_violations)}")

    if report.by_severity:
        print("\n按嚴重性:")
        for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if sev in report.by_severity:
                print(f"  {sev}: {report.by_severity[sev]}")

    if report.by_category:
        print("\n按類別:")
        for cat, count in report.by_category.items():
            print(f"  {cat}: {count}")

    if filtered_violations:
        print(f"\n{'='*70}")
        print("違規詳情:")
        print(f"{'='*70}")

        for v in filtered_violations[:50]:  # 只顯示前50個
            print(f"\n[{v.severity}] {v.rule_id}")
            print(f"  路徑: {v.path}")
            print(f"  名稱: {v.name}")
            print(f"  問題: {v.message}")
            print(f"  建議: {v.suggestion}")
            if v.line_number:
                print(f"  行號: {v.line_number}")

        if len(filtered_violations) > 50:
            print(f"\n... 還有 {len(filtered_violations) - 50} 個違規未顯示")

    # 保存報告
    if args.output:
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "workspace": str(workspace),
            "summary": {
                "total_scanned": report.total_items_scanned,
                "directories": report.directories_scanned,
                "files": report.files_scanned,
                "violations": len(report.violations),
                "by_severity": report.by_severity,
                "by_category": report.by_category,
            },
            "violations": [
                {
                    "rule_id": v.rule_id,
                    "category": v.category,
                    "path": v.path,
                    "name": v.name,
                    "expected_style": v.expected_style,
                    "actual_style": v.actual_style,
                    "severity": v.severity,
                    "message": v.message,
                    "suggestion": v.suggestion,
                    "line_number": v.line_number,
                    "auto_fixable": v.auto_fixable,
                }
                for v in report.violations
            ],
        }

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print(f"\n報告已保存至: {args.output}")

    # 生成修復腳本
    if args.fix_script:
        script = enforcer.generate_fix_script(report.violations)
        with open(args.fix_script, "w") as f:
            f.write(script)
        print(f"修復腳本已保存至: {args.fix_script}")

    # 返回狀態碼
    critical_count = report.by_severity.get("CRITICAL", 0) + report.by_severity.get(
        "HIGH", 0
    )
    return 1 if critical_count > 0 else 0


if __name__ == "__main__":
    exit(main())
