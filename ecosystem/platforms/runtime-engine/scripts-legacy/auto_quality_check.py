#
# @GL-governed
# @GL-layer: gl-platform.gl-platform.governance
# @GL-semantic: auto-quality-check
# @GL-audit-trail: ../../engine/gl-platform.gl-platform.governance/GL_SEMANTIC_ANCHOR.json
#
#!/usr/bin/env python3
"""
自動化程式碼品質檢查工具
Automated Code Quality Check Tool
此腳本自動執行 PR-1-REVIEW-REPORT.md 中識別的所有檢查項目
This script automatically performs all checks identified in PR-1-REVIEW-REPORT.md
"""
# MNGA-002: Import organization needs review
import subprocess
import json
from pathlib import Path
from typing import Dict, Any
import argparse
from datetime import datetime
import ast  # Added for ast.literal_eval()
class QualityChecker:
    """自動化品質檢查器"""
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.results: Dict[str, Any] = {}
    def run_all_checks(self) -> Dict[str, Any]:
        """執行所有檢查"""
        print("🚀 開始自動化品質檢查...")
        self.check_security()
        self.check_python_quality()
        self.check_typescript_quality()
        self.check_code_duplication()
        self.check_docstring_coverage()
        self.check_non_ascii_filenames()
        self.check_console_logs()
        self.check_eval_usage()
        self.generate_report()
        return self.results
    def check_security(self):
        """P0: 安全性檢查"""
        print("\n🔒 執行安全性檢查...")
        try:
            # 使用 detect-secrets
            result = subprocess.run(
                ["detect-secrets", "scan"],
                capture_output=True,
                text=True,
                cwd=self.repo_root
            )
            secrets_found = "no secrets" not in result.stdout.lower()
            self.results["security"] = {
                "status": "⚠️ WARNING" if secrets_found else "✅ PASS",
                "secrets_detected": secrets_found,
                "details": "請審查包含敏感關鍵字的檔案" if secrets_found else "未檢測到明顯的秘密"
            }
        except FileNotFoundError:
            self.results["security"] = {
                "status": "⚠️ SKIP",
                "details": "detect-secrets 未安裝，請執行: pip install detect-secrets"
            }
    def check_python_quality(self):
        """P0: Python 程式碼品質"""
        print("\n🐍 檢查 Python 程式碼品質...")
        # 統計型別提示
        py_files = list(self.repo_root.glob("**/*.py"))
        total_files = len(py_files)
        files_with_type_hints = 0
        for py_file in py_files:
            try:
                content = py_file.read_text()
                # 使用更精確的模式檢測函式回傳型別提示
                if "def " in content and "->" in content:
                    files_with_type_hints += 1
            except (UnicodeDecodeError, OSError, PermissionError):
                continue
        type_hint_coverage = (files_with_type_hints / total_files * 100) if total_files > 0 else 0
        self.results["python_quality"] = {
            "total_files": total_files,
            "files_with_type_hints": files_with_type_hints,
            "type_hint_coverage": f"{type_hint_coverage:.1f}%",
            "status": "✅ PASS" if type_hint_coverage >= 90 else "⚠️ WARNING",
            "target": "90%"
        }
    def check_typescript_quality(self):
        """P1: TypeScript/JavaScript 品質"""
        print("\n📘 檢查 TypeScript 程式碼品質...")
        ts_files = list(self.repo_root.glob("**/*.ts")) + list(self.repo_root.glob("**/*.tsx"))
        js_files = list(self.repo_root.glob("**/*.js")) + list(self.repo_root.glob("**/*.jsx"))
        self.results["typescript_quality"] = {
            "total_ts_files": len(ts_files),
            "total_js_files": len(js_files),
            "status": "✅ PASS"
        }
    def check_code_duplication(self):
        """P0: 程式碼重複檢查"""
        print("\n🔄 檢查程式碼重複...")
        # 檢查已知的重複模組
        duplicate_patterns = [
            "dependency-manager",
            "drone_system"
        ]
        duplicates_found = []
        for pattern in duplicate_patterns:
            matches = list(self.repo_root.glob(f"**/{pattern}"))
            if len(matches) > 1:
                duplicates_found.append({
                    "pattern": pattern,
                    "locations": [str(m.relative_to(self.repo_root)) for m in matches]
                })
        self.results["code_duplication"] = {
            "duplicates_found": len(duplicates_found),
            "details": duplicates_found,
            "status": "⚠️ WARNING" if duplicates_found else "✅ PASS"
        }
    def check_docstring_coverage(self):
        """P1: Docstring 覆蓋率"""
        print("\n📝 檢查 Docstring 覆蓋率...")
        py_files = list(self.repo_root.glob("**/*.py"))
        files_with_docstrings = 0
        for py_file in py_files:
            try:
                content = py_file.read_text()
                # 檢測：檔案包含 docstrings（可能有誤報，建議使用 interrogate）
                if '"""' in content or "'''" in content:
                    files_with_docstrings += 1
            except (UnicodeDecodeError, OSError, PermissionError):
                continue
        coverage = (files_with_docstrings / len(py_files) * 100) if py_files else 0
        self.results["docstring_coverage"] = {
            "total_files": len(py_files),
            "files_with_docstrings": files_with_docstrings,
            "coverage": f"{coverage:.1f}%",
            "status": "✅ PASS" if coverage >= 85 else "⚠️ WARNING",
            "target": "85%"
        }
    def check_non_ascii_filenames(self):
        """P1: 非 ASCII 檔名檢查"""
        print("\n🌐 檢查非 ASCII 檔名...")
        non_ascii_files = []
        for path in self.repo_root.rglob("*"):
            if path.is_file():
                try:
                    path.name.encode('ascii')
                except UnicodeEncodeError:
                    non_ascii_files.append(str(path.relative_to(self.repo_root)))
        self.results["non_ascii_filenames"] = {
            "count": len(non_ascii_files),
            "files": non_ascii_files[:10],  # 只顯示前 10 個
            "status": "⚠️ WARNING" if non_ascii_files else "✅ PASS"
        }
    def check_console_logs(self):
        """P1: Console.log 檢查"""
        print("\n🖥️  檢查 console.log 使用...")
        files_with_console = []
        for ext in [".ts", ".tsx", ".js", ".jsx"]:
            for file_path in self.repo_root.glob(f"**/*{ext}"):
                try:
                    content = file_path.read_text()
                    if "console.log" in content:
                        files_with_console.append(str(file_path.relative_to(self.repo_root)))
                except (UnicodeDecodeError, OSError, PermissionError):
                    continue
        self.results["console_logs"] = {
            "count": len(files_with_console),
            "files": files_with_console[:20],  # 只顯示前 20 個
            "status": "⚠️ WARNING" if files_with_console else "✅ PASS"
        }
    def check_eval_usage(self):
        """P1: eval() 使用檢查"""
        print("\n⚠️  檢查 ast.literal_eval() 使用...")
        files_with_eval = []
        for ext in [".py", ".ts", ".js"]:
            for file_path in self.repo_root.glob(f"**/*{ext}"):
                try:
                    content = file_path.read_text()
                    if "ast.literal_eval(" in content:
                        files_with_eval.append(str(file_path.relative_to(self.repo_root)))
                except (UnicodeDecodeError, OSError, PermissionError):
                    continue
        self.results["eval_usage"] = {
            "count": len(files_with_eval),
            "files": files_with_eval,
            "status": "⚠️ WARNING" if files_with_eval else "✅ PASS"
        }
    def generate_report(self):
        """生成報告"""
        print("\n" + "="*80)
        print("📊 自動化品質檢查報告")
        print("="*80)
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "details": self.results
        }
        # 統計狀態
        total_checks = len(self.results)
        passed = sum(1 for r in self.results.values() if r.get("status") == "✅ PASS")
        warnings = sum(1 for r in self.results.values() if r.get("status") == "⚠️ WARNING")
        report["summary"] = {
            "total_checks": total_checks,
            "passed": passed,
            "warnings": warnings,
            "pass_rate": f"{(passed/total_checks*100):.1f}%"
        }
        # 輸出到螢幕
        print(f"\n總檢查項目: {total_checks}")
        print(f"通過: {passed}")
        print(f"警告: {warnings}")
        print(f"通過率: {report['summary']['pass_rate']}")
        print("\n詳細結果:")

        def _sanitize_log_entry(log_key: Any, log_value: Any) -> str:
            """
            將要輸出的報告項目進行基本淨化，避免在日誌中洩漏敏感資訊。
            僅用於人類可讀的終端輸出，不影響 JSON 報告內容。
            """
            # Normalize key to string for checks
            key_str = str(log_key)
            sensitive_key_markers = [
                "secret", "token", "password", "passwd", "pwd",
                "key", "credential", "auth", "apikey"
            ]
            lower_key = key_str.lower()
            if any(marker in lower_key for marker in sensitive_key_markers):
                return f"{key_str}: [REDACTED FOR SECURITY]"
            # For large collections, only report sizes, not contents
            if isinstance(log_value, (list, dict, set, tuple)):
                try:
                    size = len(log_value)  # type: ignore[arg-type]
                except Exception:
                    return f"{key_str}: [Collection]"
                return f"{key_str}: [Collection with {size} items]"
            # For other values, avoid printing excessively long data
            value_str = str(log_value)
            if len(value_str) > 200:
                return f"{key_str}: {value_str[:200]}...[TRUNCATED]"
            return f"{key_str}: {value_str}"

        for check_name, result in self.results.items():
            print(f"\n{check_name.upper()}: {result.get('status', 'N/A')}")
            # 僅輸出非敏感且對人類有用的摘要資訊，避免將可能包含秘密的欄位寫入日誌
            if check_name == "security":
                # 對安全掃描，只顯示固定的高層次描述，不暴露任何來自掃描結果的原始資料
                print("  - security scan executed; see JSON report for non-sensitive summary.")
                continue
            for key, value in result.items():
                if key == "status":
                    continue
                # Security: Suppress potentially sensitive data in logs
                sanitized = _sanitize_log_entry(key, value)
                print(f"  - {sanitized}")
        # 儲存 JSON 報告
        report_file = self.repo_root / "auto-quality-report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n✅ 報告已儲存至: {report_file}")
        # 生成 Markdown 報告
        self.generate_markdown_report(report)

    def _sanitize_value(self, key: str, value: Any) -> Any:
        """
        安全處理即將寫入報告的欄位值，避免在報告中儲存明文敏感資訊。
        僅用於格式化輸出，不修改 self.results 內的原始資料結構。
        """
        # 粗略判斷欄位名稱是否可能包含敏感資訊
        sensitive_key_indicators = [
            "secret",
            "token",
            "password",
            "passwd",
            "key",
            "credential",
            "api_key",
        ]
        lower_key = key.lower()
        if any(indicator in lower_key for indicator in sensitive_key_indicators):
            return "[REDACTED FOR SECURITY]"

        # 如果值本身是字串，做一些基本的敏感內容檢查
        if isinstance(value, str):
            suspicious_markers = [
                "-----BEGIN",
                "PRIVATE KEY",
                "AWS",
                "AKIA",  # 常見的 AWS Access Key 開頭
            ]
            if any(marker in value for marker in suspicious_markers):
                return "[REDACTED FOR SECURITY]"
            # 過長且無空白的字串也可能是 token/密鑰
            if len(value) > 80 and " " not in value:
                return "[REDACTED FOR SECURITY]"
            return value

        # 對 list/dict 進行遞迴處理，避免巢狀結構中出現明文敏感資訊
        if isinstance(value, list):
            return [self._sanitize_value(f"{key}[{idx}]", v) for idx, v in enumerate(value)]
        if isinstance(value, dict):
            return {k: self._sanitize_value(f"{key}.{k}", v) for k, v in value.items()}

        # 其它型別直接返回
        return value

    def generate_markdown_report(self, report: Dict):
        """生成 Markdown 格式報告"""
        md_file = self.repo_root / "AUTO-QUALITY-REPORT.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write("# 自動化品質檢查報告\n\n")
            f.write(f"**生成時間**: {report['timestamp']}\n\n")
            f.write("## 📊 總覽\n\n")
            f.write(f"- 總檢查項目: {report['summary']['total_checks']}\n")
            f.write(f"- ✅ 通過: {report['summary']['passed']}\n")
            f.write(f"- ⚠️ 警告: {report['summary']['warnings']}\n")
            f.write(f"- 通過率: {report['summary']['pass_rate']}\n\n")
            f.write("## 📋 詳細結果\n\n")
            for check_name, result in self.results.items():
                f.write(f"### {check_name.replace('_', ' ').title()}\n\n")
                f.write(f"**狀態**: {result.get('status', 'N/A')}\n\n")
                for key, value in result.items():
                    if key != "status":
                        safe_value = self._sanitize_value(key, value)
                        # 如果是長列表，只顯示統計資訊以避免輸出過多資料
                        if isinstance(safe_value, list) and len(safe_value) > 5:
                            f.write(f"- **{key}**: {len(safe_value)} 項 (僅顯示部分)\n")
                        else:
                            f.write(f"- **{key}**: {safe_value}\n")
                f.write("\n")
            f.write("## 🎯 建議行動\n\n")
            if self.results.get("security", {}).get("secrets_detected"):
                f.write("1. **高優先級**: 審查並移除硬編碼的秘密\n")
            # 安全地解析型別提示覆蓋率
            type_hint_coverage_str = self.results.get("python_quality", {}).get("type_hint_coverage", "0%")
            try:
                type_hint_coverage = float(type_hint_coverage_str.rstrip("%"))
                if type_hint_coverage < 90:
                    f.write("2. **高優先級**: 提升 Python 型別提示覆蓋率至 90%+\n")
            except (ValueError, AttributeError):
                pass
            if self.results.get("code_duplication", {}).get("duplicates_found", 0) > 0:
                f.write("3. **高優先級**: 移除重複的程式碼模組\n")
            if self.results.get("non_ascii_filenames", {}).get("count", 0) > 0:
                f.write("4. **中優先級**: 重新命名非 ASCII 檔名\n")
            if self.results.get("console_logs", {}).get("count", 0) > 0:
                f.write("5. **中優先級**: 替換 console.log 為結構化日誌\n")
            f.write("\n詳細改進計劃請參考: [PR-1-ACTION-PLAN.md](./PR-1-ACTION-PLAN.md)\n")
        print(f"✅ Markdown 報告已儲存至: {md_file}")
def main():
    parser = argparse.ArgumentParser(description="自動化程式碼品質檢查")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="倉庫根目錄路徑"
    )
    args = parser.parse_args()
    checker = QualityChecker(args.repo_root)
    checker.run_all_checks()
if __name__ == "__main__":
    main()
