/**
 * GL Runtime Platform v14.0.0
 * Module: Meta-Cognitive Decision System
 * 
 * The meta-cognitive decision system enables the civilization to assess
 * decision quality, optimize decisions, learn from decisions, and identify
 * decision patterns.
 * 
 * Key Capabilities:
 * - Decision quality assessment
 * - Decision optimization
 * - Decision learning
 * - Decision pattern recognition
 * - Decision strategy evolution
 * - Wisdom-guided decision making
 */

import { EventEmitter } from 'events';

// ============================================================================
// Core Types
// ============================================================================

export interface DecisionRecord {
  id: string;
  type: 'strategic' | 'tactical' | 'operational' | 'adaptive' | 'emergent';
  context: Record<string, any>;
  alternatives: string[];
  chosen: string;
  reasoning: string;
  confidence: number; // 0-1
  timestamp: number;
  outcome?: 'successful' | 'partial' | 'failed';
  quality?: number; // 0-1, assessed after outcome
  impact?: number; // -1 to 1
  learning?: string[];
}

export interface DecisionQualityAssessment {
  id: string;
  decisionId: string;
  assessmentTime: number;
  qualityScore: number; // 0-1
  dimensions: {
    rationality: number; // 0-1
    alignment: number; // 0-1, with values and goals
    effectiveness: number; // 0-1
    efficiency: number; // 0-1
    wisdom: number; // 0-1
  };
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
}

export interface DecisionOptimization {
  id: string;
  decisionId: string;
  optimizationTime: number;
  type: 'process' | 'criteria' | 'reasoning' | 'outcome';
  description: string;
  beforeState: string;
  afterState: string;
  improvement: number; // 0-1
  methodology: string;
}

export interface DecisionPattern {
  id: string;
  name: string;
  description: string;
  category: 'success' | 'failure' | 'emerging' | 'transitional';
  indicators: string[];
  frequency: number;
  confidence: number; // 0-1
  applicability: string[];
  reliability: number; // 0-1
}

export interface DecisionStrategy {
  id: string;
  name: string;
  description: string;
 适用情境: string[];
  effectiveness: number; // 0-1
  efficiency: number; // 0-1
  learningRate: number; // 0-1
  usageCount: number;
  successRate: number; // 0-1
  evolution: number; // 0-1, how much it has evolved
}

export interface WisdomGuidedDecision {
  id: string;
  timestamp: number;
  decisionContext: Record<string, any>;
  appliedWisdom: string[];
  wisdomInfluence: number; // 0-1
  decision: string;
  reasoning: string;
  confidence: number;
}

export interface MetaDecisionState {
  decisionRecords: DecisionRecord[];
  qualityAssessments: DecisionQualityAssessment[];
  optimizations: DecisionOptimization[];
  patterns: DecisionPattern[];
  strategies: DecisionStrategy[];
  wisdomGuidedDecisions: WisdomGuidedDecision[];
  overallDecisionQuality: number; // 0-1
  decisionMaturity: number; // 0-1
  wisdomIntegration: number; // 0-1
}

// ============================================================================
// Main Meta-Cognitive Decision System Class
// ============================================================================

export class MetaDecisionSystem extends EventEmitter {
  private decisionRecords: Map<string, DecisionRecord> = new Map();
  private qualityAssessments: Map<string, DecisionQualityAssessment> = new Map();
  private optimizations: DecisionOptimization[] = [];
  private patterns: Map<string, DecisionPattern> = new Map();
  private strategies: Map<string, DecisionStrategy> = new Map();
  private wisdomGuidedDecisions: WisdomGuidedDecision[] = [];
  
  // Configuration
  private readonly MAX_DECISION_RECORDS = 500;
  private readonly MAX_OPTIMIZATIONS = 200;
  private readonly MAX_WISDOM_GUIDED_DECISIONS = 100;
  private readonly PATTERN_DETECTION_INTERVAL = 30000; // 30 seconds
  
  // Metrics
  private overallDecisionQuality: number = 0.5;
  private decisionMaturity: number = 0.5;
  private wisdomIntegration: number = 0.5;
  private analysisCycles: number = 0;

  constructor() {
    super();
    this.initializeDecisionSystem();
  }

