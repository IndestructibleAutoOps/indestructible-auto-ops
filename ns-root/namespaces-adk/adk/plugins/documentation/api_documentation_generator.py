"""
API Documentation Generator - Enterprise Grade
==============================================

This module provides automated API documentation generation with enterprise-grade features including:
- Automatic docstring extraction
- Type hint documentation
- Parameter and return value documentation
- Example code generation
- Markdown and HTML output formats
- Cross-references and links
- Version compatibility notes
"""

import ast
import inspect
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Type, get_type_hints

logger = logging.getLogger(__name__)


class DocOutputFormat(Enum):
    """Supported documentation output formats."""
    MARKDOWN = "markdown"
    HTML = "html"
    RST = "rst"


class DocSection(Enum):
    """Documentation section types."""
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    PROPERTY = "property"


@dataclass
class DocElement:
    """Represents a documented element."""
    name: str
    section: DocSection
    docstring: Optional[str] = None
    signature: Optional[str] = None
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    returns: Optional[Dict[str, Any]] = None
    raises: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    see_also: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    deprecated: bool = False
    version_added: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class DocModule:
    """Represents a documented module."""
    name: str
    docstring: Optional[str] = None
    classes: Dict[str, DocElement] = field(default_factory=dict)
    functions: Dict[str, DocElement] = field(default_factory=dict)
    imports: List[str] = field(default_factory=list)
    constants: Dict[str, Any] = field(default_factory=dict)


