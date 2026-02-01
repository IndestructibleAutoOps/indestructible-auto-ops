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
 * GL Meta-Cognitive Runtime - Decision Optimizer (Version 14.0.0 Deep)
 * 
 * The Decision Optimizer provides advanced decision-making capabilities:
 * - Multi-criteria decision analysis
 * - Decision quality assessment
 * - Decision learning and optimization
 * - Decision prediction and simulation
 * - Decision traceability and auditability
 * 
 * This improves decision quality through continuous learning and optimization.
 */

import { EventEmitter } from 'events';

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface Decision {
  id: string;
  timestamp: Date;
  decisionType: DecisionType;
  context: DecisionContext;
  alternatives: DecisionAlternative[];
  selectedAlternative: string;
  reasoning: DecisionReasoning;
  outcome?: DecisionOutcome;
  quality?: DecisionQuality;
}

export type DecisionType = 
  | 'strategic'
  | 'tactical'
  | 'operational'
  | 'emergent'
  | 'ethical'
  | 'creative';

export interface DecisionContext {
  goals: string[];
  constraints: string[];
  resources: any;
  stakeholders: string[];
  timeline?: any;
  riskFactors: string[];
}

export interface DecisionAlternative {
  id: string;
  description: string;
  criteria: DecisionCriteria;
  expectedOutcome: any;
  riskLevel: number;
  confidence: number;
}

export interface DecisionCriteria {
  effectiveness: number;
  efficiency: number;
  feasibility: number;
  acceptability: number;
  sustainability: number;
  ethicalAlignment: number;
  strategicAlignment: number;
}

export interface DecisionReasoning {
  process: string;
  chain: ReasoningStep[];
  biases?: string[];
  assumptions: string[];
  evidence: Evidence[];
  confidence: number;
}

export interface ReasoningStep {
  step: string;
  type: 'premise' | 'inference' | 'evaluation' | 'conclusion';
  logic: string;
  confidence: number;
}

export interface Evidence {
  source: string;
  type: 'empirical' | 'analytical' | 'experiential' | 'wisdom';
  content: any;
  reliability: number;
}

export interface DecisionOutcome {
  actualResult: any;
  success: boolean;
  effectiveness: number;
  efficiency: number;
  sideEffects: string[];
  learningPoints: string[];
}

export interface DecisionQuality {
  overall: number;
  rationality: number;
  effectiveness: number;
  efficiency: number;
  ethicalAlignment: number;
  strategicAlignment: number;
  learning: number;
  traceability: number;
}

export interface DecisionLearning {
  decisionId: string;
  timestamp: Date;
  lessons: string[];
  patterns: string[];
  improvements: string[];
  confidence: number;
}

export interface DecisionSimulation {
  id: string;
  timestamp: Date;
  decision: Decision;
  simulatedOutcomes: SimulatedOutcome[];
  probabilityDistribution: Map<string, number>;
  recommendation: string;
  confidence: number;
}

export interface SimulatedOutcome {
  scenario: string;
  probability: number;
  outcome: DecisionOutcome;
  riskLevel: number;
  confidence: number;
}

// ============================================================================
// DECISION OPTIMIZER CLASS
// ============================================================================

export class DecisionOptimizer extends EventEmitter {
  private decisions: Map<string, Decision>;
  private decisionHistory: Decision[];
  private learningHistory: DecisionLearning[];
  private decisionPatterns: Map<string, any>;
  private decisionStrategies: Map<string, any>;
  private readonly MAX_HISTORY = 5000;

  constructor() {
    super();
    this.decisions = new Map();
    this.decisionHistory = [];
    this.learningHistory = [];
    this.decisionPatterns = new Map();
    this.decisionStrategies = new Map();
  }

  // ========================================================================
  // DECISION MAKING
  // ========================================================================

