/**
 * @fileoverview GL-Gate:19 - Governance Summary (Compliance Reporting)
 * @module @machine-native-ops/gl-gate/gates/GovernanceSummaryGate
 * @version 1.0.0
 * @since 2026-01-26
 * @author MachineNativeOps
 * @gl-governed true
 * @gl-layer GL-40-GOVERNANCE
 * @gl-gate gl-gate:19
 * 
 * gl-gate:19 — Governance Summary (Compliance Reporting)
 * gl-gate:19：治理摘要（合規報告）
 * 
 * 彙整治理層級的執行情況、合規性報告、稽核紀錄與治理事件摘要，
 * 提供決策與審查依據。
 * 
 * GL Unified Charter Activated
 */

import { BaseGate } from './BaseGate';
import {
  GateId,
  GateContext,
  GateResult,
  GateConfig,
  GateFinding,
  GateMetric
} from '../types';

/**
 * Governance Summary Gate Configuration
 */
export interface GovernanceSummaryGateConfig extends GateConfig {
  /** Compliance frameworks to check */
  complianceFrameworks?: string[];
  /** Minimum compliance score */
  minComplianceScore?: number;
  /** Include detailed audit records */
  includeAuditRecords?: boolean;
  /** Report format */
  reportFormat?: 'json' | 'markdown' | 'html';
}

/**
 * Governance summary data
 */
export interface GovernanceSummary {
  overallCompliance: ComplianceOverview;
  gateExecutionSummary: GateExecutionOverview;
  auditRecords: AuditRecord[];
  governanceEvents: GovernanceEvent[];
  recommendations: Recommendation[];
  riskAssessment: RiskAssessment;
}

export interface ComplianceOverview {
  overallScore: number;
  frameworkScores: Record<string, number>;
  compliantItems: number;
  nonCompliantItems: number;
  partiallyCompliantItems: number;
  lastAssessmentDate: Date;
}

export interface GateExecutionOverview {
  totalExecutions: number;
  passedExecutions: number;
  failedExecutions: number;
  averageDurationMs: number;
  mostFailedGates: { gateId: string; failureCount: number }[];
  executionTrend: 'improving' | 'stable' | 'degrading';
}

export interface AuditRecord {
  id: string;
  timestamp: Date;
  action: string;
  actor: string;
  resource: string;
  outcome: 'success' | 'failure';
  details: string;
}

export interface GovernanceEvent {
  id: string;
  timestamp: Date;
  type: string;
  severity: string;
  description: string;
  resolved: boolean;
}

export interface Recommendation {
  id: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  category: string;
  title: string;
  description: string;
  estimatedEffort: string;
  expectedImpact: string;
}

export interface RiskAssessment {
  overallRiskLevel: 'critical' | 'high' | 'medium' | 'low';
  riskFactors: RiskFactor[];
  mitigationStatus: number;
}

export interface RiskFactor {
  name: string;
  level: 'critical' | 'high' | 'medium' | 'low';
  description: string;
  mitigated: boolean;
}

/**
 * GL-Gate:19 - Governance Summary Gate
 * 治理摘要閘門
 * 
 * Aggregates governance execution status, compliance reports,
 * audit records, and governance event summaries.
 */
export class GovernanceSummaryGate extends BaseGate {
  public readonly gateId: GateId = 'gl-gate:19';
  public readonly nameEN = 'Governance Summary (Compliance Reporting)';
  public readonly nameZH = '治理摘要（合規報告）';

  private defaultComplianceFrameworks = ['SLSA', 'SOC2', 'ISO27001'];
  private defaultMinComplianceScore = 80;

