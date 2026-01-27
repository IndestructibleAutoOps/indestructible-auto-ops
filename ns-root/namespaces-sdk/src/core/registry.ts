/**
 * GL Governance Markers
 * @gl-layer GL-00-NAMESPACE
 * @gl-module ns-root/namespaces-sdk/src/core
 * @gl-semantic-anchor GL-00-SRC_CORE_REGISTRY
 * @gl-evidence-required false
 * GL Unified Charter Activated
 */

/**
 * Tool Registry - Dynamic tool discovery and registration
 * 
 * Maintains a registry of all available tools, adapters, and plugins,
 * supporting dynamic discovery, registration, and querying.
 */

import { Tool, ToolMetadata } from './tool';
import { SDKError, ErrorCode } from './errors';
import { Logger } from '../observability/logger';

/**
 * Tool registration options
 */
export interface ToolRegistrationOptions {
  /** Override existing tool with same name */
  override?: boolean;
  /** Tool category/namespace */
  category?: string;
  /** Tool tags for filtering */
  tags?: string[];
}

/**
 * Tool query filters
 */
export interface ToolQueryFilter {
  /** Filter by category */
  category?: string;
  /** Filter by tags (any match) */
  tags?: string[];
  /** Filter by capability */
  capability?: string;
  /** Filter by adapter name */
  adapter?: string;
  /** Filter by version */
  version?: string;
}

/**
 * Registered tool entry
 */
interface ToolEntry {
  tool: Tool;
  metadata: ToolMetadata;
  registeredAt: Date;
  category?: string;
  tags: string[];
}

/**
 * Tool Registry Class
 * 
 * Responsibilities:
 * - Register and unregister tools at runtime
 * - Support querying tools by name, capability, or adapter
 * - Enable hot-pluggable extension via plugin loading
 * - Maintain thread-safe registry operations
 */
export class ToolRegistry {
  private tools: Map<string, ToolEntry> = new Map();
  private logger: Logger;
  private registryVersion: number = 0;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  /**
   * Register a tool in the registry
   * @param tool Tool instance to register
   * @param options Registration options
   */
  register(tool: Tool, options: ToolRegistrationOptions = {}): void {
    const metadata = tool.getMetadata();
    const toolName = metadata.name;

    // Check if tool already exists
    if (this.tools.has(toolName) && !options.override) {
      throw new SDKError(
        ErrorCode.TOOL_ALREADY_REGISTERED,
        `Tool already registered: ${toolName}. Use override option to replace.`
      );
    }

    // Validate tool metadata
    this.validateToolMetadata(metadata);

    // Create tool entry
    const entry: ToolEntry = {
      tool,
      metadata,
      registeredAt: new Date(),
      category: options.category,
      tags: options.tags || []
    };

    // Register the tool
    this.tools.set(toolName, entry);
    this.registryVersion++;

    this.logger.info(`Tool registered: ${toolName}`, {
      version: metadata.version,
      category: options.category,
      tags: options.tags
    });
  }

  /**
   * Unregister a tool from the registry
   * @param toolName Name of the tool to unregister
   * @returns true if tool was unregistered, false if not found
   */
  unregister(toolName: string): boolean {
    const existed = this.tools.delete(toolName);
    
    if (existed) {
      this.registryVersion++;
      this.logger.info(`Tool unregistered: ${toolName}`);
    }

    return existed;
  }

  /**
   * Get a tool instance by name
   * @param toolName Name of the tool
   * @returns Tool instance or undefined if not found
   */
  getToolInstance(toolName: string): Tool | undefined {
    const entry = this.tools.get(toolName);
    return entry?.tool;
  }

  /**
   * Get tool metadata by name
   * @param toolName Name of the tool
   * @returns Tool metadata or undefined if not found
   */
  getTool(toolName: string): ToolMetadata | undefined {
    const entry = this.tools.get(toolName);
    return entry?.metadata;
  }

  /**
   * Check if a tool is registered
   * @param toolName Name of the tool
   * @returns true if tool is registered
   */
  hasTool(toolName: string): boolean {
    return this.tools.has(toolName);
  }

  /**
   * List all registered tools
   * @param filter Optional filter criteria
   * @returns Array of tool metadata
   */
  listTools(filter?: ToolQueryFilter): ToolMetadata[] {
    let entries = Array.from(this.tools.values());

    // Apply filters
    if (filter) {
      entries = this.applyFilters(entries, filter);
    }

    return entries.map(entry => entry.metadata);
  }

  /**
   * Get tool count
   * @returns Number of registered tools
   */
  getToolCount(): number {
    return this.tools.size;
  }

  /**
   * Get tools by category
   * @param category Category name
   * @returns Array of tool metadata
   */
  getToolsByCategory(category: string): ToolMetadata[] {
    return this.listTools({ category });
  }

