/**
 * Universal Learning Loop
 * 通用學習迴圈 - 具備永續學習能力
 * 
 * 核心能力：
 * - 觀察 → 推理 → 學習 → 抽象 → 應用 → 再推理 → 再學習
 * - 永續學習機制
 * - 知識積累
 */

// ============================================================================
// Data Types & Interfaces
// ============================================================================

export interface Observation {
  id: string;
  content: string;
  context: Record<string, any>;
  timestamp: Date;
  source: string;
}

export interface Inference {
  id: string;
  observationId: string;
  reasoning: string;
  conclusion: string;
  confidence: number;
  timestamp: Date;
}

export interface Learning {
  id: string;
  inferenceId: string;
  learnedConcept: string;
  learnedRule: string;
  confidence: number;
  timestamp: Date;
}

export interface Abstraction {
  id: string;
  learningId: string;
  abstractedConcept: string;
  abstractionLevel: number;
  generalization: string;
  timestamp: Date;
}

export interface Application {
  id: string;
  abstractionId: string;
  context: Record<string, any>;
  action: string;
  result: string;
  success: boolean;
  timestamp: Date;
}

export interface LearningCycle {
  id: string;
  observation: Observation;
  inference: Inference;
  learning: Learning;
  abstraction: Abstraction;
  application: Application;
  nextInference?: Inference;
  overallConfidence: number;
  timestamp: Date;
}

export interface LearningMetrics {
  totalObservations: number;
  totalInferences: number;
  totalLearnings: number;
  totalAbstractions: number;
  totalApplications: number;
  successRate: number;
  averageConfidence: number;
  knowledgeGrowthRate: number;
}

// ============================================================================
// Universal Learning Loop
// ============================================================================

export class UniversalLearningLoop {
  private observations: Map<string, Observation>;
  private inferences: Map<string, Inference>;
  private learnings: Map<string, Learning>;
  private abstractions: Map<string, Abstraction>;
  private applications: Map<string, Application>;
  private cycles: Map<string, LearningCycle>;
  private knowledgeBase: Map<string, any>;

  constructor() {
    this.observations = new Map();
    this.inferences = new Map();
    this.learnings = new Map();
    this.abstractions = new Map();
    this.applications = new Map();
    this.cycles = new Map();
    this.knowledgeBase = new Map();
  }

  /**
   * Execute complete learning cycle
   */
  async executeCycle(observationContent: string, context: Record<string, any>): Promise<LearningCycle> {
    // Phase 1: Observation
    const observation = this.observe(observationContent, context);

    // Phase 2: Inference
    const inference = await this.infer(observation);

    // Phase 3: Learning
    const learning = await this.learn(inference);

    // Phase 4: Abstraction
    const abstraction = await this.abstract(learning);

    // Phase 5: Application
    const application = await this.apply(abstraction, context);

    // Phase 6: Next Inference (continuous learning)
    const nextInference = application.success
      ? await this.inferFromResult(application)
      : undefined;

    // Calculate overall confidence
    const overallConfidence = this.calculateCycleConfidence(
      inference,
      learning,
      abstraction
    );

    // Create cycle
    const cycle: LearningCycle = {
      id: `cycle-${Date.now()}`,
      observation,
      inference,
      learning,
      abstraction,
      application,
      nextInference,
      overallConfidence,
      timestamp: new Date()
    };

    this.cycles.set(cycle.id, cycle);
    this.updateKnowledgeBase(cycle);

    return cycle;
  }

  /**
   * Observe
   */
  private observe(content: string, context: Record<string, any>): Observation {
    const observation: Observation = {
      id: `observation-${Date.now()}`,
      content,
      context,
      timestamp: new Date(),
      source: 'environment'
    };

    this.observations.set(observation.id, observation);
    return observation;
  }

