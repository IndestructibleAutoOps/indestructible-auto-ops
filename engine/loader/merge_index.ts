/**
 * @module merge_index
 * @description Merge multiple load results with conflict resolution
 * @gl-governed
 * GL Unified Charter Activated
 * @gl-layer GL-30-EXECUTION
 * @gl-module engine/loader
 * @gl-semantic-anchor GL-30-EXEC-TS
 * @gl-evidence-required true
 * @version 1.0.0
 * @since 2026-01-24
 * @author MachineNativeOps Team
 */

import { LoadResult, EvidenceRecord, MergeStrategy } from '../interfaces.d';
import type { ConfigObject, FileEntry, MergeResult } from '../types';

interface FileData {
  path: string;
  fullPath: string;
  content: string;
  type: string;
  size: number;
  hash: string;
  modified: string;
  merged?: boolean;
  sources?: Array<{ hash: string; modified: string }>;
}

/**
 * Merge Index
 * 
 * GL30-49: Execution Layer - Loader Stage
 * 
 * Merges multiple load results into a unified index with
 * conflict resolution strategies. Maintains complete audit trail.
 */
export class MergeIndex {
  private evidence: EvidenceRecord[] = [];
  private readonly mergeStrategy: MergeStrategy;

  constructor(strategy: MergeStrategy = 'error') {
    this.mergeStrategy = strategy;
  }

  /**
   * Merge multiple load results into a unified index
   */
  merge(results: LoadResult[]): LoadResult {
    const startTime = Date.now();
    const mergedFiles: Map<string, ConfigObject> = new Map();
    const allErrors: string[] = [];
    const conflicts: Map<string, FileData[]> = new Map();

    try {
      // Collect all files and detect conflicts
      for (const result of results) {
        // Merge evidence
        this.evidence.push(...result.evidence);
        
        // Collect errors
        allErrors.push(...result.errors);

        // Merge files with conflict detection
        for (const [key, file] of result.files.entries()) {
          if (mergedFiles.has(key)) {
            // Conflict detected
            if (!conflicts.has(key)) {
              conflicts.set(key, [mergedFiles.get(key) as unknown as FileData]);
            }
            conflicts.get(key)!.push(file as unknown as FileData);
          } else {
            mergedFiles.set(key, file);
          }
        }
      }

      // Handle conflicts based on strategy
      const conflictErrors: string[] = [];
      for (const [path, files] of conflicts.entries()) {
        const resolved = this.resolveConflict(path, files);
        
        if (resolved.error) {
          conflictErrors.push(resolved.error);
        } else if (resolved.file) {
          mergedFiles.set(path, resolved.file);
        }
      }

      allErrors.push(...conflictErrors);

      // Generate evidence record
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'loader',
        component: 'merge_index',
        action: 'merge',
        status: conflictErrors.length > 0 ? 
          (this.mergeStrategy === 'error' ? 'error' : 'warning') : 'success',
        input: { resultCount: results.length, strategy: this.mergeStrategy },
        output: {
          fileCount: mergedFiles.size,
          conflictCount: conflicts.size,
          errorCount: allErrors.length
        },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        status: conflictErrors.length > 0 && this.mergeStrategy === 'error' ? 'error' : 
               conflictErrors.length > 0 ? 'warning' : 'success',
        files: mergedFiles,
        errors: allErrors,
        evidence: this.evidence
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'loader',
        component: 'merge_index',
        action: 'merge',
        status: 'error',
        input: { resultCount: results.length },
        output: { error: errorMsg },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        status: 'error',
        files: mergedFiles,
        errors: [errorMsg, ...allErrors],
        evidence: this.evidence
      };
    }
  }

  /**
   * Resolve conflict based on merge strategy
   */
  private resolveConflict(
    path: string,
    files: FileData[]
  ): MergeResult {
    switch (this.mergeStrategy) {
      case 'error':
        return {
          error: `Conflict detected for ${path}: ${files.length} sources with same path. Strategy: error`
        };

      case 'first':
        // Use first file (already in mergedFiles)
        return { file: files[0] as unknown as ConfigObject };

      case 'last':
        // Use last file
        return { file: files[files.length - 1] as unknown as ConfigObject };

      case 'newest':
        // Use file with most recent modification time
        const sorted = [...files].sort((a, b) => 
          new Date(b.modified).getTime() - new Date(a.modified).getTime()
        );
        return { file: sorted[0] as unknown as ConfigObject };

      case 'custom':
        // Custom resolution: merge content if possible
        return this.customMerge(path, files);

      default:
        return {
          error: `Unknown merge strategy: ${this.mergeStrategy}`
        };
    }
  }

  /**
   * Custom merge strategy: attempt to merge YAML/JSON content
   */
  private customMerge(
    path: string,
    files: FileData[]
  ): MergeResult {
    try {
      const yaml = require('js-yaml');
      const merged: Record<string, unknown> = {};

      for (const file of files) {
        let parsed: Record<string, unknown>;
        
        if (file.type === '.json') {
          parsed = JSON.parse(file.content) as Record<string, unknown>;
        } else {
          parsed = yaml.load(file.content) as Record<string, unknown>;
        }

        // Deep merge objects
        this.deepMerge(merged, parsed);
      }

      const yamlOutput = yaml.dump(merged) as string;

      return {
        file: {
          path,
          fullPath: files[0].fullPath,
          content: yamlOutput,
          type: files[0].type,
          size: yamlOutput.length,
          hash: this.generateHash(yamlOutput),
          modified: new Date().toISOString(),
          merged: true,
          sources: files.map(f => ({
            hash: f.hash,
            modified: f.modified
          }))
        } as unknown as ConfigObject
      };
    } catch (error) {
      return {
        error: `Failed to merge ${path}: ${error instanceof Error ? error.message : String(error)}`
      };
    }
  }

  /**
   * Deep merge objects
   */
  private deepMerge(target: Record<string, unknown>, source: Record<string, unknown>): void {
    for (const key in source) {
      // Only merge own properties and prevent prototype pollution
      if (!Object.prototype.hasOwnProperty.call(source, key)) {
        continue;
      }
      if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
        continue;
      }
      // Only recurse if both target[key] and source[key] are non-null objects (not arrays)
      if (
        source[key] instanceof Object &&
        !Array.isArray(source[key]) &&
        key in target &&
        target[key] instanceof Object &&
        !Array.isArray(target[key])
      ) {
        this.deepMerge(
          target[key] as Record<string, unknown>,
          source[key] as Record<string, unknown>
        );
      } else {
        target[key] = source[key];
      }
    }
  }

  /**
   * Generate SHA256 hash
   */
  private generateHash(content: string): string {
    const crypto = require('crypto');
    return crypto.createHash('sha256').update(content).digest('hex') as string;
  }

  /**
   * Get evidence records
   */
  getEvidence(): EvidenceRecord[] {
    return this.evidence;
  }
}