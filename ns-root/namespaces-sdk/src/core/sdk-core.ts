/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/core
 * @gl-semantic-anchor GL-00-SRC_CORE_SDKCORE
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Namespaces SDK Core - INSTANT Implementation
 * <100ms 延遲，並行執行，100%自治
 */

import { EventEmitter } from 'events';
import { RegistryManager } from './registry-manager';
import { NamespaceManager, NamespaceConfig as NSManagerConfig } from './namespace-manager';
import { ErrorHandler, ErrorCode } from './errors';

export interface SDKConfig {
  environment: string;
  debug: boolean;
  observability: {
    enableMetrics: boolean;
    enableTracing: boolean;
    enableAudit: boolean;
  };
  // Registry manager config
  autoResolve?: boolean;
  cacheEnabled?: boolean;
  parallelDiscovery?: boolean;
  // Namespace manager config
  autoValidation?: boolean;
  parallelDeployment?: boolean;
  instantRollback?: boolean;
}

export interface DeploymentResult {
  success: boolean;
  namespace: string;
  deploymentLatency: number;
  withinTarget: boolean;
  // Backward-compatible shape for existing callers (e.g. result.performanceMetrics.withinTarget)
  performanceMetrics?: {
    withinTarget: boolean;
  };
  error?: string;
}

export interface NamespaceConfig {
  name: string;
  environment?: string;
  region?: string;
  resources?: {
    cpu?: string | { requests?: string; limits?: string };
    memory?: string | { requests?: string; limits?: string };
  };
  labels?: Record<string, string>;
  annotations?: Record<string, string>;
  [key: string]: unknown;
}

export class NamespaceSDK extends EventEmitter {
  private registry: RegistryManager;
  private namespaceManager: NamespaceManager;
  private config: SDKConfig;
  private state: 'initializing' | 'ready' | 'error' = 'initializing';

  constructor(config: SDKConfig) {
    super();
    this.config = config;
    this.registry = new RegistryManager({
      autoResolve: config.autoResolve ?? true,
      cacheEnabled: config.cacheEnabled ?? true,
      parallelDiscovery: config.parallelDiscovery ?? true
    });
    this.namespaceManager = new NamespaceManager({
      autoValidation: config.autoValidation ?? true,
      parallelDeployment: config.parallelDeployment ?? true,
      instantRollback: config.instantRollback ?? true
    });
  }

  async initialize(): Promise<void> {
    const startTime = Date.now();
    
    try {
      this.state = 'initializing';
      
      await Promise.all([
        this.registry.initialize(),
        this.namespaceManager.initialize()
      ]);

      this.state = 'ready';
      const latency = Date.now() - startTime;
      
      if (latency > 100) {
        console.warn(`SDK initialization took ${latency}ms (>100ms target)`);
      }
      
      this.emit('ready', { latency, state: this.state });
    } catch (error) {
      this.state = 'error';
      throw ErrorHandler.wrap(error as Error, ErrorCode.INTERNAL_ERROR, {
        component: 'NamespaceSDK',
        operation: 'initialize'
      });
    }
  }

  async deployNamespace(config: NamespaceConfig): Promise<DeploymentResult> {
    if (this.state !== 'ready') {
      throw ErrorHandler.wrap(
        new Error('SDK not ready'),
        ErrorCode.INVALID_STATE,
        { state: this.state }
      );
    }

    try {
      // Convert NamespaceConfig to match NamespaceManager's expected format
      const nsConfig: NSManagerConfig = {
        name: config.name,
        environment: config.environment || this.config.environment,
        region: config.region
      };

      const result = await this.namespaceManager.deploy(nsConfig);

      this.emit('namespace:deployed', {
        namespace: config.name,
        latency: result.deploymentLatency,
        success: result.success
      });

      return {
        ...result,
        performanceMetrics: {
          withinTarget: result.withinTarget
        }
      };
    } catch (error) {
      throw ErrorHandler.wrap(error as Error, ErrorCode.DEPLOYMENT_FAILED, {
        namespace: config.name,
        config
      });
    }
  }

  getState(): string {
    return this.state;
  }

  getConfig(): SDKConfig {
    return { ...this.config };
  }
}
