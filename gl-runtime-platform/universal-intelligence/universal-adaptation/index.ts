/**
 * Universal Adaptation Engine
 * 通用適應引擎 - 具備適應任何環境、規則、文明、任務的能力
 * 
 * 核心能力：
 * - 適應新環境
 * - 適應新規則
 * - 適應新文明
 * - 適應新任務
 */

// ============================================================================
// Data Types & Interfaces
// ============================================================================

export interface Environment {
  id: string;
  name: string;
  type: string;
  characteristics: Record<string, any>;
  constraints: string[];
  opportunities: string[];
  stability: number;
}

export interface AdaptationRequest {
  targetType: 'environment' | 'rules' | 'civilization' | 'task';
  targetId: string;
  currentContext: Record<string, any>;
  newContext: Record<string, any>;
  requirements?: string[];
}

export interface Adaptation {
  id: string;
  targetType: AdaptationRequest['targetType'];
  targetId: string;
  adaptations: AdaptationChange[];
  confidence: number;
  effectiveness?: number;
  timestamp: Date;
}

export interface AdaptationChange {
  type: 'behavioral' | 'structural' | 'strategic' | 'cognitive';
  description: string;
  reason: string;
  impact: 'low' | 'medium' | 'high';
}

export interface Rule {
  id: string;
  name: string;
  description: string;
  domain: string;
  constraints: string[];
  priority: number;
}

export interface Civilization {
  id: string;
  name: string;
  values: string[];
  norms: string[];
  governance: string;
  maturity: number;
}

export interface Task {
  id: string;
  name: string;
  type: string;
  requirements: string[];
  constraints: string[];
  context: Record<string, any>;
}

export interface AdaptationModel {
  id: string;
  environment: string;
  rules: Rule[];
  civilization: Civilization;
  tasks: Task[];
  adaptationHistory: Adaptation[];
  successRate: number;
}

// ============================================================================
// Universal Adaptation Engine
// ============================================================================

export class UniversalAdaptationEngine {
  private environments: Map<string, Environment>;
  private rules: Map<string, Rule>;
  private civilizations: Map<string, Civilization>;
  private tasks: Map<string, Task>;
  private adaptations: Map<string, Adaptation>;
  private adaptationModels: Map<string, AdaptationModel>;

  constructor() {
    this.environments = new Map();
    this.rules = new Map();
    this.civilizations = new Map();
    this.tasks = new Map();
    this.adaptations = new Map();
    this.adaptationModels = new Map();

    this.initializeDefaultEnvironments();
  }

  /**
   * Initialize default environments
   */
  private initializeDefaultEnvironments(): void {
    const defaultEnvironments: Environment[] = [
      {
        id: 'development',
        name: 'Development Environment',
        type: 'software',
        characteristics: {
          stability: 0.9,
          resourceAvailability: 0.8,
          complexity: 0.6
        },
        constraints: ['local execution', 'debugging enabled'],
        opportunities: ['rapid iteration', 'flexible changes'],
        stability: 0.9
      },
      {
        id: 'production',
        name: 'Production Environment',
        type: 'software',
        characteristics: {
          stability: 0.95,
          resourceAvailability: 0.9,
          complexity: 0.8
        },
        constraints: ['high availability', 'performance requirements'],
        opportunities: ['scale', 'real-world feedback'],
        stability: 0.95
      },
      {
        id: 'research',
        name: 'Research Environment',
        type: 'academic',
        characteristics: {
          stability: 0.7,
          resourceAvailability: 0.9,
          complexity: 0.9
        },
        constraints: ['experimental', 'uncertainty'],
        opportunities: ['innovation', 'discovery'],
        stability: 0.7
      }
    ];

    defaultEnvironments.forEach(env => this.environments.set(env.id, env));
  }

