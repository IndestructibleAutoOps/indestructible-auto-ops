/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/credentials
 * @gl-semantic-anchor GL-00-SRC_CREDENTI_MANAGER
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Credential Manager
 * 
 * Centralizes credential storage, retrieval, rotation, and usage tracking.
 * Supports multiple credential providers with secure handling.
 */

import { CredentialProvider, Credential, CredentialConfig } from './types';
import { CredentialError, ErrorCode } from '../core/errors';
import { Logger } from '../observability/logger';
import { AuditLogger } from '../observability/audit';

/**
 * Credential cache entry
 */
interface CacheEntry {
  credential: Credential;
  cachedAt: Date;
  expiresAt?: Date;
  accessCount: number;
  lastAccessedAt: Date;
}

/**
 * Credential Manager Options
 */
export interface CredentialManagerOptions {
  /** Credential providers to use */
  providers?: string[];
  
  /** Default provider */
  defaultProvider?: string;
  
  /** Cache TTL in milliseconds */
  cacheTTL?: number;
  
  /** Enable credential caching */
  enableCache?: boolean;
  
  /** Maximum cache size */
  maxCacheSize?: number;
}

/**
 * Credential Manager Class
 * 
 * Responsibilities:
 * - Load credentials from multiple sources
 * - Provide secure APIs for credential access
 * - Support credential rotation and expiration
 * - Track credential usage for audit
 * - Cache credentials with TTL
 */
export class CredentialManager {
  private providers: Map<string, CredentialProvider> = new Map();
  private cache: Map<string, CacheEntry> = new Map();
  private logger: Logger;
  private audit: AuditLogger;
  private options: CredentialManagerOptions;
  private initialized: boolean = false;

  constructor(
    options: CredentialManagerOptions = {},
    logger: Logger,
    audit: AuditLogger
  ) {
    this.options = {
      cacheTTL: 300000, // 5 minutes default
      enableCache: true,
      maxCacheSize: 100,
      ...options
    };
    this.logger = logger;
    this.audit = audit;
  }

  /**
   * Initialize the credential manager
   */
  async initialize(): Promise<void> {
    if (this.initialized) {
      return;
    }

    this.logger.info('Initializing credential manager...');

    try {
      // Load and initialize providers
      await this.loadProviders();

      this.initialized = true;
      this.logger.info('Credential manager initialized', {
        providerCount: this.providers.size
      });

      this.audit.log('credential_manager.initialized', {
        providerCount: this.providers.size,
        providers: Array.from(this.providers.keys())
      });

    } catch (error) {
      this.logger.error('Failed to initialize credential manager', error);
      throw new CredentialError(
        'Credential manager initialization failed',
        ErrorCode.CREDENTIAL_PROVIDER_FAILED,
        { details: error }
      );
    }
  }

  /**
   * Register a credential provider
   * @param name Provider name
   * @param provider Provider instance
   */
  registerProvider(name: string, provider: CredentialProvider): void {
    if (this.providers.has(name)) {
      this.logger.warn('Overwriting existing credential provider', { name });
    }

    this.providers.set(name, provider);
    this.logger.info('Credential provider registered', { name });
  }

  /**
   * Get a credential by key
   * @param key Credential key
   * @param scope Optional credential scope
   * @returns Credential or undefined if not found
   */
  async getCredential(
    key: string,
    scope?: string
  ): Promise<Credential | undefined> {
    this.ensureInitialized();

    const cacheKey = this.getCacheKey(key, scope);

    // Check cache first
    if (this.options.enableCache) {
      const cached = this.getFromCache(cacheKey);
      if (cached) {
        this.logger.debug('Credential retrieved from cache', { key, scope });
        this.audit.log('credential.accessed', {
          key,
          scope,
          source: 'cache'
        });
        return cached;
      }
    }

    // Try each provider in order
    for (const [providerName, provider] of this.providers.entries()) {
      try {
        const credential = await provider.getCredential(key, scope);
        
        if (credential) {
          this.logger.debug('Credential retrieved from provider', {
            key,
            scope,
            provider: providerName
          });

          // Cache the credential
          if (this.options.enableCache) {
            this.addToCache(cacheKey, credential);
          }

          this.audit.log('credential.accessed', {
            key,
            scope,
            source: providerName
          });

          return credential;
        }
      } catch (error) {
        this.logger.warn('Provider failed to retrieve credential', {
          key,
          scope,
          provider: providerName,
          error: error instanceof Error ? error.message : String(error)
        });
      }
    }

    this.logger.warn('Credential not found', { key, scope });
    this.audit.log('credential.not_found', { key, scope });

    return undefined;
  }

