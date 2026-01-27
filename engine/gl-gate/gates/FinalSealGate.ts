/**
 * @fileoverview GL-Gate:20 - Final Seal Layer (Irreversible Governance Baselines)
 * @module @machine-native-ops/gl-gate/gates/FinalSealGate
 * @version 1.0.0
 * @since 2026-01-26
 * @author MachineNativeOps
 * @gl-governed true
 * @gl-layer GL-40-GOVERNANCE
 * @gl-gate gl-gate:20
 * 
 * gl-gate:20 — Final Seal Layer (Irreversible Governance Baselines)
 * gl-gate:20：最終封印層（不可逆治理基線）
 * 
 * 負責將治理基線進行最終封存，使其不可逆、不可修改，
 * 確保治理狀態的完整性與永久性。
 * 
 * GL Unified Charter Activated
 */

import { createHash, createHmac, randomBytes } from 'crypto';
import { BaseGate } from './BaseGate';
import {
  GateId,
  GateContext,
  GateResult,
  GateConfig,
  GateFinding,
  GateMetric,
  GateEvidence
} from '../types';

/**
 * Final Seal Gate Configuration
 */
export interface FinalSealGateConfig extends GateConfig {
  /** Signing algorithm */
  algorithm?: 'sha256' | 'sha384' | 'sha512';
  /** Include timestamp in seal */
  includeTimestamp?: boolean;
  /** Require all prerequisite gates to pass */
  requireAllGatesPassed?: boolean;
  /** Evidence retention policy */
  retentionPolicy?: {
    minRetentionDays: number;
    maxRetentionDays: number;
  };
}

/**
 * Seal data structure
 */
export interface SealData {
  /** Seal ID */
  sealId: string;
  /** Seal version */
  version: string;
  /** Timestamp */
  timestamp: Date;
  /** Target being sealed */
  target: string;
  /** Environment */
  environment: string;
  /** Evidence chain */
  evidenceChain: EvidenceChainEntry[];
  /** Gate results summary */
  gateResultsSummary: GateResultSummary;
  /** Metadata */
  metadata: Record<string, unknown>;
}

export interface EvidenceChainEntry {
  /** Entry ID */
  id: string;
  /** Entry type */
  type: string;
  /** Content hash */
  hash: string;
  /** Previous entry hash (for chain) */
  previousHash: string;
  /** Timestamp */
  timestamp: Date;
}

export interface GateResultSummary {
  totalGates: number;
  passedGates: number;
  failedGates: number;
  warningGates: number;
  gateIds: string[];
}

/**
 * Sealed baseline
 */
export interface SealedBaseline {
  /** Seal data */
  sealData: SealData;
  /** Cryptographic signature */
  signature: string;
  /** Signature algorithm */
  algorithm: string;
  /** Public key fingerprint */
  keyFingerprint: string;
  /** Seal status */
  status: 'sealed' | 'verified' | 'invalid';
  /** Verification timestamp */
  verifiedAt?: Date;
}

/**
 * GL-Gate:20 - Final Seal Gate
 * 最終封印閘門
 * 
 * Responsible for final sealing of governance baselines,
 * making them irreversible and immutable.
 */
export class FinalSealGate extends BaseGate {
  public readonly gateId: GateId = 'gl-gate:20';
  public readonly nameEN = 'Final Seal Layer (Irreversible Governance Baselines)';
  public readonly nameZH = '最終封印層（不可逆治理基線）';

  private sealedBaselines: Map<string, SealedBaseline> = new Map();