  /**
   * Execute governance summary gate
   */
  public async execute(context: GateContext, config?: GovernanceSummaryGateConfig): Promise<GateResult> {
    const startTime = Date.now();
    const findings: GateFinding[] = [];
    const metrics: GateMetric[] = [];

    const frameworks = config?.complianceFrameworks ?? this.defaultComplianceFrameworks;
    const minScore = config?.minComplianceScore ?? this.defaultMinComplianceScore;

    try {
      // Collect governance summary
      const summary = await this.collectGovernanceSummary(context, frameworks);

      // Validate compliance overview
      await this.validateComplianceOverview(summary.overallCompliance, minScore, findings, metrics);

      // Validate gate execution summary
      await this.validateGateExecutionSummary(summary.gateExecutionSummary, findings, metrics);

      // Validate audit records
      await this.validateAuditRecords(summary.auditRecords, findings, metrics);

      // Validate governance events
      await this.validateGovernanceEvents(summary.governanceEvents, findings, metrics);

      // Process risk assessment
      await this.processRiskAssessment(summary.riskAssessment, findings, metrics);

      // Add recommendations as findings
      for (const rec of summary.recommendations) {
        if (rec.priority === 'critical' || rec.priority === 'high') {
          findings.push(this.createFinding(
            'recommendation',
            rec.priority,
            rec.title,
            rec.description,
            { remediation: `Estimated effort: ${rec.estimatedEffort}. Expected impact: ${rec.expectedImpact}` }
          ));
        }
      }

      // Calculate governance health score
      const healthScore = this.calculateGovernanceHealthScore(summary);
      metrics.push(this.createMetric(
        'governance_health_score',
        healthScore,
        'score',
        { component: 'overall' }
      ));

      // Determine overall status
      const status = this.determineStatus(findings);
      const message = this.generateResultMessage(summary, healthScore);

      if (status === 'passed') {
        return this.createSuccessResult(context, message, findings, metrics, startTime);
      } else if (status === 'warning') {
        return this.createWarningResult(context, message, findings, metrics, startTime);
      } else {
        return this.createFailedResult(context, message, findings, metrics, startTime);
      }

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      findings.push(this.createFinding(
        'violation',
        'critical',
        'Governance Summary Gate Execution Error',
        `Failed to execute governance summary gate: ${errorMessage}`
      ));
      return this.createFailedResult(context, `Governance summary gate failed: ${errorMessage}`, findings, metrics, startTime);
    }
  }

  /**
   * Validate compliance overview
   */
  private async validateComplianceOverview(
    compliance: ComplianceOverview,
    minScore: number,
    findings: GateFinding[],
    metrics: GateMetric[]
  ): Promise<void> {
    metrics.push(this.createMetric(
      'overall_compliance_score',
      compliance.overallScore,
      'score',
      { component: 'compliance' },
      minScore
    ));

    metrics.push(this.createMetric(
      'compliant_items',
      compliance.compliantItems,
      'count',
      { component: 'compliance' }
    ));

    metrics.push(this.createMetric(
      'non_compliant_items',
      compliance.nonCompliantItems,
      'count',
      { component: 'compliance' }
    ));

    // Add framework-specific scores
    for (const [framework, score] of Object.entries(compliance.frameworkScores)) {
      metrics.push(this.createMetric(
        `compliance_score_${framework.toLowerCase()}`,
        score,
        'score',
        { component: 'compliance', framework }
      ));

      if (score < minScore) {
        findings.push(this.createFinding(
          'warning',
          'high',
          `${framework} Compliance Below Threshold`,
          `${framework} compliance score (${score}) is below minimum threshold (${minScore})`,
          { remediation: `Review and address ${framework} compliance gaps` }
        ));
      }
    }

    if (compliance.overallScore < minScore) {
      findings.push(this.createFinding(
        'violation',
        'high',
        'Overall Compliance Below Threshold',
        `Overall compliance score (${compliance.overallScore}) is below minimum threshold (${minScore})`,
        { remediation: 'Address critical compliance gaps across all frameworks' }
      ));
    }

    if (compliance.nonCompliantItems > 0) {
      findings.push(this.createFinding(
        'warning',
        'medium',
        'Non-Compliant Items Detected',
        `${compliance.nonCompliantItems} non-compliant items require attention`,
        { remediation: 'Review and remediate non-compliant items' }
      ));
    }
  }

