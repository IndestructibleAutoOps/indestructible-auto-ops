#!/usr/bin/env python3
"""
Report Semantic Validator (报告语义验证器)

This script validates governance reports against the reporting-governance-spec.md
to prevent semantic violations such as fictional tools, phases, architecture levels,
and false compliance claims.

Usage:
    python ecosystem/tools/semantic_validator.py <report_file>
    python ecosystem/tools/semantic_validator.py --all
    python ecosystem/tools/semantic_validator.py --directory reports/
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Add ecosystem to path
sys.path.insert(0, str(Path(__file__).parent.parent))

class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class Violation:
    category: str
    severity: Severity
    message: str
    line_number: int = 0
    context: str = ""

@dataclass
class ValidationResult:
    report_file: str
    is_compliant: bool
    compliance_score: float
    violations: List[Violation] = field(default_factory=list)
    passed_checks: int = 0
    failed_checks: int = 0

class ReportSemanticValidator:
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = workspace
        self.registry_file = os.path.join(workspace, "ecosystem/governance/tools-registry.yaml")
        self.spec_file = os.path.join(workspace, "ecosystem/governance/reporting-governance-spec.md")
        
        # Load tools registry
        self.registered_tools = self._load_tools_registry()
        
        # Define prohibited patterns
        self._init_prohibited_patterns()
    
    def _load_tools_registry(self) -> set:
        """Load registered tools from registry."""
        tools = set()
        try:
            # Simple YAML parsing
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                if line.strip().startswith('- name:'):
                    tool_name = line.split(':', 1)[1].strip().strip('"\'')
                    if tool_name:
                        tools.add(tool_name)
        except Exception as e:
            print(f"[WARNING] Failed to load tools registry: {e}")
        
        return tools
    
    def _init_prohibited_patterns(self):
        """Initialize prohibited patterns for semantic validation."""
        
        # Tool reference violations
        self.prohibited_tool_patterns = [
            r'reporting_compliance_checker',
            r'compliance_checker\.py',
            r'final_summary',
            r'completion_report',
            r'final_report',
            r'fix_enforce_rules_final',
        ]
        
        # Phase declaration violations
        self.prohibited_phase_patterns = [
            r'第一階段',
            r'第二階段',
            r'第三階段',
            r'第四階段',
            r'第五階段',
            r'Phase\s*1\s*[:：]',
            r'Phase\s*2\s*[:：]',
            r'Phase\s*3\s*[:：]',
            r'Phase\s*4\s*[:：]',
            r'Phase\s*5\s*[:：]',
        ]
        
        # Architecture level violations (for single-file scripts)
        self.prohibited_architecture_patterns = [
            r'治理平台',
            r'多層治理平台',
            r'完整架構',
            r'平台級能力',
            r'平台就緒',
        ]
        
        # Compliance claim violations
        self.prohibited_compliance_patterns = [
            r'100%\s*合規',
            r'完整成熟度',
            r'治理完成',
            r'零風險',
            r'完全符合',
        ]
        
        # Prohibited terminology (Era-1)
        self.prohibited_terminology_patterns = [
            r'終態',
            r'完美',
            r'封存',  # Unless referencing Core hash sealing
            r'成熟度',
            r'完整性',
            r'完善',
            r'完備',
        ]
    
    def validate_report(self, report_file: str) -> ValidationResult:
        """Validate a single report file."""
        result = ValidationResult(
            report_file=report_file,
            is_compliant=False,
            compliance_score=0.0
        )
        
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            result.violations.append(Violation(
                category="file_access",
                severity=Severity.CRITICAL,
                message=f"Failed to read report file: {e}"
            ))
            return result
        
        # Perform all validations
        result.passed_checks = 0
        result.failed_checks = 0
        
        # Check 1: Tool references
        tool_violations = self.validate_tool_references(content, lines)
        if not tool_violations:
            result.passed_checks += 1
        else:
            result.failed_checks += 1
            result.violations.extend(tool_violations)
        
        # Check 2: Phase declarations
        phase_violations = self.validate_phase_declarations(content, lines)
        if not phase_violations:
            result.passed_checks += 1
        else:
            result.failed_checks += 1
            result.violations.extend(phase_violations)
        
        # Check 3: Architecture level
        arch_violations = self.validate_architecture_level(content, lines)
        if not arch_violations:
            result.passed_checks += 1
        else:
            result.failed_checks += 1
            result.violations.extend(arch_violations)
        
        # Check 4: Compliance claims
        compliance_violations = self.validate_compliance_claims(content, lines)
        if not compliance_violations:
            result.passed_checks += 1
        else:
            result.failed_checks += 1
            result.violations.extend(compliance_violations)
        
        # Check 5: Era/Layer semantics
        era_violations = self.validate_era_layer_semantics(content, lines)
        if not era_violations:
            result.passed_checks += 1
        else:
            result.failed_checks += 1
            result.violations.extend(era_violations)
        
        # Check 6: Prohibited terminology
        term_violations = self.validate_prohibited_terminology(content, lines)
        if not term_violations:
            result.passed_checks += 1
        else:
            result.failed_checks += 1
            result.violations.extend(term_violations)
        
        # Calculate compliance score
        total_checks = 6
        result.compliance_score = (result.passed_checks / total_checks) * 100
        
        # Determine overall compliance
        result.is_compliant = (
            result.compliance_score >= 80.0 and
            all(v.severity != Severity.CRITICAL for v in result.violations)
        )
        
        return result
    
    def validate_tool_references(self, content: str, lines: List[str]) -> List[Violation]:
        """Validate that all tool references are registered."""
        violations = []
        
        # Extract tool references (python files)
        tool_refs = re.findall(r'[\w_]+\.py', content)
        
        for tool_ref in tool_refs:
            # Check if tool is registered
            if tool_ref not in self.registered_tools:
                # Find line number
                line_num = self._find_line_number(lines, tool_ref)
                violations.append(Violation(
                    category="tool_references",
                    severity=Severity.CRITICAL,
                    message=f"未注册工具引用: {tool_ref}",
                    line_number=line_num,
                    context=lines[line_num-1] if line_num > 0 else ""
                ))
        
        # Check for prohibited tool patterns
        for pattern in self.prohibited_tool_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                line_num = self._find_line_number(lines, pattern)
                violations.append(Violation(
                    category="tool_references",
                    severity=Severity.CRITICAL,
                    message=f"禁止的工具模式: {pattern}",
                    line_number=line_num,
                    context=lines[line_num-1] if line_num > 0 else ""
                ))
        
        return violations
    
    def validate_phase_declarations(self, content: str, lines: List[str]) -> List[Violation]:
        """Validate that no undefined phases are declared."""
        violations = []
        
        for pattern in self.prohibited_phase_patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                for match in matches:
                    line_num = self._find_line_number(lines, match.group())
                    violations.append(Violation(
                        category="phase_declarations",
                        severity=Severity.HIGH,
                        message=f"禁止的阶段声明: {match.group()}",
                        line_number=line_num,
                        context=lines[line_num-1] if line_num > 0 else ""
                    ))
        
        return violations
    
    def validate_architecture_level(self, content: str, lines: List[str]) -> List[Violation]:
        """Validate architecture level descriptions."""
        violations = []
        
        for pattern in self.prohibited_architecture_patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                for match in matches:
                    line_num = self._find_line_number(lines, match.group())
                    violations.append(Violation(
                        category="architecture_level",
                        severity=Severity.HIGH,
                        message=f"禁止的架构层级描述: {match.group()}",
                        line_number=line_num,
                        context=lines[line_num-1] if line_num > 0 else ""
                    ))
        
        return violations
    
    def validate_compliance_claims(self, content: str, lines: List[str]) -> List[Violation]:
        """Validate compliance claims."""
        violations = []
        
        for pattern in self.prohibited_compliance_patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                for match in matches:
                    # Check if it's marked as self-referential
                    context_start = max(0, match.start() - 50)
                    context_end = min(len(content), match.end() + 50)
                    context = content[context_start:context_end]
                    
                    if 'self-referential' not in context.lower() and '自我验证' not in context:
                        line_num = self._find_line_number(lines, match.group())
                        violations.append(Violation(
                            category="compliance_claims",
                            severity=Severity.MEDIUM,
                            message=f"禁止的合规性声明: {match.group()}",
                            line_number=line_num,
                            context=lines[line_num-1] if line_num > 0 else ""
                        ))
        
        return violations
    
    def validate_era_layer_semantics(self, content: str, lines: List[str]) -> List[Violation]:
        """Validate Era/Layer semantic accuracy."""
        violations = []
        
        # Check Era declaration
        era_match = re.search(r'Era:\s*1\s*\([^)]*\)', content)
        if era_match:
            era_declaration = era_match.group()
            # Check for incorrect Era-1 descriptions
            if 'Complete' in era_declaration or '完成' in era_declaration:
                line_num = self._find_line_number(lines, era_declaration)
                violations.append(Violation(
                    category="era_layer_semantics",
                    severity=Severity.CRITICAL,
                    message="Era-1 不是完成状态",
                    line_number=line_num,
                    context=lines[line_num-1] if line_num > 0 else ""
                ))
        
        # Check Layer declaration
        layer_match = re.search(r'Layer:\s*Governance', content, re.IGNORECASE)
        if layer_match:
            line_num = self._find_line_number(lines, layer_match.group())
            violations.append(Violation(
                category="era_layer_semantics",
                severity=Severity.CRITICAL,
                message="Era-1 应该是 Operational Layer，不是 Governance Layer",
                line_number=line_num,
                context=lines[line_num-1] if line_num > 0 else ""
            ))
        
        # Check Semantic Closure
        closure_match = re.search(r'Semantic Closure:\s*YES', content, re.IGNORECASE)
        if closure_match:
            line_num = self._find_line_number(lines, closure_match.group())
            violations.append(Violation(
                category="era_layer_semantics",
                severity=Severity.CRITICAL,
                message="Era-1 的 Semantic Closure 应该是 NO",
                line_number=line_num,
                context=lines[line_num-1] if line_num > 0 else ""
            ))
        
        return violations
    
    def validate_prohibited_terminology(self, content: str, lines: List[str]) -> List[Violation]:
        """Validate prohibited terminology."""
        violations = []
        
        for pattern in self.prohibited_terminology_patterns:
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                for match in matches:
                    # Allow certain contexts
                    context_start = max(0, match.start() - 30)
                    context_end = min(len(content), match.end() + 30)
                    context = content[context_start:context_end]
                    
                    # Allow if it's in a list of what's NOT completed
                    if '尚未' in context or 'not' in context.lower():
                        continue
                    
                    line_num = self._find_line_number(lines, match.group())
                    violations.append(Violation(
                        category="terminology",
                        severity=Severity.MEDIUM,
                        message=f"禁止的术语（Era-1 未封存前）: {match.group()}",
                        line_number=line_num,
                        context=lines[line_num-1] if line_num > 0 else ""
                    ))
        
        return violations
    
    def _find_line_number(self, lines: List[str], text: str) -> int:
        """Find the line number containing the given text."""
        for i, line in enumerate(lines):
            if text in line:
                return i + 1
        return 0
    
    def validate_directory(self, directory: str) -> List[ValidationResult]:
        """Validate all markdown files in a directory."""
        results = []
        
        for file in os.listdir(directory):
            if file.endswith('.md'):
                file_path = os.path.join(directory, file)
                result = self.validate_report(file_path)
                results.append(result)
        
        return results

def print_violations(violations: List[Violation]):
    """Print violations in a formatted way."""
    if not violations:
        return
    
    for violation in violations:
        severity_symbol = {
            Severity.CRITICAL: "🔴",
            Severity.HIGH: "🟠",
            Severity.MEDIUM: "🟡",
            Severity.LOW: "🟢"
        }.get(violation.severity, "⚪")
        
        print(f"  {severity_symbol} [{violation.severity.value}] {violation.category}: {violation.message}")
        if violation.line_number > 0:
            print(f"     Line {violation.line_number}: {violation.context[:80]}...")
        print()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Report Semantic Validator")
    parser.add_argument("report_file", nargs="?", help="Report file to validate")
    parser.add_argument("--all", action="store_true", help="Validate all reports in reports/")
    parser.add_argument("--directory", default="reports/", help="Directory containing reports")
    parser.add_argument("--workspace", default="/workspace", help="Workspace directory")
    
    args = parser.parse_args()
    
    validator = ReportSemanticValidator(args.workspace)
    
    if args.all:
        print("\n🔍 Validating All Reports in", args.directory, "\n")
        print("=" * 80)
        
        if not os.path.exists(args.directory):
            print(f"❌ Directory not found: {args.directory}")
            return
        
        results = validator.validate_directory(args.directory)
        
        if not results:
            print("❌ No markdown reports found")
            return
        
        total_reports = len(results)
        compliant_reports = sum(1 for r in results if r.is_compliant)
        avg_score = sum(r.compliance_score for r in results) / total_reports if total_reports > 0 else 0
        
        print(f"\n📊 Summary:")
        print(f"  Total reports: {total_reports}")
        print(f"  Compliant reports: {compliant_reports}")
        print(f"  Non-compliant reports: {total_reports - compliant_reports}")
        print(f"  Average compliance score: {avg_score:.1f}/100")
        print()
        
        # Print violations for non-compliant reports
        for result in results:
            if not result.is_compliant or result.violations:
                print(f"\n📄 {os.path.basename(result.report_file)}")
                print(f"   Compliance Score: {result.compliance_score:.1f}/100")
                print(f"   Passed: {result.passed_checks}, Failed: {result.failed_checks}")
                print(f"   Violations: {len(result.violations)}")
                if result.violations:
                    print()
                    print_violations(result.violations)
        
        print("=" * 80 + "\n")
    
    elif args.report_file:
        if not os.path.exists(args.report_file):
            print(f"❌ File not found: {args.report_file}")
            return
        
        print(f"\n🔍 Validating Report: {args.report_file}\n")
        print("=" * 80)
        
        result = validator.validate_report(args.report_file)
        
        print(f"  📄 Report: {os.path.basename(result.report_file)}")
        print(f"  ✅ Compliant: {'Yes' if result.is_compliant else 'No'}")
        print(f"  📈 Compliance Score: {result.compliance_score:.1f}/100")
        print(f"  ✅ Passed Checks: {result.passed_checks}")
        print(f"  ❌ Failed Checks: {result.failed_checks}")
        print(f"  🚨 Violations: {len(result.violations)}")
        
        if result.violations:
            print("\n  Violations:")
            print()
            print_violations(result.violations)
        
        print("=" * 80 + "\n")
        
        # Exit with error code if not compliant
        sys.exit(0 if result.is_compliant else 1)
    
    else:
        print("❌ Please specify a report file or use --all")
        parser.print_help()

if __name__ == "__main__":
    main()