#!/usr/bin/env python3
"""
企业级严格工程验证系统 - 执行入口
Enterprise Strict Engineering Validation System - Entry Point

Usage:
    python run_strict_validation.py [--project-root PATH] [--strict] [--no-whitelist]

Exit codes:
    0 - 验证通过
    1 - 验证失败（存在阻塞性问题）
"""

import argparse
import os
import sys

# 确保可以导入 validation 模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from validation.strict_validator import ValidationEngine
from validation.validator import ValidationConfig


def parse_args():
    parser = argparse.ArgumentParser(
        description="企业级严格工程验证系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用默认配置运行
  python run_strict_validation.py

  # 指定项目根目录
  python run_strict_validation.py --project-root /path/to/project

  # 严格模式 + 自定义阈值
  python run_strict_validation.py --strict --perf-threshold 0.15 --metric-threshold 0.08

  # 禁用白名单
  python run_strict_validation.py --no-whitelist
        """,
    )
    parser.add_argument(
        "--project-root",
        default=os.getcwd(),
        help="项目根目录 (默认: 当前目录)",
    )
    parser.add_argument(
        "--baseline-dir",
        default=".baselines",
        help="基线数据目录 (默认: .baselines)",
    )
    parser.add_argument(
        "--output-dir",
        default=".validation",
        help="报告输出目录 (默认: .validation)",
    )

    # 计算相对于脚本的默认白名单路径
    whitelist_default = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "configs",
            "validation_whitelist.yaml",
        )
    )
    parser.add_argument(
        "--whitelist",
        default=whitelist_default,
        help="白名单配置文件路径",
    )
    parser.add_argument(
        "--no-whitelist",
        action="store_true",
        help="禁用白名单",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="启用严格模式 (默认: 禁用)",
    )
    parser.add_argument(
        "--no-strict",
        dest="strict",
        action="store_false",
        help="禁用严格模式",
    )
    parser.add_argument(
        "--perf-threshold",
        type=float,
        default=0.2,
        help="性能偏差阈值 (默认: 0.2 即 20%%)",
    )
    parser.add_argument(
        "--metric-threshold",
        type=float,
        default=0.1,
        help="通用指标偏差阈值 (默认: 0.1 即 10%%)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 60)
    print("  企业级严格工程验证系统 v1.0.0")
    print("  Enterprise Strict Validation System")
    print("=" * 60)
    print(f"\n📁 项目根目录: {args.project_root}")
    print(f"📊 严格模式: {'启用' if args.strict else '禁用'}")
    print(f"📏 性能阈值: {args.perf_threshold * 100:.0f}%")
    print(f"📏 指标阈值: {args.metric_threshold * 100:.0f}%")

    # 构建配置
    whitelist_path = None
    if not args.no_whitelist:
        wl_path = os.path.join(args.project_root, args.whitelist)
        if os.path.exists(wl_path):
            whitelist_path = wl_path
            print(f"📋 白名单: {wl_path}")
        else:
            print(f"⚠️  白名单文件不存在: {wl_path}")

    config = ValidationConfig(
        project_root=args.project_root,
        baseline_dir=os.path.join(args.project_root, args.baseline_dir),
        output_dir=os.path.join(args.project_root, args.output_dir),
        whitelist_path=whitelist_path,
        strict_mode=args.strict,
        performance_threshold=args.perf_threshold,
        metric_threshold=args.metric_threshold,
    )

    print(f"\n{'─' * 60}")
    print("🚀 开始验证...\n")

    # 创建引擎并执行
    engine = ValidationEngine(config)
    result = engine.run()

    # 打印报告
    print(f"\n{'─' * 60}")
    result.print_report()
    print(f"{'─' * 60}")

    # 退出码
    if result.overall_passed:
        print("\n🟢 验证通过 - 可安全部署")
        sys.exit(0)
    else:
        print("\n🔴 验证失败 - 部署被阻止")
        sys.exit(1)


if __name__ == "__main__":
    main()
