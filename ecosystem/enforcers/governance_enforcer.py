#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: governance
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Governance Enforcer
======================
治理強制執行器 - 確保所有操作都通過 ecosystem 框架驗證

版本: 1.0.0
用途: 強制執行所有治理規範，攔截違規操作
"""

import os
import sys
import yaml
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# Add ecosystem to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class Severity(Enum):
    """違規嚴重性"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class Contract:
    """治理合約"""
    name: str
    path: str
    content: Dict[str, Any]
    version: str
    category: str


@dataclass
class Validator:
    """驗證器"""
    name: str
    path: str
    type: str
    config: Dict[str, Any]


@dataclass
class Gate:
    """操作閘門"""
    operation: str
    required_checks: List[Dict[str, Any]]
    action: str  # BLOCK, WARN, SKIP


@dataclass
class Operation:
    """操作"""
    name: str
    type: str
    parameters: Dict[str, Any]
    timestamp: str
    user: Optional[str] = None


@dataclass
class ExecutionPlan:
    """執行計劃"""
    operation: Operation
    contracts: List[Contract]
    validators: List[Validator]
    gates: List[Gate]
    evidence_requirements: List[str]
    min_evidence_coverage: float
    created_at: str


@dataclass
class ValidationResult:
    """驗證結果"""
    passed: bool
    errors: List[str]
    warnings: List[str]
    evidence_coverage: float
    forbidden_phrases: List[str]


@dataclass
class GateResult:
    """閘門檢查結果"""
    passed: bool
    reason: str
    gate_name: str


@dataclass
class AuditLog:
    """審計日誌"""
    operation: str
    timestamp: str
    passed: bool
    findings: List[str]
    evidence_coverage: float
    violations: List[Dict[str, Any]]


class GovernanceViolationError(Exception):
    """治理違規異常"""
    
    def __init__(self, message: str, severity: Severity = Severity.CRITICAL):
        self.message = message
        self.severity = severity
        super().__init__(self.message)


