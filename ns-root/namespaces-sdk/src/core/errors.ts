// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/core
 * @gl-semantic-anchor GL-00-SRC_CORE_ERRORS
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Error Types and Handling
 * 
 * Defines standardized error types, codes, and handling logic for the SDK.
 * Aligns with MCP and JSON-RPC error conventions.
 */

/**
 * Standard error codes
 * Aligned with JSON-RPC 2.0 and MCP protocol conventions
 */
export enum ErrorCode {
  // SDK Lifecycle Errors (1xxx)
  INITIALIZATION_FAILED = 'SDK_1001',
  INVALID_STATE = 'SDK_1002',
  SHUTDOWN_FAILED = 'SDK_1003',

  // Tool Registry Errors (2xxx)
  TOOL_NOT_FOUND = 'REGISTRY_2001',
  TOOL_ALREADY_REGISTERED = 'REGISTRY_2002',
  INVALID_TOOL_METADATA = 'REGISTRY_2003',
  TOOL_REGISTRATION_FAILED = 'REGISTRY_2004',

  // Tool Execution Errors (3xxx)
  TOOL_EXECUTION_FAILED = 'TOOL_3001',
  TOOL_TIMEOUT = 'TOOL_3002',
  TOOL_CANCELLED = 'TOOL_3003',
  INVALID_TOOL_PARAMS = 'TOOL_3004',
  DEPLOYMENT_FAILED = 'TOOL_3005',

  // Schema Validation Errors (4xxx)
  VALIDATION_FAILED = 'SCHEMA_4001',
  INVALID_SCHEMA = 'SCHEMA_4002',
  SCHEMA_NOT_FOUND = 'SCHEMA_4003',
  SCHEMA_VERSION_MISMATCH = 'SCHEMA_4004',

  // Credential Errors (5xxx)
  CREDENTIAL_NOT_FOUND = 'CRED_5001',
  CREDENTIAL_EXPIRED = 'CRED_5002',
  CREDENTIAL_INVALID = 'CRED_5003',
  CREDENTIAL_PROVIDER_FAILED = 'CRED_5004',
  CREDENTIAL_ACCESS_DENIED = 'CRED_5005',

  // Plugin Errors (6xxx)
  PLUGIN_NOT_FOUND = 'PLUGIN_6001',
  PLUGIN_LOAD_FAILED = 'PLUGIN_6002',
  PLUGIN_INCOMPATIBLE = 'PLUGIN_6003',
  PLUGIN_INITIALIZATION_FAILED = 'PLUGIN_6004',

  // Configuration Errors (7xxx)
  CONFIG_LOAD_FAILED = 'CONFIG_7001',
  CONFIG_INVALID = 'CONFIG_7002',
  CONFIG_NOT_FOUND = 'CONFIG_7003',

  // Network/API Errors (8xxx)
  NETWORK_ERROR = 'NET_8001',
  API_ERROR = 'NET_8002',
  RATE_LIMIT_EXCEEDED = 'NET_8003',
  TIMEOUT = 'NET_8004',
  CONNECTION_FAILED = 'NET_8005',

  // Protocol Errors (9xxx) - MCP/JSON-RPC
  INVALID_REQUEST = 'PROTO_9001',
  METHOD_NOT_FOUND = 'PROTO_9002',
  INVALID_PARAMS = 'PROTO_9003',
  INTERNAL_ERROR = 'PROTO_9004',
  PARSE_ERROR = 'PROTO_9005',

  // Generic Errors
  UNKNOWN_ERROR = 'UNKNOWN_0000',
  NOT_IMPLEMENTED = 'NOT_IMPL_0001'
}

/**
 * Error severity levels
 */
export enum ErrorSeverity {
  DEBUG = 'debug',
  INFO = 'info',
  WARNING = 'warning',
  ERROR = 'error',
  CRITICAL = 'critical'
}

/**
 * Base SDK Error class
 * All SDK errors extend this class
 */
export class SDKError extends Error {
  public readonly code: ErrorCode | string;
  public readonly severity: ErrorSeverity;
  public readonly timestamp: Date;
  public readonly cause?: Error;
  public readonly details?: unknown;
  public readonly context?: Record<string, any>;

