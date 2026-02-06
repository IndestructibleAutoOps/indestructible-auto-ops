"""
Simple YAML Parser
Minimal YAML parser for rule files (zero external dependencies)

@GL-semantic: simple-yaml-parser
@GL-audit-trail: enabled
"""

import re
from typing import Dict, Any, List


def parse_yaml(content: str) -> Dict[str, Any]:
    """Parse simple YAML content
    
    Args:
        content: YAML content string
        
    Returns:
        Parsed dictionary
    """
    result = {}
    current_section = result
    stack = []
    current_list = None
    current_dict = None
    
    for line in content.split('\n'):
        # Skip empty lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
            
        # Handle list items (-)
        if stripped.startswith('- '):
            item = stripped[2:].strip()
            if current_list is not None:
                current_list.append(item)
            continue
            
        # Calculate indent
        indent = len(line) - len(line.lstrip())
        
        # Handle section changes (key with colon)
        if ':' in line and not line.strip().startswith('-'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # If value is empty, it's a section header
            if not value:
                section_dict = {}
                
                if indent == 0:
                    result[key] = section_dict
                    current_section = section_dict
                    stack = [(indent, section_dict)]
                else:
                    # Navigate to correct section
                    while stack and stack[-1][0] >= indent:
                        stack.pop()
                    
                    if stack:
                        parent_section = stack[-1][1]
                        parent_section[key] = section_dict
                        current_section = section_dict
                        stack.append((indent, section_dict))
                
                current_dict = section_dict
                current_list = None
                continue
            
            # Parse value
            parsed_value = _parse_value(value)
            current_dict[key] = parsed_value
            current_list = None
            
        # Handle list continuation
        elif line.strip().startswith('- ') and current_list is not None:
            item = line.strip()[2:].strip()
            current_list.append(item)
    
    return result


def _parse_value(value: str) -> Any:
    """Parse a YAML value
    
    Args:
        value: String value
        
    Returns:
        Parsed value
    """
    value = value.strip()
    
    # List value
    if value.startswith('[') and value.endswith(']'):
        inner = value[1:-1].strip()
        if inner:
            return [v.strip().strip('"\'') for v in inner.split(',')]
        return []
    
    # Boolean
    if value.lower() in ('true', 'yes', 'on'):
        return True
    if value.lower() in ('false', 'no', 'off'):
        return False
    
    # Number
    if value.isdigit():
        return int(value)
    if value.replace('.', '', 1).isdigit():
        return float(value)
    
    # String
    return value.strip('"\'').strip()


def load_yaml_file(file_path: str) -> Dict[str, Any]:
    """Load YAML file
    
    Args:
        file_path: Path to YAML file
        
    Returns:
        Parsed dictionary
    """
    with open(file_path, 'r') as f:
        content = f.read()
    return parse_yaml(content)
