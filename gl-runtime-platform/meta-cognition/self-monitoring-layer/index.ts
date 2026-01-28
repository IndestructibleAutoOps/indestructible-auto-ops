/**
 * GL Meta-Cognitive Runtime - Self-Monitoring Layer (Version 14.0.0)
 * 
 * The Self-Monitoring Layer provides the GL Runtime with the ability to:
 * - Monitor its own performance
 * - Track its own errors
 * - Observe its own evolution
 * - Assess its own civilization state
 * 
 * This is the "I know if I'm doing well" capability.
 */

import { EventEmitter } from 'events';

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface SelfMonitoringState {
  overallHealth: number;
  performanceMetrics: PerformanceMetrics;
  errorTracking: ErrorTracking;
  evolutionMonitoring: EvolutionMonitoring;
  civilizationMonitoring: CivilizationMonitoring;
  lastMonitoringCycle?: Date;
}

export interface PerformanceMetrics {
  cpuUsage: number;
  memoryUsage: number;
  responseTime: number;
  throughput: number;
  successRate: number;
  efficiency: number;
  reliability: number;
}

export interface ErrorTracking {
  totalErrors: number;
  errorRate: number;
  errorTypes: Map<string, number>;
  recentErrors: ErrorRecord[];
  errorTrends: ErrorTrend[];
}

export interface ErrorRecord {
  id: string;
  timestamp: Date;
  errorType: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  message: string;
  context: any;
  resolution?: string;
  resolvedAt?: Date;
}

export interface ErrorTrend {
  errorType: string;
  trend: 'increasing' | 'decreasing' | 'stable';
  rate: number;
}

export interface EvolutionMonitoring {
  currentVersion: string;
  evolutionProgress: number;
  mutationCount: number;
  optimizationCount: number;
  versionHistory: VersionRecord[];
  evolutionaryPatterns: Map<string, number>;
}

export interface VersionRecord {
  version: string;
  timestamp: Date;
  changes: string[];
  effectiveness: number;
}

export interface CivilizationMonitoring {
  governanceHealth: number;
  culturalCohesion: number;
  swarmEffectiveness: number;
  meshHealth: number;
  evolutionaryVelocity: number;
  civilizationMaturity: number;
}

export interface MonitoringAlert {
  id: string;
  timestamp: Date;
  alertType: 'performance' | 'error' | 'evolution' | 'civilization';
  severity: 'info' | 'warning' | 'critical';
  message: string;
  data: any;
}

// ============================================================================
// SELF-MONITORING LAYER CLASS
// ============================================================================

export class SelfMonitoringLayer extends EventEmitter {
  private state: SelfMonitoringState;
  private alerts: MonitoringAlert[];
  private monitoringInterval?: NodeJS.Timeout;
  private readonly MAX_ALERTS = 1000;
  private readonly MAX_ERRORS = 10000;

  constructor() {
    super();
    this.state = this.initializeState();
    this.alerts = [];
  }

  // ========================================================================
  // INITIALIZATION
  // ========================================================================

  private initializeState(): SelfMonitoringState {
    return {
      overallHealth: 0.8,
      performanceMetrics: {
        cpuUsage: 0,
        memoryUsage: 0,
        responseTime: 0,
        throughput: 0,
        successRate: 0.95,
        efficiency: 0.85,
        reliability: 0.9
      },
      errorTracking: {
        totalErrors: 0,
        errorRate: 0.05,
        errorTypes: new Map(),
        recentErrors: [],
        errorTrends: []
      },
      evolutionMonitoring: {
        currentVersion: '14.0.0',
        evolutionProgress: 0.3,
        mutationCount: 0,
        optimizationCount: 0,
        versionHistory: [],
        evolutionaryPatterns: new Map()
      },
      civilizationMonitoring: {
        governanceHealth: 0.85,
        culturalCohesion: 0.8,
        swarmEffectiveness: 0.88,
        meshHealth: 0.85,
        evolutionaryVelocity: 0.6,
        civilizationMaturity: 0.7
      }
    };
  }

  // ========================================================================
  // CORE MONITORING OPERATIONS
  // ========================================================================

  /**
   * Monitor overall system performance
   */
  public async monitorPerformance(metrics: Partial<PerformanceMetrics>): Promise<void> {
    // Update performance metrics
    this.state.performanceMetrics = {
      ...this.state.performanceMetrics,
      ...metrics
    };

    // Calculate overall health based on performance
    const performanceHealth = this.calculatePerformanceHealth();

    // Update overall health
    this.state.overallHealth = this.calculateOverallHealth(performanceHealth);

    // Check for performance alerts
    this.checkPerformanceAlerts();

    this.state.lastMonitoringCycle = new Date();
    this.emit('performance-monitored', this.state.performanceMetrics);
  }

