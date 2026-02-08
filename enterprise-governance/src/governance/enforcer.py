#!/usr/bin/env python3
"""
治理執行引擎 - Governance Enforcement Engine
Implements the 20 Forbidden Principles for Enterprise Governance
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from enum import Enum

from src.audit.logger import AuditLogger, log_audit


class Severity(Enum):
    """違規嚴重程度"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Category(Enum):
    """違規類別"""
    AI_CONTROL_BOUNDARY = "AI控制邊界"
    EVENT_HANDLING = "事件處理"
    SWITCHER = "切換器"
    GOVERNANCE_LAYER = "治理層"
    AUDIT_RECONSTRUCTION = "審計與重建"


@dataclass
class ForbiddenPrinciple:
    """禁令定義"""
    id: str
    name: str
    severity: Severity
    category: Category
    description: str
    detection_patterns: List[str]
    required_mitigations: List[str]
    code_patterns: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """轉換為字典"""
        return {
            "id": self.id,
            "name": self.name,
            "severity": self.severity.value,
            "category": self.category.value,
            "description": self.description,
            "detection_patterns": self.detection_patterns,
            "required_mitigations": self.required_mitigations,
            "code_patterns": self.code_patterns
        }


@dataclass
class Violation:
    """違規記錄"""
    principle_id: str
    principle_name: str
    severity: Severity
    category: Category
    detected_pattern: str
    file_path: str
    line_number: int
    code_snippet: str
    timestamp: str
    required_mitigations: List[str]
    
    def to_dict(self) -> Dict:
        """轉換為字典"""
        return {
            "principle_id": self.principle_id,
            "principle_name": self.principle_name,
            "severity": self.severity.value,
            "category": self.category.value,
            "detected_pattern": self.detected_pattern,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "code_snippet": self.code_snippet,
            "timestamp": self.timestamp,
            "required_mitigations": self.required_mitigations
        }


