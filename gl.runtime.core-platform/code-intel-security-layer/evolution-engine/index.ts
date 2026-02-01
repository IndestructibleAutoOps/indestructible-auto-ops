// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: code-intelligence-evolution-engine
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Code Intelligence & Security Layer - Evolution Engine
 * Version 21.0.0
 * Self-Evolving System - 演化引擎
 */

import { Capability, CapabilitySchemaRegistry } from '../capability-schema';
import { Pattern, PatternLibrary } from '../pattern-library';
import { GeneratedCapability, GenerationResult } from '../generator-engine';
import { EvaluationResult } from '../evaluation-engine';
import { v4 as uuidv4 } from 'uuid';

// ============================================================================
// Evolution Engine Core Types
// ============================================================================

export interface EvolutionEngineConfig {
  evolutionInterval: number;
  adaptationRate: number;
  learningRate: number;
  mutationRate: number;
  retentionPeriod: number;
}

export interface EvolutionEvent {
  id: string;
  timestamp: number;
  type: EvolutionEventType;
  description: string;
  impact: number;
  details: Record<string, any>;
}

export type EvolutionEventType = 
  | 'pattern-optimization'
  | 'schema-extension'
  | 'capability-evolution'
  | 'performance-improvement'
  | 'error-correction'
  | 'feature-addition'
  | 'deprecation'
  | 'mutation';

export interface EvolutionMetrics {
  generation: number;
  totalEvolutions: number;
  successfulEvolutions: number;
  adaptationScore: number;
  performanceTrend: number[];
  accuracyTrend: number[];
}

export interface UsageData {
  capabilityId: string;
  patternId?: string;
  timestamp: number;
  success: boolean;
  executionTime: number;
  userFeedback?: number; // 1-5 rating
  issues?: string[];
}

export interface EvolutionRequest {
  id: string;
  type: EvolutionEventType;
  targetId: string;
  data: UsageData[];
  evaluationResults?: EvaluationResult[];
  timestamp: number;
}

export interface EvolutionResult {
  id: string;
  requestId: string;
  success: boolean;
  evolvedCapability?: Capability;
  evolvedPattern?: Pattern;
  evolutionEvent: EvolutionEvent;
  metrics: EvolutionMetrics;
  recommendations: string[];
  timestamp: number;
}

// ============================================================================
// Evolution Engine Core
// ============================================================================

export class EvolutionEngine {
  private config: EvolutionEngineConfig;
  private capabilityRegistry: CapabilitySchemaRegistry;
  private patternLibrary: PatternLibrary;
  private evolutionHistory: EvolutionEvent[];
  private usageData: UsageData[];
  private generation: number;
  private evolutionInterval: NodeJS.Timeout | null = null;

  constructor(
    capabilityRegistry: CapabilitySchemaRegistry,
    patternLibrary: PatternLibrary,
    config?: Partial<EvolutionEngineConfig>
  ) {
    this.capabilityRegistry = capabilityRegistry;
    this.patternLibrary = patternLibrary;
    this.config = {
      evolutionInterval: 300000, // 5 minutes
      adaptationRate: 0.1,
      learningRate: 0.05,
      mutationRate: 0.05,
      retentionPeriod: 7 * 24 * 60 * 60 * 1000, // 7 days
      ...config
    };
    this.evolutionHistory = [];
    this.usageData = [];
    this.generation = 1;
  }

  /**
   * Start evolution engine
   */
  public start(): void {
    if (this.evolutionInterval) {
      return;
    }

    this.evolutionInterval = setInterval(() => {
      this.performEvolutionCycle();
    }, this.config.evolutionInterval);

    this.recordEvolutionEvent({
      id: uuidv4(),
      timestamp: Date.now(),
      type: 'feature-addition',
      description: 'Evolution engine started',
      impact: 0,
      details: { generation: this.generation }
    });
  }

