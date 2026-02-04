#!/usr/bin/env python3
"""
Reporting Governance Compliance Checker
報告治理合規性檢查器

This script validates governance reports against the Reporting Governance Specification
(ecosystem/governance/reporting-governance-spec.md)

Usage:
    python ecosystem/tools/reporting_compliance_checker.py <report_file>
    python ecosystem/tools/reporting_compliance_checker.py --audit
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class ComplianceIssue:
    severity: Severity
    rule_number: str
    description: str
    location: str
    suggestion: Optional[str] = None


class ReportingComplianceChecker:
    """檢查治理報告是否符合報告生成強制規格"""
    
    # 強制規格要求
    REQUIRED_FIELDS = ["Layer:", "Era:", "Semantic Closure:"]
    
    # 禁止的終態敘事詞彙
    FORBIDDEN_PHRASES = [
        "100% 治理合規",
        "100%治理合規",
        "所有治理元件全部通過",
        "完整治理閉環",
        "系統已完全準備好投入生產",
        "已準備就緒，可投入生產",
        "MNGA 架構完全通過",
        "治理閉環已建立",
        "Ready for Deployment: True",
        "Governance Closed Loop Established",
        "10-Step Closed-Loop Governance Cycle Complete",
        "governance cycle is now active"
    ]
    
    # 允許的 Era-1 上下文詞彙（用於檢測是否在 Era-1 上下文中）
    ERA_1_CONTEXT = [
        "Era-1",
        "Evidence-Native Bootstrap",
        "Evidence-Native",
        "Bootstrap"
    ]
    
    # 歷史缺口聲明的必需關鍵詞
    HISTORY_GAP_KEYWORDS = [
        "Era-0",
        "歷史",
        "證據鏈",
        "尚未完成",
        "仍在演化"
    ]
    
    def __init__(self, report_path: str):
        self.report_path = Path(report_path)
        self.issues: List[ComplianceIssue] = []
        self.report_content = ""
        
    def load_report(self) -> bool:
        """載入報告文件"""
        if not self.report_path.exists():
            self.issues.append(ComplianceIssue(
                severity=Severity.CRITICAL,
                rule_number="R0",
                description=f"報告文件不存在: {self.report_path}",
                location="File System"
            ))
            return False
        
        with open(self.report_path, 'r', encoding='utf-8') as f:
            self.report_content = f.read()
        
        return True
    
    def check_required_fields(self) -> None:
        """檢查 1：開頭三個必備欄位"""
        # 檢查是否在報告開頭（前 20 行）
        lines = self.report_content.split('\n')[:20]
        header_content = '\n'.join(lines)
        
        for field in self.REQUIRED_FIELDS:
            if field not in header_content:
                self.issues.append(ComplianceIssue(
                    severity=Severity.CRITICAL,
                    rule_number="R1",
                    description=f"缺少必需欄位: {field}",
                    location="Report Header",
                    suggestion=f"在報告開頭添加: **{field}**"
                ))
            else:
                # 驗證欄位值
                field_line = [line for line in lines if field in line]
                if field_line:
                    value = field_line[0].split(field)[1].strip().strip('*').strip()
                    
                    if field == "Layer:":
                        # 提取主值（去除括號內的說明）
                        layer_main = value.split('(')[0].strip()
                        if layer_main not in ["Operational", "Governance"]:
                            self.issues.append(ComplianceIssue(
                                severity=Severity.HIGH,
                                rule_number="R1",
                                description=f"Layer 值無效: {value}（主值必須是 Operational 或 Governance）",
                                location="Report Header"
                            ))
                    
                    elif field == "Era:":
                        if not re.match(r'\d+\s+\(.+\)', value):
                            self.issues.append(ComplianceIssue(
                                severity=Severity.HIGH,
                                rule_number="R1",
                                description=f"Era 格式無效: {value}（必須是: 數字 (名稱)）",
                                location="Report Header"
                            ))
                    
                    elif field == "Semantic Closure:":
                        # 提取主值（去除括號內的說明）
                        closure_main = value.split('(')[0].strip()
                        if closure_main not in ["YES", "NO"]:
                            self.issues.append(ComplianceIssue(
                                severity=Severity.HIGH,
                                rule_number="R1",
                                description=f"Semantic Closure 值無效: {value}（主值必須是 YES 或 NO）",
                                location="Report Header"
                            ))
    
    def check_forbidden_phrases(self) -> None:
        """檢查 2：禁止的終態敘事"""
        # 檢查是否有達到終態的條件（已封存、已閉環等）
        has_sealed_condition = (
            "SEALED" in self.report_content and
            "core-hash.json" in self.report_content
        )
        has_closure_condition = (
            "Semantic Closure: YES" in self.report_content or
            "語義閉環" in self.report_content and "已完成" in self.report_content
        )
        
        # 如果沒有達到終態條件，則嚴格檢查禁止詞彙
        if not (has_sealed_condition and has_closure_condition):
            for phrase in self.FORBIDDEN_PHRASES:
                if phrase in self.report_content:
                    self.issues.append(ComplianceIssue(
                        severity=Severity.CRITICAL,
                        rule_number="R2",
                        description=f"使用禁止的終態敘事: &quot;{phrase}&quot;",
                        location="Full Report",
                        suggestion=f"替代方案: 將其改為 Era-1 上下文，例如「Era-1 Evidence-Native Bootstrap 完成」"
                    ))
    
    def check_history_gap_statement(self) -> None:
        """檢查 4：歷史缺口聲明"""
        history_section = False
        found_keywords = set()
        
        # 尋找歷史相關的段落
        lines = self.report_content.split('\n')
        for i, line in enumerate(lines):
            # 檢查是否有歷史相關的標題或段落
            if "歷史" in line or "History" in line or "Era-0" in line:
                # 檢查接下來的 20 行
                context = '\n'.join(lines[i:i+20])
                for keyword in self.HISTORY_GAP_KEYWORDS:
                    if keyword in context:
                        found_keywords.add(keyword)
                        history_section = True
        
        if not history_section or len(found_keywords) < 3:
            self.issues.append(ComplianceIssue(
                severity=Severity.CRITICAL,
                rule_number="R4",
                description="缺少歷史缺口聲明或聲明不完整",
                location="History Section",
                suggestion="添加歷史完整性聲明，說明 Era-0 證據鏈缺損、Era-1 是第一個具備證據鏈的時期"
            ))
    
    def check_pending_governance_section(self) -> None:
        """檢查 6：尚未完成的治理面專門區塊"""
        # 尋找專門區塊
        lines = self.report_content.split('\n')
        found_section = False
        has_three_states = False
        
        for i, line in enumerate(lines):
            if "尚未完成" in line or "Pending" in line or "Incomplete" in line:
                # 檢查這是否是一個標題（### 或 ##）
                if line.strip().startswith('##'):
                    found_section = True
                    # 檢查接下來的內容是否有三種狀態
                    context = '\n'.join(lines[i:i+30])
                    has_not_built = "尚未建立" in context or "❌" in context
                    has_in_progress = "進行中" in context or "⏳" in context
                    has_completed = "已完成" in context or "✅" in context
                    
                    if has_not_built and has_in_progress and has_completed:
                        has_three_states = True
                    break
        
        if not found_section:
            self.issues.append(ComplianceIssue(
                severity=Severity.HIGH,
                rule_number="R6",
                description="缺少「尚未完成的治理面」專門區塊",
                location="Pending Governance Section",
                suggestion="添加專門區塊，區分「尚未建立」、「進行中」、「已完成」三種狀態"
            ))
        elif not has_three_states:
            self.issues.append(ComplianceIssue(
                severity=Severity.HIGH,
                rule_number="R6",
                description="「尚未完成的治理面」區塊不完整",
                location="Pending Governance Section",
                suggestion="確保區塊包含三種狀態：尚未建立（❌）、進行中（⏳）、已完成（✅）"
            ))
    
    def check_era_1_positioning(self) -> None:
        """檢查 3：Era-1 的正確定位"""
        # 檢查是否有 Era-1 的正確定位聲明
        era_1_positioning_keywords = [
            "Evidence-Native Bootstrap",
            "Operational Layer",
            "Governance Layer",
            "仍在建構中"
        ]
        
        has_correct_positioning = any(
            keyword in self.report_content 
            for keyword in era_1_positioning_keywords
        )
        
        # 檢查是否有錯誤的終態聲明
        has_final_state = any(
            phrase in self.report_content 
            for phrase in ["已完成", "完成", "100%", "Ready"]
        )
        
        if has_final_state and not has_correct_positioning:
            self.issues.append(ComplianceIssue(
                severity=Severity.MEDIUM,
                rule_number="R3",
                description="缺少 Era-1 的正確定位聲明",
                location="Report Content",
                suggestion="添加 Era-1 範圍說明，明確區分 Operational Layer 和 Governance Layer"
            ))
    
    def check_conclusion_tone(self) -> None:
        """檢查 5：允許的結論語氣"""
        # 尋找結論部分
        lines = self.report_content.split('\n')
        conclusion_found = False
        conclusion_tone_ok = False
        
        for i, line in enumerate(lines):
            if "結論" in line or "Conclusion" in line:
                conclusion_found = True
                # 檢查結論部分
                context = '\n'.join(lines[i:i+15])
                # 檢查是否有正確的結論語氣
                if any(phrase in context for phrase in [
                    "Evidence-Native Bootstrap",
                    "Operational Layer",
                    "Governance Layer",
                    "尚未完成",
                    "仍需"
                ]):
                    conclusion_tone_ok = True
                break
        
        if conclusion_found and not conclusion_tone_ok:
            self.issues.append(ComplianceIssue(
                severity=Severity.MEDIUM,
                rule_number="R5",
                description="結論語氣超出允許範圍",
                location="Conclusion Section",
                suggestion="使用允許的結論語氣，強調 Era-1 的 Bootstrap 性質和 Governance Layer 的未完成狀態"
            ))
    
    def run_all_checks(self) -> List[ComplianceIssue]:
        """執行所有檢查"""
        if not self.load_report():
            return self.issues
        
        # 執行所有檢查規則
        self.check_required_fields()
        self.check_forbidden_phrases()
        self.check_history_gap_statement()
        self.check_pending_governance_section()
        self.check_era_1_positioning()
        self.check_conclusion_tone()
        
        return self.issues
    
    def generate_report(self) -> str:
        """生成合規性檢查報告"""
        report = []
        report.append("=" * 80)
        report.append("報告治理合規性檢查")
        report.append("=" * 80)
        report.append(f"\n報告文件: {self.report_path}")
        report.append(f"檢查時間: 2026-02-03")
        report.append(f"依據規格: ecosystem/governance/reporting-governance-spec.md")
        
        # 統計問題
        critical_issues = [i for i in self.issues if i.severity == Severity.CRITICAL]
        high_issues = [i for i in self.issues if i.severity == Severity.HIGH]
        medium_issues = [i for i in self.issues if i.severity == Severity.MEDIUM]
        
        report.append("\n" + "=" * 80)
        report.append("問題統計")
        report.append("=" * 80)
        report.append(f"🔴 CRITICAL: {len(critical_issues)}")
        report.append(f"🟠 HIGH: {len(high_issues)}")
        report.append(f"🟡 MEDIUM: {len(medium_issues)}")
        report.append(f"📊 總計: {len(self.issues)}")
        
        # 詳細問題
        if self.issues:
            report.append("\n" + "=" * 80)
            report.append("詳細問題")
            report.append("=" * 80)
            
            for i, issue in enumerate(self.issues, 1):
                severity_icon = {
                    Severity.CRITICAL: "🔴",
                    Severity.HIGH: "🟠",
                    Severity.MEDIUM: "🟡",
                    Severity.LOW: "🟢"
                }.get(issue.severity, "⚪")
                
                report.append(f"\n{i}. [{severity_icon}] {issue.severity.value} - {issue.rule_number}")
                report.append(f"   描述: {issue.description}")
                report.append(f"   位置: {issue.location}")
                if issue.suggestion:
                    report.append(f"   建議: {issue.suggestion}")
        
        # 合規性評分
        total_score = 100
        score_deduction = len(critical_issues) * 20 + len(high_issues) * 10 + len(medium_issues) * 5
        final_score = max(0, total_score - score_deduction)
        
        report.append("\n" + "=" * 80)
        report.append("合規性評分")
        report.append("=" * 80)
        report.append(f"原始分數: 100")
        report.append(f"扣分: {score_deduction}")
        report.append(f"最終分數: {final_score}/100")
        
        if final_score >= 90:
            compliance_status = "✅ PASS - 優秀"
        elif final_score >= 70:
            compliance_status = "⚠️ PASS - 需改進"
        elif final_score >= 50:
            compliance_status = "🟠 WARNING - 有嚴重問題"
        else:
            compliance_status = "🔴 FAIL - 不合規"
        
        report.append(f"狀態: {compliance_status}")
        
        # 處理建議
        if critical_issues:
            report.append("\n" + "=" * 80)
            report.append("處理建議")
            report.append("=" * 80)
            report.append("🔴 存在 CRITICAL 問題，建議：")
            report.append("   1. 阻擋報告發布")
            report.append("   2. 要求重寫報告")
            report.append("   3. 記錄到治理事件流")
        
        report.append("\n" + "=" * 80)
        
        return '\n'.join(report)


def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("用法: python reporting_compliance_checker.py <report_file>")
        print("      python reporting_compliance_checker.py --audit  (檢查所有報告)")
        sys.exit(1)
    
    if sys.argv[1] == "--audit":
        # 審計模式：檢查 reports/ 目錄下的所有報告
        reports_dir = Path("reports")
        if not reports_dir.exists():
            print(f"錯誤: reports/ 目錄不存在")
            sys.exit(1)
        
        report_files = list(reports_dir.glob("*.md"))
        if not report_files:
            print(f"未找到任何報告文件")
            sys.exit(0)
        
        print(f"找到 {len(report_files)} 個報告文件")
        print("=" * 80)
        
        all_issues = []
        for report_file in report_files:
            print(f"\n檢查: {report_file}")
            checker = ReportingComplianceChecker(str(report_file))
            issues = checker.run_all_checks()
            all_issues.extend(issues)
            
            # 輸出簡要結果
            critical_count = sum(1 for i in issues if i.severity == Severity.CRITICAL)
            high_count = sum(1 for i in issues if i.severity == Severity.HIGH)
            print(f"  🔴 CRITICAL: {critical_count}, 🟠 HIGH: {high_count}, 🟡 MEDIUM: {len(issues) - critical_count - high_count}")
        
        # 總結
        print("\n" + "=" * 80)
        print("總結")
        print("=" * 80)
        print(f"總共檢查: {len(report_files)} 個報告")
        print(f"總共發現: {len(all_issues)} 個問題")
        
        critical_total = sum(1 for i in all_issues if i.severity == Severity.CRITICAL)
        high_total = sum(1 for i in all_issues if i.severity == Severity.HIGH)
        print(f"🔴 CRITICAL: {critical_total}")
        print(f"🟠 HIGH: {high_total}")
        print(f"🟡 MEDIUM: {len(all_issues) - critical_total - high_total}")
        
        if critical_total > 0:
            print("\n🔴 建議：阻擋發布，要求修正所有 CRITICAL 問題")
        elif high_total > 0:
            print("\n🟠 建議：警告但仍允許發布，建議修正 HIGH 問題")
        else:
            print("\n✅ 所有報告合規")
        
    else:
        # 單文件檢查模式
        report_file = sys.argv[1]
        checker = ReportingComplianceChecker(report_file)
        issues = checker.run_all_checks()
        
        report = checker.generate_report()
        print(report)
        
        # 根據嚴重性返回不同的退出碼
        critical_count = sum(1 for i in issues if i.severity == Severity.CRITICAL)
        high_count = sum(1 for i in issues if i.severity == Severity.HIGH)
        
        if critical_count > 0:
            sys.exit(2)  # FAIL
        elif high_count > 0:
            sys.exit(1)  # WARNING
        else:
            sys.exit(0)  # PASS


if __name__ == "__main__":
    main()