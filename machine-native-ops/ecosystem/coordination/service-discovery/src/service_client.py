#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: coordination
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Service Client
=================
服務客戶端 - 用於發現和調用服務

GL Governance Layer: GL10-29 (Operational Layer)
"""

import random
from typing import Optional, List, Dict, Any
import logging

from service_registry import (
    ServiceRegistry,
    ServiceInstance,
    ServiceStatus,
    HealthStatus
)


class LoadBalancingStrategy:
    """負載均衡策略基類"""
    
    def select(self, instances: List[ServiceInstance]) -> Optional[ServiceInstance]:
        """
        選擇一個服務實例
        
        Args:
            instances: 可用的服務實例列表
            
        Returns:
            選中的服務實例或None
        """
        raise NotImplementedError


class RoundRobinStrategy(LoadBalancingStrategy):
    """輪詢策略"""
    
    def __init__(self):
        self.current_index = 0
    
    def select(self, instances: List[ServiceInstance]) -> Optional[ServiceInstance]:
        if not instances:
            return None
        
        instance = instances[self.current_index % len(instances)]
        self.current_index += 1
        return instance


class RandomStrategy(LoadBalancingStrategy):
    """隨機策略"""
    
    def select(self, instances: List[ServiceInstance]) -> Optional[ServiceInstance]:
        if not instances:
            return None
        return random.choice(instances)


class HealthBasedStrategy(LoadBalancingStrategy):
    """基於健康狀態的策略 - 只選擇健康的實例"""
    
    def __init__(self, fallback_strategy: Optional[LoadBalancingStrategy] = None):
        self.fallback_strategy = fallback_strategy or RandomStrategy()
    
    def select(self, instances: List[ServiceInstance]) -> Optional[ServiceInstance]:
        if not instances:
            return None
        
        # 過濾健康的實例
        healthy_instances = [
            inst for inst in instances
            if inst.health_status == HealthStatus.HEALTHY
        ]
        
        # 如果有健康的實例，使用回退策略選擇
        if healthy_instances:
            return self.fallback_strategy.select(healthy_instances)
        
        # 如果沒有健康的實例，嘗試使用狀態為UNKNOWN的
        unknown_instances = [
            inst for inst in instances
            if inst.health_status == HealthStatus.UNKNOWN
        ]
        
        if unknown_instances:
            return self.fallback_strategy.select(unknown_instances)
        
        # 最後的回退：使用任何實例
        return self.fallback_strategy.select(instances)


class WeightedStrategy(LoadBalancingStrategy):
    """加權策略"""
    
    def select(self, instances: List[ServiceInstance]) -> Optional[ServiceInstance]:
        if not instances:
            return None
        
        # 根據成功率計算權重
        weights = []
        for inst in instances:
            total = inst.success_count + inst.failure_count
            if total > 0:
                weight = inst.success_count / total
            else:
                weight = 1.0
            weights.append(weight)
        
        # 加權隨機選擇
        total_weight = sum(weights)
        if total_weight == 0:
            return random.choice(instances)
        
        r = random.uniform(0, total_weight)
        cumulative = 0
        for inst, weight in zip(instances, weights):
            cumulative += weight
            if r <= cumulative:
                return inst
        
        return instances[-1]


class LeastConnectionsStrategy(LoadBalancingStrategy):
    """最少連接策略"""
    
    def select(self, instances: List[ServiceInstance]) -> Optional[ServiceInstance]:
        if not instances:
            return None
        
        # 選擇連接數最少的實例
        return min(instances, key=lambda inst: inst.connection_count)


class ServiceClient:
    """服務客戶端"""
    
    def __init__(
        self,
        registry: ServiceRegistry,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化服務客戶端
        
        Args:
            registry: 服務註冊中心
            config: 配置字典
        """
        self.registry = registry
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 負載均衡策略
        self.load_balancing_strategies = {
            'round-robin': RoundRobinStrategy(),
            'random': RandomStrategy(),
            'health-based': HealthBasedStrategy(),
            'weighted': WeightedStrategy(),
            'least-connections': LeastConnectionsStrategy()
        }
        
        # 默認策略 - 驗證配置並在未知值時回退到安全默認值
        default_strategy_name = self.config.get(
            'load_balancing', {}
        ).get('default_strategy', 'health-based')
        self.default_strategy = self.load_balancing_strategies.get(default_strategy_name)
        if self.default_strategy is None:
            # 未知的負載均衡策略名稱，記錄警告並回退到 health-based
            self.logger.warning(
                "Unknown load_balancing.default_strategy '%s'; "
                "falling back to 'health-based'",
                default_strategy_name,
            )
            fallback_name = 'health-based'
            fallback_strategy = self.load_balancing_strategies.get(fallback_name)
            if fallback_strategy is None:
                # 編碼錯誤或配置錯誤：連安全默認策略都不可用，立即失敗
                raise ValueError(
                    "Invalid load_balancing.default_strategy configuration: "
                    f"'{default_strategy_name}' is not a known strategy and "
                    f"fallback '{fallback_name}' is not available."
                )
            self.default_strategy = fallback_strategy
        
        self.logger.info("Service Client initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('ServiceClient')
        level = self.config.get('monitoring', {}).get('logging', {}).get('level', 'INFO')
        logger.setLevel(getattr(logging, level))
        
        # Avoid attaching multiple identical StreamHandlers to the same logger
        if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def discover_services(
        self,
        name: Optional[str] = None,
        platform: Optional[str] = None,
        service_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        only_healthy: bool = True,
        only_active: bool = True
    ) -> List[ServiceInstance]:
        """
        發現服務
        
        Args:
            name: 服務名稱
            platform: 平台名稱
            service_type: 服務類型
            tags: 標籤列表
            only_healthy: 只返回健康的服務
            only_active: 只返回活躍的服務
            
        Returns:
            匹配的服務實例列表
        """
        status = ServiceStatus.ACTIVE if only_active else None
        health_status = HealthStatus.HEALTHY if only_healthy else None
        
        services = self.registry.discover_services(
            name=name,
            platform=platform,
            service_type=service_type,
            tags=tags,
            status=status,
            health_status=health_status
        )
        
        self.logger.debug(f"Discovered {len(services)} services")
        return services
    
    def get_service_instance(
        self,
        name: Optional[str] = None,
        platform: Optional[str] = None,
        service_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        strategy: Optional[str] = None
    ) -> Optional[ServiceInstance]:
        """
        獲取一個服務實例（使用負載均衡）
        
        Args:
            name: 服務名稱
            platform: 平台名稱
            service_type: 服務類型
            tags: 標籤列表
            strategy: 負載均衡策略名稱
            
        Returns:
            選中的服務實例或None
        """
        # 發現服務
        instances = self.discover_services(
            name=name,
            platform=platform,
            service_type=service_type,
            tags=tags,
            only_healthy=False,  # 讓負載均衡策略處理健康檢查
            only_active=True
        )
        
        if not instances:
            self.logger.warning(f"No services found for name={name}, platform={platform}, type={service_type}")
            return None
        
        # 選擇負載均衡策略
        lb_strategy = self.default_strategy
        if strategy and strategy in self.load_balancing_strategies:
            lb_strategy = self.load_balancing_strategies[strategy]
        
        # 選擇實例
        instance = lb_strategy.select(instances)
        
        if instance:
            self.logger.debug(f"Selected service instance: {instance.id}")
            # 增加連接計數
            instance.connection_count += 1
        
        return instance
    
    def call_service(
        self,
        name: str,
        method: str = 'GET',
        path: str = '/',
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        platform: Optional[str] = None,
        service_type: Optional[str] = None
    ) -> Optional[Any]:
        """
        調用服務
        
        Args:
            name: 服務名稱
            method: HTTP方法
            path: 請求路徑
            data: 請求數據
            headers: 請求頭
            timeout: 超時時間
            platform: 平台名稱
            service_type: 服務類型
            
        Returns:
            響應數據或None
        """
        # 獲取服務實例
        instance = self.get_service_instance(
            name=name,
            platform=platform,
            service_type=service_type
        )
        
        if not instance:
            self.logger.error(f"No available service instance for {name}")
            return None
        
        try:
            import requests
            
            # 構建URL
            endpoint = instance.metadata.endpoint
            if not endpoint.startswith('http'):
                endpoint = f"http://{endpoint}"
            
            url = f"{endpoint.rstrip('/')}/{path.lstrip('/')}"
            
            # 發送請求
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=timeout
            )
            
            response.raise_for_status()
            
            # 更新成功計數
            self.registry.update_health_status(instance.id, HealthStatus.HEALTHY)
            
            return response.json() if response.content else None
            
        except ImportError:
            self.logger.error("requests library not available")
            return None
        except Exception as e:
            self.logger.error(f"Error calling service {name}: {e}")
            # 更新失敗計數
            self.registry.update_health_status(instance.id, HealthStatus.UNHEALTHY)
            return None
    
    def get_service_info(self, service_id: str) -> Optional[Dict[str, Any]]:
        """
        獲取服務詳細信息
        
        Args:
            service_id: 服務ID
            
        Returns:
            服務信息字典或None
        """
        instance = self.registry.get_service(service_id)
        if not instance:
            return None
        
        return {
            'id': instance.id,
            'name': instance.metadata.name,
            'platform': instance.metadata.platform,
            'endpoint': instance.metadata.endpoint,
            'type': instance.metadata.type,
            'version': instance.metadata.version,
            'tags': instance.metadata.tags,
            'capabilities': instance.metadata.capabilities,
            'status': instance.status.value,
            'health_status': instance.health_status.value,
            'registered_at': instance.registered_at,
            'last_heartbeat': instance.last_heartbeat,
            'success_count': instance.success_count,
            'failure_count': instance.failure_count,
            'connection_count': instance.connection_count
        }
