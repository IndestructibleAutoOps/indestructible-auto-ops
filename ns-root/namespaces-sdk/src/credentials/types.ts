/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/credentials
 * @gl-semantic-anchor GL-00-SRC_CREDENTI_TYPES
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Credential Types and Interfaces
 * 
 * Defines types and interfaces for credentials, tokens, and provider configurations.
 */

/**
 * Credential interface
 */
export interface Credential {
  /** Credential key/identifier */
  key: string;
  
  /** Credential value (token, API key, password, etc.) */
  value: string;
  
  /** Credential scope (e.g., 'repo', 'user', 'admin') */
  scope?: string;
  
  /** Credential type */
  type?: CredentialType;
  
  /** Expiration date */
  expiresAt?: Date;
  
  /** Additional metadata */
  metadata?: Record<string, any>;
}

/**
 * Credential type enumeration
 */
export enum CredentialType {
  /** API key */
  API_KEY = 'api_key',
  
  /** OAuth token */
  OAUTH_TOKEN = 'oauth_token',
  
  /** Bearer token */
  BEARER_TOKEN = 'bearer_token',
  
  /** Basic auth (username:password) */
  BASIC_AUTH = 'basic_auth',
  
  /** SSH key */
  SSH_KEY = 'ssh_key',
  
  /** Certificate */
  CERTIFICATE = 'certificate',
  
  /** Service account key */
  SERVICE_ACCOUNT = 'service_account',
  
  /** Custom credential type */
  CUSTOM = 'custom'
}

/**
 * Credential configuration
 */
export interface CredentialConfig {
  /** Provider name */
  provider: string;
  
  /** Provider-specific configuration */
  config?: Record<string, any>;
  
  /** Credential mappings */
  mappings?: Record<string, string>;
}

/**
 * Credential provider interface
 */
export interface CredentialProvider {
  /** Provider name */
  name: string;
  
  /**
   * Initialize the provider
   */
  initialize?(): Promise<void>;
  
  /**
   * Get a credential by key
   * @param key Credential key
   * @param scope Optional credential scope
   * @returns Credential or undefined if not found
   */
  getCredential(key: string, scope?: string): Promise<Credential | undefined>;
  
  /**
   * Set a credential
   * @param credential Credential to set
   */
  setCredential(credential: Credential): Promise<void>;
  
  /**
   * Delete a credential
   * @param key Credential key
   * @param scope Optional credential scope
   */
  deleteCredential(key: string, scope?: string): Promise<void>;
  
  /**
   * List all credential keys
   * @returns Array of credential keys
   */
  listCredentials?(): Promise<string[]>;
  
  /**
   * Check if provider supports a specific operation
   * @param operation Operation name
   * @returns true if supported
   */
  supports?(operation: string): boolean;
  
  /**
   * Cleanup provider resources
   */
  cleanup?(): Promise<void>;
}

/**
 * OAuth token credential
 */
export interface OAuthCredential extends Credential {
  type: CredentialType.OAUTH_TOKEN;
  
  /** Access token */
  accessToken: string;
  
  /** Refresh token */
  refreshToken?: string;
  
  /** Token type (e.g., 'Bearer') */
  tokenType?: string;
  
  /** Token scopes */
  scopes?: string[];
  
  /** Token expiration timestamp */
  expiresAt?: Date;
}

/**
 * API key credential
 */
export interface ApiKeyCredential extends Credential {
  type: CredentialType.API_KEY;
  
  /** API key value */
  apiKey: string;
  
  /** API key name/identifier */
  keyName?: string;
  
  /** Associated user/account */
  userId?: string;
}

/**
 * Basic auth credential
 */
export interface BasicAuthCredential extends Credential {
  type: CredentialType.BASIC_AUTH;
  
  /** Username */
  username: string;
  
  /** Password */
  password: string;
}

/**
 * SSH key credential
 */
export interface SshKeyCredential extends Credential {
  type: CredentialType.SSH_KEY;
  
  /** Private key */
  privateKey: string;
  
  /** Public key */
  publicKey?: string;
  
  /** Passphrase */
  passphrase?: string;
}

/**
 * Certificate credential
 */
export interface CertificateCredential extends Credential {
  type: CredentialType.CERTIFICATE;
  
  /** Certificate content */
  certificate: string;
  
  /** Private key */
  privateKey?: string;
  
  /** Certificate chain */
  chain?: string[];
  
  /** Certificate format (PEM, DER, etc.) */
  format?: string;
}

/**
 * Service account credential
 */
export interface ServiceAccountCredential extends Credential {
  type: CredentialType.SERVICE_ACCOUNT;
  
  /** Service account email/identifier */
  email: string;
  
  /** Private key */
  privateKey: string;
  
  /** Project ID */
  projectId?: string;
  
  /** Additional service account data */
  data?: Record<string, any>;
}

/**
 * Credential provider configuration
 */
