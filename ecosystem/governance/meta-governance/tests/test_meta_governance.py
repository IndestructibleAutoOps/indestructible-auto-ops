#!/usr/bin/env python3
"""
Meta-Governance Tests
=====================
測試元治理框架
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from version_manager import VersionManager, SemanticVersion, VersionType
from change_manager import ChangeManager, ImpactLevel
from review_manager import ReviewManager, ReviewLayer, ReviewDecision
from dependency_manager import DependencyManager
from governance_framework import GovernanceFramework


def test_version_manager():
    """測試版本管理器"""
    print("\n=== Test Version Manager ===")

    vm = VersionManager()

    # 測試版本解析
    version = SemanticVersion.parse("2.1.3")
    assert version.major == 2, "Major version incorrect"
    assert version.minor == 1, "Minor version incorrect"
    assert version.patch == 3, "Patch version incorrect"
    print("✓ Version parsing works")

    # 測試版本創建
    v1 = vm.create_version(
        component="validator-core",
        version_type="minor",
        changes=["Add new rule", "Fix bug"],
    )

    assert v1.version.major == 1, "Initial major version should be 1"
    assert v1.version.minor == 0, "Initial minor version should be 0"
    print(f"✓ Version created: {v1.version}")

    # 測試版本遞增
    v2 = vm.create_version(
        component="validator-core", version_type="patch", changes=["Fix critical bug"]
    )

    assert v2.version.patch == 1, "Patch version should increment"
    print(f"✓ Version incremented: {v2.version}")

    # 測試版本比較
    assert v2.version > v1.version, "Version comparison failed"
    print("✓ Version comparison works")

    # 測試 LTS
    vm.set_lts_version("validator-core", str(v1.version))
    lts = vm.get_lts_version("validator-core")
    assert lts == str(v1.version), "LTS version incorrect"
    print(f"✓ LTS version set: {lts}")

    # 測試變更日誌生成
    changelog = vm.generate_changelog("validator-core")
    assert "validator-core" in changelog, "Changelog missing component name"
    print("✓ Changelog generated")

    # 測試兼容性檢查
    compat = vm.check_compatibility("validator-core", "1.0.0", "1.0.1")
    assert compat["compatible"], "Patch upgrade should be compatible"
    print("✓ Compatibility check works")

    print("✅ Version Manager tests passed")


def test_change_manager():
    """測試變更管理器"""
    print("\n=== Test Change Manager ===")

    cm = ChangeManager()

    # 提交變更
    change_id = cm.submit_change(
        title="Add OAuth2 support",
        description="Implement OAuth2 authentication",
        impact_level="medium",
        affected_components=["api-gateway"],
        submitter="developer",
    )

    assert change_id != "", "Change submission failed"
    print(f"✓ Change submitted: {change_id}")

    # 評估變更
    assessment = cm.assess_change(change_id)
    assert "risk_score" in assessment, "Assessment missing risk score"
    print(f"✓ Change assessed (risk: {assessment['risk_score']})")

    # 批准變更
    cm.approve_change(change_id, "team_lead")
    cm.approve_change(change_id, "tech_lead")

    change = cm.get_change(change_id)
    assert len(change.approvers) == 2, "Approvers not recorded"
    assert change.status.value == "approved", "Change not approved"
    print("✓ Change approved")

    # 執行變更
    success = cm.execute_change(change_id)
    assert success, "Change execution failed"
    print("✓ Change execution started")

    # 完成變更
    cm.complete_change(change_id, {"tests_passed": True})

    change = cm.get_change(change_id)
    assert change.status.value == "completed", "Change not completed"
    print("✓ Change completed")

    # 測試統計
    stats = cm.get_stats()
    assert stats["total_changes"] >= 1, "Stats incorrect"
    print(f"✓ Stats: {stats}")

    print("✅ Change Manager tests passed")


def test_review_manager():
    """測試審查管理器"""
    print("\n=== Test Review Manager ===")

    rm = ReviewManager()

    # 創建審查
    review_id = rm.create_review(
        change_id="test-change-123", required_layers=["technical", "architecture"]
    )

    assert review_id != "", "Review creation failed"
    print(f"✓ Review created: {review_id}")

    # 提交技術審查
    rm.submit_review(
        review_id=review_id,
        reviewer="dev-lead",
        layer="technical",
        decision="approved",
        comments="Code looks good",
    )

    print("✓ Technical review submitted")

    # 提交架構審查
    rm.submit_review(
        review_id=review_id,
        reviewer="architect",
        layer="architecture",
        decision="approved",
        comments="Design is sound",
    )

    print("✓ Architecture review submitted")

    # 檢查狀態
    status = rm.get_review_status(review_id)
    assert status is not None, "Status not found"
    assert status["completed"], "Review should be completed"
    print("✓ Review completed")

    print("✅ Review Manager tests passed")


def test_dependency_manager():
    """測試依賴管理器"""
    print("\n=== Test Dependency Manager ===")

    dm = DependencyManager({"max_dependency_depth": 3})

    # 添加依賴
    dm.add_dependency("api-gateway", "service-discovery", "1.0.0")
    dm.add_dependency("api-gateway", "jwt-library", "2.5.0")
    dm.add_dependency("service-discovery", "yaml-parser", "1.1.0")

    print("✓ Dependencies added")

    # 獲取直接依賴
    deps = dm.get_dependencies("api-gateway", recursive=False)
    assert len(deps) == 2, "Direct dependencies count incorrect"
    print(f"✓ Direct dependencies: {len(deps)}")

    # 獲取遞歸依賴
    all_deps = dm.get_dependencies("api-gateway", recursive=True)
    assert len(all_deps) >= 2, "Recursive dependencies incorrect"
    print(f"✓ Recursive dependencies: {len(all_deps)}")

    # 計算依賴深度
    depth = dm.calculate_dependency_depth("api-gateway")
    assert depth >= 1, "Dependency depth incorrect"
    print(f"✓ Dependency depth: {depth}")

    # 驗證依賴
    validation = dm.validate_dependencies("api-gateway")
    assert validation["valid"], f"Validation failed: {validation['errors']}"
    print("✓ Dependencies validated")

    # 測試循環依賴檢測
    dm.add_dependency("yaml-parser", "api-gateway", "1.0.0")  # 創建循環
    cycles = dm.detect_circular_dependencies()
    assert len(cycles) >= 1, "Circular dependency not detected"
    print(f"✓ Circular dependency detected: {len(cycles)} cycles")

    print("✅ Dependency Manager tests passed")


def test_governance_framework():
    """測試治理框架"""
    print("\n=== Test Governance Framework ===")

    gf = GovernanceFramework()

    # 提出變更
    result = gf.propose_change(
        title="Upgrade authentication",
        description="Add OAuth2 support",
        component="api-gateway",
        impact_level="medium",
        submitter="developer",
    )

    assert "change_id" in result, "Change proposal failed"
    assert "review_id" in result, "Review not created"
    print(f"✓ Change proposed: {result['change_id']}")
    print(f"  Review: {result['review_id']}")
    print(f"  Risk score: {result['risk_score']}")

    # 發布版本
    version = gf.release_version(
        component="api-gateway",
        version_type="minor",
        changes=["Add OAuth2 support"],
        breaking_changes=[],
    )

    assert version != "", "Version release failed"
    print(f"✓ Version released: {version}")

    # 生成治理報告
    report = gf.get_governance_report()
    assert "version_management" in report, "Report missing version management"
    assert "change_management" in report, "Report missing change management"
    print("✓ Governance report generated")
    print(f"  Versions: {report['version_management']['total_versions']}")
    print(f"  Changes: {report['change_management']['total_changes']}")

    print("✅ Governance Framework tests passed")


def main():
    """運行所有測試"""
    print("\n" + "=" * 60)
    print("Meta-Governance Framework - Test Suite")
    print("=" * 60)

    try:
        test_version_manager()
        test_change_manager()
        test_review_manager()
        test_dependency_manager()
        test_governance_framework()

        print("\n" + "=" * 60)
        print("✅ ALL META-GOVERNANCE TESTS PASSED")
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
