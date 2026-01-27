/**
 * @fileoverview GL-Gate Base Gate - Abstract base class for all governance gates
 * @module @machine-native-ops/gl-gate/gates/BaseGate
 * @version 1.0.0
 * @since 2026-01-26
 * @author MachineNativeOps
 * @gl-governed true
 * @gl-layer GL-40-GOVERNANCE
 * 
 * GL Unified Charter Activated
 */

import { randomBytes } from 'crypto';
import {
  GateId,
  GateContext,
  GateResult,
  GateConfig,
  GateFinding,
  GateMetric,
  GateStatus,
  GateSeverity
} from '../types';

/**
 * Abstract Base Gate
 * 抽象基礎閘門
 * 
 * Base class that all governance gate implementations must extend.
 * Provides common functionality and enforces consistent interface.
 */
export abstract class BaseGate {
  /** Gate identifier */
  public abstract readonly gateId: GateId;
  
  /** Gate name (English) */
  public abstract readonly nameEN: string;
  
  /** Gate name (Chinese) */
  public abstract readonly nameZH: string;

  /**
   * Execute the gate
   * 執行閘門
   * 
   * @param context - Execution context
   * @param config - Optional gate configuration
   * @returns Gate execution result
   */
  public abstract execute(context: GateContext, config?: GateConfig): Promise<GateResult>;

  /**
   * Validate gate prerequisites
   * 驗證閘門前置條件
   * 
   * @param context - Execution context
   * @returns Whether prerequisites are met
   */
  public async validatePrerequisites(_context: GateContext): Promise<{ valid: boolean; errors: string[] }> {
    return { valid: true, errors: [] };
  }

  /**
   * Create a successful result
   * 建立成功結果
   */
  protected createSuccessResult(
    context: GateContext,
    message: string,
    findings: GateFinding[] = [],
    metrics: GateMetric[] = [],
    startTime: number
  ): GateResult {
    return {
      gateId: this.gateId,
      status: 'passed',
      durationMs: Date.now() - startTime,
      message,
      findings,
      metrics,
      evidence: [],
      timestamp: new Date(),
      context
    };
  }

  /**
   * Create a failed result
   * 建立失敗結果
   */
  protected createFailedResult(
    context: GateContext,
    message: string,
    findings: GateFinding[],
    metrics: GateMetric[] = [],
    startTime: number
  ): GateResult {
    return {
      gateId: this.gateId,
      status: 'failed',
      durationMs: Date.now() - startTime,
      message,
      findings,
      metrics,
      evidence: [],
      timestamp: new Date(),
      context
    };
  }

  /**
   * Create a warning result
   * 建立警告結果
   */
  protected createWarningResult(
    context: GateContext,
    message: string,
    findings: GateFinding[],
    metrics: GateMetric[] = [],
    startTime: number
  ): GateResult {
    return {
      gateId: this.gateId,
      status: 'warning',
      durationMs: Date.now() - startTime,
      message,
      findings,
      metrics,
      evidence: [],
      timestamp: new Date(),
      context
    };
  }

  /**
   * Create a finding
   * 建立發現
   */
  protected createFinding(
    type: 'violation' | 'warning' | 'info' | 'recommendation',
    severity: GateSeverity,
    title: string,
    description: string,
    options?: {
      location?: string;
      remediation?: string;
    }
  ): GateFinding {
    return {
      id: this.generateFindingId(),
      type,
      severity,
      title,
      description,
      location: options?.location,
      remediation: options?.remediation
    };
  }

  /**
   * Create a metric
   * 建立指標
   * 
   * @param name - Metric name
   * @param value - Metric value
   * @param unit - Unit of measurement
   * @param labels - Metric labels
   * @param threshold - Threshold value (if applicable)
   * @param isMinimumThreshold - If true, threshold is a minimum (value < threshold is bad). If false, threshold is a maximum (value > threshold is bad). Defaults to false for backward compatibility.
   */
  protected createMetric(
    name: string,
    value: number,
    unit: string,
    labels: Record<string, string> = {},
    threshold?: number,
    isMinimumThreshold = false
  ): GateMetric {
    let thresholdExceeded: boolean | undefined;
    if (threshold !== undefined) {
      // For minimum thresholds (e.g., cache_hit_rate), exceeding means value < threshold
      // For maximum thresholds (e.g., latency), exceeding means value > threshold
      thresholdExceeded = isMinimumThreshold ? value < threshold : value > threshold;
    }
    
    return {
      name,
      value,
      unit,
      threshold,
      thresholdExceeded,
      labels: {
        gate: this.gateId,
        ...labels
      }
    };
  }

  /**
   * Determine result status based on findings
   * 根據發現決定結果狀態
   */
  protected determineStatus(findings: GateFinding[]): GateStatus {
    const hasViolation = findings.some(f => f.type === 'violation');
    const hasWarning = findings.some(f => f.type === 'warning');
    
    if (hasViolation) return 'failed';
    if (hasWarning) return 'warning';
    return 'passed';
  }

  /**
   * Generate finding ID using cryptographically secure random bytes
   */
  private generateFindingId(): string {
    const random = randomBytes(4).toString('base64url').substring(0, 6);
    return `${this.gateId}-fnd-${Date.now()}-${random}`;
  }
}

// GL Unified Charter Activated