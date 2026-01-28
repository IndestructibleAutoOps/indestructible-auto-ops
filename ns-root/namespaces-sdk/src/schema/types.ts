// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/schema
 * @gl-semantic-anchor GL-00-SRC_SCHEMA_TYPES
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Schema Type System and Definitions
 * 
 * Defines TypeScript types and interfaces for schemas, tool metadata,
 * and validation results. Provides type-safe schema construction.
 */

import { JSONSchema } from '../core/tool';

/**
 * Schema type enumeration
 */
export enum SchemaType {
  STRING = 'string',
  NUMBER = 'number',
  INTEGER = 'integer',
  BOOLEAN = 'boolean',
  OBJECT = 'object',
  ARRAY = 'array',
  NULL = 'null'
}

/**
 * Schema format enumeration
 */
export enum SchemaFormat {
  // String formats
  DATE_TIME = 'date-time',
  DATE = 'date',
  TIME = 'time',
  EMAIL = 'email',
  HOSTNAME = 'hostname',
  IPV4 = 'ipv4',
  IPV6 = 'ipv6',
  URI = 'uri',
  URI_REFERENCE = 'uri-reference',
  URI_TEMPLATE = 'uri-template',
  JSON_POINTER = 'json-pointer',
  RELATIVE_JSON_POINTER = 'relative-json-pointer',
  REGEX = 'regex',
  UUID = 'uuid',
  
  // Custom formats
  GITHUB_REPO = 'github-repo',
  SEMVER = 'semver',
  DURATION = 'duration'
}

/**
 * Property schema definition
 */
export interface PropertySchema extends JSONSchema {
  /** Property description */
  description?: string;
  
  /** Default value */
  default?: unknown;
  
  /** Examples */
  examples?: unknown[];
  
  /** Whether property is deprecated */
  deprecated?: boolean;
  
  /** Read-only property */
  readOnly?: boolean;
  
  /** Write-only property */
  writeOnly?: boolean;
}

/**
 * Object schema definition
 */
export interface ObjectSchema extends JSONSchema {
  type: 'object';
  properties: Record<string, PropertySchema>;
  required?: string[];
  additionalProperties?: boolean | JSONSchema;
  minProperties?: number;
  maxProperties?: number;
  dependencies?: Record<string, string[] | JSONSchema>;
  patternProperties?: Record<string, JSONSchema>;
}

/**
 * Array schema definition
 */
export interface ArraySchema extends JSONSchema {
  type: 'array';
  items: JSONSchema | JSONSchema[];
  minItems?: number;
  maxItems?: number;
  uniqueItems?: boolean;
  contains?: JSONSchema;
  minContains?: number;
  maxContains?: number;
}

/**
 * String schema definition
 */
export interface StringSchema extends JSONSchema {
  type: 'string';
  minLength?: number;
  maxLength?: number;
  pattern?: string;
  format?: SchemaFormat | string;
  enum?: string[];
}

/**
 * Number schema definition
 */
export interface NumberSchema extends JSONSchema {
  type: 'number' | 'integer';
  minimum?: number;
  maximum?: number;
  exclusiveMinimum?: number;
  exclusiveMaximum?: number;
  multipleOf?: number;
  enum?: number[];
}

/**
 * Boolean schema definition
 */
export interface BooleanSchema extends JSONSchema {
  type: 'boolean';
  enum?: boolean[];
}

/**
 * Union schema definition (oneOf, anyOf, allOf)
 */
export interface UnionSchema extends JSONSchema {
  oneOf?: JSONSchema[];
  anyOf?: JSONSchema[];
  allOf?: JSONSchema[];
}

/**
 * Schema metadata
 */
export interface SchemaMetadata {
  /** Schema ID */
  $id?: string;
  
  /** Schema version */
  $schema?: string;
  
  /** Schema title */
  title?: string;
  
  /** Schema description */
  description?: string;
  
  /** Schema examples */
  examples?: unknown[];
  
  /** Schema definitions */
  definitions?: Record<string, JSONSchema>;
  
