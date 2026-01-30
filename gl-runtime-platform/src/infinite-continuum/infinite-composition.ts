// @GL-governed
// @GL-layer: GL100-119
// @GL-semantic: runtime-infinite-continuum
// @GL-charter-version: 4.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

/**
 * GL Infinite Learning Continuum - Infinite Composition
 * Version 20.0.0
 * Unbounded composition generation and optimization
 */

import {
  CompositionTemplate,
  CompositionNode,
  CompositionConstraints,
  ResourceLimits,
  CompositionPerformance
} from './types';
import { v4 as uuidv4 } from 'uuid';

export class InfiniteCompositionEngine {
  private templates: Map<string, CompositionTemplate>;
  private compositionCache: Map<string, any>;
  private config: {
    maxCompositions: number;
    searchDepth: number;
    diversityThreshold: number;
    pruningInterval: number;
  };
  private pruningInterval: NodeJS.Timeout | null = null;

  constructor(config?: Partial<InfiniteCompositionEngine['config']>) {
    this.config = {
      maxCompositions: 1000,
      searchDepth: 5,
      diversityThreshold: 0.3,
      pruningInterval: 300000, // 5 minutes
      ...config
    };

    this.templates = new Map();
    this.compositionCache = new Map();
  }

  /**
   * Start composition engine
   */
  public start(): void {
    if (this.pruningInterval) {
      return;
    }

    this.pruningInterval = setInterval(() => {
      this.pruneCompositions();
    }, this.config.pruningInterval);
  }

  /**
   * Stop composition engine
   */
  public stop(): void {
    if (this.pruningInterval) {
      clearInterval(this.pruningInterval);
      this.pruningInterval = null;
    }
  }

  /**
   * Generate a new composition
   */
  public generateComposition(
    constraints: CompositionConstraints,
    seed?: string
  ): CompositionTemplate | null {
    if (this.templates.size >= this.config.maxCompositions) {
      this.pruneCompositions();
    }

    // Generate composition structure
    const structure = this.generateStructure(constraints, seed);
    if (!structure) {
      return null;
    }

    // Create template
    const template: CompositionTemplate = {
      id: uuidv4(),
      structure,
      constraints,
      performance: {
        quality: 0.5,
        efficiency: 0.5,
        reliability: 0.5,
        lastExecuted: 0
      },
      usage: 0
    };

    this.templates.set(template.id, template);
    return template;
  }

  /**
   * Generate composition structure
   */
  private generateStructure(
    constraints: CompositionConstraints,
    seed?: string
  ): CompositionNode[] | null {
    const structure: CompositionNode[] = [];
    const nodeTypes = (constraints.allowedTypes as CompositionNode['type'][]) || ['algorithm', 'data', 'control', 'transformation'];
    const depth = Math.min(this.config.searchDepth, constraints.maxComplexity);

    try {
      for (let i = 0; i < depth; i++) {
        const nodeType = nodeTypes[Math.floor(Math.random() * nodeTypes.length)];
        const node: CompositionNode = {
          id: uuidv4(),
          type: nodeType,
          config: this.generateNodeConfig(nodeType, seed),
          dependencies: this.generateDependencies(i, structure)
        };

        structure.push(node);
      }

      // Validate structure
      if (!this.validateStructure(structure, constraints)) {
        return null;
      }

      return structure;
    } catch (error) {
      console.error('Failed to generate structure:', error);
      return null;
    }
  }

  /**
   * Generate node configuration
   */
  private generateNodeConfig(nodeType: CompositionNode['type'], seed?: string): any {
    const baseConfig: Record<string, any> = {
      seed: seed || Date.now().toString(),
      timestamp: Date.now()
    };

    switch (nodeType) {
      case 'algorithm':
        return {
          ...baseConfig,
          algorithmType: this.randomChoice(['transform', 'aggregate', 'filter', 'map']),
          parameters: {
            iterations: Math.floor(Math.random() * 100) + 1,
            threshold: Math.random(),
            learningRate: Math.random() * 0.1
          }
        };

      case 'data':
        return {
          ...baseConfig,
          dataType: this.randomChoice(['stream', 'batch', 'cache', 'persistent']),
          size: Math.floor(Math.random() * 1000) + 1,
          format: this.randomChoice(['json', 'binary', 'text', 'protobuf'])
        };

      case 'control':
        return {
          ...baseConfig,
          controlType: this.randomChoice(['sequence', 'parallel', 'conditional', 'loop']),
          condition: this.randomChoice(['true', 'false', 'random', 'computed']),
          maxIterations: Math.floor(Math.random() * 10) + 1
        };

      case 'transformation':
        return {
          ...baseConfig,
          transformType: this.randomChoice(['normalize', 'encode', 'decode', 'compress']),
          parameters: {
            preserveOrder: Math.random() < 0.5,
            compress: Math.random() < 0.3
          }
        };

      default:
        return baseConfig;
    }
  }

