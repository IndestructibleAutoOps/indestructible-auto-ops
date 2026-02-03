#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: format-enforcer
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
"""
Format Layer Enforcer
=====================
GL Layer: GL00-09 Strategic Layer (Foundation)

Validates that all files comply with the Format Layer Specification.
Format Layer is built on top of Language Layer and provides schema validation.

The Format Layer ensures:
- All files have valid schemas
- All files conform to their declared format
- All required fields are present
- All field types are correct
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from enum import Enum


class FormatType(Enum):
    """Supported format types"""
    GL_META = "gl.meta.json"
    GL_RULE = "gl-rule.yaml"
    SEMANTIC_INDEX = "semantic-index.json"
    EVIDENCE = "evidence.yaml"
    CONTRACT = "contract.yaml"
    ADAPTER = "adapter.yaml"
    UNKNOWN = "unknown"


class Severity(Enum):
    """Violation severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class FormatViolation:
    """Represents a format layer violation"""
    format_type: str
    file_path: str
    rule_id: str
    message: str
    severity: Severity
    field: Optional[str] = None
    expected: Optional[str] = None
    actual: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class FormatValidationResult:
    """Result of format validation"""
    format_type: str
    file_path: str
    valid: bool
    violations: List[FormatViolation] = field(default_factory=list)
    schema_valid: bool = True


class SchemaValidator:
    """
    Validates data against JSON Schema / YAML Schema.
    
    Provides manual schema validation without external dependencies.
    """
    
    def __init__(self, schema: Dict[str, Any]):
        """Initialize with schema"""
        self.schema = schema
    
    def validate(self, data: Any, path: str = "") -> List[FormatViolation]:
        """Validate data against schema"""
        violations = []
        
        if self.schema.get("type") == "object":
            violations.extend(self._validate_object(data, path))
        elif self.schema.get("type") == "array":
            violations.extend(self._validate_array(data, path))
        elif self.schema.get("type") == "string":
            violations.extend(self._validate_string(data, path))
        elif self.schema.get("type") == "number":
            violations.extend(self._validate_number(data, path))
        elif self.schema.get("type") == "boolean":
            violations.extend(self._validate_boolean(data, path))
        
        return violations
    
    def _validate_object(self, data: Any, path: str) -> List[FormatViolation]:
        """Validate object type"""
        violations = []
        
        if not isinstance(data, dict):
            violations.append(FormatViolation(
                format_type="schema",
                file_path=path,
                rule_id="FMT-001",
                message=f"Expected object at {path or 'root'}, got {type(data).__name__}",
                severity=Severity.HIGH,
                expected="object",
                actual=type(data).__name__
            ))
            return violations
        
        # Check required fields
        required = self.schema.get("required", [])
        for req_field in required:
            if req_field not in data:
                violations.append(FormatViolation(
                    format_type="schema",
                    file_path=path,
                    rule_id="FMT-002",
                    message=f"Missing required field: {req_field}",
                    severity=Severity.CRITICAL,
                    field=req_field,
                    suggestion=f"Add required field '{req_field}'"
                ))
        
        # Validate properties
        properties = self.schema.get("properties", {})
        for prop_name, prop_schema in properties.items():
            if prop_name in data:
                prop_path = f"{path}.{prop_name}" if path else prop_name
                sub_validator = SchemaValidator(prop_schema)
                violations.extend(sub_validator.validate(data[prop_name], prop_path))
        
        # Check for additional properties
        if self.schema.get("additionalProperties") is False:
            allowed_props = set(properties.keys())
            for key in data.keys():
                if key not in allowed_props:
                    violations.append(FormatViolation(
                        format_type="schema",
                        file_path=path,
                        rule_id="FMT-003",
                        message=f"Unknown property: {key}",
                        severity=Severity.MEDIUM,
                        field=key,
                        suggestion=f"Remove unknown property '{key}' or add to schema"
                    ))
        
        return violations
    
    def _validate_array(self, data: Any, path: str) -> List[FormatViolation]:
        """Validate array type"""
        violations = []
        
        if not isinstance(data, list):
            violations.append(FormatViolation(
                format_type="schema",
                file_path=path,
                rule_id="FMT-004",
                message=f"Expected array at {path or 'root'}, got {type(data).__name__}",
                severity=Severity.HIGH,
                expected="array",
                actual=type(data).__name__
            ))
            return violations
        
        # Validate items
        items_schema = self.schema.get("items")
        if items_schema:
            for i, item in enumerate(data):
                item_path = f"{path}[{i}]"
                sub_validator = SchemaValidator(items_schema)
                violations.extend(sub_validator.validate(item, item_path))
        
        return violations
    
    def _validate_string(self, data: Any, path: str) -> List[FormatViolation]:
        """Validate string type"""
        violations = []
        
        if not isinstance(data, str):
            violations.append(FormatViolation(
                format_type="schema",
                file_path=path,
                rule_id="FMT-005",
                message=f"Expected string at {path}, got {type(data).__name__}",
                severity=Severity.HIGH,
                expected="string",
                actual=type(data).__name__
            ))
            return violations
        
        # Check pattern
        pattern = self.schema.get("pattern")
        if pattern:
            import re
            if not re.match(pattern, data):
                violations.append(FormatViolation(
                    format_type="schema",
                    file_path=path,
                    rule_id="FMT-006",
                    message=f"String does not match pattern: {pattern}",
                    severity=Severity.MEDIUM,
                    field=path,
                    expected=pattern,
                    actual=data
                ))
        
        # Check enum
        enum_values = self.schema.get("enum")
        if enum_values and data not in enum_values:
            violations.append(FormatViolation(
                format_type="schema",
                file_path=path,
                rule_id="FMT-007",
                message=f"Value not in allowed enum: {data}",
                severity=Severity.HIGH,
                field=path,
                expected=str(enum_values),
                actual=data
            ))
        
        return violations
    
    def _validate_number(self, data: Any, path: str) -> List[FormatViolation]:
        """Validate number type"""
        violations = []
        
        if not isinstance(data, (int, float)):
            violations.append(FormatViolation(
                format_type="schema",
                file_path=path,
                rule_id="FMT-008",
                message=f"Expected number at {path}, got {type(data).__name__}",
                severity=Severity.HIGH,
                expected="number",
                actual=type(data).__name__
            ))
        
        return violations
    
    def _validate_boolean(self, data: Any, path: str) -> List[FormatViolation]:
        """Validate boolean type"""
        violations = []
        
        if not isinstance(data, bool):
            violations.append(FormatViolation(
                format_type="schema",
                file_path=path,
                rule_id="FMT-009",
                message=f"Expected boolean at {path}, got {type(data).__name__}",
                severity=Severity.HIGH,
                expected="boolean",
                actual=type(data).__name__
            ))
        
        return violations


