// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/schema
 * @gl-semantic-anchor GL-00-SRC_SCHEMA_REGISTRY
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Schema Registry and Versioning
 * 
 * Manages registration, lookup, and versioning of all schemas used in the SDK.
 * Supports dynamic schema loading and compatibility checks.
 */

import { JSONSchema } from '../core/tool';
import { SDKError, ErrorCode } from '../core/errors';
import { Logger } from '../observability/logger';

/**
 * Schema version information
 */
export interface SchemaVersion {
  /** Version string (semantic versioning) */
  version: string;
  
  /** Schema definition */
  schema: JSONSchema;
  
  /** Registration timestamp */
  registeredAt: Date;
  
  /** Whether this version is deprecated */
  deprecated?: boolean;
  
  /** Deprecation message */
  deprecationMessage?: string;
  
  /** Migration guide to newer version */
  migrationGuide?: string;
}

/**
 * Schema entry in registry
 */
interface SchemaEntry {
  /** Schema name/ID */
  name: string;
  
  /** All versions of this schema */
  versions: Map<string, SchemaVersion>;
  
  /** Latest version */
  latestVersion: string;
  
  /** Schema metadata */
  metadata?: {
    description?: string;
    category?: string;
    tags?: string[];
  };
}

/**
 * Schema compatibility check result
 */
export interface CompatibilityResult {
  /** Whether schemas are compatible */
  compatible: boolean;
  
  /** Compatibility issues if any */
  issues?: string[];
  
  /** Breaking changes */
  breakingChanges?: string[];
}

/**
 * Schema Registry Class
 * 
 * Responsibilities:
 * - Register and retrieve schemas by name and version
 * - Support schema migration and compatibility checks
 * - Enforce immutability of published schemas
 * - Support dynamic schema loading
 */
export class SchemaRegistry {
  private schemas: Map<string, SchemaEntry> = new Map();
  private logger: Logger;
  private immutable: boolean;

  constructor(logger: Logger, options?: { immutable?: boolean }) {
    this.logger = logger;
    this.immutable = options?.immutable !== false;
  }

  /**
   * Register a schema
   * @param name Schema name/ID
   * @param version Schema version
   * @param schema Schema definition
   * @param options Registration options
   */
  register(
    name: string,
    version: string,
    schema: JSONSchema,
    options?: {
      metadata?: {
        description?: string;
        category?: string;
        tags?: string[];
      };
      setAsLatest?: boolean;
    }
  ): void {
    // Validate version format
    this.validateVersion(version);

    // Get or create schema entry
    let entry = this.schemas.get(name);
    
    if (!entry) {
      entry = {
        name,
        versions: new Map(),
        latestVersion: version,
        metadata: options?.metadata
      };
      this.schemas.set(name, entry);
    }

    // Check if version already exists
    if (entry.versions.has(version)) {
      if (this.immutable) {
        throw new SDKError(
          ErrorCode.SCHEMA_VERSION_MISMATCH,
          `Schema version already exists and is immutable: ${name}@${version}`
        );
      }
      
      this.logger.warn('Overwriting existing schema version', {
        name,
        version
      });
    }

    // Register the version
    const schemaVersion: SchemaVersion = {
      version,
      schema,
      registeredAt: new Date()
    };

    entry.versions.set(version, schemaVersion);

    // Update latest version if requested or if this is the first version
    if (options?.setAsLatest || entry.versions.size === 1) {
      entry.latestVersion = version;
    }

    this.logger.info('Schema registered', {
      name,
      version,
      isLatest: entry.latestVersion === version
    });
  }

  /**
   * Get a schema by name and version
   * @param name Schema name
   * @param version Schema version (optional, defaults to latest)
   * @returns Schema or undefined if not found
   */
  get(name: string, version?: string): JSONSchema | undefined {
    const entry = this.schemas.get(name);
    
    if (!entry) {
      return undefined;
    }

    const targetVersion = version || entry.latestVersion;
    const schemaVersion = entry.versions.get(targetVersion);

    if (!schemaVersion) {
      return undefined;
    }

    // Log warning if deprecated
    if (schemaVersion.deprecated) {
      this.logger.warn('Using deprecated schema version', {
        name,
        version: targetVersion,
        message: schemaVersion.deprecationMessage
      });
    }

    return schemaVersion.schema;
  }

  /**
   * Get schema version information
   * @param name Schema name
   * @param version Schema version
   * @returns Schema version info or undefined
   */
  getVersion(name: string, version: string): SchemaVersion | undefined {
    const entry = this.schemas.get(name);
    return entry?.versions.get(version);
  }

  /**
   * Get latest version of a schema
   * @param name Schema name
   * @returns Latest schema or undefined
   */
  getLatest(name: string): JSONSchema | undefined {
    return this.get(name);
  }

  /**
   * Get all versions of a schema
   * @param name Schema name
   * @returns Array of version strings
   */
  getVersions(name: string): string[] {
    const entry = this.schemas.get(name);
    return entry ? Array.from(entry.versions.keys()) : [];
  }

  /**
   * Check if a schema exists
   * @param name Schema name
   * @param version Optional version
   * @returns true if schema exists
   */
  has(name: string, version?: string): boolean {
    const entry = this.schemas.get(name);
    
    if (!entry) {
      return false;
    }

    if (!version) {
      return true;
    }

    return entry.versions.has(version);
  }

