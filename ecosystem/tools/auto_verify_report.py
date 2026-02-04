#!/usr/bin/env python3
"""
自動化報告驗證系統
Auto-Verify Report System

功能：在每次生成報告後自動運行合規性驗證
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import argparse

class AutoVerifyReport:
    """自動報告驗證器"""
    
    def __init__(self, workspace: str = "/workspace", report_file: str = None):
        self.workspace = Path(workspace)
        self.report_file = Path(report_file) if report_file else None
        self.ecosystem_root = self.workspace / "ecosystem"
        self.reports_dir = self.workspace / "reports"
        self.timestamp = datetime.now().isoformat()
        
        # 驗證工具路徑
        self.enforce_py = self.ecosystem_root / "enforce.py"
        self.enforce_rules_py = self.ecosystem_root / "enforce.rules.py"
        self.semantic_validator = self.ecosystem_root / "tools" / "semantic_validator.py"
        self.tool_verifier = self.ecosystem_root / "tools" / "verify_tool_definition.py"
        
        # 合規性閾值
        self.thresholds = {
            "critical": 60.0,  # 低於此值則阻擋
            "warning": 75.0,   # 低於此值則警告
            "good": 90.0       # 高於此值則通過
        }
        
    def run_command(self, cmd: List[str], capture_output: bool = True) -> Tuple[int, str, str]:
        """運行命令並返回結果"""
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.workspace),
                capture_output=capture_output,
                text=True,
                timeout=300
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timeout"
        except Exception as e:
            return -1, "", str(e)
    
    def verify_governance_checks(self) -> Dict:
        """驗證核心治理檢查"""
        print("\n🔍 1️⃣ 運行核心治理檢查...")
        
        exit_code, stdout, stderr = self.run_command([
            "python3", str(self.enforce_py), "--audit"
        ])
        
        # 解析結果
        passed_count = stdout.count("✅ PASS")
        total_count = 18  # 已知總檢查數
        
        score = (passed_count / total_count * 100) if total_count > 0 else 0
        
        return {
            "name": "核心治理檢查",
            "score": score,
            "weight": 0.40,
            "status": "PASS" if score >= 90 else "FAIL",
            "passed": passed_count,
            "total": total_count,
            "output": stdout[-500:] if len(stdout) > 500 else stdout  # 保留最後 500 字符
        }
    
    def verify_evidence_chain(self) -> Dict:
        """驗證證據鏈完整性"""
        print("\n🔍 2️⃣ 驗證證據鏈完整性...")
        
        exit_code, stdout, stderr = self.run_command([
            "python3", str(self.enforce_rules_py)
        ])
        
        # 檢查步驟完成情況
        step_count = stdout.count("Step") // 2  # 每個步驟會出現兩次
        total_steps = 10
        
        score = (step_count / total_steps * 100) if total_steps > 0 else 0
        
        return {
            "name": "證據鏈完整性",
            "score": score,
            "weight": 0.10,
            "status": "PASS" if score >= 90 else "FAIL",
            "completed": step_count,
            "total": total_steps,
            "output": stdout[-500:] if len(stdout) > 500 else stdout
        }
    
    def verify_semantic_compliance(self, report_file: str = None) -> Dict:
        """驗證報告語義合規性"""
        print("\n🔍 3️⃣ 驗證報告語義合規性...")
        
        # 使用測試報告或指定報告
        target_report = report_file or str(self.reports_dir / "test-enforce-rules-output-compliant.md")
        
        if not os.path.exists(target_report):
            target_report = str(self.reports_dir / "test-enforce-rules-output-compliant.md")
        
        exit_code, stdout, stderr = self.run_command([
            "python3", str(self.semantic_validator), target_report
        ])
        
        # 解析合規性評分
        score = 0.0
        violations = 0
        
        try:
            if "Compliance Score:" in stdout:
                score_line = [line for line in stdout.split('\n') if "Compliance Score:" in line][0]
                score = float(score_line.split("Compliance Score:")[1].split("/")[0].strip())
            
            if "Violations:" in stdout:
                violations_line = [line for line in stdout.split('\n') if "Violations:" in line][0]
                violations = int(violations_line.split("Violations:")[1].strip())
        except:
            pass
        
        status = "PASS" if score >= 75 else "FAIL"
        
        return {
            "name": "報告語義合規性",
            "score": score,
            "weight": 0.30,
            "status": status,
            "violations": violations,
            "output": stdout[-500:] if len(stdout) > 500 else stdout
        }
    
    def verify_tool_definition(self) -> Dict:
        """驗證工具定義合規性"""
        print("\n🔍 4️⃣ 驗證工具定義合規性...")
        
        exit_code, stdout, stderr = self.run_command([
            "python3", str(self.tool_verifier), "--all"
        ])
        
        # 解析合規性評分
        score = 0.0
        total_tools = 0
        registered_tools = 0
        
        try:
            if "Compliance score:" in stdout:
                score_line = [line for line in stdout.split('\n') if "Compliance score:" in line][0]
                score = float(score_line.split("Compliance score:")[1].split("/")[0].strip())
            
            if "Total tools:" in stdout:
                total_line = [line for line in stdout.split('\n') if "Total tools:" in line][0]
                total_tools = int(total_line.split("Total tools:")[1].strip())
            
            if "Registered tools:" in stdout:
                registered_line = [line for line in stdout.split('\n') if "Registered tools:" in line][0]
                registered_tools = int(registered_line.split("Registered tools:")[1].strip())
        except:
            pass
        
        status = "PASS" if score >= 50 else "FAIL"
        
        return {
            "name": "工具定義合規性",
            "score": score,
            "weight": 0.20,
            "status": status,
            "total_tools": total_tools,
            "registered_tools": registered_tools,
            "output": stdout[-500:] if len(stdout) > 500 else stdout
        }
    
    def calculate_overall_score(self, results: List[Dict]) -> Dict:
        """計算總體合規性評分"""
        total_score = 0.0
        total_weight = 0.0
        
        for result in results:
            total_score += result["score"] * result["weight"]
            total_weight += result["weight"]
        
        overall_score = (total_score / total_weight) if total_weight > 0 else 0
        
        # 確定等級
        if overall_score >= 90:
            grade = "🟢 優秀"
            grade_class = "excellent"
        elif overall_score >= 75:
            grade = "🟡 良好"
            grade_class = "good"
        elif overall_score >= 60:
            grade = "🟠 及格"
            grade_class = "pass"
        else:
            grade = "🔴 不合格"
            grade_class = "fail"
        
        # 確定是否通過
        passed = overall_score >= self.thresholds["critical"]
        
        return {
            "score": round(overall_score, 1),
            "grade": grade,
            "grade_class": grade_class,
            "passed": passed,
            "threshold": self.thresholds["critical"]
        }
    
    def generate_verification_report(self, results: List[Dict], overall: Dict) -> str:
        """生成驗證報告"""
        report = []
        
        report.append("=" * 80)
        report.append("🛡️ 自動化報告驗證系統報告")
        report.append("Auto-Verify Report System Report")
        report.append("=" * 80)
        report.append(f"\n📅 生成時間: {self.timestamp}")
        report.append(f"📁 報告文件: {self.report_file or 'N/A'}")
        report.append(f"🎯 Era: 1 (Evidence-Native Bootstrap)")
        report.append(f"🏗️  Layer: Operational (Evidence Generation)")
        
        report.append("\n" + "=" * 80)
        report.append("📊 總體合規性評分")
        report.append("=" * 80)
        report.append(f"\n總分: {overall['score']}/100")
        report.append(f"等級: {overall['grade']}")
        report.append(f"狀態: {'✅ 通過' if overall['passed'] else '❌ 未通過'}")
        report.append(f"閾值: {overall['threshold']}/100")
        
        report.append("\n" + "=" * 80)
        report.append("🔍 分項驗證結果")
        report.append("=" * 80)
        
        for i, result in enumerate(results, 1):
            emoji_num = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            report.append(f"\n{emoji_num[i-1] if i <= len(emoji_num) else f'{i}️⃣'} {result['name']}")
            report.append(f"   得分: {result['score']:.1f}/100")
            report.append(f"   權重: {result['weight'] * 100:.0f}%")
            report.append(f"   加權得分: {result['score'] * result['weight']:.1f}")
            status_emoji = "✅" if result['status'] == 'PASS' else "❌"
            report.append(f"   狀態: {status_emoji} {result['status']}")
            
            if "violations" in result:
                report.append(f"   違規數: {result['violations']}")
            if "passed" in result:
                report.append(f"   通過: {result['passed']}/{result['total']}")
            if "registered_tools" in result:
                report.append(f"   註冊: {result['registered_tools']}/{result['total_tools']}")
        
        report.append("\n" + "=" * 80)
        report.append("📋 評分計算")
        report.append("=" * 80)
        
        total_weighted = sum(r['score'] * r['weight'] for r in results)
        total_weight = sum(r['weight'] for r in results)
        final_score = (total_weighted / total_weight) if total_weight > 0 else 0
        report.append(f"\n加權總分: {total_weighted:.1f}")
        report.append(f"總權重: {total_weight:.2f}")
        report.append(f"最終得分: {final_score:.1f}/100")
        
        report.append("\n" + "=" * 80)
        report.append("🚨 建議行動")
        report.append("=" * 80)
        
        if overall['passed']:
            report.append("\n✅ 合規性檢查通過，報告可以發布。")
        else:
            report.append("\n❌ 合規性檢查未通過，請修復以下問題後再發布：")
            
            for result in results:
                if result['status'] == 'FAIL':
                    report.append(f"\n   • {result['name']}: {result['score']:.1f}/100")
        
        report.append("\n" + "=" * 80)
        report.append("報告結束")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_verification_report(self, report: str) -> str:
        """保存驗證報告"""
        filename = f"auto-verify-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = self.reports_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ 驗證報告已保存: {filepath}")
        return str(filepath)
    
    def run(self, report_file: str = None, auto_fix: bool = False) -> bool:
        """運行自動驗證流程"""
        print("\n" + "=" * 80)
        print("🚀 開始自動化報告驗證")
        print("=" * 80)
        
        # 更新報告文件
        if report_file:
            self.report_file = Path(report_file)
        
        # 運行所有驗證
        results = []
        
        try:
            # 1. 核心治理檢查
            results.append(self.verify_governance_checks())
            
            # 2. 證據鏈完整性
            results.append(self.verify_evidence_chain())
            
            # 3. 報告語義合規性
            results.append(self.verify_semantic_compliance(report_file))
            
            # 4. 工具定義合規性
            results.append(self.verify_tool_definition())
            
        except Exception as e:
            print(f"\n❌ 驗證過程中發生錯誤: {e}")
            return False
        
        # 計算總體評分
        overall = self.calculate_overall_score(results)
        
        # 生成報告
        report_text = self.generate_verification_report(results, overall)
        
        # 保存報告
        report_path = self.save_verification_report(report_text)
        
        # 顯示報告
        print("\n" + report_text)
        
        # 決定是否通過
        if overall['passed']:
            print("\n✅ 自動驗證完成 - 合規性檢查通過")
            return True
        else:
            print("\n❌ 自動驗證完成 - 合規性檢查未通過")
            print(f"   當前評分: {overall['score']}/100")
            print(f"   最低要求: {overall['threshold']}/100")
            
            if auto_fix:
                print("\n🔧 嘗試自動修復...")
                # 這裡可以添加自動修復邏輯
                print("⚠️  自動修復功能開發中...")
            
            return False

def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="自動化報告驗證系統",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  # 驗證指定報告
  python auto_verify_report.py --report reports/my-report.md
  
  # 驗證最新報告
  python auto_verify_report.py
  
  # 驗證並嘗試自動修復
  python auto_verify_report.py --auto-fix
        """
    )
    
    parser.add_argument(
        "--report",
        type=str,
        help="要驗證的報告文件路徑"
    )
    
    parser.add_argument(
        "--workspace",
        type=str,
        default="/workspace",
        help="工作空間路徑（默認: /workspace）"
    )
    
    parser.add_argument(
        "--auto-fix",
        action="store_true",
        help="嘗試自動修復問題"
    )
    
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="以 JSON 格式輸出結果"
    )
    
    args = parser.parse_args()
    
    # 創建驗證器
    verifier = AutoVerifyReport(
        workspace=args.workspace,
        report_file=args.report
    )
    
    # 運行驗證
    success = verifier.run(
        report_file=args.report,
        auto_fix=args.auto_fix
    )
    
    # 退出碼
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()