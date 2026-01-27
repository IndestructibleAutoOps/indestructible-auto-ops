/**
 * @module schema_validator
 * @description JSON Schema validation with comprehensive error reporting
 * @gl-governed
 * GL Unified Charter Activated
 * @gl-layer GL-30-EXECUTION
 * @gl-module engine/validator
 * @gl-semantic-anchor GL-30-EXEC-TS
 * @gl-evidence-required true
 * @version 1.0.0
 * @since 2026-01-24
 * @author MachineNativeOps Team
 */

import Ajv, { KeywordDefinition, SchemaObject, ErrorObject } from 'ajv';
import { ValidatorInterface, ValidationResult, EvidenceRecord } from '../interfaces.d';
import type { ConfigObject, SchemaValidationInput, AjvError } from '../types';

/**
 * Schema Validator
 * 
 * GL30-49: Execution Layer - Validator Stage
 * 
 * Validates configuration against JSON Schema with
 * comprehensive error reporting and evidence generation.
 */
export class SchemaValidator implements ValidatorInterface {
  private evidence: EvidenceRecord[] = [];
  private readonly ajv: Ajv;

  constructor(options?: {
    allErrors?: boolean;
    strict?: boolean;
  }) {
    this.ajv = new Ajv({
      allErrors: options?.allErrors ?? true,
      strict: options?.strict ?? true,
      verbose: true,
      coerceTypes: false
    });
  }

  /**
   * Validate configuration against schema
   */
  async validate(
    config: ConfigObject,
    schema: ConfigObject,
    configPath: string = 'root'
  ): Promise<ValidationResult> {
    const startTime = Date.now();

    try {
      // Compile schema
      const validate = this.ajv.compile(schema as SchemaObject);

      // Validate config
      const valid = validate(config);

      // Collect errors
      const errors: string[] = [];
      if (!valid && validate.errors) {
        for (const error of validate.errors) {
          errors.push(this.formatError(error, configPath));
        }
      }

      // Generate evidence record
      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'validator',
        component: 'schema_validator',
        action: 'validate',
        status: valid ? 'success' : 'error',
        input: { path: configPath, schemaKeys: Object.keys(schema) },
        output: {
          valid,
          errorCount: errors.length,
          errors: errors.slice(0, 10) // Limit in evidence
        },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        valid,
        errors,
        warnings: [],
        duration: Date.now() - startTime,
        evidence: this.evidence
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);

      this.evidence.push({
        timestamp: new Date().toISOString(),
        stage: 'validator',
        component: 'schema_validator',
        action: 'validate',
        status: 'error',
        input: { path: configPath },
        output: { error: errorMsg },
        metrics: { duration: Date.now() - startTime }
      });

      return {
        valid: false,
        errors: [errorMsg],
        warnings: [],
        duration: Date.now() - startTime,
        evidence: this.evidence
      };
    }
  }

  /**
   * Validate multiple configurations
   */
  async validateBatch(
    configs: Map<string, SchemaValidationInput>
  ): Promise<Map<string, ValidationResult>> {
    const results: Map<string, ValidationResult> = new Map();

    for (const [path, { config, schema }] of configs.entries()) {
      const result = await this.validate(config, schema, path);
      results.set(path, result);
    }

    return results;
  }

  /**
   * Format AJV error message
   */
  private formatError(error: ErrorObject, path: string): string {
    const dataPath = error.instancePath ? `${path}${error.instancePath}` : path;
    const keyword = error.keyword;
    const message = error.message || 'Validation error';
    const params = error.params as Record<string, unknown>;

    switch (keyword) {
      case 'required':
        return `Required property missing: ${params.missingProperty} at ${dataPath}`;
      case 'type':
        return `Type mismatch at ${dataPath}: expected ${params.type}, got ${typeof error.data}`;
      case 'additionalProperties':
        return `Additional property not allowed: ${params.additionalProperty} at ${dataPath}`;
      case 'enum':
        return `Invalid value at ${dataPath}: must be one of ${(params.allowedValues as unknown[]).join(', ')}`;
      case 'minimum':
        return `Value at ${dataPath} must be >= ${params.limit}`;
      case 'maximum':
        return `Value at ${dataPath} must be <= ${params.limit}`;
      case 'minLength':
        return `String at ${dataPath} must have minimum length of ${params.limit}`;
      case 'maxLength':
        return `String at ${dataPath} must have maximum length of ${params.limit}`;
      case 'pattern':
        return `String at ${dataPath} does not match pattern: ${params.pattern}`;
      case 'format':
        return `String at ${dataPath} does not match format: ${params.format}`;
      default:
        return `${message} at ${dataPath}`;
    }
  }

  /**
   * Add custom keyword
   */
  addKeyword(keyword: string, definition: KeywordDefinition): void {
    this.ajv.addKeyword({ keyword, ...definition });
  }

  /**
   * Add schema to registry
   */
  addSchema(schema: ConfigObject, id?: string): void {
    this.ajv.addSchema(schema as SchemaObject, id);
  }

  /**
   * Get evidence records
   */
  getEvidence(): EvidenceRecord[] {
    return this.evidence;
  }
}