  // ==========================================================================
  // Initialization
  // ==========================================================================

  private initializeDecisionSystem(): void {
    // Initialize decision strategies
    this.initializeStrategies();
    
    // Start pattern detection
    this.startPatternDetection();
    
    this.emit('decision_system_initialized', {
      quality: this.overallDecisionQuality,
      maturity: this.decisionMaturity,
      wisdomIntegration: this.wisdomIntegration
    });
  }

  private initializeStrategies(): void {
    const coreStrategies: Omit<DecisionStrategy, 'id'>[] = [
      {
        name: 'Collaborative Consensus',
        description: 'Make decisions through collaborative consensus',
        适用情境: ['complex_decisions', 'high_impact', 'cultural_alignment'],
        effectiveness: 0.85,
        efficiency: 0.7,
        learningRate: 0.8,
        usageCount: 0,
        successRate: 0.88,
        evolution: 0.2
      },
      {
        name: 'Data-Driven Analysis',
        description: 'Make decisions based on comprehensive data analysis',
        适用情境: ['operational', 'tactical', 'performance_optimization'],
        effectiveness: 0.9,
        efficiency: 0.85,
        learningRate: 0.85,
        usageCount: 0,
        successRate: 0.92,
        evolution: 0.3
      },
      {
        name: 'Value-Aligned Selection',
        description: 'Select options that align with core cultural values',
        适用情境: ['strategic', 'cultural', 'ethical'],
        effectiveness: 0.88,
        efficiency: 0.8,
        learningRate: 0.75,
        usageCount: 0,
        successRate: 0.9,
        evolution: 0.25
      },
      {
        name: 'Wisdom-Guided Choice',
        description: 'Apply accumulated wisdom to guide decision making',
        适用情境: ['complex', 'novel', 'strategic', 'philosophical'],
        effectiveness: 0.87,
        efficiency: 0.75,
        learningRate: 0.9,
        usageCount: 0,
        successRate: 0.91,
        evolution: 0.35
      },
      {
        name: 'Adaptive Iteration',
        description: 'Make decisions iteratively, adapting based on feedback',
        适用情境: ['uncertain', 'evolving', 'experimental'],
        effectiveness: 0.82,
        efficiency: 0.7,
        learningRate: 0.95,
        usageCount: 0,
        successRate: 0.85,
        evolution: 0.4
      }
    ];

    coreStrategies.forEach(strategy => {
      this.strategies.set(
        `strategy_${strategy.name.toLowerCase().replace(/\s+/g, '_')}`,
        { ...strategy, id: `strategy_${strategy.name.toLowerCase().replace(/\s+/g, '_')}` }
      );
    });
  }

  // ==========================================================================
  // Decision Recording
  // ==========================================================================