  /**
   * Deprecate a schema version
   * @param name Schema name
   * @param version Schema version
   * @param message Deprecation message
   * @param migrationGuide Optional migration guide
   */
  deprecate(
    name: string,
    version: string,
    message: string,
    migrationGuide?: string
  ): void {
    const entry = this.schemas.get(name);
    
    if (!entry) {
      throw new SDKError(
        ErrorCode.SCHEMA_NOT_FOUND,
        `Schema not found: ${name}`
      );
    }

    const schemaVersion = entry.versions.get(version);
    
    if (!schemaVersion) {
      throw new SDKError(
        ErrorCode.SCHEMA_NOT_FOUND,
        `Schema version not found: ${name}@${version}`
      );
    }

    schemaVersion.deprecated = true;
    schemaVersion.deprecationMessage = message;
    schemaVersion.migrationGuide = migrationGuide;

    this.logger.info('Schema version deprecated', {
      name,
      version,
      message
    });
  }

  /**
   * Check compatibility between two schema versions
   * @param name Schema name
   * @param fromVersion Source version
   * @param toVersion Target version
   * @returns Compatibility result
   */
  checkCompatibility(
    name: string,
    fromVersion: string,
    toVersion: string
  ): CompatibilityResult {
    const fromSchema = this.get(name, fromVersion);
    const toSchema = this.get(name, toVersion);

    if (!fromSchema || !toSchema) {
      throw new SDKError(
        ErrorCode.SCHEMA_NOT_FOUND,
        `Schema version not found: ${name}`
      );
    }

    return this.compareSchemas(fromSchema, toSchema);
  }

  /**
   * List all registered schemas
   * @returns Array of schema names
   */
  list(): string[] {
    return Array.from(this.schemas.keys());
  }

  /**
   * Get registry statistics
   */
  getStats(): {
    totalSchemas: number;
    totalVersions: number;
    schemas: Array<{
      name: string;
      versions: number;
      latestVersion: string;
    }>;
  } {
    const schemas = Array.from(this.schemas.values()).map(entry => ({
      name: entry.name,
      versions: entry.versions.size,
      latestVersion: entry.latestVersion
    }));

    const totalVersions = schemas.reduce((sum, s) => sum + s.versions, 0);

    return {
      totalSchemas: this.schemas.size,
      totalVersions,
      schemas
    };
  }

  /**
   * Clear all schemas
   */
  clear(): void {
    const count = this.schemas.size;
    this.schemas.clear();
    this.logger.info('Schema registry cleared', { count });
  }

  /**
   * Export registry as JSON
   */
  toJSON(): unknown {
    const schemas: Record<string, unknown> = {};

    for (const [name, entry] of this.schemas.entries()) {
      schemas[name] = {
        latestVersion: entry.latestVersion,
        metadata: entry.metadata,
        versions: Array.from(entry.versions.entries()).map(([version, info]) => ({
          version,
          deprecated: info.deprecated,
          deprecationMessage: info.deprecationMessage,
          registeredAt: info.registeredAt.toISOString()
        }))
      };
    }

    return {
      immutable: this.immutable,
      schemaCount: this.schemas.size,
      schemas
    };
  }

  /**
   * Validate version format (semantic versioning)
   */
  private validateVersion(version: string): void {
    const versionRegex = /^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$/;
    
    if (!versionRegex.test(version)) {
      throw new SDKError(
        ErrorCode.INVALID_SCHEMA,
        `Invalid version format: ${version}. Expected semantic versioning (e.g., 1.0.0)`
      );
    }
  }

  /**
   * Compare two schemas for compatibility
   */
  private compareSchemas(
    fromSchema: JSONSchema,
    toSchema: JSONSchema
  ): CompatibilityResult {
    const issues: string[] = [];
    const breakingChanges: string[] = [];

    // Check type changes
    if (fromSchema.type !== toSchema.type) {
      breakingChanges.push(
        `Type changed from ${fromSchema.type} to ${toSchema.type}`
      );
    }

    // Check required properties (for objects)
    if (fromSchema.type === 'object' && toSchema.type === 'object') {
      const fromRequired = new Set(fromSchema.required || []);
      const toRequired = new Set(toSchema.required || []);

      // New required properties are breaking changes
      for (const prop of toRequired) {
        if (!fromRequired.has(prop)) {
          breakingChanges.push(`New required property: ${prop}`);
        }
      }

      // Removed properties are breaking changes
      const fromProps = new Set(Object.keys(fromSchema.properties || {}));
      const toProps = new Set(Object.keys(toSchema.properties || {}));

      for (const prop of fromProps) {
        if (!toProps.has(prop)) {
          breakingChanges.push(`Removed property: ${prop}`);
        }
      }
    }

    // Check enum values
    if (fromSchema.enum && toSchema.enum) {
      const fromEnum = new Set(fromSchema.enum);
      const toEnum = new Set(toSchema.enum);

      for (const value of fromEnum) {
        if (!toEnum.has(value)) {
          breakingChanges.push(`Removed enum value: ${value}`);
        }
      }
    }

    const compatible = breakingChanges.length === 0;

    return {
      compatible,
      issues: issues.length > 0 ? issues : undefined,
      breakingChanges: breakingChanges.length > 0 ? breakingChanges : undefined
    };
  }
}