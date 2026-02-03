#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: autofix-engine
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
"""
AutoFix Engine
==============
GL Layer: GL30-49 Execution Layer

Automatic violation remediation engine for governance enforcement.

Features:
- Rule-based automatic fixes
- Naming convention corrections
- Configuration drift remediation
- Audit trail of all changes
- Safe mode for preview without changes
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field


@dataclass
class Violation:
    """Represents a governance violation"""
    rule_id: str
    file: str
    line: Optional[int] = None
    column: Optional[int] = None
    severity: str = "MEDIUM"
    message: str = ""
    suggestion: str = ""
    fixable: bool = True


@dataclass
class FixResult:
    """Result of an auto-fix attempt"""
    violation: Violation
    fixed: bool
    original: str = ""
    replacement: str = ""
    error: Optional[str] = None


@dataclass
class AutoFixReport:
    """Report of auto-fix execution"""
    timestamp: str
    total_violations: int
    fixed_count: int
    failed_count: int
    skipped_count: int
    fixes: List[Dict]
    errors: List[str]
    

class AutoFixEngine:
    """
    Automatic violation remediation engine.
    
    Supports:
    - Naming convention fixes (NAM-*)
    - Configuration fixes (CFG-*)
    - Documentation fixes (DOC-*)
    - Security fixes (SEC-*)
    """
    
    VERSION = "1.0.0"
    
    # Naming pattern rules
    NAMING_RULES = {
        "NAM-001": {
            "description": "Class names must be PascalCase",
            "pattern": r"class\s+([a-z_][a-zA-Z0-9_]*)\s*[:\(]",
            "fix_func": "_fix_class_name"
        },
        "NAM-002": {
            "description": "Function names must be snake_case",
            "pattern": r"def\s+([A-Z][a-zA-Z0-9_]*)\s*\(",
            "fix_func": "_fix_function_name"
        },
        "NAM-003": {
            "description": "Constants must be UPPER_SNAKE_CASE",
            "pattern": r"^([a-z][a-z0-9_]*)\s*=\s*['\"\d]",
            "fix_func": "_fix_constant_name"
        },
        "NAM-004": {
            "description": "Variable names must be snake_case",
            "pattern": r"([A-Z][a-z]+[A-Z][a-zA-Z0-9]*)\s*=",
            "fix_func": "_fix_variable_name"
        }
    }
    
    # Configuration rules
    CONFIG_RULES = {
        "CFG-001": {
            "description": "Configuration files must have version field",
            "fix_func": "_fix_config_version"
        },
        "CFG-002": {
            "description": "YAML files must use consistent indentation",
            "fix_func": "_fix_yaml_indentation"
        }
    }
    
    def __init__(self, project_root: Optional[str] = None, safe_mode: bool = True):
        """
        Initialize AutoFix engine.
        
        Args:
            project_root: Project root directory
            safe_mode: If True, preview changes without applying
        """
        self.project_root = Path(project_root) if project_root else self._detect_project_root()
        self.safe_mode = safe_mode
        self.fixes_applied: List[FixResult] = []
        self.errors: List[str] = []
    
    def _detect_project_root(self) -> Path:
        """Auto-detect project root"""
        current = Path(__file__).parent
        while current != current.parent:
            if (current / "governance-manifest.yaml").exists():
                return current
            if (current / "ecosystem").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    @staticmethod
    def get_timestamp() -> str:
        """Get UTC timestamp in RFC3339 format"""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def load_violations_from_report(self, report_path: str) -> List[Violation]:
        """
        Load violations from audit report JSON.
        
        Args:
            report_path: Path to audit report JSON
            
        Returns:
            List of Violation objects
        """
        violations = []
        
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            for v in report.get("violations", []):
                violations.append(Violation(
                    rule_id=v.get("rule_id", "UNKNOWN"),
                    file=v.get("file", ""),
                    line=v.get("line"),
                    column=v.get("column"),
                    severity=v.get("severity", "MEDIUM"),
                    message=v.get("message", ""),
                    suggestion=v.get("suggestion", ""),
                    fixable=v.get("fixable", True)
                ))
        except Exception as e:
            self.errors.append(f"Failed to load violations from {report_path}: {str(e)}")
        
        return violations
    
    def fix_violations(self, violations: List[Violation]) -> AutoFixReport:
        """
        Attempt to fix all violations.
        
        Args:
            violations: List of violations to fix
            
        Returns:
            AutoFixReport with results
        """
        fixed_count = 0
        failed_count = 0
        skipped_count = 0
        fixes = []
        
        for violation in violations:
            if not violation.fixable:
                skipped_count += 1
                continue
            
            result = self._fix_violation(violation)
            
            if result.fixed:
                fixed_count += 1
            elif result.error:
                failed_count += 1
            else:
                skipped_count += 1
            
            fixes.append(asdict(result))
            self.fixes_applied.append(result)
        
        return AutoFixReport(
            timestamp=self.get_timestamp(),
            total_violations=len(violations),
            fixed_count=fixed_count,
            failed_count=failed_count,
            skipped_count=skipped_count,
            fixes=fixes,
            errors=self.errors
        )
    
    def _fix_violation(self, violation: Violation) -> FixResult:
        """
        Fix a single violation.
        
        Args:
            violation: Violation to fix
            
        Returns:
            FixResult with outcome
        """
        rule_prefix = violation.rule_id.split("-")[0] if "-" in violation.rule_id else ""
        
        if rule_prefix == "NAM":
            return self._fix_naming_violation(violation)
        elif rule_prefix == "CFG":
            return self._fix_config_violation(violation)
        elif rule_prefix == "DOC":
            return self._fix_documentation_violation(violation)
        else:
            return FixResult(
                violation=violation,
                fixed=False,
                error=f"No fix handler for rule type: {rule_prefix}"
            )
    
    def _fix_naming_violation(self, violation: Violation) -> FixResult:
        """Fix naming convention violations"""
        rule = self.NAMING_RULES.get(violation.rule_id)
        
        if not rule:
            return FixResult(
                violation=violation,
                fixed=False,
                error=f"Unknown naming rule: {violation.rule_id}"
            )
        
        file_path = self.project_root / violation.file
        
        if not file_path.exists():
            return FixResult(
                violation=violation,
                fixed=False,
                error=f"File not found: {violation.file}"
            )
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get fix function
            fix_func = getattr(self, rule["fix_func"], None)
            
            if not fix_func:
                return FixResult(
                    violation=violation,
                    fixed=False,
                    error=f"Fix function not found: {rule['fix_func']}"
                )
            
            # Apply fix
            new_content, original, replacement = fix_func(content, violation)
            
            if new_content != content:
                if not self.safe_mode:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                
                return FixResult(
                    violation=violation,
                    fixed=True,
                    original=original,
                    replacement=replacement
                )
            
            return FixResult(
                violation=violation,
                fixed=False,
                error="No changes needed or pattern not found"
            )
            
        except Exception as e:
            return FixResult(
                violation=violation,
                fixed=False,
                error=str(e)
            )
    
    def _fix_class_name(self, content: str, violation: Violation) -> Tuple[str, str, str]:
        """Fix class name to PascalCase"""
        pattern = r"class\s+([a-z_][a-zA-Z0-9_]*)\s*([:\(])"
        
        def to_pascal_case(match):
            name = match.group(1)
            # Convert snake_case to PascalCase
            parts = name.split('_')
            pascal = ''.join(part.capitalize() for part in parts)
            return f"class {pascal}{match.group(2)}"
        
        new_content = re.sub(pattern, to_pascal_case, content, count=1)
        
        # Find original
        match = re.search(pattern, content)
        original = match.group(1) if match else ""
        
        # Find replacement
        match_new = re.search(r"class\s+([A-Z][a-zA-Z0-9]*)\s*[:\(]", new_content)
        replacement = match_new.group(1) if match_new else ""
        
        return new_content, original, replacement
    
    def _fix_function_name(self, content: str, violation: Violation) -> Tuple[str, str, str]:
        """Fix function name to snake_case"""
        pattern = r"def\s+([A-Z][a-zA-Z0-9_]*)\s*\("
        
        def to_snake_case(match):
            name = match.group(1)
            # Convert PascalCase/camelCase to snake_case
            snake = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
            return f"def {snake}("
        
        new_content = re.sub(pattern, to_snake_case, content, count=1)
        
        match = re.search(pattern, content)
        original = match.group(1) if match else ""
        
        match_new = re.search(r"def\s+([a-z_][a-z0-9_]*)\s*\(", new_content)
        replacement = match_new.group(1) if match_new else ""
        
        return new_content, original, replacement
    
    def _fix_constant_name(self, content: str, violation: Violation) -> Tuple[str, str, str]:
        """Fix constant name to UPPER_SNAKE_CASE"""
        lines = content.split('\n')
        new_lines = []
        original = ""
        replacement = ""
        
        for line in lines:
            match = re.match(r'^([a-z][a-z0-9_]*)\s*=\s*([\'"\d])', line)
            if match and not original:
                original = match.group(1)
                replacement = original.upper()
                line = line.replace(original, replacement, 1)
            new_lines.append(line)
        
        return '\n'.join(new_lines), original, replacement
    
    def _fix_variable_name(self, content: str, violation: Violation) -> Tuple[str, str, str]:
        """Fix variable name to snake_case"""
        pattern = r'([A-Z][a-z]+[A-Z][a-zA-Z0-9]*)\s*='
        
        def to_snake(match):
            name = match.group(1)
            snake = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
            return f"{snake} ="
        
        new_content = re.sub(pattern, to_snake, content, count=1)
        
        match = re.search(pattern, content)
        original = match.group(1) if match else ""
        
        # Extract replacement
        replacement = re.sub(r'(?<!^)(?=[A-Z])', '_', original).lower() if original else ""
        
        return new_content, original, replacement
    
    def _fix_config_violation(self, violation: Violation) -> FixResult:
        """Fix configuration violations"""
        return FixResult(
            violation=violation,
            fixed=False,
            error="Config fixes not yet implemented"
        )
    
    def _fix_documentation_violation(self, violation: Violation) -> FixResult:
        """Fix documentation violations"""
        return FixResult(
            violation=violation,
            fixed=False,
            error="Documentation fixes not yet implemented"
        )
    
    def generate_pr_description(self, report: AutoFixReport) -> str:
        """
        Generate PR description for auto-fix changes.
        
        Args:
            report: AutoFixReport with fix results
            
        Returns:
            Markdown formatted PR description
        """
        description = f"""## [AutoFix] Rule Violation Fixes

