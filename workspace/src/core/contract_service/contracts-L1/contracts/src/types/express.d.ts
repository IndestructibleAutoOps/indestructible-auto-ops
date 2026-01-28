// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * Express Request type extensions
 * Extends the Express Request interface to include custom properties
 */

declare namespace Express {
  export interface Request {
    traceId?: string;
  }
}
