#!/usr/bin/env python3
"""
Service Health Check Script
GL Runtime Platform - Service Verification

@GL-governed
@GL-layer: GL10-29 Operational
@GL-semantic: service-health-check-script
@GL-charter-version: 1.0.0
"""

import subprocess
import json
import sys
from datetime import datetime

def check_service(service_name, port, health_endpoint=None):
    """Check if a service is healthy"""
    try:
        # Try to connect to the port
        sock = subprocess.run(
            ['nc', '-z', 'localhost', str(port)],
            capture_output=True,
            timeout=5
        )
        
        if sock.returncode != 0:
            return {
                "service": service_name,
                "port": port,
                "status": "unreachable",
                "health_endpoint": health_endpoint
            }
        
        # If health endpoint is specified, check it
        if health_endpoint:
            import urllib.request
            try:
                url = f"http://localhost:{port}{health_endpoint}"
                response = urllib.request.urlopen(url, timeout=5)
                return {
                    "service": service_name,
                    "port": port,
                    "status": "healthy",
                    "health_endpoint": health_endpoint,
                    "http_status": response.getcode()
                }
            except Exception as e:
                return {
                    "service": service_name,
                    "port": port,
                    "status": "port_open_but_health_check_failed",
                    "error": str(e)
                }
        
        return {
            "service": service_name,
            "port": port,
            "status": "port_open"
        }
        
    except Exception as e:
        return {
            "service": service_name,
            "port": port,
            "status": "error",
            "error": str(e)
        }

def main():
    services = [
        {"name": "main-app", "port": 3000, "health": "/health"},
        {"name": "rest-api", "port": 8080, "health": "/api/health"},
        {"name": "nlp-control-plane", "port": 5001, "health": "/health"},
        {"name": "minio", "port": 9000, "health": None},
        {"name": "redis", "port": 6379, "health": None},
        {"name": "postgres", "port": 5432, "health": None},
        {"name": "prometheus", "port": 9090, "health": "/-/healthy"}
    ]
    
    results = {
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    all_healthy = True
    for service in services:
        result = check_service(service["name"], service["port"], service.get("health"))
        results["services"][service["name"]] = result
        status = result["status"]
        print(f"{service['name']}: {status}")
        if status not in ["healthy", "port_open"]:
            all_healthy = False
    
    results["overall_status"] = "all_healthy" if all_healthy else "some_services_unhealthy"
    
    # Save results
    with open('/tmp/service-health-results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    sys.exit(0 if all_healthy else 1)

if __name__ == "__main__":
    main()