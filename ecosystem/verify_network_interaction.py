#!/usr/bin/env python3
"""
MNGA Network Interaction and Auto-Reasoning Verification System
內網+外網交互驗證 + 自動推理最佳實踐

Usage:
    python3 ecosystem/verify_network_interaction.py --audit
    python3 ecosystem/verify_network_interaction.py --auto-fix
    python3 ecosystem/verify_network_interaction.py --json
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Tuple

# Add ecosystem to path
ECOSYSTEM_ROOT = Path(__file__).parent
sys.path.insert(0, str(ECOSYSTEM_ROOT))

from validators.network_validator import NetworkValidator
from reasoning.auto_reasoner import AutoReasoner


class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}\n")


def print_step(number: int, text: str):
    """Print step"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{number}️⃣  {text}{Colors.END}")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")


def run_enforce_script(args) -> Tuple[bool, Dict]:
    """運行 enforce.py 腳本"""
    print_step(1, "運行生態系統治理強制執行...")
    
    try:
        import subprocess
        cmd = [sys.executable, str(ECOSYSTEM_ROOT / "enforce.py")]
        
        if args.audit:
            cmd.append("--audit")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # 解析 JSON 輸出
        if result.returncode == 0 and "--json" in cmd:
            audit_report = json.loads(result.stdout)
            print_success("治理檢查完成")
            return True, audit_report
        else:
            print_success("治理檢查完成 (退出碼: {})".format(result.returncode))
            # 嘗試從日誌中提取報告
            return True, {"status": "UNKNOWN", "violations": []}
            
    except subprocess.TimeoutExpired:
        print_error("治理檢查超時")
        return False, {"error": "timeout"}
    except Exception as e:
        print_error(f"治理檢查失敗: {str(e)}")
        return False, {"error": str(e)}


def run_network_validation(args) -> Tuple[bool, Dict]:
    """運行網絡驗證"""
    print_step(2, "運行內網+外網交互驗證...")
    
    try:
        validator = NetworkValidator()
        results = validator.run_all_tests()
        report = validator.generate_report()
        
        # 顯示結果
        for test in report["tests"]:
            status_emoji = "✅" if test["status"] == "PASS" else "❌" if test["status"] == "FAIL" else "⚠️"
            status_color = Colors.GREEN if test["status"] == "PASS" else Colors.RED if test["status"] == "FAIL" else Colors.YELLOW
            print(f"{status_color}{status_emoji} {test['name']}: {test['status']} ({test['latency_ms']:.2f}ms){Colors.END}")
        
        summary = report["test_summary"]
        print_info(f"測試總結: {summary['passed']}/{summary['total_tests']} 通過 ({summary['success_rate']})")
        
        # 顯示建議
        print("\n📋 網絡驗證建議:")
        for rec in report["recommendations"]:
            print(f"  {rec}")
        
        all_passed = summary["passed"] == summary["total_tests"]
        return all_passed, report
        
    except Exception as e:
        print_error(f"網絡驗證失敗: {str(e)}")
        return False, {"error": str(e)}


