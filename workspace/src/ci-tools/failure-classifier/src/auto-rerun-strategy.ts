/**
 * 自動重跑策略 - 智能決定是否重跑 CI
 */

import { RerunStrategy, ClassificationResult, ErrorType, ErrorSeverity } from './types.js';

export class AutoRerunStrategy {
  private rerunHistory: Map<string, number[]> = new Map();
  private maxRerunHistorySize: number = 50;

  /**
   * 計算重跑策略
   */
  public calculateRerunStrategy(
    classificationResult: ClassificationResult,
    workflowName: string,
    runId: string
  ): RerunStrategy {
    const shouldRerun = this.shouldRerun(classificationResult);
    const maxReruns = this.calculateMaxReruns(classificationResult);
    const rerunDelay = this.calculateRerunDelay(classificationResult, workflowName);

    return {
      shouldRerun,
      maxReruns,
      rerunDelay,
      rerunConditions: this.getRerunConditions(classificationResult)
    };
  }

  /**
   * 判斷是否應該重跑
   */
  private shouldRerun(classificationResult: ClassificationResult): boolean {
    // 如果分類結果建議重跑
    if (classificationResult.shouldRerun) {
      return true;
    }

    // 如果是 CI 問題且嚴重性不高，可以重跑
    if (
      classificationResult.errorType === ErrorType.CI_INDUCED &&
      classificationResult.severity !== ErrorSeverity.CRITICAL
    ) {
      return true;
    }

    // 如果是模稜兩可的情況，可以嘗試重跑
    if (
      classificationResult.errorType === ErrorType.AMBIGUOUS &&
      classificationResult.confidence < 60
    ) {
      return true;
    }

    // PR 問題不建議重跑
    if (classificationResult.errorType === ErrorType.PR_INDUCED) {
      return false;
    }

    return false;
  }

  /**
   * 計算最大重跑次數
   */
  private calculateMaxReruns(classificationResult: ClassificationResult): number {
    // 嚴重性越高，重跑次數越少
    switch (classificationResult.severity) {
      case ErrorSeverity.CRITICAL:
        return 1;
      case ErrorSeverity.HIGH:
        return 2;
      case ErrorSeverity.MEDIUM:
        return 3;
      case ErrorSeverity.LOW:
        return 4;
      default:
        return 2;
    }
  }

  /**
   * 計算重跑延遲
   */
  private calculateRerunDelay(
    classificationResult: ClassificationResult,
    workflowName: string
  ): number {
    // 檢查最近的重跑歷史
    const recentReruns = this.rerunHistory.get(workflowName) || [];
    const recentCount = recentReruns.filter(
      time => Date.now() - time < 5 * 60 * 1000 // 5 分鐘內
    ).length;

    // 如果最近重跑過，增加延遲
    if (recentCount > 0) {
      return Math.min(60000 * recentCount, 300000); // 最多延遲 5 分鐘
    }

    // 根據錯誤類型設置延遲
    switch (classificationResult.errorType) {
      case ErrorType.CI_INDUCED:
        return 10000; // 10 秒
      case ErrorType.AMBIGUOUS:
        return 30000; // 30 秒
      default:
        return 0;
    }
  }

  /**
   * 獲取重跑條件
   */
  private getRerunConditions(classificationResult: ClassificationResult): string[] {
    const conditions: string[] = [];

    if (classificationResult.errorType === ErrorType.CI_INDUCED) {
      conditions.push('CI 系統問題');
      conditions.push('非 PR 代碼問題');
    }

    if (classificationResult.errorType === ErrorType.AMBIGUOUS) {
      conditions.push('無法確定錯誤來源');
      conditions.push('信心度較低');
    }

    if (classificationResult.ciHealth?.flakyTests && classificationResult.ciHealth.flakyTests.length > 0) {
      conditions.push('Flaky test 檢測');
    }

    return conditions;
  }

