// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/governance
 * @gl-semantic-anchor GL-00-SRC_GOVERNAN_INDEX
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Governance Module - Unified Exports
 * 
 * Provides comprehensive governance capabilities including policy management,
 * compliance checking, audit logging, and governance dashboards.
 * 
 * @module governance
 */

// Policy Engine
export {
  PolicyEngine,
  createPolicyEngine,
  PolicySeverity,
  PolicyAction,
  PolicyOperator,
  type Policy,
  type PolicyRule,
  type PolicyCondition,
  type PolicyContext,
  type PolicyEvaluationResult,
  type PolicyViolation,
  type PolicyVersion,
  type PolicyEngineConfig
} from './policy/policy-engine';

// Compliance Checker
export {
  ComplianceChecker,
  createComplianceChecker,
  ComplianceFramework,
  ComplianceStatus,
  ComplianceSeverity,
  type ComplianceRule,
  type ComplianceContext,
  type ComplianceValidationResult,
  type ComplianceViolation,
  type ComplianceScanResult,
  type ComplianceReport,
  type ComplianceCheckerConfig
} from './compliance/compliance-checker';

// Audit Manager
export {
  AuditManager,
  createAuditManager,
  AuditEventType,
  AuditSeverity,
  AuditStatus,
  type AuditEvent,
  type AuditQuery,
  type AuditReport,
  type AuditRetentionPolicy,
  type AuditManagerConfig
} from './audit/audit-manager';

// Governance Dashboard
export {
  GovernanceDashboard,
  createGovernanceDashboard,
  WidgetType,
  ChartType,
  type DashboardWidget,
  type DashboardLayout,
  type GovernanceMetrics,
  type DashboardDataSource,
  type DashboardAlert,
  type GovernanceDashboardConfig
} from './dashboard/governance-dashboard';

// Deployment Pipeline
export {
  DeploymentPipeline,
  createDeploymentPipeline,
  DeploymentEnvironment,
  DeploymentStatus,
  DeploymentStrategy,
  type DeploymentStage,
  type DeploymentContext,
  type DeploymentConfig,
  type DeploymentResult,
  type HealthCheckResult,
  type DeploymentPipelineConfig
} from './deployment/deployment-pipeline';

/**
 * Create a complete governance system
 */
export function createGovernanceSystem(config?: {
  policy?: unknown;
  compliance?: unknown;
  audit?: unknown;
  dashboard?: unknown;
  deployment?: unknown;
}) {
  const policyEngine = createPolicyEngine(config?.policy);
  const complianceChecker = createComplianceChecker(config?.compliance);
  const auditManager = createAuditManager(config?.audit);
  const dashboard = createGovernanceDashboard(config?.dashboard);
  const deploymentPipeline = createDeploymentPipeline(config?.deployment);

  return {
    policyEngine,
    complianceChecker,
    auditManager,
    dashboard,
    deploymentPipeline
  };
}