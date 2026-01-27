/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/plugins
 * @gl-semantic-anchor GL-00-SRC_PLUGINS_INDEX
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Plugin System and Connector Registry
 * 
 * Implements plugin discovery, loading, and registration logic.
 */

import { Tool } from '../core/tool';
import { SDKError, ErrorCode, PluginError } from '../core/errors';
import { Logger } from '../observability/logger';

/**
 * Plugin metadata
 */
export interface PluginMetadata {
  /** Plugin name */
  name: string;
  
  /** Plugin version */
  version: string;
  
  /** Plugin description */
  description: string;
  
  /** Plugin author */
  author?: string;
  
  /** Plugin homepage */
  homepage?: string;
  
  /** Plugin dependencies */
  dependencies?: Record<string, string>;
  
  /** SDK version compatibility */
  sdkVersion?: string;
}

/**
 * Plugin interface
 */
export interface Plugin {
  /** Plugin metadata */
  metadata: PluginMetadata;
  
  /**
   * Initialize the plugin
   * @param context Plugin initialization context
   */
  initialize(context: PluginContext): Promise<void>;
  
  /**
   * Get tools provided by this plugin
   */
  getTools?(): Tool[];
  
  /**
   * Cleanup plugin resources
   */
  cleanup?(): Promise<void>;
}

/**
 * Plugin context
 */
export interface PluginContext {
  /** SDK version */
  sdkVersion: string;
  
  /** Logger instance */
  logger: Logger;
  
  /** Configuration */
  config?: Record<string, any>;
  
  /** Register a tool */
  registerTool: (tool: Tool) => void;
}

/**
 * Plugin loader options
 */
export interface PluginLoaderOptions {
  /** Plugin directories to search */
  directories?: string[];
  
  /** Auto-load plugins on initialization */
  autoLoad?: boolean;
  
  /** Plugin name filter */
  filter?: (name: string) => boolean;
  
  /** Enable plugin sandboxing */
  sandbox?: boolean;
}

/**
 * Plugin entry
 */
interface PluginEntry {
  plugin: Plugin;
  metadata: PluginMetadata;
  loadedAt: Date;
  initialized: boolean;
}

/**
 * Plugin Loader Class
 * 
 * Responsibilities:
 * - Discover plugins from configured directories
 * - Load and initialize plugins at runtime
 * - Register plugin-provided tools
 * - Enforce compatibility and version checks
 * - Manage plugin lifecycle
 */
export class PluginLoader {
  private plugins: Map<string, PluginEntry> = new Map();
  private logger: Logger;
  private options: PluginLoaderOptions;
  private sdkVersion: string;

  constructor(logger: Logger, sdkVersion: string, options: PluginLoaderOptions = {}) {
    this.logger = logger;
    this.sdkVersion = sdkVersion;
    this.options = {
      directories: [],
      autoLoad: false,
      sandbox: false,
      ...options
    };
  }

  /**
   * Initialize the plugin loader
   */
  async initialize(): Promise<void> {
    if (this.options.autoLoad) {
      await this.loadAll();
    }
  }

  /**
   * Load all plugins from configured directories
   */
  async loadAll(): Promise<void> {
    this.logger.info('Loading plugins...');

    // Plugin loading would scan directories and load plugin modules
    // This is a placeholder for the actual implementation
    
    this.logger.info('Plugin loading complete', {
      count: this.plugins.size
    });
  }

  /**
   * Load a specific plugin
   */
  async load(pluginName: string, pluginPath?: string): Promise<void> {
    try {
      // Check if already loaded
      if (this.plugins.has(pluginName)) {
        this.logger.warn('Plugin already loaded', { pluginName });
        return;
      }

      // Load plugin module
      // This would use dynamic import or require
      // const pluginModule = await import(pluginPath || pluginName);
      // const plugin: Plugin = pluginModule.default || pluginModule;

      // For now, throw not implemented
      throw new PluginError(
        pluginName,
        'Plugin loading not yet implemented',
        ErrorCode.PLUGIN_LOAD_FAILED
      );

    } catch (error) {
      this.logger.error('Failed to load plugin', error);
      throw new PluginError(
        pluginName,
        `Failed to load plugin: ${error instanceof Error ? error.message : String(error)}`,
        ErrorCode.PLUGIN_LOAD_FAILED,
        { cause: error instanceof Error ? error : undefined }
      );
    }
  }

  /**
   * Register a plugin
   */
  async register(plugin: Plugin): Promise<void> {
    const metadata = plugin.metadata;

    // Validate metadata
    this.validateMetadata(metadata);

    // Check compatibility
    if (!this.isCompatible(metadata)) {
      throw new PluginError(
        metadata.name,
        `Plugin is not compatible with SDK version ${this.sdkVersion}`,
        ErrorCode.PLUGIN_INCOMPATIBLE
      );
    }

    // Check if already registered
    if (this.plugins.has(metadata.name)) {
      throw new PluginError(
        metadata.name,
        'Plugin already registered',
        ErrorCode.PLUGIN_LOAD_FAILED
      );
    }

    // Create plugin entry
    const entry: PluginEntry = {
      plugin,
      metadata,
      loadedAt: new Date(),
      initialized: false
    };

    this.plugins.set(metadata.name, entry);

    this.logger.info('Plugin registered', {
      name: metadata.name,
      version: metadata.version
    });

    // Initialize the plugin
    await this.initializePlugin(entry);
  }

