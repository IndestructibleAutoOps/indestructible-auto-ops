/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/credentials/providers
 * @gl-semantic-anchor GL-00-CREDENTI_PROVIDER_FILE
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * File-based Credential Provider
 * 
 * Loads credentials from JSON, YAML, or .env files.
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { CredentialProvider, Credential, CredentialType } from '../types';

/**
 * File provider options
 */
export interface FileProviderOptions {
  /** Path to credentials file */
  path: string;
  
  /** File format */
  format?: 'json' | 'yaml' | 'env';
  
  /** Whether to watch file for changes */
  watch?: boolean;
  
  /** Encryption key for encrypted files */
  encryptionKey?: string;
}

/**
 * File Credential Provider
 * 
 * Loads credentials from a file with support for JSON, YAML, and .env formats.
 */
export class FileCredentialProvider implements CredentialProvider {
  public readonly name = 'file';
  private options: FileProviderOptions;
  private credentials: Map<string, Credential> = new Map();
  private watcher?: unknown;

  constructor(options: FileProviderOptions) {
    this.options = {
      format: 'json',
      watch: false,
      ...options
    };
  }

  async initialize(): Promise<void> {
    await this.loadCredentials();

    if (this.options.watch) {
      await this.startWatching();
    }
  }

  async getCredential(key: string, scope?: string): Promise<Credential | undefined> {
    const cacheKey = this.getCacheKey(key, scope);
    return this.credentials.get(cacheKey);
  }

  async setCredential(credential: Credential): Promise<void> {
    const cacheKey = this.getCacheKey(credential.key, credential.scope);
    this.credentials.set(cacheKey, credential);
    await this.saveCredentials();
  }

  async deleteCredential(key: string, scope?: string): Promise<void> {
    const cacheKey = this.getCacheKey(key, scope);
    this.credentials.delete(cacheKey);
    await this.saveCredentials();
  }

  async listCredentials(): Promise<string[]> {
    return Array.from(this.credentials.keys());
  }

  supports(operation: string): boolean {
    return ['get', 'set', 'delete', 'list'].includes(operation);
  }

  async cleanup(): Promise<void> {
    if (this.watcher) {
      this.watcher.close();
      this.watcher = undefined;
    }
  }

  /**
   * Load credentials from file
   */
  private async loadCredentials(): Promise<void> {
    try {
      const content = await fs.readFile(this.options.path, 'utf-8');
      const data = this.parseContent(content);

      this.credentials.clear();

      for (const [key, value] of Object.entries(data)) {
        const credential: Credential = {
          key,
          value: typeof value === 'string' ? value : JSON.stringify(value),
          type: CredentialType.CUSTOM,
          metadata: {
            source: 'file',
            filePath: this.options.path
          }
        };

        this.credentials.set(key, credential);
      }
    } catch (error) {
      if (error instanceof Error && 'code' in error && error.code === 'ENOENT') {
        // File doesn't exist, start with empty credentials
        this.credentials.clear();
      } else {
        throw error;
      }
    }
  }

  /**
   * Save credentials to file
   */
  private async saveCredentials(): Promise<void> {
    const data: Record<string, string> = {};

    for (const [key, credential] of this.credentials.entries()) {
      data[credential.key] = credential.value;
    }

    const content = this.formatContent(data);

    // Ensure directory exists
    const dir = path.dirname(this.options.path);
    await fs.mkdir(dir, { recursive: true });

    // Write file
    await fs.writeFile(this.options.path, content, 'utf-8');
  }

  /**
   * Parse file content based on format
   */
  private parseContent(content: string): Record<string, any> {
    switch (this.options.format) {
      case 'json':
        return JSON.parse(content);
      
      case 'env':
        return this.parseEnvFormat(content);
      
      case 'yaml':
        // YAML parsing would require a library like 'js-yaml'
        // For now, fall back to JSON
        return JSON.parse(content);
      
      default:
        return JSON.parse(content);
    }
  }

  /**
   * Format content based on format
   */
  private formatContent(data: Record<string, any>): string {
    switch (this.options.format) {
      case 'json':
        return JSON.stringify(data, null, 2);
      
      case 'env':
        return this.formatEnv(data);
      
      case 'yaml':
        // YAML formatting would require a library
        // For now, fall back to JSON
        return JSON.stringify(data, null, 2);
      
      default:
        return JSON.stringify(data, null, 2);
    }
  }

  /**
   * Parse .env format
   */
  private parseEnvFormat(content: string): Record<string, string> {
    const result: Record<string, string> = {};
    const lines = content.split('\n');

    for (const line of lines) {
      const trimmed = line.trim();
      
      // Skip empty lines and comments
      if (!trimmed || trimmed.startsWith('#')) {
        continue;
      }

      const index = trimmed.indexOf('=');
      if (index === -1) {
        continue;
      }

      const key = trimmed.substring(0, index).trim();
      let value = trimmed.substring(index + 1).trim();

      // Remove quotes if present
      if (
        (value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))
      ) {
        value = value.substring(1, value.length - 1);
      }

      result[key] = value;
    }

    return result;
  }

  /**
   * Format as .env
   */
  private formatEnv(data: Record<string, string>): string {
    const lines: string[] = [];

    for (const [key, value] of Object.entries(data)) {
      // Quote value if it contains spaces
      const quotedValue = value.includes(' ') ? `"${value}"` : value;
      lines.push(`${key}=${quotedValue}`);
    }

    return lines.join('\n');
  }

  /**
   * Start watching file for changes
   */
  private async startWatching(): Promise<void> {
    // File watching would require fs.watch or a library like chokidar
    // This is a placeholder for the implementation
  }

  /**
   * Get cache key
   */
  private getCacheKey(key: string, scope?: string): string {
    return scope ? `${key}:${scope}` : key;
  }
}