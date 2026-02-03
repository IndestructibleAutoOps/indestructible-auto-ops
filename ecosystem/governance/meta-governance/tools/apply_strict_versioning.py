#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: version-enforcement-tool
# @GL-audit-trail: ../../GL_SEMANTIC_ANCHOR.json
#
"""
Apply Strict Versioning to Ecosystem
=====================================
將嚴格版本管理應用到整個 Ecosystem

執行：版本標註注入 → 依賴聲明 → 兼容性驗證 → 審計追蹤
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import os
import re
import json
# Import simple_yaml for zero-dependency YAML parsing
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.simple_yaml import safe_load
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ComponentVersion:
    """組件版本"""
    component_id: str
    version: str
    file_path: str
    dependencies: List[Dict] = None
    version_metadata: Dict = None


class StrictVersioningApplicator:
    """嚴格版本應用器"""
    
    COMPONENT_VERSIONS = {
        # GL10-29: Operational Layer
        'service-discovery': '1.0.0',
        'api-gateway': '1.0.0',
        'communication': '1.0.0',
        'data-synchronization': '1.0.0',
        'core-template': '1.0.0',
        'cloud-template': '1.0.0',
        'on-premise-template': '1.0.0',
        'platform-registry-manager': '1.0.0',
        'service-registry-manager': '1.0.0',
        'data-catalog-manager': '1.0.0',
        
        # GL30-49: Execution Layer
        'governance-enforcer': '1.0.0',
        'self-auditor': '1.0.0',
        'execution-hooks': '1.0.0',
        
        # GL90-99: Meta Layer
        'meta-governance': '1.0.0',
        'version-manager': '1.0.0',
        'change-manager': '1.0.0',
        'review-manager': '1.0.0',
        'dependency-manager': '1.0.0',
        'strict-version-enforcer': '1.0.0',
        'impact-analyzer': '1.0.0',
    }
    
    COMPONENT_DEPENDENCIES = {
        'api-gateway': [
            {'spec_id': 'service-discovery', 'version': '1.0.0'}
        ],
        'platform-manager': [
            {'spec_id': 'service-discovery', 'version': '1.0.0'},
            {'spec_id': 'api-gateway', 'version': '1.0.0'},
            {'spec_id': 'communication', 'version': '1.0.0'},
            {'spec_id': 'data-synchronization', 'version': '1.0.0'}
        ],
        'governance-framework': [
            {'spec_id': 'version-manager', 'version': '1.0.0'},
            {'spec_id': 'change-manager', 'version': '1.0.0'},
            {'spec_id': 'review-manager', 'version': '1.0.0'},
            {'spec_id': 'dependency-manager', 'version': '1.0.0'}
        ]
    }
    
    def __init__(self, root_dir: str = '/workspace/ecosystem'):
        self.root = Path(root_dir)
        self.components_found: List[ComponentVersion] = []
        self.version_registry: Dict[str, str] = {}
        
    def scan_and_version(self) -> Dict:
        """掃描並添加版本標註"""
        print("=" * 80)
        print("STRICT VERSIONING APPLICATION")
        print("=" * 80)
        
        # Stage 1: 掃描組件
        print("\n[Stage 1] 掃描組件...")
        self._scan_components()
        
        # Stage 2: 注入版本元數據
        print("\n[Stage 2] 注入版本元數據...")
        injected = self._inject_version_metadata()
        
        # Stage 3: 創建版本清單
        print("\n[Stage 3] 創建版本清單...")
        self._create_version_manifest()
        
        # Stage 4: 驗證版本一致性
        print("\n[Stage 4] 驗證版本一致性...")
        validation = self._validate_versions()
        
        return {
            'components_found': len(self.components_found),
            'versions_injected': injected,
            'validation': validation
        }
    
    def _scan_components(self):
        """掃描所有組件"""
        # 掃描 Python 包
        for init_file in self.root.rglob('__init__.py'):
            if 'tests' in str(init_file) or '__pycache__' in str(init_file):
                continue
            
            component_dir = init_file.parent
            component_name = self._infer_component_name(component_dir)
            
            if component_name in self.COMPONENT_VERSIONS:
                comp_ver = ComponentVersion(
                    component_id=component_name,
                    version=self.COMPONENT_VERSIONS[component_name],
                    file_path=str(init_file.relative_to(self.root))
                )
                self.components_found.append(comp_ver)
        
        print(f"  ✓ 找到 {len(self.components_found)} 個組件")
    
    def _infer_component_name(self, component_dir: Path) -> str:
        """推斷組件名稱"""
        dir_name = component_dir.name
        parent_name = component_dir.parent.name
        
        # 特殊映射
        if dir_name == 'src':
            if 'service-discovery' in str(component_dir):
                return 'service-discovery'
            elif 'api-gateway' in str(component_dir):
                return 'api-gateway'
            elif 'communication' in str(component_dir):
                return 'communication'
            elif 'data-synchronization' in str(component_dir):
                return 'data-synchronization'
            elif 'meta-governance' in str(component_dir):
                return 'meta-governance'
        
        return dir_name
    
    def _inject_version_metadata(self) -> int:
        """注入版本元數據到 __init__.py"""
        injected = 0
        
        for component in self.components_found:
            init_path = self.root / component.file_path
            
            try:
                with open(init_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 檢查是否已有 __version__
                if '__version__' in content:
                    # 更新版本
                    content = re.sub(
                        r"__version__\s*=\s*['\"][^'\"]*['\"]",
                        f"__version__ = '{component.version}'",
                        content
                    )
                else:
                    # 添加版本（在文檔字符串後）
                    lines = content.split('\n')
                    insert_pos = len(lines)
                    
                    # 找到文檔字符串結束位置
                    in_docstring = False
                    docstring_end = 0
                    for i, line in enumerate(lines):
                        if '"""' in line or "'''" in line:
                            if not in_docstring:
                                in_docstring = True
                            else:
                                docstring_end = i + 1
                                break
                    
                    if docstring_end > 0:
                        lines.insert(docstring_end, '')
                        lines.insert(docstring_end + 1, f"__version__ = '{component.version}'")
                        content = '\n'.join(lines)
                    else:
                        # 在文件開頭（GL標記後）添加
                        content += f"\n\n__version__ = '{component.version}'\n"
                
                # 寫回文件
                with open(init_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                injected += 1
                
            except Exception as e:
                print(f"  ! 錯誤處理 {component.component_id}: {e}")
        
        print(f"  ✓ 注入版本到 {injected} 個組件")
        return injected
    
    def _create_version_manifest(self):
        """創建版本清單"""
        manifest = {
            'manifest_version': '1.0.0',
            'generated_at': datetime.utcnow().isoformat(),
            'ecosystem_version': '1.0.0',
            'components': {}
        }
        
        for component in self.components_found:
            manifest['components'][component.component_id] = {
                'version': component.version,
                'location': component.file_path,
                'dependencies': self.COMPONENT_DEPENDENCIES.get(component.component_id, []),
                'release_type': 'stable',
                'published': datetime.utcnow().isoformat()
            }
        
        # 保存清單
        manifest_path = self.root / 'VERSION_MANIFEST.json'
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"  ✓ 版本清單已創建: {manifest_path}")
    
    def _validate_versions(self) -> Dict:
        """驗證版本一致性"""
        errors = []
        warnings = []
        
        # 驗證所有組件都有版本
        for component in self.components_found:
            if not component.version:
                errors.append(f"{component.component_id}: 缺少版本")
        
        # 驗證依賴版本
        for component_id, deps in self.COMPONENT_DEPENDENCIES.items():
            for dep in deps:
                if dep['spec_id'] not in self.COMPONENT_VERSIONS:
                    warnings.append(
                        f"{component_id}: 依賴未知組件 {dep['spec_id']}"
                    )
        
        result = {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
        
        print(f"  ✓ 驗證完成: {len(errors)} 錯誤, {len(warnings)} 警告")
        
        return result


def main():
    """主函數"""
    applicator = StrictVersioningApplicator()
    result = applicator.scan_and_version()
    
    print("\n" + "=" * 80)
    print("✅ STRICT VERSIONING APPLIED")
    print("=" * 80)
    print(f"\n組件: {result['components_found']}")
    print(f"版本注入: {result['versions_injected']}")
    print(f"驗證: {'通過' if result['validation']['valid'] else '失敗'}")
    print("")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
