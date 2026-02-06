#!/usr/bin/env python3
"""
@GL-governed
@GL-layer: GL30-49
@GL-semantic: governance-validation
@GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json

NG Namespace Validator
Validates namespace compliance against NG000-999 framework
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

class Era(Enum):
    ERA1 = "Era-1"
    ERA2 = "Era-2"
    ERA3 = "Era-3"
    CROSS_ERA = "Cross-Era"

class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class NGViolation:
    """NG Namespace Violation"""
    ng_code: str
    era: Era
    file_path: str
    line_number: Optional[int]
    message: str
    severity: Severity
    suggestion: str
    auto_fixable: bool = True

@dataclass
class NGValidationResult:
    """NG Validation Result"""
    ng_code: str
    era: Era
    passed: bool
    violations: List[NGViolation] = field(default_factory=list)
    files_scanned: int = 0

class NGNamespaceValidator:
    """NG Namespace Governance Validator"""
    
    def __init__(self, workspace_root: Path):
        self.workspace = workspace_root
        self.violations: List[NGViolation] = []
        
        # NG Naming patterns
        self.patterns = {
            "kebab-case": re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$'),
            "snake_case": re.compile(r'^[a-z0-9]+(_[a-z0-9]+)*$'),
            "PascalCase": re.compile(r'^[A-Z][a-zA-Z0-9]*$'),
            "camelCase": re.compile(r'^[a-z][a-zA-Z0-9]*$'),
        }
        
        # NG Code definitions
        self.ng_standards = self._load_ng_standards()
        
    def _load_ng_standards(self) -> Dict:
        """Load NG namespace standards"""
        return {
            # NG000-099: Meta Framework
            "NG00000": {"era": Era.CROSS_ERA, "name": "Namespace Governance Charter"},
            
            # NG100-199: Era-1 Code
            "NG10100": {
                "era": Era.ERA1,
                "name": "Code Package Namespace",
                "pattern": "kebab-case",
                "applies_to": ["directories"],
                "rule": "Directories must use kebab-case",
                "exceptions": [".git", "__pycache__", "node_modules", ".venv", "venv"]
            },
            
            # NG200-299: Era-1 Architecture
            "NG20100": {
                "era": Era.ERA1,
                "name": "Module Namespace",
                "pattern": "kebab-case",
                "applies_to": ["modules"]
            },
            
            # NG300-399: Era-2 Microservices
            "NG30100": {
                "era": Era.ERA2,
                "name": "Microservice Boundary Namespace",
                "pattern": "kebab-case",
                "applies_to": ["services"]
            },
        }
    
    def validate_ng10100(self) -> NGValidationResult:
        """Validate NG10100: Code Package Namespace (kebab-case)"""
        result = NGValidationResult(
            ng_code="NG10100",
            era=Era.ERA1,
            passed=True
        )
        
        standard = self.ng_standards["NG10100"]
        excluded = standard["exceptions"]
        pattern = self.patterns[standard["pattern"]]
        
        for dir_path in self.workspace.rglob("*"):
            if not dir_path.is_dir():
                continue
            
            # Skip excluded directories
            if any(excl in str(dir_path) for excl in excluded):
                continue
            
            # Skip hidden directories
            if dir_path.name.startswith('.'):
                continue
            
            result.files_scanned += 1
            dir_name = dir_path.name
            
            # Check if directory name violates kebab-case
            if not pattern.match(dir_name):
                violation = NGViolation(
                    ng_code="NG10100",
                    era=Era.ERA1,
                    file_path=str(dir_path.relative_to(self.workspace)),
                    line_number=None,
                    message=f"Directory '{dir_name}' uses underscores/special chars, should use kebab-case",
                    severity=Severity.MEDIUM,
                    suggestion=f"Rename to '{dir_name.replace('_', '-').lower()}'",
                    auto_fixable=True
                )
                result.violations.append(violation)
                result.passed = False
        
        return result
    
    def validate_era1(self) -> List[NGValidationResult]:
        """Validate all Era-1 namespaces"""
        results = []
        
        # NG10100: Code Package Namespace
        results.append(self.validate_ng10100())
        
        return results
    
    def validate_all(self) -> Dict:
        """Validate all NG namespaces"""
        all_results = []
        
        # Era-1 validation
        all_results.extend(self.validate_era1())
        
        # Era-2 validation (placeholder for future)
        # all_results.extend(self.validate_era2())
        
        # Era-3 validation (placeholder for future)
        # all_results.extend(self.validate_era3())
        
        # Compile summary
        total_violations = sum(len(r.violations) for r in all_results)
        passed = sum(1 for r in all_results if r.passed)
        failed = len(all_results) - passed
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "governance_version": "NG000-999 v3.0",
            "summary": {
                "total_checks": len(all_results),
                "passed": passed,
                "failed": failed,
                "total_violations": total_violations
            },
            "results": [
                {
                    "ng_code": r.ng_code,
                    "era": r.era.value,
                    "passed": r.passed,
                    "files_scanned": r.files_scanned,
                    "violations": [
                        {
                            "ng_code": v.ng_code,
                            "file_path": v.file_path,
                            "message": v.message,
                            "severity": v.severity.value,
                            "suggestion": v.suggestion,
                            "auto_fixable": v.auto_fixable
                        }
                        for v in r.violations
                    ]
                }
                for r in all_results
            ]
        }
    
    def generate_fix_script(self) -> str:
        """Generate shell script to fix violations"""
        results = self.validate_all()
        
        script_lines = [
            "#!/bin/bash",
            "#",
            "# NG Namespace Auto-Fix Script",
            "# Generated by NG Namespace Validator",
            f"# Timestamp: {datetime.now(timezone.utc).isoformat()}",
            "#",
            "",
            "set -e",
            ""
        ]
        
        for result in results["results"]:
            for violation in result["violations"]:
                if violation["auto_fixable"]:
                    old_path = violation["file_path"]
                    new_path = violation["suggestion"].split("'")[1]
                    script_lines.append(f"# Fix: {violation['message']}")
                    script_lines.append(f"mv '{old_path}' '{new_path}' || echo 'Failed to rename {old_path}'")
                    script_lines.append("")
        
        return "\n".join(script_lines)

def main():
    """Main entry point"""
    workspace = Path("/workspace")
    validator = NGNamespaceValidator(workspace)
    
    # Run validation
    results = validator.validate_all()
    
    # Print results
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Generate fix script
    fix_script = validator.generate_fix_script()
    
    # Save fix script
    script_path = workspace / "ecosystem" / "ng-governance" / "implementation" / "fix-namespace-violations.sh"
    script_path.parent.mkdir(parents=True, exist_ok=True)
    script_path.write_text(fix_script)
    
    print(f"\nFix script generated: {script_path}")

if __name__ == "__main__":
    main()