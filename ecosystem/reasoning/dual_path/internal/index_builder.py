#!/usr/bin/env python3
"""
索引構建工具
Index Builder Tool

@GL-governed
@GL-layer: GL30-39
@GL-semantic: reasoning-indexing

用於構建和維護內部檢索索引：
- 代碼向量索引
- 文檔全文索引
- 知識圖譜索引
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone


@dataclass
class IndexEntry:
    """索引條目"""
    id: str
    content: str
    content_type: str  # code, doc, config
    file_path: str
    line_start: int
    line_end: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class IndexStats:
    """索引統計"""
    total_entries: int = 0
    code_entries: int = 0
    doc_entries: int = 0
    config_entries: int = 0
    last_updated: str = ""
    index_size_bytes: int = 0


class IndexBuilder:
    """
    索引構建器
    
    負責：
    1. 掃描代碼庫
    2. 提取可索引內容
    3. 生成向量嵌入
    4. 構建和更新索引
    """
    
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.index_dir = self.workspace / "ecosystem" / "indexes" / "internal"
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        # 索引文件路徑
        self.code_index_path = self.index_dir / "code_vectors" / "index.json"
        self.docs_index_path = self.index_dir / "docs_index" / "index.json"
        
        # 支持的文件類型
        self.code_extensions = ['.py', '.js', '.ts', '.go', '.rs', '.java']
        self.doc_extensions = ['.md', '.rst', '.txt']
        self.config_extensions = ['.yaml', '.yml', '.json', '.toml']
        
        # 排除的目錄
        self.exclude_dirs = [
            '.git', 'node_modules', '__pycache__', '.venv', 
            'venv', 'dist', 'build', '.tox', '.pytest_cache'
        ]
        
        self.entries: List[IndexEntry] = []
        self.stats = IndexStats()
    
    def _generate_id(self, content: str, file_path: str) -> str:
        """生成唯一 ID"""
        hash_input = f"{file_path}:{content[:100]}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    def _should_exclude(self, path: Path) -> bool:
        """檢查是否應該排除"""
        for exclude in self.exclude_dirs:
            if exclude in path.parts:
                return True
        return False
    
    def scan_codebase(self) -> List[IndexEntry]:
        """掃描代碼庫"""
        entries = []
        
        # 掃描代碼文件
        for ext in self.code_extensions:
            for file_path in self.workspace.rglob(f"*{ext}"):
                if self._should_exclude(file_path):
                    continue
                entries.extend(self._extract_code_entries(file_path))
        
        # 掃描文檔文件
        for ext in self.doc_extensions:
            for file_path in self.workspace.rglob(f"*{ext}"):
                if self._should_exclude(file_path):
                    continue
                entries.extend(self._extract_doc_entries(file_path))
        
        # 掃描配置文件
        for ext in self.config_extensions:
            for file_path in self.workspace.rglob(f"*{ext}"):
                if self._should_exclude(file_path):
                    continue
                entries.extend(self._extract_config_entries(file_path))
        
        self.entries = entries
        self._update_stats()
        return entries
    
    def _extract_code_entries(self, file_path: Path) -> List[IndexEntry]:
        """提取代碼條目"""
        entries = []
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            # 提取函數和類定義
            current_block = []
            block_start = 0
            
            for i, line in enumerate(lines):
                # 檢測函數或類定義
                if line.strip().startswith(('def ', 'class ', 'async def ')):
                    if current_block:
                        # 保存之前的塊
                        block_content = '\n'.join(current_block)
                        if len(block_content.strip()) > 10:
                            entries.append(IndexEntry(
                                id=self._generate_id(block_content, str(file_path)),
                                content=block_content,
                                content_type="code",
                                file_path=str(file_path.relative_to(self.workspace)),
                                line_start=block_start + 1,
                                line_end=i,
                                metadata={
                                    "language": file_path.suffix[1:],
                                    "block_type": "function" if "def " in current_block[0] else "class"
                                }
                            ))
                    current_block = [line]
                    block_start = i
                elif current_block:
                    current_block.append(line)
            
            # 保存最後一個塊
            if current_block:
                block_content = '\n'.join(current_block)
                if len(block_content.strip()) > 10:
                    entries.append(IndexEntry(
                        id=self._generate_id(block_content, str(file_path)),
                        content=block_content,
                        content_type="code",
                        file_path=str(file_path.relative_to(self.workspace)),
                        line_start=block_start + 1,
                        line_end=len(lines),
                        metadata={
                            "language": file_path.suffix[1:],
                            "block_type": "function" if "def " in current_block[0] else "class"
                        }
                    ))
                    
        except Exception as e:
            pass
        
        return entries
    
    def _extract_doc_entries(self, file_path: Path) -> List[IndexEntry]:
        """提取文檔條目"""
        entries = []
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # 按章節分割（Markdown 標題）
            sections = []
            current_section = []
            section_start = 0
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if line.startswith('#'):
                    if current_section:
                        sections.append((section_start, i - 1, '\n'.join(current_section)))
                    current_section = [line]
                    section_start = i
                else:
                    current_section.append(line)
            
            if current_section:
                sections.append((section_start, len(lines) - 1, '\n'.join(current_section)))
            
            for start, end, section_content in sections:
                if len(section_content.strip()) > 20:
                    entries.append(IndexEntry(
                        id=self._generate_id(section_content, str(file_path)),
                        content=section_content[:2000],  # 限制長度
                        content_type="doc",
                        file_path=str(file_path.relative_to(self.workspace)),
                        line_start=start + 1,
                        line_end=end + 1,
                        metadata={
                            "format": file_path.suffix[1:]
                        }
                    ))
                    
        except Exception as e:
            pass
        
        return entries
    
    def _extract_config_entries(self, file_path: Path) -> List[IndexEntry]:
        """提取配置條目"""
        entries = []
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            if len(content.strip()) > 10:
                entries.append(IndexEntry(
                    id=self._generate_id(content, str(file_path)),
                    content=content[:2000],
                    content_type="config",
                    file_path=str(file_path.relative_to(self.workspace)),
                    line_start=1,
                    line_end=content.count('\n') + 1,
                    metadata={
                        "format": file_path.suffix[1:]
                    }
                ))
                
        except Exception as e:
            pass
        
        return entries
    
    def _update_stats(self):
        """更新統計信息"""
        self.stats.total_entries = len(self.entries)
        self.stats.code_entries = len([e for e in self.entries if e.content_type == "code"])
        self.stats.doc_entries = len([e for e in self.entries if e.content_type == "doc"])
        self.stats.config_entries = len([e for e in self.entries if e.content_type == "config"])
        self.stats.last_updated = datetime.now(timezone.utc).isoformat()
    
    def build_index(self) -> Dict[str, Any]:
        """構建索引"""
        if not self.entries:
            self.scan_codebase()
        
        # 創建索引目錄
        (self.index_dir / "code_vectors").mkdir(parents=True, exist_ok=True)
        (self.index_dir / "docs_index").mkdir(parents=True, exist_ok=True)
        
        # 分類保存
        code_entries = [asdict(e) for e in self.entries if e.content_type == "code"]
        doc_entries = [asdict(e) for e in self.entries if e.content_type == "doc"]
        config_entries = [asdict(e) for e in self.entries if e.content_type == "config"]
        
        # 保存代碼索引
        code_index = {
            "version": "1.0.0",
            "type": "code_vectors",
            "entries": code_entries,
            "stats": {
                "total": len(code_entries),
                "updated": self.stats.last_updated
            }
        }
        self.code_index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.code_index_path, 'w', encoding='utf-8') as f:
            json.dump(code_index, f, indent=2, ensure_ascii=False)
        
        # 保存文檔索引
        docs_index = {
            "version": "1.0.0",
            "type": "docs_index",
            "entries": doc_entries + config_entries,
            "stats": {
                "total": len(doc_entries) + len(config_entries),
                "updated": self.stats.last_updated
            }
        }
        self.docs_index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.docs_index_path, 'w', encoding='utf-8') as f:
            json.dump(docs_index, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "success",
            "stats": asdict(self.stats),
            "index_paths": {
                "code": str(self.code_index_path),
                "docs": str(self.docs_index_path)
            }
        }
    
    def search(self, query: str, content_type: Optional[str] = None, limit: int = 10) -> List[IndexEntry]:
        """簡單搜索（基於關鍵字匹配）"""
        results = []
        query_lower = query.lower()
        
        for entry in self.entries:
            if content_type and entry.content_type != content_type:
                continue
            
            if query_lower in entry.content.lower():
                results.append(entry)
                if len(results) >= limit:
                    break
        
        return results


def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Index Builder - 索引構建工具")
    parser.add_argument("--workspace", default=".", help="工作空間路徑")
    parser.add_argument("--build", action="store_true", help="構建索引")
    parser.add_argument("--search", type=str, help="搜索查詢")
    parser.add_argument("--type", choices=["code", "doc", "config"], help="內容類型過濾")
    
    args = parser.parse_args()
    
    builder = IndexBuilder(args.workspace)
    
    if args.build:
        print("正在掃描代碼庫...")
        builder.scan_codebase()
        print(f"找到 {builder.stats.total_entries} 個條目")
        print(f"  - 代碼: {builder.stats.code_entries}")
        print(f"  - 文檔: {builder.stats.doc_entries}")
        print(f"  - 配置: {builder.stats.config_entries}")
        
        print("\n正在構建索引...")
        result = builder.build_index()
        print(f"索引構建完成: {result['status']}")
        print(f"索引路徑:")
        for name, path in result['index_paths'].items():
            print(f"  - {name}: {path}")
    
    elif args.search:
        builder.scan_codebase()
        results = builder.search(args.search, args.type)
        print(f"找到 {len(results)} 個結果:")
        for r in results[:5]:
            print(f"\n[{r.content_type}] {r.file_path}:{r.line_start}-{r.line_end}")
            print(f"  {r.content[:100]}...")


if __name__ == "__main__":
    main()