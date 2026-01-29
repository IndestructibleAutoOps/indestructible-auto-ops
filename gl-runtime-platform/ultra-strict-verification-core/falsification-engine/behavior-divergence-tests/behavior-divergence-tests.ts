# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: falsification-engine-behavior-divergence-tests
# @GL-charter-version: 2.0.0

/**
 * Falsification Engine: Behavior Divergence Tests
 * 
 * Core Philosophy: "驗證不是證明你是對的，而是證明你還沒被推翻。"
 * (Verification is not proving you're right, but proving you haven't been overturned yet.)
 * 
 * Purpose: Detect behavior divergences between expected and actual behavior
 * 
 * This module actively searches for:
 * - Expected vs actual behavior differences
 * - Side effect divergences
 * - Performance divergences
 * - State management divergences
 * - Error handling divergences
 */

import { 
  BehaviorDivergenceResult,
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class BehaviorDivergenceTests {
  private findings: VerificationFinding[] = [];

  /**
   * Test behavior divergences in a component
   */
  async testBehaviorDivergence(component: string): Promise<BehaviorDivergenceResult> {
    this.findings = [];
    
    // Scan component for behavior divergences
    await this.scanComponent(component);
    
    return {
      diverged: this.findings.length > 0,
      divergences: this.extractDivergences()
    };
  }

  /**
   * Scan component for behavior divergences
   */
  private async scanComponent(component: string): Promise<void> {
    // 1. Detect side effect divergences
    await this.detectSideEffectDivergences(component);
    
    // 2. Detect error handling divergences
    await this.detectErrorHandlingDivergences(component);
    
    // 3. Detect state management divergences
    await this.detectStateManagementDivergences(component);
    
    // 4. Detect async behavior divergences
    await this.detectAsyncBehaviorDivergences(component);
  }

  /**
   * Detect side effect divergences
   */
  private async detectSideEffectDivergences(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find pure function declarations (should have no side effects)
      const pureFunctionMatches = content.matchAll(
        /\/\/\s*@\s*pure\s*\n\s*(?:function|const\s+\w+\s*=\s*)\s*(\w+)\s*\([^)]*\)\s*{([^}]+)}/gs
      );
      
      for (const match of pureFunctionMatches) {
        const functionName = match[1];
        const functionBody = match[2];
        
        // Check for side effects
        const sideEffects = this.detectSideEffects(functionBody);
        
        if (sideEffects.length > 0) {
          this.findings.push({
            id: this.generateId(),
            type: 'BEHAVIOR_DIVERGENCE',
            severity: VerificationSeverity.HIGH,
            component: file,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Pure Function Side Effect Divergence',
            description: `Function '${functionName}' is marked as pure but has side effects: ${sideEffects.join(', ')}`,
            evidence: [{
              type: 'code',
              source: file,
              content: functionBody.substring(0, 100),
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
   * Detect error handling divergences
   */
  private async detectErrorHandlingDivergences(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find functions that should throw but don't
      const shouldThrowMatches = content.matchAll(
        /function\s+(\w+)\s*\([^)]*\)\s*{([^}]*(?:if\s*\([^)]*\)\s*{[^}]*}))?[^}]*}/gs
      );
      
      for (const match of shouldThrowMatches) {
        const functionName = match[1];
        const functionBody = match[2];
        
        // Check for potential error scenarios
        if (this.shouldHaveErrorHandling(functionName, functionBody)) {
          if (!functionBody.includes('throw') && !functionBody.includes('Error')) {
            this.findings.push({
              id: this.generateId(),
              type: 'BEHAVIOR_DIVERGENCE',
              severity: VerificationSeverity.MEDIUM,
              component: file,
              location: {
                file,
                line: this.getLineNumber(content, match.index!),
                module: component
              },
              title: 'Error Handling Divergence',
              description: `Function '${functionName}' should have error handling but doesn't throw errors`,
              evidence: [{
                type: 'code',
                source: file,
                content: functionBody.substring(0, 100),
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
   * Detect state management divergences
   */
  private async detectStateManagementDivergences(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find state mutations
      const stateMutationMatches = content.matchAll(
        /(\w+)\s*\.\s*(\w+)\s*=/g
      );
      
      for (const match of stateMutationMatches) {
        const objectName = match[1];
        const propertyName = match[2];
        
        // Check if state should be immutable
        if (objectName.toLowerCase().includes('state') || 
            objectName.toLowerCase().includes('store')) {
          
          const line = this.getLineNumber(content, match.index!);
          
          this.findings.push({
            id: this.generateId(),
            type: 'BEHAVIOR_DIVERGENCE',
            severity: VerificationSeverity.MEDIUM,
            component: file,
            location: {
              file,
              line,
              module: component
            },
            title: 'State Mutation Divergence',
            description: `Direct mutation of state object '${objectName}.${propertyName}' detected - should use immutable updates`,
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
   * Detect async behavior divergences
   */
  private async detectAsyncBehaviorDivergences(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find async functions without proper error handling
      const asyncMatches = content.matchAll(
        /async\s+function\s+(\w+)\s*\(([^)]*)\)\s*{([^}]+)}/gs
      );
      
      for (const match of asyncMatches) {
        const functionName = match[1];
        const functionBody = match[2];
        
        // Check for await without try-catch
        if (functionBody.includes('await') && 
            !functionBody.includes('try') && 
            !functionBody.includes('.catch')) {
          
          this.findings.push({
            id: this.generateId(),
            type: 'BEHAVIOR_DIVERGENCE',
            severity: VerificationSeverity.HIGH,
            component: file,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Async Error Handling Divergence',
            description: `Async function '${functionName}' has await but no try-catch or .catch`,
            evidence: [{
              type: 'code',
              source: file,
              content: functionBody.substring(0, 100),
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
   * Detect side effects in function body
   */
  private detectSideEffects(functionBody: string): string[] {
    const sideEffects: string[] = [];
    
    if (functionBody.includes('console.')) {
      sideEffects.push('console logging');
    }
    
    if (functionBody.includes('.push(') || functionBody.includes('.pop(')) {
      sideEffects.push('array mutation');
    }
    
    if (functionBody.includes('.delete(') || functionBody.includes('.set(')) {
      sideEffects.push('map mutation');
    }
    
    if (functionBody.includes('fetch(') || functionBody.includes('axios.')) {
      sideEffects.push('network request');
    }
    
    if (functionBody.includes('fs.') || functionBody.includes('readFile') || functionBody.includes('writeFile')) {
      sideEffects.push('file system operation');
    }
    
    if (/=\s*\w+\./.test(functionBody)) {
      sideEffects.push('object mutation');
    }
    
    return sideEffects;
  }

  /**
   * Check if function should have error handling
   */
  private shouldHaveErrorHandling(functionName: string, functionBody: string): boolean {
    const nameLower = functionName.toLowerCase();
    
    // Functions that should handle errors
    const errorHandlingFunctions = [
      'parse', 'decode', 'decrypt', 'validate', 'check', 'verify',
      'fetch', 'request', 'get', 'post', 'put', 'delete',
      'connect', 'open', 'close', 'read', 'write'
    ];
    
    return errorHandlingFunctions.some(fn => nameLower.includes(fn));
  }

  /**
   * Extract divergences from findings
   */
  private extractDivergences() {
    return this.findings.map(finding => ({
      scenario: finding.title,
      expectedBehavior: 'Expected behavior as documented',
      actualBehavior: finding.description,
      divergence: finding.type,
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
    return `behavior-divergence-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}