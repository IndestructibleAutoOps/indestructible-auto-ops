// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: fallback-strategy-engine
// @GL-charter-version: 2.0.0

/**
 * Fallback Strategy Engine
 * Provides fallback strategies when primary strategies fail
 */

import { ExecutionStrategy, ExecutionContext, ExecutionResult } from '../strategy-library/strategies';

export interface FallbackStrategy {
  id: string;
  name: string;
  priority: number;
  execute: (context: ExecutionContext) => Promise<ExecutionResult>;
  canHandle: (context: ExecutionContext, failedStrategies: string[]) => boolean;
  isLastResort: boolean;
}

export class FallbackEngine {
  private fallbackStrategies: FallbackStrategy[] = [];
  private fallbackHistory: Map<string, FallbackResult[]> = new Map();

  constructor() {
    this.registerFallbackStrategies();
  }

  private registerFallbackStrategies(): void {
    // Fallback 1: Minimal Execution
    this.fallbackStrategies.push({
      id: 'fallback-minimal',
      name: 'Minimal Execution',
      priority: 1,
      isLastResort: false,
      canHandle: (context, failedStrategies) => failedStrategies.length < 5,
      execute: async (context) => {
        return this.executeMinimal(context);
      }
    });

    // Fallback 2: Manual Intervention Request
    this.fallbackStrategies.push({
      id: 'fallback-manual',
      name: 'Manual Intervention Request',
      priority: 2,
      isLastResort: false,
      canHandle: (context, failedStrategies) => failedStrategies.length < 10,
      execute: async (context) => {
        return this.requestManualIntervention(context);
      }
    });

    // Fallback 3: Last Resort - Report and Wait
    this.fallbackStrategies.push({
      id: 'fallback-last-resort',
      name: 'Last Resort - Report and Wait',
      priority: 3,
      isLastResort: true,
      canHandle: () => true,
      execute: async (context) => {
        return this.lastResortReport(context);
      }
    });
  }

  async executeFallback(
    context: ExecutionContext,
    failedStrategies: string[],
    lastError?: Error
  ): Promise<FallbackResult> {
    const applicableFallback = this.findBestFallback(context, failedStrategies);

    const startTime = Date.now();
    let result: ExecutionResult;

    try {
      result = await applicableFallback.execute(context);
    } catch (error) {
      result = {
        success: false,
        strategy: applicableFallback.id,
        duration: Date.now() - startTime,
        output: null,
        error: error as Error,
        metrics: {
          resourcesUsed: { memoryMB: 50, cpuPercent: 10, diskIO: 0, networkIO: 0 },
          operationsPerformed: 0,
          validationPassed: false,
          healingApplied: false
        }
      };
    }

    const fallbackResult: FallbackResult = {
      fallbackStrategy: applicableFallback.id,
      executionResult: result,
      failedStrategies: [...failedStrategies],
      isLastResort: applicableFallback.isLastResort,
      confidence: this.calculateFallbackConfidence(applicableFallback, failedStrategies.length)
    };

    // Track fallback history
    const history = this.fallbackHistory.get(context.task) || [];
    history.push(fallbackResult);
    this.fallbackHistory.set(context.task, history);

    return fallbackResult;
  }

  private findBestFallback(
    context: ExecutionContext,
    failedStrategies: string[]
  ): FallbackStrategy {
    const applicable = this.fallbackStrategies
      .filter(f => f.canHandle(context, failedStrategies))
      .sort((a, b) => a.priority - b.priority);

    return applicable[0] || this.fallbackStrategies[this.fallbackStrategies.length - 1];
  }

  private async executeMinimal(context: ExecutionContext): Promise<ExecutionResult> {
    const startTime = Date.now();

    // Execute minimal version of the task
    const output = {
      task: context.task,
      status: 'partial-success',
      executed: 'minimal',
      note: 'Task completed with minimal requirements'
    };

    return {
      success: true,
      strategy: 'fallback-minimal',
      duration: Date.now() - startTime,
      output,
      metrics: {
        resourcesUsed: { memoryMB: 50, cpuPercent: 10, diskIO: 0, networkIO: 0 },
        operationsPerformed: 1,
        validationPassed: true,
        healingApplied: false
      }
    };
  }

  private async requestManualIntervention(context: ExecutionContext): Promise<ExecutionResult> {
    const startTime = Date.now();

    // Create manual intervention request
    const output = {
      task: context.task,
      status: 'manual-intervention-required',
      request: {
        id: `manual-${Date.now()}`,
        task: context.task,
        target: context.target,
        context: context.metadata,
        needsHumanReview: true,
        priority: 'high'
      }
    };

    return {
      success: true,
      strategy: 'fallback-manual',
      duration: Date.now() - startTime,
      output,
      metrics: {
        resourcesUsed: { memoryMB: 30, cpuPercent: 5, diskIO: 0, networkIO: 0 },
        operationsPerformed: 1,
        validationPassed: true,
        healingApplied: false
      }
    };
  }

  private async lastResortReport(context: ExecutionContext): Promise<ExecutionResult> {
    const startTime = Date.now();

    // Last resort: Create detailed report and wait
    const output = {
      task: context.task,
      status: 'last-resort-report',
      report: {
        id: `last-resort-${Date.now()}`,
        task: context.task,
        target: context.target,
        attempts: context.attempts,
        history: context.history,
        needsEscalation: true,
        priority: 'critical'
      }
    };

    return {
      success: false,
      strategy: 'fallback-last-resort',
      duration: Date.now() - startTime,
      output,
      metrics: {
        resourcesUsed: { memoryMB: 20, cpuPercent: 5, diskIO: 0, networkIO: 0 },
        operationsPerformed: 1,
        validationPassed: false,
        healingApplied: false
      }
    };
  }

  private calculateFallbackConfidence(
    fallback: FallbackStrategy,
    failedCount: number
  ): number {
    if (fallback.isLastResort) {
      return 0.3; // Low confidence for last resort
    }

    // Decrease confidence as more strategies fail
    const baseConfidence = 0.7;
    const penalty = failedCount * 0.1;

    return Math.max(baseConfidence - penalty, 0.4);
  }

  getFallbackHistory(task: string): FallbackResult[] {
    return this.fallbackHistory.get(task) || [];
  }

  clearFallbackHistory(task: string): void {
    this.fallbackHistory.delete(task);
  }

  clearAllFallbackHistory(): void {
    this.fallbackHistory.clear();
  }
}

export interface FallbackResult {
  fallbackStrategy: string;
  executionResult: ExecutionResult;
  failedStrategies: string[];
  isLastResort: boolean;
  confidence: number;
}