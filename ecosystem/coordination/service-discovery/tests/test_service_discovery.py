#!/usr/bin/env python3
"""
Service Discovery System Tests
===============================
測試服務發現系統的核心功能
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from service_registry import (
    ServiceRegistry,
    ServiceInstance,
    ServiceMetadata,
    HealthCheck,
    ServiceStatus,
    HealthStatus
)
from service_agent import ServiceAgent
from service_client import ServiceClient


def test_service_registry():
    """測試服務註冊中心"""
    print("\n=== Test Service Registry ===")
    
    # 創建註冊中心
    config = {'registry': {'persistence': False}}
    registry = ServiceRegistry(config)
    
    # 創建服務實例
    metadata = ServiceMetadata(
        name="test-service",
        platform="test-platform",
        endpoint="http://localhost:8080",
        type="compute",
        version="1.0.0",
        tags=["test", "compute"]
    )
    
    instance = ServiceInstance(
        id="test-service-001",
        metadata=metadata
    )
    
    # 測試註冊
    assert registry.register_service(instance), "Failed to register service"
    print("✓ Service registered")
    
    # 測試獲取
    retrieved = registry.get_service("test-service-001")
    assert retrieved is not None, "Failed to get service"
    assert retrieved.id == "test-service-001", "Service ID mismatch"
    print("✓ Service retrieved")
    
    # 測試發現
    services = registry.discover_services(name="test-service")
    assert len(services) == 1, "Failed to discover service"
    print("✓ Service discovered")
    
    # 測試健康狀態更新
    assert registry.update_health_status("test-service-001", HealthStatus.HEALTHY), "Failed to update health"
    retrieved = registry.get_service("test-service-001")
    assert retrieved.health_status == HealthStatus.HEALTHY, "Health status not updated"
    print("✓ Health status updated")
    
    # 測試統計
    stats = registry.get_statistics()
    assert stats['total_services'] == 1, "Statistics incorrect"
    print(f"✓ Statistics: {stats}")
    
    # 測試註銷
    assert registry.deregister_service("test-service-001"), "Failed to deregister service"
    assert registry.get_service("test-service-001") is None, "Service still exists after deregistration"
    print("✓ Service deregistered")
    
    print("✅ Service Registry tests passed")


def test_service_agent():
    """測試服務代理"""
    print("\n=== Test Service Agent ===")
    
    # 創建註冊中心和代理
    config = {'registry': {'persistence': False}}
    registry = ServiceRegistry(config)
    agent = ServiceAgent(registry, config)
    
    # 測試服務註冊
    service_id = agent.register_service(
        name="agent-test-service",
        platform="test-platform",
        endpoint="http://localhost:9000",
        service_type="storage",
        version="2.0.0",
        tags=["test", "storage"],
        auto_health_check=False  # 禁用自動健康檢查用於測試
    )
    
    assert service_id is not None, "Failed to register service via agent"
    print(f"✓ Service registered via agent: {service_id}")
    
    # 驗證服務已註冊
    instance = registry.get_service(service_id)
    assert instance is not None, "Service not found in registry"
    assert instance.metadata.name == "agent-test-service", "Service name mismatch"
    print("✓ Service verified in registry")
    
    # 測試註銷
    assert agent.deregister_service(service_id), "Failed to deregister service via agent"
    assert registry.get_service(service_id) is None, "Service still exists after agent deregistration"
    print("✓ Service deregistered via agent")
    
    print("✅ Service Agent tests passed")


def test_service_client():
    """測試服務客戶端"""
    print("\n=== Test Service Client ===")
    
    # 創建註冊中心和客戶端
    config = {
        'registry': {'persistence': False},
        'load_balancing': {'default_strategy': 'round-robin'}
    }
    registry = ServiceRegistry(config)
    client = ServiceClient(registry, config)
    
    # 註冊多個服務實例
    for i in range(3):
        metadata = ServiceMetadata(
            name="client-test-service",
            platform=f"platform-{i}",
            endpoint=f"http://localhost:800{i}",
            type="api",
            version="1.0.0"
        )
        
        instance = ServiceInstance(
            id=f"client-test-{i}",
            metadata=metadata,
            health_status=HealthStatus.HEALTHY
        )
        
        registry.register_service(instance)
    
    print("✓ Registered 3 service instances")
    
    # 測試服務發現
    services = client.discover_services(name="client-test-service")
    assert len(services) == 3, f"Expected 3 services, found {len(services)}"
    print(f"✓ Discovered {len(services)} services")
    
    # 測試負載均衡
    selected_instances = set()
    for _ in range(6):
        instance = client.get_service_instance(name="client-test-service", strategy="round-robin")
        assert instance is not None, "Failed to get service instance"
        selected_instances.add(instance.id)
    
    assert len(selected_instances) == 3, "Round-robin not working correctly"
    print(f"✓ Load balancing (round-robin) working: selected all {len(selected_instances)} instances")
    
    # 測試健康狀態過濾
    # 標記一個服務為不健康
    registry.update_health_status("client-test-0", HealthStatus.UNHEALTHY)
    
    healthy_services = client.discover_services(name="client-test-service", only_healthy=True)
    assert len(healthy_services) == 2, f"Expected 2 healthy services, found {len(healthy_services)}"
    print("✓ Health-based filtering working")
    
    # 測試服務信息獲取
    info = client.get_service_info("client-test-1")
    assert info is not None, "Failed to get service info"
    assert info['name'] == "client-test-service", "Service info incorrect"
    print("✓ Service info retrieved")
    
    print("✅ Service Client tests passed")


def test_integration():
    """集成測試"""
    print("\n=== Integration Test ===")
    
    # 創建完整系統
    config = {
        'registry': {'persistence': False},
        'load_balancing': {'default_strategy': 'health-based'}
    }
    
    registry = ServiceRegistry(config)
    agent = ServiceAgent(registry, config)
    client = ServiceClient(registry, config)
    
    # 通過代理註冊服務
    service_ids = []
    for i in range(3):
        service_id = agent.register_service(
            name="integration-service",
            platform=f"platform-{i}",
            endpoint=f"http://localhost:900{i}",
            service_type="compute",
            version="1.0.0",
            auto_health_check=False
        )
        service_ids.append(service_id)
    
    print(f"✓ Registered {len(service_ids)} services via agent")
    
    # 通過客戶端發現服務
    discovered = client.discover_services(name="integration-service", only_healthy=False)
    assert len(discovered) == 3, "Service discovery failed in integration test"
    print(f"✓ Discovered {len(discovered)} services via client")
    
    # 更新健康狀態
    for i, service_id in enumerate(service_ids):
        status = HealthStatus.HEALTHY if i < 2 else HealthStatus.UNHEALTHY
        registry.update_health_status(service_id, status)
    
    # 使用健康策略獲取實例
    instance = client.get_service_instance(
        name="integration-service",
        strategy="health-based"
    )
    assert instance is not None, "Failed to get instance with health-based strategy"
    assert instance.health_status in [HealthStatus.HEALTHY, HealthStatus.UNKNOWN], "Got unhealthy instance"
    print("✓ Health-based load balancing working in integration")
    
    # 清理
    for service_id in service_ids:
        agent.deregister_service(service_id)
    
    stats = registry.get_statistics()
    assert stats['total_services'] == 0, "Services not cleaned up"
    print("✓ Cleanup successful")
    
    print("✅ Integration test passed")


def main():
    """運行所有測試"""
    print("\n" + "="*60)
    print("Service Discovery System - Test Suite")
    print("="*60)
    
    try:
        test_service_registry()
        test_service_agent()
        test_service_client()
        test_integration()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60 + "\n")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
