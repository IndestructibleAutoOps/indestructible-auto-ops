"""
Unit Tests for API Documentation Generator
==========================================

Tests for the enterprise-grade API documentation generation system.
"""

import tempfile
from pathlib import Path

import pytest

from api_documentation_generator import (
    APIDocumentationGenerator,
    DocOutputFormat,
    DocSection,
    DocElement,
    DocModule,
    generate_api_docs
)


# Sample module for testing
SAMPLE_MODULE = """
def test_function(param1: str, param2: int = 10) -> str:
    '''
    Test function for documentation.
    
    Args:
        param1: First parameter
        param2: Second parameter
    
    Returns:
        Result string
    
    Raises:
        ValueError: If invalid input
    '''
    return f"{param1}_{param2}"


class TestClass:
    '''Test class for documentation.'''
    
    def __init__(self, value: int):
        '''Initialize test class.'''
        self.value = value
    
    def method1(self, param: str) -> str:
        '''Test method one.'''
        return param
    
    def method2(self) -> int:
        '''Test method two.'''
        return self.value
"""


@pytest.fixture
def temp_doc_dir():
    """Create temporary directory for documentation files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def doc_generator():
    """Create documentation generator instance."""
    return APIDocumentationGenerator(
        output_format=DocOutputFormat.MARKDOWN
    )


class TestAPIDocumentationGenerator:
    """Test suite for APIDocumentationGenerator."""
    
    def test_initialization(self):
        """Test documentation generator initialization."""
        generator = APIDocumentationGenerator(
            output_format=DocOutputFormat.MARKDOWN,
            include_private=False,
            include_dunder=False
        )
        
        assert generator.output_format == DocOutputFormat.MARKDOWN
        assert generator.include_private is False
        assert generator.include_dunder is False
    
    def test_initialization_with_defaults(self):
        """Test initialization with default values."""
        generator = APIDocumentationGenerator()
        
        assert generator.output_format == DocOutputFormat.MARKDOWN
        assert generator.include_private is False
        assert generator.include_dunder is False
        assert generator.add_examples is True
        assert generator.add_version_info is True
    
    def test_generate_markdown_from_module(self, temp_doc_dir):
        """Test generating Markdown documentation from module."""
        # Create temporary module file
        module_path = temp_doc_dir / "test_module.py"
        module_path.write_text(SAMPLE_MODULE)
        
        # Import module
        import sys
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Generate documentation
        generator = APIDocumentationGenerator(output_format=DocOutputFormat.MARKDOWN)
        output_path = temp_doc_dir / "test_module.md"
        
        result = generator.generate_from_module(module, str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
        assert "test_function" in Path(result).read_text()
        assert "TestClass" in Path(result).read_text()
    
    def test_generate_html_from_module(self, temp_doc_dir):
        """Test generating HTML documentation from module."""
        # Create temporary module file
        module_path = temp_doc_dir / "test_module.py"
        module_path.write_text(SAMPLE_MODULE)
        
        # Import module
        import sys
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Generate documentation
        generator = APIDocumentationGenerator(output_format=DocOutputFormat.HTML)
        output_path = temp_doc_dir / "test_module.html"
        
        result = generator.generate_from_module(module, str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
        content = Path(result).read_text()
        assert "<h1>" in content
        assert "test_function" in content
    
    def test_generate_rst_from_module(self, temp_doc_dir):
        """Test generating RST documentation from module."""
        # Create temporary module file
        module_path = temp_doc_dir / "test_module.py"
        module_path.write_text(SAMPLE_MODULE)
        
        # Import module
        import sys
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Generate documentation
        generator = APIDocumentationGenerator(output_format=DocOutputFormat.RST)
        output_path = temp_doc_dir / "test_module.rst"
        
        result = generator.generate_from_module(module, str(output_path))
        
        assert Path(result).exists()
        assert Path(result).stat().st_size > 0
        content = Path(result).read_text()
        assert ".. function::" in content or ".. class::" in content
    
    def test_include_private_members(self, temp_doc_dir):
        """Test including private members."""
        # Create module with private members
        module_code = """
def public_function():
    '''Public function.'''
    pass

def _private_function():
    '''Private function.'''
    pass