  /**
   * Adapt to environment
   */
  async adaptToEnvironment(
    environmentId: string,
    currentContext: Record<string, any>
  ): Promise<Adaptation> {
    const environment = this.environments.get(environmentId);
    if (!environment) {
      throw new Error(`Environment not found: ${environmentId}`);
    }

    const adaptations = this.generateEnvironmentAdaptations(environment, currentContext);
    const confidence = this.calculateAdaptationConfidence(adaptations);

    const adaptation: Adaptation = {
      id: `adaptation-${Date.now()}`,
      targetType: 'environment',
      targetId: environmentId,
      adaptations,
      confidence,
      timestamp: new Date()
    };

    this.adaptations.set(adaptation.id, adaptation);
    return adaptation;
  }

  /**
   * Generate environment adaptations
   */
  private generateEnvironmentAdaptations(
    environment: Environment,
    currentContext: Record<string, any>
  ): AdaptationChange[] {
    const changes: AdaptationChange[] = [];

    // Behavioral adaptations
    changes.push({
      type: 'behavioral',
      description: `Adjust behavior for ${environment.type} environment`,
      reason: environment.type === 'production' ? 'Ensure stability' : 'Enable flexibility',
      impact: environment.stability > 0.8 ? 'high' : 'medium'
    });

    // Structural adaptations
    changes.push({
      type: 'structural',
      description: `Optimize structure for environment characteristics`,
      reason: 'Match environment complexity and stability',
      impact: 'medium'
    });

    // Strategic adaptations
    changes.push({
      type: 'strategic',
      description: `Leverage opportunities: ${environment.opportunities.join(', ')}`,
      reason: 'Maximize environment advantages',
      impact: 'high'
    });

    return changes;
  }

  /**
   * Adapt to rules
   */
  async adaptToRules(
    rules: Rule[],
    currentContext: Record<string, any>
  ): Promise<Adaptation> {
    const adaptations = this.generateRuleAdaptations(rules, currentContext);
    const confidence = this.calculateAdaptationConfidence(adaptations);

    const adaptation: Adaptation = {
      id: `adaptation-${Date.now()}`,
      targetType: 'rules',
      targetId: rules.map(r => r.id).join(','),
      adaptations,
      confidence,
      timestamp: new Date()
    };

    this.adaptations.set(adaptation.id, adaptation);
    return adaptation;
  }

  /**
   * Generate rule adaptations
   */
  private generateRuleAdaptations(
    rules: Rule[],
    currentContext: Record<string, any>
  ): AdaptationChange[] {
    const changes: AdaptationChange[] = [];

    // Sort rules by priority
    const sortedRules = [...rules].sort((a, b) => b.priority - a.priority);

    for (const rule of sortedRules) {
      changes.push({
        type: 'behavioral',
        description: `Comply with rule: ${rule.name}`,
        reason: rule.description,
        impact: rule.priority > 0.8 ? 'high' : 'medium'
      });

      if (rule.constraints.length > 0) {
        changes.push({
          type: 'structural',
          description: `Implement constraints: ${rule.constraints.join(', ')}`,
          reason: `Rule domain: ${rule.domain}`,
          impact: 'high'
        });
      }
    }

    return changes;
  }

  /**
   * Adapt to civilization
   */
  async adaptToCivilization(
    civilizationId: string,
    currentContext: Record<string, any>
  ): Promise<Adaptation> {
    let civilization = this.civilizations.get(civilizationId);
    if (!civilization) {
      // Create new civilization if not exists
      const newCivilization: Civilization = {
        id: civilizationId,
        name: `Civilization ${civilizationId}`,
        values: [],
        norms: [],
        governance: 'autonomous',
        maturity: 0.5
      };
      this.civilizations.set(civilizationId, newCivilization);
      civilization = newCivilization;
    }

    const adaptations = this.generateCivilizationAdaptations(civilization, currentContext);
    const confidence = this.calculateAdaptationConfidence(adaptations);

    const adaptation: Adaptation = {
      id: `adaptation-${Date.now()}`,
      targetType: 'civilization',
      targetId: civilizationId,
      adaptations,
      confidence,
      timestamp: new Date()
    };

    this.adaptations.set(adaptation.id, adaptation);
    return adaptation;
  }