  /** Schema comments */
  $comment?: string;
}

/**
 * Complete schema definition
 */
export interface CompleteSchema extends SchemaMetadata {
  /** Root schema type */
  type?: SchemaType | SchemaType[];
  
  /** Schema properties (for objects) */
  properties?: Record<string, PropertySchema>;
  
  /** Required properties */
  required?: string[];
  
  /** Additional properties */
  additionalProperties?: boolean | JSONSchema;
  
  /** Array items */
  items?: JSONSchema | JSONSchema[];
  
  /** Union schemas */
  oneOf?: JSONSchema[];
  anyOf?: JSONSchema[];
  allOf?: JSONSchema[];
  
  /** Conditional schemas */
  if?: JSONSchema;
  then?: JSONSchema;
  else?: JSONSchema;
  
  /** Enum values */
  enum?: unknown[];
  
  /** Const value */
  const?: unknown;
  
  /** Default value */
  default?: unknown;
}

/**
 * Schema builder for type-safe schema construction
 */
export class SchemaBuilder {
  private schema: Partial<CompleteSchema> = {};

  /**
   * Set schema ID
   */
  id(id: string): this {
    this.schema.$id = id;
    return this;
  }

  /**
   * Set schema title
   */
  title(title: string): this {
    this.schema.title = title;
    return this;
  }

  /**
   * Set schema description
   */
  description(description: string): this {
    this.schema.description = description;
    return this;
  }

  /**
   * Set schema type
   */
  type(type: SchemaType | SchemaType[]): this {
    this.schema.type = type;
    return this;
  }

  /**
   * Add object properties
   */
  properties(properties: Record<string, PropertySchema>): this {
    this.schema.properties = properties;
    return this;
  }

  /**
   * Set required properties
   */
  required(...properties: string[]): this {
    this.schema.required = properties;
    return this;
  }

  /**
   * Set additional properties
   */
  additionalProperties(allowed: boolean | JSONSchema): this {
    this.schema.additionalProperties = allowed;
    return this;
  }

  /**
   * Set array items schema
   */
  items(items: JSONSchema | JSONSchema[]): this {
    this.schema.items = items;
    return this;
  }

  /**
   * Set enum values
   */
  enum(...values: unknown[]): this {
    this.schema.enum = values;
    return this;
  }

  /**
   * Set default value
   */
  default(value: unknown): this {
    this.schema.default = value;
    return this;
  }

  /**
   * Add examples
   */
  examples(...examples: unknown[]): this {
    this.schema.examples = examples;
    return this;
  }

  /**
   * Add definitions
   */
  definitions(definitions: Record<string, JSONSchema>): this {
    this.schema.definitions = definitions;
    return this;
  }

  /**
   * Set oneOf schemas
   */
  oneOf(...schemas: JSONSchema[]): this {
    this.schema.oneOf = schemas;
    return this;
  }

  /**
   * Set anyOf schemas
   */
  anyOf(...schemas: JSONSchema[]): this {
    this.schema.anyOf = schemas;
    return this;
  }

  /**
   * Set allOf schemas
   */
  allOf(...schemas: JSONSchema[]): this {
    this.schema.allOf = schemas;
    return this;
  }

  /**
   * Build the schema
   */
  build(): JSONSchema {
    return this.schema as JSONSchema;
  }
}

/**
 * Common schema patterns
 */
export class CommonSchemas {
  /**
   * Email schema
   */
  static email(options?: {
    description?: string;
    required?: boolean;
  }): StringSchema {
    return {
      type: 'string',
      format: SchemaFormat.EMAIL,
      description: options?.description || 'Email address'
    };
  }

  /**
   * URL schema
   */
  static url(options?: {
    description?: string;
    required?: boolean;
  }): StringSchema {
    return {
      type: 'string',
      format: SchemaFormat.URI,
      description: options?.description || 'URL'
    };
  }

  /**
   * UUID schema
   */
  static uuid(options?: {
    description?: string;
  }): StringSchema {
    return {
      type: 'string',
      format: SchemaFormat.UUID,
      description: options?.description || 'UUID'
    };
  }

