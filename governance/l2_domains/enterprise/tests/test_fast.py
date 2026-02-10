#!/usr/bin/env python3
"""
Fast Test Suite - Quick validation (<30 seconds)
Run with: python -m pytest tests/test_fast.py -v
"""

import pytest
import json
from pathlib import Path
from datetime import datetime

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audit.logger import AuditLogger, AuditRecord


class TestAuditLogger:
    """測試審計日誌記錄器"""
    
    @pytest.fixture
    def logger(self):
        """創建測試用的日誌記錄器"""
        log_file = "test_audit.log"
        logger = AuditLogger(
            service_name="test-service",
            version="1.0.0",
            log_file=log_file
        )
        yield logger
        # 清理
        if Path(log_file).exists():
            Path(log_file).unlink()
    
    def test_audit_record_validation(self, logger):
        """測試審計記錄驗證"""
        record = logger.log(
            actor="test-user",
            action="test:action",
            resource="test://resource",
            result="success"
        )
        assert record.validate() is True
        assert record.result == "success"
        assert record.actor == "test-user"
    
    def test_audit_record_failure(self, logger):
        """測試失敗記錄"""
        record = logger.log(
            actor="test-user",
            action="test:fail",
            resource="test://resource",
            result="fail"
        )
        assert record.result == "fail"
    
    def test_audit_record_warning(self, logger):
        """測試警告記錄"""
        record = logger.log(
            actor="test-user",
            action="test:warning",
            resource="test://resource",
            result="warning"
        )
        assert record.result == "warning"
    
    def test_audit_ids_generation(self, logger):
        """測試 ID 生成"""
        record = logger.log(
            actor="test-user",
            action="test:ids",
            resource="test://resource"
        )
        assert len(record.requestId) == 36  # UUID length
        assert len(record.correlationId) == 36
        assert len(record.spanId) == 16
        assert len(record.traceId) == 36
    
    def test_audit_hash_calculation(self, logger):
        """測試雜湊計算"""
        record1 = logger.log(
            actor="test-user",
            action="test:hash1",
            resource="test://resource1"
        )
        record2 = logger.log(
            actor="test-user",
            action="test:hash1",
            resource="test://resource1"
        )
        # 相同輸入應該產生相同雜湊
        assert record1.hash == record2.hash
    
    def test_audit_timestamp_format(self, logger):
        """測試時間戳格式"""
        record = logger.log(
            actor="test-user",
            action="test:timestamp",
            resource="test://resource"
        )
        # 驗證 RFC3339 格式
        assert "T" in record.timestamp
        assert record.timestamp.endswith("Z")
        datetime.fromisoformat(record.timestamp.replace("Z", "+00:00"))
    
    def test_audit_stats(self, logger):
        """測試統計功能"""
        logger.log(actor="user1", action="action1", resource="res1", result="success")
        logger.log(actor="user2", action="action2", resource="res2", result="fail")
        logger.log(actor="user3", action="action3", resource="res3", result="warning")
        
        stats = logger.get_stats()
        assert stats["total_records"] == 3
        assert stats["success_records"] == 1
        assert stats["fail_records"] == 1
        assert stats["warning_records"] == 1
    
    def test_audit_query(self, logger):
        """測試查詢功能"""
        logger.log(actor="user1", action="action1", resource="res1")
        logger.log(actor="user2", action="action2", resource="res2")
        logger.log(actor="user1", action="action3", resource="res3")
        
        # 查詢特定 actor
        records = logger.query_logs(actor="user1")
        assert len(records) == 2
        assert all(r.actor == "user1" for r in records)
        
        # 查詢特定 action
        records = logger.query_logs(action="action2")
        assert len(records) == 1
        assert records[0].action == "action2"
    
    def test_audit_jsonl_format(self, logger):
        """測試 JSONL 格式"""
        record = logger.log(
            actor="test-user",
            action="test:jsonl",
            resource="test://resource"
        )
        
        jsonl = record.to_jsonl()
        assert "\n" in jsonl
        
        data = json.loads(jsonl.strip())
        assert data["actor"] == "test-user"
        assert data["action"] == "test:jsonl"
    
    def test_audit_metadata(self, logger):
        """測試 metadata 功能"""
        metadata = {"key1": "value1", "key2": 123}
        record = logger.log(
            actor="test-user",
            action="test:metadata",
            resource="test://resource",
            metadata=metadata
        )
        
        assert record.metadata == metadata
        data = record.to_dict()
        assert "metadata" in data
        assert data["metadata"] == metadata


class TestAuditRecordValidation:
    """測試審計記錄驗證邏輯"""
    
    def test_valid_record(self):
        """測試有效記錄"""
        record = AuditRecord(
            actor="user@example.com",
            action="create:resource",
            resource="resource://test/id",
            result="success",
            hash="abc123",
            version="1.0.0",
            requestId="550e8400-e29b-41d4-a716-446655440000",
            correlationId="550e8400-e29b-41d4-a716-446655440001",
            ip="192.168.1.1",
            userAgent="TestAgent/1.0",
            timestamp="2024-01-01T00:00:00Z"
        )
        assert record.validate() is True
    
    def test_invalid_result(self):
        """測試無效的結果值"""
        record = AuditRecord(
            actor="user@example.com",
            action="create:resource",
            resource="resource://test/id",
            result="invalid",  # 無效值
            hash="abc123",
            version="1.0.0",
            requestId="550e8400-e29b-41d4-a716-446655440000",
            correlationId="550e8400-e29b-41d4-a716-446655440001",
            ip="192.168.1.1",
            userAgent="TestAgent/1.0",
            timestamp="2024-01-01T00:00:00Z"
        )
        assert record.validate() is False
    
    def test_missing_required_field(self):
        """測試缺少必填欄位"""
        record = AuditRecord(
            actor="",  # 空值
            action="create:resource",
            resource="resource://test/id",
            result="success",
            hash="abc123",
            version="1.0.0",
            requestId="550e8400-e29b-41d4-a716-446655440000",
            correlationId="550e8400-e29b-41d4-a716-446655440001",
            ip="192.168.1.1",
            userAgent="TestAgent/1.0",
            timestamp="2024-01-01T00:00:00Z"
        )
        assert record.validate() is False
    
    def test_invalid_timestamp(self):
        """測試無效的時間戳"""
        record = AuditRecord(
            actor="user@example.com",
            action="create:resource",
            resource="resource://test/id",
            result="success",
            hash="abc123",
            version="1.0.0",
            requestId="550e8400-e29b-41d4-a716-446655440000",
            correlationId="550e8400-e29b-41d4-a716-446655440001",
            ip="192.168.1.1",
            userAgent="TestAgent/1.0",
            timestamp="invalid-timestamp"  # 無效格式
        )
        assert record.validate() is False


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])