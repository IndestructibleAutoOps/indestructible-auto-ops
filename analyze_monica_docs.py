#!/usr/bin/env python3
"""Analyze Monica AI Agent research documents for IndestructibleAutoOps AI research"""

import json
import re
from pathlib import Path

def read_document(filepath):
    """Read a document that may not have line terminators"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return ""

def extract_sections(content):
    """Extract main sections from markdown content"""
    # Split on markdown headers
    sections = re.split(r'\n(?=##\s)', content)
    return sections

def extract_key_features(content):
    """Extract key features and functionality"""
    features = []
    
    # Look for feature lists
    feature_patterns = [
        r'(?:功能|功能模块|核心功能)\s*[:：]\s*([^#\n]+)',
        r'(?:功能特性|技术特点)\s*[:：]\s*([^#\n]+)',
        r'\*\s*([^*]+)\s*[:：]',
    ]
    
    for pattern in feature_patterns:
        matches = re.findall(pattern, content)
        features.extend(matches)
    
    return features

def analyze_document(filepath):
    """Analyze a document and return structured insights"""
    content = read_document(filepath)
    
    if not content:
        return None
    
    sections = extract_sections(content)
    features = extract_key_features(content)
    
    # Extract key statistics
    stats = {
        'length': len(content),
        'sections': len(sections),
        'has_code_blocks': '```' in content,
        'has_tables': '|' in content,
        'word_count': len(content.split())
    }
    
    return {
        'filepath': filepath,
        'stats': stats,
        'sections_count': len(sections),
        'features_found': len(features),
        'sample_features': features[:10] if features else []
    }

def main():
    # Analyze both documents
    docs = [
        "/workspace/monica-ai-agent-comprehensive-analysis-1.md",
        "/workspace/monica-ai-agent-engineering-specification.md"
    ]
    
    results = []
    for doc in docs:
        result = analyze_document(doc)
        if result:
            results.append(result)
    
    # Output analysis
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    # Save detailed analysis
    with open('/workspace/monica_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\nAnalysis saved to /workspace/monica_analysis.json")

if __name__ == "__main__":
    main()