  /**
   * Make an optimized decision
   */
  public async makeDecision(
    decisionType: DecisionType,
    context: DecisionContext,
    alternatives: DecisionAlternative[],
    reasoning: DecisionReasoning
  ): Promise<Decision> {
    // Analyze alternatives
    const analyzedAlternatives = await this.analyzeAlternatives(
      alternatives,
      context
    );

    // Select best alternative
    const selectedAlternativeId = await this.selectAlternative(
      analyzedAlternatives,
      context
    );

    // Create decision record
    const decision: Decision = {
      id: this.generateId(),
      timestamp: new Date(),
      decisionType,
      context,
      alternatives: analyzedAlternatives,
      selectedAlternative: selectedAlternativeId,
      reasoning
    };

    // Assess decision quality (before outcome)
    decision.quality = await this.assessDecisionQuality(decision);

    // Store decision
    this.decisions.set(decision.id, decision);
    this.decisionHistory.unshift(decision);

    // Maintain history limit
    if (this.decisionHistory.length > this.MAX_HISTORY) {
      this.decisionHistory.pop();
    }

    this.emit('decision-made', decision);

    return decision;
  }

  // ========================================================================
  // ALTERNATIVE ANALYSIS
  // ========================================================================

  private async analyzeAlternatives(
    alternatives: DecisionAlternative[],
    context: DecisionContext
  ): Promise<DecisionAlternative[]> {
    const analyzed = alternatives.map(alt => {
      // Calculate comprehensive score
      const score = this.calculateAlternativeScore(alt, context);
      
      // Adjust confidence based on criteria
      const adjustedConfidence = this.adjustConfidence(alt, score);

      return {
        ...alt,
        confidence: adjustedConfidence
      };
    });

    // Sort by score
    analyzed.sort((a, b) => {
      const scoreA = this.calculateAlternativeScore(a, context);
      const scoreB = this.calculateAlternativeScore(b, context);
      return scoreB - scoreA;
    });

    return analyzed;
  }

  private calculateAlternativeScore(
    alternative: DecisionAlternative,
    context: DecisionContext
  ): number {
    const criteria = alternative.criteria;

    // Weighted score calculation
    const weights = {
      effectiveness: 0.25,
      efficiency: 0.15,
      feasibility: 0.15,
      acceptability: 0.10,
      sustainability: 0.10,
      ethicalAlignment: 0.15,
      strategicAlignment: 0.10
    };

    const score =
      criteria.effectiveness * weights.effectiveness +
      criteria.efficiency * weights.efficiency +
      criteria.feasibility * weights.feasibility +
      criteria.acceptability * weights.acceptability +
      criteria.sustainability * weights.sustainability +
      criteria.ethicalAlignment * weights.ethicalAlignment +
      criteria.strategicAlignment * weights.strategicAlignment;

    // Adjust for risk
    const riskAdjustment = 1 - (alternative.riskLevel * 0.2);

    return score * riskAdjustment;
  }

  private adjustConfidence(
    alternative: DecisionAlternative,
    score: number
  ): number {
    // Adjust confidence based on score
    const confidenceAdjustment = (score - 0.5) * 0.2;
    return Math.max(0, Math.min(1, alternative.confidence + confidenceAdjustment));
  }

  // ========================================================================
  // ALTERNATIVE SELECTION
  // ========================================================================

  private async selectAlternative(
    alternatives: DecisionAlternative[],
    context: DecisionContext
  ): Promise<string> {
    if (alternatives.length === 0) {
      throw new Error('No alternatives to select from');
    }

    // Get top alternatives
    const topAlternatives = alternatives.slice(0, Math.min(3, alternatives.length));

    // If only one alternative, select it
    if (topAlternatives.length === 1) {
      return topAlternatives[0].id;
    }

    // Multiple top alternatives - use selection strategy
    const strategy = this.determineSelectionStrategy(context);

    switch (strategy) {
      case 'highest-score':
        return topAlternatives[0].id;

      case 'risk-averse':
        return this.selectRiskAverse(topAlternatives);

      case 'balanced':
        return this.selectBalanced(topAlternatives);

      case 'strategic':
        return this.selectStrategic(topAlternatives, context);

      default:
        return topAlternatives[0].id;
    }
  }