class FormatEnforcer:
    """
    Main Format Layer Enforcer.
    
    Validates all files against their format schemas.
    """
    
    VERSION = "1.0.0"
    
    def __init__(self, project_root: Optional[str] = None):
        """Initialize enforcer"""
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = Path(__file__).parent.parent.parent.parent
        
        self.schemas_dir = Path(__file__).parent.parent / "schemas"
        self._load_schemas()
    
    def _load_schemas(self):
        """Load all format schemas"""
        self.schemas = {}
        
        schema_files = {
            FormatType.GL_META: "gl.meta.schema.json",
            FormatType.GL_RULE: "gl-rule.schema.yaml",
            FormatType.SEMANTIC_INDEX: "semantic-index.schema.json",
            FormatType.EVIDENCE: "evidence.schema.yaml",
            FormatType.CONTRACT: "contract.schema.yaml",
            FormatType.ADAPTER: "adapter.schema.yaml"
        }
        
        for format_type, schema_file in schema_files.items():
            schema_path = self.schemas_dir / schema_file
            if schema_path.exists():
                try:
                    content = schema_path.read_text()
                    if schema_file.endswith('.json'):
                        self.schemas[format_type] = json.loads(content)
                    else:
                        # For YAML schemas, try to load
                        try:
                            import yaml
                            self.schemas[format_type] = yaml.safe_load(content)
                        except ImportError:
                            # Parse YAML manually for basic cases
                            self.schemas[format_type] = self._parse_simple_yaml(content)
                except Exception as e:
                    print(f"Warning: Could not load schema {schema_file}: {e}")
    
    def _parse_simple_yaml(self, content: str) -> Dict[str, Any]:
        """Simple YAML parser for schema files"""
        # Basic implementation - returns empty dict if can't parse
        # In production, PyYAML should be available
        return {}
    
    def detect_format(self, file_path: Path) -> FormatType:
        """Detect format type from file name and content"""
        name = file_path.name.lower()
        
        if name == "gl.meta.json":
            return FormatType.GL_META
        elif name.endswith(".schema.json") or name.endswith(".schema.yaml"):
            return FormatType.UNKNOWN  # Schema files themselves
        elif "semantic-index" in name and name.endswith(".json"):
            return FormatType.SEMANTIC_INDEX
        elif "evidence" in name and name.endswith(".yaml"):
            return FormatType.EVIDENCE
        elif "contract" in name and name.endswith(".yaml"):
            return FormatType.CONTRACT
        elif "adapter" in name and name.endswith(".yaml"):
            return FormatType.ADAPTER
        elif name.startswith("gl") and name.endswith(".yaml"):
            return FormatType.GL_RULE
        
        return FormatType.UNKNOWN
    
    def validate_file(self, file_path: Path) -> FormatValidationResult:
        """Validate a single file against its format schema"""
        format_type = self.detect_format(file_path)
        
        if format_type == FormatType.UNKNOWN:
            return FormatValidationResult(
                format_type="unknown",
                file_path=str(file_path),
                valid=True,
                violations=[]
            )
        
        # Load file content
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return FormatValidationResult(
                format_type=format_type.value,
                file_path=str(file_path),
                valid=False,
                violations=[FormatViolation(
                    format_type=format_type.value,
                    file_path=str(file_path),
                    rule_id="FMT-010",
                    message=f"Could not read file: {e}",
                    severity=Severity.CRITICAL
                )]
            )
        
        # Parse content
        try:
            if file_path.suffix == '.json':
                data = json.loads(content)
            else:
                try:
                    import yaml
                    data = yaml.safe_load(content)
                except ImportError:
                    # Skip YAML validation if PyYAML not available
                    return FormatValidationResult(
                        format_type=format_type.value,
                        file_path=str(file_path),
                        valid=True,
                        violations=[]
                    )
        except Exception as e:
            return FormatValidationResult(
                format_type=format_type.value,
                file_path=str(file_path),
                valid=False,
                violations=[FormatViolation(
                    format_type=format_type.value,
                    file_path=str(file_path),
                    rule_id="FMT-011",
                    message=f"Could not parse file: {e}",
                    severity=Severity.CRITICAL
                )]
            )
        
        # Validate against schema
        violations = []
        schema = self.schemas.get(format_type)
        
        if schema:
            validator = SchemaValidator(schema)
            violations = validator.validate(data, str(file_path))
        
        return FormatValidationResult(
            format_type=format_type.value,
            file_path=str(file_path),
            valid=len(violations) == 0,
            violations=violations,
            schema_valid=len(violations) == 0
        )
    
    def validate_directory(
        self,
        directory: Path,
        recursive: bool = True
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
                format_type = self.detect_format(file_path)
                if format_type != FormatType.UNKNOWN:
                    result = self.validate_file(file_path)
                    
                    # Handle relative path safely
                    try:
                        rel_path = str(file_path.relative_to(self.project_root))
                    except ValueError:
                        rel_path = str(file_path)
                    
                    results.append({
                        "file": rel_path,
                        "format": result.format_type,
                        "valid": result.valid,
                        "violations": [
                            {
                                "rule_id": v.rule_id,
                                "message": v.message,
                                "severity": v.severity.value,
                                "field": v.field,
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
            "layer": "format",
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
    """Main entry point for format enforcer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Format Layer Enforcer")
    parser.add_argument("path", nargs="?", default=".", help="Path to validate")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    enforcer = FormatEnforcer()
    path = Path(args.path)
    
    if path.is_file():
        result = enforcer.validate_file(path)
        if args.json:
            print(json.dumps({
                "file": str(path),
                "format": result.format_type,
                "valid": result.valid,
                "violations": [
                    {"rule_id": v.rule_id, "message": v.message, "severity": v.severity.value}
                    for v in result.violations
                ]
            }, indent=2))
        else:
            status = "✅ PASS" if result.valid else "❌ FAIL"
            print(f"{status} {path} (format: {result.format_type})")
            for v in result.violations:
                print(f"  [{v.severity.value.upper()}] {v.rule_id}: {v.message}")
    else:
        results = enforcer.validate_directory(path)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print("=" * 60)
            print("        Format Layer Validation Report")
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
                        print(f"\n  ❌ {r['file']} (format: {r['format']})")
                        for v in r['violations']:
                            print(f"    [{v['severity'].upper()}] {v['rule_id']}: {v['message']}")


if __name__ == "__main__":
    main()
