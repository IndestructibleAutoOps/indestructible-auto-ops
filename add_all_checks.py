#!/usr/bin/env python3
"""
一次性添加所有新檢查到 enforce.py
"""

from pathlib import Path

def main():
    enforce_path = Path("/workspace/ecosystem/enforce.py")
    content = enforce_path.read_text(encoding='utf-8')
    
    # 新檢查方法
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
            path = self.workspace / module_path
            if not path.exists():
                violations.append(Violation(path=module_path, line=0, severity="MEDIUM", message=f"Foundation module not found: {module_path}"))
                continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    if "@GL-governed" not in f.read():
                        violations.append(Violation(path=module_path, line=1, severity="LOW", message="Missing @GL-governed annotation"))
            except: pass
        return EnforcementResult(check_name="Foundation Layer", passed=len(violations)==0, violations=violations, message=f"Scanned {len(foundation_modules)} foundation modules, found {len(violations)} issues")
    
    def check_coordination_layer(self) -> EnforcementResult:
        """檢查協調層組件"""
        violations = []
        for coord_path in ["ecosystem/coordination/api-gateway", "ecosystem/coordination/communication", "ecosystem/coordination/data-synchronization", "ecosystem/coordination/service-discovery"]:
            if not (self.workspace / coord_path).exists():
                violations.append(Violation(path=coord_path, line=0, severity="MEDIUM", message=f"Coordination component not found: {coord_path}"))
        return EnforcementResult(check_name="Coordination Layer", passed=len(violations)==0, violations=violations, message=f"Checked 4 coordination components, found {len(violations)} issues")
    
    def check_governance_engines(self) -> EnforcementResult:
        """檢查治理引擎"""
        violations = []
        for module_path, class_name in [("ecosystem/governance/engines/validation/validation_engine.py", "ValidationEngine"), ("ecosystem/governance/engines/refresh/refresh_engine.py", "RefreshEngine"), ("ecosystem/governance/engines/reverse-architecture/reverse_architecture_engine.py", "ReverseArchitectureEngine"), ("ecosystem/governance/meta-governance/src/governance_framework.py", "GovernanceFramework")]:
            path = self.workspace / module_path
            if not path.exists():
                violations.append(Violation(path=module_path, line=0, severity="HIGH", message=f"Governance engine not found: {module_path}"))
            else:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        if f"class {class_name}" not in f.read():
                            violations.append(Violation(path=module_path, line=0, severity="HIGH", message=f"Class {class_name} not defined"))
                except: pass
        return EnforcementResult(check_name="Governance Engines", passed=len(violations)==0, violations=violations, message=f"Checked 4 governance engines, found {len(violations)} issues")
    
    def check_tools_layer(self) -> EnforcementResult:
        """檢查工具層"""
        violations = []
        for tool_path in ["ecosystem/tools/scan_secrets.py", "ecosystem/tools/fix_security_issues.py", "ecosystem/tools/generate_governance_dashboard.py", "ecosystem/tools/fact-verification/gl_fact_pipeline.py"]:
            if not (self.workspace / tool_path).exists():
                violations.append(Violation(path=tool_path, line=0, severity="MEDIUM", message=f"Critical tool not found: {tool_path}"))
        return EnforcementResult(check_name="Tools Layer", passed=len(violations)==0, violations=violations, message=f"Checked 4 critical tools, found {len(violations)} issues")
    
    def check_events_layer(self) -> EnforcementResult:
        """檢查事件處理層"""
        violations = []
        path = self.workspace / "ecosystem/events/event_emitter.py"
        if not path.exists():
            violations.append(Violation(path="ecosystem/events/event_emitter.py", line=0, severity="HIGH", message="Event emitter not found"))
        else:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    if "class EventEmitter" not in f.read():
                        violations.append(Violation(path="ecosystem/events/event_emitter.py", line=0, severity="HIGH", message="EventEmitter class not defined"))
            except: pass
        return EnforcementResult(check_name="Events Layer", passed=len(violations)==0, violations=violations, message=f"Checked event layer, found {len(violations)} issues")
    
    def check_complete_naming_enforcer(self) -> EnforcementResult:
        """檢查完整命名強制執行器"""
        violations = []
        path = self.workspace / "ecosystem/enforcers/complete_naming_enforcer.py"
        if not path.exists():
            violations.append(Violation(path="ecosystem/enforcers/complete_naming_enforcer.py", line=0, severity="HIGH", message="Complete naming enforcer not found"))
        else:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for naming_type in ["CommentNaming", "MappingNaming", "ReferenceNaming", "PathNaming", "PortNaming", "ServiceNaming", "DependencyNaming", "ShortNaming", "LongNaming", "DirectoryNaming", "FileNaming", "EventNaming", "VariableNaming", "EnvironmentVariableNaming", "GitOpsNaming", "HelmReleaseNaming"]:
                        if naming_type not in content:
                            violations.append(Violation(path="ecosystem/enforcers/complete_naming_enforcer.py", line=0, severity="MEDIUM", message=f"Naming type {naming_type} not implemented"))
            except: pass
        return EnforcementResult(check_name="Complete Naming Enforcer", passed=len(violations)==0, violations=violations, message=f"Checked complete naming enforcer, found {len(violations)} issues")
    
    def check_enforcers_completeness(self) -> EnforcementResult:
        """檢查強制執行器完整性"""
        violations = []
        for module_path, class_name in [("ecosystem/enforcers/closed_loop_governance.py", "ClosedLoopGovernance"), ("ecosystem/enforcers/pipeline_integration.py", "PipelineIntegration"), ("ecosystem/enforcers/role_executor.py", "RoleExecutor"), ("ecosystem/enforcers/semantic_violation_classifier.py", "SemanticViolationClassifier")]:
            path = self.workspace / module_path
            if not path.exists():
                violations.append(Violation(path=module_path, line=0, severity="MEDIUM", message=f"Enforcer module not found: {module_path}"))
            else:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if f"class {class_name}" not in content:
                            violations.append(Violation(path=module_path, line=0, severity="MEDIUM", message=f"Class {class_name} not defined"))
                        if "@GL-governed" not in content:
                            violations.append(Violation(path=module_path, line=1, severity="LOW", message="Missing @GL-governed annotation"))
                except: pass
        return EnforcementResult(check_name="Enforcers Completeness", passed=len(violations)==0, violations=violations, message=f"Checked 4 enforcer modules, found {len(violations)} issues")
    
    def check_coordination_services(self) -> EnforcementResult:
        """檢查協調服務"""
        violations = []
        for module_path, class_name in [("ecosystem/coordination/api-gateway/src/gateway.py", "Gateway"), ("ecosystem/coordination/communication/src/event_dispatcher.py", "EventDispatcher"), ("ecosystem/coordination/communication/src/message_bus.py", "MessageBus"), ("ecosystem/coordination/data-synchronization/src/conflict_resolver.py", "ConflictResolver"), ("ecosystem/coordination/data-synchronization/src/sync_scheduler.py", "SyncScheduler"), ("ecosystem/coordination/service-discovery/src/service_registry.py", "ServiceRegistry")]:
            path = self.workspace / module_path
            if not path.exists():
                violations.append(Violation(path=module_path, line=0, severity="MEDIUM", message=f"Coordination service not found: {module_path}"))
            else:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        if f"class {class_name}" not in f.read():
                            violations.append(Violation(path=module_path, line=0, severity="MEDIUM", message=f"Class {class_name} not defined"))
                except: pass
        return EnforcementResult(check_name="Coordination Services", passed=len(violations)==0, violations=violations, message=f"Checked 6 coordination services, found {len(violations)} issues")
    
    def check_meta_governance_systems(self) -> EnforcementResult:
        """檢查元治理系統"""
        violations = []
        for module_path, class_name in [("ecosystem/governance/meta-governance/src/change_control_system.py", "ChangeControlSystem"), ("ecosystem/governance/meta-governance/src/dependency_manager.py", "DependencyManager"), ("ecosystem/governance/meta-governance/src/impact_analyzer.py", "ImpactAnalyzer"), ("ecosystem/governance/meta-governance/src/review_manager.py", "ReviewManager"), ("ecosystem/governance/meta-governance/src/sha_integrity_system.py", "SHAIntegritySystem"), ("ecosystem/governance/meta-governance/src/strict_version_enforcer.py", "StrictVersionEnforcer"), ("ecosystem/governance/meta-governance/src/version_manager.py", "VersionManager")]:
            path = self.workspace / module_path
            if not path.exists():
                violations.append(Violation(path=module_path, line=0, severity="HIGH", message=f"Meta-governance module not found: {module_path}"))
            else:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if f"class {class_name}" not in content:
                            violations.append(Violation(path=module_path, line=0, severity="HIGH", message=f"Class {class_name} not defined"))
                        if "@GL-governed" not in content:
                            violations.append(Violation(path=module_path, line=1, severity="LOW", message="Missing @GL-governed annotation"))
                except: pass
        return EnforcementResult(check_name="Meta-Governance Systems", passed=len(violations)==0, violations=violations, message=f"Checked 7 meta-governance modules, found {len(violations)} issues")
    
    def check_reasoning_system(self) -> EnforcementResult:
        """檢查推理系統"""
        violations = []
        path = self.workspace / "ecosystem/reasoning/auto_reasoner.py"
        if not path.exists():
            violations.append(Violation(path="ecosystem/reasoning/auto_reasoner.py", line=0, severity="MEDIUM", message="Auto reasoner not found"))
        else:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    if "class AutoReasoner" not in f.read():
                        violations.append(Violation(path="ecosystem/reasoning/auto_reasoner.py", line=0, severity="MEDIUM", message="AutoReasoner class not defined"))
            except: pass
        return EnforcementResult(check_name="Reasoning System", passed=len(violations)==0, violations=violations, message=f"Checked reasoning system, found {len(violations)} issues")
    
    def check_validators_layer(self) -> EnforcementResult:
        """檢查驗證器層"""
        violations = []
        path = self.workspace / "ecosystem/validators/network_validator.py"
        if not path.exists():
            violations.append(Violation(path="ecosystem/validators/network_validator.py", line=0, severity="MEDIUM", message="Validator not found"))
        else:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    if "class NetworkValidator" not in f.read():
                        violations.append(Violation(path="ecosystem/validators/network_validator.py", line=0, severity="MEDIUM", message="NetworkValidator class not defined"))
            except: pass
        return EnforcementResult(check_name="Validators Layer", passed=len(violations)==0, violations=violations, message=f"Checked validators, found {len(violations)} issues")

