/**
 * 錯誤分類器 - 核心分類邏輯
 */

import { ErrorType, ErrorSeverity, ClassificationResult, PRDiff, CIFailure, CIHealthMetrics, SystemConfig } from './types.js';

export class ErrorClassifier {
  private config: SystemConfig;

  constructor(config: SystemConfig) {
    this.config = config;
  }

  /**
   * 主分類方法
   */
  public classify(
    prDiff: PRDiff,
    ciFailure: CIFailure,
    ciHealth: CIHealthMetrics
  ): ClassificationResult {
    // 1. 檢查是否為基礎設施錯誤
    if (this.isInfraError(ciFailure)) {
      return this.createResult(
        ErrorType.CI_INDUCED,
        ErrorSeverity.HIGH,
        95,
        '偵測到基礎設施錯誤',
        ['檢查 CI 環境配置', '聯系 DevOps 團隊'],
        ciHealth,
        false,
        '修復 CI 基礎設施問題'
      );
    }

    // 2. 檢查是否為 Flaky Test
    if (this.isFlakyTest(ciFailure, ciHealth)) {
      return this.createResult(
        ErrorType.CI_INDUCED,
        ErrorSeverity.MEDIUM,
        90,
        '偵測到不穩定的測試',
        ['標記測試為 flaky', '修復測試穩定性', '自動重跑'],
        ciHealth,
        true,
        '重跑並修復測試'
      );
    }

    // 3. 檢查 CI 是否整體不健康
    if (!ciHealth.isHealthy && ciHealth.failureRate > 0.5) {
      return this.createResult(
        ErrorType.CI_INDUCED,
        ErrorSeverity.CRITICAL,
        88,
        'CI pipeline 整體失敗率過高',
        ['檢查 CI 配置', '查看最近的變更', '聯系 CI 維護團隊'],
        ciHealth,
        false,
        '修復 CI pipeline'
      );
    }

    // 4. 檢查錯誤是否與 PR 相關
    const isPRRelated = this.isFailureRelatedToPR(prDiff, ciFailure);

    if (isPRRelated) {
      return this.createResult(
        ErrorType.PR_INDUCED,
        ErrorSeverity.HIGH,
        85,
        '錯誤與 PR 變更直接相關',
        ['修復 PR 中的代碼問題', '運行本地測試驗證'],
        ciHealth,
        false,
        '修正 PR 代碼'
      );
    }

    // 5. 如果無法確定
    return this.createResult(
      ErrorType.AMBIGUOUS,
      ErrorSeverity.MEDIUM,
      50,
      '無法確定錯誤來源',
      ['人工審查', '檢查日誌', '運行更多測試'],
      ciHealth,
      true,
      '需要人工審查'
    );
  }

  /**
   * 檢查是否為基礎設施錯誤
   */
  private isInfraError(ciFailure: CIFailure): boolean {
    const infraKeywords = [
      'timeout',
      'network',
      'connection refused',
      'docker pull',
      'out of memory',
      'OOM',
      'disk space',
      'permission denied',
      'certificate',
      'ssl',
      'tls',
      'rate limit',
      'quota exceeded',
      'service unavailable',
      '503',
      '504'
    ];

    const lowerLog = ciFailure.failureLog.toLowerCase();
    const lowerMessage = ciFailure.failureMessage.toLowerCase();

    return infraKeywords.some(keyword =>
      lowerLog.includes(keyword) || lowerMessage.includes(keyword)
    );
  }

  /**
   * 檢查是否為 Flaky Test
   */
  private isFlakyTest(ciFailure: CIFailure, ciHealth: CIHealthMetrics): boolean {
    // 檢查是否在 flaky tests 列表中
    if (ciHealth.flakyTests.includes(ciFailure.stepName)) {
      return true;
    }

    // 檢查過去失敗頻率
    if (ciHealth.last7DaysFailures >= this.config.flakyTestThreshold) {
      return true;
    }

    // 檢查測試名稱中的常見 flaky 模式
    const flakyPatterns = [
      'race condition',
      'timing',
      'async',
      'concurrent',
      'parallel',
      'flaky',
      'intermittent'
    ];

    const lowerName = ciFailure.stepName.toLowerCase();
    return flakyPatterns.some(pattern => lowerName.includes(pattern));
  }

  /**
   * 檢查失敗是否與 PR 相關
   */
  private isFailureRelatedToPR(prDiff: PRDiff, ciFailure: CIFailure): boolean {
    // 檢查失敗的文件是否在 PR 變更中
    const failedFilesInPR = ciFailure.failedFiles.some(file =>
      prDiff.changedFiles.includes(file)
    );

    if (failedFilesInPR) {
      return true;
    }

    // 檢查失敗的文件是否在 PR 變更的文件中
    // 注意：由於我們只有變更統計而不是具體行號，我們只能檢查文件級別的關聯
    for (const changedLine of prDiff.changedLines) {
      if (ciFailure.failedFiles.includes(changedLine.file)) {
        // 如果文件有變更（添加或刪除的行數大於0），認為相關
        if (changedLine.added > 0 || changedLine.removed > 0) {
          return true;
        }
      }
    }

    // 檢查模組是否相關
    const failedModulesInPR = ciFailure.failedFiles.some(file => {
      const fileModule = this.extractModule(file);
      return prDiff.changedModules.includes(fileModule);
    });

    if (failedModulesInPR) {
      return true;
    }

    return false;
  }

  /**
   * 提取模組名稱
   */
  private extractModule(filePath: string): string {
    const parts = filePath.split('/');
    return parts.length > 1 ? parts[0] : 'root';
  }

  /**
   * 創建分類結果
   */
  private createResult(
    errorType: ErrorType,
    severity: ErrorSeverity,
    confidence: number,
    reasoning: string,
    recommendations: string[],
    ciHealth?: CIHealthMetrics,
    shouldRerun: boolean = false,
    suggestedAction: string = ''
  ): ClassificationResult {
    return {
      errorType,
      severity,
      confidence,
      reasoning,
      recommendations,
      ciHealth,
      shouldRerun,
      suggestedAction
    };
  }

  /**
   * 處理 LLM 判斷結果
   */
  public processLLMJudgment(
    llmResponse: { errorType: ErrorType; confidence: number; reasoning: string },
    ruleBasedResult: ClassificationResult
  ): ClassificationResult {
    // 如果 LLM 信心度高，使用 LLM 結果
    if (llmResponse.confidence >= this.config.confidenceThreshold) {
      return {
        ...ruleBasedResult,
        errorType: llmResponse.errorType,
        confidence: llmResponse.confidence,
        reasoning: `LLM 判斷: ${llmResponse.reasoning}\n規則判斷: ${ruleBasedResult.reasoning}`,
        recommendations: [
          ...ruleBasedResult.recommendations,
          '基於 AI 分析的建議'
        ]
      };
    }

    // 否則使用規則結果，但保留 LLM 的洞察
    return {
      ...ruleBasedResult,
      reasoning: `${ruleBasedResult.reasoning}\n\nLLM 補充: ${llmResponse.reasoning}`
    };
  }
}