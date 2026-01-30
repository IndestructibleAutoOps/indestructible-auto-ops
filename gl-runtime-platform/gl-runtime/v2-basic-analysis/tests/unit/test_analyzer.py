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
