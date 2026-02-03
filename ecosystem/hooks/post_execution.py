#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: general
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Post-Execution Hook
=======================
執行後鉤子 - 在操作完成後，強制驗證結果和報告

版本: 1.0.0
用途: 確保所有操作完成後都通過治理驗證
"""

# MNGA-002: Import organization needs review
"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add ecosystem to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ecosystem.enforcers.governance_enforcer import (
    GovernanceEnforcer,
    Operation,
    ValidationResult,
    GovernanceViolationError
)


class PostExecutionResult:
    """執行後驗證結果"""
    
    def __init__(
        self,
        passed: bool,
        validation_result: Optional[ValidationResult] = None,
        audit_result: Optional[Dict[str, Any]] = None,
        violations: Optional[list] = None
    ):
        self.passed = passed
        self.validation_result = validation_result
        self.audit_result = audit_result or {}
        self.violations = violations or []
        self.timestamp = datetime.now().isoformat()


def post_execution_hook(
    operation_name: str,
    operation_type: str,
    result: Any,
    workspace_path: str = "."
) -> PostExecutionResult:
    """
    執行後鉤子：操作完成後必須通過驗證
    
    Args:
        operation_name: 操作名稱
        operation_type: 操作類型
        result: 操作結果
        workspace_path: 工作空間路徑
    
    Returns:
        執行後驗證結果
    
    Raises:
        GovernanceViolationError: 如果驗證失敗
    """
    print("\n" + "="*80)
    print("🔍 GL Post-Execution Hook v1.0.0")
    print("="*80)
    print(f"操作: {operation_name}")
    print(f"類型: {operation_type}")
    print(f"時間: {datetime.now().isoformat()}")
    print("="*80)
    
    # 創建操作對象
    operation = Operation(
        name=operation_name,
        type=operation_type,
        parameters={},
        timestamp=datetime.now().isoformat(),
        user=None
    )
    
    # 初始化治理強制執行器
    enforcer = GovernanceEnforcer(workspace_path=workspace_path)
    
    violations = []
    
    try:
        # [GA-003] 檢查證據鏈
        print(f"\n[GA-003] 檢查證據鏈...")
        if hasattr(result, 'has_evidence'):
            if not result.has_evidence():
                violation = {
                    "rule": "GA-003",
                    "severity": "CRITICAL",
                    "message": "缺少證據鏈",
                    "remediation": "請使用 GL Fact Verification Pipeline 生成證據鏈"
                }
                violations.append(violation)
                raise GovernanceViolationError(violation["message"])
            
            print(f"✅ 證據鏈存在")
            
            # 檢查證據覆蓋率
            if hasattr(result, 'evidence_coverage'):
                coverage = result.evidence_coverage
                print(f"   證據覆蓋率: {coverage * 100}%")
                
                if coverage < 0.9:
                    violation = {
                        "rule": "GA-003",
                        "severity": "CRITICAL",
                        "message": f"證據覆蓋率不足: {coverage} < 0.9",
                        "coverage": coverage,
                        "required": 0.9,
                        "remediation": "請提高證據覆蓋率到至少 90%"
                    }
                    violations.append(violation)
                    raise GovernanceViolationError(violation["message"])
                
                print(f"✅ 證據覆蓋率符合要求")
        else:
            print(f"⚠️  結果對象沒有 has_evidence 方法")
            violation = {
                "rule": "GA-003",
                "severity": "CRITICAL",
                "message": "結果對象缺少 has_evidence 方法",
                "remediation": "請確保結果對象實現 has_evidence 方法"
            }
            violations.append(violation)
            raise GovernanceViolationError(violation["message"])
        
        # [GA-004] 驗證報告
        print(f"\n[GA-004] 驗證報告...")
        if hasattr(result, 'report'):
            report = result.report
            print(f"✅ 報告存在")
            
            # 檢查禁止短語
            forbidden_phrases = [
                "100% 完成",
                "完全符合",
                "已全部实现",
                "覆盖所有标准",
                "100% complete",
                "fully compliant",
                "completely implemented",
                "covers all standards"
            ]
            
            forbidden_found = []
            for phrase in forbidden_phrases:
                if phrase in report:
                    forbidden_found.append(phrase)
            
            if forbidden_found:
                violation = {
                    "rule": "GA-004",
                    "severity": "CRITICAL",
                    "message": f"報告包含禁止短語: {forbidden_found}",
                    "forbidden_phrases": forbidden_found,
                    "remediation": "請使用更具體的描述，避免使用絕對性詞匯"
                }
                violations.append(violation)
                raise GovernanceViolationError(violation["message"])
            
            print(f"✅ 報告未包含禁止短語")
        else:
            print(f"⚠️  結果對象沒有 report 屬性")
            violation = {
                "rule": "GA-004",
                "severity": "CRITICAL",
                "message": "結果對象缺少 report 屬性",
                "remediation": "請確保結果對象包含 report 屬性"
            }
            violations.append(violation)
            raise GovernanceViolationError(violation["message"])
        
        # [GA-AUDIT] 生成治理審計日誌
        print(f"\n[GA-AUDIT] 生成治理審計日誌...")
        audit_log = enforcer.generate_audit_log(operation, result)
        enforcer.save_audit_log(audit_log)
        print(f"✅ 審計日誌已保存")
        
        # 檢查是否有違規
        if not audit_log.passed:
            print(f"\n⚠️  審計發現違規:")
            for finding in audit_log.findings:
                print(f"   - {finding}")
            
            violation = {
                "rule": "GA-AUDIT",
                "severity": "CRITICAL",
                "message": "審計發現違規",
                "findings": audit_log.findings,
                "violations": audit_log.violations,
                "remediation": "請修復所有審計發現的問題"
            }
            violations.append(violation)
            raise GovernanceViolationError(violation["message"])
        
        print(f"✅ 審計通過")
        
        # 所有驗證通過
        print("\n" + "="*80)
        print("✅ 所有驗證通過")
        print("="*80)
        
        # 返回成功結果
        validation_result = ValidationResult(
            passed=True,
            errors=[],
            warnings=[],
            evidence_coverage=getattr(result, 'evidence_coverage', 1.0),
            forbidden_phrases=[]
        )
        
        return PostExecutionResult(
            passed=True,
            validation_result=validation_result,
            audit_result={
                "operation": audit_log.operation,
                "timestamp": audit_log.timestamp,
                "passed": audit_log.passed,
                "findings": audit_log.findings,
                "evidence_coverage": audit_log.evidence_coverage,
                "violations": audit_log.violations
            }
        )
        
    except GovernanceViolationError as e:
        print("\n" + "="*80)
        print(f"❌ 執行後驗證失敗")
        print("="*80)
        print(f"原因: {e.message}")
        print(f"嚴重性: {e.severity.value}")
        print("\n違規項:")
        for v in violations:
            print(f"  [{v['rule']}] {v['severity']}")
            print(f"  說明: {v['message']}")
            if 'remediation' in v:
                print(f"  修復: {v['remediation']}")
        print("\n請修復問題後重新提交")
        print("="*80 + "\n")
        
        # 返回失敗結果
        return PostExecutionResult(
            passed=False,
            violations=violations
        )
    
    except Exception as e:
        # 未預期的錯誤
        print(f"\n❌ 執行後驗證發生未預期的錯誤: {e}")
        
        violation = {
            "rule": "UNEXPECTED_ERROR",
            "severity": "CRITICAL",
            "message": str(e),
            "remediation": "請檢查系統配置和環境"
        }
        violations.append(violation)
        
        return PostExecutionResult(
            passed=False,
            violations=violations
        )


def main():
    """測試執行後鉤子"""
    print("🧪 測試 Post-Execution Hook")
    print("="*80)
    
    # 測試案例 1: 成功的結果
    print("\n測試案例 1: 成功的結果")
    print("-"*80)
    
    class SuccessfulResult:
        def __init__(self):
            self.report = "遷移完成，所有文件已成功移動到目標目錄"
            self.evidence_coverage = 0.95
            self.evidence_links = ["file1", "file2", "file3"]
        
        def has_evidence(self):
            return True
    
    result = SuccessfulResult()
    
    post_result = post_execution_hook(
        operation_name="文件遷移",
        operation_type="file_migration",
        result=result,
        workspace_path="."
    )
    
    if post_result.passed:
        print("\n✅ 測試案例 1 通過")
        print(f"審計結果: {json.dumps(post_result.audit_result, indent=2, ensure_ascii=False)}")
    else:
        print("\n❌ 測試案例 1 失敗")
        print(f"違規項: {json.dumps(post_result.violations, indent=2, ensure_ascii=False)}")
    
    # 測試案例 2: 缺少證據鏈
    print("\n" + "="*80)
    print("\n測試案例 2: 缺少證據鏈")
    print("-"*80)
    
    class NoEvidenceResult:
        def __init__(self):
            self.report = "遷移完成"
        
        def has_evidence(self):
            return False
    
    result = NoEvidenceResult()
    
    post_result = post_execution_hook(
        operation_name="文件遷移",
        operation_type="file_migration",
        result=result,
        workspace_path="."
    )
    
    if post_result.passed:
        print("\n✅ 測試案例 2 通過")
    else:
        print("\n❌ 測試案例 2 失敗（預期行為）")
        print(f"違規項: {json.dumps(post_result.violations, indent=2, ensure_ascii=False)}")
    
    # 測試案例 3: 報告包含禁止短語
    print("\n" + "="*80)
    print("\n測試案例 3: 報告包含禁止短語")
    print("-"*80)
    
    class ForbiddenPhraseResult:
        def __init__(self):
            self.report = "100% 完成，完全符合所有標準"
            self.evidence_coverage = 0.95
        
        def has_evidence(self):
            return True
    
    result = ForbiddenPhraseResult()
    
    post_result = post_execution_hook(
        operation_name="文件遷移",
        operation_type="file_migration",
        result=result,
        workspace_path="."
    )
    
    if post_result.passed:
        print("\n✅ 測試案例 3 通過")
    else:
        print("\n❌ 測試案例 3 失敗（預期行為）")
        print(f"違規項: {json.dumps(post_result.violations, indent=2, ensure_ascii=False)}")
    
    # 測試案例 4: 證據覆蓋率不足
    print("\n" + "="*80)
    print("\n測試案例 4: 證據覆蓋率不足")
    print("-"*80)
    
    class LowCoverageResult:
        def __init__(self):
            self.report = "遷移完成"
            self.evidence_coverage = 0.85
        
        def has_evidence(self):
            return True
    
    result = LowCoverageResult()
    
    post_result = post_execution_hook(
        operation_name="文件遷移",
        operation_type="file_migration",
        result=result,
        workspace_path="."
    )
    
    if post_result.passed:
        print("\n✅ 測試案例 4 通過")
    else:
        print("\n❌ 測試案例 4 失敗（預期行為）")
        print(f"違規項: {json.dumps(post_result.violations, indent=2, ensure_ascii=False)}")
    
    print("\n" + "="*80)
    print("測試完成")
    print("="*80)


if __name__ == "__main__":
    main()