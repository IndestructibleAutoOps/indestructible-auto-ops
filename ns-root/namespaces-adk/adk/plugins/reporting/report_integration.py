"""
Report Integration - PDF Export Integration
============================================

This module provides integration between existing reporting system and PDF generation
with enterprise-grade features including:
- Seamless integration with existing generators
- Multi-format output support
- Automated chart generation
- Template-based reporting
- Batch processing capabilities
"""

import asyncio
import io
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .pdf_generator import PDFGenerator, PDFStyle, PDFPageSize, create_pdf_generator
from .chart_renderer import ChartRenderer, ChartData, ChartType, create_chart_renderer

logger = logging.getLogger(__name__)


@dataclass
class ReportSection:
    """Report section configuration."""
    title: str
    content: str
    charts: Optional[List[Dict[str, Any]]] = None
    tables: Optional[List[Dict[str, Any]]] = None


@dataclass
class PDFReportConfig:
    """PDF report generation configuration."""
    title: str
    subtitle: Optional[str] = None
    author: str = "MachineNativeOps"
    subject: str = "Report"
    keywords: List[str] = None
    page_size: str = "A4"
    color_scheme: str = "corporate"
    enable_toc: bool = True
    enable_page_numbers: bool = True
    
    # Style overrides
    margin_top: float = 0.75
    margin_right: float = 0.75
    margin_bottom: float = 0.75
    margin_left: float = 0.75


class PDFReportGenerator:
    """
    Enterprise-grade PDF report generator with integration capabilities.
    
    Features:
    - Seamless integration with existing reporting system
    - Multi-format output support
    - Automated chart generation
    - Template-based reporting
    - Batch processing capabilities
    
    Performance Targets:
    - 10-page report: <5s
    - 50-page report: <15s
    - Memory usage: <50MB
    """
    
    def __init__(self, config: Optional[PDFReportConfig] = None):
        """
        Initialize PDF report generator.
        
        Args:
            config: PDF report configuration
        """
        self.config = config or PDFReportConfig(title="Report")
        
        # Initialize components
        self.pdf_generator = create_pdf_generator(
            page_size=self.config.page_size,
            color_scheme=self.config.color_scheme,
            enable_toc=self.config.enable_toc
        )
        self.chart_renderer = create_chart_renderer(
            color_scheme=self.config.color_scheme
        )
        
        # Report sections
        self.sections: List[ReportSection] = []
        
        logger.info(
            f"PDFReportGenerator initialized with title={self.config.title}"
        )
    
    def add_section(self, section: ReportSection) -> None:
        """
        Add section to report.
        
        Args:
            section: Report section
        """
        self.sections.append(section)
        logger.debug(f"Added section: {section.title}")
    
    def add_cover_page(
        self,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        author: Optional[str] = None,
        date: Optional[str] = None
    ) -> None:
        """
        Add cover page to report.
        
        Args:
            title: Report title
            subtitle: Report subtitle
            author: Report author
            date: Report date
        """
        title = title or self.config.title
        subtitle = subtitle or self.config.subtitle
        author = author or self.config.author
        date = date or datetime.now().strftime("%B %d, %Y")
        
        # Add title page
        self.pdf_generator.add_title(title, subtitle)
        self.pdf_generator.add_paragraph(f"Author: {author}")
        self.pdf_generator.add_paragraph(f"Date: {date}")
        self.pdf_generator.add_page_break()
        
        logger.debug("Added cover page")
    
    def add_executive_summary(self, summary: str) -> None:
        """
        Add executive summary to report.
        
        Args:
            summary: Executive summary text
        """
        self.pdf_generator.add_heading("Executive Summary")
        self.pdf_generator.add_paragraph(summary)
        self.pdf_generator.add_page_break()
        
        logger.debug("Added executive summary")
    
    def add_table_of_contents(self) -> None:
        """Add table of contents to report."""
        if self.config.enable_toc:
            self.pdf_generator.add_heading("Table of Contents")
            # Add TOC entries
            for section in self.sections:
                self.pdf_generator.add_paragraph(f"• {section.title}")
            self.pdf_generator.add_page_break()
            
            logger.debug("Added table of contents")
    
    def add_section_content(self, section: ReportSection) -> None:
        """
        Add section content to report.
        
        Args:
            section: Report section
        """
        # Add section heading
        self.pdf_generator.add_heading(section.title, level=2)
        
        # Add content
        self.pdf_generator.add_paragraph(section.content)
        
        # Add tables if any
        if section.tables:
            for table in section.tables:
                self.pdf_generator.add_table(
                    data=table["data"],
                    headers=table.get("headers"),
                    col_widths=table.get("col_widths")
                )
        
        # Add charts if any
        if section.charts:
            for chart_config in section.charts:
                self._add_chart_to_report(chart_config)
    
    def _add_chart_to_report(self, chart_config: Dict[str, Any]) -> None:
        """
        Add chart to report.
        
        Args:
            chart_config: Chart configuration
        """
        # Extract chart data
        chart_type = chart_config.get("type", "bar")
        labels = chart_config.get("labels", [])
        values = chart_config.get("values", [])
        title = chart_config.get("title", "Chart")
        
        # Create chart data
        chart_data = ChartData(
            labels=labels,
            values=values,
            series_name=title
        )
        
        # Render chart to temporary file
        temp_chart_path = f"/tmp/chart_{datetime.now().timestamp()}.png"
        
        try:
            if chart_type == "bar":
                self.chart_renderer.render_bar_chart(chart_data, temp_chart_path)
            elif chart_type == "line":
                self.chart_renderer.render_line_chart(chart_data, temp_chart_path)
            elif chart_type == "pie":
                self.chart_renderer.render_pie_chart(chart_data, temp_chart_path)
            elif chart_type == "scatter":
                self.chart_renderer.render_scatter_chart(chart_data, temp_chart_path)
            elif chart_type == "area":
                self.chart_renderer.render_area_chart(chart_data, temp_chart_path)
            
            # Add chart to PDF
            self.pdf_generator.add_image(
                temp_chart_path,
                width=6.0,
                caption=title
            )
        
        except Exception as e:
            logger.error(f"Failed to add chart to report: {e}")
        
        finally:
            # Clean up temp file
            try:
                Path(temp_chart_path).unlink()
            except:
                pass
    
    def add_appendix(self, content: str) -> None:
        """
        Add appendix to report.
        
        Args:
            content: Appendix content
        """
        self.pdf_generator.add_page_break()
        self.pdf_generator.add_heading("Appendix", level=1)
        self.pdf_generator.add_paragraph(content)
        
        logger.debug("Added appendix")
    
    def generate(self, output_path: str) -> str:
        """
        Generate complete PDF report.
        
        Args:
            output_path: Path to save PDF file
            
        Returns:
            Path to generated PDF file
        """
        logger.info(f"Generating PDF report: {output_path}")
        
        # Add all sections
        for section in self.sections:
            self.add_section_content(section)
        
        # Generate PDF
        result_path = self.pdf_generator.generate(output_path)
        
        logger.info(f"PDF report generated: {result_path}")
        return result_path
    
    def generate_bytes(self) -> bytes:
        """
        Generate PDF report as bytes.
        
        Returns:
            PDF file content as bytes
        """
        # Add all sections
        for section in self.sections:
            self.add_section_content(section)
        
        # Generate PDF bytes
        return self.pdf_generator.generate_bytes()
    
    def clear(self) -> None:
        """Clear all sections and reset document."""
        self.sections = []
        self.pdf_generator.clear()
        
        logger.debug("Cleared report")
    
    def get_section_count(self) -> int:
        """Get number of sections in report."""
        return len(self.sections)


