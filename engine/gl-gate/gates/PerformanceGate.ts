/**
 * @fileoverview GL-Gate:01 - Performance Optimization with Batching and Caching
 * @module @machine-native-ops/gl-gate/gates/PerformanceGate
 * @version 1.0.0
 * @since 2026-01-26
 * @author MachineNativeOps
 * @gl-governed true
 * @gl-layer GL-40-GOVERNANCE
 * @gl-gate gl-gate:01
 * 
 * gl-gate:01 — Performance Optimization with Batching and Caching
 * gl-gate:01：利用批次與快取進行效能優化
 * 
 * 負責透過批次處理、快取策略、重複查詢合併與資源重用來提升系統效能，
 * 降低延遲與運算成本。
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
 * Performance Gate Configuration
 */
export interface PerformanceGateConfig extends GateConfig {
  thresholds?: {
    /** Minimum acceptable cache hit rate (0-1) */
    cacheHitRate?: number;
    /** Maximum acceptable latency in ms */
    maxLatencyMs?: number;
    /** Minimum batch processing success rate (0-1) */
    batchSuccessRate?: number;
    /** Maximum memory usage percentage */
    maxMemoryUsagePercent?: number;
  };
}

/**
 * Performance metrics input
 */
export interface PerformanceMetrics {
  cacheHitRate: number;
  cacheMissRate: number;
  averageLatencyMs: number;
  p95LatencyMs: number;
  p99LatencyMs: number;
  batchProcessingSuccessRate: number;
  queryDeduplicationRate: number;
  resourceUtilization: number;
  memoryUsagePercent: number;
  cpuUsagePercent: number;
}

/**
 * GL-Gate:01 - Performance Optimization Gate
 * 效能優化閘門
 * 
 * Validates system performance through batch processing efficiency,
 * caching effectiveness, and resource utilization metrics.
 */
export class PerformanceGate extends BaseGate {
  public readonly gateId: GateId = 'gl-gate:01';
  public readonly nameEN = 'Performance Optimization with Batching and Caching';
  public readonly nameZH = '利用批次與快取進行效能優化';

  private defaultThresholds = {
    cacheHitRate: 0.8,
    maxLatencyMs: 1000,
    batchSuccessRate: 0.99,
    maxMemoryUsagePercent: 85
  };

