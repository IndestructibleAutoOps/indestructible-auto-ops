/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/modules/module-5e-universal-integration
 * @gl-semantic-anchor GL-00-MODULES_MODULE5E_INDEX
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Module 5E: Universal Integration Hub
 * 
 * Complete integration hub providing:
 * - Universal Adapter: Auto-discovery system (<30s discovery)
 * - Protocol Translator: Multi-protocol support (<100ms translation)
 * - Data Transformer: Format conversion (<50ms transformation)
 * - API Gateway: Unified management (<25ms gateway latency)
 * - Integration Orchestrator: Workflow automation (<1s orchestration)
 * 
 * @module Module5E
 */

// Universal Adapter
export {
  UniversalAdapter,
  createUniversalAdapter,
  DiscoveryProtocol,
  ServiceProtocol,
  ServiceHealth,
  DiscoveredService,
  DiscoveryConfig,
  AdapterConfig,
  ServiceConnection,
  DiscoveryStats
} from './universal-adapter';

// Protocol Translator
export {
  ProtocolTranslator,
  createProtocolTranslator,
  ProtocolType,
  MessageEncoding,
  ProtocolMessage,
  TranslationResult,
  ProtocolConfig,
  TranslatorConfig,
  TranslationStats,
  ProtocolConverter
} from './protocol-translator';

// Data Transformer
export {
  DataTransformer,
  createDataTransformer,
  DataFormat,
  TransformOperation,
  TransformRequest,
  TransformResult,
  TransformerConfig,
  TransformStats,
  FormatConverter
} from './data-transformer';

// API Gateway
export {
  APIGateway,
  createAPIGateway,
  HttpMethod,
  RouteConfig,
  RateLimitConfig,
  AuthConfig,
  CacheConfig,
  TransformConfig,
  GatewayRequest,
  GatewayResponse,
  GatewayConfig,
  GatewayStats
} from './api-gateway';

// Integration Orchestrator
export {
  IntegrationOrchestrator,
  createIntegrationOrchestrator,
  StepType,
  StepStatus,
  WorkflowStatus,
  WorkflowStep,
  WorkflowDefinition,
  ErrorHandlingConfig,
  ErrorHandler,
  WorkflowContext,
  WorkflowExecutionResult,
  StepExecutionResult,
  OrchestratorConfig,
  OrchestratorStats
} from './integration-orchestrator';

// Universal Integration System
export {
  UniversalIntegrationSystem,
  createUniversalIntegrationSystem,
  IntegrationRequest,
  IntegrationResult,
  IntegrationStep,
  SystemConfig,
  SystemStats
} from './universal-integration-system';