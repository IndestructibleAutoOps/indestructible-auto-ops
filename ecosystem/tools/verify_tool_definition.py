#!/usr/bin/env python3
"""
Tool Definition Verifier (工具定义验证器)

This script verifies that all tools in the ecosystem comply with the
Tool Definition Protocol (tool-definition-protocol.md).

Usage:
    python ecosystem/tools/verify_tool_definition.py <tool_name>
    python ecosystem/tools/verify_tool_definition.py --all
    python ecosystem/tools/verify_tool_definition.py --list-undefined
    python ecosystem/tools/verify_tool_definition.py --audit
"""

import os
import sys
import json
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Import simple_yaml module
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
try:
    from simple_yaml import load_yaml
    yaml_available = True
except ImportError:
    yaml_available = False
    def load_yaml(file_path: str) -> Dict[str, Any]:
        """Fallback simple YAML loader."""
        result = {}
        current_dict = result
        stack = [result]
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip()
                
                if not line or line.strip().startswith('#'):
                    continue
                
                if line.startswith('- '):
                    item = line[2:].strip()
                    if ':' in item:
                        key, value = item.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        current_dict[key] = value
                    continue
                
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if value:
                        value = value.strip('"\'')
                        if value.lower() in ['true', 'yes', 'on']:
                            value = True
                        elif value.lower() in ['false', 'no', 'off']:
                            value = False
                        elif value.lower() in ['null', 'none', '~', '']:
                            value = None
                        current_dict[key] = value
                    else:
                        if key not in current_dict:
                            current_dict[key] = {}
                        stack.append(current_dict)
                        current_dict = current_dict[key]
        
        return result

# Add ecosystem to path
sys.path.insert(0, str(Path(__file__).parent.parent))

class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class Violation:
    tool_name: str
    severity: Severity
    category: str
    message: str
    line_number: int = 0

@dataclass
class ComplianceResult:
    tool_name: str
    is_registered: bool
    is_compliant: bool
    compliance_score: float
    violations: List[Violation] = field(default_factory=list)

