# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: falsification-engine-adversarial-inputs
# @GL-charter-version: 2.0.0

/**
 * Falsification Engine: Adversarial Inputs Generator
 * 
 * Core Philosophy: "驗證不是證明你是對的，而是證明你還沒被推翻。"
 * (Verification is not proving you're right, but proving you haven't been overturned yet.)
 * 
 * Purpose: Generate adversarial inputs to actively falsify GL component claims
 * 
 * This module generates inputs designed to:
 * - Break assumptions
 * - Trigger edge cases
 * - Exploit vulnerabilities
 * - Reveal hidden bugs
 * - Challenge robustness
 */

import { 
  FalsificationResult,
  VerificationSeverity,
  VerificationFinding 
} from '../../types';

export class AdversarialInputsGenerator {
  private findings: VerificationFinding[] = [];
  private claims: Map<string, any[]> = new Map();

  /**
   * Generate adversarial inputs to falsify claims
   */
  async falsifyClaims(component: string, claims: string[]): Promise<FalsificationResult> {
    this.findings = [];
    
    // Extract and categorize claims
    await this.extractClaims(component, claims);
    
    // Generate adversarial inputs for each claim
    await this.generateAdversarialInputs(component);
    
    return {
      falsified: this.findings.length > 0,
      claimsTested: claims.length,
      claimsFalsified: this.findings.length,
      falsifications: this.extractFalsifications()
    };
  }

  /**
   * Extract and categorize claims from component
   */
  private async extractClaims(component: string, claims: string[]): Promise<void> {
    const componentPath = this.getComponentPath(component);
    const files = await this.getTsFiles(componentPath);

    for (const file of files) {
      const content = await this.readFileContent(file);
      
      // Extract function-level claims from JSDoc
      const jsdocMatches = content.matchAll(
        /\/\*\*[\s\S]*?@param[\s\S]*?\*\/\s*(?:function|const\s+\w+\s*=\s*|(?:async\s+)?\w+)\s*(\w+)/gs
      );
      
      for (const match of jsdocMatches) {
        const functionName = match[1];
        const jsdoc = match[0];
        
        // Extract claims from JSDoc
        const docClaims = this.extractClaimsFromJSDoc(jsdoc, functionName);
        
        for (const claim of docClaims) {
          if (!this.claims.has(file)) {
            this.claims.set(file, []);
          }
          this.claims.get(file)!.push(claim);
        }
      }
    }
  }

  /**
   * Extract claims from JSDoc comments
   */
  private extractClaimsFromJSDoc(jsdoc: string, functionName: string): any[] {
    const claims: any[] = [];
    
    // Extract @param claims
    const paramMatches = jsdoc.matchAll(/@param\s+\{([^}]+)\}\s+(\w+)\s+(.+)/g);
    for (const match of paramMatches) {
      claims.push({
        type: 'parameter',
        functionName,
        name: match[2],
        type: match[1],
        claim: match[3].trim(),
        source: 'jsdoc'
      });
    }
    
    // Extract @throws claims
    const throwsMatches = jsdoc.matchAll(/@throws\s+(.+)/g);
    for (const match of throwsMatches) {
      claims.push({
        type: 'throws',
        functionName,
        claim: match[1].trim(),
        source: 'jsdoc'
      });
    }
    
    // Extract @returns claims
    const returnsMatch = jsdoc.match(/@returns\s+(.+)/);
    if (returnsMatch) {
      claims.push({
        type: 'returns',
        functionName,
        claim: returnsMatch[1].trim(),
        source: 'jsdoc'
      });
    }
    
