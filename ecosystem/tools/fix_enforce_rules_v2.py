#!/usr/bin/env python3
"""
修復 ecosystem/enforce.rules.py 的報告生成邏輯 - 第二版
使用逐行修改方法，避免複雜的正則表達式
"""

import sys
from pathlib import Path


def add_methods_before_run_full_cycle():
    """在 run_full_cycle 方法之前添加新方法"""
    file_path = Path("ecosystem/enforce.rules.py")
    
    # 新增的方法
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
    
    # 讀取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到 run_full_cycle 方法的位置
    for i, line in enumerate(lines):
        if 'def run_full_cycle(self)' in line:
            # 在這行之前插入新方法
            lines.insert(i, new_methods)
            print(f"✅ 在第 {i+1} 行之前添加新方法")
            break
    else:
        print("⚠️  未找到 run_full_cycle 方法")
        return False
    
    # 寫回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return True


def modify_step_2():
    """修改 step_2_local_reasoning 方法"""
    file_path = Path("ecosystem/enforce.rules.py")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False
    
    for i, line in enumerate(lines):
        # 修復 Engine 聲明
        if 'print(f"   ✅ Engines: {completeness[\'engines\']}")' in line:
            lines[i] = '        print(f"   ⏸️  Engines: PARTIAL - Core engines present, validation incomplete")\\n'
            print(f"✅ 修復第 {i+1} 行: Engine 聲明")
            modified = True
        
        # 修復缺口分析
        if 'gaps = []' in line and i < len(lines) - 3:
            if 'if not gaps:' in lines[i+1] and 'print("   ✅ No gaps found")' in lines[i+2]:
                lines[i:i+3] = [
                    '        gaps = [\\n',
                    '            "Evidence verification logic: MISSING",\\n',
                    '            "Governance closure: NOT DEFINED"\\n',
                    '        ]\\n',
                    '        if gaps:\\n',
                    '            print("   ⚠️  Gaps found:")\\n',
                    '            for gap in gaps:\\n',
                    '                print(f"      - {gap}")\\n'
                ]
                print(f"✅ 修復第 {i+1} 行: 缺口分析")
                modified = True
        
        # 修復風險分析
        if 'risks = []' in line and i < len(lines) - 3:
            if 'if not risks:' in lines[i+1] and 'print("   ✅ No risks detected")' in lines[i+2]:
                lines[i:i+3] = [
                    '        risks = [\\n',
                    '            "Evidence credibility risk: Present (historical)",\\n',
                    '            "Governance completeness risk: Present"\\n',
                    '        ]\\n',
                    '        if risks:\\n',
                    '            print("   ⚠️  Risks detected:")\\n',
                    '            for risk in risks:\\n',
                    '                print(f"      - {risk}")\\n'
                ]
                print(f"✅ 修復第 {i+1} 行: 風險分析")
                modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    return modified


def modify_step_10():
    """修改 step_10_loop_back 方法"""
    file_path = Path("ecosystem/enforce.rules.py")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False
    
    for i, line in enumerate(lines):
        # 修復終態敘事
        if 'print(f"\\n✅ Governance Closed Loop Established")' in line:
            lines[i] = '        print(f"\\n✅ Era-1 Evidence-Native Bootstrap 階段完成")\\n'
            print(f"✅ 修復第 {i+1} 行: 終態敘事")
            modified = True
        
        if 'print(f"\\n🎉 The 10-step closed-loop governance cycle is now active!")' in line:
            lines[i] = '        print(f"   系統已準備進入持續治理循環")\\n'
            print(f"✅ 修復第 {i+1} 行: 激活敘事")
            modified = True
        
        if 'print(f"   Ready to loop back to Step 1 for perpetual governance...")' in line:
            lines[i] = '\\n'
            print(f"✅ 移除第 {i+1} 行: 重複敘事")
            modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    return modified


def modify_run_full_cycle():
    """修改 run_full_cycle 方法"""
    file_path = Path("ecosystem/enforce.rules.py")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False
    
    for i, line in enumerate(lines):
        # 在方法開頭添加報告頭調用
        if 'print("🚀 Immutable Core Governance Engineering Methodology v1.0")' in line:
            if i < len(lines) - 2:
                if 'print("="*70)' in lines[i+1] and not '_print_report_header' in lines[i-1]:
                    lines.insert(i+2, '\\n        # 在所有步驟之前輸出報告頭\\n        self._print_report_header()\\n')
                    print(f"✅ 在第 {i+3} 行添加報告頭調用")
                    modified = True
        
        # 修改總結標題
        if 'print("✅ 10-Step Closed-Loop Governance Cycle Complete")' in line:
            lines[i] = '            print("✅ 10-Step Closed-Loop Governance Cycle - Era-1 Bootstrap Complete")\\n'
            print(f"✅ 修復第 {i+1} 行: 總結標題")
            modified = True
        
        # 在 Step 10 之後添加額外區塊
        if 'result_10 = self.step_10_loop_back()' in line and i < len(lines) - 2:
            if 'results.append(result_10)' in lines[i+1] and '# 總結' in lines[i+2]:
                lines.insert(i+2, '\\n            # 在 Step 10 之後輸出額外區塊\\n            self._print_pending_governance_section()\\n            self._print_history_disclaimer()\\n            self._print_era_1_conclusion()\\n')
                print(f"✅ 在第 {i+3} 行添加額外區塊")
                modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    return modified


def main():
    """主函數"""
    file_path = Path("ecosystem/enforce.rules.py")
    
    if not file_path.exists():
        print(f"錯誤: 文件不存在 {file_path}")
        sys.exit(1)
    
    # 創建備份
    backup_path = file_path.with_suffix('.py.backup')
    import shutil
    shutil.copy2(file_path, backup_path)
    print(f"✅ 創建備份: {backup_path}")
    print()
    
    print("步驟 1: 添加新方法")
    if not add_methods_before_run_full_cycle():
        print("⚠️  添加新方法失敗")
    
    print()
    print("步驟 2: 修改 Step 2")
    if not modify_step_2():
        print("⚠️  修改 Step 2 失敗")
    
    print()
    print("步驟 3: 修改 Step 10")
    if not modify_step_10():
        print("⚠️  修改 Step 10 失敗")
    
    print()
    print("步驟 4: 修改 run_full_cycle")
    if not modify_run_full_cycle():
        print("⚠️  修改 run_full_cycle 失敗")
    
    print()
    print("=" * 70)
    print("✅ 修復完成")
    print()
    print("下一步:")
    print("1. 驗證語法: python -m py_compile ecosystem/enforce.rules.py")
    print("2. 運行測試: python ecosystem/enforce.rules.py")
    print("3. 檢查合規性: python ecosystem/tools/reporting_compliance_checker.py <output.txt>")
    print("=" * 70)


if __name__ == "__main__":
    main()