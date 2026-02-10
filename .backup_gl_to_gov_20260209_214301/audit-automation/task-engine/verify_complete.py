#!/usr/bin/env python3
"""
完整性驗證腳本
驗證 auto_task_project 的所有組件和功能
"""

import sys

sys.path.insert(0, ".")

from pathlib import Path
import json


def verify_structure():
    """驗證目錄結構"""
    print("=" * 70)
    print("🔍 驗證目錄結構")
    print("=" * 70)

    required_files = [
        "main.py",
        "auto_executor.py",
        "scheduler.py",
        "event_bus.py",
        "logger.py",
        "config.py",
        "pyproject.toml",
        ".gitignore",
        ".env.example",
    ]

    required_dirs = ["tasks", "utils", "models", "api", "logs"]

    all_good = True

    print("\n核心文件:")
    for file in required_files:
        exists = Path(file).exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")
        if not exists:
            all_good = False

    print("\n目錄結構:")
    for dir_name in required_dirs:
        exists = Path(dir_name).exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {dir_name}/")
        if not exists:
            all_good = False

    return all_good


def verify_tasks():
    """驗證任務載入"""
    print("\n" + "=" * 70)
    print("🔍 驗證任務系統")
    print("=" * 70)

    try:
        from auto_executor import executor

        # 自動發現
        executor.auto_discover("tasks")

        task_count = len(executor.get_all_tasks())
        print(f"\n✅ 成功載入 {task_count} 個任務")

        if task_count >= 14:
            print(f"✅ 任務數量正常（預期 ≥14，實際 {task_count}）")
            return True
        else:
            print(f"⚠️  任務數量不足（預期 ≥14，實際 {task_count}）")
            return False

    except Exception as e:
        print(f"❌ 任務載入失敗: {e}")
        return False


def verify_registries():
    """驗證註冊表數據"""
    print("\n" + "=" * 70)
    print("🔍 驗證註冊表數據")
    print("=" * 70)

    registries_dir = Path("tasks/registries")

    if not registries_dir.exists():
        print("❌ 註冊表目錄不存在")
        return False

    registry_files = list(registries_dir.glob("*.json")) + list(
        registries_dir.glob("*.yaml")
    )
    print(f"\n📂 找到 {len(registry_files)} 個註冊表文件")

    total_size = sum(f.stat().st_size for f in registry_files if f.is_file())
    print(f"📊 總大小: {total_size / 1024:.1f} KB")

    # 檢查子目錄
    subdirs = [d.name for d in registries_dir.iterdir() if d.is_dir()]
    print(f"📁 子目錄 ({len(subdirs)}):")
    for subdir in subdirs:
        print(f"  - {subdir}/")

    return len(registry_files) >= 3


def verify_documentation():
    """驗證文檔完整性"""
    print("\n" + "=" * 70)
    print("🔍 驗證文檔系統")
    print("=" * 70)

    docs = [
        "README.md",
        "TASKS-OVERVIEW.md",
        "REGISTRY-MIGRATION-REPORT.md",
        "DEPLOYMENT-GUIDE.md",
        "FINAL-SUMMARY.md",
    ]

    all_good = True

    for doc in docs:
        exists = Path(doc).exists()
        status = "✅" if exists else "❌"
        if exists:
            size = Path(doc).stat().st_size
            print(f"  {status} {doc} ({size / 1024:.1f} KB)")
        else:
            print(f"  {status} {doc}")
            all_good = False

    return all_good


def verify_event_system():
    """驗證事件系統"""
    print("\n" + "=" * 70)
    print("🔍 驗證事件系統")
    print("=" * 70)

    try:
        from event_bus import event_bus

        # 測試事件註冊
        test_called = []

        def test_handler():
            test_called.append(True)

        event_bus.on("test_event", test_handler)
        event_bus.emit("test_event")

        if test_called:
            print("✅ 事件系統正常工作")
            return True
        else:
            print("❌ 事件系統異常")
            return False

    except Exception as e:
        print(f"❌ 事件系統錯誤: {e}")
        return False


def generate_verification_report(results):
    """生成驗證報告"""
    print("\n" + "=" * 70)
    print("📋 驗證結果總結")
    print("=" * 70)

    all_passed = all(results.values())

    for check, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")

    print("\n" + "=" * 70)

    if all_passed:
        print("🎉 所有驗證通過！專案完整無誤！")
        print("=" * 70)
        print("\n✨ 可以開始使用：")
        print("   cd auto_task_project")
        print("   pip install -e .")
        print("   python main.py")
        print("\n🚀 系統就緒，生產可用！")
        return 0
    else:
        print("⚠️  部分驗證失敗，請檢查上述錯誤")
        print("=" * 70)
        return 1


def main():
    """執行完整性驗證"""
    print("\n" + "=" * 70)
    print("🎯 AUTO TASK PROJECT - 完整性驗證")
    print("=" * 70)

    results = {
        "目錄結構": verify_structure(),
        "任務系統": verify_tasks(),
        "註冊表數據": verify_registries(),
        "文檔系統": verify_documentation(),
        "事件系統": verify_event_system(),
    }

    return generate_verification_report(results)


if __name__ == "__main__":
    sys.exit(main())
