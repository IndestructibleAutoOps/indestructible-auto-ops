// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: task-completion-checker
// @GL-charter-version: 2.0.0

/**
 * Task Completion Checker
 * Validates that tasks are truly complete, not just executed
 */

import { ExecutionResult, ExecutionContext } from '../strategy-library/strategies';

export interface CompletionConfig {
  strictMode: boolean;
  requireValidation: boolean;
  requireGovernance: boolean;
  requireArtifacts: boolean;
  requireTraceability: boolean;
  requireProvability: boolean;
}

export interface CompletionCheck {
  id: string;
  name: string;
  passed: boolean;
  severity: 'critical' | 'high' | 'medium' | 'low';
  message: string;
  details?: any;
}

export interface CompletionResult {
  task: string;
  completed: boolean;
  score: number;
  checks: CompletionCheck[];
  criticalFailures: CompletionCheck[];
  warnings: CompletionCheck[];
  summary: string;
  recommendations: string[];
}

export class CompletionChecker {
  private defaultConfig: CompletionConfig = {
    strictMode: true,
    requireValidation: true,
    requireGovernance: true,
    requireArtifacts: true,
    requireTraceability: true,
    requireProvability: true
  };

  async checkCompletion(
    result: ExecutionResult,
    context: ExecutionContext,
    config?: Partial<CompletionConfig>
  ): Promise<CompletionResult> {
    const mergedConfig = { ...this.defaultConfig, ...config };
    const checks: CompletionCheck[] = [];

    // Check 1: Execution Success
    checks.push(await this.checkExecutionSuccess(result, mergedConfig));

    // Check 2: Output Validity
    checks.push(await this.checkOutputValidity(result, mergedConfig));

    // Check 3: Validation Status
    if (mergedConfig.requireValidation) {
      checks.push(await this.checkValidationStatus(result, mergedConfig));
    }

    // Check 4: Governance Compliance
    if (mergedConfig.requireGovernance) {
      checks.push(await this.checkGovernanceCompliance(result, context, mergedConfig));
    }

    // Check 5: Artifact Generation
    if (mergedConfig.requireArtifacts) {
      checks.push(await this.checkArtifactGeneration(result, context, mergedConfig));
    }

    // Check 6: Traceability
    if (mergedConfig.requireTraceability) {
      checks.push(await this.checkTraceability(result, context, mergedConfig));
    }

    // Check 7: Provability
    if (mergedConfig.requireProvability) {
      checks.push(await this.checkProvability(result, context, mergedConfig));
    }

    // Check 8: Side Effects
    checks.push(await this.checkSideEffects(result, context, mergedConfig));

    // Calculate completion score
    const score = this.calculateCompletionScore(checks);

    // Determine if completed
    const criticalFailures = checks.filter(c => !c.passed && c.severity === 'critical');
    const completed = criticalFailures.length === 0 && (!mergedConfig.strictMode || score >= 0.8);

    // Generate summary
    const summary = this.generateSummary(checks, completed, score);

    // Generate recommendations
    const recommendations = this.generateRecommendations(checks);

    return {
      task: context.task,
      completed,
      score,
      checks,
      criticalFailures,
      warnings: checks.filter(c => !c.passed && c.severity === 'medium'),
      summary,
      recommendations
    };
  }

  private async checkExecutionSuccess(
    result: ExecutionResult,
    config: CompletionConfig
  ): Promise<CompletionCheck> {
    return {
      id: 'execution-success',
      name: 'Execution Success',
      passed: result.success,
      severity: 'critical',
      message: result.success 
        ? 'Task executed successfully' 
        : 'Task execution failed',
      details: {
        strategy: result.strategy,
        duration: result.duration
      }
    };
  }

  private async checkOutputValidity(
    result: ExecutionResult,
    config: CompletionConfig
  ): Promise<CompletionCheck> {
    const hasOutput = result.output !== null && result.output !== undefined;
    const isValid = hasOutput && typeof result.output === 'object';

    return {
      id: 'output-validity',
      name: 'Output Validity',
      passed: isValid,
      severity: 'critical',
      message: isValid 
        ? 'Valid output generated' 
        : hasOutput ? 'Output is not a valid object' : 'No output generated',
      details: {
        hasOutput,
        outputType: typeof result.output
      }
    };
  }

  private async checkValidationStatus(
    result: ExecutionResult,
    config: CompletionConfig
  ): Promise<CompletionCheck> {
    const validated = result.metrics?.validationPassed || false;

    return {
      id: 'validation-status',
      name: 'Validation Status',
      passed: validated,
      severity: 'high',
      message: validated 
        ? 'Result validated successfully' 
        : 'Result validation failed or not performed',
      details: { validated }
    };
  }

  private async checkGovernanceCompliance(
    result: ExecutionResult,
    context: ExecutionContext,
    config: CompletionConfig
  ): Promise<CompletionCheck> {
    // Check if output has governance markers
    const hasGovernanceMarkers = this.hasGovernanceMarkers(result.output);
    
    // Check if context has governance metadata
    const hasGovernanceMetadata = this.hasGovernanceMetadata(context);

    return {
      id: 'governance-compliance',
      name: 'Governance Compliance',
      passed: hasGovernanceMarkers && hasGovernanceMetadata,
      severity: 'high',
      message: (hasGovernanceMarkers && hasGovernanceMetadata)
        ? 'Governance compliance verified'
        : 'Missing governance markers or metadata',
      details: {
        hasGovernanceMarkers,
        hasGovernanceMetadata
      }
    };
  }

