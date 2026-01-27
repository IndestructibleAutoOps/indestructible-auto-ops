/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src
 * @gl-semantic-anchor GL-00-NAMESPAC_SRC_INDEX
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * namespace-sdk - Main Entry Point
 * 
 * A Machine-Native, Auditable Platform Integration Layer for MCP Tool Wrapping
 */

// Core exports
export { NamespaceSDK, SDKConfig, SDKState } from './core/sdk';
export { ToolRegistry, ToolRegistrationOptions, ToolQueryFilter } from './core/registry';
export {
  Tool,
  ToolMetadata,
  ToolContext,
  ToolInvocationResult,
  JSONSchema,
  CredentialRequirement,
  SimpleTool,
  ToolBuilder,
  createTool
} from './core/tool';
export {
  SDKError,
  ErrorCode,
  ErrorSeverity,
  ToolExecutionError,
  ValidationError,
  CredentialError,
  NetworkError,
  RateLimitError,
  TimeoutError,
  PluginError,
  ConfigError,
  ErrorHandler,
  createError,
  assert
} from './core/errors';

// Schema exports
export {
  SchemaValidator,
  ValidationResult,
  ValidationErrorDetail,
  ValidatorOptions,
  SchemaUtils
} from './schema/validator';
export {
  SchemaType,
  SchemaFormat,
  PropertySchema,
  ObjectSchema,
  ArraySchema,
  StringSchema,
  NumberSchema,
  BooleanSchema,
  UnionSchema,
  SchemaMetadata,
  CompleteSchema,
  SchemaBuilder,
  CommonSchemas,
  createSchema,
  isObjectSchema,
  isArraySchema,
  isStringSchema,
  isNumberSchema
} from './schema/types';
export {
  SchemaRegistry,
  SchemaVersion,
  CompatibilityResult
} from './schema/registry';

// Credential exports
export { CredentialManager, CredentialManagerOptions } from './credentials/manager';
export {
  Credential,
  CredentialType,
  CredentialConfig,
  CredentialProvider,
  OAuthCredential,
  ApiKeyCredential,
  BasicAuthCredential,
  SshKeyCredential,
  CertificateCredential,
  ServiceAccountCredential,
  ProviderConfig,
  EnvProviderConfig,
  FileProviderConfig,
  VaultProviderConfig,
  CloudProviderConfig,
  RotationPolicy,
  CredentialUsage,
  CredentialValidation,
  SecurityOptions,
  isOAuthCredential,
  isApiKeyCredential,
  isBasicAuthCredential,
  isSshKeyCredential,
  isCertificateCredential,
  isServiceAccountCredential
} from './credentials/types';
export { EnvCredentialProvider, EnvProviderOptions } from './credentials/providers/env';
export { FileCredentialProvider, FileProviderOptions } from './credentials/providers/file';
export { VaultCredentialProvider, VaultProviderOptions } from './credentials/providers/vault';
export { CloudCredentialProvider, CloudProviderOptions, CloudProviderType } from './credentials/providers/cloud';

// Observability exports
export {
  Logger,
  LogLevel,
  LogEntry,
  LoggerOptions,
  createLogger
} from './observability/logger';
export {
  Tracer,
  Span,
  SpanStatus,
  SpanAttributes,
  SpanEvent,
  TracerOptions,
  createTracer
} from './observability/tracer';
export {
  MetricsCollector,
  MetricType,
  MetricLabels,
  MetricValue,
  HistogramBucket,
  HistogramData,
  MetricsCollectorOptions,
  createMetricsCollector
} from './observability/metrics';
export {
  AuditLogger,
  AuditEvent,
  AuditLoggerOptions,
  createAuditLogger
} from './observability/audit';

// Configuration exports
export {
  ConfigManager,
  SDKConfig as ConfigSDKConfig,
  ConfigSource,
  ConfigManagerOptions,
  createConfigManager
} from './config';

// Plugin exports
export {
  PluginLoader,
  Plugin,
  PluginMetadata,
  PluginContext,
  PluginLoaderOptions,
  createPluginLoader
} from './plugins';

// Version
export const VERSION = '1.0.0';

/**
 * Create and initialize a new SDK instance
 * 
 * @param config SDK configuration
 * @returns Initialized SDK instance
 * 
 * @example
 * ```typescript
 * import { createSDK } from 'namespace-sdk';
 * 
 * const sdk = await createSDK({
 *   debug: true,
 *   credentials: {
 *     providers: ['env', 'file'],
 *     defaultProvider: 'env'
 *   }
 * });
 * 
 * // Register tools
 * sdk.registerTool(myTool);
 * 
 * // Invoke tools
 * const result = await sdk.invokeTool('my_tool', { param: 'value' });
 * ```
 */
export async function createSDK(config?: SDKConfig): Promise<NamespaceSDK> {
  const sdk = new NamespaceSDK(config);
  await sdk.initialize();
  return sdk;
}

/**
 * Default export
 */
export default {
  NamespaceSDK,
  createSDK,
  VERSION
};