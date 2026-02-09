#!/usr/bin/env python3
"""
白名單管理器 - 管理重構過程中的例外
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
import re


@dataclass
class WhitelistEntry:
    """白名單條目"""
    pattern: str
    reason: str
    category: str
    expiry: Optional[str] = None  # ISO 格式日期


class WhitelistManager:
    """白名單管理器"""
    
    def __init__(self, whitelist_path: Path):
        self.whitelist_path = whitelist_path
        self.entries: List[WhitelistEntry] = []
        self._load_whitelist()
    
    def _load_whitelist(self):
        """加載白名單"""
        if self.whitelist_path.exists():
            with open(self.whitelist_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.entries = [
                    WhitelistEntry(**entry) for entry in data.get('entries', [])
                ]
    
    def _save_whitelist(self):
        """保存白名單"""
        data = {
            'entries': [
                {
                    'pattern': entry.pattern,
                    'reason': entry.reason,
                    'category': entry.category,
                    'expiry': entry.expiry
                }
                for entry in self.entries
            ]
        }
        self.whitelist_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.whitelist_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add(self, pattern: str, reason: str, category: str, expiry: Optional[str] = None):
        """添加白名單條目"""
        entry = WhitelistEntry(pattern=pattern, reason=reason, category=category, expiry=expiry)
        self.entries.append(entry)
        self._save_whitelist()
    
    def is_whitelisted(self, item: str) -> bool:
        """檢查項目是否在白名單中"""
        for entry in self.entries:
            if re.match(entry.pattern, item):
                return True
        return False
    
    def get_by_category(self, category: str) -> List[WhitelistEntry]:
        """按類別獲取白名單條目"""
        return [entry for entry in self.entries if entry.category == category]
    
    def remove(self, pattern: str):
        """移除白名單條目"""
        self.entries = [entry for entry in self.entries if entry.pattern != pattern]
        self._save_whitelist()


# 預定義的白名單
DEFAULT_WHITELIST = {
    "directories": [
        {"pattern": r"^\.", "reason": "隱藏目錄", "category": "system"},
        {"pattern": r"^node_modules$", "reason": "第三方依賴", "category": "dependencies"},
        {"pattern": r"^__pycache__$", "reason": "Python 緩存", "category": "system"},
        {"pattern": r"\.git$", "reason": "Git 版本控制", "category": "system"},
    ],
    "files": [
        {"pattern": r"\.pyc$", "reason": "Python 編譯文件", "category": "system"},
        {"pattern": r"\.log$", "reason": "日誌文件", "category": "logs"},
        {"pattern": r"\.tmp$", "reason": "臨時文件", "category": "system"},
    ],
    "naming": [
        {"pattern": r"^README\.md$", "reason": "標準文檔", "category": "documentation"},
        {"pattern": r"^LICENSE$", "reason": "許可證文件", "category": "legal"},
        {"pattern": r"^\.gitignore$", "reason": "Git 配置", "category": "system"},
    ]
}


def create_default_whitelist(whitelist_path: Path):
    """創建預設白名單"""
    whitelist_path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "entries": [],
        "categories": {
            "system": "系統文件和目錄",
            "dependencies": "第三方依賴",
            "documentation": "文檔文件",
            "legal": "法律文件",
            "logs": "日誌文件",
        }
    }
    
    # 添加預設條目
    for category, entries in DEFAULT_WHITELIST.items():
        for entry in entries:
            data["entries"].append(entry)
    
    with open(whitelist_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 創建預設白名單: {whitelist_path}")


if __name__ == '__main__':
    # 創建預設白名單
    whitelist_path = Path('/workspace/indestructibleautoops/refactor/tools/whitelist.json')
    create_default_whitelist(whitelist_path)
    
    # 測試白名單管理器
    manager = WhitelistManager(whitelist_path)
    
    # 測試檢查
    print("\n測試白名單檢查:")
    test_items = [".git", "test.py", "README.md", "node_modules"]
    for item in test_items:
        is_whitelisted = manager.is_whitelisted(item)
        print(f"  {item}: {'✅ 在白名單中' if is_whitelisted else '❌ 不在白名單中'}")