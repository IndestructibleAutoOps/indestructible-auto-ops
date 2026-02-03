#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: governance
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Dependency Manager
=====================
依賴管理器 - 依賴關係追蹤和驗證

GL Governance Layer: GL90-99 (Meta-Specification Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import logging


@dataclass
class Dependency:
    """依賴項"""
    name: str
    version: str
    required_by: str
    dependency_type: str = "runtime"  # runtime, development, optional
    compatible_versions: List[str] = field(default_factory=list)


class DependencyManager:
    """依賴管理器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化依賴管理器"""
        self.config = config or {}
        self.logger = self._setup_logger()
        
        # 依賴關係圖: {component: [Dependency]}
        self._dependencies: Dict[str, List[Dependency]] = {}
        
        # 最大依賴深度
        self.max_depth = self.config.get('max_dependency_depth', 3)
        
        self.logger.info("Dependency Manager initialized")
    
    def _setup_logger(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('DependencyManager')
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def add_dependency(
        self,
        component: str,
        dependency_name: str,
        version: str,
        dependency_type: str = "runtime"
    ) -> bool:
        """
        添加依賴
        
        Args:
            component: 組件名稱
            dependency_name: 依賴名稱
            version: 版本
            dependency_type: 依賴類型
            
        Returns:
            成功返回True
        """
        dependency = Dependency(
            name=dependency_name,
            version=version,
            required_by=component,
            dependency_type=dependency_type
        )
        
        if component not in self._dependencies:
            self._dependencies[component] = []
        
        self._dependencies[component].append(dependency)
        
        self.logger.info(
            f"Dependency added: {component} -> {dependency_name} {version}"
        )
        
        return True
    
    def get_dependencies(
        self,
        component: str,
        recursive: bool = False
    ) -> List[Dependency]:
        """
        獲取依賴列表
        
        Args:
            component: 組件名稱
            recursive: 是否遞歸獲取
            
        Returns:
            依賴列表
        """
        direct_deps = self._dependencies.get(component, [])
        
        if not recursive:
            return direct_deps
        
        # 遞歸獲取所有依賴
        all_deps = set()
        visited = set()
        
        def collect_deps(comp, depth=0):
            if comp in visited or depth > self.max_depth:
                return
            
            visited.add(comp)
            
            for dep in self._dependencies.get(comp, []):
                all_deps.add((dep.name, dep.version))
                collect_deps(dep.name, depth + 1)
        
        collect_deps(component)
        
        return [
            Dependency(name=name, version=ver, required_by=component)
            for name, ver in all_deps
        ]
    
    def detect_circular_dependencies(self) -> List[List[str]]:
        """
        檢測循環依賴
        
        Returns:
            循環依賴鏈列表
        """
        cycles = []
        
        def dfs(node, path, visited):
            if node in path:
                # 找到循環
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            
            if node in visited:
                return
            
            visited.add(node)
            path.append(node)
            
            for dep in self._dependencies.get(node, []):
                dfs(dep.name, path.copy(), visited)
        
        for component in self._dependencies.keys():
            dfs(component, [], set())
        
        return cycles
    
    def calculate_dependency_depth(self, component: str) -> int:
        """
        計算依賴深度
        
        Args:
            component: 組件名稱
            
        Returns:
            最大依賴深度
        """
        max_depth = 0
        
        def calc_depth(comp, current_depth=0):
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)
            
            if current_depth >= self.max_depth:
                return
            
            for dep in self._dependencies.get(comp, []):
                calc_depth(dep.name, current_depth + 1)
        
        calc_depth(component)
        return max_depth
    
    def validate_dependencies(self, component: str) -> Dict[str, Any]:
        """
        驗證依賴
        
        Args:
            component: 組件名稱
            
        Returns:
            驗證結果
        """
        errors = []
        warnings = []
        
        # 檢查循環依賴
        cycles = self.detect_circular_dependencies()
        if cycles:
            for cycle in cycles:
                if component in cycle:
                    errors.append(f"Circular dependency detected: {' -> '.join(cycle)}")
        
        # 檢查依賴深度
        depth = self.calculate_dependency_depth(component)
        if depth > self.max_depth:
            warnings.append(
                f"Dependency depth {depth} exceeds maximum {self.max_depth}"
            )
        
        # 檢查是否有依賴
        deps = self._dependencies.get(component, [])
        if len(deps) > 20:
            warnings.append(f"Component has {len(deps)} dependencies (consider refactoring)")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'dependency_count': len(deps),
            'dependency_depth': depth
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        total_deps = sum(len(deps) for deps in self._dependencies.values())
        
        return {
            'total_components': len(self._dependencies),
            'total_dependencies': total_deps,
            'circular_dependencies': len(self.detect_circular_dependencies())
        }