  /**
   * Date-time schema
   */
  static dateTime(options?: {
    description?: string;
  }): StringSchema {
    return {
      type: 'string',
      format: SchemaFormat.DATE_TIME,
      description: options?.description || 'ISO 8601 date-time'
    };
  }

  /**
   * Positive integer schema
   */
  static positiveInteger(options?: {
    description?: string;
    maximum?: number;
  }): NumberSchema {
    return {
      type: 'integer',
      minimum: 1,
      maximum: options?.maximum,
      description: options?.description || 'Positive integer'
    };
  }

  /**
   * Non-negative integer schema
   */
  static nonNegativeInteger(options?: {
    description?: string;
    maximum?: number;
  }): NumberSchema {
    return {
      type: 'integer',
      minimum: 0,
      maximum: options?.maximum,
      description: options?.description || 'Non-negative integer'
    };
  }

  /**
   * Percentage schema (0-100)
   */
  static percentage(options?: {
    description?: string;
  }): NumberSchema {
    return {
      type: 'number',
      minimum: 0,
      maximum: 100,
      description: options?.description || 'Percentage (0-100)'
    };
  }

  /**
   * GitHub repository schema
   */
  static githubRepo(options?: {
    description?: string;
  }): StringSchema {
    return {
      type: 'string',
      format: SchemaFormat.GITHUB_REPO,
      pattern: '^[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$',
      description: options?.description || 'GitHub repository (owner/repo)'
    };
  }

  /**
   * Semantic version schema
   */
  static semver(options?: {
    description?: string;
  }): StringSchema {
    return {
      type: 'string',
      format: SchemaFormat.SEMVER,
      pattern: '^\\d+\\.\\d+\\.\\d+(-[a-zA-Z0-9.-]+)?(\\+[a-zA-Z0-9.-]+)?$',
      description: options?.description || 'Semantic version (e.g., 1.0.0)'
    };
  }

  /**
   * Pagination schema
   */
  static pagination(): ObjectSchema {
    return {
      type: 'object',
      properties: {
        page: {
          type: 'integer',
          minimum: 1,
          default: 1,
          description: 'Page number'
        },
        pageSize: {
          type: 'integer',
          minimum: 1,
          maximum: 100,
          default: 20,
          description: 'Items per page'
        }
      },
      additionalProperties: false
    };
  }

  /**
   * Timestamp range schema
   */
  static timestampRange(): ObjectSchema {
    return {
      type: 'object',
      properties: {
        start: {
          type: 'string',
          format: SchemaFormat.DATE_TIME,
          description: 'Start timestamp'
        },
        end: {
          type: 'string',
          format: SchemaFormat.DATE_TIME,
          description: 'End timestamp'
        }
      },
      required: ['start', 'end'],
      additionalProperties: false
    };
  }

  /**
   * Error response schema
   */
  static errorResponse(): ObjectSchema {
    return {
      type: 'object',
      properties: {
        code: {
          type: 'string',
          description: 'Error code'
        },
        message: {
          type: 'string',
          description: 'Error message'
        },
        details: {
          type: 'object',
          description: 'Additional error details'
        }
      },
      required: ['code', 'message'],
      additionalProperties: false
    };
  }
}

/**
 * Create a new schema builder
 */
export function createSchema(): SchemaBuilder {
  return new SchemaBuilder();
}

/**
 * Type guard for object schema
 */
export function isObjectSchema(schema: JSONSchema): schema is ObjectSchema {
  return schema.type === 'object';
}

/**
 * Type guard for array schema
 */
export function isArraySchema(schema: JSONSchema): schema is ArraySchema {
  return schema.type === 'array';
}

/**
 * Type guard for string schema
 */
export function isStringSchema(schema: JSONSchema): schema is StringSchema {
  return schema.type === 'string';
}

/**
 * Type guard for number schema
 */
export function isNumberSchema(schema: JSONSchema): schema is NumberSchema {
  return schema.type === 'number' || schema.type === 'integer';
}