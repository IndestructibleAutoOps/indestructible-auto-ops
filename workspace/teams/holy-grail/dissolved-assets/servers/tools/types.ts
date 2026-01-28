// @GL-governed
// @GL-layer: GL-L0-UNCLASSIFIED
// @GL-semantic: governance-layer-unclassified
// @GL-revision: 1.0.0
// @GL-status: active

/**
 * Shared type definitions for namespace-mcp dissolved tools
 * @module tools/types
 */

export interface ToolDefinition {
  name: string;
  description: string;
  sourceModule: string;
  inputSchema: object;
  quantumEnabled: boolean;
  fallbackEnabled?: boolean;
  priority: number;
}

export interface ResourceDefinition {
  uri: string;
  name: string;
  description: string;
  mimeType: string;
  metadata: object;
}

export interface PromptDefinition {
  name: string;
  description: string;
  arguments: Array<{ name: string; description: string; required: boolean }>;
}
