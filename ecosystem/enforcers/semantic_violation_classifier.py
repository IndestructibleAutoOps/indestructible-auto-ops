#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: semantic-governance
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Semantic Violation Classifier Implementation
GL 語意違規分類器實現

Purpose: 自動判斷語意破損，分類違規，防止錯誤結論
Version: 1.0.0
Date: 2026-02-03
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import re
import hashlib
import json
from pathlib import Path

# Import simple_yaml for zero-dependency YAML parsing
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.simple_yaml import safe_load
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ViolationSeverity(Enum):
    """違規嚴重程度"""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ViolationClassification(Enum):
    """違規分類"""

    SEMANTIC_DAMAGE_CRITICAL = "SEMANTIC_DAMAGE_CRITICAL"
    VIOLATION = "VIOLATION"
    EXPECTED_BEHAVIOR = "EXPECTED_BEHAVIOR"


class ViolationAction(Enum):
    """違規處理動作"""

    BLOCK_OPERATION = "BLOCK_OPERATION"
    WARN_ONLY = "WARN_ONLY"
    ALLOW = "ALLOW"


@dataclass
class EvidenceLink:
    """證據鏈接"""

    file_path: str
    line_range: Tuple[int, int]
    checksum: str
    timestamp: str

    def to_dict(self) -> Dict:
        return {
            "file_path": self.file_path,
            "line_range": self.line_range,
            "checksum": self.checksum,
            "timestamp": self.timestamp,
        }


@dataclass
class SemanticViolation:
    """語意違規"""

    violation_type: str
    severity: ViolationSeverity
    classification: ViolationClassification
    action: ViolationAction
    message: str
    evidence_chain: List[EvidenceLink] = field(default_factory=list)
    remediation: List[str] = field(default_factory=list)
    false_positive_threshold: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "violation_type": self.violation_type,
            "severity": self.severity.value,
            "classification": self.classification.value,
            "action": self.action.value,
            "message": self.message,
            "evidence_chain": [e.to_dict() for e in self.evidence_chain],
            "remediation": self.remediation,
            "false_positive_threshold": self.false_positive_threshold,
        }


@dataclass
class GovernanceEvent:
    """治理事件"""

    event_id: str
    timestamp: str
    actor: str
    action: str
    resource: str
    violation_type: str
    classification: str
    severity: str
    evidence_chain: List[Dict]
    remediation_plan: List[str]
    semantic_anchor: str
    hash: str
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    ip: Optional[str] = None
    user_agent: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "action": self.action,
            "resource": self.resource,
            "violation_type": self.violation_type,
            "classification": self.classification,
            "severity": self.severity,
            "evidence_chain": self.evidence_chain,
            "remediation_plan": self.remediation_plan,
            "semantic_anchor": self.semantic_anchor,
            "hash": self.hash,
            "correlation_id": self.correlation_id,
            "request_id": self.request_id,
            "ip": self.ip,
            "user_agent": self.user_agent,
        }


