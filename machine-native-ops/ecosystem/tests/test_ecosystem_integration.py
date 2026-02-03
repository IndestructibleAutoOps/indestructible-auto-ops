#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: testing
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
Ecosystem Integration Tests
============================
測試 ecosystem 所有組件的集成

GL Governance Layer: GL10-29 (Operational Layer)
"""

import sys
import time
from pathlib import Path

# Add coordination modules to path
ECOSYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ECOSYSTEM_ROOT / 'coordination' / 'service-discovery' / 'src'))
sys.path.insert(0, str(ECOSYSTEM_ROOT / 'coordination' / 'api-gateway' / 'src'))
sys.path.insert(0, str(ECOSYSTEM_ROOT / 'coordination' / 'communication' / 'src'))
sys.path.insert(0, str(ECOSYSTEM_ROOT / 'coordination' / 'data-synchronization' / 'src'))

from service_registry import ServiceRegistry, ServiceInstance, ServiceMetadata, HealthStatus
from service_agent import ServiceAgent
from service_client import ServiceClient
from gateway import Gateway
from router import Route
from message_bus import MessageBus
from event_dispatcher import EventDispatcher
from sync_engine import SyncEngine, SyncMode


def test_service_discovery_and_gateway_integration():
    """測試服務發現與 API Gateway 集成"""
    print("\n=== Test Service Discovery + API Gateway Integration ===")
    
    # 配置
    config = {
        'registry': {'persistence': False},
        'load_balancing': {'default_strategy': 'health-based'},
        'rate_limiting': {'enabled': True, 'default_limit': 100},
        'logging': {'level': 'ERROR'}
    }
    
    # 創建組件
    registry = ServiceRegistry(config)
    agent = ServiceAgent(registry, config)
    client = ServiceClient(registry, config)
    gateway = Gateway(config)
    
    # 1. 註冊後端服務
    service_id = agent.register_service(
        name='backend-api',
        platform='test-platform',
        endpoint='http://localhost:9000',
        service_type='api',
        auto_health_check=False
    )
    
    assert service_id is not None, "Service registration failed"
    
    # 更新健康狀態
    registry.update_health_status(service_id, HealthStatus.HEALTHY)
    
    print("✓ Backend service registered and healthy")
    
    # 2. 配置 Gateway 路由
    route = Route(
        path='/api/v1/backend/*',
        platform='test-platform',
        service='backend-api',
        methods=['GET', 'POST'],
        timeout=30
    )
    
    gateway.add_route(route)
    print("✓ Gateway route configured")
    
    # 3. 通過 Gateway 訪問服務
    status, headers, body = gateway.handle_request(
        method='GET',
        path='/api/v1/backend/users',
        headers={}
    )
    
    assert status == 200, f"Gateway request failed: {status}"
    assert 'X-RateLimit-Remaining' in headers, "Rate limit headers missing"
    
    print("✓ Request through gateway successful")
    print(f"  Status: {status}")
    print(f"  Rate limit remaining: {headers.get('X-RateLimit-Remaining')}")
    
    print("✅ Service Discovery + Gateway integration test passed")


def test_communication_and_sync_integration():
    """測試通信系統與數據同步集成"""
    print("\n=== Test Communication + Data Sync Integration ===")
    
    config = {
        'message_bus': {'max_queue_size': 1000},
        'sync_engine': {'batch_size': 100},
        'monitoring': {'logging': {'level': 'ERROR'}}
    }
    
    # 創建組件
    message_bus = MessageBus(config)
    message_bus.start()
    
    dispatcher = EventDispatcher(message_bus, config)
    sync_engine = SyncEngine(config)
    
    # 1. 設置事件驅動的數據同步
    sync_events = []
    
    def sync_event_handler(message):
        """處理同步事件"""
        sync_events.append(message)
        
        # 觸發數據同步
        payload = message.payload
        if 'source' in payload and 'destinations' in payload:
            job_id = sync_engine.create_sync_job(
                dataset=payload.get('dataset', 'auto-sync'),
                source=payload['source'],
                destinations=payload['destinations'],
                mode=SyncMode.MANUAL
            )
            sync_engine.execute_sync_job(job_id)
    
    # 註冊事件處理器
    dispatcher.register_handler('data.sync.request', sync_event_handler)
    dispatcher.subscribe_to_events('sync.events', ['data.sync.request'])
    
    time.sleep(0.1)
    
    print("✓ Event-driven sync configured")
    
    # 2. 添加源數據
    for i in range(5):
        sync_engine.add_data('platform-a', f'item-{i}', {'value': i})
    
    print("✓ Source data added")
    
    # 3. 通過事件觸發同步
    dispatcher.dispatch_event(
        topic='sync.events',
        event_type='data.sync.request',
        payload={
            'dataset': 'test-data',
            'source': 'platform-a',
            'destinations': ['platform-b']
        }
    )
    
    time.sleep(0.5)  # 等待事件處理
    
    assert len(sync_events) >= 1, "Sync event not received"
    print("✓ Sync event received and processed")
    
    # 4. 驗證同步結果
    dest_items = sync_engine.list_data('platform-b')
    assert len(dest_items) == 5, f"Expected 5 items, got {len(dest_items)}"
    
    print("✓ Data synchronized successfully")
    
    # 清理
    message_bus.stop()
    
    print("✅ Communication + Data Sync integration test passed")


def test_full_ecosystem_integration():
    """完整 ecosystem 集成測試"""
    print("\n=== Test Full Ecosystem Integration ===")
    
    config = {
        'registry': {'persistence': False},
        'load_balancing': {'default_strategy': 'round-robin'},
        'rate_limiting': {'enabled': True, 'default_limit': 1000},
        'message_bus': {'max_queue_size': 10000},
        'sync_engine': {'batch_size': 100},
        'monitoring': {'logging': {'level': 'ERROR'}}
    }
    
    # 創建所有組件
    registry = ServiceRegistry(config)
    agent = ServiceAgent(registry, config)
    client = ServiceClient(registry, config)
    gateway = Gateway(config)
    message_bus = MessageBus(config)
    message_bus.start()
    dispatcher = EventDispatcher(message_bus, config)
    sync_engine = SyncEngine(config)
    
    print("✓ All ecosystem components initialized")
    
    # Scenario: 服務註冊 -> API 調用 -> 事件發布 -> 數據同步
    
    # 1. 註冊服務
    service_id = agent.register_service(
        name='user-service',
        platform='platform-main',
        endpoint='http://localhost:9100',
        service_type='api',
        auto_health_check=False
    )
    
    registry.update_health_status(service_id, HealthStatus.HEALTHY)
    print("✓ Service registered")
    
    # 2. 配置 Gateway
    gateway.add_route(Route(
        path='/api/v1/users/*',
        platform='platform-main',
        service='user-service',
        methods=['GET', 'POST'],
        authentication='optional'
    ))
    
    print("✓ Gateway route configured")
    
    # 3. 設置事件處理
    events_received = []
    
    def event_handler(message):
        events_received.append(message)
    
    dispatcher.register_handler('user.created', event_handler)
    dispatcher.subscribe_to_events('user.events', ['user.created'])
    
    time.sleep(0.1)
    print("✓ Event handler configured")
    
    # 4. 模擬 API 請求
    status, headers, body = gateway.handle_request(
        method='POST',
        path='/api/v1/users/create',
        headers={},
        body={'username': 'testuser'}
    )
    
    assert status == 200, f"API request failed: {status}"
    print("✓ API request processed")
    
    # 5. 發布事件
    dispatcher.dispatch_event(
        topic='user.events',
        event_type='user.created',
        payload={'username': 'testuser', 'id': 123}
    )
    
    time.sleep(0.5)
    
    assert len(events_received) >= 1, "Event not received"
    print("✓ Event published and received")
    
    # 6. 添加並同步數據
    sync_engine.add_data('platform-main', 'user-123', {'username': 'testuser'})
    
    job_id = sync_engine.create_sync_job(
        dataset='user-data',
        source='platform-main',
        destinations=['platform-backup'],
        mode=SyncMode.MANUAL
    )
    
    sync_engine.execute_sync_job(job_id)
    
    job_status = sync_engine.get_job_status(job_id)
    assert job_status['status'] == 'completed', "Sync job failed"
    
    print("✓ Data synchronized")
    
    # 7. 驗證完整流程
    # 獲取所有組件的統計信息
    stats = {
        'service_discovery': registry.get_statistics(),
        'api_gateway': gateway.get_stats(),
        'message_bus': message_bus.get_stats(),
        'data_sync': sync_engine.get_stats()
    }
    
    print("\n✓ Full ecosystem flow completed:")
    print(f"  Services: {stats['service_discovery']['total_services']}")
    print(f"  Gateway routes: {stats['api_gateway']['routes']}")
    print(f"  Messages published: {stats['message_bus']['published']}")
    print(f"  Sync jobs: {stats['data_sync']['total_jobs']}")
    
    # 清理
    message_bus.stop()
    agent.shutdown()
    
    print("\n✅ Full ecosystem integration test passed")


def test_multi_platform_coordination():
    """測試多平台協調"""
    print("\n=== Test Multi-Platform Coordination ===")
    
    config = {
        'registry': {'persistence': False},
        'message_bus': {'max_queue_size': 1000},
        'sync_engine': {'batch_size': 50},
        'monitoring': {'logging': {'level': 'ERROR'}}
    }
    
    # 創建組件
    registry = ServiceRegistry(config)
    message_bus = MessageBus(config)
    message_bus.start()
    sync_engine = SyncEngine(config)
    
    # 模擬3個平台
    platforms = ['platform-aws', 'platform-gcp', 'platform-azure']
    
    # 1. 每個平台註冊服務
    agents = {}
    for platform in platforms:
        agent = ServiceAgent(registry, config)
        
        service_id = agent.register_service(
            name='compute-service',
            platform=platform,
            endpoint=f'http://{platform}:8080',
            auto_health_check=False
        )
        
        registry.update_health_status(service_id, HealthStatus.HEALTHY)
        agents[platform] = agent
    
    print(f"✓ {len(platforms)} platforms registered with services")
    
    # 2. 跨平台服務發現
    client = ServiceClient(registry, config)
    all_services = client.discover_services(name='compute-service')
    
    assert len(all_services) == 3, f"Expected 3 services, got {len(all_services)}"
    print(f"✓ Cross-platform service discovery: found {len(all_services)} instances")
    
    # 3. 跨平台消息通信
    platform_messages = {p: [] for p in platforms}
    
    for platform in platforms:
        def make_handler(p):
            def handler(msg):
                platform_messages[p].append(msg)
            return handler
        
        message_bus.subscribe(f'{platform}.events', make_handler(platform))
    
    # 發送廣播消息
    for platform in platforms:
        message_bus.publish(
            f'{platform}.events',
            'platform.status',
            {'platform': platform, 'status': 'running'}
        )
    
    time.sleep(0.5)
    
    # 每個平台應該收到消息
    for platform in platforms:
        assert len(platform_messages[platform]) >= 1, f"{platform} did not receive message"
    
    print("✓ Cross-platform messaging working")
    
    # 4. 跨平台數據同步
    # 在 platform-aws 添加數據
    for i in range(10):
        sync_engine.add_data('platform-aws', f'config-{i}', {'id': i, 'platform': 'aws'})
    
    # 同步到其他平台
    job_id = sync_engine.create_sync_job(
        dataset='shared-config',
        source='platform-aws',
        destinations=['platform-gcp', 'platform-azure'],
        mode=SyncMode.MANUAL
    )
    
    sync_engine.execute_sync_job(job_id)
    
    # 驗證
    gcp_items = sync_engine.list_data('platform-gcp')
    azure_items = sync_engine.list_data('platform-azure')
    
    assert len(gcp_items) == 10, "GCP sync failed"
    assert len(azure_items) == 10, "Azure sync failed"
    
    print("✓ Cross-platform data sync working")
    
    # 5. 統計
    stats = registry.get_statistics()
    print(f"\n✓ Multi-platform coordination completed:")
    print(f"  Platforms: {stats['platforms']}")
    print(f"  Services: {stats['total_services']}")
    print(f"  Messages: {message_bus.get_stats()['published']}")
    print(f"  Synced items: 20")
    
    # 清理
    for agent in agents.values():
        agent.shutdown()
    message_bus.stop()
    
    print("\n✅ Multi-platform coordination test passed")


def test_end_to_end_workflow():
    """端到端工作流測試"""
    print("\n=== Test End-to-End Workflow ===")
    
    config = {
        'registry': {'persistence': False},
        'rate_limiting': {'enabled': True, 'default_limit': 1000},
        'message_bus': {'max_queue_size': 10000},
        'sync_engine': {'batch_size': 100},
        'monitoring': {'logging': {'level': 'ERROR'}}
    }
    
    # 完整系統
    registry = ServiceRegistry(config)
    agent = ServiceAgent(registry, config)
    client = ServiceClient(registry, config)
    gateway = Gateway(config)
    message_bus = MessageBus(config)
    message_bus.start()
    dispatcher = EventDispatcher(message_bus, config)
    sync_engine = SyncEngine(config)
    
    print("✓ Full ecosystem initialized")
    
    # Workflow: 用戶創建 -> API 調用 -> 事件通知 -> 數據同步 -> 備份
    
    workflow_steps = []
    
    # Step 1: 註冊用戶服務
    user_service = agent.register_service(
        name='user-service',
        platform='app-platform',
        endpoint='http://localhost:8080',
        auto_health_check=False
    )
    registry.update_health_status(user_service, HealthStatus.HEALTHY)
    workflow_steps.append("service_registered")
    
    # Step 2: 配置 API 路由
    gateway.add_route(Route(
        path='/api/v1/users/*',
        platform='app-platform',
        service='user-service',
        methods=['POST'],
        authentication='optional'
    ))
    workflow_steps.append("route_configured")
    
    # Step 3: 設置事件監聽（觸發數據同步）
    def sync_on_user_created(message):
        # 添加用戶數據
        user_data = message.payload
        sync_engine.add_data('app-platform', f"user-{user_data['id']}", user_data)
        
        # 同步到備份平台
        job_id = sync_engine.create_sync_job(
            dataset='user-data',
            source='app-platform',
            destinations=['backup-platform'],
            mode=SyncMode.MANUAL
        )
        sync_engine.execute_sync_job(job_id)
        
        workflow_steps.append("data_synced")
    
    dispatcher.register_handler('user.created', sync_on_user_created)
    dispatcher.subscribe_to_events('user.events', ['user.created'])
    time.sleep(0.1)
    workflow_steps.append("event_handler_registered")
    
    # Step 4: 模擬 API 請求創建用戶
    status, _, body = gateway.handle_request(
        method='POST',
        path='/api/v1/users/create',
        body={'username': 'newuser', 'email': 'user@example.com'}
    )
    
    assert status == 200, "API request failed"
    workflow_steps.append("api_request_processed")
    
    # Step 5: 發布用戶創建事件
    dispatcher.dispatch_event(
        topic='user.events',
        event_type='user.created',
        payload={'id': 123, 'username': 'newuser', 'email': 'user@example.com'}
    )
    
    time.sleep(0.5)
    workflow_steps.append("event_published")
    
    # Step 6: 驗證數據已同步到備份
    backup_items = sync_engine.list_data('backup-platform')
    assert len(backup_items) >= 1, "Data not synced to backup"
    workflow_steps.append("backup_verified")
    
    # 驗證完整工作流
    expected_steps = [
        'service_registered',
        'route_configured',
        'event_handler_registered',
        'api_request_processed',
        'event_published',
        'data_synced',
        'backup_verified'
    ]
    
    for step in expected_steps:
        assert step in workflow_steps, f"Workflow step missing: {step}"
    
    print(f"\n✓ End-to-end workflow completed ({len(workflow_steps)} steps):")
    for i, step in enumerate(workflow_steps, 1):
        print(f"  {i}. {step}")
    
    # 清理
    agent.shutdown()
    message_bus.stop()
    
    print("\n✅ End-to-end workflow test passed")


def main():
    """運行所有集成測試"""
    print("\n" + "="*60)
    print("Ecosystem Integration Tests")
    print("="*60)
    
    try:
        test_service_discovery_and_gateway_integration()
        test_communication_and_sync_integration()
        test_multi_platform_coordination()
        test_end_to_end_workflow()
        
        print("\n" + "="*60)
        print("✅ ALL INTEGRATION TESTS PASSED")
        print("="*60)
        print("")
        print("Summary:")
        print("  ✓ Service Discovery + API Gateway integration")
        print("  ✓ Communication + Data Sync integration")
        print("  ✓ Multi-platform coordination")
        print("  ✓ End-to-end workflow")
        print("")
        print("Ecosystem is fully integrated and operational!")
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