  /**
   * Execute final seal gate
   */
  public async execute(context: GateContext, config?: FinalSealGateConfig): Promise<GateResult> {
    const startTime = Date.now();
    const findings: GateFinding[] = [];
    const metrics: GateMetric[] = [];

    const algorithm = config?.algorithm ?? 'sha256';
    const requireAllPassed = config?.requireAllGatesPassed ?? true;

    try {
      // Validate prerequisites
      const prereqValidation = await this.validatePrerequisites(context);
      if (!prereqValidation.valid) {
        for (const error of prereqValidation.errors) {
          findings.push(this.createFinding(
            'violation',
            'critical',
            'Prerequisite Validation Failed',
            error
          ));
        }
        return this.createFailedResult(
          context,
          'Final seal prerequisites not met',
          findings,
          metrics,
          startTime
        );
      }

      // Collect evidence chain
      const evidenceChain = await this.collectEvidenceChain(context);
      
      metrics.push(this.createMetric(
        'evidence_chain_length',
        evidenceChain.length,
        'count',
        { component: 'evidence' }
      ));

      // Validate evidence chain integrity
      const chainValidation = this.validateEvidenceChain(evidenceChain);
      
      metrics.push(this.createMetric(
        'evidence_chain_valid',
        chainValidation.valid ? 1 : 0,
        'boolean',
        { component: 'evidence' }
      ));

      if (!chainValidation.valid) {
        findings.push(this.createFinding(
          'violation',
          'critical',
          'Evidence Chain Integrity Failure',
          `Evidence chain validation failed: ${chainValidation.errors.join(', ')}`,
          { remediation: 'Investigate evidence chain tampering or corruption' }
        ));
        return this.createFailedResult(
          context,
          'Evidence chain integrity check failed',
          findings,
          metrics,
          startTime
        );
      }

      // Collect gate results summary
      const gateResultsSummary = await this.collectGateResultsSummary(context);
      
      metrics.push(this.createMetric(
        'gates_passed',
        gateResultsSummary.passedGates,
        'count',
        { component: 'gates' }
      ));

      metrics.push(this.createMetric(
        'gates_failed',
        gateResultsSummary.failedGates,
        'count',
        { component: 'gates' }
      ));

      // Check if all gates passed (if required)
      if (requireAllPassed && gateResultsSummary.failedGates > 0) {
        findings.push(this.createFinding(
          'violation',
          'high',
          'Not All Gates Passed',
          `${gateResultsSummary.failedGates} gate(s) failed. Cannot seal with failures.`,
          { remediation: 'Resolve all gate failures before sealing' }
        ));
        return this.createFailedResult(
          context,
          'Cannot seal: not all gates passed',
          findings,
          metrics,
          startTime
        );
      }

      // Create seal data
      const sealData: SealData = {
        sealId: this.generateSealId(),
        version: '1.0.0',
        timestamp: new Date(),
        target: context.target,
        environment: context.environment,
        evidenceChain,
        gateResultsSummary,
        metadata: {
          executionId: context.executionId,
          ...context.metadata
        }
      };

      // Generate cryptographic seal
      const sealedBaseline = await this.createSeal(sealData, algorithm);
      
      metrics.push(this.createMetric(
        'seal_created',
        1,
        'boolean',
        { component: 'seal' }
      ));

      // Verify seal immediately
      const verificationResult = await this.verifySeal(sealedBaseline);
      
      metrics.push(this.createMetric(
        'seal_verified',
        verificationResult.valid ? 1 : 0,
        'boolean',
        { component: 'seal' }
      ));

      if (!verificationResult.valid) {
        findings.push(this.createFinding(
          'violation',
          'critical',
          'Seal Verification Failed',
          `Seal verification failed immediately after creation: ${verificationResult.error}`,
          { remediation: 'Investigate seal generation process' }
        ));
        return this.createFailedResult(
          context,
          'Seal verification failed',
          findings,
          metrics,
          startTime
        );
      }

      // Store sealed baseline
      this.sealedBaselines.set(sealedBaseline.sealData.sealId, sealedBaseline);

      // Add seal evidence
      const sealEvidence: GateEvidence = {
        id: `seal-evidence-${sealedBaseline.sealData.sealId}`,
        type: 'signature',
        content: JSON.stringify({
          sealId: sealedBaseline.sealData.sealId,
          signature: sealedBaseline.signature,
          algorithm: sealedBaseline.algorithm,
          timestamp: sealedBaseline.sealData.timestamp
        }),
        hash: this.hashContent(sealedBaseline.signature),
        timestamp: new Date(),
        sealed: true,
        signature: sealedBaseline.signature
      };

      // Success findings
      findings.push(this.createFinding(
        'info',
        'info',
        'Governance Baseline Sealed',
        `Baseline sealed successfully with ID: ${sealedBaseline.sealData.sealId}`,
        { location: `seal://${sealedBaseline.sealData.sealId}` }
      ));

      const result = this.createSuccessResult(
        context,
        `Governance baseline sealed successfully. Seal ID: ${sealedBaseline.sealData.sealId}`,
        findings,
        metrics,
        startTime
      );

      result.evidence = [sealEvidence];

      return result;

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      findings.push(this.createFinding(
        'violation',
        'critical',
        'Final Seal Gate Execution Error',
        `Failed to execute final seal gate: ${errorMessage}`
      ));
      return this.createFailedResult(
        context,
        `Final seal gate failed: ${errorMessage}`,
        findings,
        metrics,
        startTime
      );
    }
  }

  /**
   * Validate prerequisites for sealing
   */
  public override async validatePrerequisites(context: GateContext): Promise<{ valid: boolean; errors: string[] }> {
    const errors: string[] = [];

    // Check that context has required fields
    if (!context.executionId) {
      errors.push('Execution ID is required for sealing');
    }

    if (!context.target) {
      errors.push('Target is required for sealing');
    }

    if (!context.environment) {
      errors.push('Environment is required for sealing');
    }

    // Check that governance summary gate (gl-gate:19) has been executed
    // In real implementation, this would check actual execution history
    const governanceSummaryExecuted = true; // Simulated
    if (!governanceSummaryExecuted) {
      errors.push('Governance summary gate (gl-gate:19) must be executed before sealing');
    }

    return { valid: errors.length === 0, errors };
  }

