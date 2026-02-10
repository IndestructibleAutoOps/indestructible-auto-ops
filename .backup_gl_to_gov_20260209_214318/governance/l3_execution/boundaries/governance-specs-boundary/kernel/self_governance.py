"""
Self-Governance Mechanism
治理模組自我治理機制
GL Level: GL50 (Indestructible Kernel)

Purpose:
- 確保治理模組本身被治理
- 防止治理假象
- 提供治理模組的自我驗證能力

Key Features:
- 自我文檔檢查
- 自我測試檢查
- 自我證據封存檢查
- 自我執行追蹤檢查
- 可重播的自我驗證
"""

import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class SelfGovernanceCheck:
    """自我治理檢查結果"""
    check_type: str
    description: str
    status: str  # PASS, FAIL, WARN
    evidence: Dict[str, Any]
    timestamp: str

class SelfGovernanceChecker:
    """治理模組自我檢查器"""
    
    def __init__(self, module_name: str, module_path: Optional[Path] = None):
        self.module_name = module_name
        self.module_path = module_path or Path(f"governance/kernel/{module_name}.py")
        self.checks: List[SelfGovernanceCheck] = []
        self.start_time: Optional[float] = None
    
    def check_self(self) -> Dict[str, Any]:
        """對自己執行治理檢查"""
        
        print(f"\n{'='*70}")
        print(f"🔍 [{self.module_name}] 開始自我治理檢查...")
        print(f"{'='*70}\n")
        
        self.start_time = time.time()
        
        # 1. 檢查模組是否有文檔
        self._check_documentation()
        
        # 2. 檢查模組是否有測試
        self._check_tests()
        
        # 3. 檢查模組是否有證據封存
        self._check_evidence_sealing()
        
        # 4. 檢查模組執行是否有 trace
        self._check_execution_trace()
        
        # 5. 檢查模組是否符合命名規範
        self._check_naming_conventions()
        
        # 6. 檢查模組是否有治理合規性標記
        self._check_governance_compliance_markers()
        
        elapsed = time.time() - self.start_time
        
        # 生成自我治理報告
        report = self._generate_report(elapsed)
        
        # 封存報告
        self._seal_self_check_report(report)
        
        # 輸出摘要
        self._print_summary(report)
        
        return report
    
    def _check_documentation(self):
        """檢查文檔"""
        
        start = time.time()
        
        has_docstring = False
        has_module_docstring = False
        has_class_docstrings = False
        has_function_docstrings = False
        
        if self.module_path.exists():
            with open(self.module_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # 檢查模組 docstring
                lines = content.split('\n')
                if len(lines) > 1 and lines[0].strip().startswith('"""'):
                    has_module_docstring = True
                    has_docstring = True
                
                # 檢查 class docstrings
                if 'class ' in content:
                    for i, line in enumerate(lines):
                        if line.strip().startswith('class '):
                            # 檢查後幾行是否有 docstring
                            for j in range(i+1, min(i+5, len(lines))):
                                if '"""' in lines[j] or "'''" in lines[j]:
                                    has_class_docstrings = True
                                    break
                
                # 檢查 function docstrings
                if 'def ' in content:
                    for i, line in enumerate(lines):
                        if line.strip().startswith('def '):
                            # 檢查後幾行是否有 docstring
                            for j in range(i+1, min(i+3, len(lines))):
                                if '"""' in lines[j] or "'''" in lines[j]:
                                    has_function_docstrings = True
                                    break
        
        elapsed = (time.time() - start) * 1000
        
        status = "PASS"
        if not has_module_docstring:
            status = "FAIL"
        elif not has_class_docstrings or not has_function_docstrings:
            status = "WARN"
        
        self.checks.append(SelfGovernanceCheck(
            check_type="documentation",
            description="檢查模組文檔完整性",
            status=status,
            evidence={
                "module_docstring": has_module_docstring,
                "class_docstrings": has_class_docstrings,
                "function_docstrings": has_function_docstrings
            },
            timestamp=datetime.utcnow().isoformat() + 'Z'
        ))
        
        print(f"{'✅' if status == 'PASS' else '❌' if status == 'FAIL' else '⚠️'}  文檔檢查: {status}")
    
    def _check_tests(self):
        """檢查測試"""
        
        start = time.time()
        
        # 查找測試文件
        test_patterns = [
            Path(f"tests/kernel/{self.module_name}.py"),
            Path(f"tests/kernel/test_{self.module_name}.py"),
            Path(f"tests/{self.module_name}_test.py"),
        ]
        
        test_file_exists = any(p.exists() for p in test_patterns)
        
        # 檢查測試內容
        test_cases_count = 0
        for test_file in test_patterns:
            if test_file.exists():
                with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # 統計 test_ 開頭的函式
                    test_cases_count = content.count('def test_')
                break
        
        elapsed = (time.time() - start) * 1000
        
        status = "PASS"
        if not test_file_exists:
            status = "FAIL"
        elif test_cases_count == 0:
            status = "WARN"
        
        self.checks.append(SelfGovernanceCheck(
            check_type="tests",
            description="檢查模組測試覆蓋",
            status=status,
            evidence={
                "test_file_exists": test_file_exists,
                "test_cases_count": test_cases_count
            },
            timestamp=datetime.utcnow().isoformat() + 'Z'
        ))
        
        print(f"{'✅' if status == 'PASS' else '❌' if status == 'FAIL' else '⚠️'}  測試檢查: {status} ({test_cases_count} 個測試)")
    
    def _check_evidence_sealing(self):
        """檢查證據封存"""
        
        start = time.time()
        
        has_sealing_logic = False
        has_json_dump = False
        has_yaml_dump = False
        has_event_stream = False
        
        if self.module_path.exists():
            with open(self.module_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                has_sealing_logic = 'seal' in content.lower()
                has_json_dump = 'json.dump' in content
                has_yaml_dump = 'yaml.dump' in content
                has_event_stream = 'event_stream' in content.lower() or 'event-stream' in content.lower()
        
        elapsed = (time.time() - start) * 1000
        
        status = "PASS"
        if not has_sealing_logic:
            status = "FAIL"
        elif not (has_json_dump or has_yaml_dump or has_event_stream):
            status = "WARN"
        
        self.checks.append(SelfGovernanceCheck(
            check_type="evidence_sealing",
            description="檢查證據封存能力",
            status=status,
            evidence={
                "has_sealing_logic": has_sealing_logic,
                "has_json_dump": has_json_dump,
                "has_yaml_dump": has_yaml_dump,
                "has_event_stream": has_event_stream
            },
            timestamp=datetime.utcnow().isoformat() + 'Z'
        ))
        
        print(f"{'✅' if status == 'PASS' else '❌' if status == 'FAIL' else '⚠️'}  證據封存: {status}")
    
    def _check_execution_trace(self):
        """檢查執行追蹤"""
        
        start = time.time()
        
        has_logging = False
        has_trace_generation = False
        has_timestamp_logging = False
        
        if self.module_path.exists():
            with open(self.module_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                has_logging = 'logger' in content.lower() or 'print(' in content
                has_trace_generation = 'trace' in content.lower()
                has_timestamp_logging = 'datetime' in content or 'time.time()' in content
        
        elapsed = (time.time() - start) * 1000
        
        status = "PASS"
        if not has_logging:
            status = "WARN"
        if not has_timestamp_logging:
            status = "WARN"
        
        self.checks.append(SelfGovernanceCheck(
            check_type="execution_trace",
            description="檢查執行追蹤能力",
            status=status,
            evidence={
                "has_logging": has_logging,
                "has_trace_generation": has_trace_generation,
                "has_timestamp_logging": has_timestamp_logging
            },
            timestamp=datetime.utcnow().isoformat() + 'Z'
        ))
        
        print(f"{'✅' if status == 'PASS' else '⚠️'}  執行追蹤: {status}")
    
    def _check_naming_conventions(self):
        """檢查命名規範"""
        
        start = time.time()
        
        follows_snake_case = True
        follows_pep8 = True
        
        if self.module_path.exists():
            with open(self.module_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # 檢查是否有駝峰命名
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('class '):
                        # 類別應該是 PascalCase
                        class_name = line.split()[1].split('(')[0].split(':')[0]
                        if not class_name[0].isupper():
                            follows_pep8 = False
        
        elapsed = (time.time() - start) * 1000
        
        status = "PASS" if follows_pep8 else "WARN"
        
        self.checks.append(SelfGovernanceCheck(
            check_type="naming_conventions",
            description="檢查命名規範符合性",
            status=status,
            evidence={
                "follows_snake_case": follows_snake_case,
                "follows_pep8": follows_pep8
            },
            timestamp=datetime.utcnow().isoformat() + 'Z'
        ))
        
        print(f"{'✅' if status == 'PASS' else '⚠️'}  命名規範: {status}")
    
    def _check_governance_compliance_markers(self):
        """檢查治理合規性標記"""
        
        start = time.time()
        
        has_gl_level = False
        has_governance_marker = False
        has_unified_charter = False
        
        if self.module_path.exists():
            with open(self.module_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                has_gl_level = 'GL Level:' in content or 'gl_level' in content
                has_governance_marker = 'GL Unified Charter' in content or 'governance' in content.lower()
                has_unified_charter = 'Unified Charter' in content or 'charter_activated' in content
        
        elapsed = (time.time() - start) * 1000
        
        status = "PASS"
        if not has_gl_level:
            status = "WARN"
        if not has_governance_marker:
            status = "WARN"
        
        self.checks.append(SelfGovernanceCheck(
            check_type="governance_compliance_markers",
            description="檢查治理合規性標記",
            status=status,
            evidence={
                "has_gl_level": has_gl_level,
                "has_governance_marker": has_governance_marker,
                "has_unified_charter": has_unified_charter
            },
            timestamp=datetime.utcnow().isoformat() + 'Z'
        ))
        
        print(f"{'✅' if status == 'PASS' else '⚠️'}  治理標記: {status}")
    
    def _generate_report(self, elapsed: float) -> Dict[str, Any]:
        """生成自我治理報告"""
        
        total_checks = len(self.checks)
        passed = sum(1 for c in self.checks if c.status == "PASS")
        failed = sum(1 for c in self.checks if c.status == "FAIL")
        warnings = sum(1 for c in self.checks if c.status == "WARN")
        
        # 計算報告 hash
        report_data = [asdict(c) for c in self.checks]
        report_hash = hashlib.sha256(
            json.dumps(report_data, sort_keys=True).encode()
        ).hexdigest()
        
        return {
            "module": self.module_name,
            "module_path": str(self.module_path),
            "self_check_at": datetime.utcnow().isoformat() + 'Z',
            "checks": report_data,
            "total_checks": total_checks,
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "execution_time_ms": elapsed * 1000,
            "report_hash": report_hash
        }
    
    def _seal_self_check_report(self, report: Dict[str, Any]):
        """封存自我檢查報告"""
        
        report_dir = Path(".governance/self-checks")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        report_file = report_dir / f"{self.module_name}_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # 附加到 event stream
        event_stream = Path(".governance/event-stream.jsonl")
        
        # 獲取下一個 event ID
        next_event_id = 1
        if event_stream.exists():
            with open(event_stream, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if lines:
                last_event = json.loads(lines[-1])
                next_event_id = last_event.get("event_id", 0) + 1
        
        event = {
            "event_id": next_event_id,
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "event_type": "self_governance_check",
            "namespace": f"/governance/kernel/{self.module_name}/",
            "layer": "kernel",
            "platform": "all",
            "era": "Era-1",
            "payload": {
                "module": self.module_name,
                "total_checks": report["total_checks"],
                "passed": report["passed"],
                "failed": report["failed"],
                "warnings": report["warnings"],
                "report_hash": report["report_hash"],
                "report_file": str(report_file)
            }
        }
        
        with open(event_stream, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
    
    def _print_summary(self, report: Dict[str, Any]):
        """輸出摘要"""
        
        print(f"\n{'='*70}")
        print(f"📊 [{self.module_name}] 自我治理報告")
        print(f"{'='*70}")
        print(f"檢查時間: {report['self_check_at']}")
        print(f"總檢查數: {report['total_checks']}")
        print(f"通過: {report['passed']} ✅")
        print(f"失敗: {report['failed']} ❌")
        print(f"警告: {report['warnings']} ⚠️")
        print(f"執行時間: {report['execution_time_ms']:.2f}ms")
        print(f"報告 Hash: {report['report_hash']}")
        print(f"{'='*70}\n")

def check_governance_engine():
    """檢查治理引擎自身"""
    checker = SelfGovernanceChecker("enforce.rules", Path("ecosystem/enforce.rules.v2.py"))
    return checker.check_self()

if __name__ == "__main__":
    # 對治理引擎執行自我檢查
    check_governance_engine()