#!/usr/bin/env python3
"""修復 enforce.rules.py 中的 YAML 解析器 - 使用 sed"""

import re

# 讀取文件
with open('/workspace/ecosystem/enforce.rules.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 _load_yaml 方法並替換
# 匹配從 "def _load_yaml" 到下一個 "def" 之前的所有內容
pattern = r'(    def _load_yaml\(self, file_path: Path\) -> Optional\[Dict\]:.*?)(\n    def )'

replacement = r'''    def _load_yaml(self, file_path: Path) -> Optional[Dict]:
        """載入 YAML 文件使用 PyYAML"""
        try:
            if not file_path.exists():
                print(f"[WARNING] File not found: {file_path}")
                return None
            
            import yaml
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load {file_path}: {e}")
            return None

\2'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# 寫回文件
with open('/workspace/ecosystem/enforce.rules.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ 已修復 YAML 解析器")