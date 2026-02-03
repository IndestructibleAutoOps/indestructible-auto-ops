# @GL-semantic: org.mnga.engines.validation@1.0.0
# @GL-audit-trail: enabled
"""
Validation Engine - Validate governance specifications
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class ValidationSeverity(Enum):
    """Severity levels for validation errors"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationError:
    """Represents a validation error"""
    rule_id: str
    severity: ValidationSeverity
    message: str
    file_path: str
    line_number: Optional[int] = None
    context: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of validation operation"""
    success: bool
    total_files: int = 0
    valid_files: int = 0
    invalid_files: int = 0
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')


class ValidationEngine:
    """
    Validation Engine for governance specifications.
    
    This engine validates all governance specifications for compliance
    with GL governance rules and best practices.
    """
    
    def __init__(self, workspace_root: str = "/workspace"):
        """
        Initialize Validation Engine
        
        Args:
            workspace_root: Root directory of the workspace
        """
        self.workspace_root = workspace_root
        self.governance_root = os.path.join(workspace_root, "ecosystem", "governance")
        
        # Define validation rules
        self.rules = self._define_rules()
    
    def validate_all(self) -> ValidationResult:
        """
        Validate all governance specifications
        
        Returns:
            ValidationResult with validation details
        """
        result = ValidationResult(success=True)
        
        print("=== Validation Engine: Starting Validation ===")
        print(f"Workspace: {self.workspace_root}")
        print(f"Governance Root: {self.governance_root}")
        print()
        
        # Step 1: Scan all specification files
        print("Step 1: Scanning specification files...")
        spec_files = self._scan_spec_files()
        result.total_files = len(spec_files)
        print(f"Found {len(spec_files)} specification files")
        print()
        
        # Step 2: Validate each file
        print("Step 2: Validating specifications...")
        for spec_file in spec_files:
            file_result = self._validate_file(spec_file)
            
            if file_result['valid']:
                result.valid_files += 1
                print(f"  ✓ {spec_file}")
            else:
                result.invalid_files += 1
                print(f"  ✗ {spec_file}")
                
                # Add errors and warnings
                for error in file_result['errors']:
                    if error.severity == ValidationSeverity.ERROR:
                        result.errors.append(error)
                    else:
                        result.warnings.append(error)
        
        print()
        
        # Step 3: Generate summary
        print("=== Validation Summary ===")
        print(f"Total files: {result.total_files}")
        print(f"Valid: {result.valid_files}")
        print(f"Invalid: {result.invalid_files}")
        print(f"Errors: {len(result.errors)}")
        print(f"Warnings: {len(result.warnings)}")
        print(f"Timestamp: {result.timestamp}")
        print()
        
        # Determine overall success
        if result.errors:
            result.success = False
            print("Errors found:")
            for error in result.errors:
                print(f"  [{error.severity.value.upper()}] {error.rule_id}: {error.message}")
                print(f"    File: {error.file_path}")
                if error.line_number:
                    print(f"    Line: {error.line_number}")
                print()
        
        if result.warnings:
            print("Warnings:")
            for warning in result.warnings:
                print(f"  [{warning.severity.value.upper()}] {warning.rule_id}: {warning.message}")
                print(f"    File: {warning.file_path}")
                print()
        
        return result
    
    def _define_rules(self) -> List[Dict[str, Any]]:
        """
        Define validation rules
        
        Returns:
            List of rule definitions
        """
        return [
            {
                "id": "GL_VAL_001",
                "name": "gl_semantic_marker_required",
                "severity": ValidationSeverity.ERROR,
                "description": "All specifications must have @GL-semantic marker",
                "check": self._check_gl_semantic_marker
            },
            {
                "id": "GL_VAL_002",
                "name": "gl_audit_trail_marker_required",
                "severity": ValidationSeverity.ERROR,
                "description": "All specifications must have @GL-audit-trail marker",
                "check": self._check_gl_audit_trail_marker
            },
            {
                "id": "GL_VAL_003",
                "name": "spec_id_required",
                "severity": ValidationSeverity.ERROR,
                "description": "All specifications must have spec_id field",
                "check": self._check_spec_id
            },
            {
                "id": "GL_VAL_004",
                "name": "spec_id_format_valid",
                "severity": ValidationSeverity.ERROR,
                "description": "spec_id must follow format: org.mnga.[component]@[version]",
                "check": self._check_spec_id_format
            },
            {
                "id": "GL_VAL_005",
                "name": "audit_trail_section_required",
                "severity": ValidationSeverity.ERROR,
                "description": "All specifications must have audit_trail section",
                "check": self._check_audit_trail_section
            },
            {
                "id": "GL_VAL_006",
                "name": "checksum_required",
                "severity": ValidationSeverity.WARNING,
                "description": "audit_trail should have checksum field",
                "check": self._check_checksum
            },
            {
                "id": "GL_VAL_007",
                "name": "naming_convention_snake_case",
                "severity": ValidationSeverity.WARNING,
                "description": "Field names should use snake_case convention",
                "check": self._check_naming_convention
            },
            {
                "id": "GL_VAL_008",
                "name": "no_external_dependencies",
                "severity": ValidationSeverity.ERROR,
                "description": "Specifications should not reference external dependencies",
                "check": self._check_no_external_dependencies
            },
            {
                "id": "GL_VAL_009",
                "name": "immutable_layer_protection",
                "severity": ValidationSeverity.WARNING,
                "description": "Immutable layers should have immutable: true",
                "check": self._check_immutable_layer
            },
            {
                "id": "GL_VAL_010",
                "name": "version_format_valid",
                "severity": ValidationSeverity.ERROR,
                "description": "Version must follow semantic versioning (x.y.z)",
                "check": self._check_version_format
            }
        ]
    
    def _scan_spec_files(self) -> List[str]:
        """
        Scan for all specification files
        
        Returns:
            List of specification file paths (relative to workspace)
        """
        spec_files = []
        
        patterns = [
            "**/*.spec.yaml",
            "**/*.spec.json",
            "**/*.schema.json",
            "**/meta*.json",
            "**/registry.json",
            "**/topology*.yaml",
            "**/semantics*.yaml",
            "**/index*.yaml",
            "**/tokens.yaml",
            "**/ast.yaml"
        ]
        
        for root, dirs, files in os.walk(self.governance_root):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.workspace_root)
                
                for pattern in patterns:
                    if self._matches_pattern(rel_path, pattern):
                        spec_files.append(rel_path)
                        break
        
        return sorted(spec_files)
    
    def _matches_pattern(self, file_path: str, pattern: str) -> bool:
        """Check if file path matches pattern"""
        if pattern.startswith("**/"):
            suffix = pattern[3:]
            return file_path.endswith(suffix)
        elif pattern.endswith("/*"):
            prefix = pattern[:-2]
            return file_path.startswith(prefix)
        else:
            return file_path == pattern
    
    def _validate_file(self, file_path: str) -> Dict[str, Any]:
        """
        Validate a single file
        
        Args:
            file_path: Path to file (relative to workspace)
            
        Returns:
            Dict with validation result
        """
        result = {
            "valid": True,
            "errors": []
        }
        
        full_path = os.path.join(self.workspace_root, file_path)
        
        # Read file content
        try:
            with open(full_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            error = ValidationError(
                rule_id="FILE_READ_ERROR",
                severity=ValidationSeverity.ERROR,
                message=f"Could not read file: {str(e)}",
                file_path=file_path
            )
            result["errors"].append(error)
            result["valid"] = False
            return result
        
        # Apply all rules
        for rule in self.rules:
            try:
                rule_errors = rule["check"](file_path, content, lines)
                for error in rule_errors:
                    result["errors"].append(error)
                    if error.severity == ValidationSeverity.ERROR:
                        result["valid"] = False
            except Exception as e:
                error = ValidationError(
                    rule_id=rule["id"],
                    severity=ValidationSeverity.ERROR,
                    message=f"Rule execution failed: {str(e)}",
                    file_path=file_path
                )
                result["errors"].append(error)
                result["valid"] = False
        
        return result
    
    def _check_gl_semantic_marker(self, file_path: str, content: str, lines: List[str]) -> List[ValidationError]:
        """Check for @GL-semantic marker"""
        errors = []
        
        if '@GL-semantic' not in content:
            error = ValidationError(
                rule_id="GL_VAL_001",
                severity=ValidationSeverity.ERROR,
                message="Missing @GL-semantic marker",
                file_path=file_path,
                line_number=1
            )
            errors.append(error)
        
        return errors
    
    def _check_gl_audit_trail_marker(self, file_path: str, content: str, lines: List[str]) -> List[ValidationError]:
        """Check for @GL-audit-trail marker"""
        errors = []
        
        if '@GL-audit-trail' not in content:
            error = ValidationError(
                rule_id="GL_VAL_002",
                severity=ValidationSeverity.ERROR,
                message="Missing @GL-audit-trail marker",
                file_path=file_path,
                line_number=1
            )
            errors.append(error)
        
        return errors
    
    def _check_spec_id(self, file_path: str, content: str, lines: List[str]) -> List[ValidationError]:
        """Check for spec_id field"""
        errors = []
        
        if 'spec_id:' not in content and '"spec_id"' not in content:
            error = ValidationError(
                rule_id="GL_VAL_003",
                severity=ValidationSeverity.ERROR,
                message="Missing spec_id field",
                file_path=file_path
            )
            errors.append(error)
        
        return errors
    
    def _check_spec_id_format(self, file_path: str, content: str, lines: List[str]) -> List[ValidationError]:
        """Check spec_id format"""
        errors = []
        
        # Extract spec_id value
        spec_id_match = re.search(r'spec_id:\s*([^\s\n]+)|"spec_id":\s*"([^"]+)"', content)
        if spec_id_match:
            spec_id = spec_id_match.group(1) or spec_id_match.group(2)
            
            # Check format: org.mnga.[component]@[version]
            pattern = r'^org\.mnga\.[^@]+@\d+\.\d+\.\d+$'
            if not re.match(pattern, spec_id):
                error = ValidationError(
                    rule_id="GL_VAL_004",
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid spec_id format: {spec_id}. Expected: org.mnga.[component]@[version]",
                    file_path=file_path
                )
                errors.append(error)
        
        return errors
    
    def _check_audit_trail_section(self, file_path: str, content: str, lines: List[str]) -> List[ValidationError]:
        """Check for audit_trail section"""
        errors = []
        
        if 'audit_trail:' not in content and '"audit_trail"' not in content:
            error = ValidationError(
                rule_id="GL_VAL_005",
                severity=ValidationSeverity.ERROR,
                message="Missing audit_trail section",
                file_path=file_path
            )
            errors.append(error)
        
        return errors
    
    def _check_checksum(self, file_path: str, content: str, lines: List[str]) -> List[ValidationError]:
        """Check for checksum field"""
        errors = []
        
        if 'checksum:' not in content and '"checksum"' not in content:
            error = ValidationError(
                rule_id="GL_VAL_006",
                severity=ValidationSeverity.WARNING,
                message="Missing checksum field in audit_trail",
                file_path=file_path
            )
            errors.append(error)
        
        return errors
    
    def _check_naming_convention(self, file_path: str, content: str, lines: List[str]) -> List[ValidationError]:
        """Check snake_case naming convention"""
        errors = []
        
        # Skip JSON files (they use camelCase)
        if file_path.endswith('.json'):
            return errors
        
        # Check for camelCase in YAML keys
        camel_case_pattern = r'^\s*[a-z]+[A-Z][a-zA-Z]*:'
        for i, line in enumerate(lines, 1):
            if re.match(camel_case_pattern, line):
                # Skip comments
                if not line.strip().startswith('#'):
                    error = ValidationError(
                        rule_id="GL_VAL_007",
                        severity=ValidationSeverity.WARNING,
                        message=f"Field name should use snake_case convention",
                        file_path=file_path,
                        line_number=i,
                        context=line.strip()
                    )
                    errors.append(error)
        
        return errors
    
    def _check_no_external_dependencies(self, file_path: str, content: str, lines: List[str]) -> List[ValidationError]:
        """Check for external dependencies"""
        errors = []
        
        # Common external dependency patterns
        external_patterns = [
            r'import\s+(numpy|pandas|requests|pyyaml|yaml)',
            r'from\s+(numpy|pandas|requests|pyyaml|yaml)',
            r'require\(["\']',
            r'pip install',
            r'npm install'
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern in external_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Skip comments
                    if not line.strip().startswith('#'):
                        error = ValidationError(
                            rule_id="GL_VAL_008",
                            severity=ValidationSeverity.ERROR,
                            message=f"External dependency detected: {line.strip()}",
                            file_path=file_path,
                            line_number=i,
                            context=line.strip()
                        )
                        errors.append(error)
        
        return errors
    
    def _check_immutable_layer(self, file_path: str, content: str, lines: List[str]) -> List[ValidationError]:
        """Check immutable layer protection"""
        errors = []
        
        # Check if file is in an immutable layer
        immutable_layers = ['l00', 'l01', 'l02', 'l03', 'l04', 'l50']
        is_immutable_layer = any(f'/{layer}/' in file_path.lower() for layer in immutable_layers)
        
        if is_immutable_layer:
            if 'immutable:' not in content and '"immutable"' not in content:
                error = ValidationError(
                    rule_id="GL_VAL_009",
                    severity=ValidationSeverity.WARNING,
                    message="Immutable layer should have immutable: true field",
                    file_path=file_path
                )
                errors.append(error)
        
        return errors
    
    def _check_version_format(self, file_path: str, content: str, lines: List[str]) -> List[ValidationError]:
        """Check version format"""
        errors = []
        
        # Extract version values - more specific pattern to avoid false positives
        # Match only actual version fields, not regex patterns or comments
        version_matches = re.findall(r'^\s*version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$|^\s*"version":\s*"([0-9]+\.[0-9]+\.[0-9]+)"\s*$', content, re.MULTILINE)
        
        for match in version_matches:
            version = match[0] or match[1]
            
            # Check semantic versioning format
            if version and not re.match(r'^\d+\.\d+\.\d+$', version):
                error = ValidationError(
                    rule_id="GL_VAL_010",
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid version format: {version}. Expected: x.y.z",
                    file_path=file_path
                )
                errors.append(error)
        
        return errors


def main():
    """Main entry point for validation engine"""
    engine = ValidationEngine()
    result = engine.validate_all()
    
    if result.success:
        print("✓ Validation completed successfully")
        return 0
    else:
        print("✗ Validation completed with errors")
        return 1


if __name__ == "__main__":
    exit(main())