// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: self-healing-orchestration-engine
// @GL-charter-version: 2.0.0

/**
 * GL Self-Healing Orchestration Engine (SHEL) v8.0.0
 * The brain of the GL Runtime Platform - enables autonomous task completion
 */

import { StrategyLibrary, ExecutionStrategy, ExecutionContext, ExecutionResult } from './strategy-library/strategies';
import { MutationEngine } from './mutation-engine/mutator';
import { FallbackEngine } from './fallback-engine/fallback';
import { RetryEngine, RetryConfig } from './retry-engine/retry';
import { ValidationLoop, ValidationConfig } from './validation-loop/validator';
import { MultiPathRunner, SelectionCriteria, PathConfig } from './multi-path-runner/runner';
import { CompletionChecker, CompletionConfig, CompletionResult } from './completion-checker/checker';
import { v4 as uuidv4 } from 'uuid';

export interface SelfHealingConfig {
  enableRetry: boolean;
  enableMutation: boolean;
  enableFallback: boolean;
  enableValidationLoop: boolean;
  enableMultiPath: boolean;
  retryConfig?: Partial<RetryConfig>;
  validationConfig?: Partial<ValidationConfig>;
  pathConfig?: Partial<PathConfig>;
  completionConfig?: Partial<CompletionConfig>;
}

export interface SelfHealingResult {
  taskId: string;
  task: string;
  completed: boolean;
  completionScore: number;
  executionResults: ExecutionResult[];
  mutationHistory: any[];
  fallbackHistory: any[];
  validationHistory: any[];
  multiPathHistory: any[];
  finalResult: ExecutionResult | null;
  completionCheck: CompletionResult | null;
  durationMs: number;
  startTime: Date;
  endTime: Date;
}

export class SelfHealingOrchestrationEngine {
  private strategyLibrary: StrategyLibrary;
  private mutationEngine: MutationEngine;
  private fallbackEngine: FallbackEngine;
  private retryEngine: RetryEngine;
  private validationLoop: ValidationLoop;
  private multiPathRunner: MultiPathRunner;
  private completionChecker: CompletionChecker;

  private executionHistory: Map<string, SelfHealingResult[]> = new Map();

  constructor() {
    this.strategyLibrary = new StrategyLibrary();
    this.mutationEngine = new MutationEngine();
    this.fallbackEngine = new FallbackEngine();
    this.retryEngine = new RetryEngine();
    this.validationLoop = new ValidationLoop();
    this.multiPathRunner = new MultiPathRunner();
    this.completionChecker = new CompletionChecker();
  }

  async executeTask(
    task: string,
    target: string,
    metadata: Record<string, any> = {},
    config?: Partial<SelfHealingConfig>
  ): Promise<SelfHealingResult> {
    const startTime = new Date();
    const taskId = uuidv4();
    
    const mergedConfig: SelfHealingConfig = {
      enableRetry: true,
      enableMutation: true,
      enableFallback: true,
      enableValidationLoop: true,
      enableMultiPath: false,
      ...config
    };

    // Initialize execution context
    const context: ExecutionContext = {
      task,
      target,
      metadata: {
        ...metadata,
        taskId,
        timestamp: startTime.toISOString(),
        executionId: uuidv4(),
        auditTrail: []
      },
      history: [],
      attempts: 0,
      maxAttempts: 10
    };

    const result: SelfHealingResult = {
      taskId,
      task,
      completed: false,
      completionScore: 0,
      executionResults: [],
      mutationHistory: [],
      fallbackHistory: [],
      validationHistory: [],
      multiPathHistory: [],
      finalResult: null,
      completionCheck: null,
      durationMs: 0,
      startTime,
      endTime: startTime
    };

    try {
      // Execute with self-healing
      await this.executeWithSelfHealing(context, result, mergedConfig);

      // Check completion
      if (result.finalResult) {
        result.completionCheck = await this.completionChecker.checkCompletion(
          result.finalResult,
          context,
          mergedConfig.completionConfig
        );
        result.completed = result.completionCheck.completed;
        result.completionScore = result.completionCheck.score;
      }

    } catch (error) {
      result.finalResult = {
        success: false,
        strategy: 'error',
        duration: Date.now() - startTime.getTime(),
        output: null,
        error: error as Error,
        metrics: {
          resourcesUsed: { memoryMB: 0, cpuPercent: 0, diskIO: 0, networkIO: 0 },
          operationsPerformed: 0,
          validationPassed: false,
          healingApplied: false
        }
      };
      result.completed = false;
    }

    result.endTime = new Date();
    result.durationMs = result.endTime.getTime() - result.startTime.getTime();

    // Track execution history
    this.trackExecution(task, result);

    return result;
  }