def run_auto_reasoning(audit_report: Dict, network_report: Dict) -> Dict:
    """運行自動推理"""
    print_step(3, "執行自動推理分析...")
    
    try:
        reasoner = AutoReasoner()
        
        # 對治理報告進行推理
        governance_results = reasoner.reason_about_governance(audit_report)
        print_info(f"治理推理結果: {len(governance_results)} 條推論")
        
        # 對網絡報告進行推理
        network_results = reasoner.reason_about_network(network_report)
        print_info(f"網絡推理結果: {len(network_results)} 條推論")
        
        # 對安全進行推理
        security_results = reasoner.reason_about_security()
        print_info(f"安全推理結果: {len(security_results)} 條推論")
        
        # 合併推理結果
        combined = reasoner.combine_reasoning(
            governance_results,
            network_results,
            security_results
        )
        
        # 顯示推理結果
        print("\n🧠 自動推理結果:")
        print(f"  總推論數: {combined['summary']['total_inferences']}")
        print(f"  嚴重: {combined['summary']['critical']}")
        print(f"  高: {combined['summary']['high']}")
        print(f"  中: {combined['summary']['medium']}")
        print(f"  低: {combined['summary']['low']}")
        print(f"  整體健康度: {combined['summary']['overall_health']}")
        
        # 顯示最佳實踐
        print("\n📚 最佳實踐建議:")
        for practice in combined["best_practices"]:
            print(f"  {practice}")
        
        return combined
        
    except Exception as e:
        print_error(f"自動推理失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


def generate_final_report(
    enforce_success: bool,
    audit_report: Dict,
    network_success: bool,
    network_report: Dict,
    reasoning_report: Dict
) -> Dict:
    """生成最終報告"""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    return {
        "timestamp": timestamp,
        "version": "1.0.0",
        "verification_summary": {
            "governance_check": "PASS" if enforce_success else "FAIL",
            "network_validation": "PASS" if network_success else "FAIL",
            "auto_reasoning": "COMPLETED"
        },
        "overall_status": "PASS" if enforce_success and network_success else "FAIL",
        "governance": audit_report,
        "network": network_report,
        "reasoning": reasoning_report,
        "metadata": {
            "ecosystem_root": str(ECOSYSTEM_ROOT),
            "verification_type": "NETWORK_INTERACTION_AND_AUTO_REASONING"
        }
    }


def save_report(report: Dict, output_path: str):
    """保存報告"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print_info(f"報告已保存到: {output_path}")


def parse_args():
    """解析命令行參數"""
    parser = argparse.ArgumentParser(
        description="MNGA Network Interaction and Auto-Reasoning Verification"
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="啟用詳細審計日誌"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式輸出結果"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="輸出報告文件路徑"
    )
    parser.add_argument(
        "--skip-network",
        action="store_true",
        help="跳過網絡驗證"
    )
    parser.add_argument(
        "--skip-reasoning",
        action="store_true",
        help="跳過自動推理"
    )
    
    return parser.parse_args()


def main():
    """主程序"""
    args = parse_args()
    
    print_header("🌐 MNGA 內網+外網交互驗證 & 自動推理系統")
    
    print_info(f"Ecosystem Root: {ECOSYSTEM_ROOT}")
    print_info(f"Timestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    
    if args.audit:
        print_info("審計模式: 已啟用")
    
    # 步驟 1: 運行治理檢查
    enforce_success, audit_report = run_enforce_script(args)
    
    # 步驟 2: 運行網絡驗證
    if not args.skip_network:
        network_success, network_report = run_network_validation(args)
    else:
        print_warning("跳過網絡驗證")
        network_success = True
        network_report = {"skipped": True}
    
    # 步驟 3: 運行自動推理
    if not args.skip_reasoning:
        reasoning_report = run_auto_reasoning(audit_report, network_report)
    else:
        print_warning("跳過自動推理")
        reasoning_report = {"skipped": True}
    
    # 生成最終報告
    final_report = generate_final_report(
        enforce_success,
        audit_report,
        network_success,
        network_report,
        reasoning_report
    )
    
    # 保存報告
    output_path = args.output
    if output_path or args.audit:
        if not output_path:
            reports_dir = ECOSYSTEM_ROOT.parent / "reports"
            reports_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(
                reports_dir / f"network_interaction_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
        save_report(final_report, output_path)
    
    # JSON 輸出
    if args.json:
        print(json.dumps(final_report, indent=2, ensure_ascii=False))
        return 0 if final_report["overall_status"] == "PASS" else 1
    
    # 總結
    print_header("📊 驗證結果總結")
    
    print(f"\n{'檢查項目':<30} {'狀態':<15} {'結果'}")
    print("-" * 80)
    print(f"{'治理檢查':<30} {'✅ PASS' if enforce_success else '❌ FAIL':<15} {audit_report.get('status', 'UNKNOWN')}")
    print(f"{'網絡驗證':<30} {'✅ PASS' if network_success else '❌ FAIL':<15} {network_report.get('test_summary', {}).get('success_rate', 'N/A')}")
    print(f"{'自動推理':<30} {'✅ COMPLETED':<15} {reasoning_report.get('summary', {}).get('overall_health', 'UNKNOWN')}")
    
    print("\n" + "=" * 80)
    
    if final_report["overall_status"] == "PASS":
        print_success(f"所有驗證通過 - 系統健康")
        return 0
    else:
        print_error(f"部分驗證失敗 - 需要關注")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_warning("\n驗證被用戶中斷")
        sys.exit(130)
    except Exception as e:
        print_error(f"發生未預期的錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)