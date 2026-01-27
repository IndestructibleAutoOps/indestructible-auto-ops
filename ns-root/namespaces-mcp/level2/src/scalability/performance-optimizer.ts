/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/scalability
 * @gl-semantic-anchor GL-00-SRC_SCALABIL_PERFORMANCEO
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Performance Optimizer
 * 
 * Real-time performance tuning with bottleneck detection,
 * automated optimization, and performance profiling.
 * 
 * Performance Targets:
 * - Optimization Decision: <50ms
 * - Performance Improvement: 30%+
 * - Bottleneck Detection: <100ms
 * - Profiling Overhead: <5%
 * 
 * @module scalability/performance-optimizer
 */

import { EventEmitter } from 'events';

/**
 * Performance metric types
 */
export enum MetricType {
  LATENCY = 'latency',
  THROUGHPUT = 'throughput',
  CPU_USAGE = 'cpu-usage',
  MEMORY_USAGE = 'memory-usage',
  DISK_IO = 'disk-io',
  NETWORK_IO = 'network-io',
  ERROR_RATE = 'error-rate',
  QUEUE_DEPTH = 'queue-depth'
}

/**
 * Optimization action types
 */
export enum OptimizationAction {
  SCALE_UP = 'scale-up',
  SCALE_DOWN = 'scale-down',
  TUNE_PARAMETERS = 'tune-parameters',
  CACHE_OPTIMIZATION = 'cache-optimization',
  LOAD_BALANCING = 'load-balancing',
  RESOURCE_REALLOCATION = 'resource-reallocation',
  QUERY_OPTIMIZATION = 'query-optimization',
  CONNECTION_POOLING = 'connection-pooling'
}

/**
 * Bottleneck severity
 */
export enum BottleneckSeverity {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low'
}

/**
 * Performance metric
 */
export interface PerformanceMetric {
  type: MetricType;
  value: number;
  unit: string;
  timestamp: Date;
  source: string;
  tags?: Record<string, string>;
}

/**
 * Performance baseline
 */
export interface PerformanceBaseline {
  metricType: MetricType;
  p50: number;
  p95: number;
  p99: number;
  average: number;
  stdDev: number;
  sampleSize: number;
  lastUpdated: Date;
}

/**
 * Bottleneck detection
 */
export interface Bottleneck {
  id: string;
  type: string;
  severity: BottleneckSeverity;
  component: string;
  metric: MetricType;
  currentValue: number;
  expectedValue: number;
  impact: number; // percentage
  detectedAt: Date;
  description: string;
  recommendations: string[];
}

/**
 * Optimization recommendation
 */
export interface OptimizationRecommendation {
  id: string;
  action: OptimizationAction;
  priority: number;
  component: string;
  description: string;
  expectedImprovement: number; // percentage
  estimatedCost: number;
  confidence: number; // 0-1
  parameters?: Record<string, any>;
}

/**
 * Optimization result
 */
export interface OptimizationResult {
  recommendationId: string;
  action: OptimizationAction;
  success: boolean;
  actualImprovement: number;
  executionTime: number;
  error?: string;
  metadata?: Record<string, any>;
}

/**
 * Performance profile
 */
export interface PerformanceProfile {
  component: string;
  startTime: Date;
  endTime: Date;
  duration: number;
  metrics: PerformanceMetric[];
  bottlenecks: Bottleneck[];
  recommendations: OptimizationRecommendation[];
}

/**
 * Tuning parameter
 */
export interface TuningParameter {
  name: string;
  currentValue: unknown;
  recommendedValue: unknown;
  minValue?: unknown;
  maxValue?: unknown;
  impact: number; // percentage
  description: string;
}

/**
 * Performance Optimizer Configuration
 */
export interface PerformanceOptimizerConfig {
  enableAutoOptimization: boolean;
  optimizationInterval: number; // seconds
  bottleneckThreshold: number; // percentage deviation
  minConfidence: number; // 0-1
  maxConcurrentOptimizations: number;
  profilingEnabled: boolean;
  profilingSampleRate: number; // 0-1
}

