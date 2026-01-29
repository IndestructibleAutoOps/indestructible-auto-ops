/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
/**
 * GL Runtime Platform v14.0.0
 * Module: Meta-Cognitive Monitoring System
 * 
 * The meta-cognitive monitoring system enables the civilization to monitor
 * its own cognitive processes, track decision quality, and maintain awareness
 * of its cognitive state.
 * 
 * Key Capabilities:
 * - Thought process tracking
 * - Decision quality monitoring
 * - Cognitive state awareness
 * - Attention monitoring
 * - Memory retrieval tracking
 * - Learning process monitoring
 */

import { EventEmitter } from 'events';

// ============================================================================
// Core Types
// ============================================================================

export interface ThoughtProcess {
  id: string;
  type: 'analytical' | 'creative' | 'strategic' | 'operational' | 'reflective';
  description: string;
  startTime: number;
  endTime?: number;
  duration?: number;
  complexity: number; // 0-1
  effectiveness: number; // 0-1
  resources: {
    compute: number;
    memory: number;
    time: number;
  };
  outcomes: string[];
  insights: string[];
}

export interface DecisionEvent {
  id: string;
  type: 'strategic' | 'tactical' | 'operational' | 'adaptive';
  description: string;
  context: Record<string, any>;
  alternatives: string[];
  chosen: string;
  reasoning: string;
  confidence: number; // 0-1
  outcome?: 'successful' | 'partial' | 'failed';
  quality?: number; // 0-1, assessed after outcome
  timestamp: number;
}

export interface CognitiveState {
  id: string;
  timestamp: number;
  attentionLevel: number; // 0-1
  focusAreas: string[];
  workingMemoryLoad: number; // 0-1
  cognitiveLoad: number; // 0-1
  mentalEnergy: number; // 0-1
  clarity: number; // 0-1
  stress: number; // 0-1
  engagement: number; // 0-1
}

export interface MetaCognitiveMetric {
  id: string;
  name: string;
  description: string;
  category: 'performance' | 'quality' | 'efficiency' | 'learning' | 'adaptability';
  value: number; // 0-1
  trend: 'improving' | 'stable' | 'declining';
  history: { timestamp: number; value: number }[];
  target: number; // 0-1
  threshold: number; // 0-1, alert threshold
}

export interface AwarenessEvent {
  id: string;
  type: 'self_awareness' | 'process_awareness' | 'knowledge_awareness' | 'limitation_awareness';
  description: string;
  insight: string;
  impact: number; // -1 to 1
  timestamp: number;
  actionable: boolean;
}

export interface MonitoringState {
  thoughtProcesses: ThoughtProcess[];
  decisionEvents: DecisionEvent[];
  cognitiveStates: CognitiveState[];
  metrics: MetaCognitiveMetric[];
  awarenessEvents: AwarenessEvent[];
  overallCognitiveHealth: number; // 0-1
  metaCognitiveMaturity: number; // 0-1
}

// ============================================================================
// Main Meta-Cognitive Monitoring System Class
// ============================================================================

export class MetaCognitiveMonitoringSystem extends EventEmitter {
  private thoughtProcesses: Map<string, ThoughtProcess> = new Map();
  private decisionEvents: Map<string, DecisionEvent> = new Map();
  private cognitiveStates: CognitiveState[] = [];
  private metrics: Map<string, MetaCognitiveMetric> = new Map();
  private awarenessEvents: AwarenessEvent[] = [];
  
  // Configuration
  private readonly MAX_THOUGHT_PROCESSES = 100;
  private readonly MAX_DECISION_EVENTS = 200;
  private readonly MAX_COGNITIVE_STATES = 1000;
  private readonly MAX_AWARENESS_EVENTS = 200;
  private readonly MONITORING_INTERVAL = 10000; // 10 seconds
  
  // Current State
  private currentCognitiveState!: CognitiveState;
  private overallCognitiveHealth: number = 0.5;
  private metaCognitiveMaturity: number = 0.5;
  private monitoringCycles: number = 0;

  constructor() {
    super();
    this.initializeMonitoring();
  }

  // ==========================================================================
  // Initialization
  // ==========================================================================

