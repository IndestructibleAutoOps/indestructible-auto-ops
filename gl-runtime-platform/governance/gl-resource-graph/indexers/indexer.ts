// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: resource-graph-indexer
// @GL-charter-version: 2.0.0

import { FileScanResult } from '../scanners/scanner';
import { createLogger } from '../../src/utils/logger';

const logger = createLogger('ResourceGraphIndexer');

export interface IndexEntry {
  path: string;
  type: string;
  language: string;
  semanticAnchor?: string;
  layer?: string;
  charterVersion?: string;
  dependencies: string[];
  dependents: string[];
}

export class ResourceGraphIndexer {
  private pathIndex: Map<string, IndexEntry> = new Map();
  private typeIndex: Map<string, Set<string>> = new Map();
  private languageIndex: Map<string, Set<string>> = new Map();
  private semanticIndex: Map<string, Set<string>> = new Map();

  public buildIndex(scanResults: FileScanResult[]): void {
    logger.info(`Building index for ${scanResults.length} files`);
    
    for (const result of scanResults) {
      const entry: IndexEntry = {
        path: result.path,
        type: result.type,
        language: result.language,
        dependencies: [],
        dependents: []
      };

      this.pathIndex.set(result.path, entry);
      
      // Build type index
      if (!this.typeIndex.has(result.type)) {
        this.typeIndex.set(result.type, new Set());
      }
      this.typeIndex.get(result.type)!.add(result.path);
      
      // Build language index
      if (!this.languageIndex.has(result.language)) {
        this.languageIndex.set(result.language, new Set());
      }
      this.languageIndex.get(result.language)!.add(result.path);
    }

    // Extract semantic anchors and metadata
    this.extractMetadata(scanResults);
    
    // Build dependency graph
    this.buildDependencyGraph(scanResults);
    
    logger.info(`Index built: ${this.pathIndex.size} entries`);
  }

  private extractMetadata(scanResults: FileScanResult[]): void {
    for (const result of scanResults) {
      if (!result.hasSemanticAnchor) continue;
      
      // Extract semantic anchor (simplified)
      const semanticAnchor = this.extractSemanticAnchor(result.path);
      if (semanticAnchor) {
        const entry = this.pathIndex.get(result.path);
        if (entry) {
          entry.semanticAnchor = semanticAnchor;
          
          if (!this.semanticIndex.has(semanticAnchor)) {
            this.semanticIndex.set(semanticAnchor, new Set());
          }
          this.semanticIndex.get(semanticAnchor)!.add(result.path);
        }
      }
    }
  }

  private extractSemanticAnchor(filePath: string): string | null {
    // Simplified semantic anchor extraction
    // In production, would parse file headers
    const parts = filePath.split('/');
    if (parts.includes('gl-runtime-platform')) {
      return 'GL-ROOT-GOVERNANCE';
    }
    return null;
  }

  private buildDependencyGraph(scanResults: FileScanResult[]): void {
    // Simplified dependency detection
    // In production, would parse import statements, requires, etc.
    for (const result of scanResults) {
      const entry = this.pathIndex.get(result.path);
      if (!entry) continue;

      // Detect TypeScript/JavaScript imports
      if (result.language === 'typescript' || result.language === 'javascript') {
        const imports = this.detectImports(result.path);
        entry.dependencies = imports;
      }

      // Detect Python imports
      if (result.language === 'python') {
        const imports = this.detectPythonImports(result.path);
        entry.dependencies = imports;
      }
    }

    // Build reverse dependencies (dependents)
    for (const entry of this.pathIndex.values()) {
      for (const dep of entry.dependencies) {
        const depEntry = this.pathIndex.get(dep);
        if (depEntry) {
          depEntry.dependents.push(entry.path);
        }
      }
    }
  }

  private detectImports(filePath: string): string[] {
    // Simplified import detection
    // In production, would use AST parsing
    const imports: string[] = [];
    const dir = filePath.substring(0, filePath.lastIndexOf('/'));
    
    // Common import patterns (would be more sophisticated)
    if (filePath.includes('/src/')) {
      imports.push(dir);
    }
    
    return imports;
  }

  private detectPythonImports(filePath: string): string[] {
    // Simplified Python import detection
    const imports: string[] = [];
    const dir = filePath.substring(0, filePath.lastIndexOf('/'));
    
    if (filePath.includes('/src/')) {
      imports.push(dir);
    }
    
    return imports;
  }

  public getByPath(path: string): IndexEntry | undefined {
    return this.pathIndex.get(path);
  }

  public getByType(type: string): IndexEntry[] {
    const paths = this.typeIndex.get(type) || [];
    return Array.from(paths).map(p => this.pathIndex.get(p)!).filter(Boolean);
  }

  public getByLanguage(language: string): IndexEntry[] {
    const paths = this.languageIndex.get(language) || [];
    return Array.from(paths).map(p => this.pathIndex.get(p)!).filter(Boolean);
  }

  public getBySemanticAnchor(semanticAnchor: string): IndexEntry[] {
    const paths = this.semanticIndex.get(semanticAnchor) || [];
    return Array.from(paths).map(p => this.pathIndex.get(p)!).filter(Boolean);
  }

  public getAllDependencies(path: string): string[] {
    const entry = this.pathIndex.get(path);
    return entry?.dependencies || [];
  }

  public getAllDependents(path: string): string[] {
    const entry = this.pathIndex.get(path);
    return entry?.dependents || [];
  }

  public getIndexSize(): number {
    return this.pathIndex.size;
  }
}