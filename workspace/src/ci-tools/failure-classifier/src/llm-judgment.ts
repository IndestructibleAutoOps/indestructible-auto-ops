// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * LLM 語意判斷器 - 使用 AI 進行智能分類
 */

import { ErrorType, LLMJudgmentRequest, LLMJudgmentResponse, ClassificationResult } from './types.js';

export class LLMJudgment {
  /**
   * 請求 LLM 判斷
   */
  public async requestJudgment(request: LLMJudgmentRequest): Promise<LLMJudgmentResponse> {
    // 構建提示詞
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const prompt = this.buildPrompt(request);

    // 在實際應用中，這裡會調用 LLM API
    // 這裡我們使用模擬的 LLM 響應
    const response = await this.simulateLLMResponse(request);

    return response;
  }

  /**
   * 構建提示詞
   */
  private buildPrompt(request: LLMJudgmentRequest): string {
    const { prDiff, ciFailure, ciHistory, context } = request;

    return `
你是一個 CI/CD 專家，需要判斷 CI 失敗是由 PR 內容造成還是 CI 系統本身問題。

## PR 信息
- PR 號碼: ${prDiff.prNumber}
- 標題: ${prDiff.title}
- 作者: ${prDiff.author}
- 變更文件: ${prDiff.changedFiles.join(', ')}
- 變更模組: ${prDiff.changedModules.join(', ')}

## CI 失敗信息
- Workflow: ${ciFailure.workflowName}
- Job: ${ciFailure.jobName}
- Step: ${ciFailure.stepName}
- 失敗訊息: ${ciFailure.failureMessage}
- 失敗文件: ${ciFailure.failedFiles.join(', ')}

## CI 健康度
- 失敗率: ${(ciHistory.failureRate * 100).toFixed(1)}%
- 最近 7 天失敗: ${ciHistory.last7DaysFailures} 次
- Flaky tests: ${ciHistory.flakyTests.join(', ')}
- 系統健康: ${ciHistory.isHealthy ? '健康' : '不健康'}

## 上下文
${context}

## 請判斷
這個 CI 失敗是 PR 問題還是 CI 問題？

請回答：
1. 錯誤類型 (PR_INDUCED / CI_INDUCED / AMBIGUOUS)
2. 信心度 (0-100)
3. 推理理由
4. 支持證據

請以 JSON 格式返回：
{
  "errorType": "PR_INDUCED | CI_INDUCED | AMBIGUOUS",
  "confidence": 85,
  "reasoning": "詳細理由",
  "evidence": ["證據1", "證據2"]
}
`;
  }

  /**
   * 模擬 LLM 響應
   * 在實際應用中，這裡會調用真實的 LLM API
   */
  private async simulateLLMResponse(request: LLMJudgmentRequest): Promise<LLMJudgmentResponse> {
    // 這是一個模擬實現，實際應該調用 LLM API
    // 例如 OpenAI API、Anthropic API、或其他 LLM 服務

    const { prDiff, ciFailure, ciHistory } = request;

    // 模擬邏輯
    let errorType: ErrorType;
    let confidence: number;
    let reasoning: string;
    const evidence: string[] = [];

    // 檢查是否為基礎設施錯誤
    const infraKeywords = ['timeout', 'network', 'connection', 'docker', 'memory'];
    const hasInfraError = infraKeywords.some(keyword =>
      ciFailure.failureMessage.toLowerCase().includes(keyword)
    );

    if (hasInfraError) {
      errorType = ErrorType.CI_INDUCED;
      confidence = 90;
      reasoning = '檢測到基礎設施相關錯誤，這類錯誤通常與 PR 代碼無關';
      evidence.push('錯誤訊息包含基礎設施關鍵字');
      evidence.push('CI 健康度顯示系統不穩定');
    } else if (ciHistory.last7DaysFailures >= 3) {
      errorType = ErrorType.CI_INDUCED;
      confidence = 85;
      reasoning = '該測試在過去 7 天內多次失敗，可能是 flaky test';
      evidence.push(`過去 7 天失敗 ${ciHistory.last7DaysFailures} 次`);
      evidence.push('CI 健康度顯示存在 flaky tests');
    } else {
      // 檢查 PR 變更是否與失敗相關
      const hasOverlap = ciFailure.failedFiles.some(file =>
        prDiff.changedFiles.includes(file)
      );

      if (hasOverlap) {
        errorType = ErrorType.PR_INDUCED;
        confidence = 80;
        reasoning = '失敗的文件包含在 PR 變更中，錯誤很可能由 PR 引起';
        evidence.push('PR 變更了失敗的文件');
        evidence.push('錯誤出現在 PR 修改的代碼路徑中');
      } else {
        errorType = ErrorType.AMBIGUOUS;
        confidence = 60;
        reasoning = '無法確定錯誤來源，需要更多信息或人工判斷';
        evidence.push('PR 變更與失敗文件無直接關聯');
        evidence.push('CI 健康度正常');
      }
    }

    return {
      errorType,
      confidence,
      reasoning,
      evidence
    };
  }