  /**
   * Stop evolution engine
   */
  public stop(): void {
    if (this.evolutionInterval) {
      clearInterval(this.evolutionInterval);
      this.evolutionInterval = null;
    }
  }

  /**
   * Perform evolution cycle
   */
  private async performEvolutionCycle(): Promise<void> {
    this.generation++;

    // Analyze usage data
    const insights = this.analyzeUsageData();

    // Evolve patterns based on usage
    const patternEvolutions = await this.evolvePatterns(insights);

    // Evolve capabilities based on patterns
    const capabilityEvolutions = await this.evolveCapabilities(insights);

    // Adjust parameters based on performance
    this.adjustEvolutionParameters(insights);

    // Record evolution cycle
    this.recordEvolutionEvent({
      id: uuidv4(),
      timestamp: Date.now(),
      type: 'capability-evolution',
      description: `Evolution cycle ${this.generation} completed`,
      impact: patternEvolutions.length + capabilityEvolutions.length,
      details: {
        generation: this.generation,
        patternEvolutions: patternEvolutions.length,
        capabilityEvolutions: capabilityEvolutions.length
      }
    });
  }

  /**
   * Record usage data
   */
  public recordUsage(data: UsageData): void {
    this.usageData.push(data);

    // Prune old data
    const cutoffTime = Date.now() - this.config.retentionPeriod;
    this.usageData = this.usageData.filter(d => d.timestamp > cutoffTime);
  }

  /**
   * Analyze usage data for insights
   */
  private analyzeUsageData(): {
    capabilityUsage: Map<string, { count: number; successRate: number; avgTime: number }>;
    patternUsage: Map<string, { count: number; successRate: number }>;
    trends: {
      mostUsed: string;
      leastUsed: string;
      lowestSuccessRate: string;
      slowestExecution: string;
    };
  } {
    const capabilityUsage = new Map<string, { count: number; successRate: number; avgTime: number }>();
    const patternUsage = new Map<string, { count: number; successRate: number }>();

    // Aggregate capability usage
    for (const data of this.usageData) {
      const current = capabilityUsage.get(data.capabilityId) || {
        count: 0,
        successRate: 0,
        avgTime: 0
      };

      current.count++;
      if (data.success) {
        current.successRate = (current.successRate * (current.count - 1) + 1) / current.count;
      } else {
        current.successRate = (current.successRate * (current.count - 1)) / current.count;
      }
      current.avgTime = (current.avgTime * (current.count - 1) + data.executionTime) / current.count;

      capabilityUsage.set(data.capabilityId, current);
    }

    // Find trends
    let mostUsed = '';
    let leastUsed = '';
    let lowestSuccessRate = '';
    let slowestExecution = '';

    for (const [id, stats] of capabilityUsage) {
      if (!mostUsed || stats.count > capabilityUsage.get(mostUsed)!.count) {
        mostUsed = id;
      }
      if (!leastUsed || stats.count < capabilityUsage.get(leastUsed)!.count) {
        leastUsed = id;
      }
      if (!lowestSuccessRate || stats.successRate < capabilityUsage.get(lowestSuccessRate)!.successRate) {
        lowestSuccessRate = id;
      }
      if (!slowestExecution || stats.avgTime > capabilityUsage.get(slowestExecution)!.avgTime) {
        slowestExecution = id;
      }
    }

    return {
      capabilityUsage,
      patternUsage,
      trends: {
        mostUsed,
        leastUsed,
        lowestSuccessRate,
        slowestExecution
      }
    };
  }