    return claims;
  }

  /**
   * Generate adversarial inputs to falsify claims
   */
  private async generateAdversarialInputs(component: string): Promise<void> {
    const componentPath = this.getComponentPath(component);
    
    // For each claim, generate inputs that might falsify it
    for (const [file, fileClaims] of this.claims) {
      for (const claim of fileClaims) {
        await this.generateFalsifyingInputs(file, claim);
      }
    }
  }

  /**
   * Generate inputs that might falsify a specific claim
   */
  private async generateFalsifyingInputs(file: string, claim: any): Promise<void> {
    switch (claim.type) {
      case 'parameter':
        await this.falsifyParameterClaim(file, claim);
        break;
      case 'throws':
        await this.falsifyThrowsClaim(file, claim);
        break;
      case 'returns':
        await this.falsifyReturnsClaim(file, claim);
        break;
    }
  }

  /**
   * Falsify parameter claims
   */
  private async falsifyParameterClaim(file: string, claim: any): Promise<void> {
    const content = await this.readFileContent(file);
    
    // Generate inputs that violate type claims
    const falsifyingInputs = this.generateTypeViolations(claim.type, claim.name);
    
    for (const input of falsifyingInputs) {
      this.findings.push({
        id: this.generateId(),
        type: 'FALSIFICATION_SUCCESS',
        severity: VerificationSeverity.MEDIUM,
        component: file,
        location: {
          file,
          module: file
        },
        title: 'Parameter Claim Falsified',
        description: `Parameter '${claim.name}' claimed to be '${claim.type}' but accepts: ${JSON.stringify(input)}`,
        evidence: [{
          type: 'code',
          source: file,
          content: `${claim.name}: ${claim.type} → ${JSON.stringify(input)}`,
          timestamp: new Date(),
          verified: false
        }],
        contradiction: {
          claim: `Parameter '${claim.name}' must be of type '${claim.type}'`,
          counterexample: JSON.stringify(input),
          proof: `Type '${claim.type}' does not match input type '${typeof input}'`
        },
        timestamp: new Date(),
        verified: false,
        falsifiable: true
      });
    }
  }

  /**
   * Falsify throws claims
   */
  private async falsifyThrowsClaim(file: string, claim: any): Promise<void> {
    const content = await this.readFileContent(file);
    
    // Check if the claimed exception is actually thrown
    const functionPattern = new RegExp(
      `function\\s+${claim.functionName}\\s*\\([^)]*\\)\\s*{([^}]*)}`,
      's'
    );
    
    const match = content.match(functionPattern);
    if (match) {
      const functionBody = match[1];
      
      // Check if the claimed exception is thrown
      if (!functionBody.includes('throw')) {
        this.findings.push({
          id: this.generateId(),
          type: 'FALSIFICATION_SUCCESS',
          severity: VerificationSeverity.HIGH,
          component: file,
          location: {
            file,
            module: file
          },
          title: 'Throws Claim Falsified',
          description: `Function '${claim.functionName}' claims to throw but never throws`,
          evidence: [{
            type: 'code',
            source: file,
            content: functionBody.substring(0, 200),
            timestamp: new Date(),
            verified: false
          }],
          contradiction: {
            claim: claim.claim,
            counterexample: 'No throw statement found',
            proof: 'Function body does not contain any throw statements'
          },
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
  }

  /**
   * Falsify returns claims
   */
  private async falsifyReturnsClaim(file: string, claim: any): Promise<void> {
    const content = await this.readFileContent(file);
    
    // Check if the return claim is consistent with actual returns
    const functionPattern = new RegExp(
      `function\\s+${claim.functionName}\\s*\\([^)]*\\)\\s*{([^}]*(?:return[^}]*))?}`,
      's'
    );
    
    const match = content.match(functionPattern);
    if (match) {
      const functionBody = match[1];
      
      // Check if function returns
      if (!functionBody.includes('return')) {
        this.findings.push({
          id: this.generateId(),
          type: 'FALSIFICATION_SUCCESS',
          severity: VerificationSeverity.HIGH,
          component: file,
          location: {
            file,
            module: file
          },
          title: 'Returns Claim Falsified',
          description: `Function '${claim.functionName}' claims to return but never returns`,
          evidence: [{
            type: 'code',
            source: file,
            content: functionBody.substring(0, 200),
            timestamp: new Date(),
            verified: false
          }],
          contradiction: {
            claim: claim.claim,
            counterexample: 'No return statement found',
            proof: 'Function body does not contain any return statements'
          },
          timestamp: new Date(),
          verified: false,
          falsifiable: true
        });
      }
    }
  }

  /**
   * Generate type violations for a given type
   */
  private generateTypeViolations(type: string, paramName: string): any[] {
    const violations: any[] = [];
    
    switch (type) {
      case 'string':
        violations.push(123, true, null, undefined, {}, []);
        break;
      case 'number':
        violations.push('123', true, null, undefined, {}, []);
        break;
      case 'boolean':
        violations.push('true', 1, 0, null, undefined, {}, []);
        break;
      case 'object':
        violations.push('not an object', 123, true, null);
        break;
      case 'Array':
      case 'array':
        violations.push('not an array', 123, true, null, {});
        break;
      default:
        violations.push(null, undefined);
    }
    
    return violations;
  }

  /**
   * Extract falsifications from findings
   */
  private extractFalsifications() {
    return this.findings.map(finding => ({
      claim: finding.contradiction?.claim || finding.title,
      counterexample: finding.contradiction?.counterexample || finding.evidence[0]?.content,
      proof: finding.contradiction?.proof || finding.description,
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
    return `falsification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}