class GLSemanticViolationClassifier:
    """GL 語意違規分類器"""

    def __init__(self, contract_path: Path, base_path: Path):
        """初始化分類器

        Args:
            contract_path: 分類器契約路徑
            base_path: 項目根路徑
        """
        self.contract_path = contract_path
        self.base_path = base_path

        # 加載契約
        self.contract = self._load_contract()

        # 語意錨點
        self.semantic_anchor = "SEMANTICVIOLATIONCLASSIFIER"

    def _load_contract(self) -> Dict:
        """加載分類器契約"""
        if not self.contract_path.exists():
            raise FileNotFoundError(f"Contract not found: {self.contract_path}")

        with open(self.contract_path, "r", encoding="utf-8") as f:
            return safe_load(f)

    def _calculate_checksum(self, content: bytes) -> str:
        """計算 SHA-256 校驗和"""
        return hashlib.sha256(content).hexdigest()

    def _get_timestamp(self) -> str:
        """獲取 RFC3339 UTC 時間戳"""
        return datetime.now(timezone.utc).isoformat()

    def _parse_evidence_link(self, link: str) -> Optional[EvidenceLink]:
        """解析證據鏈接格式: [證據: path/to/file#L10-L15]"""
        match = re.match(r"\[證據:\s*(.+?)#L(\d+)-L(\d+)\]", link)
        if not match:
            return None

        file_path = match.group(1)
        start_line = int(match.group(2))
        end_line = int(match.group(3))

        full_path = self.base_path / file_path
        if not full_path.exists():
            return None

        # 計算校驗和
        with open(full_path, "rb") as f:
            checksum = self._calculate_checksum(f.read())

        return EvidenceLink(
            file_path=str(full_path),
            line_range=(start_line, end_line),
            checksum=checksum,
            timestamp=self._get_timestamp(),
        )

    def _validate_evidence_chain(
        self, evidence_links: List[str]
    ) -> Tuple[List[EvidenceLink], List[str]]:
        """驗證證據鏈

        Returns:
            (valid_evidences, errors)
        """
        valid_evidences = []
        errors = []

        for link in evidence_links:
            evidence = self._parse_evidence_link(link)
            if evidence:
                valid_evidences.append(evidence)
            else:
                errors.append(f"無效證據鏈接: {link}")

        return valid_evidences, errors

    def _check_evidence_integrity(self, operation: Dict) -> List[SemanticViolation]:
        """檢查證據鏈完整性"""
        violations = []

        evidence_links = operation.get("evidence_links", [])
        contract = operation.get("contract", {})
        requires_evidence = contract.get("requires_evidence", True)

        # 規則: EVIDENCE_MISSING
        if requires_evidence and len(evidence_links) == 0:
            violations.append(
                SemanticViolation(
                    violation_type="EVIDENCE_MISSING",
                    severity=ViolationSeverity.CRITICAL,
                    classification=ViolationClassification.SEMANTIC_DAMAGE_CRITICAL,
                    action=ViolationAction.BLOCK_OPERATION,
                    message="CRITICAL: 語意破損 - 缺少必需證據鏈",
                    false_positive_threshold=0.0,
                    remediation=[
                        "Add evidence links using format [證據: path/to/file#L10-L15]",
                        "Verify evidence sources exist",
                        "Ensure SHA-256 checksums are provided",
                    ],
                )
            )

        # 規則: EVIDENCE_COVERAGE_INSUFFICIENT
        # 上下文感知: 測試環境容錯
        environment = operation.get("environment", "production")
        is_test = operation.get("type") == "validation_test"

        if environment == "production":
            threshold = 0.95
        elif environment == "staging":
            threshold = 0.90
        else:  # test
            threshold = 0.70

        # 計算證據覆蓋率（簡化實現）
        total_statements = len(operation.get("content", "").split("."))
        # 避免除零
        total_statements = max(total_statements, 1)
        # 證據鏈接數作為覆蓋率基礎
        statements_with_evidence = len(evidence_links)

        # 更合理的覆蓋率計算：
        # - 如果證據鏈接數 < 閾值的絕對數，則視為覆蓋率不足
        # - 否則使用證據鏈接數 / 語句數
        min_evidence_for_prod = 5  # 生產環境至少需要 5 個證據
        min_evidence_for_staging = 3  # 測試環境至少需要 3 個證擋
        min_evidence_for_test = 1  # 測試環境至少需要 1 個證據

        if environment == "production":
            min_required = min_evidence_for_prod
            coverage = statements_with_evidence / max(min_required, total_statements)
        elif environment == "staging":
            min_required = min_evidence_for_staging
            coverage = statements_with_evidence / max(min_required, total_statements)
        else:  # test
            min_required = min_evidence_for_test
            coverage = statements_with_evidence / max(min_required, total_statements)

        if coverage < threshold and not is_test:
            violations.append(
                SemanticViolation(
                    violation_type="EVIDENCE_COVERAGE_INSUFFICIENT",
                    severity=ViolationSeverity.HIGH,
                    classification=ViolationClassification.VIOLATION,
                    action=ViolationAction.BLOCK_OPERATION,
                    message=f"HIGH: 證據覆蓋率不足 ({coverage:.1%} < {threshold:.1%})",
                    false_positive_threshold=0.0,
                    remediation=[
                        "Add evidence links to statements",
                        f"Increase coverage to >={threshold:.0%}",
                        "Validate all claims with evidence",
                    ],
                )
            )
        elif coverage < threshold and is_test:
            # 測試環境: 警告級別
            violations.append(
                SemanticViolation(
                    violation_type="EVIDENCE_COVERAGE_INSUFFICIENT",
                    severity=ViolationSeverity.LOW,
                    classification=ViolationClassification.EXPECTED_BEHAVIOR,
                    action=ViolationAction.WARN_ONLY,
                    message=f"INFO: 測試配置低覆蓋率是預期行為（{coverage:.1%} < {threshold:.1%}）",
                    false_positive_threshold=1.0,
                    remediation=[
                        f"For production, increase coverage to >={threshold:.0%}"
                    ],
                )
            )

        # 驗證證據有效性
        valid_evidences, errors = self._validate_evidence_chain(evidence_links)
        if errors and not is_test:
            violations.append(
                SemanticViolation(
                    violation_type="EVIDENCE_INVALID",
                    severity=ViolationSeverity.CRITICAL,
                    classification=ViolationClassification.SEMANTIC_DAMAGE_CRITICAL,
                    action=ViolationAction.BLOCK_OPERATION,
                    message=f"CRITICAL: 證據無效 - {', '.join(errors)}",
                    false_positive_threshold=0.0,
                    remediation=[
                        "Verify file paths exist",
                        "Recalculate SHA-256 checksums",
                        "Validate timestamps in RFC3339 format",
                    ],
                )
            )

        return violations

    def _check_contract_completeness(self, operation: Dict) -> List[SemanticViolation]:
        """檢查契約完整性"""
        violations = []

        # 規則: METHOD_MISSING
        contract = operation.get("contract", {})
        implementation = operation.get("implementation", {})

        required_methods = contract.get("required_methods", [])
        implemented_methods = implementation.get("methods", [])

        missing_methods = set(required_methods) - set(implemented_methods)

        if missing_methods:
            violations.append(
                SemanticViolation(
                    violation_type="METHOD_MISSING",
                    severity=ViolationSeverity.CRITICAL,
                    classification=ViolationClassification.SEMANTIC_DAMAGE_CRITICAL,
                    action=ViolationAction.BLOCK_OPERATION,
                    message=f"CRITICAL: 語意破損 - 契約方法缺失: {', '.join(missing_methods)}",
                    false_positive_threshold=0.0,
                    remediation=[
                        "Implement all required methods",
                        "Verify method signatures match contract",
                        "Add unit tests for missing methods",
                    ],
                )
            )

        return violations

    def _check_artifact_completeness(self, operation: Dict) -> List[SemanticViolation]:
        """檢查 Artifact 完整性"""
        violations = []

        # 規則: PHASE_INCOMPLETE
        phases = operation.get("phases", [])
        for phase in phases:
            if phase.get("required", False) and phase.get("status") != "completed":
                deadline = phase.get("deadline", "")
                if deadline and datetime.now(timezone.utc) > datetime.fromisoformat(
                    deadline
                ):
                    violations.append(
                        SemanticViolation(
                            violation_type="PHASE_INCOMPLETE",
                            severity=ViolationSeverity.CRITICAL,
                            classification=ViolationClassification.SEMANTIC_DAMAGE_CRITICAL,
                            action=ViolationAction.BLOCK_OPERATION,
                            message=f"CRITICAL: 語意破損 - 必需階段未完成: {phase.get('name', 'unknown')}",
                            false_positive_threshold=0.0,
                            remediation=[
                                "Complete all phase tasks",
                                "Update milestone status",
                                "Generate completion evidence",
                            ],
                        )
                    )

        return violations

    def classify_violations(self, operation: Dict) -> List[SemanticViolation]:
        """分類所有違規

        Args:
            operation: 操作字典

        Returns:
            違規列表
        """
        all_violations = []

        # 檢查各個維度
        all_violations.extend(self._check_evidence_integrity(operation))
        all_violations.extend(self._check_contract_completeness(operation))
        all_violations.extend(self._check_artifact_completeness(operation))

        return all_violations

    def should_block_operation(self, violations: List[SemanticViolation]) -> bool:
        """判斷是否應該阻塞操作

        Args:
            violations: 違規列表

        Returns:
            True if should block, False otherwise
        """
        return any(v.action == ViolationAction.BLOCK_OPERATION for v in violations)

    def generate_governance_event(
        self, violation: SemanticViolation, actor: str, action: str, resource: str
    ) -> GovernanceEvent:
        """生成治理事件

        Args:
            violation: 違規
            actor: 執行者
            action: 動作
            resource: 資源

        Returns:
            治理事件
        """
        event_id = f"evt_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        timestamp = self._get_timestamp()

        # 計算事件 hash
        event_payload = {
            "event_id": event_id,
            "timestamp": timestamp,
            "violation_type": violation.violation_type,
            "classification": violation.classification.value,
            "severity": violation.severity.value,
        }
        event_hash = self._calculate_checksum(
            json.dumps(event_payload, sort_keys=True).encode()
        )

        return GovernanceEvent(
            event_id=event_id,
            timestamp=timestamp,
            actor=actor,
            action=action,
            resource=resource,
            violation_type=violation.violation_type,
            classification=violation.classification.value,
            severity=violation.severity.value,
            evidence_chain=[e.to_dict() for e in violation.evidence_chain],
            remediation_plan=violation.remediation,
            semantic_anchor=self.semantic_anchor,
            hash=event_hash,
        )

    def generate_remediation_plan(self, violations: List[SemanticViolation]) -> Dict:
        """生成修復計劃

        Args:
            violations: 違規列表

        Returns:
            修復計劃字典
        """
        plan = {
            "timestamp": self._get_timestamp(),
            "total_violations": len(violations),
            "blocking_violations": sum(
                1 for v in violations if v.action == ViolationAction.BLOCK_OPERATION
            ),
            "remediations_by_severity": {
                "CRITICAL": [],
                "HIGH": [],
                "MEDIUM": [],
                "LOW": [],
            },
        }

        for violation in violations:
            severity = violation.severity.value
            plan["remediations_by_severity"][severity].extend(violation.remediation)

        return plan

    def analyze(self, operation: Dict) -> Dict:
        """分析操作，檢測並分類違規

        Args:
            operation: 操作字典

        Returns:
            分析結果字典
        """
        # 分類違規
        violations = self.classify_violations(operation)

        # 判斷是否阻塞
        should_block = self.should_block_operation(violations)

        # 生成修復計劃
        remediation_plan = self.generate_remediation_plan(violations)

        return {
            "timestamp": self._get_timestamp(),
            "semantic_anchor": self.semantic_anchor,
            "violations": [v.to_dict() for v in violations],
            "should_block": should_block,
            "remediation_plan": remediation_plan,
            "analysis_metadata": {
                "total_violations": len(violations),
                "blocking_violations": sum(
                    1 for v in violations if v.action == ViolationAction.BLOCK_OPERATION
                ),
                "warnings": sum(
                    1 for v in violations if v.action == ViolationAction.WARN_ONLY
                ),
            },
        }