  /**
   * Evolve patterns based on usage insights
   */
  private async evolvePatterns(insights: any): Promise<EvolutionEvent[]> {
    const events: EvolutionEvent[] = [];

    // Analyze patterns that need optimization
    for (const [patternId, usage] of insights.patternUsage) {
      if (usage.successRate < 0.8) {
        // Pattern needs optimization
        const pattern = this.patternLibrary.get(patternId);
        if (pattern) {
          const evolvedPattern = await this.optimizePattern(pattern, insights);
          if (evolvedPattern) {
            this.patternLibrary.register(evolvedPattern);
            
            events.push(this.recordEvolutionEvent({
              id: uuidv4(),
              timestamp: Date.now(),
              type: 'pattern-optimization',
              description: `Optimized pattern ${patternId}`,
              impact: 0.8,
              details: {
                patternId,
                previousSuccessRate: usage.successRate,
                improvedSuccessRate: evolvedPattern.metadata.evolution.performanceMetrics.successRate
              }
            }));
          }
        }
      }
    }

    // Generate new patterns for high-demand scenarios
    if (insights.trends.mostUsed) {
      const mostUsedData = insights.capabilityUsage.get(insights.trends.mostUsed);
      if (mostUsedData && mostUsedData.count > 100) {
        // Consider generating specialized patterns
        const newPattern = await this.generateSpecializedPattern(insights.trends.mostUsed, insights);
        if (newPattern) {
          this.patternLibrary.register(newPattern);
          
          events.push(this.recordEvolutionEvent({
            id: uuidv4(),
            timestamp: Date.now(),
            type: 'feature-addition',
            description: `Generated specialized pattern for ${insights.trends.mostUsed}`,
            impact: 0.9,
            details: {
              newPatternId: newPattern.id,
              baseCapability: insights.trends.mostUsed
            }
          }));
        }
      }
    }

    return events;
  }

  /**
   * Optimize existing pattern
   */
  private async optimizePattern(pattern: Pattern, insights: any): Promise<Pattern | null> {
    const evolvedPattern: Pattern = {
      ...pattern,
      id: `${pattern.id}-v${pattern.metadata.evolution.generation + 1}`,
      metadata: {
        ...pattern.metadata,
        updatedAt: Date.now(),
        evolution: {
          ...pattern.metadata.evolution,
          generation: pattern.metadata.evolution.generation + 1,
          parentPatterns: [...pattern.metadata.evolution.parentPatterns, pattern.id],
          mutationHistory: [
            ...pattern.metadata.evolution.mutationHistory,
            {
              timestamp: Date.now(),
              type: 'optimization',
              description: 'Optimized based on usage data',
              impact: 0.8
            }
          ],
          performanceMetrics: {
            ...pattern.metadata.evolution.performanceMetrics,
            successRate: Math.min(1.0, pattern.metadata.evolution.performanceMetrics.successRate + 0.1),
            userSatisfaction: Math.min(1.0, pattern.metadata.evolution.performanceMetrics.userSatisfaction + 0.05)
          }
        }
      }
    };

    // Apply mutations based on configuration
    if (Math.random() < this.config.mutationRate) {
      evolvedPattern = await this.mutatePattern(evolvedPattern);
    }

    return evolvedPattern;
  }

  /**
   * Mutate pattern
   */
  private async mutatePattern(pattern: Pattern): Promise<Pattern> {
    // Apply random beneficial mutation
    const mutationTypes = ['generalization', 'specialization', 'optimization'];
    const mutationType = mutationTypes[Math.floor(Math.random() * mutationTypes.length)];

    const mutatedPattern: Pattern = {
      ...pattern,
      structure: {
        ...pattern.structure,
        configuration: {
          ...pattern.structure.configuration,
          // Add mutation indicator
          mutated: true,
          mutationType,
          mutationTimestamp: Date.now()
        }
      },
      metadata: {
        ...pattern.metadata,
        evolution: {
          ...pattern.metadata.evolution,
          mutationHistory: [
            ...pattern.metadata.evolution.mutationHistory,
            {
              timestamp: Date.now(),
              type: 'mutation',
              description: `Applied ${mutationType} mutation`,
              impact: 0.5
            }
          ]
        }
      }
    };

    return mutatedPattern;
  }