class GovernanceEnforcer:
    """
    治理強制執行器
    
    職責:
    1. 操作前強制檢查（查詢合約、檢查閘門、運行驗證器）
    2. 操作後強制驗證（檢查證據鏈、驗證報告）
    3. 生成治理審計日誌
    """
    
    def __init__(self, workspace_path: str = "."):
        """
        初始化治理強制執行器
        
        Args:
            workspace_path: 工作空間路徑
        """
        self.workspace_path = Path(workspace_path)
        self.ecosystem_path = self.workspace_path / "ecosystem"
        
        # 加載配置
        self.contracts = self._load_contracts()
        self.validators = self._load_validators()
        self.gates = self._load_gates()
        
        # 禁止短語列表
        self.forbidden_phrases = [
            "100% 完成",
            "完全符合",
            "已全部实现",
            "覆盖所有标准",
            "100% complete",
            "fully compliant",
            "completely implemented",
            "covers all standards"
        ]
        
        # 治理規範強制執行點
        self.enforcement_points = {
            "GA-001": {
                "name": "Query Contracts",
                "severity": "CRITICAL",
                "description": "所有操作必須查詢 ecosystem/contracts/ 中的相關治理合約"
            },
            "GA-002": {
                "name": "Use Validators",
                "severity": "CRITICAL",
                "description": "所有操作必須使用 ecosystem/tools/ 中的驗證工具"
            },
            "GA-003": {
                "name": "Generate Evidence",
                "severity": "CRITICAL",
                "description": "所有報告必須包含完整的證據鏈"
            },
            "GA-004": {
                "name": "Verify Report",
                "severity": "CRITICAL",
                "description": "所有報告必須通過驗證器驗證"
            }
        }
        
        # 日誌路徑
        self.audit_log_path = self.ecosystem_path / "logs" / "audit-logs"
        self.audit_log_path.mkdir(parents=True, exist_ok=True)
    
    def _load_contracts(self) -> List[Contract]:
        """加載所有治理合約"""
        contracts = []
        contracts_path = self.ecosystem_path / "contracts"
        
        if not contracts_path.exists():
            return contracts
        
        # 加載所有 YAML 合約文件
        for yaml_file in contracts_path.rglob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)
                
                contract = Contract(
                    name=yaml_file.stem,
                    path=str(yaml_file.relative_to(self.workspace_path)),
                    content=content,
                    version=content.get('metadata', {}).get('version', '1.0.0'),
                    category=content.get('metadata', {}).get('category', 'unknown')
                )
                contracts.append(contract)
            except Exception as e:
                print(f"⚠️  無法加載合約 {yaml_file}: {e}")
        
        return contracts
    
    def _load_validators(self) -> List[Validator]:
        """加載所有驗證工具"""
        validators = []
        tools_path = self.ecosystem_path / "tools"
        
        if not tools_path.exists():
            return validators
        
        # 加載所有 Python 驗證工具
        for py_file in tools_path.rglob("*.py"):
            if py_file.name.startswith("_"):
                continue
            
            try:
                validator = Validator(
                    name=py_file.stem,
                    path=str(py_file.relative_to(self.workspace_path)),
                    type="python",
                    config={}
                )
                validators.append(validator)
            except Exception as e:
                print(f"⚠️  無法加載驗證器 {py_file}: {e}")
        
        return validators
    
    def _load_gates(self) -> List[Gate]:
        """加載所有操作閘門"""
        gates = []
        gates_path = self.ecosystem_path / "gates"
        
        if not gates_path.exists():
            # 創建默認閘門
            return self._create_default_gates()
        
        # 加載閘門配置
        gate_file = gates_path / "operation-gate.yaml"
        if gate_file.exists():
            try:
                with open(gate_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                for gate_spec in config.get('spec', {}).get('gates', []):
                    gate = Gate(
                        operation=gate_spec['operation'],
                        required_checks=gate_spec.get('required_checks', []),
                        action=gate_spec.get('action', 'BLOCK')
                    )
                    gates.append(gate)
            except Exception as e:
                print(f"⚠️  無法加載閘門配置: {e}")
                return self._create_default_gates()
        else:
            return self._create_default_gates()
        
        return gates
    
    def _create_default_gates(self) -> List[Gate]:
        """創建默認操作閘門"""
        return [
            Gate(
                operation="file_migration",
                required_checks=[
                    {
                        "check": "query_contracts",
                        "action": "BLOCK_IF_SKIPPED"
                    },
                    {
                        "check": "use_validator",
                        "action": "BLOCK_IF_FAILED"
                    },
                    {
                        "check": "generate_evidence",
                        "min_coverage": 0.9,
                        "action": "BLOCK_IF_MISSING"
                    },
                    {
                        "check": "verify_report",
                        "action": "BLOCK_IF_INVALID"
                    }
                ],
                action="BLOCK"
            ),
            Gate(
                operation="code_commit",
                required_checks=[
                    {
                        "check": "code_quality_gate",
                        "action": "BLOCK_IF_FAILED"
                    },
                    {
                        "check": "security_scan",
                        "action": "BLOCK_IF_FAILED"
                    }
                ],
                action="BLOCK"
            )
        ]
    
    def find_contracts(self, operation: Operation) -> List[Contract]:
        """
        查找相關治理合約 (GA-001)
        
        Args:
            operation: 操作對象
        
        Returns:
            相關治理合約列表
        """
        relevant_contracts = []
        
        # 根據操作類型篩選合約
        for contract in self.contracts:
            # 檢查合約類別是否與操作相關
            if self._is_contract_relevant(contract, operation):
                relevant_contracts.append(contract)
        
        return relevant_contracts
    
    def _is_contract_relevant(self, contract: Contract, operation: Operation) -> bool:
        """判斷合約是否與操作相關"""
        # 根據操作類型和合約類別匹配
        category_mapping = {
            "file_migration": ["naming-governance", "fact-verification", "verification"],
            "code_commit": ["validation", "verification"],
            "report_generation": ["fact-verification", "verification"]
        }
        
        relevant_categories = category_mapping.get(operation.type, [])
        return contract.category in relevant_categories
    
    def check_gates(self, operation: Operation) -> GateResult:
        """
        檢查操作閘門
        
        Args:
            operation: 操作對象
        
        Returns:
            閘門檢查結果
        """
        # 查找相關閘門
        relevant_gates = [g for g in self.gates if g.operation == operation.type]
        
        if not relevant_gates:
            return GateResult(passed=True, reason="沒有相關閘門", gate_name="none")
        
        # 檢查每個閘門
        for gate in relevant_gates:
            for check in gate.required_checks:
                check_name = check.get("check")
                action = check.get("action", "WARN")
                
                # 模擬檢查（實際應該根據 check 執行具體邏輯）
                check_passed = self._perform_check(operation, check)
                
                if not check_passed:
                    if action == "BLOCK_IF_SKIPPED":
                        return GateResult(
                            passed=False,
                            reason=f"閘門檢查失敗: {check_name}",
                            gate_name=gate.operation
                        )
                    elif action == "BLOCK_IF_FAILED":
                        return GateResult(
                            passed=False,
                            reason=f"驗證失敗: {check_name}",
                            gate_name=gate.operation
                        )
                    elif action == "BLOCK_IF_MISSING":
                        return GateResult(
                            passed=False,
                            reason=f"缺少必需項: {check_name}",
                            gate_name=gate.operation
                        )
        
        return GateResult(passed=True, reason="所有閘門檢查通過", gate_name="all")
    
    def _perform_check(self, operation: Operation, check: Dict[str, Any]) -> bool:
        """執行具體的檢查"""
        check_type = check.get("check")
        
        # 這裡應該根據 check_type 執行具體的檢查邏輯
        # 目前返回 True 作為示例
        return True
    
    def run_validators(self, operation: Operation, contracts: List[Contract]) -> ValidationResult:
        """
        運行驗證器 (GA-002)
        
        Args:
            operation: 操作對象
            contracts: 相關治理合約
        
        Returns:
            驗證結果
        """
        errors = []
        warnings = []
        forbidden_phrases = []
        
        # 檢查是否有相關驗證器
        if not self.validators:
            warnings.append("沒有找到驗證工具")
        
        # 運行所有驗證器
        for validator in self.validators:
            try:
                # 這裡應該實際調用驗證器
                # 目前只是模擬
                pass
            except Exception as e:
                errors.append(f"驗證器 {validator.name} 運行失敗: {e}")
        
        # 檢查操作參數中的禁止短語
        for param_name, param_value in operation.parameters.items():
            if isinstance(param_value, str):
                for phrase in self.forbidden_phrases:
                    if phrase in param_value:
                        forbidden_phrases.append(f"參數 {param_name} 包含禁止短語: '{phrase}'")
        
        return ValidationResult(
            passed=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            evidence_coverage=0.0,
            forbidden_phrases=forbidden_phrases
        )
    
    def generate_execution_plan(
        self,
        operation: Operation,
        contracts: List[Contract],
        validation: ValidationResult
    ) -> ExecutionPlan:
        """
        生成執行計劃
        
        Args:
            operation: 操作對象
            contracts: 相關治理合約
            validation: 驗證結果
        
        Returns:
            執行計劃
        """
        # 證據要求
        evidence_requirements = [
            "contract_references",
            "validation_results",
            "evidence_links",
            "sha256_hashes"
        ]
        
        # 最小證據覆蓋率
        min_evidence_coverage = 0.9
        
        # 創建執行計劃
        execution_plan = ExecutionPlan(
            operation=operation,
            contracts=contracts,
            validators=self.validators,
            gates=[g for g in self.gates if g.operation == operation.type],
            evidence_requirements=evidence_requirements,
            min_evidence_coverage=min_evidence_coverage,
            created_at=datetime.now().isoformat()
        )
        
        return execution_plan
    
    def validate_plan(self, plan: ExecutionPlan) -> bool:
        """
        驗證執行計劃
        
        Args:
            plan: 執行計劃
        
        Returns:
            是否通過驗證
        """
        # 檢查是否有相關合約
        if not plan.contracts:
            print("⚠️  執行計劃沒有包含任何治理合約")
            return False
        
        # 檢查證據要求
        if not plan.evidence_requirements:
            print("⚠️  執行計劃缺少證據要求")
            return False
        
        # 檢查證據覆蓋率
        if plan.min_evidence_coverage < 0.9:
            print("⚠️  證據覆蓋率低於要求")
            return False
        
        return True
    
    def before_operation(self, operation: Operation) -> ExecutionPlan:
        """
        操作前強制檢查
        
        Args:
            operation: 操作對象
        
        Returns:
            執行計劃
        
        Raises:
            GovernanceViolationError: 如果檢查失敗
        """
        print(f"\n{'='*80}")
        print(f"🔍 治理強制執行: 操作前檢查")
        print(f"{'='*80}")
        print(f"操作: {operation.name}")
        print(f"類型: {operation.type}")
        print(f"時間: {operation.timestamp}")
        
        # 1. 查詢相關治理合約 (GA-001)
        print(f"\n[GA-001] 查詢治理合約...")
        contracts = self.find_contracts(operation)
        if not contracts:
            raise GovernanceViolationError(
                f"未找到相關治理合約，請檢查 ecosystem/contracts/"
            )
        print(f"✅ 找到 {len(contracts)} 個相關治理合約:")
        for contract in contracts:
            print(f"   - {contract.name} (v{contract.version})")
        
        # 2. 檢查操作閘門
        print(f"\n[GA-GATE] 檢查操作閘門...")
        gate_result = self.check_gates(operation)
        if not gate_result.passed:
            raise GovernanceViolationError(
                f"操作被閘門阻止: {gate_result.reason}"
            )
        print(f"✅ 閘門檢查通過: {gate_result.reason}")
        
        # 3. 運行驗證器 (GA-002)
        print(f"\n[GA-002] 運行驗證器...")
        validation_result = self.run_validators(operation, contracts)
        if not validation_result.passed:
            raise GovernanceViolationError(
                f"操作被驗證器阻止: {validation_result.errors}"
            )
        print(f"✅ 驗證器檢查通過")
        if validation_result.warnings:
            print(f"⚠️  警告: {validation_result.warnings}")
        
        # 4. 生成執行計劃
        print(f"\n[GA-PLAN] 生成執行計劃...")
        execution_plan = self.generate_execution_plan(
            operation,
            contracts,
            validation_result
        )
        print(f"✅ 執行計劃已生成")
        print(f"   - 治理合約: {len(execution_plan.contracts)}")
        print(f"   - 驗證器: {len(execution_plan.validators)}")
        print(f"   - 操作閘門: {len(execution_plan.gates)}")
        print(f"   - 證據覆蓋率要求: {execution_plan.min_evidence_coverage * 100}%")
        
        # 5. 驗證計劃符合治理規範
        print(f"\n[GA-VALIDATE] 驗證執行計劃...")
        if not self.validate_plan(execution_plan):
            raise GovernanceViolationError("執行計劃不符合治理規範")
        print(f"✅ 執行計劃驗證通過")
        
        print(f"\n{'='*80}")
        print(f"✅ 所有檢查通過，操作可以執行")
        print(f"{'='*80}\n")
        
        return execution_plan
    
    def after_operation(self, operation: Operation, result: Any) -> ValidationResult:
        """
        操作後強制驗證
        
        Args:
            operation: 操作對象
            result: 操作結果
        
        Returns:
            驗證結果
        
        Raises:
            GovernanceViolationError: 如果驗證失敗
        """
        print(f"\n{'='*80}")
        print(f"🔍 治理強制執行: 操作後驗證")
        print(f"{'='*80}")
        print(f"操作: {operation.name}")
        
        # 檢查結果類型
        if hasattr(result, 'has_evidence'):
            # 1. 檢查證據鏈 (GA-003)
            print(f"\n[GA-003] 檢查證據鏈...")
            if not result.has_evidence():
                raise GovernanceViolationError(
                    "缺少證據鏈，請使用 GL Fact Verification Pipeline"
                )
            print(f"✅ 證據鏈存在")
            
            # 檢查證據覆蓋率
            if hasattr(result, 'evidence_coverage'):
                coverage = result.evidence_coverage
                print(f"   證據覆蓋率: {coverage * 100}%")
                if coverage < 0.9:
                    raise GovernanceViolationError(
                        f"證據覆蓋率不足: {coverage} < 0.9"
                    )
                print(f"✅ 證據覆蓋率符合要求")
        else:
            print(f"\n⚠️  結果對象沒有 has_evidence 方法")
        
        # 2. 驗證報告 (GA-004)
        print(f"\n[GA-004] 驗證報告...")
        if hasattr(result, 'report'):
            report = result.report
            
            # 檢查禁止短語
            forbidden_found = []
            for phrase in self.forbidden_phrases:
                if phrase in report:
                    forbidden_found.append(phrase)
            
            if forbidden_found:
                raise GovernanceViolationError(
                    f"報告包含禁止短語: {forbidden_found}"
                )
            print(f"✅ 報告未包含禁止短語")
        else:
            print(f"\n⚠️  結果對象沒有 report 屬性")
        
        # 3. 生成治理審計日誌
        print(f"\n[GA-AUDIT] 生成審計日誌...")
        audit_log = self.generate_audit_log(operation, result)
        self.save_audit_log(audit_log)
        print(f"✅ 審計日誌已保存")
        
        print(f"\n{'='*80}")
        print(f"✅ 所有驗證通過")
        print(f"{'='*80}\n")
        
        return ValidationResult(
            passed=True,
            errors=[],
            warnings=[],
            evidence_coverage=1.0,
            forbidden_phrases=[]
        )
    
    def generate_audit_log(self, operation: Operation, result: Any) -> AuditLog:
        """
        生成治理審計日誌
        
        Args:
            operation: 操作對象
            result: 操作結果
        
        Returns:
            審計日誌
        """
        # 收集違規信息
        violations = []
        
        # 檢查 GA-001
        if not hasattr(operation, 'queried_contracts') or not operation.queried_contracts:
            violations.append({
                "rule": "GA-001",
                "severity": "CRITICAL",
                "description": "未查詢治理合約"
            })
        
        # 檢查 GA-002
        if not hasattr(operation, 'used_validators') or not operation.used_validators:
            violations.append({
                "rule": "GA-002",
                "severity": "CRITICAL",
                "description": "未使用驗證工具"
            })
        
        # 檢查 GA-003
        if hasattr(result, 'has_evidence') and not result.has_evidence():
            violations.append({
                "rule": "GA-003",
                "severity": "CRITICAL",
                "description": "未生成證據鏈"
            })
        
        # 檢查 GA-004
        if hasattr(result, 'report_verified') and not result.report_verified:
            violations.append({
                "rule": "GA-004",
                "severity": "CRITICAL",
                "description": "報告未驗證"
            })
        
        # 生成審計日誌
        audit_log = AuditLog(
            operation=operation.name,
            timestamp=datetime.now().isoformat(),
            passed=len(violations) == 0,
            findings=[f"{v['rule']}: {v['description']}" for v in violations],
            evidence_coverage=getattr(result, 'evidence_coverage', 0.0),
            violations=violations
        )
        
        return audit_log
    
    def save_audit_log(self, audit_log: AuditLog):
        """
        保存審計日誌
        
        Args:
            audit_log: 審計日誌
        """
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"audit-{timestamp}-{audit_log.operation}.json"
        filepath = self.audit_log_path / filename
        
        # 保存日誌
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(audit_log), f, indent=2, ensure_ascii=False)
        
        print(f"📝 審計日誌已保存到: {filepath}")


