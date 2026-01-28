// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/core
 * @gl-semantic-anchor GL-00-SRC_CORE_SDK
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Main SDK Class - Core orchestration and lifecycle management
 * 
 * This class serves as the primary entry point for the namespace-sdk,
 * managing initialization, tool registration, invocation routing,
 * and integration with observability and credential management systems.
 */

import { ToolRegistry } from './registry';
import { Tool, ToolMetadata, ToolInvocationResult } from './tool';
import { SDKError, ErrorCode, ErrorHandler } from './errors';
import { CredentialManager } from '../credentials/manager';
import { SchemaValidator } from '../schema/validator';
import { Logger } from '../observability/logger';
import { Tracer } from '../observability/tracer';
import { MetricsCollector } from '../observability/metrics';
import { AuditLogger } from '../observability/audit';
import { ConfigManager } from '../config';

/**
 * Helper function to safely extract error message from unknown error type
 * @param error Unknown error object
 * @returns Error message string
 */
function getErrorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}


/**
 * SDK Configuration Options
 */
export interface SDKConfig {
  /** Enable debug logging */
  debug?: boolean;
  /** Credential provider configuration */
  credentials?: {
    providers?: string[];
    defaultProvider?: string;
  };
  /** Observability configuration */
  observability?: {
    enableLogging?: boolean;
    enableTracing?: boolean;
    enableMetrics?: boolean;
    enableAudit?: boolean;
  };
  /** Plugin configuration */
  plugins?: {
    autoLoad?: boolean;
    directories?: string[];
  };
  /** Environment name (development, staging, production) */
  environment?: string;
}

/**
 * SDK Initialization State
 */
export enum SDKState {
  UNINITIALIZED = 'uninitialized',
  INITIALIZING = 'initializing',
  READY = 'ready',
  SHUTTING_DOWN = 'shutting_down',
  SHUTDOWN = 'shutdown',
  ERROR = 'error'
}

/**
 * Main SDK Class
 * 
 * Responsibilities:
 * - Manage SDK lifecycle (initialization, shutdown, cleanup)
 * - Coordinate tool registration and discovery
 * - Route tool invocations to appropriate adapters
 * - Integrate observability, auditing, and error handling
 * - Enforce MCP protocol compliance
 */
export class NamespaceSDK {
  private state: SDKState = SDKState.UNINITIALIZED;
  private config: SDKConfig;
  
  // Core components
  private registry: ToolRegistry;
  private credentialManager: CredentialManager;
  private schemaValidator: SchemaValidator;
  
  // Observability components
  private logger: Logger;
  private tracer: Tracer;
  private metrics: MetricsCollector;
  private audit: AuditLogger;
  
  // Configuration manager
  private configManager: ConfigManager;

  /**
   * Create a new SDK instance
   * @param config SDK configuration options
   */
  constructor(config: SDKConfig = {}) {
    this.config = config;
    
    // Initialize configuration manager
    this.configManager = new ConfigManager(config.environment);
    
    // Initialize observability components
    this.logger = new Logger({
      debug: config.debug,
      enabled: config.observability?.enableLogging !== false
    });
    
    this.tracer = new Tracer({
      enabled: config.observability?.enableTracing !== false
    });
    
    this.metrics = new MetricsCollector({
      enabled: config.observability?.enableMetrics !== false
    });
    
    this.audit = new AuditLogger({
      enabled: config.observability?.enableAudit !== false
    });
    
    // Initialize core components
    this.registry = new ToolRegistry(this.logger);
    this.credentialManager = new CredentialManager(
      config.credentials,
      this.logger,
      this.audit
    );
    this.schemaValidator = new SchemaValidator(this.logger);
    
    this.logger.info('SDK instance created', { config });
  }

