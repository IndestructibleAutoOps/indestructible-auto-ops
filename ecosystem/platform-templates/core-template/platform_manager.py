#!/usr/bin/env python3
"""
GL Platform Manager
===================
平台管理工具 - 統一管理平台服務

GL Governance Layer: GL10-29 (Operational Layer)
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add ecosystem to path
ECOSYSTEM_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ECOSYSTEM_ROOT))

try:
    from coordination.service_discovery import ServiceRegistry, ServiceAgent, ServiceClient
    from coordination.api_gateway import Gateway
    from coordination.communication import MessageBus, EventDispatcher
    from coordination.data_synchronization import SyncEngine, SyncMode
    ECOSYSTEM_AVAILABLE = True
except ImportError:
    ECOSYSTEM_AVAILABLE = False


class PlatformManager:
    """平台管理器"""
    
    def __init__(self, config_path: str):
        """
        初始化平台管理器
        
        Args:
            config_path: 配置文件路徑
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
        # 提取平台信息
        self.platform_name = self.config.get('platform', {}).get('name', 'unknown')
        
        # 初始化組件（如果 ecosystem 可用）
        self.registry = None
        self.agent = None
        self.client = None
        self.gateway = None
        self.message_bus = None
        self.sync_engine = None
        
        if ECOSYSTEM_AVAILABLE:
            self._initialize_components()
        else:
            print("Warning: Ecosystem modules not available")
    
    def _load_config(self) -> Dict[str, Any]:
        """加載配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _initialize_components(self):
        """初始化 ecosystem 組件"""
        # Service Discovery
        if self.config.get('service_discovery', {}).get('enabled'):
            self.registry = ServiceRegistry(self.config)
            self.agent = ServiceAgent(self.registry, self.config)
            self.client = ServiceClient(self.registry, self.config)
            print(f"✓ Service Discovery initialized")
        
        # API Gateway
        if self.config.get('api_gateway', {}).get('enabled'):
            self.gateway = Gateway(self.config)
            print(f"✓ API Gateway initialized")
        
        # Communication
        if self.config.get('communication', {}).get('enabled'):
            self.message_bus = MessageBus(self.config)
            self.message_bus.start()
            print(f"✓ Message Bus initialized")
        
        # Data Sync
        if self.config.get('data_sync', {}).get('enabled'):
            self.sync_engine = SyncEngine(self.config)
            print(f"✓ Sync Engine initialized")
    
    def register_service(
        self,
        name: str,
        endpoint: str,
        service_type: Optional[str] = None,
        health_check: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Optional[str]:
        """
        註冊服務
        
        Args:
            name: 服務名稱
            endpoint: 服務端點
            service_type: 服務類型
            health_check: 健康檢查配置
            **kwargs: 其他參數
            
        Returns:
            服務ID或None
        """
        if not self.agent:
            print("Error: Service Agent not initialized")
            return None
        
        from coordination.service_discovery import HealthCheck
        
        hc = None
        if health_check:
            hc = HealthCheck(
                type=health_check.get('type', 'http'),
                endpoint=health_check.get('path'),
                interval=health_check.get('interval', 30),
                timeout=health_check.get('timeout', 5)
            )
        
        return self.agent.register_service(
            name=name,
            platform=self.platform_name,
            endpoint=endpoint,
            service_type=service_type,
            health_check=hc,
            **kwargs
        )
    
    def discover_services(self, **filters) -> List[Any]:
        """發現服務"""
        if not self.client:
            print("Error: Service Client not initialized")
            return []
        
        return self.client.discover_services(**filters)
    
    def add_route(
        self,
        path: str,
        service: str,
        methods: List[str],
        **kwargs
    ) -> bool:
        """添加 API 路由"""
        if not self.gateway:
            print("Error: Gateway not initialized")
            return False
        
        from coordination.api_gateway import Route
        
        route = Route(
            path=path,
            platform=self.platform_name,
            service=service,
            methods=methods,
            **kwargs
        )
        
        return self.gateway.add_route(route)
    
    def publish_event(self, topic: str, event_type: str, payload: Dict[str, Any]) -> str:
        """發布事件"""
        if not self.message_bus:
            print("Error: Message Bus not initialized")
            return ""
        
        return self.message_bus.publish(
            topic=topic,
            event_type=event_type,
            payload=payload,
            source=self.platform_name
        )
    
    def subscribe_events(self, topic: str, handler: callable) -> str:
        """訂閱事件"""
        if not self.message_bus:
            print("Error: Message Bus not initialized")
            return ""
        
        return self.message_bus.subscribe(topic, handler)
    
    def sync_data(
        self,
        source: str,
        destinations: List[str],
        dataset: str
    ) -> Optional[str]:
        """同步數據"""
        if not self.sync_engine:
            print("Error: Sync Engine not initialized")
            return None
        
        job_id = self.sync_engine.create_sync_job(
            dataset=dataset,
            source=source,
            destinations=destinations,
            mode=SyncMode.MANUAL
        )
        
        self.sync_engine.execute_sync_job(job_id)
        return job_id
    
    def get_platform_status(self) -> Dict[str, Any]:
        """獲取平台狀態"""
        status = {
            'platform': self.platform_name,
            'components': {}
        }
        
        if self.registry:
            status['components']['service_discovery'] = self.registry.get_statistics()
        
        if self.gateway:
            status['components']['api_gateway'] = self.gateway.get_stats()
        
        if self.message_bus:
            status['components']['message_bus'] = self.message_bus.get_stats()
        
        if self.sync_engine:
            status['components']['data_sync'] = self.sync_engine.get_stats()
        
        return status
    
    def shutdown(self):
        """關閉平台"""
        print(f"Shutting down platform: {self.platform_name}")
        
        if self.agent:
            self.agent.shutdown()
        
        if self.message_bus:
            self.message_bus.stop()
        
        print("Platform shut down completed")


def main():
    """主函數 - 命令行工具"""
    import argparse
    
    parser = argparse.ArgumentParser(description='GL Platform Manager')
    parser.add_argument('--config', default='configs/platform-config.yaml', help='Config file path')
    parser.add_argument('--status', action='store_true', help='Show platform status')
    
    args = parser.parse_args()
    
    try:
        pm = PlatformManager(args.config)
        
        if args.status:
            status = pm.get_platform_status()
            import json
            print(json.dumps(status, indent=2))
        else:
            print(f"Platform Manager initialized: {pm.platform_name}")
            print("Use --status to view platform status")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
