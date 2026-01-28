// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/schema
 * @gl-semantic-anchor GL-00-SRC_SCHEMA_VALIDATOR
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Schema Validation Engine
 * 
 * Implements core schema validation logic, supporting both static and dynamic
 * validation of tool inputs and outputs using JSON Schema.
 */

import Ajv, { ValidateFunction, ErrorObject } from 'ajv';
import addFormats from 'ajv-formats';
import { JSONSchema } from '../core/tool';
import { ValidationError, ErrorCode } from '../core/errors';
import { Logger } from '../observability/logger';

/**
 * Validation result
 */
export interface ValidationResult {
  /** Whether validation passed */
  valid: boolean;
  
  /** Validation errors if any */
  errors?: ValidationErrorDetail[];
  
  /** Validated data (may be coerced) */
  data?: Record<string, unknown>;
}

/**
 * Detailed validation error
 */
export interface ValidationErrorDetail {
  /** Error path in the data */
  path: string;
  
  /** Error message */
  message: string;
  
  /** Error keyword (e.g., 'required', 'type') */
  keyword: string;
  
  /** Schema path */
  schemaPath: string;
  
  /** Additional error parameters */
  params?: Record<string, any>;
}

/**
 * Validator options
 */
export interface ValidatorOptions {
  /** Allow additional properties not in schema */
  allowAdditionalProperties?: boolean;
  
  /** Coerce types (e.g., string to number) */
  coerceTypes?: boolean;
  
  /** Remove additional properties */
  removeAdditional?: boolean | 'all' | 'failing';
  
  /** Use defaults from schema */
  useDefaults?: boolean;
  
  /** Strict mode */
  strict?: boolean;
}

/**
 * Schema Validator Class
 * 
 * Responsibilities:
 * - Validate data against JSON Schema definitions
 * - Support both synchronous and asynchronous validation
 * - Provide clear error messages and validation reports
 * - Cache compiled schemas for performance
 */
export class SchemaValidator {
  private ajv: Ajv;
  private logger: Logger;
  private compiledSchemas: Map<string, ValidateFunction> = new Map();

  constructor(logger: Logger, options: ValidatorOptions = {}) {
    this.logger = logger;
    
    // Initialize Ajv with options
    this.ajv = new Ajv({
      allErrors: true,
      verbose: true,
      strict: options.strict !== false,
      coerceTypes: options.coerceTypes || false,
      useDefaults: options.useDefaults !== false,
      removeAdditional: options.removeAdditional || false,
      allowUnionTypes: true
    });

    // Add format validators
    addFormats(this.ajv);

    // Add custom formats if needed
    this.addCustomFormats();
  }

  /**
   * Validate data against a schema
   * @param data Data to validate
   * @param schema JSON Schema
   * @param options Validation options
   * @returns Validation result
   */
  async validate(
    data: Record<string, unknown>,
    schema: JSONSchema,
    options?: ValidatorOptions
  ): Promise<ValidationResult> {
    try {
      // Get or compile schema
      const schemaKey = this.getSchemaKey(schema);
      let validateFn = this.compiledSchemas.get(schemaKey);

      if (!validateFn) {
        validateFn = this.ajv.compile(schema);
        this.compiledSchemas.set(schemaKey, validateFn);
        this.logger.debug('Schema compiled and cached', { schemaKey });
      }

      // Clone data to avoid mutation
      const dataToValidate = JSON.parse(JSON.stringify(data));

      // Validate
      const valid = validateFn(dataToValidate);

      if (valid) {
        return {
          valid: true,
          data: dataToValidate
        };
      }

      // Format errors
      const errors = this.formatErrors(validateFn.errors || []);

      this.logger.debug('Validation failed', {
        schemaKey,
        errorCount: errors.length,
        errors
      });

      return {
        valid: false,
        errors,
        data: dataToValidate
      };

    } catch (error) {
      this.logger.error('Validation error', error);
      
      throw new ValidationError(
        'Schema validation failed',
        [{
          path: '',
          message: error instanceof Error ? error.message : String(error),
          keyword: 'error',
          schemaPath: ''
        }]
      );
    }
  }

  /**
   * Validate and throw on error
   * @param data Data to validate
   * @param schema JSON Schema
   * @param options Validation options
   * @returns Validated data
   * @throws ValidationError if validation fails
   */
  async validateOrThrow(
    data: Record<string, unknown>,
    schema: JSONSchema,
    options?: ValidatorOptions
  ): Promise<unknown> {
    const result = await this.validate(data, schema, options);

    if (!result.valid) {
      throw new ValidationError(
        'Validation failed',
        result.errors || []
      );
    }

    return result.data;
  }

  /**
   * Validate synchronously
   * @param data Data to validate
   * @param schema JSON Schema
   * @returns Validation result
   */
  validateSync(data: Record<string, unknown>, schema: JSONSchema): ValidationResult {
    try {
      const schemaKey = this.getSchemaKey(schema);
      let validateFn = this.compiledSchemas.get(schemaKey);

      if (!validateFn) {
        validateFn = this.ajv.compile(schema);
        this.compiledSchemas.set(schemaKey, validateFn);
      }

      const dataToValidate = JSON.parse(JSON.stringify(data));
      const valid = validateFn(dataToValidate);

      if (valid) {
        return { valid: true, data: dataToValidate };
      }

      return {
        valid: false,
        errors: this.formatErrors(validateFn.errors || []),
        data: dataToValidate
      };

    } catch (error) {
      throw new ValidationError(
        'Schema validation failed',
        [{
          path: '',
          message: error instanceof Error ? error.message : String(error),
          keyword: 'error',
          schemaPath: ''
        }]
      );
    }
  }