  /**
   * Initialize the SDK
   * Loads configuration, credentials, plugins, and prepares for tool invocation
   */
  async initialize(): Promise<void> {
    if (this.state !== SDKState.UNINITIALIZED) {
      throw new SDKError(
        ErrorCode.INVALID_STATE,
        `Cannot initialize SDK in state: ${this.state}`
      );
    }

    this.state = SDKState.INITIALIZING;
    const span = this.tracer.startSpan('sdk.initialize');

    try {
      this.logger.info('Initializing SDK...');

      // Load configuration
      await this.configManager.load();
      this.logger.debug('Configuration loaded');

      // Initialize credential manager
      await this.credentialManager.initialize();
      this.logger.debug('Credential manager initialized');

      // Load plugins if auto-load is enabled
      if (this.config.plugins?.autoLoad) {
        await this.loadPlugins();
      }

      // Validate registry state
      const toolCount = this.registry.getToolCount();
      this.logger.info(`SDK initialized with ${toolCount} tools`);

      this.state = SDKState.READY;
      this.metrics.increment('sdk.initialized');
      this.audit.log('sdk.initialized', { toolCount });

      span.status = { code: 0, message: 'Success' };
    } catch (error) {
      this.state = SDKState.ERROR;
      this.logger.error('SDK initialization failed', error);
      this.metrics.increment('sdk.initialization_failed');
      
      span.status = { code: 1, message: error instanceof Error ? error.message : String(error) };
      throw new SDKError(
        ErrorCode.INITIALIZATION_FAILED,
        'Failed to initialize SDK',
        error
      );
    } finally {
      span.end();
    }
  }

  /**
   * Register a tool with the SDK
   * @param tool Tool instance to register
   */
  registerTool(tool: Tool): void {
    this.ensureReady();
    
    const metadata = tool.getMetadata();
    
    const span = this.tracer.startSpan('sdk.registerTool', {
      toolName: metadata.name
    });

    try {
      this.registry.register(tool);
      this.logger.info(`Tool registered: ${metadata.name}`);
      this.metrics.increment('sdk.tool_registered', { tool: metadata.name });
      this.audit.log('tool.registered', { 
        toolName: metadata.name,
        toolVersion: metadata.version 
      });

      span.status = { code: 0, message: 'Success' };
    } catch (error) {
      this.logger.error(`Failed to register tool: ${tool.metadata.name}`, error);
      span.setStatus({ code: 1, message: getErrorMessage(error) });
      span.setStatus({ code: 1, message: ErrorHandler.getErrorMessage(error) });
      this.logger.error(`Failed to register tool: ${metadata.name}`, error);
      span.status = { code: 1, message: error instanceof Error ? error.message : String(error) };
      throw error;
    } finally {
      span.end();
    }
  }

  /**
   * List all available tools
   * @returns Array of tool metadata
   */
  listTools(): ToolMetadata[] {
    this.ensureReady();
    return this.registry.listTools();
  }

  /**
   * Get metadata for a specific tool
   * @param toolName Name of the tool
   * @returns Tool metadata or undefined if not found
   */
  getTool(toolName: string): ToolMetadata | undefined {
    this.ensureReady();
    return this.registry.getTool(toolName);
  }

  /**
   * Invoke a tool with the given parameters
   * @param toolName Name of the tool to invoke
   * @param params Tool invocation parameters
   * @returns Tool invocation result
   */
  async invokeTool(
    toolName: string,
    params: Record<string, any>
  ): Promise<ToolInvocationResult> {
    this.ensureReady();

    const span = this.tracer.startSpan('sdk.invokeTool', {
      toolName,
      paramsKeys: Object.keys(params).join(',')
    });

    const startTime = Date.now();

    try {
      this.logger.info(`Invoking tool: ${toolName}`, { params });

      // Get tool from registry
      const tool = this.registry.getToolInstance(toolName);
      if (!tool) {
        throw new SDKError(
          ErrorCode.TOOL_NOT_FOUND,
          `Tool not found: ${toolName}`
        );
      }

      // Validate input parameters against schema
      const inputSchema = tool.getInputSchema();
      const validationResult = await this.schemaValidator.validate(
        params,
        inputSchema
      );

      if (!validationResult.valid) {
        throw new SDKError(
          ErrorCode.VALIDATION_FAILED,
          'Input validation failed',
          validationResult.errors
        );
      }

      // Get credentials if required
      const credentials = await this.getToolCredentials(tool);

      // Invoke the tool
      const result = await tool.invoke(params, credentials);

      // Validate output against schema
      const outputSchema = tool.getOutputSchema();
      if (outputSchema) {
        const outputValidation = await this.schemaValidator.validate(
          result.data,
          outputSchema
        );

        if (!outputValidation.valid) {
          this.logger.warn('Output validation failed', {
            toolName,
            errors: outputValidation.errors
          });
        }
      }

      // Record metrics
      const duration = Date.now() - startTime;
      this.metrics.recordHistogram('sdk.tool_invocation_duration', duration, {
        tool: toolName,
        success: 'true'
      });
      this.metrics.increment('sdk.tool_invoked', { tool: toolName });

      // Audit log
      this.audit.log('tool.invoked', {
        toolName,
        duration,
        success: true,
        resultSize: JSON.stringify(result.data).length
      });

      this.logger.info(`Tool invocation successful: ${toolName}`, {
        duration
      });

      span.status = { code: 0, message: 'Success' };
      return result;

    } catch (error) {
      const duration = Date.now() - startTime;
      
      this.logger.error(`Tool invocation failed: ${toolName}`, error);
      
      this.metrics.recordHistogram('sdk.tool_invocation_duration', duration, {
        tool: toolName,
        success: 'false'
      });
      this.metrics.increment('sdk.tool_invocation_failed', { tool: toolName });

      this.audit.log('tool.invocation_failed', {
        toolName,
        duration,
        error: error instanceof Error ? error.message : String(error)
      });

      span.setStatus({ code: 1, message: error instanceof Error ? error.message : String(error) });

      // Re-throw as SDKError if not already
      if (error instanceof SDKError) {
        throw error;
      }

      throw new SDKError(
        ErrorCode.TOOL_EXECUTION_FAILED,
        `Tool execution failed: ${toolName}`,
        error
      );
    } finally {
      span.end();
    }
  }

