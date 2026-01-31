# @GL-governed
# @GL-layer: GL00-09
# @GL-semantic: general-component
# @GL-audit-trail: gl-platform-universe/gl_platform_universegl_platform_universe.governance/audit-trails/GL00_09-audit.json
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/gl_platform_universegl_platform_universe.governance/GL-UNIFIED-NAMING-CHARTER.yaml


"""GL Runtime 統一服務啟動器"""
import sys
import importlib
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading

class GLRuntimeHandler(BaseHTTPRequestHandler):
    def __init__(self, version, service, *args, **kwargs):
        self.version = version
        self.service = service
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {
            "version": self.version,
            "status": "running",
            "service": self.service.__class__.__name__
        }
        self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        pass  # 靜默日誌

def create_handler(version, service):
    def handler(*args, **kwargs):
        GLRuntimeHandler(version, service, *args, **kwargs)
    return handler

def start_service(version, port):
    print(f"[{version}] 啟動服務於端口 {port}...")
    
VERSION_PORTS = {
    "v1": 8001, "v2": 8002, "v3": 8003, "v4": 8004, "v5": 8005,
    "v6": 8006, "v7": 8007, "v8": 8008, "v9": 8009, "v10": 8010,
    "v11": 8011, "v12": 8012, "v13": 8013, "v14": 8014, "v15": 8015,
    "v16": 8016, "v17": 8017, "v18": 8018, "v19": 8019, "v20": 8020,
    "v21": 8021, "v22": 8022, "v23": 8023, "v24": 8024, "v25": 8025,
}

if __name__ == "__main__":
    version = sys.argv[1] if len(sys.argv) > 1 else "v1"
    port = VERSION_PORTS.get(version, 8000)
    print(f"GL Runtime {version} 服務啟動於 http://localhost:{port}")
