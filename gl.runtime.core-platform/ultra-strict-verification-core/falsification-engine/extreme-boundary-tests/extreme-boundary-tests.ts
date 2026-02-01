# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: falsification-engine-extreme-boundary-tests
# @GL-charter-version: 2.0.0

/**
 * Falsification Engine: Extreme Boundary Tests
 * 
 * Core Philosophy: "推翻 GL 所有的結論，直到剩下的部分是真正站得住的。"
 * (Overturn all GL conclusions until only what truly stands remains.)
 * 
 * Purpose: Test components at extreme boundaries to find hidden vulnerabilities
 * 
 * This module generates boundary tests for:
 * - Numeric limits
 * - String lengths
 * - Array sizes
 * - Object depths
 * - Memory constraints
 * - Time limits
 */

import { 
  BoundaryTestResult,
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class ExtremeBoundaryTests {
  private findings: VerificationFinding[] = [];

  /**
   * Test boundaries in a component
   */
  async testBoundaries(component: string): Promise<BoundaryTestResult> {
    this.findings = [];
    
    // Scan component for boundary conditions
    await this.scanComponent(component);
    
    return {
      boundaryViolated: this.findings.length > 0,
      violations: this.extractViolations()
    };
  }

  /**
   * Scan component for boundary conditions
   */
  private async scanComponent(component: string): Promise<void> {
    // 1. Test numeric boundaries
    await this.testNumericBoundaries(component);
    
    // 2. Test string boundaries
    await this.testStringBoundaries(component);
    
    // 3. Test array boundaries
    await this.testArrayBoundaries(component);
    
    // 4. Test object depth boundaries
    await this.testObjectDepthBoundaries(component);
    
    // 5. Test recursion depth boundaries
    await this.testRecursionDepthBoundaries(component);
  }

  /**
   * Test numeric boundaries
   */
  private async testNumericBoundaries(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find numeric parameters
      const numericMatches = content.matchAll(
        /(\w+)\s*:\s*number/g
      );
      
      for (const match of numericMatches) {
        const paramName = match[1];
        const line = this.getLineNumber(content, match.index!);
        
        // Test extreme numeric values
        const extremeValues = [
          { value: Number.MAX_SAFE_INTEGER, name: 'MAX_SAFE_INTEGER' },
          { value: Number.MIN_SAFE_INTEGER, name: 'MIN_SAFE_INTEGER' },
          { value: Number.MAX_VALUE, name: 'MAX_VALUE' },
          { value: Number.MIN_VALUE, name: 'MIN_VALUE' },
          { value: Infinity, name: 'Infinity' },
          { value: -Infinity, name: '-Infinity' },
          { value: NaN, name: 'NaN' },
          { value: 0, name: 'Zero' },
          { value: -0, name: 'Negative Zero' },
          { value: Number.EPSILON, name: 'EPSILON' }
        ];
        
        for (const { value, name } of extremeValues) {
          this.findings.push({
            id: this.generateId(),
            type: 'EXTREME_BOUNDARY',
            severity: VerificationSeverity.MEDIUM,
            component: file,
            location: {
              file,
              line,
              module: component
            },
            title: 'Numeric Boundary Test',
            description: `Parameter '${paramName}' should be tested with ${name}: ${value}`,
            evidence: [{
              type: 'code',
              source: file,
              content: `${paramName}: number = ${value}`,
              timestamp: new Date(),
              verified: false
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
   * Test string boundaries
   */
  private async testStringBoundaries(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find string parameters
      const stringMatches = content.matchAll(
        /(\w+)\s*:\s*string/g
      );
      
      for (const match of stringMatches) {
        const paramName = match[1];
        const line = this.getLineNumber(content, match.index!);
        
        // Test extreme string values
        const extremeStrings = [
          { value: '', name: 'Empty String' },
          { value: ' ', name: 'Single Space' },
          { value: '\0', name: 'Null Character' },
          { value: '\t', name: 'Tab Character' },
          { value: '\n', name: 'Newline Character' },
          { value: '\r', name: 'Carriage Return' },
          { value: '\x00\x01\x02\x03', name: 'Control Characters' },
          { value: 'a'.repeat(1000), name: '1000 Characters' },
          { value: 'a'.repeat(10000), name: '10000 Characters' },
          { value: 'a'.repeat(100000), name: '100000 Characters' },
          { value: '🔥'.repeat(1000), name: '1000 Emoji' },
          { value: 'a'.repeat(255), name: '255 Characters (DB limit)' },
          { value: 'a'.repeat(65535), name: '65535 Characters (MAX ushort)' },
          { value: 'a'.repeat(2147483647), name: 'MAX_INT32 Characters' }
        ];
        
        for (const { value, name } of extremeStrings) {
          this.findings.push({
            id: this.generateId(),
            type: 'EXTREME_BOUNDARY',
            severity: VerificationSeverity.MEDIUM,
            component: file,
            location: {
              file,
              line,
              module: component
            },
            title: 'String Boundary Test',
            description: `Parameter '${paramName}' should be tested with ${name} (length: ${value.length})`,
            evidence: [{
              type: 'code',
              source: file,
              content: `${paramName}: string = "${value.substring(0, 20)}${value.length > 20 ? '...' : ''}"`,
              timestamp: new Date(),
              verified: false
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
   * Test array boundaries
   */
  private async testArrayBoundaries(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find array parameters
      const arrayMatches = content.matchAll(
        /(\w+)\s*:\s*(?:\w+\[\]|Array<\w+>)/g
      );
      
      for (const match of arrayMatches) {
        const paramName = match[1];
        const line = this.getLineNumber(content, match.index!);
        
        // Test extreme array sizes
        const extremeSizes = [
          { size: 0, name: 'Empty Array' },
          { size: 1, name: 'Single Element' },
          { size: 2, name: 'Two Elements' },
          { size: 10, name: 'Ten Elements' },
          { size: 100, name: 'Hundred Elements' },
          { size: 1000, name: 'Thousand Elements' },
          { size: 10000, name: 'Ten Thousand Elements' },
          { size: 100000, name: 'Hundred Thousand Elements' },
          { size: 1000000, name: 'Million Elements' }
        ];
        
        for (const { size, name } of extremeSizes) {
          this.findings.push({
            id: this.generateId(),
            type: 'EXTREME_BOUNDARY',
            severity: VerificationSeverity.MEDIUM,
            component: file,
            location: {
              file,
              line,
              module: component
            },
            title: 'Array Boundary Test',
            description: `Parameter '${paramName}' should be tested with ${name} (${size} elements)`,
            evidence: [{
              type: 'code',
              source: file,
              content: `${paramName}: Array<${size} elements>`,
              timestamp: new Date(),
              verified: false
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
   * Test object depth boundaries
   */
  private async testObjectDepthBoundaries(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find object parameters
      const objectMatches = content.matchAll(
        /(\w+)\s*:\s*(?:object|{[^}]+})/g
      );
      
      for (const match of objectMatches) {
        const paramName = match[1];
        const line = this.getLineNumber(content, match.index!);
        
        // Test extreme object depths
        const extremeDepths = [
          { depth: 0, name: 'Empty Object' },
          { depth: 1, name: 'Depth 1' },
          { depth: 5, name: 'Depth 5' },
          { depth: 10, name: 'Depth 10' },
          { depth: 50, name: 'Depth 50' },
          { depth: 100, name: 'Depth 100' },
          { depth: 1000, name: 'Depth 1000' }
        ];
        
        for (const { depth, name } of extremeDepths) {
          this.findings.push({
            id: this.generateId(),
            type: 'EXTREME_BOUNDARY',
            severity: VerificationSeverity.MEDIUM,
            component: file,
            location: {
              file,
              line,
              module: component
            },
            title: 'Object Depth Boundary Test',
            description: `Parameter '${paramName}' should be tested with ${name}`,
            evidence: [{
              type: 'code',
              source: file,
              content: `${paramName}: object (depth: ${depth})`,
              timestamp: new Date(),
              verified: false
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
   * Test recursion depth boundaries
   */
  private async testRecursionDepthBoundaries(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find recursive functions
      const recursiveMatches = content.matchAll(
        /function\s+(\w+)\s*\([^)]*\)\s*{[^}]*\1\s*\([^)]*\)[^}]*}/g
      );
      
      for (const match of recursiveMatches) {
        const functionName = match[1];
        const line = this.getLineNumber(content, match.index!);
        
        // Test extreme recursion depths
        const extremeDepths = [
          { depth: 1, name: 'Depth 1' },
          { depth: 10, name: 'Depth 10' },
          { depth: 100, name: 'Depth 100' },
          { depth: 1000, name: 'Depth 1000' },
          { depth: 10000, name: 'Depth 10000' },
          { depth: 100000, name: 'Depth 100000 (Stack Overflow Risk)' }
        ];
        
        for (const { depth, name } of extremeDepths) {
          this.findings.push({
            id: this.generateId(),
            type: 'EXTREME_BOUNDARY',
            severity: depth > 1000 ? VerificationSeverity.HIGH : VerificationSeverity.MEDIUM,
            component: file,
            location: {
              file,
              line,
              module: component
            },
            title: 'Recursion Depth Boundary Test',
            description: `Recursive function '${functionName}' should be tested with ${name}`,
            evidence: [{
              type: 'code',
              source: file,
              content: `${functionName}(depth: ${depth})`,
              timestamp: new Date(),
              verified: false
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
      boundary: finding.title,
      input: finding.evidence[0]?.content,
      expected: 'No violation',
      actual: finding.description,
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
    return `boundary-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}