  private async checkArtifactGeneration(
    result: ExecutionResult,
    context: ExecutionContext,
    config: CompletionConfig
  ): Promise<CompletionCheck> {
    // Check if artifacts were generated
    const hasArtifacts = context.metadata.artifacts !== undefined;

    return {
      id: 'artifact-generation',
      name: 'Artifact Generation',
      passed: hasArtifacts,
      severity: 'medium',
      message: hasArtifacts 
        ? 'Artifacts generated successfully' 
        : 'No artifacts generated',
      details: { hasArtifacts }
    };
  }

  private async checkTraceability(
    result: ExecutionResult,
    context: ExecutionContext,
    config: CompletionConfig
  ): Promise<CompletionCheck> {
    // Check if execution is traceable
    const hasExecutionId = context.metadata.executionId !== undefined;
    const hasTimestamp = context.metadata.timestamp !== undefined;
    const hasHistory = context.history.length > 0;

    return {
      id: 'traceability',
      name: 'Traceability',
      passed: hasExecutionId && hasTimestamp && hasHistory,
      severity: 'high',
      message: (hasExecutionId && hasTimestamp && hasHistory)
        ? 'Execution is fully traceable'
        : 'Missing traceability information',
      details: {
        hasExecutionId,
        hasTimestamp,
        hasHistory,
        historyLength: context.history.length
      }
    };
  }

  private async checkProvability(
    result: ExecutionResult,
    context: ExecutionContext,
    config: CompletionConfig
  ): Promise<CompletionCheck> {
    // Check if execution is provable
    const hasSignatures = context.metadata.signatures !== undefined;
    const hasChecksums = context.metadata.checksums !== undefined;
    const hasAuditTrail = context.metadata.auditTrail !== undefined;

    return {
      id: 'provability',
      name: 'Provability',
      passed: hasSignatures && hasChecksums && hasAuditTrail,
      severity: 'high',
      message: (hasSignatures && hasChecksums && hasAuditTrail)
        ? 'Execution is provable'
        : 'Missing provability information',
      details: {
        hasSignatures,
        hasChecksums,
        hasAuditTrail
      }
    };
  }

  private async checkSideEffects(
    result: ExecutionResult,
    context: ExecutionContext,
    config: CompletionConfig
  ): Promise<CompletionCheck> {
    // Check for unintended side effects
    const hasSideEffects = result.metrics?.operationsPerformed > 10;
    const sideEffectsAcceptable = !hasSideEffects || context.metadata.allowSideEffects === true;

    return {
      id: 'side-effects',
      name: 'Side Effects',
      passed: sideEffectsAcceptable,
      severity: 'medium',
      message: sideEffectsAcceptable
        ? 'No unacceptable side effects detected'
        : 'Potential side effects detected',
      details: {
        hasSideEffects,
        operationsPerformed: result.metrics?.operationsPerformed
      }
    };
  }

  private hasGovernanceMarkers(output: any): boolean {
    if (!output || typeof output !== 'object') return false;
    
    // Check for common governance markers
    const markers = ['governed', 'governance', 'compliance', 'audit'];
    const outputStr = JSON.stringify(output).toLowerCase();
    
    return markers.some(marker => outputStr.includes(marker));
  }

  private hasGovernanceMetadata(context: ExecutionContext): boolean {
    const metadata = context.metadata;
    return metadata.governance !== undefined || 
           metadata.auditTrail !== undefined ||
           metadata.governanceLayer !== undefined;
  }

  private calculateCompletionScore(checks: CompletionCheck[]): number {
    if (checks.length === 0) return 0;

    let totalScore = 0;
    let maxScore = 0;

    for (const check of checks) {
      let weight = 1;
      
      switch (check.severity) {
        case 'critical':
          weight = 3;
          break;
        case 'high':
          weight = 2;
          break;
        case 'medium':
          weight = 1;
          break;
        case 'low':
          weight = 0.5;
          break;
      }

      maxScore += weight;
      if (check.passed) {
        totalScore += weight;
      }
    }

    return maxScore > 0 ? totalScore / maxScore : 0;
  }

  private generateSummary(checks: CompletionCheck[], completed: boolean, score: number): string {
    const passed = checks.filter(c => c.passed).length;
    const total = checks.length;

    if (completed) {
      return `Task completed successfully. Passed ${passed}/${total} checks (${(score * 100).toFixed(1)}% score)`;
    } else {
      const critical = checks.filter(c => !c.passed && c.severity === 'critical').length;
      return `Task not completed. ${critical} critical failures. Passed ${passed}/${total} checks (${(score * 100).toFixed(1)}% score)`;
    }
  }

  private generateRecommendations(checks: CompletionCheck[]): string[] {
    const recommendations: string[] = [];
    const failedChecks = checks.filter(c => !c.passed);

    for (const check of failedChecks) {
      switch (check.id) {
        case 'execution-success':
          recommendations.push('Review execution strategy and consider retrying with different approach');
          break;
        case 'output-validity':
          recommendations.push('Ensure output is properly generated and validated');
          break;
        case 'validation-status':
          recommendations.push('Implement proper validation logic for task results');
          break;
        case 'governance-compliance':
          recommendations.push('Add governance markers and metadata to output');
          break;
        case 'artifact-generation':
          recommendations.push('Generate proper artifacts for task execution');
          break;
        case 'traceability':
          recommendations.push('Ensure execution ID, timestamp, and history are tracked');
          break;
        case 'provability':
          recommendations.push('Add signatures, checksums, and audit trail for provability');
          break;
        case 'side-effects':
          recommendations.push('Review and minimize unintended side effects');
          break;
      }
    }

    return recommendations;
  }
}