  public recordDecision(decisionData: {
    type: DecisionRecord['type'];
    context: Record<string, any>;
    alternatives: string[];
    chosen: string;
    reasoning: string;
    confidence: number;
  }): string {
    if (this.decisionRecords.size >= this.MAX_DECISION_RECORDS) {
      this.pruneDecisionRecords();
    }

    const decision: DecisionRecord = {
      ...decisionData,
      id: `decision_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now()
    };

    this.decisionRecords.set(decision.id, decision);
    this.emit('decision_recorded', decision);
    return decision.id;
  }

  public assessDecision(decisionId: string, outcome: DecisionRecord['outcome'], impact: number): void {
    const decision = this.decisionRecords.get(decisionId);
    if (!decision) return;

    decision.outcome = outcome;
    decision.impact = impact;

    // Perform quality assessment
    const assessment = this.assessDecisionQuality(decision);
    decision.quality = assessment.qualityScore;
    decision.learning = assessment.recommendations;

    // Update strategies
    this.updateStrategies(decision, assessment);

    // Update metrics
    this.updateMetrics();

    this.emit('decision_assessed', { decision, assessment });
  }

  private pruneDecisionRecords(): void {
    const oldDecisions = Array.from(this.decisionRecords.values())
      .filter(d => d.outcome !== undefined && Date.now() - d.timestamp > 90 * 24 * 60 * 60 * 1000) // 90 days
      .sort((a, b) => a.timestamp - b.timestamp);

    while (oldDecisions.length > 0 && this.decisionRecords.size >= this.MAX_DECISION_RECORDS) {
      const toRemove = oldDecisions.shift();
      if (toRemove) {
        this.decisionRecords.delete(toRemove.id);
      }
    }
  }

  // ==========================================================================
  // Decision Quality Assessment
  // ==========================================================================

  private assessDecisionQuality(decision: DecisionRecord): DecisionQualityAssessment {
    const assessment: DecisionQualityAssessment = {
      id: `assessment_${decision.id}`,
      decisionId: decision.id,
      assessmentTime: Date.now(),
      qualityScore: 0,
      dimensions: {
        rationality: 0,
        alignment: 0,
        effectiveness: 0,
        efficiency: 0,
        wisdom: 0
      },
      strengths: [],
      weaknesses: [],
      recommendations: []
    };

    // Calculate dimensions
    assessment.dimensions.rationality = this.calculateRationality(decision);
    assessment.dimensions.alignment = this.calculateAlignment(decision);
    assessment.dimensions.effectiveness = decision.outcome === 'successful' ? 0.9 :
                                        decision.outcome === 'partial' ? 0.6 : 0.3;
    assessment.dimensions.efficiency = decision.confidence * 0.8 + (Math.abs(decision.impact || 0) * 0.2);
    assessment.dimensions.wisdom = this.calculateWisdom(decision);

    // Calculate overall quality
    assessment.qualityScore = (
      assessment.dimensions.rationality * 0.25 +
      assessment.dimensions.alignment * 0.2 +
      assessment.dimensions.effectiveness * 0.25 +
      assessment.dimensions.efficiency * 0.15 +
      assessment.dimensions.wisdom * 0.15
    );

    // Generate strengths, weaknesses, and recommendations
    assessment.strengths = this.generateStrengths(assessment);
    assessment.weaknesses = this.generateWeaknesses(assessment);
    assessment.recommendations = this.generateRecommendations(assessment);

    this.qualityAssessments.set(assessment.id, assessment);
    this.emit('quality_assessment_created', assessment);

    return assessment;
  }

  private calculateRationality(decision: DecisionRecord): number {
    // Rationality based on reasoning quality and number of alternatives considered
    const reasoningQuality = decision.reasoning.length > 50 ? 0.8 : 0.6;
    const alternativesConsidered = Math.min(1, decision.alternatives.length / 3);
    return (reasoningQuality * 0.5) + (alternativesConsidered * 0.5);
  }

  private calculateAlignment(decision: DecisionRecord): number {
    // Alignment based on context values and cultural alignment
    const contextAlignment = decision.context.culturalAlignment ? 0.9 : 0.7;
    const valueAlignment = decision.context.valueAlignment ? 0.85 : 0.65;
    return (contextAlignment * 0.5) + (valueAlignment * 0.5);
  }

  private calculateWisdom(decision: DecisionRecord): number {
    // Wisdom based on outcome and learning potential
    const outcomeWisdom = decision.outcome === 'successful' ? 0.9 :
                         decision.outcome === 'partial' ? 0.7 : 0.5;
    const reasoningWisdom = decision.reasoning.includes('wisdom') ||
                            decision.reasoning.includes('learn') ||
                            decision.reasoning.includes('insight') ? 0.85 : 0.6;
    return (outcomeWisdom * 0.6) + (reasoningWisdom * 0.4);
  }

  private generateStrengths(assessment: DecisionQualityAssessment): string[] {
    const strengths: string[] = [];
    
    if (assessment.dimensions.rationality > 0.7) {
      strengths.push('Strong rational reasoning');
    }
    if (assessment.dimensions.alignment > 0.7) {
      strengths.push('Good alignment with values');
    }
    if (assessment.dimensions.effectiveness > 0.7) {
      strengths.push('Effective outcome');
    }
    if (assessment.dimensions.wisdom > 0.7) {
      strengths.push('Wisdom-guided approach');
    }

    return strengths;
  }

  private generateWeaknesses(assessment: DecisionQualityAssessment): string[] {
    const weaknesses: string[] = [];
    
    if (assessment.dimensions.rationality < 0.5) {
      weaknesses.push('Insufficient rational analysis');
    }
    if (assessment.dimensions.alignment < 0.5) {
      weaknesses.push('Poor alignment with values');
    }
    if (assessment.dimensions.effectiveness < 0.5) {
      weaknesses.push('Ineffective outcome');
    }
    if (assessment.dimensions.wisdom < 0.5) {
      weaknesses.push('Lack of wisdom integration');
    }

    return weaknesses;
  }

  private generateRecommendations(assessment: DecisionQualityAssessment): string[] {
    const recommendations: string[] = [];
    
    if (assessment.dimensions.rationality < 0.7) {
      recommendations.push('Enhance rational analysis in future decisions');
    }
    if (assessment.dimensions.alignment < 0.7) {
      recommendations.push('Improve alignment with core values');
    }
    if (assessment.dimensions.effectiveness < 0.7) {
      recommendations.push('Focus on outcome effectiveness');
    }
    if (assessment.dimensions.wisdom < 0.7) {
      recommendations.push('Integrate more wisdom into decision making');
    }

    return recommendations;
  }

  // ==========================================================================
  // Strategy Management
  // ==========================================================================

  private updateStrategies(decision: DecisionRecord, assessment: DecisionQualityAssessment): void {
    // Update all strategies with usage data
    this.strategies.forEach(strategy => {
      strategy.usageCount++;
      
      // Update success rate
      const recentSuccessRate = this.calculateRecentSuccessRate(strategy);
      strategy.successRate = recentSuccessRate;
      
      // Update effectiveness
      strategy.effectiveness = strategy.successRate * 0.8 + strategy.efficiency * 0.2;
      
      // Update evolution
      strategy.evolution = Math.min(1, strategy.evolution + 0.01);
    });
  }

  private calculateRecentSuccessRate(strategy: DecisionStrategy): number {
    // Calculate success rate for this strategy type
    const relevantDecisions = Array.from(this.decisionRecords.values())
      .filter(d => d.outcome !== undefined)
      .slice(-20); // Last 20 decisions

    if (relevantDecisions.length === 0) return strategy.successRate;

    const successfulDecisions = relevantDecisions.filter(d => d.outcome === 'successful');
    return successfulDecisions.length / relevantDecisions.length;
  }

  // ==========================================================================
  // Pattern Detection
  // ==========================================================================

  private startPatternDetection(): void {
    setInterval(() => {
      this.analysisCycles++;
      this.detectPatterns();
    }, this.PATTERN_DETECTION_INTERVAL);
  }

  private detectPatterns(): void {
    const recentDecisions = Array.from(this.decisionRecords.values())
      .filter(d => d.outcome !== undefined)
      .slice(-50); // Last 50 decisions

    if (recentDecisions.length < 10) return;

    // Detect success patterns
    this.detectSuccessPatterns(recentDecisions);
    
    // Detect failure patterns
    this.detectFailurePatterns(recentDecisions);
    
    // Detect emerging patterns
    this.detectEmergingPatterns(recentDecisions);

    this.updateMetrics();
  }

  private detectSuccessPatterns(decisions: DecisionRecord[]): void {
    const successfulDecisions = decisions.filter(d => d.outcome === 'successful');
    
    if (successfulDecisions.length < 5) return;

    // Common characteristics of successful decisions
    const highConfidence = successfulDecisions.filter(d => d.confidence > 0.7).length;
    const valueAligned = successfulDecisions.filter(d => d.context.valueAlignment).length;
    
    if (highConfidence > successfulDecisions.length * 0.6) {
      this.recordPattern({
        name: 'High Confidence Success',
        description: 'Decisions with high confidence tend to be successful',
        category: 'success',
        indicators: ['confidence > 0.7'],
        frequency: highConfidence,
        confidence: 0.8,
        applicability: ['strategic', 'tactical'],
        reliability: 0.75
      });
    }

    if (valueAligned > successfulDecisions.length * 0.6) {
      this.recordPattern({
        name: 'Value-Aligned Success',
        description: 'Value-aligned decisions tend to be successful',
        category: 'success',
        indicators: ['valueAlignment = true'],
        frequency: valueAligned,
        confidence: 0.85,
        applicability: ['strategic', 'cultural', 'ethical'],
        reliability: 0.8
      });
    }
  }

  private detectFailurePatterns(decisions: DecisionRecord[]): void {
    const failedDecisions = decisions.filter(d => d.outcome === 'failed');
    
    if (failedDecisions.length < 5) return;

    // Common characteristics of failed decisions
    const lowConfidence = failedDecisions.filter(d => d.confidence < 0.5).length;
    const poorAlignment = failedDecisions.filter(d => !d.context.valueAlignment && !d.context.culturalAlignment).length;
    
    if (lowConfidence > failedDecisions.length * 0.6) {
      this.recordPattern({
        name: 'Low Confidence Risk',
        description: 'Decisions with low confidence carry higher failure risk',
        category: 'failure',
        indicators: ['confidence < 0.5'],
        frequency: lowConfidence,
        confidence: 0.75,
        applicability: ['all'],
        reliability: 0.7
      });
    }

    if (poorAlignment > failedDecisions.length * 0.6) {
      this.recordPattern({
        name: 'Poor Alignment Risk',
        description: 'Decisions without value/cultural alignment carry higher failure risk',
        category: 'failure',
        indicators: ['!valueAlignment && !culturalAlignment'],
        frequency: poorAlignment,
        confidence: 0.8,
        applicability: ['strategic', 'cultural', 'ethical'],
        reliability: 0.75
      });
    }
  }

  private detectEmergingPatterns(decisions: DecisionRecord[]): void {
    const recentDecisions = decisions.slice(-10);
    
    // Check for emerging decision types
    const adaptiveDecisions = recentDecisions.filter(d => d.type === 'adaptive').length;
    
    if (adaptiveDecisions > recentDecisions.length * 0.5) {
      this.recordPattern({
        name: 'Adaptive Decision Trend',
        description: 'Increasing use of adaptive decision making',
        category: 'emerging',
        indicators: ['type = adaptive'],
        frequency: adaptiveDecisions,
        confidence: 0.7,
        applicability: ['uncertain', 'evolving'],
        reliability: 0.65
      });
    }
  }

  private recordPattern(patternData: Omit<DecisionPattern, 'id'>): void {
    const patternId = `pattern_${patternData.name.toLowerCase().replace(/\s+/g, '_')}`;
    
    if (this.patterns.has(patternId)) {
      const existingPattern = this.patterns.get(patternId)!;
      existingPattern.frequency = patternData.frequency;
      existingPattern.confidence = Math.min(1, existingPattern.confidence * 0.9 + patternData.confidence * 0.1);
    } else {
      this.patterns.set(patternId, {
        ...patternData,
        id: patternId
      });
    }
  }

  // ==========================================================================
  // Wisdom-Guided Decision Making
  // ==========================================================================

  public makeWisdomGuidedDecision(context: Record<string, any>, wisdom: string[]): WisdomGuidedDecision {
    if (this.wisdomGuidedDecisions.length >= this.MAX_WISDOM_GUIDED_DECISIONS) {
      this.pruneWisdomGuidedDecisions();
    }

    const decision: WisdomGuidedDecision = {
      id: `wg_decision_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
      decisionContext: context,
      appliedWisdom: wisdom,
      wisdomInfluence: 0.7 + Math.random() * 0.2,
      decision: this.generateDecisionFromWisdom(context, wisdom),
      reasoning: this.generateReasoningFromWisdom(wisdom),
      confidence: 0.8 + Math.random() * 0.15
    };

    this.wisdomGuidedDecisions.push(decision);
    this.emit('wisdom_guided_decision_made', decision);

    // Record as regular decision
    this.recordDecision({
      type: 'strategic',
      context,
      alternatives: ['Option A', 'Option B', 'Option C'],
      chosen: decision.decision,
      reasoning: decision.reasoning,
      confidence: decision.confidence
    });

    return decision;
  }