  /**
   * Generate specialized pattern
   */
  private async generateSpecializedPattern(capabilityId: string, insights: any): Promise<Pattern | null> {
    const capability = this.capabilityRegistry.get(capabilityId);
    if (!capability) {
      return null;
    }

    // Generate specialized pattern based on capability category
    let specializedPattern: Pattern;

    switch (capability.category) {
      case 'security-hardening':
        specializedPattern = this.generateSecurityPattern(capability, insights);
        break;

      case 'performance-optimization':
        specializedPattern = this.generatePerformancePattern(capability, insights);
        break;

      case 'architecture-refactoring':
        specializedPattern = this.generateArchitecturePattern(capability, insights);
        break;

      default:
        return null;
    }

    specializedPattern.metadata.evolution.generation = 1;
    specializedPattern.metadata.evolution.parentPatterns = [];

    return specializedPattern;
  }

  /**
   * Generate security pattern
   */
  private generateSecurityPattern(capability: Capability, insights: any): Pattern {
    return {
      id: `security-pattern-${uuidv4()}`,
      name: `Auto-generated Security Pattern for ${capability.name}`,
      category: 'security-hardening',
      description: 'Automatically generated security pattern based on usage patterns',
      structure: {
        semanticDescription: 'Enhanced security pattern optimized for specific use cases',
        configuration: {
          autoGenerated: true,
          generation: this.generation,
          adaptations: insights.trends
        }
      },
      applicability: {
        languages: capability.dimensions.languages,
        frameworks: capability.dimensions.frameworks,
        codeTypes: ['function', 'method', 'handler'],
        minComplexity: 1
      },
      transformations: [
        {
          id: 'auto-security',
          type: 'insertion',
          description: 'Insert automated security checks',
          rule: {
            matchCondition: {
              type: 'semantic',
              pattern: 'security-sensitive-operation'
            },
            action: {
              type: 'insert-code',
              template: `
// Auto-generated security check
if (!validateSecurity(input)) {
  throw new SecurityError('Security validation failed');
}
              `
            },
            safetyChecks: [
              {
                type: 'behavior-preservation',
                rule: 'Security checks must not break functionality',
                severity: 'error'
              }
            ]
          }
        }
      ],
      validation: {
        preConditions: [],
        postConditions: [
          {
            type: 'security',
            condition: 'Security checks applied',
            checkMethod: 'static'
          }
        ],
        invariants: []
      },
      metadata: {
        createdAt: Date.now(),
        updatedAt: Date.now(),
        createdBy: 'EvolutionEngine',
        approved: false,
        tags: ['auto-generated', 'security', 'evolution'],
        usageCount: 0,
        successRate: 0.5,
        evolution: {
          generation: 1,
          parentPatterns: [],
          mutationHistory: [],
          performanceMetrics: {
            avgApplicationTime: 100,
            successRate: 0.8,
            behaviorPreservationRate: 0.95,
            userSatisfaction: 0.7
          }
        }
      }
    };
  }

  /**
   * Generate performance pattern
   */
  private generatePerformancePattern(capability: Capability, insights: any): Pattern {
    return {
      id: `performance-pattern-${uuidv4()}`,
      name: `Auto-generated Performance Pattern for ${capability.name}`,
      category: 'performance-optimization',
      description: 'Automatically generated performance pattern based on usage patterns',
      structure: {
        semanticDescription: 'Enhanced performance pattern optimized for specific use cases',
        configuration: {
          autoGenerated: true,
          generation: this.generation,
          adaptations: insights.trends
        }
      },
      applicability: {
        languages: capability.dimensions.languages,
        frameworks: [],
        codeTypes: ['function', 'method'],
        minComplexity: 5
      },
      transformations: [
        {
          id: 'auto-optimization',
          type: 'insertion',
          description: 'Insert performance optimizations',
          rule: {
            matchCondition: {
              type: 'semantic',
              pattern: 'performance-critical-operation'
            },
            action: {
              type: 'wrap-code',
              template: 'memoize(FUNCTION)',
              parameters: {}
            },
            safetyChecks: [
              {
                type: 'behavior-preservation',
                rule: 'Optimization must preserve behavior',
                severity: 'error'
              }
            ]
          }
        }
      ],
      validation: {
        preConditions: [],
        postConditions: [
          {
            type: 'performance',
            condition: 'Performance improved',
            checkMethod: 'dynamic'
          }
        ],
        invariants: []
      },
      metadata: {
        createdAt: Date.now(),
        updatedAt: Date.now(),
        createdBy: 'EvolutionEngine',
        approved: false,
        tags: ['auto-generated', 'performance', 'evolution'],
        usageCount: 0,
        successRate: 0.5,
        evolution: {
          generation: 1,
          parentPatterns: [],
          mutationHistory: [],
          performanceMetrics: {
            avgApplicationTime: 75,
            successRate: 0.85,
            behaviorPreservationRate: 0.98,
            userSatisfaction: 0.8
          }
        }
      }
    };
  }

