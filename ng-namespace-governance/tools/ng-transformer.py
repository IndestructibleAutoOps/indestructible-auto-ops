#!/usr/bin/env python3
"""
NG 命名空間轉換引擎
NG Namespace Transformer Engine

用途：執行完整的 Era 間轉換（包含元數據、依賴、配置）
模式：BINARY_EXECUTION
"""

import sys
import json
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict
from enum import Enum


class TransformationType(Enum):
    """轉換類型"""
    ERA1_TO_ERA2 = "era1_to_era2"
    ERA2_TO_ERA3 = "era2_to_era3"
    ERA1_TO_ERA3 = "era1_to_era3"  # 直接映射


@dataclass
class NamespaceTransformation:
    """命名空間轉換"""
    source_namespace: str
    target_namespace: str
    source_era: str
    target_era: str
    transformation_type: str
    metadata_transformed: Dict
    dependencies_mapped: List[str]
    config_migrated: Dict


class NgTransformer:
    """NG 命名空間轉換引擎"""
    
    def __init__(self):
        """初始化轉換引擎"""
        self.transformation_history = []
        print("🔄 NG 轉換引擎已初始化")
    
    def transform(
        self,
        source_namespace: str,
        target_era: str,
        metadata: Dict = None
    ) -> Dict[str, any]:
        """
        執行完整轉換（二元執行）
        
        Returns:
            {'result': 'pass', 'transformation': {...}} 或
            {'result': 'block', 'reason': '...'}
        """
        # 步驟 1: 命名空間映射
        import importlib.util
        
        mapper_path = Path(__file__).parent / 'ng-mapper.py'
        spec = importlib.util.spec_from_file_location("ng_mapper", mapper_path)
        ng_mapper_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ng_mapper_module)
        
        NgMapper = ng_mapper_module.NgMapper
        Era = ng_mapper_module.Era
        
        mapper = NgMapper()
        era_enum = Era[f"ERA_{target_era[-1]}"] if target_era.startswith('era') else Era.CROSS
        
        mapping_result = mapper.map_namespace(source_namespace, era_enum)
        
        if mapping_result['result'] == 'block':
            return mapping_result  # 直接返回 BLOCK
        
        target_namespace = mapping_result['target_namespace']
        
        # 步驟 2: 元數據轉換
        metadata_result = self._transform_metadata(
            metadata or {},
            source_namespace,
            target_namespace
        )
        
        if metadata_result['result'] == 'block':
            return metadata_result
        
        # 步驟 3: 依賴映射
        dependencies_result = self._map_dependencies(
            metadata.get('dependencies', []) if metadata else [],
            target_era
        )
        
        if dependencies_result['result'] == 'block':
            return dependencies_result
        
        # 步驟 4: 配置遷移
        config_result = self._migrate_config(
            metadata.get('config', {}) if metadata else {},
            target_era
        )
        
        if config_result['result'] == 'block':
            return config_result
        
        # 創建轉換記錄
        transformation = NamespaceTransformation(
            source_namespace=source_namespace,
            target_namespace=target_namespace,
            source_era=mapping_result['source_era'],
            target_era=target_era,
            transformation_type=mapping_result['transformation'],
            metadata_transformed=metadata_result['transformed_metadata'],
            dependencies_mapped=dependencies_result['mapped_dependencies'],
            config_migrated=config_result['migrated_config']
        )
        
        self.transformation_history.append(transformation)
        
        # 所有步驟通過（二元結果：PASS）
        return {
            'result': 'pass',
            'transformation': asdict(transformation),
            'rule_code': 'NG90102',
            'steps_completed': [
                'namespace_mapping',
                'metadata_transformation',
                'dependencies_mapping',
                'config_migration'
            ]
        }
    
    def _transform_metadata(
        self,
        source_metadata: Dict,
        source_ns: str,
        target_ns: str
    ) -> Dict[str, any]:
        """轉換元數據（二元執行）"""
        transformed = source_metadata.copy()
        
        # 更新命名空間引用
        transformed['namespace'] = target_ns
        transformed['source_namespace'] = source_ns
        transformed['transformation_timestamp'] = '動態生成'
        
        return {
            'result': 'pass',
            'transformed_metadata': transformed
        }
    
    def _map_dependencies(
        self,
        dependencies: List[str],
        target_era: str
    ) -> Dict[str, any]:
        """映射依賴（二元執行）"""
        # 依賴也需要映射到目標 Era
        mapped_deps = []
        
        for dep in dependencies:
            # 簡化：假設依賴格式正確
            if '.era1.' in dep:
                mapped = dep.replace('.era1.', f'.{target_era}.')
            elif '.era2.' in dep:
                mapped = dep.replace('.era2.', f'.{target_era}.')
            else:
                mapped = dep
            
            mapped_deps.append(mapped)
        
        return {
            'result': 'pass',
            'mapped_dependencies': mapped_deps
        }
    
    def _migrate_config(
        self,
        config: Dict,
        target_era: str
    ) -> Dict[str, any]:
        """遷移配置（二元執行）"""
        migrated = config.copy()
        
        # Era-2 配置可能需要環境變數化
        if target_era == 'era2':
            # 將硬編碼配置改為環境變數引用
            for key in migrated:
                if isinstance(migrated[key], str) and not migrated[key].startswith('${'):
                    migrated[key] = f"${{ENV_{key.upper()}}}"
        
        return {
            'result': 'pass',
            'migrated_config': migrated
        }


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("NG 命名空間轉換引擎測試")
    print("=" * 70)
    
    transformer = NgTransformer()
    
    # 測試完整轉換
    print("\n測試: Era-1 → Era-2 完整轉換")
    print("-" * 70)
    
    result = transformer.transform(
        source_namespace="pkg.era1.platform.core",
        target_era="era2",
        metadata={
            'owner': 'platform-team',
            'dependencies': [
                'mod.era1.runtime.executor',
                'cls.era1.registry.manager'
            ],
            'config': {
                'timeout': '30s',
                'max_workers': '10'
            }
        }
    )
    
    print(f"結果: {result['result'].upper()}")
    
    if result['result'] == 'pass':
        trans = result['transformation']
        print(f"\n✅ 轉換成功:")
        print(f"   源: {trans['source_namespace']}")
        print(f"   目標: {trans['target_namespace']}")
        print(f"   類型: {trans['transformation_type']}")
        print(f"\n   依賴映射:")
        for dep in trans['dependencies_mapped']:
            print(f"     - {dep}")
        print(f"\n   配置遷移:")
        for k, v in trans['config_migrated'].items():
            print(f"     {k}: {v}")
    else:
        print(f"🚫 轉換失敗:")
        print(f"   原因: {result['reason']}")
    
    print("\n" + "=" * 70)
    print("✅ NG 轉換引擎測試完成")
    print("   所有轉換都是二元結果（PASS 或 BLOCK）")
    print("=" * 70)
