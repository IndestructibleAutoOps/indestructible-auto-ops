#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Base Connector
=================
數據連接器基類

GL Governance Layer: GL10-29 (Operational Layer)
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import logging


class BaseConnector(ABC):
    """數據連接器基類"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化連接器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    @abstractmethod
    def connect(self) -> bool:
        """
        連接到數據源
        
        Returns:
            成功返回True
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """
        斷開連接
        
        Returns:
            成功返回True
        """
        pass
    
    @abstractmethod
    def read(self, path: str) -> Optional[Any]:
        """
        讀取數據
        
        Args:
            path: 數據路徑
            
        Returns:
            數據或None
        """
        pass
    
    @abstractmethod
    def write(self, path: str, data: Any) -> bool:
        """
        寫入數據
        
        Args:
            path: 數據路徑
            data: 數據
            
        Returns:
            成功返回True
        """
        pass
    
    @abstractmethod
    def list(self, path: str = "") -> List[str]:
        """
        列出數據項
        
        Args:
            path: 路徑
            
        Returns:
            數據項列表
        """
        pass
    
    @abstractmethod
    def delete(self, path: str) -> bool:
        """
        刪除數據
        
        Args:
            path: 數據路徑
            
        Returns:
            成功返回True
        """
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """
        獲取統計信息
        
        Returns:
            統計信息字典
        """
        return {
            'connector_type': self.__class__.__name__,
            'connected': False
        }
