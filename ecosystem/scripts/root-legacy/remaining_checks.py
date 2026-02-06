
    def check_enforcers_completeness(self) -> EnforcementResult:
        """檢查強制執行器完整性"""
        violations = []
        
        enforcer_modules = [
            ("ecosystem/enforcers/closed_loop_governance.py", "ClosedLoopGovernance"),
            ("ecosystem/enforcers/pipeline_integration.py", "PipelineIntegration"),
            ("ecosystem/enforcers/role_executor.py", "RoleExecutor"),
            ("ecosystem/enforcers/semantic_violation_classifier.py", "SemanticViolationClassifier")
        ]
        
        for module_path, class_name in enforcer_modules:
            path = self.workspace / module_path
            if not path.exists():
                violations.append(Violation(
                    path=module_path,
                    line=0,
                    severity="MEDIUM",
                    message=f"Enforcer module not found: {module_path}"
                ))
                continue
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if f"class {class_name}" not in content:
                    violations.append(Violation(
                        path=module_path,
                        line=0,
                        severity="MEDIUM",
                        message=f"Class {class_name} not defined"
                    ))
                
                if "@GL-governed" not in content:
                    violations.append(Violation(
                        path=module_path,
                        line=1,
                        severity="LOW",
                        message=f"Missing @GL-governed annotation"
                    ))
            except Exception:
                pass
        
        return EnforcementResult(
            check_name="Enforcers Completeness",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Checked {len(enforcer_modules)} enforcer modules, found {len(violations)} issues"
        )
    
    def check_coordination_services(self) -> EnforcementResult:
        """檢查協調服務"""
        violations = []
        
        coordination_services = [
            ("ecosystem/coordination/api-gateway/src/gateway.py", "Gateway"),
            ("ecosystem/coordination/communication/src/event_dispatcher.py", "EventDispatcher"),
            ("ecosystem/coordination/communication/src/message_bus.py", "MessageBus"),
            ("ecosystem/coordination/data-synchronization/src/conflict_resolver.py", "ConflictResolver"),
            ("ecosystem/coordination/data-synchronization/src/sync_scheduler.py", "SyncScheduler"),
            ("ecosystem/coordination/service-discovery/src/service_registry.py", "ServiceRegistry")
        ]
        
        for module_path, class_name in coordination_services:
            path = self.workspace / module_path
            if not path.exists():
                violations.append(Violation(
                    path=module_path,
                    line=0,
                    severity="MEDIUM",
                    message=f"Coordination service not found: {module_path}"
                ))
                continue
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if f"class {class_name}" not in content:
                    violations.append(Violation(
                        path=module_path,
                        line=0,
                        severity="MEDIUM",
                        message=f"Class {class_name} not defined"
                    ))
            except Exception:
                pass
        
        return EnforcementResult(
            check_name="Coordination Services",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Checked {len(coordination_services)} coordination services, found {len(violations)} issues"
        )
    
    def check_meta_governance_systems(self) -> EnforcementResult:
        """檢查元治理系統"""
        violations = []
        
        meta_governance_modules = [
            ("ecosystem/governance/meta-governance/src/change_control_system.py", "ChangeControlSystem"),
            ("ecosystem/governance/meta-governance/src/dependency_manager.py", "DependencyManager"),
            ("ecosystem/governance/meta-governance/src/impact_analyzer.py", "ImpactAnalyzer"),
            ("ecosystem/governance/meta-governance/src/review_manager.py", "ReviewManager"),
            ("ecosystem/governance/meta-governance/src/sha_integrity_system.py", "SHAIntegritySystem"),
            ("ecosystem/governance/meta-governance/src/strict_version_enforcer.py", "StrictVersionEnforcer"),
            ("ecosystem/governance/meta-governance/src/version_manager.py", "VersionManager")
        ]
        
        for module_path, class_name in meta_governance_modules:
            path = self.workspace / module_path
            if not path.exists():
                violations.append(Violation(
                    path=module_path,
                    line=0,
                    severity="HIGH",
                    message=f"Meta-governance module not found: {module_path}"
                ))
                continue
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if f"class {class_name}" not in content:
                    violations.append(Violation(
                        path=module_path,
                        line=0,
                        severity="HIGH",
                        message=f"Class {class_name} not defined"
                    ))
                
                if "@GL-governed" not in content:
                    violations.append(Violation(
                        path=module_path,
                        line=1,
                        severity="LOW",
                        message=f"Missing @GL-governed annotation"
                    ))
            except Exception:
                pass
        
        return EnforcementResult(
            check_name="Meta-Governance Systems",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Checked {len(meta_governance_modules)} meta-governance modules, found {len(violations)} issues"
        )
    
    def check_reasoning_system(self) -> EnforcementResult:
        """檢查推理系統"""
        violations = []
        
        auto_reasoner_path = "ecosystem/reasoning/auto_reasoner.py"
        path = self.workspace / auto_reasoner_path
        
        if not path.exists():
            violations.append(Violation(
                path=auto_reasoner_path,
                line=0,
                severity="MEDIUM",
                message=f"Auto reasoner not found"
            ))
        else:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "class AutoReasoner" not in content:
                    violations.append(Violation(
                        path=auto_reasoner_path,
                        line=0,
                        severity="MEDIUM",
                        message=f"AutoReasoner class not defined"
                    ))
            except Exception:
                pass
        
        return EnforcementResult(
            check_name="Reasoning System",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Checked reasoning system, found {len(violations)} issues"
        )
    
    def check_validators_layer(self) -> EnforcementResult:
        """檢查驗證器層"""
        violations = []
        
        validators = [
            ("ecosystem/validators/network_validator.py", "NetworkValidator")
        ]
        
        for module_path, class_name in validators:
            path = self.workspace / module_path
            if not path.exists():
                violations.append(Violation(
                    path=module_path,
                    line=0,
                    severity="MEDIUM",
                    message=f"Validator not found: {module_path}"
                ))
                continue
            
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if f"class {class_name}" not in content:
                    violations.append(Violation(
                        path=module_path,
                        line=0,
                        severity="MEDIUM",
                        message=f"Class {class_name} not defined"
                    ))
            except Exception:
                pass
        
        return EnforcementResult(
            check_name="Validators Layer",
            passed=len(violations) == 0,
            violations=violations,
            message=f"Checked {len(validators)} validators, found {len(violations)} issues"
        )