  /**
   * Unregister a plugin
   */
  async unregister(pluginName: string): Promise<void> {
    const entry = this.plugins.get(pluginName);

    if (!entry) {
      throw new PluginError(
        pluginName,
        'Plugin not found',
        ErrorCode.PLUGIN_NOT_FOUND
      );
    }

    // Cleanup plugin
    if (entry.plugin.cleanup) {
      try {
        await entry.plugin.cleanup();
      } catch (error) {
        this.logger.error('Plugin cleanup failed', error);
      }
    }

    this.plugins.delete(pluginName);

    this.logger.info('Plugin unregistered', { name: pluginName });
  }

  /**
   * Get a plugin by name
   */
  get(pluginName: string): Plugin | undefined {
    return this.plugins.get(pluginName)?.plugin;
  }

  /**
   * Check if a plugin is loaded
   */
  has(pluginName: string): boolean {
    return this.plugins.has(pluginName);
  }

  /**
   * List all loaded plugins
   */
  list(): PluginMetadata[] {
    return Array.from(this.plugins.values()).map(entry => entry.metadata);
  }

  /**
   * Get plugin statistics
   */
  getStats(): {
    total: number;
    initialized: number;
    plugins: Array<{
      name: string;
      version: string;
      initialized: boolean;
      loadedAt: string;
    }>;
  } {
    const plugins = Array.from(this.plugins.values()).map(entry => ({
      name: entry.metadata.name,
      version: entry.metadata.version,
      initialized: entry.initialized,
      loadedAt: entry.loadedAt.toISOString()
    }));

    return {
      total: this.plugins.size,
      initialized: plugins.filter(p => p.initialized).length,
      plugins
    };
  }

  /**
   * Cleanup all plugins
   */
  async cleanup(): Promise<void> {
    this.logger.info('Cleaning up plugins...');

    for (const [name, entry] of this.plugins.entries()) {
      try {
        if (entry.plugin.cleanup) {
          await entry.plugin.cleanup();
        }
      } catch (error) {
        this.logger.error('Plugin cleanup failed', {
          plugin: name,
          error: error instanceof Error ? error.message : String(error)
        });
      }
    }

    this.plugins.clear();
  }

  /**
   * Initialize a plugin
   */
  private async initializePlugin(entry: PluginEntry): Promise<void> {
    const context: PluginContext = {
      sdkVersion: this.sdkVersion,
      logger: this.logger.child({ plugin: entry.metadata.name }),
      registerTool: (tool: Tool) => {
        // Tool registration would be handled by the SDK
        this.logger.debug('Tool registered by plugin', {
          plugin: entry.metadata.name,
          tool: tool.getMetadata().name
        });
      }
    };

    try {
      await entry.plugin.initialize(context);
      entry.initialized = true;

      this.logger.info('Plugin initialized', {
        name: entry.metadata.name
      });

    } catch (error) {
      this.logger.error('Plugin initialization failed', error);
      throw new PluginError(
        entry.metadata.name,
        `Plugin initialization failed: ${error instanceof Error ? error.message : String(error)}`,
        ErrorCode.PLUGIN_INITIALIZATION_FAILED,
        { cause: error instanceof Error ? error : undefined }
      );
    }
  }

  /**
   * Validate plugin metadata
   */
  private validateMetadata(metadata: PluginMetadata): void {
    if (!metadata.name) {
      throw new SDKError(
        ErrorCode.PLUGIN_LOAD_FAILED,
        'Plugin name is required'
      );
    }

    if (!metadata.version) {
      throw new SDKError(
        ErrorCode.PLUGIN_LOAD_FAILED,
        'Plugin version is required'
      );
    }

    // Validate version format
    const versionRegex = /^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$/;
    if (!versionRegex.test(metadata.version)) {
      throw new SDKError(
        ErrorCode.PLUGIN_LOAD_FAILED,
        `Invalid plugin version format: ${metadata.version}`
      );
    }
  }

  /**
   * Check if plugin is compatible with SDK
   */
  private isCompatible(metadata: PluginMetadata): boolean {
    if (!metadata.sdkVersion) {
      return true; // No version requirement
    }

    // Simple version compatibility check
    // In production, this would use semver comparison
    const [sdkMajor] = this.sdkVersion.split('.');
    const [pluginMajor] = metadata.sdkVersion.split('.');

    return sdkMajor === pluginMajor;
  }
}

/**
 * Create a plugin loader instance
 */
export function createPluginLoader(
  logger: Logger,
  sdkVersion: string,
  options?: PluginLoaderOptions
): PluginLoader {
  return new PluginLoader(logger, sdkVersion, options);
}