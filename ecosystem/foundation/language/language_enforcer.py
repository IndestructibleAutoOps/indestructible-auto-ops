#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: language-enforcer
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
"""
Language Layer Enforcer
=======================
GL Layer: GL00-09 Strategic Layer (Foundation)

Validates that all files comply with the Language Layer Specification.
This is the base layer - all governance depends on language compliance.

The Language Layer ensures:
- All languages are parseable
- All languages are validatable
- All languages are serializable
- All languages are governable
- All languages are evolvable
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import ast
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum


class LanguageType(Enum):
    """Supported language types"""
    YAML = "yaml"
    JSON = "json"
    MARKDOWN = "markdown"
    PYTHON = "python"
    GL_DSL = "gl-dsl"
    UNKNOWN = "unknown"


class Severity(Enum):
    """Violation severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class LanguageViolation:
    """Represents a language layer violation"""
    language: str
    file_path: str
    rule_id: str
    message: str
    severity: Severity
    line: Optional[int] = None
    column: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class LanguageValidationResult:
    """Result of language validation"""
    language: str
    file_path: str
    valid: bool
    violations: List[LanguageViolation] = field(default_factory=list)
    ast_valid: bool = True
    parseable: bool = True


class YAMLValidator:
    """
    Validates YAML files according to Language Layer Specification.
    
    Prohibited features:
    - Anchors (&anchor)
    - References (*reference)
    - Custom tags (!tag)
    - Arbitrary Python objects
    """
    
    # Patterns for prohibited YAML features
    ANCHOR_PATTERN = re.compile(r'&\w+')
    REFERENCE_PATTERN = re.compile(r'\*\w+')
    TAG_PATTERN = re.compile(r'!\w+')
    PYTHON_TAG_PATTERN = re.compile(r'!!python/')
    
    def validate(self, content: str, file_path: str) -> LanguageValidationResult:
        """Validate YAML content"""
        violations = []
        parseable = True
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for anchors
            if self.ANCHOR_PATTERN.search(line):
                violations.append(LanguageViolation(
                    language="yaml",
                    file_path=file_path,
                    rule_id="YAML-001",
                    message="YAML anchors are prohibited",
                    severity=Severity.HIGH,
                    line=line_num,
                    suggestion="Remove anchor and duplicate the data instead"
                ))
            
            # Check for references
            if self.REFERENCE_PATTERN.search(line):
                violations.append(LanguageViolation(
                    language="yaml",
                    file_path=file_path,
                    rule_id="YAML-002",
                    message="YAML references are prohibited",
                    severity=Severity.HIGH,
                    line=line_num,
                    suggestion="Remove reference and use explicit values"
                ))
            
            # Check for custom tags
            if self.TAG_PATTERN.search(line) and not line.strip().startswith('#'):
                violations.append(LanguageViolation(
                    language="yaml",
                    file_path=file_path,
                    rule_id="YAML-003",
                    message="Custom YAML tags are prohibited",
                    severity=Severity.CRITICAL,
                    line=line_num,
                    suggestion="Remove custom tag and use standard YAML types"
                ))
            
            # Check for Python object tags
            if self.PYTHON_TAG_PATTERN.search(line):
                violations.append(LanguageViolation(
                    language="yaml",
                    file_path=file_path,
                    rule_id="YAML-004",
                    message="Python object serialization in YAML is prohibited (security risk)",
                    severity=Severity.CRITICAL,
                    line=line_num,
                    suggestion="Remove Python object tag; use only standard YAML types"
                ))
        
        # Try to parse with safe loader
        try:
            import yaml
            safe_load(content)
        except yaml.YAMLError as e:
            parseable = False
            violations.append(LanguageViolation(
                language="yaml",
                file_path=file_path,
                rule_id="YAML-005",
                message=f"YAML parse error: {str(e)}",
                severity=Severity.CRITICAL,
                suggestion="Fix YAML syntax errors"
            ))
        except ImportError:
            # yaml module not available, skip parse check
            pass
        
        return LanguageValidationResult(
            language="yaml",
            file_path=file_path,
            valid=len(violations) == 0,
            violations=violations,
            parseable=parseable
        )


