#!/usr/bin/env python3
"""
NG Namespace Registry
命名空間註冊系統

NG Code: NG00103
Purpose: 管理所有命名空間的註冊、查詢、更新、歸檔
"""

import json
import yaml
import uuid
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class Era(Enum):
    """Era 定義"""

    ERA_1 = "era-1"  # 代碼層
    ERA_2 = "era-2"  # 微碼層
    ERA_3 = "era-3"  # 無碼層
    CROSS = "cross"  # 跨層級


class NamespaceStatus(Enum):
    """命名空間狀態"""

    PROPOSED = "proposed"
    APPROVED = "approved"
    REGISTERED = "registered"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    MIGRATING = "migrating"
    ARCHIVED = "archived"
    DESTROYED = "destroyed"


@dataclass
class NamespaceSpec:
    """命名空間規範"""

    namespace_id: str
    namespace_type: str
    era: Era
    domain: str
    component: str
    owner: str
    description: str
    version: str = "1.0.0"
    tags: List[str] = None
    metadata: Dict[str, Any] = None

    def to_dict(self) -> Dict:
        """轉換為字典"""
        data = asdict(self)
        data["era"] = self.era.value
        return data


@dataclass
class NamespaceRecord:
    """命名空間記錄"""

    id: str
    ng_code: str
    spec: NamespaceSpec
    status: NamespaceStatus
    created_at: str
    updated_at: str
    approved_by: Optional[str] = None
    audit_trail: List[Dict] = None

    def to_dict(self) -> Dict:
        """轉換為字典"""
        data = {
            "id": self.id,
            "ng_code": self.ng_code,
            "spec": self.spec.to_dict(),
            "status": self.status.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "approved_by": self.approved_by,
            "audit_trail": self.audit_trail or [],
        }
        return data