  /**
   * Get a credential or throw if not found
   * @param key Credential key
   * @param scope Optional credential scope
   * @returns Credential
   * @throws CredentialError if not found
   */
  async getCredentialOrThrow(
    key: string,
    scope?: string
  ): Promise<Credential> {
    const credential = await this.getCredential(key, scope);

    if (!credential) {
      throw new CredentialError(
        `Credential not found: ${key}`,
        ErrorCode.CREDENTIAL_NOT_FOUND,
        { context: { key, scope } }
      );
    }

    return credential;
  }

  /**
   * Set a credential
   * @param key Credential key
   * @param value Credential value
   * @param options Credential options
   */
  async setCredential(
    key: string,
    value: string,
    options?: {
      scope?: string;
      expiresAt?: Date;
      metadata?: Record<string, any>;
      provider?: string;
    }
  ): Promise<void> {
    this.ensureInitialized();

    const credential: Credential = {
      key,
      value,
      scope: options?.scope,
      expiresAt: options?.expiresAt,
      metadata: options?.metadata
    };

    // Use specified provider or default
    const providerName = options?.provider || this.options.defaultProvider;
    
    if (!providerName) {
      throw new CredentialError(
        'No credential provider specified',
        ErrorCode.CREDENTIAL_PROVIDER_FAILED
      );
    }

    const provider = this.providers.get(providerName);
    
    if (!provider) {
      throw new CredentialError(
        `Credential provider not found: ${providerName}`,
        ErrorCode.CREDENTIAL_PROVIDER_FAILED
      );
    }

    try {
      await provider.setCredential(credential);

      // Update cache
      if (this.options.enableCache) {
        const cacheKey = this.getCacheKey(key, options?.scope);
        this.addToCache(cacheKey, credential);
      }

      this.logger.info('Credential set', {
        key,
        scope: options?.scope,
        provider: providerName
      });

      this.audit.log('credential.set', {
        key,
        scope: options?.scope,
        provider: providerName
      });

    } catch (error) {
      this.logger.error('Failed to set credential', error);
      throw new CredentialError(
        `Failed to set credential: ${key}`,
        ErrorCode.CREDENTIAL_PROVIDER_FAILED,
        { cause: error instanceof Error ? error : undefined }
      );
    }
  }

  /**
   * Delete a credential
   * @param key Credential key
   * @param scope Optional credential scope
   */
  async deleteCredential(key: string, scope?: string): Promise<void> {
    this.ensureInitialized();

    // Remove from cache
    const cacheKey = this.getCacheKey(key, scope);
    this.cache.delete(cacheKey);

    // Delete from all providers
    for (const [providerName, provider] of this.providers.entries()) {
      try {
        await provider.deleteCredential(key, scope);
        this.logger.debug('Credential deleted from provider', {
          key,
          scope,
          provider: providerName
        });
      } catch (error) {
        this.logger.warn('Failed to delete credential from provider', {
          key,
          scope,
          provider: providerName,
          error: error instanceof Error ? error.message : String(error)
        });
      }
    }

    this.audit.log('credential.deleted', { key, scope });
  }

  /**
   * Rotate a credential
   * @param key Credential key
   * @param newValue New credential value
   * @param scope Optional credential scope
   */
  async rotateCredential(
    key: string,
    newValue: string,
    scope?: string
  ): Promise<void> {
    this.ensureInitialized();

    // Get current credential
    const current = await this.getCredential(key, scope);

    if (!current) {
      throw new CredentialError(
        `Cannot rotate non-existent credential: ${key}`,
        ErrorCode.CREDENTIAL_NOT_FOUND
      );
    }

    // Set new credential
    await this.setCredential(key, newValue, {
      scope,
      expiresAt: current.expiresAt,
      metadata: {
        ...current.metadata,
        rotatedAt: new Date().toISOString(),
        previousValue: current.value.substring(0, 4) + '...' // Log prefix only
      }
    });

    this.logger.info('Credential rotated', { key, scope });
    this.audit.log('credential.rotated', { key, scope });
  }

  /**
   * Check if a credential is expired
   * @param credential Credential to check
   * @returns true if expired
   */
  isExpired(credential: Credential): boolean {
    if (!credential.expiresAt) {
      return false;
    }

    return new Date() > credential.expiresAt;
  }

