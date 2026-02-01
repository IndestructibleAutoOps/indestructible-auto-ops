# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: anti-fabric-adversarial-generator
# @GL-charter-version: 2.0.0

/**
 * Anti-Fabric: Adversarial Generator
 * 
 * Core Philosophy: "推翻 GL 所有的結論，直到剩下的部分是真正站得住的。"
 * (Overturn all GL conclusions until only what truly stands remains.)
 * 
 * Purpose: Generate adversarial inputs to actively challenge and break GL components
 * 
 * This module actively creates:
 * - Malformed inputs
 * - Edge cases
 * - Boundary violations
 * - Stress scenarios
 * - Unexpected data types
 * - Conflicting states
 */

import { 
  AdversarialResult,
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class AdversarialGenerator {
  private findings: VerificationFinding[] = [];
  private adversarialInputs: Array<{ input: any; category: string; purpose: string }> = [];

  /**
   * Generate adversarial inputs for a component
   */
  async generateAdversarialInputs(component: string): Promise<AdversarialResult> {
    this.findings = [];
    this.adversarialInputs = [];
    
    // Generate adversarial inputs
    await this.generateForComponent(component);
    
    return {
      adversarialInputs: this.adversarialInputs,
      systemFailures: this.extractFailures()
    };
  }

  /**
   * Generate adversarial inputs for a component
   */
  private async generateForComponent(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    
    // 1. Generate malformed inputs
    await this.generateMalformedInputs(component, componentPath);
    
    // 2. Generate boundary violations
    await this.generateBoundaryViolations(component, componentPath);
    
    // 3. Generate unexpected types
    await this.generateUnexpectedTypes(component, componentPath);
    
    // 4. Generate conflicting states
    await this.generateConflictingStates(component, componentPath);
    
    // 5. Generate stress scenarios
    await this.generateStressScenarios(component, componentPath);
  }

  /**
   * Generate malformed inputs
   */
  private async generateMalformedInputs(component: string, componentPath: string): Promise<void> {
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find function signatures
      const functionMatches = content.matchAll(
        /(?:function|const\s+\w+\s*=\s*|(?:async\s+)?\w+)\s*(\w+)\s*\(([^)]*)\)/g
      );
      
      for (const match of functionMatches) {
        const functionName = match[1];
        const params = match[2];
        
        if (params && params.trim()) {
          // Generate malformed inputs for each parameter
          const paramList = params.split(',').map(p => p.trim().split(':')[0]);
          
          for (const param of paramList) {
            if (param) {
              this.adversarialInputs.push({
                input: { [param]: null },
                category: 'malformed',
                purpose: `Null value for parameter '${param}' in function '${functionName}'`
              });
              
              this.adversarialInputs.push({
                input: { [param]: undefined },
                category: 'malformed',
                purpose: `Undefined value for parameter '${param}' in function '${functionName}'`
              });
              
              this.adversarialInputs.push({
                input: { [param]: '' },
                category: 'malformed',
                purpose: `Empty string for parameter '${param}' in function '${functionName}'`
              });
            }
          }
        }
      }
    }
  }

  /**
   * Generate boundary violations
   */
  private async generateBoundaryViolations(component: string, componentPath: string): Promise<void> {
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find numeric parameters
      const numericMatches = content.matchAll(
        /(\w+)\s*:\s*number/g
      );
      
      for (const match of numericMatches) {
        const paramName = match[1];
        
        this.adversarialInputs.push({
          input: { [paramName]: Number.MAX_SAFE_INTEGER },
          category: 'boundary',
          purpose: `Maximum safe integer for parameter '${paramName}'`
        });
        
        this.adversarialInputs.push({
          input: { [paramName]: Number.MIN_SAFE_INTEGER },
          category: 'boundary',
          purpose: `Minimum safe integer for parameter '${paramName}'`
        });
        
        this.adversarialInputs.push({
          input: { [paramName]: Infinity },
          category: 'boundary',
          purpose: `Infinity for parameter '${paramName}'`
        });
        
        this.adversarialInputs.push({
          input: { [paramName]: -Infinity },
          category: 'boundary',
          purpose: `Negative infinity for parameter '${paramName}'`
        });
        
        this.adversarialInputs.push({
          input: { [paramName]: NaN },
          category: 'boundary',
          purpose: `NaN for parameter '${paramName}'`
        });
      }
      
      // Find string parameters
      const stringMatches = content.matchAll(/(\w+)\s*:\s*string/g);
      
      for (const match of stringMatches) {
        const paramName = match[1];
        
        this.adversarialInputs.push({
          input: { [paramName]: 'a'.repeat(100000) },
          category: 'boundary',
          purpose: `Very long string for parameter '${paramName}'`
        });
        
        this.adversarialInputs.push({
          input: { [paramName]: '\0' },
          category: 'boundary',
          purpose: `Null character for parameter '${paramName}'`
        });
        
        this.adversarialInputs.push({
          input: { [paramName]: '\x00\x01\x02\x03' },
          category: 'boundary',
          purpose: `Control characters for parameter '${paramName}'`
        });
        
        // Unicode edge cases
        this.adversarialInputs.push({
          input: { [paramName]: '🔥'.repeat(1000) },
          category: 'boundary',
          purpose: `Many emoji for parameter '${paramName}'`
        });
      }
      
      // Find array parameters
      const arrayMatches = content.matchAll(/(\w+)\s*:\s*\w+\[\]/g);
      
      for (const match of arrayMatches) {
        const paramName = match[1];
        
        this.adversarialInputs.push({
          input: { [paramName]: [] },
          category: 'boundary',
          purpose: `Empty array for parameter '${paramName}'`
        });
        
        this.adversarialInputs.push({
          input: { [paramName]: Array(100000).fill(null) },
          category: 'boundary',
          purpose: `Very large array for parameter '${paramName}'`
        });
      }
    }
  }

  /**
   * Generate unexpected types
   */
  private async generateUnexpectedTypes(component: string, componentPath: string): Promise<void> {
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find all typed parameters
      const typeMatches = content.matchAll(/(\w+)\s*:\s*(\w+)/g);
      
      for (const match of typeMatches) {
        const paramName = match[1];
        const typeName = match[2];
        
        // Generate wrong type inputs
        if (typeName === 'string') {
          this.adversarialInputs.push({
            input: { [paramName]: 123 },
            category: 'unexpected-type',
            purpose: `Number for string parameter '${paramName}'`
          });
          
          this.adversarialInputs.push({
            input: { [paramName]: true },
            category: 'unexpected-type',
            purpose: `Boolean for string parameter '${paramName}'`
          });
        } else if (typeName === 'number') {
          this.adversarialInputs.push({
            input: { [paramName]: '123' },
            category: 'unexpected-type',
            purpose: `String for number parameter '${paramName}'`
          });
          
          this.adversarialInputs.push({
            input: { [paramName]: {} },
            category: 'unexpected-type',
            purpose: `Object for number parameter '${paramName}'`
          });
        } else if (typeName === 'boolean') {
          this.adversarialInputs.push({
            input: { [paramName]: 'true' },
            category: 'unexpected-type',
            purpose: `String for boolean parameter '${paramName}'`
          });
          
          this.adversarialInputs.push({
            input: { [paramName]: 1 },
            category: 'unexpected-type',
            purpose: `Number for boolean parameter '${paramName}'`
          });
        } else if (typeName.includes('Array')) {
          this.adversarialInputs.push({
            input: { [paramName]: {} },
            category: 'unexpected-type',
            purpose: `Object for array parameter '${paramName}'`
          });
          
          this.adversarialInputs.push({
            input: { [paramName]: 'not an array' },
            category: 'unexpected-type',
            purpose: `String for array parameter '${paramName}'`
          });
        }
      }
    }
  }

  /**
   * Generate conflicting states
   */
  private async generateConflictingStates(component: string, componentPath: string): Promise<void> {
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find object parameters
      const objectMatches = content.matchAll(/(\w+)\s*:\s*(?:object|{[^}]+})/g);
      
      for (const match of objectMatches) {
        const paramName = match[1];
        
        // Generate conflicting properties
        this.adversarialInputs.push({
          input: {
            [paramName]: {
              enabled: true,
              enabled: false,  // Duplicate property with different value
              count: 5,
              count: 'five',   // Duplicate property with different type
            }
          },
          category: 'conflicting-state',
          purpose: `Duplicate properties with conflicting values for object parameter '${paramName}'`
        });
        
        // Generate circular reference
        const circularObj: any = { name: 'circular' };
        circularObj.self = circularObj;
        
        this.adversarialInputs.push({
          input: { [paramName]: circularObj },
          category: 'conflicting-state',
          purpose: `Circular reference for object parameter '${paramName}'`
        });
        
        // Generate mutually exclusive properties
        this.adversarialInputs.push({
          input: {
            [paramName]: {
              isPresent: true,
              isAbsent: true,
              count: 0,
              count: -1,
            }
          },
          category: 'conflicting-state',
          purpose: `Mutually exclusive properties for object parameter '${paramName}'`
        });
      }
    }
  }

  /**
   * Generate stress scenarios
   */
  private async generateStressScenarios(component: string, componentPath: string): Promise<void> {
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Find functions that might have loops
      const functionMatches = content.matchAll(
        /function\s+(\w+)\s*\([^)]*\)\s*{[^}]*(?:for|while|do)[^}]*}/g
      );
      
      for (const match of functionMatches) {
        const functionName = match[1];
        
        // Generate inputs that might cause infinite loops
        this.adversarialInputs.push({
          input: {
            iterations: Number.MAX_SAFE_INTEGER,
            condition: true
          },
          category: 'stress',
          purpose: `Potential infinite loop scenario for function '${functionName}'`
        });
        
        this.adversarialInputs.push({
          input: {
            array: Array(1000000).fill('item'),
            predicate: () => false  // Never matches
          },
          category: 'stress',
          purpose: `Exhaustive search scenario for function '${functionName}'`
        });
      }
      
      // Find recursive functions
      const recursiveMatches = content.matchAll(
        /function\s+(\w+)\s*\([^)]*\)\s*{[^}]*\1\s*\([^)]*\)[^}]*}/g
      );
      
      for (const match of recursiveMatches) {
        const functionName = match[1];
        
        // Generate inputs that might cause stack overflow
        this.adversarialInputs.push({
          input: {
            depth: 100000
          },
          category: 'stress',
          purpose: `Potential stack overflow scenario for recursive function '${functionName}'`
        });
      }
    }
  }

  /**
   * Extract failures from findings
   */
  private extractFailures() {
    return this.findings.map(finding => ({
      input: finding.evidence[0]?.content,
      failure: finding.description,
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

  private generateId(): string {
    return `adversarial-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}