#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Service Agent
================
服務代理 - 運行在每個平台上，負責服務註冊和健康檢查

GL Governance Layer: GL10-29 (Operational Layer)
"""

import uuid
import threading
import time
from typing import Optional, Dict, Any, Callable
from datetime import datetime
import logging

from service_registry import (
    ServiceRegistry,
    ServiceInstance,
    ServiceMetadata,
    HealthCheck,
    ServiceStatus,
    HealthStatus
)


class ServiceAgent:
    """服務代理 - 在每個平台上運行"""
    
    def __init__(
        self,
        registry: ServiceRegistry,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化服務代理
        
        Args:
            registry: 服務註冊中心
            config: 配置字典
        """
        self.registry = registry
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 註冊的服務: {service_id: ServiceInstance}
        self._registered_services: Dict[str, ServiceInstance] = {}
        
        # 健康檢查線程
        self._health_check_thread: Optional[threading.Thread] = None
        self._health_check_running = False
        
        # 心跳線程
        self._heartbeat_thread: Optional[threading.Thread] = None
        self._heartbeat_running = False
        
        self.logger.info("Service Agent initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('ServiceAgent')
        level = self.config.get('monitoring', {}).get('logging', {}).get('level', 'INFO')
        logger.setLevel(getattr(logging, level))
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def register_service(
        self,
        name: str,
        platform: str,
        endpoint: str,
        service_type: Optional[str] = None,
        version: Optional[str] = "1.0.0",
        tags: Optional[list] = None,
        capabilities: Optional[list] = None,
        health_check: Optional[HealthCheck] = None,
        auto_health_check: bool = True,
        custom_metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        註冊服務
        
        Args:
            name: 服務名稱
            platform: 平台名稱
            endpoint: 服務端點
            service_type: 服務類型
            version: 服務版本
            tags: 標籤列表
            capabilities: 能力列表
            health_check: 健康檢查配置
            auto_health_check: 是否自動健康檢查
            custom_metadata: 自定義元數據
            
        Returns:
            服務ID或None（如果註冊失敗）
        """
        try:
            # 生成服務ID
            service_id = f"{platform}-{name}-{uuid.uuid4().hex[:8]}"
            
            # 創建服務元數據
            metadata = ServiceMetadata(
                name=name,
                platform=platform,
                endpoint=endpoint,
                type=service_type,
                version=version,
                tags=tags or [],
                capabilities=capabilities or [],
                custom_metadata=custom_metadata or {}
            )
            
            # 創建服務實例
            instance = ServiceInstance(
                id=service_id,
                metadata=metadata,
                health_check=health_check,
                status=ServiceStatus.ACTIVE,
                health_status=HealthStatus.UNKNOWN
            )
            
            # 註冊到註冊中心
            if self.registry.register_service(instance):
                self._registered_services[service_id] = instance
                
                # 啟動健康檢查（如果配置）
                if auto_health_check and not self._health_check_running:
                    self.start_health_checks()
                
                # 啟動心跳（如果尚未啟動）
                if not self._heartbeat_running:
                    self.start_heartbeat()
                
                self.logger.info(f"Service registered successfully: {service_id}")
                return service_id
            else:
                self.logger.error(f"Failed to register service: {name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error registering service {name}: {e}")
            return None
    
    def deregister_service(self, service_id: str) -> bool:
        """
        註銷服務
        
        Args:
            service_id: 服務ID
            
        Returns:
            成功返回True
        """
        try:
            if service_id in self._registered_services:
                del self._registered_services[service_id]
            
            if self.registry.deregister_service(service_id):
                self.logger.info(f"Service deregistered: {service_id}")
                return True
            else:
                self.logger.warning(f"Service not found in registry: {service_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error deregistering service {service_id}: {e}")
            return False
    
    def start_health_checks(self):
        """啟動健康檢查"""
        if self._health_check_running:
            self.logger.warning("Health checks already running")
            return
        
        self._health_check_running = True
        self._health_check_thread = threading.Thread(
            target=self._health_check_loop,
            daemon=True
        )
        self._health_check_thread.start()
        self.logger.info("Health check thread started")
    
    def stop_health_checks(self):
        """停止健康檢查"""
        if not self._health_check_running:
            return
        
        self._health_check_running = False
        if self._health_check_thread:
            self._health_check_thread.join(timeout=5)
        self.logger.info("Health check thread stopped")
    
    def start_heartbeat(self):
        """啟動心跳"""
        if self._heartbeat_running:
            self.logger.warning("Heartbeat already running")
            return
        
        self._heartbeat_running = True
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            daemon=True
        )
        self._heartbeat_thread.start()
        self.logger.info("Heartbeat thread started")
    
    def stop_heartbeat(self):
        """停止心跳"""
        if not self._heartbeat_running:
            return
        
        self._heartbeat_running = False
        if self._heartbeat_thread:
            self._heartbeat_thread.join(timeout=5)
        self.logger.info("Heartbeat thread stopped")
    
    def _health_check_loop(self):
        """健康檢查循環"""
        while self._health_check_running:
            try:
                for service_id, instance in list(self._registered_services.items()):
                    if not instance.health_check:
                        continue
                    
                    # 執行健康檢查
                    is_healthy = self._perform_health_check(instance)
                    
                    # 更新健康狀態
                    new_status = HealthStatus.HEALTHY if is_healthy else HealthStatus.UNHEALTHY
                    self.registry.update_health_status(service_id, new_status)
                
                # 等待下一次檢查
                time.sleep(10)  # 每10秒檢查一次
                
            except Exception as e:
                self.logger.error(f"Error in health check loop: {e}")
                time.sleep(5)
    
    def _heartbeat_loop(self):
        """心跳循環"""
        while self._heartbeat_running:
            try:
                for service_id in list(self._registered_services.keys()):
                    self.registry.update_heartbeat(service_id)
                
                # 等待下一次心跳
                time.sleep(30)  # 每30秒發送心跳
                
            except Exception as e:
                self.logger.error(f"Error in heartbeat loop: {e}")
                time.sleep(10)
    
    def _perform_health_check(self, instance: ServiceInstance) -> bool:
        """
        執行健康檢查
        
        Args:
            instance: 服務實例
            
        Returns:
            健康返回True
        """
        if not instance.health_check:
            return True
        
        health_check = instance.health_check
        
        try:
            if health_check.type == 'http':
                return self._http_health_check(instance, health_check)
            elif health_check.type == 'tcp':
                return self._tcp_health_check(instance, health_check)
            elif health_check.type == 'custom' and health_check.custom_check:
                return health_check.custom_check(instance)
            else:
                self.logger.warning(f"Unknown health check type: {health_check.type}")
                return True
                
        except Exception as e:
            self.logger.error(f"Health check failed for {instance.id}: {e}")
            return False
    
    def _http_health_check(self, instance: ServiceInstance, health_check: HealthCheck) -> bool:
        """HTTP健康檢查"""
        try:
            import requests
            
            endpoint = health_check.endpoint or instance.metadata.endpoint
            if not endpoint.startswith('http'):
                endpoint = f"http://{endpoint}"
            
            response = requests.get(
                f"{endpoint}/health" if not health_check.endpoint else endpoint,
                timeout=health_check.timeout
            )
            
            return response.status_code == 200
            
        except ImportError:
            self.logger.warning("requests library not available, skipping HTTP health check")
            return True
        except Exception as e:
            self.logger.debug(f"HTTP health check failed: {e}")
            return False
    
    def _tcp_health_check(self, instance: ServiceInstance, health_check: HealthCheck) -> bool:
        """TCP健康檢查"""
        try:
            import socket
            
            # 解析端點
            endpoint = instance.metadata.endpoint
            if '://' in endpoint:
                endpoint = endpoint.split('://')[1]
            
            if ':' in endpoint:
                host, port = endpoint.rsplit(':', 1)
                port = int(port)
            else:
                host = endpoint
                port = 80
            
            # 嘗試連接
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(health_check.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            return result == 0
            
        except Exception as e:
            self.logger.debug(f"TCP health check failed: {e}")
            return False
    
    def shutdown(self):
        """關閉代理"""
        self.logger.info("Shutting down Service Agent")
        
        # 停止健康檢查和心跳
        self.stop_health_checks()
        self.stop_heartbeat()
        
        # 註銷所有服務
        for service_id in list(self._registered_services.keys()):
            self.deregister_service(service_id)
        
        self.logger.info("Service Agent shut down completed")