# ============================================================================
# 測試和使用示例
# ============================================================================
if __name__ == "__main__":
    # 創建分類器
    contract_path = Path(
        "/workspace/machine-native-ops/ecosystem/contracts/governance/gl-semantic-violation-classifier.yaml"
    )
    base_path = Path("/workspace/machine-native-ops")

    classifier = GLSemanticViolationClassifier(contract_path, base_path)

    # 測試案例 1: 缺少證據鏈 (CRITICAL)
    print("=" * 70)
    print("測試案例 1: 缺少證據鏈")
    print("=" * 70)

    operation_without_evidence = {
        "type": "validation_test",
        "files": ["ecosystem/enforce.py"],
        "content": "test content for validation",
        "contract": {"requires_evidence": True},
        "environment": "production",
    }

    result1 = classifier.analyze(operation_without_evidence)
    print(f"應該阻塞: {result1['should_block']}")
    print(f"違規數量: {result1['analysis_metadata']['total_violations']}")
    for violation in result1["violations"]:
        print(f"  - {violation['violation_type']}: {violation['message']}")

    # 測試案例 2: 測試環境低覆蓋率 (預期行為)
    print("\n" + "=" * 70)
    print("測試案例 2: 測試環境低覆蓋率")
    print("=" * 70)

    operation_test_low_coverage = {
        "type": "validation_test",
        "files": ["ecosystem/enforce.py"],
        "content": "test content for validation",
        "evidence_links": [
            "[證據: ecosystem/enforce.py#L1-L100]",
            "[證據: ecosystem/enforcers/governance_enforcer.py#L1-L100]",
        ],
        "contract": {"requires_evidence": True},
        "environment": "test",
    }

    result2 = classifier.analyze(operation_test_low_coverage)
    print(f"應該阻塞: {result2['should_block']}")
    print(f"違規數量: {result2['analysis_metadata']['total_violations']}")
    print(f"警告數量: {result2['analysis_metadata']['warnings']}")
    for violation in result2["violations"]:
        print(f"  - {violation['violation_type']}: {violation['classification']}")

    # 測試案例 3: 生產環境低覆蓋率 (違規)
    print("\n" + "=" * 70)
    print("測試案例 3: 生產環境低覆蓋率")
    print("=" * 70)

    operation_prod_low_coverage = {
        "type": "deployment",
        "files": ["ecosystem/enforce.py"],
        "content": "test content for validation",
        "evidence_links": [
            "[證據: ecosystem/enforce.py#L1-L100]",
            "[證據: ecosystem/enforcers/governance_enforcer.py#L1-L100]",
        ],
        "contract": {"requires_evidence": True},
        "environment": "production",
    }

    result3 = classifier.analyze(operation_prod_low_coverage)
    print(f"應該阻塞: {result3['should_block']}")
    print(f"違規數量: {result3['analysis_metadata']['total_violations']}")
    for violation in result3["violations"]:
        print(f"  - {violation['violation_type']}: {violation['message']}")

    # 測試案例 4: 缺少契約方法 (CRITICAL)
    print("\n" + "=" * 70)
    print("測試案例 4: 缺少契約方法")
    print("=" * 70)

    operation_missing_method = {
        "type": "validation_test",
        "contract": {"required_methods": ["validate", "audit", "check"]},
        "implementation": {"methods": ["validate", "audit"]},  # 缺少 check
        "environment": "production",
    }

    result4 = classifier.analyze(operation_missing_method)
    print(f"應該阻塞: {result4['should_block']}")
    print(f"違規數量: {result4['analysis_metadata']['total_violations']}")
    for violation in result4["violations"]:
        print(f"  - {violation['violation_type']}: {violation['message']}")

    print("\n" + "=" * 70)
    print("所有測試完成")
    print("=" * 70)