"""
        module_path = temp_doc_dir / "test_private.py"
        module_path.write_text(module_code)
        
        # Import module
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_private", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Generate with private members
        generator = APIDocumentationGenerator(include_private=True)
        output_path = temp_doc_dir / "test_private.md"
        generator.generate_from_module(module, str(output_path))
        
        content = Path(output_path).read_text()
        assert "_private_function" in content
    
    def test_exclude_private_members(self, temp_doc_dir):
        """Test excluding private members."""
        # Create module with private members
        module_code = """
def public_function():
    '''Public function.'''
    pass

def _private_function():
    '''Private function.'''
    pass
"""
        module_path = temp_doc_dir / "test_public.py"
        module_path.write_text(module_code)
        
        # Import module
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_public", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Generate without private members
        generator = APIDocumentationGenerator(include_private=False)
        output_path = temp_doc_dir / "test_public.md"
        generator.generate_from_module(module, str(output_path))
        
        content = Path(output_path).read_text()
        assert "_private_function" not in content


class TestDocElement:
    """Test suite for DocElement."""
    
    def test_doc_element_creation(self):
        """Test creating a documentation element."""
        element = DocElement(
            name="test_function",
            section=DocSection.FUNCTION,
            docstring="Test function",
            signature="test_function(param1, param2)"
        )
        
        assert element.name == "test_function"
        assert element.section == DocSection.FUNCTION
        assert element.docstring == "Test function"
        assert element.signature == "test_function(param1, param2)"
        assert element.parameters == []
        assert element.returns is None
        assert element.raises == []
    
    def test_doc_element_with_parameters(self):
        """Test creating element with parameters."""
        element = DocElement(
            name="test_function",
            section=DocSection.FUNCTION,
            parameters=[
                {"name": "param1", "description": "First parameter"},
                {"name": "param2", "description": "Second parameter"}
            ]
        )
        
        assert len(element.parameters) == 2
        assert element.parameters[0]["name"] == "param1"
        assert element.parameters[1]["name"] == "param2"


class TestDocModule:
    """Test suite for DocModule."""
    
    def test_doc_module_creation(self):
        """Test creating a documentation module."""
        module = DocModule(
            name="test_module",
            docstring="Test module documentation"
        )
        
        assert module.name == "test_module"
        assert module.docstring == "Test module documentation"
        assert module.classes == {}
        assert module.functions == {}
        assert module.imports == []
    
    def test_doc_module_with_content(self):
        """Test creating module with content."""
        class_doc = DocElement(
            name="TestClass",
            section=DocSection.CLASS
        )
        func_doc = DocElement(
            name="test_function",
            section=DocSection.FUNCTION
        )
        
        module = DocModule(
            name="test_module",
            classes={"TestClass": class_doc},
            functions={"test_function": func_doc}
        )
        
        assert len(module.classes) == 1
        assert len(module.functions) == 1
        assert "TestClass" in module.classes
        assert "test_function" in module.functions


class TestFactoryFunction:
    """Test suite for factory functions."""
    
    def test_generate_api_docs_markdown(self, temp_doc_dir):
        """Test generating API docs via factory function."""
        # Create simple module
        module_code = """
def simple_function():
    '''Simple function.'''
    pass
"""
        module_path = temp_doc_dir / "simple.py"
        module_path.write_text(module_code)
        
        # Import module
        import importlib.util
        spec = importlib.util.spec_from_file_location("simple", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Generate documentation
        output_path = temp_doc_dir / "simple.md"
        result = generate_api_docs(module, str(output_path), output_format="markdown")
        
        assert Path(result).exists()
        assert Path(result).suffix == ".md"
    
    def test_generate_api_docs_html(self, temp_doc_dir):
        """Test generating API docs in HTML format."""
        # Create simple module
        module_code = """
def simple_function():
    '''Simple function.'''
    pass
"""
        module_path = temp_doc_dir / "simple.py"
        module_path.write_text(module_code)
        
        # Import module
        import importlib.util
        spec = importlib.util.spec_from_file_location("simple", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Generate documentation
        output_path = temp_doc_dir / "simple.html"
        result = generate_api_docs(module, str(output_path), output_format="html")
        
        assert Path(result).exists()
        assert Path(result).suffix == ".html"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])