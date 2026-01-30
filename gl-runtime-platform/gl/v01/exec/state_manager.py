# GL Runtime V1 - State Manager
# @GL-governed
# @GL-layer: V01-execution
# @GL-semantic: state-management-core

"""
GL Runtime V1: 狀態管理器
核心功能: 任務狀態追蹤、狀態持久化、狀態查詢
"""

from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import threading


class StateType(Enum):
    TASK = "task"
    SYSTEM = "system"
    USER = "user"
    SESSION = "session"


@dataclass
class StateEntry:
    key: str
    value: Any
    state_type: StateType
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


class StateManager:
    """GL V1 狀態管理器 - 記憶體內部儲存"""
    
    def __init__(self):
        self._states: Dict[str, StateEntry] = {}
        self._history: Dict[str, List[StateEntry]] = {}
        self._lock = threading.RLock()
    
    def set(
        self,
        key: str,
        value: Any,
        state_type: StateType = StateType.TASK,
        metadata: Optional[Dict[str, Any]] = None
    ) -> StateEntry:
        """設置狀態"""
        with self._lock:
            existing = self._states.get(key)
            
            if existing:
                # 保存歷史
                if key not in self._history:
                    self._history[key] = []
                self._history[key].append(existing)
                
                # 更新版本
                version = existing.version + 1
            else:
                version = 1
            
            entry = StateEntry(
                key=key,
                value=value,
                state_type=state_type,
                version=version,
                metadata=metadata or {}
            )
            
            self._states[key] = entry
            return entry
    
    def get(self, key: str) -> Optional[Any]:
        """獲取狀態值"""
        with self._lock:
            entry = self._states.get(key)
            return entry.value if entry else None
    
    def get_entry(self, key: str) -> Optional[StateEntry]:
        """獲取完整狀態條目"""
        with self._lock:
            return self._states.get(key)
    
    def delete(self, key: str) -> bool:
        """刪除狀態"""
        with self._lock:
            if key in self._states:
                del self._states[key]
                if key in self._history:
                    del self._history[key]
                return True
            return False
    
    def exists(self, key: str) -> bool:
        """檢查狀態是否存在"""
        with self._lock:
            return key in self._states
    
    def list_keys(self, state_type: Optional[StateType] = None) -> List[str]:
        """列出所有鍵"""
        with self._lock:
            if state_type:
                return [k for k, v in self._states.items() if v.state_type == state_type]
            return list(self._states.keys())
    
    def get_history(self, key: str) -> List[StateEntry]:
        """獲取狀態歷史"""
        with self._lock:
            return self._history.get(key, []).copy()
    
    def cleanup(self) -> None:
        """零殘留清理"""
        with self._lock:
            self._states.clear()
            self._history.clear()
    
    def export_snapshot(self) -> Dict[str, Any]:
        """導出狀態快照"""
        with self._lock:
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "states": {
                    k: {
                        "value": v.value,
                        "type": v.state_type.value,
                        "version": v.version
                    }
                    for k, v in self._states.items()
                }
            }


# 全局狀態管理器
_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager


def cleanup_state_manager() -> None:
    global _state_manager
    if _state_manager:
        _state_manager.cleanup()
        _state_manager = None
