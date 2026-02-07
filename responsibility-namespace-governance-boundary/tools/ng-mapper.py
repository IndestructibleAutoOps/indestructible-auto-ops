#!/usr/bin/env python3
"""
NG 命名空間映射器
NG Namespace Mapper

用途：實作 Era 間的精確映射轉換
模式：BINARY_EXECUTION（只返回 PASS 或 BLOCK）
"""

import re
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class Era(Enum):
    """Era 定義"""

    ERA_1 = "era1"
    ERA_2 = "era2"
    ERA_3 = "era3"
    CROSS = "cross"


class MappingResult(Enum):
    """映射結果（二元）"""

    PASS = "pass"
    BLOCK = "block"


@dataclass
class MappingRule:
    """映射規則"""

    source_pattern: str
    target_pattern: str
    transformation: str
    examples: List[Dict]


class NgMapper:
    """NG 命名空間映射器"""

    def __init__(self):
        """初始化映射器"""
        self.mappings = {}
        self._load_mapping_rules()
        print("🗺️  NG 映射器已初始化")

    def _load_mapping_rules(self):
        """載入映射規則"""
        # Era-1 → Era-2 映射規則
        self.mappings["era1_to_era2"] = {
            "pkg": {
                "pattern": r"pkg\.era1\.([a-z0-9-]+)\.([a-z0-9-]+)",
                "target": "svc.era2.{domain}.{component}",
                "type": "package → service",
            },
            "mod": {
                "pattern": r"mod\.era1\.([a-z0-9-]+)\.([a-z0-9-]+)",
                "target": "api.era2.{domain}.{component}",
                "type": "module → api",
            },
            "cls": {
                "pattern": r"cls\.era1\.([a-z0-9-]+)\.([a-z0-9-]+)",
                "target": "cmp.era2.{domain}.{component}",
                "type": "class → component",
            },
            "fn": {
                "pattern": r"fn\.era1\.([a-z0-9-]+)\.([a-z0-9-]+)",
                "target": "ep.era2.{domain}.{component}",
                "type": "function → endpoint",
            },
        }

        # Era-2 → Era-3 映射規則
        self.mappings["era2_to_era3"] = {
            "svc": {
                "pattern": r"svc\.era2\.([a-z0-9-]+)\.([a-z0-9-]+)",
                "target": "int.era3.{domain}.{component}",
                "type": "service → intent",
            },
            "api": {
                "pattern": r"api\.era2\.([a-z0-9-]+)\.([a-z0-9-]+)",
                "target": "sem.era3.{domain}.{component}",
                "type": "api → semantic",
            },
            "evt": {
                "pattern": r"evt\.era2\.([a-z0-9-]+)\.([a-z0-9-]+)",
                "target": "int.era3.{domain}.{component}",
                "type": "event → intent",
            },
            "stm": {
                "pattern": r"stm\.era2\.([a-z0-9-]+)\.([a-z0-9-]+)",
                "target": "neu.era3.{domain}.{component}",
                "type": "stream → neural",
            },
        }

        print(f"  ✓ 載入 {len(self.mappings['era1_to_era2'])} 個 Era-1→Era-2 規則")
        print(f"  ✓ 載入 {len(self.mappings['era2_to_era3'])} 個 Era-2→Era-3 規則")

    def map_namespace(self, source_namespace: str, target_era: Era) -> Dict[str, any]:
        """
        映射命名空間（二元執行）

        Args:
            source_namespace: 源命名空間
            target_era: 目標 Era

        Returns:
            {'result': 'pass', 'target_namespace': '...'} 或
            {'result': 'block', 'reason': '...'}
        """
        # 檢測源 Era
        source_era = self._detect_era(source_namespace)

        if not source_era:
            return {
                "result": MappingResult.BLOCK.value,
                "reason": f"無法檢測源命名空間 Era: {source_namespace}",
                "rule_code": "NG90101",
                "user_action": "命名空間必須包含 era1/era2/era3",
            }

        # 確定映射類型
        mapping_key = f"{source_era}_to_{target_era.value}"

        if mapping_key not in self.mappings:
            return {
                "result": MappingResult.BLOCK.value,
                "reason": f"不支援的映射: {source_era} → {target_era.value}",
                "rule_code": "NG90101",
                "supported_mappings": list(self.mappings.keys()),
                "user_action": "僅支援相鄰 Era 映射（era1→era2, era2→era3）",
            }

        # 執行映射
        mapping_rules = self.mappings[mapping_key]

        # 檢測源類型
        source_type = source_namespace.split(".")[0]

        if source_type not in mapping_rules:
            return {
                "result": MappingResult.BLOCK.value,
                "reason": f"不支援的源類型: {source_type}",
                "rule_code": "NG90101",
                "supported_types": list(mapping_rules.keys()),
                "user_action": f"支援的類型: {', '.join(mapping_rules.keys())}",
            }

        # 應用映射規則
        rule = mapping_rules[source_type]
        match = re.match(rule["pattern"], source_namespace)

        if not match:
            return {
                "result": MappingResult.BLOCK.value,
                "reason": f"源命名空間格式不符合規則: {source_namespace}",
                "rule_code": "NG90101",
                "expected_pattern": rule["pattern"],
                "user_action": "命名空間必須符合格式規範",
            }

        # 提取組件
        domain = match.group(1)
        component = match.group(2)

        # 生成目標命名空間
        target_namespace = rule["target"].format(domain=domain, component=component)

        # 驗證目標命名空間格式
        target_valid = self._validate_namespace_format(target_namespace)

        if not target_valid["valid"]:
            return {
                "result": MappingResult.BLOCK.value,
                "reason": f"生成的目標命名空間格式無效: {target_namespace}",
                "rule_code": "NG90101",
                "validation_error": target_valid["error"],
                "user_action": "映射規則可能有誤，請報告此問題",
            }

        # 映射成功（二元結果：PASS）
        return {
            "result": MappingResult.PASS.value,
            "source_namespace": source_namespace,
            "target_namespace": target_namespace,
            "source_era": source_era,
            "target_era": target_era.value,
            "transformation": rule["type"],
            "rule_code": "NG90101",
            "mapping_verified": True,
        }

    def _detect_era(self, namespace: str) -> Optional[str]:
        """檢測命名空間所屬 Era"""
        if ".era1." in namespace:
            return "era1"
        elif ".era2." in namespace:
            return "era2"
        elif ".era3." in namespace:
            return "era3"
        elif ".cross." in namespace:
            return "cross"
        return None

    def _validate_namespace_format(self, namespace: str) -> Dict[str, any]:
        """驗證命名空間格式"""
        pattern = (
            r"^[a-z][a-z0-9-]*\.(era[123]|cross)\.[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*$"
        )

        if re.match(pattern, namespace):
            return {"valid": True}
        else:
            return {"valid": False, "error": "格式不符合規範"}

    def batch_map(self, namespaces: List[str], target_era: Era) -> Dict[str, any]:
        """
        批量映射（二元執行）

        Returns:
            {'result': 'pass', 'mappings': [...]} 或
            {'result': 'block', 'reason': '...', 'failed_namespaces': [...]}
        """
        results = []
        failed = []

        for ns in namespaces:
            result = self.map_namespace(ns, target_era)

            if result["result"] == "pass":
                results.append(result)
            else:
                failed.append({"namespace": ns, "reason": result["reason"]})

        # 二元決策：任何失敗 = 整個批次 BLOCK
        if failed:
            return {
                "result": MappingResult.BLOCK.value,
                "reason": f"{len(failed)} 個命名空間映射失敗",
                "failed_namespaces": failed,
                "rule_code": "NG90101",
                "user_action": "修復失敗的命名空間後重新提交整個批次",
            }

        return {
            "result": MappingResult.PASS.value,
            "total_mapped": len(results),
            "mappings": results,
            "rule_code": "NG90101",
        }

    def generate_mapping_report(self) -> str:
        """生成映射報告"""
        lines = ["=" * 70, "NG 命名空間映射器", "=" * 70, f"載入的映射規則:", ""]

        for mapping_name, rules in self.mappings.items():
            lines.append(f"{mapping_name}:")
            for source_type, rule in rules.items():
                lines.append(f"  {source_type} → {rule['type']}")

        lines.extend(["", "=" * 70])

        return "\n".join(lines)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("NG 命名空間映射器測試")
    print("=" * 70)

    mapper = NgMapper()

    # 測試 Era-1 → Era-2 映射
    print("\n測試 1: Era-1 → Era-2 映射")
    print("-" * 70)

    test_cases_e1_e2 = [
        "pkg.era1.platform.core",
        "mod.era1.runtime.executor",
        "cls.era1.governance.enforcer",
        "fn.era1.registry.register",
    ]

    for ns in test_cases_e1_e2:
        result = mapper.map_namespace(ns, Era.ERA_2)

        if result["result"] == "pass":
            print(f"✅ {ns}")
            print(f"   → {result['target_namespace']}")
            print(f"   轉換: {result['transformation']}")
        else:
            print(f"🚫 {ns}")
            print(f"   原因: {result['reason']}")
        print()

    # 測試 Era-2 → Era-3 映射
    print("測試 2: Era-2 → Era-3 映射")
    print("-" * 70)

    test_cases_e2_e3 = [
        "svc.era2.platform.deployment",
        "api.era2.runtime.execute",
        "evt.era2.registry.updated",
        "stm.era2.data.pipeline",
    ]

    for ns in test_cases_e2_e3:
        result = mapper.map_namespace(ns, Era.ERA_3)

        if result["result"] == "pass":
            print(f"✅ {ns}")
            print(f"   → {result['target_namespace']}")
            print(f"   轉換: {result['transformation']}")
        else:
            print(f"🚫 {ns}")
            print(f"   原因: {result['reason']}")
        print()

    # 測試批量映射
    print("測試 3: 批量映射（二元執行）")
    print("-" * 70)

    batch_namespaces = [
        "pkg.era1.platform.core",
        "pkg.era1.runtime.engine",
        "pkg.era1.governance.system",
    ]

    batch_result = mapper.batch_map(batch_namespaces, Era.ERA_2)

    print(f"結果: {batch_result['result'].upper()}")
    if batch_result["result"] == "pass":
        print(f"映射數: {batch_result['total_mapped']}")
        for mapping in batch_result["mappings"]:
            print(f"  ✅ {mapping['source_namespace']} → {mapping['target_namespace']}")
    else:
        print(f"原因: {batch_result['reason']}")

    # 測試錯誤情況（驗證二元執行）
    print("\n測試 4: 錯誤情況（驗證 BLOCK）")
    print("-" * 70)

    error_cases = [
        ("INVALID.format", Era.ERA_2),
        ("pkg.era1.platform", Era.ERA_2),  # 格式不完整
        ("pkg.era1.platform.core", Era.ERA_3),  # 跨越 Era
    ]

    for ns, target_era in error_cases:
        result = mapper.map_namespace(ns, target_era)

        if result["result"] == "block":
            print(f"🚫 {ns} → {target_era.value}")
            print(f"   原因: {result['reason']}")
            print(f"   ✅ 正確 BLOCK")
        else:
            print(f"❌ {ns} 應該被 BLOCK 但沒有")
        print()

    # 生成報告
    print(mapper.generate_mapping_report())

    print("\n" + "=" * 70)
    print("✅ NG 映射器測試完成")
    print("   所有映射都是二元結果（PASS 或 BLOCK）")
    print("=" * 70)
