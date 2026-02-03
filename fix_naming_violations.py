#!/usr/bin/env python3
"""
MNGA 命名違規自動修復腳本
自動修復文件和目錄命名問題
"""

import os
import re
import json
import shutil
from pathlib import Path
from typing import List, Dict, Set, Tuple
from datetime import datetime

class NamingFixer:
    def __init__(self, workspace: Path, dry_run: bool = True):
        self.workspace = workspace
        self.dry_run = dry_run
        self.fixed_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        self.rename_map: Dict[str, str] = {}  # old_path -> new_path
        
        # 排除目錄
        self.excluded_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            '.idea', '.vscode', 'outputs', '.governance'
        }
        
        # 需要更新引用的文件類型
        self.reference_file_types = {'.py', '.yaml', '.yml', '.json', '.md', '.sh', '.ts', '.js'}
    
    def to_snake_case(self, name: str) -> str:
        """轉換為 snake_case"""
        # 處理擴展名
        if '.' in name:
            stem, ext = name.rsplit('.', 1)
            return self._convert_to_snake(stem) + '.' + ext
        return self._convert_to_snake(name)
    
    def _convert_to_snake(self, s: str) -> str:
        """內部轉換函數"""
        # 將連字符轉為下劃線
        s = s.replace('-', '_')
        # 將駝峰轉為下劃線
        s = re.sub(r'([a-z])([A-Z])', r'\1_\2', s)
        return s.lower()
    
    def to_kebab_case(self, name: str) -> str:
        """轉換為 kebab-case"""
        if '.' in name:
            stem, ext = name.rsplit('.', 1)
            return self._convert_to_kebab(stem) + '.' + ext
        return self._convert_to_kebab(name)
    
    def _convert_to_kebab(self, s: str) -> str:
        """內部轉換函數"""
        # 將下劃線轉為連字符
        s = s.replace('_', '-')
        # 將駝峰轉為連字符
        s = re.sub(r'([a-z])([A-Z])', r'\1-\2', s)
        return s.lower()
    
    def should_skip(self, path: Path) -> bool:
        """檢查是否應跳過"""
        for part in path.parts:
            if part in self.excluded_dirs:
                return True
            if part.startswith('.') and part not in {'.github', '.governance'}:
                return True
        return False
    
    def is_python_package(self, dir_path: Path) -> bool:
        """檢查是否是 Python 包"""
        return (dir_path / '__init__.py').exists()
    
    def collect_python_file_renames(self) -> List[Tuple[Path, Path]]:
        """收集需要重命名的 Python 文件"""
        renames = []
        
        for file_path in self.workspace.rglob('*.py'):
            if self.should_skip(file_path):
                continue
            
            name = file_path.name
            stem = file_path.stem
            
            # 跳過特殊文件
            if name.startswith('__') and name.endswith('__.py'):
                continue
            
            # 檢查是否使用連字符
            if '-' in stem:
                new_name = self.to_snake_case(name)
                new_path = file_path.parent / new_name
                if new_path != file_path:
                    renames.append((file_path, new_path))
        
        return renames
    
    def collect_config_file_renames(self) -> List[Tuple[Path, Path]]:
        """收集需要重命名的配置文件"""
        renames = []
        
        for ext in ['.yaml', '.yml', '.json', '.toml']:
            for file_path in self.workspace.rglob(f'*{ext}'):
                if self.should_skip(file_path):
                    continue
                
                name = file_path.name
                stem = file_path.stem
                
                # 跳過特殊文件
                if name in {'package.json', 'package-lock.json', 'tsconfig.json'}:
                    continue
                # 跳過 GL 語義文件
                if stem.startswith('GL') and re.match(r'^GL\d{2}', stem):
                    continue
                
                # 檢查是否使用下劃線
                if '_' in stem:
                    new_name = self.to_kebab_case(name)
                    new_path = file_path.parent / new_name
                    if new_path != file_path:
                        renames.append((file_path, new_path))
        
        return renames
    
    def collect_directory_renames(self) -> List[Tuple[Path, Path]]:
        """收集需要重命名的目錄"""
        renames = []
        
        # 收集所有目錄，按深度排序（深的先處理）
        dirs = []
        for dir_path in self.workspace.rglob('*'):
            if not dir_path.is_dir():
                continue
            if self.should_skip(dir_path):
                continue
            dirs.append(dir_path)
        
        # 按深度排序（深的先處理）
        dirs.sort(key=lambda p: len(p.parts), reverse=True)
        
        for dir_path in dirs:
            name = dir_path.name
            
            # 跳過 Python 包
            if self.is_python_package(dir_path):
                continue
            
            # 跳過特殊目錄
            if name.startswith('.') or name.startswith('__'):
                continue
            
            # 跳過 GitHub 標準目錄
            if name in {'PULL_REQUEST_TEMPLATE', 'ISSUE_TEMPLATE'}:
                continue
            
            # 檢查是否使用下劃線
            if '_' in name and not name.startswith('_'):
                new_name = self.to_kebab_case(name)
                new_path = dir_path.parent / new_name
                if new_path != dir_path and not new_path.exists():
                    renames.append((dir_path, new_path))
        
        return renames
    
    def update_references(self, old_name: str, new_name: str):
        """更新文件中的引用"""
        if self.dry_run:
            return
        
        # 只更新 Python import 語句
        old_module = old_name.replace('.py', '').replace('-', '_')
        new_module = new_name.replace('.py', '')
        
        if old_module == new_module:
            return
        
        for ext in self.reference_file_types:
            for file_path in self.workspace.rglob(f'*{ext}'):
                if self.should_skip(file_path):
                    continue
                
                try:
                    content = file_path.read_text(encoding='utf-8')
                    
                    # 檢查是否包含舊名稱的引用
                    if old_module in content or old_name in content:
                        # 更新 import 語句
                        new_content = content.replace(f'import {old_module}', f'import {new_module}')
                        new_content = new_content.replace(f'from {old_module}', f'from {new_module}')
                        new_content = new_content.replace(f'"{old_name}"', f'"{new_name}"')
                        new_content = new_content.replace(f"'{old_name}'", f"'{new_name}'")
                        
                        if new_content != content:
                            file_path.write_text(new_content, encoding='utf-8')
                except (UnicodeDecodeError, PermissionError):
                    pass
    
    def rename_file(self, old_path: Path, new_path: Path) -> bool:
        """重命名文件"""
        try:
            if self.dry_run:
                print(f"  [DRY-RUN] {old_path.relative_to(self.workspace)} -> {new_path.name}")
                return True
            
            # 使用 git mv 如果在 git 倉庫中
            if (self.workspace / '.git').exists():
                import subprocess
                result = subprocess.run(
                    ['git', 'mv', str(old_path), str(new_path)],
                    cwd=self.workspace,
                    capture_output=True
                )
                if result.returncode != 0:
                    # 如果 git mv 失敗，使用普通 mv
                    shutil.move(str(old_path), str(new_path))
            else:
                shutil.move(str(old_path), str(new_path))
            
            # 記錄重命名
            self.rename_map[str(old_path.relative_to(self.workspace))] = str(new_path.relative_to(self.workspace))
            
            # 更新引用
            self.update_references(old_path.name, new_path.name)
            
            print(f"  ✓ {old_path.relative_to(self.workspace)} -> {new_path.name}")
            return True
            
        except Exception as e:
            print(f"  ✗ {old_path.relative_to(self.workspace)}: {e}")
            return False
    
    def rename_directory(self, old_path: Path, new_path: Path) -> bool:
        """重命名目錄"""
        try:
            if self.dry_run:
                print(f"  [DRY-RUN] {old_path.relative_to(self.workspace)}/ -> {new_path.name}/")
                return True
            
            # 使用 git mv 如果在 git 倉庫中
            if (self.workspace / '.git').exists():
                import subprocess
                result = subprocess.run(
                    ['git', 'mv', str(old_path), str(new_path)],
                    cwd=self.workspace,
                    capture_output=True
                )
                if result.returncode != 0:
                    shutil.move(str(old_path), str(new_path))
            else:
                shutil.move(str(old_path), str(new_path))
            
            print(f"  ✓ {old_path.relative_to(self.workspace)}/ -> {new_path.name}/")
            return True
            
        except Exception as e:
            print(f"  ✗ {old_path.relative_to(self.workspace)}/: {e}")
            return False
    
    def run(self):
        """執行修復"""
        print(f"\n{'='*70}")
        print(f"{'MNGA 命名違規自動修復':^70}")
        print(f"{'='*70}")
        print(f"\n模式: {'DRY-RUN (預覽)' if self.dry_run else 'APPLY (實際修改)'}")
        print(f"工作區: {self.workspace}\n")
        
        # 1. 修復 Python 文件命名
        print("\n📁 Python 文件命名修復 (連字符 -> 下劃線):")
        print("-" * 50)
        py_renames = self.collect_python_file_renames()
        for old_path, new_path in py_renames:
            if self.rename_file(old_path, new_path):
                self.fixed_count += 1
            else:
                self.failed_count += 1
        print(f"  共 {len(py_renames)} 個文件")
        
        # 2. 修復配置文件命名
        print("\n📄 配置文件命名修復 (下劃線 -> 連字符):")
        print("-" * 50)
        config_renames = self.collect_config_file_renames()
        for old_path, new_path in config_renames:
            if self.rename_file(old_path, new_path):
                self.fixed_count += 1
            else:
                self.failed_count += 1
        print(f"  共 {len(config_renames)} 個文件")
        
        # 3. 修復目錄命名
        print("\n📂 目錄命名修復 (下劃線 -> 連字符):")
        print("-" * 50)
        dir_renames = self.collect_directory_renames()
        for old_path, new_path in dir_renames:
            if self.rename_directory(old_path, new_path):
                self.fixed_count += 1
            else:
                self.failed_count += 1
        print(f"  共 {len(dir_renames)} 個目錄")
        
        # 總結
        print(f"\n{'='*70}")
        print("修復總結:")
        print(f"  ✓ 成功: {self.fixed_count}")
        print(f"  ✗ 失敗: {self.failed_count}")
        print(f"  ⊘ 跳過: {self.skipped_count}")
        
        if self.dry_run:
            print(f"\n⚠️  這是預覽模式，沒有實際修改文件")
            print(f"   使用 --apply 參數來實際執行修復")
        
        # 保存重命名映射
        if not self.dry_run and self.rename_map:
            map_file = self.workspace / 'reports' / 'naming-fix-map.json'
            map_file.parent.mkdir(parents=True, exist_ok=True)
            with open(map_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'renames': self.rename_map
                }, f, indent=2, ensure_ascii=False)
            print(f"\n重命名映射已保存至: {map_file}")
        
        return self.failed_count == 0


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='MNGA 命名違規自動修復')
    parser.add_argument('--workspace', '-w', default='.', help='工作區路徑')
    parser.add_argument('--apply', action='store_true', help='實際執行修復（默認為預覽模式）')
    
    args = parser.parse_args()
    
    workspace = Path(args.workspace).resolve()
    fixer = NamingFixer(workspace, dry_run=not args.apply)
    
    success = fixer.run()
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
