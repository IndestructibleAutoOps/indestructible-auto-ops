/**
 * @fileoverview GL-Gate:06 - Observability (Logging, Metrics, Tracing)
 * @module @machine-native-ops/gl-gate/gates/ObservabilityGate
 * @version 1.0.0
 * @since 2026-01-26
 * @author MachineNativeOps
 * @gl-governed true
 * @gl-layer GL-40-GOVERNANCE
 * @gl-gate gl-gate:06
 * 
 * gl-gate:06 — Observability (Logging, Metrics, Tracing)
 * gl-gate:06：可觀察性（記錄、指標、追蹤）
 * 
 * 建立完整的可觀察性框架，涵蓋日誌、系統指標、分散式追蹤，
 * 以支援問題診斷、效能分析與行為監控。
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
 * Observability Gate Configuration
 */
export interface ObservabilityGateConfig extends GateConfig {
  thresholds?: {
    /** Minimum log coverage percentage */
    minLogCoverage?: number;
    /** Minimum metric collection rate */
    minMetricRate?: number;
    /** Minimum trace sampling rate */
    minTraceSamplingRate?: number;
  };
  /** Required log levels */
  requiredLogLevels?: string[];
  /** Required metrics */
  requiredMetrics?: string[];
  /** Compliance requirements (GDPR, etc.) */
  complianceRequirements?: string[];
}

/**
 * Observability status
 */
export interface ObservabilityStatus {
  logging: LoggingStatus;
  metrics: MetricsStatus;
  tracing: TracingStatus;
  telemetry: TelemetryStatus;
  compliance: ComplianceStatus;
}

export interface LoggingStatus {
  enabled: boolean;
  coverage: number;
  structuredLogging: boolean;
  logLevels: string[];
  retentionDays: number;
  centralizedLogging: boolean;
}

export interface MetricsStatus {
  enabled: boolean;
  collectionRate: number;
  metricsCount: number;
  customMetrics: string[];
  alertsConfigured: number;
  dashboardsAvailable: boolean;
}

export interface TracingStatus {
  enabled: boolean;
  samplingRate: number;
  distributedTracing: boolean;
  contextPropagation: boolean;
  spanCount: number;
  traceRetentionDays: number;
}

export interface TelemetryStatus {
  enabled: boolean;
  openTelemetryCompliant: boolean;
  exporters: string[];
  dataPrivacyCompliant: boolean;
}

export interface ComplianceStatus {
  gdprCompliant: boolean;
  piiFiltered: boolean;
  dataRetentionPolicy: boolean;
  auditTrailEnabled: boolean;
}

/**
 * GL-Gate:06 - Observability Gate
 * 可觀察性閘門
 * 
 * Validates observability implementation including logging,
 * metrics collection, distributed tracing, and compliance.
 */
export class ObservabilityGate extends BaseGate {
  public readonly gateId: GateId = 'gl-gate:06';
  public readonly nameEN = 'Observability (Logging, Metrics, Tracing)';
  public readonly nameZH = '可觀察性（記錄、指標、追蹤）';

  private defaultThresholds = {
    minLogCoverage: 0.95,
    minMetricRate: 0.99,
    minTraceSamplingRate: 0.1
  };

  /**
   * Execute observability gate validation
   */
  public async execute(context: GateContext, config?: ObservabilityGateConfig): Promise<GateResult> {
    const startTime = Date.now();
    const findings: GateFinding[] = [];
    const metrics: GateMetric[] = [];

    const thresholds = {
      ...this.defaultThresholds,
      ...config?.thresholds
    };

    try {
      // Collect observability status
      const status = await this.collectObservabilityStatus(context);

      // Validate Logging
      await this.validateLogging(status.logging, thresholds, findings, metrics);

      // Validate Metrics
      await this.validateMetrics(status.metrics, thresholds, findings, metrics);

      // Validate Tracing
      await this.validateTracing(status.tracing, thresholds, findings, metrics);

      // Validate Telemetry
      await this.validateTelemetry(status.telemetry, findings, metrics);

      // Validate Compliance
      await this.validateCompliance(status.compliance, config?.complianceRequirements, findings, metrics);

      // Calculate observability score
      const observabilityScore = this.calculateObservabilityScore(status, findings);
      metrics.push(this.createMetric(
        'observability_score',
        observabilityScore,
        'score',
        { component: 'overall' }
      ));

      // Determine overall status
      const resultStatus = this.determineStatus(findings);
      const message = this.generateResultMessage(findings, observabilityScore);

      if (resultStatus === 'passed') {
        return this.createSuccessResult(context, message, findings, metrics, startTime);
      } else if (resultStatus === 'warning') {
        return this.createWarningResult(context, message, findings, metrics, startTime);
      } else {
        return this.createFailedResult(context, message, findings, metrics, startTime);
      }

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      findings.push(this.createFinding(
        'violation',
        'critical',
        'Observability Gate Execution Error',
        `Failed to execute observability gate: ${errorMessage}`
      ));
      return this.createFailedResult(context, `Observability gate failed: ${errorMessage}`, findings, metrics, startTime);
    }
  }