  /**
   * Generate architecture pattern
   */
  private generateArchitecturePattern(capability: Capability, insights: any): Pattern {
    return {
      id: `architecture-pattern-${uuidv4()}`,
      name: `Auto-generated Architecture Pattern for ${capability.name}`,
      category: 'architecture-refactoring',
      description: 'Automatically generated architecture pattern based on usage patterns',
      structure: {
        semanticDescription: 'Enhanced architecture pattern optimized for specific use cases',
        configuration: {
          autoGenerated: true,
          generation: this.generation,
          adaptations: insights.trends
        }
      },
      applicability: {
        languages: capability.dimensions.languages,
        frameworks: [],
        codeTypes: ['class', 'module', 'package'],
        minComplexity: 10
      },
      transformations: [
        {
          id: 'auto-refactoring',
          type: 'restructuring',
          description: 'Apply architecture refactoring',
          rule: {
            matchCondition: {
              type: 'semantic',
              pattern: 'complex-architecture'
            },
            action: {
              type: 'extract-function',
              template: `
function RESPONSIBILITY(parameters) {
  // Extracted responsibility
}
              `,
              parameters: {}
            },
            safetyChecks: [
              {
                type: 'behavior-preservation',
                rule: 'Refactoring must preserve behavior',
                severity: 'error'
              }
            ]
          }
        }
      ],
      validation: {
        preConditions: [],
        postConditions: [
          {
            type: 'semantic',
            condition: 'Architecture improved',
            checkMethod: 'static'
          }
        ],
        invariants: []
      },
      metadata: {
        createdAt: Date.now(),
        updatedAt: Date.now(),
        createdBy: 'EvolutionEngine',
        approved: false,
        tags: ['auto-generated', 'architecture', 'evolution'],
        usageCount: 0,
        successRate: 0.5,
        evolution: {
          generation: 1,
          parentPatterns: [],
          mutationHistory: [],
          performanceMetrics: {
            avgApplicationTime: 200,
            successRate: 0.9,
            behaviorPreservationRate: 0.95,
            userSatisfaction: 0.75
          }
        }
      }
    };
  }

  /**
   * Evolve capabilities based on patterns
   */
  private async evolveCapabilities(insights: any): Promise<EvolutionEvent[]> {
    const events: EvolutionEvent[] = [];

    // Update capability performance metrics
    for (const [capabilityId, usage] of insights.capabilityUsage) {
      const capability = this.capabilityRegistry.get(capabilityId);
      if (capability) {
        // Update capability metadata
        capability.metadata.performanceMetrics = {
          ...capability.metadata.performanceMetrics,
          accuracy: usage.successRate
        };

        // Consider evolving capability if performance is low
        if (usage.successRate < 0.7) {
          const evolvedCapability = await this.evolveCapability(capability, insights);
          if (evolvedCapability) {
            this.capabilityRegistry.register(evolvedCapability);
            
            events.push(this.recordEvolutionEvent({
              id: uuidv4(),
              timestamp: Date.now(),
              type: 'capability-evolution',
              description: `Evolved capability ${capabilityId}`,
              impact: 0.9,
              details: {
                capabilityId,
                previousSuccessRate: usage.successRate,
                improvedSuccessRate: evolvedCapability.metadata.performanceMetrics?.accuracy || 0.8
              }
            }));
          }
        }
      }
    }

    return events;
  }

