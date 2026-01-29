# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: ultra-strict-verification-core-types
# @GL-charter-version: 2.0.0

/**
 * Ultra-Strict Verification Core - Type Definitions
 * 
 * Core Philosophy: "推翻 GL 所有的結論，直到剩下的部分是真正站得住的。"
 * (Overturn all GL conclusions until only what truly stands remains.)
 */

// ============================================================================
// Core Verification Types
// ============================================================================

/**
 * Severity levels for verification findings
 */
export enum VerificationSeverity {
  CRITICAL = 'CRITICAL',      // System-breaking issues
  HIGH = 'HIGH',            // Major inconsistencies or contradictions
  MEDIUM = 'MEDIUM',        // Significant concerns
  LOW = 'LOW',              // Minor issues
  INFO = 'INFO'             // Observations
}

/**
 * Verification finding types
 */
export enum VerificationFindingType {
  CONTRADICTION = 'CONTRADICTION',              // Direct logical contradictions
  INCONSISTENCY = 'INCONSISTENCY',              // Inconsistent behavior or data
  ASSUMPTION_VIOLATION = 'ASSUMPTION_VIOLATION',// Invalid assumptions
  SEMANTIC_MISMATCH = 'SEMANTIC_MISMATCH',      // Semantic differences
  BEHAVIOR_DIVERGENCE = 'BEHAVIOR_DIVERGENCE',  // Actual vs expected behavior diff
  REALITY_VS_REPORT = 'REALITY_VS_REPORT',      // Report doesn't match reality
  PATTERN_BREAK = 'PATTERN_BREAK',              // Established pattern violations
  ADVERSARIAL_FAILURE = 'ADVERSARIAL_FAILURE',  // Failed under adversarial conditions
  EXTREME_BOUNDARY = 'EXTREME_BOUNDARY',        // Boundary condition failures
  REGRESSION = 'REGRESSION',                    // Functional regressions
  PERFORMANCE_DEGRADATION = 'PERFORMANCE_DEGRADATION',  // Performance issues
  SECURITY_VULNERABILITY = 'SECURITY_VULNERABILITY',    // Security concerns
  GOVERNANCE_VIOLATION = 'GOVERNANCE_VIOLATION',        // Governance violations
  UNVERIFIED_CLAIM = 'UNVERIFIED_CLAIM',        // Claims without evidence
  FALSIFICATION_SUCCESS = 'FALSIFICATION_SUCCESS',      // Successfully falsified claim
}

/**
 * Verification finding result
 */
export interface VerificationFinding {
  id: string;
  type: VerificationFindingType;
  severity: VerificationSeverity;
  component: string;
  location: {
    file?: string;
    line?: number;
    column?: number;
    module?: string;
  };
  title: string;
  description: string;
  evidence: Evidence[];
  contradiction?: {
    claim: string;
    counterexample: string;
    proof: string;
  };
  metrics?: {
    expected: any;
    actual: any;
    divergence: any;
  };
  timestamp: Date;
  verified: boolean;
  falsifiable: boolean;
}

/**
 * Evidence supporting a finding
 */
export interface Evidence {
  type: 'code' | 'execution' | 'data' | 'report' | 'baseline' | 'oracle';
  source: string;
  content: any;
  timestamp: Date;
  verified: boolean;
}

/**
 * Verification context for tracking
 */
export interface VerificationContext {
  executionId: string;
  startTime: Date;
  scope: string[];
  baselineVersion: string;
  oracleVersion: string;
  config: VerificationConfig;
}

/**
 * Verification configuration
 */
export interface VerificationConfig {
  strictness: 'ultra' | 'strict' | 'moderate' | 'permissive';
  stopOnFirstFailure: boolean;
  requireEvidence: boolean;
  requireFalsification: boolean;
  requireBaseline: boolean;
  requireOracle: boolean;
  timeout: number;
  parallelExecution: boolean;
  maxConcurrent: number;
}

// ============================================================================
// Anti-Fabric Types
// ============================================================================

/**
 * Contradiction detection result
 */