  constructor(
    code: ErrorCode | string,
    message: string,
    cause?: Error | any,
    options?: {
      severity?: ErrorSeverity;
      details?: unknown;
      context?: Record<string, any>;
    }
  ) {
    super(message);
    
    this.name = 'SDKError';
    this.code = code;
    this.severity = options?.severity || ErrorSeverity.ERROR;
    this.timestamp = new Date();
    this.cause = cause instanceof Error ? cause : undefined;
    this.details = options?.details || (cause && !(cause instanceof Error) ? cause : undefined);
    this.context = options?.context;

    // Maintains proper stack trace for where our error was thrown
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, SDKError);
    }
  }

  /**
   * Convert error to JSON representation
   */
  toJSON(): unknown {
    return {
      name: this.name,
      code: this.code,
      message: this.message,
      severity: this.severity,
      timestamp: this.timestamp.toISOString(),
      details: this.details,
      context: this.context,
      stack: this.stack,
      cause: this.cause ? {
        name: this.cause.name,
        message: this.cause.message,
        stack: this.cause.stack
      } : undefined
    };
  }

  /**
   * Convert error to MCP-compatible error response
   */
  toMCPError(): {
    code: number;
    message: string;
    data?: Record<string, unknown>;
  } {
    return {
      code: this.getMCPErrorCode(),
      message: this.message,
      data: {
        sdkCode: this.code,
        severity: this.severity,
        details: this.details,
        context: this.context
      }
    };
  }

  /**
   * Get MCP/JSON-RPC compatible error code
   */
  private getMCPErrorCode(): number {
    // Map SDK error codes to JSON-RPC error codes
    const codePrefix = this.code.split('_')[0];
    
    switch (codePrefix) {
      case 'PROTO':
        // Protocol errors map to standard JSON-RPC codes
        if (this.code === ErrorCode.PARSE_ERROR) return -32700;
        if (this.code === ErrorCode.INVALID_REQUEST) return -32600;
        if (this.code === ErrorCode.METHOD_NOT_FOUND) return -32601;
        if (this.code === ErrorCode.INVALID_PARAMS) return -32602;
        if (this.code === ErrorCode.INTERNAL_ERROR) return -32603;
        return -32603; // Internal error
      
      case 'TOOL':
      case 'REGISTRY':
        return -32001; // Tool/method errors
      
      case 'SCHEMA':
        return -32602; // Invalid params
      
      case 'CRED':
        return -32002; // Authentication/authorization errors
      
      case 'NET':
        return -32003; // Network/API errors
      
      default:
        return -32603; // Internal error
    }
  }
}

/**
 * Tool execution error
 */
export class ToolExecutionError extends SDKError {
  constructor(
    toolName: string,
    message: string,
    cause?: Error | any,
    options?: {
      details?: unknown;
      context?: Record<string, any>;
    }
  ) {
    super(
      ErrorCode.TOOL_EXECUTION_FAILED,
      `Tool execution failed: ${toolName} - ${message}`,
      cause,
      {
        ...options,
        context: {
          ...options?.context,
          toolName
        }
      }
    );
    this.name = 'ToolExecutionError';
  }
}

/**
 * Validation error
 */
export class ValidationError extends SDKError {
  public readonly validationErrors: unknown[];

  constructor(
    message: string,
    validationErrors: unknown[],
    options?: {
      context?: Record<string, any>;
    }
  ) {
    super(
      ErrorCode.VALIDATION_FAILED,
      message,
      undefined,
      {
        severity: ErrorSeverity.WARNING,
        details: { validationErrors },
        context: options?.context
      }
    );
    this.name = 'ValidationError';
    this.validationErrors = validationErrors;
  }
}

/**
 * Credential error
 */
export class CredentialError extends SDKError {
  constructor(
    message: string,
    code: ErrorCode = ErrorCode.CREDENTIAL_NOT_FOUND,
    options?: {
      details?: unknown;
      context?: Record<string, any>;
      cause?: Error;
    }
  ) {
    super(code, message, options?.cause, {
      severity: ErrorSeverity.ERROR,
      ...options
    });
    this.name = 'CredentialError';
  }
}

/**
 * Network error
 */
export class NetworkError extends SDKError {
  public readonly statusCode?: number;
  public readonly response?: unknown;

  constructor(
    message: string,
    options?: {
      statusCode?: number;
      response?: unknown;
      cause?: Error;
      context?: Record<string, any>;
    }
  ) {
    super(
      ErrorCode.NETWORK_ERROR,
      message,
      options?.cause,
      {
        severity: ErrorSeverity.ERROR,
        details: {
          statusCode: options?.statusCode,
          response: options?.response
        },
        context: options?.context
      }
    );
    this.name = 'NetworkError';
    this.statusCode = options?.statusCode;
    this.response = options?.response;
  }
}

/**
 * Rate limit error
 */
export class RateLimitError extends NetworkError {
  public readonly retryAfter?: number;

  constructor(
    message: string,
    options?: {
      retryAfter?: number;
      statusCode?: number;
      response?: unknown;
      context?: Record<string, any>;
    }
  ) {
    super(message, {
      statusCode: options?.statusCode || 429,
      response: options?.response,
      context: options?.context
    });
    this.name = 'RateLimitError';
    this.retryAfter = options?.retryAfter;
  }
}

