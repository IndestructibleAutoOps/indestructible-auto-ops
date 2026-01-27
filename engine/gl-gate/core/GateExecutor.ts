/**
 * @fileoverview GL-Gate Executor - Core execution engine for governance gates
 * @module @machine-native-ops/gl-gate/core/GateExecutor
 * @version 1.0.0
 * @since 2026-01-26
 * @author MachineNativeOps
 * @gl-governed true
 * @gl-layer GL-40-GOVERNANCE
 * 
 * GL Unified Charter Activated
 */

import { createHash, randomBytes } from 'crypto';
import {
  GateId,
  GateContext,
  GateResult,
  GateConfig,
  GateEvidence,
  GateStatus,
  GateExecutionSummary,
  GateOrchestration,
  GateEvent
} from '../types';
import { GateRegistry, gateRegistry } from './GateRegistry';
import { BaseGate } from '../gates/BaseGate';

/**
 * Gate Executor Options
 */
export interface GateExecutorOptions {
  /** Enable parallel execution where possible */
  parallelExecution?: boolean;
  
  /** Maximum concurrent gates */
  maxConcurrency?: number;
  
  /** Global timeout in milliseconds */
  globalTimeoutMs?: number;
  
  /** Enable evidence sealing */
  enableSealing?: boolean;
  
  /** Event handler for gate events */
  eventHandler?: (event: GateEvent) => void;
  
  /** Logger instance */
  logger?: Console;
}

/**
 * GL-Gate Executor
 * 治理閘門執行器
 * 
 * Core execution engine responsible for running governance gates,
 * collecting results, and generating evidence chains.
 */
export class GateExecutor {
  private registry: GateRegistry;
  private gates: Map<GateId, BaseGate> = new Map();
  private configs: Map<GateId, GateConfig> = new Map();
  private options: Required<GateExecutorOptions>;
  private eventListeners: ((event: GateEvent) => void)[] = [];

  constructor(options: GateExecutorOptions = {}) {
    this.registry = gateRegistry;
    this.options = {
      parallelExecution: options.parallelExecution ?? false,
      maxConcurrency: options.maxConcurrency ?? 4,
      globalTimeoutMs: options.globalTimeoutMs ?? 300000, // 5 minutes
      enableSealing: options.enableSealing ?? true,
      eventHandler: options.eventHandler ?? (() => {}),
      logger: options.logger ?? console
    };
    
    if (options.eventHandler) {
      this.eventListeners.push(options.eventHandler);
    }
  }

  /**
   * Register a gate implementation
   */
  public registerGate(gateId: GateId, gate: BaseGate): void {
    this.gates.set(gateId, gate);
  }

  /**
   * Configure a gate
   */
  public configureGate(config: GateConfig): void {
    this.configs.set(config.gateId, config);
  }

