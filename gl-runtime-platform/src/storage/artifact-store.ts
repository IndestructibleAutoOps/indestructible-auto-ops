// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: artifact-store
// @GL-charter-version: 2.0.0

import fs from 'fs/promises';
import path from 'path';
import { createLogger } from '../utils/logger';

const logger = createLogger('ArtifactStore');

export interface Artifact {
  id: string;
  type: 'audit-report' | 'patch' | 'metadata' | 'validation-result';
  name: string;
  content: any;
  timestamp: string;
  metadata: any;
}

export class ArtifactStore {
  private artifactsPath: string;
  private artifacts: Map<string, Artifact> = new Map();

  constructor() {
    this.artifactsPath = path.join(process.cwd(), 'storage', 'gl-artifacts');
  }

  public async storeArtifact(artifact: Artifact): Promise<void> {
    this.artifacts.set(artifact.id, artifact);
    await this.persistArtifact(artifact);
    logger.info(`Artifact stored: ${artifact.id}`);
  }

  private async persistArtifact(artifact: Artifact): Promise<void> {
    try {
      const artifactPath = path.join(this.artifactsPath, artifact.type);
      await fs.mkdir(artifactPath, { recursive: true });
      
      const filePath = path.join(artifactPath, `${artifact.id}.json`);
      await fs.writeFile(filePath, JSON.stringify(artifact, null, 2));
    } catch (error: any) {
      logger.error(`Failed to persist artifact: ${error.message}`);
      throw error;
    }
  }

  public async loadArtifact(id: string): Promise<Artifact | null> {
    const cached = this.artifacts.get(id);
    if (cached) return cached;

    try {
      const artifactPath = path.join(this.artifactsPath);
      const files = await fs.readdir(artifactPath, { recursive: true });
      
      for (const dir of files) {
        try {
          const filePath = path.join(this.artifactsPath, dir, `${id}.json`);
          const content = await fs.readFile(filePath, 'utf-8');
          const artifact = JSON.parse(content);
          this.artifacts.set(id, artifact);
          return artifact;
        } catch {
          continue;
        }
      }
      
      return null;
    } catch (error: any) {
      logger.error(`Failed to load artifact: ${error.message}`);
      return null;
    }
  }

  public async getArtifactsByType(type: string): Promise<Artifact[]> {
    const allArtifacts: Artifact[] = [];
    
    try {
      const typePath = path.join(this.artifactsPath, type);
      const files = await fs.readdir(typePath);
      
      for (const file of files) {
        const artifactId = file.replace('.json', '');
        const artifact = await this.loadArtifact(artifactId);
        if (artifact) {
          allArtifacts.push(artifact);
        }
      }
    } catch (error: any) {
      if (error.code !== 'ENOENT') {
        logger.error(`Failed to get artifacts by type: ${error.message}`);
      }
    }
    
    return allArtifacts;
  }

  public async deleteArtifact(id: string): Promise<void> {
    this.artifacts.delete(id);
    
    try {
      const artifactPath = path.join(this.artifactsPath);
      const files = await fs.readdir(artifactPath, { recursive: true });
      
      for (const dir of files) {
        try {
          const filePath = path.join(this.artifactsPath, dir, `${id}.json`);
          await fs.unlink(filePath);
          logger.info(`Artifact deleted: ${id}`);
          return;
        } catch {
          continue;
        }
      }
    } catch (error: any) {
      logger.error(`Failed to delete artifact: ${error.message}`);
    }
  }

  public getArtifactCount(): number {
    return this.artifacts.size;
  }

  public clearArtifacts(): void {
    this.artifacts.clear();
  }
}