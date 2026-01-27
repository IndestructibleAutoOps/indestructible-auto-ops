"""
Documentation Package - Enterprise Grade
========================================

This package provides enterprise-grade documentation capabilities.
"""

from .api_documentation_generator import (
    APIDocumentationGenerator,
    DocOutputFormat,
    DocSection,
    DocElement,
    DocModule,
    generate_api_docs
)

from .test_coverage_analyzer import (
    TestCoverageAnalyzer,
    CoverageMetrics,
    CoverageReport,
    CoverageReportFormat,
    analyze_test_coverage
)

__all__ = [
    # API Documentation
    "APIDocumentationGenerator",
    "DocOutputFormat",
    "DocSection",
    "DocElement",
    "DocModule",
    "generate_api_docs",
    
    # Test Coverage
    "TestCoverageAnalyzer",
    "CoverageMetrics",
    "CoverageReport",
    "CoverageReportFormat",
    "analyze_test_coverage",
]