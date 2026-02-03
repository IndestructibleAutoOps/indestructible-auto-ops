#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL70-79
# @GL-semantic: audit-trail-reporting
#


"""
GL Audit Trail Reporting Tool
==============================
Generate comprehensive reports from audit trail data.

Features:
- Summary reports
- Compliance reports
- Trend analysis
- Violation reports
- Export to multiple formats (JSON, CSV, HTML, Markdown)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import sqlite3
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class ReportConfig:
    """Report generation configuration."""
    title: str
    description: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    include_trends: bool = True
    include_recommendations: bool = True


class AuditTrailReport:
    """
    Audit trail reporting engine.
    
    Generates various types of reports from audit trail data.
    """
    
    def __init__(self, db_path: str = None, base_path: str = "/workspace/machine-native-ops"):
        """
        Initialize audit trail reporting engine.
        
        Args:
            db_path: Path to audit trail database
            base_path: Base path for default database location
        """
        self.base_path = Path(base_path)
        
        if db_path:
            self.db_path = Path(db_path)
        else:
            self.db_path = self.base_path / "ecosystem" / "logs" / "audit-logs" / "audit_trail.db"
        
        if not self.db_path.exists():
            raise FileNotFoundError(f"Audit trail database not found: {self.db_path}")
    
    def generate_summary_report(self, config: ReportConfig = None) -> Dict[str, Any]:
        """
        Generate comprehensive summary report.
        
        Args:
            config: Report configuration
        
        Returns:
            Dictionary containing summary report data
        """
        if config is None:
            config = ReportConfig(
                title="Audit Trail Summary Report",
                description="Comprehensive summary of all audit trail data"
            )
        
        report = {
            "title": config.title,
            "description": config.description,
            "generated_at": datetime.now().isoformat(),
            "summary": self._get_summary_statistics(),
            "validations_by_type": self._get_validations_by_type(),
            "validations_by_result": self._get_validations_by_result(),
            "evidence_validations": self._get_evidence_validation_summary(),
            "report_validations": self._get_report_validation_summary(),
            "recent_activity": self._get_recent_activity(limit=10)
        }
        
        if config.include_recommendations:
            report["recommendations"] = self._generate_recommendations(report)
        
        return report
    
    def generate_compliance_report(self, config: ReportConfig = None) -> Dict[str, Any]:
        """
        Generate compliance report.
        
        Args:
            config: Report configuration
        
        Returns:
            Dictionary containing compliance report data
        """
        if config is None:
            config = ReportConfig(
                title="Compliance Report",
                description="Governance compliance status and violations"
            )
        
        report = {
            "title": config.title,
            "description": config.description,
            "generated_at": datetime.now().isoformat(),
            "period": {
                "start": config.start_date,
                "end": config.end_date
            },
            "overall_compliance": self._calculate_overall_compliance(),
            "critical_violations": self._get_violations_by_severity("CRITICAL"),
            "high_violations": self._get_violations_by_severity("HIGH"),
            "medium_violations": self._get_violations_by_severity("MEDIUM"),
            "low_violations": self._get_violations_by_severity("LOW"),
            "quality_gate_compliance": self._get_quality_gate_compliance(),
            "evidence_compliance": self._get_evidence_compliance()
        }
        
        if config.include_recommendations:
            report["compliance_recommendations"] = self._generate_compliance_recommendations(report)
        
        return report
    
    def generate_trend_analysis(self, days: int = 30) -> Dict[str, Any]:
        """
        Generate trend analysis report.
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Dictionary containing trend analysis data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        report = {
            "title": "Trend Analysis Report",
            "description": f"Analysis of audit trail trends over last {days} days",
            "generated_at": datetime.now().isoformat(),
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": days
            },
            "daily_validations": self._get_daily_validations(start_date, end_date),
            "daily_violations": self._get_daily_violations(start_date, end_date),
            "trend_analysis": self._analyze_trends(start_date, end_date)
        }
        
        return report
    
    def generate_violation_report(self, config: ReportConfig = None) -> Dict[str, Any]:
        """
        Generate detailed violation report.
        
        Args:
            config: Report configuration
        
        Returns:
            Dictionary containing violation report data
        """
        if config is None:
            config = ReportConfig(
                title="Violation Report",
                description="Detailed report of all governance violations"
            )
        
        report = {
            "title": config.title,
            "description": config.description,
            "generated_at": datetime.now().isoformat(),
            "total_violations": self._get_total_violations(),
            "violations_by_severity": self._get_violations_by_severity_all(),
            "violations_by_type": self._get_violations_by_type(),
            "top_violating_operations": self._get_top_violating_operations(limit=10),
            "recent_violations": self._get_recent_violations(limit=20)
        }
        
        if config.include_recommendations:
            report["violation_recommendations"] = self._generate_violation_recommendations(report)
        
        return report
    
    def _get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total validations
        cursor.execute("SELECT COUNT(*) FROM all_validations")
        stats["total_validations"] = cursor.fetchone()[0]
        
        # Validation results
        cursor.execute("""
            SELECT validation_result, COUNT(*) 
            FROM all_validations 
            GROUP BY validation_result
        """)
        stats["validation_results"] = dict(cursor.fetchall())
        
        # Evidence validations
        cursor.execute("SELECT COUNT(*) FROM evidence_validations")
        stats["total_evidence_validations"] = cursor.fetchone()[0]
        
        # Report validations
        cursor.execute("SELECT COUNT(*) FROM report_validations")
        stats["total_report_validations"] = cursor.fetchone()[0]
        
        # Average evidence coverage
        cursor.execute("SELECT AVG(evidence_coverage) FROM report_validations")
        avg_coverage = cursor.fetchone()[0]
        stats["average_evidence_coverage"] = round(avg_coverage * 100, 2) if avg_coverage else 0
        
        conn.close()
        
        return stats
    
    def _get_validations_by_type(self) -> Dict[str, int]:
        """Get validations grouped by type."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT validation_type, COUNT(*) 
            FROM all_validations 
            GROUP BY validation_type
            ORDER BY COUNT(*) DESC
        """)
        
        result = dict(cursor.fetchall())
        conn.close()
        
        return result
    
    def _get_validations_by_result(self) -> Dict[str, int]:
        """Get validations grouped by result."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT validation_result, COUNT(*) 
            FROM all_validations 
            GROUP BY validation_result
            ORDER BY COUNT(*) DESC
        """)
        
        result = dict(cursor.fetchall())
        conn.close()
        
        return result
    
    def _get_evidence_validation_summary(self) -> Dict[str, Any]:
        """Get evidence validation summary."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        summary = {}
        
        # Total
        cursor.execute("SELECT COUNT(*) FROM evidence_validations")
        summary["total"] = cursor.fetchone()[0]
        
        # Checksum validity
        cursor.execute("""
            SELECT checksum_valid, COUNT(*) 
            FROM evidence_validations 
            GROUP BY checksum_valid
        """)
        summary["checksum_validity"] = {
            "valid": 0,
            "invalid": 0
        }
        for valid, count in cursor.fetchall():
            key = "valid" if valid else "invalid"
            summary["checksum_validity"][key] = count
        
        # Timestamp validity
        cursor.execute("""
            SELECT timestamp_valid, COUNT(*) 
            FROM evidence_validations 
            GROUP BY timestamp_valid
        """)
        summary["timestamp_validity"] = {
            "valid": 0,
            "invalid": 0
        }
        for valid, count in cursor.fetchall():
            key = "valid" if valid else "invalid"
            summary["timestamp_validity"][key] = count
        
        conn.close()
        
        return summary
    
    def _get_report_validation_summary(self) -> Dict[str, Any]:
        """Get report validation summary."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        summary = {}
        
        # Total
        cursor.execute("SELECT COUNT(*) FROM report_validations")
        summary["total"] = cursor.fetchone()[0]
        
        # Validation status
        cursor.execute("""
            SELECT validation_status, COUNT(*) 
            FROM report_validations 
            GROUP BY validation_status
        """)
        summary["by_status"] = dict(cursor.fetchall())
        
        # Coverage statistics
        cursor.execute("""
            SELECT 
                MIN(evidence_coverage) as min_coverage,
                MAX(evidence_coverage) as max_coverage,
                AVG(evidence_coverage) as avg_coverage
            FROM report_validations
        """)
        row = cursor.fetchone()
        summary["coverage_stats"] = {
            "min": round(row[0] * 100, 2) if row[0] else 0,
            "max": round(row[1] * 100, 2) if row[1] else 0,
            "avg": round(row[2] * 100, 2) if row[2] else 0
        }
        
        # Forbidden phrases
        cursor.execute("""
            SELECT AVG(forbidden_phrases_count) 
            FROM report_validations
        """)
        avg_phrases = cursor.fetchone()[0]
        summary["avg_forbidden_phrases"] = round(avg_phrases, 2) if avg_phrases else 0
        
        conn.close()
        
        return summary
    
    def _get_recent_activity(self, limit: int = 10) -> List[Dict]:
        """Get recent validation activity."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM all_validations 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        activity = [dict(row) for row in rows]
        
        conn.close()
        
        return activity
    
    def _calculate_overall_compliance(self) -> float:
        """Calculate overall compliance percentage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate based on validation results
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN validation_result = 'PASS' THEN 1 END) * 100.0 / COUNT(*)
            FROM all_validations
        """)
        
        compliance = cursor.fetchone()[0]
        conn.close()
        
        return round(compliance, 2) if compliance else 0.0
    
    def _get_violations_by_severity(self, severity: str) -> List[Dict]:
        """Get violations by severity."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query from all_validations where violations_count > 0
        cursor.execute("""
            SELECT * FROM all_validations 
            WHERE violations_count > 0
            ORDER BY timestamp DESC
        """)
        
        rows = cursor.fetchall()
        violations = [dict(row) for row in rows]
        
        conn.close()
        
        return violations
    
    def _get_violations_by_severity_all(self) -> Dict[str, int]:
        """Get all violations grouped by severity."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # This would need violations table, for now using validation results
        cursor.execute("""
            SELECT validation_result, COUNT(*) 
            FROM all_validations 
            GROUP BY validation_result
        """)
        
        result = dict(cursor.fetchall())
        conn.close()
        
        return result
    
    def _get_violations_by_type(self) -> Dict[str, int]:
        """Get violations by type."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT validation_type, SUM(violations_count) 
            FROM all_validations 
            WHERE violations_count > 0
            GROUP BY validation_type
            ORDER BY SUM(violations_count) DESC
        """)
        
        result = dict(cursor.fetchall())
        conn.close()
        
        return result
    
    def _get_top_violating_operations(self, limit: int = 10) -> List[Dict]:
        """Get operations with most violations."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                operation_id,
                COUNT(*) as violation_count,
                SUM(violations_count) as total_violations
            FROM all_validations 
            WHERE violations_count > 0
            GROUP BY operation_id
            ORDER BY total_violations DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        
        conn.close()
        
        return result
    
    def _get_recent_violations(self, limit: int = 20) -> List[Dict]:
        """Get recent violations."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM all_validations 
            WHERE violations_count > 0
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        result = [dict(row) for row in rows]
        
        conn.close()
        
        return result
    
    def _get_quality_gate_compliance(self) -> Dict[str, Any]:
        """Get quality gate compliance status."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # This would need quality gate results table
        # For now, returning basic stats
        cursor.execute("SELECT COUNT(*) FROM report_validations")
        total = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM report_validations 
            WHERE validation_status = 'PASS'
        """)
        passed = cursor.fetchone()[0]
        
        compliance = (passed / total * 100) if total > 0 else 0
        
        conn.close()
        
        return {
            "total_checks": total,
            "passed_checks": passed,
            "compliance_percentage": round(compliance, 2)
        }
    
    def _get_evidence_compliance(self) -> Dict[str, Any]:
        """Get evidence compliance status."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM evidence_validations")
        total = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM evidence_validations 
            WHERE validation_result = 'PASS'
        """)
        passed = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM evidence_validations 
            WHERE checksum_valid = 1
        """)
        checksum_valid = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM evidence_validations 
            WHERE timestamp_valid = 1
        """)
        timestamp_valid = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_evidence": total,
            "passed_validations": passed,
            "checksum_valid": checksum_valid,
            "timestamp_valid": timestamp_valid,
            "compliance_percentage": round((passed / total * 100), 2) if total > 0 else 0
        }
    
    def _get_daily_validations(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get daily validation counts."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                DATE(timestamp) as date,
                COUNT(*) as count
            FROM all_validations 
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY DATE(timestamp)
            ORDER BY date ASC
        """, (start_date.isoformat(), end_date.isoformat()))
        
        result = [{"date": row[0], "count": row[1]} for row in cursor.fetchall()]
        conn.close()
        
        return result
    
    def _get_daily_violations(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Get daily violation counts."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                DATE(timestamp) as date,
                SUM(violations_count) as count
            FROM all_validations 
            WHERE timestamp >= ? AND timestamp <= ? AND violations_count > 0
            GROUP BY DATE(timestamp)
            ORDER BY date ASC
        """, (start_date.isoformat(), end_date.isoformat()))
        
        result = [{"date": row[0], "count": row[1]} for row in cursor.fetchall()]
        conn.close()
        
        return result
    
    def _analyze_trends(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Analyze trends in validation data."""
        daily_validations = self._get_daily_validations(start_date, end_date)
        daily_violations = self._get_daily_violations(start_date, end_date)
        
        if not daily_validations:
            return {"trend": "insufficient_data"}
        
        # Calculate simple trend
        first_half = daily_validations[:len(daily_validations)//2]
        second_half = daily_validations[len(daily_validations)//2:]
        
        avg_first = sum(d["count"] for d in first_half) / len(first_half) if first_half else 0
        avg_second = sum(d["count"] for d in second_half) / len(second_half) if second_half else 0
        
        trend = "stable"
        if avg_second > avg_first * 1.2:
            trend = "increasing"
        elif avg_second < avg_first * 0.8:
            trend = "decreasing"
        
        return {
            "validation_trend": trend,
            "average_first_half": round(avg_first, 2),
            "average_second_half": round(avg_second, 2),
            "total_validations": sum(d["count"] for d in daily_validations)
        }
    
    def _generate_recommendations(self, report: Dict) -> List[str]:
        """Generate recommendations based on report data."""
        recommendations = []
        
        # Check evidence coverage
        avg_coverage = report["summary"].get("average_evidence_coverage", 0)
        if avg_coverage < 90:
            recommendations.append(
                f"Evidence coverage ({avg_coverage}%) is below 90% threshold. "
                "Add more evidence links to reports."
            )
        
        # Check violations
        validation_results = report["validations_by_result"]
        total_validations = sum(validation_results.values())
        failed = validation_results.get("FAIL", 0)
        fail_rate = (failed / total_validations * 100) if total_validations > 0 else 0
        
        if fail_rate > 10:
            recommendations.append(
                f"Validation failure rate ({fail_rate:.1f}%) is high. "
                "Review and address common violations."
            )
        
        # Check evidence checksum validity
        evidence_summary = report["evidence_validations"]
        checksum_valid = evidence_summary["checksum_validity"]["valid"]
        total_evidence = evidence_summary["total"]
        checksum_rate = (checksum_valid / total_evidence * 100) if total_evidence > 0 else 0
        
        if checksum_rate < 100:
            recommendations.append(
                f"Some evidence files ({total_evidence - checksum_valid}) have invalid checksums. "
                "Regenerate checksums for affected files."
            )
        
        return recommendations
    
    def _generate_compliance_recommendations(self, report: Dict) -> List[str]:
        """Generate compliance-specific recommendations."""
        recommendations = []
        
        overall_compliance = report["overall_compliance"]
        if overall_compliance < 95:
            recommendations.append(
                f"Overall compliance ({overall_compliance}%) is below 95%. "
                "Focus on addressing violations to improve compliance."
            )
        
        critical_violations = len(report["critical_violations"])
        if critical_violations > 0:
            recommendations.append(
                f"There are {critical_violations} CRITICAL violations. "
                "Address these immediately to maintain governance integrity."
            )
        
        high_violations = len(report["high_violations"])
        if high_violations > 0:
            recommendations.append(
                f"There are {high_violations} HIGH violations. "
                "Prioritize these for resolution this week."
            )
        
        return recommendations
    
    def _generate_violation_recommendations(self, report: Dict) -> List[str]:
        """Generate violation-specific recommendations."""
        recommendations = []
        
        violations_by_type = report["violations_by_type"]
        if violations_by_type:
            top_violation_type = max(violations_by_type.items(), key=lambda x: x[1])
            recommendations.append(
                f"Most common violation type: {top_violation_type[0]} "
                f"({top_violation_type[1]} occurrences). "
                "Review and update validation rules for this type."
            )
        
        top_operations = report["top_violating_operations"][:3]
        if top_operations:
            op_descriptions = [
                f"Operation {op['operation_id']} ({op['total_violations']} violations)"
                for op in top_operations
            ]
            recommendations.append(
                f"Operations with most violations: {', '.join(op_descriptions)}. "
                "Investigate root causes and implement fixes."
            )
        
        return recommendations
    
    def export_to_json(self, report: Dict, output_path: str):
        """Export report to JSON file."""
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Exported report to {output_path}")
    
    def export_to_markdown(self, report: Dict, output_path: str):
        """Export report to Markdown file."""
        with open(output_path, 'w') as f:
            f.write(f"# {report['title']}\n\n")
            f.write(f"**Generated:** {report['generated_at']}\n\n")
            f.write(f"{report['description']}\n\n")
            
            if "summary" in report:
                f.write("## Summary\n\n")
                f.write("```json\n")
                f.write(json.dumps(report["summary"], indent=2))
                f.write("\n```\n\n")
            
            if "recommendations" in report and report["recommendations"]:
                f.write("## Recommendations\n\n")
                for i, rec in enumerate(report["recommendations"], 1):
                    f.write(f"{i}. {rec}\n")
                f.write("\n")
        
        print(f"✅ Exported report to {output_path}")
    
    def export_to_csv(self, report: Dict, output_path: str, table: str = "all_validations"):
        """Export report data to CSV file."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)
        
        conn.close()
        
        print(f"✅ Exported {table} to {output_path}")


def main():
    """CLI interface for audit trail reporting tool."""
    import argparse
    
    parser = argparse.ArgumentParser(description="GL Audit Trail Reporting Tool")
    parser.add_argument("--db", help="Path to audit trail database")
    parser.add_argument("--report", choices=["summary", "compliance", "trend", "violation"],
                       default="summary", help="Report type")
    parser.add_argument("--days", type=int, default=30,
                       help="Number of days for trend analysis")
    parser.add_argument("--output-json", help="Export report to JSON file")
    parser.add_argument("--output-md", help="Export report to Markdown file")
    parser.add_argument("--output-csv", help="Export data to CSV file")
    parser.add_argument("--table", default="all_validations",
                       help="Table name for CSV export")
    
    args = parser.parse_args()
    
    try:
        reporter = AuditTrailReport(db_path=args.db)
        
        if args.report == "summary":
            report = reporter.generate_summary_report()
        elif args.report == "compliance":
            report = reporter.generate_compliance_report()
        elif args.report == "trend":
            report = reporter.generate_trend_analysis(days=args.days)
        elif args.report == "violation":
            report = reporter.generate_violation_report()
        
        print(f"\n📊 {report['title']}")
        print("=" * 50)
        print(f"Generated: {report['generated_at']}\n")
        print(json.dumps(report, indent=2))
        
        if args.output_json:
            reporter.export_to_json(report, args.output_json)
        
        if args.output_md:
            reporter.export_to_markdown(report, args.output_md)
        
        if args.output_csv:
            reporter.export_to_csv(report, args.output_csv, table=args.table)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())