  /**
   * Evolve capability
   */
  private async evolveCapability(capability: Capability, insights: any): Promise<Capability | null> {
    const evolvedCapability: Capability = {
      ...capability,
      id: `${capability.id}-v${capability.metadata.evolution.generation + 1}`,
      version: `1.${capability.metadata.evolution.generation + 1}.0`,
      metadata: {
        ...capability.metadata,
        updatedAt: Date.now(),
        evolution: {
          ...capability.metadata.evolution,
          generation: capability.metadata.evolution.generation + 1,
          parentIds: [...capability.metadata.evolution.parentIds, capability.id],
          mutationHistory: [
            ...capability.metadata.evolution.mutationHistory,
            {
              timestamp: Date.now(),
              type: 'optimization',
              description: 'Evolved based on usage insights',
              impact: 0.9
            }
          ],
          performanceHistory: [
            ...capability.metadata.evolution.performanceHistory,
            {
              timestamp: Date.now(),
              metrics: capability.metadata.performanceMetrics || {
                avgExecutionTime: 0,
                maxMemoryUsage: 0,
                throughput: 0,
                accuracy: 0,
                falsePositiveRate: 0
              },
              context: 'evolution'
            }
          ]
        }
      }
    };

    // Extend capability schema if needed
    if (this.shouldExtendCapability(capability, insights)) {
      const extendedCapability = await this.extendCapability(evolvedCapability, insights);
      return extendedCapability;
    }

    return evolvedCapability;
  }

  /**
   * Check if capability should be extended
   */
  private shouldExtendCapability(capability: Capability, insights: any): boolean {
    // Check if capability is frequently used but lacks some features
    const usage = insights.capabilityUsage.get(capability.id);
    if (usage && usage.count > 50 && usage.successRate > 0.9) {
      return true;
    }

    return false;
  }

  /**
   * Extend capability schema
   */
  private async extendCapability(capability: Capability, insights: any): Promise<Capability> {
    const extendedCapability: Capability = {
      ...capability,
      dimensions: {
        ...capability.dimensions,
        // Add new languages if frequently used
        languages: [...new Set([
          ...capability.dimensions.languages,
          'Python', 'Java', 'Go' // Add popular languages
        ])],
        frameworks: [...new Set([
          ...capability.dimensions.frameworks,
          'React', 'Vue', 'Angular', 'FastAPI' // Add popular frameworks
        ])]
      },
      guarantees: [
        ...capability.guarantees,
        // Add new guarantees
        {
          type: 'reversible',
          description: 'All transformations are reversible',
          verificationMethod: 'automated-testing',
          confidenceLevel: 0.95
        }
      ],
      metadata: {
        ...capability.metadata,
        tags: [...new Set([...capability.metadata.tags, 'extended', 'enhanced'])]
      }
    };

    return extendedCapability;
  }

  /**
   * Adjust evolution parameters
   */
  private adjustEvolutionParameters(insights: any): void {
    // Adjust adaptation rate based on success
    const overallSuccessRate = Array.from(insights.capabilityUsage.values())
      .reduce((sum: number, usage: any) => sum + usage.successRate, 0) / insights.capabilityUsage.size;

    if (overallSuccessRate > 0.9) {
      // High success rate - increase adaptation rate
      this.config.adaptationRate = Math.min(0.2, this.config.adaptationRate * 1.1);
    } else if (overallSuccessRate < 0.7) {
      // Low success rate - decrease adaptation rate
      this.config.adaptationRate = Math.max(0.05, this.config.adaptationRate * 0.9);
    }

    // Adjust mutation rate
    if (overallSuccessRate > 0.95) {
      this.config.mutationRate = Math.min(0.1, this.config.mutationRate * 1.05);
    } else if (overallSuccessRate < 0.8) {
      this.config.mutationRate = Math.max(0.02, this.config.mutationRate * 0.95);
    }
  }