  /**
   * Validate gate execution summary
   */
  private async validateGateExecutionSummary(
    execSummary: GateExecutionOverview,
    findings: GateFinding[],
    metrics: GateMetric[]
  ): Promise<void> {
    const passRate = execSummary.totalExecutions > 0 
      ? execSummary.passedExecutions / execSummary.totalExecutions 
      : 0;

    metrics.push(this.createMetric(
      'gate_pass_rate',
      passRate,
      'ratio',
      { component: 'execution' }
    ));

    metrics.push(this.createMetric(
      'total_gate_executions',
      execSummary.totalExecutions,
      'count',
      { component: 'execution' }
    ));

    metrics.push(this.createMetric(
      'average_gate_duration_ms',
      execSummary.averageDurationMs,
      'milliseconds',
      { component: 'execution' }
    ));

    if (passRate < 0.9) {
      findings.push(this.createFinding(
        'warning',
        'medium',
        'Low Gate Pass Rate',
        `Gate pass rate (${(passRate * 100).toFixed(1)}%) is below 90%`,
        { remediation: 'Investigate and address recurring gate failures' }
      ));
    }

    if (execSummary.executionTrend === 'degrading') {
      findings.push(this.createFinding(
        'warning',
        'high',
        'Degrading Gate Execution Trend',
        'Gate execution success rate is trending downward',
        { remediation: 'Investigate root causes of increasing failures' }
      ));
    }

    // Report most failed gates
    for (const failedGate of execSummary.mostFailedGates.slice(0, 3)) {
      if (failedGate.failureCount > 5) {
        findings.push(this.createFinding(
          'info',
          'medium',
          `Frequently Failing Gate: ${failedGate.gateId}`,
          `Gate ${failedGate.gateId} has failed ${failedGate.failureCount} times`,
          { remediation: `Review configuration and requirements for ${failedGate.gateId}` }
        ));
      }
    }
  }

  /**
   * Validate audit records
   */
  private async validateAuditRecords(
    auditRecords: AuditRecord[],
    findings: GateFinding[],
    metrics: GateMetric[]
  ): Promise<void> {
    metrics.push(this.createMetric(
      'audit_records_count',
      auditRecords.length,
      'count',
      { component: 'audit' }
    ));

    const failedAudits = auditRecords.filter(r => r.outcome === 'failure');
    metrics.push(this.createMetric(
      'failed_audit_actions',
      failedAudits.length,
      'count',
      { component: 'audit' }
    ));

    if (auditRecords.length === 0) {
      findings.push(this.createFinding(
        'warning',
        'medium',
        'No Audit Records Found',
        'No audit records are available for review',
        { remediation: 'Ensure audit logging is properly configured' }
      ));
    }

    const failureRateThreshold = 0.1;
    if (failedAudits.length > auditRecords.length * failureRateThreshold) {
      const failureRatePercent = failureRateThreshold * 100;
      findings.push(this.createFinding(
        'warning',
        'high',
        'High Audit Failure Rate',
        `${failedAudits.length} failed audit actions detected (>${failureRatePercent}% of total)`,
        { remediation: 'Investigate failed audit actions for potential security issues' }
      ));
    }
  }

  /**
   * Validate governance events
   */
  private async validateGovernanceEvents(
    events: GovernanceEvent[],
    findings: GateFinding[],
    metrics: GateMetric[]
  ): Promise<void> {
    const unresolvedEvents = events.filter(e => !e.resolved);
    const criticalEvents = events.filter(e => e.severity === 'critical');

    metrics.push(this.createMetric(
      'governance_events_total',
      events.length,
      'count',
      { component: 'events' }
    ));

    metrics.push(this.createMetric(
      'unresolved_events',
      unresolvedEvents.length,
      'count',
      { component: 'events' }
    ));

    metrics.push(this.createMetric(
      'critical_events',
      criticalEvents.length,
      'count',
      { component: 'events' }
    ));

    const unresolvedCritical = unresolvedEvents.filter(e => e.severity === 'critical');
    if (unresolvedCritical.length > 0) {
      findings.push(this.createFinding(
        'violation',
        'critical',
        'Unresolved Critical Governance Events',
        `${unresolvedCritical.length} critical governance events remain unresolved`,
        { remediation: 'Immediately address unresolved critical events' }
      ));
    }

    if (unresolvedEvents.length > 10) {
      findings.push(this.createFinding(
        'warning',
        'medium',
        'High Number of Unresolved Events',
        `${unresolvedEvents.length} governance events remain unresolved`,
        { remediation: 'Review and resolve pending governance events' }
      ));
    }
  }