  /**
   * Execute a single gate
   */
  public async executeGate(gateId: GateId, context: GateContext): Promise<GateResult> {
    const startTime = Date.now();
    const definition = this.registry.getGate(gateId);
    
    if (!definition) {
      return this.createErrorResult(gateId, context, `Gate ${gateId} not found in registry`, startTime);
    }

    const config = this.configs.get(gateId);
    if (config && !config.enabled) {
      return this.createSkippedResult(gateId, context, 'Gate disabled by configuration', startTime);
    }

    const gate = this.gates.get(gateId);
    if (!gate) {
      return this.createErrorResult(gateId, context, `Gate ${gateId} implementation not registered`, startTime);
    }

    // Emit start event
    this.emitEvent({
      eventId: this.generateEventId(),
      eventType: 'gate.started',
      gateId,
      timestamp: new Date(),
      payload: { context, definition: definition.nameEN },
      correlationId: context.executionId
    });

    try {
      // Check dependencies
      if (definition.dependencies && definition.dependencies.length > 0) {
        const depCheck = await this.checkDependencies(definition.dependencies, context);
        if (!depCheck.satisfied) {
          return this.createErrorResult(
            gateId, 
            context, 
            `Dependencies not satisfied: ${depCheck.missing.join(', ')}`,
            startTime
          );
        }
      }

      // Execute gate with timeout
      const timeoutMs = config?.timeoutMs ?? 60000;
      const result = await this.executeWithTimeout(
        () => gate.execute(context, config),
        timeoutMs
      );

      // Generate evidence
      const evidence = await this.generateEvidence(gateId, result, context);
      result.evidence = evidence;

      // Emit completion event
      this.emitEvent({
        eventId: this.generateEventId(),
        eventType: result.status === 'failed' ? 'gate.failed' : 'gate.completed',
        gateId,
        timestamp: new Date(),
        payload: { status: result.status, durationMs: result.durationMs, findingsCount: result.findings.length },
        correlationId: context.executionId
      });

      return result;

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      
      this.emitEvent({
        eventId: this.generateEventId(),
        eventType: 'gate.failed',
        gateId,
        timestamp: new Date(),
        payload: { error: errorMessage },
        correlationId: context.executionId
      });

      return this.createErrorResult(gateId, context, errorMessage, startTime);
    }
  }

  /**
   * Execute multiple gates according to orchestration
   */
  public async executeOrchestration(orchestration: GateOrchestration, context: GateContext): Promise<GateExecutionSummary> {
    const startTime = new Date();
    const results: GateResult[] = [];
    
    // Validate execution order
    const validation = this.registry.validateExecutionOrder(orchestration.gates);
    if (!validation.valid) {
      this.options.logger.warn('Gate execution order validation warnings:', validation.errors);
    }

    if (orchestration.mode === 'sequential') {
      for (const gateId of orchestration.gates) {
        const result = await this.executeGate(gateId, context);
        results.push(result);
        
        if (orchestration.stopOnFailure && result.status === 'failed') {
          break;
        }
      }
    } else if (orchestration.mode === 'parallel') {
      const chunks = this.chunkArray(orchestration.gates, this.options.maxConcurrency);
      
      for (const chunk of chunks) {
        const chunkResults = await Promise.all(
          chunk.map(gateId => this.executeGate(gateId, context))
        );
        results.push(...chunkResults);
        
        if (orchestration.stopOnFailure && chunkResults.some(r => r.status === 'failed')) {
          break;
        }
      }
    } else {
      // DAG mode - execute respecting dependencies
      const executed = new Set<GateId>();
      const remaining = new Set(orchestration.gates);
      
      while (remaining.size > 0) {
        const ready: GateId[] = [];
        
        for (const gateId of remaining) {
          const deps = this.registry.getGateDependencies(gateId);
          if (deps.every(d => executed.has(d) || !orchestration.gates.includes(d))) {
            ready.push(gateId);
          }
        }
        
        if (ready.length === 0 && remaining.size > 0) {
          throw new Error('Circular dependency detected in gate orchestration');
        }
        
        const readyResults = await Promise.all(
          ready.slice(0, this.options.maxConcurrency).map(gateId => this.executeGate(gateId, context))
        );
        
        for (const result of readyResults) {
          results.push(result);
          executed.add(result.gateId);
          remaining.delete(result.gateId);
        }
        
        if (orchestration.stopOnFailure && readyResults.some(r => r.status === 'failed')) {
          break;
        }
      }
    }

    const endTime = new Date();
    const summary = this.createExecutionSummary(orchestration.id, results, startTime, endTime);
    
    return summary;
  }

  /**
   * Create execution context
   */
  public createContext(
    target: string,
    environment: 'development' | 'staging' | 'production' = 'development',
    metadata: Record<string, unknown> = {}
  ): GateContext {
    return {
      executionId: this.generateExecutionId(),
      timestamp: new Date(),
      environment,
      target,
      metadata
    };
  }

  /**
   * Add event listener
   */
  public addEventListener(listener: (event: GateEvent) => void): void {
    this.eventListeners.push(listener);
  }