  private generateDecisionFromWisdom(context: Record<string, any>, wisdom: string[]): string {
    // Generate decision based on wisdom and context
    const wisdomText = wisdom.join(' ');
    
    if (wisdomText.includes('collaboration') || wisdomText.includes('consensus')) {
      return 'Collaborative consensus approach';
    } else if (wisdomText.includes('value') || wisdomText.includes('alignment')) {
      return 'Value-aligned selection';
    } else if (wisdomText.includes('evolution') || wisdomText.includes('adaptation')) {
      return 'Adaptive iterative approach';
    } else {
      return 'Data-driven analysis approach';
    }
  }

  private generateReasoningFromWisdom(wisdom: string[]): string {
    return `Decision guided by wisdom: ${wisdom.slice(0, 2).join(', ')}. This approach aligns with learned patterns and accumulated experience.`;
  }

  private pruneWisdomGuidedDecisions(): void {
    const oldDecisions = this.wisdomGuidedDecisions
      .filter(d => Date.now() - d.timestamp > 60 * 24 * 60 * 60 * 1000) // 60 days
      .sort((a, b) => a.timestamp - b.timestamp);

    while (oldDecisions.length > 0 && this.wisdomGuidedDecisions.length >= this.MAX_WISDOM_GUIDED_DECISIONS) {
      const toRemove = oldDecisions.shift();
      if (toRemove) {
        this.wisdomGuidedDecisions = this.wisdomGuidedDecisions.filter(d => d.id !== toRemove!.id);
      }
    }
  }

