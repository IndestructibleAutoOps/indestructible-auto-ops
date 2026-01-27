/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/scalability
 * @gl-semantic-anchor GL-00-SRC_SCALABIL_AUTOSCALINGE
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Auto-Scaling Engine
 * 
 * Predictive scaling with metric-based triggers and custom policies
 * for automatic resource scaling.
 * 
 * Performance Targets:
 * - Prediction Accuracy: >99%
 * - Scaling Time: <60s
 * - Decision Latency: <100ms
 * - Scale Events: 1000+ per hour
 * 
 * @module scalability/auto-scaling-engine
 */

import { EventEmitter } from 'events';

/**
 * Scaling direction
 */
export enum ScalingDirection {
  UP = 'up',
  DOWN = 'down',
  NONE = 'none'
}

/**
 * Scaling trigger type
 */
export enum TriggerType {
  METRIC = 'metric',
  SCHEDULE = 'schedule',
  EVENT = 'event',
  PREDICTIVE = 'predictive',
  CUSTOM = 'custom'
}

/**
 * Metric comparison operator
 */
export enum ComparisonOperator {
  GREATER_THAN = 'gt',
  GREATER_THAN_OR_EQUAL = 'gte',
  LESS_THAN = 'lt',
  LESS_THAN_OR_EQUAL = 'lte',
  EQUAL = 'eq',
  NOT_EQUAL = 'ne'
}

/**
 * Scaling metric
 */
export interface ScalingMetric {
  name: string;
  value: number;
  unit: string;
  timestamp: Date;
  source: string;
}

/**
 * Metric-based trigger
 */
export interface MetricTrigger {
  id: string;
  type: TriggerType.METRIC;
  metricName: string;
  operator: ComparisonOperator;
  threshold: number;
  duration: number; // seconds
  cooldown: number; // seconds
  direction: ScalingDirection;
  amount: number;
  enabled: boolean;
}

/**
 * Schedule-based trigger
 */
export interface ScheduleTrigger {
  id: string;
  type: TriggerType.SCHEDULE;
  cron: string;
  direction: ScalingDirection;
  amount: number;
  enabled: boolean;
}

/**
 * Event-based trigger
 */
export interface EventTrigger {
  id: string;
  type: TriggerType.EVENT;
  eventType: string;
  condition?: (event: unknown) => boolean;
  direction: ScalingDirection;
  amount: number;
  enabled: boolean;
}

/**
 * Predictive trigger
 */
export interface PredictiveTrigger {
  id: string;
  type: TriggerType.PREDICTIVE;
  metricName: string;
  predictionWindow: number; // seconds
  confidence: number; // 0-1
  direction: ScalingDirection;
  enabled: boolean;
}

/**
 * Custom trigger
 */
export interface CustomTrigger {
  id: string;
  type: TriggerType.CUSTOM;
  evaluate: (metrics: ScalingMetric[]) => ScalingDecision | null;
  enabled: boolean;
}

/**
 * Scaling trigger union type
 */
export type ScalingTrigger = 
  | MetricTrigger 
  | ScheduleTrigger 
  | EventTrigger 
  | PredictiveTrigger 
  | CustomTrigger;

/**
 * Scaling policy
 */
export interface ScalingPolicy {
  id: string;
  name: string;
  resourceType: string;
  minSize: number;
  maxSize: number;
  desiredSize: number;
  triggers: ScalingTrigger[];
  cooldownPeriod: number; // seconds
  enabled: boolean;
  metadata: Record<string, any>;
}

/**
 * Scaling decision
 */
export interface ScalingDecision {
  policyId: string;
  triggerId: string;
  direction: ScalingDirection;
  currentSize: number;
  targetSize: number;
  amount: number;
  reason: string;
  confidence: number;
  timestamp: Date;
}

/**
 * Scaling event
 */
export interface ScalingEvent {
  id: string;
  policyId: string;
  decision: ScalingDecision;
  startTime: Date;
  endTime?: Date;
  status: 'pending' | 'in-progress' | 'completed' | 'failed';
  error?: string;
  metadata: Record<string, any>;
}

/**
 * Prediction model
 */
export interface PredictionModel {
  name: string;
  type: 'linear' | 'exponential' | 'seasonal' | 'ml';
  accuracy: number;
  lastTrained?: Date;
  parameters: Record<string, any>;
}

/**
 * Time series data point
 */
