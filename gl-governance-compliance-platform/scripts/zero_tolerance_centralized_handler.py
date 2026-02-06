#!/usr/bin/env python3
"""
Zero-tolerance centralized violation handler.

Strict flow model:
  [internal] -> [external] -> [global] -> [cross-validate] -> [insight] -> (next loop)
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


FLOW_MODEL = ["internal", "external", "global", "cross-validate", "insight"]
TEAM_ENV = "IND_AUTOOPS_TEAM_TAG"

DEFAULT_REPORT_DIR = Path("/workspace/reports/zero-tolerance")
DEFAULT_REPO_ROOT = Path("/workspace")
DEFAULT_NG_SCRIPT = Path(
    "/workspace/gl-governance-compliance-platform/scripts/naming/ng_namespace_pipeline.py"
)
DEFAULT_BOUNDARY_SCRIPT = Path(
    "/workspace/gl-governance-compliance-platform/scripts/boundary_checker.py"
)
DEFAULT_NAMING_SCAN = Path(
    "/workspace/gl-governance-compliance-platform/scripts/scan_naming_violations.py"
)
DEFAULT_MARKER_SCAN = Path("/workspace/scan_files.py")
DEFAULT_FIX_NAMING = Path("/workspace/fix_naming_violations.py")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class StageResult:
    name: str
    status: str
    output: Optional[str] = None
    error: Optional[str] = None


def run_command(
    command: List[str],
    cwd: Optional[Path] = None,
    env: Optional[Dict[str, str]] = None,
    stdout_path: Optional[Path] = None,
    timeout: int = 600,
) -> str:
    if stdout_path:
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        with stdout_path.open("w", encoding="utf-8") as handle:
            result = subprocess.run(
                command,
                cwd=str(cwd) if cwd else None,
                env=env,
                stdout=handle,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout,
            )
    else:
        result = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )

    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(command)}\n{result.stderr.strip()}"
        )
    return result.stdout if stdout_path is None else ""


def load_json(path: Path) -> Dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def get_git_sha(repo_root: Path) -> str:
    try:
        output = run_command(["git", "rev-parse", "HEAD"], cwd=repo_root).strip()
    except Exception:
        output = ""
    return output


def get_git_status(repo_root: Path) -> str:
    try:
        output = run_command(["git", "status", "--porcelain"], cwd=repo_root).strip()
    except Exception:
        output = ""
    return output


def ensure_clean_worktree(repo_root: Path, allow_dirty: bool) -> None:
    status = get_git_status(repo_root)
    if status and not allow_dirty:
        raise RuntimeError(
            "Dirty git worktree detected. Commit/stash changes or pass --allow-dirty."
        )


def ensure_team_tag(value: Optional[str]) -> str:
    tag = (value or os.environ.get(TEAM_ENV, "")).strip()
    if not tag:
        raise RuntimeError(
            f"Missing team tag. Use --team-tag or set {TEAM_ENV}."
        )
    return tag


def run_internal_stage(
    report_dir: Path,
    repo_root: Path,
    team_tag: str,
    label: Optional[str] = None,
) -> List[StageResult]:
    results = []
    suffix = f"-{label}" if label else ""

    boundary_report = report_dir / f"boundary-report{suffix}.json"
    run_command(
        [
            "python3",
            str(DEFAULT_BOUNDARY_SCRIPT),
            "--report",
            "--format",
            "json",
            "--project-root",
            str(repo_root),
        ],
        stdout_path=boundary_report,
        timeout=600,
    )
    results.append(StageResult(f"internal{suffix}:boundary", "ok", str(boundary_report)))

    run_command(["python3", str(DEFAULT_MARKER_SCAN)], timeout=600)
    scan_results = Path("/workspace/scan_results.json")
    if scan_results.exists():
        marker_copy = report_dir / f"gl-marker-scan{suffix}.json"
        marker_copy.write_text(scan_results.read_text(encoding="utf-8"), encoding="utf-8")
        results.append(StageResult(f"internal{suffix}:gl-marker-scan", "ok", str(marker_copy)))
    else:
        results.append(StageResult(f"internal{suffix}:gl-marker-scan", "error", error="scan_results.json missing"))

    naming_report = report_dir / f"naming-violations{suffix}.json"
    run_command(
        [
            "python3",
            str(DEFAULT_NAMING_SCAN),
            "--path",
            str(repo_root),
            "--output",
            str(naming_report),
        ],
        timeout=600,
    )
    results.append(StageResult(f"internal{suffix}:naming-violations", "ok", str(naming_report)))

    run_command(
        [
            "python3",
            str(DEFAULT_NG_SCRIPT),
            "--stage",
            "internal",
            "--team-tag",
            team_tag,
        ],
        timeout=600,
    )
    results.append(StageResult(f"internal{suffix}:ng-namespace", "ok"))

    return results


def run_ng_stage(stage: str, team_tag: str, timeout: int = 600, label: Optional[str] = None) -> StageResult:
    run_command(
        [
            "python3",
            str(DEFAULT_NG_SCRIPT),
            "--stage",
            stage,
            "--team-tag",
            team_tag,
        ],
        timeout=timeout,
    )
    suffix = f"-{label}" if label else ""
    return StageResult(f"{stage}{suffix}:ng-namespace", "ok")


def generate_fix_plan(repo_root: Path, report_dir: Path) -> Path:
    plan_path = report_dir / "fix-plan.json"
    run_command(
        [
            "python3",
            str(DEFAULT_FIX_NAMING),
            "--workspace",
            str(repo_root),
            "--plan-output",
            str(plan_path),
        ],
        timeout=600,
    )
    return plan_path


def create_backup_bundle(repo_root: Path, report_dir: Path, plan_path: Path) -> Path:
    payload = load_json(plan_path)
    changes = payload.get("changes", [])
    backup_root = repo_root / ".governance" / "backups" / f"zero-tolerance-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    backup_root.mkdir(parents=True, exist_ok=True)

    for change in changes:
        old_rel = change.get("old_path")
        if not old_rel:
            continue
        source_path = repo_root / old_rel
        if not source_path.exists():
            continue
        target_path = backup_root / old_rel
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if source_path.is_dir():
            shutil.copytree(source_path, target_path, dirs_exist_ok=True)
        else:
            shutil.copy2(source_path, target_path)
    return backup_root


def rollback_from_backup(repo_root: Path, backup_root: Path, plan_path: Path) -> None:
    payload = load_json(plan_path)
    changes = payload.get("changes", [])
    for change in changes:
        old_rel = change.get("old_path")
        new_rel = change.get("new_path")
        if not old_rel:
            continue
        old_path = repo_root / old_rel
        new_path = repo_root / new_rel if new_rel else None
        backup_path = backup_root / old_rel
        if new_path and new_path.exists():
            if new_path.is_dir():
                shutil.rmtree(new_path)
            else:
                new_path.unlink()
        if backup_path.exists():
            old_path.parent.mkdir(parents=True, exist_ok=True)
            if backup_path.is_dir():
                shutil.copytree(backup_path, old_path, dirs_exist_ok=True)
            else:
                shutil.copy2(backup_path, old_path)


def apply_fixes(repo_root: Path, report_dir: Path, ack_destructive: bool) -> List[str]:
    actions = []
    if not ack_destructive:
        raise RuntimeError(
            "Destructive fixes require --ack-destructive to proceed."
        )
    run_command(
        [
            "python3",
            str(DEFAULT_FIX_NAMING),
            "--workspace",
            str(repo_root),
            "--apply",
        ],
        timeout=600,
    )
    actions.append("Applied naming violation auto-fix.")
    return actions


def build_summary(report_dir: Path, label: Optional[str] = None) -> Dict:
    suffix = f"-{label}" if label else ""
    boundary = load_json(report_dir / f"boundary-report{suffix}.json")
    marker_scan = load_json(report_dir / f"gl-marker-scan{suffix}.json")
    naming = load_json(report_dir / f"naming-violations{suffix}.json")
    ng_cross = load_json(
        Path(
            "/workspace/gl-governance-compliance-platform/governance/naming/registry/ng-era1-cross-validation.json"
        )
    )

    naming_summary = naming.get("violation_summary", {})
    naming_total = sum(naming_summary.values()) if naming_summary else 0

    return {
        "boundary": {
            "total_violations": boundary.get("total_violations", 0),
            "compliance_rate": boundary.get("compliance_rate"),
        },
        "gl_marker": {
            "total_files": marker_scan.get("scan_summary", {}).get("total_files"),
            "needs_adjustment": marker_scan.get("scan_summary", {}).get("files_needing_adjustment"),
            "compliance_rate": marker_scan.get("scan_summary", {}).get("compliance_rate"),
        },
        "naming": {
            "total_violations": naming_total,
            "by_type": naming_summary,
        },
        "ng_namespace": {
            "total_records": ng_cross.get("counts", {}).get("total_records"),
            "unmapped_layers": ng_cross.get("counts", {}).get("unmapped_layers"),
            "missing_era2_mapping": ng_cross.get("counts", {}).get("missing_era2_mapping"),
            "prefix_collisions": ng_cross.get("counts", {}).get("prefix_collisions"),
        },
    }


def determine_zero_tolerance_status(summary: Dict) -> Dict:
    failures = []
    if summary["boundary"]["total_violations"]:
        failures.append("boundary_violations")
    if summary["gl_marker"]["needs_adjustment"]:
        failures.append("gl_marker_missing")
    if summary["naming"]["total_violations"]:
        failures.append("naming_violations")
    if summary["ng_namespace"]["unmapped_layers"]:
        failures.append("ng_unmapped_layers")
    if summary["ng_namespace"]["missing_era2_mapping"]:
        failures.append("ng_missing_era2_mapping")
    if summary["ng_namespace"]["prefix_collisions"]:
        failures.append("ng_prefix_collisions")

    return {
        "status": "blocked" if failures else "pass",
        "failures": failures,
    }


def build_remediation_plan(summary: Dict) -> List[Dict]:
    plan = []
    if summary["boundary"]["total_violations"]:
        plan.append(
            {
                "issue": "Boundary violations detected",
                "action": "Run boundary checker per layer and fix dependency violations.",
                "command": "python3 gl-governance-compliance-platform/scripts/boundary_checker.py --check --project-root /workspace",
            }
        )
    if summary["gl_marker"]["needs_adjustment"]:
        plan.append(
            {
                "issue": "Missing GL markers",
                "action": "Update files listed in scan_results.json to include GL markers.",
                "artifact": "/workspace/scan_results.json",
            }
        )
    if summary["naming"]["total_violations"]:
        plan.append(
            {
                "issue": "Naming violations",
                "action": "Review naming violations report and apply renames.",
                "command": "python3 fix_naming_violations.py --workspace /workspace --apply",
            }
        )
    if summary["ng_namespace"]["unmapped_layers"]:
        plan.append(
            {
                "issue": "Unmapped layers in namespace scan",
                "action": "Update LAYER_MAP or add explicit mappings.",
                "artifact": "/workspace/gl-governance-compliance-platform/scripts/naming/ng_namespace_pipeline.py",
            }
        )
    if summary["ng_namespace"]["missing_era2_mapping"]:
        plan.append(
            {
                "issue": "Missing Era-2 mappings",
                "action": "Extend ng-era1-era2-mapping.yaml for coverage.",
                "artifact": "/workspace/gl-governance-compliance-platform/governance/naming/ng-era1-era2-mapping.yaml",
            }
        )
    if summary["ng_namespace"]["prefix_collisions"]:
        plan.append(
            {
                "issue": "Prefix collisions",
                "action": "Normalize prefixes and enforce uniqueness per module.",
            }
        )
    return plan


def write_markdown(
    report_path: Path,
    summary: Dict,
    status: Dict,
    plan: List[Dict],
    team_tag: str,
    run_id: str,
) -> None:
    lines = [
        "# Zero-Tolerance Centralized Report",
        "",
        f"Timestamp: {utc_now()}",
        f"Run ID: {run_id}",
        f"Team Tag: {team_tag}",
        "",
        "## Flow Model",
        " -> ".join(FLOW_MODEL),
        "",
        "## Status",
        f"- Status: {status['status'].upper()}",
        f"- Failures: {', '.join(status['failures']) if status['failures'] else 'None'}",
        "",
        "## Summary",
        f"- Boundary violations: {summary['boundary']['total_violations']}",
        f"- GL marker missing: {summary['gl_marker']['needs_adjustment']}",
        f"- Naming violations: {summary['naming']['total_violations']}",
        f"- NG unmapped layers: {summary['ng_namespace']['unmapped_layers']}",
        f"- NG missing Era-2 mapping: {summary['ng_namespace']['missing_era2_mapping']}",
        f"- NG prefix collisions: {summary['ng_namespace']['prefix_collisions']}",
        "",
        "## Remediation Plan",
    ]
    for item in plan:
        lines.append(f"- Issue: {item['issue']}")
        lines.append(f"  Action: {item.get('action')}")
        if item.get("command"):
            lines.append(f"  Command: {item['command']}")
        if item.get("artifact"):
            lines.append(f"  Artifact: {item['artifact']}")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Zero-tolerance centralized violation handler",
    )
    parser.add_argument("--team-tag", help="Team tag for authorization")
    parser.add_argument(
        "--report-dir",
        default=str(DEFAULT_REPORT_DIR),
        help="Directory for centralized reports",
    )
    parser.add_argument(
        "--repo-root",
        default=str(DEFAULT_REPO_ROOT),
        help="Repository root",
    )
    parser.add_argument(
        "--apply-fixes",
        action="store_true",
        help="Apply auto-fixes where available (requires --ack-destructive).",
    )
    parser.add_argument(
        "--ack-destructive",
        action="store_true",
        help="Acknowledge destructive fixes (renames).",
    )
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Generate fix plan only (no modifications).",
    )
    parser.add_argument(
        "--rollback-on-fail",
        action="store_true",
        help="Rollback from backup if apply or re-validation fails.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow running apply fixes on a dirty git worktree.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    repo_root = Path(args.repo_root)

    team_tag = ensure_team_tag(args.team_tag)
    run_id = str(uuid.uuid4())
    actor = os.environ.get("USER", "")
    git_sha_before = get_git_sha(repo_root)
    git_status_before = get_git_status(repo_root)

    stage_results: List[StageResult] = []
    stage_results.extend(run_internal_stage(report_dir, repo_root, team_tag))
    stage_results.append(run_ng_stage("external", team_tag))
    stage_results.append(run_ng_stage("global", team_tag))
    stage_results.append(run_ng_stage("cross-validate", team_tag))
    stage_results.append(run_ng_stage("insight", team_tag))

    fix_actions: List[str] = []
    fix_plan_path = generate_fix_plan(repo_root, report_dir)
    backup_path = ""

    if args.plan_only:
        summary = build_summary(report_dir)
        status = determine_zero_tolerance_status(summary)
        plan = build_remediation_plan(summary)
        report_payload = {
            "timestamp": utc_now(),
            "run_id": run_id,
            "team_tag": team_tag,
            "actor": actor,
            "git_sha_before": git_sha_before,
            "git_status_before": git_status_before,
            "flow_model": FLOW_MODEL,
            "stage_results": [result.__dict__ for result in stage_results],
            "summary": summary,
            "status": status,
            "remediation_plan": plan,
            "fix_plan_path": str(fix_plan_path),
            "fix_actions": [],
        }
        json_report = report_dir / "centralized-report.json"
        json_report.write_text(
            json.dumps(report_payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        markdown_report = report_dir / "centralized-report.md"
        write_markdown(markdown_report, summary, status, plan, team_tag, run_id)
        return 2 if status["status"] == "blocked" else 0

    if args.apply_fixes:
        ensure_clean_worktree(repo_root, args.allow_dirty)
        backup_root = create_backup_bundle(repo_root, report_dir, fix_plan_path)
        backup_path = str(backup_root)
        try:
            fix_actions = apply_fixes(repo_root, report_dir, args.ack_destructive)
        except Exception:
            if args.rollback_on_fail and backup_path:
                rollback_from_backup(repo_root, Path(backup_path), fix_plan_path)
            raise

        stage_results.extend(run_internal_stage(report_dir, repo_root, team_tag, label="postfix"))
        stage_results.append(run_ng_stage("external", team_tag, label="postfix"))
        stage_results.append(run_ng_stage("global", team_tag, label="postfix"))
        stage_results.append(run_ng_stage("cross-validate", team_tag, label="postfix"))
        stage_results.append(run_ng_stage("insight", team_tag, label="postfix"))

    summary_label = "postfix" if args.apply_fixes else None
    summary = build_summary(report_dir, label=summary_label)
    status = determine_zero_tolerance_status(summary)
    plan = build_remediation_plan(summary)
    git_sha_after = get_git_sha(repo_root)
    git_status_after = get_git_status(repo_root)

    rollback_performed = False
    if args.apply_fixes and args.rollback_on_fail and status["status"] == "blocked" and backup_path:
        rollback_from_backup(repo_root, Path(backup_path), fix_plan_path)
        rollback_performed = True
        git_sha_after = get_git_sha(repo_root)
        git_status_after = get_git_status(repo_root)

    report_payload = {
        "timestamp": utc_now(),
        "run_id": run_id,
        "team_tag": team_tag,
        "actor": actor,
        "git_sha_before": git_sha_before,
        "git_sha_after": git_sha_after,
        "git_status_before": git_status_before,
        "git_status_after": git_status_after,
        "flow_model": FLOW_MODEL,
        "stage_results": [result.__dict__ for result in stage_results],
        "summary": summary,
        "status": status,
        "remediation_plan": plan,
        "fix_plan_path": str(fix_plan_path),
        "backup_bundle": backup_path,
        "rollback_performed": rollback_performed,
        "fix_actions": fix_actions,
    }

    json_report = report_dir / "centralized-report.json"
    json_report.write_text(
        json.dumps(report_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    markdown_report = report_dir / "centralized-report.md"
    write_markdown(markdown_report, summary, status, plan, team_tag, run_id)

    return 0 if status["status"] == "pass" else 2


if __name__ == "__main__":
    sys.exit(main())
