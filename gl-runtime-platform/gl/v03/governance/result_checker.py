# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: gl_platform_universegl_platform_universe.governance-core
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL90_99-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""
GL Runtime V3 - 結果檢查器
成功/失敗判定模組
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class ResultStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    UNKNOWN = "unknown"


@dataclass
class CheckResult:
    status: ResultStatus
    score: float
    message: str
    details: Dict[str, Any]


class ResultChecker:
    """結果判定檢查器"""
    
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
    
    def check(self, expected: Any, actual: Any) -> CheckResult:
        """檢查執行結果"""
        if expected == actual:
            return CheckResult(
                status=ResultStatus.SUCCESS,
                score=1.0,
                message="完全匹配",
                details={"expected": expected, "actual": actual}
            )
        
        similarity = self._calculate_similarity(expected, actual)
        if similarity >= self.threshold:
            return CheckResult(
                status=ResultStatus.PARTIAL,
                score=similarity,
                message="部分匹配",
                details={"expected": expected, "actual": actual, "similarity": similarity}
            )
        
        return CheckResult(
            status=ResultStatus.FAILURE,
            score=similarity,
            message="不匹配",
            details={"expected": expected, "actual": actual}
        )
    
    def _calculate_similarity(self, a: Any, b: Any) -> float:
        """計算相似度"""
        if type(a) != type(b):
            return 0.0
        if isinstance(a, str):
            return len(set(a) & set(b)) / max(len(set(a) | set(b)), 1)
        return 0.0
