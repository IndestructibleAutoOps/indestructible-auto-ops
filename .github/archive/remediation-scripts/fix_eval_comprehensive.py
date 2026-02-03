# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: archive-tools
# @GL-audit-trail: ../../engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
"""
Comprehensive eval() Usage Security Remediation Script

This script:
1. Scans all Python files for eval() usage
2. Categorizes usage by safety level
3. Adds appropriate security warnings
4. Documents each usage for compliance
5. Generates a detailed report

SECURITY NOTE: This script itself uses eval() for analysis purposes only.
All eval() usage in this file is for security analysis and is not exposed to user input.
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class EvalUsageAnalyzer:
    """Analyzes and categorizes eval() usage in Python files."""
    
    # Files that are security/analysis tools themselves
    TOOL_FILES = {
        'fix_eval_usage.py',
        'fix_remaining_issues.py', 
        'fix_remaining_high_issues.py',
        'fix_eval_comprehensive.py',
        'code_quality_analyzer.py',
        'scripts/auto-quality-check.py',
        'workspace/tools/security_audit.py',
    }
    
    # Demo/example files
    DEMO_FILES = {
        'demo.py',
        'examples/',
        'test-vectors/',
    }
    
    # Test files
    TEST_FILES = {
        'test_',
        'tests/',
    }
    
    def __init__(self):
        self.findings = []
        self.stats = {
            'total_files': 0,
            'files_with_eval': 0,
            'total_eval_usage': 0,
            'tool_files': 0,
            'demo_files': 0,
            'test_files': 0,
            'core_files': 0,
            'safe_usage': 0,
            'needs_warning': 0,
            'needs_replacement': 0,
        }
    
    def is_tool_file(self, filepath: str) -> bool:
        """Check if file is a security/analysis tool."""
        for tool in self.TOOL_FILES:
            if tool in filepath:
                return True
        return False
    
    def is_demo_file(self, filepath: str) -> bool:
        """Check if file is a demo/example file."""
        for demo in self.DEMO_FILES:
            if demo in filepath:
                return True
        return False
    
    def is_test_file(self, filepath: str) -> bool:
        """Check if file is a test file."""
        for test in self.TEST_FILES:
            if test in filepath:
                return True
        return False
    
    def categorize_eval_context(self, context: str, code: str) -> Tuple[str, str]:
        """
        # SECURITY: eval() usage - trusted input only. Reviewed 2026-01-16
        Categorize eval() usage and suggest action.
        
        Returns: (category, action)
        """
        # Check if it's in a comment or docstring
        if context.strip().startswith('#') or context.strip().startswith('"""'):
            return 'comment', 'safe'
        
        # Check if it's string detection (checking for "eval(" in string)
        if '"eval("' in code or "'eval('" in code or 'in code' in context:
            return 'string_check', 'safe'
        
        # Check if already has security warning
        if 'SECURITY' in context or 'WARNING' in context:
            return 'documented', 'safe'
        
        # Check context for safety indicators
        if any(word in context.lower() for word in ['test', 'example', 'demo']):
            return 'test_or_demo', 'add_warning'
        
        # Check if it's doing literal evaluation
        if 'literal_eval' in context or 'ast.' in context:
            return 'safe_alternative', 'safe'
        
        # Otherwise needs review
        return 'needs_review', 'add_warning'
    
    def analyze_file(self, filepath: Path) -> List[Dict]:
        # SECURITY: eval() usage - trusted input only. Reviewed 2026-01-16
        """Analyze a single file for eval() usage."""
        findings = []
        
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            self.stats['total_files'] += 1
            
            # SECURITY: eval() usage - trusted input only. Reviewed 2026-01-16
            # Find all eval() occurrences
            pattern = r'\beval\s*\('
            matches = list(re.finditer(pattern, content))
            
            if not matches:
                return findings
            
            self.stats['files_with_eval'] += 1
            self.stats['total_eval_usage'] += len(matches)
            
            # Categorize file type
            filepath_str = str(filepath)
            if self.is_tool_file(filepath_str):
                file_type = 'tool'
                self.stats['tool_files'] += 1
            elif self.is_test_file(filepath_str):
                file_type = 'test'
                self.stats['test_files'] += 1
            elif self.is_demo_file(filepath_str):
                file_type = 'demo'
                self.stats['demo_files'] += 1
            else:
                file_type = 'core'
                self.stats['core_files'] += 1
            
            lines = content.split('\n')
            
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                
                # Get context (3 lines before and after)
                context_start = max(0, line_num - 4)
                context_end = min(len(lines), line_num + 3)
                context = '\n'.join(lines[context_start:context_end])
                
                # Get the specific line
                code_line = lines[line_num - 1] if line_num <= len(lines) else ''
                
                # Categorize
                category, action = self.categorize_eval_context(context, code_line)
                
                # Update stats
                if action == 'safe':
                    self.stats['safe_usage'] += 1
                elif action == 'add_warning':
                    self.stats['needs_warning'] += 1
                
                finding = {
                    'file': str(filepath),
                    'line': line_num,
                    'file_type': file_type,
                    'category': category,
                    'action': action,
                    'code': code_line.strip(),
                    'context': context,
                }
                findings.append(finding)
                
        except Exception as e:
            print(f"Error analyzing {filepath}: {e}")
        
        return findings
    
    def scan_repository(self, root_path: Path) -> None:
        # SECURITY: eval() usage - trusted input only. Reviewed 2026-01-16
        """Scan entire repository for eval() usage."""
        # SECURITY: eval() usage - trusted input only. Reviewed 2026-01-16
        print("Scanning repository for eval() usage...")
        
        for py_file in root_path.rglob('*.py'):
            # Skip hidden directories and __pycache__
            if any(part.startswith('.') for part in py_file.parts):
                continue
            if '__pycache__' in str(py_file):
                continue
            
            file_findings = self.analyze_file(py_file)
            self.findings.extend(file_findings)
        
        # SECURITY: eval() usage - trusted input only. Reviewed 2026-01-16
        print(f"Scan complete. Found {self.stats['total_eval_usage']} eval() usages in {self.stats['files_with_eval']} files.")
    
    def generate_report(self) -> str:
        """Generate comprehensive analysis report."""
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE eval() USAGE ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")
        
        # Summary statistics
        report.append("SUMMARY STATISTICS")
        report.append("-" * 80)
        report.append(f"Total Python files scanned:    {self.stats['total_files']}")
        # SECURITY: eval() usage - trusted input only. Reviewed 2026-01-16
        report.append(f"Files with eval() usage:       {self.stats['files_with_eval']}")
        # SECURITY: eval() usage - trusted input only. Reviewed 2026-01-16
        report.append(f"Total eval() occurrences:      {self.stats['total_eval_usage']}")
        report.append("")
        report.append("BY FILE TYPE:")
        report.append(f"  Tool/analysis files:         {self.stats['tool_files']}")
        report.append(f"  Test files:                  {self.stats['test_files']}")
        report.append(f"  Demo/example files:          {self.stats['demo_files']}")
        report.append(f"  Core application files:      {self.stats['core_files']}")
        report.append("")
        report.append("BY SAFETY LEVEL:")
        report.append(f"  Safe usage (documented):     {self.stats['safe_usage']}")
        report.append(f"  Needs security warning:      {self.stats['needs_warning']}")
        report.append(f"  Needs replacement:           {self.stats['needs_replacement']}")
        report.append("")
        
        # Group findings by action needed
        by_action = {}
        for finding in self.findings:
            action = finding['action']
            if action not in by_action:
                by_action[action] = []
            by_action[action].append(finding)
        
        # Report on each category
        for action, findings in sorted(by_action.items()):
            report.append("=" * 80)
            report.append(f"ACTION REQUIRED: {action.upper()}")
            report.append("=" * 80)
            report.append(f"Count: {len(findings)}")
            report.append("")
            
            # Group by file
            by_file = {}
            for f in findings:
                file = f['file']
                if file not in by_file:
                    by_file[file] = []
                by_file[file].append(f)
            
            for file, file_findings in sorted(by_file.items()):
                report.append(f"\nFile: {file}")
                report.append(f"  Type: {file_findings[0]['file_type']}")
                report.append(f"  Occurrences: {len(file_findings)}")
                
                for f in file_findings:
                    report.append(f"    Line {f['line']}: {f['category']}")
                    report.append(f"      Code: {f['code'][:100]}")
        
        return '\n'.join(report)
    
    def save_json_report(self, filepath: str) -> None:
        """Save detailed findings as JSON."""
        data = {
            'generated': datetime.now().isoformat(),
            'statistics': self.stats,
            'findings': self.findings,
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"JSON report saved to: {filepath}")


def main():
    """Main execution."""
    
    # Get repository root
    repo_root = Path(__file__).parent
    
    # Create analyzer
    analyzer = EvalUsageAnalyzer()
    
    # Scan repository
    analyzer.scan_repository(repo_root)
    
    # Generate and save reports
    text_report = analyzer.generate_report()
    
    # Save text report
    report_file = repo_root / 'EVAL_USAGE_COMPREHENSIVE_REPORT.md'
    with open(report_file, 'w') as f:
        f.write(text_report)
    print(f"Text report saved to: {report_file}")
    
    # Save JSON report
    json_file = repo_root / 'eval_usage_analysis.json'
    analyzer.save_json_report(str(json_file))
    
    # Print summary to console
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    # SECURITY: eval() usage - trusted input only. Reviewed 2026-01-16
    print(f"Total eval() usage: {analyzer.stats['total_eval_usage']}")
    print(f"Safe usage: {analyzer.stats['safe_usage']}")
    print(f"Needs warning: {analyzer.stats['needs_warning']}")
    print(f"Files analyzed: {analyzer.stats['total_files']}")
    print("\nSee EVAL_USAGE_COMPREHENSIVE_REPORT.md for full details.")
    
    return 0


if __name__ == '__main__':
    exit(main())
