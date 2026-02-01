// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: multi-path-execution-runner
// @GL-charter-version: 2.0.0

/**
 * Multi-Path Execution Runner
 * Executes tasks through multiple parallel paths and selects best result
 */

import { ExecutionStrategy, ExecutionContext, ExecutionResult } from '../strategy-library/strategies';

export interface PathConfig {
  maxConcurrentPaths: number;
  timeoutMs: number;
  selectionCriteria: SelectionCriteria;
}

export enum SelectionCriteria {
  FIRST_SUCCESS = 'first-success',
  HIGHEST_QUALITY = 'highest-quality',
  FASTEST = 'fastest',
  MAJORITY_CONSENSUS = 'majority-consensus'
}

export interface ExecutionPath {
  id: string;
  strategy: ExecutionStrategy;
  priority: number;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  result?: ExecutionResult;
  durationMs?: number;
}

export interface MultiPathResult {
  selectedResult: ExecutionResult;
  allPaths: ExecutionPath[];
  selectionReason: string;
  totalDurationMs: number;
}

export class MultiPathRunner {
  private defaultConfig: PathConfig = {
    maxConcurrentPaths: 3,
    timeoutMs: 60000,
    selectionCriteria: SelectionCriteria.FIRST_SUCCESS
  };

  private executionHistory: Map<string, MultiPathResult[]> = new Map();

  async executeMultiPath(
    strategies: ExecutionStrategy[],
    context: ExecutionContext,
    config?: Partial<PathConfig>
  ): Promise<MultiPathResult> {
    const mergedConfig = { ...this.defaultConfig, ...config };
    const startTime = Date.now();

    // Create execution paths
    const paths: ExecutionPath[] = strategies.map((strategy, index) => ({
      id: `path-${index}`,
      strategy,
      priority: index,
      status: 'pending'
    }));

    // Execute paths in parallel (up to maxConcurrentPaths)
    const concurrentStrategies = strategies.slice(0, mergedConfig.maxConcurrentPaths);
    const results = await this.executeConcurrentPaths(concurrentStrategies, context, mergedConfig);

    // Update path statuses
    results.forEach((result, index) => {
      paths[index].status = result.success ? 'completed' : 'failed';
      paths[index].result = result;
      paths[index].durationMs = result.duration;
    });

    // Select best result based on criteria
    const selectedResult = this.selectBestResult(
      paths,
      mergedConfig.selectionCriteria,
      context
    );

    const multiPathResult: MultiPathResult = {
      selectedResult,
      allPaths: paths,
      selectionReason: this.getSelectionReason(selectedResult, mergedConfig.selectionCriteria),
      totalDurationMs: Date.now() - startTime
    };

    // Track execution history
    this.trackExecution(context.task, multiPathResult);

    return multiPathResult;
  }

  private async executeConcurrentPaths(
    strategies: ExecutionStrategy[],
    context: ExecutionContext,
    config: PathConfig
  ): Promise<ExecutionResult[]> {
    const results: ExecutionResult[] = [];
    const promises = strategies.map(strategy => 
      this.executeWithTimeout(strategy, context, config.timeoutMs)
    );

    // Execute all paths concurrently
    const settledResults = await Promise.allSettled(promises);

    for (const settled of settledResults) {
      if (settled.status === 'fulfilled') {
        results.push(settled.value);
      } else {
        results.push({
          success: false,
          strategy: 'unknown',
          duration: config.timeoutMs,
          output: null,
          error: settled.reason as Error,
          metrics: {
            resourcesUsed: { memoryMB: 0, cpuPercent: 0, diskIO: 0, networkIO: 0 },
            operationsPerformed: 0,
            validationPassed: false,
            healingApplied: false
          }
        });
      }
    }

    return results;
  }

  private async executeWithTimeout(
    strategy: ExecutionStrategy,
    context: ExecutionContext,
    timeoutMs: number
  ): Promise<ExecutionResult> {
    return Promise.race([
      strategy.execute(context),
      this.timeoutPromise(timeoutMs)
    ]);
  }

  private timeoutPromise(timeoutMs: number): Promise<ExecutionResult> {
    return new Promise((_, reject) => {
      setTimeout(() => {
        reject(new Error(`Execution timeout after ${timeoutMs}ms`));
      }, timeoutMs);
    });
  }

  private selectBestResult(
    paths: ExecutionPath[],
    criteria: SelectionCriteria,
    context: ExecutionContext
  ): ExecutionResult {
    const completedPaths = paths.filter(p => p.status === 'completed' && p.result);

    if (completedPaths.length === 0) {
      // Return first failed result if no successes
      const failedPath = paths.find(p => p.status === 'failed' && p.result);
      return failedPath!.result!;
    }

    switch (criteria) {
      case SelectionCriteria.FIRST_SUCCESS:
        return completedPaths[0].result!;

      case SelectionCriteria.HIGHEST_QUALITY:
        return this.selectHighestQuality(completedPaths);

      case SelectionCriteria.FASTEST:
        return this.selectFastest(completedPaths);

      case SelectionCriteria.MAJORITY_CONSENSUS:
        return this.selectByConsensus(completedPaths, context);

      default:
        return completedPaths[0].result!;
    }
  }

  private selectHighestQuality(paths: ExecutionPath[]): ExecutionResult {
    // Score based on metrics and validation
    return paths.reduce((best, current) => {
      const bestScore = this.calculateQualityScore(best.result!);
      const currentScore = this.calculateQualityScore(current.result!);
      return currentScore > bestScore ? current : best;
    }).result!;
  }

  private selectFastest(paths: ExecutionPath[]): ExecutionResult {
    // Select shortest duration
    return paths.reduce((best, current) => {
      return (current.durationMs || Infinity) < (best.durationMs || Infinity) 
        ? current 
        : best;
    }).result!;
  }

  private selectByConsensus(paths: ExecutionPath[], context: ExecutionContext): ExecutionResult {
    // Group similar results and select most common
    const groups = new Map<string, ExecutionPath[]>();

    for (const path of paths) {
      const key = JSON.stringify(path.result!.output);
      const existing = groups.get(key) || [];
      existing.push(path);
      groups.set(key, existing);
    }

    // Find largest group
    let largestGroup: ExecutionPath[] = [];
    for (const group of groups.values()) {
      if (group.length > largestGroup.length) {
        largestGroup = group;
      }
    }

    // Return result from largest group
    return largestGroup[0].result!;
  }

  private calculateQualityScore(result: ExecutionResult): number {
    let score = 0;

    // Success is most important
    score += result.success ? 100 : 0;

    // Validation score
    if (result.metrics) {
      score += result.metrics.validationPassed ? 20 : 0;
      score += result.metrics.healingApplied ? 10 : 0;
      
      // Resource efficiency (lower is better)
      const resourceScore = 100 - (result.metrics.resourcesUsed.memoryMB / 10);
      score += Math.max(resourceScore, 0);
    }

    return score;
  }

  private getSelectionReason(result: ExecutionResult, criteria: SelectionCriteria): string {
    return `Selected result using ${criteria} criteria. Success: ${result.success}`;
  }

  private trackExecution(task: string, result: MultiPathResult): void {
    const history = this.executionHistory.get(task) || [];
    history.push(result);
    this.executionHistory.set(task, history);
  }

  getExecutionHistory(task: string): MultiPathResult[] {
    return this.executionHistory.get(task) || [];
  }

  clearExecutionHistory(task: string): void {
    this.executionHistory.delete(task);
  }

  clearAllExecutionHistory(): void {
    this.executionHistory.clear();
  }
}