class PrincipleRegistry:
    """禁令註冊表 - 20 Forbidden Principles"""
    
    def __init__(self):
        self.principles: Dict[str, ForbiddenPrinciple] = {}
        self._register_principles()
    
    def _register_principles(self):
        """註冊所有20條禁令"""
        
        # ===== AI Control Boundary (5 principles) =====
        self.register(ForbiddenPrinciple(
            id="FP-001",
            name="AI直接觸發模式切換",
            severity=Severity.CRITICAL,
            category=Category.AI_CONTROL_BOUNDARY,
            description="AI 在 VM/容器/執行環境中直接觸發模式切換",
            detection_patterns=[
                "ai.trigger_mode_switch",
                "ai.switch_mode",
                "model_output → mode_change",
                "直接從推理循環觸發切換"
            ],
            required_mitigations=[
                "所有模式切換必須通過治理層事件閘門",
                "必須有獨立的切換器模組",
                "必須提供切換前狀態快照"
            ],
            code_patterns=[
                r"ai\.(trigger|switch|change).*mode",
                r"def.*mode.*switch.*ai.*:",
                r"\.switch.*\(.*ai.*output"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-002",
            name="語意觸發作為控制訊號",
            severity=Severity.CRITICAL,
            category=Category.AI_CONTROL_BOUNDARY,
            description="使用 AI 自然語言輸出作為控制訊號",
            detection_patterns=[
                "if '我認為' in output:",
                "if '危險' in text:",
                "if '錯誤' in message:",
                "semantic_trigger = True"
            ],
            required_mitigations=[
                "控制訊號必須轉換為結構化事件",
                "必須有明確的事件 schema",
                "必須有機器可驗證的簽章"
            ],
            code_patterns=[
                r"if\s+['&quot;].*[我認為危險錯誤].*['&quot;]\s+in\s+",
                r"semantic.*trigger\s*=",
                r"text.*match.*pattern.*trigger"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-003",
            name="AI作為最終決策來源",
            severity=Severity.HIGH,
            category=Category.AI_CONTROL_BOUNDARY,
            description="AI 輸出直接作為系統決策",
            detection_patterns=[
                "decision = ai_model.predict(input)",
                "直接執行 AI 生成的代碼",
                "缺乏決策審批步驟"
            ],
            required_mitigations=[
                "AI 輸出必須標記為 '建議' 而非 '決策'",
                "決策必須有獨立記錄點",
                "必須有決策覆蓋機制"
            ],
            code_patterns=[
                r"decision\s*=\s*ai.*predict",
                r"execute.*ai.*output",
                r"run.*ai.*generated.*code"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-004",
            name="AI修改自身控制參數",
            severity=Severity.CRITICAL,
            category=Category.AI_CONTROL_BOUNDARY,
            description="AI 修改自身的治理參數或控制邏輯",
            detection_patterns=[
                "ai.update_parameter('temperature', value)",
                "ai.modify_prompt_template(new_template)",
                "缺乏參數修改審計日誌"
            ],
            required_mitigations=[
                "控制參數必須有唯讀保護",
                "修改必須通過治理層審批",
                "必須有參數版本控制"
            ],
            code_patterns=[
                r"ai\.(update|modify|change).*parameter",
                r"set.*parameter.*ai",
                r"modify.*prompt.*template"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-005",
            name="AI繞過事件驗證",
            severity=Severity.HIGH,
            category=Category.AI_CONTROL_BOUNDARY,
            description="AI 繞過事件驗證直接執行操作",
            detection_patterns=[
                "ai.execute_without_verification(command)",
                "跳過事件隊列直接執行",
                "缺乏操作前驗證步驟"
            ],
            required_mitigations=[
                "所有操作必須有驗證事件",
                "必須有事件簽章驗證",
                "必須有操作前置檢查"
            ],
            code_patterns=[
                r"execute.*without.*verification",
                r"skip.*verify.*execute",
                r"bypass.*event.*queue"
            ]
        ))
        
        # ===== Event Handling (4 principles) =====
        self.register(ForbiddenPrinciple(
            id="FP-006",
            name="事件未經治理層驗證",
            severity=Severity.CRITICAL,
            category=Category.EVENT_HANDLING,
            description="事件直接進入切換器而未經治理層驗證",
            detection_patterns=[
                "event_queue → mode_switcher",
                "缺乏驗證中間層",
                "事件直接觸發操作"
            ],
            required_mitigations=[
                "所有事件必須經過治理層驗證",
                "必須有事件簽章",
                "必須有時序檢查",
                "必須有 DAG 檢查",
                "必須有衝突檢查"
            ],
            code_patterns=[
                r"event.*queue.*mode.*switcher",
                r"direct.*event.*trigger",
                r"skip.*governance.*layer"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-007",
            name="非確定性事件格式",
            severity=Severity.HIGH,
            category=Category.EVENT_HANDLING,
            description="使用非確定性事件格式（多行、自由輸出、無 schema）",
            detection_patterns=[
                "事件包含換行符",
                "事件為自由文本格式",
                "缺乏 schema 驗證"
            ],
            required_mitigations=[
                "事件必須是單行 JSON",
                "必須有嚴格 schema",
                "必須有 RFC3339 時間戳",
                "必須有事件哈希",
                "必須有重播令牌"
            ],
            code_patterns=[
                r"event.*\n.*\n",
                r"free.*text.*event",
                r"event.*without.*schema"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-008",
            name="事件無時間順序保證",
            severity=Severity.HIGH,
            category=Category.EVENT_HANDLING,
            description="事件處理無時間順序保證",
            detection_patterns=[
                "並行處理無序事件",
                "缺乏事件序列號",
                "時鐘不同步"
            ],
            required_mitigations=[
                "必須使用單調遞增序列號",
                "必須有事件時鐘同步",
                "必須有因果關係標記"
            ],
            code_patterns=[
                r"parallel.*unordered.*event",
                r"missing.*sequence.*number",
                r"clock.*unsynchronized"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-009",
            name="事件丟失無追蹤",
            severity=Severity.MEDIUM,
            category=Category.EVENT_HANDLING,
            description="事件丟失或丟棄無追蹤記錄",
            detection_patterns=[
                "事件緩存無持久化",
                "丟棄事件無日誌",
                "缺乏事件完整性驗證"
            ],
            required_mitigations=[
                "所有事件必須持久化",
                "丟棄事件必須有審計記錄",
                "必須有事件完整性檢查"
            ],
            code_patterns=[
                r"event.*cache.*no.*persist",
                r"drop.*event.*no.*log",
                r"event.*integrity.*check.*missing"
            ]
        ))
        
        # ===== Switcher (4 principles) =====
        self.register(ForbiddenPrinciple(
            id="FP-010",
            name="非確定性切換器",
            severity=Severity.CRITICAL,
            category=Category.SWITCHER,
            description="切換器依賴非確定性邏輯（AI、推論、語意）",
            detection_patterns=[
                "switch_logic = ai.infer(state)",
                "切換條件包含模糊邏輯",
                "缺乏狀態機明確定義"
            ],
            required_mitigations=[
                "切換器必須是確定性函數",
                "必須有完整狀態機定義",
                "必須可重播",
                "必須可審計"
            ],
            code_patterns=[
                r"switch.*logic.*ai.*infer",
                r"switch.*condition.*fuzzy",
                r"state.*machine.*undefined"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-011",
            name="切換無狀態快照",
            severity=Severity.HIGH,
            category=Category.SWITCHER,
            description="模式切換無前後狀態快照",
            detection_patterns=[
                "直接修改狀態變數",
                "缺乏狀態版本控制",
                "無法重建歷史狀態"
            ],
            required_mitigations=[
                "切換前必須保存狀態快照",
                "切換後必須記錄新狀態",
                "必須有狀態差異分析"
            ],
            code_patterns=[
                r"state.*variable.*direct.*modify",
                r"no.*state.*version",
                r"history.*state.*rebuild.*fail"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-012",
            name="切換無隔離邊界",
            severity=Severity.HIGH,
            category=Category.SWITCHER,
            description="模式切換影響無關系統組件",
            detection_patterns=[
                "全局狀態修改",
                "跨模組副作用",
                "缺乏隔離機制"
            ],
            required_mitigations=[
                "切換必須有作用域限制",
                "必須有影響分析",
                "必須有隔離機制"
            ],
            code_patterns=[
                r"global.*state.*modify",
                r"cross.*module.*side.*effect",
                r"isolation.*missing"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-013",
            name="切換無回滾機制",
            severity=Severity.HIGH,
            category=Category.SWITCHER,
            description="模式切換無回滾或恢復機制",
            detection_patterns=[
                "切換操作不可逆",
                "缺乏錯誤恢復路徑",
                "切換阻塞無超時"
            ],
            required_mitigations=[
                "必須有回滾計劃",
                "必須有健康檢查",
                "必須有超時機制"
            ],
            code_patterns=[
                r"switch.*irreversible",
                r"error.*recovery.*path.*missing",
                r"switch.*block.*no.*timeout"
            ]
        ))
        
        # ===== Governance Layer (4 principles) =====
        self.register(ForbiddenPrinciple(
            id="FP-014",
            name="治理層旁路",
            severity=Severity.CRITICAL,
            category=Category.GOVERNANCE_LAYER,
            description="存在繞過治理層的直接路徑",
            detection_patterns=[
                "直接 API 調用繞過治理",
                "緊急後門",
                "調試接口無保護"
            ],
            required_mitigations=[
                "所有控制路徑必須通過治理層",
                "必須有訪問控制",
                "必須有路徑審計"
            ],
            code_patterns=[
                r"direct.*api.*bypass.*governance",
                r"emergency.*backdoor",
                r"debug.*interface.*no.*protection"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-015",
            name="治理規則無版本控制",
            severity=Severity.MEDIUM,
            category=Category.GOVERNANCE_LAYER,
            description="治理規則無版本控制與變更追蹤",
            detection_patterns=[
                "規則直接修改無記錄",
                "缺乏規則版本",
                "規則變更無審批"
            ],
            required_mitigations=[
                "所有規則必須有版本",
                "必須有變更審計",
                "必須有規則測試"
            ],
            code_patterns=[
                r"rule.*direct.*modify.*no.*record",
                r"missing.*rule.*version",
                r"rule.*change.*no.*approval"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-016",
            name="治理決策無因果鏈",
            severity=Severity.HIGH,
            category=Category.GOVERNANCE_LAYER,
            description="治理決策無完整因果鏈追蹤",
            detection_patterns=[
                "決策為黑盒",
                "缺乏決策依據記錄",
                "無法重建決策過程"
            ],
            required_mitigations=[
                "決策必須有輸入輸出記錄",
                "必須有決策樹追蹤",
                "必須有影響分析"
            ],
            code_patterns=[
                r"decision.*blackbox",
                r"missing.*decision.*basis",
                r"rebuild.*decision.*process.*fail"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-017",
            name="治理層無健康監控",
            severity=Severity.MEDIUM,
            category=Category.GOVERNANCE_LAYER,
            description="治理層自身無健康監控與自我修復",
            detection_patterns=[
                "治理層無監控",
                "故障無告警",
                "缺乏備份機制"
            ],
            required_mitigations=[
                "必須有健康檢查",
                "必須有故障轉移",
                "必須有自我修復"
            ],
            code_patterns=[
                r"governance.*layer.*no.*monitor",
                r"failure.*no.*alert",
                r"backup.*mechanism.*missing"
            ]
        ))
        
        # ===== Audit & Reconstruction (3 principles) =====
        self.register(ForbiddenPrinciple(
            id="FP-018",
            name="操作無完整審計軌跡",
            severity=Severity.HIGH,
            category=Category.AUDIT_RECONSTRUCTION,
            description="系統操作無完整審計軌跡",
            detection_patterns=[
                "操作無日誌",
                "日誌可修改",
                "缺乏操作者信息"
            ],
            required_mitigations=[
                "所有操作必須有審計記錄",
                "必須有不可變日誌",
                "必須有操作者標識"
            ],
            code_patterns=[
                r"operation.*no.*log",
                r"log.*mutable",
                r"missing.*operator.*info"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-019",
            name="系統狀態不可重建",
            severity=Severity.CRITICAL,
            category=Category.AUDIT_RECONSTRUCTION,
            description="系統狀態無法從事件日誌完整重建",
            detection_patterns=[
                "狀態存儲在內存無持久化",
                "事件日誌不完整",
                "缺乏重建工具"
            ],
            required_mitigations=[
                "必須有事件溯源機制",
                "必須有狀態快照點",
                "必須有重建腳本"
            ],
            code_patterns=[
                r"state.*memory.*no.*persist",
                r"event.*log.*incomplete",
                r"rebuild.*tool.*missing"
            ]
        ))
        
        self.register(ForbiddenPrinciple(
            id="FP-020",
            name="無獨立驗證機制",
            severity=Severity.HIGH,
            category=Category.AUDIT_RECONSTRUCTION,
            description="系統無獨立於運行環境的驗證機制",
            detection_patterns=[
                "驗證依賴運行時狀態",
                "缺乏獨立驗證工具",
                "審計需要系統權限"
            ],
            required_mitigations=[
                "必須有離線驗證工具",
                "必須有第三方審計接口",
                "必須有驗證報告"
            ],
            code_patterns=[
                r"verify.*runtime.*state.*dependent",
                r"independent.*verify.*tool.*missing",
                r"audit.*require.*system.*privilege"
            ]
        ))
    
    def register(self, principle: ForbiddenPrinciple):
        """註冊禁令"""
        self.principles[principle.id] = principle
    
    def get_principle(self, principle_id: str) -> Optional[ForbiddenPrinciple]:
        """獲取禁令"""
        return self.principles.get(principle_id)
    
    def get_all_principles(self) -> List[ForbiddenPrinciple]:
        """獲取所有禁令"""
        return list(self.principles.values())
    
    def get_principles_by_severity(self, severity: Severity) -> List[ForbiddenPrinciple]:
        """按嚴重程度獲取禁令"""
        return [p for p in self.principles.values() if p.severity == severity]
    
    def get_principles_by_category(self, category: Category) -> List[ForbiddenPrinciple]:
        """按類別獲取禁令"""
        return [p for p in self.principles.values() if p.category == category]


class GovernanceEnforcer:
    """治理執行器"""
    
    def __init__(self, audit_logger: Optional[AuditLogger] = None):
        self.registry = PrincipleRegistry()
        self.audit_logger = audit_logger or log_audit
        self.violations: List[Violation] = []
    
    def check_file(self, file_path: str) -> List[Violation]:
        """檢查單個文件"""
        violations = []
        path = Path(file_path)
        
        if not path.exists():
            return violations
        
        try:
            content = path.read_text(encoding="utf-8")
            lines = content.split('\n')
            
            for principle in self.registry.get_all_principles():
                # 檢查代碼模式
                for pattern in principle.code_patterns:
                    for line_num, line in enumerate(lines, start=1):
                        try:
                            if re.search(pattern, line, re.IGNORECASE):
                                violation = Violation(
                                    principle_id=principle.id,
                                    principle_name=principle.name,
                                    severity=principle.severity,
                                    category=principle.category,
                                    detected_pattern=pattern,
                                    file_path=str(file_path),
                                    line_number=line_num,
                                    code_snippet=line.strip(),
                                    timestamp=datetime.utcnow().isoformat() + "Z",
                                    required_mitigations=principle.required_mitigations
                                )
                                violations.append(violation)
                                self.violations.append(violation)
                        except re.error:
                            continue
        
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return violations
    
    def check_directory(self, directory: str, patterns: List[str] = None) -> Dict[str, List[Violation]]:
        """檢查目錄中的所有文件"""
        if patterns is None:
            patterns = ['*.py', '*.js', '*.ts', '*.java', '*.go', '*.rs']
        
        violations_by_file = {}
        path = Path(directory)
        
        for pattern in patterns:
            for file_path in path.rglob(pattern):
                if file_path.is_file():
                    violations = self.check_file(str(file_path))
                    if violations:
                        violations_by_file[str(file_path)] = violations
        
        # 記錄審計
        log_audit(
            actor="system:governance-enforcer",
            action="check:codebase",
            resource=f"codebase://{directory}",
            result="success",
            metadata={
                "files_checked": len(violations_by_file),
                "total_violations": sum(len(v) for v in violations_by_file.values())
            }
        )
        
        return violations_by_file
    
    def generate_report(self) -> Dict:
        """生成違規報告"""
        total_violations = len(self.violations)
        
        severity_count = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
        
        category_count = {}
        
        for violation in self.violations:
            severity_count[violation.severity.value] += 1
            
            category = violation.category.value
            if category not in category_count:
                category_count[category] = 0
            category_count[category] += 1
        
        return {
            "report_id": f"fp_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_violations": total_violations,
            "by_severity": severity_count,
            "by_category": category_count,
            "violations_by_principle": self._count_by_principle(),
            "principles_registered": len(self.registry.principles)
        }
    
    def _count_by_principle(self) -> Dict[str, int]:
        """按禁令統計違規"""
        count = {}
        for violation in self.violations:
            pid = violation.principle_id
            if pid not in count:
                count[pid] = 0
            count[pid] += 1
        return count
    
    def clear_violations(self):
        """清除違規記錄"""
        self.violations.clear()


# 使用範例
if __name__ == "__main__":
    print("=== Governance Enforcement Engine Test ===\n")
    
    # 創建執行器
    enforcer = GovernanceEnforcer()
    
    # 測試：創建測試文件
    test_file = "test_governance.py"
    Path(test_file).write_text("""
# Test file with violations

# FP-001: AI directly triggers mode switch
def ai_callback(result):
    if result.risk > 0.8:
        ai.switch_mode("safe")  # VIOLATION!

# FP-002: Semantic trigger
output = model.generate("analyze")
if "危險" in output:  # VIOLATION!
    trigger_emergency()

# FP-003: AI as final decision
decision = ai.predict(input)  # VIOLATION!
execute(decision)
""", encoding="utf-8")
    
    # 檢查文件
    print(f"Checking file: {test_file}")
    violations = enforcer.check_file(test_file)
    
    # 輸出結果
    print(f"\nFound {len(violations)} violations:\n")
    for v in violations:
        print(f"[{v.severity.value}] {v.principle_name}")
        print(f"  Line {v.line_number}: {v.code_snippet}")
        print(f"  Pattern: {v.detected_pattern}")
        print()
    
    # 生成報告
    report = enforcer.generate_report()
    print("=== Report ===")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # 清理
    Path(test_file).unlink()