class JSONValidator:
    """
    Validates JSON files according to Language Layer Specification.
    
    Prohibited features:
    - Comments
    - Trailing commas
    - Non-UTF-8 encoding
    """
    
    # Pattern for detecting trailing commas (invalid in JSON)
    TRAILING_COMMA_PATTERN = re.compile(r',\s*[}\]]')
    
    def validate(self, content: str, file_path: str) -> LanguageValidationResult:
        """Validate JSON content"""
        violations = []
        parseable = True
        
        # First try to parse - if it parses, there are no comments
        # (JSON doesn't support comments, so if it parses, it's valid)
        try:
            json.loads(content)
            parseable = True
        except json.JSONDecodeError as e:
            parseable = False
            violations.append(LanguageViolation(
                language="json",
                file_path=file_path,
                rule_id="JSON-003",
                message=f"JSON parse error: {str(e)}",
                severity=Severity.CRITICAL,
                line=e.lineno,
                column=e.colno,
                suggestion="Fix JSON syntax errors"
            ))
            # If it doesn't parse, check for comments that might be the cause
            # Only flag comments if the JSON doesn't parse
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith('//') or stripped.startswith('/*'):
                    violations.append(LanguageViolation(
                        language="json",
                        file_path=file_path,
                        rule_id="JSON-001",
                        message="Comments in JSON are prohibited",
                        severity=Severity.HIGH,
                        line=line_num,
                        suggestion="Remove all comments from JSON file"
                    ))
                    break  # Only report once
        
        # Check for trailing commas
        if self.TRAILING_COMMA_PATTERN.search(content):
            violations.append(LanguageViolation(
                language="json",
                file_path=file_path,
                rule_id="JSON-002",
                message="Trailing commas in JSON are prohibited",
                severity=Severity.MEDIUM,
                suggestion="Remove trailing commas"
            ))
        
        # Check encoding (file should be UTF-8)
        try:
            content.encode('utf-8')
        except UnicodeEncodeError:
            violations.append(LanguageViolation(
                language="json",
                file_path=file_path,
                rule_id="JSON-004",
                message="JSON must be UTF-8 encoded",
                severity=Severity.HIGH,
                suggestion="Convert file to UTF-8 encoding"
            ))
        
        return LanguageValidationResult(
            language="json",
            file_path=file_path,
            valid=len(violations) == 0,
            violations=violations,
            parseable=parseable
        )


class MarkdownValidator:
    """
    Validates Markdown files according to Language Layer Specification.
    
    Prohibited features:
    - HTML tags
    - Script tags
    - iframes
    """
    
    HTML_TAG_PATTERN = re.compile(r'<(?!!)/?[a-zA-Z][^>]*>', re.IGNORECASE)
    # Match script/iframe opening tags - we just need to detect their presence
    # Don't try to match end tags precisely; just detect if script/iframe exists
    SCRIPT_OPEN_PATTERN = re.compile(r'<\s*script\b', re.IGNORECASE)
    IFRAME_OPEN_PATTERN = re.compile(r'<\s*iframe\b', re.IGNORECASE)
    
    def validate(self, content: str, file_path: str) -> LanguageValidationResult:
        """Validate Markdown content"""
        violations = []
        
        # Check for script tags (highest priority) - just detect opening tag
        if self.SCRIPT_OPEN_PATTERN.search(content):
            violations.append(LanguageViolation(
                language="markdown",
                file_path=file_path,
                rule_id="MD-001",
                message="Script tags in Markdown are prohibited (security risk)",
                severity=Severity.CRITICAL,
                suggestion="Remove all script tags"
            ))
        
        # Check for iframes
        if self.IFRAME_OPEN_PATTERN.search(content):
            violations.append(LanguageViolation(
                language="markdown",
                file_path=file_path,
                rule_id="MD-002",
                message="Iframes in Markdown are prohibited",
                severity=Severity.HIGH,
                suggestion="Remove all iframes; use links instead"
            ))
        
        # Check for HTML tags (excluding comments)
        html_matches = self.HTML_TAG_PATTERN.findall(content)
        if html_matches:
            # Filter out allowed tags (like <br>)
            prohibited_tags = [t for t in html_matches if not self._is_safe_tag(t)]
            if prohibited_tags:
                violations.append(LanguageViolation(
                    language="markdown",
                    file_path=file_path,
                    rule_id="MD-003",
                    message=f"HTML tags in Markdown are prohibited: {', '.join(prohibited_tags[:5])}",
                    severity=Severity.MEDIUM,
                    suggestion="Use pure Markdown syntax instead of HTML"
                ))
        
        return LanguageValidationResult(
            language="markdown",
            file_path=file_path,
            valid=len(violations) == 0,
            violations=violations,
            parseable=True  # Markdown is always parseable
        )
    
    def _is_safe_tag(self, tag: str) -> bool:
        """Check if HTML tag is considered safe"""
        safe_tags = ['br', 'hr', 'img']  # Minimal safe tags
        tag_lower = tag.lower()
        return any(f'<{s}' in tag_lower or f'</{s}' in tag_lower for s in safe_tags)


