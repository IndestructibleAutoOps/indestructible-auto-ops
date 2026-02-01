#!/usr/bin/env python3
"""
Port Availability Check Script
GL Runtime Platform - Port Verification

@GL-governed
@GL-layer: GL10-29 Operational
@GL-semantic: port-check-script
@GL-charter-version: 1.0.0
"""

import socket
import sys
import json
from datetime import datetime

def check_port(port, host='localhost'):
    """Check if a port is open"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((host, port))
    is_open = result == 0
    sock.close()
    return is_open

def main():
    ports_to_check = [3000, 8080, 5001, 9000, 6379, 5432, 9090, 3001, 3002]
    
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "host": "localhost",
        "ports": {}
    }
    
    all_open = True
    for port in ports_to_check:
        is_open = check_port(port)
        status = "OPEN" if is_open else "CLOSED"
        results["ports"][f"port_{port}"] = status
        print(f"Port {port}: {status}")
        if not is_open:
            all_open = False
    
    results["overall_status"] = "all_ports_open" if all_open else "some_ports_closed"
    
    # Save results
    with open('/tmp/port-check-results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    sys.exit(0 if all_open else 1)

if __name__ == "__main__":
    main()