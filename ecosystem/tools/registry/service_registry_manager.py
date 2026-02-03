#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: registry
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Service Registry Manager
============================
服務註冊表管理工具

GL Governance Layer: GL10-29 (Operational Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import argparse


class ServiceRegistryManager:
    """服務註冊表管理器"""
    
    def __init__(self, registry_path: Optional[str] = None):
        """
        初始化管理器
        
        Args:
            registry_path: 註冊表文件路徑
        """
        if registry_path is None:
            registry_path = "ecosystem/registry/service-registry/service-catalog.yaml"
        
        self.registry_path = Path(registry_path)
        self.services = self._load_registry()
    
    def _load_registry(self) -> Dict[str, Any]:
        """加載註冊表"""
        if not self.registry_path.exists():
            return {'services': []}
        
        try:
            with open(self.registry_path, 'r') as f:
                data = yaml.safe_load(f)
                return data or {'services': []}
        except Exception as e:
            print(f"Error loading registry: {e}")
            return {'services': []}
    
    def _save_registry(self) -> bool:
        """保存註冊表"""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.registry_path, 'w') as f:
                yaml.dump(self.services, f, default_flow_style=False, allow_unicode=True)
            
            return True
        except Exception as e:
            print(f"Error saving registry: {e}")
            return False
    
    def register_service(
        self,
        name: str,
        platform: str,
        service_type: str,
        endpoint: str,
        version: str = "1.0.0",
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        註冊服務
        
        Args:
            name: 服務名稱
            platform: 平台名稱
            service_type: 服務類型
            endpoint: 服務端點
            version: 版本
            tags: 標籤
            metadata: 元數據
            
        Returns:
            成功返回True
        """
        # 生成服務ID
        service_id = f"{platform}-{name}"
        
        # 檢查是否已存在
        if self.get_service(service_id):
            print(f"Service already registered: {service_id}")
            return False
        
        # 創建服務條目
        service = {
            'id': service_id,
            'name': name,
            'platform': platform,
            'type': service_type,
            'endpoint': endpoint,
            'version': version,
            'status': 'active',
            'registered_at': datetime.utcnow().isoformat(),
            'tags': tags or [],
            'metadata': metadata or {}
        }
        
        # 添加到註冊表
        if 'services' not in self.services:
            self.services['services'] = []
        
        self.services['services'].append(service)
        
        # 保存
        if self._save_registry():
            print(f"✓ Service registered: {service_id}")
            return True
        else:
            return False
    
    def unregister_service(self, service_id: str) -> bool:
        """註銷服務"""
        services_list = self.services.get('services', [])
        
        for i, service in enumerate(services_list):
            if service['id'] == service_id:
                services_list.pop(i)
                
                if self._save_registry():
                    print(f"✓ Service unregistered: {service_id}")
                    return True
                else:
                    return False
        
        print(f"Service not found: {service_id}")
        return False
    
    def get_service(self, service_id: str) -> Optional[Dict[str, Any]]:
        """獲取服務信息"""
        services_list = self.services.get('services', [])
        
        for service in services_list:
            if service['id'] == service_id:
                return service
        
        return None
    
    def list_services(
        self,
        platform: Optional[str] = None,
        service_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """列出服務"""
        services_list = self.services.get('services', [])
        
        results = []
        for service in services_list:
            if platform and service.get('platform') != platform:
                continue
            if service_type and service.get('type') != service_type:
                continue
            if status and service.get('status') != status:
                continue
            
            results.append(service)
        
        return results
    
    def update_service_status(self, service_id: str, status: str) -> bool:
        """更新服務狀態"""
        services_list = self.services.get('services', [])
        
        for service in services_list:
            if service['id'] == service_id:
                service['status'] = status
                service['updated_at'] = datetime.utcnow().isoformat()
                
                if self._save_registry():
                    print(f"✓ Service status updated: {service_id} -> {status}")
                    return True
                else:
                    return False
        
        print(f"Service not found: {service_id}")
        return False
    
    def generate_report(self) -> str:
        """生成服務註冊表報告"""
        services_list = self.services.get('services', [])
        
        report = []
        report.append("=" * 60)
        report.append("Service Registry Report")
        report.append("=" * 60)
        report.append("")
        
        # 統計
        total = len(services_list)
        by_type = {}
        by_platform = {}
        by_status = {}
        
        for service in services_list:
            stype = service.get('type', 'unknown')
            platform = service.get('platform', 'unknown')
            status = service.get('status', 'unknown')
            
            by_type[stype] = by_type.get(stype, 0) + 1
            by_platform[platform] = by_platform.get(platform, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1
        
        report.append(f"Total Services: {total}")
        report.append("")
        
        report.append("By Type:")
        for stype, count in by_type.items():
            report.append(f"  - {stype}: {count}")
        report.append("")
        
        report.append("By Platform:")
        for platform, count in by_platform.items():
            report.append(f"  - {platform}: {count}")
        report.append("")
        
        report.append("By Status:")
        for status, count in by_status.items():
            report.append(f"  - {status}: {count}")
        report.append("")
        
        return "\n".join(report)


def main():
    """命令行工具"""
    parser = argparse.ArgumentParser(description='Service Registry Manager')
    parser.add_argument('--registry', default='ecosystem/registry/service-registry/service-catalog.yaml')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Register
    register_parser = subparsers.add_parser('register', help='Register a service')
    register_parser.add_argument('--name', required=True)
    register_parser.add_argument('--platform', required=True)
    register_parser.add_argument('--type', required=True)
    register_parser.add_argument('--endpoint', required=True)
    register_parser.add_argument('--version', default='1.0.0')
    
    # Unregister
    unregister_parser = subparsers.add_parser('unregister', help='Unregister a service')
    unregister_parser.add_argument('--id', required=True)
    
    # List
    list_parser = subparsers.add_parser('list', help='List services')
    list_parser.add_argument('--platform', help='Filter by platform')
    list_parser.add_argument('--type', help='Filter by type')
    list_parser.add_argument('--json', action='store_true')
    
    # Report
    subparsers.add_parser('report', help='Generate report')
    
    args = parser.parse_args()
    
    manager = ServiceRegistryManager(args.registry)
    
    if args.command == 'register':
        manager.register_service(
            args.name, args.platform, args.type,
            args.endpoint, args.version
        )
    
    elif args.command == 'unregister':
        manager.unregister_service(args.id)
    
    elif args.command == 'list':
        services = manager.list_services(args.platform, args.type)
        
        if args.json:
            print(json.dumps(services, indent=2))
        else:
            print(f"\nFound {len(services)} services:\n")
            for service in services:
                print(f"  - {service['id']} ({service['type']}) @ {service['endpoint']}")
            print()
    
    elif args.command == 'report':
        print(manager.generate_report())
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
