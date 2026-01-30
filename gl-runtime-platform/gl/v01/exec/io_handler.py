"""
GL Runtime V1 - I/O Handler
任務輸入輸出處理模組
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class IOType(Enum):
    FILE = "file"
    STREAM = "stream"
    MEMORY = "memory"
    NETWORK = "network"


@dataclass
class IOConfig:
    io_type: IOType
    encoding: str = "utf-8"
    buffer_size: int = 8192
    zero_residual: bool = True


class IOHandler:
    """任務 I/O 處理器"""
    
    def __init__(self, config: Optional[IOConfig] = None):
        self.config = config or IOConfig(io_type=IOType.MEMORY)
        self._buffers: Dict[str, Any] = {}
    
    def read(self, source: str) -> Any:
        """讀取輸入數據"""
        if self.config.io_type == IOType.MEMORY:
            return self._buffers.get(source)
        raise NotImplementedError(f"IO type {self.config.io_type} not implemented")
    
    def write(self, target: str, data: Any) -> bool:
        """寫入輸出數據"""
        if self.config.io_type == IOType.MEMORY:
            self._buffers[target] = data
            return True
        raise NotImplementedError(f"IO type {self.config.io_type} not implemented")
    
    def cleanup(self) -> None:
        """零殘留清理"""
        if self.config.zero_residual:
            self._buffers.clear()