  /**
   * Track and analyze errors
   */
  public async trackError(error: ErrorRecord): Promise<void> {
    // Add to error tracking
    this.state.errorTracking.totalErrors++;
    this.state.errorTracking.recentErrors.unshift(error);

    // Update error types
    const currentCount = this.state.errorTracking.errorTypes.get(error.errorType) || 0;
    this.state.errorTracking.errorTypes.set(error.errorType, currentCount + 1);

    // Maintain max errors
    if (this.state.errorTracking.recentErrors.length > this.MAX_ERRORS) {
      this.state.errorTracking.recentErrors.pop();
    }

    // Recalculate error rate
    this.state.errorTracking.errorRate = this.calculateErrorRate();

    // Update error trends
    this.updateErrorTrends();

    // Check for error alerts
    this.checkErrorAlerts(error);

    this.emit('error-tracked', error);
  }

  /**
   * Monitor evolutionary progress
   */
  public async monitorEvolution(evolutionData: any): Promise<void> {
    // Update evolution monitoring
    if (evolutionData.version) {
      this.state.evolutionMonitoring.currentVersion = evolutionData.version;
    }

    if (evolutionData.mutationCount !== undefined) {
      this.state.evolutionMonitoring.mutationCount = evolutionData.mutationCount;
    }

    if (evolutionData.optimizationCount !== undefined) {
      this.state.evolutionMonitoring.optimizationCount = evolutionData.optimizationCount;
    }

    if (evolutionData.progress !== undefined) {
      this.state.evolutionMonitoring.evolutionProgress = evolutionData.progress;
    }

    // Add version record if new version
    if (evolutionData.newVersion) {
      this.state.evolutionMonitoring.versionHistory.push({
        version: evolutionData.newVersion,
        timestamp: new Date(),
        changes: evolutionData.changes || [],
        effectiveness: evolutionData.effectiveness || 0.5
      });
    }

    // Update evolutionary patterns
    if (evolutionData.pattern) {
      const count = this.state.evolutionMonitoring.evolutionaryPatterns.get(evolutionData.pattern) || 0;
      this.state.evolutionMonitoring.evolutionaryPatterns.set(evolutionData.pattern, count + 1);
    }

    this.emit('evolution-monitored', this.state.evolutionMonitoring);
  }

  /**
   * Monitor civilization state
   */
  public async monitorCivilization(civData: Partial<CivilizationMonitoring>): Promise<void> {
    // Update civilization monitoring
    this.state.civilizationMonitoring = {
      ...this.state.civilizationMonitoring,
      ...civData
    };

    // Check for civilization alerts
    this.checkCivilizationAlerts();

    this.emit('civilization-monitored', this.state.civilizationMonitoring);
  }

  // ========================================================================
  // HEALTH CALCULATION
  // ========================================================================

  private calculatePerformanceHealth(): number {
    const metrics = this.state.performanceMetrics;

    const health = (
      (1 - metrics.cpuUsage) * 0.15 +
      (1 - metrics.memoryUsage) * 0.15 +
      metrics.successRate * 0.25 +
      metrics.efficiency * 0.2 +
      metrics.reliability * 0.25
    );

    return Math.max(0, Math.min(1, health));
  }

  private calculateOverallHealth(performanceHealth: number): number {
    const errorHealth = 1 - this.state.errorTracking.errorRate;
    const civHealth = this.calculateCivilizationHealth();

    const overall = (
      performanceHealth * 0.4 +
      errorHealth * 0.3 +
      civHealth * 0.3
    );

    return Math.max(0, Math.min(1, overall));
  }

  private calculateCivilizationHealth(): number {
    const civ = this.state.civilizationMonitoring;

    return (
      civ.governanceHealth * 0.25 +
      civ.culturalCohesion * 0.2 +
      civ.swarmEffectiveness * 0.2 +
      civ.meshHealth * 0.2 +
      civ.civilizationMaturity * 0.15
    );
  }

  // ========================================================================
  // ERROR TRACKING
  // ========================================================================

  private calculateErrorRate(): number {
    const totalOps = this.state.performanceMetrics.throughput || 1000;
    const errors = this.state.errorTracking.totalErrors;

    // Simple error rate calculation
    return Math.min(1, errors / totalOps);
  }

  private updateErrorTrends(): void {
    const trends: ErrorTrend[] = [];
    const recentErrors = this.state.errorTracking.recentErrors.slice(0, 100);

    // Group errors by type and calculate trends
    const errorGroups = new Map<string, ErrorRecord[]>();
    recentErrors.forEach(error => {
      const group = errorGroups.get(error.errorType) || [];
      group.push(error);
      errorGroups.set(error.errorType, group);
    });

    errorGroups.forEach((errors, type) => {
      const recentCount = errors.length;
      const olderCount = Math.floor(recentCount * 0.7); // Assume 30% growth rate baseline

      let trend: 'increasing' | 'decreasing' | 'stable';
      if (recentCount > olderCount * 1.5) {
        trend = 'increasing';
      } else if (recentCount < olderCount * 0.8) {
        trend = 'decreasing';
      } else {
        trend = 'stable';
      }

      trends.push({
        errorType: type,
        trend,
        rate: recentCount
      });
    });

    this.state.errorTracking.errorTrends = trends;
  }

