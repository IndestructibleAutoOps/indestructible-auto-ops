/**
 * CI Fail 自動分類系統 - 類型定義
 */

/**
 * 錯誤類型枚舉
 */
export enum ErrorType {
  PR_INDUCED = 'PR_INDUCED',        // 由 PR 內容直接造成
  CI_INDUCED = 'CI_INDUCED',        // CI pipeline 本身壞掉
  AMBIGUOUS = 'AMBIGUOUS'           // 無法判斷、需人工介入
}

/**
 * 錯誤嚴重程度
 */
export enum ErrorSeverity {
  CRITICAL = 'CRITICAL',            // 關鍵錯誤，必須立即處理
  HIGH = 'HIGH',                    // 高優先級
  MEDIUM = 'MEDIUM',                // 中等優先級
  LOW = 'LOW'                       // 低優先級
}

/**
 * PR 變更信息
 */
export interface PRDiff {
  prNumber: number;
  title: string;
  author: string;
  baseBranch: string;
  headBranch: string;
  changedFiles: string[];
  changedLines: {
    file: string;
    added: number;
    removed: number;
  }[];
  changedModules: string[];
  timestamp: number;
}

/**
 * CI 失敗信息
 */
export interface CIFailure {
  workflowName: string;
  workflowId: string;
  jobName: string;
  stepName: string;
  failureMessage: string;
  failureLog: string;
  failedFiles: string[];
  failedLines: number[];
  timestamp: number;
  runNumber: number;
  runId: string;
}

/**
 * CI 健康度指標
 */
export interface CIHealthMetrics {
  workflowName: string;
  timestamp: number;
  totalRuns: number;
  failureRate: number;
  averageDuration: number;
  last7DaysFailures: number;
  last30DaysFailures: number;
  flakyTests: string[];
  infraErrors: number;
  isHealthy: boolean;
}

/**
 * 語意比對結果
 */
export interface SemanticMatchResult {
  hasOverlap: boolean;
  overlapFiles: string[];
  overlapLines: number[];
  overlapModules: string[];
  similarityScore: number;        // 0-100
  confidenceLevel: 'HIGH' | 'MEDIUM' | 'LOW';
}

/**
 * 分類結果
 */
export interface ClassificationResult {
  errorType: ErrorType;
  severity: ErrorSeverity;
  confidence: number;             // 0-100
  reasoning: string;
  recommendations: string[];
  semanticMatch?: SemanticMatchResult;
  ciHealth?: CIHealthMetrics;
  shouldRerun: boolean;
  suggestedAction: string;
}

/**
 * 自動重跑策略
 */
export interface RerunStrategy {
  shouldRerun: boolean;
  maxReruns: number;
  rerunDelay: number;             // milliseconds
  rerunConditions: string[];
}

/**
 * LLM 判斷請求
 */
export interface LLMJudgmentRequest {
  prDiff: PRDiff;
  ciFailure: CIFailure;
  ciHistory: CIHealthMetrics;
  context: string;
}

/**
 * LLM 判斷響應
 */
export interface LLMJudgmentResponse {
  errorType: ErrorType;
  confidence: number;
  reasoning: string;
  evidence: string[];
}

/**
 * 系統配置
 */
export interface SystemConfig {
  enableLLMJudgment: boolean;
  enableAutoRerun: boolean;
  enableAutoLabeling: boolean;
  enableAutoComment: boolean;
  maxRerunAttempts: number;
  flakyTestThreshold: number;      // 過去 N 天失敗多少次算 flaky
  similarityThreshold: number;     // 語意相似度閾值
  confidenceThreshold: number;     // 信心度閾值
}