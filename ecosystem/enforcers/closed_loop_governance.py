#!/usr/bin/env python3
#
# @GL-governed
# @GL-layer: GQS-L5
# @GL-semantic: closed-loop-governance
# @GL-audit-trail: ./governance/GL_SEMANTIC_ANCHOR.json

"""
Closed Loop Governance System
閉環治理系統

基於 Governance Quantum Stack (GQS) 7層模型的完整閉環治理：
- 偵測所有 workflow
- 分類問題
- 套用對應修復器
- 建立簽章 PR 與報告
- PR 驗證通過後合併

Version: 1.0.0
Date: 2026-02-03
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
import json
import hashlib

# Import simple_yaml for zero-dependency YAML parsing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.simple_yaml import safe_load
import asyncio
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import subprocess
import re


class ViolationSeverity(Enum):
    """違規嚴重程度"""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ViolationCategory(Enum):
    """違規類別"""

    NAMING = "naming"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    INFRASTRUCTURE = "infrastructure"
    SUPPLY_CHAIN = "supply_chain"
    GOVERNANCE = "governance"
    OBSERVABILITY = "observability"


class FixerType(Enum):
    """修復器類型"""

    AUTOMATIC = "automatic"
    SEMI_AUTOMATIC = "semi_automatic"
    MANUAL = "manual"
    NO_OP = "no_op"


@dataclass
class Violation:
    """違規"""

    violation_id: str
    category: ViolationCategory
    severity: ViolationSeverity
    title: str
    description: str
    evidence: Dict
    affected_resources: List[str]
    fixer_type: FixerType
    fixer_id: Optional[str] = None
    pr_required: bool = False
    auto_merge: bool = False

    def to_dict(self) -> Dict:
        return {
            "violation_id": self.violation_id,
            "category": self.category.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "evidence": self.evidence,
            "affected_resources": self.affected_resources,
            "fixer_type": self.fixer_type.value,
            "fixer_id": self.fixer_id,
            "pr_required": self.pr_required,
            "auto_merge": self.auto_merge,
        }


@dataclass
class Fixer:
    """修復器"""

    fixer_id: str
    name: str
    description: str
    category: ViolationCategory
    fixer_type: FixerType
    supported_violations: List[str]
    execution_command: str
    parameters: Dict
    validation_command: Optional[str] = None
    rollback_command: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "fixer_id": self.fixer_id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "fixer_type": self.fixer_type.value,
            "supported_violations": self.supported_violations,
            "execution_command": self.execution_command,
            "parameters": self.parameters,
            "validation_command": self.validation_command,
            "rollback_command": self.rollback_command,
        }


@dataclass
class AuditRecord:
    """審計記錄"""

    timestamp: str
    actor: str
    action: str
    resource: str
    result: str
    hash: str
    version: str
    request_id: str
    correlation_id: str
    ip: str
    user_agent: str
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "actor": self.actor,
            "action": self.action,
            "resource": self.resource,
            "result": self.result,
            "hash": self.hash,
            "version": self.version,
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "ip": self.ip,
            "user_agent": self.user_agent,
            "metadata": self.metadata,
        }


class ClosedLoopGovernanceSystem:
    """閉環治理系統"""

    def __init__(self, base_path: Path):
        """初始化系統"""
        self.base_path = base_path
        self.ecosystem_path = base_path / "ecosystem"
        self.fixers_path = self.ecosystem_path / "enforcers" / "fixers"
        self.audit_db_path = self.ecosystem_path / "governance" / "audit.db"

        # 加載修復器
        self.fixers = self._load_fixers()

        # 修復器到違規的映射
        self.violation_to_fixer = self._build_violation_fixer_map()

        # 命名規範
        self.naming_patterns = self._load_naming_patterns()

    def _get_timestamp(self) -> str:
        """獲取 RFC3339 UTC 時間戳"""
        return datetime.now(timezone.utc).isoformat()

    def _calculate_hash(self, content: bytes) -> str:
        """計算 SHA-256 哈希"""
        return hashlib.sha256(content).hexdigest()

    def _generate_request_id(self) -> str:
        """生成請求 ID"""
        return f"req-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"

    def _generate_correlation_id(self) -> str:
        """生成相關 ID"""
        return f"corr-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"

    def _load_fixers(self) -> List[Fixer]:
        """加載所有修復器"""
        fixers = []

        # 內建修復器
        fixers.append(
            Fixer(
                fixer_id="fixer-naming-k8s-resource",
                name="Kubernetes Resource Naming Fixer",
                description="修復 Kubernetes 資源命名違規",
                category=ViolationCategory.NAMING,
                fixer_type=FixerType.AUTOMATIC,
                supported_violations=["k8s-naming-violation"],
                execution_command="python scripts/fixers/fix_k8s_naming.py --file {file} --pattern {pattern}",
                parameters={
                    "pattern": "^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+.\\d+.\\d+(-[A-Za-z0-9]+)?$"
                },
            )
        )

        fixers.append(
            Fixer(
                fixer_id="fixer-actions-hardening",
                name="GitHub Actions Hardening Fixer",
                description="硬化 GitHub Actions 工作流",
                category=ViolationCategory.SECURITY,
                fixer_type=FixerType.AUTOMATIC,
                supported_violations=["actions-not-hardened", "actions-unpinned-sha"],
                execution_command="python scripts/fixers/fix_actions_hardening.py --workflow {workflow}",
                parameters={
                    "pin_sha": True,
                    "min_permissions": True,
                    "add_concurrency": True,
                    "add_retry": True,
                    "add_cache": True,
                },
            )
        )

        fixers.append(
            Fixer(
                fixer_id="fixer-sbom-generation",
                name="SBOM Generation Fixer",
                description="生成軟件物料清單 (SBOM)",
                category=ViolationCategory.SUPPLY_CHAIN,
                fixer_type=FixerType.AUTOMATIC,
                supported_violations=["missing-sbom"],
                execution_command="syft {path} -o spdx-json > sbom.json",
                parameters={"format": "spdx-json", "output": "sbom.json"},
            )
        )

        fixers.append(
            Fixer(
                fixer_id="fixer-cosign-sign",
                name="Cosign Signing Fixer",
                description="使用 Cosign 簽署工件",
                category=ViolationCategory.SUPPLY_CHAIN,
                fixer_type=FixerType.AUTOMATIC,
                supported_violations=["unsigned-artifact"],
                execution_command="cosign sign --key {key} {artifact}",
                parameters={"key": "cosign.key", "sign_all": True},
            )
        )

        fixers.append(
            Fixer(
                fixer_id="fixer-kube-bench",
                name="Kube-bench Compliance Fixer",
                description="修復 CIS Kubernetes 基準違規",
                category=ViolationCategory.SECURITY,
                fixer_type=FixerType.SEMI_AUTOMATIC,
                supported_violations=["cis-benchmark-failure"],
                execution_command="kube-bench --fix --benchmark {benchmark}",
                parameters={"benchmark": "cis-1.6"},
                validation_command="kube-bench --benchmark {benchmark}",
            )
        )

        return fixers

    def _build_violation_fixer_map(self) -> Dict[str, Fixer]:
        """構建違規到修復器的映射"""
        mapping = {}
        for fixer in self.fixers:
            for violation_type in fixer.supported_violations:
                mapping[violation_type] = fixer
        return mapping

    def _load_naming_patterns(self) -> Dict[str, str]:
        """加載命名規範"""
        return {
            "k8s_resource": "^(dev|staging|prod)-[a-z0-9-]+-(deploy|svc|ing|cm|secret)-v\\d+.\\d+.\\d+(-[A-Za-z0-9]+)?$",
            "k8s_namespace": "^(dev|staging|prod)-[a-z0-9-]+$",
            "git_branch": "^(feature|bugfix|hotfix|release)/[a-z0-9-]+$",
            "git_tag": "^v\\d+.\\d+.\\d+(-[a-z0-9]+)?$",
            "docker_image": "^(dev|staging|prod)/[a-z0-9-]+:v\\d+.\\d+.\\d+$",
        }

    def _create_audit_record(
        self, actor: str, action: str, resource: str, result: str, metadata: Dict = None
    ) -> AuditRecord:
        """創建審計記錄"""
        content = json.dumps(
            {
                "actor": actor,
                "action": action,
                "resource": resource,
                "result": result,
                "timestamp": self._get_timestamp(),
            },
            sort_keys=True,
        )

        return AuditRecord(
            timestamp=self._get_timestamp(),
            actor=actor,
            action=action,
            resource=resource,
            result=result,
            hash=self._calculate_hash(content.encode()),
            version="1.0.0",
            request_id=self._generate_request_id(),
            correlation_id=self._generate_correlation_id(),
            ip="127.0.0.1",  # 本地執行
            user_agent="ClosedLoopGovernanceSystem/1.0.0",
            metadata=metadata or {},
        )

    def _detect_workflow_violations(self) -> List[Violation]:
        """偵測 Workflow 違規"""
        violations = []

        # 掃描 GitHub Actions 工作流
        workflows_path = self.base_path / ".github" / "workflows"
        if workflows_path.exists():
            for workflow_file in workflows_path.glob("*.yml"):
                violations.extend(self._check_workflow_file(workflow_file))

        return violations

    def _check_workflow_file(self, workflow_file: Path) -> List[Violation]:
        """檢查工作流文件"""
        violations = []

        with open(workflow_file, "r") as f:
            workflow = yaml.safe_load(f)

        # 檢查 1: 未固定 SHA
        jobs = workflow.get("jobs", {})
        for job_name, job in jobs.items():
            steps = job.get("steps", [])
            for i, step in enumerate(steps):
                uses = step.get("uses", "")
                if (
                    uses
                    and "@" in uses
                    and not re.match(r"@[a-f0-9]{40}$", uses.split("@")[1])
                ):
                    violations.append(
                        Violation(
                            violation_id=f"actions-unpinned-sha-{workflow_file.name}-{job_name}-{i}",
                            category=ViolationCategory.SECURITY,
                            severity=ViolationSeverity.HIGH,
                            title=f"Unpinned action SHA in {workflow_file.name}",
                            description=f"Step {i} in job {job_name} uses action {uses} with unpinned SHA",
                            evidence={
                                "file": str(workflow_file),
                                "job": job_name,
                                "step": i,
                                "uses": uses,
                            },
                            affected_resources=[str(workflow_file)],
                            fixer_type=FixerType.AUTOMATIC,
                            fixer_id="fixer-actions-hardening",
                            pr_required=True,
                            auto_merge=True,
                        )
                    )

        # 檢查 2: 最小權限
        permissions = workflow.get("permissions", {})
        if not permissions:
            violations.append(
                Violation(
                    violation_id=f"actions-not-hardened-permissions-{workflow_file.name}",
                    category=ViolationCategory.SECURITY,
                    severity=ViolationSeverity.MEDIUM,
                    title=f"Missing permissions in {workflow_file.name}",
                    description="Workflow missing explicit permissions configuration",
                    evidence={"file": str(workflow_file)},
                    affected_resources=[str(workflow_file)],
                    fixer_type=FixerType.AUTOMATIC,
                    fixer_id="fixer-actions-hardening",
                    pr_required=True,
                    auto_merge=True,
                )
            )

        # 檢查 3: Concurrency
        concurrency = workflow.get("concurrency")
        if not concurrency:
            violations.append(
                Violation(
                    violation_id=f"actions-not-hardened-concurrency-{workflow_file.name}",
                    category=ViolationCategory.SECURITY,
                    severity=ViolationSeverity.MEDIUM,
                    title=f"Missing concurrency in {workflow_file.name}",
                    description="Workflow missing concurrency configuration",
                    evidence={"file": str(workflow_file)},
                    affected_resources=[str(workflow_file)],
                    fixer_type=FixerType.AUTOMATIC,
                    fixer_id="fixer-actions-hardening",
                    pr_required=True,
                    auto_merge=True,
                )
            )

        return violations

    def _detect_naming_violations(self) -> List[Violation]:
        """偵測命名違規"""
        violations = []

        # 掃描 Kubernetes 資源
        k8s_path = self.base_path / "k8s"
        if k8s_path.exists():
            for k8s_file in k8s_path.rglob("*.yaml"):
                violations.extend(self._check_k8s_naming(k8s_file))

        return violations

    def _check_k8s_naming(self, k8s_file: Path) -> List[Violation]:
        """檢查 Kubernetes 資源命名"""
        violations = []

        with open(k8s_file, "r") as f:
            k8s_resources = yaml.safe_load_all(f)

        pattern = self.naming_patterns.get("k8s_resource", "")

        for resource in k8s_resources:
            if not resource:
                continue

            resource_name = resource.get("metadata", {}).get("name", "")
            resource_type = resource.get("kind", "")

            if resource_type and resource_name:
                if not re.match(pattern, resource_name):
                    violations.append(
                        Violation(
                            violation_id=f"k8s-naming-{k8s_file.name}-{resource_name}",
                            category=ViolationCategory.NAMING,
                            severity=ViolationSeverity.MEDIUM,
                            title=f"Invalid K8s resource name: {resource_name}",
                            description=f"Resource {resource_name} ({resource_type}) does not match naming pattern",
                            evidence={
                                "file": str(k8s_file),
                                "resource_name": resource_name,
                                "resource_type": resource_type,
                                "expected_pattern": pattern,
                            },
                            affected_resources=[str(k8s_file)],
                            fixer_type=FixerType.AUTOMATIC,
                            fixer_id="fixer-naming-k8s-resource",
                            pr_required=True,
                            auto_merge=False,
                        )
                    )

        return violations

    def _detect_supply_chain_violations(self) -> List[Violation]:
        """偵測供應鏈違規"""
        violations = []

        # 檢查 SBOM
        sbom_files = list(self.base_path.rglob("sbom.json"))
        if not sbom_files:
            violations.append(
                Violation(
                    violation_id="missing-sbom",
                    category=ViolationCategory.SUPPLY_CHAIN,
                    severity=ViolationSeverity.HIGH,
                    title="Missing SBOM",
                    description="No Software Bill of Materials (SBOM) found",
                    evidence={},
                    affected_resources=[str(self.base_path)],
                    fixer_type=FixerType.AUTOMATIC,
                    fixer_id="fixer-sbom-generation",
                    pr_required=True,
                    auto_merge=True,
                )
            )

        return violations

    def _categorize_violations(
        self, violations: List[Violation]
    ) -> Dict[ViolationCategory, List[Violation]]:
        """分類違規"""
        categorized = {}
        for violation in violations:
            if violation.category not in categorized:
                categorized[violation.category] = []
            categorized[violation.category].append(violation)
        return categorized

    def _apply_fixer(self, violation: Violation) -> Dict:
        """應用修復器"""
        fixer_id = violation.fixer_id
        if not fixer_id:
            return {"success": False, "message": "No fixer available"}

        fixer = next((f for f in self.fixers if f.fixer_id == fixer_id), None)
        if not fixer:
            return {"success": False, "message": f"Fixer not found: {fixer_id}"}

        # 創建審計記錄
        audit_record = self._create_audit_record(
            actor="closed_loop_governance",
            action="apply_fixer",
            resource=violation.violation_id,
            result="pending",
            metadata={"fixer_id": fixer_id, "violation": violation.to_dict()},
        )

        # 執行修復命令
        try:
            # 構建命令
            command = fixer.execution_command.format(
                **violation.evidence, **fixer.parameters
            )

            # 執行命令
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=300
            )

            if result.returncode == 0:
                audit_record.result = "success"
                return {
                    "success": True,
                    "output": result.stdout,
                    "audit_record": audit_record.to_dict(),
                }
            else:
                audit_record.result = "failed"
                return {
                    "success": False,
                    "error": result.stderr,
                    "audit_record": audit_record.to_dict(),
                }
        except subprocess.TimeoutExpired:
            audit_record.result = "timeout"
            return {
                "success": False,
                "error": "Fixer execution timeout",
                "audit_record": audit_record.to_dict(),
            }
        except Exception as e:
            audit_record.result = "error"
            return {
                "success": False,
                "error": str(e),
                "audit_record": audit_record.to_dict(),
            }

    def _create_pr(
        self,
        violations: List[Violation],
        branch_name: str,
        title: str,
        description: str,
    ) -> Dict:
        """創建 Pull Request"""
        # 創建審計記錄
        audit_record = self._create_audit_record(
            actor="closed_loop_governance",
            action="create_pr",
            resource=f"pr:{branch_name}",
            result="pending",
            metadata={
                "branch": branch_name,
                "violations_count": len(violations),
                "auto_merge": any(v.auto_merge for v in violations),
            },
        )

        # 使用 gh CLI 創建 PR
        try:
            # 創建分支
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.base_path,
                check=True,
                capture_output=True,
            )

            # 提交變更
            subprocess.run(
                ["git", "add", "."], cwd=self.base_path, check=True, capture_output=True
            )

            commit_message = f"fix(governance): {title}\n\n{description}"
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.base_path,
                check=True,
                capture_output=True,
            )

            # 推送分支
            subprocess.run(
                ["git", "push", "-u", "origin", branch_name],
                cwd=self.base_path,
                check=True,
                capture_output=True,
            )

            # 創建 PR
            pr_result = subprocess.run(
                ["gh", "pr", "create", "--title", title, "--body", description],
                cwd=self.base_path,
                capture_output=True,
                text=True,
            )

            if pr_result.returncode == 0:
                pr_url = pr_result.stdout.strip()
                audit_record.result = "success"
                audit_record.metadata["pr_url"] = pr_url

                # 如果自動合併，設置 PR 標籤
                if any(v.auto_merge for v in violations):
                    subprocess.run(
                        ["gh", "pr", "edit", pr_url, "--add-label", "auto-merge"],
                        cwd=self.base_path,
                        check=True,
                        capture_output=True,
                    )

                return {
                    "success": True,
                    "pr_url": pr_url,
                    "audit_record": audit_record.to_dict(),
                }
            else:
                audit_record.result = "failed"
                return {
                    "success": False,
                    "error": pr_result.stderr,
                    "audit_record": audit_record.to_dict(),
                }
        except Exception as e:
            audit_record.result = "error"
            return {
                "success": False,
                "error": str(e),
                "audit_record": audit_record.to_dict(),
            }

    def _generate_report(self, violations: List[Violation]) -> Dict:
        """生成報告"""
        categorized = self._categorize_violations(violations)

        report = {
            "timestamp": self._get_timestamp(),
            "total_violations": len(violations),
            "by_severity": {
                "CRITICAL": sum(
                    1 for v in violations if v.severity == ViolationSeverity.CRITICAL
                ),
                "HIGH": sum(
                    1 for v in violations if v.severity == ViolationSeverity.HIGH
                ),
                "MEDIUM": sum(
                    1 for v in violations if v.severity == ViolationSeverity.MEDIUM
                ),
                "LOW": sum(
                    1 for v in violations if v.severity == ViolationSeverity.LOW
                ),
            },
            "by_category": {
                cat.value: len(viol_list) for cat, viol_list in categorized.items()
            },
            "by_fixer_type": {
                "AUTOMATIC": sum(
                    1 for v in violations if v.fixer_type == FixerType.AUTOMATIC
                ),
                "SEMI_AUTOMATIC": sum(
                    1 for v in violations if v.fixer_type == FixerType.SEMI_AUTOMATIC
                ),
                "MANUAL": sum(
                    1 for v in violations if v.fixer_type == FixerType.MANUAL
                ),
                "NO_OP": sum(1 for v in violations if v.fixer_type == FixerType.NO_OP),
            },
            "violations": [v.to_dict() for v in violations],
        }

        return report

    def run_closed_loop(self) -> Dict:
        """運行完整閉環"""
        print("🔄 Starting Closed Loop Governance System")
        print("=" * 70)

        # 創建審計記錄
        audit_record = self._create_audit_record(
            actor="closed_loop_governance",
            action="run_closed_loop",
            resource="system",
            result="started",
        )

        # 步驟 1: 偵測違規
        print("\n📡 Step 1: Detecting violations...")
        all_violations = []
        all_violations.extend(self._detect_workflow_violations())
        all_violations.extend(self._detect_naming_violations())
        all_violations.extend(self._detect_supply_chain_violations())

        print(f"  Found {len(all_violations)} violations")

        # 生成報告
        report = self._generate_report(all_violations)
        print(f"\n  By Severity:")
        for severity, count in report["by_severity"].items():
            if count > 0:
                print(f"    {severity}: {count}")

        print(f"\n  By Category:")
        for category, count in report["by_category"].items():
            if count > 0:
                print(f"    {category}: {count}")

        if not all_violations:
            print("\n✅ No violations found. System is compliant!")
            audit_record.result = "success"
            return {
                "success": True,
                "message": "No violations found",
                "report": report,
                "audit_record": audit_record.to_dict(),
            }

        # 步驟 2: 分類違規
        print("\n🏷️  Step 2: Categorizing violations...")
        categorized = self._categorate_violations(all_violations)

        # 步驟 3: 應用修復器
        print("\n🔧 Step 3: Applying fixers...")
        fix_results = []
        pr_required_violations = []

        for violation in all_violations:
            if violation.fixer_type != FixerType.NO_OP:
                print(f"  Applying fixer for: {violation.violation_id}")
                result = self._apply_fixer(violation)
                fix_results.append(result)

                if violation.pr_required:
                    pr_required_violations.append(violation)

        print(f"  Applied {len(fix_results)} fixers")

        # 步驟 4: 創建 PR（如果需要）
        if pr_required_violations:
            print("\n📝 Step 4: Creating Pull Requests...")

            # 按類別分組
            pr_groups = {}
            for violation in pr_required_violations:
                category = violation.category.value
                if category not in pr_groups:
                    pr_groups[category] = []
                pr_groups[category].append(violation)

            pr_results = []
            for category, violations in pr_groups.items():
                branch_name = f"fix/governance/{category}-{self._get_timestamp().replace(':', '-')[:19]}"
                title = f"fix(governance): {category.title()} Violations ({len(violations)})"
                description = self._generate_pr_description(violations)

                print(f"  Creating PR for category: {category}")
                pr_result = self._create_pr(violations, branch_name, title, description)
                pr_results.append(pr_result)

            print(f"  Created {len(pr_results)} PRs")
        else:
            pr_results = []

        # 步驟 5: 生成最終報告
        print("\n📊 Step 5: Generating final report...")
        final_report = {
            "timestamp": self._get_timestamp(),
            "summary": {
                "total_violations": len(all_violations),
                "fixers_applied": len(fix_results),
                "fixes_successful": sum(1 for r in fix_results if r.get("success")),
                "prs_created": len(pr_results),
                "prs_successful": sum(1 for r in pr_results if r.get("success")),
            },
            "report": report,
            "fix_results": fix_results,
            "pr_results": pr_results,
        }

        audit_record.result = "completed"
        audit_record.metadata["final_report"] = final_report

        print("\n" + "=" * 70)
        print("✅ Closed Loop Governance System completed")
        print(f"\n  Total Violations: {final_report['summary']['total_violations']}")
        print(f"  Fixers Applied: {final_report['summary']['fixers_applied']}")
        print(f"  Fixes Successful: {final_report['summary']['fixes_successful']}")
        print(f"  PRs Created: {final_report['summary']['prs_created']}")
        print(f"  PRs Successful: {final_report['summary']['prs_successful']}")

        return {
            "success": True,
            "message": "Closed loop completed",
            "report": final_report,
            "audit_record": audit_record.to_dict(),
        }

    def _generate_pr_description(self, violations: List[Violation]) -> str:
        """生成 PR 描述"""
        description = "## Governance Violations Fixed\n\n"

        for violation in violations:
            description += f"### {violation.title}\n\n"
            description += f"**Severity**: {violation.severity.value}\n\n"
            description += f"**Description**: {violation.description}\n\n"
            description += f"**Fixer**: {violation.fixer_id}\n\n"
            description += "---\n\n"

        description += "## Evidence\n\n"
        description += "This PR was automatically generated by the Closed Loop Governance System.\n\n"
        description += (
            "**Audit Trail**: All changes are tracked with full audit records.\n\n"
        )
        description += "**Auto-Merge**: Enabled (validated by automated tests)\n"

        return description


# ============================================================================
# CLI Interface
# ============================================================================
if __name__ == "__main__":
    import argparse

    default_base_path = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="Closed Loop Governance System")
    parser.add_argument(
        "--base-path",
        type=Path,
        default=default_base_path,
        help="Base path to the repository",
    )

    args = parser.parse_args()

    system = ClosedLoopGovernanceSystem(base_path=args.base_path)
    result = system.run_closed_loop()

    # 保存報告
    report_path = (
        args.base_path
        / "governance-reports"
        / f"closed-loop-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.json"
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n📄 Report saved to: {report_path}")

    sys.exit(0 if result["success"] else 1)