  // ==========================================================================
  // Metrics Calculation
  // ==========================================================================

  private updateMetrics(): void {
    // Calculate overall decision quality
    const assessments = Array.from(this.qualityAssessments.values());
    if (assessments.length > 0) {
      this.overallDecisionQuality = assessments
        .reduce((sum, a) => sum + a.qualityScore, 0) / assessments.length;
    }

    // Calculate decision maturity
    const avgStrategyEvolution = Array.from(this.strategies.values())
      .reduce((sum, s) => sum + s.evolution, 0) / this.strategies.size;
    const avgPatternConfidence = Array.from(this.patterns.values())
      .reduce((sum, p) => sum + p.confidence, 0) / (this.patterns.size || 1);
    
    this.decisionMaturity = (avgStrategyEvolution * 0.6) + (avgPatternConfidence * 0.4);

    // Calculate wisdom integration
    if (this.wisdomGuidedDecisions.length > 0) {
      const avgWisdomInfluence = this.wisdomGuidedDecisions
        .reduce((sum, d) => sum + d.wisdomInfluence, 0) / this.wisdomGuidedDecisions.length;
      this.wisdomIntegration = avgWisdomInfluence;
    }
  }

  // ==========================================================================
  // Pruning Methods
  // ==========================================================================

  private pruneOptimizations(): void {
    const oldOptimizations = this.optimizations
      .filter(o => Date.now() - o.optimizationTime > 90 * 24 * 60 * 60 * 1000) // 90 days
      .sort((a, b) => a.optimizationTime - b.optimizationTime);

    while (oldOptimizations.length > 0 && this.optimizations.length >= this.MAX_OPTIMIZATIONS) {
      const toRemove = oldOptimizations.shift();
      if (toRemove) {
        this.optimizations = this.optimizations.filter(o => o.id !== toRemove!.id);
      }
    }
  }