  /**
   * Infer
   */
  private async infer(observation: Observation): Promise<Inference> {
    // Analyze observation
    const analysis = this.analyzeObservation(observation);

    // Generate reasoning
    const reasoning = this.generateReasoning(observation, analysis);

    // Draw conclusion
    const conclusion = this.drawConclusion(reasoning, analysis);

    // Calculate confidence
    const confidence = this.calculateInferenceConfidence(observation, reasoning, conclusion);

    const inference: Inference = {
      id: `inference-${Date.now()}`,
      observationId: observation.id,
      reasoning,
      conclusion,
      confidence,
      timestamp: new Date()
    };

    this.inferences.set(inference.id, inference);
    return inference;
  }

  /**
   * Analyze observation
   */
  private analyzeObservation(observation: Observation): Record<string, any> {
    return {
      content: observation.content,
      contextKeys: Object.keys(observation.context),
      contextValues: Object.values(observation.context).map(v => typeof v),
      complexity: observation.content.length
    };
  }

  /**
   * Generate reasoning
   */
  private generateReasoning(observation: Observation, analysis: Record<string, any>): string {
    return `Based on observation "${observation.content.substring(0, 50)}..." with ${analysis.contextKeys.length} context factors, I reason that the underlying pattern can be extracted through systematic analysis.`;
  }

  /**
   * Draw conclusion
   */
  private drawConclusion(reasoning: string, analysis: Record<string, any>): string {
    return `Conclusion: The observation reveals patterns that can be generalized into actionable knowledge.`;
  }

  /**
   * Calculate inference confidence
   */
  private calculateInferenceConfidence(
    observation: Observation,
    reasoning: string,
    conclusion: string
  ): number {
    let confidence = 0.7; // Base confidence

    // Boost based on context
    if (Object.keys(observation.context).length > 0) {
      confidence += 0.1;
    }

    // Boost based on reasoning quality
    if (reasoning.length > 50) {
      confidence += 0.1;
    }

    // Boost based on conclusion clarity
    if (conclusion.length > 20) {
      confidence += 0.1;
    }

    return Math.min(1, confidence);
  }

  /**
   * Learn
   */
  private async learn(inference: Inference): Promise<Learning> {
    // Extract learned concept
    const learnedConcept = this.extractConcept(inference);

    // Extract learned rule
    const learnedRule = this.extractRule(inference);

    // Calculate confidence
    const confidence = inference.confidence * 0.9;

    const learning: Learning = {
      id: `learning-${Date.now()}`,
      inferenceId: inference.id,
      learnedConcept,
      learnedRule,
      confidence,
      timestamp: new Date()
    };

    this.learnings.set(learning.id, learning);
    return learning;
  }

  /**
   * Extract concept
   */
  private extractConcept(inference: Inference): string {
    return `Concept extracted from: ${inference.conclusion}`;
  }

  /**
   * Extract rule
   */
  private extractRule(inference: Inference): string {
    return `Rule: When observation matches pattern, inference suggests ${inference.conclusion}`;
  }

  /**
   * Abstract
   */
  private async abstract(learning: Learning): Promise<Abstraction> {
    // Determine abstraction level
    const abstractionLevel = this.determineAbstractionLevel(learning);

    // Generate generalization
    const generalization = this.generateGeneralization(learning, abstractionLevel);

    const abstraction: Abstraction = {
      id: `abstraction-${Date.now()}`,
      learningId: learning.id,
      abstractedConcept: learning.learnedConcept,
      abstractionLevel,
      generalization,
      timestamp: new Date()
    };

    this.abstractions.set(abstraction.id, abstraction);
    return abstraction;
  }

  /**
   * Determine abstraction level
   */
  private determineAbstractionLevel(learning: Learning): number {
    // Higher confidence -> higher abstraction level
    if (learning.confidence > 0.9) return 4;
    if (learning.confidence > 0.8) return 3;
    if (learning.confidence > 0.7) return 2;
    return 1;
  }

  /**
   * Generate generalization
   */
  private generateGeneralization(learning: Learning, level: number): string {
    const levels = [
      'Specific instance',
      'Category pattern',
      'General principle',
      'Universal law',
      'Metaphysical truth'
    ];
    return `${levels[level - 1]}: ${learning.learnedConcept} can be generalized as ${learning.learnedRule}`;
  }

