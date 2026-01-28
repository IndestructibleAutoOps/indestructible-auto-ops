/**
 * GL Self-Versioning
 * @GL-layer: GL12
 * @GL-semantic: self-versioning
 * @GL-audit-trail: ../../governance/GL_ROOT_SEMANTIC_ANCHOR.json
 * 
 * Generates, compares, selects, and deploys new versions autonomously.
 */

import { EventEmitter } from 'events';

export interface Version {
  id: string;
  number: string;
  type: 'major' | 'minor' | 'patch' | 'evolution';
  createdAt: Date;
  changes: VersionChange[];
  metrics: VersionMetrics;
  status: 'draft' | 'candidate' | 'stable' | 'deprecated';
}

export interface VersionChange {
  type: 'feature' | 'improvement' | 'fix' | 'refactor' | 'evolution';
  component: string;
  description: string;
}

export interface VersionMetrics {
  performance: number;
  stability: number;
  compatibility: number;
  overall: number;
}

export interface VersionComparison {
  versionA: Version;
  versionB: Version;
  winner: Version;
  reason: string;
  improvement: number;
}

export class SelfVersioning extends EventEmitter {
  private versions: Map<string, Version> = new Map();
  private currentVersion: Version | null = null;
  private autoDeploy: boolean = false;
  private autoPromote: boolean = true;

  constructor() {
    super();
  }

  /**
   * Create a new version
   */
  async createVersion(
    baseVersion: string,
    changes: VersionChange[],
    type: 'major' | 'minor' | 'patch' | 'evolution'
  ): Promise<Version> {
    const newNumber = this.incrementVersion(baseVersion, type);
    
    const version: Version = {
      id: this.generateId(),
      number: newNumber,
      type,
      createdAt: new Date(),
      changes,
      metrics: {
        performance: 0,
        stability: 0,
        compatibility: 0,
        overall: 0
      },
      status: 'draft'
    };

    this.versions.set(version.id, version);
    this.emit('version-created', version);

    return version;
  }

  /**
   * Promote version to candidate
   */
  async promoteToCandidate(versionId: string): Promise<boolean> {
    const version = this.versions.get(versionId);
    if (!version) {
      return false;
    }

    version.status = 'candidate';
    this.emit('version-promoted', { version, status: 'candidate' });
    return true;
  }

  /**
   * Promote version to stable
   */
  async promoteToStable(versionId: string): Promise<boolean> {
    const version = this.versions.get(versionId);
    if (!version) {
      return false;
    }

    version.status = 'stable';
    this.emit('version-promoted', { version, status: 'stable' });
    
    // Auto-deploy if enabled
    if (this.autoDeploy) {
      await this.deployVersion(versionId);
    }
    
    return true;
  }

  /**
   * Deprecate a version
   */
  async deprecateVersion(versionId: string): Promise<boolean> {
    const version = this.versions.get(versionId);
    if (!version) {
      return false;
    }

    version.status = 'deprecated';
    this.emit('version-deprecated', version);
    return true;
  }

  /**
   * Compare two versions
   */
  async compareVersions(versionAId: string, versionBId: string): Promise<VersionComparison> {
    const versionA = this.versions.get(versionAId);
    const versionB = this.versions.get(versionBId);

    if (!versionA || !versionB) {
      throw new Error('One or both versions not found');
    }

    const comparison = this.calculateComparison(versionA, versionB);
    this.emit('versions-compared', comparison);

    return comparison;
  }

  /**
   * Select best version from candidates
   */
  async selectBestVersion(candidateIds: string[]): Promise<Version | null> {
    if (candidateIds.length === 0) {
      return null;
    }

    let bestVersion: Version | null = null;
    let bestScore = -1;

    for (const id of candidateIds) {
      const version = this.versions.get(id);
      if (!version || version.status !== 'candidate') {
        continue;
      }

      const score = this.calculateScore(version);
      if (score > bestScore) {
        bestScore = score;
        bestVersion = version;
      }
    }

    return bestVersion;
  }

