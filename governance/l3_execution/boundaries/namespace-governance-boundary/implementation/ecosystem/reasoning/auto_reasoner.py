#!/usr/bin/env python3
"""
MNGA Automatic Reasoning Engine
自動推理引擎 - 基於驗證結果進行推理和最佳實踐建議
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class ReasoningResult:
    """推理結果"""

    inference_type: str
    confidence: float  # 0.0 to 1.0
    conclusion: str
    evidence: List[str]
    recommendations: List[str]
    priority: str  # HIGH, MEDIUM, LOW
    timestamp: str


class AutoReasoner:
    """自動推理引擎"""

    def __init__(self):
        self.reasoning_rules = self._initialize_rules()

    def _initialize_rules(self) -> Dict:
        """初始化推理規則"""
        return {
            "governance_rules": [
                {
                    "rule_id": "GR001",
                    "name": "Evidence Coverage Rule",
                    "description": "如果 evidence coverage < 90%，需要補充證據鏈",
                    "condition": "evidence_coverage < 0.90",
                    "inference": "證據覆蓋率不足，違反 GL 統一框架要求",
                    "priority": "HIGH",
                    "action": "添加 [證據: path/to/file#L10-L15] 格式的證據鏈",
                },
                {
                    "rule_id": "GR002",
                    "name": "GL Semantic Anchor Rule",
                    "description": "如果缺少 GL 語義錨點，無法進行語意驗證",
                    "condition": "semantic_anchor_missing == true",
                    "inference": "缺少 GL 語義錨點，影響跨模組語意一致性",
                    "priority": "CRITICAL",
                    "action": "在文件頭部添加 @GL-semantic: tag 和 @GL-audit-trail 註解",
                },
                {
                    "rule_id": "GR003",
                    "name": "Boundary Violation Rule",
                    "description": "如果發現邊界違規，需要重新架構",
                    "condition": "boundary_violations > 0",
                    "inference": "檢測到 GL 邊界違規，違反 GL 統一框架 E0-003 規則",
                    "priority": "HIGH",
                    "action": "根據 boundary-reference-matrix.md 重新組織代碼結構",
                },
            ],
            "network_rules": [
                {
                    "rule_id": "NR001",
                    "name": "External Connectivity Rule",
                    "description": "如果外網連接失敗，無法進行 GitHub 操作",
                    "condition": "external_connectivity == FAIL",
                    "inference": "外網連接失敗，無法進行 GitHub push/pull 操作",
                    "priority": "HIGH",
                    "action": "檢查網絡連接、代理設置和防火牆配置",
                },
                {
                    "rule_id": "NR002",
                    "name": "Latency Threshold Rule",
                    "description": "如果平均延遲 > 1000ms，影響用戶體驗",
                    "condition": "avg_latency_ms > 1000",
                    "inference": "網絡延遲過高，可能影響 API 調用性能",
                    "priority": "MEDIUM",
                    "action": "優化網絡路由或使用 CDN 加速",
                },
            ],
            "security_rules": [
                {
                    "rule_id": "SR001",
                    "name": "Token Exposure Rule",
                    "description": "如果檢測到 token 洩露，立即警告",
                    "condition": "token_detected == true",
                    "inference": "檢測到敏感 token 可能洩露，存在安全風險",
                    "priority": "CRITICAL",
                    "action": "立即撤銷 token，並檢查訪問日誌",
                },
                {
                    "rule_id": "SR002",
                    "name": "Permission Rule",
                    "description": "如果權限不足，無法執行某些操作",
                    "condition": "permission_denied == true",
                    "inference": "權限不足，無法完成請求的操作",
                    "priority": "MEDIUM",
                    "action": "聯繫管理員獲取適當的權限",
                },
            ],
        }

    def evaluate_condition(self, condition: str, context: Dict) -> bool:
        """評估條件是否成立"""
        try:
            # 簡單的條件評估器
            if ">" in condition:
                var, value = condition.split(">")
                var = var.strip()
                value = float(value.strip())
                return context.get(var, 0) > value
            elif "<" in condition:
                var, value = condition.split("<")
                var = var.strip()
                value = float(value.strip())
                return context.get(var, 0) < value
            elif "==" in condition:
                var, value = condition.split("==")
                var = var.strip()
                value = value.strip().strip("\"'")
                return str(context.get(var, "")) == value
            else:
                return context.get(condition, False)
        except Exception as e:
            print(f"Condition evaluation error: {e}")
            return False

    def reason_about_governance(self, audit_report: Dict) -> List[ReasoningResult]:
        """對治理報告進行推理"""
        results = []

        context = {
            "evidence_coverage": audit_report.get("metadata", {}).get(
                "evidence_coverage", 1.0
            ),
            "boundary_violations": len(audit_report.get("violations", [])),
            "semantic_anchor_missing": any(
                "GL-semantic" not in v.get("file", "")
                for v in audit_report.get("violations", [])
            ),
        }

        for rule in self.reasoning_rules["governance_rules"]:
            if self.evaluate_condition(rule["condition"], context):
                results.append(
                    ReasoningResult(
                        inference_type="GOVERNANCE",
                        confidence=0.9,
                        conclusion=rule["inference"],
                        evidence=[
                            f"Condition met: {rule['condition']}",
                            f"Rule: {rule['name']}",
                        ],
                        recommendations=[rule["action"]],
                        priority=rule["priority"],
                        timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    )
                )

        return results

    def reason_about_network(self, network_report: Dict) -> List[ReasoningResult]:
        """對網絡報告進行推理"""
        results = []

        test_summary = network_report.get("test_summary", {})
        tests = network_report.get("tests", [])

        context = {
            "external_connectivity": (
                "PASS"
                if any(
                    t["status"] == "PASS" and t["test_type"] == "EXTERNAL"
                    for t in tests
                )
                else "FAIL"
            ),
            "avg_latency_ms": float(test_summary.get("average_latency_ms", 0)),
        }

        for rule in self.reasoning_rules["network_rules"]:
            if self.evaluate_condition(rule["condition"], context):
                results.append(
                    ReasoningResult(
                        inference_type="NETWORK",
                        confidence=0.85,
                        conclusion=rule["inference"],
                        evidence=[
                            f"External connectivity: {context['external_connectivity']}",
                            f"Average latency: {context['avg_latency_ms']:.2f}ms",
                        ],
                        recommendations=[rule["action"]],
                        priority=rule["priority"],
                        timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    )
                )

        return results

    def reason_about_security(
        self, security_scan: Optional[Dict] = None
    ) -> List[ReasoningResult]:
        """對安全掃描結果進行推理"""
        results = []

        context = {"token_detected": False, "permission_denied": False}

        if security_scan:
            context.update(security_scan)

        for rule in self.reasoning_rules["security_rules"]:
            if self.evaluate_condition(rule["condition"], context):
                results.append(
                    ReasoningResult(
                        inference_type="SECURITY",
                        confidence=0.95,
                        conclusion=rule["inference"],
                        evidence=[f"Condition met: {rule['condition']}"],
                        recommendations=[rule["action"]],
                        priority=rule["priority"],
                        timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    )
                )

        return results

    def combine_reasoning(
        self,
        governance_results: List[ReasoningResult],
        network_results: List[ReasoningResult],
        security_results: List[ReasoningResult],
    ) -> Dict:
        """合併推理結果"""
        all_results = governance_results + network_results + security_results

        # 按優先級排序
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        all_results.sort(key=lambda x: priority_order.get(x.priority, 99))

        # 統計
        critical_count = sum(1 for r in all_results if r.priority == "CRITICAL")
        high_count = sum(1 for r in all_results if r.priority == "HIGH")
        medium_count = sum(1 for r in all_results if r.priority == "MEDIUM")
        low_count = sum(1 for r in all_results if r.priority == "LOW")

        return {
            "summary": {
                "total_inferences": len(all_results),
                "critical": critical_count,
                "high": high_count,
                "medium": medium_count,
                "low": low_count,
                "overall_health": (
                    "HEALTHY"
                    if critical_count == 0 and high_count == 0
                    else "ATTENTION_NEEDED"
                ),
            },
            "reasoning_results": [
                {
                    "type": r.inference_type,
                    "confidence": f"{r.confidence:.2f}",
                    "conclusion": r.conclusion,
                    "evidence": r.evidence,
                    "recommendations": r.recommendations,
                    "priority": r.priority,
                    "timestamp": r.timestamp,
                }
                for r in all_results
            ],
            "best_practices": self._generate_best_practices(all_results),
        }

    def _generate_best_practices(self, results: List[ReasoningResult]) -> List[str]:
        """生成最佳實踐建議"""
        practices = [
            "✅ 始終在代碼中保持證據鏈覆蓋率 >= 90%",
            "✅ 所有治理文件必須包含 GL 語義錨點",
            "✅ 定期運行邊界檢查以確保架構一致性",
            "✅ 在部署前驗證內網和外網連接性",
            "✅ 監控網絡延遲並優化 API 性能",
            "✅ 實施 CI/CD 管道自動化治理檢查",
        ]

        # 根據推理結果添加特定建議
        if any(r.inference_type == "NETWORK" for r in results):
            practices.append("⚠️ 考慮實施網絡故障轉移機制")

        if any(r.inference_type == "SECURITY" for r in results):
            practices.append("⚠️ 定期進行安全掃描和權限審計")

        return practices


if __name__ == "__main__":
    # 測試推理引擎
    reasoner = AutoReasoner()

    # 模擬治理報告
    mock_audit_report = {
        "metadata": {"evidence_coverage": 0.85},
        "violations": [{"file": "test.py", "rule_id": "GR001"}],
    }

    # 模擬網絡報告
    mock_network_report = {"test_summary": {"average_latency_ms": 1500}, "tests": []}

    # 執行推理
    governance_results = reasoner.reason_about_governance(mock_audit_report)
    network_results = reasoner.reason_about_network(mock_network_report)
    security_results = reasoner.reason_about_security()

    # 合併結果
    combined = reasoner.combine_reasoning(
        governance_results, network_results, security_results
    )

    print(json.dumps(combined, indent=2, ensure_ascii=False))