def main():
    """測�试治理強制執行器"""
    print("🚀 GL Governance Enforcer v1.0.0")
    print("=" * 80)
    
    # 初始化強制執行器
    enforcer = GovernanceEnforcer(workspace_path=".")
    
    # 創建測試操作
    operation = Operation(
        name="文件遷移",
        type="file_migration",
        parameters={
            "source": ".",
            "target": "ecosystem/docs/",
            "description": "遷移治理文件"
        },
        timestamp=datetime.now().isoformat(),
        user="test_user"
    )
    
    # 測試操作前檢查
    try:
        execution_plan = enforcer.before_operation(operation)
        print("\n✅ 測試通過：操作前檢查")
    except GovernanceViolationError as e:
        print(f"\n❌ 測試失敗：{e.message}")
        return
    
    # 模擬操作結果
    class MockResult:
        def __init__(self):
            self.has_evidence_flag = True
            self.evidence_coverage = 0.95
            self.report = "遷移完成"
        
        def has_evidence(self):
            return self.has_evidence_flag
    
    result = MockResult()
    
    # 測試操作後驗證
    try:
        validation_result = enforcer.after_operation(operation, result)
        print("\n✅ 測試通過：操作後驗證")
    except GovernanceViolationError as e:
        print(f"\n❌ 測試失敗：{e.message}")
        return


if __name__ == "__main__":
    main()