def generate_pdf_report_from_dict(
    report_data: Dict[str, Any],
    output_path: str,
    config: Optional[PDFReportConfig] = None
) -> str:
    """
    Generate PDF report from dictionary data.
    
    Args:
        report_data: Report data dictionary
        output_path: Path to save PDF
        config: PDF configuration
        
    Returns:
        Path to generated PDF
    """
    # Create generator
    generator = PDFReportGenerator(config=config)
    
    # Add cover page
    generator.add_cover_page(
        title=report_data.get("title"),
        subtitle=report_data.get("subtitle")
    )
    
    # Add executive summary
    if "executive_summary" in report_data:
        generator.add_executive_summary(report_data["executive_summary"])
    
    # Add sections
    for section_data in report_data.get("sections", []):
        section = ReportSection(
            title=section_data["title"],
            content=section_data["content"],
            charts=section_data.get("charts"),
            tables=section_data.get("tables")
        )
        generator.add_section(section)
    
    # Add appendix
    if "appendix" in report_data:
        generator.add_appendix(report_data["appendix"])
    
    # Generate report
    return generator.generate(output_path)


def generate_pdf_report_from_markdown(
    markdown_path: str,
    output_path: str,
    config: Optional[PDFReportConfig] = None
) -> str:
    """
    Generate PDF report from markdown file.
    
    Args:
        markdown_path: Path to markdown file
        output_path: Path to save PDF
        config: PDF configuration
        
    Returns:
        Path to generated PDF
    """
    # Read markdown file
    with open(markdown_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Parse markdown (simple parsing)
    lines = markdown_content.split('\n')
    
    # Create generator
    generator = PDFReportGenerator(config=config)
    
    # Parse and add content
    current_section = None
    current_content = []
    
    for line in lines:
        if line.startswith('# '):
            # Title
            if current_section:
                generator.add_section(ReportSection(
                    title=current_section,
                    content=' '.join(current_content)
                ))
            current_section = line[2:].strip()
            current_content = []
        elif line.startswith('## '):
            # Subtitle
            if current_section:
                generator.add_section(ReportSection(
                    title=current_section,
                    content=' '.join(current_content)
                ))
            current_section = line[3:].strip()
            current_content = []
        elif line.startswith('- '):
            # List item
            current_content.append(line[2:].strip())
        else:
            # Regular text
            if line.strip():
                current_content.append(line.strip())
    
    # Add last section
    if current_section:
        generator.add_section(ReportSection(
            title=current_section,
            content=' '.join(current_content)
        ))
    
    # Generate report
    return generator.generate(output_path)