  /**
   * Remove event listener
   */
  public removeEventListener(listener: (event: GateEvent) => void): void {
    const index = this.eventListeners.indexOf(listener);
    if (index > -1) {
      this.eventListeners.splice(index, 1);
    }
  }

  // Private helper methods

  private async executeWithTimeout<T>(fn: () => Promise<T>, timeoutMs: number): Promise<T> {
    return Promise.race([
      fn(),
      new Promise<T>((_, reject) => 
        setTimeout(() => reject(new Error(`Gate execution timed out after ${timeoutMs}ms`)), timeoutMs)
      )
    ]);
  }

  private async checkDependencies(
    dependencies: GateId[], 
    context: GateContext
  ): Promise<{ satisfied: boolean; missing: GateId[] }> {
    /**
     * Dependency verification:
     * - Gate must be registered.
     * - Gate must have been executed in the current context.
     * - Gate execution must have completed successfully (PASSED).
     *
     * NOTE: We intentionally read execution results from the context using a
     *       type-safe cast to avoid changing shared type definitions. The
     *       expected shape is a map: { [gateId: string]: GateResult }.
     */
    const missingOrUnsatisfied: GateId[] = [];

    // Attempt to read execution results from the current orchestration context.
    // We support multiple possible property names to remain backward compatible.
    const executionResults =
      (context as any).executionResults ??
      (context as any).results ??
      null;

    for (const dep of dependencies) {
      // If the gate implementation itself is not registered, dependency is not satisfied.
      if (!this.gates.has(dep)) {
        missingOrUnsatisfied.push(dep);
        continue;
      }

      // If we have no execution results in this context, or no entry for this
      // dependency, treat it as not satisfied (not executed in this context).
      const depResult: GateResult | undefined =
        executionResults && typeof executionResults === 'object'
          ? executionResults[dep]
          : undefined;

      if (!depResult) {
        missingOrUnsatisfied.push(dep);
        continue;
      }

      // Only consider the dependency satisfied if it explicitly passed.
      if (depResult.status !== 'passed') {
        missingOrUnsatisfied.push(dep);
      }
    }

    const satisfied = missingOrUnsatisfied.length === 0;
    return { satisfied, missing: missingOrUnsatisfied };
  }

  private async generateEvidence(
    gateId: GateId,
    result: GateResult,
    context: GateContext
  ): Promise<GateEvidence[]> {
    const evidence: GateEvidence[] = [];
    
    // Create execution evidence
    const executionEvidence: GateEvidence = {
      id: this.generateEvidenceId(),
      type: 'log',
      content: JSON.stringify({
        gateId,
        status: result.status,
        timestamp: result.timestamp,
        context: {
          executionId: context.executionId,
          environment: context.environment,
          target: context.target
        },
        findings: result.findings.length,
        metrics: result.metrics
      }),
      hash: '',
      timestamp: new Date(),
      sealed: false
    };
    
    executionEvidence.hash = this.hashContent(executionEvidence.content as string);
    
    if (this.options.enableSealing) {
      executionEvidence.sealed = true;
      executionEvidence.signature = this.signEvidence(executionEvidence);
      
      this.emitEvent({
        eventId: this.generateEventId(),
        eventType: 'evidence.sealed',
        gateId,
        timestamp: new Date(),
        payload: { evidenceId: executionEvidence.id, hash: executionEvidence.hash },
        correlationId: context.executionId
      });
    }
    
    evidence.push(executionEvidence);
    
    return evidence;
  }

  private createErrorResult(
    gateId: GateId,
    context: GateContext,
    message: string,
    startTime: number
  ): GateResult {
    return {
      gateId,
      status: 'failed',
      durationMs: Date.now() - startTime,
      message,
      findings: [{
        id: this.generateFindingId(),
        type: 'violation',
        severity: 'critical',
        title: 'Gate Execution Error',
        description: message
      }],
      metrics: [],
      evidence: [],
      timestamp: new Date(),
      context
    };
  }

