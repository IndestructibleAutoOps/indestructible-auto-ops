# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: falsification-engine-semantic-contradiction-tests
# @GL-charter-version: 2.0.0

/**
 * Falsification Engine: Semantic Contradiction Tests
 * 
 * Core Philosophy: "推翻 GL 所有的結論，直到剩下的部分是真正站得住的。"
 * (Overturn all GL conclusions until only what truly stands remains.)
 * 
 * Purpose: Detect semantic contradictions in GL components
 * 
 * This module actively searches for:
 * - Meaning contradictions
 * - Context contradictions
 * - Purpose contradictions
 * - Intent contradictions
 * - Semantic drift
 */

import { 
  SemanticContradictionTestResult,
  VerificationSeverity,
  VerificationFinding,
  Evidence 
} from '../../types';

export class SemanticContradictionTests {
  private findings: VerificationFinding[] = [];

  /**
   * Test semantic contradictions in a component
   */
  async testSemanticContradictions(component: string): Promise<SemanticContradictionTestResult> {
    this.findings = [];
    
    // Scan component for semantic contradictions
    await this.scanComponent(component);
    
    return {
      contradictionFound: this.findings.length > 0,
      contradictions: this.extractContradictions()
    };
  }

  /**
   * Scan component for semantic contradictions
   */
  private async scanComponent(component: string): Promise<void> {
    // 1. Detect function name vs implementation contradictions
    await this.detectNameImplementationContradictions(component);
    
    // 2. Detect documentation vs implementation contradictions
    await this.detectDocumentationImplementationContradictions(component);
    
    // 3. Detect type vs usage contradictions
    await this.detectTypeUsageContradictions(component);
    
    // 4. Detect interface vs implementation contradictions
    await this.detectInterfaceImplementationContradictions(component);
    
    // 5. Detect promise vs async contradictions
    await this.detectPromiseAsyncContradictions(component);
  }

