#!/usr/bin/env python3
"""
擴展 enforce.py 來綁定未綁定的模組
"""

from pathlib import Path
import re

def add_new_checks_to_enforce():
    """添加新的檢查方法到 enforce.py"""
    enforce_path = Path("/workspace/ecosystem/enforce.py")
    
    # 讀取現有 enforce.py
    with open(enforce_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 check_mnga_architecture 方法結束的位置
    # 在那裡添加新的檢查方法
    
    new_checks = '''
    def check_foundation_layer(self) -> EnforcementResult:
        """檢查基礎層組件"""
        violations = []
        
        foundation_modules = [
            "ecosystem/foundation/foundation_dag.py",
            "ecosystem/foundation/format/format_enforcer.py",
            "ecosystem/foundation/language/language_enforcer.py"
        ]
        
        for module_path in foundation_modules:
            path = self.workspace_path / module_path
            if not path.exists():
                violations.append(Violation(
                    path=module_path,
                    line=0,
                    severity="MEDIUM",
                    message=f"Foundation module not found: {module_path}"
                ))
                continue
            
            # 檢查模組是否有 GL 標記
            with open(path, 'r', encoding='utf-8') as f:
                module_content = f.read()
            
            if "@GL-governed" not in module_content:
                violations.append(Violation(
                    path=module_path,
                    line=1,
                    severity="LOW",
                    message=f"Foundation module missing @GL-governed annotation"
                ))
        
        return EnforcementResult(
            check_name="Foundation Layer",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Scanned {len(foundation_modules)} foundation modules, found {len(violations)} issues"
        )
    
    def check_coordination_layer(self) -> EnforcementResult:
        """檢查協調層組件"""
        violations = []
        
        coordination_paths = [
            "ecosystem/coordination/api-gateway",
            "ecosystem/coordination/communication",
            "ecosystem/coordination/data-synchronization",
            "ecosystem/coordination/service-discovery"
        ]
        
        for coord_path in coordination_paths:
            full_path = self.workspace_path / coord_path
            if not full_path.exists():
                violations.append(Violation(
                    path=coord_path,
                    line=0,
                    severity="MEDIUM",
                    message=f"Coordination component not found: {coord_path}"
                ))
                continue
            
            # 檢查是否至少有一個模組
            py_files = list(full_path.rglob("*.py"))
            if not py_files:
                violations.append(Violation(
                    path=coord_path,
                    line=0,
                    severity="LOW",
                    message=f"Coordination component has no Python files"
                ))
        
        return EnforcementResult(
            check_name="Coordination Layer",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Checked {len(coordination_paths)} coordination components, found {len(violations)} issues"
        )
    
    def check_governance_engines(self) -> EnforcementResult:
        """檢查治理引擎"""
        violations = []
        
        governance_engines = [
            ("ecosystem/governance/engines/validation/validation_engine.py", "ValidationEngine"),
            ("ecosystem/governance/engines/refresh/refresh_engine.py", "RefreshEngine"),
            ("ecosystem/governance/engines/reverse-architecture/reverse_architecture_engine.py", "ReverseArchitectureEngine"),
            ("ecosystem/governance/meta-governance/src/governance_framework.py", "GovernanceFramework")
        ]
        
        for module_path, class_name in governance_engines:
            path = self.workspace_path / module_path
            if not path.exists():
                violations.append(Violation(
                    path=module_path,
                    line=0,
                    severity="HIGH",
                    message=f"Governance engine not found: {module_path}"
                ))
                continue
            
            # 檢查類是否存在
            with open(path, 'r', encoding='utf-8') as f:
                module_content = f.read()
            
            if f"class {class_name}" not in module_content:
                violations.append(Violation(
                    path=module_path,
                    line=0,
                    severity="HIGH",
                    message=f"Class {class_name} not defined in {module_path}"
                ))
        
        return EnforcementResult(
            check_name="Governance Engines",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Checked {len(governance_engines)} governance engines, found {len(violations)} issues"
        )
    
    def check_tools_layer(self) -> EnforcementResult:
        """檢查工具層"""
        violations = []
        
        # 關鍵工具列表
        critical_tools = [
            "ecosystem/tools/scan_secrets.py",
            "ecosystem/tools/fix_security_issues.py",
            "ecosystem/tools/generate_governance_dashboard.py",
            "ecosystem/tools/fact-verification/gl_fact_pipeline.py"
        ]
        
        for tool_path in critical_tools:
            path = self.workspace_path / tool_path
            if not path.exists():
                violations.append(Violation(
                    path=tool_path,
                    line=0,
                    severity="MEDIUM",
                    message=f"Critical tool not found: {tool_path}"
                ))
        
        return EnforcementResult(
            check_name="Tools Layer",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Checked {len(critical_tools)} critical tools, found {len(violations)} issues"
        )
    
    def check_events_layer(self) -> EnforcementResult:
        """檢查事件處理層"""
        violations = []
        
        event_emitter_path = "ecosystem/events/event_emitter.py"
        path = self.workspace_path / event_emitter_path
        
        if not path.exists():
            violations.append(Violation(
                path=event_emitter_path,
                line=0,
                severity="HIGH",
                message=f"Event emitter not found: {event_emitter_path}"
            ))
        else:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "class EventEmitter" not in content:
                violations.append(Violation(
                    path=event_emitter_path,
                    line=0,
                    severity="HIGH",
                    message=f"EventEmitter class not defined"
                ))
        
        return EnforcementResult(
            check_name="Events Layer",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Checked event layer, found {len(violations)} issues"
        )
    
    def check_complete_naming_enforcer(self) -> EnforcementResult:
        """檢查完整命名強制執行器"""
        violations = []
        
        complete_naming_path = "ecosystem/enforcers/complete_naming_enforcer.py"
        path = self.workspace_path / complete_naming_path
        
        if not path.exists():
            violations.append(Violation(
                path=complete_naming_path,
                line=0,
                severity="HIGH",
                message=f"Complete naming enforcer not found"
            ))
        else:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 檢查是否有 16 種命名類型
            naming_types = [
                "CommentNaming", "MappingNaming", "ReferenceNaming", "PathNaming",
                "PortNaming", "ServiceNaming", "DependencyNaming", "ShortNaming",
                "LongNaming", "DirectoryNaming", "FileNaming", "EventNaming",
                "VariableNaming", "EnvironmentVariableNaming", "GitOpsNaming", "HelmReleaseNaming"
            ]
            
            for naming_type in naming_types:
                if naming_type not in content:
                    violations.append(Violation(
                        path=complete_naming_path,
                        line=0,
                        severity="MEDIUM",
                        message=f"Naming type {naming_type} not implemented"
                    ))
        
        return EnforcementResult(
            check_name="Complete Naming Enforcer",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Checked complete naming enforcer, found {len(violations)} issues"
        )
'''
    
    # 在 run_all_checks 方法中添加新的檢查調用
    # 找到 return self.check_mnga_architecture() 的位置
    old_return = "        return self.check_mnga_architecture()"
    new_return = f'''        return self.check_mnga_architecture()'''
    
    # 在 check_mnga_architecture 之後添加新方法
    # 找到方法定義的結束位置
    pattern = r'(    def check_mnga_architecture\(self\).*?return EnforcementResult\([^)]+\))'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # 在 check_mnga_architecture 方法之後添加新方法
        insert_pos = match.end()
        content = content[:insert_pos] + new_checks + content[insert_pos:]
        
        # 現在更新 run_all_checks 方法
        # 找到所有檢查調用的列表
        run_all_checks_pattern = r'(    def run_all_checks\(self\).*?def check_gl_compliance)'
        run_all_checks_match = re.search(run_all_checks_pattern, content, re.DOTALL)
        
        if run_all_checks_match:
            # 在現有檢查列表之後添加新的檢查
            old_checks_section = run_all_checks_match.group(0)
            new_checks_section = old_checks_section.replace(
                '''        return [
            self.check_gl_compliance(),
            self.check_naming_conventions(),
            self.check_security(),
            self.check_evidence_chain(),
            self.check_governance_enforcer(),
            self.check_self_auditor(),
            self.check_mnga_architecture(),
        ]
''',
                '''        return [
            self.check_gl_compliance(),
            self.check_naming_conventions(),
            self.check_security(),
            self.check_evidence_chain(),
            self.check_governance_enforcer(),
            self.check_self_auditor(),
            self.check_mnga_architecture(),
            self.check_foundation_layer(),
            self.check_coordination_layer(),
            self.check_governance_engines(),
            self.check_tools_layer(),
            self.check_events_layer(),
            self.check_complete_naming_enforcer(),
        ]
'''
            )
            content = content.replace(old_checks_section, new_checks_section)
        
        # 寫回文件
        with open(enforce_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully expanded enforce.py with new checks")
        print("   Added checks for:")
        print("   - Foundation Layer")
        print("   - Coordination Layer")
        print("   - Governance Engines")
        print("   - Tools Layer")
        print("   - Events Layer")
        print("   - Complete Naming Enforcer")
        print("\nTotal checks: 13 (was 7)")
    else:
        print("❌ Could not find check_mnga_architecture method")

if __name__ == "__main__":
    add_new_checks_to_enforce()