import yaml
import sys

try:
    with open('.github/workflows/hardened-ci.yml', 'r') as f:
        content = f.read()
    
    # Try to parse line by line to find the issue
    lines = content.split('\n')
    print(f"Total lines: {len(lines)}")
    print(f"Line 256: {repr(lines[255])}")
    print(f"Line 257: {repr(lines[256])}")
    print(f"Line 258: {repr(lines[257])}")
    
    # Try loading
    data = yaml.safe_load(content)
    print("YAML is valid!")
except yaml.YAMLError as e:
    print(f"YAML Error: {e}")
    if hasattr(e, 'problem_mark'):
        mark = e.problem_mark
        print(f"Error at line {mark.line + 1}, column {mark.column + 1}")
        print(f"Context: {lines[mark.line - 2:mark.line + 3]}")
except Exception as e:
    print(f"Error: {e}")