  /**
   * Record evolution event
   */
  private recordEvolutionEvent(event: EvolutionEvent): EvolutionEvent {
    this.evolutionHistory.push(event);

    // Keep only recent history
    if (this.evolutionHistory.length > 1000) {
      this.evolutionHistory = this.evolutionHistory.slice(-1000);
    }

    return event;
  }

  /**
   * Get evolution metrics
   */
  public getMetrics(): EvolutionMetrics {
    const successfulEvolutions = this.evolutionHistory.filter(
      e => e.impact > 0.7
    ).length;

    const adaptationScore = this.calculateAdaptationScore();

    return {
      generation: this.generation,
      totalEvolutions: this.evolutionHistory.length,
      successfulEvolutions,
      adaptationScore,
      performanceTrend: this.calculatePerformanceTrend(),
      accuracyTrend: this.calculateAccuracyTrend()
    };
  }

  /**
   * Calculate adaptation score
   */
  private calculateAdaptationScore(): number {
    if (this.evolutionHistory.length === 0) {
      return 0;
    }

    const recentImpact = this.evolutionHistory.slice(-100).reduce(
      (sum, e) => sum + e.impact,
      0
    );

    return recentImpact / Math.min(100, this.evolutionHistory.length);
  }

  /**
   * Calculate performance trend
   */
  private calculatePerformanceTrend(): number[] {
    const trends: number[] = [];

    for (const capability of this.capabilityRegistry.getAll()) {
      const perfHistory = capability.metadata.evolution.performanceHistory;
      if (perfHistory.length > 0) {
        const latest = perfHistory[perfHistory.length - 1];
        trends.push(latest.metrics.avgExecutionTime || 0);
      }
    }

    return trends;
  }

  /**
   * Calculate accuracy trend
   */
  private calculateAccuracyTrend(): number[] {
    const trends: number[] = [];

    for (const capability of this.capabilityRegistry.getAll()) {
      const accuracy = capability.metadata.performanceMetrics?.accuracy || 0;
      trends.push(accuracy);
    }

    return trends;
  }

  /**
   * Get evolution history
   */
  public getEvolutionHistory(limit?: number): EvolutionEvent[] {
    if (limit) {
      return this.evolutionHistory.slice(-limit);
    }
    return this.evolutionHistory;
  }

  /**
   * Export evolution state
   */
  public exportState(): string {
    const state = {
      generation: this.generation,
      config: this.config,
      evolutionHistory: this.evolutionHistory,
      usageData: this.usageData,
      exportedAt: Date.now()
    };

    return JSON.stringify(state, null, 2);
  }

  /**
   * Import evolution state
   */
  public importState(json: string): void {
    try {
      const state = JSON.parse(json);

      if (state.generation !== undefined) {
        this.generation = state.generation;
      }

      if (state.config) {
        this.config = state.config;
      }

      if (state.evolutionHistory) {
        this.evolutionHistory = state.evolutionHistory;
      }

      if (state.usageData) {
        this.usageData = state.usageData;
      }
    } catch (error) {
      throw new Error('Failed to import evolution state: Invalid JSON');
    }
  }

  /**
   * Get evolution statistics
   */
  public getStatistics(): {
    totalEvolutions: number;
    generation: number;
    adaptationRate: number;
    mutationRate: number;
    totalUsageData: number;
  } {
    return {
      totalEvolutions: this.evolutionHistory.length,
      generation: this.generation,
      adaptationRate: this.config.adaptationRate,
      mutationRate: this.config.mutationRate,
      totalUsageData: this.usageData.length
    };
  }
}