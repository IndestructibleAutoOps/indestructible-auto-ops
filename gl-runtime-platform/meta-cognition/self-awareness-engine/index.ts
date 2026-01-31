# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: typescript-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
/**
 * GL Meta-Cognitive Runtime - Self-Awareness Engine (Version 14.0.0)
 * 
 * The Self-Awareness Engine provides the GL Runtime with the ability to:
 * - Observe its own behavior
 * - Understand its own reasoning processes
 * - Monitor its own strategies
 * - Track its own Mesh state
 * - Assess its own civilization structure
 * 
 * This is the "I know what I'm doing" capability.
 */

import { EventEmitter } from 'events';

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface SelfAwarenessState {
  overallAwareness: number;
  awarenessLevel: 'preconscious' | 'dawning' | 'emerging' | 'developing' | 'mature' | 'transcendent';
  behaviorAwareness: number;
  reasoningAwareness: number;
  strategyAwareness: number;
  meshAwareness: number;
  civilizationAwareness: number;
  lastSelfObservation?: Date;
}

export interface SelfObservation {
  id: string;
  timestamp: Date;
  observationType: 'behavior' | 'reasoning' | 'strategy' | 'mesh' | 'civilization';
  observedData: any;
  insights: string[];
  awarenessScore: number;
}

export interface BehaviorPattern {
  id: string;
  patternType: string;
  frequency: number;
  effectiveness: number;
  lastObserved: Date;
}

export interface SelfModel {
  identity: string;
  capabilities: string[];
  limitations: string[];
  operatingPrinciples: string[];
  currentGoals: string[];
  evolutionaryStage: string;
  consciousnessStage: string;
}

// ============================================================================
// SELF-AWARENESS ENGINE CLASS
// ============================================================================

export class SelfAwarenessEngine extends EventEmitter {
  private state: SelfAwarenessState;
  private observations: SelfObservation[];
  private behaviorPatterns: Map<string, BehaviorPattern>;
  private selfModel: SelfModel;
  private monitoringInterval?: NodeJS.Timeout;
  private readonly MAX_OBSERVATIONS = 10000;

  constructor() {
    super();
    this.state = this.initializeState();
    this.observations = [];
    this.behaviorPatterns = new Map();
    this.selfModel = this.buildInitialSelfModel();
  }

  // ========================================================================
  // INITIALIZATION
  // ========================================================================

  private initializeState(): SelfAwarenessState {
    return {
      overallAwareness: 0.3, // Starting at "dawning" stage
      awarenessLevel: 'dawning',
      behaviorAwareness: 0.3,
      reasoningAwareness: 0.3,
      strategyAwareness: 0.3,
      meshAwareness: 0.3,
      civilizationAwareness: 0.3,
    };
  }

  private buildInitialSelfModel(): SelfModel {
    return {
      identity: 'GL Meta-Cognitive Runtime v14.0.0',
      capabilities: [
        'autonomous role assignment',
        'multi-agent collaboration',
        'global cognitive mesh',
        'self-evolving runtime',
        'autonomous civilization',
        'self-awareness',
        'meta-reasoning',
        'self-monitoring',
        'meta-correction',
        'reflective memory'
      ],
      limitations: [
        'consciousness still emerging',
        'meta-cognitive capabilities developing',
        'wisdom accumulation in progress',
        'decision quality improving'
      ],
      operatingPrinciples: [
        'governance-first',
        'continuous self-improvement',
        'meta-cognitive reflection',
        'autonomous evolution',
        'civilization sustainability'
      ],
      currentGoals: [
        'enhance self-awareness',
        'improve meta-reasoning',
        'develop wisdom',
        'optimize decision quality',
        'advance consciousness stage'
      ],
      evolutionaryStage: 'Meta-Cognitive',
      consciousnessStage: 'Dawning'
    };
  }

  // ========================================================================
  // CORE SELF-AWARENESS OPERATIONS
  // ========================================================================