export interface ContradictionResult {
  contradicted: boolean;
  contradictions: Array<{
    statement1: string;
    statement2: string;
    location1: string;
    location2: string;
    severity: VerificationSeverity;
    explanation: string;
  }>;
}

/**
 * Semantic inconsistency result
 */
export interface SemanticInconsistencyResult {
  inconsistent: boolean;
  inconsistencies: Array<{
    element: string;
    expectedSemantics: string;
    actualSemantics: string;
    divergence: string;
    severity: VerificationSeverity;
  }>;
}

/**
 * Pattern break detection result
 */
export interface PatternBreakResult {
  patternBroken: boolean;
  breaks: Array<{
    pattern: string;
    violation: string;
    location: string;
    justification: string;
  }>;
}

/**
 * Assumption validation result
 */
export interface AssumptionValidationResult {
  assumptionsValidated: boolean;
  violations: Array<{
    assumption: string;
    invalidationMethod: string;
    counterexample: any;
    severity: VerificationSeverity;
  }>;
}

/**
 * Adversarial generation result
 */
export interface AdversarialResult {
  adversarialInputs: Array<{
    input: any;
    category: string;
    purpose: string;
  }>;
  systemFailures: Array<{
    input: any;
    failure: string;
    severity: VerificationSeverity;
  }>;
}

// ============================================================================
// Falsification Engine Types
// ============================================================================

/**
 * Falsification test result
 */
export interface FalsificationResult {
  falsified: boolean;
  claimsTested: number;
  claimsFalsified: number;
  falsifications: Array<{
    claim: string;
    counterexample: any;
    proof: string;
    severity: VerificationSeverity;
  }>;
}

/**
 * Boundary test result
 */
export interface BoundaryTestResult {
  boundaryViolated: boolean;
  violations: Array<{
    boundary: string;
    input: any;
    expected: any;
    actual: any;
    severity: VerificationSeverity;
  }>;
}

/**
 * Semantic contradiction test result
 */
export interface SemanticContradictionTestResult {
  contradictionFound: boolean;
  contradictions: Array<{
    context: string;
    contradiction: string;
    evidence: Evidence[];
  }>;
}

/**
 * Behavior divergence test result
 */
export interface BehaviorDivergenceResult {
  diverged: boolean;
  divergences: Array<{
    scenario: string;
    expectedBehavior: string;
    actualBehavior: string;
    divergence: string;
    severity: VerificationSeverity;
  }>;
}

/**
 * Reality vs report comparison result
 */
export interface RealityVsReportResult {
  discrepancyFound: boolean;
  discrepancies: Array<{
    claim: string;
    reportValue: any;
    realityValue: any;
    difference: string;
    severity: VerificationSeverity;
  }>;
}

// ============================================================================
// Execution Harness Types
// ============================================================================

/**
 * Real execution result
 */
export interface RealExecutionResult {
  executed: boolean;
  success: boolean;
  output: any;
  error?: any;
  performance: {
    executionTime: number;
    memoryUsed: number;
    cpuTime: number;
  };
}

/**
 * Baseline comparison result
 */
export interface BaselineComparisonResult {
  baselineMatched: boolean;
  differences: Array<{
    metric: string;
    baseline: any;
    current: any;
    delta: any;
    severity: VerificationSeverity;
  }>;
}

/**
 * Oracle validation result
 */
export interface OracleValidationResult {
  oracleValidated: boolean;
  violations: Array<{
    oracle: string;
    expected: any;
    actual: any;
    violation: string;
    severity: VerificationSeverity;
  }>;
}

/**
 * Stress test result
 */
export interface StressTestResult {
  stressPassed: boolean;
  load: number;
  failures: Array<{
    load: number;
    failure: string;
    severity: VerificationSeverity;
  }>;
  performance: {
    avgResponseTime: number;
    maxResponseTime: number;
    errorRate: number;
  };
}

/**
 * Fuzzing test result
 */
export interface FuzzingResult {
  fuzzed: boolean;
  inputs: number;
  crashes: number;
  hangs: number;
  anomalies: number;
  findings: Array<{
    input: any;
    crash?: string;
    hang?: string;
    anomaly?: string;
    severity: VerificationSeverity;
  }>;
}

