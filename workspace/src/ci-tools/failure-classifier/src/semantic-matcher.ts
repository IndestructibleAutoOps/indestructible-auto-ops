// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * 語意比對器 - 判斷 CI Fail 與 PR 的關聯性
 */

import { PRDiff, CIFailure, SemanticMatchResult } from './types.js';

export class SemanticMatcher {
  /**
   * 執行語意比對
   */
  public match(prDiff: PRDiff, ciFailure: CIFailure): SemanticMatchResult {
    const fileMatches = this.matchFiles(prDiff, ciFailure);
    const lineMatches = this.matchLines(prDiff, ciFailure);
    const moduleMatches = this.matchModules(prDiff, ciFailure);

    const similarityScore = this.calculateSimilarityScore(
      fileMatches,
      lineMatches,
      moduleMatches
    );

    const confidenceLevel = this.calculateConfidenceLevel(similarityScore);

    return {
      hasOverlap: similarityScore > 0,
      overlapFiles: this.getOverlapFiles(prDiff, ciFailure),
      overlapLines: lineMatches,
      overlapModules: moduleMatches,
      similarityScore,
      confidenceLevel
    };
  }

  /**
   * 比對文件
   */
  private matchFiles(prDiff: PRDiff, ciFailure: CIFailure): boolean {
    return ciFailure.failedFiles.some(file =>
      prDiff.changedFiles.includes(file)
    );
  }

  /**
   * 比對行數
   */
  private matchLines(prDiff: PRDiff, ciFailure: CIFailure): number[] {
    const overlappingLines: number[] = [];

    for (const failedFile of ciFailure.failedFiles) {
      const changedLineData = prDiff.changedLines.find(
        cl => cl.file === failedFile
      );

      if (!changedLineData) continue;

      // 由於我們只有變更統計而不是具體行號，
      // 如果該文件有變更（添加或刪除的行數大於0），我們認為所有失敗行都可能相關
      if (changedLineData.added > 0 || changedLineData.removed > 0) {
        for (const failedLine of ciFailure.failedLines) {
          overlappingLines.push(failedLine);
        }
      }
    }

    return [...new Set(overlappingLines)]; // 去重
  }

  /**
   * 比對模組
   */
  private matchModules(prDiff: PRDiff, ciFailure: CIFailure): string[] {
    const failedModules = ciFailure.failedFiles.map(file => this.extractModule(file));
    const overlappingModules = failedModules.filter(module =>
      prDiff.changedModules.includes(module)
    );

    return [...new Set(overlappingModules)]; // 去重
  }

  /**
   * 提取模組名稱
   */
  private extractModule(filePath: string): string {
    const parts = filePath.split('/');
    return parts.length > 1 ? parts[0] : 'root';
  }

  /**
   * 獲取重疊的文件
   */
  private getOverlapFiles(prDiff: PRDiff, ciFailure: CIFailure): string[] {
    return ciFailure.failedFiles.filter(file =>
      prDiff.changedFiles.includes(file)
    );
  }

  /**
   * 計算相似度分數
   */
  private calculateSimilarityScore(
    fileMatches: boolean,
    lineMatches: number[],
    moduleMatches: string[]
  ): number {
    let score = 0;

    // 文件匹配佔 40%
    if (fileMatches) {
      score += 40;
    }

    // 行數匹配佔 40%
    if (lineMatches.length > 0) {
      const lineScore = Math.min(40, lineMatches.length * 5);
      score += lineScore;
    }

    // 模組匹配佔 20%
    if (moduleMatches.length > 0) {
      score += 20;
    }

    return Math.min(100, score);
  }

  /**
   * 計算信心等級
   */
  private calculateConfidenceLevel(score: number): 'HIGH' | 'MEDIUM' | 'LOW' {
    if (score >= 70) return 'HIGH';
    if (score >= 40) return 'MEDIUM';
    return 'LOW';
  }

  /**
   * 分析錯誤類型
   */
  public analyzeErrorType(ciFailure: CIFailure): {
    isLintError: boolean;
    isFormatError: boolean;
    isTypeError: boolean;
    isTestError: boolean;
    isBuildError: boolean;
  } {
    const lowerLog = ciFailure.failureLog.toLowerCase();
    const lowerMessage = ciFailure.failureMessage.toLowerCase();

    return {
      isLintError: lowerLog.includes('lint') || lowerMessage.includes('lint'),
      isFormatError: lowerLog.includes('format') || lowerMessage.includes('format'),
      isTypeError: lowerLog.includes('type error') || lowerMessage.includes('type error'),
      isTestError: lowerLog.includes('test') || lowerMessage.includes('test'),
      isBuildError: lowerLog.includes('build') || lowerMessage.includes('build')
    };
  }

  /**
   * 檢查錯誤是否在 PR 變更的上下文中
   */
  public isInPRContext(prDiff: PRDiff, ciFailure: CIFailure): boolean {
    const semanticMatch = this.match(prDiff, ciFailure);
    return semanticMatch.hasOverlap && semanticMatch.confidenceLevel !== 'LOW';
  }

  /**
   * 詳細比對報告
   */
  public generateDetailedReport(
    prDiff: PRDiff,
    ciFailure: CIFailure
  ): {
    summary: string;
    details: Record<string, unknown>;
    recommendations: string[];
  } {
    const match = this.match(prDiff, ciFailure);
    const errorType = this.analyzeErrorType(ciFailure);

    let summary = '';
    let details: Record<string, unknown> = {};
    const recommendations: string[] = [];

    // 生成摘要
    if (match.hasOverlap) {
      summary = `錯誤與 PR 變更有直接關聯 (相似度: ${match.similarityScore}%)`;
      recommendations.push('檢查 PR 中相關文件的修改');
      recommendations.push('運行本地測試驗證修復');
    } else {
      summary = `錯誤與 PR 變更無明顯關聯 (相似度: ${match.similarityScore}%)`;
      recommendations.push('檢查 CI 配置');
      recommendations.push('考慮重跑 CI');
    }

    // 詳細信息
    details = {
      similarityScore: match.similarityScore,
      confidenceLevel: match.confidenceLevel,
      overlappingFiles: match.overlapFiles.length,
      overlappingLines: match.overlapLines.length,
      overlappingModules: match.overlapModules.length,
      errorType,
      prChanges: {
        totalFiles: prDiff.changedFiles.length,
        totalModules: prDiff.changedModules.length
      },
      ciFailure: {
        failedFiles: ciFailure.failedFiles.length,
        failedLines: ciFailure.failedLines.length
      }
    };

    // 根據錯誤類型添加建議
    if (errorType.isLintError) {
      recommendations.push('運行 linter 修復自動可修復的問題');
    }
    if (errorType.isFormatError) {
      recommendations.push('運行 formatter 修復格式問題');
    }
    if (errorType.isTypeError) {
      recommendations.push('檢查類型定義和導入');
    }
    if (errorType.isTestError) {
      recommendations.push('檢查測試用例和測試數據');
    }

    return { summary, details, recommendations };
  }
}