  /**
   * Get tools by tag
   * @param tag Tag name
   * @returns Array of tool metadata
   */
  getToolsByTag(tag: string): ToolMetadata[] {
    return this.listTools({ tags: [tag] });
  }

  /**
   * Get tools by adapter
   * @param adapter Adapter name
   * @returns Array of tool metadata
   */
  getToolsByAdapter(adapter: string): ToolMetadata[] {
    return this.listTools({ adapter });
  }

  /**
   * Search tools by keyword
   * @param keyword Search keyword
   * @returns Array of tool metadata
   */
  searchTools(keyword: string): ToolMetadata[] {
    const lowerKeyword = keyword.toLowerCase();
    
    return Array.from(this.tools.values())
      .filter(entry => {
        const metadata = entry.metadata;
        return (
          metadata.name.toLowerCase().includes(lowerKeyword) ||
          metadata.description.toLowerCase().includes(lowerKeyword) ||
          entry.tags.some(tag => tag.toLowerCase().includes(lowerKeyword))
        );
      })
      .map(entry => entry.metadata);
  }

  /**
   * Get registry version
   * Increments on any registration/unregistration
   * @returns Current registry version
   */
  getVersion(): number {
    return this.registryVersion;
  }

  /**
   * Clear all registered tools
   */
  clear(): void {
    const count = this.tools.size;
    this.tools.clear();
    this.registryVersion++;
    
    this.logger.info(`Registry cleared: ${count} tools removed`);
  }

  /**
   * Get registry statistics
   * @returns Registry statistics
   */
  getStats(): {
    totalTools: number;
    categories: Record<string, number>;
    adapters: Record<string, number>;
    version: number;
  } {
    const categories: Record<string, number> = {};
    const adapters: Record<string, number> = {};

    for (const entry of this.tools.values()) {
      // Count by category
      if (entry.category) {
        categories[entry.category] = (categories[entry.category] || 0) + 1;
      }

      // Count by adapter
      const adapter = entry.metadata.adapter;
      if (adapter) {
        adapters[adapter] = (adapters[adapter] || 0) + 1;
      }
    }

    return {
      totalTools: this.tools.size,
      categories,
      adapters,
      version: this.registryVersion
    };
  }

  /**
   * Export registry as JSON
   * @returns JSON representation of registry
   */
  toJSON(): unknown {
    return {
      version: this.registryVersion,
      toolCount: this.tools.size,
      tools: Array.from(this.tools.values()).map(entry => ({
        name: entry.metadata.name,
        version: entry.metadata.version,
        description: entry.metadata.description,
        adapter: entry.metadata.adapter,
        category: entry.category,
        tags: entry.tags,
        registeredAt: entry.registeredAt.toISOString()
      }))
    };
  }

  /**
   * Validate tool metadata
   */
  private validateToolMetadata(metadata: ToolMetadata): void {
    if (!metadata.name || typeof metadata.name !== 'string') {
      throw new SDKError(
        ErrorCode.INVALID_TOOL_METADATA,
        'Tool name is required and must be a string'
      );
    }

    if (!metadata.description || typeof metadata.description !== 'string') {
      throw new SDKError(
        ErrorCode.INVALID_TOOL_METADATA,
        'Tool description is required and must be a string'
      );
    }

    if (!metadata.version || typeof metadata.version !== 'string') {
      throw new SDKError(
        ErrorCode.INVALID_TOOL_METADATA,
        'Tool version is required and must be a string'
      );
    }

    // Validate version format (semantic versioning)
    const versionRegex = /^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$/;
    if (!versionRegex.test(metadata.version)) {
      throw new SDKError(
        ErrorCode.INVALID_TOOL_METADATA,
        `Invalid version format: ${metadata.version}. Expected semantic versioning (e.g., 1.0.0)`
      );
    }
  }

  /**
   * Apply filters to tool entries
   */
  private applyFilters(
    entries: ToolEntry[],
    filter: ToolQueryFilter
  ): ToolEntry[] {
    return entries.filter(entry => {
      // Filter by category
      if (filter.category && entry.category !== filter.category) {
        return false;
      }

      // Filter by tags (any match)
      if (filter.tags && filter.tags.length > 0) {
        const hasMatchingTag = filter.tags.some(tag =>
          entry.tags.includes(tag)
        );
        if (!hasMatchingTag) {
          return false;
        }
      }

      // Filter by adapter
      if (filter.adapter && entry.metadata.adapter !== filter.adapter) {
        return false;
      }

      // Filter by version
      if (filter.version && entry.metadata.version !== filter.version) {
        return false;
      }

      // Filter by capability
      if (filter.capability) {
        const hasCapability = entry.metadata.capabilities?.includes(
          filter.capability
        );
        if (!hasCapability) {
          return false;
        }
      }

      return true;
    });
  }
}