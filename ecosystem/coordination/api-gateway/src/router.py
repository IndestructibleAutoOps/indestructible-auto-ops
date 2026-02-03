#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL API Gateway Router
=====================
路由器 - 請求路由和轉發

GL Governance Layer: GL10-29 (Operational Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import logging


class RouteMatchType(Enum):
    """路由匹配類型"""
    EXACT = "exact"
    PREFIX = "prefix"
    REGEX = "regex"


@dataclass
class Route:
    """路由定義"""
    path: str
    platform: str
    service: str
    methods: List[str]
    timeout: int = 30
    authentication: str = "optional"  # required, optional, none
    match_type: RouteMatchType = RouteMatchType.PREFIX
    pattern: Optional[re.Pattern] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """初始化後處理"""
        if self.metadata is None:
            self.metadata = {}
        
        # 編譯正則表達式
        if self.match_type == RouteMatchType.REGEX:
            self.pattern = re.compile(self.path)
        elif self.match_type == RouteMatchType.PREFIX:
            # 將通配符路徑轉換為正則表達式
            path_pattern = self.path.replace('*', '.*')
            self.pattern = re.compile(f"^{path_pattern}")


class Router:
    """API 網關路由器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化路由器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 路由表
        self.routes: List[Route] = []
        
        # 從配置加載路由
        self._load_routes_from_config()
        
        self.logger.info(f"Router initialized with {len(self.routes)} routes")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('Router')
        level = self.config.get('logging', {}).get('level', 'INFO')
        logger.setLevel(getattr(logging, level))
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _load_routes_from_config(self):
        """從配置加載路由"""
        routes_config = self.config.get('routes', [])
        
        for route_data in routes_config:
            try:
                route = Route(
                    path=route_data['path'],
                    platform=route_data['platform'],
                    service=route_data['service'],
                    methods=route_data.get('methods', ['GET']),
                    timeout=route_data.get('timeout', 30),
                    authentication=route_data.get('authentication', 'optional'),
                    match_type=RouteMatchType.PREFIX
                )
                self.add_route(route)
            except Exception as e:
                self.logger.error(f"Failed to load route {route_data.get('path')}: {e}")
    
    def add_route(self, route: Route) -> bool:
        """
        添加路由
        
        Args:
            route: 路由對象
            
        Returns:
            成功返回True
        """
        try:
            # 檢查是否已存在
            for existing_route in self.routes:
                if existing_route.path == route.path:
                    self.logger.warning(f"Route {route.path} already exists, replacing")
                    self.routes.remove(existing_route)
                    break
            
            self.routes.append(route)
            self.logger.info(f"Route added: {route.path} -> {route.platform}/{route.service}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add route: {e}")
            return False
    
    def remove_route(self, path: str) -> bool:
        """
        移除路由
        
        Args:
            path: 路由路徑
            
        Returns:
            成功返回True
        """
        for route in self.routes:
            if route.path == path:
                self.routes.remove(route)
                self.logger.info(f"Route removed: {path}")
                return True
        
        self.logger.warning(f"Route not found: {path}")
        return False
    
    def match_route(self, path: str, method: str = 'GET') -> Optional[Route]:
        """
        匹配路由
        
        Args:
            path: 請求路徑
            method: HTTP方法
            
        Returns:
            匹配的路由或None
        """
        # 優先匹配精確路由，然後前綴路由
        exact_matches = []
        prefix_matches = []
        
        for route in self.routes:
            # 檢查方法
            if method not in route.methods:
                continue
            
            # 匹配路徑
            if route.match_type == RouteMatchType.EXACT:
                if route.path == path:
                    exact_matches.append(route)
            elif route.match_type == RouteMatchType.PREFIX:
                if route.pattern and route.pattern.match(path):
                    prefix_matches.append(route)
            elif route.match_type == RouteMatchType.REGEX:
                if route.pattern and route.pattern.match(path):
                    prefix_matches.append(route)
        
        # 優先返回精確匹配
        if exact_matches:
            return exact_matches[0]
        
        # 返回最長前綴匹配
        if prefix_matches:
            # 按路徑長度排序，返回最長的
            prefix_matches.sort(key=lambda r: len(r.path), reverse=True)
            return prefix_matches[0]
        
        self.logger.debug(f"No route matched for {method} {path}")
        return None
    
    def get_route_info(self, path: str) -> Optional[Dict[str, Any]]:
        """
        獲取路由信息
        
        Args:
            path: 路由路徑
            
        Returns:
            路由信息字典或None
        """
        for route in self.routes:
            if route.path == path:
                return {
                    'path': route.path,
                    'platform': route.platform,
                    'service': route.service,
                    'methods': route.methods,
                    'timeout': route.timeout,
                    'authentication': route.authentication,
                    'match_type': route.match_type.value
                }
        
        return None
    
    def list_routes(self) -> List[Dict[str, Any]]:
        """
        列出所有路由
        
        Returns:
            路由列表
        """
        return [
            {
                'path': route.path,
                'platform': route.platform,
                'service': route.service,
                'methods': route.methods,
                'timeout': route.timeout,
                'authentication': route.authentication
            }
            for route in self.routes
        ]
    
    def rewrite_path(self, original_path: str, route: Route) -> str:
        """
        重寫路徑（移除路由前綴）
        
        Args:
            original_path: 原始路徑
            route: 匹配的路由
            
        Returns:
            重寫後的路徑
        """
        # 移除路由前綴
        route_prefix = route.path.rstrip('/*')
        if original_path.startswith(route_prefix):
            rewritten = original_path[len(route_prefix):]
            if not rewritten.startswith('/'):
                rewritten = '/' + rewritten
            return rewritten
        
        return original_path
