# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: anti-fabric-semantic-inconsistency-scanner
# @GL-charter-version: 2.0.0

/**
 * Anti-Fabric: Semantic Inconsistency Scanner
 * 
 * Core Philosophy: "驗證不是證明你是對的，而是證明你還沒被推翻。"
 * (Verification is not proving you're right, but proving you haven't been overturned yet.)
 * 
 * Purpose: Detect semantic inconsistencies within GL components
 * 
 * This module actively searches for:
 * - Naming vs implementation mismatches
 * - Type vs usage inconsistencies
 * - Documentation vs code divergences
 * - API contract violations
 * - Semantic drift across components
 */

import { 
  SemanticInconsistencyResult,
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class SemanticInconsistencyScanner {
  private findings: VerificationFinding[] = [];

  /**
   * Detect semantic inconsistencies in a component
   */
  async detectSemanticInconsistencies(component: string): Promise<SemanticInconsistencyResult> {
    this.findings = [];
    
    // Scan component for semantic inconsistencies
    await this.scanComponent(component);
    
    return {
      inconsistent: this.findings.length > 0,
      inconsistencies: this.extractInconsistencies()
    };
  }

  /**
   * Scan component for various semantic inconsistency patterns
   */
  private async scanComponent(component: string): Promise<void> {
    // 1. Detect naming vs implementation mismatches
    await this.detectNamingImplementationMismatches(component);
    
    // 2. Detect type vs usage inconsistencies
    await this.detectTypeUsageInconsistencies(component);
    
    // 3. Detect documentation vs code divergences
    await this.detectDocumentationCodeDivergences(component);
    
    // 4. Detect API contract violations
    await this.detectApiContractViolations(component);
    
    // 5. Detect semantic drift across files
    await this.detectSemanticDrift(component);
  }

  /**
   * Detect naming vs implementation mismatches
   */
  private async detectNamingImplementationMismatches(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Detect function name mismatches
      const functionMatches = content.matchAll(
        /(?:function|const\s+\w+\s*=\s*|(?:async\s+)?\w+)\s*(\w+)\s*\(([^)]*)\)\s*{([^}]+)}/gs
      );
      
      for (const match of functionMatches) {
        const functionName = match[1];
        const params = match[2];
        const implementation = match[3];
        const line = this.getLineNumber(content, match.index!);
        
        // Check for naming vs implementation contradictions
        if (this.hasNamingImplementationMismatch(functionName, implementation)) {
          const expectedSemantics = this.inferExpectedSemantics(functionName);
          const actualSemantics = this.inferActualSemantics(implementation);
          
          this.findings.push({
            id: this.generateId(),
            type: 'SEMANTIC_MISMATCH',
            severity: VerificationSeverity.MEDIUM,
            component,
            location: {
              file,
              line,
              module: component
            },
            title: 'Naming vs Implementation Mismatch',
            description: `Function '${functionName}' name suggests '${expectedSemantics}' but implementation does '${actualSemantics}'`,
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
  }

  /**
   * Detect type vs usage inconsistencies
   */
  private async detectTypeUsageInconsistencies(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Detect type annotations vs actual usage
      const typeMatches = content.matchAll(
        /(\w+)\s*:\s*([A-Z]\w+)\s*=/gs
      );
      
      for (const match of typeMatches) {
        const variableName = match[1];
        const declaredType = match[2];
        const assignment = content.substring(match.index! + match[0].length);
        
        // Check for type vs actual value mismatch
        if (this.hasTypeUsageMismatch(declaredType, assignment)) {
          this.findings.push({
            id: this.generateId(),
            type: 'INCONSISTENCY',
            severity: VerificationSeverity.HIGH,
            component,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Type vs Usage Inconsistency',
            description: `Variable '${variableName}' declared as '${declaredType}' but assigned incompatible value`,
            evidence: [{
              type: 'code',
              source: file,
              content: match[0] + assignment.substring(0, 100),
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
   * Detect documentation vs code divergences
   */
  private async detectDocumentationCodeDivergences(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Detect JSDoc comments
      const jsdocMatches = content.matchAll(
        /\/\*\*[\s\S]*?\*\/\s*(?:function|const\s+\w+\s*=\s*|(?:async\s+)?\w+)\s*(\w+)/gs
      );
      
      for (const match of jsdocMatches) {
        const jsdoc = match[0];
        const functionName = match[1];
        
        // Extract documented behavior
        const documentedBehavior = this.extractDocumentedBehavior(jsdoc);
        
        // Extract actual implementation
        const implementationMatch = content.match(
          new RegExp(`${functionName}\\s*\\([^)]*\\)\\s*{([^}]+)}`, 's')
        );
        
        if (implementationMatch) {
          const actualBehavior = this.extractActualBehavior(implementationMatch[1]);
          
          if (this.documentationDiverges(documentedBehavior, actualBehavior)) {
            const line = this.getLineNumber(content, match.index!);
            
            this.findings.push({
              id: this.generateId(),
              type: 'INCONSISTENCY',
              severity: VerificationSeverity.MEDIUM,
              component,
              location: {
                file,
                line,
                module: component
              },
              title: 'Documentation vs Code Divergence',
              description: `Function '${functionName}' documentation says '${documentedBehavior}' but code does '${actualBehavior}'`,
              evidence: [
                {
                  type: 'code',
                  source: file,
                  content: jsdoc + '\n' + implementationMatch[0],
                  timestamp: new Date(),
                  verified: true
                }
              ],
              timestamp: new Date(),
              verified: false,
              falsifiable: true
            });
          }
        }
      }
    }
  }

  /**
   * Detect API contract violations
   */
  private async detectApiContractViolations(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Detect interface definitions
      const interfaceMatches = content.matchAll(
        /interface\s+(\w+)\s*{([^}]+)}/gs
      );
      
      for (const match of interfaceMatches) {
        const interfaceName = match[1];
        const interfaceBody = match[2];
        
        // Find implementations of this interface
        const implMatches = content.matchAll(
          new RegExp(`class\\s+(\\w+)\\s+(?:implements\\s+)?${interfaceName}\\s*?\\{`, 'g')
        );
        
        for (const implMatch of implMatches) {
          const className = implMatch[1];
          const classMatch = content.match(
            new RegExp(`class\\s+${className}\\s*?\\{([^}]+)}`, 's')
          );
          
          if (classMatch) {
            const classBody = classMatch[1];
            
            // Check for contract violations
            const violations = this.detectContractViolations(interfaceName, interfaceBody, className, classBody);
            
            for (const violation of violations) {
              this.findings.push({
                id: this.generateId(),
                type: 'INCONSISTENCY',
                severity: VerificationSeverity.HIGH,
                component,
                location: {
                  file,
                  line: this.getLineNumber(content, implMatch.index!),
                  module: component
                },
                title: 'API Contract Violation',
                description: violation,
                evidence: [
                  {
                    type: 'code',
                    source: file,
                    content: match[0] + '\n' + classMatch[0],
                    timestamp: new Date(),
                    verified: true
                  }
                ],
                timestamp: new Date(),
                verified: false,
                falsifiable: true
              });
            }
          }
        }
      }
    }
  }

  /**
   * Detect semantic drift across files
   */
  private async detectSemanticDrift(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    // Build semantic map of functions
    const semanticMap = new Map<string, Array<{ file: string; semantics: string }>>();

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      const functionMatches = content.matchAll(
        /(?:function|const\s+\w+\s*=\s*|(?:async\s+)?\w+)\s*(\w+)\s*\([^)]*\)\s*{([^}]+)}/gs
      );
      
      for (const match of functionMatches) {
        const functionName = match[1];
        const implementation = match[2];
        const semantics = this.inferActualSemantics(implementation);
        
        if (!semanticMap.has(functionName)) {
          semanticMap.set(functionName, []);
        }
        semanticMap.get(functionName)!.push({ file, semantics });
      }
    }

    // Check for semantic drift
    for (const [functionName, implementations] of semanticMap) {
      if (implementations.length > 1) {
        const uniqueSemantics = new Set(implementations.map(imp => imp.semantics));
        
        if (uniqueSemantics.size > 1) {
          this.findings.push({
            id: this.generateId(),
            type: 'SEMANTIC_MISMATCH',
            severity: VerificationSeverity.MEDIUM,
            component,
            location: {
              module: component
            },
            title: 'Semantic Drift Detected',
            description: `Function '${functionName}' has inconsistent semantics across ${implementations.length} implementations`,
            evidence: implementations.map(imp => ({
              type: 'code' as const,
              source: imp.file,
              content: imp.semantics,
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
  }

  /**
   * Extract inconsistencies from findings
   */
  private extractInconsistencies() {
    return this.findings.map(finding => ({
      element: finding.location.file + ':' + finding.location.line,
      expectedSemantics: finding.evidence[0]?.content || '',
      actualSemantics: finding.evidence[1]?.content || finding.evidence[0]?.content || '',
      divergence: finding.description,
      severity: finding.severity
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
    return `semantic-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private hasNamingImplementationMismatch(name: string, implementation: string): boolean {
    // Check for naming vs implementation contradictions
    const negativeKeywords = ['not', 'never', 'fail', 'error', 'invalid'];
    const positiveKeywords = ['success', 'valid', 'pass', 'ok', 'true'];
    
    const nameLower = name.toLowerCase();
    const implLower = implementation.toLowerCase();
    
    // Name says "validate" but implementation doesn't check
    if (nameLower.includes('validate') && !implLower.includes('if') && !implLower.includes('check')) {
      return true;
    }
    
    // Name says "compute" but implementation returns constant
    if (nameLower.includes('compute') || nameLower.includes('calculate')) {
      if (implLower.includes('return ') && !implLower.includes('+') && !implLower.includes('-') && !implLower.includes('*') && !implLower.includes('/')) {
        return true;
      }
    }
    
    return false;
  }

  private inferExpectedSemantics(name: string): string {
    if (name.includes('validate')) return 'validation logic';
    if (name.includes('compute') || name.includes('calculate')) return 'computation';
    if (name.includes('check')) return 'checking logic';
    if (name.includes('get') || name.includes('fetch')) return 'data retrieval';
    if (name.includes('set') || name.includes('update')) return 'data modification';
    if (name.includes('create') || name.includes('add')) return 'creation';
    if (name.includes('delete') || name.includes('remove')) return 'deletion';
    return name;
  }

  private inferActualSemantics(implementation: string): string {
    const implLower = implementation.toLowerCase();
    
    if (implLower.includes('if') || implLower.includes('check')) return 'conditional check';
    if (implLower.includes('return')) return 'value return';
    if (implLower.includes('throw') || implLower.includes('error')) return 'error handling';
    if (implLower.includes('console.log')) return 'logging';
    if (implLower.includes('await') || implLower.includes('promise')) return 'async operation';
    
    return 'implementation';
  }

  private hasTypeUsageMismatch(declaredType: string, assignment: string): boolean {
    const typeToValuePattern: Record<string, RegExp> = {
      'String': /^['"`]/,
      'Number': /^\d/,
      'Boolean': /^(true|false)/,
      'Array': /^\[/,
      'Object': /^{/
    };
    
    const pattern = typeToValuePattern[declaredType];
    if (pattern) {
      return !pattern.test(assignment.trim());
    }
    
    return false;
  }

  private extractDocumentedBehavior(jsdoc: string): string {
    // Extract @description or first paragraph
    const descMatch = jsdoc.match(/@description\s+([^\n]+)/);
    if (descMatch) return descMatch[1].trim();
    
    const firstLineMatch = jsdoc.match(/\*\s+([^\n@]+)/);
    if (firstLineMatch) return firstLineMatch[1].trim();
    
    return 'undocumented';
  }

  private extractActualBehavior(implementation: string): string {
    return this.inferActualSemantics(implementation);
  }

  private documentationDiverges(documented: string, actual: string): boolean {
    return documented !== actual && documented !== 'undocumented';
  }

  private detectContractViolations(
    interfaceName: string,
    interfaceBody: string,
    className: string,
    classBody: string
  ): string[] {
    const violations: string[] = [];
    
    // Extract interface properties and methods
    const interfaceMembers = this.extractMembers(interfaceBody);
    const classMembers = this.extractMembers(classBody);
    
    // Check for missing members
    for (const [name, type] of interfaceMembers) {
      if (!classMembers.has(name)) {
        violations.push(`Class '${className}' missing member '${name}' from interface '${interfaceName}'`);
      }
    }
    
    // Check for type mismatches
    for (const [name, implType] of classMembers) {
      const interfaceType = interfaceMembers.get(name);
      if (interfaceType && interfaceType !== implType) {
        violations.push(`Class '${className}' member '${name}' has type '${implType}' but interface expects '${interfaceType}'`);
      }
    }
    
    return violations;
  }

  private extractMembers(body: string): Map<string, string> {
    const members = new Map<string, string>();
    
    const propertyMatches = body.matchAll(/(\w+)\s*:\s*([^;]+);/g);
    for (const match of propertyMatches) {
      members.set(match[1], match[2].trim());
    }
    
    return members;
  }
}