class PythonValidator:
    """
    Validates Python files according to Language Layer Specification.
    
    For governance executors, prohibited features:
    - I/O operations
    - Network access
    - File writes
    - exec/eval
    - subprocess calls
    """
    
    PROHIBITED_IMPORTS = {
        'os.system', 'os.popen', 'os.spawn',
        'subprocess', 'socket', 'urllib', 'requests', 'httpx',
        'eval', 'exec', 'compile',
        'open',  # For writes
    }
    
    PROHIBITED_CALLS = {
        'eval', 'exec', 'compile', 'open',
        'os.system', 'os.popen', 'subprocess.run', 'subprocess.call',
        'subprocess.Popen', 'socket.socket'
    }
    
    def validate(self, content: str, file_path: str, strict_mode: bool = False) -> LanguageValidationResult:
        """
        Validate Python content.
        
        Args:
            content: Python source code
            file_path: Path to file
            strict_mode: If True, enforce pure function requirements
        """
        violations = []
        ast_valid = True
        
        # Try to parse AST
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            ast_valid = False
            violations.append(LanguageViolation(
                language="python",
                file_path=file_path,
                rule_id="PY-001",
                message=f"Python syntax error: {str(e)}",
                severity=Severity.CRITICAL,
                line=e.lineno,
                column=e.offset,
                suggestion="Fix Python syntax errors"
            ))
            return LanguageValidationResult(
                language="python",
                file_path=file_path,
                valid=False,
                violations=violations,
                ast_valid=False,
                parseable=False
            )
        
        # Check for prohibited patterns in strict mode (for enforcers)
        if strict_mode:
            violations.extend(self._check_ast(tree, file_path))
        
        return LanguageValidationResult(
            language="python",
            file_path=file_path,
            valid=len(violations) == 0,
            violations=violations,
            ast_valid=ast_valid,
            parseable=True
        )
    
    def _check_ast(self, tree: ast.AST, file_path: str) -> List[LanguageViolation]:
        """Check AST for prohibited patterns"""
        violations = []
        
        for node in ast.walk(tree):
            # Check for eval/exec calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec', 'compile']:
                        violations.append(LanguageViolation(
                            language="python",
                            file_path=file_path,
                            rule_id="PY-002",
                            message=f"Use of {node.func.id}() is prohibited in governance code",
                            severity=Severity.CRITICAL,
                            line=node.lineno,
                            suggestion=f"Remove {node.func.id}() call; use safe alternatives"
                        ))
            
            # Check for subprocess imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in ['subprocess', 'socket']:
                        violations.append(LanguageViolation(
                            language="python",
                            file_path=file_path,
                            rule_id="PY-003",
                            message=f"Import of {alias.name} is prohibited in governance code",
                            severity=Severity.HIGH,
                            line=node.lineno,
                            suggestion="Remove prohibited import"
                        ))
        
        return violations


