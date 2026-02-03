# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: github-scripts
# @GL-audit-trail: ../../engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import os
import re
import json
import sys

def analyze_task(task_description):
    """
    分析任務描述並返回建議的代理列表
    """
    agents_dir = ".github/agents"
    available_agents = []
    
    # 讀取所有代理定義
    for file in os.listdir(agents_dir):
        if file.endswith(".agent.md"):
            path = os.path.join(agents_dir, file)
            with open(path, 'r') as f:
                content = f.read()
                # 提取名稱和描述
                name_match = re.search(r"name: '(.*?)'", content)
                desc_match = re.search(r"description: '(.*?)'", content)
                if name_match and desc_match:
                    available_agents.append({
                        "file": file,
                        "name": name_match.group(1),
                        "description": desc_match.group(1)
                    })

    selected_agents = []
    
    # 基礎研究代理（預設必選）
    selected_agents.append("research-coordinator.agent.md")
    selected_agents.append("domain-researcher.agent.md")

    # 根據關鍵字動態選擇
    task_lower = task_description.lower()
    
    if any(kw in task_lower for kw in ["web", "deploy", "site", "website", "部署", "網站"]):
        selected_agents.append("web-architect.agent.md")
        
    if any(kw in task_lower for kw in ["slide", "ppt", "presentation", "幻燈片", "報告"]):
        selected_agents.append("presentation-specialist.agent.md")
        
    if any(kw in task_lower for kw in ["security", "audit", "safe", "安全", "審計"]):
        selected_agents.append("security-reviewer.agent.md")

    if any(kw in task_lower for kw in ["custom agent", "custom-agent", "agent profile", "自訂代理", "自訂代理人"]):
        selected_agents.append("custom-agent.agent.md")

    return list(set(selected_agents))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 agent-selector.py '<task_description>'")
        sys.exit(1)
        
    task_desc = sys.argv[1]
    selected = analyze_task(task_desc)
    print(json.dumps(selected, indent=2))
