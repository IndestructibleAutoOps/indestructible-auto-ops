/**
 * @module fs_loader
 * @description File system configuration loader
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

import * as fs from 'fs';
import * as path from 'path';
import { LoaderInterface, LoadResult, EvidenceRecord } from '../interfaces.d';

/**
 * File System Loader
 * 
 * GL30-49: Execution Layer - Loader Stage
 * 
 * Recursively loads YAML/JSON files from the file system,
 * maintaining directory structure and generating evidence chains.
 */
export class FsLoader implements LoaderInterface {
  private evidence: EvidenceRecord[] = [];
  private readonly baseDir: string;
  private readonly ignorePatterns: string[];

  constructor(baseDir: string, options?: { ignore?: string[] }) {
    this.baseDir = path.resolve(baseDir);
    this.ignorePatterns = options?.ignore || [
      'node_modules',
      '.git',
      '.DS_Store',
      '*.log'
    ];
  }

  /**
   * Load all DSL files from the file system
   */
  async load(): Promise<LoadResult> {
    const startTime = Date.now();
    const files: Map<string, any> = new Map();
    const errors: string[] = [];

    try {
      // Validate base directory exists
      if (!fs.existsSync(this.baseDir)) {
        throw new Error(`Base directory does not exist: ${this.baseDir}`);
      }

      // Recursively load files
      await this.loadDirectory(this.baseDir, '', files, errors);

      // Generate evidence record
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'loader',
        component: 'fs_loader',
        action: 'load',
        status: errors.length > 0 ? 'warning' : 'success',
        input: { baseDir: this.baseDir },
        output: { fileCount: files.size, errorCount: errors.length },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        status: errors.length > 0 ? 'warning' : 'success',
        files,
        errors,
        evidence: this.evidence
      };
    } catch (error) {
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'loader',
        component: 'fs_loader',
        action: 'load',
        status: 'error',
        input: { baseDir: this.baseDir },
        output: { error: error instanceof Error ? error.message : String(error) },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        status: 'error',
        files,
        errors: [error instanceof Error ? error.message : String(error)],
        evidence: this.evidence
      };
    }
  }

  /**
   * Recursively load directory contents
   */
  private async loadDirectory(
    dirPath: string,
    relativePath: string,
    files: Map<string, any>,
    errors: string[]
  ): Promise<void> {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dirPath, entry.name);
      const relPath = path.join(relativePath, entry.name);

      // Skip ignored patterns
      if (this.shouldIgnore(entry.name)) {
        continue;
      }

      if (entry.isDirectory()) {
        // Recursively process subdirectories
        await this.loadDirectory(fullPath, relPath, files, errors);
      } else if (entry.isFile()) {
        // Load file content
        try {
          await this.loadFile(fullPath, relPath, files);
        } catch (error) {
          errors.push(
            `Failed to load ${relPath}: ${error instanceof Error ? error.message : String(error)}`
          );
        }
      }
    }
  }

  /**
   * Load single file content
   */
  private async loadFile(
    fullPath: string,
    relativePath: string,
    files: Map<string, any>
  ): Promise<void> {
    const ext = path.extname(fullPath).toLowerCase();

    // Only load YAML/JSON files
    if (
!['.yaml', '.yml', '.json'].includes(ext)
) {
      return;
    }

    const content = fs.readFileSync(fullPath, 'utf-8');
    
    files.set(relativePath, {
      path: relativePath,
      fullPath,
      content,
      type: ext,
      size: content.length,
      hash: this.generateHash(content),
      modified: fs.statSync(fullPath).mtime.toISOString()
    });

    // Record evidence for each file
    this.evidence.push({
      timestamp: new Date().toISOString(),
      stage: 'loader',
      component: 'fs_loader',
      action: 'load_file',
      status: 'success',
      input: { path: relativePath },
      output: { size: content.length, type: ext },
      metrics: {}
    });
  }

  /**
   * Check if file/directory should be ignored
   */
  private shouldIgnore(name: string): boolean {
    return this.ignorePatterns.some(pattern => {
      if (pattern.includes('*')) {
        const regex = new RegExp(pattern.replace(/\*/g, '.*'));
        return regex.test(name);
      }
      return name === pattern;
    });
  }

  /**
   * Generate SHA256 hash for content integrity
   */
  private generateHash(content: string): string {
    const crypto = require('crypto');
    return crypto.createHash('sha256').update(content).digest('hex');
  }

  /**
   * Get evidence records
   */
  getEvidence(): EvidenceRecord[] {
    return this.evidence;
  }
}