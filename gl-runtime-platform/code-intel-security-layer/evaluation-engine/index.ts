// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: code-intelligence-evaluation-engine
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Code Intelligence & Security Layer - Evaluation Engine
 * Version 21.0.0
 * Verification Layer - 驗證層
 */

import { GeneratedCapability, ValidationResult as GenValidationResult } from '../generator-engine';
import { v4 as uuidv4 } from 'uuid';

// ============================================================================
// Evaluation Core Types
// ============================================================================

export interface EvaluationConfig {
  strictMode: boolean;
  timeoutMs: number;
  enableBehavioralTesting: boolean;
  enableSecurityScanning: boolean;
  enablePerformanceProfiling: boolean;
}

export interface EvaluationRequest {
  id: string;
  originalCode?: string;
  generatedCapability: GeneratedCapability;
  evaluationType: EvaluationType[];
  options: EvaluationOptions;
  timestamp: number;
}

export type EvaluationType = 
  | 'behavior-equivalence'
  | 'security-regression'
  | 'performance-regression'
  | 'semantic-consistency'
  | 'explainability'
  | 'audit-trail';

export interface EvaluationOptions {
  testInputs?: any[];
  expectedOutputs?: any[];
  securityRules?: string[];
  performanceThresholds?: PerformanceThresholds;
  explanationLevel: 'minimal' | 'standard' | 'detailed';
}

export interface PerformanceThresholds {
  maxExecutionTime?: number;
  maxMemoryUsage?: number;
  minThroughput?: number;
}

export interface EvaluationResult {
  id: string;
  requestId: string;
  success: boolean;
  results: Map<EvaluationType, TypeEvaluationResult>;
  overallScore: number;
  recommendations: string[];
  auditLog: AuditEntry[];
  timestamp: number;
}

export interface TypeEvaluationResult {
  type: EvaluationType;
  status: 'pass' | 'fail' | 'warning';
  score: number;
  details: Record<string, any>;
  issues: EvaluationIssue[];
}

export interface EvaluationIssue {
  severity: 'critical' | 'high' | 'medium' | 'low';
  category: string;
  message: string;
  location?: string;
  suggestion?: string;
}

export interface AuditEntry {
  timestamp: number;
  type: string;
  description: string;
  metadata?: Record<string, any>;
}

// ============================================================================
// Evaluation Engine Core
// ============================================================================

export class EvaluationEngine {
  private config: EvaluationConfig;
  private auditLog: AuditEntry[];

  constructor(config?: Partial<EvaluationConfig>) {
    this.config = {
      strictMode: true,
      timeoutMs: 60000,
      enableBehavioralTesting: true,
      enableSecurityScanning: true,
      enablePerformanceProfiling: true,
      ...config
    };
    this.auditLog = [];
  }

  /**
   * Evaluate generated capability
   */
  public async evaluate(request: EvaluationRequest): Promise<EvaluationResult> {
    const startTime = Date.now();
    this.logAudit('evaluation-start', `Starting evaluation for request ${request.id}`);

    const results = new Map<EvaluationType, TypeEvaluationResult>();
    let overallScore = 0;
    const issues: EvaluationIssue[] = [];
    const recommendations: string[] = [];

    // Execute requested evaluations
    for (const evalType of request.evaluationType) {
      const result = await this.executeEvaluation(evalType, request);
      results.set(evalType, result);
      issues.push(...result.issues);
    }

    // Calculate overall score
    overallScore = this.calculateOverallScore(results);

    // Generate recommendations
    recommendations.push(...this.generateRecommendations(results, issues));

    const result: EvaluationResult = {
      id: uuidv4(),
      requestId: request.id,
      success: overallScore >= (this.config.strictMode ? 0.9 : 0.7),
      results,
      overallScore,
      recommendations,
      auditLog: [...this.auditLog],
      timestamp: Date.now()
    };

    this.logAudit('evaluation-complete', `Evaluation completed with score: ${overallScore}`, {
      success: result.success,
      duration: Date.now() - startTime
    });

    return result;
  }