  private determineSelectionStrategy(context: DecisionContext): string {
    // Determine strategy based on context
    if (context.riskFactors && context.riskFactors.length > 2) {
      return 'risk-averse';
    }

    if (context.goals.some(g => g.toLowerCase().includes('strategic'))) {
      return 'strategic';
    }

    if (context.constraints && context.constraints.length > 3) {
      return 'balanced';
    }

    return 'highest-score';
  }

  private selectRiskAverse(alternatives: DecisionAlternative[]): string {
    // Select alternative with lowest risk among top scorers
    const sortedByRisk = [...alternatives].sort((a, b) => a.riskLevel - b.riskLevel);
    return sortedByRisk[0].id;
  }

  private selectBalanced(alternatives: DecisionAlternative[]): string {
    // Select alternative with best balance of criteria
    const balancedScores = alternatives.map(alt => {
      const criteria = alt.criteria;
      const stdDev = this.calculateStandardDeviation([
        criteria.effectiveness,
        criteria.efficiency,
        criteria.feasibility,
        criteria.acceptability,
        criteria.sustainability,
        criteria.ethicalAlignment,
        criteria.strategicAlignment
      ]);

      return {
        id: alt.id,
        balancedScore: alt.criteria.effectiveness - (stdDev * 0.5)
      };
    });

    balancedScores.sort((a, b) => b.balancedScore - a.balancedScore);
    return balancedScores[0].id;
  }

  private selectStrategic(
    alternatives: DecisionAlternative[],
    context: DecisionContext
  ): string {
    // Select alternative with highest strategic alignment
    const sortedByStrategic = [...alternatives].sort(
      (a, b) => b.criteria.strategicAlignment - a.criteria.strategicAlignment
    );
    return sortedByStrategic[0].id;
  }

  private calculateStandardDeviation(values: number[]): number {
    const mean = values.reduce((sum, v) => sum + v, 0) / values.length;
    const squaredDiffs = values.map(v => Math.pow(v - mean, 2));
    const avgSquaredDiff = squaredDiffs.reduce((sum, v) => sum + v, 0) / values.length;
    return Math.sqrt(avgSquaredDiff);
  }

  // ========================================================================
  // DECISION QUALITY ASSESSMENT
  // ========================================================================

  /**
   * Assess decision quality
   */
  public async assessDecisionQuality(decision: Decision): Promise<DecisionQuality> {
    const quality: DecisionQuality = {
      overall: 0.5,
      rationality: 0.5,
      effectiveness: 0.5,
      efficiency: 0.5,
      ethicalAlignment: 0.5,
      strategicAlignment: 0.5,
      learning: 0.5,
      traceability: 0.5
    };

    // Assess rationality
    quality.rationality = this.assessRationality(decision);

    // Assess effectiveness (if outcome available)
    if (decision.outcome) {
      quality.effectiveness = decision.outcome.effectiveness;
      quality.efficiency = decision.outcome.efficiency;
    } else {
      quality.effectiveness = decision.alternatives.find(
        a => a.id === decision.selectedAlternative
      )?.criteria.effectiveness || 0.5;
    }

    // Assess ethical alignment
    quality.ethicalAlignment = this.assessEthicalAlignment(decision);

    // Assess strategic alignment
    quality.strategicAlignment = this.assessStrategicAlignment(decision);

    // Assess learning potential
    quality.learning = this.assessLearningPotential(decision);

    // Assess traceability
    quality.traceability = this.assessTraceability(decision);

    // Calculate overall quality
    quality.overall = this.calculateOverallQuality(quality);

    return quality;
  }

  private assessRationality(decision: Decision): number {
    let score = 0.5;

    // Check reasoning chain
    if (decision.reasoning.chain && decision.reasoning.chain.length > 3) {
      score += 0.2;
    }

    // Check for evidence
    if (decision.reasoning.evidence && decision.reasoning.evidence.length > 0) {
      score += 0.15;
    }

    // Check for bias awareness
    if (decision.reasoning.biases && decision.reasoning.biases.length > 0) {
      score += 0.1;
    }

    // Check confidence
    if (decision.reasoning.confidence > 0.7) {
      score += 0.05;
    }

    return Math.min(1.0, score);
  }

