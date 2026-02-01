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
 * Intelligence Transfer Engine
 * 智慧轉移引擎 - 具備跨領域、跨文明、跨 Mesh 的智慧轉移能力
 * 
 * 核心能力：
 * - 跨領域智慧轉移
 * - 跨文明智慧轉移
 * - 跨 Mesh 智慧轉移
 */

// ============================================================================
// Data Types & Interfaces
// ============================================================================

export interface IntelligenceArtifact {
  id: string;
  name: string;
  type: 'concept' | 'strategy' | 'pattern' | 'rule' | 'solution';
  sourceContext: string;
  content: Record<string, any>;
  effectiveness: number;
  adaptability: number;
  timestamp: Date;
}

export interface TransferRequest {
  artifactId: string;
  sourceContext: string;
  targetContext: string;
  transferMode: 'domain' | 'civilization' | 'mesh' | 'universal';
  adaptationLevel?: 'minimal' | 'moderate' | 'extensive';
}

export interface TransferResult {
  id: string;
  requestId: string;
  transferredArtifact: IntelligenceArtifact;
  adaptations: Adaptation[];
  confidence: number;
  success: boolean;
  timestamp: Date;
}

export interface Adaptation {
  type: 'structural' | 'semantic' | 'contextual' | 'behavioral';
  description: string;
  reason: string;
  impact: 'low' | 'medium' | 'high';
}

export interface ContextProfile {
  id: string;
  name: string;
  type: 'domain' | 'civilization' | 'mesh';
  characteristics: Record<string, any>;
  constraints: string[];
  capabilities: string[];
}

export interface TransferHistory {
  id: string;
  artifactId: string;
  fromContext: string;
  toContext: string;
  success: boolean;
  effectiveness: number;
  timestamp: Date;
}

// ============================================================================
// Intelligence Transfer Engine
// ============================================================================

export class IntelligenceTransferEngine {
  private artifacts: Map<string, IntelligenceArtifact>;
  private transfers: Map<string, TransferResult>;
  private contexts: Map<string, ContextProfile>;
  private history: Map<string, TransferHistory>;
  private transferPatterns: Map<string, number>;

  constructor() {
    this.artifacts = new Map();
    this.transfers = new Map();
    this.contexts = new Map();
    this.history = new Map();
    this.transferPatterns = new Map();

    this.initializeDefaultContexts();
  }

  /**
   * Initialize default contexts
   */
  private initializeDefaultContexts(): void {
    const defaultContexts: ContextProfile[] = [
      {
        id: 'software-engineering',
        name: 'Software Engineering',
        type: 'domain',
        characteristics: {
          abstraction: 'high',
          modularity: 'high',
          formalism: 'high'
        },
        constraints: ['syntax', 'typing', 'performance'],
        capabilities: ['algorithmic-thinking', 'system-design', 'debugging']
      },
      {
        id: 'data-science',
        name: 'Data Science',
        type: 'domain',
        characteristics: {
          abstraction: 'medium',
          modularity: 'medium',
          formalism: 'medium'
        },
        constraints: ['data-quality', 'model-accuracy', 'interpretability'],
        capabilities: ['pattern-recognition', 'statistical-analysis', 'prediction']
      },
      {
        id: 'cognitive-mesh',
        name: 'Cognitive Mesh',
        type: 'mesh',
        characteristics: {
          abstraction: 'high',
          distribution: 'high',
          synchronization: 'high'
        },
        constraints: ['latency', 'consistency', 'scalability'],
        capabilities: ['distributed-cognition', 'knowledge-sharing', 'collaborative-reasoning']
      },
      {
        id: 'civilization-alpha',
        name: 'Civilization Alpha',
        type: 'civilization',
        characteristics: {
          governance: 'democratic',
          values: ['innovation', 'collaboration', 'transparency'],
          maturity: 0.8
        },
        constraints: ['ethical-guidelines', 'social-responsibility'],
        capabilities: ['collective-intelligence', 'adaptive-governance', 'knowledge-preservation']
      }
    ];

    defaultContexts.forEach(context => this.contexts.set(context.id, context));
  }

  /**
   * Register intelligence artifact
   */
  registerArtifact(artifact: IntelligenceArtifact): void {
    this.artifacts.set(artifact.id, artifact);
  }