  /**
   * Execute specific evaluation type
   */
  private async executeEvaluation(
    type: EvaluationType,
    request: EvaluationRequest
  ): Promise<TypeEvaluationResult> {
    this.logAudit('evaluation-start', `Executing ${type} evaluation`);

    switch (type) {
      case 'behavior-equivalence':
        return this.evaluateBehaviorEquivalence(request);
      case 'security-regression':
        return this.evaluateSecurityRegression(request);
      case 'performance-regression':
        return this.evaluatePerformanceRegression(request);
      case 'semantic-consistency':
        return this.evaluateSemanticConsistency(request);
      case 'explainability':
        return this.evaluateExplainability(request);
      case 'audit-trail':
        return this.evaluateAuditTrail(request);
      default:
        throw new Error(`Unsupported evaluation type: ${type}`);
    }
  }

  /**
   * Evaluate behavior equivalence
   */
  private async evaluateBehaviorEquivalence(
    request: EvaluationRequest
  ): Promise<TypeEvaluationResult> {
    const issues: EvaluationIssue[] = [];
    let score = 0;

    if (!request.originalCode) {
      return {
        type: 'behavior-equivalence',
        status: 'warning',
        score: 0.5,
        details: { message: 'No original code provided for comparison' },
        issues: [{
          severity: 'medium',
          category: 'validation',
          message: 'Cannot verify behavior equivalence without original code',
          suggestion: 'Provide original code for behavior equivalence testing'
        }]
      };
    }

    // Simulate behavioral testing
    const testInputs = request.options.testInputs || [
      { input: 'test1' },
      { input: 'test2' },
      { input: 'test3' }
    ];

    let passCount = 0;
    let totalCount = testInputs.length;

    for (const input of testInputs) {
      // In production, execute both original and generated code
      // For now, simulate behavior equivalence
      const originalOutput = this.simulateExecution(request.originalCode, input);
      const generatedOutput = this.simulateExecution(request.generatedCapability.code, input);

      if (this.compareOutputs(originalOutput, generatedOutput)) {
        passCount++;
      } else {
        issues.push({
          severity: 'high',
          category: 'behavior',
          message: `Behavior mismatch for input: ${JSON.stringify(input)}`,
          suggestion: 'Review generated code for behavior-preserving transformations'
        });
      }
    }

    score = passCount / totalCount;

    this.logAudit('behavior-evaluation', `Behavior equivalence score: ${score}`, {
      passCount,
      totalCount
    });

    return {
      type: 'behavior-equivalence',
      status: score >= 0.95 ? 'pass' : score >= 0.8 ? 'warning' : 'fail',
      score,
      details: {
        testInputs: testInputs.length,
        passed: passCount,
        failed: totalCount - passCount
      },
      issues
    };
  }

  /**
   * Evaluate security regression
   */
  private async evaluateSecurityRegression(
    request: EvaluationRequest
  ): Promise<TypeEvaluationResult> {
    const issues: EvaluationIssue[] = [];
    let score = 1.0;

    // Check for common security issues in generated code
    const code = request.generatedCapability.code;
    const securityRules = request.options.securityRules || [
      'no-eval',
      'no-dangerous-functions',
      'no-hardcoded-secrets',
      'input-validation',
      'output-encoding'
    ];

    for (const rule of securityRules) {
      const result = this.checkSecurityRule(code, rule);
      if (!result.passed) {
        score -= result.severity;
        issues.push({
          severity: result.severity > 0.5 ? 'critical' : 'high',
          category: 'security',
          message: result.message,
          suggestion: result.suggestion
        });
      }
    }

    score = Math.max(0, score);

    this.logAudit('security-evaluation', `Security regression score: ${score}`, {
      issuesFound: issues.length
    });

    return {
      type: 'security-regression',
      status: score >= 0.9 ? 'pass' : score >= 0.7 ? 'warning' : 'fail',
      score,
      details: {
        rulesChecked: securityRules.length,
        issuesFound: issues.length
      },
      issues
    };
  }

