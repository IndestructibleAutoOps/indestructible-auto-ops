#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: general
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""GL治理執行層 - 完整系統測試"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from self_auditor import SelfAuditor
from pipeline_integration import PipelineIntegration


def test_enforcement():
    print("=== GL治理執行層 - 完整系統測試 ===\n")

    auditor = SelfAuditor()
    repo_root = Path(__file__).resolve().parents[2]
    pipeline = PipelineIntegration(workspace_path=str(repo_root))

    # 測試1: 禁止短語檢測
    print("1. 測試禁止短語檢測")
    report = "這個項目已經100%完成了，完全符合標準，必須成功。"
    violations = auditor.check_forbidden_phrases(report)
    print(
        f"   檢測到 {len(violations)} 個違規: {'✅' if len(violations) > 0 else '❌'}"
    )
    print()

    # 測試2: 證據覆蓋率
    print("2. 測試證據覆蓋率")
    coverage = auditor.calculate_evidence_coverage("這是一個報告。沒有證據。")
    print(f"   覆蓋率: {coverage:.1%} (閾值: 90%): {'✅' if coverage < 0.90 else '❌'}")
    print()

    # 測試3: 證據收集
    print("3. 測試證據收集")
    sources = [
        {"type": "contract", "path": "ecosystem/contracts/platforms/gl-platforms.yaml"}
    ]
    evidence = pipeline.collect_evidence(sources, "test-001")
    print(f"   收集到 {len(evidence)} 個證據: {'✅' if len(evidence) > 0 else '❌'}")
    print()

    print("=== 測試完成 ===")
    return 0


if __name__ == "__main__":
    sys.exit(test_enforcement())