  private assessEthicalAlignment(decision: Decision): number {
    const selected = decision.alternatives.find(
      a => a.id === decision.selectedAlternative
    );

    return selected?.criteria.ethicalAlignment || 0.5;
  }

  private assessStrategicAlignment(decision: Decision): number {
    const selected = decision.alternatives.find(
      a => a.id === decision.selectedAlternative
    );

    return selected?.criteria.strategicAlignment || 0.5;
  }

  private assessLearningPotential(decision: Decision): number {
    let score = 0.5;

    // Check for multiple alternatives
    if (decision.alternatives.length > 2) {
      score += 0.2;
    }

    // Check for detailed reasoning
    if (decision.reasoning.chain && decision.reasoning.chain.length > 5) {
      score += 0.15;
    }

    // Check for evidence
    if (decision.reasoning.evidence && decision.reasoning.evidence.length > 2) {
      score += 0.1;
    }

    return Math.min(1.0, score);
  }

  private assessTraceability(decision: Decision): number {
    let score = 0.5;

    // Check for reasoning steps
    if (decision.reasoning.chain && decision.reasoning.chain.length > 0) {
      score += 0.2;
    }

    // Check for evidence
    if (decision.reasoning.evidence && decision.reasoning.evidence.length > 0) {
      score += 0.15;
    }

    // Check for assumptions documentation
    if (decision.reasoning.assumptions && decision.reasoning.assumptions.length > 0) {
      score += 0.1;
    }

    return Math.min(1.0, score);
  }

  private calculateOverallQuality(quality: DecisionQuality): number {
    return (
      quality.rationality * 0.2 +
      quality.effectiveness * 0.25 +
      quality.efficiency * 0.15 +
      quality.ethicalAlignment * 0.15 +
      quality.strategicAlignment * 0.15 +
      quality.learning * 0.05 +
      quality.traceability * 0.05
    );
  }

  // ========================================================================
  // DECISION LEARNING
  // ========================================================================

  /**
   * Record decision outcome and learn from it
   */
  public async recordOutcome(
    decisionId: string,
    outcome: DecisionOutcome
  ): Promise<DecisionLearning> {
    const decision = this.decisions.get(decisionId);

    if (!decision) {
      throw new Error(`Decision not found: ${decisionId}`);
    }

    // Update decision with outcome
    decision.outcome = outcome;

    // Reassess decision quality with outcome
    decision.quality = await this.assessDecisionQuality(decision);

    // Extract learning
    const learning = await this.extractLearning(decision, outcome);

    // Store learning
    this.learningHistory.unshift(learning);

    // Update decision patterns
    this.updateDecisionPatterns(decision, outcome, learning);

    this.emit('decision-outcome-recorded', { decisionId, outcome, learning });

    return learning;
  }

  private async extractLearning(
    decision: Decision,
    outcome: DecisionOutcome
  ): Promise<DecisionLearning> {
    const learning: DecisionLearning = {
      decisionId: decision.id,
      timestamp: new Date(),
      lessons: [],
      patterns: [],
      improvements: [],
      confidence: 0.7
    };

    // Extract lessons from outcome
    if (outcome.learningPoints && outcome.learningPoints.length > 0) {
      learning.lessons.push(...outcome.learningPoints);
    }

    // Analyze effectiveness
    if (outcome.effectiveness > 0.8) {
      learning.lessons.push(`Highly effective decision type: ${decision.decisionType}`);
    } else if (outcome.effectiveness < 0.5) {
      learning.improvements.push(`Low effectiveness - review ${decision.decisionType} decisions`);
    }

    // Analyze efficiency
    if (outcome.efficiency > 0.8) {
      learning.patterns.push(`Efficient pattern identified in ${decision.decisionType} decisions`);
    }

    // Analyze side effects
    if (outcome.sideEffects && outcome.sideEffects.length > 0) {
      learning.lessons.push(`Side effects observed: ${outcome.sideEffects.join(', ')}`);
    }

    // Compare expected vs actual
    const selected = decision.alternatives.find(
      a => a.id === decision.selectedAlternative
    );

    if (selected) {
      const expectedEffectiveness = selected.criteria.effectiveness;
      const actualEffectiveness = outcome.effectiveness;
      const difference = Math.abs(expectedEffectiveness - actualEffectiveness);

      if (difference > 0.2) {
        learning.improvements.push(
          `Prediction accuracy issue: expected ${expectedEffectiveness.toFixed(2)}, got ${actualEffectiveness.toFixed(2)}`
        );
      }
    }

    return learning;
  }

