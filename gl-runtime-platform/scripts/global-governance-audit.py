#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GL Global Governance Audit Script
Version 21.0.0

This script performs a comprehensive gl_platform_universegl_platform_universe.governance audit across all components
of the GL Runtime Platform and generates detailed audit reports.
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict
import hashlib

# ============================================================================
# Governance Audit Configuration
# ============================================================================

AUDIT_CONFIG = {
    "version": "21.0.0",
    "audit_date": datetime.datetime.now().isoformat(),
    "workspace_root": "/workspace",
    "scan_directories": [
        "/workspace/gl-runtime-platform",
        "/workspace/elasticsearch-search-system",
        "/workspace/.github/agents",
        "/workspace/file-organizer-system",
        "/workspace/.gl_platform_universegl_platform_universe.governance",
        "/workspace/infrastructure",
        "/workspace/.agent_hooks",
        "/workspace/engine",
        "/workspace/esync-platform",
        "/workspace/instant",
        "/workspace/summarized_conversations"
    ],
    "file_extensions_to_scan": [
        ".ts", ".js", ".json", ".yaml", ".yml", 
        ".md", ".txt", ".py", ".sh"
    ],
    "gl_platform_universegl_platform_universe.governance_checks": {
        "gl_gl_platform_universegl_platform_universe.governance_tags": {
            "required_tags": ["@GL-governed", "@GL-layer", "@GL-semantic"],
            "description": "Check for GL gl_platform_universegl_platform_universe.governance header tags"
        },
        "semantic_anchors": {
            "required": True,
            "description": "Check for semantic anchor references"
        },
        "charter_version": {
            "required": True,
            "description": "Check for charter version compliance"
        },
        "audit_trail": {
            "required": True,
            "description": "Check for audit trail references"
        }
    },
    "output_directory": "./gl_platform_universegl_platform_universe.governance-audit-reports"
}

# ============================================================================
# Audit Result Types
# ============================================================================

