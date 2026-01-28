// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/credentials/providers
 * @gl-semantic-anchor GL-00-CREDENTI_PROVIDER_ENV
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Environment Variable Credential Provider
 * 
 * Loads credentials from environment variables.
 */

import { CredentialProvider, Credential, CredentialType } from '../types';

/**
 * Environment variable provider options
 */
export interface EnvProviderOptions {
  /** Prefix for environment variables (e.g., 'SDK_') */
  prefix?: string;
  
  /** Variable name mappings (key -> env var name) */
  mappings?: Record<string, string>;
  
  /** Whether to convert keys to uppercase */
  uppercase?: boolean;
}

/**
 * Environment Variable Credential Provider
 * 
 * Loads credentials from process.env with optional prefix and mappings.
 */
export class EnvCredentialProvider implements CredentialProvider {
  public readonly name = 'env';
  private options: EnvProviderOptions;

  constructor(options: EnvProviderOptions = {}) {
    this.options = {
      prefix: '',
      uppercase: true,
      ...options
    };
  }

  async initialize(): Promise<void> {
    // No initialization needed for env provider
  }

  async getCredential(key: string, scope?: string): Promise<Credential | undefined> {
    const envVarName = this.getEnvVarName(key, scope);
    const value = process.env[envVarName];

    if (!value) {
      return undefined;
    }

    return {
      key,
      value,
      scope,
      type: this.inferCredentialType(key),
      metadata: {
        source: 'environment',
        envVarName
      }
    };
  }

  async setCredential(credential: Credential): Promise<void> {
    const envVarName = this.getEnvVarName(credential.key, credential.scope);
    process.env[envVarName] = credential.value;
  }

  async deleteCredential(key: string, scope?: string): Promise<void> {
    const envVarName = this.getEnvVarName(key, scope);
    delete process.env[envVarName];
  }

  async listCredentials(): Promise<string[]> {
    const prefix = this.options.prefix || '';
    const keys: string[] = [];

    for (const key of Object.keys(process.env)) {
      if (key.startsWith(prefix)) {
        keys.push(key.substring(prefix.length));
      }
    }

    return keys;
  }

  supports(operation: string): boolean {
    return ['get', 'set', 'delete', 'list'].includes(operation);
  }

  /**
   * Get environment variable name for a credential key
   */
  private getEnvVarName(key: string, scope?: string): string {
    // Check mappings first
    if (this.options.mappings && this.options.mappings[key]) {
      return this.options.mappings[key];
    }

    // Build env var name
    let envVarName = key;

    if (scope) {
      envVarName = `${key}_${scope}`;
    }

    if (this.options.uppercase) {
      envVarName = envVarName.toUpperCase();
    }

    if (this.options.prefix) {
      envVarName = `${this.options.prefix}${envVarName}`;
    }

    return envVarName;
  }

  /**
   * Infer credential type from key name
   */
  private inferCredentialType(key: string): CredentialType {
    const lowerKey = key.toLowerCase();

    if (lowerKey.includes('token')) {
      return CredentialType.BEARER_TOKEN;
    }

    if (lowerKey.includes('api_key') || lowerKey.includes('apikey')) {
      return CredentialType.API_KEY;
    }

    if (lowerKey.includes('oauth')) {
      return CredentialType.OAUTH_TOKEN;
    }

    if (lowerKey.includes('ssh')) {
      return CredentialType.SSH_KEY;
    }

    return CredentialType.CUSTOM;
  }
}