// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * 結果格式化器 - 生成清晰的判斷結論
 */

import { ClassificationResult, ErrorType, ErrorSeverity, SemanticMatchResult } from './types.js';

export class ResultFormatter {
  /**
   * 生成完整的判斷報告
   */
  public generateReport(
    classificationResult: ClassificationResult,
    semanticMatch?: SemanticMatchResult
  ): string {
    const lines: string[] = [];

    // 標題
    lines.push('# CI Fail 自動分類判斷報告\n');

    // 結論
    lines.push('## 🎯 判斷結論\n');
    lines.push(`**錯誤類型**: ${this.getErrorTypeLabel(classificationResult.errorType)}\n`);
    lines.push(`**嚴重程度**: ${this.getSeverityLabel(classificationResult.severity)}\n`);
    lines.push(`**信心度**: ${classificationResult.confidence}%\n`);
    lines.push(`**建議操作**: ${classificationResult.suggestedAction}\n`);

    // 推理
    lines.push('## 🧠 推理分析\n');
    lines.push(classificationResult.reasoning);
    lines.push('');

    // 語意比對結果
    if (semanticMatch) {
      lines.push('## 🔍 語意比對結果\n');
      lines.push(`**是否有重疊**: ${semanticMatch.hasOverlap ? '是' : '否'}\n`);
      lines.push(`**相似度分數**: ${semanticMatch.similarityScore}%\n`);
      lines.push(`**信心等級**: ${semanticMatch.confidenceLevel}\n`);

      if (semanticMatch.overlapFiles.length > 0) {
        lines.push('**重疊文件**:\n');
        for (const file of semanticMatch.overlapFiles) {
          lines.push(`  - ${file}`);
        }
        lines.push('');
      }

      if (semanticMatch.overlapLines.length > 0) {
        lines.push('**重疊行數**:\n');
        lines.push(`  ${semanticMatch.overlapLines.join(', ')}\n`);
      }

      if (semanticMatch.overlapModules.length > 0) {
        lines.push('**重疊模組**:\n');
        for (const module of semanticMatch.overlapModules) {
          lines.push(`  - ${module}`);
        }
        lines.push('');
      }
    }

    // CI 健康度
    if (classificationResult.ciHealth) {
      lines.push('## 📊 CI 健康度\n');
      lines.push(`**系統狀態**: ${classificationResult.ciHealth.isHealthy ? '✅ 健康' : '❌ 不健康'}\n`);
      lines.push(`**失敗率**: ${(classificationResult.ciHealth.failureRate * 100).toFixed(1)}%\n`);
      lines.push(`**最近 7 天失敗**: ${classificationResult.ciHealth.last7DaysFailures} 次\n`);
      lines.push(`**最近 30 天失敗**: ${classificationResult.ciHealth.last30DaysFailures} 次\n`);

      if (classificationResult.ciHealth.flakyTests.length > 0) {
        lines.push('**Flaky Tests**:\n');
        for (const test of classificationResult.ciHealth.flakyTests) {
          lines.push(`  - ${test}`);
        }
        lines.push('');
      }
    }

    // 建議
    lines.push('## 💡 建議行動\n');
    for (let i = 0; i < classificationResult.recommendations.length; i++) {
      lines.push(`${i + 1}. ${classificationResult.recommendations[i]}`);
    }
    lines.push('');

    // 重跑策略
    lines.push('## 🔄 重跑策略\n');
    if (classificationResult.shouldRerun) {
      lines.push('✅ 建議自動重跑 CI\n');
    } else {
      lines.push('❌ 不建議重跑 CI\n');
    }
    lines.push('');

    return lines.join('');
  }

  /**
   * 生成簡潔摘要
   */
  public generateSummary(classificationResult: ClassificationResult): string {
    const typeEmoji = this.getErrorTypeEmoji(classificationResult.errorType);
    const severityEmoji = this.getSeverityEmoji(classificationResult.severity);

    return `
${typeEmoji} **${this.getErrorTypeLabel(classificationResult.errorType)}** | 
${severityEmoji} **${this.getSeverityLabel(classificationResult.severity)}** | 
📊 **${classificationResult.confidence}%** 信心度

${classificationResult.reasoning}

建議: ${classificationResult.suggestedAction}
    `.trim();
  }

