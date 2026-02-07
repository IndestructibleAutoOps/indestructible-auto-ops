#!/usr/bin/env python3
"""
API Gateway Tests
=================
測試 API 網關系統的核心功能
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from router import Router, Route, RouteMatchType
from authenticator import Authenticator, AuthToken
from rate_limiter import RateLimiter, RateLimitConfig
from gateway import Gateway


def test_router():
    """測試路由器"""
    print("\n=== Test Router ===")

    config = {}
    router = Router(config)

    # 添加路由
    route = Route(
        path="/api/v1/services/*",
        platform="service-discovery",
        service="discovery-api",
        methods=["GET", "POST"],
        timeout=30,
        authentication="optional",
    )

    assert router.add_route(route), "Failed to add route"
    print("✓ Route added")

    # 測試路由匹配
    matched = router.match_route("/api/v1/services/list", "GET")
    assert matched is not None, "Route matching failed"
    assert matched.platform == "service-discovery", "Route platform mismatch"
    print("✓ Route matched")

    # 測試方法過濾
    matched_post = router.match_route("/api/v1/services/create", "POST")
    assert matched_post is not None, "POST route matching failed"

    matched_delete = router.match_route("/api/v1/services/delete", "DELETE")
    assert matched_delete is None, "DELETE should not match"
    print("✓ Method filtering works")

    # 測試路徑重寫
    rewritten = router.rewrite_path("/api/v1/services/list", matched)
    assert rewritten == "/list", f"Path rewrite failed: {rewritten}"
    print("✓ Path rewriting works")

    # 列出路由
    routes = router.list_routes()
    assert len(routes) == 1, "Route listing failed"
    print("✓ Route listing works")

    print("✅ Router tests passed")


def test_authenticator():
    """測試認證器"""
    print("\n=== Test Authenticator ===")

    config = {
        "authentication": {
            "jwt": {
                "enabled": True,
                "secret": "test-secret",
                "algorithm": "HS256",
                "expiration": 3600,
            }
        }
    }

    auth = Authenticator(config)

    # 生成 JWT
    token = auth.generate_jwt(
        user_id="user123", username="testuser", roles=["user", "admin"]
    )

    assert token is not None, "JWT generation failed"
    print(f"✓ JWT generated: {token[:20]}...")

    # 驗證 JWT
    auth_token = auth.verify_jwt(token)
    assert auth_token is not None, "JWT verification failed"
    assert auth_token.username == "testuser", "Username mismatch"
    assert "admin" in auth_token.roles, "Roles mismatch"
    assert not auth_token.is_expired(), "Token should not be expired"
    print("✓ JWT verified")

    # 測試角色檢查
    assert auth_token.has_role("admin"), "Role check failed"
    assert not auth_token.has_role("superuser"), "Role check should fail"
    print("✓ Role checking works")

    # 測試 API Key
    api_key = auth.generate_api_key(
        user_id="user456", username="apiuser", roles=["api"]
    )

    assert api_key is not None, "API Key generation failed"
    # Mask the API key in logs to avoid exposing sensitive data
    print(f"✓ API Key generated: {'*' * 20}... (masked for security)")

    # 驗證 API Key
    api_auth_token = auth.verify_api_key(api_key)
    assert api_auth_token is not None, "API Key verification failed"
    assert api_auth_token.username == "apiuser", "API Key username mismatch"
    print("✓ API Key verified")

    # 測試請求認證
    headers = {"Authorization": f"Bearer {token}"}
    authenticated = auth.authenticate(headers)
    assert authenticated is not None, "Request authentication failed"
    print("✓ Request authentication works")

    print("✅ Authenticator tests passed")


def test_rate_limiter():
    """測試速率限制器"""
    print("\n=== Test Rate Limiter ===")

    config = {
        "rate_limiting": {
            "enabled": True,
            "default_limit": 10,  # 每分鐘10個請求（用於測試）
            "burst": 5,
        }
    }

    limiter = RateLimiter(config)

    # 測試速率限制
    client_id = "test-client"
    route = "default"

    # 前5個請求應該成功（burst容量）
    success_count = 0
    for i in range(7):
        allowed, limit_info = limiter.check_rate_limit(client_id, route)
        if allowed:
            success_count += 1

    assert success_count == 5, f"Expected 5 successful requests, got {success_count}"
    print(f"✓ Burst capacity works (allowed {success_count}/7 requests)")

    # 測試限制信息
    _, limit_info = limiter.check_rate_limit(client_id, route)
    assert "limit" in limit_info, "Limit info missing 'limit'"
    assert "remaining" in limit_info, "Limit info missing 'remaining'"
    assert "reset" in limit_info, "Limit info missing 'reset'"
    print("✓ Limit info provided")

    # 測試路由特定限制
    limiter.set_route_limit("/api/v1/special", limit=20, burst=10)
    allowed, _ = limiter.check_rate_limit("another-client", "/api/v1/special")
    assert allowed, "Special route limit failed"
    print("✓ Route-specific limits work")

    # 測試重置
    limiter.reset_client_limits(client_id)
    allowed, _ = limiter.check_rate_limit(client_id, route)
    assert allowed, "Client limit reset failed"
    print("✓ Client limit reset works")

    # 測試統計
    stats = limiter.get_stats()
    assert "enabled" in stats, "Stats missing 'enabled'"
    assert "total_clients" in stats, "Stats missing 'total_clients'"
    print(f"✓ Stats: {stats}")

    # 清理
    limiter.stop_cleanup()

    print("✅ Rate Limiter tests passed")


def test_gateway():
    """測試完整網關"""
    print("\n=== Test Gateway ===")

    config = {
        "routes": [
            {
                "path": "/api/v1/test/*",
                "platform": "test-platform",
                "service": "test-service",
                "methods": ["GET", "POST"],
                "timeout": 30,
                "authentication": "optional",
            }
        ],
        "authentication": {
            "jwt": {"enabled": True, "secret": "test-secret", "algorithm": "HS256"}
        },
        "rate_limiting": {"enabled": True, "default_limit": 100, "burst": 10},
        "logging": {"level": "WARNING"},  # Reduce log noise in tests
    }

    gateway = Gateway(config)

    # 測試未認證請求（authentication: optional）
    status, headers, body = gateway.handle_request(
        method="GET", path="/api/v1/test/hello", headers={}, client_ip="127.0.0.1"
    )

    assert status == 200, f"Expected 200, got {status}"
    print("✓ Unauthenticated request works")

    # 測試認證請求
    token = gateway.authenticator.generate_jwt("user1", "testuser", ["user"])
    status, headers, body = gateway.handle_request(
        method="GET",
        path="/api/v1/test/hello",
        headers={"Authorization": f"Bearer {token}"},
        client_ip="127.0.0.1",
    )

    assert status == 200, f"Expected 200, got {status}"
    assert "X-RateLimit-Limit" in headers, "Rate limit headers missing"
    print("✓ Authenticated request works")

    # 測試不存在的路由
    status, headers, body = gateway.handle_request(
        method="GET", path="/api/v1/nonexistent", headers={}, client_ip="127.0.0.1"
    )

    assert status == 404, f"Expected 404, got {status}"
    print("✓ 404 for non-existent route")

    # 測試方法不允許
    status, headers, body = gateway.handle_request(
        method="DELETE", path="/api/v1/test/hello", headers={}, client_ip="127.0.0.1"
    )

    assert status == 404, f"Expected 404 for unsupported method, got {status}"
    print("✓ Unsupported method rejected")

    # 測試統計
    stats = gateway.get_stats()
    assert "routes" in stats, "Stats missing 'routes'"
    assert "rate_limiter" in stats, "Stats missing 'rate_limiter'"
    print(f"✓ Gateway stats: {stats}")

    print("✅ Gateway tests passed")


def test_integration():
    """集成測試"""
    print("\n=== Integration Test ===")

    config = {
        "routes": [
            {
                "path": "/api/v1/public/*",
                "platform": "public",
                "service": "public-api",
                "methods": ["GET"],
                "authentication": "none",
            },
            {
                "path": "/api/v1/protected/*",
                "platform": "protected",
                "service": "protected-api",
                "methods": ["GET", "POST"],
                "authentication": "required",
            },
        ],
        "authentication": {"jwt": {"enabled": True, "secret": "integration-secret"}},
        "rate_limiting": {
            "enabled": True,
            "default_limit": 60,  # 每分鐘60個請求
            "burst": 10,  # Burst容量10
            "per_route": {"/api/v1/public/*": 120},  # 公共路由更高限制
        },
        "logging": {"level": "ERROR"},
    }

    gateway = Gateway(config)

    # 1. 公共路由（無需認證）
    status, _, _ = gateway.handle_request(
        "GET", "/api/v1/public/info", {}, client_ip="1.1.1.1"
    )
    assert status == 200, "Public route failed"
    print("✓ Public route accessible")

    # 2. 受保護路由（需要認證）
    status, _, body = gateway.handle_request(
        "GET", "/api/v1/protected/data", {}, client_ip="1.1.1.1"
    )
    assert status == 401, "Protected route should require auth"
    print("✓ Protected route requires authentication")

    # 3. 帶認證的受保護路由
    token = gateway.authenticator.generate_jwt("user1", "testuser", ["user"])
    status, headers, _ = gateway.handle_request(
        "GET",
        "/api/v1/protected/data",
        {"Authorization": f"Bearer {token}"},
        client_ip="1.1.1.1",
    )
    assert status == 200, "Authenticated request failed"
    assert "X-RateLimit-Limit" in headers, "Rate limit headers missing"
    print("✓ Protected route accessible with auth")

    # 4. 測試速率限制
    client_ip = "2.2.2.2"
    requests_allowed = 0

    for i in range(5):
        status, _, _ = gateway.handle_request(
            "GET",
            "/api/v1/protected/data",
            {"Authorization": f"Bearer {token}"},
            client_ip=client_ip,
        )
        if status == 200:
            requests_allowed += 1

    # 應該允許所有請求（burst容量足夠）
    assert (
        requests_allowed >= 3
    ), f"Expected at least 3 requests, got {requests_allowed}"
    print(f"✓ Rate limiting works ({requests_allowed}/5 requests allowed)")

    # 5. 測試路由特定的速率限制
    public_requests = 0
    for i in range(12):
        status, _, _ = gateway.handle_request(
            "GET", "/api/v1/public/test", {}, client_ip="3.3.3.3"
        )
        if status == 200:
            public_requests += 1

    # 公共路由的限制應該更寬鬆
    assert (
        public_requests >= 10
    ), f"Public route rate limit too strict: {public_requests}"
    print(
        f"✓ Route-specific rate limits work ({public_requests}/12 public requests allowed)"
    )

    print("✅ Integration test passed")


def main():
    """運行所有測試"""
    print("\n" + "=" * 60)
    print("API Gateway System - Test Suite")
    print("=" * 60)

    try:
        test_router()
        test_authenticator()
        test_rate_limiter()
        test_gateway()
        test_integration()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60 + "\n")

        return 0

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