export interface ProviderConfig {
  /** Provider type */
  type: 'env' | 'file' | 'vault' | 'cloud' | 'custom';
  
  /** Provider name */
  name: string;
  
  /** Provider priority (lower = higher priority) */
  priority?: number;
  
  /** Provider-specific options */
  options?: Record<string, any>;
  
  /** Whether provider is enabled */
  enabled?: boolean;
}

/**
 * Environment variable provider configuration
 */
export interface EnvProviderConfig extends ProviderConfig {
  type: 'env';
  
  options?: {
    /** Prefix for environment variables */
    prefix?: string;
    
    /** Variable name mappings */
    mappings?: Record<string, string>;
  };
}

/**
 * File provider configuration
 */
export interface FileProviderConfig extends ProviderConfig {
  type: 'file';
  
  options: {
    /** Path to credentials file */
    path: string;
    
    /** File format (json, yaml, env) */
    format?: 'json' | 'yaml' | 'env';
    
    /** Whether to watch file for changes */
    watch?: boolean;
  };
}

/**
 * Vault provider configuration
 */
export interface VaultProviderConfig extends ProviderConfig {
  type: 'vault';
  
  options: {
    /** Vault server URL */
    url: string;
    
    /** Vault token */
    token: string;
    
    /** Vault namespace */
    namespace?: string;
    
    /** Secret path prefix */
    pathPrefix?: string;
    
    /** KV version (1 or 2) */
    kvVersion?: 1 | 2;
  };
}

/**
 * Cloud provider configuration (AWS, GCP, Azure)
 */
export interface CloudProviderConfig extends ProviderConfig {
  type: 'cloud';
  
  options: {
    /** Cloud provider type */
    provider: 'aws' | 'gcp' | 'azure';
    
    /** Region */
    region?: string;
    
    /** Secret name prefix */
    prefix?: string;
    
    /** Additional provider-specific options */
    [key: string]: unknown;
  };
}

/**
 * Credential rotation policy
 */
export interface RotationPolicy {
  /** Whether rotation is enabled */
  enabled: boolean;
  
  /** Rotation interval in milliseconds */
  interval: number;
  
  /** Grace period before old credential expires */
  gracePeriod?: number;
  
  /** Rotation strategy */
  strategy?: 'immediate' | 'gradual' | 'blue-green';
  
  /** Notification settings */
  notifications?: {
    /** Notify before rotation */
    beforeRotation?: boolean;
    
    /** Notify after rotation */
    afterRotation?: boolean;
    
    /** Notification channels */
    channels?: string[];
  };
}

/**
 * Credential usage tracking
 */
export interface CredentialUsage {
  /** Credential key */
  key: string;
  
  /** Number of times accessed */
  accessCount: number;
  
  /** Last access timestamp */
  lastAccessedAt: Date;
  
  /** First access timestamp */
  firstAccessedAt: Date;
  
  /** Access history */
  history?: Array<{
    timestamp: Date;
    operation: string;
    success: boolean;
  }>;
}

/**
 * Credential validation result
 */
export interface CredentialValidation {
  /** Whether credential is valid */
  valid: boolean;
  
  /** Validation errors if any */
  errors?: string[];
  
  /** Validation warnings */
  warnings?: string[];
  
  /** Credential strength score (0-100) */
  strength?: number;
  
  /** Expiration status */
  expirationStatus?: 'valid' | 'expiring-soon' | 'expired';
  
  /** Days until expiration */
  daysUntilExpiration?: number;
}

/**
 * Credential security options
 */
export interface SecurityOptions {
  /** Encrypt credentials at rest */
  encryptAtRest?: boolean;
  
  /** Encryption algorithm */
  encryptionAlgorithm?: string;
  
  /** Require secure transport */
  requireSecureTransport?: boolean;
  
  /** Enable audit logging */
  enableAudit?: boolean;
  
  /** Access control list */
  acl?: Array<{
    principal: string;
    permissions: string[];
  }>;
}

/**
 * Type guards
 */

export function isOAuthCredential(
  credential: Credential
): credential is OAuthCredential {
  return credential.type === CredentialType.OAUTH_TOKEN;
}

export function isApiKeyCredential(
  credential: Credential
): credential is ApiKeyCredential {
  return credential.type === CredentialType.API_KEY;
}

export function isBasicAuthCredential(
  credential: Credential
): credential is BasicAuthCredential {
  return credential.type === CredentialType.BASIC_AUTH;
}

export function isSshKeyCredential(
  credential: Credential
): credential is SshKeyCredential {
  return credential.type === CredentialType.SSH_KEY;
}

export function isCertificateCredential(
  credential: Credential
): credential is CertificateCredential {
  return credential.type === CredentialType.CERTIFICATE;
}

export function isServiceAccountCredential(
  credential: Credential
): credential is ServiceAccountCredential {
  return credential.type === CredentialType.SERVICE_ACCOUNT;
}