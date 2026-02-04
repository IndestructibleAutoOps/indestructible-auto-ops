#!/usr/bin/env python3
"""
修復 ecosystem/enforce.rules.py 的報告生成邏輯
使其符合「報告生成強制規格」
"""

import re
from pathlib import Path


def fix_enforce_rules():
    """執行所有修復"""
    file_path = Path("ecosystem/enforce.rules.py")
    
    if not file_path.exists():
        print(f"錯誤: 文件不存在 {file_path}")
        return False
    
    # 讀取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修復 1: 新增報告頭輸出方法（在 class EnforcementCoordinator 中）
    new_methods = '''
    
    def _print_report_header(self):
        """輸出報告強制欄位（規格 #1）"""
        print("\\n" + "=" * 70)
        print("Layer: Operational (Evidence Generation)")
        print("Era: 1 (Evidence-Native Bootstrap)")
        print("Semantic Closure: NO (Evidence layer only, governance not closed)")
        print("=" * 70 + "\\n")

    def _print_history_disclaimer(self):
        """輸出歷史完整性聲明（規格 #4）"""
        print("\\n" + "=" * 70)
        print("⚠️ 歷史完整性聲明")
        print("=" * 70)
        print("- Era-0 歷史沒有完整的證據鏈，只能部分重建")
        print("- Era-1 是本系統第一個具備完整證據鏈的時期，仍在演化中")
        print("- 治理閉環、不可變核心、完整 MNGA 合規「尚未完成」")
        print("=" * 70 + "\\n")

    def _print_pending_governance_section(self):
        """輸出尚未完成的治理面（規格 #6）"""
        print("\\n" + "=" * 70)
        print("🚧 尚未完成的治理面（Era-1 現狀）")
        print("=" * 70)
        print("\\n### ❌ 尚未建立")
        print("- Era 封存流程（Era Sealing Protocol）")
        print("- Core hash 封存（core-hash.json 標記為 SEALED）")
        print("- Semantic Distillation 流程")
        print("- v1.0.0 抽離與版本管理")
        print("\\n### ⏳ 進行中")
        print("- Semantic Closure 定義與驗證")
        print("- Immutable Core 邊界確定")
        print("- 完整 Lineage 重建與驗證")
        print("\\n### ✅ 已完成（Era-1）")
        print("- Evidence Generation Layer 啟動")
        print("- Event Stream 基礎設施")
        print("- SHA256 完整性保護")
        print("- Step-by-Step 執行軌跡")
        print("=" * 70 + "\\n")

    def _print_era_1_conclusion(self):
        """輸出 Era-1 結論（規格 #5）"""
        print("\\n" + "=" * 70)
        print("🎯 結論")
        print("=" * 70)
        print("本次變更屬於 Evidence-Native Bootstrap，而非完整治理閉環。")
        print("目前僅在 Operational Layer 達成穩定，Governance Layer 仍在建構中。")
        print("未來仍需：Era 封存、核心 hash 封存、語義閉環與治理一致性驗證。")
        print("=" * 70 + "\\n")
'''
    
    # 在 class EnforcementCoordinator 末尾（在 run_full_cycle 方法之前）新增方法
    pattern = r'(class EnforcementCoordinator:.*?\n    def run_full_cycle)'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(
            pattern,
            r'\1' + new_methods,
            content,
            count=1,
            flags=re.DOTALL
        )
        print("✅ 新增 4 個報告輸出方法")
    
    # 修復 2: 修改 step_2_local_reasoning 中的 "Engines: 100%"
    old_engines = r'print\(f"   ✅ Engines: \{completeness\[\'engines\'\]\}"\)'
    new_engines = 'print(f"   ⏸️  Engines: PARTIAL - Core engines present, validation incomplete")'
    if re.search(old_engines, content):
        content = re.sub(old_engines, new_engines, content)
        print("✅ 修復 Step 2 的虛假 Engine 聲明")
    
    # 修復 3: 修改 step_2_local_reasoning 中的 "No gaps found"
    old_gaps = r'gaps = \[\]\s+if not gaps:\s+print\("   ✅ No gaps found"\)'
    new_gaps = '''gaps = [
            "Evidence verification logic: MISSING",
            "Governance closure: NOT DEFINED"
        ]
        if gaps:
            print("   ⚠️  Gaps found:")
            for gap in gaps:
                print(f"      - {gap}")'''
    if re.search(old_gaps, content, re.MULTILINE):
        content = re.sub(old_gaps, new_gaps, content, flags=re.MULTILINE)
        print("✅ 修復 Step 2 的缺口分析")
    
    # 修復 4: 修改 step_2_local_reasoning 中的 "No risks detected"
    old_risks = r'risks = \[\]\s+if not risks:\s+print\("   ✅ No risks detected"\)'
    new_risks = '''risks = [
            "Evidence credibility risk: Present (historical)",
            "Governance completeness risk: Present"
        ]
        if risks:
            print("   ⚠️  Risks detected:")
            for risk in risks:
                print(f"      - {risk}")'''
    if re.search(old_risks, content, re.MULTILINE):
        content = re.sub(old_risks, new_risks, content, flags=re.MULTILINE)
        print("✅ 修復 Step 2 的風險分析")
    
    # 修復 5: 修改 step_10_loop_back 中的終態敘事
    old_final = r'print\(f"\\n✅ Governance Closed Loop Established"\)\s+print\(f"\\n🎉 The 10-step closed-loop governance cycle is now active!"\)\s+print\(f"   Ready to loop back to Step 1 for perpetual governance\.\.\."\)'
    new_final = 'print(f"\\n✅ Era-1 Evidence-Native Bootstrap 階段完成")\\n        print(f"   系統已準備進入持續治理循環")'
    if re.search(old_final, content, re.MULTILINE | re.DOTALL):
        content = re.sub(old_final, new_final, content, flags=re.MULTILINE | re.DOTALL)
        print("✅ 修復 Step 10 的終態敘事")
    
    # 修復 6: 在 run_full_cycle 開頭添加報告頭
    old_run_start = r'(def run_full_cycle\(self\).*?print\("="\*70\)\s+print\("🚀 Immutable Core Governance Engineering Methodology v1\.0"\))'
    new_run_start = r'\1\n        \n        # 在所有步驟之前輸出報告頭\n        self._print_report_header()'
    if re.search(old_run_start, content, re.DOTALL):
        content = re.sub(old_run_start, new_run_start, content, flags=re.DOTALL)
        print("✅ 在 run_full_cycle 開頭添加報告頭")
    
    # 修復 7: 修改總結標題
    old_summary = r'print\("✅ 10-Step Closed-Loop Governance Cycle Complete"\)'
    new_summary = 'print("✅ 10-Step Closed-Loop Governance Cycle - Era-1 Bootstrap Complete")'
    if old_summary in content:
        content = content.replace(old_summary, new_summary)
        print("✅ 修復總結標題")
    
    # 修復 8: 在 Step 10 之後添加額外區塊
    old_before_summary = r'(result_10 = self\.step_10_loop_back\(\)\s+results\.append\(result_10\)\s+\s+# 總結)'
    new_before_summary = r'\1\n            \n            # 在 Step 10 之後輸出額外區塊\n            self._print_pending_governance_section()\n            self._print_history_disclaimer()\n            self._print_era_1_conclusion()'
    if re.search(old_before_summary, content):
        content = re.sub(old_before_summary, new_before_summary, content)
        print("✅ 在 Step 10 之後添加額外區塊")
    
    # 寫回文件
    if content != original_content:
        # 創建備份
        backup_path = file_path.with_suffix('.py.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"✅ 創建備份: {backup_path}")
        
        # 寫入修正後的內容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修正完成: {file_path}")
        return True
    else:
        print("⚠️  沒有需要修改的內容")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("修復 ecosystem/enforce.rules.py 的報告生成邏輯")
    print("=" * 70)
    print()
    
    success = fix_enforce_rules()
    
    print()
    print("=" * 70)
    if success:
        print("✅ 修復成功完成")
        print()
        print("下一步:")
        print("1. 運行: python ecosystem/enforce.rules.py")
        print("2. 驗證報告合規性: python ecosystem/tools/reporting_compliance_checker.py <output.txt>")
    else:
        print("⚠️  修復失敗或無需修改")
    print("=" * 70)