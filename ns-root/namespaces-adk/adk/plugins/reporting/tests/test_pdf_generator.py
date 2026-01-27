"""
Unit Tests for PDF Generator
=============================

Tests for the enterprise-grade PDF generation system.
"""

import io
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from pdf_generator import (
    PDFGenerator,
    PDFStyle,
    PDFPageSize,
    PDFColorScheme,
    create_pdf_generator
)


@pytest.fixture
def temp_pdf_dir():
    """Create temporary directory for PDF files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def pdf_generator():
    """Create PDF generator instance."""
    return create_pdf_generator(
        page_size="A4",
        color_scheme="corporate"
    )


class TestPDFGenerator:
    """Test suite for PDFGenerator."""
    
    def test_initialization(self):
        """Test PDF generator initialization."""
        generator = PDFGenerator(
            page_size=PDFPageSize.A4,
            enable_toc=True
        )
        
        assert generator.page_size == PDFPageSize.A4
        assert generator.enable_toc is True
        assert generator.enable_page_numbers is True
        assert len(generator.elements) == 0
    
    def test_custom_style_initialization(self):
        """Test initialization with custom style."""
        style = PDFStyle(
            font_size=12,
            primary_color="#FF0000",
            margin=(1.0, 1.0, 1.0, 1.0)
        )
        
        generator = PDFGenerator(style=style)
        
        assert generator.style.font_size == 12
        assert generator.style.primary_color == "#FF0000"
        assert generator.style.margin == (1.0, 1.0, 1.0, 1.0)
    
    def test_add_title(self, pdf_generator):
        """Test adding title to document."""
        pdf_generator.add_title("Test Title", "Test Subtitle")
        
        assert pdf_generator.get_element_count() > 0
    
    def test_add_heading(self, pdf_generator):
        """Test adding heading to document."""
        pdf_generator.add_heading("Test Heading", level=2)
        
        assert pdf_generator.get_element_count() > 0
    
    def test_add_paragraph(self, pdf_generator):
        """Test adding paragraph to document."""
        pdf_generator.add_paragraph("This is a test paragraph.")
        
        assert pdf_generator.get_element_count() > 0
    
    def test_add_list_unordered(self, pdf_generator):
        """Test adding unordered list to document."""
        items = ["Item 1", "Item 2", "Item 3"]
        pdf_generator.add_list(items, ordered=False)
        
        assert pdf_generator.get_element_count() == 3
    
    def test_add_list_ordered(self, pdf_generator):
        """Test adding ordered list to document."""
        items = ["Item 1", "Item 2", "Item 3"]
        pdf_generator.add_list(items, ordered=True)
        
        assert pdf_generator.get_element_count() == 3
    
    def test_add_table(self, pdf_generator):
        """Test adding table to document."""
        data = [
            ["Row 1, Col 1", "Row 1, Col 2"],
            ["Row 2, Col 1", "Row 2, Col 2"],
            ["Row 3, Col 1", "Row 3, Col 2"]
        ]
        headers = ["Column 1", "Column 2"]
        
        pdf_generator.add_table(data, headers=headers)
        
        assert pdf_generator.get_element_count() > 0
    
    def test_add_page_break(self, pdf_generator):
        """Test adding page break to document."""
        initial_count = pdf_generator.get_element_count()
        pdf_generator.add_page_break()
        
        assert pdf_generator.get_element_count() == initial_count + 1
    
    def test_add_spacer(self, pdf_generator):
        """Test adding spacer to document."""
        initial_count = pdf_generator.get_element_count()
        pdf_generator.add_spacer(height=1.0)
        
        assert pdf_generator.get_element_count() == initial_count + 1
    
    def test_add_horizontal_rule(self, pdf_generator):
        """Test adding horizontal rule to document."""
        initial_count = pdf_generator.get_element_count()
        pdf_generator.add_horizontal_rule()
        
        assert pdf_generator.get_element_count() == initial_count + 1
    
    def test_generate_pdf_file(self, pdf_generator, temp_pdf_dir):
        """Test generating PDF file."""
        # Add content
        pdf_generator.add_title("Test Report")
        pdf_generator.add_paragraph("This is a test paragraph.")
        
        # Generate PDF
        output_path = temp_pdf_dir / "test.pdf"
        result = pdf_generator.generate(str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
    
    def test_generate_pdf_bytes(self, pdf_generator):
        """Test generating PDF as bytes."""
        # Add content
        pdf_generator.add_title("Test Report")
        pdf_generator.add_paragraph("This is a test paragraph.")
        
        # Generate PDF bytes
        pdf_bytes = pdf_generator.generate_bytes()
        
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        assert pdf_bytes.startswith(b'%PDF')
    
    def test_clear_elements(self, pdf_generator):
        """Test clearing all elements."""
        # Add content
        pdf_generator.add_title("Test Title")
        pdf_generator.add_paragraph("Test paragraph")
        
        # Clear
        pdf_generator.clear()
        
        assert pdf_generator.get_element_count() == 0
    
    def test_get_element_count(self, pdf_generator):
        """Test getting element count."""
        assert pdf_generator.get_element_count() == 0
        
        pdf_generator.add_paragraph("Test")
        assert pdf_generator.get_element_count() == 1
        
        pdf_generator.add_paragraph("Test 2")
        assert pdf_generator.get_element_count() == 2
    
    def test_multiple_page_sizes(self, temp_pdf_dir):
        """Test different page sizes."""
        sizes = [PDFPageSize.LETTER, PDFPageSize.A4, PDFPageSize.LEGAL]
        
        for size in sizes:
            generator = PDFGenerator(page_size=size)
            generator.add_title(f"Test {size.value}")
            
            output_path = temp_pdf_dir / f"test_{size.value}.pdf"
            result = generator.generate(str(output_path))
            
            assert Path(result).exists()


class TestPDFStyle:
    """Test suite for PDFStyle."""
    
    def test_default_style(self):
        """Test default style configuration."""
        style = PDFStyle()
        
        assert style.font_family == "Helvetica"
        assert style.font_size == 10
        assert style.line_spacing == 1.5
        assert style.margin == (0.75, 0.75, 0.75, 0.75)
        assert style.header_enabled is True
        assert style.footer_enabled is True
        assert style.page_numbers is True
    
    def test_custom_style(self):
        """Test custom style configuration."""
        style = PDFStyle(
            font_family="Arial",
            font_size=12,
            line_spacing=2.0,
            margin=(1.0, 1.0, 1.0, 1.0),
            primary_color="#FF0000",
            header_enabled=False
        )
        
        assert style.font_family == "Arial"
        assert style.font_size == 12
        assert style.line_spacing == 2.0
        assert style.margin == (1.0, 1.0, 1.0, 1.0)
        assert style.primary_color == "#FF0000"
        assert style.header_enabled is False


class TestFactoryFunction:
    """Test suite for factory functions."""
    
    def test_create_pdf_generator(self):
        """Test creating PDF generator via factory function."""
        generator = create_pdf_generator(
            page_size="A4",
            color_scheme="corporate"
        )
        
        assert isinstance(generator, PDFGenerator)
        assert generator.page_size == PDFPageSize.A4
    
    def test_create_pdf_generator_different_schemes(self):
        """Test creating generator with different color schemes."""
        schemes = ["corporate", "modern", "minimal", "dark"]
        
        for scheme in schemes:
            generator = create_pdf_generator(color_scheme=scheme)
            assert isinstance(generator, PDFGenerator)


class TestColorSchemes:
    """Test suite for color schemes."""
    
    def test_color_schemes_exist(self):
        """Test that all color schemes are defined."""
        schemes = [
            PDFColorScheme.CORPORATE,
            PDFColorScheme.MODERN,
            PDFColorScheme.MINIMAL,
            PDFColorScheme.DARK
        ]
        
        for scheme in schemes:
            assert scheme in PDFGenerator.COLOR_SCHEMES
    
    def test_color_scheme_colors(self):
        """Test color scheme color values."""
        corporate_colors = PDFGenerator.COLOR_SCHEMES[PDFColorScheme.CORPORATE]
        
        assert "primary" in corporate_colors
        assert "secondary" in corporate_colors
        assert "accent" in corporate_colors
        assert "text" in corporate_colors
        assert "background" in corporate_colors


class TestPerformance:
    """Performance tests for PDF generator."""
    
    def test_small_document_performance(self, temp_pdf_dir):
        """Test performance for small document (10 pages)."""
        generator = PDFGenerator()
        
        # Add content for 10 pages
        for i in range(10):
            generator.add_heading(f"Section {i+1}")
            generator.add_paragraph("Test paragraph content. " * 20)
            generator.add_page_break()
        
        output_path = temp_pdf_dir / "performance_small.pdf"
        
        # Generate and measure time
        import time
        start_time = time.time()
        generator.generate(str(output_path))
        elapsed_time = time.time() - start_time
        
        # Should be <5s for 10 pages
        assert elapsed_time < 5.0, f"Small document took {elapsed_time:.2f}s (target: <5s)"
    
    def test_large_document_performance(self, temp_pdf_dir):
        """Test performance for large document (50 pages)."""
        generator = PDFGenerator()
        
        # Add content for 50 pages
        for i in range(50):
            generator.add_heading(f"Section {i+1}")
            generator.add_paragraph("Test paragraph content. " * 20)
            generator.add_page_break()
        
        output_path = temp_pdf_dir / "performance_large.pdf"
        
        # Generate and measure time
        import time
        start_time = time.time()
        generator.generate(str(output_path))
        elapsed_time = time.time() - start_time
        
        # Should be <15s for 50 pages
        assert elapsed_time < 15.0, f"Large document took {elapsed_time:.2f}s (target: <15s)"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])