export interface TimeSeriesPoint {
  timestamp: Date;
  value: number;
}

/**
 * Auto-Scaling Engine Configuration
 */
export interface AutoScalingEngineConfig {
  policies: ScalingPolicy[];
  enablePredictive: boolean;
  predictionModels: PredictionModel[];
  evaluationInterval: number; // seconds
  metricsRetention: number; // seconds
  maxConcurrentScaling: number;
}

/**
 * Auto-Scaling Engine
 * 
 * Automatically scales resources based on metrics, schedules, events,
 * and predictive analysis.
 */
export class AutoScalingEngine extends EventEmitter {
  private config: AutoScalingEngineConfig;
  private policies: Map<string, ScalingPolicy>;
  private metrics: Map<string, TimeSeriesPoint[]>;
  private events: Map<string, ScalingEvent>;
  private lastScaleTime: Map<string, Date>;
  private activeScaling: Set<string>;
  private isRunning: boolean;

  constructor(config: AutoScalingEngineConfig) {
    super();
    this.config = config;
    this.policies = new Map();
    this.metrics = new Map();
    this.events = new Map();
    this.lastScaleTime = new Map();
    this.activeScaling = new Set();
    this.isRunning = false;

    this.initializePolicies();
  }

  /**
   * Initialize scaling policies
   */
  private initializePolicies(): void {
    for (const policy of this.config.policies) {
      this.policies.set(policy.id, policy);
      this.lastScaleTime.set(policy.id, new Date(0));
    }

    this.emit('policies-initialized', {
      count: this.policies.size,
      policies: Array.from(this.policies.keys())
    });
  }

  /**
   * Start the auto-scaling engine
   */
  async start(): Promise<void> {
    if (this.isRunning) {
      throw new Error('Auto-scaling engine already running');
    }

    this.isRunning = true;
    this.emit('started');

    // Start evaluation loop
    this.startEvaluationLoop();

    // Start metrics cleanup
    this.startMetricsCleanup();
  }

  /**
   * Stop the auto-scaling engine
   */
  async stop(): Promise<void> {
    this.isRunning = false;
    this.emit('stopped');
  }

  /**
   * Add scaling policy
   */
  addPolicy(policy: ScalingPolicy): void {
    this.policies.set(policy.id, policy);
    this.lastScaleTime.set(policy.id, new Date(0));
    
    this.emit('policy-added', { policyId: policy.id });
  }

  /**
   * Remove scaling policy
   */
  removePolicy(policyId: string): void {
    this.policies.delete(policyId);
    this.lastScaleTime.delete(policyId);
    
    this.emit('policy-removed', { policyId });
  }

  /**
   * Update scaling policy
   */
  updatePolicy(policyId: string, updates: Partial<ScalingPolicy>): void {
    const policy = this.policies.get(policyId);
    if (policy) {
      Object.assign(policy, updates);
      this.emit('policy-updated', { policyId });
    }
  }

  /**
   * Record metric
   */
  recordMetric(metric: ScalingMetric): void {
    const key = `${metric.source}:${metric.name}`;
    
    if (!this.metrics.has(key)) {
      this.metrics.set(key, []);
    }

    const series = this.metrics.get(key)!;
    series.push({
      timestamp: metric.timestamp,
      value: metric.value
    });

    // Keep only recent data
    const cutoff = new Date(Date.now() - this.config.metricsRetention * 1000);
    const filtered = series.filter(p => p.timestamp >= cutoff);
    this.metrics.set(key, filtered);

    this.emit('metric-recorded', { metric });
  }

  /**
   * Evaluate scaling policies
   */
  async evaluate(): Promise<ScalingDecision[]> {
    const decisions: ScalingDecision[] = [];

    for (const policy of this.policies.values()) {
      if (!policy.enabled) continue;

      // Check cooldown
      const lastScale = this.lastScaleTime.get(policy.id);
      if (lastScale) {
        const timeSinceLastScale = (Date.now() - lastScale.getTime()) / 1000;
        if (timeSinceLastScale < policy.cooldownPeriod) {
          continue;
        }
      }

      // Check if already scaling
      if (this.activeScaling.has(policy.id)) {
        continue;
      }

      // Evaluate triggers
      for (const trigger of policy.triggers) {
        if (!trigger.enabled) continue;

        const decision = await this.evaluateTrigger(policy, trigger);
        if (decision) {
          decisions.push(decision);
          break; // Only one decision per policy per evaluation
        }
      }
    }

    return decisions;
  }

