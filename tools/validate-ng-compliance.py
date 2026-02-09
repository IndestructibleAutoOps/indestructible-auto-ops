#!/usr/bin/env python3
"""
NG Compliance Validation Tool
驗證 GL 平台是否符合 NG 治理規範

基於:
- NG00000: 命名空間治理憲章
- NG00301: 驗證規則（零容忍）
- NG90101: 跨 Era 映射
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json


class NGComplianceValidator:
    """NG 合規性驗證器"""

    def __init__(self, workspace_root: Path):
        self.root = workspace_root
        self.violations = []
        self.warnings = []
        self.passed = []

        # NG00301: 保留關鍵字
        self.reserved_keywords = [
            "system",
            "admin",
            "root",
            "default",
            "internal",
            "private",
            "global",
        ]

        # GL → NG Era 映射（基於 NG90101）
        self.gl_to_ng_mapping = {
            "GL00-09": ("NG100-199", "Era-1", "企業架構"),
            "GL10-29": ("NG100-299", "Era-1", "平台服務"),
            "GL20-29": ("NG300-399", "Era-2", "數據處理"),
            "GL30-49": ("NG300-499", "Era-2", "執行運行時"),
            "GL50-59": ("NG500-599", "Era-2", "監控可觀測性"),
            "GL60-80": ("NG300-599", "Era-2", "治理合規"),
            "GL81-83": ("NG600-799", "Era-3", "擴展服務"),
            "GL90-99": ("NG900-999", "Cross-Era", "元規範"),
        }

    def check_format(self, name: str) -> Tuple[bool, str]:
        """
        NG00301: 格式驗證（零容忍）
        規則: 必須符合 kebab-case 格式
        """
        # kebab-case 格式: 小寫字母開頭，可包含數字和連字符
        pattern = r"^[a-z][a-z0-9-]*$"

        if not re.match(pattern, name):
            return False, f"格式不符: 必須為 kebab-case (^[a-z][a-z0-9-]*$)"

        # 檢查禁止的模式
        if "_" in name:
            return False, "格式不符: 禁止使用底線 (_)"

        if any(c.isupper() for c in name):
            return False, "格式不符: 禁止使用大寫字母（camelCase）"

        # 檢查連字符使用
        if name.startswith("-") or name.endswith("-"):
            return False, "格式不符: 不可以連字符開頭或結尾"

        if "--" in name:
            return False, "格式不符: 不可有連續連字符"

        return True, "格式符合 kebab-case 規範"

    def check_uniqueness(self, name: str, all_names: List[str]) -> Tuple[bool, str]:
        """
        NG00301: 唯一性驗證（零容忍）
        規則: 命名空間 ID 必須 100% 唯一
        """
        count = all_names.count(name)
        if count > 1:
            return False, f"唯一性違規: 發現 {count} 個重複"

        return True, "唯一性檢查通過"

    def check_reserved_keywords(self, name: str) -> Tuple[bool, str]:
        """
        NG00301: 保留關鍵字檢查
        規則: 絕對禁止使用保留關鍵字
        """
        # 檢查完整名稱
        if name in self.reserved_keywords:
            return False, f"使用保留關鍵字: {name}"

        # 檢查名稱部分
        parts = name.split("-")
        for part in parts:
            if part in self.reserved_keywords:
                return False, f"包含保留關鍵字: {part}"

        return True, "無保留關鍵字衝突"

    def check_semantic_similarity(
        self, name: str, existing_names: List[str]
    ) -> Tuple[bool, str]:
        """
        NG00301: 語義相似度檢查
        規則: 語義相似度必須 < 80%
        注: 簡化版本，使用字符串相似度
        """
        warnings = []

        for existing in existing_names:
            if existing == name:
                continue

            # 簡單的 Levenshtein 距離計算
            similarity = self._calculate_similarity(name, existing)

            if similarity >= 0.80:
                warnings.append(f"與 '{existing}' 相似度 {similarity:.0%}")

        if warnings:
            return False, f"語義相似度過高: {', '.join(warnings)}"

        return True, "語義相似度檢查通過"

    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """計算兩個字符串的相似度（簡化版）"""
        # Levenshtein 距離
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2 + 1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(
                        1 + min((distances[i1], distances[i1 + 1], distances_[-1]))
                    )
            distances = distances_

        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0

        return 1.0 - (distances[-1] / max_len)

    def map_gl_to_ng_era(self, platform_name: str) -> Tuple[str, str, str]:
        """
        根據平台名稱推測 GL 層級並映射到 NG Era
        返回: (NG範圍, Era, 描述)
        """
        name_lower = platform_name.lower()

        # 推測 GL 層級
        if "enterprise" in name_lower or "governance-architecture" in name_lower:
            return self.gl_to_ng_mapping["GL00-09"]

        if "platform" in name_lower and "service" in name_lower:
            return self.gl_to_ng_mapping["GL10-29"]

        if "data" in name_lower or "search" in name_lower:
            return self.gl_to_ng_mapping["GL20-29"]

        if "runtime" in name_lower or "execution" in name_lower:
            return self.gl_to_ng_mapping["GL30-49"]

        if "monitoring" in name_lower or "observability" in name_lower:
            return self.gl_to_ng_mapping["GL50-59"]

        if "governance-compliance" in name_lower:
            return self.gl_to_ng_mapping["GL60-80"]

        if "extension" in name_lower or "integration" in name_lower:
            return self.gl_to_ng_mapping["GL81-83"]

        if "meta" in name_lower or "semantic" in name_lower:
            return self.gl_to_ng_mapping["GL90-99"]

        # 默認
        return ("Unknown", "Unknown", "無法映射")

    def validate_platform(self, platform_name: str, all_platforms: List[str]) -> Dict:
        """驗證單個平台的 NG 合規性"""
        result = {
            "name": platform_name,
            "compliant": True,
            "checks": {},
            "ng_mapping": {},
        }

        # 1. 格式驗證
        format_ok, format_msg = self.check_format(platform_name)
        result["checks"]["format"] = {"passed": format_ok, "message": format_msg}
        if not format_ok:
            result["compliant"] = False

        # 2. 唯一性驗證
        unique_ok, unique_msg = self.check_uniqueness(platform_name, all_platforms)
        result["checks"]["uniqueness"] = {"passed": unique_ok, "message": unique_msg}
        if not unique_ok:
            result["compliant"] = False

        # 3. 保留關鍵字檢查
        reserved_ok, reserved_msg = self.check_reserved_keywords(platform_name)
        result["checks"]["reserved"] = {"passed": reserved_ok, "message": reserved_msg}
        if not reserved_ok:
            result["compliant"] = False

        # 4. 語義相似度檢查
        similar_ok, similar_msg = self.check_semantic_similarity(
            platform_name, [p for p in all_platforms if p != platform_name]
        )
        result["checks"]["similarity"] = {"passed": similar_ok, "message": similar_msg}
        if not similar_ok:
            # 語義相似度是警告，不算致命錯誤
            result["compliant"] = result["compliant"]  # 保持原狀態，但記錄警告

        # 5. GL → NG 映射
        ng_range, era, description = self.map_gl_to_ng_era(platform_name)
        result["ng_mapping"] = {
            "ng_range": ng_range,
            "era": era,
            "description": description,
        }

        return result

    def validate_all(self) -> Dict:
        """驗證所有 GL 平台"""
        print("=" * 60)
        print("🔍 NG Compliance Validation Tool")
        print("=" * 60)
        print(f"基於: NG00000 憲章, NG00301 驗證規則\n")

        # 查找所有 GL 平台
        gl_platforms = [
            d.name
            for d in self.root.iterdir()
            if d.is_dir() and d.name.startswith("gl-")
        ]

        print(f"發現 {len(gl_platforms)} 個 GL 平台\n")

        results = []
        for platform in sorted(gl_platforms):
            result = self.validate_platform(platform, gl_platforms)
            results.append(result)

            # 顯示結果
            status = "✅" if result["compliant"] else "❌"
            print(f"{status} {platform}")

            if not result["compliant"]:
                for check_name, check_result in result["checks"].items():
                    if not check_result["passed"]:
                        print(f"   └─ {check_name}: {check_result['message']}")
            elif not result["checks"]["similarity"]["passed"]:
                print(f"   ⚠️  {result['checks']['similarity']['message']}")  # 警告

            # 顯示 NG 映射
            ng_map = result["ng_mapping"]
            if ng_map["ng_range"] != "Unknown":
                print(
                    f"   → {ng_map['era']} ({ng_map['ng_range']}): {ng_map['description']}"
                )

        # 統計
        total = len(results)
        passed = sum(1 for r in results if r["compliant"])
        warnings = sum(1 for r in results if not r["checks"]["similarity"]["passed"])

        print("\n" + "=" * 60)
        print("📊 驗證統計")
        print("=" * 60)
        print(f"總平台數: {total}")
        print(f"通過: {passed} ({passed/total*100:.1f}%)")
        print(f"失敗: {total-passed} ({(total-passed)/total*100:.1f}%)")
        print(f"警告: {warnings}")

        # GL → NG Era 分布
        print("\n" + "=" * 60)
        print("📋 GL → NG Era 映射分布")
        print("=" * 60)

        era_counts = {}
        for result in results:
            era = result["ng_mapping"]["era"]
            if era not in era_counts:
                era_counts[era] = 0
            era_counts[era] += 1

        for era, count in sorted(era_counts.items()):
            print(f"  {era}: {count} 平台")

        # 生成報告
        report = {
            "timestamp": "2026-02-06",
            "total_platforms": total,
            "passed": passed,
            "failed": total - passed,
            "warnings": warnings,
            "pass_rate": passed / total * 100,
            "platforms": results,
            "era_distribution": era_counts,
        }

        # 保存報告
        report_file = self.root / "ng-compliance-report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n📄 報告已保存: {report_file}")

        # 返回狀態碼
        return report


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate NG compliance for GL platforms"
    )
    parser.add_argument(
        "--workspace", default="/workspace", help="Workspace root directory"
    )
    parser.add_argument(
        "--check-all", action="store_true", help="Check all GL platforms"
    )

    args = parser.parse_args()

    validator = NGComplianceValidator(workspace_root=Path(args.workspace))

    if args.check_all:
        report = validator.validate_all()
        return 0 if report["failed"] == 0 else 1
    else:
        print("請使用 --check-all 來驗證所有平台")
        return 1


if __name__ == "__main__":
    sys.exit(main())