  /**
   * Generate dependencies for a node
   */
  private generateDependencies(index: number, structure: CompositionNode[]): string[] {
    const dependencies: string[] = [];
    
    // Add dependency to previous node with some probability
    if (index > 0 && Math.random() < 0.7) {
      dependencies.push(structure[index - 1].id);
    }

    // Add random dependency to earlier nodes
    if (index > 2 && Math.random() < 0.3) {
      const randomIndex = Math.floor(Math.random() * (index - 1));
      dependencies.push(structure[randomIndex].id);
    }

    return dependencies;
  }

  /**
   * Validate composition structure
   */
  private validateStructure(
    structure: CompositionNode[],
    constraints: CompositionConstraints
  ): boolean {
    // Check complexity
    if (structure.length > constraints.maxComplexity) {
      return false;
    }

    // Check for cycles
    if (this.hasCycles(structure)) {
      return false;
    }

    // Check node types
    const allowedTypes = constraints.allowedTypes || ['algorithm', 'data', 'control', 'transformation'];
    for (const node of structure) {
      if (!allowedTypes.includes(node.type)) {
        return false;
      }
    }

    // Check dependencies
    for (const node of structure) {
      for (const depId of node.dependencies) {
        const depExists = structure.some(n => n.id === depId);
        if (!depExists) {
          return false;
        }
      }
    }

    return true;
  }

  /**
   * Check for cycles in composition
   */
  private hasCycles(structure: CompositionNode[]): boolean {
    const visited = new Set<string>();
    const recursionStack = new Set<string>();

    const hasCycle = (nodeId: string): boolean => {
      visited.add(nodeId);
      recursionStack.add(nodeId);

      const node = structure.find(n => n.id === nodeId);
      if (!node) {
        recursionStack.delete(nodeId);
        return false;
      }

      for (const depId of node.dependencies) {
        if (!visited.has(depId)) {
          if (hasCycle(depId)) {
            return true;
          }
        } else if (recursionStack.has(depId)) {
          return true;
        }
      }

      recursionStack.delete(nodeId);
      return false;
    };

    for (const node of structure) {
      if (!visited.has(node.id)) {
        if (hasCycle(node.id)) {
          return true;
        }
      }
    }

    return false;
  }

  /**
   * Optimize composition
   */
  public optimizeComposition(templateId: string): CompositionTemplate | null {
    const template = this.templates.get(templateId);
    if (!template) {
      return null;
    }

    // Optimize structure
    const optimizedStructure = this.optimizeStructure(template.structure, template.constraints);
    if (!optimizedStructure) {
      return null;
    }

    // Update template
    template.structure = optimizedStructure;
    template.performance.quality = Math.min(1.0, template.performance.quality + 0.1);
    template.performance.efficiency = Math.min(1.0, template.performance.efficiency + 0.05);

    return template;
  }

  /**
   * Optimize composition structure
   */
  private optimizeStructure(
    structure: CompositionNode[],
    constraints: CompositionConstraints
  ): CompositionNode[] | null {
    const optimized: CompositionNode[] = [];

    // Remove redundant nodes
    for (const node of structure) {
      const isRedundant = this.isRedundantNode(node, optimized);
      if (!isRedundant) {
        optimized.push(node);
      }
    }

    // Validate optimized structure
    if (!this.validateStructure(optimized, constraints)) {
      return structure; // Return original if optimization breaks validity
    }

    return optimized;
  }

  /**
   * Check if node is redundant
   */
  private isRedundantNode(node: CompositionNode, optimized: CompositionNode[]): boolean {
    // Check for duplicate configurations
    for (const existing of optimized) {
      if (existing.type === node.type) {
        const configMatch = JSON.stringify(existing.config) === JSON.stringify(node.config);
        const depsMatch = JSON.stringify(existing.dependencies) === JSON.stringify(node.dependencies);
        
        if (configMatch && depsMatch) {
          return true;
        }
      }
    }

    return false;
  }

