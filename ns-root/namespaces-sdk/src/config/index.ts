/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/config
 * @gl-semantic-anchor GL-00-SRC_CONFIG_INDEX
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Configuration Management
 * 
 * Centralizes configuration loading, validation, and environment management.
 */

import * as fs from 'fs/promises';
import * as path from 'path';

/**
 * Configuration schema
 */
export interface SDKConfig {
  /** SDK version */
  version?: string;
  
  /** Environment name */
  environment?: string;
  
  /** Service configuration */
  service?: {
    name?: string;
    version?: string;
  };
  
  /** Logging configuration */
  logging?: {
    level?: string;
    format?: string;
    enabled?: boolean;
  };
  
  /** Tracing configuration */
  tracing?: {
    enabled?: boolean;
    samplingRate?: number;
    serviceName?: string;
  };
  
  /** Metrics configuration */
  metrics?: {
    enabled?: boolean;
    prefix?: string;
  };
  
  /** Audit configuration */
  audit?: {
    enabled?: boolean;
    retentionDays?: number;
  };
  
  /** Credential configuration */
  credentials?: {
    providers?: string[];
    defaultProvider?: string;
  };
  
  /** Plugin configuration */
  plugins?: {
    autoLoad?: boolean;
    directories?: string[];
  };
  
  /** Custom configuration */
  [key: string]: unknown;
}

/**
 * Configuration source
 */
export enum ConfigSource {
  FILE = 'file',
  ENV = 'env',
  DEFAULT = 'default',
  OVERRIDE = 'override'
}

/**
 * Configuration entry
 */
interface ConfigEntry {
  value: unknown;
  source: ConfigSource;
}

/**
 * Config manager options
 */
export interface ConfigManagerOptions {
  /** Configuration file path */
  configPath?: string;
  
  /** Environment name */
  environment?: string;
  
  /** Environment variable prefix */
  envPrefix?: string;
  
  /** Allow environment variable overrides */
  allowEnvOverrides?: boolean;
  
  /** Default configuration */
  defaults?: SDKConfig;
}

/**
 * Configuration Manager Class
 * 
 * Responsibilities:
 * - Load configuration from multiple sources
 * - Support environment-specific overrides
 * - Validate configuration against schema
 * - Provide type-safe configuration access
 */
export class ConfigManager {
  private config: Map<string, ConfigEntry> = new Map();
  private options: ConfigManagerOptions;
  private loaded: boolean = false;

  constructor(environment?: string, options?: ConfigManagerOptions) {
    this.options = {
      environment: environment || process.env.NODE_ENV || 'development',
      envPrefix: 'SDK_',
      allowEnvOverrides: true,
      ...options
    };
  }

  /**
   * Load configuration
   */
  async load(): Promise<void> {
    if (this.loaded) {
      return;
    }

    // Load default configuration
    if (this.options.defaults) {
      this.loadDefaults(this.options.defaults);
    }

    // Load configuration file
    if (this.options.configPath) {
      await this.loadFile(this.options.configPath);
    } else {
      // Try to load from default locations
      await this.loadDefaultFiles();
    }

    // Load environment-specific configuration
    await this.loadEnvironmentConfig();

    // Load environment variable overrides
    if (this.options.allowEnvOverrides) {
      this.loadEnvOverrides();
    }

    this.loaded = true;
  }

  /**
   * Get configuration value
   */
  get<T = unknown>(key: string, defaultValue?: T): T {
    const entry = this.config.get(key);
    
    if (entry === undefined) {
      return defaultValue as T;
    }

    return entry.value as T;
  }

  /**
   * Set configuration value
   */
  set(key: string, value: unknown, source: ConfigSource = ConfigSource.OVERRIDE): void {
    this.config.set(key, { value, source });
  }

  /**
   * Check if configuration key exists
   */
  has(key: string): boolean {
    return this.config.has(key);
  }

  /**
   * Get all configuration
   */
  getAll(): SDKConfig {
    const config: Record<string, unknown> = {};

    for (const [key, entry] of this.config.entries()) {
      this.setNestedValue(config, key, entry.value);
    }

    return config;
  }

  /**
   * Get configuration source
   */
  getSource(key: string): ConfigSource | undefined {
    return this.config.get(key)?.source;
  }

  /**
   * Validate configuration
   */
  validate(): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Add validation logic here
    // For now, just return valid

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Reload configuration
   */
  async reload(): Promise<void> {
    this.config.clear();
    this.loaded = false;
    await this.load();
  }

  /**
   * Export configuration as JSON
   */
  toJSON(): unknown {
    return this.getAll();
  }

  /**
   * Load default configuration
   */
  private loadDefaults(defaults: SDKConfig): void {
    this.loadObject(defaults, ConfigSource.DEFAULT);
  }

