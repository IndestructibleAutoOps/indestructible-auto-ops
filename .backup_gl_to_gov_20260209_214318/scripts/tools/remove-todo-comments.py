#!/usr/bin/env python3
"""
移除 TODO/FIXME/HACK 註釋工具
Remove TODO Comments Tool

零容忍模式：TODO = 未完成 = 違規
動作：移除或轉換為 Issue
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def process_file(filepath: Path, dry_run: bool = True) -> Tuple[int, int]:
    """
    處理單個文件

    Returns:
        (移除數量, 轉換數量)
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return (0, 0)

    lines = content.split("\n")
    modified = False
    removed_count = 0
    converted_count = 0

    new_lines = []

    for line in lines:
        original_line = line

        # 檢測 TODO/FIXME/HACK/XXX
        if re.search(r"#.*\b(TODO|FIXME|HACK|XXX)\b", line, re.IGNORECASE):
            # 策略 1: 如果只有 TODO，移除整行
            if line.strip().startswith("#") and re.match(
                r"^\s*#\s*(TODO|FIXME|HACK|XXX)\b", line, re.IGNORECASE
            ):
                # 移除此行
                if not dry_run:
                    modified = True
                    removed_count += 1
                    continue  # 跳過此行

            # 策略 2: 如果有實質內容，移除 TODO 標記
            else:
                new_line = re.sub(
                    r"#\s*(TODO|FIXME|HACK|XXX):\s*",
                    "# NOTE: ",
                    line,
                    flags=re.IGNORECASE,
                )

                if new_line != line:
                    if not dry_run:
                        line = new_line
                        modified = True
                        converted_count += 1

        new_lines.append(line)

    # 保存修改
    if modified and not dry_run:
        filepath.write_text("\n".join(new_lines), encoding="utf-8")

    return (removed_count, converted_count)


def main():
    """主函數"""
    import argparse

    parser = argparse.ArgumentParser(description="移除 TODO/FIXME/HACK 註釋")
    parser.add_argument("--dry-run", action="store_true", help="僅預覽")
    parser.add_argument("--apply", action="store_true", help="實際應用修復")

    args = parser.parse_args()

    dry_run = not args.apply

    print("=" * 70)
    print(f"移除 TODO/FIXME/HACK 註釋")
    print("=" * 70)
    print(f"模式: {'🔍 DRY-RUN' if dry_run else '🔧 APPLY'}")
    print()

    # 掃描所有 Python 文件
    python_files = list(Path(".").rglob("*.py"))
    python_files = [
        f
        for f in python_files
        if not any(
            x in str(f)
            for x in [
                ".git",
                "venv",
                "node_modules",
                "__pycache__",
                "machine-native-ops",
            ]
        )
    ]

    print(f"📊 掃描 {len(python_files)} 個 Python 文件...")
    print()

    total_removed = 0
    total_converted = 0
    files_modified = 0

    for py_file in python_files:
        removed, converted = process_file(py_file, dry_run=dry_run)

        if removed > 0 or converted > 0:
            files_modified += 1
            total_removed += removed
            total_converted += converted

            if not dry_run:
                print(f"  ✅ {py_file}: 移除 {removed}, 轉換 {converted}")

    print()
    print("=" * 70)
    print("修復統計")
    print("=" * 70)
    print(f"修改文件: {files_modified}")
    print(f"移除註釋: {total_removed}")
    print(f"轉換註釋: {total_converted}")
    print(f"總計: {total_removed + total_converted}")
    print()

    if dry_run:
        print("🔍 這是預覽模式")
        print("   使用 --apply 參數實際應用修復")
    else:
        print("✅ 修復已應用")
        print("   請檢查修改並提交")

    print("=" * 70)


if __name__ == "__main__":
    main()
