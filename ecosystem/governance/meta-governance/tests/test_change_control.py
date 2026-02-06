#!/usr/bin/env python3
"""
Change Control System Tests
============================
測試嚴格變更控制系統
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from change_control_system import (
    ChangeControlSystem,
    ChangeProposal,
    ReviewDecision,
    ChangeCategory,
    UrgencyLevel,
    ChangeStatus,
)


def test_proposal_submission():
    """測試提案提交"""
    print("\n=== Test Proposal Submission ===")

    system = ChangeControlSystem()

    # 創建提案
    proposal = ChangeProposal(
        proposal_id="CR-2024-001",
        spec_id="security-baseline",
        current_version="1.3.5",
        proposed_version="1.4.0",
        change_category=ChangeCategory.FEATURE_ENHANCEMENT,
        urgency_level=UrgencyLevel.NORMAL,
        title="新增多因素身份驗證要求",
        abstract="在安全基礎規範中新增MFA強制要求",
        rationale={
            "business_drivers": ["提升安全性"],
            "technical_drivers": ["現有驗證不足"],
        },
        detailed_changes=[{"location": "section-4.2"}],
        impact_analysis={"affected_validators": 145},
        risk_assessment={"security_risks": []},
        test_plan={"unit_tests": []},
        proposer_id="proposer-001",
        proposer_role="spec-owner",
    )

    # 提交提案
    success, errors = system.submit_proposal(proposal)

    assert success, f"提案提交失敗: {errors}"
    print(f"✓ 提案已提交: {proposal.proposal_id}")

    # 驗證狀態
    assert proposal.status == ChangeStatus.PROPOSED, "狀態應為PROPOSED"
    print("✓ 狀態正確")

    print("✅ Proposal Submission tests passed")


def test_review_process():
    """測試審查流程"""
    print("\n=== Test Review Process ===")

    system = ChangeControlSystem()

    # 提交提案
    proposal = ChangeProposal(
        proposal_id="CR-2024-002",
        spec_id="ops-spec",
        current_version="2.0.0",
        proposed_version="2.0.1",
        change_category=ChangeCategory.BUG_FIX,
        urgency_level=UrgencyLevel.NORMAL,
        title="修正文檔錯誤",
        abstract="修正配置示例",
        rationale={"technical_drivers": ["文檔錯誤"]},
        detailed_changes=[{"location": "doc"}],
        impact_analysis={"affected": 1},
        risk_assessment={"risks": []},
        test_plan={"tests": ["unit"]},
        proposer_id="proposer-002",
        proposer_role="validator-owner",
    )

    system.submit_proposal(proposal)

    # 分配審查者
    reviewers = system.assign_reviewers("CR-2024-002", auto_assign=True)

    assert len(reviewers) >= 2, f"應至少分配2名審查者，實際{len(reviewers)}"
    print(f"✓ 審查者已分配: {len(reviewers)} 名")

    # 提交審查意見
    for i, reviewer in enumerate(reviewers):
        review = ReviewDecision(
            reviewer_id=reviewer,
            proposal_id="CR-2024-002",
            decision="approve",
            score={
                "技術正確性": 5,
                "清晰度": 4,
                "影響分析": 4,
                "風險管理": 5,
                "實施可行性": 5,
            },
            comments=[{"text": "LGTM"}],
        )

        system.submit_review("CR-2024-002", review)

    print(f"✓ 審查已完成: {len(reviewers)} 個審查意見")

    # 驗證狀態
    assert (
        proposal.status == ChangeStatus.REVIEWED
    ), f"狀態應為REVIEWED，實際{proposal.status}"
    print("✓ 審查狀態正確")

    print("✅ Review Process tests passed")


def test_approval_workflow():
    """測試批准工作流"""
    print("\n=== Test Approval Workflow ===")

    system = ChangeControlSystem()

    # 提交並審查提案
    proposal = ChangeProposal(
        proposal_id="CR-2024-003",
        spec_id="test-spec",
        current_version="1.0.0",
        proposed_version="1.0.1",
        change_category=ChangeCategory.BUG_FIX,
        urgency_level=UrgencyLevel.NORMAL,
        title="修正Bug",
        abstract="修正功能錯誤",
        rationale={"technical_drivers": ["bug"]},
        detailed_changes=[{"fix": "bug"}],
        impact_analysis={"affected": 1},
        risk_assessment={"low": True},
        test_plan={"unit": True},
        proposer_id="proposer-003",
        proposer_role="spec-owner",
    )

    system.submit_proposal(proposal)
    proposal.status = ChangeStatus.REVIEWED  # 模擬已審查

    # 請求批准
    approval_id = system.request_approval("CR-2024-003")

    assert approval_id != "", "批准請求失敗"
    print(f"✓ 批准已請求: {approval_id}")

    # 批准（需要spec-owner + 1-reviewer）
    system.approve("CR-2024-003", "spec-owner", "signature-1")
    system.approve("CR-2024-003", "1-reviewer", "signature-2")

    # 驗證狀態
    assert proposal.status == ChangeStatus.APPROVED, "狀態應為APPROVED"
    print("✓ 提案已批准")

    print("✅ Approval Workflow tests passed")


def test_full_workflow():
    """測試完整工作流"""
    print("\n=== Test Full Workflow ===")

    system = ChangeControlSystem()

    # 1. 提交提案
    proposal = ChangeProposal(
        proposal_id="CR-2024-FULL",
        spec_id="full-spec",
        current_version="1.0.0",
        proposed_version="1.1.0",
        change_category=ChangeCategory.FEATURE_ENHANCEMENT,
        urgency_level=UrgencyLevel.NORMAL,
        title="新功能",
        abstract="添加新功能",
        rationale={"business_drivers": ["需求"]},
        detailed_changes=[{"change": "new"}],
        impact_analysis={"validators": 10},
        risk_assessment={"medium": True},
        test_plan={"full": True},
        proposer_id="proposer-full",
        proposer_role="spec-owner",
    )

    success, _ = system.submit_proposal(proposal)
    assert success, "提案提交失敗"
    print("✓ 階段1: 提案已提交")

    # 2. 分配審查
    reviewers = system.assign_reviewers("CR-2024-FULL")
    assert len(reviewers) >= 2, "審查者不足"
    print(f"✓ 階段2: 審查者已分配 ({len(reviewers)})")

    # 3. 提交審查
    for reviewer in reviewers:
        review = ReviewDecision(
            reviewer_id=reviewer,
            proposal_id="CR-2024-FULL",
            decision="approve",
            score={
                "技術正確性": 4,
                "清晰度": 4,
                "影響分析": 4,
                "風險管理": 4,
                "實施可行性": 4,
            },
            comments=[],
        )
        system.submit_review("CR-2024-FULL", review)

    assert proposal.status == ChangeStatus.REVIEWED, "審查未完成"
    print("✓ 階段3: 審查已完成")

    # 4. 請求批准
    approval_id = system.request_approval("CR-2024-FULL")
    assert approval_id != "", "批准請求失敗"
    print("✓ 階段4: 批准已請求")

    # 5. 批准
    system.approve("CR-2024-FULL", "governance-core", "sig-1")
    system.approve("CR-2024-FULL", "spec-owner", "sig-2")
    assert proposal.status == ChangeStatus.APPROVED, "批准失敗"
    print("✓ 階段5: 已批准")

    # 6. 發布
    release_result = system.release_version("CR-2024-FULL")
    assert release_result.get("error") is None, "發布失敗"
    assert proposal.status == ChangeStatus.RELEASED, "發布狀態錯誤"
    print("✓ 階段6: 已發布")

    # 7. 通知
    notification_result = system.notify_stakeholders("CR-2024-FULL")
    assert notification_result["success"], "通知失敗"
    print("✓ 階段7: 通知已發送")

    # 8. 驗證審計追蹤
    audit = system.get_audit_trail("CR-2024-FULL")
    assert len(audit) >= 5, f"審計記錄不完整，應至少5條，實際{len(audit)}"
    print(f"✓ 階段8: 審計追蹤完整 ({len(audit)} 條記錄)")

    print("✅ Full Workflow tests passed")


def main():
    """運行所有測試"""
    print("\n" + "=" * 60)
    print("Change Control System - Test Suite")
    print("=" * 60)

    try:
        test_proposal_submission()
        test_review_process()
        test_approval_workflow()
        test_full_workflow()

        print("\n" + "=" * 60)
        print("✅ ALL CHANGE CONTROL TESTS PASSED")
        print("=" * 60)
        print("")
        print("驗證結果:")
        print("  ✓ 提案提交流程")
        print("  ✓ 審查分配與執行")
        print("  ✓ 批准工作流")
        print("  ✓ 完整端到端流程")
        print("")
        print("五階段變更控制: OPERATIONAL")
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