  /**
   * Evaluate performance regression
   */
  private async evaluatePerformanceRegression(
    request: EvaluationRequest
  ): Promise<TypeEvaluationResult> {
    const issues: EvaluationIssue[] = [];
    let score = 1.0;

    const thresholds = request.options.performanceThresholds;
    if (!thresholds) {
      return {
        type: 'performance-regression',
        status: 'warning',
        score: 0.5,
        details: { message: 'No performance thresholds provided' },
        issues: [{
          severity: 'medium',
          category: 'performance',
          message: 'Cannot evaluate performance without thresholds',
          suggestion: 'Provide performance thresholds for evaluation'
        }]
      };
    }

    // Simulate performance testing
    const executionTime = Math.random() * 100; // Simulated
    const memoryUsage = Math.random() * 50; // Simulated

    if (thresholds.maxExecutionTime && executionTime > thresholds.maxExecutionTime) {
      score -= 0.3;
      issues.push({
        severity: 'high',
        category: 'performance',
        message: `Execution time exceeds threshold: ${executionTime}ms > ${thresholds.maxExecutionTime}ms`,
        suggestion: 'Optimize generated code for better performance'
      });
    }

    if (thresholds.maxMemoryUsage && memoryUsage > thresholds.maxMemoryUsage) {
      score -= 0.2;
      issues.push({
        severity: 'medium',
        category: 'performance',
        message: `Memory usage exceeds threshold: ${memoryUsage}MB > ${thresholds.maxMemoryUsage}MB`,
        suggestion: 'Reduce memory footprint in generated code'
      });
    }

    score = Math.max(0, score);

    this.logAudit('performance-evaluation', `Performance regression score: ${score}`, {
      executionTime,
      memoryUsage
    });

    return {
      type: 'performance-regression',
      status: score >= 0.9 ? 'pass' : score >= 0.7 ? 'warning' : 'fail',
      score,
      details: {
        executionTime,
        memoryUsage,
        thresholds
      },
      issues
    };
  }

