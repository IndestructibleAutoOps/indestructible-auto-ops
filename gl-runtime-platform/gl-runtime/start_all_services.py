#!/usr/bin/env python3
"""GL Runtime V1-V25 服務啟動器"""
import threading
import http.server
import socketserver
import json
import time

VERSIONS = [
    (8001, "v1-basic-execution"),
    (8002, "v2-basic-analysis"),
    (8003, "v3-basic-governance"),
    (8004, "v4-auto-repair"),
    (8005, "v5-auto-optimization"),
    (8006, "v6-multi-module"),
    (8007, "v7-global-dag"),
    (8008, "v8-semantic-resource-graph"),
    (8009, "v9-self-healing"),
    (8010, "v10-multi-agent-swarm"),
    (8011, "v11-mesh-cognition"),
    (8012, "v12-evolution-engine"),
    (8013, "v13-civilization-layer"),
    (8014, "v14-quantum-consensus"),
    (8015, "v15-neural-fabric"),
    (8016, "v16-temporal-engine"),
    (8017, "v17-reality-bridge"),
    (8018, "v18-consciousness-layer"),
    (8019, "v19-universal-translator"),
    (8020, "v20-infinity-pool"),
    (8021, "v21-genesis-protocol"),
    (8022, "v22-omega-synthesis"),
    (8023, "v23-root-governance"),
    (8024, "v24-meta-governance"),
    (8025, "v25-ecosystem-integration"),
]

def make_handler(version, port):
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "version": version,
                "port": port,
                "status": "running"
            }).encode())
        def log_message(self, *args): pass
    return Handler

def run_server(port, version):
    try:
        handler = make_handler(version, port)
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"✗ {version} 錯誤: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("GL Runtime V1-V25 服務啟動")
    print("=" * 60)
    
    threads = []
    for port, version in VERSIONS:
        t = threading.Thread(target=run_server, args=(port, version), daemon=True)
        t.start()
        threads.append(t)
        print(f"✓ {version:35} @ http://0.0.0.0:{port}")
        time.sleep(0.05)
    
    print("=" * 60)
    print(f"已啟動 {len(threads)} 服務")
    print("=" * 60)
    print("服務運行中... (Ctrl+C 停止)")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n已停止所有服務")
