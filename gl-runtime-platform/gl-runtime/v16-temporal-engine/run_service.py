#!/usr/bin/env python3
"""v16-temporal-engine 服務"""
import http.server, socketserver, json
PORT, VER = 8016, "v16-temporal-engine"
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"version":VER,"port":PORT,"status":"running"}).encode())
    def log_message(self,*a):pass
if __name__=="__main__":
    print(f"✓ {VER} @ http://0.0.0.0:{PORT}")
    socketserver.TCPServer(("",PORT),H).serve_forever()
