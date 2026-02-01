#!/usr/bin/env python3
"""
Service Registration Example
=============================
示例：如何註冊服務到平台
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from platform_manager import PlatformManager


def main():
    """註冊服務示例"""
    print("\n=== Service Registration Example ===\n")
    
    # 1. 創建平台管理器
    pm = PlatformManager('configs/platform-config.yaml')
    print(f"✓ Platform Manager initialized: {pm.platform_name}\n")
    
    # 2. 註冊服務
    print("Registering services...\n")
    
    # 註冊計算服務
    compute_service = pm.register_service(
        name='compute-service',
        endpoint='http://localhost:9001',
        service_type='compute',
        version='1.0.0',
        tags=['compute', 'cpu'],
        health_check={
            'type': 'http',
            'path': '/health',
            'interval': 30
        }
    )
    
    if compute_service:
        print(f"✓ Compute service registered: {compute_service}")
    
    # 註冊存儲服務
    storage_service = pm.register_service(
        name='storage-service',
        endpoint='http://localhost:9002',
        service_type='storage',
        version='1.0.0',
        tags=['storage', 's3'],
        health_check={
            'type': 'http',
            'path': '/health',
            'interval': 30
        }
    )
    
    if storage_service:
        print(f"✓ Storage service registered: {storage_service}")
    
    # 3. 發現服務
    print("\nDiscovering services...\n")
    
    services = pm.discover_services(only_healthy=False)
    print(f"Found {len(services)} services:")
    for service in services:
        print(f"  - {service.metadata.name} @ {service.metadata.endpoint}")
    
    # 4. 查看平台狀態
    print("\nPlatform status:\n")
    status = pm.get_platform_status()
    
    if 'service_discovery' in status['components']:
        sd_stats = status['components']['service_discovery']
        print(f"  Services registered: {sd_stats['total_services']}")
        print(f"  Platforms: {sd_stats['platforms']}")
    
    print("\n✅ Example completed successfully!\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