class NgNamespaceRegistry:
    """NG 命名空間註冊系統"""

    def __init__(self, registry_path: str = "registry/namespaces.json"):
        """初始化註冊系統"""
        self.registry_path = Path(registry_path)
        self.namespaces: Dict[str, NamespaceRecord] = {}
        self.ng_code_counter = {}
        self._load_registry()

    def _load_registry(self):
        """加載註冊表"""
        if not self.registry_path.exists():
            return

        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for ns_id, ns_data in data.get("namespaces", {}).items():
                # 重構記錄
                spec_data = ns_data["spec"]
                spec = NamespaceSpec(
                    namespace_id=spec_data["namespace_id"],
                    namespace_type=spec_data["namespace_type"],
                    era=Era(spec_data["era"]),
                    domain=spec_data["domain"],
                    component=spec_data["component"],
                    owner=spec_data["owner"],
                    description=spec_data["description"],
                    version=spec_data.get("version", "1.0.0"),
                    tags=spec_data.get("tags"),
                    metadata=spec_data.get("metadata"),
                )

                record = NamespaceRecord(
                    id=ns_data["id"],
                    ng_code=ns_data["ng_code"],
                    spec=spec,
                    status=NamespaceStatus(ns_data["status"]),
                    created_at=ns_data["created_at"],
                    updated_at=ns_data["updated_at"],
                    approved_by=ns_data.get("approved_by"),
                    audit_trail=ns_data.get("audit_trail", []),
                )

                self.namespaces[ns_id] = record

            print(f"✅ 已加載 {len(self.namespaces)} 個命名空間")

        except Exception as e:
            print(f"⚠️  加載註冊表失敗: {e}")

    def _save_registry(self):
        """保存註冊表"""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "metadata": {
                    "version": "3.0.0",
                    "updated_at": datetime.now().isoformat(),
                    "namespace_count": len(self.namespaces),
                },
                "namespaces": {
                    ns_id: record.to_dict() for ns_id, record in self.namespaces.items()
                },
            }

            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ 註冊表已保存: {self.registry_path}")
            return True

        except Exception as e:
            print(f"❌ 保存註冊表失敗: {e}")
            return False

    def register_namespace(self, spec: NamespaceSpec) -> str:
        """註冊命名空間

        Args:
            spec: 命名空間規範

        Returns:
            命名空間 ID
        """
        # 1. 驗證唯一性
        if self.check_conflict(spec.namespace_id):
            raise ValueError(f"命名空間衝突: {spec.namespace_id}")

        # 2. 生成 ID 和 NG 編碼
        namespace_id = self._generate_namespace_id(spec)
        ng_code = self._assign_ng_code(spec)

        # 3. 創建記錄
        record = NamespaceRecord(
            id=namespace_id,
            ng_code=ng_code,
            spec=spec,
            status=NamespaceStatus.REGISTERED,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            audit_trail=[
                {
                    "action": "registered",
                    "timestamp": datetime.now().isoformat(),
                    "ng_code": ng_code,
                }
            ],
        )

        # 4. 存儲
        self.namespaces[namespace_id] = record

        # 5. 保存
        self._save_registry()

        print(f"✅ 註冊命名空間: {spec.namespace_id} [{ng_code}]")

        return namespace_id

    def _generate_namespace_id(self, spec: NamespaceSpec) -> str:
        """生成命名空間 ID"""
        components = [spec.namespace_type, spec.era.value, spec.domain, spec.component]
        namespace_str = ".".join(components)

        # 使用 UUID 確保唯一性
        unique_id = str(uuid.uuid4())[:8]

        return f"{namespace_str}-{unique_id}"

    def _assign_ng_code(self, spec: NamespaceSpec) -> str:
        """分配 NG 編碼"""
        # 根據 Era 確定層級
        era_mapping = {Era.ERA_1: 100, Era.ERA_2: 300, Era.ERA_3: 600, Era.CROSS: 900}

        base_level = era_mapping.get(spec.era, 0)

        # 領域映射（簡化版）
        domain_map = {
            "platform": 0,
            "runtime": 1,
            "governance": 2,
            "data": 3,
            "security": 4,
        }

        domain_code = domain_map.get(spec.domain, 0)

        # 序列號（遞增）
        key = f"{base_level}_{domain_code}"
        if key not in self.ng_code_counter:
            self.ng_code_counter[key] = 0

        self.ng_code_counter[key] += 1
        sequence = self.ng_code_counter[key]

        # 組裝 NG 編碼
        ng_code = f"NG{base_level + domain_code * 10:03d}{sequence:02d}"

        return ng_code

    def check_conflict(self, namespace_id: str) -> bool:
        """檢查命名空間衝突"""
        return any(
            record.spec.namespace_id == namespace_id
            for record in self.namespaces.values()
        )

    def get_namespace(self, namespace_id: str) -> Optional[NamespaceRecord]:
        """取得命名空間"""
        for record in self.namespaces.values():
            if record.spec.namespace_id == namespace_id or record.id == namespace_id:
                return record
        return None

    def list_namespaces(
        self, era: Era = None, status: NamespaceStatus = None, domain: str = None
    ) -> List[NamespaceRecord]:
        """列出命名空間"""
        results = list(self.namespaces.values())

        if era:
            results = [r for r in results if r.spec.era == era]

        if status:
            results = [r for r in results if r.status == status]

        if domain:
            results = [r for r in results if r.spec.domain == domain]

        return results

    def update_namespace_status(
        self, namespace_id: str, new_status: NamespaceStatus, actor: str = "system"
    ) -> bool:
        """更新命名空間狀態"""
        record = self.get_namespace(namespace_id)

        if not record:
            print(f"❌ 命名空間不存在: {namespace_id}")
            return False

        # 記錄審計
        audit_entry = {
            "action": "status_change",
            "from": record.status.value,
            "to": new_status.value,
            "actor": actor,
            "timestamp": datetime.now().isoformat(),
        }

        # 更新狀態
        record.status = new_status
        record.updated_at = datetime.now().isoformat()
        record.audit_trail.append(audit_entry)

        # 保存
        self._save_registry()

        print(f"✅ 更新命名空間狀態: {namespace_id} → {new_status.value}")

        return True

    def get_statistics(self) -> Dict[str, Any]:
        """取得統計資訊"""
        stats = {
            "total": len(self.namespaces),
            "by_era": {},
            "by_status": {},
            "by_domain": {},
        }

        for record in self.namespaces.values():
            # Era 統計
            era_key = record.spec.era.value
            stats["by_era"][era_key] = stats["by_era"].get(era_key, 0) + 1

            # 狀態統計
            status_key = record.status.value
            stats["by_status"][status_key] = stats["by_status"].get(status_key, 0) + 1

            # 領域統計
            domain_key = record.spec.domain
            stats["by_domain"][domain_key] = stats["by_domain"].get(domain_key, 0) + 1

        return stats


if __name__ == "__main__":
    # 測試註冊系統
    registry = NgNamespaceRegistry()

    # 註冊範例命名空間
    example_spec = NamespaceSpec(
        namespace_id="pkg.era1.platform.core",
        namespace_type="package",
        era=Era.ERA_1,
        domain="platform",
        component="core",
        owner="platform-team",
        description="平台核心包命名空間",
    )

    try:
        ns_id = registry.register_namespace(example_spec)
        print(f"\n✅ 註冊成功: {ns_id}")

        # 查詢
        record = registry.get_namespace(ns_id)
        print(f"   NG Code: {record.ng_code}")
        print(f"   Status: {record.status.value}")

        # 統計
        stats = registry.get_statistics()
        print(f"\n📊 統計:")
        print(f"   總計: {stats['total']}")
        print(f"   Era-1: {stats['by_era'].get('era-1', 0)}")

    except Exception as e:
        print(f"❌ 測試失敗: {e}")