  private async executeWithSelfHealing(
    context: ExecutionContext,
    result: SelfHealingResult,
    config: SelfHealingConfig
  ): Promise<void> {
    let currentStrategy = this.strategyLibrary.getBestStrategy(context);
    let failedStrategies: string[] = [];
    let attempts = 0;
    const maxAttempts = context.maxAttempts;

    while (attempts < maxAttempts && !result.completed) {
      context.attempts = attempts + 1;

      // Strategy A: Try current strategy with retry
      if (config.enableRetry) {
        const retryResults = await this.retryEngine.executeWithRetry(
          currentStrategy,
          context,
          config.retryConfig
        );
        result.executionResults.push(...retryResults.map(r => r.result));

        const lastResult = retryResults[retryResults.length - 1];
        if (lastResult.success) {
          result.finalResult = lastResult.result;
          return;
        }

        failedStrategies.push(currentStrategy.id);
      } else {
        const execResult = await currentStrategy.execute(context);
        result.executionResults.push(execResult);

        if (execResult.success) {
          result.finalResult = execResult;
          return;
        }

        failedStrategies.push(currentStrategy.id);
      }

      // Strategy B: Try mutation if enabled
      if (config.enableMutation && attempts < maxAttempts - 2) {
        const mutation = await this.mutationEngine.mutateStrategy(
          currentStrategy,
          context,
          result.executionResults[result.executionResults.length - 1].error
        );
        result.mutationHistory.push(mutation);
        currentStrategy = mutation.mutatedStrategy;
        attempts++;
        continue;
      }

      // Strategy C: Try validation loop if enabled
      if (config.enableValidationLoop && attempts < maxAttempts - 3) {
        const validationResults = await this.validationLoop.executeWithValidationLoop(
          currentStrategy,
          context,
          config.validationConfig
        );
        result.validationHistory.push(validationResults);

        const lastIteration = validationResults[validationResults.length - 1];
        if (lastIteration.completed) {
          result.finalResult = lastIteration.executionResult;
          return;
        }
      }

      // Strategy D: Try multi-path execution if enabled
      if (config.enableMultiPath && attempts < maxAttempts - 4) {
        const allStrategies = this.strategyLibrary.getAllStrategies();
        const multiPathResult = await this.multiPathRunner.executeMultiPath(
          allStrategies,
          context,
          config.pathConfig
        );
        result.multiPathHistory.push(multiPathResult);

        if (multiPathResult.selectedResult.success) {
          result.finalResult = multiPathResult.selectedResult;
          return;
        }

        failedStrategies.push(...allStrategies.map(s => s.id));
      }

      // Strategy E: Try fallback if enabled
      if (config.enableFallback && attempts >= maxAttempts - 2) {
        const fallbackResult = await this.fallbackEngine.executeFallback(
          context,
          failedStrategies,
          result.executionResults[result.executionResults.length - 1].error
        );
        result.fallbackHistory.push(fallbackResult);

        if (fallbackResult.executionResult.success) {
          result.finalResult = fallbackResult.executionResult;
          return;
        }

        if (fallbackResult.isLastResort) {
          result.finalResult = fallbackResult.executionResult;
          return;
        }
      }

      // Get next strategy from library
      currentStrategy = this.strategyLibrary.getBestStrategy(context);
      attempts++;
    }

    // If we've exhausted all attempts, use the last result
    if (result.executionResults.length > 0) {
      result.finalResult = result.executionResults[result.executionResults.length - 1];
    }
  }

  private trackExecution(task: string, result: SelfHealingResult): void {
    const history = this.executionHistory.get(task) || [];
    history.push(result);
    this.executionHistory.set(task, history);
  }

  getExecutionHistory(task: string): SelfHealingResult[] {
    return this.executionHistory.get(task) || [];
  }

  clearExecutionHistory(task: string): void {
    this.executionHistory.delete(task);
  }

  clearAllExecutionHistory(): void {
    this.executionHistory.clear();
  }

  getStatistics(): SelfHealingStatistics {
    const allResults: SelfHealingResult[] = [];
    for (const history of this.executionHistory.values()) {
      allResults.push(...history);
    }

    if (allResults.length === 0) {
      return {
        totalTasks: 0,
        completedTasks: 0,
        failedTasks: 0,
        completionRate: 0,
        averageDurationMs: 0,
        averageCompletionScore: 0,
        totalMutations: 0,
        totalFallbacks: 0,
        totalValidationLoops: 0,
        totalMultiPathExecutions: 0
      };
    }

    const completed = allResults.filter(r => r.completed);
    const failed = allResults.filter(r => !r.completed);

    return {
      totalTasks: allResults.length,
      completedTasks: completed.length,
      failedTasks: failed.length,
      completionRate: completed.length / allResults.length,
      averageDurationMs: allResults.reduce((sum, r) => sum + r.durationMs, 0) / allResults.length,
      averageCompletionScore: completed.length > 0
        ? completed.reduce((sum, r) => sum + r.completionScore, 0) / completed.length
        : 0,
      totalMutations: allResults.reduce((sum, r) => sum + r.mutationHistory.length, 0),
      totalFallbacks: allResults.reduce((sum, r) => sum + r.fallbackHistory.length, 0),
      totalValidationLoops: allResults.reduce((sum, r) => sum + r.validationHistory.length, 0),
      totalMultiPathExecutions: allResults.reduce((sum, r) => sum + r.multiPathHistory.length, 0)
    };
  }
}

export interface SelfHealingStatistics {
  totalTasks: number;
  completedTasks: number;
  failedTasks: number;
  completionRate: number;
  averageDurationMs: number;
  averageCompletionScore: number;
  totalMutations: number;
  totalFallbacks: number;
  totalValidationLoops: number;
  totalMultiPathExecutions: number;
}

// Export singleton instance
export const selfHealingEngine = new SelfHealingOrchestrationEngine();