  // ========================================================================
  // ALERT CHECKING
  // ========================================================================

  private checkPerformanceAlerts(): void {
    const metrics = this.state.performanceMetrics;

    // CPU usage alert
    if (metrics.cpuUsage > 0.8) {
      this.createAlert('performance', 'warning', 'High CPU usage detected', { cpuUsage: metrics.cpuUsage });
    }

    // Memory usage alert
    if (metrics.memoryUsage > 0.8) {
      this.createAlert('performance', 'warning', 'High memory usage detected', { memoryUsage: metrics.memoryUsage });
    }

    // Success rate alert
    if (metrics.successRate < 0.9) {
      this.createAlert('performance', 'warning', 'Low success rate detected', { successRate: metrics.successRate });
    }
  }

  private checkErrorAlerts(error: ErrorRecord): void {
    // Critical error alert
    if (error.severity === 'critical') {
      this.createAlert('error', 'critical', `Critical error: ${error.message}`, error);
    }

    // High error rate alert
    if (this.state.errorTracking.errorRate > 0.1) {
      this.createAlert('error', 'warning', 'High error rate detected', {
        errorRate: this.state.errorTracking.errorRate
      });
    }
  }

  private checkCivilizationAlerts(): void {
    const civ = this.state.civilizationMonitoring;

    // Governance health alert
    if (civ.governanceHealth < 0.7) {
      this.createAlert('civilization', 'warning', 'Governance health declining', {
        governanceHealth: civ.governanceHealth
      });
    }

    // Cultural cohesion alert
    if (civ.culturalCohesion < 0.7) {
      this.createAlert('civilization', 'warning', 'Cultural cohesion declining', {
        culturalCohesion: civ.culturalCohesion
      });
    }
  }

  private createAlert(
    alertType: 'performance' | 'error' | 'evolution' | 'civilization',
    severity: 'info' | 'warning' | 'critical',
    message: string,
    data: any
  ): void {
    const alert: MonitoringAlert = {
      id: this.generateId(),
      timestamp: new Date(),
      alertType,
      severity,
      message,
      data
    };

    this.alerts.unshift(alert);

    // Maintain max alerts
    if (this.alerts.length > this.MAX_ALERTS) {
      this.alerts.pop();
    }

    this.emit('alert-created', alert);
  }

  // ========================================================================
  // MONITORING CYCLES
  // ========================================================================

  public startMonitoring(intervalMs: number = 30000): void {
    if (this.monitoringInterval) {
      this.stopMonitoring();
    }

    this.monitoringInterval = setInterval(async () => {
      await this.performMonitoringCycle();
    }, intervalMs);

    this.emit('monitoring-started', { intervalMs });
  }

  public stopMonitoring(): void {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
      this.monitoringInterval = undefined;
      this.emit('monitoring-stopped');
    }
  }

  private async performMonitoringCycle(): Promise<void> {
    // This will trigger the meta-cognitive orchestrator
    // to perform full monitoring cycle
    this.emit('monitoring-cycle-requested');
  }

  // ========================================================================
  // STATE MANAGEMENT
  // ========================================================================

  public getState(): SelfMonitoringState {
    return {
      ...this.state,
      errorTracking: {
        ...this.state.errorTracking,
        errorTypes: new Map(this.state.errorTracking.errorTypes)
      },
      evolutionMonitoring: {
        ...this.state.evolutionMonitoring,
        evolutionaryPatterns: new Map(this.state.evolutionMonitoring.evolutionaryPatterns)
      }
    };
  }

  public getAlerts(filter?: {
    type?: string;
    severity?: string;
    since?: Date;
    limit?: number;
  }): MonitoringAlert[] {
    let filtered = this.alerts;

    if (filter?.type) {
      filtered = filtered.filter(alert => alert.alertType === filter.type);
    }

    if (filter?.severity) {
      filtered = filtered.filter(alert => alert.severity === filter.severity);
    }

    if (filter?.since) {
      filtered = filtered.filter(alert => alert.timestamp >= filter.since!);
    }

    if (filter?.limit) {
      filtered = filtered.slice(0, filter.limit);
    }

    return filtered;
  }

  public getRecentErrors(limit: number = 50): ErrorRecord[] {
    return this.state.errorTracking.recentErrors.slice(0, limit);
  }

  public getErrorTrends(): ErrorTrend[] {
    return this.state.errorTracking.errorTrends;
  }

  public getVersionHistory(): VersionRecord[] {
    return this.state.evolutionMonitoring.versionHistory;
  }

  // ========================================================================
  // UTILITY METHODS
  // ========================================================================

  private generateId(): string {
    return `mon_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // ========================================================================
  // CLEANUP
  // ========================================================================

  public destroy(): void {
    this.stopMonitoring();
    this.removeAllListeners();
    this.alerts = [];
  }
}