  /**
   * Transfer intelligence
   */
  async transferIntelligence(request: TransferRequest): Promise<TransferResult> {
    // Get source artifact
    const artifact = this.artifacts.get(request.artifactId);
    if (!artifact) {
      throw new Error(`Artifact not found: ${request.artifactId}`);
    }

    // Get source and target contexts
    const sourceContext = this.contexts.get(request.sourceContext);
    const targetContext = this.contexts.get(request.targetContext);

    if (!sourceContext || !targetContext) {
      throw new Error(`Context not found: source=${request.sourceContext}, target=${request.targetContext}`);
    }

    // Analyze transfer feasibility
    const feasibility = this.analyzeTransferFeasibility(artifact, sourceContext, targetContext);

    // Generate adaptations
    const adaptations = this.generateAdaptations(
      artifact,
      sourceContext,
      targetContext,
      request.adaptationLevel || 'moderate'
    );

    // Create transferred artifact
    const transferredArtifact: IntelligenceArtifact = {
      id: `transferred-${Date.now()}`,
      name: `${artifact.name} (transferred to ${targetContext.name})`,
      type: artifact.type,
      sourceContext: request.targetContext,
      content: this.adaptContent(artifact.content, adaptations),
      effectiveness: artifact.effectiveness * feasibility,
      adaptability: this.calculateAdaptability(adaptations),
      timestamp: new Date()
    };

    // Calculate confidence
    const confidence = this.calculateTransferConfidence(adaptations, feasibility);

    // Determine success
    const success = confidence > 0.6;

    const result: TransferResult = {
      id: `transfer-${Date.now()}`,
      requestId: request.artifactId,
      transferredArtifact,
      adaptations,
      confidence,
      success,
      timestamp: new Date()
    };

    this.transfers.set(result.id, result);
    this.recordTransferHistory(artifact.id, request.sourceContext, request.targetContext, success, confidence);
    this.updateTransferPatterns(request.sourceContext, request.targetContext, success);

    return result;
  }

  /**
   * Analyze transfer feasibility
   */
  private analyzeTransferFeasibility(
    artifact: IntelligenceArtifact,
    sourceContext: ContextProfile,
    targetContext: ContextProfile
  ): number {
    let feasibility = 0.5;

    // Check type compatibility
    if (sourceContext.type === targetContext.type) {
      feasibility += 0.2;
    }

    // Check capability overlap
    const sourceCapabilities = new Set(sourceContext.capabilities);
    const targetCapabilities = new Set(targetContext.capabilities);
    let overlap = 0;
    for (const capability of sourceCapabilities) {
      if (targetCapabilities.has(capability)) overlap++;
    }
    feasibility += (overlap / Math.max(sourceCapabilities.size, targetCapabilities.size)) * 0.3;

    // Check artifact adaptability
    feasibility += artifact.adaptability * 0.2;

    return Math.min(1, feasibility);
  }

  /**
   * Generate adaptations
   */
  private generateAdaptations(
    artifact: IntelligenceArtifact,
    sourceContext: ContextProfile,
    targetContext: ContextProfile,
    adaptationLevel: 'minimal' | 'moderate' | 'extensive'
  ): Adaptation[] {
    const adaptations: Adaptation[] = [];

    // Structural adaptations
    if (adaptationLevel !== 'minimal') {
      adaptations.push({
        type: 'structural',
        description: `Restructure for ${targetContext.name} context`,
        reason: 'Context-specific structural requirements',
        impact: 'medium'
      });
    }

    // Semantic adaptations
    adaptations.push({
      type: 'semantic',
      description: `Translate semantics from ${sourceContext.name} to ${targetContext.name}`,
      reason: 'Semantic alignment between contexts',
      impact: 'high'
    });

    // Contextual adaptations
    if (adaptationLevel === 'extensive') {
      adaptations.push({
        type: 'contextual',
        description: `Integrate with ${targetContext.name} characteristics`,
        reason: 'Full contextual integration',
        impact: 'high'
      });
    }

    // Behavioral adaptations
    adaptations.push({
      type: 'behavioral',
      description: `Align with ${targetContext.name} constraints`,
      reason: 'Constraint compliance',
      impact: adaptationLevel === 'minimal' ? 'low' : 'medium'
    });

    return adaptations;
  }

