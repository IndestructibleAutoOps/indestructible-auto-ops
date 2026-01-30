"""
GL Runtime V3 - 審計模組
基礎審計追蹤
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class AuditLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class AuditRecord:
    timestamp: datetime
    action: str
    level: AuditLevel
    details: Dict[str, Any]
    actor: str = "system"


class AuditTrail:
    """基礎審計追蹤器"""
    
    def __init__(self):
        self._records: List[AuditRecord] = []
    
    def log(self, action: str, level: AuditLevel, details: Dict[str, Any], actor: str = "system") -> None:
        """記錄審計事件"""
        record = AuditRecord(
            timestamp=datetime.utcnow(),
            action=action,
            level=level,
            details=details,
            actor=actor
        )
        self._records.append(record)
    
    def get_records(self, level: Optional[AuditLevel] = None) -> List[AuditRecord]:
        """獲取審計記錄"""
        if level:
            return [r for r in self._records if r.level == level]
        return self._records.copy()
    
    def clear(self) -> None:
        """清理審計記錄（零殘留）"""
        self._records.clear()