  /**
   * Collect evidence chain from previous gate executions
   */
  private async collectEvidenceChain(context: GateContext): Promise<EvidenceChainEntry[]> {
    // Simulated evidence chain - in production, collect from actual gate executions
    const chain: EvidenceChainEntry[] = [];
    let previousHash = '0'.repeat(64); // Genesis hash

    const gateIds = ['gl-gate:01', 'gl-gate:06', 'gl-gate:07', 'gl-gate:11', 'gl-gate:19'];
    
    for (let i = 0; i < gateIds.length; i++) {
      const entry: EvidenceChainEntry = {
        id: `evidence-${i + 1}`,
        type: 'gate-execution',
        hash: this.hashContent(`${gateIds[i]}-${context.executionId}-${i}`),
        previousHash,
        timestamp: new Date(Date.now() - (gateIds.length - i) * 60000)
      };
      
      previousHash = entry.hash;
      chain.push(entry);
    }

    return chain;
  }

  /**
   * Validate evidence chain integrity
   */
  private validateEvidenceChain(chain: EvidenceChainEntry[]): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (chain.length === 0) {
      errors.push('Evidence chain is empty');
      return { valid: false, errors };
    }

    // Verify chain linkage
    for (let i = 1; i < chain.length; i++) {
      if (chain[i].previousHash !== chain[i - 1].hash) {
        errors.push(`Chain broken at entry ${i}: previous hash mismatch`);
      }
    }

    // Verify timestamps are sequential
    for (let i = 1; i < chain.length; i++) {
      if (chain[i].timestamp < chain[i - 1].timestamp) {
        errors.push(`Timestamp inconsistency at entry ${i}`);
      }
    }

    return { valid: errors.length === 0, errors };
  }

  /**
   * Collect gate results summary
   */
  private async collectGateResultsSummary(_context: GateContext): Promise<GateResultSummary> {
    // Simulated summary - in production, collect from actual gate executions
    // TODO: Replace with actual gate execution result aggregation from context
    return {
      totalGates: 9,
      passedGates: 9,
      failedGates: 0,
      warningGates: 2,
      gateIds: [
        'gl-gate:01', 'gl-gate:02', 'gl-gate:06', 'gl-gate:07',
        'gl-gate:08', 'gl-gate:11', 'gl-gate:15', 'gl-gate:19', 'gl-gate:20'
      ]
    };
  }

  /**
   * Create cryptographic seal
   */
  private async createSeal(sealData: SealData, algorithm: string): Promise<SealedBaseline> {
    const dataToSign = JSON.stringify(sealData);
    const signature = this.signData(dataToSign, algorithm);
    const keyFingerprint = this.generateKeyFingerprint();

    return {
      sealData,
      signature,
      algorithm,
      keyFingerprint,
      status: 'sealed'
    };
  }

  /**
   * Verify seal integrity
   */
  private async verifySeal(baseline: SealedBaseline): Promise<{ valid: boolean; error?: string }> {
    try {
      const dataToVerify = JSON.stringify(baseline.sealData);
      const expectedSignature = this.signData(dataToVerify, baseline.algorithm);

      if (baseline.signature !== expectedSignature) {
        return { valid: false, error: 'Signature mismatch' };
      }

      baseline.status = 'verified';
      baseline.verifiedAt = new Date();

      return { valid: true };
    } catch (error) {
      return { 
        valid: false, 
        error: error instanceof Error ? error.message : 'Unknown verification error' 
      };
    }
  }

  /**
   * Get sealed baseline by ID
   */
  public getSealedBaseline(sealId: string): SealedBaseline | undefined {
    return this.sealedBaselines.get(sealId);
  }

  /**
   * Verify existing seal
   */
  public async verifyExistingSeal(sealId: string): Promise<{ valid: boolean; error?: string }> {
    const baseline = this.sealedBaselines.get(sealId);
    if (!baseline) {
      return { valid: false, error: 'Seal not found' };
    }
    return this.verifySeal(baseline);
  }

  /**
   * Sign data using HMAC
   */
  private signData(data: string, algorithm: string): string {
    // In production, GL_SEAL_SECRET must be provided via secure key management (HSM, KMS, etc.)
    const baseSecret = process.env.GL_SEAL_SECRET;

    if (process.env.NODE_ENV === 'production' && (!baseSecret || baseSecret.trim() === '')) {
      throw new Error('GL_SEAL_SECRET must be set in production environments for FinalSealGate.');
    }

    // In non-production environments, fall back to a clearly marked development key if no secret is provided.
    const effectiveSecret = baseSecret && baseSecret.trim() !== '' ? baseSecret : 'default-dev-key';
    const secretKey = `gl-gate-seal-key-${effectiveSecret}`;
    
    return createHmac(algorithm, secretKey).update(data).digest('hex');
  }

  /**
   * Hash content
   */
  private hashContent(content: string): string {
    return createHash('sha256').update(content).digest('hex');
  }

  /**
   * Generate seal ID using cryptographically secure random bytes
   */
  private generateSealId(): string {
    const timestamp = Date.now().toString(36);
    const random = randomBytes(6).toString('base64url').substring(0, 9);
    return `seal-${timestamp}-${random}`;
  }

  /**
   * Generate key fingerprint
   */
  private generateKeyFingerprint(): string {
    // In production, derive from actual public key
    return createHash('sha256')
      .update('gl-gate-public-key')
      .digest('hex')
      .substring(0, 16);
  }
}

// GL Unified Charter Activated