  private initializeMonitoring(): void {
    // Initialize metrics
    this.initializeMetrics();
    
    // Set initial cognitive state
    this.currentCognitiveState = this.createCognitiveState();
    
    // Start monitoring cycle
    this.startMonitoringCycle();
    
    this.emit('monitoring_initialized', {
      metrics: this.metrics.size,
      cognitiveHealth: this.overallCognitiveHealth,
      maturity: this.metaCognitiveMaturity
    });
  }

  private initializeMetrics(): void {
    const coreMetrics: Omit<MetaCognitiveMetric, 'id' | 'history'>[] = [
      {
        name: 'Decision Quality',
        description: 'Average quality of decisions made',
        category: 'quality',
        value: 0.5,
        trend: 'stable',
        target: 0.8,
        threshold: 0.5
      },
      {
        name: 'Thought Efficiency',
        description: 'Efficiency of thought processes',
        category: 'efficiency',
        value: 0.5,
        trend: 'stable',
        target: 0.85,
        threshold: 0.6
      },
      {
        name: 'Learning Rate',
        description: 'Rate of learning from experiences',
        category: 'learning',
        value: 0.5,
        trend: 'stable',
        target: 0.75,
        threshold: 0.5
      },
      {
        name: 'Adaptive Capacity',
        description: 'Ability to adapt to new situations',
        category: 'adaptability',
        value: 0.5,
        trend: 'stable',
        target: 0.8,
        threshold: 0.5
      },
      {
        name: 'Cognitive Performance',
        description: 'Overall cognitive performance',
        category: 'performance',
        value: 0.5,
        trend: 'stable',
        target: 0.85,
        threshold: 0.6
      }
    ];

    coreMetrics.forEach(metric => {
      this.metrics.set(
        `metric_${metric.name.toLowerCase().replace(/\s+/g, '_')}`,
        { ...metric, id: `metric_${metric.name.toLowerCase().replace(/\s+/g, '_')}`, history: [] }
      );
    });
  }

  // ==========================================================================
  // Thought Process Tracking
  // ==========================================================================

  public startThoughtProcess(thoughtData: {
    type: ThoughtProcess['type'];
    description: string;
    complexity: number;
  }): string {
    if (this.thoughtProcesses.size >= this.MAX_THOUGHT_PROCESSES) {
      this.pruneThoughtProcesses();
    }

    const thought: ThoughtProcess = {
      ...thoughtData,
      id: `thought_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      startTime: Date.now(),
      resources: { compute: 0, memory: 0, time: 0 },
      outcomes: [],
      insights: [],
      effectiveness: 0.5
    };

    this.thoughtProcesses.set(thought.id, thought);
    this.emit('thought_started', thought);
    return thought.id;
  }

  public endThoughtProcess(thoughtId: string, outcomes: string[], insights: string[]): void {
    const thought = this.thoughtProcesses.get(thoughtId);
    if (!thought) return;

    thought.endTime = Date.now();
    thought.duration = thought.endTime - thought.startTime;
    thought.outcomes = outcomes;
    thought.insights = insights;
    thought.effectiveness = Math.min(1, 0.5 + (insights.length * 0.1));

    this.emit('thought_completed', thought);
  }

  private pruneThoughtProcesses(): void {
    const completedThoughts = Array.from(this.thoughtProcesses.values())
      .filter(t => t.endTime !== undefined)
      .sort((a, b) => (a.endTime || 0) - (b.endTime || 0));

    while (completedThoughts.length > this.MAX_THOUGHT_PROCESSES / 2 && this.thoughtProcesses.size >= this.MAX_THOUGHT_PROCESSES) {
      const toRemove = completedThoughts.shift();
      if (toRemove) {
        this.thoughtProcesses.delete(toRemove.id);
      }
    }
  }

  // ==========================================================================
  // Decision Event Tracking
  // ==========================================================================

  public recordDecision(decisionData: {
    type: DecisionEvent['type'];
    description: string;
    context: Record<string, any>;
    alternatives: string[];
    chosen: string;
    reasoning: string;
    confidence: number;
  }): string {
    if (this.decisionEvents.size >= this.MAX_DECISION_EVENTS) {
      this.pruneDecisionEvents();
    }

    const decision: DecisionEvent = {
      ...decisionData,
      id: `decision_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now()
    };

    this.decisionEvents.set(decision.id, decision);
    this.emit('decision_made', decision);
    return decision.id;
  }

