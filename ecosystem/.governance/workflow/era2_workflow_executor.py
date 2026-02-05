"""
Era-2 Zero Tolerance Workflow Executor
執行完整的工作流程，綁定零容忍強制執行引擎
"""

import json
import sys
import time
import subprocess
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import yaml

# Add paths for module imports
workflow_dir = Path(__file__).parent
governance_dir = workflow_dir.parent
enforcement_dir = governance_dir / "enforcement"

sys.path.insert(0, str(enforcement_dir))
sys.path.insert(0, str(governance_dir))

# Direct import from enforcement directory
import zero_tolerance_engine

ZeroToleranceEnforcementEngine = zero_tolerance_engine.ZeroToleranceEnforcementEngine
EnforcementContext = zero_tolerance_engine.EnforcementContext
Decision = zero_tolerance_engine.Decision

class Era2WorkflowExecutor:
    """Era-2 零容恐工作流執行器"""
    
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = Path(workspace)
        self.workflow_file = self.workspace / "ecosystem" / ".governance" / "workflow" / "era2_zero_tolerance_workflow.yaml"
        self.enforcement_engine = ZeroToleranceEnforcementEngine(workspace)
        self.workflow_data = self._load_workflow()
        
    def _load_workflow(self) -> Dict:
        """載入工作流程配置"""
        if self.workflow_file.exists():
            with open(self.workflow_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                # 提取規範部分的階段
                if 'spec' in data:
                    return {
                        "name": data.get('metadata', {}).get('name', 'Unknown'),
                        "version": data.get('metadata', {}).get('version', '1.0'),
                        "description": data.get('metadata', {}).get('description', ''),
                        "phases": data['spec'].get('phases', []),
                        "principles": data['spec'].get('principles', []),
                        "glcm_rules": data['spec'].get('glcm_rules', {}),
                        "success_criteria": data['spec'].get('success_criteria', {})
                    }
        return {
            "name": "Era-2 Zero Tolerance Workflow",
            "version": "1.0",
            "phases": []
        }
    
    def execute(self) -> Dict[str, Any]:
        """執行完整的工作流程"""
        start_time = time.time()
        results = {
            "workflow_name": self.workflow_data.get("name", "Unknown"),
            "start_time": datetime.now().isoformat(),
            "phases": [],
            "decisions": [],
            "violations": [],
            "compliance_score": 0.0
        }
        
        print(f"🚀 啟動 {results['workflow_name']}")
        print(f"📅 開始時間: {results['start_time']}")
        print("-" * 60)
        
        # 執行各階段
        for phase in self.workflow_data.get("phases", []):
            phase_result = self._execute_phase(phase)
            results["phases"].append(phase_result)
            
            if not phase_result.get("success", False):
                print(f"❌ 階段失敗: {phase.get('name', 'Unknown')}")
                break
        
        # 計算合規得分
        results["compliance_score"] = self._calculate_compliance_score(results)
        results["end_time"] = datetime.now().isoformat()
        results["duration_seconds"] = time.time() - start_time
        
        print("-" * 60)
        print(f"✅ 工作流程完成")
        print(f"📊 合規得分: {results['compliance_score']:.2f}/100")
        print(f"⏱️  總時長: {results['duration_seconds']:.2f}秒")
        
        return results
    
    def _execute_phase(self, phase: Dict) -> Dict[str, Any]:
        """執行單個階段"""
        phase_id = phase.get("phase_id", "unknown")
        phase_name = phase.get("phase_name", "Unknown Phase")
        priority = phase.get("priority", 1000)
        blocking = phase.get("blocking", True)
        
        print(f"\n📋 執行階段: {phase_name} ({phase_id})")
        print(f"   優先級: {priority}, 阻塞模式: {blocking}")
        
        phase_result = {
            "phase_id": phase_id,
            "name": phase_name,
            "priority": priority,
            "blocking": blocking,
            "start_time": datetime.now().isoformat(),
            "success": True,
            "decisions": [],
            "violations": [],
            "steps_executed": 0
        }
        
        # 執行階段中的每個步驟
        steps = phase.get("steps", [])
        for step in steps:
            step_result = self._execute_step(step, phase_name)
            phase_result["steps_executed"] += 1
            phase_result["decisions"].extend(step_result.get("decisions", []))
            phase_result["violations"].extend(step_result.get("violations", []))
            
            if not step_result.get("success", False):
                phase_result["success"] = False
                if blocking:
                    print(f"   ❌ 步驟失敗且阻塞模式啟用: {step.get('step_name', 'Unknown')}")
                    break
        
        phase_result["end_time"] = datetime.now().isoformat()
        
        status = "✅ 成功" if phase_result["success"] else "❌ 失敗"
        print(f"   {status}: {phase_name} (步驟: {phase_result['steps_executed']}/{len(steps)})")
        
        return phase_result
    
    def _execute_step(self, step: Dict, phase_name: str) -> Dict[str, Any]:
        """執行單個步驟"""
        step_id = step.get("step_id", "unknown")
        step_name = step.get("step_name", "Unknown Step")
        required = step.get("required", True)
        
        print(f"   🔧 執行步驟: {step_name}")
        
        step_result = {
            "step_id": step_id,
            "name": step_name,
            "required": required,
            "success": True,
            "decisions": [],
            "violations": []
        }
        
        # 建立執行上下文
        context = EnforcementContext(
            operation_id=step_id,
            operation_type=f"phase_{phase_name}",
            module_id=step_name,
            metadata={
                "phase": phase_name,
                "required": required,
                "tool": step.get("tool", ""),
                "enforcement_point": step.get("enforcement_point", "")
            }
        )
        
        # 執行強制檢查
        try:
            # 使用 ZeroToleranceEnforcementEngine 執行操作檢查
            decision = self.enforcement_engine.enforce_operation(
                operation_id=step_id,
                module_id=step_name
            )
            step_result["decisions"].append(decision.to_dict())
            
            # 檢查決定是否需要阻止
            if decision.decision == Decision.BLOCK:
                step_result["success"] = False
                step_result["violations"].append({
                    "type": "policy_violation",
                    "description": decision.reason,
                    "severity": "high"
                })
            
            # 嘗試執行工具
            tool = step.get("tool", "")
            if tool and not tool.startswith("manual_"):
                execution_success = self._execute_tool(tool, step)
                if not execution_success:
                    step_result["success"] = False
                    if required:
                        step_result["violations"].append({
                            "type": "tool_execution_failure",
                            "description": f"Tool execution failed: {tool}",
                            "severity": "high"
                        })
                
        except Exception as e:
            step_result["success"] = False
            step_result["error"] = str(e)
            print(f"      ❌ 步驟執行錯誤: {e}")
        
        status = "✅" if step_result["success"] else "❌"
        print(f"      {status} {step_name}")
        
        return step_result
    
    def _execute_tool(self, tool: str, step: Dict) -> bool:
        """執行工具腳本"""
        import subprocess
        import os
        
        try:
            # 處理不同格式的工具路徑
            if tool.startswith("python "):
                tool_path = tool.replace("python ", "").strip()
                cmd = ["python", tool_path]
            elif tool.startswith("ecosystem/"):
                tool_path = os.path.join(str(self.workspace), tool)
                if tool_path.endswith(".py"):
                    cmd = ["python", tool_path]
                else:
                    cmd = [tool_path]
            else:
                # 相對路徑
                tool_path = os.path.join(str(self.workspace), tool)
                cmd = ["python", tool_path]
            
            # 執行工具
            result = subprocess.run(
                cmd,
                cwd=str(self.workspace),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"      ✅ 工具執行成功: {tool}")
                return True
            else:
                print(f"      ⚠️  工具執行返回非零: {tool}")
                if result.stderr:
                    print(f"      錯誤: {result.stderr[:200]}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"      ❌ 工具執行超時: {tool}")
            return False
        except FileNotFoundError:
            print(f"      ⚠️  工具文件不存在，跳過: {tool}")
            return True  # 工具不存在不算失敗
        except Exception as e:
            print(f"      ❌ 工具執行異常: {e}")
            return False
    
    def _calculate_compliance_score(self, results: Dict) -> float:
        """計算合規得分"""
        if not results["phases"]:
            return 0.0
        
        successful_phases = sum(1 for p in results["phases"] if p.get("success", False))
        total_phases = len(results["phases"])
        
        base_score = (successful_phases / total_phases) * 100
        
        # 檢查是否有違規
        total_violations = sum(len(p.get("violations", [])) for p in results["phases"])
        violation_penalty = total_violations * 5
        
        final_score = max(0, base_score - violation_penalty)
        return round(final_score, 2)
    
    def generate_report(self, results: Dict) -> str:
        """生成詳細報告"""
        report = []
        report.append("=" * 60)
        report.append(f"Era-2 零容忍工作流程執行報告")
        report.append("=" * 60)
        report.append(f"工作流程: {results['workflow_name']}")
        report.append(f"開始時間: {results['start_time']}")
        report.append(f"結束時間: {results['end_time']}")
        report.append(f"執行時長: {results['duration_seconds']:.2f}秒")
        report.append(f"合規得分: {results['compliance_score']:.2f}/100")
        report.append("")
        
        report.append("執行階段:")
        for phase in results["phases"]:
            status = "✅ 成功" if phase.get("success") else "❌ 失敗"
            report.append(f"  {status} - {phase['name']}")
            
            if phase.get("violations"):
                for violation in phase["violations"]:
                    report.append(f"    ⚠️  {violation['type']}: {violation['description']}")
        
        return "\n".join(report)

def main():
    """主執行函數"""
    executor = Era2WorkflowExecutor()
    results = executor.execute()
    
    # 生成並保存報告
    report = executor.generate_report(results)
    print("\n" + report)
    
    # 保存結果
    report_file = Path("/workspace/ecosystem/reports/era2_workflow_execution.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 報告已保存: {report_file}")

if __name__ == "__main__":
    main()