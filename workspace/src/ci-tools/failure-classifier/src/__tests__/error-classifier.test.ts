/**
 * Error Classifier 測試
 */

import { ErrorClassifier } from '../error-classifier.js';
import { SystemConfig, PRDiff, CIFailure, CIHealthMetrics, ErrorType, ErrorSeverity } from '../types.js';

describe('ErrorClassifier', () => {
  let classifier: ErrorClassifier;
  let config: SystemConfig;

  beforeEach(() => {
    config = {
      enableLLMJudgment: false,
      enableAutoRerun: true,
      enableAutoLabeling: true,
      enableAutoComment: true,
      maxRerunAttempts: 3,
      flakyTestThreshold: 3,
      similarityThreshold: 40,
      confidenceThreshold: 70
    };
    classifier = new ErrorClassifier(config);
  });

  describe('分類基礎設施錯誤', () => {
    it('應該正確識別 timeout 錯誤', () => {
      const prDiff: PRDiff = {
        prNumber: 123,
        title: 'Test PR',
        author: 'test',
        baseBranch: 'main',
        headBranch: 'feature',
        changedFiles: [],
        changedLines: [],
        changedModules: [],
        timestamp: Date.now()
      };

      const ciFailure: CIFailure = {
        workflowName: 'test-workflow',
        workflowId: '1',
        jobName: 'test-job',
        stepName: 'test-step',
        failureMessage: 'Connection timeout',
        failureLog: 'Error: Connection timeout after 30s',
        failedFiles: [],
        failedLines: [],
        timestamp: Date.now(),
        runNumber: 1,
        runId: '1'
      };

      const ciHealth: CIHealthMetrics = {
        workflowName: 'test-workflow',
        timestamp: Date.now(),
        totalRuns: 10,
        failureRate: 0.2,
        averageDuration: 300,
        last7DaysFailures: 2,
        last30DaysFailures: 5,
        flakyTests: [],
        infraErrors: 1,
        isHealthy: true
      };

      const result = classifier.classify(prDiff, ciFailure, ciHealth);

      expect(result.errorType).toBe(ErrorType.CI_INDUCED);
      expect(result.severity).toBe(ErrorSeverity.HIGH);
      expect(result.confidence).toBeGreaterThanOrEqual(90);
    });

    it('應該正確識別 OOM 錯誤', () => {
      const ciFailure: CIFailure = {
        workflowName: 'test-workflow',
        workflowId: '1',
        jobName: 'test-job',
        stepName: 'test-step',
        failureMessage: 'Out of memory',
        failureLog: 'Error: Process out of memory',
        failedFiles: [],
        failedLines: [],
        timestamp: Date.now(),
        runNumber: 1,
        runId: '1'
      };

      const prDiff: PRDiff = {
        prNumber: 123,
        title: 'Test PR',
        author: 'test',
        baseBranch: 'main',
        headBranch: 'feature',
        changedFiles: [],
        changedLines: [],
        changedModules: [],
        timestamp: Date.now()
      };

      const ciHealth: CIHealthMetrics = {
        workflowName: 'test-workflow',
        timestamp: Date.now(),
        totalRuns: 10,
        failureRate: 0.2,
        averageDuration: 300,
        last7DaysFailures: 2,
        last30DaysFailures: 5,
        flakyTests: [],
        infraErrors: 1,
        isHealthy: true
      };

      const result = classifier.classify(prDiff, ciFailure, ciHealth);

      expect(result.errorType).toBe(ErrorType.CI_INDUCED);
      expect(result.shouldRerun).toBe(false);
    });
  });

  describe('分類 Flaky Test', () => {
    it('應該正確識別 flaky test', () => {
      const prDiff: PRDiff = {
        prNumber: 123,
        title: 'Test PR',
        author: 'test',
        baseBranch: 'main',
        headBranch: 'feature',
        changedFiles: [],
        changedLines: [],
        changedModules: [],
        timestamp: Date.now()
      };

      const ciFailure: CIFailure = {
        workflowName: 'test-workflow',
        workflowId: '1',
        jobName: 'test-job',
        stepName: 'test-flaky-test',
        failureMessage: 'Test failed',
        failureLog: 'Error: Test assertion failed',
        failedFiles: [],
        failedLines: [],
        timestamp: Date.now(),
        runNumber: 1,
        runId: '1'
      };

      const ciHealth: CIHealthMetrics = {
        workflowName: 'test-workflow',
        timestamp: Date.now(),
        totalRuns: 10,
        failureRate: 0.3,
        averageDuration: 300,
        last7DaysFailures: 4,
        last30DaysFailures: 10,
        flakyTests: ['test-flaky-test'],
        infraErrors: 0,
        isHealthy: false
      };

      const result = classifier.classify(prDiff, ciFailure, ciHealth);

      expect(result.errorType).toBe(ErrorType.CI_INDUCED);
      expect(result.shouldRerun).toBe(true);
    });
  });

  describe('分類 PR 相關錯誤', () => {
    it('應該正確識別 PR 引起的錯誤', () => {
      const prDiff: PRDiff = {
        prNumber: 123,
        title: 'Test PR',
        author: 'test',
        baseBranch: 'main',
        headBranch: 'feature',
        changedFiles: ['src/index.ts'],
        changedLines: [
          {
            file: 'src/index.ts',
            added: 3,
            removed: 0
          }
        ],
        changedModules: ['src'],
        timestamp: Date.now()
      };

      const ciFailure: CIFailure = {
        workflowName: 'test-workflow',
        workflowId: '1',
        jobName: 'test-job',
        stepName: 'test-step',
        failureMessage: 'Type error in src/index.ts:12',
        failureLog: 'Error: Type mismatch at line 12',
        failedFiles: ['src/index.ts'],
        failedLines: [12],
        timestamp: Date.now(),
        runNumber: 1,
        runId: '1'
      };

      const ciHealth: CIHealthMetrics = {
        workflowName: 'test-workflow',
        timestamp: Date.now(),
        totalRuns: 10,
        failureRate: 0.1,
        averageDuration: 300,
        last7DaysFailures: 1,
        last30DaysFailures: 2,
        flakyTests: [],
        infraErrors: 0,
        isHealthy: true
      };

      const result = classifier.classify(prDiff, ciFailure, ciHealth);

      expect(result.errorType).toBe(ErrorType.PR_INDUCED);
      expect(result.shouldRerun).toBe(false);
    });
  });

  describe('LLM 判斷整合', () => {
    it('應該正確整合 LLM 判斷', () => {
      const prDiff: PRDiff = {
        prNumber: 123,
        title: 'Test PR',
        author: 'test',
        baseBranch: 'main',
        headBranch: 'feature',
        changedFiles: [],
        changedLines: [],
        changedModules: [],
        timestamp: Date.now()
      };

      const ciFailure: CIFailure = {
        workflowName: 'test-workflow',
        workflowId: '1',
        jobName: 'test-job',
        stepName: 'test-step',
        failureMessage: 'Test failed',
        failureLog: 'Error: Test failed',
        failedFiles: [],
        failedLines: [],
        timestamp: Date.now(),
        runNumber: 1,
        runId: '1'
      };

      const ciHealth: CIHealthMetrics = {
        workflowName: 'test-workflow',
        timestamp: Date.now(),
        totalRuns: 10,
        failureRate: 0.1,
        averageDuration: 300,
        last7DaysFailures: 1,
        last30DaysFailures: 2,
        flakyTests: [],
        infraErrors: 0,
        isHealthy: true
      };

      const ruleBasedResult = classifier.classify(prDiff, ciFailure, ciHealth);

      const llmResponse = {
        errorType: ErrorType.CI_INDUCED,
        confidence: 85,
        reasoning: 'LLM 判斷這是 CI 問題',
        evidence: ['證據1', '證據2']
      };

      const integratedResult = classifier.processLLMJudgment(
        llmResponse,
        ruleBasedResult
      );

      expect(integratedResult.errorType).toBe(ErrorType.CI_INDUCED);
      expect(integratedResult.confidence).toBeGreaterThanOrEqual(80);
      expect(integratedResult.reasoning).toContain('LLM 判斷');
    });
  });
});