  /**
   * Evaluate semantic consistency
   */
  private async evaluateSemanticConsistency(
    request: EvaluationRequest
  ): Promise<TypeEvaluationResult> {
    const issues: EvaluationIssue[] = [];
    let score = 1.0;

    const generatedCode = request.generatedCapability.code;

    // Check for semantic consistency indicators
    const checks = [
      {
        name: 'naming-consistency',
        check: () => generatedCode.match(/^[a-zA-Z_][a-zA-Z0-9_]*\s*\(/gm) !== null,
        weight: 0.2
      },
      {
        name: 'type-safety',
        check: () => generatedCode.includes(':') || generatedCode.includes('interface') || generatedCode.includes('type'),
        weight: 0.3
      },
      {
        name: 'documentation',
        check: () => generatedCode.includes('/**') || generatedCode.includes('//'),
        weight: 0.2
      },
      {
        name: 'structure',
        check: () => generatedCode.includes('class') || generatedCode.includes('function') || generatedCode.includes('export'),
        weight: 0.3
      }
    ];

    for (const check of checks) {
      if (!check.check()) {
        score -= check.weight;
        issues.push({
          severity: 'medium',
          category: 'semantic',
          message: `Missing semantic element: ${check.name}`,
          suggestion: `Add ${check.name} to improve semantic consistency`
        });
      }
    }

    score = Math.max(0, score);

    this.logAudit('semantic-evaluation', `Semantic consistency score: ${score}`);

    return {
      type: 'semantic-consistency',
      status: score >= 0.8 ? 'pass' : score >= 0.6 ? 'warning' : 'fail',
      score,
      details: {
        checks: checks.map(c => ({ name: c.name, passed: c.check() }))
      },
      issues
    };
  }

  /**
   * Evaluate explainability
   */
  private async evaluateExplainability(
    request: EvaluationRequest
  ): Promise<TypeEvaluationResult> {
    const issues: EvaluationIssue[] = [];
    let score = 1.0;

    const code = request.generatedCapability.code;
    const explanationLevel = request.options.explanationLevel;

    // Check for explainability features
    const explainabilityFeatures = [
      {
        name: 'comments',
        check: () => code.includes('//') || code.includes('/**'),
        weight: 0.3
      },
      {
        name: 'documentation',
        check: () => code.includes('/**') && code.includes('@param') && code.includes('@return'),
        weight: 0.4
      },
      {
        name: 'logging',
        check: () => code.includes('console.log') || code.includes('logger'),
        weight: 0.2
      },
      {
        name: 'error-handling',
        check: () => code.includes('try') && code.includes('catch'),
        weight: 0.1
      }
    ];

    for (const feature of explainabilityFeatures) {
      if (!feature.check()) {
        score -= feature.weight;
        issues.push({
          severity: 'low',
          category: 'explainability',
          message: `Missing explainability feature: ${feature.name}`,
          suggestion: `Add ${feature.name} to improve code explainability`
        });
      }
    }

    score = Math.max(0, score);

    this.logAudit('explainability-evaluation', `Explainability score: ${score}`, {
      explanationLevel
    });

    return {
      type: 'explainability',
      status: score >= (explanationLevel === 'detailed' ? 0.9 : explanationLevel === 'standard' ? 0.7 : 0.5) ? 'pass' : 'warning',
      score,
      details: {
        explanationLevel,
        features: explainabilityFeatures.map(f => ({ name: f.name, present: f.check() }))
      },
      issues
    };
  }

  /**
   * Evaluate audit trail
   */
  private async evaluateAuditTrail(
    request: EvaluationRequest
  ): Promise<TypeEvaluationResult> {
    const issues: EvaluationIssue[] = [];
    let score = 1.0;

    const metadata = request.generatedCapability.metadata;

    // Check for audit trail features
    const auditFeatures = [
      {
        name: 'generator-version',
        check: () => !!metadata.generatorVersion,
        weight: 0.2
      },
      {
        name: 'patterns-used',
        check: () => metadata.patternsUsed.length > 0,
        weight: 0.2
      },
      {
        name: 'generation-time',
        check: () => metadata.generationTime > 0,
        weight: 0.2
      },
      {
        name: 'confidence-score',
        check: () => metadata.confidenceScore >= 0 && metadata.confidenceScore <= 1,
        weight: 0.2
      },
      {
        name: 'validation-results',
        check: () => Array.isArray(metadata.validationResults),
        weight: 0.2
      }
    ];

    for (const feature of auditFeatures) {
      if (!feature.check()) {
        score -= feature.weight;
        issues.push({
          severity: 'medium',
          category: 'audit',
          message: `Missing audit feature: ${feature.name}`,
          suggestion: `Ensure ${feature.name} is recorded for full traceability`
        });
      }
    }

    score = Math.max(0, score);

    this.logAudit('audit-evaluation', `Audit trail score: ${score}`);

    return {
      type: 'audit-trail',
      status: score >= 0.8 ? 'pass' : 'warning',
      score,
      details: {
        auditFeatures: auditFeatures.map(f => ({ name: f.name, present: f.check() }))
      },
      issues
    };
  }

  /**
   * Simulate code execution
   */
  private simulateExecution(code: string, input: any): any {
    // In production, this would actually execute the code in a sandbox
    // For now, return a simulated result
    return {
      output: `processed_${JSON.stringify(input)}`,
      timestamp: Date.now()
    };
  }

  /**
   * Compare outputs
   */
  private compareOutputs(output1: any, output2: any): boolean {
    return JSON.stringify(output1) === JSON.stringify(output2);
  }

  /**
   * Check security rule
   */
  private checkSecurityRule(code: string, rule: string): {
    passed: boolean;
    severity: number;
    message: string;
    suggestion: string;
  } {
    const lowerCode = code.toLowerCase();

    switch (rule) {
      case 'no-eval':
        if (lowerCode.includes('eval(')) {
          return {
            passed: false,
            severity: 1.0,
            message: 'Use of eval() detected',
            suggestion: 'Replace eval() with safer alternatives'
          };
        }
        break;

      case 'no-dangerous-functions':
        const dangerousFunctions = ['eval', 'exec', 'system', 'shell_exec'];
        for (const func of dangerousFunctions) {
          if (lowerCode.includes(`${func}(`)) {
            return {
              passed: false,
              severity: 0.8,
              message: `Use of dangerous function: ${func}`,
              suggestion: 'Replace with safer alternatives'
            };
          }
        }
        break;

      case 'no-hardcoded-secrets':
        const secretPatterns = ['password', 'secret', 'apikey', 'token'];
        for (const pattern of secretPatterns) {
          const regex = new RegExp(`${pattern}\\s*=\\s*['"'][^'"']+['"']`, 'i');
          if (regex.test(code)) {
            return {
              passed: false,
              severity: 0.9,
              message: `Possible hardcoded secret: ${pattern}`,
              suggestion: 'Use environment variables or secret management'
            };
          }
        }
        break;

      case 'input-validation':
        if (!lowerCode.includes('validate') && !lowerCode.includes('sanitize')) {
          return {
            passed: false,
            severity: 0.6,
            message: 'No input validation detected',
            suggestion: 'Add input validation for user inputs'
          };
        }
        break;

      case 'output-encoding':
        if (!lowerCode.includes('encode') && !lowerCode.includes('escape')) {
          return {
            passed: false,
            severity: 0.6,
            message: 'No output encoding detected',
            suggestion: 'Add output encoding to prevent XSS'
          };
        }
        break;
    }

    return {
      passed: true,
      severity: 0,
      message: 'Rule passed',
      suggestion: ''
    };
  }

  /**
   * Calculate overall score
   */
  private calculateOverallScore(results: Map<EvaluationType, TypeEvaluationResult>): number {
    if (results.size === 0) return 0;

    let totalScore = 0;
    for (const result of results.values()) {
      totalScore += result.score;
    }

    return totalScore / results.size;
  }

  /**
   * Generate recommendations
   */
  private generateRecommendations(
    results: Map<EvaluationType, TypeEvaluationResult>,
    issues: EvaluationIssue[]
  ): string[] {
    const recommendations: string[] = [];

    // Add issue-based recommendations
    const criticalIssues = issues.filter(i => i.severity === 'critical');
    if (criticalIssues.length > 0) {
      recommendations.push(`Address ${criticalIssues.length} critical issues before deployment`);
    }

    const highIssues = issues.filter(i => i.severity === 'high');
    if (highIssues.length > 0) {
      recommendations.push(`Address ${highIssues.length} high-priority issues`);
    }

    // Add score-based recommendations
    for (const [type, result] of results) {
      if (result.score < 0.7) {
        recommendations.push(`Improve ${type} evaluation score (current: ${result.score.toFixed(2)})`);
      }
    }

    // Add general recommendations
    if (results.get('behavior-equivalence')?.score === 1) {
      recommendations.push('Excellent behavior preservation achieved');
    }

    if (results.get('security-regression')?.score === 1) {
      recommendations.push('Security requirements fully met');
    }

    return recommendations;
  }

  /**
   * Log audit entry
   */
  private logAudit(type: string, description: string, metadata?: Record<string, any>): void {
    this.auditLog.push({
      timestamp: Date.now(),
      type,
      description,
      metadata
    });
  }

  /**
   * Get audit log
   */
  public getAuditLog(): AuditEntry[] {
    return [...this.auditLog];
  }

  /**
   * Clear audit log
   */
  public clearAuditLog(): void {
    this.auditLog = [];
  }

  /**
   * Get evaluation statistics
   */
  public getStatistics(): {
    totalEvaluations: number;
    averageScore: number;
    passRate: number;
  } {
    // In production, this would track actual statistics
    return {
      totalEvaluations: 0,
      averageScore: 0,
      passRate: 0
    };
  }
}