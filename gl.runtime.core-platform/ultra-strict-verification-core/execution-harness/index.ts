# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: execution-harness-integration
# @GL-charter-version: 2.0.0

/**
 * Execution-Grounded Reality Harness: Unified Execution System
 * 
 * Core Philosophy: "禁止「只產生報告」的虛假驗證"
 * (Prohibit "report-only" false verification)
 * 
 * Purpose: Enforce actual execution and verification of all components
 * 
 * This module integrates all Execution-Harness components:
 * - Real Runner: Actually execute code and verify real behavior
 * - Baseline Comparator: Compare current behavior against established baselines
 * - Oracle Validator: Validate system behavior against trusted oracles
 * - Stress Tester: Test components under extreme load
 * - Fuzzing Engine: Fuzz test components to find vulnerabilities
 * - Regression Diff: Detect regressions between versions
 */

import { IExecutionHarness } from '../types';
import { RealRunner } from './real-runner/real-runner';
import { BaselineComparator } from './baseline-comparator/baseline-comparator';
import { OracleValidator } from './oracle-validator/oracle-validator';
import { StressTester } from './stress-tester/stress-tester';
import { FuzzingEngine } from './fuzzing-engine/fuzzing-engine';
import { RegressionDiff } from './regression-diff/regression-diff';

export class ExecutionHarness implements IExecutionHarness {
  private realRunner: RealRunner;
  private baselineComparator: BaselineComparator;
  private oracleValidator: OracleValidator;
  private stressTester: StressTester;
  private fuzzingEngine: FuzzingEngine;
  private regressionDiff: RegressionDiff;

  constructor() {
    this.realRunner = new RealRunner();
    this.baselineComparator = new BaselineComparator();
    this.oracleValidator = new OracleValidator();
    this.stressTester = new StressTester();
    this.fuzzingEngine = new FuzzingEngine();
    this.regressionDiff = new RegressionDiff();
  }

  /**
   * Execute real scenario and verify results
   * 
   * This method actually executes code and verifies real behavior
   */
  async executeReal(component: string, scenario: string): Promise<any> {
    return await this.realRunner.executeReal(component, scenario);
  }

  /**
   * Compare metrics against baseline
   * 
   * This method compares current behavior against established baselines
   */
  async compareBaseline(component: string, metrics: any): Promise<any> {
    return await this.baselineComparator.compareBaseline(component, metrics);
  }

  /**
   * Validate against oracle
   * 
   * This method validates system behavior against trusted oracles
   */
  async validateOracle(component: string, oracle: string): Promise<any> {
    return await this.oracleValidator.validateOracle(component, oracle);
  }

  /**
   * Stress test a component
   * 
   * This method tests components under extreme load
   */
  async stressTest(component: string, maxLoad: number): Promise<any> {
    return await this.stressTester.stressTest(component, maxLoad);
  }

  /**
   * Fuzz test a component
   * 
   * This method fuzz tests components to find vulnerabilities
   */
  async fuzzTest(component: string, iterations: number): Promise<any> {
    return await this.fuzzingEngine.fuzzTest(component, iterations);
  }

  /**
   * Detect regressions between current and previous version
   * 
   * This method detects regressions between versions
   */
  async detectRegression(component: string, previousVersion: string): Promise<any> {
    return await this.regressionDiff.detectRegression(component, previousVersion);
  }

  /**
   * Execute complete Execution-Harness verification
   * 
   * Runs all six Execution-Harness components and returns aggregated results
   */
  async executeFullExecutionVerification(component: string, config: {
    scenarios?: string[];
    metrics?: any;
    oracle?: string;
    maxLoad?: number;
    fuzzIterations?: number;
    previousVersion?: string;
  } = {}): Promise<{
    executions: any[];
    baselineComparisons: any[];
    oracleValidations: any[];
    stressTests: any[];
    fuzzingResults: any[];
    regressionDiffs: any[];
    summary: {
      totalExecutions: number;
      totalBaselineDifferences: number;
      totalOracleViolations: number;
      totalStressFailures: number;
      totalCrashes: number;
      totalRegressions: number;
      overallStatus: 'FAILED' | 'PASSED' | 'CONDITIONAL';
    };
  }> {
    const results = {
      executions: [] as any[],
      baselineComparisons: [] as any[],
      oracleValidations: [] as any[],
      stressTests: [] as any[],
      fuzzingResults: [] as any[],
      regressionDiffs: [] as any[]
    };

    // Execute scenarios
    if (config.scenarios && config.scenarios.length > 0) {
      for (const scenario of config.scenarios) {
        const result = await this.executeReal(component, scenario);
        results.executions.push(result);
      }
    }

    // Compare baseline
    if (config.metrics) {
      const result = await this.compareBaseline(component, config.metrics);
      results.baselineComparisons.push(result);
    }

    // Validate oracle
    if (config.oracle) {
      const result = await this.validateOracle(component, config.oracle);
      results.oracleValidations.push(result);
    }

    // Stress test
    if (config.maxLoad) {
      const result = await this.stressTest(component, config.maxLoad);
      results.stressTests.push(result);
    }

    // Fuzz test
    if (config.fuzzIterations) {
      const result = await this.fuzzTest(component, config.fuzzIterations);
      results.fuzzingResults.push(result);
    }

    // Detect regression
    if (config.previousVersion) {
      const result = await this.detectRegression(component, config.previousVersion);
      results.regressionDiffs.push(result);
    }

    // Calculate summary
    const totalExecutions = results.executions.length;
    const totalBaselineDifferences = results.baselineComparisons.reduce((sum, r) => sum + (r.differences?.length || 0), 0);
    const totalOracleViolations = results.oracleValidations.reduce((sum, r) => sum + (r.violations?.length || 0), 0);
    const totalStressFailures = results.stressTests.reduce((sum, r) => sum + (r.failures?.length || 0), 0);
    const totalCrashes = results.fuzzingResults.reduce((sum, r) => sum + (r.crashes || 0), 0);
    const totalRegressions = results.regressionDiffs.reduce((sum, r) => sum + (r.regressions?.length || 0), 0);

    // Determine overall status
    let overallStatus: 'FAILED' | 'PASSED' | 'CONDITIONAL' = 'PASSED';
    
    if (totalCrashes > 0 || totalStressFailures > 0 || totalRegressions > 0) {
      overallStatus = 'FAILED';
    } else if (totalBaselineDifferences > 0 || totalOracleViolations > 0) {
      overallStatus = 'CONDITIONAL';
    }

    return {
      ...results,
      summary: {
        totalExecutions,
        totalBaselineDifferences,
        totalOracleViolations,
        totalStressFailures,
        totalCrashes,
        totalRegressions,
        overallStatus
      }
    };
  }
}

// Export all components for individual use
export { RealRunner } from './real-runner/real-runner';
export { BaselineComparator } from './baseline-comparator/baseline-comparator';
export { OracleValidator } from './oracle-validator/oracle-validator';
export { StressTester } from './stress-tester/stress-tester';
export { FuzzingEngine } from './fuzzing-engine/fuzzing-engine';
export { RegressionDiff } from './regression-diff/regression-diff';