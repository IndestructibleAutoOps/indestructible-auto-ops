"""
Unit Tests for Report Integration
==================================

Tests for the PDF report integration system.
"""

import tempfile
from pathlib import Path

import pytest

from report_integration import (
    PDFReportGenerator,
    PDFReportConfig,
    ReportSection,
    generate_pdf_report_from_dict,
    generate_pdf_report_from_markdown
)


@pytest.fixture
def temp_report_dir():
    """Create temporary directory for report files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def report_generator():
    """Create report generator instance."""
    config = PDFReportConfig(
        title="Test Report",
        subtitle="Test Subtitle",
        author="Test Author"
    )
    return PDFReportGenerator(config=config)


@pytest.fixture
def sample_report_data():
    """Create sample report data."""
    return {
        "title": "Sample Report",
        "subtitle": "Enterprise Grade",
        "author": "MachineNativeOps",
        "executive_summary": "This is a sample executive summary for testing.",
        "sections": [
            {
                "title": "Introduction",
                "content": "This is the introduction section with detailed content.",
                "tables": [
                    {
                        "data": [
                            ["A", "100"],
                            ["B", "200"],
                            ["C", "300"]
                        ],
                        "headers": ["Category", "Value"]
                    }
                ],
                "charts": [
                    {
                        "type": "bar",
                        "title": "Sample Bar Chart",
                        "labels": ["A", "B", "C"],
                        "values": [100, 200, 300]
                    }
                ]
            },
            {
                "title": "Analysis",
                "content": "This is the analysis section with more detailed content."
            }
        ],
        "appendix": "Additional information in the appendix."
    }


class TestPDFReportGenerator:
    """Test suite for PDFReportGenerator."""
    
    def test_initialization(self):
        """Test report generator initialization."""
        config = PDFReportConfig(
            title="Test Report",
            author="Test Author"
        )
        
        generator = PDFReportGenerator(config=config)
        
        assert generator.config.title == "Test Report"
        assert generator.config.author == "Test Author"
        assert len(generator.sections) == 0
    
    def test_initialization_with_defaults(self):
        """Test initialization with default configuration."""
        generator = PDFReportGenerator()
        
        assert generator.config.title == "Report"
        assert generator.config.author == "MachineNativeOps"
        assert generator.config.page_size == "A4"
        assert generator.config.color_scheme == "corporate"
    
    def test_add_section(self, report_generator):
        """Test adding section to report."""
        section = ReportSection(
            title="Test Section",
            content="Test content"
        )
        
        report_generator.add_section(section)
        
        assert len(report_generator.sections) == 1
        assert report_generator.sections[0].title == "Test Section"
    
    def test_add_multiple_sections(self, report_generator):
        """Test adding multiple sections to report."""
        for i in range(5):
            section = ReportSection(
                title=f"Section {i+1}",
                content=f"Content {i+1}"
            )
            report_generator.add_section(section)
        
        assert len(report_generator.sections) == 5
    
    def test_add_cover_page(self, report_generator):
        """Test adding cover page to report."""
        report_generator.add_cover_page(
            title="Custom Title",
            subtitle="Custom Subtitle"
        )
        
        # Cover page adds elements to PDF generator
        assert report_generator.pdf_generator.get_element_count() > 0
    
    def test_add_executive_summary(self, report_generator):
        """Test adding executive summary to report."""
        summary = "This is the executive summary."
        report_generator.add_executive_summary(summary)
        
        # Executive summary adds elements to PDF generator
        assert report_generator.pdf_generator.get_element_count() > 0
    
    def test_add_table_of_contents(self, report_generator):
        """Test adding table of contents to report."""
        # Add sections first
        section1 = ReportSection(title="Section 1", content="Content 1")
        section2 = ReportSection(title="Section 2", content="Content 2")
        report_generator.add_section(section1)
        report_generator.add_section(section2)
        
        # Add TOC
        report_generator.add_table_of_contents()
        
        # TOC adds elements to PDF generator
        assert report_generator.pdf_generator.get_element_count() > 0
    
    def test_add_section_content_with_tables(self, report_generator):
        """Test adding section content with tables."""
        section = ReportSection(
            title="Section with Tables",
            content="Content",
            tables=[
                {
                    "data": [["A", "100"], ["B", "200"]],
                    "headers": ["Category", "Value"]
                }
            ]
        )
        
        initial_count = report_generator.pdf_generator.get_element_count()
        report_generator.add_section_content(section)
        
        # Section content adds elements
        assert report_generator.pdf_generator.get_element_count() > initial_count
    
    def test_add_section_content_with_charts(self, report_generator):
        """Test adding section content with charts."""
        section = ReportSection(
            title="Section with Charts",
            content="Content",
            charts=[
                {
                    "type": "bar",
                    "title": "Test Chart",
                    "labels": ["A", "B", "C"],
                    "values": [10, 20, 30]
                }
            ]
        )
        
        initial_count = report_generator.pdf_generator.get_element_count()
        report_generator.add_section_content(section)
        
        # Section content adds elements
        assert report_generator.pdf_generator.get_element_count() > initial_count
    
    def test_add_appendix(self, report_generator):
        """Test adding appendix to report."""
        appendix = "This is the appendix content."
        report_generator.add_appendix(appendix)
        
        # Appendix adds elements to PDF generator
        assert report_generator.pdf_generator.get_element_count() > 0
    
    def test_generate_pdf_file(self, report_generator, temp_report_dir):
        """Test generating PDF report file."""
        # Add content
        section = ReportSection(
            title="Test Section",
            content="Test content"
        )
        report_generator.add_section(section)
        
        # Generate report
        output_path = temp_report_dir / "test_report.pdf"
        result = report_generator.generate(str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
    
    def test_generate_pdf_bytes(self, report_generator):
        """Test generating PDF report as bytes."""
        # Add content
        section = ReportSection(
            title="Test Section",
            content="Test content"
        )
        report_generator.add_section(section)
        
        # Generate report bytes
        pdf_bytes = report_generator.generate_bytes()
        
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b'%PDF')
    
    def test_clear_report(self, report_generator):
        """Test clearing report."""
        # Add sections
        section1 = ReportSection(title="Section 1", content="Content 1")
        section2 = ReportSection(title="Section 2", content="Content 2")
        report_generator.add_section(section1)
        report_generator.add_section(section2)
        
        # Clear
        report_generator.clear()
        
        assert len(report_generator.sections) == 0
        assert report_generator.pdf_generator.get_element_count() == 0
    
    def test_get_section_count(self, report_generator):
        """Test getting section count."""
        assert report_generator.get_section_count() == 0
        
        report_generator.add_section(ReportSection(title="S1", content="C1"))
        assert report_generator.get_section_count() == 1
        
        report_generator.add_section(ReportSection(title="S2", content="C2"))
        assert report_generator.get_section_count() == 2


class TestReportSection:
    """Test suite for ReportSection."""
    
    def test_section_creation(self):
        """Test creating report section."""
        section = ReportSection(
            title="Test Section",
            content="Test content"
        )
        
        assert section.title == "Test Section"
        assert section.content == "Test content"
        assert section.charts is None
        assert section.tables is None
    
    def test_section_with_tables(self):
        """Test creating section with tables."""
        tables = [{"data": [["A", "100"]], "headers": ["Cat", "Val"]}]
        section = ReportSection(
            title="Section",
            content="Content",
            tables=tables
        )
        
        assert section.tables == tables
    
    def test_section_with_charts(self):
        """Test creating section with charts."""
        charts = [
            {
                "type": "bar",
                "title": "Chart",
                "labels": ["A"],
                "values": [100]
            }
        ]
        section = ReportSection(
            title="Section",
            content="Content",
            charts=charts
        )
        
        assert section.charts == charts


class TestPDFReportConfig:
    """Test suite for PDFReportConfig."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = PDFReportConfig()
        
        assert config.title == "Report"
        assert config.author == "MachineNativeOps"
        assert config.subject == "Report"
        assert config.page_size == "A4"
        assert config.color_scheme == "corporate"
        assert config.enable_toc is True
        assert config.enable_page_numbers is True
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = PDFReportConfig(
            title="Custom Report",
            subtitle="Custom Subtitle",
            author="Custom Author",
            page_size="LETTER",
            color_scheme="modern"
        )
        
        assert config.title == "Custom Report"
        assert config.subtitle == "Custom Subtitle"
        assert config.author == "Custom Author"
        assert config.page_size == "LETTER"
        assert config.color_scheme == "modern"


