// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: auto-retry-engine
// @GL-charter-version: 2.0.0

/**
 * Auto-Retry Engine
 * Intelligent retry mechanism with exponential backoff and jitter
 */

import { ExecutionStrategy, ExecutionContext, ExecutionResult } from '../strategy-library/strategies';

export interface RetryConfig {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  backoffMultiplier: number;
  jitterEnabled: boolean;
  jitterFactor: number;
  retryableErrors: string[];
}

export interface RetryResult {
  attempt: number;
  success: boolean;
  result: ExecutionResult;
  delayMs: number;
  totalDurationMs: number;
}

export class RetryEngine {
  private defaultConfig: RetryConfig = {
    maxRetries: 5,
    baseDelayMs: 1000,
    maxDelayMs: 60000,
    backoffMultiplier: 2,
    jitterEnabled: true,
    jitterFactor: 0.1,
    retryableErrors: [
      'timeout',
      'network',
      'temporary',
      'rate limit',
      'connection',
      'econnrefused',
      'etimedout'
    ]
  };

  private retryHistory: Map<string, RetryResult[]> = new Map();

  async executeWithRetry(
    strategy: ExecutionStrategy,
    context: ExecutionContext,
    config?: Partial<RetryConfig>
  ): Promise<RetryResult[]> {
    const mergedConfig = { ...this.defaultConfig, ...config };
    const results: RetryResult[] = [];
    let totalDuration = 0;

    for (let attempt = 0; attempt <= mergedConfig.maxRetries; attempt++) {
      const attemptStartTime = Date.now();
      
      try {
        const result = await strategy.execute(context);
        const attemptDuration = Date.now() - attemptStartTime;
        totalDuration += attemptDuration;

        const retryResult: RetryResult = {
          attempt: attempt + 1,
          success: result.success,
          result,
          delayMs: 0,
          totalDurationMs: totalDuration
        };

        results.push(retryResult);

        // Track retry history
        this.trackRetry(context.task, retryResult);

        // If successful, return results
        if (result.success) {
          return results;
        }

        // If error is not retryable, stop
        if (!this.isRetryable(result.error, mergedConfig.retryableErrors)) {
          return results;
        }

      } catch (error) {
        const attemptDuration = Date.now() - attemptStartTime;
        totalDuration += attemptDuration;

        const retryResult: RetryResult = {
          attempt: attempt + 1,
          success: false,
          result: {
            success: false,
            strategy: strategy.id,
            duration: attemptDuration,
            output: null,
            error: error as Error,
            metrics: {
              resourcesUsed: { memoryMB: 0, cpuPercent: 0, diskIO: 0, networkIO: 0 },
              operationsPerformed: 0,
              validationPassed: false,
              healingApplied: false
            }
          },
          delayMs: 0,
          totalDurationMs: totalDuration
        };

        results.push(retryResult);
        this.trackRetry(context.task, retryResult);

        // If error is not retryable, stop
        if (!this.isRetryable(error as Error, mergedConfig.retryableErrors)) {
          return results;
        }
      }

      // Calculate delay for next retry
      if (attempt < mergedConfig.maxRetries) {
        const delayMs = this.calculateDelay(attempt, mergedConfig);
        await this.sleep(delayMs);

        // Update last result with delay
        results[results.length - 1].delayMs = delayMs;
        totalDuration += delayMs;
        results[results.length - 1].totalDurationMs = totalDuration;
      }
    }

    return results;
  }

  private isRetryable(error: Error | undefined, retryableErrors: string[]): boolean {
    if (!error) return false;

    const errorMessage = error.message.toLowerCase();
    return retryableErrors.some(retryableError => 
      errorMessage.includes(retryableError)
    );
  }

  private calculateDelay(attempt: number, config: RetryConfig): number {
    // Exponential backoff
    let delay = config.baseDelayMs * Math.pow(config.backoffMultiplier, attempt);

    // Cap at max delay
    delay = Math.min(delay, config.maxDelayMs);

    // Add jitter if enabled
    if (config.jitterEnabled) {
      const jitter = delay * config.jitterFactor * (Math.random() * 2 - 1);
      delay = delay + jitter;
    }

    return Math.max(delay, config.baseDelayMs);
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private trackRetry(task: string, result: RetryResult): void {
    const history = this.retryHistory.get(task) || [];
    history.push(result);
    this.retryHistory.set(task, history);
  }

  getRetryHistory(task: string): RetryResult[] {
    return this.retryHistory.get(task) || [];
  }

  getRetryStatistics(task: string): RetryStatistics {
    const history = this.getRetryHistory(task);
    
    if (history.length === 0) {
      return {
        totalAttempts: 0,
        successfulAttempts: 0,
        failedAttempts: 0,
        successRate: 0,
        averageRetries: 0,
        totalDurationMs: 0,
        averageDelayMs: 0
      };
    }

    const successful = history.filter(r => r.success);
    const failed = history.filter(r => !r.success);
    const delays = history.map(r => r.delayMs).filter(d => d > 0);

    return {
      totalAttempts: history.length,
      successfulAttempts: successful.length,
      failedAttempts: failed.length,
      successRate: successful.length / history.length,
      averageRetries: history.length - 1,
      totalDurationMs: history[history.length - 1].totalDurationMs,
      averageDelayMs: delays.length > 0 
        ? delays.reduce((a, b) => a + b, 0) / delays.length 
        : 0
    };
  }

  clearRetryHistory(task: string): void {
    this.retryHistory.delete(task);
  }

  clearAllRetryHistory(): void {
    this.retryHistory.clear();
  }
}

export interface RetryStatistics {
  totalAttempts: number;
  successfulAttempts: number;
  failedAttempts: number;
  successRate: number;
  averageRetries: number;
  totalDurationMs: number;
  averageDelayMs: number;
}