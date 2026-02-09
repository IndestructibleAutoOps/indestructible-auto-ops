"""
Pipeline Integration - GL治理執行層與事實驗證管道的集成

負責將 gl-fact-pipeline.py 集成到治理執行層，提供：
1. 標準化的管道執行接口
2. 與 GovernanceEnforcer 的無縫集成
3. 證據收集和驗證的自動化
4. 報告生成和驗證

@GL-governed
"""
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: pipeline-integration

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

# Import simple_yaml for zero-dependency YAML parsing
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.simple_yaml import safe_load
from datetime import datetime

# 添加事實驗證工具的路徑
fact_verification_path = Path(__file__).parent.parent / "tools" / "fact-verification"
sys.path.insert(0, str(fact_verification_path))

try:
    from gov_fact_pipeline import (
        GLFactPipeline,
        ValidationResult,
        InternalSource,
        ExternalReference,
        DifferenceCategory,
    )
except ImportError as e:
    print(f"警告: 無法導入 gov_fact_pipeline: {e}")
    print("將使用模擬實現")

    # 模擬類（用於測試）
    class ValidationResult:
        def __init__(self, passed: bool, errors: List[str], warnings: List[str]):
            self.passed = passed
            self.errors = errors
            self.warnings = warnings

    class DifferenceCategory:
        ALIGNED = "aligned"
        INTENTIONAL_DEVIATION = "intentional-deviation"
        TECHNICAL_DEBT = "technical-debt"
        GAP = "gap"
        EXTENSION = "extension"


