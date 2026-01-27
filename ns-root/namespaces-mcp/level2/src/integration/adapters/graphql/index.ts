/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-mcp/level2/src/integration/adapters/graphql
 * @gl-semantic-anchor GL-00-ADAPTERS_GRAPHQL_INDEX
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * GraphQL Adapter Module - Unified Exports
 * 
 * @module integration/adapters/graphql
 */

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
  type SchemaValidationResult,
  type QueryComplexityResult,
  type GraphQLAdapterConfig,
  type Subscription,
  type Observable
} from './graphql-adapter';