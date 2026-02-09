#!/usr/bin/env python3
"""
可審計日誌系統 - 支援 OpenTelemetry 與 JSONL 輸出
Enterprise Audit Logger with OpenTelemetry Integration
"""

import json
import uuid
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field
from pathlib import Path
import logging

# OpenTelemetry imports (optional - will work without it)
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    trace = None

# Structured logging
try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False


@dataclass
class AuditRecord:
    """審計記錄資料類別"""
    actor: str
    action: str
    resource: str
    result: str  # "success", "fail", "warning"
    hash: str
    version: str
    requestId: str
    correlationId: str
    ip: str
    userAgent: str
    timestamp: str
    spanId: Optional[str] = None
    traceId: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    severity: str = "INFO"
    
    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        data = asdict(self)
        # 移除 None 值
        return {k: v for k, v in data.items() if v is not None}
    
    def to_json(self) -> str:
        """轉換為 JSON 字串"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def to_jsonl(self) -> str:
        """轉換為 JSONL 格式 (單行)"""
        return self.to_json() + "\n"
    
    def validate(self) -> bool:
        """驗證記錄完整性"""
        required_fields = ['actor', 'action', 'resource', 'result', 'hash', 
                          'version', 'requestId', 'correlationId', 'timestamp']
        for field in required_fields:
            if not getattr(self, field, None):
                return False
        
        # 驗證時間戳格式
        try:
            datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return False
        
        # 驗證結果值
        if self.result not in ['success', 'fail', 'warning']:
            return False
        
        return True


class AuditLogger:
    """可審計日誌記錄器 - Enterprise Grade"""
    
    def __init__(
        self,
        service_name: str,
        version: str,
        log_file: str = "audit.log",
        enable_otel: bool = False,
        enable_structlog: bool = False
    ):
        self.service_name = service_name
        self.version = version
        self.log_file = Path(log_file)
        self.enable_otel = enable_otel and OTEL_AVAILABLE
        self.enable_structlog = enable_structlog and STRUCTLOG_AVAILABLE
        
        # 確保日誌目錄存在
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化 OpenTelemetry
        self.tracer = None
        if self.enable_otel and trace:
            trace.set_tracer_provider(TracerProvider())
            self.tracer = trace.get_tracer(__name__)
        
        # 初始化 Structlog
        if self.enable_structlog and STRUCTLOG_AVAILABLE:
            structlog.configure(
                processors=[
                    structlog.stdlib.filter_by_level,
                    structlog.stdlib.add_logger_name,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.PositionalArgumentsFormatter(),
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.StackInfoRenderer(),
                    structlog.processors.format_exc_info,
                    structlog.processors.UnicodeDecoder(),
                    structlog.processors.JSONRenderer()
                ],
                context_class=dict,
                logger_factory=structlog.stdlib.LoggerFactory(),
                wrapper_class=structlog.stdlib.BoundLogger,
                cache_logger_on_first_use=True,
            )
            self.logger = structlog.get_logger()
        else:
            self.logger = logging.getLogger(self.service_name)
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
        
        # 統計信息
        self.stats = {
            "total_records": 0,
            "success_records": 0,
            "fail_records": 0,
            "warning_records": 0
        }
    
    def generate_ids(self) -> Dict[str, str]:
        """生成追蹤 ID"""
        return {
            "requestId": str(uuid.uuid4()),
            "correlationId": str(uuid.uuid4()),
            "spanId": str(uuid.uuid4())[:16],
            "traceId": str(uuid.uuid4())
        }
    
    def calculate_hash(self, data: Dict[str, Any]) -> str:
        """計算資料雜湊值"""
        # 移除 hash 欄位以避免遞歸
        data_copy = {k: v for k, v in data.items() if k != 'hash'}
        json_str = json.dumps(data_copy, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(json_str.encode('utf-8')).hexdigest()
    
    def log(
        self,
        actor: str,
        action: str,
        resource: str,
        result: str = "success",
        ip: str = "127.0.0.1",
        user_agent: str = "EnterpriseGovernanceModule/2.0",
        metadata: Optional[Dict[str, Any]] = None,
        severity: str = "INFO"
    ) -> AuditRecord:
        """記錄審計事件"""
        
        # 生成追蹤 ID
        ids = self.generate_ids()
        
        # 建立記錄
        record = AuditRecord(
            actor=actor,
            action=action,
            resource=resource,
            result=result,
            hash="",  # 稍後計算
            version=self.version,
            requestId=ids["requestId"],
            correlationId=ids["correlationId"],
            ip=ip,
            userAgent=user_agent,
            timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            spanId=ids["spanId"],
            traceId=ids["traceId"],
            metadata=metadata,
            severity=severity
        )
        
        # 驗證記錄
        if not record.validate():
            raise ValueError(f"Invalid audit record: {record}")
        
        # 計算雜湊
        record.hash = self.calculate_hash(record.to_dict())
        
        # 輸出到 JSONL
        self._write_to_file(record)
        
        # 輸出到控制台 (OpenTelemetry 格式)
        self._log_to_console(record)
        
        # 更新統計
        self._update_stats(record)
        
        # 輸出到 Structlog (如果啟用)
        if self.enable_structlog:
            self.logger.info(
                "audit_event",
                actor=actor,
                action=action,
                resource=resource,
                result=result,
                requestId=record.requestId
            )
        
        return record
    
    def _write_to_file(self, record: AuditRecord):
        """寫入日誌文件"""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(record.to_jsonl())
    
    def _log_to_console(self, record: AuditRecord):
        """輸出到控制台"""
        log_data = {
            "timestamp": record.timestamp,
            "severity": record.severity,
            "name": f"{self.service_name}.audit",
            "body": f"Actor {record.actor} performed {record.action} on {record.resource} with result {record.result}",
            "attributes": record.to_dict(),
            "traceId": record.traceId,
            "spanId": record.spanId
        }
        print(json.dumps(log_data, ensure_ascii=False))
    
    def _update_stats(self, record: AuditRecord):
        """更新統計信息"""
        self.stats["total_records"] += 1
        if record.result == "success":
            self.stats["success_records"] += 1
        elif record.result == "fail":
            self.stats["fail_records"] += 1
        elif record.result == "warning":
            self.stats["warning_records"] += 1
    
    def query_logs(
        self,
        actor: Optional[str] = None,
        action: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 100
    ) -> List[AuditRecord]:
        """查詢審計日誌"""
        records = []
        
        if not self.log_file.exists():
            return records
        
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    record = AuditRecord(**data)
                    
                    # 過濾條件
                    if actor and record.actor != actor:
                        continue
                    if action and record.action != action:
                        continue
                    if start_time and record.timestamp < start_time:
                        continue
                    if end_time and record.timestamp > end_time:
                        continue
                    
                    records.append(record)
                    
                    if len(records) >= limit:
                        break
                        
                except (json.JSONDecodeError, TypeError) as e:
                    continue
        
        return records
    
    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        return {
            **self.stats,
            "service_name": self.service_name,
            "version": self.version,
            "otel_enabled": self.enable_otel,
            "structlog_enabled": self.enable_structlog
        }
    
    def replay_logs(self, start_time: Optional[str] = None, end_time: Optional[str] = None) -> List[AuditRecord]:
        """重播日誌 - 用於調試和驗證"""
        return self.query_logs(start_time=start_time, end_time=end_time, limit=10000)


# 單例實例
_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    """獲取單例審計日誌記錄器"""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger(
            service_name="engineering-governance-module",
            version="2.0.0",
            log_file="audit.log"
        )
    return _audit_logger


def log_audit(
    actor: str,
    action: str,
    resource: str,
    result: str = "success",
    **kwargs
) -> AuditRecord:
    """便捷函數：記錄審計事件"""
    logger = get_audit_logger()
    return logger.log(
        actor=actor,
        action=action,
        resource=resource,
        result=result,
        **kwargs
    )


if __name__ == "__main__":
    # 測試範例
    print("=== Enterprise Audit Logger Test ===\n")
    
    # 創建審計記錄器
    logger = AuditLogger(
        service_name="engineering-governance-module",
        version="2.0.0",
        log_file="test_audit.log"
    )
    
    # 記錄測試事件
    print("1. Recording system initialization...")
    record1 = logger.log(
        actor="system:initializer",
        action="initialize:system",
        resource="system://governance-engine",
        result="success",
        metadata={"startup_time_ms": 1250}
    )
    print(f"   ✓ Record ID: {record1.requestId}")
    
    # 記錄錯誤事件
    print("\n2. Recording validation error...")
    record2 = logger.log(
        actor="user:admin@example.com",
        action="validate:config",
        resource="config://security/policy",
        result="fail",
        severity="ERROR",
        metadata={"error_code": "POLICY_INVALID"}
    )
    print(f"   ✓ Record ID: {record2.requestId}")
    
    # 查詢日誌
    print("\n3. Querying audit logs...")
    records = logger.query_logs(limit=10)
    print(f"   ✓ Found {len(records)} records")
    
    # 獲取統計
    print("\n4. Statistics:")
    stats = logger.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # 重播日誌
    print("\n5. Replaying logs...")
    replayed = logger.replay_logs()
    print(f"   ✓ Replayed {len(replayed)} records")
    
    print("\n=== Test Complete ===")
    print(f"Logs saved to: {logger.log_file}")