  /**
   * Load configuration from file
   */
  private async loadFile(filePath: string): Promise<void> {
    try {
      const content = await fs.readFile(filePath, 'utf-8');
      const config = JSON.parse(content);
      this.loadObject(config, ConfigSource.FILE);
    } catch (error) {
      if (error instanceof Error && 'code' in error && error.code !== 'ENOENT') {
        throw error;
      }
      // File doesn't exist, skip
    }
  }

  /**
   * Load configuration from default file locations
   */
  private async loadDefaultFiles(): Promise<void> {
    const defaultPaths = [
      'config.json',
      '.sdkrc',
      '.sdkrc.json',
      path.join(process.cwd(), 'config.json'),
      path.join(process.cwd(), '.sdkrc')
    ];

    for (const filePath of defaultPaths) {
      try {
        await this.loadFile(filePath);
        return; // Stop after first successful load
      } catch (error) {
        // Continue to next path
      }
    }
  }

  /**
   * Load environment-specific configuration
   */
  private async loadEnvironmentConfig(): Promise<void> {
    const envConfigPath = path.join(
      process.cwd(),
      'config',
      `${this.options.environment}.json`
    );

    try {
      await this.loadFile(envConfigPath);
    } catch (error) {
      // Environment config is optional
    }
  }

  /**
   * Load environment variable overrides
   */
  private loadEnvOverrides(): void {
    const prefix = this.options.envPrefix || '';

    for (const [key, value] of Object.entries(process.env)) {
      if (key.startsWith(prefix) && value !== undefined) {
        const configKey = key
          .substring(prefix.length)
          .toLowerCase()
          .replace(/_/g, '.');

        this.config.set(configKey, {
          value: this.parseEnvValue(value),
          source: ConfigSource.ENV
        });
      }
    }
  }

  /**
   * Load configuration from object
   */
  private loadObject(obj: unknown, source: ConfigSource, prefix: string = ''): void {
    for (const [key, value] of Object.entries(obj)) {
      const fullKey = prefix ? `${prefix}.${key}` : key;

      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        this.loadObject(value, source, fullKey);
      } else {
        this.config.set(fullKey, { value, source });
      }
    }
  }

  /**
   * Parse environment variable value
   */
  private parseEnvValue(value: string): unknown {
    // Try to parse as JSON
    if (value.startsWith('{') || value.startsWith('[')) {
      try {
        return JSON.parse(value);
      } catch {
        return value;
      }
    }

    // Parse boolean
    if (value === 'true') return true;
    if (value === 'false') return false;

    // Parse number
    if (/^\d+$/.test(value)) {
      return parseInt(value, 10);
    }

    if (/^\d+\.\d+$/.test(value)) {
      return parseFloat(value);
    }

    return value;
  }

  /**
   * Check if property name is safe (not a prototype pollution vector)
   */
  private isSafePropertyName(name: string): boolean {
    const dangerousNames = ['__proto__', 'constructor', 'prototype'];
    return !dangerousNames.includes(name);
  }

  /**
   * Safely get property value without prototype chain traversal
   */
  private safeGetProperty(obj: Record<string, unknown>, key: string): unknown {
    if (!this.isSafePropertyName(key)) {
      throw new Error(`Invalid property name: ${key}`);
    }
    const descriptor = Object.getOwnPropertyDescriptor(obj, key);
    return descriptor ? descriptor.value : undefined;
  }

  /**
   * Set nested value in object using safe property assignment
   * @security Protected against prototype pollution via property name validation,
   * Object.getOwnPropertyDescriptor for safe reads, and Object.defineProperty for safe writes
   */
  private setNestedValue(obj: Record<string, unknown>, path: string, value: unknown): void {
    const parts = path.split('.');
    
    // Validate all parts before any assignment
    for (const part of parts) {
      if (!this.isSafePropertyName(part)) {
        throw new Error(`Invalid property name: ${part}`);
      }
    }
    
    let current: Record<string, unknown> = obj;

    for (let i = 0; i < parts.length - 1; i++) {
      const part = parts[i];
      
      const existing = this.safeGetProperty(current, part);
      if (existing === undefined) {
        // Use Object.defineProperty for safe property creation
        const newObj: Record<string, unknown> = {};
        Object.defineProperty(current, part, {
          value: newObj,
          writable: true,
          enumerable: true,
          configurable: true
        });
        current = newObj;
      } else {
        current = existing as Record<string, unknown>;
      }
    }

    const lastPart = parts[parts.length - 1];
    
    // Use Object.defineProperty for safe final assignment
    Object.defineProperty(current, lastPart, {
      value: value,
      writable: true,
      enumerable: true,
      configurable: true
    });
  }
}

/**
 * Create a configuration manager instance
 */
export function createConfigManager(
  environment?: string,
  options?: ConfigManagerOptions
): ConfigManager {
  return new ConfigManager(environment, options);
}