  /**
   * Validate logging configuration
   */
  private async validateLogging(
    logging: LoggingStatus,
    thresholds: typeof this.defaultThresholds,
    findings: GateFinding[],
    metrics: GateMetric[]
  ): Promise<void> {
    metrics.push(this.createMetric(
      'logging_enabled',
      logging.enabled ? 1 : 0,
      'boolean',
      { component: 'logging' }
    ));

    metrics.push(this.createMetric(
      'log_coverage',
      logging.coverage,
      'ratio',
      { component: 'logging' },
      thresholds.minLogCoverage,
      true // isMinimumThreshold - we want coverage >= threshold
    ));

    metrics.push(this.createMetric(
      'log_retention_days',
      logging.retentionDays,
      'days',
      { component: 'logging' }
    ));

    if (!logging.enabled) {
      findings.push(this.createFinding(
        'violation',
        'critical',
        'Logging Not Enabled',
        'Logging is not enabled for the system',
        { remediation: 'Enable logging with appropriate configuration' }
      ));
    }

    if (logging.coverage < thresholds.minLogCoverage) {
      findings.push(this.createFinding(
        'warning',
        'medium',
        'Insufficient Log Coverage',
        `Log coverage (${(logging.coverage * 100).toFixed(1)}%) is below threshold (${(thresholds.minLogCoverage * 100).toFixed(1)}%)`,
        { remediation: 'Add logging to uncovered components and critical paths' }
      ));
    }

    if (!logging.structuredLogging) {
      findings.push(this.createFinding(
        'warning',
        'medium',
        'Structured Logging Not Implemented',
        'Logs are not in structured format (JSON)',
        { remediation: 'Implement structured logging for better searchability and analysis' }
      ));
    }

    if (!logging.centralizedLogging) {
      findings.push(this.createFinding(
        'warning',
        'low',
        'Centralized Logging Not Configured',
        'Logs are not sent to a centralized logging system',
        { remediation: 'Configure centralized logging (ELK, Loki, CloudWatch, etc.)' }
      ));
    }
  }

  /**
   * Validate metrics configuration
   */
  private async validateMetrics(
    metricsStatus: MetricsStatus,
    thresholds: typeof this.defaultThresholds,
    findings: GateFinding[],
    metrics: GateMetric[]
  ): Promise<void> {
    metrics.push(this.createMetric(
      'metrics_enabled',
      metricsStatus.enabled ? 1 : 0,
      'boolean',
      { component: 'metrics' }
    ));

    metrics.push(this.createMetric(
      'metric_collection_rate',
      metricsStatus.collectionRate,
      'ratio',
      { component: 'metrics' },
      thresholds.minMetricRate
    ));

    metrics.push(this.createMetric(
      'metrics_count',
      metricsStatus.metricsCount,
      'count',
      { component: 'metrics' }
    ));

    metrics.push(this.createMetric(
      'alerts_configured',
      metricsStatus.alertsConfigured,
      'count',
      { component: 'metrics' }
    ));

    if (!metricsStatus.enabled) {
      findings.push(this.createFinding(
        'violation',
        'high',
        'Metrics Collection Not Enabled',
        'Metrics collection is not enabled',
        { remediation: 'Enable metrics collection with Prometheus, Datadog, or similar' }
      ));
    }

    if (metricsStatus.collectionRate < thresholds.minMetricRate) {
      findings.push(this.createFinding(
        'warning',
        'medium',
        'Low Metric Collection Rate',
        `Metric collection rate (${(metricsStatus.collectionRate * 100).toFixed(1)}%) is below threshold`,
        { remediation: 'Investigate and fix metric collection failures' }
      ));
    }

    if (metricsStatus.alertsConfigured === 0) {
      findings.push(this.createFinding(
        'warning',
        'medium',
        'No Alerts Configured',
        'No alerting rules are configured for metrics',
        { remediation: 'Configure alerts for critical metrics and SLOs' }
      ));
    }

    if (!metricsStatus.dashboardsAvailable) {
      findings.push(this.createFinding(
        'info',
        'low',
        'No Dashboards Available',
        'No monitoring dashboards are configured',
        { remediation: 'Create dashboards for key metrics visualization' }
      ));
    }
  }

