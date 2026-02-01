// @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: resource-graph-model
# @GL-charter-version: 2.0.0

import { IndexEntry } from '../indexers/indexer';
import { createLogger } from '../../src/utils/logger';

const logger = createLogger('ResourceGraphModel');

export interface GraphNode {
  id: string;
  path: string;
  type: string;
  language: string;
  semanticAnchor?: string;
  layer?: string;
  charterVersion?: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  type: 'dependency' | 'reference' | 'include' | 'import';
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export class ResourceGraphModel {
  private graphData: GraphData = {
    nodes: [],
    edges: []
  };

  public buildGraph(indexEntries: Map<string, IndexEntry>): void {
    logger.info(`Building graph with ${indexEntries.size} entries`);
    
    // Build nodes
    for (const [path, entry] of indexEntries.entries()) {
      const node: GraphNode = {
        id: this.generateNodeId(path),
        path: entry.path,
        type: entry.type,
        language: entry.language,
        semanticAnchor: entry.semanticAnchor,
        layer: entry.layer,
        charterVersion: entry.charterVersion
      };
      
      this.graphData.nodes.push(node);
    }

    // Build edges
    for (const entry of indexEntries.values()) {
      const sourceId = this.generateNodeId(entry.path);
      
      for (const depPath of entry.dependencies) {
        const depEntry = indexEntries.get(depPath);
        if (depEntry) {
          const targetId = this.generateNodeId(depPath);
          const edge: GraphEdge = {
            source: sourceId,
            target: targetId,
            type: 'dependency'
          };
          
          this.graphData.edges.push(edge);
        }
      }
    }

    logger.info(`Graph built: ${this.graphData.nodes.length} nodes, ${this.graphData.edges.length} edges`);
  }

  private generateNodeId(path: string): string {
    // Generate a unique ID from path
    return path.replace(/[^a-zA-Z0-9]/g, '_');
  }

  public getNodes(): GraphNode[] {
    return this.graphData.nodes;
  }

  public getEdges(): GraphEdge[] {
    return this.graphData.edges;
  }

  public getNodeById(id: string): GraphNode | undefined {
    return this.graphData.nodes.find(n => n.id === id);
  }

  public getNodeByPath(path: string): GraphNode | undefined {
    return this.graphData.nodes.find(n => n.path === path);
  }

  public getDependencies(nodeId: string): GraphNode[] {
    const edges = this.graphData.edges.filter(e => e.source === nodeId);
    return edges.map(e => this.getNodeById(e.target)!).filter(Boolean);
  }

  public getDependents(nodeId: string): GraphNode[] {
    const edges = this.graphData.edges.filter(e => e.target === nodeId);
    return edges.map(e => this.getNodeById(e.source)!).filter(Boolean);
  }

  public getNodesByType(type: string): GraphNode[] {
    return this.graphData.nodes.filter(n => n.type === type);
  }

  public getNodesByLanguage(language: string): GraphNode[] {
    return this.graphData.nodes.filter(n => n.language === language);
  }

  public getNodesBySemanticAnchor(semanticAnchor: string): GraphNode[] {
    return this.graphData.nodes.filter(n => n.semanticAnchor === semanticAnchor);
  }

  public exportGraph(): GraphData {
    return {
      nodes: [...this.graphData.nodes],
      edges: [...this.graphData.edges]
    };
  }

  public importGraph(graphData: GraphData): void {
    this.graphData = {
      nodes: [...graphData.nodes],
      edges: [...graphData.edges]
    };
    logger.info(`Graph imported: ${this.graphData.nodes.length} nodes, ${this.graphData.edges.length} edges`);
  }

  public getStatistics(): { nodeCount: number; edgeCount: number; avgDegree: number } {
    const nodeCount = this.graphData.nodes.length;
    const edgeCount = this.graphData.edges.length;
    const avgDegree = nodeCount > 0 ? (edgeCount * 2) / nodeCount : 0;

    return {
      nodeCount,
      edgeCount,
      avgDegree
    };
  }
}