  /**
   * 記錄重跑
   */
  public recordRerun(workflowName: string): void {
    if (!this.rerunHistory.has(workflowName)) {
      this.rerunHistory.set(workflowName, []);
    }

    const history = this.rerunHistory.get(workflowName)!;
    history.push(Date.now());

    // 限制歷史記錄大小
    if (history.length > this.maxRerunHistorySize) {
      history.shift();
    }
  }

  /**
   * 檢查是否達到重跑限制
   */
  public hasReachedRerunLimit(workflowName: string, maxReruns: number): boolean {
    const history = this.rerunHistory.get(workflowName) || [];
    const oneHourAgo = Date.now() - 60 * 60 * 1000;

    const recentReruns = history.filter(time => time >= oneHourAgo);
    return recentReruns.length >= maxReruns;
  }

  /**
   * 獲取重跑統計
   */
  public getRerunStatistics(workflowName: string): {
    totalReruns: number;
    rerunsInLastHour: number;
    rerunsInLast24Hours: number;
    averageRerunInterval: number;
  } {
    const history = this.rerunHistory.get(workflowName) || [];
    const now = Date.now();
    const oneHourAgo = now - 60 * 60 * 1000;
    const oneDayAgo = now - 24 * 60 * 60 * 1000;

    const rerunsInLastHour = history.filter(time => time >= oneHourAgo).length;
    const rerunsInLast24Hours = history.filter(time => time >= oneDayAgo).length;

    // 計算平均重跑間隔
    let averageRerunInterval = 0;
    if (history.length > 1) {
      const intervals: number[] = [];
      for (let i = 1; i < history.length; i++) {
        intervals.push(history[i] - history[i - 1]);
      }
      averageRerunInterval = intervals.reduce((a, b) => a + b, 0) / intervals.length;
    }

    return {
      totalReruns: history.length,
      rerunsInLastHour,
      rerunsInLast24Hours,
      averageRerunInterval
    };
  }

  /**
   * 智能重跑建議
   */
  public generateRerunRecommendation(
    classificationResult: ClassificationResult,
    workflowName: string
  ): {
    shouldRerun: boolean;
    reason: string;
    estimatedSuccessRate: number;
    alternativeActions: string[];
  } {
    const strategy = this.calculateRerunStrategy(
      classificationResult,
      workflowName,
      'current'
    );

    let estimatedSuccessRate = 0;
    let reason = '';
    const alternativeActions: string[] = [];

    // 估算成功率
    if (classificationResult.errorType === ErrorType.CI_INDUCED) {
      estimatedSuccessRate = 70;
      reason = 'CI 問題，重跑成功率較高';
    } else if (classificationResult.errorType === ErrorType.AMBIGUOUS) {
      estimatedSuccessRate = 50;
      reason = '無法確定，嘗試重跑';
    } else {
      estimatedSuccessRate = 10;
      reason = 'PR 問題，重跑成功率低';
      alternativeActions.push('修復 PR 代碼');
      alternativeActions.push('聯系 reviewer');
    }

    // 根據健康度調整
    if (classificationResult.ciHealth?.isHealthy === false) {
      estimatedSuccessRate -= 20;
      alternativeActions.push('修復 CI 系統');
      alternativeActions.push('通知 DevOps 團隊');
    }

    // 如果重跑過多次，降低成功率
    const stats = this.getRerunStatistics(workflowName);
    if (stats.rerunsInLastHour > 3) {
      estimatedSuccessRate -= 30;
      alternativeActions.push('等待 CI 系統恢復');
    }

    return {
      shouldRerun: strategy.shouldRerun && estimatedSuccessRate > 30,
      reason,
      estimatedSuccessRate: Math.max(0, estimatedSuccessRate),
      alternativeActions
    };
  }

  /**
   * 清除重跑歷史
   */
  public clearRerunHistory(workflowName?: string): void {
    if (workflowName) {
      this.rerunHistory.delete(workflowName);
    } else {
      this.rerunHistory.clear();
    }
  }
}