  /**
   * Validate tracing configuration
   */
  private async validateTracing(
    tracing: TracingStatus,
    thresholds: typeof this.defaultThresholds,
    findings: GateFinding[],
    metrics: GateMetric[]
  ): Promise<void> {
    metrics.push(this.createMetric(
      'tracing_enabled',
      tracing.enabled ? 1 : 0,
      'boolean',
      { component: 'tracing' }
    ));

    metrics.push(this.createMetric(
      'trace_sampling_rate',
      tracing.samplingRate,
      'ratio',
      { component: 'tracing' },
      thresholds.minTraceSamplingRate
    ));

    metrics.push(this.createMetric(
      'span_count',
      tracing.spanCount,
      'count',
      { component: 'tracing' }
    ));

    if (!tracing.enabled) {
      findings.push(this.createFinding(
        'warning',
        'medium',
        'Distributed Tracing Not Enabled',
        'Distributed tracing is not enabled',
        { remediation: 'Enable distributed tracing with Jaeger, Zipkin, or similar' }
      ));
    }

    if (tracing.enabled && tracing.samplingRate < thresholds.minTraceSamplingRate) {
      findings.push(this.createFinding(
        'info',
        'low',
        'Low Trace Sampling Rate',
        `Trace sampling rate (${(tracing.samplingRate * 100).toFixed(1)}%) may miss important traces`,
        { remediation: 'Consider increasing sampling rate for better visibility' }
      ));
    }

    if (tracing.enabled && !tracing.contextPropagation) {
      findings.push(this.createFinding(
        'warning',
        'medium',
        'Trace Context Propagation Not Configured',
        'Trace context is not propagated across service boundaries',
        { remediation: 'Implement W3C Trace Context or B3 propagation' }
      ));
    }
  }

  /**
   * Validate telemetry configuration
   */
  private async validateTelemetry(
    telemetry: TelemetryStatus,
    findings: GateFinding[],
    metrics: GateMetric[]
  ): Promise<void> {
    metrics.push(this.createMetric(
      'telemetry_enabled',
      telemetry.enabled ? 1 : 0,
      'boolean',
      { component: 'telemetry' }
    ));

    metrics.push(this.createMetric(
      'opentelemetry_compliant',
      telemetry.openTelemetryCompliant ? 1 : 0,
      'boolean',
      { component: 'telemetry' }
    ));

    if (!telemetry.openTelemetryCompliant) {
      findings.push(this.createFinding(
        'info',
        'low',
        'Not OpenTelemetry Compliant',
        'Telemetry is not OpenTelemetry compliant',
        { remediation: 'Consider migrating to OpenTelemetry for vendor neutrality' }
      ));
    }

    if (!telemetry.dataPrivacyCompliant) {
      findings.push(this.createFinding(
        'warning',
        'high',
        'Telemetry Data Privacy Concerns',
        'Telemetry data may contain sensitive information',
        { remediation: 'Implement PII filtering in telemetry pipeline' }
      ));
    }
  }

