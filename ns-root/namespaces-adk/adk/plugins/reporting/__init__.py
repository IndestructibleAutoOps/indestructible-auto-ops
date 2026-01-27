"""
Reporting Package - Enterprise Grade
=====================================

This package provides enterprise-grade reporting capabilities.
"""

from .pdf_generator import (
    PDFGenerator,
    PDFStyle,
    PDFPageSize,
    PDFColorScheme,
    PDFChart,
    create_pdf_generator
)

from .chart_renderer import (
    ChartRenderer,
    ChartData,
    ChartStyle,
    ChartType,
    ChartColorScheme as ChartColorSchemeType,
    create_chart_renderer
)

from .report_integration import (
    PDFReportGenerator,
    PDFReportConfig,
    ReportSection,
    generate_pdf_report_from_dict,
    generate_pdf_report_from_markdown
)

__all__ = [
    # PDF Generation
    "PDFGenerator",
    "PDFStyle",
    "PDFPageSize",
    "PDFColorScheme",
    "PDFChart",
    "create_pdf_generator",
    
    # Chart Rendering
    "ChartRenderer",
    "ChartData",
    "ChartStyle",
    "ChartType",
    "ChartColorSchemeType",
    "create_chart_renderer",
    
    # Report Integration
    "PDFReportGenerator",
    "PDFReportConfig",
    "ReportSection",
    "generate_pdf_report_from_dict",
    "generate_pdf_report_from_markdown",
]