**Generated**: {report.timestamp}
**Engine Version**: {self.VERSION}

### Summary

| Metric | Count |
|--------|-------|
| Total Violations | {report.total_violations} |
| Fixed | {report.fixed_count} |
| Failed | {report.failed_count} |
| Skipped | {report.skipped_count} |

### Changes Made

"""
        
        for fix in report.fixes:
            if fix.get("fixed"):
                violation = fix.get("violation", {})
                description += f"""#### {violation.get('rule_id', 'UNKNOWN')}
- **File**: `{violation.get('file', '')}`
- **Original**: `{fix.get('original', '')}`
- **Replacement**: `{fix.get('replacement', '')}`

"""
        
        if report.errors:
            description += "\n### Errors\n\n"
            for error in report.errors:
                description += f"- {error}\n"
        
        description += """
---
*This PR was automatically generated by the AutoFix Engine.*
*Please review the changes before merging.*
"""
        
        return description
    
    def save_report(self, report: AutoFixReport, output_path: Optional[str] = None) -> str:
        """
        Save auto-fix report to JSON file.
        
        Args:
            report: AutoFixReport to save
            output_path: Optional output path
            
        Returns:
            Path to saved report
        """
        if output_path is None:
            reports_dir = self.project_root / "reports"
            reports_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(reports_dir / f"autofix_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        
        return output_path


def main():
    """Main entry point for command-line execution"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AutoFix Engine - Automatic violation remediation"
    )
    parser.add_argument(
        "--report",
        type=str,
        help="Path to audit report JSON with violations"
    )
    parser.add_argument(
        "--safe-mode",
        action="store_true",
        default=True,
        help="Preview changes without applying (default: True)"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes (disable safe mode)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output path for fix report"
    )
    
    args = parser.parse_args()
    
    # Initialize engine
    safe_mode = not args.apply
    engine = AutoFixEngine(safe_mode=safe_mode)
    
    print(f"AutoFix Engine v{engine.VERSION}")
    print(f"Project Root: {engine.project_root}")
    print(f"Safe Mode: {safe_mode}")
    print("")
    
    # Load violations
    violations = []
    
    if args.report:
        print(f"Loading violations from: {args.report}")
        violations = engine.load_violations_from_report(args.report)
    else:
        print("No report specified. Creating sample violations for demo.")
        # Demo violations
        violations = [
            Violation(
                rule_id="NAM-001",
                file="example.py",
                message="Class name should be PascalCase",
                suggestion="rename_foo_class"
            )
        ]
    
    print(f"Found {len(violations)} violations")
    print("")
    
    # Fix violations
    report = engine.fix_violations(violations)
    
    # Print results
    print("=" * 60)
    print("AutoFix Results")
    print("=" * 60)
    print(f"Total: {report.total_violations}")
    print(f"Fixed: {report.fixed_count}")
    print(f"Failed: {report.failed_count}")
    print(f"Skipped: {report.skipped_count}")
    
    if report.errors:
        print("\nErrors:")
        for error in report.errors:
            print(f"  - {error}")
    
    # Save report
    report_path = engine.save_report(report, args.output)
    print(f"\nReport saved to: {report_path}")
    
    # Generate PR description
    if report.fixed_count > 0:
        print("\nPR Description:")
        print("-" * 40)
        print(engine.generate_pr_description(report))
    
    return 0 if report.failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
