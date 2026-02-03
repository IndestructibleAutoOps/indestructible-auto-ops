#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: mock-service
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json
#
"""
Mock Service for Local Development
===================================
GL Layer: GL30-49 Execution Layer

This mock service simulates external dependencies for local development.

Features:
- Mock API responses
- Fake data generation
- Service simulation
- Audit logging integration
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class MockService:
    """
    Mock service implementation.
    
    Simulates external services for local development and testing.
    """
    
    VERSION = "1.0.0-mock"
    
    def __init__(self, mock_data_dir: Optional[str] = None):
        """
        Initialize mock service.
        
        Args:
            mock_data_dir: Directory containing mock data files
        """
        self.mock_data_dir = Path(mock_data_dir) if mock_data_dir else self._get_default_data_dir()
        self._cache: Dict[str, Any] = {}
    
    def _get_default_data_dir(self) -> Path:
        """Get default mock data directory"""
        return Path(__file__).parent.parent / "data"
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current UTC timestamp in RFC3339 format"""
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def get_health(self) -> Dict[str, Any]:
        """
        Get mock health status.
        
        Returns:
            Dictionary with health status
        """
        return {
            "status": "healthy",
            "mock": True,
            "version": self.VERSION,
            "timestamp": self.get_timestamp(),
            "services": {
                "database": "mock",
                "cache": "mock",
                "queue": "mock"
            }
        }
    
    def get_users(self) -> List[Dict[str, Any]]:
        """
        Get mock users.
        
        Returns:
            List of mock user dictionaries
        """
        users_file = self.mock_data_dir / "sample-users.json"
        
        if users_file.exists():
            with open(users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Return default mock users if file doesn't exist
        return [
            {"id": 1, "name": "Mock User", "email": "mock@test.local"}
        ]
    
    def simulate_response(
        self,
        endpoint: str,
        method: str = "GET",
        body: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Simulate an API response.
        
        Args:
            endpoint: API endpoint path
            method: HTTP method
            body: Request body (optional)
        
        Returns:
            Dictionary with simulated response
        """
        timestamp = self.get_timestamp()
        
        # Common response structure
        response = {
            "success": True,
            "mock": True,
            "timestamp": timestamp,
            "endpoint": endpoint,
            "method": method,
            "data": {}
        }
        
        # Simulate different endpoints
        if "/health" in endpoint:
            response["data"] = self.get_health()
        elif "/users" in endpoint:
            if method == "GET":
                response["data"] = {"users": self.get_users()}
            elif method == "POST":
                response["data"] = {
                    "id": 999,
                    "created": True,
                    **(body or {})
                }
        elif "/governance" in endpoint:
            response["data"] = {
                "compliance": True,
                "gl_layer": "GL30-49",
                "status": "mock"
            }
        else:
            response["data"] = {"message": "Mock response for " + endpoint}
        
        return response
    
    def simulate_database_query(
        self,
        table: str,
        operation: str = "SELECT",
        conditions: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Simulate a database query.
        
        Args:
            table: Table name
            operation: SQL operation (SELECT, INSERT, UPDATE, DELETE)
            conditions: Query conditions
        
        Returns:
            Dictionary with simulated query result
        """
        return {
            "success": True,
            "mock": True,
            "operation": operation,
            "table": table,
            "conditions": conditions or {},
            "rows_affected": 1,
            "data": []
        }
    
    def simulate_cache_operation(
        self,
        key: str,
        operation: str = "GET",
        value: Optional[Any] = None,
        ttl: int = 3600
    ) -> Dict[str, Any]:
        """
        Simulate a cache operation.
        
        Args:
            key: Cache key
            operation: Operation (GET, SET, DELETE)
            value: Value to cache (for SET)
            ttl: Time to live in seconds
        
        Returns:
            Dictionary with simulated cache result
        """
        if operation == "SET" and value is not None:
            self._cache[key] = {
                "value": value,
                "expires": datetime.now(timezone.utc).timestamp() + ttl
            }
            return {"success": True, "operation": "SET", "key": key}
        
        elif operation == "GET":
            cached = self._cache.get(key)
            if cached and cached["expires"] > datetime.now(timezone.utc).timestamp():
                return {
                    "success": True,
                    "operation": "GET",
                    "key": key,
                    "value": cached["value"],
                    "hit": True
                }
            return {
                "success": True,
                "operation": "GET",
                "key": key,
                "value": None,
                "hit": False
            }
        
        elif operation == "DELETE":
            if key in self._cache:
                del self._cache[key]
            return {"success": True, "operation": "DELETE", "key": key}
        
        return {"success": False, "error": "Unknown operation"}
    
    def simulate_queue_operation(
        self,
        queue: str,
        operation: str = "PUBLISH",
        message: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Simulate a message queue operation.
        
        Args:
            queue: Queue name
            operation: Operation (PUBLISH, CONSUME)
            message: Message to publish
        
        Returns:
            Dictionary with simulated queue result
        """
        if operation == "PUBLISH":
            return {
                "success": True,
                "operation": "PUBLISH",
                "queue": queue,
                "message_id": f"msg_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "mock": True
            }
        
        elif operation == "CONSUME":
            return {
                "success": True,
                "operation": "CONSUME",
                "queue": queue,
                "messages": [
                    {"id": "mock_msg_1", "body": {"type": "mock", "data": {}}}
                ],
                "mock": True
            }
        
        return {"success": False, "error": "Unknown operation"}


# Singleton instance
_mock_service: Optional[MockService] = None


def get_mock_service(mock_data_dir: Optional[str] = None) -> MockService:
    """
    Get mock service instance (singleton).
    
    Args:
        mock_data_dir: Optional mock data directory
    
    Returns:
        MockService instance
    """
    global _mock_service
    
    if _mock_service is None or mock_data_dir is not None:
        _mock_service = MockService(mock_data_dir=mock_data_dir)
    
    return _mock_service


def is_mock_enabled() -> bool:
    """
    Check if mock services are enabled.
    
    Returns:
        True if DEV_MOCK_EXTERNAL_SERVICES is set to true
    """
    return os.environ.get("DEV_MOCK_EXTERNAL_SERVICES", "").lower() == "true"


if __name__ == "__main__":
    # Demo usage
    service = get_mock_service()
    
    print("Mock Service Demo")
    print("=" * 50)
    
    print("\n1. Health Check:")
    print(json.dumps(service.get_health(), indent=2))
    
    print("\n2. Get Users:")
    print(json.dumps(service.get_users(), indent=2))
    
    print("\n3. Simulate API Response:")
    print(json.dumps(service.simulate_response("/api/v1/users", "GET"), indent=2))
    
    print("\n4. Simulate Database Query:")
    print(json.dumps(service.simulate_database_query("users", "SELECT"), indent=2))
    
    print("\n5. Simulate Cache Operation:")
    print(json.dumps(service.simulate_cache_operation("test_key", "SET", "test_value"), indent=2))
    print(json.dumps(service.simulate_cache_operation("test_key", "GET"), indent=2))
    
    print("\n6. Simulate Queue Operation:")
    print(json.dumps(service.simulate_queue_operation("events", "PUBLISH", {"event": "test"}), indent=2))
