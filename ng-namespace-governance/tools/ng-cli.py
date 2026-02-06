#!/usr/bin/env python3
"""
NG Command Line Interface
命名空間治理命令行工具

Usage:
    python ng-cli.py register --namespace pkg.era1.platform.core --owner team-a
    python ng-cli.py list --era era-1
    python ng-cli.py validate --namespace pkg.era1.platform.core
    python ng-cli.py stats
"""

import sys
import argparse
from pathlib import Path

# Add registry to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from registry.namespace_registry import (
    NgNamespaceRegistry,
    NamespaceSpec,
    Era,
    NamespaceStatus
)


class NgCli:
    """NG 命令行介面"""
    
    def __init__(self):
        self.registry = NgNamespaceRegistry("registry/namespaces.json")
    
    def register(self, namespace: str, owner: str, description: str = ""):
        """註冊命名空間"""
        print(f"🔍 註冊命名空間: {namespace}")
        
        # 解析命名空間
        parts = namespace.split('.')
        if len(parts) < 4:
            print("❌ 無效的命名空間格式")
            print("   格式: {type}.{era}.{domain}.{component}")
            return False
        
        ns_type, era_str, domain, component = parts[:4]
        
        # 映射 Era
        era_map = {
            'era1': Era.ERA_1,
            'era2': Era.ERA_2,
            'era3': Era.ERA_3,
            'cross': Era.CROSS
        }
        era = era_map.get(era_str)
        
        if not era:
            print(f"❌ 無效的 Era: {era_str}")
            return False
        
        # 創建規範
        spec = NamespaceSpec(
            namespace_id=namespace,
            namespace_type=ns_type,
            era=era,
            domain=domain,
            component=component,
            owner=owner,
            description=description or f"{component} namespace"
        )
        
        try:
            ns_id = self.registry.register_namespace(spec)
            
            record = self.registry.get_namespace(ns_id)
            print(f"\n✅ 註冊成功！")
            print(f"   ID: {ns_id}")
            print(f"   NG Code: {record.ng_code}")
            print(f"   Era: {era.value}")
            
            return True
            
        except Exception as e:
            print(f"❌ 註冊失敗: {e}")
            return False
    
    def list_namespaces(self, era: str = None, status: str = None, domain: str = None):
        """列出命名空間"""
        print("📋 命名空間列表\n")
        
        # 映射參數
        era_obj = None
        if era:
            era_map = {
                'era1': Era.ERA_1,
                'era2': Era.ERA_2,
                'era3': Era.ERA_3,
                'cross': Era.CROSS
            }
            era_obj = era_map.get(era.lower())
        
        status_obj = None
        if status:
            try:
                status_obj = NamespaceStatus(status.lower())
            except ValueError:
                pass
        
        # 查詢
        results = self.registry.list_namespaces(
            era=era_obj,
            status=status_obj,
            domain=domain
        )
        
        if not results:
            print("沒有找到符合條件的命名空間")
            return
        
        # 顯示結果
        print(f"找到 {len(results)} 個命名空間:\n")
        
        for i, record in enumerate(results, 1):
            print(f"{i}. {record.spec.namespace_id}")
            print(f"   NG Code: {record.ng_code}")
            print(f"   Era: {record.spec.era.value}")
            print(f"   Domain: {record.spec.domain}")
            print(f"   Status: {record.status.value}")
            print(f"   Owner: {record.spec.owner}")
            print()
    
    def validate(self, namespace: str):
        """驗證命名空間"""
        print(f"🔍 驗證命名空間: {namespace}\n")
        
        record = self.registry.get_namespace(namespace)
        
        if not record:
            print("❌ 命名空間不存在")
            return False
        
        print("✅ 命名空間存在")
        print(f"   NG Code: {record.ng_code}")
        print(f"   Status: {record.status.value}")
        print(f"   Created: {record.created_at}")
        print(f"   Updated: {record.updated_at}")
        
        # 驗證格式
        parts = namespace.split('.')
        if len(parts) >= 4:
            print("\n✅ 格式驗證通過")
            print(f"   Type: {parts[0]}")
            print(f"   Era: {parts[1]}")
            print(f"   Domain: {parts[2]}")
            print(f"   Component: {parts[3]}")
        else:
            print("\n⚠️  格式不完整")
        
        return True
    
    def stats(self):
        """顯示統計資訊"""
        print("📊 NG 命名空間統計\n")
        
        stats = self.registry.get_statistics()
        
        print(f"總命名空間數: {stats['total']}\n")
        
        print("按 Era 分布:")
        for era, count in stats['by_era'].items():
            print(f"  {era}: {count}")
        
        print("\n按狀態分布:")
        for status, count in stats['by_status'].items():
            print(f"  {status}: {count}")
        
        print("\n按領域分布:")
        for domain, count in stats['by_domain'].items():
            print(f"  {domain}: {count}")


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="NG Namespace Governance CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # register 命令
    register_parser = subparsers.add_parser('register', help='註冊命名空間')
    register_parser.add_argument('--namespace', required=True, help='命名空間 ID')
    register_parser.add_argument('--owner', required=True, help='擁有者')
    register_parser.add_argument('--description', default='', help='描述')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出命名空間')
    list_parser.add_argument('--era', choices=['era1', 'era2', 'era3', 'cross'], help='篩選 Era')
    list_parser.add_argument('--status', help='篩選狀態')
    list_parser.add_argument('--domain', help='篩選領域')
    
    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='驗證命名空間')
    validate_parser.add_argument('--namespace', required=True, help='命名空間 ID')
    
    # stats 命令
    stats_parser = subparsers.add_parser('stats', help='顯示統計資訊')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = NgCli()
    
    if args.command == 'register':
        cli.register(args.namespace, args.owner, args.description)
    
    elif args.command == 'list':
        cli.list_namespaces(args.era, args.status, args.domain)
    
    elif args.command == 'validate':
        cli.validate(args.namespace)
    
    elif args.command == 'stats':
        cli.stats()


if __name__ == "__main__":
    main()