/**
 * Timeout error
 */
export class TimeoutError extends SDKError {
  public readonly timeoutMs: number;

  constructor(
    message: string,
    timeoutMs: number,
    options?: {
      context?: Record<string, any>;
    }
  ) {
    super(
      ErrorCode.TIMEOUT,
      message,
      undefined,
      {
        severity: ErrorSeverity.WARNING,
        details: { timeoutMs },
        context: options?.context
      }
    );
    this.name = 'TimeoutError';
    this.timeoutMs = timeoutMs;
  }
}

/**
 * Plugin error
 */
export class PluginError extends SDKError {
  constructor(
    pluginName: string,
    message: string,
    code: ErrorCode = ErrorCode.PLUGIN_LOAD_FAILED,
    options?: {
      cause?: Error;
      details?: unknown;
      context?: Record<string, any>;
    }
  ) {
    super(
      code,
      `Plugin error: ${pluginName} - ${message}`,
      options?.cause,
      {
        severity: ErrorSeverity.ERROR,
        details: options?.details,
        context: {
          ...options?.context,
          pluginName
        }
      }
    );
    this.name = 'PluginError';
  }
}

/**
 * Configuration error
 */
export class ConfigError extends SDKError {
  constructor(
    message: string,
    code: ErrorCode = ErrorCode.CONFIG_INVALID,
    options?: {
      cause?: Error;
      details?: unknown;
      context?: Record<string, any>;
    }
  ) {
    super(code, message, options?.cause, {
      severity: ErrorSeverity.ERROR,
      details: options?.details,
      context: options?.context
    });
    this.name = 'ConfigError';
  }
}

/**
 * Error handler utility
 */
export class ErrorHandler {
  /**
   * Wrap an error as SDKError if it's not already
   */
  static wrap(error: unknown, code?: ErrorCode, context?: Record<string, any>): SDKError {
    if (error instanceof SDKError) {
      return error;
    }

    if (error instanceof Error) {
      return new SDKError(
        code || ErrorCode.UNKNOWN_ERROR,
        error.message,
        error,
        { context }
      );
    }

    return new SDKError(
      code || ErrorCode.UNKNOWN_ERROR,
      String(error),
      undefined,
      { details: error, context }
    );
  }

  /**
   * Check if error is retryable
   */
  static isRetryable(error: SDKError): boolean {
    const retryableCodes = [
      ErrorCode.NETWORK_ERROR,
      ErrorCode.TIMEOUT,
      ErrorCode.RATE_LIMIT_EXCEEDED,
      ErrorCode.CONNECTION_FAILED
    ];

    return retryableCodes.includes(error.code as ErrorCode);
  }

  /**
   * Get retry delay for error
   */
  static getRetryDelay(error: SDKError, attempt: number): number {
    if (error instanceof RateLimitError && error.retryAfter) {
      return error.retryAfter * 1000;
    }

    // Exponential backoff: 1s, 2s, 4s, 8s, ...
    return Math.min(1000 * Math.pow(2, attempt), 30000);
  }

  /**
   * Format error for logging
   */
  static format(error: SDKError): string {
    const parts = [
      `[${error.code}]`,
      error.message
    ];

    if (error.context) {
      parts.push(`Context: ${JSON.stringify(error.context)}`);
    }

    if (error.details) {
      parts.push(`Details: ${JSON.stringify(error.details)}`);
    }

    if (error.cause) {
      parts.push(`Cause: ${error.cause.message}`);
    }

    return parts.join(' | ');
  }

  /**
   * Get error message from unknown error type
   * Safely extracts error message from unknown error type.
   * Returns error.message for Error instances, otherwise converts to string.
   * 
   * @param error - The error of unknown type
   * @returns The error message as a string
   */
  static getErrorMessage(error: unknown): string {
    return error instanceof Error ? error.message : String(error);
  }
}

/**
 * Create a typed error
 */
export function createError(
  code: ErrorCode,
  message: string,
  options?: {
    cause?: Error | any;
    severity?: ErrorSeverity;
    details?: unknown;
    context?: Record<string, any>;
  }
): SDKError {
  return new SDKError(code, message, options?.cause, {
    severity: options?.severity,
    details: options?.details,
    context: options?.context
  });
}

/**
 * Assert condition and throw error if false
 */
export function assert(
  condition: boolean,
  code: ErrorCode,
  message: string,
  context?: Record<string, any>
): asserts condition {
  if (!condition) {
    throw new SDKError(code, message, undefined, { context });
  }
}