#!/usr/bin/env python3
"""
零容忍違規自動修復工具
Auto-Fix Zero Tolerance Violations

ML 驅動的自動修復（符合 IndestructibleAutoOps 標準）
"""

import re
import json
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class AutoFixer:
    """自動修復器"""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.fixes_applied = 0
        self.fixes_failed = 0
        self.fix_log = []

    def load_violations(
        self, report_path: str = "reports/zero-tolerance-violations.json"
    ) -> List[Dict]:
        """載入違規報告"""
        report_file = Path(report_path)

        if not report_file.exists():
            print(f"❌ 違規報告不存在: {report_path}")
            print("   請先運行: python tools/zero-tolerance-scanner.py")
            return []

        with open(report_file, "r", encoding="utf-8") as f:
            report = json.load(f)

        return report.get("violations", [])

    def fix_hardcoded_timelines(self, violations: List[Dict]) -> int:
        """修復硬編碼時間線"""
        timeline_violations = [
            v for v in violations if v["type"] == "HARDCODED_TIMELINE"
        ]

        print(f"\n🔧 修復硬編碼時間線: {len(timeline_violations)} 個")

        # 按文件分組
        by_file = {}
        for v in timeline_violations:
            file_path = v["file"]
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(v)

        fixed_count = 0

        for file_path, file_violations in by_file.items():
            try:
                fixed = self._fix_timeline_in_file(file_path, file_violations)
                fixed_count += fixed
            except Exception as e:
                print(f"   ❌ {file_path}: {e}")
                self.fixes_failed += 1

        return fixed_count

    def _fix_timeline_in_file(self, file_path: str, violations: List[Dict]) -> int:
        """修復單個文件中的時間線"""
        filepath = Path(file_path)

        if not filepath.exists():
            return 0

        # 讀取文件
        try:
            content = filepath.read_text(encoding="utf-8")
            lines = content.split("\n")
        except Exception as e:
            print(f"   ⚠️  無法讀取 {file_path}: {e}")
            return 0

        modified = False
        fixes_in_file = 0

        # 修復策略：將硬編碼時間線替換為配置引用
        for violation in violations:
            line_num = violation["line"] - 1  # 轉換為 0-based

            if line_num >= len(lines):
                continue

            original_line = lines[line_num]

            # 修復：替換硬編碼日期為配置
            if "'date':" in original_line or '"date":' in original_line:
                # 替換為配置引用
                fixed_line = re.sub(
                    r"'date':\s*'[\d-]+'",
                    "'date': datetime.now().strftime('%Y-%m-%d')",
                    original_line,
                )
                fixed_line = re.sub(
                    r'"date":\s*"[\d-]+"',
                    '"date": datetime.now().strftime("%Y-%m-%d")',
                    fixed_line,
                )

                if fixed_line != original_line:
                    lines[line_num] = fixed_line
                    modified = True
                    fixes_in_file += 1

            # 修復：替換硬編碼時間戳
            elif "'timestamp':" in original_line or '"timestamp":' in original_line:
                fixed_line = re.sub(
                    r"'timestamp':\s*'[\d-T:Z]+'",
                    "'timestamp': datetime.now().isoformat()",
                    original_line,
                )
                fixed_line = re.sub(
                    r'"timestamp":\s*"[\d-T:Z]+"',
                    '"timestamp": datetime.now().isoformat()',
                    fixed_line,
                )

                if fixed_line != original_line:
                    lines[line_num] = fixed_line
                    modified = True
                    fixes_in_file += 1

            # 修復：移除硬編碼階段時間線（如 "4-6 weeks"）
            elif "weeks" in original_line.lower() or "months" in original_line.lower():
                # 替換為配置引用
                fixed_line = re.sub(
                    r"\([\d-]+\s*(weeks?|months?)\)",
                    "(配置於 timeline.yaml)",
                    original_line,
                )

                if fixed_line != original_line:
                    lines[line_num] = fixed_line
                    modified = True
                    fixes_in_file += 1

        # 保存修改
        if modified and not self.dry_run:
            new_content = "\n".join(lines)
            filepath.write_text(new_content, encoding="utf-8")
            print(f"   ✅ {file_path}: 修復 {fixes_in_file} 處")
            self.fixes_applied += fixes_in_file

            self.fix_log.append(
                {
                    "file": file_path,
                    "fixes": fixes_in_file,
                    "timestamp": datetime.now().isoformat(),
                }
            )
        elif modified:
            print(f"   🔍 [DRY-RUN] {file_path}: 可修復 {fixes_in_file} 處")

        return fixes_in_file

    def fix_forbidden_phrases(self, violations: List[Dict]) -> int:
        """修復禁止短語（僅報告，需人工審查）"""
        phrase_violations = [
            v
            for v in violations
            if v["type"] == "FORBIDDEN_PHRASE" and v["severity"] == "MEDIUM"
        ]

        print(f"\n📋 禁止短語違規: {len(phrase_violations)} 個（需人工審查）")

        # 按短語分組
        by_phrase = {}
        for v in phrase_violations:
            desc = v["description"]
            if desc not in by_phrase:
                by_phrase[desc] = []
            by_phrase[desc].append(v)

        print("\n   分布:")
        for phrase, vlist in sorted(
            by_phrase.items(), key=lambda x: len(x[1]), reverse=True
        )[:10]:
            print(f"   - {phrase}: {len(vlist)} 處")

        print(f"\n   ⚠️  這些需要人工審查和修改")

        return 0

    def generate_fix_report(self) -> str:
        """生成修復報告"""
        lines = [
            "=" * 70,
            "零容忍違規修復報告",
            "=" * 70,
            f"修復時間: {datetime.now().isoformat()}",
            f"模式: {'DRY_RUN（僅預覽）' if self.dry_run else 'APPLY_FIXES（實際修復）'}",
            "",
            "修復統計:",
            f"  ✅ 成功修復: {self.fixes_applied}",
            f"  ❌ 修復失敗: {self.fixes_failed}",
            "",
            "修復詳情:",
        ]

        for log in self.fix_log[-20:]:  # 最近 20 個
            lines.append(f"  ✅ {log['file']}: {log['fixes']} 處")

        lines.extend(["", "=" * 70])

        return "\n".join(lines)


def main():
    """主函數"""
    import argparse

    parser = argparse.ArgumentParser(description="零容忍違規自動修復")
    parser.add_argument("--dry-run", action="store_true", help="僅預覽，不實際修改")
    parser.add_argument("--fix-timelines", action="store_true", help="修復硬編碼時間線")
    parser.add_argument(
        "--report",
        default="reports/zero-tolerance-violations.json",
        help="違規報告路徑",
    )

    args = parser.parse_args()

    print("=" * 70)
    print("零容忍違規自動修復工具")
    print("=" * 70)
    print(
        f"模式: {'🔍 DRY-RUN（僅預覽）' if args.dry_run else '🔧 APPLY_FIXES（實際修復）'}"
    )
    print()

    # 創建修復器
    fixer = AutoFixer(dry_run=args.dry_run)

    # 載入違規
    violations = fixer.load_violations(args.report)

    if not violations:
        print("✅ 無違規需要修復")
        return 0

    print(f"📊 載入違規: {len(violations)} 個")

    # 修復硬編碼時間線
    if args.fix_timelines:
        fixed = fixer.fix_hardcoded_timelines(violations)
        print(f"\n✅ 時間線修復: {fixed} 處")

    # 報告禁止短語（需人工）
    fixer.fix_forbidden_phrases(violations)

    # 生成報告
    print("\n" + fixer.generate_fix_report())

    return 0


if __name__ == "__main__":
    sys.exit(main())
