#!/usr/bin/env python3
"""
Data Synchronization System Tests
==================================
測試數據同步系統的核心功能
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from sync_engine import SyncEngine, SyncMode, SyncStatus
from conflict_resolver import ConflictResolver
from sync_scheduler import SyncScheduler
from connectors import FilesystemConnector


def test_sync_engine():
    """測試同步引擎"""
    print("\n=== Test Sync Engine ===")
    
    config = {
        'sync_engine': {
            'batch_size': 10,
            'max_retries': 3
        },
        'conflict_resolution': {
            'default_strategy': 'last-write-wins'
        },
        'monitoring': {
            'logging': {
                'level': 'WARNING'
            }
        }
    }
    
    engine = SyncEngine(config)
    
    # 添加源數據
    for i in range(5):
        engine.add_data('source-a', f'item-{i}', {'value': i, 'name': f'item_{i}'})
    
    print("✓ Source data added (5 items)")
    
    # 創建同步任務
    job_id = engine.create_sync_job(
        dataset='test-dataset',
        source='source-a',
        destinations=['dest-b', 'dest-c'],
        mode=SyncMode.MANUAL
    )
    
    assert job_id != "", "Job creation failed"
    print(f"✓ Sync job created: {job_id}")
    
    # 執行同步
    success = engine.execute_sync_job(job_id)
    assert success, "Sync job execution failed"
    print("✓ Sync job executed")
    
    # 驗證同步結果
    status = engine.get_job_status(job_id)
    assert status is not None, "Job status not found"
    assert status['status'] == SyncStatus.COMPLETED.value, f"Job not completed: {status['status']}"
    assert status['items_synced'] == 10, f"Expected 10 items synced, got {status['items_synced']}"
    print(f"✓ Sync completed: {status['items_synced']} items synced")
    
    # 驗證目標數據
    dest_items = engine.list_data('dest-b')
    assert len(dest_items) == 5, f"Expected 5 items in dest-b, got {len(dest_items)}"
    print("✓ Destination data verified")
    
    # 測試衝突檢測
    # 修改源數據
    engine.add_data('source-a', 'item-0', {'value': 100, 'name': 'modified'})
    
    # 再次同步
    job_id2 = engine.create_sync_job(
        dataset='test-dataset',
        source='source-a',
        destinations=['dest-b'],
        mode=SyncMode.MANUAL
    )
    
    engine.execute_sync_job(job_id2)
    status2 = engine.get_job_status(job_id2)
    
    assert status2['conflicts'] >= 1, "Expected at least 1 conflict"
    print(f"✓ Conflict detected and resolved: {status2['conflicts']} conflicts")
    
    # 測試統計
    stats = engine.get_stats()
    assert stats['total_items'] >= 5, "Stats incorrect"
    assert stats['sync_count'] >= 2, "Sync count incorrect"
    print(f"✓ Stats: {stats}")
    
    print("✅ Sync Engine tests passed")


def test_conflict_resolver():
    """測試衝突解決器"""
    print("\n=== Test Conflict Resolver ===")
    
    config = {
        'monitoring': {
            'logging': {
                'level': 'ERROR'
            }
        }
    }
    
    resolver = ConflictResolver(config)
    
    # 測試 Last-Write-Wins
    source_data = {'value': 100}
    target_data = {'value': 50}
    source_ts = "2026-02-01T10:00:00"
    target_ts = "2026-02-01T09:00:00"
    
    result = resolver.resolve(
        'item-1',
        source_data,
        target_data,
        source_ts,
        target_ts,
        'last-write-wins'
    )
    
    assert result == source_data, "LWW resolution incorrect"
    print("✓ Last-Write-Wins resolution works")
    
    # 測試 Merge
    source_dict = {'a': 1, 'b': 2}
    target_dict = {'b': 3, 'c': 4}
    
    result = resolver.resolve(
        'item-2',
        source_dict,
        target_dict,
        source_ts,
        target_ts,
        'merge'
    )
    
    assert 'a' in result and 'b' in result and 'c' in result, "Merge failed"
    print("✓ Merge resolution works")
    
    # 測試自定義策略
    def custom_strategy(source, target):
        return {'custom': True}
    
    resolver.register_custom_strategy('my-strategy', custom_strategy)
    print("✓ Custom strategy registered")
    
    # 測試統計
    stats = resolver.get_stats()
    assert stats['total_conflicts'] >= 2, "Conflict count incorrect"
    print(f"✓ Stats: {stats}")
    
    print("✅ Conflict Resolver tests passed")


def test_sync_scheduler():
    """測試同步調度器"""
    print("\n=== Test Sync Scheduler ===")
    
    executed_jobs = []
    
    def sync_callback(dataset, source, destinations):
        job_id = f"job-{len(executed_jobs)}"
        executed_jobs.append({
            'job_id': job_id,
            'dataset': dataset,
            'source': source,
            'destinations': destinations
        })
        return job_id
    
    config = {
        'scheduler': {
            'schedules': [
                {
                    'name': 'test-schedule',
                    'source': 'source-a',
                    'destinations': ['dest-b'],
                    'interval': 2,  # 2 seconds for testing
                    'enabled': True
                }
            ]
        },
        'monitoring': {
            'logging': {
                'level': 'WARNING'
            }
        }
    }
    
    scheduler = SyncScheduler(sync_callback, config)
    
    # 測試手動添加調度
    success = scheduler.add_schedule(
        'manual-schedule',
        'source-b',
        ['dest-c'],
        interval=5,
        enabled=False
    )
    
    assert success, "Failed to add schedule"
    print("✓ Schedule added manually")
    
    # 測試列出調度
    schedules = scheduler.get_schedules()
    assert len(schedules) >= 2, f"Expected at least 2 schedules, got {len(schedules)}"
    print(f"✓ Schedules listed: {len(schedules)} schedules")
    
    # 測試啟動調度器
    scheduler.start()
    print("✓ Scheduler started")
    
    # 等待調度執行
    time.sleep(3)
    
    # 檢查是否執行了調度
    assert len(executed_jobs) >= 1, f"Expected at least 1 job executed, got {len(executed_jobs)}"
    print(f"✓ Scheduled jobs executed: {len(executed_jobs)} jobs")
    
    # 測試禁用調度
    scheduler.disable_schedule('test-schedule')
    print("✓ Schedule disabled")
    
    # 停止調度器
    scheduler.stop()
    print("✓ Scheduler stopped")
    
    print("✅ Sync Scheduler tests passed")


def test_filesystem_connector():
    """測試文件系統連接器"""
    print("\n=== Test Filesystem Connector ===")
    
    config = {
        'connectors': {
            'onpremise': {
                'services': {
                    'filesystem': {
                        'base_path': '/tmp/test-data-sync'
                    }
                }
            }
        }
    }
    
    connector = FilesystemConnector(config)
    
    # 測試連接
    assert connector.connect(), "Connection failed"
    print("✓ Connected to filesystem")
    
    # 測試寫入
    test_data = {'key': 'value', 'number': 42}
    assert connector.write('test/data.json', test_data), "Write failed"
    print("✓ Data written")
    
    # 測試讀取
    read_data = connector.read('test/data.json')
    assert read_data is not None, "Read failed"
    assert read_data['key'] == 'value', "Data mismatch"
    print("✓ Data read")
    
    # 測試列表
    items = connector.list()
    assert len(items) >= 1, "List failed"
    print(f"✓ Items listed: {len(items)} items")
    
    # 測試刪除
    assert connector.delete('test/data.json'), "Delete failed"
    print("✓ Data deleted")
    
    # 測試統計
    stats = connector.get_stats()
    assert stats['connected'], "Connector should be connected"
    print(f"✓ Stats: {stats}")
    
    # 斷開連接
    connector.disconnect()
    print("✓ Disconnected")
    
    # 清理
    import shutil
    shutil.rmtree('/tmp/test-data-sync', ignore_errors=True)
    
    print("✅ Filesystem Connector tests passed")


def test_integration():
    """集成測試"""
    print("\n=== Integration Test ===")
    
    config = {
        'sync_engine': {
            'batch_size': 100
        },
        'conflict_resolution': {
            'default_strategy': 'merge'
        },
        'monitoring': {
            'logging': {
                'level': 'ERROR'
            }
        }
    }
    
    # 創建引擎和解決器
    engine = SyncEngine(config)
    resolver = ConflictResolver(config)
    
    # 模擬多平台數據同步
    # Platform A 的數據
    for i in range(10):
        engine.add_data('platform-a', f'config-{i}', {
            'id': i,
            'name': f'config_{i}',
            'platform': 'a'
        })
    
    # Platform B 的數據（部分重疊）
    for i in range(5, 15):
        engine.add_data('platform-b', f'config-{i}', {
            'id': i,
            'name': f'config_{i}',
            'platform': 'b'
        })
    
    print("✓ Test data created (Platform A: 10 items, Platform B: 10 items)")
    
    # 同步 A -> B
    job1 = engine.create_sync_job(
        'platform-config',
        'platform-a',
        ['platform-b'],
        SyncMode.MANUAL
    )
    
    engine.execute_sync_job(job1)
    status1 = engine.get_job_status(job1)
    
    print(f"✓ A->B sync completed: {status1['items_synced']} synced, {status1['conflicts']} conflicts")
    
    # 同步 B -> C
    job2 = engine.create_sync_job(
        'platform-config',
        'platform-b',
        ['platform-c'],
        SyncMode.MANUAL
    )
    
    engine.execute_sync_job(job2)
    status2 = engine.get_job_status(job2)
    
    print(f"✓ B->C sync completed: {status2['items_synced']} synced")
    
    # 驗證數據一致性
    a_items = set(engine.list_data('platform-a'))
    b_items = set(engine.list_data('platform-b'))
    c_items = set(engine.list_data('platform-c'))
    
    # B 應該包含 A 和 B 的所有數據
    assert len(b_items) >= len(a_items), "Platform B should have all A's data"
    print(f"✓ Data consistency verified (A:{len(a_items)}, B:{len(b_items)}, C:{len(c_items)})")
    
    # 測試整體統計
    stats = engine.get_stats()
    print(f"✓ Final stats: {stats}")
    
    print("✅ Integration test passed")


def main():
    """運行所有測試"""
    print("\n" + "="*60)
    print("Data Synchronization System - Test Suite")
    print("="*60)
    
    try:
        test_sync_engine()
        test_conflict_resolver()
        test_sync_scheduler()
        test_filesystem_connector()
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