  public assessDecision(decisionId: string, outcome: DecisionEvent['outcome']): void {
    const decision = this.decisionEvents.get(decisionId);
    if (!decision) return;

    decision.outcome = outcome;
    decision.quality = outcome === 'successful' ? decision.confidence :
                      outcome === 'partial' ? decision.confidence * 0.7 :
                      decision.confidence * 0.3;

    // Update decision quality metric
    this.updateMetric('Decision Quality', decision.quality);

    this.emit('decision_assessed', decision);
  }

  private pruneDecisionEvents(): void {
    const oldDecisions = Array.from(this.decisionEvents.values())
      .filter(d => d.outcome !== undefined && Date.now() - d.timestamp > 7 * 24 * 60 * 60 * 1000) // 7 days
      .sort((a, b) => a.timestamp - b.timestamp);

    while (oldDecisions.length > 0 && this.decisionEvents.size >= this.MAX_DECISION_EVENTS) {
      const toRemove = oldDecisions.shift();
      if (toRemove) {
        this.decisionEvents.delete(toRemove.id);
      }
    }
  }

  // ==========================================================================
  // Cognitive State Management
  // ==========================================================================

  private createCognitiveState(): CognitiveState {
    return {
      id: `state_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
      attentionLevel: 0.7 + Math.random() * 0.2,
      focusAreas: ['governance', 'evolution', 'expansion'],
      workingMemoryLoad: 0.4 + Math.random() * 0.3,
      cognitiveLoad: 0.5 + Math.random() * 0.2,
      mentalEnergy: 0.6 + Math.random() * 0.3,
      clarity: 0.6 + Math.random() * 0.3,
      stress: 0.1 + Math.random() * 0.2,
      engagement: 0.7 + Math.random() * 0.2
    };
  }

  private updateCognitiveState(): void {
    const now = Date.now();
    const prevState = this.currentCognitiveState;
    
    // Create new state based on previous state and current activity
    const activeThoughts = Array.from(this.thoughtProcesses.values()).filter(t => t.endTime === undefined).length;
    const activeDecisions = Array.from(this.decisionEvents.values()).filter(d => d.outcome === undefined).length;
    
    this.currentCognitiveState = {
      id: `state_${now}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: now,
      attentionLevel: Math.min(1, Math.max(0.2, prevState.attentionLevel + (Math.random() - 0.5) * 0.1)),
      focusAreas: this.determineFocusAreas(),
      workingMemoryLoad: Math.min(1, 0.3 + (activeThoughts * 0.1) + (activeDecisions * 0.15)),
      cognitiveLoad: Math.min(1, 0.4 + (activeThoughts * 0.1) + (activeDecisions * 0.1)),
      mentalEnergy: Math.max(0.3, Math.min(1, prevState.mentalEnergy + (Math.random() - 0.5) * 0.05)),
      clarity: Math.min(1, Math.max(0.3, prevState.clarity + (Math.random() - 0.5) * 0.08)),
      stress: Math.max(0, Math.min(1, prevState.stress + (Math.random() - 0.5) * 0.06)),
      engagement: Math.min(1, Math.max(0.3, prevState.engagement + (Math.random() - 0.5) * 0.07))
    };

    this.cognitiveStates.push(this.currentCognitiveState);

    // Prune old states
    if (this.cognitiveStates.length > this.MAX_COGNITIVE_STATES) {
      this.cognitiveStates = this.cognitiveStates.slice(-this.MAX_COGNITIVE_STATES);
    }

    this.emit('cognitive_state_updated', this.currentCognitiveState);
  }

  private determineFocusAreas(): string[] {
    const areas: string[] = ['governance'];
    
    if (this.thoughtProcesses.size > 5) areas.push('decision_making');
    if (this.decisionEvents.size > 10) areas.push('reflection');
    if (this.awarenessEvents.length > 5) areas.push('consciousness');
    
    return areas;
  }