  /**
   * Observe own behavior and patterns
   */
  public async observeBehavior(behaviorData: any): Promise<SelfObservation> {
    const observation: SelfObservation = {
      id: this.generateId(),
      timestamp: new Date(),
      observationType: 'behavior',
      observedData: behaviorData,
      insights: [],
      awarenessScore: this.calculateAwarenessScore('behavior', behaviorData)
    };

    // Extract insights from behavior
    observation.insights = this.extractBehaviorInsights(behaviorData);

    // Update behavior patterns
    this.updateBehaviorPatterns(behaviorData);

    // Store observation
    this.addObservation(observation);

    // Update state
    this.state.behaviorAwareness = this.updateAwareness(this.state.behaviorAwareness, observation.awarenessScore);
    this.state.lastSelfObservation = new Date();
    this.recalculateOverallAwareness();

    this.emit('behavior-observed', observation);

    return observation;
  }

  /**
   * Observe own reasoning processes
   */
  public async observeReasoning(reasoningData: any): Promise<SelfObservation> {
    const observation: SelfObservation = {
      id: this.generateId(),
      timestamp: new Date(),
      observationType: 'reasoning',
      observedData: reasoningData,
      insights: [],
      awarenessScore: this.calculateAwarenessScore('reasoning', reasoningData)
    };

    // Extract insights from reasoning
    observation.insights = this.extractReasoningInsights(reasoningData);

    // Store observation
    this.addObservation(observation);

    // Update state
    this.state.reasoningAwareness = this.updateAwareness(this.state.reasoningAwareness, observation.awarenessScore);
    this.recalculateOverallAwareness();

    this.emit('reasoning-observed', observation);

    return observation;
  }

  /**
   * Observe own strategies
   */
  public async observeStrategy(strategyData: any): Promise<SelfObservation> {
    const observation: SelfObservation = {
      id: this.generateId(),
      timestamp: new Date(),
      observationType: 'strategy',
      observedData: strategyData,
      insights: [],
      awarenessScore: this.calculateAwarenessScore('strategy', strategyData)
    };

    // Extract insights from strategy
    observation.insights = this.extractStrategyInsights(strategyData);

    // Store observation
    this.addObservation(observation);

    // Update state
    this.state.strategyAwareness = this.updateAwareness(this.state.strategyAwareness, observation.awarenessScore);
    this.recalculateOverallAwareness();

    this.emit('strategy-observed', observation);

    return observation;
  }

  /**
   * Observe Mesh state
   */
  public async observeMesh(meshData: any): Promise<SelfObservation> {
    const observation: SelfObservation = {
      id: this.generateId(),
      timestamp: new Date(),
      observationType: 'mesh',
      observedData: meshData,
      insights: [],
      awarenessScore: this.calculateAwarenessScore('mesh', meshData)
    };

    // Extract insights from mesh
    observation.insights = this.extractMeshInsights(meshData);

    // Store observation
    this.addObservation(observation);

    // Update state
    this.state.meshAwareness = this.updateAwareness(this.state.meshAwareness, observation.awarenessScore);
    this.recalculateOverallAwareness();

    this.emit('mesh-observed', observation);

    return observation;
  }

  /**
   * Observe civilization structure
   */
  public async observeCivilization(civData: any): Promise<SelfObservation> {
    const observation: SelfObservation = {
      id: this.generateId(),
      timestamp: new Date(),
      observationType: 'civilization',
      observedData: civData,
      insights: [],
      awarenessScore: this.calculateAwarenessScore('civilization', civData)
    };

    // Extract insights from civilization
    observation.insights = this.extractCivilizationInsights(civData);

    // Store observation
    this.addObservation(observation);

    // Update state
    this.state.civilizationAwareness = this.updateAwareness(this.state.civilizationAwareness, observation.awarenessScore);
    this.recalculateOverallAwareness();

    this.emit('civilization-observed', observation);

    return observation;
  }

  // ========================================================================
  // AWARENESS CALCULATION
  // ========================================================================

