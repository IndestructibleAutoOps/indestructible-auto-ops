#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Filesystem Connector
=======================
文件系統連接器 - 本地/網絡文件系統

GL Governance Layer: GL10-29 (Operational Layer)
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

from .base_connector import BaseConnector


class FilesystemConnector(BaseConnector):
    """文件系統連接器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化文件系統連接器
        
        Args:
            config: 配置字典
        """
        super().__init__(config)
        
        self.base_path = Path(
            self.config.get('connectors', {})
            .get('onpremise', {})
            .get('services', {})
            .get('filesystem', {})
            .get('base_path', '/tmp/data-sync')
        )
        
        self.connected = False
    
    def connect(self) -> bool:
        """連接到文件系統"""
        try:
            # 創建基礎目錄
            self.base_path.mkdir(parents=True, exist_ok=True)
            self.connected = True
            self.logger.info(f"Connected to filesystem: {self.base_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to filesystem: {e}")
            return False
    
    def disconnect(self) -> bool:
        """斷開連接"""
        self.connected = False
        self.logger.info("Disconnected from filesystem")
        return True
    
    def read(self, path: str) -> Optional[Any]:
        """
        讀取數據
        
        Args:
            path: 數據路徑
            
        Returns:
            數據或None
        """
        if not self.connected:
            self.logger.error("Not connected")
            return None
        
        try:
            file_path = self.base_path / path
            if not file_path.exists():
                self.logger.warning(f"File not found: {file_path}")
                return None
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            self.logger.debug(f"Data read from {path}")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to read {path}: {e}")
            return None
    
    def write(self, path: str, data: Any) -> bool:
        """
        寫入數據
        
        Args:
            path: 數據路徑
            data: 數據
            
        Returns:
            成功返回True
        """
        if not self.connected:
            self.logger.error("Not connected")
            return False
        
        try:
            file_path = self.base_path / path
            
            # 創建父目錄
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 寫入數據
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.logger.debug(f"Data written to {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to write {path}: {e}")
            return False
    
    def list(self, path: str = "") -> List[str]:
        """
        列出數據項
        
        Args:
            path: 路徑
            
        Returns:
            數據項列表
        """
        if not self.connected:
            self.logger.error("Not connected")
            return []
        
        try:
            dir_path = self.base_path / path if path else self.base_path
            
            if not dir_path.exists():
                return []
            
            return [
                str(item.relative_to(self.base_path))
                for item in dir_path.rglob('*.json')
            ]
            
        except Exception as e:
            self.logger.error(f"Failed to list {path}: {e}")
            return []
    
    def delete(self, path: str) -> bool:
        """
        刪除數據
        
        Args:
            path: 數據路徑
            
        Returns:
            成功返回True
        """
        if not self.connected:
            self.logger.error("Not connected")
            return False
        
        try:
            file_path = self.base_path / path
            
            if file_path.exists():
                file_path.unlink()
                self.logger.debug(f"Data deleted: {path}")
                return True
            else:
                self.logger.warning(f"File not found: {path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to delete {path}: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        try:
            items = self.list()
            total_size = sum(
                (self.base_path / item).stat().st_size
                for item in items
                if (self.base_path / item).exists()
            )
            
            return {
                'connector_type': 'FilesystemConnector',
                'connected': self.connected,
                'base_path': str(self.base_path),
                'total_items': len(items),
                'total_size_bytes': total_size
            }
        except Exception as e:
            return {
                'connector_type': 'FilesystemConnector',
                'connected': self.connected,
                'error': str(e)
            }