  /**
   * Deploy a version
   */
  async deployVersion(versionId: string): Promise<boolean> {
    const version = this.versions.get(versionId);
    if (!version || version.status !== 'stable') {
      return false;
    }

    try {
      // Implement deployment logic
      this.currentVersion = version;
      this.emit('version-deployed', version);
      return true;
    } catch (error) {
      this.emit('deployment-failed', { version, error });
      return false;
    }
  }

  /**
   * Rollback to previous version
   */
  async rollbackVersion(versionId: string): Promise<boolean> {
    const version = this.versions.get(versionId);
    if (!version) {
      return false;
    }

    try {
      // Implement rollback logic
      this.currentVersion = version;
      this.emit('version-rolled-back', version);
      return true;
    } catch (error) {
      this.emit('rollback-failed', { version, error });
      return false;
    }
  }

  /**
   * Update version metrics
   */
  async updateMetrics(versionId: string, metrics: Partial<VersionMetrics>): Promise<boolean> {
    const version = this.versions.get(versionId);
    if (!version) {
      return false;
    }

    Object.assign(version.metrics, metrics);
    
    // Calculate overall score
    version.metrics.overall = (
      version.metrics.performance + 
      version.metrics.stability + 
      version.metrics.compatibility
    ) / 3;

    this.emit('metrics-updated', { version, metrics });

    // Auto-promote if enabled and metrics are good enough
    if (this.autoPromote && version.status === 'candidate' && version.metrics.overall > 0.8) {
      await this.promoteToStable(versionId);
    }

    return true;
  }

  /**
   * Get version by ID
   */
  getVersion(versionId: string): Version | undefined {
    return this.versions.get(versionId);
  }

  /**
   * Get version by number
   */
  getVersionByNumber(versionNumber: string): Version | undefined {
    for (const version of this.versions.values()) {
      if (version.number === versionNumber) {
        return version;
      }
    }
    return undefined;
  }

  /**
   * Get current version
   */
  getCurrentVersion(): Version | null {
    return this.currentVersion;
  }

  /**
   * Get all versions
   */
  getAllVersions(): Version[] {
    return Array.from(this.versions.values());
  }

  /**
   * Get versions by status
   */
  getVersionsByStatus(status: Version['status']): Version[] {
    return Array.from(this.versions.values()).filter(v => v.status === status);
  }

  /**
   * Enable/disable auto-deploy
   */
  setAutoDeploy(enabled: boolean): void {
    this.autoDeploy = enabled;
    this.emit('auto-deploy-changed', { enabled });
  }

  /**
   * Enable/disable auto-promote
   */
  setAutoPromote(enabled: boolean): void {
    this.autoPromote = enabled;
    this.emit('auto-promote-changed', { enabled });
  }

  /**
   * Increment version number
   */
  private incrementVersion(currentVersion: string, type: string): string {
    const parts = currentVersion.split('.').map(Number);
    
    switch (type) {
      case 'major':
        parts[0]++;
        parts[1] = 0;
        parts[2] = 0;
        break;
      case 'minor':
        parts[1]++;
        parts[2] = 0;
        break;
      case 'patch':
        parts[2]++;
        break;
      case 'evolution':
        // Evolution versions add a fourth component
        parts[3] = (parts[3] || 0) + 1;
        break;
    }

    return parts.join('.');
  }

  /**
   * Calculate version comparison
   */
  private calculateComparison(versionA: Version, versionB: Version): VersionComparison {
    const scoreA = this.calculateScore(versionA);
    const scoreB = this.calculateScore(versionB);

    const winner = scoreA > scoreB ? versionA : versionB;
    const improvement = Math.abs(scoreA - scoreB);
    const reason = scoreA > scoreB 
      ? 'Version A has better metrics' 
      : 'Version B has better metrics';

    return {
      versionA,
      versionB,
      winner,
      reason,
      improvement
    };
  }

  /**
   * Calculate overall version score
   */
  private calculateScore(version: Version): number {
    return version.metrics.overall;
  }

  private generateId(): string {
    return `version_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}