  /**
   * Shutdown the SDK and cleanup resources
   */
  async shutdown(): Promise<void> {
    if (this.state === SDKState.SHUTDOWN || this.state === SDKState.SHUTTING_DOWN) {
      return;
    }

    this.state = SDKState.SHUTTING_DOWN;
    const span = this.tracer.startSpan('sdk.shutdown');

    try {
      this.logger.info('Shutting down SDK...');

      // Cleanup credential manager
      await this.credentialManager.cleanup();

      // Clear registry
      this.registry.clear();

      // Flush observability data
      await Promise.all([
        this.logger.flush(),
        this.tracer.flush(),
        this.metrics.flush(),
        this.audit.flush()
      ]);

      this.state = SDKState.SHUTDOWN;
      this.logger.info('SDK shutdown complete');

      span.status = { code: 0, message: 'Success' };
    } catch (error) {
      this.logger.error('SDK shutdown failed', error);
      span.status = { code: 1, message: error instanceof Error ? error.message : String(error) };
      span.setStatus({ code: 1, message: getErrorMessage(error) });
      span.setStatus({ code: 1, message: ErrorHandler.getErrorMessage(error) });
      span.setStatus({ code: 1, message: error instanceof Error ? error.message : String(error) });
      const message = error instanceof Error ? error.message : String(error);
      span.setStatus({ code: 1, message });
      throw error;
    } finally {
      span.end();
    }
  }

  /**
   * Get SDK state
   */
  getState(): SDKState {
    return this.state;
  }

  /**
   * Check if SDK is ready for operations
   */
  isReady(): boolean {
    return this.state === SDKState.READY;
  }

  /**
   * Load plugins from configured directories
   */
  private async loadPlugins(): Promise<void> {
    this.logger.info('Loading plugins...');
    // Plugin loading implementation will be added in plugins module
    // For now, this is a placeholder
    this.logger.debug('Plugin loading not yet implemented');
  }

  /**
   * Get credentials for a tool
   */
  private async getToolCredentials(tool: Tool): Promise<unknown> {
    const credentialRequirements = tool.getCredentialRequirements();
    
    if (!credentialRequirements || credentialRequirements.length === 0) {
      return null;
    }

    const credentials: Record<string, any> = {};

    for (const requirement of credentialRequirements) {
      const credential = await this.credentialManager.getCredential(
        requirement.key,
        requirement.scope
      );

      if (!credential && requirement.required) {
        throw new SDKError(
          ErrorCode.CREDENTIAL_NOT_FOUND,
          `Required credential not found: ${requirement.key}`
        );
      }

      if (credential) {
        credentials[requirement.key] = credential;
      }
    }

    return credentials;
  }

  /**
   * Ensure SDK is in ready state
   */
  private ensureReady(): void {
    if (this.state !== SDKState.READY) {
      throw new SDKError(
        ErrorCode.INVALID_STATE,
        `SDK is not ready. Current state: ${this.state}`
      );
    }
  }
}