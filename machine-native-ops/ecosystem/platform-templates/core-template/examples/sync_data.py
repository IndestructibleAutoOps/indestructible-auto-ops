#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: platform-templates
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
Data Synchronization Example
=============================
示例：如何同步數據到其他平台
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from platform_manager import PlatformManager


def main():
    """數據同步示例"""
    print("\n=== Data Synchronization Example ===\n")
    
    # 1. 創建平台管理器
    pm = PlatformManager('configs/platform-config.yaml')
    print(f"✓ Platform Manager initialized: {pm.platform_name}\n")
    
    if not pm.sync_engine:
        print("Error: Sync Engine not available")
        return
    
    # 2. 添加源數據
    print("Adding source data...\n")
    
    source_location = 'platform-a'
    
    for i in range(10):
        pm.sync_engine.add_data(
            source_location,
            f'config-{i}',
            {
                'id': i,
                'name': f'config_{i}',
                'value': i * 100,
                'enabled': True
            }
        )
    
    print(f"✓ Added 10 items to {source_location}")
    
    # 3. 創建同步任務
    print("\nCreating sync job...\n")
    
    destinations = ['platform-b', 'platform-c']
    
    job_id = pm.sync_data(
        source=source_location,
        destinations=destinations,
        dataset='platform-config'
    )
    
    if job_id:
        print(f"✓ Sync job created: {job_id}")
        
        # 4. 檢查同步狀態
        status = pm.sync_engine.get_job_status(job_id)
        
        print(f"\nSync job status:")
        print(f"  Status: {status['status']}")
        print(f"  Items synced: {status['items_synced']}/{status['items_total']}")
        print(f"  Conflicts: {status['conflicts']}")
        print(f"  Failed: {status['items_failed']}")
        
        # 5. 驗證目標數據
        print(f"\nVerifying synchronized data...\n")
        
        for dest in destinations:
            items = pm.sync_engine.list_data(dest)
            print(f"  {dest}: {len(items)} items")
            
            # 驗證數據內容
            if items:
                sample = pm.sync_engine.get_data(dest, items[0])
                if sample:
                    print(f"    Sample data: {sample.data}")
        
        # 6. 查看同步統計
        print(f"\nSync Engine statistics:\n")
        stats = pm.sync_engine.get_stats()
        print(f"  Total locations: {stats['locations']}")
        print(f"  Total items: {stats['total_items']}")
        print(f"  Sync jobs: {stats['total_jobs']}")
        print(f"  Conflicts resolved: {stats['conflict_count']}")
    
    print("\n✅ Example completed successfully!\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