class ToolDefinitionVerifier:
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = workspace
        self.registry_file = os.path.join(workspace, "ecosystem/governance/tools-registry.yaml")
        self.protocol_file = os.path.join(workspace, "ecosystem/governance/tool-definition-protocol.md")
        self.governance_dir = os.path.join(workspace, "ecosystem/governance")
        
        # Load registry
        self.registry = self._load_registry()
        
        # Define prohibited patterns
        self.prohibited_patterns = self._get_prohibited_patterns()
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load tools registry from YAML file."""
        try:
            result = {"registered_tools": [], "prohibited_tool_patterns": []}
            
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            current_list = None
            current_dict = None
            current_item = None
            
            for line in lines:
                line = line.rstrip()
                
                # Skip empty lines and comments
                if not line or line.strip().startswith('#'):
                    continue
                
                # Top-level keys
                if ':' in line and not line.startswith(' '):
                    key = line.split(':', 1)[0].strip()
                    if key == 'registered_tools':
                        current_list = []
                        result['registered_tools'] = current_list
                    elif key == 'prohibited_tool_patterns':
                        current_list = []
                        result['prohibited_tool_patterns'] = current_list
                    continue
                
                # List item start
                if line.strip().startswith('- '):
                    content = line.strip()[2:].strip()
                    if ':' in content:
                        key, value = content.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        current_item = {key: value}
                        if current_list is not None:
                            current_list.append(current_item)
                    continue
                
                # Nested properties
                if line.startswith('    ') and ':' in line and current_item is not None:
                    key, value = line.strip().split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    # Parse value
                    if value.lower() in ['true', 'yes', 'on']:
                        value = True
                    elif value.lower() in ['false', 'no', 'off']:
                        value = False
                    elif value.lower() in ['null', 'none', '~', '']:
                        value = None
                    elif value.isdigit():
                        value = int(value)
                    current_item[key] = value
            
            return result
            
        except Exception as e:
            print(f"[ERROR] Failed to load registry: {e}")
            import traceback
            traceback.print_exc()
            return {"registered_tools": [], "prohibited_tool_patterns": []}
    
    def _get_prohibited_patterns(self) -> List[Dict[str, str]]:
        """Get prohibited tool patterns from registry."""
        patterns = []
        if "prohibited_tool_patterns" in self.registry:
            patterns = self.registry["prohibited_tool_patterns"]
        return patterns
    
    def verify_tool(self, tool_path: str) -> ComplianceResult:
        """Verify a single tool against protocol requirements."""
        tool_name = os.path.basename(tool_path)
        
        violations = []
        compliance_score = 0.0
        
        # Check 1: Tool is registered
        is_registered = self._check_registration(tool_name)
        if not is_registered:
            violations.append(Violation(
                tool_name=tool_name,
                severity=Severity.CRITICAL,
                category="registration",
                message="Tool not registered in tools-registry.yaml"
            ))
        else:
            compliance_score += 30.0
        
        # Check 2: Tool naming compliance
        naming_compliant, naming_violations = self._check_naming_compliance(tool_name)
        if naming_compliant:
            compliance_score += 20.0
        else:
            violations.extend(naming_violations)
        
        # Check 3: Evidence generation
        evidence_compliant, evidence_violations = self._check_evidence_generation(tool_path)
        if evidence_compliant:
            compliance_score += 30.0
        else:
            violations.extend(evidence_violations)
        
        # Check 4: Era applicability
        era_compliant, era_violations = self._check_era_applicability(tool_name, tool_path)
        if era_compliant:
            compliance_score += 10.0
        else:
            violations.extend(era_violations)
        
        # Check 5: Documentation compliance
        doc_compliant, doc_violations = self._check_documentation(tool_name)
        if doc_compliant:
            compliance_score += 10.0
        else:
            violations.extend(doc_violations)
        
        # Determine overall compliance
        is_compliant = (compliance_score >= 80.0 and 
                        all(v.severity != Severity.CRITICAL for v in violations))
        
        return ComplianceResult(
            tool_name=tool_name,
            is_registered=is_registered,
            is_compliant=is_compliant,
            compliance_score=compliance_score,
            violations=violations
        )
    
    def _check_registration(self, tool_name: str) -> bool:
        """Check if tool is registered in tools-registry.yaml."""
        registered_tools = self.registry.get("registered_tools", [])
        for tool in registered_tools:
            if tool.get("name") == tool_name:
                return True
        return False
    
    def _check_naming_compliance(self, tool_name: str) -> Tuple[bool, List[Violation]]:
        """Check if tool name complies with naming conventions."""
        violations = []
        
        # Check against prohibited patterns
        for pattern in self.prohibited_patterns:
            pattern_str = pattern.get("pattern", "")
            severity = Severity(pattern.get("severity", "MEDIUM"))
            reason = pattern.get("reason", "")
            
            # Convert glob pattern to regex
            regex_pattern = pattern_str.replace("*", ".*")
            if re.match(regex_pattern, tool_name, re.IGNORECASE):
                violations.append(Violation(
                    tool_name=tool_name,
                    severity=severity,
                    category="naming",
                    message=f"Violates prohibited pattern '{pattern_str}': {reason}"
                ))
        
        return (len(violations) == 0, violations)
    
    def _check_evidence_generation(self, tool_path: str) -> Tuple[bool, List[Violation]]:
        """Check if tool has evidence generation code."""
        violations = []
        
        try:
            with open(tool_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for evidence generation keywords
            evidence_keywords = [
                "evidence_dir",
                "event-stream",
                "SHA256",
                "artifact",
                "uuid",
                "_write_step_event",
                "_generate_artifact"
            ]
            
            has_evidence = any(keyword in content for keyword in evidence_keywords)
            
            if not has_evidence:
                violations.append(Violation(
                    tool_name=os.path.basename(tool_path),
                    severity=Severity.HIGH,
                    category="evidence",
                    message="Tool missing evidence generation code"
                ))
        
        except Exception as e:
            violations.append(Violation(
                tool_name=os.path.basename(tool_path),
                severity=Severity.MEDIUM,
                category="evidence",
                message=f"Failed to check evidence generation: {e}"
            ))
        
        return (len(violations) == 0, violations)
    
    def _check_era_applicability(self, tool_name: str, tool_path: str) -> Tuple[bool, List[Violation]]:
        """Check if tool complies with Era constraints."""
        violations = []
        
        try:
            # Get tool registration info
            registered_tools = self.registry.get("registered_tools", [])
            tool_info = None
            for tool in registered_tools:
                if tool.get("name") == tool_name:
                    tool_info = tool
                    break
            
            if tool_info:
                # Check for false maturity claims in tool code
                with open(tool_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                prohibited_phrases = [
                    "100% compliance",
                    "complete maturity",
                    "governance complete",
                    "platform ready",
                    "final state"
                ]
                
                for phrase in prohibited_phrases:
                    if phrase.lower() in content.lower():
                        violations.append(Violation(
                            tool_name=tool_name,
                            severity=Severity.MEDIUM,
                            category="era",
                            message=f"Contains prohibited phrase '{phrase}' (Era-1 not sealed)"
                        ))
                        break
        
        except Exception as e:
            violations.append(Violation(
                tool_name=tool_name,
                severity=Severity.LOW,
                category="era",
                message=f"Failed to check Era compliance: {e}"
            ))
        
        return (len(violations) == 0, violations)
    
    def _check_documentation(self, tool_name: str) -> Tuple[bool, List[Violation]]:
        """Check if tool has proper documentation."""
        violations = []
        
        try:
            # Get tool registration info
            registered_tools = self.registry.get("registered_tools", [])
            tool_info = None
            for tool in registered_tools:
                if tool.get("name") == tool_name:
                    tool_info = tool
                    break
            
            if not tool_info:
                # Already handled by registration check
                return (True, violations)
            
            # Check required fields
            required_fields = [
                "category", "era", "purpose", "input_schema", 
                "output_schema", "evidence_generation"
            ]
            
            for field in required_fields:
                if not tool_info.get(field):
                    violations.append(Violation(
                        tool_name=tool_name,
                        severity=Severity.LOW,
                        category="documentation",
                        message=f"Missing required field '{field}' in registry"
                    ))
        
        except Exception as e:
            violations.append(Violation(
                tool_name=tool_name,
                severity=Severity.LOW,
                category="documentation",
                message=f"Failed to check documentation: {e}"
            ))
        
        return (len(violations) == 0, violations)
    
    def verify_all_tools(self) -> Dict[str, Any]:
        """Verify all Python files in ecosystem/."""
        results = {
            "total_tools": 0,
            "registered_tools": 0,
            "compliant_tools": 0,
            "non_compliant_tools": 0,
            "undefined_tools": [],
            "tool_results": []
        }
        
        # Find all Python files
        ecosystem_dir = os.path.join(self.workspace, "ecosystem")
        for root, dirs, files in os.walk(ecosystem_dir):
            # Skip __pycache__ and .git directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.governance', '.evidence']]
            
            for file in files:
                if file.endswith('.py'):
                    tool_path = os.path.join(root, file)
                    results["total_tools"] += 1
                    
                    # Verify tool
                    result = self.verify_tool(tool_path)
                    results["tool_results"].append(result)
                    
                    if result.is_registered:
                        results["registered_tools"] += 1
                    
                    if result.is_compliant:
                        results["compliant_tools"] += 1
                    else:
                        results["non_compliant_tools"] += 1
                        if not result.is_registered:
                            results["undefined_tools"].append(result.tool_name)
        
        # Calculate overall compliance score
        if results["total_tools"] > 0:
            results["compliance_score"] = (
                (results["registered_tools"] / results["total_tools"]) * 50 +
                (results["compliant_tools"] / results["total_tools"]) * 50
            )
        else:
            results["compliance_score"] = 0.0
        
        return results
    
    def list_undefined_tools(self) -> List[str]:
        """List all undefined tools in the ecosystem."""
        undefined = []
        
        ecosystem_dir = os.path.join(self.workspace, "ecosystem")
        for root, dirs, files in os.walk(ecosystem_dir):
            # Skip __pycache__ and .git directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.governance', '.evidence']]
            
            for file in files:
                if file.endswith('.py'):
                    tool_name = file
                    if not self._check_registration(tool_name):
                        undefined.append(tool_name)
        
        return undefined
    
    def audit_registry(self) -> Dict[str, Any]:
        """Audit the tools registry against actual files."""
        audit_results = {
            "registered_tools_count": 0,
            "registered_files_exist": 0,
            "registered_files_missing": [],
            "active_tools_count": 0,
            "deprecated_tools_count": 0,
            "orphaned_registry_entries": []
        }
        
        registered_tools = self.registry.get("registered_tools", [])
        audit_results["registered_tools_count"] = len(registered_tools)
        
        for tool in registered_tools:
            tool_name = tool.get("name", "")
            status = tool.get("status", "unknown")
            
            if status == "active":
                audit_results["active_tools_count"] += 1
            elif status == "deprecated":
                audit_results["deprecated_tools_count"] += 1
            
            # Check if file exists
            file_path = tool.get("file_path", "")
            if file_path and os.path.exists(os.path.join(self.workspace, file_path)):
                audit_results["registered_files_exist"] += 1
            elif file_path:
                audit_results["registered_files_missing"].append({
                    "name": tool_name,
                    "expected_path": file_path
                })
            else:
                audit_results["orphaned_registry_entries"].append(tool_name)
        
        return audit_results

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

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Tool Definition Verifier")
    parser.add_argument("tool_name", nargs="?", help="Tool name to verify")
    parser.add_argument("--all", action="store_true", help="Verify all tools")
    parser.add_argument("--list-undefined", action="store_true", help="List undefined tools")
    parser.add_argument("--audit", action="store_true", help="Audit registry against actual files")
    parser.add_argument("--workspace", default="/workspace", help="Workspace directory")
    
    args = parser.parse_args()
    
    verifier = ToolDefinitionVerifier(args.workspace)
    
    if args.list_undefined:
        print("\n📋 Undefined Tools (未定义工具)\n")
        print("=" * 60)
        undefined = verifier.list_undefined_tools()
        if undefined:
            for tool in undefined:
                print(f"  ❌ {tool}")
            print(f"\nTotal undefined tools: {len(undefined)}")
        else:
            print("  ✅ No undefined tools found")
        print("=" * 60 + "\n")
    
    elif args.audit:
        print("\n🔍 Registry Audit (注册表审计)\n")
        print("=" * 60)
        audit_results = verifier.audit_registry()
        
        print(f"  📊 Registered tools: {audit_results['registered_tools_count']}")
        print(f"  ✅ Active tools: {audit_results['active_tools_count']}")
        print(f"  📦 Deprecated tools: {audit_results['deprecated_tools_count']}")
        print(f"  📁 Files exist: {audit_results['registered_files_exist']}")
        print(f"  ❌ Files missing: {len(audit_results['registered_files_missing'])}")
        print(f"  🚫 Orphaned entries: {len(audit_results['orphaned_registry_entries'])}")
        
        if audit_results['registered_files_missing']:
            print("\n  Missing files:")
            for missing in audit_results['registered_files_missing']:
                print(f"    ❌ {missing['name']} ({missing['expected_path']})")
        
        if audit_results['orphaned_registry_entries']:
            print("\n  Orphaned registry entries:")
            for name in audit_results['orphaned_registry_entries']:
                print(f"    🚫 {name}")
        
        print("=" * 60 + "\n")
    
    elif args.all:
        print("\n🔍 Verifying All Tools (验证所有工具)\n")
        print("=" * 60)
        results = verifier.verify_all_tools()
        
        print(f"  📊 Total tools: {results['total_tools']}")
        print(f"  ✅ Registered tools: {results['registered_tools']}")
        print(f"  ✅ Compliant tools: {results['compliant_tools']}")
        print(f"  ❌ Non-compliant tools: {results['non_compliant_tools']}")
        print(f"  📋 Undefined tools: {len(results['undefined_tools'])}")
        print(f"  📈 Compliance score: {results['compliance_score']:.1f}/100")
        
        if results['undefined_tools']:
            print("\n  Undefined tools:")
            for tool in results['undefined_tools']:
                print(f"    ❌ {tool}")
        
        print("=" * 60 + "\n")
        
        # Print violations for non-compliant tools
        non_compliant = [r for r in results['tool_results'] if not r.is_compliant]
        if non_compliant:
            print("🚨 Violations for Non-Compliant Tools\n")
            print("=" * 60)
            for result in non_compliant:
                print(f"\n  📄 {result.tool_name}")
                print(f"     Compliance Score: {result.compliance_score:.1f}/100")
                print(f"     Registered: {'✅' if result.is_registered else '❌'}")
                print(f"     Violations: {len(result.violations)}")
                print_violations(result.violations)
            print("=" * 60 + "\n")
    
    elif args.tool_name:
        print(f"\n🔍 Verifying Tool: {args.tool_name}\n")
        print("=" * 60)
        
        # Find tool file
        tool_path = None
        ecosystem_dir = os.path.join(args.workspace, "ecosystem")
        for root, dirs, files in os.walk(ecosystem_dir):
            if args.tool_name in files:
                tool_path = os.path.join(root, args.tool_name)
                break
        
        if not tool_path:
            print(f"  ❌ Tool not found: {args.tool_name}")
            return
        
        result = verifier.verify_tool(tool_path)
        
        print(f"  📄 Tool Name: {result.tool_name}")
        print(f"  ✅ Registered: {'Yes' if result.is_registered else 'No'}")
        print(f"  ✅ Compliant: {'Yes' if result.is_compliant else 'No'}")
        print(f"  📈 Compliance Score: {result.compliance_score:.1f}/100")
        print(f"  🚨 Violations: {len(result.violations)}")
        
        if result.violations:
            print("\n  Violations:")
            print_violations(result.violations)
        
        print("=" * 60 + "\n")
    
    else:
        print("❌ Please specify a tool name or use --all, --list-undefined, or --audit")
        parser.print_help()

if __name__ == "__main__":
    main()