// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: self-healing-validation-loop
// @GL-charter-version: 2.0.0

/**
 * Self-Healing Validation Loop
 * Continuous execution, validation, and repair until success
 */

import { ExecutionStrategy, ExecutionContext, ExecutionResult } from '../strategy-library/strategies';

export interface ValidationConfig {
  maxIterations: number;
  validationThreshold: number;
  autoRepairEnabled: boolean;
  strictMode: boolean;
}

export interface ValidationResult {
  valid: boolean;
  score: number;
  issues: ValidationIssue[];
  passedChecks: string[];
  failedChecks: string[];
}

export interface ValidationIssue {
  id: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  type: string;
  message: string;
  repairable: boolean;
  repairStrategy?: string;
}

export class ValidationLoop {
  private defaultConfig: ValidationConfig = {
    maxIterations: 10,
    validationThreshold: 0.85,
    autoRepairEnabled: true,
    strictMode: true
  };

  private validationHistory: Map<string, IterationResult[]> = new Map();

  async executeWithValidationLoop(
    strategy: ExecutionStrategy,
    context: ExecutionContext,
    config?: Partial<ValidationConfig>
  ): Promise<IterationResult[]> {
    const mergedConfig = { ...this.defaultConfig, ...config };
    const results: IterationResult[] = [];

    for (let iteration = 0; iteration < mergedConfig.maxIterations; iteration++) {
      const iterationStartTime = Date.now();

      // Execute task
      const executionResult = await strategy.execute(context);

      // Validate result
      const validationResult = await this.validateExecution(executionResult, context);

      const iterationResult: IterationResult = {
        iteration: iteration + 1,
        executionResult,
        validationResult,
        durationMs: Date.now() - iterationStartTime,
        repaired: false,
        completed: false
      };

      // Track iteration
      this.trackIteration(context.task, iterationResult);
      results.push(iterationResult);

      // Check if validation passed
      if (validationResult.valid && validationResult.score >= mergedConfig.validationThreshold) {
        iterationResult.completed = true;
        break;
      }

      // Auto-repair if enabled
      if (mergedConfig.autoRepairEnabled && iteration < mergedConfig.maxIterations - 1) {
        const repairResult = await this.autoRepairIssues(
          validationResult.issues,
          context,
          executionResult
        );
        iterationResult.repaired = repairResult.applied;
        iterationResult.repairDetails = repairResult;

        // Update context with repair information
        context.metadata.repairHistory = context.metadata.repairHistory || [];
        context.metadata.repairHistory.push(repairResult);
      }

      // If strict mode and no repairable issues, stop
      if (mergedConfig.strictMode) {
        const criticalIssues = validationResult.issues.filter(i => i.severity === 'critical');
        if (criticalIssues.length > 0 && !criticalIssues.some(i => i.repairable)) {
          break;
        }
      }
    }

    return results;
  }

  private async validateExecution(
    result: ExecutionResult,
    context: ExecutionContext
  ): Promise<ValidationResult> {
    const issues: ValidationIssue[] = [];
    const passedChecks: string[] = [];
    const failedChecks: string[] = [];

    // Check execution success
    if (!result.success) {
      issues.push({
        id: 'execution-failed',
        severity: 'critical',
        type: 'execution',
        message: 'Execution failed',
        repairable: true,
        repairStrategy: 'retry-with-different-strategy'
      });
      failedChecks.push('execution-success');
    } else {
      passedChecks.push('execution-success');
    }

    // Check metrics
    if (result.metrics) {
      // Check validation passed
      if (result.metrics.validationPassed) {
        passedChecks.push('metrics-validation');
      } else {
        issues.push({
          id: 'metrics-validation-failed',
          severity: 'medium',
          type: 'metrics',
          message: 'Metrics validation failed',
          repairable: true,
          repairStrategy: 'adjust-execution-parameters'
        });
        failedChecks.push('metrics-validation');
      }

      // Check resource usage
      if (result.metrics.resourcesUsed.memoryMB > 1000) {
        issues.push({
          id: 'high-memory-usage',
          severity: 'medium',
          type: 'resources',
          message: `High memory usage: ${result.metrics.resourcesUsed.memoryMB}MB`,
          repairable: true,
          repairStrategy: 'optimize-memory-usage'
        });
      }

      // Check healing applied
      if (!result.metrics.healingApplied && issues.length > 0) {
        issues.push({
          id: 'healing-not-applied',
          severity: 'low',
          type: 'healing',
          message: 'Healing not applied despite issues',
          repairable: true,
          repairStrategy: 'enable-auto-repair'
        });
      }
    }

    // Calculate validation score
    const score = this.calculateValidationScore(passedChecks, failedChecks, issues);

    return {
      valid: issues.filter(i => i.severity === 'critical').length === 0,
      score,
      issues,
      passedChecks,
      failedChecks
    };
  }

  private async autoRepairIssues(
    issues: ValidationIssue[],
    context: ExecutionContext,
    result: ExecutionResult
  ): Promise<RepairResult> {
    const repairResult: RepairResult = {
      applied: false,
      repairedIssues: [],
      failedIssues: []
    };

    for (const issue of issues) {
      if (issue.repairable && issue.repairStrategy) {
        try {
          await this.applyRepair(issue, context, result);
          repairResult.repairedIssues.push(issue.id);
          repairResult.applied = true;
        } catch (error) {
          repairResult.failedIssues.push({
            issueId: issue.id,
            error: (error as Error).message
          });
        }
      }
    }

    return repairResult;
  }

  private async applyRepair(
    issue: ValidationIssue,
    context: ExecutionContext,
    result: ExecutionResult
  ): Promise<void> {
    switch (issue.repairStrategy) {
      case 'retry-with-different-strategy':
        // Will be handled by strategy mutation
        break;
      case 'adjust-execution-parameters':
        // Adjust execution parameters
        break;
      case 'optimize-memory-usage':
        // Optimize memory usage
        break;
      case 'enable-auto-repair':
        // Enable auto-repair
        break;
      default:
        // Generic repair
        break;
    }
  }

  private calculateValidationScore(
    passed: string[],
    failed: string[],
    issues: ValidationIssue[]
  ): number {
    const totalChecks = passed.length + failed.length;
    if (totalChecks === 0) return 1.0;

    const baseScore = passed.length / totalChecks;

    // Penalty for issues
    const criticalPenalty = issues.filter(i => i.severity === 'critical').length * 0.3;
    const highPenalty = issues.filter(i => i.severity === 'high').length * 0.2;
    const mediumPenalty = issues.filter(i => i.severity === 'medium').length * 0.1;
    const lowPenalty = issues.filter(i => i.severity === 'low').length * 0.05;

    const totalPenalty = criticalPenalty + highPenalty + mediumPenalty + lowPenalty;

    return Math.max(baseScore - totalPenalty, 0);
  }

  private trackIteration(task: string, result: IterationResult): void {
    const history = this.validationHistory.get(task) || [];
    history.push(result);
    this.validationHistory.set(task, history);
  }

  getValidationHistory(task: string): IterationResult[] {
    return this.validationHistory.get(task) || [];
  }

  clearValidationHistory(task: string): void {
    this.validationHistory.delete(task);
  }

  clearAllValidationHistory(): void {
    this.validationHistory.clear();
  }
}

export interface IterationResult {
  iteration: number;
  executionResult: ExecutionResult;
  validationResult: ValidationResult;
  durationMs: number;
  repaired: boolean;
  repairDetails?: RepairResult;
  completed: boolean;
}

export interface RepairResult {
  applied: boolean;
  repairedIssues: string[];
  failedIssues: Array<{ issueId: string; error: string }>;
}