class TestGenerateFromDict:
    """Test suite for generating reports from dictionary data."""
    
    def test_generate_from_dict_basic(self, temp_report_dir):
        """Test basic generation from dictionary."""
        report_data = {
            "title": "Test Report",
            "sections": [
                {
                    "title": "Section 1",
                    "content": "Content 1"
                }
            ]
        }
        
        output_path = temp_report_dir / "from_dict.pdf"
        result = generate_pdf_report_from_dict(report_data, str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
    
    def test_generate_from_dict_complete(self, temp_report_dir, sample_report_data):
        """Test complete generation from dictionary."""
        output_path = temp_report_dir / "from_dict_complete.pdf"
        result = generate_pdf_report_from_dict(sample_report_data, str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
    
    def test_generate_from_dict_with_config(self, temp_report_dir):
        """Test generation with custom configuration."""
        config = PDFReportConfig(
            title="Custom Report",
            color_scheme="modern"
        )
        
        report_data = {
            "title": "Test Report",
            "sections": [
                {"title": "Section 1", "content": "Content 1"}
            ]
        }
        
        output_path = temp_report_dir / "from_dict_config.pdf"
        result = generate_pdf_report_from_dict(
            report_data,
            str(output_path),
            config=config
        )
        
        assert Path(result).exists()


class TestGenerateFromMarkdown:
    """Test suite for generating reports from markdown files."""
    
    def test_generate_from_markdown_basic(self, temp_report_dir):
        """Test basic generation from markdown."""
        markdown_content = """# Test Report

## Section 1
This is the first section.

## Section 2
This is the second section.
"""
        
        # Create markdown file
        markdown_path = temp_report_dir / "test.md"
        markdown_path.write_text(markdown_content)
        
        output_path = temp_report_dir / "from_markdown.pdf"
        result = generate_pdf_report_from_markdown(
            str(markdown_path),
            str(output_path)
        )
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
    
    def test_generate_from_markdown_with_lists(self, temp_report_dir):
        """Test generation from markdown with lists."""
        markdown_content = """# Test Report

## Features
- Feature 1
- Feature 2
- Feature 3

## Analysis
Detailed analysis content here.
"""
        
        # Create markdown file
        markdown_path = temp_report_dir / "test_lists.md"
        markdown_path.write_text(markdown_content)
        
        output_path = temp_report_dir / "from_markdown_lists.pdf"
        result = generate_pdf_report_from_markdown(
            str(markdown_path),
            str(output_path)
        )
        
        assert Path(result).exists()


class TestPerformance:
    """Performance tests for report integration."""
    
    def test_small_report_performance(self, temp_report_dir):
        """Test performance for small report (10 pages)."""
        config = PDFReportConfig(title="Performance Test")
        generator = PDFReportGenerator(config=config)
        
        # Add sections
        for i in range(10):
            section = ReportSection(
                title=f"Section {i+1}",
                content="Test content. " * 50
            )
            generator.add_section(section)
        
        output_path = temp_report_dir / "perf_small.pdf"
        
        import time
        start_time = time.time()
        generator.generate(str(output_path))
        elapsed_time = time.time() - start_time
        
        # Should be <5s for 10 pages
        assert elapsed_time < 5.0, f"Small report took {elapsed_time:.2f}s (target: <5s)"
    
    def test_large_report_performance(self, temp_report_dir):
        """Test performance for large report (50 pages)."""
        config = PDFReportConfig(title="Performance Test")
        generator = PDFReportGenerator(config=config)
        
        # Add sections
        for i in range(50):
            section = ReportSection(
                title=f"Section {i+1}",
                content="Test content. " * 50
            )
            generator.add_section(section)
        
        output_path = temp_report_dir / "perf_large.pdf"
        
        import time
        start_time = time.time()
        generator.generate(str(output_path))
        elapsed_time = time.time() - start_time
        
        # Should be <15s for 50 pages
        assert elapsed_time < 15.0, f"Large report took {elapsed_time:.2f}s (target: <15s)"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])