# @GL-governed
# @GL-layer: GL30-49
# @GL-semantic: github-scripts
# @GL-audit-trail: ../../engine/gl_platform_universe.gl_platform_universe.governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
#!/usr/bin/env python3
"""
GL 工作流程自動重構腳本
Automated GL workflow refactoring script
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
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class WorkflowRefactor:
    """工作流程重構器"""
    
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.workflows_dir = self.repo_root / ".github" / "workflows"
        self.reports = []
        
    def scan_workflows(self) -> List[Path]:
        """掃描所有工作流程文件"""
        workflows = []
        if self.workflows_dir.exists():
            workflows = list(self.workflows_dir.glob("*.yml")) + list(self.workflows_dir.glob("*.yaml"))
        return sorted(workflows)
    
    def refactor_workflow(self, workflow_path: Path) -> Dict[str, Any]:
        """重構單個工作流程文件"""
        report = {
            "file": str(workflow_path.relative_to(self.repo_root)),
            "status": "success",
            "changes": [],
            "warnings": [],
            "errors": []
        }
        
        try:
            # 讀取原始文件
            with open(workflow_path, 'r', encoding='utf-8') as f:
                content = f.read()
                original = yaml.safe_load(content)
            
            if not original:
                report["status"] = "invalid"
                report["errors"].append("Empty or invalid YAML")
                return report
            
            refactored = self._apply_refactoring_rules(original, report)
            
            # 比較變更
            if original != refactored:
                # 備份原始文件
                backup_path = workflow_path.with_suffix('.yml.backup')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                report["changes"].append(f"Created backup: {backup_path.name}")
                
                # 寫入重構後的文件
                with open(workflow_path, 'w', encoding='utf-8') as f:
                    yaml.dump(refactored, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
                report["changes"].append("Applied refactoring rules")
            else:
                report["warnings"].append("No changes needed")
                
        except Exception as e:
            report["status"] = "error"
            report["errors"].append(str(e))
        
        return report
    
    def _apply_refactoring_rules(self, workflow: Dict[str, Any], report: Dict[str, Any]) -> Dict[str, Any]:
        """應用 GL 重構規則"""
        refactored = workflow.copy()
        
        # 規則 1: 確保有 name 欄位
        if 'name' not in refactored:
            refactored['name'] = "Generated Workflow"
            report["changes"].append("Added missing 'name' field")
        
        # 規則 2: 確保有 run-name 欄位（推薦）
        if 'run-name' not in refactored:
            refactored['run-name'] = "${{ github.event_name }} by @${{ github.actor }}"
            report["changes"].append("Added 'run-name' field")
        
        # 規則 3: 檢查並優化觸發條件
        if 'on' in refactored:
            refactored['on'] = self._refactor_triggers(refactored['on'], report)
        
        # 規則 4: 確保最小權限
        if 'permissions' not in refactored:
            refactored['permissions'] = {
                'contents': 'read'
            }
            report["changes"].append("Added minimal permissions")
        else:
            refactored['permissions'] = self._refactor_permissions(refactored['permissions'], report)
        
        # 規則 5: 重構 jobs
        if 'jobs' in refactored:
            refactored['jobs'] = self._refactor_jobs(refactored['jobs'], report)
        
        # 規則 6: 添加推薦的環境變數
        if 'env' not in refactored:
            refactored['env'] = {
                'NODE_VERSION': '20'
            }
            report["changes"].append("Added default environment variables")
        
        return refactored
    
    def _refactor_triggers(self, triggers: Any, report: Dict[str, Any]) -> Any:
        """重構觸發條件"""
        if isinstance(triggers, dict):
            refactored = {}
            for event, config in triggers.items():
                if event in ['push', 'pull_request']:
                    # 確保有 branches 過濾
                    if isinstance(config, dict):
                        if 'branches' not in config:
                            config['branches'] = ['main', 'master']
                            report["changes"].append(f"Added branches filter for {event}")
                    elif isinstance(config, list):
                        # 保持列表形式
                        pass
                    else:
                        config = {'branches': ['main', 'master']}
                        report["changes"].append(f"Added branches filter for {event}")
                refactored[event] = config
            return refactored
        elif isinstance(triggers, list):
            # 保持列表形式（如 ['push', 'pull_request']）
            return triggers
        return triggers
    
    def _refactor_permissions(self, permissions: Dict[str, str], report: Dict[str, Any]) -> Dict[str, str]:
        """重構權限設定"""
        refactored = {}
        
        # 移除不必要的 write-all 權限
        if 'write-all' in permissions:
            report["changes"].append("Removed 'write-all' permission (security risk)")
            del permissions['write-all']
        
        # 確保最小權限
        for scope, level in permissions.items():
            if level == 'write' and scope not in ['contents', 'issues', 'pull-requests', 'checks', 'deployments']:
                report["warnings"].append(f"Review write permission for {scope}")
            refactored[scope] = level
        
        # 如果沒有 contents 權限，添加 read
        if 'contents' not in refactored:
            refactored['contents'] = 'read'
            report["changes"].append("Added contents: read permission")
        
        return refactored
    
    def _refactor_jobs(self, jobs: Dict[str, Any], report: Dict[str, Any]) -> Dict[str, Any]:
        """重構 jobs"""
        refactored = {}
        
        for job_id, job_config in jobs.items():
            refactored_job = job_config.copy()
            
            # 確保有 job name
            if 'name' not in refactored_job:
                refactored_job['name'] = job_id.replace('-', ' ').title()
                report["changes"].append(f"Added name for job: {job_id}")
            
            # 確保有 runs-on
            if 'runs-on' not in refactored_job:
                refactored_job['runs-on'] = 'ubuntu-latest'
                report["changes"].append(f"Added runs-on for job: {job_id}")
            
            # 重構 steps
            if 'steps' in refactored_job:
                refactored_job['steps'] = self._refactor_steps(refactored_job['steps'], job_id, report)
            
            refactored[job_id] = refactored_job
        
        return refactored
    
    def _refactor_steps(self, steps: List[Dict[str, Any]], job_id: str, report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """重構 steps"""
        refactored = []
        
        for step in steps:
            refactored_step = step.copy()
            
            # 確保每個 step 都有 name
            if 'name' not in refactored_step:
                if 'uses' in refactored_step:
                    refactored_step['name'] = f"Run {refactored_step['uses']}"
                elif 'run' in refactored_step:
                    first_line = refactored_step['run'].split('\n')[0][:50]
                    refactored_step['name'] = f"Execute: {first_line}"
                report["changes"].append(f"Added name for step in job: {job_id}")
            
            # 檢查 uses 欄位的版本
            if 'uses' in refactored_step:
                refactored_step['uses'] = self._refactor_action_version(refactored_step['uses'], report)
            
            # 添加 timeout（建議）
            if 'timeout-minutes' not in refactored_step:
                # 不自動添加，只警告
                pass
            
            refactored.append(refactored_step)
        
        return refactored
    
    def _refactor_action_version(self, action_ref: str, report: Dict[str, Any]) -> str:
        """重構 action 版本"""
        # 檢查是否使用 @main, @master, @latest
        if re.search(r'@(main|master|latest)\s*$', action_ref):
            report["warnings"].append(f"Action {action_ref} uses mutable version tag")
            # 嘗試升級到 v4 或 v3
            if 'actions/checkout' in action_ref:
                return re.sub(r'@(main|master|latest)\s*$', '@v4', action_ref)
            elif 'actions/setup-node' in action_ref:
                return re.sub(r'@(main|master|latest)\s*$', '@v4', action_ref)
            elif 'actions/configure-pages' in action_ref:
                return re.sub(r'@(main|master|latest)\s*$', '@v5', action_ref)
            elif 'actions/upload-pages-artifact' in action_ref:
                return re.sub(r'@(main|master|latest)\s*$', '@v4', action_ref)
            elif 'actions/deploy-pages' in action_ref:
                return re.sub(r'@(main|master|latest)\s*$', '@v4', action_ref)
        
        return action_ref
    
    def generate_report(self) -> str:
        """生成重構報告"""
        report_lines = [
            "# GL 工作流程重構報告",
            f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "## 重構摘要",
            "",
            f"總共處理文件: {len(self.reports)}",
            f"成功: {sum(1 for r in self.reports if r['status'] == 'success')}",
            f"失敗: {sum(1 for r in self.reports if r['status'] == 'error')}",
            f"無效: {sum(1 for r in self.reports if r['status'] == 'invalid')}",
            "",
            "## 詳細報告",
            ""
        ]
        
        for report in self.reports:
            report_lines.append(f"### {report['file']}")
            report_lines.append(f"狀態: {report['status']}")
            
            if report['changes']:
                report_lines.append("變更:")
                for change in report['changes']:
                    report_lines.append(f"  - {change}")
            
            if report['warnings']:
                report_lines.append("警告:")
                for warning in report['warnings']:
                    report_lines.append(f"  - {warning}")
            
            if report['errors']:
                report_lines.append("錯誤:")
                for error in report['errors']:
                    report_lines.append(f"  - {error}")
            
            report_lines.append("")
        
        return '\n'.join(report_lines)
    
    def run(self):
        """執行重構"""
        print("=" * 60)
        print("GL 工作流程自動重構開始")
        print("=" * 60)
        
        workflows = self.scan_workflows()
        print(f"\n找到 {len(workflows)} 個工作流程文件")
        
        if not workflows:
            print("未找到工作流程文件")
            return
        
        for workflow_path in workflows:
            print(f"\n處理: {workflow_path.name}")
            report = self.refactor_workflow(workflow_path)
            self.reports.append(report)
            
            if report['status'] == 'success':
                print(f"  ✓ 成功 ({len(report['changes'])} 個變更)")
                if report['warnings']:
                    print(f"  ⚠ {len(report['warnings'])} 個警告")
            else:
                print(f"  ✗ {report['status']}")
                if report['errors']:
                    for error in report['errors'][:3]:  # 只顯示前3個錯誤
                        print(f"    - {error}")
        
        # 生成報告
        report_content = self.generate_report()
        report_path = self.repo_root / "GL-WORKFLOW-REFACTOR-REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print("\n" + "=" * 60)
        print("重構完成！")
        print(f"報告已生成: {report_path}")
        print("=" * 60)

def main():
    """主函數"""
    if len(sys.argv) > 1:
        repo_root = sys.argv[1]
    else:
        repo_root = os.getcwd()
    
    refactor = WorkflowRefactor(repo_root)
    refactor.run()

if __name__ == "__main__":
    main()