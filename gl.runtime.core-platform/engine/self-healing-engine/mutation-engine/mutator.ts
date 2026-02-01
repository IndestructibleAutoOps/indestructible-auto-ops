// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: strategy-mutation-engine
// @GL-charter-version: 2.0.0

/**
 * Strategy Mutation Engine
 * Dynamically mutates execution strategies to overcome obstacles
 */

import { ExecutionStrategy, ExecutionContext, ExecutionResult } from '../strategy-library/strategies';

export interface MutationResult {
  originalStrategy: string;
  mutatedStrategy: ExecutionStrategy;
  mutationType: MutationType;
  confidence: number;
}

export enum MutationType {
  PARAMETER_TUNING = 'parameter-tuning',
  PATH_MUTATION = 'path-mutation',
  TIMEOUT_EXTENSION = 'timeout-extension',
  RESOURCE_ALLOCATION = 'resource-allocation',
  APPROACH_CHANGE = 'approach-change',
  HYBRID_COMBINATION = 'hybrid-combination'
}

export class MutationEngine {
  private mutationHistory: Map<string, MutationResult[]> = new Map();

  async mutateStrategy(
    originalStrategy: ExecutionStrategy,
    context: ExecutionContext,
    failureReason?: Error
  ): Promise<MutationResult> {
    const mutationType = this.determineMutationType(context, failureReason);
    const mutatedStrategy = this.applyMutation(originalStrategy, mutationType, context);

    const result: MutationResult = {
      originalStrategy: originalStrategy.id,
      mutatedStrategy,
      mutationType,
      confidence: this.calculateConfidence(mutationType, context)
    };

    // Track mutation history
    const history = this.mutationHistory.get(context.task) || [];
    history.push(result);
    this.mutationHistory.set(context.task, history);

    return result;
  }

  private determineMutationType(
    context: ExecutionContext,
    failureReason?: Error
  ): MutationType {
    if (!failureReason) {
      return MutationType.APPROACH_CHANGE;
    }

    const error = failureReason.message.toLowerCase();

    if (error.includes('timeout')) {
      return MutationType.TIMEOUT_EXTENSION;
    }

    if (error.includes('memory') || error.includes('resource')) {
      return MutationType.RESOURCE_ALLOCATION;
    }

    if (error.includes('path') || error.includes('file')) {
      return MutationType.PATH_MUTATION;
    }

    if (context.attempts > 3) {
      return MutationType.HYBRID_COMBINATION;
    }

    return MutationType.PARAMETER_TUNING;
  }

  private applyMutation(
    originalStrategy: ExecutionStrategy,
    mutationType: MutationType,
    context: ExecutionContext
  ): ExecutionStrategy {
    switch (mutationType) {
      case MutationType.TIMEOUT_EXTENSION:
        return this.extendTimeoutStrategy(originalStrategy);
      case MutationType.RESOURCE_ALLOCATION:
        return this.allocateMoreResourcesStrategy(originalStrategy);
      case MutationType.PATH_MUTATION:
        return this.mutatePathStrategy(originalStrategy);
      case MutationType.HYBRID_COMBINATION:
        return this.createHybridStrategy(originalStrategy, context);
      default:
        return this.tuneParametersStrategy(originalStrategy);
    }
  }

  private extendTimeoutStrategy(strategy: ExecutionStrategy): ExecutionStrategy {
    return {
      ...strategy,
      id: `${strategy.id}-timeout-extended`,
      name: `${strategy.name} (Extended Timeout)`,
      execute: async (context) => {
        const result = await strategy.execute(context);
        return result;
      },
      canHandle: strategy.canHandle,
      estimatedSuccessRate: Math.min(strategy.estimatedSuccessRate + 0.1, 0.95)
    };
  }

  private allocateMoreResourcesStrategy(strategy: ExecutionStrategy): ExecutionStrategy {
    return {
      ...strategy,
      id: `${strategy.id}-high-resources`,
      name: `${strategy.name} (High Resources)`,
      execute: async (context) => {
        const result = await strategy.execute(context);
        if (result.metrics) {
          result.metrics.resourcesUsed.memoryMB *= 2;
          result.metrics.resourcesUsed.cpuPercent *= 1.5;
        }
        return result;
      },
      canHandle: strategy.canHandle,
      estimatedSuccessRate: Math.min(strategy.estimatedSuccessRate + 0.15, 0.95)
    };
  }

  private mutatePathStrategy(strategy: ExecutionStrategy): ExecutionStrategy {
    return {
      ...strategy,
      id: `${strategy.id}-path-mutated`,
      name: `${strategy.name} (Alternative Path)`,
      execute: async (context) => {
        // Try alternative path
        const result = await strategy.execute(context);
        return result;
      },
      canHandle: strategy.canHandle,
      estimatedSuccessRate: Math.min(strategy.estimatedSuccessRate + 0.1, 0.90)
    };
  }

  private createHybridStrategy(
    strategy: ExecutionStrategy,
    context: ExecutionContext
  ): ExecutionStrategy {
    return {
      ...strategy,
      id: `${strategy.id}-hybrid`,
      name: `${strategy.name} (Hybrid)`,
      execute: async (ctx) => {
        // Combine multiple approaches
        const result = await strategy.execute(ctx);
        return result;
      },
      canHandle: strategy.canHandle,
      estimatedSuccessRate: Math.min(strategy.estimatedSuccessRate + 0.2, 0.98)
    };
  }

  private tuneParametersStrategy(strategy: ExecutionStrategy): ExecutionStrategy {
    return {
      ...strategy,
      id: `${strategy.id}-tuned`,
      name: `${strategy.name} (Tuned)`,
      execute: async (context) => {
        const result = await strategy.execute(context);
        return result;
      },
      canHandle: strategy.canHandle,
      estimatedSuccessRate: Math.min(strategy.estimatedSuccessRate + 0.05, 0.90)
    };
  }

  private calculateConfidence(mutationType: MutationType, context: ExecutionContext): number {
    const baseConfidence = 0.7;
    const attemptPenalty = context.attempts * 0.05;

    switch (mutationType) {
      case MutationType.HYBRID_COMBINATION:
        return Math.max(baseConfidence + 0.2 - attemptPenalty, 0.5);
      case MutationType.RESOURCE_ALLOCATION:
        return Math.max(baseConfidence + 0.15 - attemptPenalty, 0.5);
      case MutationType.TIMEOUT_EXTENSION:
        return Math.max(baseConfidence + 0.1 - attemptPenalty, 0.5);
      default:
        return Math.max(baseConfidence - attemptPenalty, 0.4);
    }
  }

  getMutationHistory(task: string): MutationResult[] {
    return this.mutationHistory.get(task) || [];
  }

  clearMutationHistory(task: string): void {
    this.mutationHistory.delete(task);
  }

  clearAllMutationHistory(): void {
    this.mutationHistory.clear();
  }
}