#!/usr/bin/env python3
from pathlib import Path

enforce_path = Path("/workspace/ecosystem/enforce.py")
content = enforce_path.read_text(encoding='utf-8')

# 新的檢查方法
new_methods = '''
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
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    module_content = f.read()
                
                if "@GL-governed" not in module_content:
                    violations.append(Violation(
                        path=module_path,
                        line=1,
                        severity="LOW",
                        message=f"Foundation module missing @GL-governed annotation"
                    ))
            except Exception:
                pass
        
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
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    module_content = f.read()
                
                if f"class {class_name}" not in module_content:
                    violations.append(Violation(
                        path=module_path,
                        line=0,
                        severity="HIGH",
                        message=f"Class {class_name} not defined in {module_path}"
                    ))
            except Exception:
                pass
        
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
            "ecosystem/tools/fact-verification/gov_fact_pipeline.py"
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
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                if "class EventEmitter" not in file_content:
                    violations.append(Violation(
                        path=event_emitter_path,
                        line=0,
                        severity="HIGH",
                        message=f"EventEmitter class not defined"
                    ))
            except Exception:
                pass
        
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
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                # 檢查是否有 16 種命名類型
                naming_types = [
                    "CommentNaming", "MappingNaming", "ReferenceNaming", "PathNaming",
                    "PortNaming", "ServiceNaming", "DependencyNaming", "ShortNaming",
                    "LongNaming", "DirectoryNaming", "FileNaming", "EventNaming",
                    "VariableNaming", "EnvironmentVariableNaming", "GitOpsNaming", "HelmReleaseNaming"
                ]
                
                for naming_type in naming_types:
                    if naming_type not in file_content:
                        violations.append(Violation(
                            path=complete_naming_path,
                            line=0,
                            severity="MEDIUM",
                            message=f"Naming type {naming_type} not implemented"
                        ))
            except Exception:
                pass
        
        return EnforcementResult(
            check_name="Complete Naming Enforcer",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Checked complete naming enforcer, found {len(violations)} issues"
        )

'''

# 在 # ============================================================================ 主程式 之前插入
insert_marker = "# ============================================================================\n# \u4e3b\u7a0b\u5e8f\n# ============================================================================"

if insert_marker in content:
    content = content.replace(insert_marker, new_methods + "\n" + insert_marker)
    
    # 更新 run_all_checks 方法
    old_checks = '''        return [
            self.check_gl_compliance(),
            self.check_naming_conventions(),
            self.check_security(),
            self.check_evidence_chain(),
            self.check_governance_enforcer(),
            self.check_self_auditor(),
            self.check_mnga_architecture(),
        ]'''
    
    new_checks = '''        return [
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
        ]'''
    
    content = content.replace(old_checks, new_checks)
    
    enforce_path.write_text(content, encoding='utf-8')
    print("✅ Successfully added 6 new checks to enforce.py")
else:
    print("❌ Could not find insertion marker")