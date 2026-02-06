#!/usr/bin/env python3
"""Step 1: Internal Retrieval - Analyze Monica AI Agent documents"""

import json
import re

def extract_comprehensive_insights(content):
    """Extract comprehensive insights from Monica AI Agent documents"""
    
    insights = {
        'core_modules': [],
        'key_features': [],
        'technical_architecture': [],
        'best_practices': [],
        'challenges': [],
        'implementation_strategies': []
    }
    
    # Extract core modules
    module_patterns = [
        r'Deep Research\s*[:：]\s*([^#\n]+)',
        r'Browser Operator\s*[:：]\s*([^#\n]+)',
        r'Create Slides\s*[:：]\s*([^#\n]+)',
    ]
    
    for pattern in module_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        insights['core_modules'].extend(matches)
    
    # Extract key features
    feature_patterns = [
        r'(?:核心能力|核心功能|技术特点)\s*[:：]\s*([^#\n]+)',
        r'\*\s*([^*]+)\s*[:：]',
    ]
    
    for pattern in feature_patterns:
        matches = re.findall(pattern, content)
        insights['key_features'].extend(matches)
    
    # Extract technical architecture
    arch_patterns = [
        r'(?:架构|系统架构)\s*[:：]\s*([^#\n]+)',
        r'(?:技术栈|技术框架)\s*[:：]\s*([^#\n]+)',
    ]
    
    for pattern in arch_patterns:
        matches = re.findall(pattern, content)
        insights['technical_architecture'].extend(matches)
    
    # Extract best practices
    practice_patterns = [
        r'(?:最佳实践|Best Practice|最佳實踐)\s*[:：]\s*([^#\n]+)',
        r'(?:建议|推荐)\s*[:：]\s*([^#\n]+)',
    ]
    
    for pattern in practice_patterns:
        matches = re.findall(pattern, content)
        insights['best_practices'].extend(matches)
    
    # Extract challenges
    challenge_patterns = [
        r'(?:挑战|问题|难点)\s*[:：]\s*([^#\n]+)',
        r'(?:风险|考虑)\s*[:：]\s*([^#\n]+)',
    ]
    
    for pattern in challenge_patterns:
        matches = re.findall(pattern, content)
        insights['challenges'].extend(matches)
    
    # Extract implementation strategies
    strategy_patterns = [
        r'(?:实施|实现|Implementation)\s*[:：]\s*([^#\n]+)',
        r'(?:步骤|Step)\s*[:：]\s*([^#\n]+)',
    ]
    
    for pattern in strategy_patterns:
        matches = re.findall(pattern, content)
        insights['implementation_strategies'].extend(matches)
    
    # Clean up insights
    for key in insights:
        insights[key] = list(set([item.strip() for item in insights[key] if item.strip()]))
    
    return insights

def read_document(filepath):
    """Read a document"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return ""

def main():
    # Read both documents
    docs = [
        "/workspace/monica-ai-agent-comprehensive-analysis-1.md",
        "/workspace/monica-ai-agent-engineering-specification.md"
    ]
    
    all_insights = {
        'internal_retrieval': {
            'phase': 'Internal Retrieval (内网检索)',
            'date': '2026-02-05',
            'documents_analyzed': len(docs),
            'findings': {}
        }
    }
    
    for doc in docs:
        content = read_document(doc)
        if content:
            insights = extract_comprehensive_insights(content)
            all_insights['internal_retrieval']['findings'][doc] = insights
    
    # Save results
    with open('/workspace/step1_internal_retrieval.json', 'w', encoding='utf-8') as f:
        json.dump(all_insights, f, indent=2, ensure_ascii=False)
    
    print("✅ Internal Retrieval Complete")
    print(f"   Documents analyzed: {len(docs)}")
    print(f"   Results saved to: /workspace/step1_internal_retrieval.json")
    
    return all_insights

if __name__ == "__main__":
    main()