'''
    
    # 在 check_mnga_architecture 方法結束後插入
    marker = "        return EnforcementResult(\n            check_name=&quot;MNGA Architecture&quot;,"
    if marker in content:
        # 找到這個方法的完整結束位置
        idx = content.find(marker)
        # 找到這個 EnforcementResult 的結束括號
        end_idx = content.find(")\n\n# ============================================================================", idx)
        if end_idx != -1:
            insert_pos = end_idx + 1
            content = content[:insert_pos] + new_methods + content[insert_pos:]
            
            # 更新 run_all_checks
            old_line = "        results.append(self.check_mnga_architecture())"
            new_lines = """        results.append(self.check_mnga_architecture())
        results.append(self.check_foundation_layer())
        results.append(self.check_coordination_layer())
        results.append(self.check_governance_engines())
        results.append(self.check_tools_layer())
        results.append(self.check_events_layer())
        results.append(self.check_complete_naming_enforcer())
        results.append(self.check_enforcers_completeness())
        results.append(self.check_coordination_services())
        results.append(self.check_meta_governance_systems())
        results.append(self.check_reasoning_system())
        results.append(self.check_validators_layer())"""
            
            content = content.replace(old_line, new_lines)
            
            enforce_path.write_text(content, encoding='utf-8')
            print("✅ Successfully added 11 new checks")
            print("   Total: 18 checks (was 7)")
            return
    
    print("❌ Could not find insertion marker")

if __name__ == "__main__":
    main()