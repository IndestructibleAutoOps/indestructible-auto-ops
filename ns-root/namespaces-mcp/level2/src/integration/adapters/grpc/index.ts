// @GL-governed
// @GL-layer: GL-L6-NAMESPACE
// @GL-semantic: governance-layer-namespace
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/integration/adapters/grpc
 * @gl-semantic-anchor GL-00-ADAPTERS_GRPC_INDEX
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * gRPC Adapter Module - Unified Exports
 * 
 * @module integration/adapters/grpc
 */

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
  type ServiceDefinition,
  type MethodDefinition,
  type ProtoDefinition,
  type MessageDefinition,
  type FieldDefinition,
  type GRPCAdapterConfig
} from './grpc-adapter';