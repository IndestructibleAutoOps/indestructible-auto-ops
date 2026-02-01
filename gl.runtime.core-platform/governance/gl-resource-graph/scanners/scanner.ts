// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: resource-graph-scanner
// @GL-charter-version: 2.0.0

import fs from 'fs/promises';
import path from 'path';
import { createLogger } from '../../src/utils/logger';

const logger = createLogger('ResourceGraphScanner');

export interface FileScanResult {
  path: string;
  type: string;
  language: string;
  format: string;
  size: number;
  lastModified: string;
  hasGovernanceTags: boolean;
  hasSemanticAnchor: boolean;
  hasCharterVersion: boolean;
}

export class ResourceGraphScanner {
  private scanResults: Map<string, FileScanResult> = new Map();

  public async scanRepository(rootPath: string): Promise<FileScanResult[]> {
    logger.info(`Starting repository scan: ${rootPath}`);
    
    const files = await this.getAllFiles(rootPath);
    const results: FileScanResult[] = [];

    for (const file of files) {
      const result = await this.scanFile(file);
      results.push(result);
      this.scanResults.set(file, result);
    }

    logger.info(`Scanned ${results.length} files`);
    return results;
  }

  private async getAllFiles(dir: string): Promise<string[]> {
    const files: string[] = [];
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      // Skip node_modules, .git, dist, build
      if (['node_modules', '.git', 'dist', 'build'].includes(entry.name)) {
        continue;
      }

      if (entry.isDirectory()) {
        const subFiles = await this.getAllFiles(fullPath);
        files.push(...subFiles);
      } else {
        files.push(fullPath);
      }
    }

    return files;
  }

  private async scanFile(filePath: string): Promise<FileScanResult> {
    try {
      const stats = await fs.stat(filePath);
      const content = await fs.readFile(filePath, 'utf-8');
      const ext = path.extname(filePath);
      
      const result: FileScanResult = {
        path: filePath,
        type: this.detectFileType(filePath),
        language: this.detectLanguage(filePath),
        format: this.detectFormat(ext),
        size: stats.size,
        lastModified: stats.mtime.toISOString(),
        hasGovernanceTags: content.includes('@GL-governed'),
        hasSemanticAnchor: content.includes('@GL-semantic'),
        hasCharterVersion: content.includes('@GL-charter-version')
      };

      return result;
    } catch (error: any) {
      logger.error(`Failed to scan file ${filePath}: ${error.message}`);
      
      return {
        path: filePath,
        type: 'unknown',
        language: 'unknown',
        format: 'unknown',
        size: 0,
        lastModified: new Date().toISOString(),
        hasGovernanceTags: false,
        hasSemanticAnchor: false,
        hasCharterVersion: false
      };
    }
  }

  private detectFileType(filePath: string): string {
    const ext = path.extname(filePath);
    const fileTypes: Record<string, string> = {
      '.ts': 'typescript',
      '.js': 'javascript',
      '.py': 'python',
      '.java': 'java',
      '.yaml': 'yaml',
      '.yml': 'yaml',
      '.json': 'json',
      '.md': 'markdown',
      '.txt': 'text',
      '.sh': 'shell'
    };
    
    return fileTypes[ext] || 'unknown';
  }

  private detectLanguage(filePath: string): string {
    const ext = path.extname(filePath);
    const languages: Record<string, string> = {
      '.ts': 'typescript',
      '.js': 'javascript',
      '.py': 'python',
      '.java': 'java',
      '.go': 'go',
      '.rs': 'rust',
      '.cpp': 'cpp',
      '.c': 'c',
      '.h': 'c'
    };
    
    return languages[ext] || 'none';
  }

  private detectFormat(ext: string): string {
    const formats: Record<string, string> = {
      '.yaml': 'yaml',
      '.yml': 'yaml',
      '.json': 'json',
      '.xml': 'xml',
      '.toml': 'toml',
      '.md': 'markdown',
      '.txt': 'text'
    };
    
    return formats[ext] || 'binary';
  }

  public getScanResults(): Map<string, FileScanResult> {
    return this.scanResults;
  }

  public getFilesByType(type: string): FileScanResult[] {
    return Array.from(this.scanResults.values()).filter(f => f.type === type);
  }

  public getFilesByLanguage(language: string): FileScanResult[] {
    return Array.from(this.scanResults.values()).filter(f => f.language === language);
  }

  public getFilesWithoutGovernanceTags(): FileScanResult[] {
    return Array.from(this.scanResults.values()).filter(f => !f.hasGovernanceTags);
  }
}