// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GRAIL Standard Protocol Types
 * @module grail::types::protocols::standard
 * @description Type definitions for standard communication protocols
 * @version 1.0.0
 */

/**
 * Standard Protocol Message
 */
export interface ProtocolMessage {
  readonly type: string;
  readonly payload: unknown;
  readonly signature: Uint8Array;
  readonly timestamp: Date;
}

/**
 * Standard Protocol Interface
 */
export interface StandardProtocol {
  send(message: ProtocolMessage): Promise<void>;
  receive(): AsyncGenerator<ProtocolMessage>;
  verify(message: ProtocolMessage): Promise<boolean>;
  seal(message: ProtocolMessage): Promise<ProtocolMessage>;
}
