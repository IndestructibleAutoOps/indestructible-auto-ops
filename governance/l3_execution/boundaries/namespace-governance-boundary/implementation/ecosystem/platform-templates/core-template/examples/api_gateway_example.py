#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: platform-templates
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
API Gateway Example
===================
示例：如何配置和使用 API Gateway
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from platform_manager import PlatformManager


def main():
    """API Gateway 示例"""
    print("\n=== API Gateway Example ===\n")

    # 1. 創建平台管理器
    pm = PlatformManager("configs/platform-config.yaml")
    print(f"✓ Platform Manager initialized: {pm.platform_name}\n")

    # 2. 註冊後端服務
    print("Registering backend service...\n")

    service_id = pm.register_service(
        name="backend-api",
        endpoint="http://localhost:9000",
        service_type="api",
        auto_health_check=False,
    )

    if service_id:
        print(f"✓ Backend service registered: {service_id}")

    # 3. 配置 API 路由
    print("\nConfiguring API routes...\n")

    routes = [
        {
            "path": "/api/v1/users/*",
            "service": "backend-api",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "authentication": "required",
            "timeout": 30,
        },
        {
            "path": "/api/v1/public/*",
            "service": "backend-api",
            "methods": ["GET"],
            "authentication": "none",
            "timeout": 10,
        },
    ]

    for route_config in routes:
        success = pm.add_route(**route_config)
        if success:
            print(f"✓ Route added: {route_config['path']}")

    # 4. 測試 API 請求
    print("\nTesting API requests...\n")

    if pm.gateway:
        # 公開路由（不需要認證）
        status, headers, body = pm.gateway.handle_request(
            method="GET", path="/api/v1/public/info", headers={}
        )

        print(f"Public route response:")
        print(f"  Status: {status}")
        print(f"  Body: {body}")

        # 生成 JWT token
        if pm.gateway.authenticator:
            token = pm.gateway.authenticator.generate_jwt(
                user_id="user123", username="testuser", roles=["user", "admin"]
            )

            print(f"\n✓ JWT token generated")

            # 受保護路由（需要認證）
            status, headers, body = pm.gateway.handle_request(
                method="GET",
                path="/api/v1/users/profile",
                headers={"Authorization": f"Bearer {token}"},
            )

            print(f"\nProtected route response:")
            print(f"  Status: {status}")
            print(f"  Rate Limit: {headers.get('X-RateLimit-Remaining', 'N/A')}")

    # 5. 查看網關統計
    print("\nGateway statistics:\n")

    if pm.gateway:
        stats = pm.gateway.get_stats()
        print(f"  Routes: {stats['routes']}")
        print(
            f"  Rate limiter active clients: {stats['rate_limiter']['total_clients']}"
        )

    print("\n✅ Example completed successfully!\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback

        traceback.print_exc()
        sys.exit(1)