  /**
   * Execute performance gate validation
   */
  public async execute(context: GateContext, config?: PerformanceGateConfig): Promise<GateResult> {
    const startTime = Date.now();
    const findings: GateFinding[] = [];
    const metrics: GateMetric[] = [];

    const thresholds = {
      ...this.defaultThresholds,
      ...config?.thresholds
    };

    try {
      // Get performance metrics (in real implementation, this would collect actual metrics)
      const perfMetrics = await this.collectPerformanceMetrics(context);

      // Validate cache hit rate
      metrics.push(this.createMetric(
        'cache_hit_rate',
        perfMetrics.cacheHitRate,
        'ratio',
        { component: 'cache' },
        thresholds.cacheHitRate,
        true // isMinimumThreshold - we want value >= threshold
      ));

      if (perfMetrics.cacheHitRate < thresholds.cacheHitRate) {
        findings.push(this.createFinding(
          'warning',
          'medium',
          'Cache Hit Rate Below Threshold',
          `Cache hit rate (${(perfMetrics.cacheHitRate * 100).toFixed(1)}%) is below the threshold (${(thresholds.cacheHitRate * 100).toFixed(1)}%)`,
          {
            remediation: 'Review cache configuration, increase cache size, or optimize cache key strategies'
          }
        ));
      }

      // Validate latency
      metrics.push(this.createMetric(
        'average_latency_ms',
        perfMetrics.averageLatencyMs,
        'milliseconds',
        { component: 'latency' },
        thresholds.maxLatencyMs
      ));

      metrics.push(this.createMetric(
        'p95_latency_ms',
        perfMetrics.p95LatencyMs,
        'milliseconds',
        { component: 'latency', percentile: 'p95' }
      ));

      metrics.push(this.createMetric(
        'p99_latency_ms',
        perfMetrics.p99LatencyMs,
        'milliseconds',
        { component: 'latency', percentile: 'p99' }
      ));

      if (perfMetrics.averageLatencyMs > thresholds.maxLatencyMs) {
        findings.push(this.createFinding(
          'violation',
          'high',
          'Latency Exceeds Threshold',
          `Average latency (${perfMetrics.averageLatencyMs}ms) exceeds maximum threshold (${thresholds.maxLatencyMs}ms)`,
          {
            remediation: 'Optimize database queries, implement caching, or scale resources'
          }
        ));
      }

      // Validate batch processing
      metrics.push(this.createMetric(
        'batch_success_rate',
        perfMetrics.batchProcessingSuccessRate,
        'ratio',
        { component: 'batch' },
        thresholds.batchSuccessRate,
        true // isMinimumThreshold - we want value >= threshold
      ));

      if (perfMetrics.batchProcessingSuccessRate < thresholds.batchSuccessRate) {
        findings.push(this.createFinding(
          'violation',
          'high',
          'Batch Processing Success Rate Below Threshold',
          `Batch processing success rate (${(perfMetrics.batchProcessingSuccessRate * 100).toFixed(1)}%) is below threshold (${(thresholds.batchSuccessRate * 100).toFixed(1)}%)`,
          {
            remediation: 'Review batch job configurations, implement retry logic, or investigate failure causes'
          }
        ));
      }

      // Validate memory usage
      metrics.push(this.createMetric(
        'memory_usage_percent',
        perfMetrics.memoryUsagePercent,
        'percent',
        { component: 'memory' },
        thresholds.maxMemoryUsagePercent
      ));

      if (perfMetrics.memoryUsagePercent > thresholds.maxMemoryUsagePercent) {
        findings.push(this.createFinding(
          'warning',
          'medium',
          'High Memory Usage',
          `Memory usage (${perfMetrics.memoryUsagePercent}%) exceeds threshold (${thresholds.maxMemoryUsagePercent}%)`,
          {
            remediation: 'Optimize memory allocation, implement garbage collection tuning, or scale resources'
          }
        ));
      }

      // Add additional metrics
      metrics.push(this.createMetric(
        'query_deduplication_rate',
        perfMetrics.queryDeduplicationRate,
        'ratio',
        { component: 'optimization' }
      ));

      metrics.push(this.createMetric(
        'resource_utilization',
        perfMetrics.resourceUtilization,
        'ratio',
        { component: 'resources' }
      ));

      metrics.push(this.createMetric(
        'cpu_usage_percent',
        perfMetrics.cpuUsagePercent,
        'percent',
        { component: 'cpu' }
      ));

      // Determine overall status
      const status = this.determineStatus(findings);
      const message = this.generateResultMessage(findings, perfMetrics);

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
        'Performance Gate Execution Error',
        `Failed to execute performance gate: ${errorMessage}`
      ));
      return this.createFailedResult(context, `Performance gate failed: ${errorMessage}`, findings, metrics, startTime);
    }
  }

  /**
   * Collect performance metrics
   * In real implementation, this would integrate with monitoring systems
   */
  private async collectPerformanceMetrics(_context: GateContext): Promise<PerformanceMetrics> {
    // Simulated metrics - in production, integrate with Prometheus, Datadog, etc.
    // TODO: Replace with actual performance metrics collection from monitoring systems
    return {
      cacheHitRate: 0.85,
      cacheMissRate: 0.15,
      averageLatencyMs: 150,
      p95LatencyMs: 450,
      p99LatencyMs: 800,
      batchProcessingSuccessRate: 0.995,
      queryDeduplicationRate: 0.3,
      resourceUtilization: 0.65,
      memoryUsagePercent: 72,
      cpuUsagePercent: 45
    };
  }

  /**
   * Generate result message
   */
  private generateResultMessage(findings: GateFinding[], metrics: PerformanceMetrics): string {
    const violations = findings.filter(f => f.type === 'violation').length;
    const warnings = findings.filter(f => f.type === 'warning').length;

    if (violations === 0 && warnings === 0) {
      return `Performance gate passed. Cache hit rate: ${(metrics.cacheHitRate * 100).toFixed(1)}%, Avg latency: ${metrics.averageLatencyMs}ms`;
    }

    const parts: string[] = [];
    if (violations > 0) parts.push(`${violations} violation(s)`);
    if (warnings > 0) parts.push(`${warnings} warning(s)`);

    return `Performance gate completed with ${parts.join(' and ')}`;
  }
}

// GL Unified Charter Activated