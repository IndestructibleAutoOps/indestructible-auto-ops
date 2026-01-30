# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: anti-fabric-assumption-invalidator
# @GL-charter-version: 2.0.0

/**
 * Anti-Fabric: Assumption Invalidator
 * 
 * Core Philosophy: "驗證不是證明你是對的，而是證明你還沒被推翻。"
 * (Verification is not proving you're right, but proving you haven't been overturned yet.)
 * 
 * Purpose: Actively seek to invalidate assumptions made in GL components
 * 
 * This module actively searches for:
 * - Implicit assumptions in code
 * - Unvalidated premises
 * - Hardcoded values that should be parameters
 * - Assumptions about external systems
 * - Assumptions about data structures
 */

import { 
  AssumptionValidationResult,
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class AssumptionInvalidator {
  private findings: VerificationFinding[] = [];

  /**
   * Validate assumptions in a component
   */
  async validateAssumptions(component: string): Promise<AssumptionValidationResult> {
    this.findings = [];
    
    // Scan component for assumptions
    await this.scanComponent(component);
    
    return {
      assumptionsValidated: false, // Always false - we're looking for invalidations
      violations: this.extractViolations()
    };
  }

  /**
   * Scan component for various assumption patterns
   */
  private async scanComponent(component: string): Promise<void> {
    // 1. Detect hardcoded assumptions
    await this.detectHardcodedAssumptions(component);
    
    // 2. Detect implicit type assumptions
    await this.detectImplicitTypeAssumptions(component);
    
    // 3. Detect external system assumptions
    await this.detectExternalSystemAssumptions(component);
    
    // 4. Detect data structure assumptions
    await this.detectDataStructureAssumptions(component);
    
    // 5. Detect behavioral assumptions
    await this.detectBehavioralAssumptions(component);
  }

  /**
   * Detect hardcoded assumptions
   */
  private async detectHardcodedAssumptions(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Detect hardcoded URLs
      const urlMatches = content.matchAll(
        /['"]https?:\/\/[^\s'"]+['"]/g
      );
      
      for (const match of urlMatches) {
        const url = match[0].replace(/['"]/g, '');
        
        // Skip common test URLs
        if (!url.includes('localhost') && !url.includes('example.com') && !url.includes('test')) {
          this.findings.push({
            id: this.generateId(),
            type: 'ASSUMPTION_VIOLATION',
            severity: VerificationSeverity.MEDIUM,
            component,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Hardcoded URL Assumption Detected',
            description: `URL '${url}' is hardcoded - should be configurable`,
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
      
      // Detect hardcoded timeouts
      const timeoutMatches = content.matchAll(
        /(setTimeout|setInterval|sleep|delay)\s*\(\s*(\d+)\s*/g
      );
      
      for (const match of timeoutMatches) {
        const timeout = match[2];
        
        // Convert to seconds
        const timeoutSec = parseInt(timeout) / 1000;
        
        if (timeoutSec > 5) {
          this.findings.push({
            id: this.generateId(),
            type: 'ASSUMPTION_VIOLATION',
            severity: VerificationSeverity.LOW,
            component,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Hardcoded Timeout Assumption Detected',
            description: `Timeout of ${timeoutSec}s is hardcoded - should be configurable`,
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
      
      // Detect hardcoded limits
      const limitMatches = content.matchAll(
        /(?:limit|max|size|count|threshold)\s*[=:]\s*(\d+)/gi
      );
      
      for (const match of limitMatches) {
        const limit = match[1];
        
        // Check if it's a reasonable limit
        const limitNum = parseInt(limit);
        if (limitNum > 0 && limitNum < 1000000) {
          this.findings.push({
            id: this.generateId(),
            type: 'ASSUMPTION_VIOLATION',
            severity: VerificationSeverity.LOW,
            component,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Hardcoded Limit Assumption Detected',
            description: `Limit '${limit}' is hardcoded - should be configurable`,
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
   * Detect implicit type assumptions
   */
  private async detectImplicitTypeAssumptions(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Detect untyped function parameters
      const paramMatches = content.matchAll(
        /function\s+(\w+)\s*\(([^)]*)\)/g
      );
      
      for (const match of paramMatches) {
        const functionName = match[1];
        const params = match[2];
        
        if (params && !params.includes(':')) {
          this.findings.push({
            id: this.generateId(),
            type: 'ASSUMPTION_VIOLATION',
            severity: VerificationSeverity.MEDIUM,
            component,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Implicit Type Assumption Detected',
            description: `Function '${functionName}' has untyped parameters - assumes any type`,
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
      
      // Detect any type usage
      const anyMatches = content.matchAll(/:\s*any\b/g);
      
      for (const match of anyMatches) {
        this.findings.push({
          id: this.generateId(),
          type: 'ASSUMPTION_VIOLATION',
          severity: VerificationSeverity.HIGH,
          component,
          location: {
            file,
            line: this.getLineNumber(content, match.index!),
            module: component
          },
          title: 'Any Type Assumption Detected',
          description: 'Using "any" type makes no type assumptions - defeats type safety',
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
   * Detect external system assumptions
   */
  private async detectExternalSystemAssumptions(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Detect API calls without error handling
      const apiMatches = content.matchAll(
        /(?:fetch|axios|request|http)\s*\([^)]+\)/g
      );
      
      for (const match of apiMatches) {
        const apiCall = match[0];
        
        // Check if there's error handling
        const lineStart = content.lastIndexOf('\n', match.index!) + 1;
        const lineEnd = content.indexOf('\n', match.index!);
        const line = content.substring(lineStart, lineEnd);
        
        if (!line.includes('try') && !line.includes('catch') && !line.includes('.catch')) {
          this.findings.push({
            id: this.generateId(),
            type: 'ASSUMPTION_VIOLATION',
            severity: VerificationSeverity.HIGH,
            component,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'External System Assumption Detected',
            description: 'API call without error handling - assumes success',
            evidence: [{
              type: 'code',
              source: file,
              content: apiCall,
              timestamp: new Date(),
              verified: true
            }],
            timestamp: new Date(),
            verified: false,
            falsifiable: true
          });
        }
      }
      
      // Detect file system operations without error handling
      const fsMatches = content.matchAll(
        /(?:readFile|writeFile|exists|unlink)\s*\([^)]+\)/g
      );
      
      for (const match of fsMatches) {
        const fsCall = match[0];
        
        // Check if there's error handling
        const lineStart = content.lastIndexOf('\n', match.index!) + 1;
        const lineEnd = content.indexOf('\n', match.index!);
        const line = content.substring(lineStart, lineEnd);
        
        if (!line.includes('try') && !line.includes('catch') && !line.includes('.catch')) {
          this.findings.push({
            id: this.generateId(),
            type: 'ASSUMPTION_VIOLATION',
            severity: VerificationSeverity.HIGH,
            component,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'File System Assumption Detected',
            description: 'File system operation without error handling - assumes file exists',
            evidence: [{
              type: 'code',
              source: file,
              content: fsCall,
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
   * Detect data structure assumptions
   */
  private async detectDataStructureAssumptions(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Detect array access without bounds checking
      const arrayAccessMatches = content.matchAll(
        /(\w+)\s*\[\s*(\d+)\s*\]/g
      );
      
      for (const match of arrayAccessMatches) {
        const arrayName = match[1];
        const index = match[2];
        
        // Check if index is hardcoded
        const indexNum = parseInt(index);
        if (!isNaN(indexNum)) {
          // Look for length check
          const surroundingContext = content.substring(
            Math.max(0, match.index! - 200),
            Math.min(content.length, match.index! + 200)
          );
          
          if (!surroundingContext.includes('length') && !surroundingContext.includes('check')) {
            this.findings.push({
              id: this.generateId(),
              type: 'ASSUMPTION_VIOLATION',
              severity: VerificationSeverity.MEDIUM,
              component,
              location: {
                file,
                line: this.getLineNumber(content, match.index!),
                module: component
              },
              title: 'Array Bounds Assumption Detected',
              description: `Accessing array '${arrayName}' at index ${indexNum} without bounds check`,
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
      
      // Detect object property access without null checks
      const propertyAccessMatches = content.matchAll(
        /(\w+)\s*\.\s*(\w+)/g
      );
      
      for (const match of propertyAccessMatches) {
        const objectName = match[1];
        const propertyName = match[2];
        
        // Look for null/undefined checks
        const surroundingContext = content.substring(
          Math.max(0, match.index! - 100),
          Math.min(content.length, match.index! + 100)
        );
        
        if (!surroundingContext.includes('!') && 
            !surroundingContext.includes('??') && 
            !surroundingContext.includes('optional')) {
          this.findings.push({
            id: this.generateId(),
            type: 'ASSUMPTION_VIOLATION',
            severity: VerificationSeverity.MEDIUM,
            component,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Object Property Assumption Detected',
            description: `Accessing property '${propertyName}' on '${objectName}' without null/undefined check`,
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
   * Detect behavioral assumptions
   */
  private async detectBehavioralAssumptions(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Detect functions that always return true/false
      const returnTrueMatches = content.matchAll(
        /function\s+(\w+)\s*\([^)]*\)\s*{[^}]*return\s+true;[^}]*}/gs
      );
      
      for (const match of returnTrueMatches) {
        const functionName = match[1];
        
        // Skip trivial functions
        if (!functionName.toLowerCase().includes('dummy') && 
            !functionName.toLowerCase().includes('mock') &&
            !functionName.toLowerCase().includes('stub')) {
          this.findings.push({
            id: this.generateId(),
            type: 'ASSUMPTION_VIOLATION',
            severity: VerificationSeverity.MEDIUM,
            component,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Behavioral Assumption Detected',
            description: `Function '${functionName}' always returns true - assumes no failure cases`,
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
      
      // Detect empty catch blocks
      const catchMatches = content.matchAll(/catch\s*\([^)]*\)\s*{\s*}/g);
      
      for (const match of catchMatches) {
        this.findings.push({
          id: this.generateId(),
          type: 'ASSUMPTION_VIOLATION',
          severity: VerificationSeverity.HIGH,
          component,
          location: {
            file,
            line: this.getLineNumber(content, match.index!),
            module: component
          },
          title: 'Error Handling Assumption Detected',
          description: 'Empty catch block - assumes errors can be silently ignored',
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
   * Extract violations from findings
   */
  private extractViolations() {
    return this.findings.map(finding => ({
      assumption: finding.title,
      invalidationMethod: finding.type,
      counterexample: finding.evidence[0]?.content,
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
    return `assumption-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}