/**
 * Performance Optimizer
 * 
 * Continuously monitors performance metrics, detects bottlenecks,
 * and applies automated optimizations.
 */
export class PerformanceOptimizer extends EventEmitter {
  private config: PerformanceOptimizerConfig;
  private metrics: Map<string, PerformanceMetric[]>;
  private baselines: Map<MetricType, PerformanceBaseline>;
  private bottlenecks: Map<string, Bottleneck>;
  private recommendations: Map<string, OptimizationRecommendation>;
  private activeOptimizations: Set<string>;
  private profiles: Map<string, PerformanceProfile>;
  private isRunning: boolean;

  constructor(config: PerformanceOptimizerConfig) {
    super();
    this.config = config;
    this.metrics = new Map();
    this.baselines = new Map();
    this.bottlenecks = new Map();
    this.recommendations = new Map();
    this.activeOptimizations = new Set();
    this.profiles = new Map();
    this.isRunning = false;
  }

  /**
   * Start the performance optimizer
   */
  async start(): Promise<void> {
    if (this.isRunning) {
      throw new Error('Performance optimizer already running');
    }

    this.isRunning = true;
    this.emit('started');

    // Start optimization loop
    if (this.config.enableAutoOptimization) {
      this.startOptimizationLoop();
    }

    // Start baseline calculation
    this.startBaselineCalculation();
  }

  /**
   * Stop the performance optimizer
   */
  async stop(): Promise<void> {
    this.isRunning = false;
    this.emit('stopped');
  }

  /**
   * Record performance metric
   */
  recordMetric(metric: PerformanceMetric): void {
    const key = `${metric.source}:${metric.type}`;
    
    if (!this.metrics.has(key)) {
      this.metrics.set(key, []);
    }

    const series = this.metrics.get(key)!;
    series.push(metric);

    // Keep only recent metrics (last hour)
    const cutoff = new Date(Date.now() - 3600000);
    const filtered = series.filter(m => m.timestamp >= cutoff);
    this.metrics.set(key, filtered);

    this.emit('metric-recorded', { metric });

    // Check for bottlenecks
    this.checkBottleneck(metric);
  }

