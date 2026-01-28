// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * CI 健康度監控器 - 判斷 CI 系統的健康狀況
 */

import { CIHealthMetrics, CIFailure } from './types.js';

export class CIHealthMonitor {
  private history: Map<string, CIHealthMetrics[]> = new Map();
  private maxHistorySize: number = 100;

  /**
   * 記錄 CI 運行歷史
   */
  public recordRun(workflowName: string, metrics: CIHealthMetrics): void {
    if (!this.history.has(workflowName)) {
      this.history.set(workflowName, []);
    }

    const history = this.history.get(workflowName)!;
    history.push(metrics);

    // 限制歷史記錄大小
    if (history.length > this.maxHistorySize) {
      history.shift();
    }
  }

  /**
   * 獲取 CI 健康度指標
   */
  public async getHealthMetrics(workflowName: string): Promise<CIHealthMetrics> {
    const history = this.history.get(workflowName) || [];

    if (history.length === 0) {
      // 如果沒有歷史記錄，返回默認值
      return {
        workflowName,
        totalRuns: 0,
        failureRate: 0,
        averageDuration: 0,
        last7DaysFailures: 0,
        last30DaysFailures: 0,
        flakyTests: [],
        infraErrors: 0,
        isHealthy: true,
        timestamp: Date.now()
      };
    }

    const latestMetrics = history[history.length - 1];

    // 分析最近 7 天和 30 天的失敗情況
    const now = Date.now();
    const sevenDaysAgo = now - 7 * 24 * 60 * 60 * 1000;
    const thirtyDaysAgo = now - 30 * 24 * 60 * 60 * 1000;

    let last7DaysFailures = 0;
    let last30DaysFailures = 0;

    for (const metrics of history) {
      if (metrics.timestamp >= sevenDaysAgo) {
        last7DaysFailures++;
      }
      if (metrics.timestamp >= thirtyDaysAgo) {
        last30DaysFailures++;
      }
    }

    // 識別 flaky tests
    const flakyTests = this.identifyFlakyTests(history);

    // 計算基礎設施錯誤
    const infraErrors = this.countInfraErrors(history);

    // 判斷是否健康
    const isHealthy = this.isSystemHealthy(latestMetrics, flakyTests, infraErrors);

    return {
      ...latestMetrics,
      last7DaysFailures,
      last30DaysFailures,
      flakyTests,
      infraErrors,
      isHealthy
    };
  }

  /**
   * 識別 flaky tests
   */
  private identifyFlakyTests(history: CIHealthMetrics[]): string[] {
    const testFailureCount = new Map<string, number>();
    const flakyThreshold = 3; // 失敗 3 次以上算 flaky

    for (const metrics of history) {
      for (const testName of metrics.flakyTests) {
        testFailureCount.set(testName, (testFailureCount.get(testName) || 0) + 1);
      }
    }

    const flakyTests: string[] = [];
    for (const [testName, count] of testFailureCount.entries()) {
      if (count >= flakyThreshold) {
        flakyTests.push(testName);
      }
    }

    return flakyTests;
  }

  /**
   * 統計基礎設施錯誤
   */
  private countInfraErrors(history: CIHealthMetrics[]): number {
    let count = 0;
    for (const metrics of history) {
      count += metrics.infraErrors;
    }
    return count;
  }

  /**
   * 判斷系統是否健康
   */
  private isSystemHealthy(
    metrics: CIHealthMetrics,
    flakyTests: string[],
    infraErrors: number
  ): boolean {
    // 失敗率超過 50% 不健康
    if (metrics.failureRate > 0.5) {
      return false;
    }

    // 基礎設施錯誤過多不健康
    if (infraErrors > 10) {
      return false;
    }

    // Flaky tests 過多不健康
    if (flakyTests.length > 5) {
      return false;
    }

    return true;
  }

  /**
   * 分析失敗模式
   */
  public analyzeFailurePattern(
    workflowName: string,
    recentFailures: CIFailure[]
  ): {
    isConcurrentFailure: boolean;
    isCascadingFailure: boolean;
    isIsolatedFailure: boolean;
    patternDescription: string;
  } {
    const history = this.history.get(workflowName) || [];
    const now = Date.now();
    const oneHourAgo = now - 60 * 60 * 1000;

    // 檢查是否為並發失敗（其他 PR 也失敗）
    const isConcurrentFailure = recentFailures.length > 1;

    // 檢查是否為級聯失敗（連續失敗）
    const recentHistoryFailures = history.filter(
      m => m.timestamp >= oneHourAgo
    ).length;
    const isCascadingFailure = recentHistoryFailures >= 3;

    // 檢查是否為孤立失敗
    const isIsolatedFailure = !isConcurrentFailure && !isCascadingFailure;

    // 生成模式描述
    let patternDescription = '';

    if (isConcurrentFailure) {
      patternDescription = '並發失敗：多個 PR 同時失敗，可能是 CI 系統問題';
    } else if (isCascadingFailure) {
      patternDescription = '級聯失敗：連續失敗，可能是 CI 配置問題';
    } else if (isIsolatedFailure) {
      patternDescription = '孤立失敗：單個 PR 失敗，可能是 PR 問題';
    }

    return {
      isConcurrentFailure,
      isCascadingFailure,
      isIsolatedFailure,
      patternDescription
    };
  }

  /**
   * 獲取健康度報告
   */
  public async generateHealthReport(workflowName: string): Promise<{
    healthStatus: 'HEALTHY' | 'DEGRADED' | 'UNHEALTHY';
    metrics: CIHealthMetrics;
    recommendations: string[];
    trendAnalysis: string;
  }> {
    const metrics = await this.getHealthMetrics(workflowName);
    const history = this.history.get(workflowName) || [];

    let healthStatus: 'HEALTHY' | 'DEGRADED' | 'UNHEALTHY';
    const recommendations: string[] = [];

    // 判斷健康狀態
    if (!metrics.isHealthy) {
      healthStatus = 'UNHEALTHY';
      recommendations.push('立即檢查 CI 系統');
      recommendations.push('聯系 DevOps 團隊');
    } else if (metrics.failureRate > 0.2) {
      healthStatus = 'DEGRADED';
      recommendations.push('監控 CI 表現');
      recommendations.push('檢查最近的變更');
    } else {
      healthStatus = 'HEALTHY';
      recommendations.push('繼續監控');
    }

    // 趨勢分析
    let trendAnalysis = '';
    if (history.length > 5) {
      const recentFailureRate = history.slice(-5).filter(m => !m.isHealthy).length / 5;
      const olderFailureRate = history.slice(0, -5).filter(m => !m.isHealthy).length / Math.max(1, history.length - 5);

      if (recentFailureRate > olderFailureRate) {
        trendAnalysis = '失敗率上升，需要注意';
      } else if (recentFailureRate < olderFailureRate) {
        trendAnalysis = '失敗率下降，表現改善';
      } else {
        trendAnalysis = '表現穩定';
      }
    } else {
      trendAnalysis = '數據不足，無法分析趨勢';
    }

    return {
      healthStatus,
      metrics,
      recommendations,
      trendAnalysis
    };
  }

  /**
   * 清除歷史記錄
   */
  public clearHistory(workflowName?: string): void {
    if (workflowName) {
      this.history.delete(workflowName);
    } else {
      this.history.clear();
    }
  }

  /**
   * 獲取所有工作流名稱
   */
  public getWorkflowNames(): string[] {
    return Array.from(this.history.keys());
  }
}