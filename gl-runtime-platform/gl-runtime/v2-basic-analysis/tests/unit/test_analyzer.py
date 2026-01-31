# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: test
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""V2 Analyzer 單元測試"""
import pytest
from src.core.analyzer import Analyzer

def test_analyzer_init():
    analyzer = Analyzer()
    assert analyzer.analysis_results == []

def test_basic_analysis():
    analyzer = Analyzer()
    result = analyzer.execute({"data": {"key": "value"}, "type": "basic"})
    assert result["status"] == "completed"