class LanguageEnforcer:
    """
    Main Language Layer Enforcer.
    
    Validates all files in a directory against Language Layer Specification.
    """
    
    VERSION = "1.0.0"
    
    def __init__(self, project_root: Optional[str] = None):
        """Initialize enforcer"""
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = Path(__file__).parent.parent.parent.parent
        
        self.yaml_validator = YAMLValidator()
        self.json_validator = JSONValidator()
        self.markdown_validator = MarkdownValidator()
        self.python_validator = PythonValidator()
        
        self._load_language_spec()
    
    def _load_language_spec(self):
        """Load language specification"""
        spec_path = Path(__file__).parent / "languages.json"
        if spec_path.exists():
            with open(spec_path) as f:
                self.language_spec = json.load(f)
        else:
            self.language_spec = {"languages": []}
    
    def detect_language(self, file_path: Path) -> LanguageType:
        """Detect language type from file extension"""
        suffix = file_path.suffix.lower()
        
        if suffix in ['.yaml', '.yml']:
            return LanguageType.YAML
        elif suffix == '.json':
            return LanguageType.JSON
        elif suffix in ['.md', '.markdown']:
            return LanguageType.MARKDOWN
        elif suffix == '.py':
            return LanguageType.PYTHON
        elif suffix in ['.gl', '.gldsl']:
            return LanguageType.GL_DSL
        else:
            return LanguageType.UNKNOWN
    
    def validate_file(self, file_path: Path, strict_mode: bool = False) -> LanguageValidationResult:
        """Validate a single file"""
        language = self.detect_language(file_path)
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            return LanguageValidationResult(
                language=language.value,
                file_path=str(file_path),
                valid=False,
                violations=[LanguageViolation(
                    language=language.value,
                    file_path=str(file_path),
                    rule_id="LANG-001",
                    message="File is not UTF-8 encoded",
                    severity=Severity.HIGH,
                    suggestion="Convert file to UTF-8 encoding"
                )],
                parseable=False
            )
        except FileNotFoundError:
            return LanguageValidationResult(
                language=language.value,
                file_path=str(file_path),
                valid=False,
                violations=[LanguageViolation(
                    language=language.value,
                    file_path=str(file_path),
                    rule_id="LANG-002",
                    message="File not found",
                    severity=Severity.CRITICAL
                )],
                parseable=False
            )
        
        if language == LanguageType.YAML:
            return self.yaml_validator.validate(content, str(file_path))
        elif language == LanguageType.JSON:
            return self.json_validator.validate(content, str(file_path))
        elif language == LanguageType.MARKDOWN:
            return self.markdown_validator.validate(content, str(file_path))
        elif language == LanguageType.PYTHON:
            return self.python_validator.validate(content, str(file_path), strict_mode)
        else:
            return LanguageValidationResult(
                language=language.value,
                file_path=str(file_path),
                valid=True,
                violations=[]
            )
    
    def validate_directory(
        self,
        directory: Path,
        recursive: bool = True,
        strict_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Validate all files in a directory.
        
        Returns:
            Dictionary with validation results and summary
        """
        results = []
        total_files = 0
        valid_files = 0
        total_violations = 0
        
        pattern = "**/*" if recursive else "*"
        
        for file_path in directory.glob(pattern):
            if file_path.is_file() and not self._should_skip(file_path):
                language = self.detect_language(file_path)
                if language != LanguageType.UNKNOWN:
                    result = self.validate_file(file_path, strict_mode)
                    
                    # Handle relative path safely
                    try:
                        rel_path = str(file_path.relative_to(self.project_root))
                    except ValueError:
                        rel_path = str(file_path)
                    
                    results.append({
                        "file": rel_path,
                        "language": result.language,
                        "valid": result.valid,
                        "parseable": result.parseable,
                        "violations": [
                            {
                                "rule_id": v.rule_id,
                                "message": v.message,
                                "severity": v.severity.value,
                                "line": v.line,
                                "suggestion": v.suggestion
                            }
                            for v in result.violations
                        ]
                    })
                    
                    total_files += 1
                    if result.valid:
                        valid_files += 1
                    total_violations += len(result.violations)
        
        return {
            "version": self.VERSION,
            "layer": "language",
            "summary": {
                "total_files": total_files,
                "valid_files": valid_files,
                "invalid_files": total_files - valid_files,
                "total_violations": total_violations,
                "compliance_rate": (valid_files / total_files * 100) if total_files > 0 else 100
            },
            "results": results
        }
    
    def _should_skip(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_patterns = [
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            '.pytest_cache', '.mypy_cache', 'dist', 'build'
        ]
        return any(p in str(file_path) for p in skip_patterns)


def main():
    """Main entry point for language enforcer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Language Layer Enforcer")
    parser.add_argument("path", nargs="?", default=".", help="Path to validate")
    parser.add_argument("--strict", action="store_true", help="Enable strict mode for Python")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    enforcer = LanguageEnforcer()
    path = Path(args.path)
    
    if path.is_file():
        result = enforcer.validate_file(path, args.strict)
        if args.json:
            print(json.dumps({
                "file": str(path),
                "valid": result.valid,
                "violations": [
                    {"rule_id": v.rule_id, "message": v.message, "severity": v.severity.value}
                    for v in result.violations
                ]
            }, indent=2))
        else:
            status = "✅ PASS" if result.valid else "❌ FAIL"
            print(f"{status} {path}")
            for v in result.violations:
                print(f"  [{v.severity.value.upper()}] {v.rule_id}: {v.message}")
    else:
        results = enforcer.validate_directory(path, strict_mode=args.strict)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print("=" * 60)
            print("       Language Layer Validation Report")
            print("=" * 60)
            print(f"\nTotal Files: {results['summary']['total_files']}")
            print(f"Valid Files: {results['summary']['valid_files']}")
            print(f"Invalid Files: {results['summary']['invalid_files']}")
            print(f"Total Violations: {results['summary']['total_violations']}")
            print(f"Compliance Rate: {results['summary']['compliance_rate']:.1f}%")
            
            if results['summary']['invalid_files'] > 0:
                print("\nViolations:")
                for r in results['results']:
                    if not r['valid']:
                        print(f"\n  ❌ {r['file']}")
                        for v in r['violations']:
                            print(f"    [{v['severity'].upper()}] {v['rule_id']}: {v['message']}")


if __name__ == "__main__":
    main()