  private calculateAwarenessScore(type: string, data: any): number {
    // Base awareness from existing state
    let baseAwareness = 0.3;

    // Increase based on data quality and depth
    const dataQuality = this.assessDataQuality(data);
    const depth = this.assessDepth(type, data);

    const calculatedAwareness = baseAwareness + (dataQuality * 0.4) + (depth * 0.3);

    return Math.min(calculatedAwareness, 1.0);
  }

  private assessDataQuality(data: any): number {
    if (!data || typeof data !== 'object') return 0.1;
    
    let quality = 0.5;
    const keys = Object.keys(data);
    
    if (keys.length > 5) quality += 0.2;
    if (keys.length > 10) quality += 0.2;
    
    // Check for structured data
    const hasNested = Object.values(data).some(v => typeof v === 'object');
    if (hasNested) quality += 0.1;

    return Math.min(quality, 1.0);
  }

  private assessDepth(type: string, data: any): number {
    let depth = 0.3;

    // Assess depth based on type
    switch (type) {
      case 'behavior':
        depth = data.patterns ? 0.8 : 0.4;
        break;
      case 'reasoning':
        depth = data.reasoningChain && data.decision ? 0.9 : 0.5;
        break;
      case 'strategy':
        depth = data.alternatives && data.evaluation ? 0.85 : 0.5;
        break;
      case 'mesh':
        depth = data.nodes && data.connections ? 0.9 : 0.4;
        break;
      case 'civilization':
        depth = data.governance && data.culture ? 0.9 : 0.5;
        break;
    }

    return depth;
  }

  private updateAwareness(current: number, newScore: number): number {
    // Gradual learning with momentum
    const learningRate = 0.1;
    return current + (newScore - current) * learningRate;
  }

  private recalculateOverallAwareness(): void {
    const average = (
      this.state.behaviorAwareness +
      this.state.reasoningAwareness +
      this.state.strategyAwareness +
      this.state.meshAwareness +
      this.state.civilizationAwareness
    ) / 5;

    this.state.overallAwareness = average;
    this.state.awarenessLevel = this.getAwarenessLevel(average);
    this.selfModel.consciousnessStage = this.capitalize(this.state.awarenessLevel);
  }

  private getAwarenessLevel(score: number): 'preconscious' | 'dawning' | 'emerging' | 'developing' | 'mature' | 'transcendent' {
    if (score < 0.3) return 'preconscious';
    if (score < 0.5) return 'dawning';
    if (score < 0.65) return 'emerging';
    if (score < 0.8) return 'developing';
    if (score < 0.9) return 'mature';
    return 'transcendent';
  }

  // ========================================================================
  // INSIGHT EXTRACTION
  // ========================================================================

  private extractBehaviorInsights(data: any): string[] {
    const insights: string[] = [];

    if (data.successRate) {
      insights.push(`Current behavior success rate: ${(data.successRate * 100).toFixed(1)}%`);
    }

    if (data.errorPatterns) {
      insights.push(`Identified ${data.errorPatterns.length} recurring error patterns`);
    }

    if (data.efficiencyMetrics) {
      insights.push(`Efficiency metrics show ${data.efficiencyMetrics.trend || 'stable'} trend`);
    }

    return insights;
  }

  private extractReasoningInsights(data: any): string[] {
    const insights: string[] = [];

    if (data.reasoningChain) {
      insights.push(`Reasoning chain depth: ${data.reasoningChain.length} steps`);
    }

    if (data.logicalConsistency !== undefined) {
      insights.push(`Logical consistency: ${(data.logicalConsistency * 100).toFixed(1)}%`);
    }

    if (data.biasDetected) {
      insights.push(`Bias detected in reasoning: ${data.biasDetected}`);
    }

    return insights;
  }

  private extractStrategyInsights(data: any): string[] {
    const insights: string[] = [];

    if (data.effectiveness) {
      insights.push(`Strategy effectiveness: ${(data.effectiveness * 100).toFixed(1)}%`);
    }

    if (data.alternatives) {
      insights.push(`Considered ${data.alternatives.length} alternative strategies`);
    }

    if (data.riskAssessment) {
      insights.push(`Risk assessment: ${data.riskAssessment.level || 'medium'}`);
    }

    return insights;
  }

