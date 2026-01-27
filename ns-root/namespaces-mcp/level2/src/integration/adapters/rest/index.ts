/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/integration/adapters/rest
 * @gl-semantic-anchor GL-00-ADAPTERS_REST_INDEX
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * REST Adapter Module - Unified Exports
 * 
 * @module integration/adapters/rest
 */

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
} from './rest-adapter';