  /**
   * Add a schema to the validator
   * @param schemaId Schema ID
   * @param schema JSON Schema
   */
  addSchema(schemaId: string, schema: JSONSchema): void {
    try {
      this.ajv.addSchema(schema, schemaId);
      this.logger.debug('Schema added', { schemaId });
    } catch (error) {
      this.logger.error('Failed to add schema', error);
      throw error;
    }
  }

  /**
   * Remove a schema from the validator
   * @param schemaId Schema ID
   */
  removeSchema(schemaId: string): void {
    this.ajv.removeSchema(schemaId);
    this.compiledSchemas.delete(schemaId);
    this.logger.debug('Schema removed', { schemaId });
  }

  /**
   * Clear all cached schemas
   */
  clearCache(): void {
    this.compiledSchemas.clear();
    this.logger.debug('Schema cache cleared');
  }

  /**
   * Get cache statistics
   */
  getCacheStats(): {
    size: number;
    schemas: string[];
  } {
    return {
      size: this.compiledSchemas.size,
      schemas: Array.from(this.compiledSchemas.keys())
    };
  }

  /**
   * Format Ajv errors into our error format
   */
  private formatErrors(ajvErrors: ErrorObject[]): ValidationErrorDetail[] {
    return ajvErrors.map(error => ({
      path: error.instancePath || '/',
      message: (error instanceof Error ? error.message : String(error)) || 'Validation failed',
      keyword: error.keyword,
      schemaPath: error.schemaPath,
      params: error.params
    }));
  }

  /**
   * Generate a cache key for a schema
   */
  private getSchemaKey(schema: JSONSchema): string {
    // Use schema $id if available, otherwise generate hash
    if (schema.$id) {
      return schema.$id;
    }

    // Simple hash based on stringified schema
    const schemaStr = JSON.stringify(schema);
    let hash = 0;
    for (let i = 0; i < schemaStr.length; i++) {
      const char = schemaStr.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return `schema_${hash}`;
  }

  /**
   * Add custom format validators
   */
  private addCustomFormats(): void {
    // Add custom formats here if needed
    
    // Example: GitHub repository format
    this.ajv.addFormat('github-repo', {
      type: 'string',
      validate: (data: string) => {
        return /^[a-zA-Z0-9_-]+\/[a-zA-Z0-9_-]+$/.test(data);
      }
    });

    // Example: Semantic version format
    this.ajv.addFormat('semver', {
      type: 'string',
      validate: (data: string) => {
        return /^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$/.test(data);
      }
    });

    // Example: ISO 8601 duration format
    this.ajv.addFormat('duration', {
      type: 'string',
      validate: (data: string) => {
        return /^P(?:\d+Y)?(?:\d+M)?(?:\d+D)?(?:T(?:\d+H)?(?:\d+M)?(?:\d+(?:\.\d+)?S)?)?$/.test(data);
      }
    });

    this.logger.debug('Custom formats added');
  }
}

/**
 * Schema validation utilities
 */
export class SchemaUtils {
  /**
   * Merge two schemas
   */
  static mergeSchemas(base: JSONSchema, override: JSONSchema): JSONSchema {
    return {
      ...base,
      ...override,
      properties: {
        ...base.properties,
        ...override.properties
      },
      required: [
        ...(base.required || []),
        ...(override.required || [])
      ].filter((v, i, a) => a.indexOf(v) === i) // Remove duplicates
    };
  }

  /**
   * Create a schema for an object with specific properties
   */
  static createObjectSchema(
    properties: Record<string, JSONSchema>,
    required?: string[],
    options?: {
      additionalProperties?: boolean;
      description?: string;
    }
  ): JSONSchema {
    return {
      type: 'object',
      properties,
      required: required || [],
      additionalProperties: options?.additionalProperties !== false,
      description: options?.description
    };
  }

  /**
   * Create a schema for an array
   */
  static createArraySchema(
    items: JSONSchema,
    options?: {
      minItems?: number;
      maxItems?: number;
      uniqueItems?: boolean;
      description?: string;
    }
  ): JSONSchema {
    return {
      type: 'array',
      items,
      minItems: options?.minItems,
      maxItems: options?.maxItems,
      uniqueItems: options?.uniqueItems,
      description: options?.description
    };
  }

  /**
   * Create a schema for a string with constraints
   */
  static createStringSchema(options?: {
    minLength?: number;
    maxLength?: number;
    pattern?: string;
    format?: string;
    enum?: string[];
    description?: string;
  }): JSONSchema {
    return {
      type: 'string',
      minLength: options?.minLength,
      maxLength: options?.maxLength,
      pattern: options?.pattern,
      format: options?.format,
      enum: options?.enum,
      description: options?.description
    };
  }

  /**
   * Create a schema for a number with constraints
   */
  static createNumberSchema(options?: {
    minimum?: number;
    maximum?: number;
    multipleOf?: number;
    description?: string;
  }): JSONSchema {
    return {
      type: 'number',
      minimum: options?.minimum,
      maximum: options?.maximum,
      multipleOf: options?.multipleOf,
      description: options?.description
    };
  }

  /**
   * Create a schema for an enum
   */
  static createEnumSchema(
    values: unknown[],
    description?: string
  ): JSONSchema {
    return {
      type: 'string' as const,
      enum: values,
      description
    };
  }

  /**
   * Create a union schema (oneOf)
   */
  static createUnionSchema(
    schemas: JSONSchema[],
    description?: string
  ): JSONSchema {
    return {
      type: 'object' as const,
      oneOf: schemas,
      description
    };
  }
}