  /**
   * Apply
   */
  private async apply(abstraction: Abstraction, context: Record<string, any>): Promise<Application> {
    // Generate action
    const action = this.generateAction(abstraction, context);

    // Simulate result
    const { result, success } = this.simulateResult(action, context);

    const application: Application = {
      id: `application-${Date.now()}`,
      abstractionId: abstraction.id,
      context,
      action,
      result,
      success,
      timestamp: new Date()
    };

    this.applications.set(application.id, application);
    return application;
  }

  /**
   * Generate action
   */
  private generateAction(abstraction: Abstraction, context: Record<string, any>): string {
    return `Apply generalization: ${abstraction.generalization} in context with ${Object.keys(context).length} factors`;
  }

  /**
   * Simulate result
   */
  private simulateResult(action: string, context: Record<string, any>): {
    result: string;
    success: boolean;
  } {
    // Simulate 85% success rate
    const success = Math.random() > 0.15;
    const result = success
      ? `Action "${action.substring(0, 50)}..." executed successfully`
      : `Action "${action.substring(0, 50)}..." encountered challenges`;

    return { result, success };
  }

  /**
   * Infer from result
   */
  private async inferFromResult(application: Application): Promise<Inference> {
    const observation: Observation = {
      id: `observation-${Date.now()}`,
      content: `Application result: ${application.result}`,
      context: { success: application.success },
      timestamp: new Date(),
      source: 'application'
    };

    return this.infer(observation);
  }

  /**
   * Calculate cycle confidence
   */
  private calculateCycleConfidence(
    inference: Inference,
    learning: Learning,
    abstraction: Abstraction
  ): number {
    return (inference.confidence + learning.confidence + abstraction.abstractionLevel / 5) / 3;
  }

  /**
   * Update knowledge base
   */
  private updateKnowledgeBase(cycle: LearningCycle): void {
    // Add learned concept to knowledge base
    const key = cycle.learning.learnedConcept;
    if (this.knowledgeBase.has(key)) {
      const existing = this.knowledgeBase.get(key)!;
      this.knowledgeBase.set(key, {
        ...existing,
        applications: (existing.applications || 0) + 1,
        lastUpdated: new Date()
      });
    } else {
      this.knowledgeBase.set(key, {
        concept: key,
        rule: cycle.learning.learnedRule,
        generalization: cycle.abstraction.generalization,
        applications: 1,
        successRate: cycle.application.success ? 1 : 0,
        lastUpdated: new Date()
      });
    }
  }

  /**
   * Get knowledge base
   */
  getKnowledgeBase(): Map<string, any> {
    return this.knowledgeBase;
  }

  /**
   * Get learning metrics
   */
  getMetrics(): LearningMetrics {
    const applications = Array.from(this.applications.values());
    const successRate = applications.length > 0
      ? applications.filter(a => a.success).length / applications.length
      : 0;

    const allConfidences = [
      ...Array.from(this.inferences.values()).map(i => i.confidence),
      ...Array.from(this.learnings.values()).map(l => l.confidence)
    ];
    const avgConfidence = allConfidences.length > 0
      ? allConfidences.reduce((sum, c) => sum + c, 0) / allConfidences.length
      : 0;

    const knowledgeGrowthRate = this.observations.size > 0
      ? this.learnings.size / this.observations.size
      : 0;

    return {
      totalObservations: this.observations.size,
      totalInferences: this.inferences.size,
      totalLearnings: this.learnings.size,
      totalAbstractions: this.abstractions.size,
      totalApplications: this.applications.size,
      successRate,
      averageConfidence: avgConfidence,
      knowledgeGrowthRate
    };
  }

  /**
   * Get recent cycles
   */
  getRecentCycles(count: number = 10): LearningCycle[] {
    const cycles = Array.from(this.cycles.values())
      .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
    return cycles.slice(0, count);
  }
}