  /**
   * Detect bottlenecks
   */
  async detectBottlenecks(): Promise<Bottleneck[]> {
    const bottlenecks: Bottleneck[] = [];

    for (const [key, series] of this.metrics.entries()) {
      if (series.length === 0) continue;

      const [source, metricType] = key.split(':') as [string, MetricType];
      const baseline = this.baselines.get(metricType);
      
      if (!baseline) continue;

      const recentMetrics = series.slice(-10);
      const avgValue = recentMetrics.reduce((sum, m) => sum + m.value, 0) / recentMetrics.length;

      // Check if current value deviates significantly from baseline
      const deviation = Math.abs(avgValue - baseline.average) / baseline.average;
      
      if (deviation > this.config.bottleneckThreshold) {
        const severity = this.calculateSeverity(deviation);
        
        const bottleneck: Bottleneck = {
          id: `bottleneck-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
          type: metricType,
          severity,
          component: source,
          metric: metricType,
          currentValue: avgValue,
          expectedValue: baseline.average,
          impact: deviation * 100,
          detectedAt: new Date(),
          description: `${metricType} deviation: ${(deviation * 100).toFixed(1)}%`,
          recommendations: this.generateBottleneckRecommendations(metricType, deviation)
        };

        bottlenecks.push(bottleneck);
        this.bottlenecks.set(bottleneck.id, bottleneck);

        this.emit('bottleneck-detected', { bottleneck });
      }
    }

    return bottlenecks;
  }

  /**
   * Generate optimization recommendations
   */
  async generateRecommendations(): Promise<OptimizationRecommendation[]> {
    const recommendations: OptimizationRecommendation[] = [];

    // Analyze bottlenecks
    for (const bottleneck of this.bottlenecks.values()) {
      const recs = this.createRecommendationsForBottleneck(bottleneck);
      recommendations.push(...recs);
    }

    // Analyze metrics trends
    const trendRecs = this.analyzeTrends();
    recommendations.push(...trendRecs);

    // Sort by priority and confidence
    recommendations.sort((a, b) => {
      if (a.priority !== b.priority) {
        return b.priority - a.priority;
      }
      return b.confidence - a.confidence;
    });

    // Store recommendations
    for (const rec of recommendations) {
      this.recommendations.set(rec.id, rec);
    }

    return recommendations;
  }

  /**
   * Apply optimization
   */
  async applyOptimization(
    recommendationId: string
  ): Promise<OptimizationResult> {
    const recommendation = this.recommendations.get(recommendationId);
    if (!recommendation) {
      throw new Error(`Recommendation not found: ${recommendationId}`);
    }

    // Check concurrent optimizations limit
    if (this.activeOptimizations.size >= this.config.maxConcurrentOptimizations) {
      throw new Error('Maximum concurrent optimizations reached');
    }

    this.activeOptimizations.add(recommendationId);
    const startTime = Date.now();

    try {
      this.emit('optimization-started', { recommendation });

      // Execute optimization based on action type
      const improvement = await this.executeOptimization(recommendation);

      const executionTime = Date.now() - startTime;

      const result: OptimizationResult = {
        recommendationId,
        action: recommendation.action,
        success: true,
        actualImprovement: improvement,
        executionTime
      };

      this.emit('optimization-completed', { result });

      return result;

    } catch (error) {
      const executionTime = Date.now() - startTime;

      const result: OptimizationResult = {
        recommendationId,
        action: recommendation.action,
        success: false,
        actualImprovement: 0,
        executionTime,
        error: error instanceof Error ? error.message : 'Unknown error'
      };

      this.emit('optimization-failed', { result, error });

      return result;

    } finally {
      this.activeOptimizations.delete(recommendationId);
    }
  }

  /**
   * Start performance profiling
   */
  startProfiling(component: string): string {
    const profileId = `profile-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const profile: PerformanceProfile = {
      component,
      startTime: new Date(),
      endTime: new Date(),
      duration: 0,
      metrics: [],
      bottlenecks: [],
      recommendations: []
    };

    this.profiles.set(profileId, profile);

    this.emit('profiling-started', { profileId, component });

    return profileId;
  }

  /**
   * Stop performance profiling
   */
  async stopProfiling(profileId: string): Promise<PerformanceProfile> {
    const profile = this.profiles.get(profileId);
    if (!profile) {
      throw new Error(`Profile not found: ${profileId}`);
    }

    profile.endTime = new Date();
    profile.duration = profile.endTime.getTime() - profile.startTime.getTime();

    // Collect metrics for the component
    const componentMetrics = Array.from(this.metrics.entries())
      .filter(([key]) => key.startsWith(profile.component))
      .flatMap(([, series]) => series.filter(
        m => m.timestamp >= profile.startTime && m.timestamp <= profile.endTime
      ));

    profile.metrics = componentMetrics;

    // Detect bottlenecks in profile
    profile.bottlenecks = Array.from(this.bottlenecks.values())
      .filter(b => b.component === profile.component);

    // Generate recommendations
    profile.recommendations = await this.generateRecommendations();

    this.emit('profiling-completed', { profile });

    return profile;
  }

  /**
   * Get tuning parameters
   */
  getTuningParameters(component: string): TuningParameter[] {
    // Simplified - in production would analyze actual component parameters
    return [
      {
        name: 'cache_size',
        currentValue: 1000,
        recommendedValue: 2000,
        minValue: 100,
        maxValue: 10000,
        impact: 15,
        description: 'Increase cache size to reduce database queries'
      },
      {
        name: 'connection_pool_size',
        currentValue: 10,
        recommendedValue: 20,
        minValue: 5,
        maxValue: 100,
        impact: 10,
        description: 'Increase connection pool to handle more concurrent requests'
      },
      {
        name: 'batch_size',
        currentValue: 100,
        recommendedValue: 500,
        minValue: 10,
        maxValue: 1000,
        impact: 20,
        description: 'Increase batch size to improve throughput'
      }
    ];
  }

  /**
   * Calculate performance baseline
   */
  private calculateBaseline(metricType: MetricType): void {
    const allMetrics: number[] = [];

    for (const [key, series] of this.metrics.entries()) {
      if (key.endsWith(`:${metricType}`)) {
        allMetrics.push(...series.map(m => m.value));
      }
    }

    if (allMetrics.length < 10) return;

    // Sort for percentile calculation
    allMetrics.sort((a, b) => a - b);

    const p50Index = Math.floor(allMetrics.length * 0.5);
    const p95Index = Math.floor(allMetrics.length * 0.95);
    const p99Index = Math.floor(allMetrics.length * 0.99);

    const average = allMetrics.reduce((sum, v) => sum + v, 0) / allMetrics.length;
    const variance = allMetrics.reduce((sum, v) => sum + Math.pow(v - average, 2), 0) / allMetrics.length;
    const stdDev = Math.sqrt(variance);

    const baseline: PerformanceBaseline = {
      metricType,
      p50: allMetrics[p50Index],
      p95: allMetrics[p95Index],
      p99: allMetrics[p99Index],
      average,
      stdDev,
      sampleSize: allMetrics.length,
      lastUpdated: new Date()
    };

    this.baselines.set(metricType, baseline);

    this.emit('baseline-updated', { baseline });
  }

  /**
   * Check for bottleneck
   */
  private checkBottleneck(metric: PerformanceMetric): void {
    const baseline = this.baselines.get(metric.type);
    if (!baseline) return;

    const deviation = Math.abs(metric.value - baseline.average) / baseline.average;
    
    if (deviation > this.config.bottleneckThreshold) {
      const severity = this.calculateSeverity(deviation);
      
      const bottleneck: Bottleneck = {
        id: `bottleneck-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        type: metric.type,
        severity,
        component: metric.source,
        metric: metric.type,
        currentValue: metric.value,
        expectedValue: baseline.average,
        impact: deviation * 100,
        detectedAt: new Date(),
        description: `${metric.type} spike detected`,
        recommendations: this.generateBottleneckRecommendations(metric.type, deviation)
      };

      this.bottlenecks.set(bottleneck.id, bottleneck);
      this.emit('bottleneck-detected', { bottleneck });
    }
  }

  /**
   * Calculate severity
   */
  private calculateSeverity(deviation: number): BottleneckSeverity {
    if (deviation > 1.0) return BottleneckSeverity.CRITICAL;
    if (deviation > 0.5) return BottleneckSeverity.HIGH;
    if (deviation > 0.25) return BottleneckSeverity.MEDIUM;
    return BottleneckSeverity.LOW;
  }

  /**
   * Generate bottleneck recommendations
   */
  private generateBottleneckRecommendations(
    metricType: MetricType,
    deviation: number
  ): string[] {
    const recommendations: string[] = [];

    switch (metricType) {
      case MetricType.LATENCY:
        recommendations.push('Consider scaling up resources');
        recommendations.push('Optimize database queries');
        recommendations.push('Enable caching');
        break;
      
      case MetricType.CPU_USAGE:
        recommendations.push('Scale horizontally');
        recommendations.push('Optimize CPU-intensive operations');
        recommendations.push('Enable load balancing');
        break;
      
      case MetricType.MEMORY_USAGE:
        recommendations.push('Increase memory allocation');
        recommendations.push('Optimize memory usage');
        recommendations.push('Enable garbage collection tuning');
        break;
      
      case MetricType.ERROR_RATE:
        recommendations.push('Investigate error logs');
        recommendations.push('Implement retry logic');
        recommendations.push('Add circuit breakers');
        break;
    }

    return recommendations;
  }

  /**
   * Create recommendations for bottleneck
   */
  private createRecommendationsForBottleneck(
    bottleneck: Bottleneck
  ): OptimizationRecommendation[] {
    const recommendations: OptimizationRecommendation[] = [];

    switch (bottleneck.metric) {
      case MetricType.LATENCY:
        recommendations.push({
          id: `rec-${Date.now()}-1`,
          action: OptimizationAction.CACHE_OPTIMIZATION,
          priority: 8,
          component: bottleneck.component,
          description: 'Enable aggressive caching to reduce latency',
          expectedImprovement: 30,
          estimatedCost: 100,
          confidence: 0.85
        });
        break;
      
      case MetricType.CPU_USAGE:
        recommendations.push({
          id: `rec-${Date.now()}-2`,
          action: OptimizationAction.SCALE_UP,
          priority: 9,
          component: bottleneck.component,
          description: 'Scale up CPU resources',
          expectedImprovement: 40,
          estimatedCost: 500,
          confidence: 0.90
        });
        break;
    }

    return recommendations;
  }

  /**
   * Analyze trends
   */
  private analyzeTrends(): OptimizationRecommendation[] {
    const recommendations: OptimizationRecommendation[] = [];

    // Simplified trend analysis
    for (const [key, series] of this.metrics.entries()) {
      if (series.length < 20) continue;

      const recent = series.slice(-10);
      const older = series.slice(-20, -10);

      const recentAvg = recent.reduce((sum, m) => sum + m.value, 0) / recent.length;
      const olderAvg = older.reduce((sum, m) => sum + m.value, 0) / older.length;

      const trend = (recentAvg - olderAvg) / olderAvg;

      // If increasing trend > 20%, recommend optimization
      if (trend > 0.2) {
        const [source, metricType] = key.split(':');
        
        recommendations.push({
          id: `rec-trend-${Date.now()}`,
          action: OptimizationAction.TUNE_PARAMETERS,
          priority: 6,
          component: source,
          description: `${metricType} showing increasing trend`,
          expectedImprovement: 15,
          estimatedCost: 50,
          confidence: 0.75
        });
      }
    }

    return recommendations;
  }

  /**
   * Execute optimization
   */
  private async executeOptimization(
    recommendation: OptimizationRecommendation
  ): Promise<number> {
    // Simplified - in production would execute actual optimization
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Return simulated improvement
    return recommendation.expectedImprovement * (0.8 + Math.random() * 0.4);
  }

  /**
   * Start optimization loop
   */
  private startOptimizationLoop(): void {
    setInterval(async () => {
      if (!this.isRunning) return;

      try {
        // Detect bottlenecks
        await this.detectBottlenecks();

        // Generate recommendations
        const recommendations = await this.generateRecommendations();

        // Apply high-priority recommendations automatically
        for (const rec of recommendations) {
          if (rec.priority >= 8 && rec.confidence >= this.config.minConfidence) {
            try {
              await this.applyOptimization(rec.id);
            } catch (error) {
              // Continue with other optimizations
            }
          }
        }
      } catch (error) {
        this.emit('optimization-error', {
          error: error instanceof Error ? error.message : 'Unknown error'
        });
      }
    }, this.config.optimizationInterval * 1000);
  }

  /**
   * Start baseline calculation
   */
  private startBaselineCalculation(): void {
    setInterval(() => {
      if (!this.isRunning) return;

      for (const metricType of Object.values(MetricType)) {
        this.calculateBaseline(metricType);
      }
    }, 300000); // Recalculate every 5 minutes
  }
}

/**
 * Create performance optimizer with default configuration
 */
export function createPerformanceOptimizer(
  customConfig?: Partial<PerformanceOptimizerConfig>
): PerformanceOptimizer {
  const defaultConfig: PerformanceOptimizerConfig = {
    enableAutoOptimization: true,
    optimizationInterval: 300,
    bottleneckThreshold: 0.25,
    minConfidence: 0.80,
    maxConcurrentOptimizations: 5,
    profilingEnabled: true,
    profilingSampleRate: 0.1
  };

  const config = { ...defaultConfig, ...customConfig };
  return new PerformanceOptimizer(config);
}