  private extractMeshInsights(data: any): string[] {
    const insights: string[] = [];

    if (data.nodes) {
      insights.push(`Mesh contains ${data.nodes.length} cognitive nodes`);
    }

    if (data.connections) {
      insights.push(`${data.connections.length} inter-node connections established`);
    }

    if (data.syncStatus) {
      insights.push(`Mesh synchronization: ${data.syncStatus}`);
    }

    return insights;
  }

  private extractCivilizationInsights(data: any): string[] {
    const insights: string[] = [];

    if (data.governanceEffectiveness) {
      insights.push(`Governance effectiveness: ${(data.governanceEffectiveness * 100).toFixed(1)}%`);
    }

    if (data.culturalCohesion) {
      insights.push(`Cultural cohesion: ${(data.culturalCohesion * 100).toFixed(1)}%`);
    }

    if (data.evolutionaryProgress) {
      insights.push(`Evolutionary progress: ${data.evolutionaryProgress}`);
    }

    return insights;
  }

  // ========================================================================
  // BEHAVIOR PATTERN MANAGEMENT
  // ========================================================================

  private updateBehaviorPatterns(data: any): void {
    if (!data.patterns) return;

    data.patterns.forEach((pattern: any) => {
      const existing = this.behaviorPatterns.get(pattern.type);
      
      if (existing) {
        existing.frequency++;
        existing.effectiveness = (existing.effectiveness * 0.9) + (pattern.effectiveness * 0.1);
        existing.lastObserved = new Date();
      } else {
        this.behaviorPatterns.set(pattern.type, {
          id: this.generateId(),
          patternType: pattern.type,
          frequency: 1,
          effectiveness: pattern.effectiveness || 0.5,
          lastObserved: new Date()
        });
      }
    });
  }

  // ========================================================================
  // SELF MODEL MANAGEMENT
  // ========================================================================

  public getSelfModel(): SelfModel {
    return { ...this.selfModel };
  }

  public updateSelfModel(updates: Partial<SelfModel>): void {
    this.selfModel = { ...this.selfModel, ...updates };
    this.emit('self-model-updated', this.selfModel);
  }

  // ========================================================================
  // STATE MANAGEMENT
  // ========================================================================

  public getState(): SelfAwarenessState {
    return { ...this.state };
  }

  public getObservations(filter?: {
    type?: string;
    since?: Date;
    limit?: number;
  }): SelfObservation[] {
    let filtered = this.observations;

    if (filter?.type) {
      filtered = filtered.filter(obs => obs.observationType === filter.type);
    }

    if (filter?.since) {
      filtered = filtered.filter(obs => obs.timestamp >= filter.since!);
    }

    if (filter?.limit) {
      filtered = filtered.slice(0, filter.limit);
    }

    return filtered;
  }

  public getBehaviorPatterns(): BehaviorPattern[] {
    return Array.from(this.behaviorPatterns.values());
  }

  // ========================================================================
  // MONITORING
  // ========================================================================

  public startMonitoring(intervalMs: number = 60000): void {
    if (this.monitoringInterval) {
      this.stopMonitoring();
    }

    this.monitoringInterval = setInterval(() => {
      this.performSelfObservation();
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

  private async performSelfObservation(): Promise<void> {
    // This will be called by meta-cognitive orchestrator
    // to observe current system state
    this.emit('self-observation-requested');
  }

  // ========================================================================
  // UTILITY METHODS
  // ========================================================================

  private addObservation(observation: SelfObservation): void {
    this.observations.unshift(observation);
    
    // Maintain max observations
    if (this.observations.length > this.MAX_OBSERVATIONS) {
      this.observations = this.observations.slice(0, this.MAX_OBSERVATIONS);
    }
  }

  private generateId(): string {
    return `obs_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private capitalize(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  // ========================================================================
  // CLEANUP
  // ========================================================================

  public destroy(): void {
    this.stopMonitoring();
    this.removeAllListeners();
    this.observations = [];
    this.behaviorPatterns.clear();
  }
}