  /**
   * Generate civilization adaptations
   */
  private generateCivilizationAdaptations(
    civilization: Civilization,
    currentContext: Record<string, any>
  ): AdaptationChange[] {
    const changes: AdaptationChange[] = [];

    // Value alignment
    if (civilization.values.length > 0) {
      changes.push({
        type: 'cognitive',
        description: `Align with values: ${civilization.values.join(', ')}`,
        reason: 'Civilization value integration',
        impact: 'high'
      });
    }

    // Norm adherence
    if (civilization.norms.length > 0) {
      changes.push({
        type: 'behavioral',
        description: `Adhere to norms: ${civilization.norms.join(', ')}`,
        reason: 'Civilization norm compliance',
        impact: 'high'
      });
    }

    // Governance integration
    changes.push({
      type: 'strategic',
      description: `Integrate with ${civilization.governance} governance`,
      reason: 'Civilization governance alignment',
      impact: 'high'
    });

    return changes;
  }

  /**
   * Adapt to task
   */
  async adaptToTask(
    taskId: string,
    currentContext: Record<string, any>
  ): Promise<Adaptation> {
    const task = this.tasks.get(taskId);
    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }

    const adaptations = this.generateTaskAdaptations(task, currentContext);
    const confidence = this.calculateAdaptationConfidence(adaptations);

    const adaptation: Adaptation = {
      id: `adaptation-${Date.now()}`,
      targetType: 'task',
      targetId: taskId,
      adaptations,
      confidence,
      timestamp: new Date()
    };

    this.adaptations.set(adaptation.id, adaptation);
    return adaptation;
  }

  /**
   * Generate task adaptations
   */
  private generateTaskAdaptations(
    task: Task,
    currentContext: Record<string, any>
  ): AdaptationChange[] {
    const changes: AdaptationChange[] = [];

    // Requirement fulfillment
    changes.push({
      type: 'behavioral',
      description: `Fulfill requirements: ${task.requirements.join(', ')}`,
      reason: 'Task requirement compliance',
      impact: 'high'
    });

    // Constraint handling
    if (task.constraints.length > 0) {
      changes.push({
        type: 'structural',
        description: `Handle constraints: ${task.constraints.join(', ')}`,
        reason: 'Task constraint management',
        impact: 'medium'
      });
    }

    // Context integration
    if (Object.keys(task.context).length > 0) {
      changes.push({
        type: 'strategic',
        description: `Integrate task context: ${Object.keys(task.context).join(', ')}`,
        reason: 'Context-aware execution',
        impact: 'high'
      });
    }

    return changes;
  }

  /**
   * Calculate adaptation confidence
   */
  private calculateAdaptationConfidence(adaptations: AdaptationChange[]): number {
    if (adaptations.length === 0) return 0;

    const impactWeights = { low: 0.5, medium: 0.75, high: 1.0 };
    const totalImpact = adaptations.reduce((sum, change) => {
      return sum + impactWeights[change.impact];
    }, 0);

    return Math.min(1, totalImpact / adaptations.length);
  }

  /**
   * Register environment
   */
  registerEnvironment(environment: Environment): void {
    this.environments.set(environment.id, environment);
  }

  /**
   * Register rule
   */
  registerRule(rule: Rule): void {
    this.rules.set(rule.id, rule);
  }

  /**
   * Register civilization
   */
  registerCivilization(civilization: Civilization): void {
    this.civilizations.set(civilization.id, civilization);
  }

  /**
   * Register task
   */
  registerTask(task: Task): void {
    this.tasks.set(task.id, task);
  }

  /**
   * Get adaptation statistics
   */
  getStatistics(): {
    totalEnvironments: number;
    totalRules: number;
    totalCivilizations: number;
    totalTasks: number;
    totalAdaptations: number;
    averageAdaptationConfidence: number;
  } {
    const adaptations = Array.from(this.adaptations.values());
    const avgConfidence = adaptations.length > 0
      ? adaptations.reduce((sum, a) => sum + a.confidence, 0) / adaptations.length
      : 0;

    return {
      totalEnvironments: this.environments.size,
      totalRules: this.rules.size,
      totalCivilizations: this.civilizations.size,
      totalTasks: this.tasks.size,
      totalAdaptations: this.adaptations.size,
      averageAdaptationConfidence: avgConfidence
    };
  }
}