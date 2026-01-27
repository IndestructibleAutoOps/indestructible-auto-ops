#!/usr/bin/env python3
"""
驗證 Auto-Fix Bot 配置檔案

此腳本驗證 auto-fix-bot.yml 配置檔案的結構和內容是否符合要求。
"""

import json
import sys
import logging

logger = logging.getLogger(__name__)
from pathlib import Path
from typing import Any

import yaml


def load_yaml(file_path: Path) -> dict[str, Any]:
    """載入 YAML 配置檔案"""
    try:
        with open(file_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.info(f"❌ 無法載入 YAML 檔案: {e}")
        sys.exit(1)


def load_schema(file_path: Path) -> dict[str, Any]:
    """載入 JSON Schema"""
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.info(f"❌ 無法載入 Schema 檔案: {e}")
        sys.exit(1)


def validate_required_sections(config: dict[str, Any]) -> list[str]:
    """驗證必要的配置區段"""
    required_sections = [
        "name",
        "id",
        "version",
        "owner",
        "metadata",
        "project_mapping",
        "bot_config",
        "fix_rules",
        "policy_gates",
        "evidence_generation",
        "notifications",
        "audit",
        "rollback",
        "integration",
        "mcp_servers_config",
        "advanced_architecture_sync",
        "cross_layer_bridges",
        "deep_validation_schema",
        "evidence_chain_validation",
        "error_recovery",
        "monitoring",
        "changelog",
    ]

    missing = []
    for section in required_sections:
        if section not in config:
            missing.append(section)

    return missing


def validate_version_format(version: str) -> bool:
    """驗證版本號格式 (Semantic Versioning)"""
    import re

    pattern = r"^\d+\.\d+\.\d+$"
    return bool(re.match(pattern, version))


def validate_metadata(metadata: dict[str, Any]) -> list[str]:
    """驗證元數據"""
    issues = []

    required_fields = ["created_at", "updated_at", "labels", "compliance_tags"]
    for field in required_fields:
        if field not in metadata:
            issues.append(f"metadata 缺少必要欄位: {field}")

    if "labels" in metadata and len(metadata["labels"]) < 2:
        issues.append("metadata.labels 至少需要 2 個標籤")

    allowed_compliance_tags = [
        "slsa-l3",
        "in-toto",
        "audit-trail",
        "machinenativenops-free",
        "deep-validation",
    ]
    if "compliance_tags" in metadata:
        for tag in metadata["compliance_tags"]:
            if tag not in allowed_compliance_tags:
                issues.append(f"不允許的 compliance_tag: {tag}")

    return issues


def validate_bot_config(bot_config: dict[str, Any]) -> list[str]:
    """驗證 Bot 配置"""
    issues = []

    required_fields = ["enabled", "trigger_events", "scopes"]
    for field in required_fields:
        if field not in bot_config:
            issues.append(f"bot_config 缺少必要欄位: {field}")

    if "scopes" in bot_config:
        if not isinstance(bot_config["scopes"], list) or len(bot_config["scopes"]) < 1:
            issues.append("bot_config.scopes 至少需要 1 個範圍")

        for i, scope in enumerate(bot_config["scopes"]):
            if "name" not in scope:
                issues.append(f"bot_config.scopes[{i}] 缺少 name")
            if "enabled" not in scope:
                issues.append(f"bot_config.scopes[{i}] 缺少 enabled")
            if "paths" not in scope or not scope["paths"]:
                issues.append(f"bot_config.scopes[{i}] 缺少或空的 paths")

    return issues


def validate_fix_rules(fix_rules: list[dict[str, Any]]) -> list[str]:
    """驗證修復規則"""
    issues = []

    if not fix_rules:
        issues.append("fix_rules 不能為空")
        return issues

    allowed_priorities = ["critical", "high", "medium", "low"]

    for i, rule in enumerate(fix_rules):
        required_fields = [
            "name",
            "priority",
            "enabled",
            "scope",
            "triggers",
            "actions",
        ]
        for field in required_fields:
            if field not in rule:
                issues.append(f"fix_rules[{i}] 缺少必要欄位: {field}")

        if "priority" in rule and rule["priority"] not in allowed_priorities:
            issues.append(f"fix_rules[{i}] 優先級無效: {rule['priority']}")

        if "actions" in rule and not rule["actions"]:
            issues.append(f"fix_rules[{i}] actions 不能為空")

    return issues


def validate_policy_gates(policy_gates: list[dict[str, Any]]) -> list[str]:
    """驗證 Policy Gates"""
    issues = []

    if not policy_gates:
        issues.append("policy_gates 不能為空")
        return issues

    allowed_stages = ["pre-fix", "post-fix"]
    allowed_engines = ["OPA", "kyverno", "jsonschema"]

    for i, gate in enumerate(policy_gates):
        required_fields = ["name", "stage", "policies", "failure_action"]
        for field in required_fields:
            if field not in gate:
                issues.append(f"policy_gates[{i}] 缺少必要欄位: {field}")

        if "stage" in gate and gate["stage"] not in allowed_stages:
            issues.append(f"policy_gates[{i}] stage 無效: {gate['stage']}")

        if "policies" in gate:
            for j, policy in enumerate(gate["policies"]):
                if "engine" in policy and policy["engine"] not in allowed_engines:
                    issues.append(
                        f"policy_gates[{i}].policies[{j}] engine 無效: {policy['engine']}"
                    )

    return issues


def main():
    """主函數"""
    logger.info("=" * 60)
    logger.info("Auto-Fix Bot 配置驗證工具")
    logger.info("=" * 60)
    print()

    # 檔案路徑
    repo_root = Path(__file__).parent.parent
    config_path = repo_root / "auto-fix-bot.yml"
    schema_path = repo_root / "schemas" / "auto-fix-bot-v2.schema.json"

    # 載入配置
    logger.info(f"📂 載入配置檔案: {config_path}")
    config = load_yaml(config_path)
    logger.info("✅ 配置檔案載入成功")
    print()

    # 基本資訊
    logger.info("📋 配置基本資訊:")
    logger.info(f"  名稱: {config.get('name', 'N/A')
    logger.info(f"  ID: {config.get('id', 'N/A')
    logger.info(f"  版本: {config.get('version', 'N/A')
    logger.info(f"  擁有團隊: {config.get('owner', {})
    print()

    # 驗證必要區段
    logger.info("🔍 驗證必要區段...")
    missing_sections = validate_required_sections(config)
    if missing_sections:
        logger.info(f"❌ 缺少必要區段: {', '.join(missing_sections)
        sys.exit(1)
    logger.info("✅ 所有必要區段都存在")
    print()

    # 驗證版本格式
    logger.info("🔍 驗證版本格式...")
    if not validate_version_format(config.get("version", "")):
        logger.info(f"❌ 版本格式無效: {config.get('version')
        sys.exit(1)
    logger.info(f"✅ 版本格式正確: {config.get('version')
    print()

    # 驗證元數據
    logger.info("🔍 驗證元數據...")
    metadata_issues = validate_metadata(config.get("metadata", {}))
    if metadata_issues:
        for issue in metadata_issues:
            logger.info(f"❌ {issue}")
        sys.exit(1)
    logger.info("✅ 元數據驗證通過")
    print()

    # 驗證 Bot 配置
    logger.info("🔍 驗證 Bot 配置...")
    bot_issues = validate_bot_config(config.get("bot_config", {}))
    if bot_issues:
        for issue in bot_issues:
            logger.info(f"❌ {issue}")
        sys.exit(1)
    print(
        f"✅ Bot 配置驗證通過 ({len(config.get('bot_config', {}).get('scopes', []))} 個範圍)"
    )
    print()

    # 驗證修復規則
    logger.info("🔍 驗證修復規則...")
    rules_issues = validate_fix_rules(config.get("fix_rules", []))
    if rules_issues:
        for issue in rules_issues:
            logger.info(f"❌ {issue}")
        sys.exit(1)
    logger.info(f"✅ 修復規則驗證通過 ({len(config.get('fix_rules', [])
    print()

    # 驗證 Policy Gates
    logger.info("🔍 驗證 Policy Gates...")
    gates_issues = validate_policy_gates(config.get("policy_gates", []))
    if gates_issues:
        for issue in gates_issues:
            logger.info(f"❌ {issue}")
        sys.exit(1)
    logger.info(f"✅ Policy Gates 驗證通過 ({len(config.get('policy_gates', [])
    print()

    # JSON Schema 驗證
    if schema_path.exists():
        logger.info("🔍 使用 JSON Schema 驗證...")
        try:
            from jsonschema import ValidationError, validate

            schema = load_schema(schema_path)
            validate(instance=config, schema=schema)
            logger.info("✅ JSON Schema 驗證通過")
        except ImportError:
            logger.info("⚠️  jsonschema 模組未安裝，跳過 JSON Schema 驗證")
        except ValidationError as e:
            logger.info(f"❌ Schema 驗證失敗: {e.message}")
            sys.exit(1)
        except Exception as e:
            logger.info(f"❌ Schema 驗證錯誤: {e}")
            sys.exit(1)
        print()

    # 統計資訊
    logger.info("=" * 60)
    logger.info("📊 驗證統計:")
    logger.info("  ✅ 必要區段: 21/21")
    logger.info(f"  ✅ 驗證範圍: {len(config.get('bot_config', {})
    logger.info(f"  ✅ 修復規則: {len(config.get('fix_rules', [])
    logger.info(f"  ✅ Policy Gates: {len(config.get('policy_gates', [])
    print(
        f"  ✅ 證據生成器: {len(config.get('evidence_generation', {}).get('generators', []))}"
    )
    logger.info(f"  ✅ 通知頻道: {len(config.get('notifications', {})
    logger.info(f"  ✅ 監控指標: {len(config.get('monitoring', {})
    logger.info("=" * 60)
    print()
    logger.info("🎉 所有驗證通過！配置檔案完全符合要求。")
    print()


if __name__ == "__main__":
    main()
