# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-enterprise-architecture/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


#!/usr/bin/env python3
"""GL Runtime V1-V25 統一服務管理器"""
import subprocess
import sys
import time
import signal
import os

SERVICES = []

def start_all():
    print("=" * 60)
    print("GL Runtime 全版本服務啟動器")
    print("=" * 60)
    
    versions = [
        ("v1-basic-execution", 8001),
        ("v2-basic-analysis", 8002),
        ("v3-basic-gl_platform_universegl_platform_universe.governance", 8003),
        ("v4-auto-repair", 8004),
        ("v5-auto-optimization", 8005),
        ("v6-multi-module", 8006),
        ("v7-global-dag", 8007),
        ("v8-semantic-resource-graph", 8008),
        ("v9-self-healing", 8009),
        ("v10-multi-agent-swarm", 8010),
        ("v11-mesh-cognition", 8011),
        ("v12-evolution-engine", 8012),
        ("v13-civilization-layer", 8013),
        ("v14-quantum-consensus", 8014),
        ("v15-neural-fabric", 8015),
        ("v16-temporal-engine", 8016),
        ("v17-reality-bridge", 8017),
        ("v18-consciousness-layer", 8018),
        ("v19-universal-translator", 8019),
        ("v20-infinity-pool", 8020),
        ("v21-genesis-protocol", 8021),
        ("v22-omega-synthesis", 8022),
        ("v23-root-gl_platform_universegl_platform_universe.governance", 8023),
        ("v24-meta-gl_platform_universegl_platform_universe.governance", 8024),
        ("v25-ecosystem-integration", 8025),
    ]
    
    for name, port in versions:
        script = f"{name}/run_service.py"
        if os.path.exists(script):
            proc = subprocess.Popen(
                [sys.executable, script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            SERVICES.append((name, port, proc))
            print(f"✓ {name:35} -> http://0.0.0.0:{port}")
            time.sleep(0.1)
        else:
            print(f"✗ {name:35} -> 腳本不存在")
    
    print("=" * 60)
    print(f"已啟動 {len(SERVICES)} 個服務")
    print("=" * 60)
    return SERVICES

def stop_all():
    print("\n正在停止所有服務...")
    for name, port, proc in SERVICES:
        proc.terminate()
        print(f"✓ 已停止 {name}")

if __name__ == "__main__":
    start_all()
    print("\n服務運行中... (Ctrl+C 停止)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_all()