  /**
   * Detect function name vs implementation contradictions
   */
  private async detectNameImplementationContradictions(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      const functionMatches = content.matchAll(
        /(?:function|const\s+\w+\s*=\s*|(?:async\s+)?\w+)\s*(\w+)\s*\([^)]*\)\s*{([^}]+)}/gs
      );
      
      for (const match of functionMatches) {
        const functionName = match[1];
        const implementation = match[2];
        
        const contradictions = this.analyzeNameImplementationContradiction(functionName, implementation);
        
        if (contradictions.length > 0) {
          for (const contradiction of contradictions) {
            this.findings.push({
              id: this.generateId(),
              type: 'SEMANTIC_MISMATCH',
              severity: VerificationSeverity.MEDIUM,
              component: file,
              location: {
                file,
                line: this.getLineNumber(content, match.index!),
                module: component
              },
              title: 'Name vs Implementation Contradiction',
              description: contradiction,
              evidence: [{
                type: 'code',
                source: file,
                content: `function ${functionName}() { ${implementation.substring(0, 50)}... }`,
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
  }

  /**
   * Detect documentation vs implementation contradictions
   */
  private async detectDocumentationImplementationContradictions(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      const jsdocMatches = content.matchAll(
        /\/\*\*[\s\S]*?\*\/\s*(?:function|const\s+\w+\s*=\s*|(?:async\s+)?\w+)\s*(\w+)/gs
      );
      
      for (const match of jsdocMatches) {
        const jsdoc = match[0];
        const functionName = match[1];
        
        const docClaims = this.extractDocumentationClaims(jsdoc);
        
        // Find implementation
        const implMatch = content.match(
          new RegExp(`${functionName}\\s*\\([^)]*\\)\\s*{([^}]*(?:{[^}]*}[^}]*)*)}`, 's')
        );
        
        if (implMatch) {
          const implementation = implMatch[1];
          
          for (const claim of docClaims) {
            if (this.documentationContradictsImplementation(claim, implementation)) {
              this.findings.push({
                id: this.generateId(),
                type: 'INCONSISTENCY',
                severity: VerificationSeverity.HIGH,
                component: file,
                location: {
                  file,
                  line: this.getLineNumber(content, match.index!),
                  module: component
                },
                title: 'Documentation vs Implementation Contradiction',
                description: `Function '${functionName}' documentation claims '${claim}' but implementation contradicts this`,
                evidence: [
                  {
                    type: 'code',
                    source: file,
                    content: jsdoc,
                    timestamp: new Date(),
                    verified: true
                  },
                  {
                    type: 'code',
                    source: file,
                    content: implementation.substring(0, 100),
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
   * Detect type vs usage contradictions
   */
  private async detectTypeUsageContradictions(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find typed variables
      const typeMatches = content.matchAll(
        /(\w+)\s*:\s*(\w+)\s*=/g
      );
      
      for (const match of typeMatches) {
        const variableName = match[1];
        const declaredType = match[2];
        const assignmentStart = match.index! + match[0].length;
        const assignmentEnd = content.indexOf(';', assignmentStart);
        const assignment = content.substring(assignmentStart, assignmentEnd).trim();
        
        if (this.typeContradictsUsage(declaredType, assignment)) {
          this.findings.push({
            id: this.generateId(),
            type: 'INCONSISTENCY',
            severity: VerificationSeverity.HIGH,
            component: file,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Type vs Usage Contradiction',
            description: `Variable '${variableName}' declared as '${declaredType}' but assigned incompatible value`,
            evidence: [{
              type: 'code',
              source: file,
              content: `${variableName}: ${declaredType} = ${assignment}`,
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
   * Detect interface vs implementation contradictions
   */
  private async detectInterfaceImplementationContradictions(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find interfaces
      const interfaceMatches = content.matchAll(
        /interface\s+(\w+)\s*{([^}]+)}/gs
      );
      
      for (const interfaceMatch of interfaceMatches) {
        const interfaceName = interfaceMatch[1];
        const interfaceBody = interfaceMatch[2];
        
        // Find implementations
        const implMatches = content.matchAll(
          new RegExp(`class\\s+(\\w+)\\s+implements\\s+${interfaceName}\\s*{([^}]+)}`, 'gs')
        );
        
        for (const implMatch of implMatches) {
          const className = implMatch[1];
          const classBody = implMatch[2];
          
          const violations = this.detectInterfaceViolations(interfaceName, interfaceBody, className, classBody);
          
          for (const violation of violations) {
            this.findings.push({
              id: this.generateId(),
              type: 'INCONSISTENCY',
              severity: VerificationSeverity.HIGH,
              component: file,
              location: {
                file,
                line: this.getLineNumber(content, implMatch.index!),
                module: component
              },
              title: 'Interface vs Implementation Contradiction',
              description: violation,
              evidence: [
                {
                  type: 'code',
                  source: file,
                  content: `interface ${interfaceName} ${interfaceBody}`,
                  timestamp: new Date(),
                  verified: true
                },
                {
                  type: 'code',
                  source: file,
                  content: `class ${className} implements ${interfaceName} ${classBody}`,
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
   * Detect promise vs async contradictions
   */
  private async detectPromiseAsyncContradictions(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find async functions
      const asyncMatches = content.matchAll(
        /async\s+function\s+(\w+)\s*\(([^)]*)\)\s*{([^}]*(?:return[^}]*))?}/gs
      );
      
      for (const match of asyncMatches) {
        const functionName = match[1];
        const params = match[2];
        const body = match[3];
        
        // Check if async function doesn't return a promise
        if (body && !body.includes('return ') && !body.includes('await')) {
          this.findings.push({
            id: this.generateId(),
            type: 'INCONSISTENCY',
            severity: VerificationSeverity.MEDIUM,
            component: file,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Async Function Contradiction',
            description: `Function '${functionName}' is marked async but doesn't use await or return a promise`,
            evidence: [{
              type: 'code',
              source: file,
              content: `async function ${functionName}(${params}) { ${body.substring(0, 50)}... }`,
              timestamp: new Date(),
              verified: true
            }],
            timestamp: new Date(),
            verified: false,
            falsifiable: true
          });
        }
      }
      
      // Find functions returning promises but not marked async
      const promiseMatches = content.matchAll(
        /function\s+(\w+)\s*\([^)]*\)\s*{[^}]*return\s+(?:Promise|new\s+Promise)/gs
      );
      
      for (const match of promiseMatches) {
        const functionName = match[1];
        
        this.findings.push({
          id: this.generateId(),
          type: 'INCONSISTENCY',
          severity: VerificationSeverity.MEDIUM,
          component: file,
          location: {
            file,
            line: this.getLineNumber(content, match.index!),
            module: component
          },
          title: 'Promise Return Contradiction',
          description: `Function '${functionName}' returns a promise but is not marked async`,
          evidence: [{
            type: 'code',
            source: file,
            content: match[0].substring(0, 100),
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
   * Analyze name vs implementation contradiction
   */
  private analyzeNameImplementationContradiction(name: string, implementation: string): string[] {
    const contradictions: string[] = [];
    const nameLower = name.toLowerCase();
    const implLower = implementation.toLowerCase();
    
    // Name suggests validation but no validation logic
    if (nameLower.includes('validate') && !implLower.includes('if') && !implLower.includes('check')) {
      contradictions.push(`Function name '${name}' suggests validation but implementation lacks validation logic`);
    }
    
    // Name suggests computation but returns constant
    if ((nameLower.includes('compute') || nameLower.includes('calculate')) && 
        implLower.includes('return ') && 
        !/[\+\-\*\/]/.test(implementation)) {
      contradictions.push(`Function name '${name}' suggests computation but implementation returns constant`);
    }
    
    // Name suggests filtering but no filter logic
    if (nameLower.includes('filter') && !implLower.includes('filter') && !implLower.includes('if')) {
      contradictions.push(`Function name '${name}' suggests filtering but implementation lacks filter logic`);
    }
    
    // Name suggests mapping but no map logic
    if (nameLower.includes('map') && !implLower.includes('map') && !implLower.includes('transform')) {
      contradictions.push(`Function name '${name}' suggests mapping but implementation lacks map logic`);
    }
    
    return contradictions;
  }

  /**
   * Extract documentation claims
   */
  private extractDocumentationClaims(jsdoc: string): string[] {
    const claims: string[] = [];
    
    // Extract @param descriptions
    const paramMatches = jsdoc.matchAll(/@param\s+\{[^}]+\}\s+\w+\s+(.+)/g);
    for (const match of paramMatches) {
      claims.push(match[1].trim());
    }
    
    // Extract @returns
    const returnsMatch = jsdoc.match(/@returns\s+(.+)/);
    if (returnsMatch) {
      claims.push(returnsMatch[1].trim());
    }
    
    // Extract @throws
    const throwsMatches = jsdoc.matchAll(/@throws\s+(.+)/g);
    for (const match of throwsMatches) {
      claims.push(match[1].trim());
    }
    
    return claims;
  }

  /**
   * Check if documentation contradicts implementation
   */
  private documentationContradictsImplementation(claim: string, implementation: string): boolean {
    const claimLower = claim.toLowerCase();
    const implLower = implementation.toLowerCase();
    
    // Claim says throws but no throw in implementation
    if (claimLower.includes('throw') && !implLower.includes('throw')) {
      return true;
    }
    
    // Claim says returns but no return in implementation
    if (claimLower.includes('return') && !implLower.includes('return')) {
      return true;
    }
    
    // Claim says validates but no validation logic
    if (claimLower.includes('valid') && !implLower.includes('if') && !implLower.includes('check')) {
      return true;
    }
    
    return false;
  }

  /**
   * Check if type contradicts usage
   */
  private typeContradictsUsage(declaredType: string, assignment: string): boolean {
    const typePatterns: Record<string, RegExp[]> = {
      'string': [/^['"`]/, /^\w+$/],
      'number': [/^\d/, /^-\d/],
      'boolean': [/^(true|false)/],
      'Array': [/^\[/],
      'Object': [/^\{/]
    };
    
    const patterns = typePatterns[declaredType];
    if (patterns) {
      return !patterns.some(pattern => pattern.test(assignment));
    }
    
    return false;
  }

  /**
   * Detect interface violations
   */
  private detectInterfaceViolations(
    interfaceName: string,
    interfaceBody: string,
    className: string,
    classBody: string
  ): string[] {
    const violations: string[] = [];
    
    const interfaceMembers = this.extractMembers(interfaceBody);
    const classMembers = this.extractMembers(classBody);
    
    // Check for missing members
    for (const [name, type] of interfaceMembers) {
      if (!classMembers.has(name)) {
        violations.push(`Class '${className}' missing required member '${name}' from interface '${interfaceName}'`);
      }
    }
    
    // Check for type mismatches
    for (const [name, classType] of classMembers) {
      const interfaceType = interfaceMembers.get(name);
      if (interfaceType && interfaceType !== classType) {
        violations.push(`Class '${className}' member '${name}' has type '${classType}' but interface expects '${interfaceType}'`);
      }
    }
    
    return violations;
  }

  /**
   * Extract members from body
   */
  private extractMembers(body: string): Map<string, string> {
    const members = new Map<string, string>();
    
    const matches = body.matchAll(/(\w+)\s*:\s*([^;]+);/g);
    for (const match of matches) {
      members.set(match[1], match[2].trim());
    }
    
    return members;
  }

  /**
   * Extract contradictions from findings
   */
  private extractContradictions() {
    return this.findings.map(finding => ({
      context: `${finding.location.file}:${finding.location.line}`,
      contradiction: finding.description,
      evidence: finding.evidence
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
    return `semantic-contradiction-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}