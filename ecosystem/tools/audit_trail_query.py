#!/usr/bin/env python3

"""
GL Audit Trail Query Tool
=========================
Query and analyze audit trail data from SQLite database.

Features:
- Query all validation records
- Filter by date, operation type, status
- Sort by various fields
- Export to JSON/CSV
- Generate summary statistics
"""

import sqlite3
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class QueryResult:
    """Query result with metadata."""
    records: List[Dict]
    count: int
    query_time: str
    filters_applied: Dict[str, Any]


class AuditTrailQuery:
    """
    Audit trail query engine.
    
    Provides methods to query audit trail database with filtering,
    sorting, and export capabilities.
    """
    
    def __init__(self, db_path: str = None, base_path: str = "/workspace/machine-native-ops"):
        """
        Initialize audit trail query engine.
        
        Args:
            db_path: Path to audit trail database (default: ecosystem/logs/audit-logs/audit_trail.db)
            base_path: Base path for default database location
        """
        self.base_path = Path(base_path)
        
        if db_path:
            self.db_path = Path(db_path)
        else:
            self.db_path = self.base_path / "ecosystem" / "logs" / "audit-logs" / "audit_trail.db"
        
        if not self.db_path.exists():
            raise FileNotFoundError(f"Audit trail database not found: {self.db_path}")
    
    def query_all_validations(self, 
                             operation_id: Optional[str] = None,
                             contract_path: Optional[str] = None,
                             validation_type: Optional[str] = None,
                             validation_result: Optional[str] = None,
                             start_date: Optional[str] = None,
                             end_date: Optional[str] = None,
                             limit: Optional[int] = None,
                             order_by: str = "timestamp",
                             order_desc: bool = True) -> QueryResult:
        """
        Query all validation records.
        
        Args:
            operation_id: Filter by operation ID
            contract_path: Filter by contract path
            validation_type: Filter by validation type
            validation_result: Filter by result (PASS, FAIL, WARNING)
            start_date: Filter records after this date (ISO 8601)
            end_date: Filter records before this date (ISO 8601)
            limit: Limit number of results
            order_by: Sort field (timestamp, operation_id, validation_result)
            order_desc: Sort descending if True
        
        Returns:
            QueryResult with records and metadata
        """
        query = "SELECT * FROM all_validations WHERE 1=1"
        params = []
        filters = {}
        
        # Apply filters
        if operation_id:
            query += " AND operation_id = ?"
            params.append(operation_id)
            filters["operation_id"] = operation_id
        
        if contract_path:
            query += " AND contract_path LIKE ?"
            params.append(f"%{contract_path}%")
            filters["contract_path"] = contract_path
        
        if validation_type:
            query += " AND validation_type = ?"
            params.append(validation_type)
            filters["validation_type"] = validation_type
        
        if validation_result:
            query += " AND validation_result = ?"
            params.append(validation_result)
            filters["validation_result"] = validation_result
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
            filters["start_date"] = start_date
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
            filters["end_date"] = end_date
        
        # Order
        query += f" ORDER BY {order_by}"
        if order_desc:
            query += " DESC"
        
        # Limit
        if limit:
            query += " LIMIT ?"
            params.append(limit)
            filters["limit"] = limit
        
        # Execute query
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Convert to list of dicts
        records = [dict(row) for row in rows]
        
        conn.close()
        
        return QueryResult(
            records=records,
            count=len(records),
            query_time=datetime.now().isoformat(),
            filters_applied=filters
        )
    
    def query_evidence_validations(self,
                                  operation_id: Optional[str] = None,
                                  evidence_path: Optional[str] = None,
                                  checksum_valid: Optional[bool] = None,
                                  timestamp_valid: Optional[bool] = None,
                                  validation_result: Optional[str] = None,
                                  limit: Optional[int] = None) -> QueryResult:
        """
        Query evidence validation records.
        
        Args:
            operation_id: Filter by operation ID
            evidence_path: Filter by evidence path
            checksum_valid: Filter by checksum validity
            timestamp_valid: Filter by timestamp validity
            validation_result: Filter by result (PASS, FAIL)
            limit: Limit number of results
        
        Returns:
            QueryResult with records and metadata
        """
        query = "SELECT * FROM evidence_validations WHERE 1=1"
        params = []
        filters = {}
        
        if operation_id:
            query += " AND operation_id = ?"
            params.append(operation_id)
            filters["operation_id"] = operation_id
        
        if evidence_path:
            query += " AND evidence_path LIKE ?"
            params.append(f"%{evidence_path}%")
            filters["evidence_path"] = evidence_path
        
        if checksum_valid is not None:
            query += " AND checksum_valid = ?"
            params.append(1 if checksum_valid else 0)
            filters["checksum_valid"] = checksum_valid
        
        if timestamp_valid is not None:
            query += " AND timestamp_valid = ?"
            params.append(1 if timestamp_valid else 0)
            filters["timestamp_valid"] = timestamp_valid
        
        if validation_result:
            query += " AND validation_result = ?"
            params.append(validation_result)
            filters["validation_result"] = validation_result
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
            filters["limit"] = limit
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        records = [dict(row) for row in rows]
        
        conn.close()
        
        return QueryResult(
            records=records,
            count=len(records),
            query_time=datetime.now().isoformat(),
            filters_applied=filters
        )
    
    def query_report_validations(self,
                                report_id: Optional[str] = None,
                                min_coverage: Optional[float] = None,
                                max_coverage: Optional[float] = None,
                                validation_status: Optional[str] = None,
                                limit: Optional[int] = None) -> QueryResult:
        """
        Query report validation records.
        
        Args:
            report_id: Filter by report ID
            min_coverage: Filter by minimum evidence coverage
            max_coverage: Filter by maximum evidence coverage
            validation_status: Filter by validation status
            limit: Limit number of results
        
        Returns:
            QueryResult with records and metadata
        """
        query = "SELECT * FROM report_validations WHERE 1=1"
        params = []
        filters = {}
        
        if report_id:
            query += " AND report_id = ?"
            params.append(report_id)
            filters["report_id"] = report_id
        
        if min_coverage is not None:
            query += " AND evidence_coverage >= ?"
            params.append(min_coverage)
            filters["min_coverage"] = min_coverage
        
        if max_coverage is not None:
            query += " AND evidence_coverage <= ?"
            params.append(max_coverage)
            filters["max_coverage"] = max_coverage
        
        if validation_status:
            query += " AND validation_status = ?"
            params.append(validation_status)
            filters["validation_status"] = validation_status
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
            filters["limit"] = limit
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        records = [dict(row) for row in rows]
        
        conn.close()
        
        return QueryResult(
            records=records,
            count=len(records),
            query_time=datetime.now().isoformat(),
            filters_applied=filters
        )
    
    def query_proof_chain_validations(self,
                                      chain_id: Optional[str] = None,
                                      chain_integrity_status: Optional[str] = None,
                                      circular_references: Optional[bool] = None,
                                      limit: Optional[int] = None) -> QueryResult:
        """
        Query proof chain validation records.
        
        Args:
            chain_id: Filter by chain ID
            chain_integrity_status: Filter by integrity status
            circular_references: Filter by circular references
            limit: Limit number of results
        
        Returns:
            QueryResult with records and metadata
        """
        query = "SELECT * FROM proof_chain_validations WHERE 1=1"
        params = []
        filters = {}
        
        if chain_id:
            query += " AND chain_id = ?"
            params.append(chain_id)
            filters["chain_id"] = chain_id
        
        if chain_integrity_status:
            query += " AND chain_integrity_status = ?"
            params.append(chain_integrity_status)
            filters["chain_integrity_status"] = chain_integrity_status
        
        if circular_references is not None:
            query += " AND circular_references = ?"
            params.append(1 if circular_references else 0)
            filters["circular_references"] = circular_references
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
            filters["limit"] = limit
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        records = [dict(row) for row in rows]
        
        conn.close()
        
        return QueryResult(
            records=records,
            count=len(records),
            query_time=datetime.now().isoformat(),
            filters_applied=filters
        )
    
    def export_to_json(self, result: QueryResult, output_path: str):
        """
        Export query results to JSON file.
        
        Args:
            result: QueryResult to export
            output_path: Output file path
        """
        with open(output_path, 'w') as f:
            json.dump({
                "query_time": result.query_time,
                "count": result.count,
                "filters_applied": result.filters_applied,
                "records": result.records
            }, f, indent=2)
        
        print(f"✅ Exported {result.count} records to {output_path}")
    
    def export_to_csv(self, result: QueryResult, output_path: str):
        """
        Export query results to CSV file.
        
        Args:
            result: QueryResult to export
            output_path: Output file path
        """
        if not result.records:
            print("⚠️  No records to export")
            return
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=result.records[0].keys())
            writer.writeheader()
            writer.writerows(result.records)
        
        print(f"✅ Exported {result.count} records to {output_path}")
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """
        Get summary statistics for all audit trail data.
        
        Returns:
            Dictionary with statistics
        """
        stats = {}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # All validations stats
        cursor.execute("SELECT COUNT(*) FROM all_validations")
        stats["total_validations"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT validation_result, COUNT(*) FROM all_validations GROUP BY validation_result")
        stats["validations_by_result"] = dict(cursor.fetchall())
        
        cursor.execute("SELECT validation_type, COUNT(*) FROM all_validations GROUP BY validation_type")
        stats["validations_by_type"] = dict(cursor.fetchall())
        
        # Evidence validations stats
        cursor.execute("SELECT COUNT(*) FROM evidence_validations")
        stats["total_evidence_validations"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT checksum_valid, COUNT(*) FROM evidence_validations GROUP BY checksum_valid")
        stats["evidence_by_checksum"] = {
            "valid": 0,
            "invalid": 0
        }
        for valid, count in cursor.fetchall():
            stats["evidence_by_checksum"]["valid" if valid else "invalid"] = count
        
        # Report validations stats
        cursor.execute("SELECT COUNT(*) FROM report_validations")
        stats["total_report_validations"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(evidence_coverage) FROM report_validations")
        avg_coverage = cursor.fetchone()[0]
        stats["average_evidence_coverage"] = round(avg_coverage * 100, 2) if avg_coverage else 0
        
        cursor.execute("SELECT validation_status, COUNT(*) FROM report_validations GROUP BY validation_status")
        stats["reports_by_status"] = dict(cursor.fetchall())
        
        conn.close()
        
        return stats


def main():
    """CLI interface for audit trail query tool."""
    import argparse
    
    parser = argparse.ArgumentParser(description="GL Audit Trail Query Tool")
    parser.add_argument("--db", help="Path to audit trail database")
    parser.add_argument("--query", choices=["all", "evidence", "report", "proof-chain"],
                       default="all", help="Query type")
    parser.add_argument("--operation-id", help="Filter by operation ID")
    parser.add_argument("--result", help="Filter by validation result")
    parser.add_argument("--limit", type=int, help="Limit results")
    parser.add_argument("--export-json", help="Export results to JSON file")
    parser.add_argument("--export-csv", help="Export results to CSV file")
    parser.add_argument("--stats", action="store_true", help="Show summary statistics")
    
    args = parser.parse_args()
    
    try:
        query = AuditTrailQuery(db_path=args.db)
        
        if args.stats:
            stats = query.get_summary_statistics()
            print("\n📊 Audit Trail Summary Statistics")
            print("=" * 50)
            print(json.dumps(stats, indent=2))
        else:
            if args.query == "all":
                result = query.query_all_validations(
                    operation_id=args.operation_id,
                    validation_result=args.result,
                    limit=args.limit
                )
            elif args.query == "evidence":
                result = query.query_evidence_validations(
                    operation_id=args.operation_id,
                    validation_result=args.result,
                    limit=args.limit
                )
            elif args.query == "report":
                result = query.query_report_validations(
                    report_id=args.operation_id,
                    validation_status=args.result,
                    limit=args.limit
                )
            elif args.query == "proof-chain":
                result = query.query_proof_chain_validations(
                    chain_id=args.operation_id,
                    limit=args.limit
                )
            
            print(f"\n📋 Query Results")
            print("=" * 50)
            print(f"Count: {result.count}")
            print(f"Query Time: {result.query_time}")
            print(f"Filters: {json.dumps(result.filters_applied, indent=2)}")
            print(f"\nRecords:")
            print(json.dumps(result.records[:10], indent=2))
            
            if result.count > 10:
                print(f"\n... and {result.count - 10} more records")
            
            if args.export_json:
                query.export_to_json(result, args.export_json)
            
            if args.export_csv:
                query.export_to_csv(result, args.export_csv)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())