  /**
   * Validate compliance
   */
  private async validateCompliance(
    compliance: ComplianceStatus,
    requirements: string[] | undefined,
    findings: GateFinding[],
    metrics: GateMetric[]
  ): Promise<void> {
    metrics.push(this.createMetric(
      'gdpr_compliant',
      compliance.gdprCompliant ? 1 : 0,
      'boolean',
      { component: 'compliance' }
    ));

    metrics.push(this.createMetric(
      'pii_filtered',
      compliance.piiFiltered ? 1 : 0,
      'boolean',
      { component: 'compliance' }
    ));

    metrics.push(this.createMetric(
      'audit_trail_enabled',
      compliance.auditTrailEnabled ? 1 : 0,
      'boolean',
      { component: 'compliance' }
    ));

    if (!compliance.gdprCompliant && requirements?.includes('GDPR')) {
      findings.push(this.createFinding(
        'violation',
        'critical',
        'GDPR Compliance Required',
        'Observability data is not GDPR compliant',
        { remediation: 'Implement GDPR-compliant data handling in observability pipeline' }
      ));
    }

    if (!compliance.piiFiltered) {
      findings.push(this.createFinding(
        'warning',
        'high',
        'PII Not Filtered from Observability Data',
        'PII may be present in logs, metrics, or traces',
        { remediation: 'Implement PII filtering/masking in observability pipeline' }
      ));
    }

    if (!compliance.auditTrailEnabled) {
      findings.push(this.createFinding(
        'warning',
        'medium',
        'Audit Trail Not Enabled',
        'Audit trail for observability data access is not enabled',
        { remediation: 'Enable audit logging for observability data access' }
      ));
    }
  }

  /**
   * Collect observability status
   */
  private async collectObservabilityStatus(_context: GateContext): Promise<ObservabilityStatus> {
    // Simulated status - in production, integrate with actual observability systems
    // TODO: Replace with actual integration to observability platforms (Prometheus, Grafana, etc.)
    return {
      logging: {
        enabled: true,
        coverage: 0.96,
        structuredLogging: true,
        logLevels: ['error', 'warn', 'info', 'debug'],
        retentionDays: 30,
        centralizedLogging: true
      },
      metrics: {
        enabled: true,
        collectionRate: 0.995,
        metricsCount: 150,
        customMetrics: ['request_duration', 'error_rate', 'queue_depth'],
        alertsConfigured: 25,
        dashboardsAvailable: true
      },
      tracing: {
        enabled: true,
        samplingRate: 0.1,
        distributedTracing: true,
        contextPropagation: true,
        spanCount: 50000,
        traceRetentionDays: 7
      },
      telemetry: {
        enabled: true,
        openTelemetryCompliant: true,
        exporters: ['otlp', 'prometheus'],
        dataPrivacyCompliant: true
      },
      compliance: {
        gdprCompliant: true,
        piiFiltered: true,
        dataRetentionPolicy: true,
        auditTrailEnabled: true
      }
    };
  }

  /**
   * Calculate observability score
   */
  private calculateObservabilityScore(status: ObservabilityStatus, _findings: GateFinding[]): number {
    let score = 100;

    // Logging score (25 points)
    if (!status.logging.enabled) score -= 25;
    else {
      score -= (1 - status.logging.coverage) * 10;
      if (!status.logging.structuredLogging) score -= 5;
      if (!status.logging.centralizedLogging) score -= 5;
    }

    // Metrics score (25 points)
    if (!status.metrics.enabled) score -= 25;
    else {
      score -= (1 - status.metrics.collectionRate) * 10;
      if (status.metrics.alertsConfigured === 0) score -= 10;
    }

    // Tracing score (25 points)
    if (!status.tracing.enabled) score -= 15;
    else {
      if (!status.tracing.contextPropagation) score -= 10;
    }

    // Compliance score (25 points)
    if (!status.compliance.gdprCompliant) score -= 10;
    if (!status.compliance.piiFiltered) score -= 10;
    if (!status.compliance.auditTrailEnabled) score -= 5;

    return Math.max(0, Math.min(100, score));
  }

  /**
   * Generate result message
   */
  private generateResultMessage(findings: GateFinding[], score: number): string {
    const violations = findings.filter(f => f.type === 'violation').length;
    const warnings = findings.filter(f => f.type === 'warning').length;

    if (violations === 0 && warnings === 0) {
      return `Observability gate passed. Score: ${score}/100`;
    }

    const parts: string[] = [];
    if (violations > 0) parts.push(`${violations} violation(s)`);
    if (warnings > 0) parts.push(`${warnings} warning(s)`);

    return `Observability gate completed with ${parts.join(' and ')}. Score: ${score}/100`;
  }
}

// GL Unified Charter Activated