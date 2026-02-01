// @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: resource-graph-resolver
# @GL-charter-version: 2.0.0

import { GraphNode, GraphData } from '../graph-model/graph-model';
import { IndexEntry } from '../indexers/indexer';
import { createLogger } from '../../src/utils/logger';

const logger = createLogger('ResourceGraphResolver');

export interface ResolutionResult {
  found: boolean;
  nodes?: GraphNode[];
  missing?: string[];
  paths?: string[];
}

export class ResourceGraphResolver {
  private graphData: GraphData;
  private indexEntries: Map<string, IndexEntry>;

  constructor(graphData: GraphData, indexEntries: Map<string, IndexEntry>) {
    this.graphData = graphData;
    this.indexEntries = indexEntries;
  }

  public resolveFile(path: string): GraphNode | null {
    const node = this.graphData.nodes.find(n => n.path === path);
    if (!node) {
      logger.warn(`File not found in graph: ${path}`);
    }
    return node || null;
  }

  public resolvePath(pattern: string): ResolutionResult {
    const regex = new RegExp(pattern.replace('*', '.*'));
    const matchingNodes = this.graphData.nodes.filter(n => regex.test(n.path));
    
    return {
      found: matchingNodes.length > 0,
      nodes: matchingNodes.length > 0 ? matchingNodes : undefined,
      paths: matchingNodes.map(n => n.path)
    };
  }

  public resolveDependency(fromPath: string, toPath: string): boolean {
    const fromNode = this.resolveFile(fromPath);
    const toNode = this.resolveFile(toPath);
    
    if (!fromNode || !toNode) {
      return false;
    }

    const edge = this.graphData.edges.find(
      e => e.source === fromNode.id && e.target === toNode.id
    );
    
    return !!edge;
  }

  public resolveMissingDependencies(): ResolutionResult {
    const missing: string[] = [];
    
    for (const entry of this.indexEntries.values()) {
      for (const depPath of entry.dependencies) {
        const depNode = this.resolveFile(depPath);
        if (!depNode) {
          missing.push(`${entry.path} -> ${depPath}`);
        }
      }
    }

    return {
      found: missing.length === 0,
      missing: missing.length > 0 ? missing : undefined
    };
  }

  public resolveMissingFiles(expectedPaths: string[]): ResolutionResult {
    const missing: string[] = [];
    
    for (const path of expectedPaths) {
      const node = this.resolveFile(path);
      if (!node) {
        missing.push(path);
      }
    }

    return {
      found: missing.length === 0,
      missing: missing.length > 0 ? missing : undefined
    };
  }

  public resolveOrphanNodes(): GraphNode[] {
    const nodesWithEdges = new Set<string>();
    
    this.graphData.edges.forEach(edge => {
      nodesWithEdges.add(edge.source);
      nodesWithEdges.add(edge.target);
    });

    const orphans = this.graphData.nodes.filter(
      n => !nodesWithEdges.has(n.id)
    );

    return orphans;
  }

  public resolveCyclicDependencies(): string[][] {
    const visited = new Set<string>();
    const recursionStack = new Set<string>();
    const cycles: string[][] = [];
    const path: string[] = [];

    const dfs = (nodeId: string): void => {
      visited.add(nodeId);
      recursionStack.add(nodeId);
      path.push(nodeId);

      const edges = this.graphData.edges.filter(e => e.source === nodeId);
      for (const edge of edges) {
        if (!visited.has(edge.target)) {
          dfs(edge.target);
        } else if (recursionStack.has(edge.target)) {
          // Found a cycle
          const cycleStart = path.indexOf(edge.target);
          const cycle = path.slice(cycleStart).concat(edge.target);
          cycles.push(cycle);
        }
      }

      path.pop();
      recursionStack.delete(nodeId);
    };

    for (const node of this.graphData.nodes) {
      if (!visited.has(node.id)) {
        dfs(node.id);
      }
    }

    return cycles;
  }

  public resolveGovernanceCompliance(): ResolutionResult {
    const nonCompliant: string[] = [];
    
    for (const node of this.graphData.nodes) {
      if (!node.semanticAnchor) {
        nonCompliant.push(node.path);
      }
    }

    return {
      found: nonCompliant.length === 0,
      missing: nonCompliant.length > 0 ? nonCompliant : undefined
    };
  }

  public resolveBySemanticAnchor(semanticAnchor: string): GraphNode[] {
    return this.graphData.nodes.filter(n => n.semanticAnchor === semanticAnchor);
  }

  public resolveByType(type: string): GraphNode[] {
    return this.graphData.nodes.filter(n => n.type === type);
  }

  public resolveByLanguage(language: string): GraphNode[] {
    return this.graphData.nodes.filter(n => n.language === language);
  }

  public exportResolutions(): {
    missingDependencies: string[];
    orphanNodes: string[];
    cyclicDependencies: string[][];
    nonCompliantFiles: string[];
  } {
    const missingDeps = this.resolveMissingDependencies();
    const orphans = this.resolveOrphanNodes();
    const cycles = this.resolveCyclicDependencies();
    const compliance = this.resolveGovernanceCompliance();

    return {
      missingDependencies: missingDeps.missing || [],
      orphanNodes: orphans.map(n => n.path),
      cyclicDependencies: cycles,
      nonCompliantFiles: compliance.missing || []
    };
  }
}