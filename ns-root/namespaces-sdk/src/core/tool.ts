/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/core
 * @gl-semantic-anchor GL-00-SRC_CORE_TOOL
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Tool Base Class - Standard interface for all tool wrappers
 * 
 * Defines the base class and interfaces for all tool wrappers,
 * enforcing a standard contract for tool metadata, schema, and invocation.
 */

import { SDKError, ErrorCode } from './errors';

/**
 * Tool metadata describing the tool's identity and capabilities
 */
export interface ToolMetadata {
  /** Unique tool name (e.g., 'github_create_issue') */
  name: string;
  
  /** Human-readable tool title */
  title: string;
  
  /** Detailed description of what the tool does */
  description: string;
  
  /** Semantic version (e.g., '1.0.0') */
  version: string;
  
  /** Adapter/service this tool belongs to (e.g., 'github', 'cloudflare') */
  adapter?: string;
  
  /** Tool capabilities/features */
  capabilities?: string[];
  
  /** Additional metadata */
  metadata?: Record<string, any>;
}

/**
 * JSON Schema definition
 */
export interface JSONSchema {
  type: string;
  properties?: Record<string, any>;
  required?: string[];
  additionalProperties?: boolean | JSONSchema;
  [key: string]: unknown;
}

/**
 * Credential requirement specification
 */
export interface CredentialRequirement {
  /** Credential key/identifier */
  key: string;
  
  /** Credential scope (e.g., 'repo', 'user') */
  scope?: string;
  
  /** Whether this credential is required */
  required: boolean;
  
  /** Description of what this credential is used for */
  description?: string;
}

/**
 * Tool factory interface for creating tool instances
 */
export interface ToolFactory {
  /** Create a new instance of the tool */
  createTool: () => Tool;
  
  /** Get tool metadata */
  getToolMetadata: () => ToolMetadata;
}

/**
 * Tool descriptor containing metadata and schema information
 */
export interface ToolDescriptor {
  /** Tool metadata */
  metadata: ToolMetadata;
  
  /** Tool factory for creating instances */
  factory: ToolFactory;
  
  /** Input schema for the tool */
  inputSchema: JSONSchema;
  
  /** Output schema for the tool */
  outputSchema?: JSONSchema | null;
}

/**
 * Tool invocation context
 */
export interface ToolContext {
  /** Request ID for tracing */
  requestId?: string;
  
  /** User/agent making the request */
  userId?: string;
  
  /** Additional context metadata */
  metadata?: Record<string, any>;
}

/**
 * Tool invocation result
 */
export interface ToolInvocationResult {
  /** Whether the invocation was successful */
  success: boolean;
  
  /** Result data (structured or unstructured) */
  data?: Record<string, unknown>;
  
  /** Error information if failed */
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
  
  /** Additional metadata about the invocation */
  metadata?: {
    duration?: number;
    timestamp?: string;
    [key: string]: unknown;
  };
}

/**
 * Abstract Tool Base Class
 * 
 * All tool wrappers must extend this class and implement the required methods.
 * 
 * Responsibilities:
 * - Provide tool metadata and schema information
 * - Implement tool invocation logic
 * - Handle schema validation and error handling
 * - Support both synchronous and asynchronous execution
 */
export abstract class Tool {
  protected metadata: ToolMetadata;

  constructor(metadata: ToolMetadata) {
    this.validateMetadata(metadata);
    this.metadata = metadata;
  }

  /**
   * Get tool metadata
   * @returns Tool metadata
   */
  getMetadata(): ToolMetadata {
    return { ...this.metadata };
  }

  /**
   * Get input schema for the tool
   * @returns JSON Schema for input validation
   */
  abstract getInputSchema(): JSONSchema;

  /**
   * Get output schema for the tool (optional)
   * @returns JSON Schema for output validation, or null if not applicable
   */
  getOutputSchema(): JSONSchema | null {
    return null;
  }

  /**
   * Get credential requirements for the tool
   * @returns Array of credential requirements, or empty array if none
   */
  getCredentialRequirements(): CredentialRequirement[] {
    return [];
  }

  /**
   * Invoke the tool with given parameters
   * @param params Tool invocation parameters
   * @param credentials Credentials for the tool (if required)
   * @param context Optional invocation context
   * @returns Tool invocation result
   */
  abstract invoke(
    params: Record<string, any>,
    credentials?: unknown,
    context?: ToolContext
  ): Promise<ToolInvocationResult>;

  /**
   * Validate tool metadata
   */
  private validateMetadata(metadata: ToolMetadata): void {
    if (!metadata.name) {
      throw new SDKError(
        ErrorCode.INVALID_TOOL_METADATA,
        'Tool name is required'
      );
    }

    if (!metadata.title) {
      throw new SDKError(
        ErrorCode.INVALID_TOOL_METADATA,
        'Tool title is required'
      );
    }

    if (!metadata.description) {
      throw new SDKError(
        ErrorCode.INVALID_TOOL_METADATA,
        'Tool description is required'
      );
    }

    if (!metadata.version) {
      throw new SDKError(
        ErrorCode.INVALID_TOOL_METADATA,
        'Tool version is required'
      );
    }
  }

  /**
   * Create a success result
   */
  protected createSuccessResult(
    data: Record<string, unknown>,
    metadata?: Record<string, any>
  ): ToolInvocationResult {
    return {
      success: true,
      data,
      metadata: {
        timestamp: new Date().toISOString(),
        ...metadata
      }
    };
  }

