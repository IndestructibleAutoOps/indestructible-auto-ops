#!/usr/bin/env python3
"""
Narrative Filter Engine - Beyond Era-1 Governance Verification

Detects and filters narrative language, fuzzy semantics, platform fantasy,
and governance exaggeration in governance reports and documentation.

Purpose: Ensure IndestructibleAutoOps produces only verifiable, factual,
hash-sealed content without subjective language or unsupported claims.
"""

import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class NarrativeViolation:
    """Represents a narrative violation found in text"""
    category: str
    pattern: str
    match: str
    context: str
    line_number: int
    hash: str
    suggestion: str


class NarrativeFilterEngine:
    """
    Narrative Filter Engine for detecting narrative violations in governance reports.
    
    Detects:
    - Narrative statements (subjective language)
    - Fuzzy semantics (imprecise language)
    - Platform fantasy (unsupported claims about platform capabilities)
    - Governance exaggeration (absolute claims without evidence)
    """
    
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = Path(workspace)
        self.evidence_dir = self.workspace / "ecosystem" / "evidence" / "governance"
        
        # Define narrative patterns
        self.patterns = {
            "narrative_statements": {
                "patterns": [
                    r"我們相信",
                    r"我們認為",
                    r"我們期望",
                    r"我們預期",
                    r"我們希望",
                    r"這代表",
                    r"這意味著",
                    r"這表明",
                    r"這將會",
                    r"我們覺得"
                ],
                "severity": "medium",
                "suggestion": "請改為可驗證語義，使用 '根據'、'基於'、'驗證結果顯示' 等客觀表達"
            },
            "fuzzy_semantics": {
                "patterns": [
                    r"可能",
                    r"或許",
                    r"應該",
                    r"大概",
                    r"大約",
                    r"估計",
                    r"預期",
                    r"可能會",
                    r"差不多",
                    r"基本上"
                ],
                "severity": "medium",
                "suggestion": "請使用精確的量化指標或確定的語義"
            },
            "platform_fantasy": {
                "patterns": [
                    r"平台將自動",
                    r"AI 將自行",
                    r"系統會智能",
                    r"自動演化",
                    r"自主決策",
                    r"自動學習",
                    r"智能適應",
                    r"自我優化",
                    r"自動理解",
                    r"無需干預"
                ],
                "severity": "critical",
                "suggestion": "請提供具體的實現細節、驗證方法、或引用相關證據"
            },
            "governance_exaggeration": {
                "patterns": [
                    r"完美",
                    r"無漏洞",
                    r"絕對",
                    r"100%保證",
                    r"絕不",
                    r"完全",
                    r"零風險",
                    r"無懈可擊",
                    r"絕無例外",
                    r"萬無一失"
                ],
                "severity": "critical",
                "suggestion": "請提供具體的測試覆蓋率、驗證結果、或限制條件說明"
            }
        }
    
    def detect_narrative_violations(self, text: str, file_path: Optional[str] = None) -> List[NarrativeViolation]:
        """
        Detect narrative violations in text.
        
        Args:
            text: Text to analyze
            file_path: Optional file path for context
        
        Returns:
            List of NarrativeViolation objects
        """
        violations = []
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            for category, config in self.patterns.items():
                for pattern in config["patterns"]:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        # Get context (surrounding text)
                        start = max(0, match.start() - 50)
                        end = min(len(line), match.end() + 50)
                        context = line[start:end].strip()
                        
                        # Generate hash of violation
                        violation_hash = hashlib.sha256(
                            f"{category}:{match.group()}:{file_path}:{line_num}".encode()
                        ).hexdigest()
                        
                        violation = NarrativeViolation(
                            category=category,
                            pattern=pattern,
                            match=match.group(),
                            context=context,
                            line_number=line_num,
                            hash=f"sha256:{violation_hash}",
                            suggestion=config["suggestion"]
                        )
                        violations.append(violation)
        
        return violations
    
    def scan_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Scan a file for narrative violations.
        
        Args:
            file_path: Path to file to scan
        
        Returns:
            Scan result dictionary
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "file": str(file_path.relative_to(self.workspace)),
                "status": "error",
                "error": str(e)
            }
        
        violations = self.detect_narrative_violations(content, str(file_path))
        
        # Categorize violations by severity
        critical_violations = [v for v in violations if self.patterns[v.category]["severity"] == "critical"]
        medium_violations = [v for v in violations if self.patterns[v.category]["severity"] == "medium"]
        
        return {
            "file": str(file_path.relative_to(self.workspace)),
            "status": "scanned",
            "total_violations": len(violations),
            "critical_violations": len(critical_violations),
            "medium_violations": len(medium_violations),
            "violations": [asdict(v) for v in violations],
            "file_hash": f"sha256:{hashlib.sha256(content.encode()).hexdigest()}"
        }
    
    def scan_directory(self, directory: Path, file_patterns: List[str] = None) -> Dict[str, Any]:
        """
        Scan all files in a directory for narrative violations.
        
        Args:
            directory: Directory to scan
            file_patterns: List of file patterns to include (e.g., ["*.md", "*.json"])
        
        Returns:
            Scan result dictionary
        """
        if file_patterns is None:
            file_patterns = ["*.md", "*.json", "*.yaml", "*.yml"]
        
        results = []
        total_violations = 0
        total_critical = 0
        total_medium = 0
        
        for pattern in file_patterns:
            for file_path in directory.rglob(pattern):
                # Skip hidden files and evidence directory
                if file_path.name.startswith('.') or 'evidence/' in str(file_path):
                    continue
                
                result = self.scan_file(file_path)
                results.append(result)
                
                if result["status"] == "scanned":
                    total_violations += result["total_violations"]
                    total_critical += result["critical_violations"]
                    total_medium += result["medium_violations"]
        
        return {
            "scan_status": "completed",
            "directory": str(directory.relative_to(self.workspace)),
            "files_scanned": len(results),
            "total_violations": total_violations,
            "total_critical": total_critical,
            "total_medium": total_medium,
            "scan_timestamp": datetime.utcnow().isoformat() + "Z",
            "results": results
        }
    
    def generate_report(self, scan_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive narrative violation report.
        
        Args:
            scan_results: Results from scan_directory
        
        Returns:
            Report dictionary
        """
        # Collect all violations
        all_violations = []
        for result in scan_results["results"]:
            if result["status"] == "scanned":
                all_violations.extend(result["violations"])
        
        # Group by category
        violations_by_category = {}
        for violation in all_violations:
            category = violation["category"]
            if category not in violations_by_category:
                violations_by_category[category] = []
            violations_by_category[category].append(violation)
        
        # Generate statistics
        report = {
            "report_id": f"narrative-violation-report-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "scan_summary": {
                "directory_scanned": scan_results["directory"],
                "files_scanned": scan_results["files_scanned"],
                "total_violations": scan_results["total_violations"],
                "critical_violations": scan_results["total_critical"],
                "medium_violations": scan_results["total_medium"]
            },
            "violations_by_category": {
                category: {
                    "count": len(violations),
                    "severity": self.patterns[category]["severity"],
                    "violations": violations
                }
                for category, violations in violations_by_category.items()
            },
            "recommendations": self._generate_recommendations(scan_results),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Generate report hash
        report_hash = hashlib.sha256(json.dumps(report, sort_keys=True).encode()).hexdigest()
        report["hash"] = f"sha256:{report_hash}"
        
        return report
    
    def _generate_recommendations(self, scan_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on scan results"""
        recommendations = []
        
        if scan_results["total_critical"] > 0:
            recommendations.append(
                f"發現 {scan_results['total_critical']} 個嚴重違規（平台幻想或治理誇大），"
                "必須立即修正以確保治理報告的可信度。"
            )
        
        if scan_results["total_medium"] > 0:
            recommendations.append(
                f"發現 {scan_results['total_medium']} 個中等違規（敘述性語言或模糊語義），"
                "建議修正以提高報告的客觀性和精確性。"
            )
        
        if scan_results["total_violations"] == 0:
            recommendations.append(
                "未發現敘事違規，所有治理報告符合可驗證語義標準。"
            )
        
        # Category-specific recommendations
        for result in scan_results["results"]:
            if result["status"] == "scanned":
                for violation in result["violations"]:
                    if violation["category"] == "platform_fantasy":
                        recommendations.append(
                            f"在 {result['file']} 中發現平台幻想：'{violation['match']}'。"
                            f"請提供具體實現細節或驗證方法。"
                        )
                    elif violation["category"] == "governance_exaggeration":
                        recommendations.append(
                            f"在 {result['file']} 中發現治理誇大：'{violation['match']}'。"
                            f"請提供測試覆蓋率或限制條件。"
                        )
        
        # Deduplicate recommendations
        recommendations = list(dict.fromkeys(recommendations))
        
        return recommendations
    
    def save_violations(self, scan_results: Dict[str, Any], output_path: Path = None) -> Path:
        """
        Save narrative violations to JSON file.
        
        Args:
            scan_results: Results from scan_directory
            output_path: Optional output path (default: evidence/governance/narrative_violations.json)
        
        Returns:
            Path to saved file
        """
        if output_path is None:
            output_path = self.evidence_dir / "narrative_violations.json"
        
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate full report
        report = self.generate_report(scan_results)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        return output_path


def main():
    """Main entry point for narrative filter engine"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Narrative Filter Engine")
    parser.add_argument("--scan", action="store_true", help="Scan for narrative violations")
    parser.add_argument("--directory", default="ecosystem/governance", help="Directory to scan")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--workspace", default="/workspace", help="Workspace path")
    
    args = parser.parse_args()
    
    if not args.scan:
        parser.print_help()
        return
    
    # Initialize engine
    engine = NarrativeFilterEngine(workspace=args.workspace)
    
    # Scan directory
    scan_dir = Path(args.workspace) / args.directory
    print(f"[INFO] Scanning directory: {scan_dir}")
    
    scan_results = engine.scan_directory(scan_dir)
    
    # Save results
    output_path = args.output if args.output else None
    saved_path = engine.save_violations(scan_results, Path(output_path) if output_path else None)
    
    print(f"[INFO] Scan complete")
    print(f"[INFO] Files scanned: {scan_results['files_scanned']}")
    print(f"[INFO] Total violations: {scan_results['total_violations']}")
    print(f"[INFO] Critical violations: {scan_results['total_critical']}")
    print(f"[INFO] Medium violations: {scan_results['total_medium']}")
    print(f"[INFO] Results saved to: {saved_path}")
    
    # Exit with error code if critical violations found
    if scan_results["total_critical"] > 0:
        print(f"[ERROR] Found {scan_results['total_critical']} critical narrative violations")
        exit(1)


if __name__ == "__main__":
    main()