class PipelineIntegration:
    """GL事實驗證管道集成器"""

    def __init__(self, config_path: Optional[str] = None, workspace_path: str = "."):
        """
        初始化管道集成器

        Args:
            config_path: 管道配置文件路徑
            workspace_path: 工作區路徑
        """
        # 默認配置路徑
        if config_path is None:
            config_path = (
                "ecosystem/contracts/naming-governance/gl.fact-pipeline-spec.yaml"
            )

        self.config_path = Path(config_path)
        self.workspace_path = Path(workspace_path)

        # 初始化事實驗證管道
        try:
            self.pipeline = GLFactPipeline(
                config_path=str(self.config_path),
                workspace_path=str(self.workspace_path),
            )
            self.pipeline_available = True
        except Exception as e:
            print(f"無法初始化 GLFactPipeline: {e}")
            self.pipeline = None
            self.pipeline_available = False

        # 輸出目錄
        self.output_dir = (
            self.workspace_path / "ecosystem" / "outputs" / "fact-verification"
        )
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def check(self) -> Dict[str, Any]:
        """
        基礎健康檢查，確保管道可用性與關鍵路徑完整。

        Returns:
            Dict with passed/issues/warnings/details.
        """
        issues: List[str] = []
        warnings: List[str] = []

        config_exists = self.config_path.exists()
        output_writable = os.access(self.output_dir, os.W_OK)

        if not config_exists:
            issues.append(f"Config not found: {self.config_path}")

        if not self.pipeline_available:
            warnings.append("GLFactPipeline unavailable; fallback to mock mode")

        if not output_writable:
            issues.append(f"Output directory not writable: {self.output_dir}")

        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "details": {
                "config_path": str(self.config_path),
                "config_exists": config_exists,
                "pipeline_available": self.pipeline_available,
                "output_dir": str(self.output_dir),
                "output_writable": output_writable,
            },
        }

    def run_verification(
        self, topics: List[str], operation_context: Optional[Dict] = None
    ) -> Dict:
        """
        執行事實驗證

        Args:
            topics: 驗證主題列表（如 ['semver', 'cncf']）
            operation_context: 操作上下文信息

        Returns:
            驗證報告
        """
        if not self.pipeline_available:
            return self._generate_mock_report(topics, operation_context)

        try:
            # 執行管道
            report = self.pipeline.run_pipeline(topics)

            # 添加操作上下文
            if operation_context:
                report["operation_context"] = operation_context

            # 保存報告
            report_path = self._save_report(report, operation_context)

            return {"status": "SUCCESS", "report": report, "report_path": report_path}
        except Exception as e:
            return {"status": "ERROR", "error": str(e), "report": None}

    def collect_evidence(self, sources: List[Dict], operation_id: str) -> List[Dict]:
        """
        收集證據

        Args:
            sources: 證據源列表 [{'type': 'contract', 'path': 'path/to/contract.yaml'}]
            operation_id: 操作ID

        Returns:
            證據鏈列表
        """
        evidence_chain = []

        for source in sources:
            try:
                source_type = source.get("type")
                source_path = source.get("path")

                # 計算文件哈希
                if Path(source_path).exists():
                    import hashlib

                    with open(source_path, "rb") as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()

                    evidence = {
                        "type": source_type,
                        "path": source_path,
                        "hash": file_hash,
                        "size": Path(source_path).stat().st_size,
                        "timestamp": datetime.now().isoformat(),
                        "operation_id": operation_id,
                    }

                    evidence_chain.append(evidence)
            except Exception as e:
                print(f"收集證據失敗 {source_path}: {e}")

        return evidence_chain

    def validate_report(
        self, report: Dict, min_evidence_coverage: float = 0.90
    ) -> Dict:
        """
        驗證報告質量

        Args:
            report: 要驗證的報告
            min_evidence_coverage: 最小證據覆蓋率閾值

        Returns:
            驗證結果
        """
        validation = {
            "has_unverified_claims": False,
            "evidence_coverage": 0.0,
            "forbidden_phrase_violations": [],
            "passed": True,
            "errors": [],
            "warnings": [],
        }

        # 檢查證據覆蓋率
        report_text = json.dumps(report, ensure_ascii=False)

        # 計算證據鏈接
        import re

        evidence_pattern = r"\[證據:\s*[^\]]+\]"
        evidence_links = re.findall(evidence_pattern, report_text)

        # 計算聲明句數
        statement_pattern = r"[^.!?。？！]+[.!?。？！]"
        statements = re.findall(statement_pattern, report_text)
        total_statements = len(statements)

        if total_statements > 0:
            validation["evidence_coverage"] = len(evidence_links) / total_statements

        # 檢查覆蓋率閾值
        if validation["evidence_coverage"] < min_evidence_coverage:
            validation["has_unverified_claims"] = True
            validation["passed"] = False
            validation["errors"].append(
                f"證據覆蓋率不足: {validation['evidence_coverage']:.1%} < {min_evidence_coverage:.1%}"
            )

        # 檢查禁止短語
        forbidden_phrases = [
            ("100% 完成", "基於已實現的功能集"),
            ("完全符合", "在[方面]與標準對齊"),
            ("已全部實現", "已實現[具體功能列表]"),
            ("應該是", "根據[證據]，建議"),
            ("可能是", "基於[證據]，推測"),
            ("我認為", "基於[證據]，分析表明"),
        ]

        for phrase, replacement in forbidden_phrases:
            if phrase in report_text:
                validation["forbidden_phrase_violations"].append(
                    {"phrase": phrase, "replacement": replacement, "severity": "HIGH"}
                )

        if validation["forbidden_phrase_violations"]:
            validation["passed"] = False
            validation["warnings"].append(
                f"發現 {len(validation['forbidden_phrase_violations'])} 個禁止短語"
            )

        return validation

    def _save_report(self, report: Dict, context: Optional[Dict] = None) -> str:
        """
        保存報告

        Args:
            report: 報告內容
            context: 上下文信息

        Returns:
            保存的文件路徑
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if context and "operation_id" in context:
            filename = f"{context['operation_id']}_report_{timestamp}.json"
        else:
            filename = f"report_{timestamp}.json"

        report_path = self.output_dir / filename

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return str(report_path)

    def _generate_mock_report(
        self, topics: List[str], context: Optional[Dict] = None
    ) -> Dict:
        """
        生成模擬報告（當管道不可用時）

        Args:
            topics: 主題列表
            context: 上下文信息

        Returns:
            模擬報告
        """
        return {
            "status": "MOCK",
            "report": {
                "verification_id": f"mock-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "topics": topics,
                "internal_facts": {"status": "collected", "sources": []},
                "external_context": {"status": "collected", "references": []},
                "differences": [],
                "summary": {
                    "total_sources": 0,
                    "aligned": 0,
                    "deviations": 0,
                    "gaps": 0,
                    "extensions": 0,
                },
                "note": "This is a mock report because GLFactPipeline is not available",
            },
            "report_path": None,
        }


def main():
    """測試Pipeline Integration"""
    print("=== Pipeline Integration 測試 ===\n")

    # 創建集成器
    integration = PipelineIntegration()

    print(f"管道可用性: {integration.pipeline_available}\n")

    # 測試執行驗證
    print("1. 測試執行驗證")
    result = integration.run_verification(
        topics=["semver", "naming"],
        operation_context={
            "operation_id": "test-001",
            "operation_type": "file_migration",
        },
    )

    print(f"   狀態: {result['status']}")
    if result["status"] == "SUCCESS":
        report = result["report"]
        print(f"   驗證ID: {report.get('verification_id', 'N/A')}")
        print(f"   主題: {report.get('topics', [])}")
        summary = report.get("summary", {})
        print(
            f"   對齊: {summary.get('aligned', 0)}, 偏差: {summary.get('deviations', 0)}"
        )
        if result.get("report_path"):
            print(f"   報告已保存: {result['report_path']}")
    print()

    # 測試收集證據
    print("2. 測試收集證據")
    sources = [
        {
            "type": "contract",
            "path": "ecosystem/contracts/naming-governance/gl-platforms.yaml",
        },
        {
            "type": "registry",
            "path": "ecosystem/registry/platforms/gl-platform-registry.yaml",
        },
    ]
    evidence = integration.collect_evidence(sources, "test-001")
    print(f"   收集到 {len(evidence)} 個證據")
    for ev in evidence:
        print(f"   - {ev['type']}: {ev['path'][:50]}... (SHA256: {ev['hash'][:16]}...)")
    print()

    # 測試驗證報告
    print("3. 測試驗證報告")
    test_report = {
        "content": "根據GL治理合約[證據: ecosystem/contracts/platforms/gl-platforms.yaml]，該操作符合規範。",
        "additional_info": "文件[證據: gl-platforms.yaml#L10-L20]也確認了這一點。",
    }
    validation = integration.validate_report(test_report)
    print(f"   通過: {validation['passed']}")
    print(f"   證據覆蓋率: {validation['evidence_coverage']:.1%}")
    print(f"   未驗證聲明: {validation['has_unverified_claims']}")
    print(f"   禁止短語違規: {len(validation['forbidden_phrase_violations'])}")
    print()

    print("=== Pipeline Integration 測試完成 ===")


if __name__ == "__main__":
    main()