  /**
   * Clear credential cache
   */
  clearCache(): void {
    const size = this.cache.size;
    this.cache.clear();
    this.logger.info('Credential cache cleared', { size });
  }

  /**
   * Get cache statistics
   */
  getCacheStats(): {
    size: number;
    maxSize: number;
    hitRate: number;
    entries: Array<{
      key: string;
      accessCount: number;
      lastAccessedAt: string;
    }>;
  } {
    const entries = Array.from(this.cache.entries()).map(([key, entry]) => ({
      key,
      accessCount: entry.accessCount,
      lastAccessedAt: entry.lastAccessedAt.toISOString()
    }));

    // Calculate hit rate (simplified)
    const totalAccesses = entries.reduce((sum, e) => sum + e.accessCount, 0);
    const hitRate = entries.length > 0 ? totalAccesses / entries.length : 0;

    return {
      size: this.cache.size,
      maxSize: this.options.maxCacheSize || 0,
      hitRate,
      entries
    };
  }

  /**
   * Cleanup expired credentials and cache entries
   */
  async cleanup(): Promise<void> {
    this.logger.info('Running credential cleanup...');

    // Clean expired cache entries
    const now = new Date();
    let expiredCount = 0;

    for (const [key, entry] of this.cache.entries()) {
      if (entry.expiresAt && now > entry.expiresAt) {
        this.cache.delete(key);
        expiredCount++;
      }
    }

    if (expiredCount > 0) {
      this.logger.info('Expired cache entries removed', { count: expiredCount });
    }

    // Cleanup providers
    for (const [name, provider] of this.providers.entries()) {
      try {
        if (provider.cleanup) {
          await provider.cleanup();
        }
      } catch (error) {
        this.logger.warn('Provider cleanup failed', {
          provider: name,
          error: error instanceof Error ? error.message : String(error)
        });
      }
    }
  }

  /**
   * Get cache key
   */
  private getCacheKey(key: string, scope?: string): string {
    return scope ? `${key}:${scope}` : key;
  }

  /**
   * Get credential from cache
   */
  private getFromCache(cacheKey: string): Credential | undefined {
    const entry = this.cache.get(cacheKey);

    if (!entry) {
      return undefined;
    }

    // Check if expired
    if (entry.expiresAt && new Date() > entry.expiresAt) {
      this.cache.delete(cacheKey);
      return undefined;
    }

    // Update access stats
    entry.accessCount++;
    entry.lastAccessedAt = new Date();

    return entry.credential;
  }

  /**
   * Add credential to cache
   */
  private addToCache(cacheKey: string, credential: Credential): void {
    // Check cache size limit
    if (
      this.options.maxCacheSize &&
      this.cache.size >= this.options.maxCacheSize
    ) {
      // Remove oldest entry
      const oldestKey = this.findOldestCacheEntry();
      if (oldestKey) {
        this.cache.delete(oldestKey);
      }
    }

    const entry: CacheEntry = {
      credential,
      cachedAt: new Date(),
      expiresAt: credential.expiresAt || this.calculateCacheExpiry(),
      accessCount: 0,
      lastAccessedAt: new Date()
    };

    this.cache.set(cacheKey, entry);
  }

  /**
   * Find oldest cache entry
   */
  private findOldestCacheEntry(): string | undefined {
    let oldestKey: string | undefined;
    let oldestTime: Date | undefined;

    for (const [key, entry] of this.cache.entries()) {
      if (!oldestTime || entry.lastAccessedAt < oldestTime) {
        oldestKey = key;
        oldestTime = entry.lastAccessedAt;
      }
    }

    return oldestKey;
  }

  /**
   * Calculate cache expiry time
   */
  private calculateCacheExpiry(): Date {
    return new Date(Date.now() + (this.options.cacheTTL || 300000));
  }

  /**
   * Load credential providers
   */
  private async loadProviders(): Promise<void> {
    // Providers will be loaded dynamically based on configuration
    // This is a placeholder for the actual implementation
    this.logger.debug('Loading credential providers...');
    
    // Default providers would be loaded here
    // For now, this is handled by external registration
  }

  /**
   * Ensure manager is initialized
   */
  private ensureInitialized(): void {
    if (!this.initialized) {
      throw new CredentialError(
        'Credential manager not initialized',
        ErrorCode.CREDENTIAL_PROVIDER_FAILED
      );
    }
  }
}