// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * GRAIL Registry Module
 * @module grail::registry
 * @description Namespace registration and component management
 */

export {
  GrailRegistry,
  GrailRegistryError,
  getGlobalRegistry,
  createRegistry
} from './grail-registry.js';

export type {
  GrailRegistryOptions,
  RegistryEventType,
  RegistryEventData,
  RegistryEventHandler,
  RegistryStats,
  RegistryExport,
  RegistryErrorCode
} from './grail-registry.js';
