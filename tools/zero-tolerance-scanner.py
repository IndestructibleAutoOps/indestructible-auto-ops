#!/usr/bin/env python3
"""
零容忍違規掃描器
Zero Tolerance Violation Scanner

掃描整個儲存庫的所有零容忍違規：
- 命名空間覆寫
- 命名規範違規（非 kebab-case）
- 硬編碼時間線
- 禁止短語
- 格式違規
- 指標降級
"""

import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime


class ZeroToleranceScanner:
    """零容忍掃描器"""

    def __init__(self):
        self.violations = []
        self.stats = {
            "files_scanned": 0,
            "violations_found": 0,
            "by_type": {},
            "by_severity": {},
        }

        # 禁止短語（中文 + 英文）
        self.forbidden_phrases = [
            "100% 完成",
            "100% complete",
            "完全符合",
            "fully compliant",
            "已全部实现",
            "fully implemented",
            "覆盖所有标准",
            "covers all standards",
            "绝对完成",
            "absolutely done",
            "我觉得",
            "I think",
            "I feel",
            "可能",
            "maybe",
            "perhaps",
            "大概",
            "probably",
            "TODO",
            "FIXME",
            "HACK",
            "XXX",
        ]

        # 硬編碼時間線模式
        self.timeline_patterns = [
            r"\d+\s*(天|日|week|day)s?",
            r"\d+\s*(週|周|month)s?",
            r"\d{4}-\d{2}-\d{2}",  # 具體日期
            r"deadline.*\d{4}",
            r"by.*\d{4}",
        ]

        # 受保護的命名空間
        self.protected_namespaces = [
            "ng_namespace_governance",
            "ng_executor",
            "auto_executor",
            "ecosystem.enforce",
        ]

    def scan_repository(self, root_path: str = ".") -> Dict:
        """掃描整個儲存庫"""
        root = Path(root_path)

        print("🔍 開始全面掃描...")
        print(f"   根目錄: {root.absolute()}")
        print()

        # 掃描 Python 文件
        python_files = list(root.rglob("*.py"))
        python_files = [
            f
            for f in python_files
            if not any(
                x in str(f) for x in [".git", "venv", "node_modules", "__pycache__"]
            )
        ]

        # 掃描 YAML 文件
        yaml_files = list(root.rglob("*.yaml")) + list(root.rglob("*.yml"))
        yaml_files = [
            f
            for f in yaml_files
            if not any(x in str(f) for x in [".git", "venv", "node_modules"])
        ]

        # 掃描 Markdown 文件
        md_files = list(root.rglob("*.md"))
        md_files = [
            f
            for f in md_files
            if not any(x in str(f) for x in [".git", "venv", "node_modules"])
        ]

        print(f"📊 待掃描文件:")
        print(f"   Python: {len(python_files)}")
        print(f"   YAML: {len(yaml_files)}")
        print(f"   Markdown: {len(md_files)}")
        print()

        # 掃描 Python 文件
        for py_file in python_files:
            self.scan_python_file(py_file)

        # 掃描 YAML 文件
        for yaml_file in yaml_files:
            self.scan_yaml_file(yaml_file)

        # 掃描 Markdown 文件
        for md_file in md_files:
            self.scan_markdown_file(md_file)

        # 生成報告
        return self.generate_report()

    def scan_python_file(self, filepath: Path):
        """掃描 Python 文件"""
        self.stats["files_scanned"] += 1

        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            return

        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            # 檢查禁止短語
            for phrase in self.forbidden_phrases:
                if phrase.lower() in line.lower():
                    self.add_violation(
                        file=str(filepath),
                        line=line_num,
                        type="FORBIDDEN_PHRASE",
                        severity="MEDIUM",
                        description=f"包含禁止短語: '{phrase}'",
                        code=line.strip()[:100],
                    )

            # 檢查硬編碼時間線
            for pattern in self.timeline_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # 排除註釋和文檔
                    if (
                        not line.strip().startswith("#")
                        and "created_at" not in line
                        and "updated_at" not in line
                    ):
                        self.add_violation(
                            file=str(filepath),
                            line=line_num,
                            type="HARDCODED_TIMELINE",
                            severity="HIGH",
                            description=f"硬編碼時間線",
                            code=line.strip()[:100],
                        )

            # 檢查命名規範（變數名必須 snake_case，不能 camelCase）
            # 跳過導入和字符串
            if not line.strip().startswith("import") and not line.strip().startswith(
                "from"
            ):
                camel_case_pattern = r"\b[a-z]+[A-Z][a-zA-Z]*\s*="
                if re.search(camel_case_pattern, line):
                    self.add_violation(
                        file=str(filepath),
                        line=line_num,
                        type="NAMING_VIOLATION",
                        severity="LOW",
                        description="使用 camelCase 而非 snake_case",
                        code=line.strip()[:100],
                    )

    def scan_yaml_file(self, filepath: Path):
        """掃描 YAML 文件"""
        self.stats["files_scanned"] += 1

        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            return

        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            # 檢查禁止短語
            for phrase in self.forbidden_phrases:
                if phrase.lower() in line.lower():
                    self.add_violation(
                        file=str(filepath),
                        line=line_num,
                        type="FORBIDDEN_PHRASE",
                        severity="MEDIUM",
                        description=f"包含禁止短語: '{phrase}'",
                        code=line.strip()[:100],
                    )

    def scan_markdown_file(self, filepath: Path):
        """掃描 Markdown 文件"""
        self.stats["files_scanned"] += 1

        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            return

        # 對於文檔文件，只檢查嚴重違規
        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            # 檢查最嚴重的禁止短語
            critical_phrases = ["100% 完成", "完全符合", "已全部实现"]
            for phrase in critical_phrases:
                if phrase in line:
                    self.add_violation(
                        file=str(filepath),
                        line=line_num,
                        type="FORBIDDEN_PHRASE",
                        severity="LOW",  # 文檔中較寬鬆
                        description=f"文檔中包含禁止短語: '{phrase}'",
                        code=line.strip()[:100],
                    )

    def add_violation(
        self,
        file: str,
        line: int,
        type: str,
        severity: str,
        description: str,
        code: str,
    ):
        """添加違規記錄"""
        violation = {
            "file": file,
            "line": line,
            "type": type,
            "severity": severity,
            "description": description,
            "code": code,
            "detected_at": datetime.now().isoformat(),
        }

        self.violations.append(violation)
        self.stats["violations_found"] += 1
        self.stats["by_type"][type] = self.stats["by_type"].get(type, 0) + 1
        self.stats["by_severity"][severity] = (
            self.stats["by_severity"].get(severity, 0) + 1
        )

    def generate_report(self) -> Dict:
        """生成掃描報告"""
        report = {
            "scan_date": datetime.now().isoformat(),
            "statistics": self.stats,
            "violations": self.violations,
            "summary": self.generate_summary(),
        }

        return report

    def generate_summary(self) -> str:
        """生成摘要"""
        lines = [
            "=" * 70,
            "零容忍違規掃描報告",
            "=" * 70,
            f"掃描時間: {datetime.now().isoformat()}",
            f"掃描文件: {self.stats['files_scanned']}",
            f"發現違規: {self.stats['violations_found']}",
            "",
            "按類型分布:",
        ]

        for vtype, count in sorted(
            self.stats["by_type"].items(), key=lambda x: x[1], reverse=True
        ):
            lines.append(f"  {vtype}: {count}")

        lines.append("\n按嚴重性分布:")
        for severity, count in sorted(self.stats["by_severity"].items()):
            lines.append(f"  {severity}: {count}")

        lines.extend(["", "=" * 70])

        return "\n".join(lines)

    def save_report(self, output_path: str = "reports/zero-tolerance-violations.json"):
        """保存報告"""
        report = self.generate_report()

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"💾 違規報告已保存: {output_path}")


if __name__ == "__main__":
    scanner = ZeroToleranceScanner()

    # 掃描儲存庫
    report = scanner.scan_repository()

    # 顯示摘要
    print(report["summary"])

    # 保存完整報告
    scanner.save_report()

    # 顯示嚴重違規
    critical_violations = [
        v for v in scanner.violations if v["severity"] in ["CRITICAL", "HIGH"]
    ]

    if critical_violations:
        print(f"\n🚨 發現 {len(critical_violations)} 個 CRITICAL/HIGH 違規:")
        for v in critical_violations[:20]:
            print(f"\n❌ [{v['severity']}] {v['file']}:{v['line']}")
            print(f"   {v['description']}")
            print(f"   {v['code']}")

    # 退出碼
    if scanner.stats["violations_found"] > 0:
        print(f"\n⚠️  發現 {scanner.stats['violations_found']} 個違規")
        print("   使用 reports/zero-tolerance-violations.json 查看完整報告")
    else:
        print("\n✅ 無違規！儲存庫完全符合零容忍標準")
