/**
 * @module manifest_generator
 * @description Deployment manifest generation with verification
 * @gl-governed
 * GL Unified Charter Activated
 * @gl-layer GL-30-EXECUTION
 * @gl-module engine/artifacts
 * @gl-semantic-anchor GL-30-EXEC-TS
 * @gl-evidence-required true
 * @version 1.0.0
 * @since 2026-01-24
 * @author MachineNativeOps Team
 */

import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';
import { EvidenceRecord } from '../interfaces.d';
import type { ManifestArtifact, GeneratedManifest, ManifestResult } from '../types';

/**
 * Manifest Generator
 * 
 * GL90-99: Meta Layer - Manifest Management
 * 
 * Generates deployment manifests with artifact listings,
 * dependencies, and verification data.
 */
export class ManifestGenerator {
  private evidence: EvidenceRecord[] = [];
  private readonly outputDir: string;

  constructor(options?: {
    outputDir?: string;
  }) {
    this.outputDir = options?.outputDir || './artifacts';
    this.ensureDirectoryExists(this.outputDir);
  }

  /**
   * Generate deployment manifest
   */
  async generate(
    config: {
      name: string;
      version: string;
      environment: string;
      artifacts: ManifestArtifact[];
      evidence?: EvidenceRecord[];
    }
  ): Promise<ManifestResult> {
    const startTime = Date.now();
    const errors: string[] = [];

    try {
      // Generate manifest
      const manifest: GeneratedManifest = {
        name: config.name,
        version: config.version,
        generatedAt: new Date().toISOString(),
        artifacts: await this.generateArtifactList(config.artifacts),
        dependencies: this.generateDependencyList(config.artifacts),
        verification: this.generateVerificationData(config.artifacts),
        metadata: {
          environment: config.environment,
          generator: 'Machine-Native-Architecture AEP',
          chainId: this.generateChainId(),
          evidence: this.generateEvidenceSummary(config.evidence || [])
        }
      };

      // Save manifest
      const manifestPath = path.join(
        this.outputDir,
        `manifest_${config.environment}_${config.version}.json`
      );

      fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), 'utf-8');

