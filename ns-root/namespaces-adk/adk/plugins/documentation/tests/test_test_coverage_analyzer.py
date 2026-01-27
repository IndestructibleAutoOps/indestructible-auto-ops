"""
Unit Tests for Test Coverage Analyzer
======================================

Tests for the enterprise-grade test coverage analysis system.
"""

import tempfile
from pathlib import Path

import pytest

from test_coverage_analyzer import (
    TestCoverageAnalyzer,
    CoverageMetrics,
    CoverageReport,
    CoverageReportFormat,
    analyze_test_coverage
)


@pytest.fixture
def temp_coverage_dir():
    """Create temporary directory for coverage analysis."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def coverage_analyzer(temp_coverage_dir):
    """Create coverage analyzer instance."""
    source_path = temp_coverage_dir / "source.py"
    test_path = temp_coverage_dir / "test_source.py"
    
    # Create sample source file
    source_path.write_text("""
def function1():
    pass

def function2():
    pass

class TestClass:
    def method1(self):
        pass
    
    def method2(self):
        pass
""")
    
    # Create sample test file
    test_path.write_text("""
import unittest

class TestSource(unittest.TestCase):
    def test_function1(self):
        function1()
    
    def test_method1(self):
        tc = TestClass()
        tc.method1()
""")
    
    return TestCoverageAnalyzer(
        source_paths=[source_path],
        test_paths=[test_path]
    )


class TestCoverageMetrics:
    """Test suite for CoverageMetrics."""
    
    def test_metrics_initialization(self):
        """Test metrics initialization."""
        metrics = CoverageMetrics()
        
        assert metrics.total_lines == 0
        assert metrics.covered_lines == 0
        assert metrics.total_branches == 0
        assert metrics.covered_branches == 0
        assert metrics.total_functions == 0
        assert metrics.covered_functions == 0
        assert metrics.total_classes == 0
        assert metrics.covered_classes == 0
    
    def test_line_coverage_calculation(self):
        """Test line coverage calculation."""
        metrics = CoverageMetrics(
            total_lines=100,
            covered_lines=80
        )
        
        assert metrics.line_coverage == 80.0
    
    def test_line_coverage_zero_denominator(self):
        """Test line coverage with zero total lines."""
        metrics = CoverageMetrics(
            total_lines=0,
            covered_lines=0
        )
        
        assert metrics.line_coverage == 0.0
    
    def test_branch_coverage_calculation(self):
        """Test branch coverage calculation."""
        metrics = CoverageMetrics(
            total_branches=20,
            covered_branches=15
        )
        
        assert metrics.branch_coverage == 75.0
    
    def test_function_coverage_calculation(self):
        """Test function coverage calculation."""
        metrics = CoverageMetrics(
            total_functions=10,
            covered_functions=8
        )
        
        assert metrics.function_coverage == 80.0
    
    def test_class_coverage_calculation(self):
        """Test class coverage calculation."""
        metrics = CoverageMetrics(
            total_classes=5,
            covered_classes=4
        )
        
        assert metrics.class_coverage == 80.0


class TestCoverageReport:
    """Test suite for CoverageReport."""
    
    def test_report_creation(self):
        """Test creating a coverage report."""
        metrics = CoverageMetrics(
            total_lines=100,
            covered_lines=80
        )
        
        report = CoverageReport(
            module_name="test_module",
            metrics=metrics
        )
        
        assert report.module_name == "test_module"
        assert report.metrics == metrics
        assert report.uncovered_files == []
        assert report.uncovered_functions == []
        assert report.uncovered_classes == []
        assert report.coverage_trend == []
        assert report.recommendations == []
    
    def test_report_with_uncovered_items(self):
        """Test creating report with uncovered items."""
        metrics = CoverageMetrics()
        
        report = CoverageReport(
            module_name="test_module",
            metrics=metrics,
            uncovered_files=["file1.py", "file2.py"],
            uncovered_functions=["func1", "func2"],
            uncovered_classes=["Class1"]
        )
        
        assert len(report.uncovered_files) == 2
        assert len(report.uncovered_functions) == 2
        assert len(report.uncovered_classes) == 1


class TestTestCoverageAnalyzer:
    """Test suite for TestCoverageAnalyzer."""
    
    def test_initialization(self, temp_coverage_dir):
        """Test analyzer initialization."""
        source_path = temp_coverage_dir / "source.py"
        test_path = temp_coverage_dir / "test_source.py"
        
        source_path.write_text("def test(): pass")
        test_path.write_text("def test_test(): pass")
        
        analyzer = TestCoverageAnalyzer(
            source_paths=[source_path],
            test_paths=[test_path],
            min_coverage_threshold=80.0
        )
        
        assert len(analyzer.source_paths) == 1
        assert len(analyzer.test_paths) == 1
        assert analyzer.min_coverage_threshold == 80.0
    
    def test_analyze_coverage(self, coverage_analyzer):
        """Test coverage analysis."""
        report = coverage_analyzer.analyze()
        
        assert isinstance(report, CoverageReport)
        assert report.module_name == "Overall"
        assert report.metrics is not None
        assert report.metrics.total_lines > 0
    
    def test_generate_text_report(self, coverage_analyzer, temp_coverage_dir):
        """Test generating text format report."""
        output_path = temp_coverage_dir / "coverage_report.txt"
        
        result = coverage_analyzer.generate_report(
            str(output_path),
            report_format=CoverageReportFormat.TEXT
        )
        
        assert Path(result).exists()
        content = Path(result).read_text()
        assert "TEST COVERAGE REPORT" in content
        assert "OVERALL COVERAGE METRICS" in content
        assert "Line Coverage" in content
    
    def test_generate_html_report(self, coverage_analyzer, temp_coverage_dir):
        """Test generating HTML format report."""
        output_path = temp_coverage_dir / "coverage_report.html"
        
        result = coverage_analyzer.generate_report(
            str(output_path),
            report_format=CoverageReportFormat.HTML
        )
        
        assert Path(result).exists()
        content = Path(result).read_text()
        assert "<!DOCTYPE html>" in content
        assert "<h1>Test Coverage Report</h1>" in content
    
    def test_generate_json_report(self, coverage_analyzer, temp_coverage_dir):
        """Test generating JSON format report."""
        output_path = temp_coverage_dir / "coverage_report.json"
        
        result = coverage_analyzer.generate_report(
            str(output_path),
            report_format=CoverageReportFormat.JSON
        )
        
        assert Path(result).exists()
        import json
        with open(result, 'r') as f:
            data = json.load(f)
        
        assert "module_name" in data
        assert "metrics" in data
        assert "line_coverage" in data["metrics"]
    
    def test_generate_xml_report(self, coverage_analyzer, temp_coverage_dir):
        """Test generating XML format report."""
        output_path = temp_coverage_dir / "coverage_report.xml"
        
        result = coverage_analyzer.generate_report(
            str(output_path),
            report_format=CoverageReportFormat.XML
        )
        
        assert Path(result).exists()
        content = Path(result).read_text()
        assert "<?xml version=" in content
        assert "<coverage>" in content
    
    def test_recommendations_generation(self, coverage_analyzer):
        """Test recommendations generation."""
        report = coverage_analyzer.analyze()
        
        # Force low coverage to test recommendations
        report.metrics.covered_lines = 50
        report.metrics.total_lines = 100
        
        recommendations = coverage_analyzer._generate_recommendations(report.metrics)
        
        assert len(recommendations) > 0
        assert any("CRITICAL" in rec or "HIGH" in rec for rec in recommendations)
    
    def test_coverage_status_determination(self, coverage_analyzer):
        """Test coverage status determination."""
        # Good coverage
        assert coverage_analyzer._get_coverage_status(95) == "good"
        
        # Warning coverage
        assert coverage_analyzer._get_coverage_status(75) == "warning"
        
        # Critical coverage
        assert coverage_analyzer._get_coverage_status(50) == "critical"


class TestFactoryFunction:
    """Test suite for factory functions."""
    
    def test_analyze_test_coverage_factory(self, temp_coverage_dir):
        """Test analyzing test coverage via factory function."""
        source_path = temp_coverage_dir / "source.py"
        test_path = temp_coverage_dir / "test_source.py"
        
        source_path.write_text("def func(): pass")
        test_path.write_text("def test_func(): func()")
        
        output_path = temp_coverage_dir / "coverage.txt"
        
        result = analyze_test_coverage(
            [str(source_path)],
            [str(test_path)],
            str(output_path)
        )
        
        assert Path(result).exists()


class TestEdgeCases:
    """Test suite for edge cases."""
    
    def test_empty_source_files(self, temp_coverage_dir):
        """Test handling of empty source files."""
        source_path = temp_coverage_dir / "empty.py"
        test_path = temp_coverage_dir / "test_empty.py"
        
        source_path.write_text("")
        test_path.write_text("")
        
        analyzer = TestCoverageAnalyzer(
            source_paths=[source_path],
            test_paths=[test_path]
        )
        
        report = analyzer.analyze()
        
        assert report.metrics.total_lines == 0
    
    def test_missing_test_files(self, temp_coverage_dir):
        """Test handling of missing test files."""
        source_path = temp_coverage_dir / "source.py"
        test_path = temp_coverage_dir / "test_source.py"
        
        source_path.write_text("def func(): pass")
        # Don't create test file
        
        analyzer = TestCoverageAnalyzer(
            source_paths=[source_path],
            test_paths=[test_path]
        )
        
        report = analyzer.analyze()
        
        # Should still generate report but with low coverage
        assert report.metrics.line_coverage < 50


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])