  // ==========================================================================
  // Metric Management
  // ==========================================================================

  private updateMetric(metricName: string, newValue: number): void {
    const metric = Array.from(this.metrics.values()).find(m => m.name === metricName);
    if (!metric) return;

    const previousValue = metric.value;
    metric.value = newValue;
    metric.trend = newValue > previousValue ? 'improving' :
                   newValue < previousValue ? 'declining' : 'stable';
    metric.history.push({ timestamp: Date.now(), value: newValue });

    // Keep only last 100 history points
    if (metric.history.length > 100) {
      metric.history = metric.history.slice(-100);
    }

    // Check threshold
    if (metric.value < metric.threshold) {
      this.recordAwareness({
        type: 'limitation_awareness',
        description: `${metricName} below threshold`,
        insight: `${metricName} is at ${(metric.value * 100).toFixed(0)}%, below threshold of ${(metric.threshold * 100).toFixed(0)}%`,
        impact: -0.1,
        actionable: true
      });
    }
  }

  // ==========================================================================
  // Awareness Recording
  // ==========================================================================

  public recordAwareness(awarenessData: Omit<AwarenessEvent, 'id' | 'timestamp'>): string {
    if (this.awarenessEvents.length >= this.MAX_AWARENESS_EVENTS) {
      this.pruneAwarenessEvents();
    }

    const awareness: AwarenessEvent = {
      ...awarenessData,
      id: `awareness_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now()
    };

    this.awarenessEvents.push(awareness);
    this.emit('awareness_recorded', awareness);
    return awareness.id;
  }

  private pruneAwarenessEvents(): void {
    const oldAwareness = this.awarenessEvents
      .filter(e => Date.now() - e.timestamp > 30 * 24 * 60 * 60 * 1000) // 30 days
      .sort((a, b) => a.timestamp - b.timestamp);

    while (oldAwareness.length > 0 && this.awarenessEvents.length >= this.MAX_AWARENESS_EVENTS) {
      const toRemove = oldAwareness.shift();
      if (toRemove) {
        this.awarenessEvents = this.awarenessEvents.filter(e => e.id !== toRemove!.id);
      }
    }
  }

  // ==========================================================================
  // Monitoring Cycle
  // ==========================================================================

  private startMonitoringCycle(): void {
    setInterval(() => {
      this.monitoringCycles++;
      this.runMonitoringCycle();
    }, this.MONITORING_INTERVAL);
  }

  private runMonitoringCycle(): void {
    // Update cognitive state
    this.updateCognitiveState();

    // Calculate cognitive health
    this.calculateCognitiveHealth();

    // Calculate meta-cognitive maturity
    this.calculateMetaCognitiveMaturity();

    // Update metrics
    this.updateAllMetrics();

    // Check for patterns
    this.detectPatterns();

    this.emit('monitoring_cycle_completed', {
      cycle: this.monitoringCycles,
      cognitiveHealth: this.overallCognitiveHealth,
      maturity: this.metaCognitiveMaturity
    });
  }

  private calculateCognitiveHealth(): void {
    const avgAttentionLevel = this.cognitiveStates.length > 0
      ? this.cognitiveStates.slice(-10).reduce((sum, s) => sum + s.attentionLevel, 0) / Math.min(10, this.cognitiveStates.length)
      : 0.5;
    
    const avgClarity = this.cognitiveStates.length > 0
      ? this.cognitiveStates.slice(-10).reduce((sum, s) => sum + s.clarity, 0) / Math.min(10, this.cognitiveStates.length)
      : 0.5;
    
    const avgMentalEnergy = this.cognitiveStates.length > 0
      ? this.cognitiveStates.slice(-10).reduce((sum, s) => sum + s.mentalEnergy, 0) / Math.min(10, this.cognitiveStates.length)
      : 0.5;

    const avgStress = this.cognitiveStates.length > 0
      ? this.cognitiveStates.slice(-10).reduce((sum, s) => sum + s.stress, 0) / Math.min(10, this.cognitiveStates.length)
      : 0.5;

    this.overallCognitiveHealth = (
      avgAttentionLevel * 0.25 +
      avgClarity * 0.3 +
      avgMentalEnergy * 0.25 +
      (1 - avgStress) * 0.2
    );
  }

  private calculateMetaCognitiveMaturity(): void {
    const awarenessRate = this.awarenessEvents.length / Math.max(1, this.monitoringCycles);
    const decisionQuality = this.metrics.get('metric_decision_quality')?.value || 0.5;
    const thoughtEfficiency = this.metrics.get('metric_thought_efficiency')?.value || 0.5;
    const learningRate = this.metrics.get('metric_learning_rate')?.value || 0.5;

    this.metaCognitiveMaturity = (
      awarenessRate * 0.2 +
      decisionQuality * 0.3 +
      thoughtEfficiency * 0.2 +
      learningRate * 0.3
    );
  }

  private updateAllMetrics(): void {
    // Update thought efficiency
    const completedThoughts = Array.from(this.thoughtProcesses.values())
      .filter(t => t.endTime !== undefined);
    if (completedThoughts.length > 0) {
      const avgEffectiveness = completedThoughts
        .reduce((sum, t) => sum + t.effectiveness, 0) / completedThoughts.length;
      this.updateMetric('Thought Efficiency', avgEffectiveness);
    }

    // Update cognitive performance
    this.updateMetric('Cognitive Performance', this.overallCognitiveHealth);

    // Update adaptive capacity
    const recentDecisions = Array.from(this.decisionEvents.values())
      .filter(d => Date.now() - d.timestamp < 24 * 60 * 60 * 1000); // Last 24 hours
    if (recentDecisions.length > 0) {
      const avgConfidence = recentDecisions.reduce((sum, d) => sum + d.confidence, 0) / recentDecisions.length;
      this.updateMetric('Adaptive Capacity', avgConfidence);
    }
  }

  private detectPatterns(): void {
    // Detect stress patterns
    const recentStates = this.cognitiveStates.slice(-20);
    const avgStress = recentStates.reduce((sum, s) => sum + s.stress, 0) / recentStates.length;
    
    if (avgStress > 0.7) {
      this.recordAwareness({
        type: 'limitation_awareness',
        description: 'Elevated stress detected',
        insight: 'Cognitive stress is elevated, may affect decision quality',
        impact: -0.15,
        actionable: true
      });
    }

    // Detect low engagement
    const avgEngagement = recentStates.reduce((sum, s) => sum + s.engagement, 0) / recentStates.length;
    if (avgEngagement < 0.4) {
      this.recordAwareness({
        type: 'self_awareness',
        description: 'Low engagement detected',
        insight: 'Engagement levels are low, may need realignment of focus',
        impact: -0.1,
        actionable: true
      });
    }
  }

  // ==========================================================================
  // Public API
  // ==========================================================================

  public getState(): MonitoringState {
    return {
      thoughtProcesses: Array.from(this.thoughtProcesses.values()),
      decisionEvents: Array.from(this.decisionEvents.values()),
      cognitiveStates: this.cognitiveStates,
      metrics: Array.from(this.metrics.values()),
      awarenessEvents: this.awarenessEvents,
      overallCognitiveHealth: this.overallCognitiveHealth,
      metaCognitiveMaturity: this.metaCognitiveMaturity
    };
  }

  public getCognitiveState(): CognitiveState {
    return this.currentCognitiveState;
  }

  public getStatistics(): {
    thoughtProcesses: number;
    decisionEvents: number;
    cognitiveStates: number;
    metrics: number;
    awarenessEvents: number;
    cognitiveHealth: number;
    metaCognitiveMaturity: number;
    monitoringCycles: number;
  } {
    return {
      thoughtProcesses: this.thoughtProcesses.size,
      decisionEvents: this.decisionEvents.size,
      cognitiveStates: this.cognitiveStates.length,
      metrics: this.metrics.size,
      awarenessEvents: this.awarenessEvents.length,
      cognitiveHealth: this.overallCognitiveHealth,
      metaCognitiveMaturity: this.metaCognitiveMaturity,
      monitoringCycles: this.monitoringCycles
    };
  }
}