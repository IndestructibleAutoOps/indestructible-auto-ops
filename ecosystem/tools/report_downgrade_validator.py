#!/usr/bin/env python3
"""
報告降階驗證工具
Report Downgrade Validator

功能：檢測並驗證報告降階，移除不符合 Era-1 狀態的高級語義
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Set
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class SemanticIssue:
    """語義問題"""
    line: int
    column: int
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    issue_type: str
    description: str
    context: str
    suggested_fix: str


@dataclass
class DowngradeReport:
    """降階報告"""
    file_path: str
    total_issues: int = 0
    critical_issues: int = 0
    high_issues: int = 0
    medium_issues: int = 0
    low_issues: int = 0
    issues: List[SemanticIssue] = field(default_factory=list)
    downgrade_needed: bool = False
    downgrade_percentage: float = 0.0


class ReportDowngradeValidator:
    """報告降階驗證器"""
    
    def __init__(self, workspace: str = "/workspace"):
        self.workspace = Path(workspace)
        self.ecosystem_root = self.workspace / "ecosystem"
        self.current_era = "1"
        self.current_layer = "Operational (Evidence Generation)"
        self.current_semantic_closure = "NO"
        
        # Era-1 禁止的術語和模式
        self.forbidden_terminology = {
            "CRITICAL": [
                # 虛構階段
                r"Phase\s+[1-9]",
                r"階段\s+[1-9]",
                r"第\s+[一二三四五六七八九十]\s*階段",
                
                # 未封存前的禁止術語
                r"完整性[保証保证]",
                r"封存",
                r"密封",
                r"鎖定",
                
                # 虛假完成聲明
                r"最終",
                r"完成[狀状态態]",
                r"結束",
                r"終點",
            ],
            "HIGH": [
                # 高級架構聲明
                r"完全[一致性统一]",
                r"統一治理",
                r"完整閉環",
                
                # 過度聲明
                r"100%[保保証証]",
                r"完美",
                r"無缺[陷点]",
            ],
            "MEDIUM": [
                # 不確定的未來聲明
                r"將[会會]",
                r"未來",
                r"預期",
                
                # 主觀評價
                r"優秀",
                r"完美",
                r"最佳",
            ]
        }
        
        # Era-1 允許的語言模式
        self.allowed_patterns = {
            "Era": r"Era\s*:\s*[01]",
            "Layer": r"Layer\s*:\s*Operational\s*\(Evidence\s+Generation\)",
            "SemanticClosure": r"Semantic\s+Closure\s*:\s*NO",
            "EraState": r"Era.*Bootstrap|Era.*初始化|Era.*啟動",
        }
        
        # 需要的元數據字段
        self.required_metadata = {
            "Era": self.current_era,
            "Layer": self.current_layer,
            "SemanticClosure": self.current_semantic_closure,
        }
    
    def read_file(self, file_path: str) -> List[str]:
        """讀取文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.readlines()
        except Exception as e:
            print(f"❌ 讀取文件失敗: {e}")
            return []
    
    def check_forbidden_terminology(self, lines: List[str]) -> List[SemanticIssue]:
        """檢查禁止術語"""
        issues = []
        
        for line_num, line in enumerate(lines, 1):
            for severity, patterns in self.forbidden_terminology.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE | re.UNICODE)
                    for match in matches:
                        issue = SemanticIssue(
                            line=line_num,
                            column=match.start() + 1,
                            severity=severity,
                            issue_type="forbidden_terminology",
                            description=f"檢測到禁止術語: '{match.group()}'",
                            context=line.strip(),
                            suggested_fix=self._suggest_fix(match.group(), severity)
                        )
                        issues.append(issue)
        
        return issues
    
    def check_allowed_patterns(self, lines: List[str]) -> List[SemanticIssue]:
        """檢查允許的模式（確保存在）"""
        issues = []
        file_content = ''.join(lines)
        
        for field, pattern in self.required_metadata.items():
            if not re.search(pattern, file_content, re.IGNORECASE):
                issue = SemanticIssue(
                    line=1,
                    column=1,
                    severity="CRITICAL",
                    issue_type="missing_metadata",
                    description=f"缺少必要的元數據字段: {field} (應為: {self.required_metadata[field]})",
                    context="文件頂部",
                    suggested_fix=f"添加元數據: {field}: {self.required_metadata[field]}"
                )
                issues.append(issue)
        
        return issues
    
    def check_phase_declarations(self, lines: List[str]) -> List[SemanticIssue]:
        """檢查虛構的階段聲明"""
        issues = []
        
        phase_patterns = [
            r"Phase\s+[1-9]",
            r"階段\s*[1-9一二三四五六七八九十]",
            r"第\s*[一二三四五六七八九十]\s*階段",
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern in phase_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # 檢查是否在允許的上下文中（如 Era 描述）
                    allowed_contexts = [r"Era", r"Evidence"]
                    if not any(re.search(ctx, line, re.IGNORECASE) for ctx in allowed_contexts):
                        issue = SemanticIssue(
                            line=line_num,
                            column=1,
                            severity="CRITICAL",
                            issue_type="fictional_phase",
                            description="檢測到虛構的階段聲明（Era-1 未定義階段）",
                            context=line.strip(),
                            suggested_fix="移除階段聲明，使用 Era + Layer 描述狀態"
                        )
                        issues.append(issue)
        
        return issues
    
    def check_completeness_claims(self, lines: List[str]) -> List[SemanticIssue]:
        """檢查完整性聲明（未封存前禁止）"""
        issues = []
        
        completeness_patterns = [
            r"完整性[保証保证]",
            r"完全一致",
            r"完整閉環",
            r"100%",
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern in completeness_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issue = SemanticIssue(
                        line=line_num,
                        column=1,
                        severity="HIGH",
                        issue_type="completeness_claim",
                        description="檢測到完整性聲明（Era-1 未封存前禁止）",
                        context=line.strip(),
                        suggested_fix="改用準確的百分比或描述，避免絕對化語言"
                    )
                    issues.append(issue)
        
        return issues
    
    def check_era_state_consistency(self, lines: List[str]) -> List[SemanticIssue]:
        """檢查 Era 狀態一致性"""
        issues = []
        file_content = ''.join(lines)
        
        # 檢查 Era 聲明
        era_matches = re.findall(r"Era\s*[:：]\s*(\d+)", file_content, re.IGNORECASE)
        if era_matches:
            era_values = set(era_matches)
            if len(era_values) > 1:
                issue = SemanticIssue(
                    line=1,
                    column=1,
                    severity="HIGH",
                    issue_type="era_inconsistency",
                    description=f"Era 聲明不一致: {era_values}",
                    context="整個文件",
                    suggested_fix="統一 Era 聲明為 Era-1"
                )
                issues.append(issue)
            elif not era_values == {"1"}:
                issue = SemanticIssue(
                    line=1,
                    column=1,
                    severity="HIGH",
                    issue_type="era_mismatch",
                    description=f"Era 聲明錯誤: {era_values} (應為 Era-1)",
                    context="整個文件",
                    suggested_fix="修正 Era 聲明為 Era-1"
                )
                issues.append(issue)
        
        # 檢查 Semantic Closure
        if re.search(r"Semantic\s+Closure\s*[:：]\s*YES", file_content, re.IGNORECASE):
            issue = SemanticIssue(
                line=1,
                column=1,
                severity="CRITICAL",
                issue_type="semantic_closure_error",
                description="Semantic Closure 聲明錯誤 (Era-1 應為 NO)",
                context="整個文件",
                suggested_fix="修正 Semantic Closure 為 NO"
            )
            issues.append(issue)
        
        return issues
    
    def _suggest_fix(self, text: str, severity: str) -> str:
        """建議修復方案"""
        fixes = {
            "Phase": "使用 Era + Layer 描述系統狀態",
            "階段": "使用 Era + Layer 描述系統狀態",
            "完整性": "使用準確的百分比或部分完成描述",
            "封存": "移除或改用「候選狀態」",
            "最終": "改用「當前」或「最新」",
            "完成": "改用「進行中」或「部分完成」",
            "100%": "使用實際百分比或描述",
        }
        
        for key, fix in fixes.items():
            if key in text:
                return fix
        
        return "移除或改用符合 Era-1 的語言"
    
    def calculate_downgrade_percentage(self, issues: List[SemanticIssue]) -> float:
        """計算需要降階的百分比"""
        if not issues:
            return 0.0
        
        # 根據嚴重級別計算權重
        weights = {
            "CRITICAL": 1.0,
            "HIGH": 0.7,
            "MEDIUM": 0.4,
            "LOW": 0.1
        }
        
        total_weight = sum(weights.get(issue.severity, 0.1) for issue in issues)
        max_weight = 100  # 假設最多 100 個問題
        
        return min((total_weight / max_weight) * 100, 100.0)
    
    def generate_downgrade_report(self, issues: List[SemanticIssue], file_path: str) -> DowngradeReport:
        """生成降階報告"""
        report = DowngradeReport(file_path=file_path)
        
        for issue in issues:
            report.issues.append(issue)
            report.total_issues += 1
            
            if issue.severity == "CRITICAL":
                report.critical_issues += 1
            elif issue.severity == "HIGH":
                report.high_issues += 1
            elif issue.severity == "MEDIUM":
                report.medium_issues += 1
            elif issue.severity == "LOW":
                report.low_issues += 1
        
        report.downgrade_needed = report.critical_issues > 0 or report.high_issues > 0
        report.downgrade_percentage = self.calculate_downgrade_percentage(issues)
        
        return report
    
    def print_report(self, report: DowngradeReport):
        """打印報告"""
        print("\n" + "=" * 80)
        print("📉 報告降階驗證報告")
        print("Report Downgrade Validation Report")
        print("=" * 80)
        print(f"\n📁 文件: {report.file_path}")
        print(f"🎯 Era: {self.current_era} (Evidence-Native Bootstrap)")
        print(f"🏗️  Layer: {self.current_layer}")
        print(f"🔒 Semantic Closure: {self.current_semantic_closure}")
        
        print("\n" + "-" * 80)
        print("📊 問題統計")
        print("-" * 80)
        print(f"總問題數: {report.total_issues}")
        print(f"🔴 CRITICAL: {report.critical_issues}")
        print(f"🟠 HIGH: {report.high_issues}")
        print(f"🟡 MEDIUM: {report.medium_issues}")
        print(f"🟢 LOW: {report.low_issues}")
        
        print(f"\n需要降階: {'是' if report.downgrade_needed else '否'}")
        print(f"降階程度: {report.downgrade_percentage:.1f}%")
        
        if report.issues:
            print("\n" + "-" * 80)
            print("🚨 詳細問題列表")
            print("-" * 80)
            
            for i, issue in enumerate(report.issues, 1):
                severity_emoji = {
                    "CRITICAL": "🔴",
                    "HIGH": "🟠",
                    "MEDIUM": "🟡",
                    "LOW": "🟢"
                }.get(issue.severity, "⚪")
                
                print(f"\n{severity_emoji} 問題 #{i}")
                print(f"   位置: 第 {issue.line} 行")
                print(f"   嚴重級別: {issue.severity}")
                print(f"   類型: {issue.issue_type}")
                print(f"   描述: {issue.description}")
                print(f"   上下文: {issue.context}")
                print(f"   建議修復: {issue.suggested_fix}")
        
        print("\n" + "=" * 80)
        print("報告結束")
        print("=" * 80)
    
    def validate_report(self, file_path: str) -> DowngradeReport:
        """驗證報告"""
        lines = self.read_file(file_path)
        
        if not lines:
            return DowngradeReport(file_path=file_path, downgrade_needed=False)
        
        # 運行所有檢查
        all_issues = []
        
        all_issues.extend(self.check_forbidden_terminology(lines))
        all_issues.extend(self.check_allowed_patterns(lines))
        all_issues.extend(self.check_phase_declarations(lines))
        all_issues.extend(self.check_completeness_claims(lines))
        all_issues.extend(self.check_era_state_consistency(lines))
        
        # 生成報告
        report = self.generate_downgrade_report(all_issues, file_path)
        
        return report
    
    def generate_downgrade_plan(self, report: DowngradeReport) -> List[str]:
        """生成降階計劃"""
        plan = []
        
        if not report.downgrade_needed:
            plan.append("✅ 報告符合 Era-1 規範，無需降階")
            return plan
        
        plan.append("🔧 降階計劃:")
        plan.append("")
        
        # 按優先級排序
        priorities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        
        for severity in priorities:
            issues = [i for i in report.issues if i.severity == severity]
            if issues:
                plan.append(f"\n{severity} 優先級:")
                for issue in issues:
                    plan.append(f"  • 第 {issue.line} 行: {issue.suggested_fix}")
        
        return plan


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="報告降階驗證工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  # 驗證報告
  python report_downgrade_validator.py reports/my-report.md
  
  # 生成降階計劃
  python report_downgrade_validator.py reports/my-report.md --plan
  
  # JSON 格式輸出
  python report_downgrade_validator.py reports/my-report.md --json
        """
    )
    
    parser.add_argument(
        "report_file",
        type=str,
        help="要驗證的報告文件"
    )
    
    parser.add_argument(
        "--workspace",
        type=str,
        default="/workspace",
        help="工作空間路徑（默認: /workspace）"
    )
    
    parser.add_argument(
        "--plan",
        action="store_true",
        help="生成降階計劃"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式輸出"
    )
    
    args = parser.parse_args()
    
    # 創建驗證器
    validator = ReportDowngradeValidator(workspace=args.workspace)
    
    # 驗證報告
    report = validator.validate_report(args.report_file)
    
    # 輸出結果
    if args.json:
        # JSON 輸出
        output = {
            "file_path": report.file_path,
            "total_issues": report.total_issues,
            "critical_issues": report.critical_issues,
            "high_issues": report.high_issues,
            "medium_issues": report.medium_issues,
            "low_issues": report.low_issues,
            "downgrade_needed": report.downgrade_needed,
            "downgrade_percentage": report.downgrade_percentage,
            "issues": [
                {
                    "line": i.line,
                    "column": i.column,
                    "severity": i.severity,
                    "issue_type": i.issue_type,
                    "description": i.description,
                    "context": i.context,
                    "suggested_fix": i.suggested_fix
                }
                for i in report.issues
            ]
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        # 文本輸出
        validator.print_report(report)
        
        if args.plan:
            plan = validator.generate_downgrade_plan(report)
            print("\n" + "=" * 80)
            print("📋 降階計劃")
            print("=" * 80)
            print("\n".join(plan))
    
    # 退出碼
    sys.exit(1 if report.downgrade_needed else 0)


if __name__ == "__main__":
    main()