  /**
   * Execute scaling decision
   */
  async executeScaling(decision: ScalingDecision): Promise<ScalingEvent> {
    const policy = this.policies.get(decision.policyId);
    if (!policy) {
      throw new Error(`Policy not found: ${decision.policyId}`);
    }

    // Check concurrent scaling limit
    if (this.activeScaling.size >= this.config.maxConcurrentScaling) {
      throw new Error('Maximum concurrent scaling operations reached');
    }

    const event: ScalingEvent = {
      id: `scale-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      policyId: decision.policyId,
      decision,
      startTime: new Date(),
      status: 'pending',
      metadata: {}
    };

    this.events.set(event.id, event);
    this.activeScaling.add(decision.policyId);

    try {
      event.status = 'in-progress';
      this.emit('scaling-started', { event });

      // Perform scaling (simplified - in production would call actual scaling API)
      await this.performScaling(policy, decision);

      // Update policy desired size
      policy.desiredSize = decision.targetSize;
      this.lastScaleTime.set(decision.policyId, new Date());

      event.status = 'completed';
      event.endTime = new Date();
      
      this.emit('scaling-completed', { event });

    } catch (error) {
      event.status = 'failed';
      event.endTime = new Date();
      event.error = error instanceof Error ? error.message : 'Unknown error';
      
      this.emit('scaling-failed', { event, error });
      
      throw error;
    } finally {
      this.activeScaling.delete(decision.policyId);
    }

    return event;
  }

  /**
   * Get scaling history
   */
  getScalingHistory(policyId?: string): ScalingEvent[] {
    const events = Array.from(this.events.values());
    
    if (policyId) {
      return events.filter(e => e.policyId === policyId);
    }
    
    return events;
  }

  /**
   * Get policy metrics
   */
  getPolicyMetrics(policyId: string): TimeSeriesPoint[] {
    const policy = this.policies.get(policyId);
    if (!policy) return [];

    const key = `${policy.resourceType}:${policy.id}`;
    return this.metrics.get(key) || [];
  }

  /**
   * Predict future metric value
   */
  async predictMetric(
    metricName: string,
    predictionWindow: number
  ): Promise<{ value: number; confidence: number }> {
    const series = this.metrics.get(metricName);
    if (!series || series.length < 10) {
      return { value: 0, confidence: 0 };
    }

    // Use appropriate prediction model
    const model = this.selectPredictionModel(metricName);
    
    switch (model.type) {
      case 'linear':
        return this.predictLinear(series, predictionWindow);
      
      case 'exponential':
        return this.predictExponential(series, predictionWindow);
      
      case 'seasonal':
        return this.predictSeasonal(series, predictionWindow);
      
      default:
        return this.predictLinear(series, predictionWindow);
    }
  }

  /**
   * Evaluate trigger
   */
  private async evaluateTrigger(
    policy: ScalingPolicy,
    trigger: ScalingTrigger
  ): Promise<ScalingDecision | null> {
    switch (trigger.type) {
      case TriggerType.METRIC:
        return this.evaluateMetricTrigger(policy, trigger);
      
      case TriggerType.SCHEDULE:
        return this.evaluateScheduleTrigger(policy, trigger);
      
      case TriggerType.EVENT:
        return this.evaluateEventTrigger(policy, trigger);
      
      case TriggerType.PREDICTIVE:
        return this.evaluatePredictiveTrigger(policy, trigger);
      
      case TriggerType.CUSTOM:
        return this.evaluateCustomTrigger(policy, trigger);
      
      default:
        return null;
    }
  }

  /**
   * Evaluate metric trigger
   */
  private evaluateMetricTrigger(
    policy: ScalingPolicy,
    trigger: MetricTrigger
  ): ScalingDecision | null {
    const key = `${policy.resourceType}:${trigger.metricName}`;
    const series = this.metrics.get(key);
    
    if (!series || series.length === 0) {
      return null;
    }

    // Check if metric exceeds threshold for duration
    const now = Date.now();
    const durationMs = trigger.duration * 1000;
    const recentPoints = series.filter(
      p => now - p.timestamp.getTime() <= durationMs
    );

    if (recentPoints.length === 0) {
      return null;
    }

    const avgValue = recentPoints.reduce((sum, p) => sum + p.value, 0) / recentPoints.length;
    
    const triggered = this.compareMetric(avgValue, trigger.operator, trigger.threshold);
    
    if (!triggered) {
      return null;
    }

    // Calculate target size
    const currentSize = policy.desiredSize;
    let targetSize: number;
    
    if (trigger.direction === ScalingDirection.UP) {
      targetSize = Math.min(currentSize + trigger.amount, policy.maxSize);
    } else {
      targetSize = Math.max(currentSize - trigger.amount, policy.minSize);
    }

    if (targetSize === currentSize) {
      return null; // No change needed
    }

    return {
      policyId: policy.id,
      triggerId: trigger.id,
      direction: trigger.direction,
      currentSize,
      targetSize,
      amount: Math.abs(targetSize - currentSize),
      reason: `Metric ${trigger.metricName} ${trigger.operator} ${trigger.threshold}`,
      confidence: 1.0,
      timestamp: new Date()
    };
  }

  /**
   * Evaluate schedule trigger
   */
  private evaluateScheduleTrigger(
    policy: ScalingPolicy,
    trigger: ScheduleTrigger
  ): ScalingDecision | null {
    // Simplified - in production would use proper cron parser
    // For now, just return null
    return null;
  }

  /**
   * Evaluate event trigger
   */
  private evaluateEventTrigger(
    policy: ScalingPolicy,
    trigger: EventTrigger
  ): ScalingDecision | null {
    // Event-based triggers are evaluated when events are received
    return null;
  }

  /**
   * Evaluate predictive trigger
   */
  private async evaluatePredictiveTrigger(
    policy: ScalingPolicy,
    trigger: PredictiveTrigger
  ): Promise<ScalingDecision | null> {
    if (!this.config.enablePredictive) {
      return null;
    }

    const prediction = await this.predictMetric(
      trigger.metricName,
      trigger.predictionWindow
    );

    if (prediction.confidence < trigger.confidence) {
      return null;
    }

    // Determine if scaling is needed based on prediction
    const currentSize = policy.desiredSize;
    const predictedLoad = prediction.value;
    
    // Simple heuristic: scale if predicted load > 80% or < 20%
    let targetSize = currentSize;
    let direction = ScalingDirection.NONE;

    if (predictedLoad > 0.8) {
      targetSize = Math.min(Math.ceil(currentSize * 1.5), policy.maxSize);
      direction = ScalingDirection.UP;
    } else if (predictedLoad < 0.2) {
      targetSize = Math.max(Math.floor(currentSize * 0.7), policy.minSize);
      direction = ScalingDirection.DOWN;
    }

    if (targetSize === currentSize) {
      return null;
    }

    return {
      policyId: policy.id,
      triggerId: trigger.id,
      direction,
      currentSize,
      targetSize,
      amount: Math.abs(targetSize - currentSize),
      reason: `Predicted load: ${(predictedLoad * 100).toFixed(1)}%`,
      confidence: prediction.confidence,
      timestamp: new Date()
    };
  }

  /**
   * Evaluate custom trigger
   */
  private evaluateCustomTrigger(
    policy: ScalingPolicy,
    trigger: CustomTrigger
  ): ScalingDecision | null {
    const allMetrics: ScalingMetric[] = [];
    
    for (const [key, series] of this.metrics.entries()) {
      if (series.length > 0) {
        const latest = series[series.length - 1];
        const [source, name] = key.split(':');
        allMetrics.push({
          name,
          value: latest.value,
          unit: '',
          timestamp: latest.timestamp,
          source
        });
      }
    }

    return trigger.evaluate(allMetrics);
  }

  /**
   * Compare metric value
   */
  private compareMetric(
    value: number,
    operator: ComparisonOperator,
    threshold: number
  ): boolean {
    switch (operator) {
      case ComparisonOperator.GREATER_THAN:
        return value > threshold;
      case ComparisonOperator.GREATER_THAN_OR_EQUAL:
        return value >= threshold;
      case ComparisonOperator.LESS_THAN:
        return value < threshold;
      case ComparisonOperator.LESS_THAN_OR_EQUAL:
        return value <= threshold;
      case ComparisonOperator.EQUAL:
        return value === threshold;
      case ComparisonOperator.NOT_EQUAL:
        return value !== threshold;
      default:
        return false;
    }
  }

  /**
   * Perform scaling operation
   */
  private async performScaling(
    policy: ScalingPolicy,
    decision: ScalingDecision
  ): Promise<void> {
    // Simplified - in production would call actual scaling API
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    this.emit('resource-scaled', {
      policyId: policy.id,
      resourceType: policy.resourceType,
      direction: decision.direction,
      amount: decision.amount,
      newSize: decision.targetSize
    });
  }

  /**
   * Select prediction model
   */
  private selectPredictionModel(metricName: string): PredictionModel {
    // Select best model based on accuracy
    const models = this.config.predictionModels.filter(
      m => m.accuracy > 0.8
    );
    
    if (models.length === 0) {
      return {
        name: 'default',
        type: 'linear',
        accuracy: 0.7,
        parameters: {}
      };
    }

    return models.reduce((best, current) =>
      current.accuracy > best.accuracy ? current : best
    );
  }

  /**
   * Linear prediction
   */
  private predictLinear(
    series: TimeSeriesPoint[],
    predictionWindow: number
  ): { value: number; confidence: number } {
    if (series.length < 2) {
      return { value: series[0]?.value || 0, confidence: 0.5 };
    }

    // Simple linear regression
    const n = series.length;
    const x = series.map((_, i) => i);
    const y = series.map(p => p.value);

    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = y.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
    const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    const predictedValue = slope * (n + predictionWindow / 60) + intercept;
    
    return {
      value: Math.max(0, predictedValue),
      confidence: 0.85
    };
  }

  /**
   * Exponential prediction
   */
  private predictExponential(
    series: TimeSeriesPoint[],
    predictionWindow: number
  ): { value: number; confidence: number } {
    // Simplified exponential smoothing
    const alpha = 0.3;
    let smoothed = series[0].value;

    for (let i = 1; i < series.length; i++) {
      smoothed = alpha * series[i].value + (1 - alpha) * smoothed;
    }

    return {
      value: smoothed,
      confidence: 0.80
    };
  }

  /**
   * Seasonal prediction
   */
  private predictSeasonal(
    series: TimeSeriesPoint[],
    predictionWindow: number
  ): { value: number; confidence: number } {
    // Simplified - use average of same time period
    const period = 24; // 24 hours
    const index = series.length % period;
    
    const seasonalValues = series.filter((_, i) => i % period === index);
    const avgValue = seasonalValues.reduce((sum, p) => sum + p.value, 0) / seasonalValues.length;

    return {
      value: avgValue,
      confidence: 0.75
    };
  }

  /**
   * Start evaluation loop
   */
  private startEvaluationLoop(): void {
    setInterval(async () => {
      if (!this.isRunning) return;

      try {
        const decisions = await this.evaluate();
        
        for (const decision of decisions) {
          try {
            await this.executeScaling(decision);
          } catch (error) {
            this.emit('scaling-error', {
              decision,
              error: error instanceof Error ? error.message : 'Unknown error'
            });
          }
        }
      } catch (error) {
        this.emit('evaluation-error', {
          error: error instanceof Error ? error.message : 'Unknown error'
        });
      }
    }, this.config.evaluationInterval * 1000);
  }

  /**
   * Start metrics cleanup
   */
  private startMetricsCleanup(): void {
    setInterval(() => {
      const cutoff = new Date(Date.now() - this.config.metricsRetention * 1000);
      
      for (const [key, series] of this.metrics.entries()) {
        const filtered = series.filter(p => p.timestamp >= cutoff);
        this.metrics.set(key, filtered);
      }
    }, 300000); // Cleanup every 5 minutes
  }
}

/**
 * Create auto-scaling engine with default configuration
 */
export function createAutoScalingEngine(
  customConfig?: Partial<AutoScalingEngineConfig>
): AutoScalingEngine {
  const defaultConfig: AutoScalingEngineConfig = {
    policies: [],
    enablePredictive: true,
    predictionModels: [
      {
        name: 'linear',
        type: 'linear',
        accuracy: 0.85,
        parameters: {}
      },
      {
        name: 'exponential',
        type: 'exponential',
        accuracy: 0.80,
        parameters: { alpha: 0.3 }
      }
    ],
    evaluationInterval: 60,
    metricsRetention: 86400, // 24 hours
    maxConcurrentScaling: 10
  };

  const config = { ...defaultConfig, ...customConfig };
  return new AutoScalingEngine(config);
}