      // Generate evidence record
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'artifacts',
        component: 'manifest_generator',
        action: 'generate',
        status: 'success',
        input: {
          name: config.name,
          version: config.version,
          environment: config.environment,
          artifactCount: config.artifacts.length
        },
        output: {
          path: manifestPath,
          artifactCount: manifest.artifacts.length,
          dependencyCount: manifest.dependencies.length
        },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        status: 'success',
        manifest,
        errors: [],
        warnings: []
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      errors.push(errorMsg);

      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'artifacts',
        component: 'manifest_generator',
        action: 'generate',
        status: 'error',
        input: { name: config.name },
        output: { error: errorMsg },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        status: 'error',
        manifest: {
          name: config.name,
          version: config.version,
          generatedAt: new Date().toISOString(),
          artifacts: [],
          dependencies: [],
          verification: { checksum: '', algorithm: 'sha256' }
        },
        errors,
        warnings: []
      };
    }
  }

  /**
   * Generate artifact list
   */
  private async generateArtifactList(artifacts: ManifestArtifact[]): Promise<ManifestArtifact[]> {
    const artifactList: ManifestArtifact[] = [];

    for (const artifact of artifacts) {
      const artifactData: ManifestArtifact = {
        id: artifact.id,
        type: artifact.type,
        name: artifact.name,
        path: artifact.path,
        checksum: artifact.checksum || this.generateHash(JSON.stringify(artifact)),
        dependencies: artifact.dependencies || [],
        metadata: artifact.metadata || {}
      };

      artifactList.push(artifactData);
    }

    return artifactList;
  }

  /**
   * Generate dependency list
   */
  private generateDependencyList(artifacts: ManifestArtifact[]): string[] {
    const dependencies = new Set<string>();

    for (const artifact of artifacts) {
      if (artifact.dependencies) {
        for (const dep of artifact.dependencies) {
          dependencies.add(dep);
        }
      }
    }

    return Array.from(dependencies);
  }

  /**
   * Generate verification data
   */
  private generateVerificationData(artifacts: ManifestArtifact[]): {
    algorithm: string;
    checksum: string;
    checksums?: Record<string, string>;
  } {
    const checksums: Record<string, string> = {};
    const hashes: string[] = [];

    for (const artifact of artifacts) {
      const hash = artifact.checksum || this.generateHash(JSON.stringify(artifact));
      checksums[artifact.id] = hash;
      hashes.push(hash);
    }

    // Generate total checksum
    const totalChecksum = this.generateHash(hashes.join(''));

    return {
      algorithm: 'sha256',
      checksum: totalChecksum,
      checksums
    };
  }

  /**
   * Generate evidence summary
   */
  private generateEvidenceSummary(evidence: EvidenceRecord[]): {
    totalRecords: number;
    byStage: Record<string, number>;
    hash: string;
  } {
    const byStage: Record<string, number> = {};

    for (const record of evidence) {
      byStage[record.stage] = (byStage[record.stage] || 0) + 1;
    }

    return {
      totalRecords: evidence.length,
      byStage,
      hash: this.generateHash(JSON.stringify(evidence))
    };
  }

  /**
   * Verify manifest
   */
  async verify(manifestPath: string): Promise<{
    valid: boolean;
    errors: string[];
  }> {
    const startTime = Date.now();
    const errors: string[] = [];

    try {
      // Load manifest
      if (!fs.existsSync(manifestPath)) {
        errors.push(`Manifest file not found: ${manifestPath}`);
        return { valid: false, errors };
      }

      const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8')) as GeneratedManifest;

      // Verify metadata
      if (!manifest.name || !manifest.version) {
        errors.push('Invalid manifest metadata');
      }

      // Verify artifacts
      if (!Array.isArray(manifest.artifacts)) {
        errors.push('Invalid artifacts list');
      } else {
        for (const artifact of manifest.artifacts) {
          if (!artifact.id || !artifact.checksum) {
            errors.push(`Invalid artifact: ${artifact.id}`);
          }

          // Verify artifact file exists if path is provided
          if (artifact.path) {
            // Sanitize path to prevent path traversal attacks
            const sanitizedPath = path.normalize(artifact.path).replace(/^(\.\.(\/|\\|$))+/, '');
            const artifactPath = path.join(this.outputDir, sanitizedPath);
            // Ensure the resolved path is within outputDir (prevent path traversal)
            const resolvedPath = path.resolve(artifactPath);
            const resolvedOutputDir = path.resolve(this.outputDir);
            if (!resolvedPath.startsWith(resolvedOutputDir + path.sep) && resolvedPath !== resolvedOutputDir) {
              errors.push(`Path traversal detected for artifact: ${artifact.id}`);
              continue;
            }
            if (fs.existsSync(resolvedPath)) {
              const content = fs.readFileSync(resolvedPath, 'utf-8');
              const hash = this.generateHash(content);

              if (hash !== artifact.checksum) {
                errors.push(`Artifact hash mismatch: ${artifact.id}`);
              }
            }
          }
        }
      }

      // Verify verification data
      if (manifest.verification && manifest.verification.checksums) {
        const hashes = Object.values(manifest.verification.checksums);
        const calculatedTotal = this.generateHash(hashes.join(''));

        if (calculatedTotal !== manifest.verification.checksum) {
          errors.push('Total checksum verification failed');
        }
      }

      const valid = errors.length === 0;

      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'artifacts',
        component: 'manifest_generator',
        action: 'verify',
        status: valid ? 'success' : 'error',
        input: { manifestPath },
        output: { valid, errorCount: errors.length },
        metrics: { duration: Date.now() - startTime }
      });

      return { valid, errors };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      errors.push(errorMsg);

      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'artifacts',
        component: 'manifest_generator',
        action: 'verify',
        status: 'error',
        input: { manifestPath },
        output: { error: errorMsg },
        metrics: { duration: Date.now() - startTime }
      });

      return { valid: false, errors };
    }
  }

  /**
   * Load manifest
   */
  load(manifestPath: string): GeneratedManifest | null {
    try {
      if (!fs.existsSync(manifestPath)) {
        return null;
      }

      return JSON.parse(fs.readFileSync(manifestPath, 'utf-8')) as GeneratedManifest;
    } catch (error) {
      return null;
    }
  }

  /**
   * Generate chain ID
   */
  private generateChainId(): string {
    return `chain_${Date.now()}_${crypto.randomBytes(8).toString('hex')}`;
  }

  /**
   * Generate SHA256 hash
   */
  private generateHash(data: string): string {
    return crypto.createHash('sha256').update(data).digest('hex');
  }

  /**
   * Ensure directory exists
   */
  private ensureDirectoryExists(dirPath: string): void {
    if (!fs.existsSync(dirPath)) {
      fs.mkdirSync(dirPath, { recursive: true });
    }
  }

  /**
   * Get evidence records
   */
  getEvidence(): EvidenceRecord[] {
    return this.evidence;
  }
}