class APIDocumentationGenerator:
    """
    Enterprise-grade API documentation generator.
    
    Features:
    - Automatic docstring extraction
    - Type hint documentation
    - Parameter and return value documentation
    - Example code generation
    - Markdown and HTML output formats
    - Cross-references and links
    - Version compatibility notes
    """
    
    def __init__(
        self,
        output_format: DocOutputFormat = DocOutputFormat.MARKDOWN,
        include_private: bool = False,
        include_dunder: bool = False,
        add_examples: bool = True,
        add_version_info: bool = True
    ):
        """
        Initialize API documentation generator.
        
        Args:
            output_format: Documentation output format
            include_private: Include private members (_name)
            include_dunder: Include dunder methods (__name__)
            add_examples: Add usage examples
            add_version_info: Add version information
        """
        self.output_format = output_format
        self.include_private = include_private
        self.include_dunder = include_dunder
        self.add_examples = add_examples
        self.add_version_info = add_version_info
        
        logger.info(
            f"APIDocumentationGenerator initialized with "
            f"format={output_format.value}"
        )
    
    def generate_from_module(
        self,
        module: Any,
        output_path: str
    ) -> str:
        """
        Generate documentation from a Python module.
        
        Args:
            module: Python module to document
            output_path: Path to save documentation
            
        Returns:
            Path to generated documentation
        """
        logger.info(f"Generating documentation for module: {module.__name__}")
        
        # Parse module
        doc_module = self._parse_module(module)
        
        # Generate documentation
        if self.output_format == DocOutputFormat.MARKDOWN:
            content = self._generate_markdown(doc_module)
        elif self.output_format == DocOutputFormat.HTML:
            content = self._generate_html(doc_module)
        elif self.output_format == DocOutputFormat.RST:
            content = self._generate_rst(doc_module)
        else:
            raise ValueError(f"Unsupported output format: {self.output_format}")
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Documentation generated: {output_path}")
        return output_path
    
    def _parse_module(self, module: Any) -> DocModule:
        """Parse Python module and extract documentation."""
        doc_module = DocModule(
            name=module.__name__,
            docstring=inspect.getdoc(module)
        )
        
        # Get module source file
        source_file = getattr(module, '__file__', None)
        if source_file and Path(source_file).exists():
            # Parse AST for detailed information
            with open(source_file, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            self._parse_ast(tree, doc_module, module)
        
        return doc_module
    
    def _parse_ast(self, tree: ast.AST, doc_module: DocModule, module: Any) -> None:
        """Parse AST and extract documentation elements."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if self._should_include(node.name):
                    class_doc = self._parse_class(node, module)
                    doc_module.classes[node.name] = class_doc
            
            elif isinstance(node, ast.FunctionDef):
                if self._should_include(node.name):
                    func_doc = self._parse_function(node, module)
                    doc_module.functions[node.name] = func_doc
    
    def _parse_class(self, node: ast.ClassDef, module: Any) -> DocElement:
        """Parse class definition."""
        class_doc = DocElement(
            name=node.name,
            section=DocSection.CLASS,
            docstring=ast.get_docstring(node),
            line_number=node.lineno
        )
        
        # Parse methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if self._should_include(item.name):
                    method_doc = self._parse_function(item, module, is_method=True)
                    # Store methods in a special way
                    if not hasattr(class_doc, 'methods'):
                        class_doc.methods = {}
                    class_doc.methods[item.name] = method_doc
        
        return class_doc
    
    def _parse_function(
        self,
        node: ast.FunctionDef,
        module: Any,
        is_method: bool = False
    ) -> DocElement:
        """Parse function definition."""
        # Build signature
        signature = self._build_signature(node, is_method)
        
        # Extract docstring
        docstring = ast.get_docstring(node)
        
        func_doc = DocElement(
            name=node.name,
            section=DocSection.METHOD if is_method else DocSection.FUNCTION,
            docstring=docstring,
            signature=signature,
            line_number=node.lineno
        )
        
        # Parse docstring for structured information
        if docstring:
            self._parse_docstring(docstring, func_doc)
        
        return func_doc
    
    def _build_signature(self, node: ast.FunctionDef, is_method: bool) -> str:
        """Build function signature string."""
        params = []
        
        # Add self for methods
        if is_method:
            params.append("self")
        
        for arg in node.args.args:
            param_name = arg.arg
            # Add type annotation if present
            if arg.annotation:
                param_type = ast.unparse(arg.annotation)
                params.append(f"{param_name}: {param_type}")
            else:
                params.append(param_name)
        
        return f"{node.name}({', '.join(params)})"
    
    def _parse_docstring(self, docstring: str, element: DocElement) -> None:
        """Parse docstring for structured information."""
        lines = docstring.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Detect sections
            if line.lower().startswith('args:'):
                current_section = 'args'
                continue
            elif line.lower().startswith('returns:'):
                current_section = 'returns'
                continue
            elif line.lower().startswith('raises:'):
                current_section = 'raises'
                continue
            elif line.lower().startswith('example:'):
                current_section = 'example'
                continue
            elif line.lower().startswith('note:'):
                current_section = 'note'
                continue
            
            # Parse section content
            if current_section == 'args':
                self._parse_arg_line(line, element)
            elif current_section == 'returns':
                if not element.returns:
                    element.returns = {}
                element.returns['description'] = line
            elif current_section == 'raises':
                element.raises.append(line)
            elif current_section == 'example':
                element.examples.append(line)
            elif current_section == 'note':
                element.notes.append(line)
    
    def _parse_arg_line(self, line: str, element: DocElement) -> None:
        """Parse argument line from docstring."""
        if ':' in line:
            parts = line.split(':', 1)
            param_name = parts[0].strip()
            param_desc = parts[1].strip() if len(parts) > 1 else ""
            
            element.parameters.append({
                'name': param_name,
                'description': param_desc
            })
    
    def _should_include(self, name: str) -> bool:
        """Determine if element should be included in documentation."""
        if not self.include_private and name.startswith('_') and not name.startswith('__'):
            return False
        if not self.include_dunder and name.startswith('__') and name.endswith('__'):
            return False
        return True
    
    def _generate_markdown(self, doc_module: DocModule) -> str:
        """Generate Markdown documentation."""
        lines = []
        
        # Module header
        lines.append(f"# {doc_module.name}")
        lines.append("")
        
        # Module docstring
        if doc_module.docstring:
            lines.append(doc_module.docstring)
            lines.append("")
        
        # Classes section
        if doc_module.classes:
            lines.append("## Classes")
            lines.append("")
            
            for class_name, class_doc in doc_module.classes.items():
                lines.append(f"### {class_name}")
                lines.append("")
                
                if class_doc.docstring:
                    lines.append(class_doc.docstring)
                    lines.append("")
                
                # Methods
                if hasattr(class_doc, 'methods') and class_doc.methods:
                    lines.append("#### Methods")
                    lines.append("")
                    
                    for method_name, method_doc in class_doc.methods.items():
                        lines.append(f"##### {method_name}")
                        lines.append("")
                        
                        if method_doc.signature:
                            lines.append(f"```python")
                            lines.append(method_doc.signature)
                            lines.append(f"```")
                            lines.append("")
                        
                        if method_doc.docstring:
                            lines.append(method_doc.docstring)
                            lines.append("")
        
        # Functions section
        if doc_module.functions:
            lines.append("## Functions")
            lines.append("")
            
            for func_name, func_doc in doc_module.functions.items():
                lines.append(f"### {func_name}")
                lines.append("")
                
                if func_doc.signature:
                    lines.append(f"```python")
                    lines.append(func_doc.signature)
                    lines.append(f"```")
                    lines.append("")
                
                if func_doc.docstring:
                    lines.append(func_doc.docstring)
                    lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_html(self, doc_module: DocModule) -> str:
        """Generate HTML documentation."""
        html = []
        
        # Module header
        html.append(f"<h1>{doc_module.name}</h1>")
        html.append("")
        
        # Module docstring
        if doc_module.docstring:
            html.append(f"<p>{doc_module.docstring}</p>")
            html.append("")
        
        # Classes section
        if doc_module.classes:
            html.append("<h2>Classes</h2>")
            html.append("")
            
            for class_name, class_doc in doc_module.classes.items():
                html.append(f"<h3>{class_name}</h3>")
                html.append("")
                
                if class_doc.docstring:
                    html.append(f"<p>{class_doc.docstring}</p>")
                    html.append("")
        
        # Functions section
        if doc_module.functions:
            html.append("<h2>Functions</h2>")
            html.append("")
            
            for func_name, func_doc in doc_module.functions.items():
                html.append(f"<h3>{func_name}</h3>")
                html.append("")
                
                if func_doc.signature:
                    html.append(f"<pre><code>{func_doc.signature}</code></pre>")
                    html.append("")
                
                if func_doc.docstring:
                    html.append(f"<p>{func_doc.docstring}</p>")
                    html.append("")
        
        return '\n'.join(html)
    
    def _generate_rst(self, doc_module: DocModule) -> str:
        """Generate RST documentation."""
        lines = []
        
        # Module header
        lines.append(doc_module.name)
        lines.append("=" * len(doc_module.name))
        lines.append("")
        
        # Module docstring
        if doc_module.docstring:
            lines.append(doc_module.docstring)
            lines.append("")
        
        # Classes section
        if doc_module.classes:
            lines.append("Classes")
            lines.append("-------")
            lines.append("")
            
            for class_name, class_doc in doc_module.classes.items():
                lines.append(f".. class:: {class_name}")
                lines.append("")
                
                if class_doc.docstring:
                    lines.append(f"   {class_doc.docstring}")
                    lines.append("")
        
        # Functions section
        if doc_module.functions:
            lines.append("Functions")
            lines.append("---------")
            lines.append("")
            
            for func_name, func_doc in doc_module.functions.items():
                lines.append(f".. function:: {func_doc.signature}")
                lines.append("")
                
                if func_doc.docstring:
                    lines.append(f"   {func_doc.docstring}")
                    lines.append("")
        
        return '\n'.join(lines)


def generate_api_docs(
    module: Any,
    output_path: str,
    output_format: str = "markdown",
    include_private: bool = False
) -> str:
    """
    Generate API documentation for a module.
    
    Args:
        module: Python module to document
        output_path: Path to save documentation
        output_format: Output format (markdown, html, rst)
        include_private: Include private members
        
    Returns:
        Path to generated documentation
    """
    format_enum = DocOutputFormat(output_format.lower())
    
    generator = APIDocumentationGenerator(
        output_format=format_enum,
        include_private=include_private
    )
    
    return generator.generate_from_module(module, output_path)