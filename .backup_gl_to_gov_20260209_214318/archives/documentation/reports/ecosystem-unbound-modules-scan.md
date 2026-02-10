================================================================================
Ecosystem Unbound Modules Scan Report
================================================================================

## 📊 Summary
Total modules scanned: 83
Modules bound to enforce.py: 13
Modules NOT bound to enforce.py: 70
Unbound modules with main class: 31

## 📈 Statistics by Module Type

Type                    Total    Bound  Unbound   Coverage
------------------------------------------------------------
coordination               18        0       18       0.0%
enforcers                   9        2        7      22.2%
events                      1        0        1       0.0%
foundation                  3        0        3       0.0%
governance                 20        0       20       0.0%
reasoning                  12       11        1      91.7%
tools                      19        0       19       0.0%
validators                  1        0        1       0.0%

## 🚨 High Priority Unbound Modules (with main class)

- [COORDINATION] ecosystem/coordination/data-synchronization/src/sync_engine.py
  Suggested check: check_coordination_layer
  Description: 協調層組件

- [ENFORCERS] ecosystem/enforcers/naming_enforcer.py
  Suggested check: check_governance_enforcer
  Description: 治理強制執行器

- [ENFORCERS] ecosystem/enforcers/complete_naming_enforcer.py
  Suggested check: check_governance_enforcer
  Description: 治理強制執行器

- [EVENTS] ecosystem/events/event_emitter.py
  Suggested check: check_events_layer
  Description: 事件處理

- [FOUNDATION] ecosystem/foundation/foundation_dag.py
  Suggested check: check_foundation_layer
  Description: 基礎層組件

- [FOUNDATION] ecosystem/foundation/format/format_enforcer.py
  Suggested check: check_foundation_layer
  Description: 基礎層組件

- [FOUNDATION] ecosystem/foundation/language/language_enforcer.py
  Suggested check: check_foundation_layer
  Description: 基礎層組件

- [GOVERNANCE] ecosystem/governance/meta-governance/tools/apply_governance.py
  Suggested check: check_governance_layer
  Description: 治理引擎和工具

- [GOVERNANCE] ecosystem/governance/meta-governance/src/governance_framework.py
  Suggested check: check_governance_layer
  Description: 治理引擎和工具

- [GOVERNANCE] ecosystem/governance/engines/validation/validation_engine.py
  Suggested check: check_governance_layer
  Description: 治理引擎和工具

- [GOVERNANCE] ecosystem/governance/engines/refresh/refresh_engine.py
  Suggested check: check_governance_layer
  Description: 治理引擎和工具

- [GOVERNANCE] ecosystem/governance/engines/reverse-architecture/reverse_architecture_engine.py
  Suggested check: check_governance_layer
  Description: 治理引擎和工具

- [TOOLS] ecosystem/tools/audit_trail_report.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/code_scanning_analysis.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/scan_secrets.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/fix_security_issues.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/audit_trail_query.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/fix_code_scanning_issues.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/generate_governance_dashboard.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/gov-markers/fix_governance_markers.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/gov-markers/add_gl_markers.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/gov-markers/add_gl_markers_batch.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/gov-markers/add_gl_markers_json.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/gov-markers/add_gl_markers_yaml.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/registry/data_catalog_manager.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/registry/platform_registry_manager.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/registry/service_registry_manager.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/registry/test_registry_tools.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/audit/gov_audit_simple.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [TOOLS] ecosystem/tools/fact-verification/gov_fact_pipeline.py
  Suggested check: check_tools_layer
  Description: 工具腳本

- [VALIDATORS] ecosystem/validators/network_validator.py
  Suggested check: check_validators_layer
  Description: 驗證器

## 📋 All Unbound Modules

