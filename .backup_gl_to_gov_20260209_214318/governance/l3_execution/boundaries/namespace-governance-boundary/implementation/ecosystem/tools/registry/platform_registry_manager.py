#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GL10-29
# @GL-semantic: registry
# @GL-audit-trail: ../../governance/GL_SEMANTIC_ANCHOR.json
#
"""
GL Platform Registry Manager
=============================
平台註冊表管理工具

GL Governance Layer: GL10-29 (Operational Layer)
"""

"""
Module docstring
================

This module is part of the GL governance framework.
Please add specific module documentation here.
"""
# MNGA-002: Import organization needs review
import os
import sys

# Import simple_yaml for zero-dependency YAML parsing
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from utils.simple_yaml import safe_load
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import argparse


class PlatformRegistryManager:
    """平台註冊表管理器"""

    def __init__(self, registry_path: Optional[str] = None):
        """
        初始化管理器

        Args:
            registry_path: 註冊表文件路徑
        """
        if registry_path is None:
            registry_path = (
                "ecosystem/registry/platform-registry/platform-manifest.yaml"
            )

        self.registry_path = Path(registry_path)
        self.platforms = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        """加載註冊表"""
        if not self.registry_path.exists():
            return {"platforms": []}

        try:
            with open(self.registry_path, "r") as f:
                data = safe_load(f)
                return data or {"platforms": []}
        except Exception as e:
            print(f"Error loading registry: {e}")
            return {"platforms": []}

    def _save_registry(self) -> bool:
        """保存註冊表"""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.registry_path, "w") as f:
                yaml.dump(
                    self.platforms, f, default_flow_style=False, allow_unicode=True
                )

            return True
        except Exception as e:
            print(f"Error saving registry: {e}")
            return False

    def register_platform(
        self,
        name: str,
        platform_type: str,
        version: str = "1.0.0",
        capabilities: Optional[List[str]] = None,
        governance_layers: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        註冊平台

        Args:
            name: 平台名稱
            platform_type: 平台類型（core, cloud, on-premise）
            version: 版本
            capabilities: 能力列表
            governance_layers: 治理層列表
            metadata: 元數據

        Returns:
            成功返回True
        """
        # 檢查是否已存在
        if self.get_platform(name):
            print(f"Platform already registered: {name}")
            return False

        # 創建平台條目
        platform = {
            "name": name,
            "type": platform_type,
            "version": version,
            "status": "active",
            "registered_at": datetime.utcnow().isoformat(),
            "capabilities": capabilities
            or ["service-discovery", "api-gateway", "messaging", "data-sync"],
            "governance": {
                "enabled": True,
                "layers": governance_layers
                or ["gov-enterprise-architecture", "gov-boundary-enforcement"],
            },
            "metadata": metadata or {},
        }

        # 添加到註冊表
        if "platforms" not in self.platforms:
            self.platforms["platforms"] = []

        self.platforms["platforms"].append(platform)

        # 保存
        if self._save_registry():
            print(f"✓ Platform registered: {name}")
            return True
        else:
            return False

    def unregister_platform(self, name: str) -> bool:
        """
        註銷平台

        Args:
            name: 平台名稱

        Returns:
            成功返回True
        """
        platforms_list = self.platforms.get("platforms", [])

        for i, platform in enumerate(platforms_list):
            if platform["name"] == name:
                platforms_list.pop(i)

                if self._save_registry():
                    print(f"✓ Platform unregistered: {name}")
                    return True
                else:
                    return False

        print(f"Platform not found: {name}")
        return False

    def get_platform(self, name: str) -> Optional[Dict[str, Any]]:
        """
        獲取平台信息

        Args:
            name: 平台名稱

        Returns:
            平台信息或None
        """
        platforms_list = self.platforms.get("platforms", [])

        for platform in platforms_list:
            if platform["name"] == name:
                return platform

        return None

    def list_platforms(
        self, platform_type: Optional[str] = None, status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        列出平台

        Args:
            platform_type: 平台類型過濾
            status: 狀態過濾

        Returns:
            平台列表
        """
        platforms_list = self.platforms.get("platforms", [])

        results = []
        for platform in platforms_list:
            if platform_type and platform.get("type") != platform_type:
                continue
            if status and platform.get("status") != status:
                continue

            results.append(platform)

        return results

    def update_platform_status(self, name: str, status: str) -> bool:
        """
        更新平台狀態

        Args:
            name: 平台名稱
            status: 新狀態（active, inactive, deprecated）

        Returns:
            成功返回True
        """
        platforms_list = self.platforms.get("platforms", [])

        for platform in platforms_list:
            if platform["name"] == name:
                platform["status"] = status
                platform["updated_at"] = datetime.utcnow().isoformat()

                if self._save_registry():
                    print(f"✓ Platform status updated: {name} -> {status}")
                    return True
                else:
                    return False

        print(f"Platform not found: {name}")
        return False

    def validate_platform(self, name: str) -> Dict[str, Any]:
        """
        驗證平台配置

        Args:
            name: 平台名稱

        Returns:
            驗證結果
        """
        platform = self.get_platform(name)

        if not platform:
            return {"valid": False, "errors": [f"Platform not found: {name}"]}

        errors = []
        warnings = []

        # 檢查必需字段
        required_fields = ["name", "type", "version", "status"]
        for field in required_fields:
            if field not in platform:
                errors.append(f"Missing required field: {field}")

        # 檢查命名規範
        if not platform["name"].startswith("gl."):
            warnings.append("Platform name should start with 'gl.'")

        if not platform["name"].endswith("-platform"):
            warnings.append("Platform name should end with '-platform'")

        # 檢查治理配置
        if "governance" not in platform:
            warnings.append("Missing governance configuration")
        elif not platform["governance"].get("enabled"):
            warnings.append("Governance not enabled")

        # 檢查能力
        if not platform.get("capabilities"):
            warnings.append("No capabilities defined")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

    def generate_report(self) -> str:
        """
        生成註冊表報告

        Returns:
            報告內容
        """
        platforms_list = self.platforms.get("platforms", [])

        report = []
        report.append("=" * 60)
        report.append("Platform Registry Report")
        report.append("=" * 60)
        report.append("")

        # 總體統計
        total = len(platforms_list)
        by_type = {}
        by_status = {}

        for platform in platforms_list:
            ptype = platform.get("type", "unknown")
            status = platform.get("status", "unknown")

            by_type[ptype] = by_type.get(ptype, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1

        report.append(f"Total Platforms: {total}")
        report.append("")

        report.append("By Type:")
        for ptype, count in by_type.items():
            report.append(f"  - {ptype}: {count}")
        report.append("")

        report.append("By Status:")
        for status, count in by_status.items():
            report.append(f"  - {status}: {count}")
        report.append("")

        # 平台詳情
        report.append("Registered Platforms:")
        report.append("-" * 60)

        for platform in platforms_list:
            report.append(f"\n{platform['name']}")
            report.append(f"  Type: {platform.get('type')}")
            report.append(f"  Version: {platform.get('version')}")
            report.append(f"  Status: {platform.get('status')}")

            if platform.get("capabilities"):
                report.append(f"  Capabilities: {', '.join(platform['capabilities'])}")

        report.append("")
        report.append("=" * 60)

        return "\n".join(report)


def main():
    """命令行工具"""
    parser = argparse.ArgumentParser(description="Platform Registry Manager")
    parser.add_argument(
        "--registry",
        default="ecosystem/registry/platform-registry/platform-manifest.yaml",
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Register command
    register_parser = subparsers.add_parser("register", help="Register a platform")
    register_parser.add_argument("--name", required=True, help="Platform name")
    register_parser.add_argument(
        "--type", required=True, choices=["core", "cloud", "on-premise"]
    )
    register_parser.add_argument("--version", default="1.0.0")

    # Unregister command
    unregister_parser = subparsers.add_parser(
        "unregister", help="Unregister a platform"
    )
    unregister_parser.add_argument("--name", required=True, help="Platform name")

    # List command
    list_parser = subparsers.add_parser("list", help="List platforms")
    list_parser.add_argument("--type", help="Filter by type")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a platform")
    validate_parser.add_argument("--name", required=True, help="Platform name")

    # Report command
    subparsers.add_parser("report", help="Generate registry report")

    args = parser.parse_args()

    # 創建管理器
    manager = PlatformRegistryManager(args.registry)

    # 執行命令
    if args.command == "register":
        manager.register_platform(args.name, args.type, args.version)

    elif args.command == "unregister":
        manager.unregister_platform(args.name)

    elif args.command == "list":
        platforms = manager.list_platforms(args.type, args.status)

        if args.json:
            print(json.dumps(platforms, indent=2))
        else:
            print(f"\nFound {len(platforms)} platforms:\n")
            for platform in platforms:
                print(
                    f"  - {platform['name']} ({platform['type']}) - {platform['status']}"
                )
            print()

    elif args.command == "validate":
        result = manager.validate_platform(args.name)

        print(f"\nValidation result for {args.name}:\n")
        print(f"  Valid: {result['valid']}")

        if result["errors"]:
            print(f"\n  Errors:")
            for error in result["errors"]:
                print(f"    - {error}")

        if result["warnings"]:
            print(f"\n  Warnings:")
            for warning in result["warnings"]:
                print(f"    - {warning}")
        print()

    elif args.command == "report":
        report = manager.generate_report()
        print(report)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