  /**
   * Execute composition
   */
  public executeComposition(templateId: string, input: any): any {
    const template = this.templates.get(templateId);
    if (!template) {
      throw new Error('Composition template not found');
    }

    // Check cache
    const cacheKey = `${templateId}_${JSON.stringify(input)}`;
    if (this.compositionCache.has(cacheKey)) {
      return this.compositionCache.get(cacheKey);
    }

    try {
      // Execute composition (simplified)
      const result = this.executeNodes(template.structure, input);

      // Update performance
      template.usage++;
      template.performance.lastExecuted = Date.now();
      template.performance.reliability = 
        template.performance.reliability * 0.9 + 0.1;

      // Cache result
      if (this.compositionCache.size < 1000) {
        this.compositionCache.set(cacheKey, result);
      }

      return result;
    } catch (error) {
      template.performance.reliability = 
        template.performance.reliability * 0.9;
      throw error;
    }
  }

  /**
   * Execute composition nodes
   */
  private executeNodes(structure: CompositionNode[], input: any): any {
    const nodeMap = new Map<string, any>();
    
    // Execute nodes in dependency order
    const executionOrder = this.topologicalSort(structure);
    
    let result = input;
    for (const nodeId of executionOrder) {
      const node = structure.find(n => n.id === nodeId);
      if (!node) {
        continue;
      }

      // Gather inputs from dependencies
      const nodeInputs: any[] = [];
      for (const depId of node.dependencies) {
        if (nodeMap.has(depId)) {
          nodeInputs.push(nodeMap.get(depId));
        }
      }

      // Execute node
      const nodeOutput = this.executeNode(node, result, nodeInputs);
      nodeMap.set(nodeId, nodeOutput);
      result = nodeOutput;
    }

    return result;
  }

  /**
   * Execute a single node
   */
  private executeNode(node: CompositionNode, input: any, dependencyInputs: any[]): any {
    switch (node.type) {
      case 'algorithm':
        return this.executeAlgorithmNode(node, input, dependencyInputs);
      
      case 'data':
        return this.executeDataNode(node, input, dependencyInputs);
      
      case 'control':
        return this.executeControlNode(node, input, dependencyInputs);
      
      case 'transformation':
        return this.executeTransformationNode(node, input, dependencyInputs);
      
      default:
        return input;
    }
  }

  /**
   * Execute algorithm node
   */
  private executeAlgorithmNode(node: CompositionNode, input: any, dependencyInputs: any[]): any {
    const params = node.config.parameters || {};
    
    switch (node.config.algorithmType) {
      case 'transform':
        return { transformed: true, data: input, ...params };
      
      case 'aggregate':
        const aggregated = [...dependencyInputs, input];
        return { count: aggregated.length, sum: aggregated.length, data: aggregated };
      
      case 'filter':
        return { filtered: true, data: input, threshold: params.threshold };
      
      case 'map':
        return { mapped: true, data: input, iterations: params.iterations };
      
      default:
        return input;
    }
  }

  /**
   * Execute data node
   */
  private executeDataNode(node: CompositionNode, input: any, dependencyInputs: any[]): any {
    return {
      dataType: node.config.dataType,
      size: node.config.size,
      format: node.config.format,
      data: input
    };
  }

  /**
   * Execute control node
   */
  private executeControlNode(node: CompositionNode, input: any, dependencyInputs: any[]): any {
    switch (node.config.controlType) {
      case 'sequence':
        return { sequenced: true, data: input };
      
      case 'parallel':
        return { parallel: true, data: input, branches: dependencyInputs.length };
      
      case 'conditional':
        const condition = node.config.condition === 'true' || 
                         (node.config.condition === 'random' && Math.random() < 0.5);
        return { conditional: true, data: input, condition };
      
      case 'loop':
        return { looped: true, data: input, iterations: node.config.maxIterations };
      
      default:
        return input;
    }
  }

  /**
   * Execute transformation node
   */
  private executeTransformationNode(node: CompositionNode, input: any, dependencyInputs: any[]): any {
    const params = node.config.parameters || {};

    switch (node.config.transformType) {
      case 'normalize':
        return { normalized: true, data: input, preserveOrder: params.preserveOrder };
      
      case 'encode':
        return { encoded: true, data: input };
      
      case 'decode':
        return { decoded: true, data: input };
      
      case 'compress':
        return { compressed: true, data: input, isCompressed: params.compress };
      
      default:
        return input;
    }
  }

  /**
   * Topological sort for dependency resolution
   */
  private topologicalSort(structure: CompositionNode[]): string[] {
    const visited = new Set<string>();
    const result: string[] = [];

    const visit = (nodeId: string) => {
      if (visited.has(nodeId)) {
        return;
      }

      visited.add(nodeId);
      const node = structure.find(n => n.id === nodeId);
      if (node) {
        for (const depId of node.dependencies) {
          visit(depId);
        }
      }
      result.push(nodeId);
    };

    for (const node of structure) {
      visit(node.id);
    }

    return result;
  }

