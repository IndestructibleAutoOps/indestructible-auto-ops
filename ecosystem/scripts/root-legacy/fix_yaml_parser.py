#!/usr/bin/env python3
"""修復 enforce.rules.py 中的 YAML 解析器"""

# 讀取文件
with open('/workspace/ecosystem/enforce.rules.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到 _load_yaml 方法的開始和結束
start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if 'def _load_yaml(self, file_path: Path) -> Optional[Dict]:' in line:
        start_idx = i
    elif start_idx is not None and line.strip().startswith('def ') and i > start_idx:
        end_idx = i
        break

if start_idx is None:
    print("ERROR: 找不到 _load_yaml 方法")
    exit(1)

if end_idx is None:
    print("ERROR: 找不到 _load_yaml 方法的結束")
    exit(1)

print(f"找到 _load_yaml 方法: 行 {start_idx+1} 到 {end_idx}")

# 新方法實現
new_method = '''    def _load_yaml(self, file_path: Path) -> Optional[Dict]:
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

'''

# 替換方法
new_lines = lines[:start_idx] + [new_method] + lines[end_idx:]

# 寫回文件
with open('/workspace/ecosystem/enforce.rules.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"✅ 已修復 YAML 解析器")
print(f"✅ 現在使用 PyYAML 的 yaml.safe_load()")