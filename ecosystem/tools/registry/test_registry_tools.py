#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: registry
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
Registry Tools Tests
====================
測試註冊表管理工具
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from platform_registry_manager import PlatformRegistryManager
from service_registry_manager import ServiceRegistryManager
from data_catalog_manager import DataCatalogManager


def test_platform_registry_manager():
    """測試平台註冊表管理器"""
    print("\n=== Test Platform Registry Manager ===")
    
    # 使用臨時文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        temp_file = f.name
    
    try:
        manager = PlatformRegistryManager(temp_file)
        
        # 註冊平台
        success = manager.register_platform(
            name='gl.test.example-platform',
            platform_type='core',
            version='1.0.0',
            capabilities=['service-discovery', 'api-gateway']
        )
        
        assert success, "Platform registration failed"
        print("✓ Platform registered")
        
        # 獲取平台
        platform = manager.get_platform('gl.test.example-platform')
        assert platform is not None, "Platform not found"
        assert platform['type'] == 'core', "Platform type mismatch"
        print("✓ Platform retrieved")
        
        # 列出平台
        platforms = manager.list_platforms()
        assert len(platforms) == 1, "Platform list incorrect"
        print("✓ Platform listed")
        
        # 驗證平台
        result = manager.validate_platform('gl.test.example-platform')
        assert result['valid'], f"Validation failed: {result['errors']}"
        print("✓ Platform validated")
        
        # 更新狀態
        success = manager.update_platform_status('gl.test.example-platform', 'inactive')
        assert success, "Status update failed"
        print("✓ Platform status updated")
        
        # 生成報告
        report = manager.generate_report()
        assert 'Total Platforms: 1' in report, "Report incorrect"
        print("✓ Report generated")
        
        # 註銷平台
        success = manager.unregister_platform('gl.test.example-platform')
        assert success, "Platform unregistration failed"
        print("✓ Platform unregistered")
        
        print("✅ Platform Registry Manager tests passed")
        
    finally:
        Path(temp_file).unlink(missing_ok=True)


def test_service_registry_manager():
    """測試服務註冊表管理器"""
    print("\n=== Test Service Registry Manager ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        temp_file = f.name
    
    try:
        manager = ServiceRegistryManager(temp_file)
        
        # 註冊服務
        success = manager.register_service(
            name='test-service',
            platform='test-platform',
            service_type='api',
            endpoint='http://localhost:8080',
            version='1.0.0',
            tags=['test']
        )
        
        assert success, "Service registration failed"
        print("✓ Service registered")
        
        # 獲取服務
        service = manager.get_service('test-platform-test-service')
        assert service is not None, "Service not found"
        print("✓ Service retrieved")
        
        # 列出服務
        services = manager.list_services(platform='test-platform')
        assert len(services) == 1, "Service list incorrect"
        print("✓ Services listed")
        
        # 更新狀態
        success = manager.update_service_status('test-platform-test-service', 'inactive')
        assert success, "Status update failed"
        print("✓ Service status updated")
        
        # 生成報告
        report = manager.generate_report()
        assert 'Total Services: 1' in report, "Report incorrect"
        print("✓ Report generated")
        
        print("✅ Service Registry Manager tests passed")
        
    finally:
        Path(temp_file).unlink(missing_ok=True)


def test_data_catalog_manager():
    """測試數據目錄管理器"""
    print("\n=== Test Data Catalog Manager ===")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        temp_file = f.name
    
    try:
        manager = DataCatalogManager(temp_file)
        
        # 註冊數據集
        success = manager.register_dataset(
            name='test-dataset',
            description='Test dataset for validation',
            schema={'type': 'object', 'properties': {'id': {'type': 'integer'}}},
            owner='test-owner',
            tags=['test', 'example']
        )
        
        assert success, "Dataset registration failed"
        print("✓ Dataset registered")
        
        # 獲取數據集
        dataset = manager.get_dataset('test-dataset')
        assert dataset is not None, "Dataset not found"
        assert dataset['owner'] == 'test-owner', "Owner mismatch"
        print("✓ Dataset retrieved")
        
        # 列出數據集
        datasets = manager.list_datasets(owner='test-owner')
        assert len(datasets) == 1, "Dataset list incorrect"
        print("✓ Datasets listed")
        
        # 驗證數據集
        result = manager.validate_dataset('test-dataset')
        assert result['valid'], f"Validation failed: {result['errors']}"
        print("✓ Dataset validated")
        
        # 生成報告
        report = manager.generate_report()
        assert 'Total Datasets: 1' in report, "Report incorrect"
        print("✓ Report generated")
        
        print("✅ Data Catalog Manager tests passed")
        
    finally:
        Path(temp_file).unlink(missing_ok=True)


def main():
    """運行所有測試"""
    print("\n" + "="*60)
    print("Registry Tools - Test Suite")
    print("="*60)
    
    try:
        test_platform_registry_manager()
        test_service_registry_manager()
        test_data_catalog_manager()
        
        print("\n" + "="*60)
        print("✅ ALL REGISTRY TOOLS TESTS PASSED")
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