/**
 * Regression diff result
 */
export interface RegressionDiffResult {
  regressionDetected: boolean;
  regressions: Array<{
    component: string;
    change: string;
    impact: string;
    severity: VerificationSeverity;
  }>;
}

// ============================================================================
// Integrated Verification Result
// ============================================================================

/**
 * Complete verification report
 */
export interface VerificationReport {
  executionId: string;
  timestamp: Date;
  context: VerificationContext;
  
  // Anti-Fabric Results
  contradictions: ContradictionResult;
  semanticInconsistencies: SemanticInconsistencyResult;
  patternBreaks: PatternBreakResult;
  assumptionViolations: AssumptionValidationResult;
  adversarialFailures: AdversarialResult;
  
  // Falsification Engine Results
  falsifications: FalsificationResult;
  boundaryViolations: BoundaryTestResult;
  semanticContradictions: SemanticContradictionTestResult;
  behaviorDivergences: BehaviorDivergenceResult;
  realityVsReport: RealityVsReportResult;
  
  // Execution Harness Results
  executions: RealExecutionResult[];
  baselineComparisons: BaselineComparisonResult[];
  oracleValidations: OracleValidationResult[];
  stressTests: StressTestResult[];
  fuzzingResults: FuzzingResult[];
  regressionDiffs: RegressionDiffResult[];
  
  // Summary
  summary: {
    totalFindings: number;
    criticalFindings: number;
    highFindings: number;
    mediumFindings: number;
    lowFindings: number;
    infoFindings: number;
    
    falsificationRate: number;  // % of claims falsified
    contradictionRate: number;  // % of contradictions found
    divergenceRate: number;     // % of behavior divergences
    realityMismatchRate: number; // % of report vs reality mismatches
    
    overallStatus: 'FAILED' | 'PASSED' | 'CONDITIONAL';
  };
  
  // Detailed Findings
  findings: VerificationFinding[];
  
  // Governance Events
  governanceEvents: any[];
}

// ============================================================================
// Verification Interfaces
// ============================================================================

/**
 * Anti-Fabric interface
 */
export interface IAntiFabric {
  detectContradictions(component: string): Promise<ContradictionResult>;
  detectSemanticInconsistencies(component: string): Promise<SemanticInconsistencyResult>;
  detectPatternBreaks(component: string): Promise<PatternBreakResult>;
  validateAssumptions(component: string): Promise<AssumptionValidationResult>;
  generateAdversarialInputs(component: string): Promise<AdversarialResult>;
}

/**
 * Falsification Engine interface
 */
export interface IFalsificationEngine {
  falsifyClaims(component: string, claims: string[]): Promise<FalsificationResult>;
  testBoundaries(component: string): Promise<BoundaryTestResult>;
  testSemanticContradictions(component: string): Promise<SemanticContradictionTestResult>;
  testBehaviorDivergence(component: string): Promise<BehaviorDivergenceResult>;
  compareRealityVsReport(component: string): Promise<RealityVsReportResult>;
}

/**
 * Execution Harness interface
 */
export interface IExecutionHarness {
  executeReal(component: string, scenario: string): Promise<RealExecutionResult>;
  compareBaseline(component: string, metrics: any): Promise<BaselineComparisonResult>;
  validateOracle(component: string, oracle: string): Promise<OracleValidationResult>;
  stressTest(component: string, maxLoad: number): Promise<StressTestResult>;
  fuzzTest(component: string, iterations: number): Promise<FuzzingResult>;
  detectRegression(component: string, previousVersion: string): Promise<RegressionDiffResult>;
}

/**
 * Ultra-Strict Verification Core interface
 */
export interface IUltraStrictVerificationCore {
  antiFabric: IAntiFabric;
  falsificationEngine: IFalsificationEngine;
  executionHarness: IExecutionHarness;
  
  executeFullVerification(component: string, context: VerificationContext): Promise<VerificationReport>;
  executeAntiFabricVerification(component: string): Promise<VerificationReport>;
  executeFalsificationVerification(component: string): Promise<VerificationReport>;
  executeExecutionVerification(component: string): Promise<VerificationReport>;
}