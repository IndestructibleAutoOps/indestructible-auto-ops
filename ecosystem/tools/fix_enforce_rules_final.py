#!/usr/bin/env python3
"""
修復 ecosystem/enforce.rules.py 的報告生成邏輯 - 最終版本
使用直接的字符串替換，確保不引入語法錯誤
"""

from pathlib import Path


def main():
    """主函數"""
    file_path = Path("ecosystem/enforce.rules.py")
    
    if not file_path.exists():
        print(f"錯誤: 文件不存在 {file_path}")
        return False
    
    # 創建備份
    backup_path = file_path.with_suffix('.py.backup')
    import shutil
    shutil.copy2(file_path, backup_path)
    print(f"✅ 創建備份: {backup_path}")
    print()
    
    # 讀取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 步驟 1: 添加新方法
    print("步驟 1: 添加新方法")
    if '_print_report_header' not in content:
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
        # 在 run_full_cycle 方法之前插入
        marker = '    def run_full_cycle(self)'
        if marker in content:
            content = content.replace(marker, new_methods + marker)
            print("✅ 添加新方法")
        else:
            print("⚠️  未找到插入點")
    else:
        print("⚠️  新方法已存在，跳過")
    
    # 步驟 2: 修改 Step 2
    print()
    print("步驟 2: 修改 Step 2")
    
    old1 = 'print(f"   ✅ Engines: {completeness[\'engines\']}")'
    new1 = 'print(f"   ⏸️  Engines: PARTIAL - Core engines present, validation incomplete")'
    if old1 in content:
        content = content.replace(old1, new1)
        print("✅ 修復 Step 2 的 Engine 聲明")
    
    old2 = '''        gaps = []
        if not gaps:
            print("   ✅ No gaps found")'''
    new2 = '''        gaps = [
            "Evidence verification logic: MISSING",
            "Governance closure: NOT DEFINED"
        ]
        if gaps:
            print("   ⚠️  Gaps found:")
            for gap in gaps:
                print(f"      - {gap}")'''
    if old2 in content:
        content = content.replace(old2, new2)
        print("✅ 修復 Step 2 的缺口分析")
    
    old3 = '''        risks = []
        if not risks:
            print("   ✅ No risks detected")'''
    new3 = '''        risks = [
            "Evidence credibility risk: Present (historical)",
            "Governance completeness risk: Present"
        ]
        if risks:
            print("   ⚠️  Risks detected:")
            for risk in risks:
                print(f"      - {risk}")'''
    if old3 in content:
        content = content.replace(old3, new3)
        print("✅ 修復 Step 2 的風險分析")
    
    # 步驟 3: 修改 Step 10
    print()
    print("步驟 3: 修改 Step 10")
    
    old4 = 'print(f"\\n✅ Governance Closed Loop Established")'
    new4 = 'print(f"\\n✅ Era-1 Evidence-Native Bootstrap 階段完成")'
    if old4 in content:
        content = content.replace(old4, new4)
        print("✅ 修復 Step 10 的終態敘事（1）")
    
    old5 = 'print(f"\\n🎉 The 10-step closed-loop governance cycle is now active!")'
    new5 = 'print(f"   系統已準備進入持續治理循環")'
    if old5 in content:
        content = content.replace(old5, new5)
        print("✅ 修復 Step 10 的終態敘事（2）")
    
    old6 = 'print(f"   Ready to loop back to Step 1 for perpetual governance...")'
    if old6 in content:
        content = content.replace(old6, '')
        print("✅ 移除重複敘事")
    
    # 步驟 4: 修改 run_full_cycle
    print()
    print("步驟 4: 修改 run_full_cycle")
    
    old7 = 'print("✅ 10-Step Closed-Loop Governance Cycle Complete")'
    new7 = 'print("✅ 10-Step Closed-Loop Governance Cycle - Era-1 Bootstrap Complete")'
    if old7 in content:
        content = content.replace(old7, new7)
        print("✅ 修復總結標題")
    
    old8 = '''result_10 = self.step_10_loop_back()
            results.append(result_10)

            # 總結'''
    new8 = '''result_10 = self.step_10_loop_back()
            results.append(result_10)

            # 在 Step 10 之後輸出額外區塊
            self._print_pending_governance_section()
            self._print_history_disclaimer()
            self._print_era_1_conclusion()

            # 總結'''
    if old8 in content:
        content = content.replace(old8, new8)
        print("✅ 在 Step 10 之後添加額外區塊")
    
    old9 = '''print("🚀 Immutable Core Governance Engineering Methodology v1.0")
        print("="*70)

        start_time = datetime.now(timezone.utc)'''
    new9 = '''print("🚀 Immutable Core Governance Engineering Methodology v1.0")
        print("="*70)

        # 在所有步驟之前輸出報告頭
        self._print_report_header()

        start_time = datetime.now(timezone.utc)'''
    if old9 in content:
        content = content.replace(old9, new9)
        print("✅ 在 run_full_cycle 開頭添加報告頭調用")
    
    # 寫回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print()
        print("=" * 70)
        print("✅ 修復完成")
        print()
        print("下一步:")
        print("1. 驗證語法: python -m py_compile ecosystem/enforce.rules.py")
        print("2. 運行測試: python ecosystem/enforce.rules.py")
        print("3. 檢查合規性: python ecosystem/tools/reporting_compliance_checker.py <output.txt>")
        print("=" * 70)
        return True
    else:
        print()
        print("⚠️  沒有需要修改的內容")
        return False


if __name__ == "__main__":
    main()