⚪ [COORDINATION] ecosystem/coordination/api-gateway/src/authenticator.py
⚪ [COORDINATION] ecosystem/coordination/api-gateway/src/gateway.py
⚪ [COORDINATION] ecosystem/coordination/api-gateway/src/rate_limiter.py
⚪ [COORDINATION] ecosystem/coordination/api-gateway/src/router.py
⚪ [COORDINATION] ecosystem/coordination/api-gateway/tests/test_api_gateway.py
⚪ [COORDINATION] ecosystem/coordination/communication/src/event_dispatcher.py
⚪ [COORDINATION] ecosystem/coordination/communication/src/message_bus.py
⚪ [COORDINATION] ecosystem/coordination/communication/tests/test_communication.py
⚪ [COORDINATION] ecosystem/coordination/data-synchronization/src/conflict_resolver.py
⚪ [COORDINATION] ecosystem/coordination/data-synchronization/src/connectors/base_connector.py
⚪ [COORDINATION] ecosystem/coordination/data-synchronization/src/connectors/filesystem_connector.py
🔴 [COORDINATION] ecosystem/coordination/data-synchronization/src/sync_engine.py
⚪ [COORDINATION] ecosystem/coordination/data-synchronization/src/sync_scheduler.py
⚪ [COORDINATION] ecosystem/coordination/data-synchronization/tests/test_data_sync.py
⚪ [COORDINATION] ecosystem/coordination/service-discovery/src/service_agent.py
⚪ [COORDINATION] ecosystem/coordination/service-discovery/src/service_client.py
⚪ [COORDINATION] ecosystem/coordination/service-discovery/src/service_registry.py
⚪ [COORDINATION] ecosystem/coordination/service-discovery/tests/test_service_discovery.py
⚪ [ENFORCERS] ecosystem/enforcers/closed_loop_governance.py
🔴 [ENFORCERS] ecosystem/enforcers/complete_naming_enforcer.py
🔴 [ENFORCERS] ecosystem/enforcers/naming_enforcer.py
⚪ [ENFORCERS] ecosystem/enforcers/pipeline_integration.py
⚪ [ENFORCERS] ecosystem/enforcers/role_executor.py
⚪ [ENFORCERS] ecosystem/enforcers/semantic_violation_classifier.py
⚪ [ENFORCERS] ecosystem/enforcers/test_complete_system.py
🔴 [EVENTS] ecosystem/events/event_emitter.py
🔴 [FOUNDATION] ecosystem/foundation/format/format_enforcer.py
🔴 [FOUNDATION] ecosystem/foundation/foundation_dag.py
🔴 [FOUNDATION] ecosystem/foundation/language/language_enforcer.py
⚪ [GOVERNANCE] ecosystem/governance/audit_logger.py
🔴 [GOVERNANCE] ecosystem/governance/engines/refresh/refresh_engine.py
🔴 [GOVERNANCE] ecosystem/governance/engines/reverse-architecture/reverse_architecture_engine.py
🔴 [GOVERNANCE] ecosystem/governance/engines/validation/validation_engine.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/src/change_control_system.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/src/change_manager.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/src/dependency_manager.py
🔴 [GOVERNANCE] ecosystem/governance/meta-governance/src/governance_framework.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/src/impact_analyzer.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/src/review_manager.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/src/sha_integrity_system.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/src/strict_version_enforcer.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/src/version_manager.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/tests/test_change_control.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/tests/test_meta_governance.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/tests/test_sha_integrity.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/tests/test_strict_version_management.py
🔴 [GOVERNANCE] ecosystem/governance/meta-governance/tools/apply_governance.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/tools/apply_strict_versioning.py
⚪ [GOVERNANCE] ecosystem/governance/meta-governance/tools/full_governance_integration.py
⚪ [REASONING] ecosystem/reasoning/auto_reasoner.py
⚪ [TOOLS] ecosystem/tools/analyze_semantic_gaps.py
🔴 [TOOLS] ecosystem/tools/audit/gov_audit_simple.py
🔴 [TOOLS] ecosystem/tools/audit_trail_query.py
🔴 [TOOLS] ecosystem/tools/audit_trail_report.py
🔴 [TOOLS] ecosystem/tools/code_scanning_analysis.py
🔴 [TOOLS] ecosystem/tools/fact-verification/gov_fact_pipeline.py
🔴 [TOOLS] ecosystem/tools/fix_code_scanning_issues.py
🔴 [TOOLS] ecosystem/tools/fix_security_issues.py
🔴 [TOOLS] ecosystem/tools/generate_governance_dashboard.py
🔴 [TOOLS] ecosystem/tools/gov-markers/add_gl_markers.py
🔴 [TOOLS] ecosystem/tools/gov-markers/add_gl_markers_batch.py
🔴 [TOOLS] ecosystem/tools/gov-markers/add_gl_markers_json.py
🔴 [TOOLS] ecosystem/tools/gov-markers/add_gl_markers_yaml.py
🔴 [TOOLS] ecosystem/tools/gov-markers/fix_governance_markers.py
🔴 [TOOLS] ecosystem/tools/registry/data_catalog_manager.py
🔴 [TOOLS] ecosystem/tools/registry/platform_registry_manager.py
🔴 [TOOLS] ecosystem/tools/registry/service_registry_manager.py
🔴 [TOOLS] ecosystem/tools/registry/test_registry_tools.py
🔴 [TOOLS] ecosystem/tools/scan_secrets.py
🔴 [VALIDATORS] ecosystem/validators/network_validator.py

## 💡 Recommendations

1. **Priority 1**: Bind all modules with main classes to enforce.py
2. **Priority 2**: Add checks for foundation and coordination layers
3. **Priority 3**: Integrate tools into the enforcement pipeline
4. **Priority 4**: Add validation for governance engines
