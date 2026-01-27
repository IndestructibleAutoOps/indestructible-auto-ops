/**
 * @module anchor_resolver
 * @description Semantic anchor resolution for configuration
 * @gl-governed
 * GL Unified Charter Activated
 * @gl-layer GL-10-OPERATIONAL
 * @gl-module engine/governance
 * @gl-semantic-anchor GL-10-GOV-TS
 * @gl-evidence-required true
 * @version 1.0.0
 * @since 2026-01-24
 * @author MachineNativeOps Team
 */

import { EvidenceRecord } from '../interfaces.d';
import type { ConfigObject, AnchorDefinition, AnchorUsage } from '../types';

interface StoredAnchor {
  name: string;
  path: string;
  value: unknown;
}

/**
 * Anchor Resolver
 * 
 * GL00-99: Unified Governance Framework
 * 
 * Resolves semantic anchors in configuration, ensuring
 * traceability and auditability of all references.
 */
export class AnchorResolver {
  private evidence: EvidenceRecord[] = [];
  private readonly anchorDefinitions: Map<string, StoredAnchor> = new Map();
  private readonly anchorUsages: Map<string, string[]> = new Map();

  constructor() {
    // Initialize with default semantic anchors
    this.initializeDefaultAnchors();
  }

  /**
   * Resolve semantic anchors in configuration
   */
  async resolve(
    config: ConfigObject
  ): Promise<{
    resolved: ConfigObject;
    anchorsFound: number;
    aliasesFound: number;
    errors: string[];
  }> {
    const startTime = Date.now();
    const errors: string[] = [];
    let anchorsFound = 0;
    let aliasesFound = 0;

    try {
      // Extract and register anchor definitions
      const anchors = this.extractAnchors(config);
      anchorsFound = anchors.length;

      for (const anchor of anchors) {
        this.anchorDefinitions.set(anchor.name, anchor);
      }

      // Extract and track anchor usages
      const usages = this.extractUsages(config);
      aliasesFound = usages.length;

      for (const usage of usages) {
        if (!this.anchorUsages.has(usage.name)) {
          this.anchorUsages.set(usage.name, []);
        }
        this.anchorUsages.get(usage.name)!.push(usage.path);
      }

      // Validate anchor references
      const validationErrors = this.validateReferences();
      errors.push(...validationErrors);

      // Resolve anchors
      const resolved = this.resolveReferences(config);

      // Generate evidence record
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'governance',
        component: 'anchor_resolver',
        action: 'resolve',
        status: errors.length === 0 ? 'success' : 'warning',
        input: { anchorsFound, aliasesFound },
        output: {
          resolved: true,
          errorCount: errors.length
        },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        resolved,
        anchorsFound,
        aliasesFound,
        errors
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      errors.push(errorMsg);

      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'governance',
        component: 'anchor_resolver',
        action: 'resolve',
        status: 'error',
        input: {},
        output: { error: errorMsg },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        resolved: config,
        anchorsFound,
        aliasesFound,
        errors
      };
    }
  }

  /**
   * Extract anchor definitions
   */
  private extractAnchors(config: ConfigObject): StoredAnchor[] {
    const anchors: StoredAnchor[] = [];

    const traverse = (obj: unknown, path: string = ''): void => {
      if (!obj || typeof obj !== 'object') {
        return;
      }

      const record = obj as Record<string, unknown>;

      // Check for anchor marker
      if (record.$anchor) {
        anchors.push({
          name: record.$anchor as string,
          path,
          value: record.value
        });
      }

      // Traverse nested objects
      for (const key in record) {
        if (key === '$anchor' || key === 'value') {
          continue;
        }
        traverse(record[key], path ? `${path}.${key}` : key);
      }
    };

    traverse(config);
    return anchors;
  }

  /**
   * Extract anchor usages
   */
  private extractUsages(config: ConfigObject): AnchorUsage[] {
    const usages: AnchorUsage[] = [];

    const traverse = (obj: unknown, path: string = ''): void => {
      if (!obj || typeof obj !== 'object') {
        return;
      }

      const record = obj as Record<string, unknown>;

      // Check for alias marker
      if (record.$ref) {
        usages.push({
          name: record.$ref as string,
          path
        });
      }

      // Traverse nested objects
      for (const key in record) {
        if (key === '$ref') {
          continue;
        }
        traverse(record[key], path ? `${path}.${key}` : key);
      }
    };

    traverse(config);
    return usages;
  }

  /**
   * Validate anchor references
   */
  private validateReferences(): string[] {
    const errors: string[] = [];

    for (const [anchorName, usages] of this.anchorUsages.entries()) {
      if (!this.anchorDefinitions.has(anchorName)) {
        for (const usage of usages) {
          errors.push(`Undefined anchor referenced: ${anchorName} at ${usage}`);
        }
      }
    }

    // Check for unused anchors
    for (const anchorName of this.anchorDefinitions.keys()) {
      if (!this.anchorUsages.has(anchorName)) {
        this.evidence.push({
          timestamp: new Date().toISOString(),
          stage: 'governance',
          component: 'anchor_resolver',
          action: 'warning',
          status: 'warning',
          input: { anchor: anchorName },
          output: { message: 'Unused anchor definition' },
          metrics: {}
        });
      }
    }

    return errors;
  }

  /**
   * Resolve anchor references
   */
  private resolveReferences(config: ConfigObject): ConfigObject {
    const resolved = JSON.parse(JSON.stringify(config)) as ConfigObject;

    const traverse = (obj: unknown, path: string = ''): void => {
      if (!obj || typeof obj !== 'object') {
        return;
      }

      const record = obj as Record<string, unknown>;

      // Resolve $ref
      if (record.$ref) {
        const anchor = this.anchorDefinitions.get(record.$ref as string);
        if (anchor) {
          Object.assign(record, { value: anchor.value });
          delete record.$ref;
        }
      }

      // Remove $anchor markers
      if (record.$anchor) {
        delete record.$anchor;
      }

      // Traverse nested objects
      for (const key in record) {
        traverse(record[key], path ? `${path}.${key}` : key);
      }
    };

    traverse(resolved);
    return resolved;
  }

  /**
   * Initialize default semantic anchors
   */
  private initializeDefaultAnchors(): void {
    // Default anchor definitions can be added here
  }

  /**
   * Register custom anchor
   */
  registerAnchor(name: string, value: unknown): void {
    this.anchorDefinitions.set(name, {
      name,
      path: 'registered',
      value
    });
  }

  /**
   * Get anchor usages
   */
  getAnchorUsages(): Map<string, string[]> {
    return this.anchorUsages;
  }

  /**
   * Get evidence records
   */
  getEvidence(): EvidenceRecord[] {
    return this.evidence;
  }
}