class FileAuditResult:
    """Audit result for a single file"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_extension = os.path.splitext(file_path)[1]
        self.file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        self.last_modified = datetime.datetime.fromtimestamp(
            os.path.getmtime(file_path)
        ).isoformat() if os.path.exists(file_path) else None
        self.hash = self._calculate_hash() if os.path.exists(file_path) else None
        
        self.gl_platform_universegl_platform_universe.governance_compliance = {
            "has_gl_platform_universegl_platform_universe.governance_tags": False,
            "has_semantic_anchor": False,
            "has_charter_version": False,
            "has_audit_trail": False,
            "missing_tags": [],
            "extra_tags": []
        }
        
        self.semantic_analysis = {
            "semantic_class": None,
            "gl_layer": None,
            "semantic_type": None,
            "semantic_confidence": 0.0
        }
        
        self.code_quality = {
            "line_count": 0,
            "comment_ratio": 0.0,
            "complexity_score": 0
        }
        
        self.security_analysis = {
            "has_secrets": False,
            "has_hardcoded_credentials": False,
            "has_insecure_patterns": False
        }
        
        self.issues = []
        self.warnings = []
        self.recommendations = []
        
    def _calculate_hash(self) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(self.file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return None
    
    def analyze_content(self, content: str):
        """Analyze file content for gl_platform_universegl_platform_universe.governance compliance"""
        lines = content.split('\n')
        
        # Analyze gl_platform_universegl_platform_universe.governance tags
        self.gl_platform_universegl_platform_universe.governance_compliance["has_gl_platform_universegl_platform_universe.governance_tags"] = (
            "@GL-governed" in content
        )
        
        # Extract specific tags
        if self.gl_platform_universegl_platform_universe.governance_compliance["has_gl_platform_universegl_platform_universe.governance_tags"]:
            if "@GL-layer:" in content:
                self.gl_platform_universegl_platform_universe.governance_compliance["has_gl_platform_universegl_platform_universe.governance_tags"] = True
                self.semantic_analysis["gl_layer"] = self._extract_tag_value(content, "@GL-layer:")
            else:
                self.gl_platform_universegl_platform_universe.governance_compliance["missing_tags"].append("@GL-layer:")
            
            if "@GL-semantic:" in content:
                self.gl_platform_universegl_platform_universe.governance_compliance["has_gl_platform_universegl_platform_universe.governance_tags"] = True
                self.semantic_analysis["semantic_type"] = self._extract_tag_value(content, "@GL-semantic:")
            else:
                self.gl_platform_universegl_platform_universe.governance_compliance["missing_tags"].append("@GL-semantic:")
            
            if "@GL-audit-trail:" in content:
                self.gl_platform_universegl_platform_universe.governance_compliance["has_audit_trail"] = True
            else:
                self.gl_platform_universegl_platform_universe.governance_compliance["missing_tags"].append("@GL-audit-trail:")
            
            if "@GL-charter-version:" in content:
                self.gl_platform_universegl_platform_universe.governance_compliance["has_charter_version"] = True
        
        # Analyze semantic anchors
        if "GL_SEMANTIC_ANCHOR" in content or "semantic-anchor" in content:
            self.gl_platform_universegl_platform_universe.governance_compliance["has_semantic_anchor"] = True
        
        # Analyze code quality
        self.code_quality["line_count"] = len(lines)
        comment_lines = [line for line in lines if line.strip().startswith('//') or line.strip().startswith('#') or line.strip().startswith('*')]
        self.code_quality["comment_ratio"] = len(comment_lines) / max(len(lines), 1)
        
        # Security analysis
        if any(keyword in content.lower() for keyword in ['password', 'secret', 'api_key', 'token']):
            self.security_analysis["has_secrets"] = True
            self.issues.append("Potential secrets detected in file")
        
        if "http://" in content or "https://" in content:
            self.security_analysis["has_hardcoded_credentials"] = False  # URLs are OK
        
        # Generate recommendations
        if not self.gl_platform_universegl_platform_universe.governance_compliance["has_gl_platform_universegl_platform_universe.governance_tags"]:
            self.recommendations.append("Add GL gl_platform_universegl_platform_universe.governance tags to file header")
        
        if self.code_quality["comment_ratio"] < 0.1:
            self.recommendations.append("Consider adding more documentation comments")
    
    def _extract_tag_value(self, content: str, tag: str) -> str:
        """Extract value from gl_platform_universegl_platform_universe.governance tag"""
        for line in content.split('\n'):
            if tag in line:
                parts = line.split(tag)
                if len(parts) > 1:
                    return parts[1].strip().strip('"')
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "file_path": self.file_path,
            "file_name": self.file_name,
            "file_extension": self.file_extension,
            "file_size": self.file_size,
            "last_modified": self.last_modified,
            "hash": self.hash,
            "gl_platform_universegl_platform_universe.governance_compliance": self.gl_platform_universegl_platform_universe.governance_compliance,
            "semantic_analysis": self.semantic_analysis,
            "code_quality": self.code_quality,
            "security_analysis": self.security_analysis,
            "issues": self.issues,
            "warnings": self.warnings,
            "recommendations": self.recommendations
        }

# ============================================================================
# Global Governance Auditor
# ============================================================================

class GlobalGovernanceAuditor:
    """Main auditor class for global gl_platform_universegl_platform_universe.governance audit"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.audit_results = []
        self.summary_statistics = {
            "total_files_scanned": 0,
            "files_with_gl_platform_universegl_platform_universe.governance_tags": 0,
            "files_compliant": 0,
            "files_with_issues": 0,
            "total_issues": 0,
            "total_recommendations": 0,
            "compliance_rate": 0.0
        }
        
        # Create output directory
        self.output_dir = Path(config["output_directory"])
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def scan_directory(self, directory: str) -> List[FileAuditResult]:
        """Scan a directory and audit all files"""
        results = []
        dir_path = Path(directory)
        
        if not dir_path.exists():
            print(f"⚠️  Directory not found: {directory}")
            return results
        
        print(f"🔍 Scanning directory: {directory}")
        
        for ext in self.config["file_extensions_to_scan"]:
            for file_path in dir_path.rglob(f"*{ext}"):
                try:
                    result = self.audit_file(str(file_path))
                    results.append(result)
                except Exception as e:
                    print(f"❌ Error auditing {file_path}: {e}")
        
        return results
    
    def audit_file(self, file_path: str) -> FileAuditResult:
        """Audit a single file"""
        result = FileAuditResult(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result.analyze_content(content)
            
            # Update statistics
            self.summary_statistics["total_files_scanned"] += 1
            if result.gl_platform_universegl_platform_universe.governance_compliance["has_gl_platform_universegl_platform_universe.governance_tags"]:
                self.summary_statistics["files_with_gl_platform_universegl_platform_universe.governance_tags"] += 1
            
            if result.issues:
                self.summary_statistics["files_with_issues"] += 1
                self.summary_statistics["total_issues"] += len(result.issues)
            
            self.summary_statistics["total_recommendations"] += len(result.recommendations)
            
        except UnicodeDecodeError:
            result.warnings.append("Could not read file as UTF-8")
        except Exception as e:
            result.issues.append(f"Error reading file: {str(e)}")
        
        return result
    
    def generate_audit_report(self) -> Dict[str, Any]:
        """Generate comprehensive audit report"""
        # Calculate compliance rate
        if self.summary_statistics["total_files_scanned"] > 0:
            self.summary_statistics["compliance_rate"] = (
                self.summary_statistics["files_with_gl_platform_universegl_platform_universe.governance_tags"] / 
                self.summary_statistics["total_files_scanned"]
            ) * 100
        
        # Categorize results
        by_extension = defaultdict(list)
        by_layer = defaultdict(list)
        by_compliance = defaultdict(list)
        
        for result in self.audit_results:
            by_extension[result.file_extension].append(result)
            
            if result.semantic_analysis["gl_layer"]:
                by_layer[result.semantic_analysis["gl_layer"]].append(result)
            
            if result.issues:
                by_compliance["non_compliant"].append(result)
            else:
                by_compliance["compliant"].append(result)
        
        report = {
            "audit_metadata": {
                "version": self.config["version"],
                "audit_date": self.config["audit_date"],
                "auditor": "GlobalGovernanceAuditor v21.0.0",
                "workspace_root": self.config["workspace_root"]
            },
            "summary_statistics": self.summary_statistics,
            "detailed_statistics": {
                "by_extension": {
                    ext: len(results) for ext, results in by_extension.items()
                },
                "by_gl_layer": {
                    layer: len(results) for layer, results in by_layer.items()
                },
                "compliance_distribution": {
                    "compliant": len(by_compliance["compliant"]),
                    "non_compliant": len(by_compliance["non_compliant"])
                }
            },
            "audit_results": [result.to_dict() for result in self.audit_results],
            "issues_summary": self._generate_issues_summary(),
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_issues_summary(self) -> List[Dict[str, Any]]:
        """Generate summary of all issues found"""
        issues_by_type = defaultdict(list)
        
        for result in self.audit_results:
            for issue in result.issues:
                issues_by_type[issue].append(result.file_path)
        
        return [
            {
                "issue_type": issue_type,
                "affected_files": files,
                "count": len(files)
            }
            for issue_type, files in sorted(issues_by_type.items(), key=lambda x: len(x[1]), reverse=True)
        ]
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations"""
        recommendations_by_priority = defaultdict(list)
        
        for result in self.audit_results:
            for recommendation in result.recommendations:
                recommendations_by_priority[recommendation].append(result.file_path)
        
        return [
            {
                "recommendation": rec,
                "affected_files": files,
                "priority": "high" if len(files) > 10 else "medium" if len(files) > 5 else "low",
                "count": len(files)
            }
            for rec, files in sorted(recommendations_by_priority.items(), key=lambda x: len(x[1]), reverse=True)
        ]
    
    def save_audit_report(self, report: Dict[str, Any]):
        """Save audit report to JSON file"""
        report_path = self.output_dir / "global-gl_platform_universegl_platform_universe.governance-audit-report.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Audit report saved to: {report_path}")
        
        # Also save a summary markdown file
        self.save_markdown_summary(report)
    
    def save_markdown_summary(self, report: Dict[str, Any]):
        """Save markdown summary of audit results"""
        summary_path = self.output_dir / "audit-summary.md"
        
        md_content = f"""# GL Global Governance Audit Report

**Version:** {report['audit_metadata']['version']}  
**Date:** {report['audit_metadata']['audit_date']}  
**Auditor:** {report['audit_metadata']['auditor']}

## Executive Summary

- **Total Files Scanned:** {report['summary_statistics']['total_files_scanned']}
- **Files with Governance Tags:** {report['summary_statistics']['files_with_gl_platform_universegl_platform_universe.governance_tags']}
- **Compliance Rate:** {report['summary_statistics']['compliance_rate']:.2f}%
- **Files with Issues:** {report['summary_statistics']['files_with_issues']}
- **Total Issues:** {report['summary_statistics']['total_issues']}
- **Total Recommendations:** {report['summary_statistics']['total_recommendations']}

## Compliance Status

{'✅' if report['summary_statistics']['compliance_rate'] >= 80 else '⚠️' if report['summary_statistics']['compliance_rate'] >= 50 else '❌'} 
Overall Compliance: **{report['summary_statistics']['compliance_rate']:.2f}%**

## Issues Summary

"""
        
        for issue in report['issues_summary'][:20]:
            md_content += f"""
### {issue['issue_type']}

- **Affected Files:** {issue['count']}
- **Priority:** High
"""
        
        md_content += """

## Recommendations

"""
        
        for rec in report['recommendations'][:20]:
            md_content += f"""
### {rec['recommendation']}

- **Affected Files:** {rec['count']}
- **Priority:** {rec['priority'].upper()}
"""
        
        md_content += """

## Detailed Statistics

### By File Extension

"""
        
        for ext, count in report['detailed_statistics']['by_extension'].items():
            md_content += f"- **{ext or 'No extension'}:** {count} files\n"
        
        md_content += "\n### By GL Layer\n"
        
        for layer, count in report['detailed_statistics']['by_gl_layer'].items():
            md_content += f"- **{layer}:** {count} files\n"
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"📝 Summary saved to: {summary_path}")
    
    def run_audit(self):
        """Run complete audit process"""
        print("🚀 Starting Global Governance Audit...")
        print(f"📁 Workspace Root: {self.config['workspace_root']}")
        print(f"📋 Scan Directories: {len(self.config['scan_directories'])}")
        print()
        
        # Scan all directories
        for directory in self.config["scan_directories"]:
            results = self.scan_directory(directory)
            self.audit_results.extend(results)
            print(f"✅ Scanned {len(results)} files in {directory}\n")
        
        print(f"\n📊 Total files audited: {len(self.audit_results)}")
        print(f"📊 Generating audit report...")
        
        # Generate and save report
        report = self.generate_audit_report()
        self.save_audit_report(report)
        
        print(f"\n✅ Audit completed successfully!")
        print(f"📊 Compliance Rate: {self.summary_statistics['compliance_rate']:.2f}%")
        print(f"📁 Reports saved to: {self.output_dir}")

# ============================================================================
# Main Execution
# ============================================================================

if __name__ == "__main__":
    print("GL Global Governance Audit Script v21.0.0")
    print("=" * 60)
    print()
    
    auditor = GlobalGovernanceAuditor(AUDIT_CONFIG)
    auditor.run_audit()