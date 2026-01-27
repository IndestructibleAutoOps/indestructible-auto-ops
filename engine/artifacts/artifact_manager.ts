/**
 * @module artifact_manager
 * @description Artifact lifecycle management with full audit trail
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
import { EvidenceRecord } from '../interfaces.d';
import type { ArtifactContent, ArtifactMetadata, ArtifactListItem } from '../types';

/**
 * Artifact Manager
 * 
 * GL90-99: Meta Layer - Artifacts Management
 * 
 * Manages artifact lifecycle including creation, storage,
 * retrieval, and cleanup with full audit trail.
 */
export class ArtifactManager {
  private evidence: EvidenceRecord[] = [];
  private readonly storageDir: string;
  private readonly artifacts: Map<string, ArtifactContent> = new Map();
  private readonly index: Map<string, string[]> = new Map();

  constructor(options?: {
    storageDir?: string;
  }) {
    this.storageDir = options?.storageDir || './artifacts';
    this.ensureDirectoryExists(this.storageDir);
    this.loadIndex();
  }

  /**
   * Store artifact
   */
  async store(
    artifactId: string,
    artifact: ArtifactContent,
    metadata?: ArtifactMetadata
  ): Promise<{
    success: boolean;
    path: string;
    errors: string[];
  }> {
    const startTime = Date.now();
    const errors: string[] = [];

    try {
      // Resolve artifact path
      const artifactPath = path.join(this.storageDir, `${artifactId}.json`);

      // Store artifact
      const artifactData: ArtifactContent = {
        ...artifact,
        metadata: {
          ...metadata,
          storedAt: new Date().toISOString(),
          version: this.generateVersion()
        }
      };

      fs.writeFileSync(artifactPath, JSON.stringify(artifactData, null, 2), 'utf-8');

      // Update index
      this.artifacts.set(artifactId, artifactData);
      this.updateIndex(artifactId, artifactData);

      // Generate evidence record
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'artifacts',
        component: 'artifact_manager',
        action: 'store',
        status: 'success',
        input: { artifactId },
        output: { path: artifactPath },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        success: true,
        path: artifactPath,
        errors: []
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      errors.push(errorMsg);

      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'artifacts',
        component: 'artifact_manager',
        action: 'store',
        status: 'error',
        input: { artifactId },
        output: { error: errorMsg },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        success: false,
        path: '',
        errors
      };
    }
  }

  /**
   * Retrieve artifact
   */
  async retrieve(artifactId: string): Promise<ArtifactContent | null> {
    const startTime = Date.now();

    try {
      const artifact = this.artifacts.get(artifactId);

      if (!artifact) {
        return null;
      }

      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'artifacts',
        component: 'artifact_manager',
        action: 'retrieve',
        status: 'success',
        input: { artifactId },
        output: {},
        metrics: { duration: Date.now() - startTime }
      });

      return artifact;
    } catch (error) {
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'artifacts',
        component: 'artifact_manager',
        action: 'retrieve',
        status: 'error',
        input: { artifactId },
        output: { error: error instanceof Error ? error.message : String(error) },
        metrics: { duration: Date.now() - startTime }
      });

      return null;
    }
  }

  /**
   * Delete artifact
   */
  async delete(artifactId: string): Promise<boolean> {
    const startTime = Date.now();

    try {
      const artifact = this.artifacts.get(artifactId);

      if (!artifact) {
        return false;
      }

      // Delete artifact file
      const artifactPath = path.join(this.storageDir, `${artifactId}.json`);

      if (fs.existsSync(artifactPath)) {
        fs.unlinkSync(artifactPath);
      }

      // Remove from index
      this.artifacts.delete(artifactId);
      this.removeFromIndex(artifactId);

      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'artifacts',
        component: 'artifact_manager',
        action: 'delete',
        status: 'success',
        input: { artifactId },
        output: {},
        metrics: { duration: Date.now() - startTime }
      });

      return true;
    } catch (error) {
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'artifacts',
        component: 'artifact_manager',
        action: 'delete',
        status: 'error',
        input: { artifactId },
        output: { error: error instanceof Error ? error.message : String(error) },
        metrics: { duration: Date.now() - startTime }
      });

      return false;
    }
  }

  /**
   * List all artifacts
   */
  list(): ArtifactListItem[] {
    return Array.from(this.artifacts.entries()).map(([id, artifact]) => ({
      id,
      type: artifact.type,
      name: artifact.name,
      tags: (artifact.metadata as ArtifactMetadata)?.tags || [],
      createdAt: (artifact.metadata as ArtifactMetadata)?.createdAt || '',
      checksum: (artifact.metadata as ArtifactMetadata)?.checksum || ''
    }));
  }

  /**
   * List artifacts by type
   */
  listByType(type: string): ArtifactListItem[] {
    return this.list().filter(artifact => artifact.type === type);
  }

  /**
   * List artifacts by tag
   */
  listByTag(tag: string): ArtifactListItem[] {
    return this.list().filter(artifact =>
      artifact.tags?.includes(tag)
    );
  }

  /**
   * Search artifacts
   */
  search(query: {
    type?: string;
    tags?: string[];
    from?: Date;
    to?: Date;
  }): ArtifactListItem[] {
    let results = this.list();

    if (query.type) {
      results = results.filter(a => a.type === query.type);
    }

    if (query.tags && query.tags.length > 0) {
      results = results.filter(a =>
        query.tags!.some(tag => a.tags?.includes(tag))
      );
    }

    if (query.from) {
      const fromTime = query.from.getTime();
      results = results.filter(a => {
        const createdAt = new Date(a.createdAt).getTime();
        return createdAt >= fromTime;
      });
    }

    if (query.to) {
      const toTime = query.to.getTime();
      results = results.filter(a => {
        const createdAt = new Date(a.createdAt).getTime();
        return createdAt <= toTime;
      });
    }

    return results;
  }

  /**
   * Generate artifact statistics
   */
  getStatistics(): {
    total: number;
    byType: Map<string, number>;
    byTag: Map<string, number>;
    totalSize: number;
  } {
    const byType = new Map<string, number>();
    const byTag = new Map<string, number>();
    let totalSize = 0;

    for (const [id, artifact] of this.artifacts.entries()) {
      // Count by type
      byType.set(artifact.type, (byType.get(artifact.type) || 0) + 1);

      // Count by tags
      const tags = (artifact.metadata as ArtifactMetadata)?.tags;
      if (tags) {
        for (const tag of tags) {
          byTag.set(tag, (byTag.get(tag) || 0) + 1);
        }
      }

      // Calculate size
      const artifactPath = path.join(this.storageDir, `${id}.json`);
      if (fs.existsSync(artifactPath)) {
        totalSize += fs.statSync(artifactPath).size;
      }
    }

    return {
      total: this.artifacts.size,
      byType,
      byTag,
      totalSize
    };
  }

  /**
   * Update index
   */
  private updateIndex(artifactId: string, artifact: ArtifactContent): void {
    const type = artifact.type;

    if (!this.index.has(type)) {
      this.index.set(type, []);
    }

    this.index.get(type)!.push(artifactId);
    this.saveIndex();
  }

  /**
   * Remove from index
   */
  private removeFromIndex(artifactId: string): void {
    const artifact = this.artifacts.get(artifactId);

    if (artifact) {
      const type = artifact.type;
      const typeIndex = this.index.get(type);

      if (typeIndex) {
        const index = typeIndex.indexOf(artifactId);
        if (index > -1) {
          typeIndex.splice(index, 1);
        }
      }

      this.saveIndex();
    }
  }

  /**
   * Load index from disk
   */
  private loadIndex(): void {
    const indexPath = path.join(this.storageDir, 'index.json');

    if (fs.existsSync(indexPath)) {
      try {
        const indexData = JSON.parse(fs.readFileSync(indexPath, 'utf-8')) as Record<string, string[]>;

        for (const [type, artifactIds] of Object.entries(indexData)) {
          this.index.set(type, artifactIds);
        }

        // Load artifacts
        for (const [, artifactIds] of this.index.entries()) {
          for (const artifactId of artifactIds) {
            const artifactPath = path.join(this.storageDir, `${artifactId}.json`);

            if (fs.existsSync(artifactPath)) {
              const artifact = JSON.parse(fs.readFileSync(artifactPath, 'utf-8')) as ArtifactContent;
              this.artifacts.set(artifactId, artifact);
            }
          }
        }
      } catch (error) {
        console.error('Failed to load index:', error);
      }
    }
  }

  /**
   * Save index to disk
   */
  private saveIndex(): void {
    const indexPath = path.join(this.storageDir, 'index.json');
    const indexData = Object.fromEntries(this.index);

    fs.writeFileSync(indexPath, JSON.stringify(indexData, null, 2), 'utf-8');
  }

  /**
   * Generate version
   */
  private generateVersion(): string {
    return `v${Date.now()}`;
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