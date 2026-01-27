/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/core
 * @gl-semantic-anchor GL-00-SRC_CORE_SERVICEADAPT
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Service Adapter Interface
 * 
 * Defines the contract for service adapters that integrate with external services.
 * This is a base interface for all service adapters (Cloudflare, GitHub, Google, OpenAI).
 */

export interface ServiceAdapter {
  /**
   * The name of the service adapter
   */
  name: string;

  /**
   * Initialize the service adapter
   */
  initialize(): Promise<void>;

  /**
   * Shutdown the service adapter
   */
  shutdown(): Promise<void>;

  /**
   * Check if the adapter is ready
   */
  isReady(): boolean;
}

/**
 * Service Adapter Base Class
 * 
 * Provides common functionality for service adapters.
 */
export abstract class BaseServiceAdapter implements ServiceAdapter {
  public readonly name: string;
  protected initialized: boolean = false;

  constructor(name: string) {
    this.name = name;
  }

  async initialize(): Promise<void> {
    this.initialized = true;
  }

  async shutdown(): Promise<void> {
    this.initialized = false;
  }

  isReady(): boolean {
    return this.initialized;
  }
}