  /**
   * Adapt content
   */
  private adaptContent(
    originalContent: Record<string, any>,
    adaptations: Adaptation[]
  ): Record<string, any> {
    const adaptedContent: Record<string, any> = { ...originalContent };

    for (const adaptation of adaptations) {
      switch (adaptation.type) {
        case 'semantic':
          adaptedContent.adaptedSemantics = true;
          adaptedContent.semanticChanges = adaptation.description;
          break;
        case 'structural':
          adaptedContent.restructured = true;
          adaptedContent.structuralChanges = adaptation.description;
          break;
        case 'contextual':
          adaptedContent.contextuallyIntegrated = true;
          adaptedContent.contextualChanges = adaptation.description;
          break;
        case 'behavioral':
          adaptedContent.behaviorallyAligned = true;
          adaptedContent.behavioralChanges = adaptation.description;
          break;
      }
    }

    return adaptedContent;
  }

  /**
   * Calculate adaptability
   */
  private calculateAdaptability(adaptations: Adaptation[]): number {
    const impactWeights = { low: 0.5, medium: 0.75, high: 1.0 };
    const totalImpact = adaptations.reduce((sum, a) => sum + impactWeights[a.impact], 0);
    return Math.min(1, totalImpact / adaptations.length);
  }

  /**
   * Calculate transfer confidence
   */
  private calculateTransferConfidence(adaptations: Adaptation[], feasibility: number): number {
    const adaptationQuality = adaptations.length > 0 ? 0.8 : 0.5;
    return (feasibility + adaptationQuality) / 2;
  }

  /**
   * Record transfer history
   */
  private recordTransferHistory(
    artifactId: string,
    fromContext: string,
    toContext: string,
    success: boolean,
    effectiveness: number
  ): void {
    const history: TransferHistory = {
      id: `history-${Date.now()}`,
      artifactId,
      fromContext,
      toContext,
      success,
      effectiveness,
      timestamp: new Date()
    };

    this.history.set(history.id, history);
  }

  /**
   * Update transfer patterns
   */
  private updateTransferPatterns(
    fromContext: string,
    toContext: string,
    success: boolean
  ): void {
    const key = `${fromContext}->${toContext}`;
    const current = this.transferPatterns.get(key) || 0;
    this.transferPatterns.set(key, current + (success ? 1 : 0));
  }

  /**
   * Create intelligence artifact
   */
  async createArtifact(
    name: string,
    type: IntelligenceArtifact['type'],
    sourceContext: string,
    content: Record<string, any>
  ): Promise<IntelligenceArtifact> {
    const artifact: IntelligenceArtifact = {
      id: `artifact-${Date.now()}`,
      name,
      type,
      sourceContext,
      content,
      effectiveness: 0.8,
      adaptability: 0.8,
      timestamp: new Date()
    };

    this.artifacts.set(artifact.id, artifact);
    return artifact;
  }

  /**
   * Get transfer statistics
   */
  getStatistics(): {
    totalArtifacts: number;
    totalTransfers: number;
    totalContexts: number;
    successRate: number;
    averageEffectiveness: number;
    mostCommonTransfers: Array<{ path: string; count: number }>;
  } {
    const transfers = Array.from(this.transfers.values());
    const successRate = transfers.length > 0
      ? transfers.filter(t => t.success).length / transfers.length
      : 0;

    const avgEffectiveness = transfers.length > 0
      ? transfers.reduce((sum, t) => sum + t.transferredArtifact.effectiveness, 0) / transfers.length
      : 0;

    const mostCommonTransfers = Array.from(this.transferPatterns.entries())
      .map(([path, count]) => ({ path, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);

    return {
      totalArtifacts: this.artifacts.size,
      totalTransfers: this.transfers.size,
      totalContexts: this.contexts.size,
      successRate,
      averageEffectiveness: avgEffectiveness,
      mostCommonTransfers
    };
  }

  /**
   * Get transfer history
   */
  getTransferHistory(): TransferHistory[] {
    return Array.from(this.history.values())
      .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
  }
}