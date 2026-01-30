# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: execution-harness-oracle-validator
# @GL-charter-version: 2.0.0

/**
 * Execution-Grounded Reality Harness: Oracle Validator
 * 
 * Core Philosophy: "所有結論 → 必須經過反例測試"
 * (All conclusions must be tested with counterexamples)
 * 
 * Purpose: Validate system behavior against trusted oracles
 * 
 * This module enforces:
 * - All behavior must be validated against oracles
 * - All outputs must be checked against oracle predictions
 * - All edge cases must be covered by oracles
 * - Oracle violations must be critical findings
 */

import { 
  OracleValidationResult,
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class OracleValidator {
  private findings: VerificationFinding[] = [];
  private oracles: Map<string, any> = new Map();

  /**
   * Validate against oracle
   */
  async validateOracle(component: string, oracle: string): Promise<OracleValidationResult> {
    this.findings = [];
    
    // Load oracle
    const oracleData = await this.loadOracle(oracle);
    
    if (!oracleData) {
      this.findings.push({
        id: this.generateId(),
        type: 'INCONSISTENCY',
        severity: VerificationSeverity.HIGH,
        component,
        location: {
          module: component
        },
        title: 'Oracle Not Found',
        description: `Oracle '${oracle}' not found - cannot validate`,
        evidence: [{
          type: 'oracle',
          source: oracle,
          content: { oracle, status: 'not found' },
          timestamp: new Date(),
          verified: false
        }],
        timestamp: new Date(),
        verified: false,
        falsifiable: true
      });
      
      return {
        oracleValidated: false,
        violations: this.extractViolations()
      };
    }
    
    // Validate component against oracle
    await this.validateAgainstOracle(component, oracleData);
    
    return {
      oracleValidated: this.findings.length === 0,
      violations: this.extractViolations()
    };
  }

  /**
   * Load oracle
   */
  private async loadOracle(oracle: string): Promise<any | null> {
    // Check if oracle is already loaded
    if (this.oracles.has(oracle)) {
      return this.oracles.get(oracle);
    }
    
    // Try to load from file
    const oraclePath = this.getOraclePath(oracle);
    
    try {
      const fs = require('fs').promises;
      const content = await fs.readFile(oraclePath, 'utf-8');
      const oracleData = JSON.parse(content);
      
      this.oracles.set(oracle, oracleData);
      return oracleData;
    } catch (error) {
      return null;
    }
  }

  /**
   * Validate component against oracle
   */
  private async validateAgainstOracle(component: string, oracle: any): Promise<void> {
    // Get component implementation
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Validate functions against oracle
      await this.validateFunctionsAgainstOracle(file, content, oracle);
      
      // Validate classes against oracle
      await this.validateClassesAgainstOracle(file, content, oracle);
    }
  }

  /**
   * Validate functions against oracle
   */
  private async validateFunctionsAgainstOracle(file: string, content: string, oracle: any): Promise<void> {
    if (!oracle.functions) return;

    for (const functionName of Object.keys(oracle.functions)) {
      const functionOracle = oracle.functions[functionName];
      
      // Find function in code
      const functionMatch = content.match(
        new RegExp(`function\\s+${functionName}\\s*\\([^)]*\\)\\s*{([^}]*(?:{[^}]*}[^}]*)*)?}`, 's')
      );
      
      if (!functionMatch) {
        this.findings.push({
          id: this.generateId(),
          type: 'INCONSISTENCY',
          severity: VerificationSeverity.HIGH,
          component: file,
          location: {
            file,
            module: file
          },
          title: 'Function Missing',
          description: `Function '${functionName}' specified in oracle but not found in implementation`,
          evidence: [{
            type: 'oracle',
            source: 'oracle',
            content: functionOracle,
            timestamp: new Date(),
            verified: false
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
        continue;
      }
      
      // Validate function signature
      if (functionOracle.signature) {
        const actualSignature = functionMatch[0].split('{')[0];
        if (!this.matchesSignature(actualSignature, functionOracle.signature)) {
          this.findings.push({
            id: this.generateId(),
            type: 'INCONSISTENCY',
            severity: VerificationSeverity.HIGH,
            component: file,
            location: {
              file,
              line: this.getLineNumber(content, functionMatch.index!),
              module: file
            },
            title: 'Function Signature Mismatch',
            description: `Function '${functionName}' signature does not match oracle`,
            evidence: [
              {
                type: 'oracle',
                source: 'oracle',
                content: { expected: functionOracle.signature, actual: actualSignature },
                timestamp: new Date(),
                verified: false
              },
              {
                type: 'code',
                source: file,
                content: actualSignature,
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
      
      // Validate function behavior
      if (functionOracle.behavior) {
        const functionBody = functionMatch[1];
        
        if (functionOracle.behavior.throws && !functionBody.includes('throw')) {
          this.findings.push({
            id: this.generateId(),
            type: 'INCONSISTENCY',
            severity: VerificationSeverity.HIGH,
            component: file,
            location: {
              file,
              line: this.getLineNumber(content, functionMatch.index!),
              module: file
            },
            title: 'Oracle Behavior Violation',
            description: `Function '${functionName}' should throw according to oracle but doesn't`,
            evidence: [
              {
                type: 'oracle',
                source: 'oracle',
                content: functionOracle,
                timestamp: new Date(),
                verified: false
              },
              {
                type: 'code',
                source: file,
                content: functionBody.substring(0, 100),
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

  /**
   * Validate classes against oracle
   */
  private async validateClassesAgainstOracle(file: string, content: string, oracle: any): Promise<void> {
    if (!oracle.classes) return;

    for (const className of Object.keys(oracle.classes)) {
      const classOracle = oracle.classes[className];
      
      // Find class in code
      const classMatch = content.match(
        new RegExp(`class\\s+${className}\\s*\\{([^}]+)}`, 's')
      );
      
      if (!classMatch) {
        this.findings.push({
          id: this.generateId(),
          type: 'INCONSISTENCY',
          severity: VerificationSeverity.HIGH,
          component: file,
          location: {
            file,
            module: file
          },
          title: 'Class Missing',
          description: `Class '${className}' specified in oracle but not found in implementation`,
          evidence: [{
            type: 'oracle',
            source: 'oracle',
            content: classOracle,
            timestamp: new Date(),
            verified: false
          }],
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
        continue;
      }
      
      // Validate class methods
      if (classOracle.methods) {
        for (const methodName of Object.keys(classOracle.methods)) {
          const methodOracle = classOracle.methods[methodName];
          
          const methodMatch = content.match(
            new RegExp(`${methodName}\\s*\\([^)]*\\)\\s*{([^}]*)}`)
          );
          
          if (!methodMatch) {
            this.findings.push({
              id: this.generateId(),
              type: 'INCONSISTENCY',
              severity: VerificationSeverity.HIGH,
              component: file,
              location: {
                file,
                module: file
              },
              title: 'Method Missing',
              description: `Method '${className}.${methodName}' specified in oracle but not found in implementation`,
              evidence: [{
                type: 'oracle',
                source: 'oracle',
                content: methodOracle,
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
  }

  /**
   * Check if signature matches
   */
  private matchesSignature(actual: string, expected: string): boolean {
    // Simplified signature matching
    const normalizedActual = actual.replace(/\s+/g, '').toLowerCase();
    const normalizedExpected = expected.replace(/\s+/g, '').toLowerCase();
    return normalizedActual === normalizedExpected;
  }

  /**
   * Extract violations from findings
   */
  private extractViolations() {
    return this.findings.map(finding => ({
      oracle: finding.location.file,
      expected: finding.evidence[0]?.content,
      actual: finding.evidence[1]?.content,
      violation: finding.description,
      severity: finding.severity
    }));
  }

  /**
   * Set oracle
   */
  setOracle(oracle: string, oracleData: any): void {
    this.oracles.set(oracle, oracleData);
  }

  /**
   * Save oracle to file
   */
  async saveOracle(oracle: string, oracleData: any): Promise<void> {
    const oraclePath = this.getOraclePath(oracle);
    const fs = require('fs').promises;
    
    await fs.writeFile(oraclePath, JSON.stringify(oracleData, null, 2), 'utf-8');
    this.oracles.set(oracle, oracleData);
  }

  /**
   * Get oracle path
   */
  private getOraclePath(oracle: string): string {
    return `/workspace/gl-runtime-platform/.oracles/${oracle}.json`;
  }

  /**
   * Get findings
   */
  getFindings(): VerificationFinding[] {
    return this.findings;
  }

  /**
   * Clear findings
   */
  clearFindings(): void {
    this.findings = [];
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
    return `oracle-validator-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}