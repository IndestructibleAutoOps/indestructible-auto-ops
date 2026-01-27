/**
 * CI Fail 自動分類系統 - 主入口
 * 統一協調所有組件
 */

import { ErrorClassifier } from './error-classifier.js';
import { SemanticMatcher } from './semantic-matcher.js';
import { CIHealthMonitor } from './ci-health-monitor.js';
import { AutoRerunStrategy } from './auto-rerun-strategy.js';
import { LLMJudgment } from './llm-judgment.js';
import { ResultFormatter } from './result-formatter.js';
import {
  SystemConfig,
  ClassificationResult,
  PRDiff,
  CIFailure,
  SemanticMatchResult,
  RerunStrategy,
  CIHealthMetrics
} from './types.js';

/**
 * 系統主類
 */
export class CIFailAutoClassificationSystem {
  private errorClassifier: ErrorClassifier;
  private semanticMatcher: SemanticMatcher;
  private ciHealthMonitor: CIHealthMonitor;
  private autoRerunStrategy: AutoRerunStrategy;
  private llmJudgment: LLMJudgment;
  private resultFormatter: ResultFormatter;
  private config: SystemConfig;

  constructor(config: Partial<SystemConfig> = {}) {
    // 默認配置
    this.config = {
      enableLLMJudgment: config.enableLLMJudgment ?? true,
      enableAutoRerun: config.enableAutoRerun ?? true,
      enableAutoLabeling: config.enableAutoLabeling ?? true,
      enableAutoComment: config.enableAutoComment ?? true,
      maxRerunAttempts: config.maxRerunAttempts ?? 3,
      flakyTestThreshold: config.flakyTestThreshold ?? 3,
      similarityThreshold: config.similarityThreshold ?? 40,
      confidenceThreshold: config.confidenceThreshold ?? 70
    };

    // 初始化組件
    this.errorClassifier = new ErrorClassifier(this.config);
    this.semanticMatcher = new SemanticMatcher();
    this.ciHealthMonitor = new CIHealthMonitor();
    this.autoRerunStrategy = new AutoRerunStrategy();
    this.llmJudgment = new LLMJudgment();
    this.resultFormatter = new ResultFormatter();
  }

  /**
   * 主分類方法
   */
  public async classify(
    prDiff: PRDiff,
    ciFailure: CIFailure
  ): Promise<{
    classificationResult: ClassificationResult;
    semanticMatch?: SemanticMatchResult;
    rerunStrategy?: RerunStrategy;
    report: string;
    summary: string;
    prComment: string;
    labels: string[];
    shouldRerun: boolean;
  }> {
    // 1. 獲取 CI 健康度
    const ciHealth = await this.ciHealthMonitor.getHealthMetrics(ciFailure.workflowName);

    // 2. 語意比對
    const semanticMatch = this.semanticMatcher.match(prDiff, ciFailure);

    // 3. 規則分類
    let classificationResult = this.errorClassifier.classify(prDiff, ciFailure, ciHealth);

    // 4. LLM 判斷（如果啟用）
    if (this.config.enableLLMJudgment) {
      const llmRequest = {
        prDiff,
        ciFailure,
        ciHistory: ciHealth,
        context: this.semanticMatcher.generateDetailedReport(prDiff, ciFailure).summary
      };

      try {
        const llmResponse = await this.llmJudgment.requestJudgment(llmRequest);
        classificationResult = this.llmJudgment.integrateLLMJudgment(
          llmResponse,
          classificationResult,
          this.config.confidenceThreshold
        );
      } catch (error) {
        console.error('LLM 判斷失敗，使用規則結果:', error);
      }
    }

    // 5. 計算重跑策略
    const rerunStrategy = this.autoRerunStrategy.calculateRerunStrategy(
      classificationResult,
      ciFailure.workflowName,
      ciFailure.runId
    );

    // 6. 生成報告
    const report = this.resultFormatter.generateReport(classificationResult, semanticMatch);
    const summary = this.resultFormatter.generateSummary(classificationResult);
    const prComment = this.resultFormatter.generatePRComment(classificationResult, semanticMatch);
    const labels = this.resultFormatter.generateLabels(classificationResult);

    return {
      classificationResult,
      semanticMatch,
      rerunStrategy,
      report,
      summary,
      prComment,
      labels,
      shouldRerun: rerunStrategy.shouldRerun
    };
  }

  /**
   * 批量分類
   */
  public async batchClassify(
    requests: Array<{ prDiff: PRDiff; ciFailure: CIFailure }>
  ): Promise<Array<{
    classificationResult: ClassificationResult;
    report: string;
    summary: string;
  }>> {
    const results = [];

    for (const request of requests) {
      const result = await this.classify(request.prDiff, request.ciFailure);
      results.push({
        classificationResult: result.classificationResult,
        report: result.report,
        summary: result.summary
      });
    }

    return results;
  }

  /**
   * 獲取 CI 健康度報告
   */
  public async getCIHealthReport(workflowName: string): Promise<{
    healthStatus: 'HEALTHY' | 'DEGRADED' | 'UNHEALTHY';
    metrics: CIHealthMetrics;
    recommendations: string[];
    trendAnalysis: string;
  }> {
    return await this.ciHealthMonitor.generateHealthReport(workflowName);
  }

  /**
   * 記錄 CI 運行
   */
  public recordCIRun(workflowName: string, metrics: CIHealthMetrics): void {
    this.ciHealthMonitor.recordRun(workflowName, metrics);
  }

  /**
   * 記錄重跑
   */
  public recordRerun(workflowName: string): void {
    this.autoRerunStrategy.recordRerun(workflowName);
  }

  /**
   * 獲取統計信息
   */
  public getStatistics(): {
    workflows: string[];
    rerunStats: Record<string, {
      totalReruns: number;
      rerunsInLastHour: number;
      rerunsInLast24Hours: number;
      averageRerunInterval: number;
    }>;
  } {
    const workflows = this.ciHealthMonitor.getWorkflowNames();
    const rerunStats: Record<string, any> = {};

    for (const workflowName of workflows) {
      rerunStats[workflowName] = this.autoRerunStrategy.getRerunStatistics(workflowName);
    }

    return {
      workflows,
      rerunStats
    };
  }

  /**
   * 導出所有組件
   */
  public getComponents() {
    return {
      errorClassifier: this.errorClassifier,
      semanticMatcher: this.semanticMatcher,
      ciHealthMonitor: this.ciHealthMonitor,
      autoRerunStrategy: this.autoRerunStrategy,
      llmJudgment: this.llmJudgment,
      resultFormatter: this.resultFormatter
    };
  }

  /**
   * 更新配置
   */
  public updateConfig(newConfig: Partial<SystemConfig>): void {
    this.config = { ...this.config, ...newConfig };
  }

  /**
   * 獲取配置
   */
  public getConfig(): SystemConfig {
    return { ...this.config };
  }
}

/**
 * 創建系統實例
 */
export function createSystem(config?: Partial<SystemConfig>): CIFailAutoClassificationSystem {
  return new CIFailAutoClassificationSystem(config);
}

// 導出所有類型和類
export * from './types.js';
export { ErrorClassifier } from './error-classifier.js';
export { SemanticMatcher } from './semantic-matcher.js';
export { CIHealthMonitor } from './ci-health-monitor.js';
export { AutoRerunStrategy } from './auto-rerun-strategy.js';
export { LLMJudgment } from './llm-judgment.js';
export { ResultFormatter } from './result-formatter.js';