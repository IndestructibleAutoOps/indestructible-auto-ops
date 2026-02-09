#!/usr/bin/env python3
"""
Strict Version Management Tests
================================
測試嚴格版本管理系統
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from strict_version_enforcer import StrictVersionEnforcer, VersionValidation
from impact_analyzer import ImpactAnalyzer, ImpactChain, MigrationPlan


def test_version_format_validation():
    """測試版本格式驗證"""
    print("\n=== Test Version Format Validation ===")

    enforcer = StrictVersionEnforcer()

    # 有效版本
    valid_versions = [
        "1.0.0",
        "1.2.3",
        "0.1.0",
        "1.0.0-alpha.1",
        "1.0.0-beta.2",
        "1.0.0-rc.1",
        "1.0.0+20240202",
    ]

    for ver in valid_versions:
        result = enforcer.validate_version_format(ver)
        assert result.valid, f"應該有效但失敗: {ver}, 錯誤: {result.errors}"

    print(f"✓ 有效版本格式: {len(valid_versions)} 個通過")

    # 無效版本
    invalid_versions = [
        "1",
        "1.0",
        "01.0.0",  # 前導零
        "1.0.0-invalid",  # 無效預發布
        "v1.0.0",  # 前綴
        "1.0.0.0",  # 四段
    ]

    for ver in invalid_versions:
        result = enforcer.validate_version_format(ver)
        assert not result.valid, f"應該無效但通過: {ver}"

    print(f"✓ 無效版本格式: {len(invalid_versions)} 個正確拒絕")

    print("✅ Version Format Validation tests passed")


def test_version_sequence_validation():
    """測試版本序列驗證"""
    print("\n=== Test Version Sequence Validation ===")

    enforcer = StrictVersionEnforcer()

    # 註冊基礎版本
    enforcer.register_version("test-spec", "1.0.0", "hash1", "sig1")
    enforcer.register_version("test-spec", "1.0.1", "hash2", "sig2")
    enforcer.register_version("test-spec", "1.1.0", "hash3", "sig3")

    print("✓ 基礎版本已註冊: 1.0.0, 1.0.1, 1.1.0")

    # 測試連續版本（應該通過）
    result = enforcer.validate_version_sequence("test-spec", "1.1.1")
    assert result.valid, f"連續版本應該通過: {result.errors}"
    print("✓ 連續版本驗證通過")

    # 測試跳躍版本（應該失敗）
    result = enforcer.validate_version_sequence("test-spec", "1.1.3")
    assert not result.valid, "跳躍版本應該失敗"
    assert "跳躍" in result.errors[0], "應該報告跳躍錯誤"
    print("✓ 跳躍版本正確拒絕")

    # 測試主版本升級（應該要求 X.0.0）
    result = enforcer.validate_version_sequence("test-spec", "2.0.1")
    assert not result.valid, "主版本升級應該重置為 X.0.0"
    print("✓ 主版本重置規則生效")

    print("✅ Version Sequence Validation tests passed")


def test_production_deployment_validation():
    """測試生產部署驗證"""
    print("\n=== Test Production Deployment Validation ===")

    enforcer = StrictVersionEnforcer()

    # 生產環境測試
    assert enforcer.validate_production_deployment(
        "1.0.0", "production"
    ), "穩定版本應該允許"
    print("✓ 穩定版本允許部署到生產")

    assert not enforcer.validate_production_deployment(
        "1.0.0-beta.1", "production"
    ), "預發布版本應該禁止"
    print("✓ 預發布版本禁止部署到生產")

    assert not enforcer.validate_production_deployment(
        "dev-feat-abc123", "production"
    ), "開發版本應該禁止"
    print("✓ 開發版本禁止部署到生產")

    # 開發環境測試
    assert enforcer.validate_production_deployment(
        "1.0.0-alpha.1", "development"
    ), "開發環境應該允許預發布版本"
    print("✓ 開發環境允許預發布版本")

    print("✅ Production Deployment Validation tests passed")


def test_compatibility_checking():
    """測試兼容性檢查"""
    print("\n=== Test Compatibility Checking ===")

    enforcer = StrictVersionEnforcer()

    # PATCH 升級（完全兼容）
    compat = enforcer.check_compatibility("test-spec", "1.0.0", "1.0.1")
    assert compat["compatible"], "PATCH升級應該兼容"
    assert compat["change_type"] == "PATCH", "應該識別為PATCH"
    print(
        f"✓ PATCH升級: compatible={compat['compatible']}, timeline={compat['timeline_days']}天"
    )

    # MINOR 升級（向後兼容）
    compat = enforcer.check_compatibility("test-spec", "1.0.0", "1.1.0")
    assert compat["compatible"], "MINOR升級應該兼容"
    assert compat["change_type"] == "MINOR", "應該識別為MINOR"
    assert compat["timeline_days"] == 30, "應該有30天測試期"
    print(f"✓ MINOR升級: compatible={compat['compatible']}, testing=30天")

    # MAJOR 升級（不兼容）
    compat = enforcer.check_compatibility("test-spec", "1.0.0", "2.0.0")
    assert not compat["compatible"], "MAJOR升級應該不兼容"
    assert compat["change_type"] == "MAJOR", "應該識別為MAJOR"
    assert compat["timeline_days"] == 90, "應該有90天遷移期"
    assert "MIGRATION" in compat["action_required"], "應該要求遷移"
    print(f"✓ MAJOR升級: breaking=True, migration=90天")

    print("✅ Compatibility Checking tests passed")


def test_impact_analyzer():
    """測試影響分析器"""
    print("\n=== Test Impact Analyzer ===")

    analyzer = ImpactAnalyzer()

    # 註冊驗證器
    analyzer.register_validator(
        "validator-1", [{"spec_id": "spec-a", "version": "1.0.0"}]
    )

    analyzer.register_validator(
        "validator-2",
        [
            {"spec_id": "spec-a", "version": "1.0.0"},
            {"spec_id": "spec-b", "version": "2.0.0"},
        ],
    )

    print("✓ 驗證器已註冊")

    # 分析影響
    impact = analyzer.analyze_version_change_impact("spec-a", "1.0.0", "2.0.0")

    assert impact.change_type == "MAJOR", "應該識別為MAJOR變更"
    assert (
        len(impact.affected_validators) == 2
    ), f"應該影響2個驗證器，實際{len(impact.affected_validators)}"
    assert impact.risk_score > 50, f"MAJOR變更風險應該>50，實際{impact.risk_score}"

    print(f"✓ 影響分析完成:")
    print(f"  - 變更類型: {impact.change_type}")
    print(f"  - 影響驗證器: {len(impact.affected_validators)}")
    print(f"  - 遷移成本: {impact.migration_cost:.1f}/100")
    print(f"  - 風險分數: {impact.risk_score:.1f}/100")

    # 生成遷移計劃
    plan = analyzer.generate_migration_plan("spec-a", "1.0.0", "2.0.0")

    assert plan.target_version == "2.0.0", "目標版本不匹配"
    assert plan.risk_level in [
        "CRITICAL",
        "HIGH",
    ], f"MAJOR升級風險應該高，實際{plan.risk_level}"
    assert len(plan.testing_requirements) >= 4, "應該有完整測試需求"

    print(f"✓ 遷移計劃已生成:")
    print(f"  - 預估工作量: {plan.estimated_effort_days} 天")
    print(f"  - 風險級別: {plan.risk_level}")
    print(f"  - 測試需求: {len(plan.testing_requirements)} 項")

    print("✅ Impact Analyzer tests passed")


def main():
    """運行所有測試"""
    print("\n" + "=" * 60)
    print("Strict Version Management - Test Suite")
    print("=" * 60)

    try:
        test_version_format_validation()
        test_version_sequence_validation()
        test_production_deployment_validation()
        test_compatibility_checking()
        test_impact_analyzer()

        print("\n" + "=" * 60)
        print("✅ ALL STRICT VERSION TESTS PASSED")
        print("=" * 60)
        print("")
        print("驗證結果:")
        print("  ✓ 版本格式驗證")
        print("  ✓ 版本序列驗證（禁止跳躍）")
        print("  ✓ 生產部署驗證")
        print("  ✓ 兼容性檢查")
        print("  ✓ 影響分析")
        print("")
        print("Airworthiness-Grade compliance achieved!")
        print("=" * 60 + "\n")

        return 0

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