  /**
   * 生成 PR 評論
   */
  public generatePRComment(
    classificationResult: ClassificationResult,
    semanticMatch?: SemanticMatchResult
  ): string {
    const lines: string[] = [];

    lines.push('## 🤖 CI Fail 自動分析結果\n');

    // 主要結論
    const typeEmoji = this.getErrorTypeEmoji(classificationResult.errorType);
    lines.push(`### ${typeEmoji} 判斷結果\n`);
    lines.push(`**${this.getErrorTypeLabel(classificationResult.errorType)}**\n`);
    lines.push(`信心度: ${classificationResult.confidence}%\n`);
    lines.push('');

    // 詳細分析
    lines.push('### 📋 分析詳情\n');
    lines.push(classificationResult.reasoning);
    lines.push('');

    // 語意比對
    if (semanticMatch && semanticMatch.hasOverlap) {
      lines.push('### 🔗 與 PR 的關聯\n');
      lines.push(`相似度: ${semanticMatch.similarityScore}%\n`);
      lines.push(`重疊文件: ${semanticMatch.overlapFiles.length} 個\n`);
      lines.push('');
    }

    // 建議
    lines.push('### 💡 建議\n');
    for (const recommendation of classificationResult.recommendations) {
      lines.push(`- ${recommendation}`);
    }
    lines.push('');

    // 自動標記
    lines.push('---\n');
    lines.push('*此評論由 CI Fail 自動分類系統生成*');

    return lines.join('');
  }

  /**
   * 生成 Label 標籤
   */
  public generateLabels(classificationResult: ClassificationResult): string[] {
    const labels: string[] = [];

    // 主要類型標籤
    switch (classificationResult.errorType) {
      case ErrorType.PR_INDUCED:
        labels.push('needs-fix', 'pr-issue');
        break;
      case ErrorType.CI_INDUCED:
        labels.push('ci-issue', 'needs-review');
        break;
      case ErrorType.AMBIGUOUS:
        labels.push('needs-human-review', 'ambiguous');
        break;
    }

    // 嚴重程度標籤
    switch (classificationResult.severity) {
      case ErrorSeverity.CRITICAL:
        labels.push('critical');
        break;
      case ErrorSeverity.HIGH:
        labels.push('high-priority');
        break;
      case ErrorSeverity.MEDIUM:
        labels.push('medium-priority');
        break;
      case ErrorSeverity.LOW:
        labels.push('low-priority');
        break;
    }

    // 附加標籤
    if (classificationResult.shouldRerun) {
      labels.push('auto-rerun');
    }

    if (classificationResult.ciHealth?.isHealthy === false) {
      labels.push('ci-unhealthy');
    }

    return labels;
  }

  /**
   * 生成 JSON 格式
   */
  public generateJSON(classificationResult: ClassificationResult): string {
    return JSON.stringify(classificationResult, null, 2);
  }

  /**
   * 生成 Markdown 表格
   */
  public generateTable(results: ClassificationResult[]): string {
    const lines: string[] = [];

    lines.push('| 類型 | 嚴重程度 | 信心度 | 建議操作 |');
    lines.push('|------|----------|--------|----------|');

    for (const result of results) {
      lines.push(
        `| ${this.getErrorTypeLabel(result.errorType)} | ` +
        `${this.getSeverityLabel(result.severity)} | ` +
        `${result.confidence}% | ` +
        `${result.suggestedAction} |`
      );
    }

    return lines.join('\n');
  }

  /**
   * 獲取錯誤類型標籤
   */
  private getErrorTypeLabel(type: ErrorType): string {
    switch (type) {
      case ErrorType.PR_INDUCED:
        return 'PR 問題';
      case ErrorType.CI_INDUCED:
        return 'CI 問題';
      case ErrorType.AMBIGUOUS:
        return '無法判斷';
      default:
        return '未知';
    }
  }

  /**
   * 獲取錯誤類型表情符號
   */
  private getErrorTypeEmoji(type: ErrorType): string {
    switch (type) {
      case ErrorType.PR_INDUCED:
        return '🔴';
      case ErrorType.CI_INDUCED:
        return '🟡';
      case ErrorType.AMBIGUOUS:
        return '🟠';
      default:
        return '⚪';
    }
  }

  /**
   * 獲取嚴重程度標籤
   */
  private getSeverityLabel(severity: ErrorSeverity): string {
    switch (severity) {
      case ErrorSeverity.CRITICAL:
        return '關鍵';
      case ErrorSeverity.HIGH:
        return '高';
      case ErrorSeverity.MEDIUM:
        return '中';
      case ErrorSeverity.LOW:
        return '低';
      default:
        return '未知';
    }
  }

  /**
   * 獲取嚴重程度表情符號
   */
  private getSeverityEmoji(severity: ErrorSeverity): string {
    switch (severity) {
      case ErrorSeverity.CRITICAL:
        return '🚨';
      case ErrorSeverity.HIGH:
        return '⚠️';
      case ErrorSeverity.MEDIUM:
        return '📊';
      case ErrorSeverity.LOW:
        return 'ℹ️';
      default:
        return '❓';
    }
  }
}