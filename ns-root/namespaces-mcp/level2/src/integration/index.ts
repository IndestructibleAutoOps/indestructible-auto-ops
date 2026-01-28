// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/integration
 * @gl-semantic-anchor GL-00-SRC_INTEGRAT_INDEX
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Integration & Extension Layer - Unified Exports
 * 
 * Provides comprehensive integration capabilities including multi-protocol adapters,
 * plugin system, extension management, middleware chain, event bridge, and adapter registry.
 * 
 * @module integration
 */

// REST Adapter
export {
  RESTAdapter,
  createRESTAdapter,
  HTTPMethod,
  CircuitState,
  type RequestOptions,
  type Response,
  type RequestConfig,
  type BatchRequest,
  type BatchResponse,
  type RequestInterceptor,
  type ResponseInterceptor,
  type CircuitBreakerConfig,
  type RESTAdapterConfig
} from './adapters/rest';

// GraphQL Adapter
export {
  GraphQLAdapter,
  createGraphQLAdapter,
  OperationType,
  type Variables,
  type QueryResult,
  type GraphQLError,
  type MutationResult,
  type SubscriptionResult,
  type BatchLoadFn,
  type DataLoaderOptions,
  type GraphQLAdapterConfig
} from './adapters/graphql';

// gRPC Adapter
export {
  GRPCAdapter,
  createGRPCAdapter,
  CallType,
  CredentialsType,
  LoadBalancingStrategy,
  ConnectionState,
  type Metadata,
  type CallOptions,
  type Stream,
  type ClientStream,
  type BidiStream,
  type Status,
  type GRPCInterceptor,
  type GRPCAdapterConfig
} from './adapters/grpc';

// Webhook Adapter
export {
  WebhookAdapter,
  createWebhookAdapter,
  type WebhookConfig,
  type RetryConfig,
  type WebhookDelivery,
  type WebhookEvent,
  type WebhookStats,
  type WebhookHealth,
  type BatchDeliveryOptions
} from './adapters/webhook';

// Plugin System
export {
  PluginSystem,
  createPluginSystem,
  PluginState,
  type PluginMetadata,
  type PluginContext,
  type Plugin,
  type PluginSystemConfig
} from './plugins/plugin-system';

// Extension Manager
export {
  ExtensionManager,
  createExtensionManager,
  ExtensionState,
  type ExtensionMetadata,
  type ExtensionConfig,
  type Extension,
  type ExtensionContext,
  type ExtensionLoadOptions,
  type ExtensionSearchCriteria,
  type MarketplaceExtension
} from './extensions';

// Event Bridge
export {
  EventBridge,
  createEventBridge,
  type Event,
  type EventPattern,
  type EventHandler,
  type EventSubscription,
  type SubscriptionOptions,
  type EventRoute,
  type EventTarget,
  type EventSchema,
  type ArchivedEvent,
  type EventBridgeStats
} from './events';

// Adapter Registry
export {
  AdapterRegistry,
  createAdapterRegistry,
  type Adapter,
  type AdapterMetadata,
  type AdapterRegistrationOptions,
  type AdapterMetrics,
  type AdapterHealth,
  type AdapterSelectionCriteria,
  type ProtocolNegotiation
} from './registry';

// Middleware Chain
export {
  MiddlewareChain,
  createMiddlewareChain,
  type Middleware,
  type MiddlewareContext,
  type NextFunction
} from './middleware/middleware-chain';

// Integration Bridge
export * from './integration-bridge';

/**
 * Create complete integration system
 */
export function createIntegrationSystem(config?: {
  rest?: unknown;
  graphql?: unknown;
  grpc?: unknown;
  webhook?: unknown;
  plugins?: unknown;
  extensions?: unknown;
  eventBridge?: unknown;
  adapterRegistry?: unknown;
}) {
  const rest = config?.rest ? createRESTAdapter(config.rest) : undefined;
  const graphql = config?.graphql ? createGraphQLAdapter(config.graphql) : undefined;
  const grpc = config?.grpc ? createGRPCAdapter(config.grpc) : undefined;
  const webhook = config?.webhook ? createWebhookAdapter(config.webhook) : undefined;
  const plugins = createPluginSystem(config?.plugins);
  const extensions = createExtensionManager(config?.extensions);
  const eventBridge = createEventBridge(config?.eventBridge);
  const adapterRegistry = createAdapterRegistry(config?.adapterRegistry);

  return {
    rest,
    graphql,
    grpc,
    webhook,
    plugins,
    extensions,
    eventBridge,
    adapterRegistry
  };
}