  /**
   * Prune low-usage compositions
   */
  private pruneCompositions(): void {
    const toRemove: string[] = [];

    for (const [id, template] of this.templates.entries()) {
      if (template.usage < 5 && template.performance.quality < 0.6) {
        toRemove.push(id);
      }
    }

    for (const id of toRemove) {
      this.templates.delete(id);
    }

    // Also clear cache periodically
    if (this.compositionCache.size > 500) {
      this.compositionCache.clear();
    }
  }

  /**
   * Get composition by ID
   */
  public getComposition(templateId: string): CompositionTemplate | null {
    return this.templates.get(templateId) || null;
  }

  /**
   * Get all compositions
   */
  public getAllCompositions(): CompositionTemplate[] {
    return Array.from(this.templates.values());
  }

  /**
   * Get composition statistics
   */
  public getStatistics(): {
    totalCompositions: number;
    averageQuality: number;
    averageEfficiency: number;
    totalExecutions: number;
    cacheSize: number;
  } {
    const compositions = Array.from(this.templates.values());
    
    const totalQuality = compositions.reduce((sum, c) => sum + c.performance.quality, 0);
    const totalEfficiency = compositions.reduce((sum, c) => sum + c.performance.efficiency, 0);
    const totalExecutions = compositions.reduce((sum, c) => sum + c.usage, 0);

    return {
      totalCompositions: compositions.length,
      averageQuality: compositions.length > 0 ? totalQuality / compositions.length : 0,
      averageEfficiency: compositions.length > 0 ? totalEfficiency / compositions.length : 0,
      totalExecutions,
      cacheSize: this.compositionCache.size
    };
  }

  /**
   * Search compositions by type
   */
  public searchByType(type: CompositionNode['type']): CompositionTemplate[] {
    return Array.from(this.templates.values()).filter(template =>
      template.structure.some(node => node.type === type)
    );
  }

  /**
   * Get similar compositions
   */
  public getSimilarCompositions(templateId: string, limit: number = 5): CompositionTemplate[] {
    const target = this.templates.get(templateId);
    if (!target) {
      return [];
    }

    const similarities: Array<{ id: string; similarity: number }> = [];

    for (const [id, template] of this.templates.entries()) {
      if (id === templateId) {
        continue;
      }

      const similarity = this.calculateCompositionSimilarity(target, template);
      similarities.push({ id, similarity });
    }

    similarities.sort((a, b) => b.similarity - a.similarity);

    return similarities
      .slice(0, limit)
      .map(s => this.templates.get(s.id)!)
      .filter(t => t !== undefined);
  }

  /**
   * Calculate composition similarity
   */
  private calculateCompositionSimilarity(
    a: CompositionTemplate,
    b: CompositionTemplate
  ): number {
    // Compare structure
    const structureSimilarity = this.calculateStructureSimilarity(a.structure, b.structure);
    
    // Compare constraints
    const constraintSimilarity = 
      a.constraints.maxComplexity === b.constraints.maxComplexity ? 0.5 : 0;
    
    // Compare performance
    const performanceSimilarity = 
      Math.abs(a.performance.quality - b.performance.quality) +
      Math.abs(a.performance.efficiency - b.performance.efficiency);

    return (structureSimilarity * 0.6) + (constraintSimilarity * 0.2) + 
           (Math.max(0, 1 - performanceSimilarity) * 0.2);
  }

  /**
   * Calculate structure similarity
   */
  private calculateStructureSimilarity(structureA: CompositionNode[], structureB: CompositionNode[]): number {
    if (structureA.length === 0 && structureB.length === 0) {
      return 1;
    }

    if (structureA.length === 0 || structureB.length === 0) {
      return 0;
    }

    const maxLength = Math.max(structureA.length, structureB.length);
    let matches = 0;

    for (let i = 0; i < maxLength; i++) {
      const nodeA = structureA[i];
      const nodeB = structureB[i];

      if (!nodeA || !nodeB) {
        continue;
      }

      if (nodeA.type === nodeB.type) {
        matches++;
      }
    }

    return matches / maxLength;
  }

  /**
   * Helper: random choice from array
   */
  private randomChoice<T>(options: T[]): T {
    return options[Math.floor(Math.random() * options.length)];
  }

  /**
   * Export compositions as JSON
   */
  public exportCompositions(): string {
    const compositions = Array.from(this.templates.values());
    return JSON.stringify(compositions, null, 2);
  }

  /**
   * Import compositions from JSON
   */
  public importCompositions(json: string): void {
    try {
      const compositions = JSON.parse(json);
      
      for (const comp of compositions) {
        this.templates.set(comp.id, comp);
      }
    } catch (error) {
      console.error('Failed to import compositions:', error);
    }
  }
}