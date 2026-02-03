#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: registry
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Data Catalog Manager
========================
數據目錄管理工具

GL Governance Layer: GL10-29 (Operational Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
# Import simple_yaml for zero-dependency YAML parsing
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.simple_yaml import safe_load
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import argparse


class DataCatalogManager:
    """數據目錄管理器"""
    
    def __init__(self, catalog_path: Optional[str] = None):
        """初始化管理器"""
        if catalog_path is None:
            catalog_path = "ecosystem/registry/data-registry/data-catalog.yaml"
        
        self.catalog_path = Path(catalog_path)
        self.catalog = self._load_catalog()
    
    def _load_catalog(self) -> Dict[str, Any]:
        """加載目錄"""
        if not self.catalog_path.exists():
            return {'datasets': []}
        
        try:
            with open(self.catalog_path, 'r') as f:
                return safe_load(f) or {'datasets': []}
        except Exception as e:
            print(f"Error loading catalog: {e}")
            return {'datasets': []}
    
    def _save_catalog(self) -> bool:
        """保存目錄"""
        try:
            self.catalog_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.catalog_path, 'w') as f:
                yaml.dump(self.catalog, f, default_flow_style=False, allow_unicode=True)
            
            return True
        except Exception as e:
            print(f"Error saving catalog: {e}")
            return False
    
    def register_dataset(
        self,
        name: str,
        description: str,
        schema: Dict[str, Any],
        owner: str,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """註冊數據集"""
        # 檢查是否已存在
        if self.get_dataset(name):
            print(f"Dataset already registered: {name}")
            return False
        
        dataset = {
            'name': name,
            'description': description,
            'schema': schema,
            'owner': owner,
            'tags': tags or [],
            'status': 'active',
            'registered_at': datetime.utcnow().isoformat(),
            'metadata': metadata or {}
        }
        
        if 'datasets' not in self.catalog:
            self.catalog['datasets'] = []
        
        self.catalog['datasets'].append(dataset)
        
        if self._save_catalog():
            print(f"✓ Dataset registered: {name}")
            return True
        else:
            return False
    
    def unregister_dataset(self, name: str) -> bool:
        """註銷數據集"""
        datasets_list = self.catalog.get('datasets', [])
        
        for i, dataset in enumerate(datasets_list):
            if dataset['name'] == name:
                datasets_list.pop(i)
                
                if self._save_catalog():
                    print(f"✓ Dataset unregistered: {name}")
                    return True
                else:
                    return False
        
        print(f"Dataset not found: {name}")
        return False
    
    def get_dataset(self, name: str) -> Optional[Dict[str, Any]]:
        """獲取數據集信息"""
        datasets_list = self.catalog.get('datasets', [])
        
        for dataset in datasets_list:
            if dataset['name'] == name:
                return dataset
        
        return None
    
    def list_datasets(
        self,
        owner: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """列出數據集"""
        datasets_list = self.catalog.get('datasets', [])
        
        results = []
        for dataset in datasets_list:
            if owner and dataset.get('owner') != owner:
                continue
            if tags:
                if not all(tag in dataset.get('tags', []) for tag in tags):
                    continue
            
            results.append(dataset)
        
        return results
    
    def validate_dataset(self, name: str) -> Dict[str, Any]:
        """驗證數據集配置"""
        dataset = self.get_dataset(name)
        
        if not dataset:
            return {
                'valid': False,
                'errors': [f"Dataset not found: {name}"]
            }
        
        errors = []
        warnings = []
        
        # 檢查必需字段
        required = ['name', 'description', 'schema', 'owner']
        for field in required:
            if field not in dataset:
                errors.append(f"Missing required field: {field}")
        
        # 檢查 schema
        if 'schema' in dataset:
            if not isinstance(dataset['schema'], dict):
                errors.append("Schema must be a dictionary")
            elif not dataset['schema']:
                warnings.append("Schema is empty")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def generate_report(self) -> str:
        """生成數據目錄報告"""
        datasets_list = self.catalog.get('datasets', [])
        
        report = []
        report.append("=" * 60)
        report.append("Data Catalog Report")
        report.append("=" * 60)
        report.append("")
        report.append(f"Total Datasets: {len(datasets_list)}")
        report.append("")
        
        # 按擁有者統計
        by_owner = {}
        for dataset in datasets_list:
            owner = dataset.get('owner', 'unknown')
            by_owner[owner] = by_owner.get(owner, 0) + 1
        
        report.append("By Owner:")
        for owner, count in by_owner.items():
            report.append(f"  - {owner}: {count}")
        report.append("")
        
        # 數據集詳情
        report.append("Datasets:")
        report.append("-" * 60)
        
        for dataset in datasets_list:
            report.append(f"\n{dataset['name']}")
            report.append(f"  Owner: {dataset.get('owner')}")
            report.append(f"  Description: {dataset.get('description')}")
            report.append(f"  Status: {dataset.get('status')}")
            
            if dataset.get('tags'):
                report.append(f"  Tags: {', '.join(dataset['tags'])}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    """命令行工具"""
    parser = argparse.ArgumentParser(description='Data Catalog Manager')
    parser.add_argument('--catalog', default='ecosystem/registry/data-registry/data-catalog.yaml')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Register
    register_parser = subparsers.add_parser('register', help='Register a dataset')
    register_parser.add_argument('--name', required=True)
    register_parser.add_argument('--description', required=True)
    register_parser.add_argument('--owner', required=True)
    register_parser.add_argument('--schema', required=True, help='JSON schema string')
    
    # List
    list_parser = subparsers.add_parser('list', help='List datasets')
    list_parser.add_argument('--owner', help='Filter by owner')
    list_parser.add_argument('--json', action='store_true')
    
    # Validate
    validate_parser = subparsers.add_parser('validate', help='Validate a dataset')
    validate_parser.add_argument('--name', required=True)
    
    # Report
    subparsers.add_parser('report', help='Generate report')
    
    args = parser.parse_args()
    
    manager = DataCatalogManager(args.catalog)
    
    if args.command == 'register':
        schema = json.loads(args.schema)
        manager.register_dataset(
            args.name, args.description, schema, args.owner
        )
    
    elif args.command == 'list':
        datasets = manager.list_datasets(args.owner)
        
        if args.json:
            print(json.dumps(datasets, indent=2))
        else:
            print(f"\nFound {len(datasets)} datasets:\n")
            for dataset in datasets:
                print(f"  - {dataset['name']} (owner: {dataset['owner']})")
            print()
    
    elif args.command == 'validate':
        result = manager.validate_dataset(args.name)
        
        print(f"\nValidation result for {args.name}:\n")
        print(f"  Valid: {result['valid']}")
        
        if result['errors']:
            print(f"\n  Errors:")
            for error in result['errors']:
                print(f"    - {error}")
        
        if result['warnings']:
            print(f"\n  Warnings:")
            for warning in result['warnings']:
                print(f"    - {warning}")
        print()
    
    elif args.command == 'report':
        print(manager.generate_report())
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
