# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: anti-fabric-contradiction-detector
# @GL-charter-version: 2.0.0

/**
 * Anti-Fabric: Contradiction Detector
 * 
 * Core Philosophy: "任何沒有被推翻的結論，都不算成立。"
 * (Any conclusion not overturned is not established.)
 * 
 * Purpose: Detect direct logical contradictions within GL components
 * 
 * This module actively searches for:
 * - Explicit contradictions in code/logic
 * - Inconsistent assertions
 * - Conflicting statements
 * - Paradoxical conditions
 */

import { 
  ContradictionResult, 
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class ContradictionDetector {
  private findings: VerificationFinding[] = [];

  /**
   * Detect contradictions in a component
   */
  async detectContradictions(component: string): Promise<ContradictionResult> {
    this.findings = [];
    
    // Scan component for contradictions
    await this.scanComponent(component);
    
    return {
      contradicted: this.findings.length > 0,
      contradictions: this.extractContradictions()
    };
  }

  /**
   * Scan component for various contradiction patterns
   */
  private async scanComponent(component: string): Promise<void> {
    // 1. Detect explicit logical contradictions
    await this.detectLogicalContradictions(component);
    
    // 2. Detect assertion conflicts
    await this.detectAssertionConflicts(component);
    
    // 3. Detect condition contradictions
    await this.detectConditionContradictions(component);
    
    // 4. Detect data contradictions
    await this.detectChangesDataContradictions(component);
    
    // 5. Detect semantic contradictions
    await this.detectSemanticContradictions(component);
  }

  /**
   * Detect explicit logical contradictions (A AND NOT A)
   */
  private async detectLogicalContradictions(component: string): Promise<void> {
    const patterns = [
      {
        pattern: /if\s*\(\s*condition\s*\)\s*{\s*[^}]*}\s*else\s*if\s*\(\s*!?\s*condition\s*\)/gs,
        description: 'Contradictory condition: condition and !condition',
        severity: VerificationSeverity.HIGH
      },
      {
        pattern: /return\s+true;\s*[^}]*return\s+false;\s*[^}]*return\s+true/gs,
        description: 'Inconsistent return logic',
        severity: VerificationSeverity.MEDIUM
      },
      {
        pattern: /assert\(.*\);\s*[^}]*assert\(.*!\s*\(.*\)\);/gs,
        description: 'Contradictory assertions',
        severity: VerificationSeverity.CRITICAL
      }
    ];

    // Scan component files for these patterns
    const componentPath = this.getComponentPath(component);
    const files = await this.getComponentFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      for (const { pattern, description, severity } of patterns) {
        const matches = content.matchAll(pattern);
        
        for (const match of matches) {
          this.findings.push({
            id: this.generateId(),
            type: 'CONTRADICTION',
            severity,
            component,
            location: {
              file: file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Logical Contradiction Detected',
            description,
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
   * Detect assertion conflicts
   */
  private async detectAssertionConflicts(component: string): Promise<void> {
    // Find assert statements that contradict each other
    const componentPath = this.getComponentPath(component);
    const files = await this.getComponentFiles(componentPath);

    const assertions: Array<{ file: string; line: number; assertion: string }> = [];

    for (const file of files) {
      const content = await this.readFileContent(file);
      const assertMatches = content.matchAll(/assert\(([^)]+)\)/g);
      
      for (const match of assertMatches) {
        assertions.push({
          file,
          line: this.getLineNumber(content, match.index!),
          assertion: match[1]
        });
      }
    }

    // Check for contradictions between assertions
    for (let i = 0; i < assertions.length; i++) {
      for (let j = i + 1; j < assertions.length; j++) {
        if (this.assertionsContradict(assertions[i].assertion, assertions[j].assertion)) {
          this.findings.push({
            id: this.generateId(),
            type: 'CONTRADICTION',
            severity: VerificationSeverity.HIGH,
            component,
            location: {
              file: assertions[i].file,
              line: assertions[i].line,
              module: component
            },
            title: 'Assertion Conflict Detected',
            description: `Contradictory assertions found:\n  - ${assertions[i].assertion} (line ${assertions[i].line})\n  - ${assertions[j].assertion} (line ${assertions[j].line})`,
            evidence: [
              {
                type: 'code',
                source: assertions[i].file,
                content: assertions[i].assertion,
                timestamp: new Date(),
                verified: true
              },
              {
                type: 'code',
                source: assertions[j].file,
                content: assertions[j].assertion,
                timestamp: new Date(),
                verified: true
              }
            ],
            contradiction: {
              claim: assertions[i].assertion,
              counterexample: assertions[j].assertion,
              proof: `Direct negation found at ${assertions[j].file}:${assertions[j].line}`
            },
            timestamp: new Date(),
            verified: false,
            falsifiable: true
          });
        }
      }
    }
  }

  /**
   * Detect condition contradictions
   */
  private async detectConditionContradictions(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getComponentFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Detect if-else contradictions
      const ifElseMatches = content.matchAll(
        /if\s*\(\s*([^)]+)\)\s*{([^}]+)}\s*else\s*{([^}]+)}/gs
      );
      
      for (const match of ifElseMatches) {
        const condition = match[1];
        const thenBlock = match[2];
        const elseBlock = match[3];

        // Check if both blocks produce the same result
        if (this.blocksProduceSameResult(thenBlock, elseBlock)) {
          const line = this.getLineNumber(content, match.index!);
          
          this.findings.push({
            id: this.generateId(),
            type: 'CONTRADICTION',
            severity: VerificationSeverity.MEDIUM,
            component,
            location: {
              file,
              line,
              module: component
            },
            title: 'Condition Contradiction Detected',
            description: `Condition '${condition}' produces identical results in both branches`,
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
   * Detect inconsistencies in data
   */
  private async detectInconsistentDataContradictions(component: string): Promise<void> {
    // Check for data structure inconsistencies
    const componentPath = this.getComponentPath(component);
    const files = await this.getJsonFiles(componentPath);

    const schemas = new Map<string, any[]>();

    for (const file of files) {
      try {
        const content = await this.readFileContent(file);
        const data = JSON.parse(content);
        
        const schema = this.extractSchema(data);
        const schemaKey = JSON.stringify(schema);
        
        if (!schemas.has(schemaKey)) {
          schemas.set(schemaKey, []);
        }
        schemas.get(schemaKey)!.push({ file, data });
      } catch (error) {
        // Skip invalid JSON
      }
    }

    // Compare schemas for contradictions
    const schemaEntries = Array.from(schemas.entries());
    for (let i = 0; i < schemaEntries.length; i++) {
      for (let j = i + 1; j < schemaEntries.length; j++) {
        if (this.schemasContradict(schemaEntries[i][0], schemaEntries[j][0])) {
          this.findings.push({
            id: this.generateId(),
            type: 'CONTRADICTION',
            severity: VerificationSeverity.HIGH,
            component,
            location: {
              module: component
            },
            title: 'Data Schema Contradiction Detected',
            description: `Inconsistent data schemas found in ${schemaEntries[i][1].length} vs ${schemaEntries[j][1].length} files`,
            evidence: [
              {
                type: 'data',
                source: schemaEntries[i][1][0].file,
                content: schemaEntries[i][1][0].data,
                timestamp: new Date(),
                verified: true
              },
              {
                type: 'data',
                source: schemaEntries[j][1][0].file,
                content: schemaEntries[j][1][0].data,
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
   * Detect semantic contradictions
   */
  private async detectSemanticContradictions(component: string): Promise<void> {
    // Check for semantic mismatches between names and implementations
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Detect function name vs implementation contradictions
      const functionMatches = content.matchAll(
        /(?:function|const\s+\w+\s*=\s*|(?:async\s+)?\w+)\s*(\w+)\s*\([^)]*\)\s*{([^}]*(?:{[^}]*}[^}]*)*)}/gs
      );
      
      for (const match of functionMatches) {
        const functionName = match[1];
        const implementation = match[2];
        
        if (this.nameImplementationContradicts(functionName, implementation)) {
          this.findings.push({
            id: this.generateId(),
            type: 'SEMANTIC_MISMATCH',
            severity: VerificationSeverity.MEDIUM,
            component,
            location: {
              file,
              line: this.getLineNumber(content, match.index!),
              module: component
            },
            title: 'Semantic Contradiction Detected',
            description: `Function '${functionName}' has contradictory implementation`,
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
   * Extract contradictions from findings
   */
  private extractContradictions() {
    return this.findings.map(finding => ({
      statement1: finding.evidence[0]?.content || '',
      statement2: finding.evidence[1]?.content || '',
      location1: `${finding.location.file}:${finding.location.line}`,
      location2: finding.evidence[1]?.source || finding.location.file,
      severity: finding.severity,
      explanation: finding.description
    }));
  }

  // ============================================================================
  // Helper Methods
  // ============================================================================

  private getComponentPath(component: string): string {
    return `/workspace/gl-runtime-platform/${component}`;
  }

  private async getComponentFiles(path: string): Promise<string[]> {
    const { exec } = require('child_process');
    return new Promise((resolve, reject) => {
      exec(`find ${path} -type f -name "*.ts" -o -name "*.js" -o -name "*.json"`, (error, stdout) => {
        if (error) reject(error);
        else resolve(stdout.trim().split('\n').filter(f => f));
      });
    });
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

  private async getJsonFiles(path: string): Promise<string[]> {
    const { exec } = require('child_process');
    return new Promise((resolve, reject) => {
      exec(`find ${path} -type f -name "*.json"`, (error, stdout) => {
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
    return `contradiction-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private assertionsContradict(assert1: string, assert2: string): boolean {
    // Check if one assertion is the negation of another
    const negationPattern = /!\s*\(*\s*(\w+)\s*\)*/;
    
    const normalized1 = assert1.replace(/\s+/g, '');
    const normalized2 = assert2.replace(/\s+/g, '');
    
    // Direct negation
    if (normalized1 === '!' + normalized2 || normalized2 === '!' + normalized1) {
      return true;
    }
    
    // Negation with parentheses
    const match1 = normalized1.match(negationPattern);
    const match2 = normalized2.match(negationPattern);
    
    if (match1 && match2 && match1[1] === match2[1]) {
      return true;
    }
    
    return false;
  }

  private blocksProduceSameResult(block1: string, block2: string): boolean {
    const normalize = (block: string) => block.replace(/\s+/g, '');
    return normalize(block1) === normalize(block2);
  }

  private extractSchema(data: any): any {
    if (Array.isArray(data)) {
      return data.length > 0 ? this.extractSchema(data[0]) : 'array';
    }
    if (typeof data === 'object' && data !== null) {
      const schema: any = {};
      for (const key of Object.keys(data)) {
        schema[key] = typeof data[key];
      }
      return schema;
    }
    return typeof data;
  }

  private schemasContradict(schema1: string, schema2: string): boolean {
    const s1 = JSON.parse(schema1);
    const s2 = JSON.parse(schema2);
    
    // Check if schemas have contradictory property types
    for (const key of Object.keys(s1)) {
      if (s2[key] && s1[key] !== s2[key]) {
        return true;
      }
    }
    
    return false;
  }

  private nameImplementationContradicts(name: string, implementation: string): Promise<boolean> {
    return Promise.resolve(false); // Simplified for now
  }
}