  private updateDecisionPatterns(
    decision: Decision,
    outcome: DecisionOutcome,
    learning: DecisionLearning
  ): void {
    const patternKey = `${decision.decisionType}:${decision.context.goals.join(',')}`;

    let pattern = this.decisionPatterns.get(patternKey);

    if (!pattern) {
      pattern = {
        count: 0,
        totalEffectiveness: 0,
        totalEfficiency: 0,
        successCount: 0
      };
      this.decisionPatterns.set(patternKey, pattern);
    }

    pattern.count++;
    pattern.totalEffectiveness += outcome.effectiveness;
    pattern.totalEfficiency += outcome.efficiency;

    if (outcome.success) {
      pattern.successCount++;
    }
  }

  // ========================================================================
  // DECISION SIMULATION
  // ========================================================================

  /**
   * Simulate decision outcomes
   */
  public async simulateDecision(
    decision: Decision,
    scenarios: number = 5
  ): Promise<DecisionSimulation> {
    const simulation: DecisionSimulation = {
      id: this.generateId(),
      timestamp: new Date(),
      decision,
      simulatedOutcomes: [],
      probabilityDistribution: new Map(),
      recommendation: '',
      confidence: 0.5
    };

    // Generate scenarios
    for (let i = 0; i < scenarios; i++) {
      const scenario = this.generateScenario(i, scenarios);
      const outcome = await this.simulateOutcome(decision, scenario);

      simulation.simulatedOutcomes.push(outcome);
    }

    // Calculate probability distribution
    const successCount = simulation.simulatedOutcomes.filter(o => o.outcome.success).length;
    const successProbability = successCount / scenarios;

    simulation.probabilityDistribution.set('success', successProbability);
    simulation.probabilityDistribution.set('failure', 1 - successProbability);

    // Generate recommendation
    simulation.recommendation = this.generateRecommendation(simulation);
    simulation.confidence = successProbability;

    this.emit('decision-simulated', simulation);

    return simulation;
  }

  private generateScenario(index: number, total: number): string {
    const scenarios = ['optimistic', 'realistic', 'pessimistic', 'uncertain', 'complex'];
    return scenarios[index % scenarios.length];
  }

  private async simulateOutcome(
    decision: Decision,
    scenario: string
  ): Promise<SimulatedOutcome> {
    const selected = decision.alternatives.find(
      a => a.id === decision.selectedAlternative
    );

    if (!selected) {
      throw new Error('Selected alternative not found');
    }

    // Simulate outcome based on scenario
    let effectiveness = selected.criteria.effectiveness;
    let efficiency = selected.criteria.efficiency;

    // Adjust based on scenario
    switch (scenario) {
      case 'optimistic':
        effectiveness = Math.min(1, effectiveness + 0.1);
        efficiency = Math.min(1, efficiency + 0.1);
        break;
      case 'pessimistic':
        effectiveness = Math.max(0, effectiveness - 0.15);
        efficiency = Math.max(0, efficiency - 0.15);
        break;
      case 'uncertain':
        effectiveness = effectiveness * 0.9;
        break;
      case 'complex':
        efficiency = efficiency * 0.85;
        break;
    }

    // Add some randomness
    effectiveness += (Math.random() - 0.5) * 0.1;
    effectiveness = Math.max(0, Math.min(1, effectiveness));

    const success = effectiveness > 0.6;

    return {
      scenario,
      probability: 1 / 5,
      outcome: {
        actualResult: { effectiveness, efficiency },
        success,
        effectiveness,
        efficiency,
        sideEffects: success ? [] : ['Side effect from simulation'],
        learningPoints: []
      },
      riskLevel: 1 - effectiveness,
      confidence: 0.7
    };
  }

