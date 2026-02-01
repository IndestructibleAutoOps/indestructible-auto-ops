// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: policy-engine
// @GL-charter-version: 2.0.0

import Ajv from 'ajv';
import { EventStreamManager } from '../events/event-stream-manager';
import { createLogger } from '../utils/logger';

const logger = createLogger('PolicyEngine');

export interface ValidationResult {
  valid: boolean;
  error?: string;
  violations?: any[];
}

export interface PolicyConfig {
  schemaValidation: boolean;
  namingValidation: boolean;
  pathValidation: boolean;
  semanticValidation: boolean;
  governanceTagValidation: boolean;
}

export class PolicyEngine {
  private ajv: Ajv;
  private eventStream: EventStreamManager;
  private policies: PolicyConfig;

  constructor() {
    this.ajv = new Ajv({ allErrors: true });
    this.eventStream = new EventStreamManager();
    this.policies = {
      schemaValidation: true,
      namingValidation: true,
      pathValidation: true,
      semanticValidation: true,
      governanceTagValidation: true
    };
  }

  public async validate(input: any, config: any): Promise<ValidationResult> {
    const violations: any[] = [];

    // Schema validation
    if (this.policies.schemaValidation && config.schema) {
      const schemaResult = this.validateSchema(input, config.schema);
      if (!schemaResult.valid) {
        violations.push({
          type: 'schema',
          violations: schemaResult.violations
        });
      }
    }

    // Naming validation
    if (this.policies.namingValidation) {
      const namingResult = this.validateNaming(input);
      if (!namingResult.valid) {
        violations.push({
          type: 'naming',
          violations: namingResult.violations
        });
      }
    }

    // Path validation
    if (this.policies.pathValidation && input.filePath) {
      const pathResult = this.validatePath(input.filePath);
      if (!pathResult.valid) {
        violations.push({
          type: 'path',
          violations: pathResult.violations
        });
      }
    }

    // Semantic validation
    if (this.policies.semanticValidation) {
      const semanticResult = this.validateSemantic(input);
      if (!semanticResult.valid) {
        violations.push({
          type: 'semantic',
          violations: semanticResult.violations
        });
      }
    }

    // Governance tag validation
    if (this.policies.governanceTagValidation) {
      const governanceResult = this.validateGovernanceTags(input);
      if (!governanceResult.valid) {
        violations.push({
          type: 'governance',
          violations: governanceResult.violations
        });
      }
    }

    const isValid = violations.length === 0;

    // Log validation event
    await this.eventStream.logEvent({
      eventType: 'policy_validation',
      layer: 'GL90-99',
      semanticAnchor: 'GL-ROOT-GOVERNANCE',
      timestamp: new Date().toISOString(),
      metadata: {
        valid: isValid,
        violationsCount: violations.length,
        violations: violations
      }
    });

    return {
      valid: isValid,
      error: isValid ? undefined : 'Policy validation failed',
      violations: violations.length > 0 ? violations : undefined
    };
  }

  private validateSchema(input: any, schema: any): ValidationResult {
    const validate = this.ajv.compile(schema);
    const valid = validate(input);
    
    return {
      valid: !!valid,
      violations: valid ? undefined : (validate.errors || undefined)
    };
  }

  private validateNaming(input: any): ValidationResult {
    const violations: string[] = [];

    if (input.filePath) {
      const filename = input.filePath.split('/').pop();
      
      // Check for kebab-case in filenames
      if (filename && !/^[a-z0-9-]+(\.[a-z]+)?$/.test(filename)) {
        violations.push(`Filename ${filename} does not follow kebab-case convention`);
      }
    }

    return {
      valid: violations.length === 0,
      violations: violations.length > 0 ? violations : undefined
    };
  }

  private validatePath(filePath: string): ValidationResult {
    const violations: string[] = [];

    // Check path structure
    if (filePath.includes('..')) {
      violations.push('Path contains parent directory reference (..)');
    }

    // Check for absolute paths
    if (filePath.startsWith('/')) {
      violations.push('Absolute paths are not allowed');
    }

    // Check path length
    if (filePath.length > 255) {
      violations.push('Path length exceeds 255 characters');
    }

    return {
      valid: violations.length === 0,
      violations: violations.length > 0 ? violations : undefined
    };
  }

  private validateSemantic(input: any): ValidationResult {
    const violations: string[] = [];

    // Check for required semantic anchors
    if (!input.semanticAnchor && !input.metadata?.semanticAnchor) {
      violations.push('Missing semantic anchor');
    }

    // Check for GL layer specification
    if (!input.layer && !input.metadata?.layer) {
      violations.push('Missing GL layer specification');
    }

    // Check for charter version
    if (!input.charterVersion && !input.metadata?.charterVersion) {
      violations.push('Missing charter version');
    }

    return {
      valid: violations.length === 0,
      violations: violations.length > 0 ? violations : undefined
    };
  }

  private validateGovernanceTags(input: any): ValidationResult {
    const violations: string[] = [];

    // Check for @GL-governed tag
    const content = input.content || '';
    if (!content.includes('@GL-governed')) {
      violations.push('Missing @GL-governed tag');
    }

    // Check for @GL-layer tag
    if (!content.includes('@GL-layer')) {
      violations.push('Missing @GL-layer tag');
    }

    // Check for @GL-semantic tag
    if (!content.includes('@GL-semantic')) {
      violations.push('Missing @GL-semantic tag');
    }

    return {
      valid: violations.length === 0,
      violations: violations.length > 0 ? violations : undefined
    };
  }

  public setPolicies(policies: PolicyConfig): void {
    this.policies = { ...this.policies, ...policies };
  }
}