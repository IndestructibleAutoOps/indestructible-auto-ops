#!/usr/bin/env python3
"""
GL Pre-Execution Hook
======================
執行前鉤子 - 在任何操作執行前，強制執行治理檢查

版本: 1.0.0
用途: 確保所有操作在執行前都通過治理檢查
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
    GovernanceViolationError
)


class PreExecutionResult:
    """執行前檢查結果"""
    
    def __init__(
        self,
        passed: bool,
        execution_plan: Optional[Dict[str, Any]] = None,
        violations: Optional[list] = None
    ):
        self.passed = passed
        self.execution_plan = execution_plan or {}
        self.violations = violations or []
        self.timestamp = datetime.now().isoformat()


def pre_execution_hook(
    operation_name: str,
    operation_type: str,
    parameters: Dict[str, Any],
    user: Optional[str] = None,
    workspace_path: str = "."
) -> PreExecutionResult:
    """
    執行前鉤子：任何操作執行前必須通過
    
    Args:
        operation_name: 操作名稱
        operation_type: 操作類型
        parameters: 操作參數
        user: 用戶（可選）
        workspace_path: 工作空間路徑
    
    Returns:
        執行前檢查結果
    
    Raises:
        GovernanceViolationError: 如果檢查失敗
    """
    print("\n" + "="*80)
    print("🔒 GL Pre-Execution Hook v1.0.0")
    print("="*80)
    print(f"操作: {operation_name}")
    print(f"類型: {operation_type}")
    print(f"用戶: {user or 'system'}")
    print(f"時間: {datetime.now().isoformat()}")
    print("="*80)
    
    # 創建操作對象
    operation = Operation(
        name=operation_name,
        type=operation_type,
        parameters=parameters,
        timestamp=datetime.now().isoformat(),
        user=user
    )
    
    # 初始化治理強制執行器
    enforcer = GovernanceEnforcer(workspace_path=workspace_path)
    
    violations = []
    
    try:
        # [GA-001] 強制查詢治理合約
        print(f"\n[GA-001] 查詢治理合約...")
        contracts = enforcer.find_contracts(operation)
        if not contracts:
            violation = {
                "rule": "GA-001",
                "severity": "CRITICAL",
                "message": "未找到相關治理合約",
                "remediation": "請檢查 ecosystem/contracts/ 了解相關治理規範"
            }
            violations.append(violation)
            raise GovernanceViolationError(violation["message"])
        
        print(f"✅ 找到 {len(contracts)} 個相關治理合約")
        for contract in contracts:
            print(f"   - {contract.name} (v{contract.version}, {contract.category})")
        
        # [GA-GATE] 檢查操作閘門
        print(f"\n[GA-GATE] 檢查操作閘門...")
        gate_result = enforcer.check_gates(operation)
        if not gate_result.passed:
            violation = {
                "rule": "GA-GATE",
                "severity": "CRITICAL",
                "message": f"操作被閘門阻止: {gate_result.reason}",
                "gate_name": gate_result.gate_name,
                "remediation": "請檢查 ecosystem/gates/operation-gate.yaml"
            }
            violations.append(violation)
            raise GovernanceViolationError(violation["message"])
        
        print(f"✅ 閘門檢查通過: {gate_result.reason}")
        
        # [GA-002] 強制使用驗證工具
        print(f"\n[GA-002] 運行驗證器...")
        validation_result = enforcer.run_validators(operation, contracts)
        if not validation_result.passed:
            violation = {
                "rule": "GA-002",
                "severity": "CRITICAL",
                "message": f"驗證失敗: {validation_result.errors}",
                "errors": validation_result.errors,
                "remediation": "請修復驗證錯誤後重試"
            }
            violations.append(violation)
            raise GovernanceViolationError(violation["message"])
        
        print(f"✅ 驗證器檢查通過")
        if validation_result.warnings:
            print(f"⚠️  警告: {validation_result.warnings}")
        
        # [GA-PLAN] 生成執行計劃
        print(f"\n[GA-PLAN] 生成執行計劃...")
        execution_plan = enforcer.generate_execution_plan(
            operation,
            contracts,
            validation_result
        )
        print(f"✅ 執行計劃已生成")
        print(f"   - 治理合約: {len(execution_plan.contracts)}")
        print(f"   - 驗證器: {len(execution_plan.validators)}")
        print(f"   - 操作閘門: {len(execution_plan.gates)}")
        print(f"   - 證據覆蓋率要求: {execution_plan.min_evidence_coverage * 100}%")
        
        # [GA-VALIDATE] 驗證計劃符合治理規範
        print(f"\n[GA-VALIDATE] 驗證執行計劃...")
        if not enforcer.validate_plan(execution_plan):
            violation = {
                "rule": "GA-VALIDATE",
                "severity": "CRITICAL",
                "message": "執行計劃不符合治理規範",
                "remediation": "請檢查執行計劃是否包含必要的治理合約和證據要求"
            }
            violations.append(violation)
            raise GovernanceViolationError(violation["message"])
        
        print(f"✅ 執行計劃驗證通過")
        
        # 所有檢查通過
        print("\n" + "="*80)
        print("✅ 所有檢查通過，操作可以執行")
        print("="*80)
        
        # 返回成功結果
        return PreExecutionResult(
            passed=True,
            execution_plan={
                "operation": operation.name,
                "type": operation.type,
                "contracts": [c.name for c in execution_plan.contracts],
                "validators": [v.name for v in execution_plan.validators],
                "gates": [g.operation for g in execution_plan.gates],
                "evidence_requirements": execution_plan.evidence_requirements,
                "min_evidence_coverage": execution_plan.min_evidence_coverage,
                "created_at": execution_plan.created_at
            }
        )
        
    except GovernanceViolationError as e:
        print("\n" + "="*80)
        print(f"❌ 操作被治理規範阻止")
        print("="*80)
        print(f"原因: {e.message}")
        print(f"嚴重性: {e.severity.value}")
        print("\n違規項:")
        for v in violations:
            print(f"  [{v['rule']}] {v['severity']}")
            print(f"  說明: {v['message']}")
            if 'remediation' in v:
                print(f"  修復: {v['remediation']}")
        print("\n請查看 ecosystem/contracts/ 了解相關治理規範")
        print("="*80 + "\n")
        
        # 返回失敗結果
        return PreExecutionResult(
            passed=False,
            violations=violations
        )
    
    except Exception as e:
        # 未預期的錯誤
        print(f"\n❌ 執行前檢查發生未預期的錯誤: {e}")
        
        violation = {
            "rule": "UNEXPECTED_ERROR",
            "severity": "CRITICAL",
            "message": str(e),
            "remediation": "請檢查系統配置和環境"
        }
        violations.append(violation)
        
        return PreExecutionResult(
            passed=False,
            violations=violations
        )


def main():
    """測試執行前鉤子"""
    print("🧪 測試 Pre-Execution Hook")
    print("="*80)
    
    # 測試案例 1: 文件遷移操作（應該成功或失敗，取決於是否有相關合約）
    print("\n測試案例 1: 文件遷移操作")
    print("-"*80)
    
    result = pre_execution_hook(
        operation_name="文件遷移",
        operation_type="file_migration",
        parameters={
            "source": ".",
            "target": "ecosystem/docs/",
            "description": "遷移治理文件"
        },
        user="test_user",
        workspace_path="."
    )
    
    if result.passed:
        print("\n✅ 測試案例 1 通過")
        print(f"執行計劃: {json.dumps(result.execution_plan, indent=2, ensure_ascii=False)}")
    else:
        print("\n❌ 測試案例 1 失敗（預期行為，因為缺少治理合約）")
        print(f"違規項: {json.dumps(result.violations, indent=2, ensure_ascii=False)}")
    
    # 測試案例 2: 代碼提交操作
    print("\n" + "="*80)
    print("\n測試案例 2: 代碼提交操作")
    print("-"*80)
    
    result = pre_execution_hook(
        operation_name="代碼提交",
        operation_type="code_commit",
        parameters={
            "branch": "feature/test",
            "files": ["test.py"],
            "message": "Test commit"
        },
        user="developer",
        workspace_path="."
    )
    
    if result.passed:
        print("\n✅ 測試案例 2 通過")
    else:
        print("\n❌ 測試案例 2 失敗（預期行為）")
    
    print("\n" + "="*80)
    print("測試完成")
    print("="*80)


if __name__ == "__main__":
    main()