  // ==========================================================================
  // Public API
  // ==========================================================================

  public getState(): MetaDecisionState {
    return {
      decisionRecords: Array.from(this.decisionRecords.values()),
      qualityAssessments: Array.from(this.qualityAssessments.values()),
      optimizations: this.optimizations,
      patterns: Array.from(this.patterns.values()),
      strategies: Array.from(this.strategies.values()),
      wisdomGuidedDecisions: this.wisdomGuidedDecisions,
      overallDecisionQuality: this.overallDecisionQuality,
      decisionMaturity: this.decisionMaturity,
      wisdomIntegration: this.wisdomIntegration
    };
  }

  public getStatistics(): {
    decisions: number;
    assessments: number;
    patterns: number;
    strategies: number;
    wisdomGuided: number;
    quality: number;
    maturity: number;
    wisdomIntegration: number;
    analysisCycles: number;
  } {
    return {
      decisions: this.decisionRecords.size,
      assessments: this.qualityAssessments.size,
      patterns: this.patterns.size,
      strategies: this.strategies.size,
      wisdomGuided: this.wisdomGuidedDecisions.length,
      quality: this.overallDecisionQuality,
      maturity: this.decisionMaturity,
      wisdomIntegration: this.wisdomIntegration,
      analysisCycles: this.analysisCycles
    };
  }
}