  /**
   * 集成 LLM 判斷到分類結果
   */
  public integrateLLMJudgment(
    llmResponse: LLMJudgmentResponse,
    ruleBasedResult: ClassificationResult,
    confidenceThreshold: number
  ): ClassificationResult {
    // 如果 LLM 信心度高，優先使用 LLM 結果
    if (llmResponse.confidence >= confidenceThreshold) {
      return {
        ...ruleBasedResult,
        errorType: llmResponse.errorType,
        confidence: Math.max(ruleBasedResult.confidence, llmResponse.confidence),
        reasoning: this.combineReasonings(
          'LLM 判斷',
          llmResponse.reasoning,
          ruleBasedResult.reasoning
        ),
        recommendations: [
          ...ruleBasedResult.recommendations,
          ...this.generateLLMRecommendations(llmResponse)
        ]
      };
    }

    // 否則，結合兩種判斷
    return {
      ...ruleBasedResult,
      reasoning: this.combineReasonings(
        '綜合判斷',
        ruleBasedResult.reasoning,
        llmResponse.reasoning
      ),
      confidence: (ruleBasedResult.confidence + llmResponse.confidence) / 2
    };
  }

  /**
   * 組合理由
   */
  private combineReasonings(
    source: string,
    reasoning1: string,
    reasoning2: string
  ): string {
    return `### ${source}\n\n${reasoning1}\n\n---\n\n${reasoning2}`;
  }

  /**
   * 生成 LLM 建議
   */
  private generateLLMRecommendations(llmResponse: LLMJudgmentResponse): string[] {
    const recommendations: string[] = [];

    if (llmResponse.errorType === ErrorType.PR_INDUCED) {
      recommendations.push('LLM 建議：修復 PR 代碼中的問題');
      recommendations.push('LLM 建議：運行本地測試驗證修復');
    } else if (llmResponse.errorType === ErrorType.CI_INDUCED) {
      recommendations.push('LLM 建議：檢查 CI 配置和環境');
      recommendations.push('LLM 建議：聯系 DevOps 團隊');
      recommendations.push('LLM 建議：考慮重跑 CI');
    } else {
      recommendations.push('LLM 建議：進行人工審查');
      recommendations.push('LLM 建議：收集更多錯誤信息');
    }

    return recommendations;
  }

  /**
   * 批量判斷
   */
  public async batchJudge(requests: LLMJudgmentRequest[]): Promise<LLMJudgmentResponse[]> {
    const responses: LLMJudgmentResponse[] = [];

    for (const request of requests) {
      const response = await this.requestJudgment(request);
      responses.push(response);
    }

    return responses;
  }

  /**
   * 獲取判斷統計
   */
  public getJudgmentStatistics(responses: LLMJudgmentResponse[]): {
    total: number;
    prInduced: number;
    ciInduced: number;
    ambiguous: number;
    averageConfidence: number;
  } {
    const total = responses.length;
    const prInduced = responses.filter(r => r.errorType === ErrorType.PR_INDUCED).length;
    const ciInduced = responses.filter(r => r.errorType === ErrorType.CI_INDUCED).length;
    const ambiguous = responses.filter(r => r.errorType === ErrorType.AMBIGUOUS).length;

    const averageConfidence = responses.reduce((sum, r) => sum + r.confidence, 0) / total;

    return {
      total,
      prInduced,
      ciInduced,
      ambiguous,
      averageConfidence
    };
  }
}