  private createSkippedResult(
    gateId: GateId,
    context: GateContext,
    message: string,
    startTime: number
  ): GateResult {
    return {
      gateId,
      status: 'skipped',
      durationMs: Date.now() - startTime,
      message,
      findings: [],
      metrics: [],
      evidence: [],
      timestamp: new Date(),
      context
    };
  }

  private createExecutionSummary(
    orchestrationId: string,
    results: GateResult[],
    startTime: Date,
    endTime: Date
  ): GateExecutionSummary {
    const passed = results.filter(r => r.status === 'passed').length;
    const failed = results.filter(r => r.status === 'failed').length;
    const skipped = results.filter(r => r.status === 'skipped').length;
    const warning = results.filter(r => r.status === 'warning').length;
    
    let overallStatus: GateStatus = 'passed';
    if (failed > 0) overallStatus = 'failed';
    else if (warning > 0) overallStatus = 'warning';
    else if (skipped === results.length) overallStatus = 'skipped';
    
    // Generate evidence chain hash
    const evidenceChainHash = this.generateEvidenceChainHash(results);
    
    return {
      orchestrationId,
      totalGates: results.length,
      passedGates: passed,
      failedGates: failed,
      skippedGates: skipped,
      warningGates: warning,
      overallStatus,
      totalDurationMs: endTime.getTime() - startTime.getTime(),
      results,
      startTime,
      endTime,
      evidenceChainHash
    };
  }

  private generateEvidenceChainHash(results: GateResult[]): string {
    const chainData = results.map(r => ({
      gateId: r.gateId,
      status: r.status,
      timestamp: r.timestamp.toISOString(),
      evidenceHashes: r.evidence.map(e => e.hash)
    }));
    
    return this.hashContent(JSON.stringify(chainData));
  }

  private hashContent(content: string): string {
    return createHash('sha256').update(content).digest('hex');
  }

  private signEvidence(evidence: GateEvidence): string {
    // In production, this would use proper cryptographic signing
    const signatureData = `${evidence.id}:${evidence.hash}:${evidence.timestamp.toISOString()}`;
    return createHash('sha256').update(signatureData).digest('hex');
  }

  private emitEvent(event: GateEvent): void {
    // Emit to all registered event listeners
    for (const listener of this.eventListeners) {
      try {
        listener(event);
      } catch (error) {
        // WARNING: If event listeners are critical for compliance or audit purposes
        // (e.g., writing to an audit log), silent failures could result in missing audit records.
        // Consider implementing critical event listener support that fails gate execution on error.
        this.options.logger.error('[GateExecutor] Event listener error - audit trail may be incomplete:', error);
      }
    }
    
    // Emit to the primary event handler if configured
    this.options.eventHandler(event);
  }

  /**
   * Generate execution ID using cryptographically secure random bytes
   */
  private generateExecutionId(): string {
    const random = randomBytes(6).toString('base64url').substring(0, 9);
    return `exec-${Date.now()}-${random}`;
  }

  /**
   * Generate event ID using cryptographically secure random bytes
   */
  private generateEventId(): string {
    const random = randomBytes(6).toString('base64url').substring(0, 9);
    return `evt-${Date.now()}-${random}`;
  }

  /**
   * Generate evidence ID using cryptographically secure random bytes
   */
  private generateEvidenceId(): string {
    const random = randomBytes(6).toString('base64url').substring(0, 9);
    return `evd-${Date.now()}-${random}`;
  }

  /**
   * Generate finding ID using cryptographically secure random bytes
   */
  private generateFindingId(): string {
    const random = randomBytes(6).toString('base64url').substring(0, 9);
    return `fnd-${Date.now()}-${random}`;
  }

  private chunkArray<T>(array: T[], size: number): T[][] {
    const chunks: T[][] = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  }
}

// GL Unified Charter Activated