  /**
   * Process risk assessment
   */
  private async processRiskAssessment(
    risk: RiskAssessment,
    findings: GateFinding[],
    metrics: GateMetric[]
  ): Promise<void> {
    const riskLevelScore = { critical: 4, high: 3, medium: 2, low: 1 };
    
    metrics.push(this.createMetric(
      'overall_risk_level',
      riskLevelScore[risk.overallRiskLevel],
      'level',
      { component: 'risk' }
    ));

    metrics.push(this.createMetric(
      'risk_mitigation_status',
      risk.mitigationStatus,
      'percent',
      { component: 'risk' }
    ));

    metrics.push(this.createMetric(
      'risk_factors_count',
      risk.riskFactors.length,
      'count',
      { component: 'risk' }
    ));

    if (risk.overallRiskLevel === 'critical') {
      findings.push(this.createFinding(
        'violation',
        'critical',
        'Critical Risk Level',
        'Overall governance risk level is critical',
        { remediation: 'Immediately address critical risk factors' }
      ));
    } else if (risk.overallRiskLevel === 'high') {
      findings.push(this.createFinding(
        'warning',
        'high',
        'High Risk Level',
        'Overall governance risk level is high',
        { remediation: 'Prioritize risk mitigation activities' }
      ));
    }

    const unmitigatedCritical = risk.riskFactors.filter(
      f => f.level === 'critical' && !f.mitigated
    );
    
    for (const factor of unmitigatedCritical) {
      findings.push(this.createFinding(
        'violation',
        'critical',
        `Unmitigated Critical Risk: ${factor.name}`,
        factor.description,
        { remediation: `Implement mitigation for ${factor.name}` }
      ));
    }
  }

  /**
   * Collect governance summary
   */
  private async collectGovernanceSummary(
    _context: GateContext,
    frameworks: string[]
  ): Promise<GovernanceSummary> {
    // Simulated data - in production, aggregate from actual governance systems
    // TODO: Replace with actual governance framework integration
    // WARNING: This is simulated data using random scores for demonstration purposes only
    const frameworkScores: Record<string, number> = {};
    for (const framework of frameworks) {
      frameworkScores[framework] = 85 + Math.floor(Math.random() * 10);
    }

    return {
      overallCompliance: {
        overallScore: 88,
        frameworkScores,
        compliantItems: 145,
        nonCompliantItems: 5,
        partiallyCompliantItems: 12,
        lastAssessmentDate: new Date()
      },
      gateExecutionSummary: {
        totalExecutions: 1250,
        passedExecutions: 1180,
        failedExecutions: 70,
        averageDurationMs: 2500,
        mostFailedGates: [
          { gateId: 'gl-gate:11', failureCount: 15 },
          { gateId: 'gl-gate:07', failureCount: 10 }
        ],
        executionTrend: 'stable'
      },
      auditRecords: [
        {
          id: 'audit-001',
          timestamp: new Date(),
          action: 'gate.execute',
          actor: 'system',
          resource: 'gl-gate:01',
          outcome: 'success',
          details: 'Gate executed successfully'
        }
      ],
      governanceEvents: [
        {
          id: 'event-001',
          timestamp: new Date(),
          type: 'compliance.check',
          severity: 'info',
          description: 'Scheduled compliance check completed',
          resolved: true
        }
      ],
      recommendations: [
        {
          id: 'rec-001',
          priority: 'medium',
          category: 'security',
          title: 'Enable MFA for all admin accounts',
          description: 'Multi-factor authentication should be enabled for all administrative accounts',
          estimatedEffort: '2 hours',
          expectedImpact: 'Significant security improvement'
        }
      ],
      riskAssessment: {
        overallRiskLevel: 'low',
        riskFactors: [
          {
            name: 'Outdated Dependencies',
            level: 'medium',
            description: 'Some dependencies have known vulnerabilities',
            mitigated: false
          }
        ],
        mitigationStatus: 85
      }
    };
  }

  /**
   * Calculate governance health score
   */
  private calculateGovernanceHealthScore(summary: GovernanceSummary): number {
    let score = 0;

    // Compliance contributes 40%
    score += summary.overallCompliance.overallScore * 0.4;

    // Gate execution contributes 30%
    const passRate = summary.gateExecutionSummary.totalExecutions > 0
      ? summary.gateExecutionSummary.passedExecutions / summary.gateExecutionSummary.totalExecutions
      : 0;
    score += passRate * 100 * 0.3;

    // Risk mitigation contributes 20%
    score += summary.riskAssessment.mitigationStatus * 0.2;

    // Event resolution contributes 10%
    const resolvedRate = summary.governanceEvents.length > 0
      ? summary.governanceEvents.filter(e => e.resolved).length / summary.governanceEvents.length
      : 1;
    score += resolvedRate * 100 * 0.1;

    return Math.round(score);
  }

  /**
   * Generate result message
   */
  private generateResultMessage(summary: GovernanceSummary, healthScore: number): string {
    return `Governance summary completed. Health score: ${healthScore}/100, ` +
      `Compliance: ${summary.overallCompliance.overallScore}%, ` +
      `Risk level: ${summary.riskAssessment.overallRiskLevel}`;
  }
}

// GL Unified Charter Activated