  private generateRecommendation(simulation: DecisionSimulation): string {
    const successProbability = simulation.probabilityDistribution.get('success') || 0;

    if (successProbability > 0.8) {
      return 'High confidence - proceed with decision';
    } else if (successProbability > 0.6) {
      return 'Moderate confidence - proceed with caution';
    } else if (successProbability > 0.4) {
      return 'Low confidence - consider alternatives';
    } else {
      return 'Very low confidence - reconsider decision';
    }
  }

  // ========================================================================
  // STATE MANAGEMENT
  // ========================================================================

  public getDecision(id: string): Decision | undefined {
    return this.decisions.get(id);
  }

  public getDecisionHistory(filter?: {
    type?: DecisionType;
    since?: Date;
    limit?: number;
  }): Decision[] {
    let results = this.decisionHistory;

    if (filter?.type) {
      results = results.filter(d => d.decisionType === filter.type);
    }

    if (filter?.since) {
      results = results.filter(d => d.timestamp >= filter.since!);
    }

    if (filter?.limit) {
      results = results.slice(0, filter.limit);
    }

    return results;
  }

  public getLearningHistory(limit?: number): DecisionLearning[] {
    return limit ? this.learningHistory.slice(0, limit) : this.learningHistory;
  }

  public getDecisionPatterns(): Map<string, any> {
    return new Map(this.decisionPatterns);
  }

  public getStatistics(): {
    totalDecisions: number;
    avgEffectiveness: number;
    avgEfficiency: number;
    successRate: number;
    byType: Map<DecisionType, { count: number; avgEffectiveness: number; avgEfficiency: number }>;
  } {
    const decisions = Array.from(this.decisions.values()).filter(d => d.outcome);

    const byType = new Map<DecisionType, { count: number; avgEffectiveness: number; avgEfficiency: number }>();

    let totalEffectiveness = 0;
    let totalEfficiency = 0;
    let successCount = 0;

    decisions.forEach(d => {
      const outcome = d.outcome!;
      totalEffectiveness += outcome.effectiveness;
      totalEfficiency += outcome.efficiency;

      if (outcome.success) {
        successCount++;
      }

      // By type
      let typeStats = byType.get(d.decisionType);
      if (!typeStats) {
        typeStats = { count: 0, avgEffectiveness: 0, avgEfficiency: 0 };
        byType.set(d.decisionType, typeStats);
      }

      typeStats.count++;
      typeStats.avgEffectiveness = (typeStats.avgEffectiveness * (typeStats.count - 1) + outcome.effectiveness) / typeStats.count;
      typeStats.avgEfficiency = (typeStats.avgEfficiency * (typeStats.count - 1) + outcome.efficiency) / typeStats.count;
    });

    return {
      totalDecisions: decisions.length,
      avgEffectiveness: decisions.length > 0 ? totalEffectiveness / decisions.length : 0,
      avgEfficiency: decisions.length > 0 ? totalEfficiency / decisions.length : 0,
      successRate: decisions.length > 0 ? successCount / decisions.length : 0,
      byType
    };
  }

  // ========================================================================
  // UTILITY METHODS
  // ========================================================================

  private generateId(): string {
    return `decision_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // ========================================================================
  // CLEANUP
  // ========================================================================

  public destroy(): void {
    this.removeAllListeners();
    this.decisions.clear();
    this.decisionHistory = [];
    this.learningHistory = [];
    this.decisionPatterns.clear();
    this.decisionStrategies.clear();
  }
}