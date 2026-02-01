# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: anti-fabric-pattern-breaker
# @GL-charter-version: 2.0.0

/**
 * Anti-Fabric: Pattern Breaker
 * 
 * Core Philosophy: "推翻 GL 所有的結論，直到剩下的部分是真正站得住的。"
 * (Overturn all GL conclusions until only what truly stands remains.)
 * 
 * Purpose: Detect violations of established patterns and conventions
 * 
 * This module actively searches for:
 * - Inconsistent coding patterns
 * - Broken architectural patterns
 * - Violated design principles
 * - Anti-patterns in code
 * - Pattern drift across components
 */

import { 
  PatternBreakResult,
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class PatternBreaker {
  private findings: VerificationFinding[] = [];
  private establishedPatterns: Map<string, string[]> = new Map();

  /**
   * Detect pattern breaks in a component
   */
  async detectPatternBreaks(component: string): Promise<PatternBreakResult> {
    this.findings = [];
    
    // Build pattern database first
    await this.buildPatternDatabase(component);
    
    // Scan component for pattern breaks
    await this.scanComponent(component);
    
    return {
      patternBroken: this.findings.length > 0,
      breaks: this.extractBreaks()
    };
  }

  /**
   * Build pattern database from component files
   */
  private async buildPatternDatabase(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Extract naming patterns
      this.extractNamingPatterns(file, content);
      
      // Extract structural patterns
      this.extractStructuralPatterns(file, content);
      
      // Extract architectural patterns
      this.extractArchitecturalPatterns(file, content);
    }
  }

  /**
   * Extract naming patterns
   */
  private extractNamingPatterns(file: string, content: string): void {
    // Class naming patterns
    const classMatches = content.matchAll(/class\s+(\w+)/g);
    for (const match of classMatches) {
      const className = match[1];
      const pattern = this.inferNamingPattern(className);
      
      if (!this.establishedPatterns.has('class-naming')) {
        this.establishedPatterns.set('class-naming', []);
      }
      this.establishedPatterns.get('class-naming')!.push(pattern);
    }
    
    // Function naming patterns
    const funcMatches = content.matchAll(/(?:function|const\s+\w+\s*=\s*)\s*(\w+)/g);
    for (const match of funcMatches) {
      const funcName = match[1];
      const pattern = this.inferNamingPattern(funcName);
      
      if (!this.establishedPatterns.has('function-naming')) {
        this.establishedPatterns.set('function-naming', []);
      }
      this.establishedPatterns.get('function-naming')!.push(pattern);
    }
    
    // Variable naming patterns
    const varMatches = content.matchAll(/(?:const|let|var)\s+(\w+)\s*=/g);
    for (const match of varMatches) {
      const varName = match[1];
      const pattern = this.inferNamingPattern(varName);
      
      if (!this.establishedPatterns.has('variable-naming')) {
        this.establishedPatterns.set('variable-naming', []);
      }
      this.establishedPatterns.get('variable-naming')!.push(pattern);
    }
  }

  /**
   * Extract structural patterns
   */
  private extractStructuralPatterns(file: string, content: string): void {
    // Import patterns
    const importMatches = content.matchAll(/import\s+.*from\s+['"]([^'"]+)['"]/g);
    for (const match of importMatches) {
      const importPath = match[1];
      
      if (!this.establishedPatterns.has('import-style')) {
        this.establishedPatterns.set('import-style', []);
      }
      this.establishedPatterns.get('import-style')!.push(importPath);
    }
    
    // Export patterns
    const exportMatches = content.matchAll(/export\s+(?:default\s+)?(?:class|function|const|interface)\s+(\w+)/g);
    for (const match of exportMatches) {
      const exportName = match[1];
      
      if (!this.establishedPatterns.has('export-style')) {
        this.establishedPatterns.set('export-style', []);
      }
      this.establishedPatterns.get('export-style')!.push(exportName);
    }
  }

  /**
   * Extract architectural patterns
   */
  private extractArchitecturalPatterns(file: string, content: string): void {
    // Service patterns
    if (file.includes('/services/') || file.includes('-service')) {
      if (!this.establishedPatterns.has('service-pattern')) {
        this.establishedPatterns.set('service-pattern', []);
      }
      this.establishedPatterns.get('service-pattern')!.push(file);
    }
    
    // Controller patterns
    if (file.includes('/controllers/') || file.includes('-controller')) {
      if (!this.establishedPatterns.has('controller-pattern')) {
        this.establishedPatterns.set('controller-pattern', []);
      }
      this.establishedPatterns.get('controller-pattern')!.push(file);
    }
    
    // Model patterns
    if (file.includes('/models/') || file.includes('-model')) {
      if (!this.establishedPatterns.has('model-pattern')) {
        this.establishedPatterns.set('model-pattern', []);
      }
      this.establishedPatterns.get('model-pattern')!.push(file);
    }
  }

  /**
   * Scan component for pattern breaks
   */
  private async scanComponent(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // 1. Detect naming pattern violations
      await this.detectNamingPatternViolations(file, content);
      
      // 2. Detect structural pattern violations
      await this.detectStructuralPatternViolations(file, content);
      
      // 3. Detect architectural pattern violations
      await this.detectArchitecturalPatternViolations(file, content);
      
      // 4. Detect anti-patterns
      await this.detectAntiPatterns(file, content);
    }
  }

  /**
   * Detect naming pattern violations
   */
  private async detectNamingPatternViolations(file: string, content: string): Promise<void> {
    // Check class naming
    const classMatches = content.matchAll(/class\s+(\w+)/g);
    for (const match of classMatches) {
      const className = match[1];
      const pattern = this.inferNamingPattern(className);
      
      const classPatterns = this.establishedPatterns.get('class-naming') || [];
      const dominantPattern = this.findDominantPattern(classPatterns);
      
      if (dominantPattern && pattern !== dominantPattern) {
        this.findings.push({
          id: this.generateId(),
          type: 'PATTERN_BREAK',
          severity: VerificationSeverity.MEDIUM,
          component: file,
          location: {
            file,
            line: this.getLineNumber(content, match.index!),
            module: file
          },
          title: 'Naming Pattern Violation',
          description: `Class '${className}' follows pattern '${pattern}' but dominant pattern is '${dominantPattern}'`,
          evidence: [{
            type: 'code',
            source: file,
            content: match[0],
            timestamp: new Date(),
            verified: true
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
  }

  /**
   * Detect structural pattern violations
   */
  private async detectStructuralPatternViolations(file: string, content: string): Promise<void> {
    // Check import ordering
    const importLines: Array<{ line: number; content: string }> = [];
    const importMatches = content.matchAll(/^import\s+.*$/gm);
    
    for (const match of importMatches) {
      importLines.push({
        line: this.getLineNumber(content, match.index!),
        content: match[0]
      });
    }
    
    // Check if imports are properly grouped
    if (importLines.length > 1) {
      const groups = this.groupImports(importLines);
      
      if (groups.length > 1 && this.importsOutOfOrder(groups)) {
        this.findings.push({
          id: this.generateId(),
          type: 'PATTERN_BREAK',
          severity: VerificationSeverity.LOW,
          component: file,
          location: {
            file,
            line: importLines[0].line,
            module: file
          },
          title: 'Import Pattern Violation',
          description: 'Imports are not properly grouped or ordered',
          evidence: importLines.map(line => ({
            type: 'code' as const,
            source: file,
            content: line.content,
            timestamp: new Date(),
            verified: true
          })),
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
  }

  /**
   * Detect architectural pattern violations
   */
  private async detectArchitecturalPatternViolations(file: string, content: string): Promise<void> {
    // Check service pattern compliance
    if (file.includes('/services/') || file.includes('-service')) {
      // Services should have specific structure
      const hasMethod = /async\s+\w+\s*\(/.test(content);
      
      if (!hasMethod) {
        this.findings.push({
          id: this.generateId(),
          type: 'PATTERN_BREAK',
          severity: VerificationSeverity.MEDIUM,
          component: file,
          location: {
            file,
            module: file
          },
          title: 'Service Pattern Violation',
          description: 'Service file should contain async methods',
          evidence: [{
            type: 'code',
            source: file,
            content: content.substring(0, 500),
            timestamp: new Date(),
            verified: true
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
    
    // Check controller pattern compliance
    if (file.includes('/controllers/') || file.includes('-controller')) {
      // Controllers should handle requests
      const hasRequestHandler = /req|request|ctx|context/.test(content);
      
      if (!hasRequestHandler) {
        this.findings.push({
          id: this.generateId(),
          type: 'PATTERN_BREAK',
          severity: VerificationSeverity.MEDIUM,
          component: file,
          location: {
            file,
            module: file
          },
          title: 'Controller Pattern Violation',
          description: 'Controller file should handle request/response',
          evidence: [{
            type: 'code',
            source: file,
            content: content.substring(0, 500),
            timestamp: new Date(),
            verified: true
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
  }

  /**
   * Detect anti-patterns
   */
  private async detectAntiPatterns(file: string, content: string): Promise<void> {
    // God object anti-pattern
    const lineCount = content.split('\n').length;
    const classMatches = content.matchAll(/class\s+(\w+)\s*{([^}]*(?:{[^}]*}[^}]*)*)}/gs);
    
    for (const match of classMatches) {
      const className = match[1];
      const classBody = match[2];
      const methodCount = (classBody.match(/\w+\s*\([^)]*\)\s*{/g) || []).length;
      
      if (methodCount > 15) {
        this.findings.push({
          id: this.generateId(),
          type: 'PATTERN_BREAK',
          severity: VerificationSeverity.HIGH,
          component: file,
          location: {
            file,
            line: this.getLineNumber(content, match.index!),
            module: file
          },
          title: 'God Object Anti-Pattern Detected',
          description: `Class '${className}' has ${methodCount} methods (threshold: 15)`,
          evidence: [{
            type: 'code',
            source: file,
            content: `class ${className} { ... } // ${methodCount} methods`,
            timestamp: new Date(),
            verified: true
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
    
    // Magic number anti-pattern
    const magicNumberMatches = content.matchAll(/(?<![\w])(\d{2,})(?![\d])/g);
    for (const match of magicNumberMatches) {
      const number = match[1];
      
      // Skip common constants
      if (!['100', '1000', '3600', '86400'].includes(number)) {
        this.findings.push({
          id: this.generateId(),
          type: 'PATTERN_BREAK',
          severity: VerificationSeverity.LOW,
          component: file,
          location: {
            file,
            line: this.getLineNumber(content, match.index!),
            module: file
          },
          title: 'Magic Number Anti-Pattern Detected',
          description: `Magic number '${number}' found - consider using a named constant`,
          evidence: [{
            type: 'code',
            source: file,
            content: match[0],
            timestamp: new Date(),
            verified: true
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
    
    // Deep nesting anti-pattern
    const lines = content.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const indentMatch = line.match(/^(\s*)/);
      if (indentMatch) {
        const indent = indentMatch[1].length;
        if (indent > 24) { // More than 6 levels of indentation
          this.findings.push({
            id: this.generateId(),
            type: 'PATTERN_BREAK',
            severity: VerificationSeverity.MEDIUM,
            component: file,
            location: {
              file,
              line: i + 1,
              module: file
            },
            title: 'Deep Nesting Anti-Pattern Detected',
            description: `Deep nesting detected at line ${i + 1} (${indent} spaces)`,
            evidence: [{
              type: 'code',
              source: file,
              content: line.trim(),
              timestamp: new Date(),
              verified: true
            }],
            timestamp: new Date(),
            verified: false,
            falsifiable: true
          });
        }
      }
    }
  }

  /**
   * Extract pattern breaks from findings
   */
  private extractBreaks() {
    return this.findings.map(finding => ({
      pattern: finding.type,
      violation: finding.description,
      location: `${finding.location.file}:${finding.location.line}`,
      justification: finding.title
    }));
  }

  // ============================================================================
  // Helper Methods
  // ============================================================================

  private getComponentPath(component: string): string {
    return `/workspace/gl-runtime-platform/${component}`;
  }

  private async getTsFiles(path: string): Promise<string[]> {
    const { exec } = require('child_process');
    return new Promise((resolve, reject) => {
      exec(`find ${path} -type f -name "*.ts"`, (error, stdout) => {
        if (error) reject(error);
        else resolve(stdout.trim().split('\n').filter(f => f));
      });
    });
  }

  private async readFileContent(filePath: string): Promise<string> {
    const fs = require('fs').promises;
    return fs.readFile(filePath, 'utf-8');
  }

  private getLineNumber(content: string, index: number): number {
    return content.substring(0, index).split('\n').length;
  }

  private generateId(): string {
    return `pattern-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private inferNamingPattern(name: string): string {
    // PascalCase
    if (/^[A-Z][a-zA-Z0-9]*$/.test(name)) {
      return 'PascalCase';
    }
    // camelCase
    if (/^[a-z][a-zA-Z0-9]*$/.test(name)) {
      return 'camelCase';
    }
    // kebab-case
    if (/^[a-z][a-z0-9-]*$/.test(name)) {
      return 'kebab-case';
    }
    // snake_case
    if (/^[a-z][a-z0-9_]*$/.test(name)) {
      return 'snake_case';
    }
    // UPPER_CASE
    if (/^[A-Z][A-Z0-9_]*$/.test(name)) {
      return 'UPPER_CASE';
    }
    
    return 'unknown';
  }

  private findDominantPattern(patterns: string[]): string | null {
    if (patterns.length === 0) return null;
    
    const counts = new Map<string, number>();
    for (const pattern of patterns) {
      counts.set(pattern, (counts.get(pattern) || 0) + 1);
    }
    
    let maxCount = 0;
    let dominantPattern = '';
    
    for (const [pattern, count] of counts) {
      if (count > maxCount) {
        maxCount = count;
        dominantPattern = pattern;
      }
    }
    
    return maxCount > patterns.length / 2 ? dominantPattern : null;
  }

  private groupImports(importLines: Array<{ line: number; content: string }>): string[][] {
    const groups: string[][] = [];
    let currentGroup: string[] = [];
    
    for (const line of importLines) {
      if (currentGroup.length === 0) {
        currentGroup.push(line.content);
      } else {
        const prevLine = currentGroup[currentGroup.length - 1];
        const gap = line.line - this.getLineNumberFromContent(prevLine, importLines) - 1;
        
        if (gap > 1) {
          groups.push(currentGroup);
          currentGroup = [line.content];
        } else {
          currentGroup.push(line.content);
        }
      }
    }
    
    if (currentGroup.length > 0) {
      groups.push(currentGroup);
    }
    
    return groups;
  }

  private importsOutOfOrder(groups: string[][]): boolean {
    // Simplified check - in reality, would check for proper ordering
    // (external -> internal -> relative)
    return groups.length > 1;
  }

  private getLineNumberFromContent(content: string, importLines: Array<{ line: number; content: string }>): number {
    const match = importLines.find(line => line.content === content);
    return match?.line || 0;
  }
}