  /**
   * Create an error result
   */
  protected createErrorResult(
    code: string,
    message: string,
    details?: unknown
  ): ToolInvocationResult {
    return {
      success: false,
      error: {
        code,
        message,
        details
      },
      metadata: {
        timestamp: new Date().toISOString()
      }
    };
  }

  /**
   * Wrap an async operation with error handling
   */
  protected async wrapInvocation<T>(
    operation: () => Promise<T>,
    errorCode: string = ErrorCode.TOOL_EXECUTION_FAILED
  ): Promise<T> {
    try {
      return await operation();
    } catch (error) {
      if (error instanceof SDKError) {
        throw error;
      }

      const errorMessage = error instanceof Error ? error.message : String(error);
      throw new SDKError(
        errorCode,k
        `Tool execution failed: ${errorMessage}`,
        `Tool execution failed: ${error instanceof Error ? error.message : String(error)}`,
        error
      );
    }
  }
}

/**
 * Simple tool implementation helper
 * For creating tools without extending the base class
 */
export class SimpleTool extends Tool {
  private inputSchema: JSONSchema;
  private outputSchema: JSONSchema | null;
  private credentialRequirements: CredentialRequirement[];
  private invokeHandler: (
    params: Record<string, any>,
    credentials?: unknown,
    context?: ToolContext
  ) => Promise<ToolInvocationResult>;

  constructor(
    metadata: ToolMetadata,
    inputSchema: JSONSchema,
    invokeHandler: (
      params: Record<string, any>,
      credentials?: unknown,
      context?: ToolContext
    ) => Promise<ToolInvocationResult>,
    options?: {
      outputSchema?: JSONSchema;
      credentialRequirements?: CredentialRequirement[];
    }
  ) {
    super(metadata);
    this.inputSchema = inputSchema;
    this.outputSchema = options?.outputSchema || null;
    this.credentialRequirements = options?.credentialRequirements || [];
    this.invokeHandler = invokeHandler;
  }

  override getInputSchema(): JSONSchema {
    return this.inputSchema;
  }

  override getOutputSchema(): JSONSchema | null {
    return this.outputSchema;
  }

  override getCredentialRequirements(): CredentialRequirement[] {
    return this.credentialRequirements;
  }

  async invoke(
    params: Record<string, any>,
    credentials?: unknown,
    context?: ToolContext
  ): Promise<ToolInvocationResult> {
    return this.invokeHandler(params, credentials, context);
  }
}

/**
 * Tool builder for fluent API
 */
export class ToolBuilder {
  private metadata: Partial<ToolMetadata> = {};
  private inputSchema?: JSONSchema;
  private outputSchema?: JSONSchema;
  private credentialRequirements: CredentialRequirement[] = [];
  private invokeHandler?: (
    params: Record<string, any>,
    credentials?: unknown,
    context?: ToolContext
  ) => Promise<ToolInvocationResult>;

  /**
   * Set tool name
   */
  name(name: string): this {
    this.metadata.name = name;
    return this;
  }

  /**
   * Set tool title
   */
  title(title: string): this {
    this.metadata.title = title;
    return this;
  }

  /**
   * Set tool description
   */
  description(description: string): this {
    this.metadata.description = description;
    return this;
  }

  /**
   * Set tool version
   */
  version(version: string): this {
    this.metadata.version = version;
    return this;
  }

  /**
   * Set tool adapter
   */
  adapter(adapter: string): this {
    this.metadata.adapter = adapter;
    return this;
  }

  /**
   * Set tool capabilities
   */
  capabilities(capabilities: string[]): this {
    this.metadata.capabilities = capabilities;
    return this;
  }

  /**
   * Set input schema
   */
  input(schema: JSONSchema): this {
    this.inputSchema = schema;
    return this;
  }

  /**
   * Set output schema
   */
  output(schema: JSONSchema): this {
    this.outputSchema = schema;
    return this;
  }

  /**
   * Add credential requirement
   */
  requireCredential(
    key: string,
    options?: {
      scope?: string;
      required?: boolean;
      description?: string;
    }
  ): this {
    this.credentialRequirements.push({
      key,
      scope: options?.scope,
      required: options?.required !== false,
      description: options?.description
    });
    return this;
  }

  /**
   * Set invoke handler
   */
  handler(
    handler: (
      params: Record<string, any>,
      credentials?: unknown,
      context?: ToolContext
    ) => Promise<ToolInvocationResult>
  ): this {
    this.invokeHandler = handler;
    return this;
  }

  /**
   * Build the tool
   */
  build(): Tool {
    if (!this.metadata.name) {
      throw new SDKError(ErrorCode.INVALID_TOOL_METADATA, 'Tool name is required');
    }

    if (!this.metadata.title) {
      throw new SDKError(ErrorCode.INVALID_TOOL_METADATA, 'Tool title is required');
    }

    if (!this.metadata.description) {
      throw new SDKError(
        ErrorCode.INVALID_TOOL_METADATA,
        'Tool description is required'
      );
    }

    if (!this.metadata.version) {
      this.metadata.version = '1.0.0';
    }

    if (!this.inputSchema) {
      throw new SDKError(
        ErrorCode.INVALID_TOOL_METADATA,
        'Input schema is required'
      );
    }

    if (!this.invokeHandler) {
      throw new SDKError(
        ErrorCode.INVALID_TOOL_METADATA,
        'Invoke handler is required'
      );
    }

    return new SimpleTool(
      this.metadata as ToolMetadata,
      this.inputSchema,
      this.invokeHandler,
      {
        outputSchema: this.outputSchema,
        credentialRequirements: this.credentialRequirements
      }
    );
  }
}

/**
 * Create a new tool builder
 */
export function createTool(): ToolBuilder {
  return new ToolBuilder();
}