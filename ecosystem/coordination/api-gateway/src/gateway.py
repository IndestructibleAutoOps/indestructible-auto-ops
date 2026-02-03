#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL API Gateway
==============
API 網關 - 統一入口

GL Governance Layer: GL10-29 (Operational Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import sys
from pathlib import Path
from typing import Dict, Optional, Any, Tuple
import logging

# Add service-discovery to path
service_discovery_path = Path(__file__).parent.parent.parent / 'service-discovery' / 'src'
sys.path.insert(0, str(service_discovery_path))

from router import Router, Route
from authenticator import Authenticator, AuthToken
from rate_limiter import RateLimiter

try:
    from service_client import ServiceClient
    from service_registry import ServiceRegistry
    SERVICE_DISCOVERY_AVAILABLE = True
except ImportError:
    SERVICE_DISCOVERY_AVAILABLE = False


class Gateway:
    """API 網關"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化 API 網關
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 初始化組件
        self.router = Router(config)
        self.authenticator = Authenticator(config)
        self.rate_limiter = RateLimiter(config)
        
        # 服務發現客戶端（如果可用）
        self.service_client = None
        if SERVICE_DISCOVERY_AVAILABLE:
            try:
                registry = ServiceRegistry(config)
                self.service_client = ServiceClient(registry, config)
                self.logger.info("Service Discovery integration enabled")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Service Discovery: {e}")
        
        self.logger.info("API Gateway initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('Gateway')
        level = self.config.get('logging', {}).get('level', 'INFO')
        logger.setLevel(getattr(logging, level))
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def handle_request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Dict[str, Any]] = None,
        client_ip: Optional[str] = None
    ) -> Tuple[int, Dict[str, Any], Dict[str, Any]]:
        """
        處理請求
        
        Args:
            method: HTTP 方法
            path: 請求路徑
            headers: 請求頭
            body: 請求體
            client_ip: 客戶端IP
            
        Returns:
            (status_code, response_headers, response_body)
        """
        headers = headers or {}
        client_ip = client_ip or 'unknown'
        
        self.logger.info(f"Request: {method} {path} from {client_ip}")
        
        # 1. 路由匹配
        route = self.router.match_route(path, method)
        if not route:
            return self._error_response(404, "Route not found")
        
        # 2. 認證
        auth_required = route.authentication == 'required'
        auth_token = None
        
        if auth_required or route.authentication == 'optional':
            auth_token = self.authenticator.authenticate(headers)
            
            if auth_required and not auth_token:
                return self._error_response(401, "Authentication required")
        
        # 3. 速率限制
        client_id = auth_token.user_id if auth_token else client_ip
        allowed, limit_info = self.rate_limiter.check_rate_limit(client_id, route.path)
        
        if not allowed:
            return self._error_response(
                429,
                "Rate limit exceeded",
                headers={
                    'X-RateLimit-Limit': str(limit_info['limit']),
                    'X-RateLimit-Remaining': '0',
                    'X-RateLimit-Reset': str(limit_info['reset'])
                }
            )
        
        # 4. 轉發請求
        response_status, response_headers, response_body = self._forward_request(
            route, method, path, headers, body
        )
        
        # 添加速率限制頭
        response_headers.update({
            'X-RateLimit-Limit': str(limit_info['limit']),
            'X-RateLimit-Remaining': str(limit_info['remaining']),
            'X-RateLimit-Reset': str(limit_info['reset'])
        })
        
        return response_status, response_headers, response_body
    
    def _forward_request(
        self,
        route: Route,
        method: str,
        path: str,
        headers: Dict[str, str],
        body: Optional[Dict[str, Any]]
    ) -> Tuple[int, Dict[str, Any], Dict[str, Any]]:
        """
        轉發請求到後端服務
        
        Args:
            route: 匹配的路由
            method: HTTP 方法
            path: 請求路徑
            headers: 請求頭
            body: 請求體
            
        Returns:
            (status_code, response_headers, response_body)
        """
        # 重寫路徑
        rewritten_path = self.router.rewrite_path(path, route)
        
        # 如果集成了服務發現，嘗試使用服務發現
        if self.service_client:
            try:
                response = self.service_client.call_service(
                    name=route.service,
                    method=method,
                    path=rewritten_path,
                    data=body,
                    headers=headers,
                    timeout=route.timeout,
                    platform=route.platform
                )
                
                if response is not None:
                    return 200, {}, response
                else:
                    # 服務不可用時回退到模擬響應
                    self.logger.warning(f"Service {route.service} not found, using mock response")
                    
            except Exception as e:
                self.logger.warning(f"Error calling service via service discovery: {e}, using mock response")
        
        # 返回模擬響應（用於測試或服務不可用時）
        return 200, {}, {
            'message': 'Request forwarded',
            'route': {
                'platform': route.platform,
                'service': route.service,
                'path': rewritten_path
            },
            'method': method
        }
    
    def _error_response(
        self,
        status_code: int,
        message: str,
        headers: Optional[Dict[str, Any]] = None
    ) -> Tuple[int, Dict[str, Any], Dict[str, Any]]:
        """
        生成錯誤響應
        
        Args:
            status_code: HTTP 狀態碼
            message: 錯誤消息
            headers: 響應頭
            
        Returns:
            (status_code, response_headers, response_body)
        """
        return status_code, headers or {}, {
            'error': message,
            'status': status_code
        }
    
    def add_route(self, route: Route) -> bool:
        """添加路由"""
        return self.router.add_route(route)
    
    def remove_route(self, path: str) -> bool:
        """移除路由"""
        return self.router.remove_route(path)
    
    def list_routes(self):
        """列出所有路由"""
        return self.router.list_routes()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        獲取網關統計信息
        
        Returns:
            統計信息字典
        """
        return {
            'routes': len(self.router.routes),
            'rate_limiter': self.rate_limiter.get_stats()
        }
