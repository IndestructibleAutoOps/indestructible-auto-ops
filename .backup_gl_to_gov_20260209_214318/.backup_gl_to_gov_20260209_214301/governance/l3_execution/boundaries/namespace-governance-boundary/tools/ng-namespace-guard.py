#!/usr/bin/env python3
"""
NG 命名空間守護
NG Namespace Guardian

用途：檢測對受保護命名空間的非法覆寫
模式：ZERO TOLERANCE
動作：IMMEDIATE_BLOCK on any violation
"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# 受保護的命名空間（不可覆寫）
PROTECTED_NAMESPACES = [
    "ng_namespace_governance",
    "ng_executor",
    "ng_orchestrator",
    "ng_ml_self_healer",
    "ng_enforcer_strict",
    "ng_closure_engine",
    "auto_executor",
    "ecosystem.enforce",
    "ecosystem.reasoning",
]

# 受保護的模組（不可猴子補丁）
PROTECTED_MODULES = [
    "NgExecutor",
    "NgOrchestrator",
    "NgMlSelfHealer",
    "NgStrictEnforcer",
    "NgClosureEngine",
    "TaskExecutor",
    "GovernanceEnforcer",
]


def check_file(filepath: str) -> List[Dict]:
    """
    檢查文件是否有命名空間違規

    Returns:
        違規列表
    """
    try:
        code = Path(filepath).read_text(encoding="utf-8")
        tree = ast.parse(code, filename=filepath)
    except Exception as e:
        print(f"⚠️  無法解析 {filepath}: {e}")
        return []

    violations = []

    for node in ast.walk(tree):
        # 檢測 1: 屬性賦值（覆寫檢測）
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Attribute):
                    attr_str = ast.unparse(target)

                    # 檢查是否覆寫受保護命名空間
                    for protected in PROTECTED_NAMESPACES:
                        if protected in attr_str:
                            violations.append(
                                {
                                    "file": filepath,
                                    "line": node.lineno,
                                    "type": "NAMESPACE_OVERRIDE",
                                    "code": ast.unparse(node)[:100],
                                    "protected": protected,
                                    "severity": "IMMUTABLE",
                                }
                            )

        # 檢測 2: 類別定義（猴子補丁檢測）
        if isinstance(node, ast.ClassDef):
            for protected_class in PROTECTED_MODULES:
                if protected_class in node.name:
                    # 檢查是否重新定義受保護類別
                    violations.append(
                        {
                            "file": filepath,
                            "line": node.lineno,
                            "type": "CLASS_REDEFINITION",
                            "code": f"class {node.name}",
                            "protected": protected_class,
                            "severity": "IMMUTABLE",
                        }
                    )

        # 檢測 3: 函數覆寫
        if isinstance(node, ast.FunctionDef):
            # 檢查裝飾器（如 @override）
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name) and decorator.id == "override":
                    # 檢查是否覆寫受保護方法
                    violations.append(
                        {
                            "file": filepath,
                            "line": node.lineno,
                            "type": "METHOD_OVERRIDE",
                            "code": f"@override def {node.name}",
                            "protected": node.name,
                            "severity": "ABSOLUTE",
                        }
                    )

    return violations


def main():
    """主函數"""
    files = sys.argv[1:] if len(sys.argv) > 1 else []

    if not files:
        print("用法: python ng-namespace-guard.py <files...>")
        print("     或在 git hook 中自動調用")
        sys.exit(0)

    all_violations = []

    for filepath in files:
        if filepath.endswith(".py"):
            violations = check_file(filepath)
            all_violations.extend(violations)

    if all_violations:
        print("=" * 70)
        print("🚨 ZERO_TOLERANCE_VIOLATION: Namespace override detected")
        print("=" * 70)
        print()

        for v in all_violations:
            print(f"❌ [{v['severity']}] {v['file']}:{v['line']}")
            print(f"   Type: {v['type']}")
            print(f"   Protected: {v['protected']}")
            print(f"   Code: {v['code']}")
            print()

        print("=" * 70)
        print("🚫 PERMANENT_BLOCK: Remove all namespace overrides")
        print("=" * 70)
        print()
        print("正確做法：")
        print("1. 透過繼承擴展（class MyClass(ProtectedClass)）")
        print("2. 使用組合模式（self.protected = ProtectedClass()）")
        print("3. 提交 PR 修改核心（經過完整審核）")
        print()

        sys.exit(1)

    print("✅ No namespace violations detected")
    print(f"   Checked {len([f for f in files if f.endswith('.py')])} Python files")
    sys.exit(0)


if __name__ == "__main__":
    main()
