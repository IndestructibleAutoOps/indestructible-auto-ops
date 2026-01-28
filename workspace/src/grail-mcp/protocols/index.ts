// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GRAIL Protocols Module
 * @module grail::protocols
 * @description Communication standards and protocol bridges
 * @version 1.0.0
 */

// Re-export protocol types from types modules
export type {
  ProtocolMessage,
  StandardProtocol
} from '../types/protocols-standard.js';

export type {
  GrailToolDefinition,
  GrailResourceDefinition,
  MCPExtension
} from '../types/protocols-mcp.js';

export type {
  ProtocolAdapter,
  InterProtocolBridge
} from '../types/protocols-bridge.js';
