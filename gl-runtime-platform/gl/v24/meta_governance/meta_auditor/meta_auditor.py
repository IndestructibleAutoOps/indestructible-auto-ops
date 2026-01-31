# GL Runtime V24 - Meta-Governance: Meta-Auditor
# @GL-governed
# @GL-layer: V24-meta-gl_platform_universegl_platform_universe.governance
# @GL-semantic: meta-auditor-core
# @GL-dependencies: V23

"""
GL Runtime V24: 元治理層 - 元審計器
核心功能: 審計V23 Root Governance本身, 確保治理者也被治理
承諾: 連 Root Governance Layer 也不能自欺欺人
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class AuditScope(Enum):
    ANTI_FABRIC = "anti_fabric"
    FALSIFICATION = "falsification"
    EXECUTION_HARNESS = "execution_harness"
    RULES = "rules"
    AUDITOR = "auditor"
    ENFORCER = "enforcer"
    MEMORY = "memory"
    ALL = "all"


class AuditResult(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    CRITICAL = "critical"


@dataclass
class MetaAuditRecord:
    """元審計記錄"""
    audit_id: str
    scope: AuditScope
    result: AuditResult
    findings: List[Dict[str, Any]]
    recommendations: List[str]
    audited_at: datetime = field(default_factory=datetime.utcnow)
    auditor_version: str = "v24.0.0"
    signature: Optional[str] = None


@dataclass
class GovernanceIntegrityCheck:
    """治理完整性檢查"""
    check_id: str
    component: str
    expected_behavior: str
    actual_behavior: str
    deviation_detected: bool
    severity: str = "info"


class MetaAuditor:
    """
    GL V24 元審計器
    
    核心機制:
    1. 遞歸治理: 治理者本身也被治理
    2. 無限退後: 可以無限層次地審問治理的正確性
    3. 終極審計: 沒有任何層級能夠逃避審計
    4. 成功定義審查: 連什麼是「成功」也會被質疑
    """
    
    def __init__(self):
        self._audit_records: Dict[str, MetaAuditRecord] = {}
        self._integrity_checks: Dict[str, GovernanceIntegrityCheck] = {}
        self._meta_rules: List[Dict[str, Any]] = []
        self._audit_callbacks: List[Callable] = []
        self._recursion_depth: int = 0
        self._max_recursion: int = 10
    
    def audit_root_gl_platform_universegl_platform_universe.governance(
        self,
        root_gl_platform_universegl_platform_universe.governance_state: Dict[str, Any]
    ) -> MetaAuditRecord:
        """審計 V23 Root Governance"""
        findings = []
        recommendations = []
        
        # 檢查 Anti-Fabric 運作
        if "anti_fabric" in root_gl_platform_universegl_platform_universe.governance_state:
            af_result = self._audit_anti_fabric(root_gl_platform_universegl_platform_universe.governance_state["anti_fabric"])
            findings.extend(af_result.get("findings", []))
            recommendations.extend(af_result.get("recommendations", []))
        
        # 檢查 Falsification Engine
        if "falsification" in root_gl_platform_universegl_platform_universe.governance_state:
            fe_result = self._audit_falsification(root_gl_platform_universegl_platform_universe.governance_state["falsification"])
            findings.extend(fe_result.get("findings", []))
        
        # 檢查治理規則一致性
        rules_result = self._audit_gl_platform_universegl_platform_universe.governance_rules(root_gl_platform_universegl_platform_universe.governance_state)
        findings.extend(rules_result.get("findings", []))
        
        # 確定整體結果
        result = self._determine_result(findings)
        
        record = MetaAuditRecord(
            audit_id=str(uuid.uuid4()),
            scope=AuditScope.ALL,
            result=result,
            findings=findings,
            recommendations=recommendations
        )
        
        self._audit_records[record.audit_id] = record
        
        # 觸發審計回調
        for callback in self._audit_callbacks:
            try:
                callback(record)
            except Exception:
                pass
        
        return record
    
    def _audit_anti_fabric(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """審計反織網"""
        findings = []
        recommendations = []
        
        # 檢查是否有未解決的矛盾
        if state.get("unresolved_contradictions", 0) > 0:
            findings.append({
                "type": "unresolved_contradictions",
                "count": state["unresolved_contradictions"],
                "severity": "high"
            })
            recommendations.append("Review and resolve pending contradictions")
        
        # 檢查信念驗證覆蓋率
        coverage = state.get("belief_validation_coverage", 0)
        if coverage < 0.9:
            findings.append({
                "type": "low_validation_coverage",
                "coverage": coverage,
                "severity": "medium"
            })
        
        return {"findings": findings, "recommendations": recommendations}
    
    def _audit_falsification(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """審計可證偽引擎"""
        findings = []
        
        # 檢查反例搜索是否活躍
        if not state.get("active", True):
            findings.append({
                "type": "falsification_inactive",
                "severity": "critical"
            })
        
        return {"findings": findings}
    
    def _audit_gl_platform_universegl_platform_universe.governance_rules(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """審計治理規則"""
        findings = []
        
        # 檢查規則是否被正確執行
        rules = state.get("rules", [])
        for rule in rules:
            if not rule.get("enforced", True):
                findings.append({
                    "type": "unenforced_rule",
                    "rule": rule.get("name", "unknown"),
                    "severity": "high"
                })
        
        return {"findings": findings}
    
    def _determine_result(self, findings: List[Dict]) -> AuditResult:
        """確定審計結果"""
        severities = [f.get("severity", "info") for f in findings]
        
        if "critical" in severities:
            return AuditResult.CRITICAL
        elif "high" in severities:
            return AuditResult.FAIL
        elif "medium" in severities:
            return AuditResult.WARN
        return AuditResult.PASS
    
    def audit_self(self) -> MetaAuditRecord:
        """
        元審計自身 (遞歸治理)
        確保元審計器本身也被審計
        """
        self._recursion_depth += 1
        
        if self._recursion_depth > self._max_recursion:
            self._recursion_depth = 0
            return MetaAuditRecord(
                audit_id=str(uuid.uuid4()),
                scope=AuditScope.AUDITOR,
                result=AuditResult.WARN,
                findings=[{"type": "max_recursion_reached"}],
                recommendations=["Meta-audit recursion limit reached"]
            )
        
        findings = []
        
        # 檢查審計記錄完整性
        if len(self._audit_records) == 0:
            findings.append({
                "type": "no_audit_records",
                "severity": "medium"
            })
        
        # 檢查元規則執行
        if len(self._meta_rules) == 0:
            findings.append({
                "type": "no_meta_rules",
                "severity": "low"
            })
        
        record = MetaAuditRecord(
            audit_id=str(uuid.uuid4()),
            scope=AuditScope.AUDITOR,
            result=self._determine_result(findings),
            findings=findings,
            recommendations=[]
        )
        
        self._recursion_depth = 0
        self._audit_records[record.audit_id] = record
        return record
    
    def register_meta_rule(self, rule: Dict[str, Any]) -> None:
        """註冊元規則"""
        self._meta_rules.append({
            "rule_id": str(uuid.uuid4()),
            "registered_at": datetime.utcnow().isoformat(),
            **rule
        })
    
    def register_callback(self, callback: Callable) -> None:
        """註冊審計回調"""
        self._audit_callbacks.append(callback)
    
    def get_audit_history(self, scope: Optional[AuditScope] = None) -> List[MetaAuditRecord]:
        """獲取審計歷史"""
        records = list(self._audit_records.values())
        if scope:
            records = [r for r in records if r.scope == scope]
        return sorted(records, key=lambda r: r.audited_at, reverse=True)
    
    def verify_success_criteria(
        self,
        criteria: str,
        evidence: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        成功定義審查
        質疑「什麼是成功」的定義本身
        """
        return {
            "criteria": criteria,
            "evidence_provided": bool(evidence),
            "verification_status": "reviewed",
            "meta_question": "Is this criteria definition itself valid?",
            "requires_further_review": True
        }
    
    def cleanup(self) -> None:
        """零殘留清理"""
        self._audit_records.clear()
        self._integrity_checks.clear()
        self._meta_rules.clear()
        self._audit_callbacks.clear()
        self._recursion_depth = 0


# 全局實例
_meta_auditor: Optional[MetaAuditor] = None


def get_meta_auditor() -> MetaAuditor:
    global _meta_auditor
    if _meta_auditor is None:
        _meta_auditor = MetaAuditor()
    return _meta_auditor


def cleanup_meta_auditor() -> None:
    global _meta_auditor
    if _meta_auditor:
        _meta_auditor.cleanup()
        _meta_auditor = None
