// @GL-governed
// @GL-layer: gl90-99
// @GL-semantic: global-dag-visualizer
// @GL-charter-version: 2.0.0

import { GlobalDAGGraph, DAGNode } from '../dag-model';

/**
 * Global DAG Visualizer
 * Generates visualization data for the global DAG
 */

export interface VisualizationData {
  nodes: Array<{
    id: string;
    type: string;
    status: string;
    x: number;
    y: number;
  }>;
  edges: Array<{
    source: string;
    target: string;
    type: string;
  }>;
  metadata: {
    totalNodes: number;
    totalEdges: number;
    layers: number;
  };
}

export class GlobalDAGVisualizer {
  private graph: GlobalDAGGraph;
  
  constructor(graph: GlobalDAGGraph) {
    this.graph = graph;
  }
  
  /**
   * Generate visualization data
   */
  async generateVisualization(): Promise<VisualizationData> {
    console.log('📊 Generating DAG visualization...');
    
    const nodes = Array.from(this.graph.getNodesByType('file'));
    const edges = this.generateEdgeData(nodes);
    const nodeData = this.generateNodeData(nodes);
    
    const layers = this.calculateLayers(nodes);
    
    const visualizationData: VisualizationData = {
      nodes: nodeData,
      edges,
      metadata: {
        totalNodes: nodes.length,
        totalEdges: edges.length,
        layers
      }
    };
    
    console.log('✅ Visualization data generated');
    return visualizationData;
  }
  
  /**
   * Generate node data for visualization
   */
  private generateNodeData(nodes: DAGNode[]): Array<{
    id: string;
    type: string;
    status: string;
    x: number;
    y: number;
  }> {
    const layers = this.calculateLayers(nodes);
    const nodesByLayer: Map<number, DAGNode[]> = new Map();
    
    // Group nodes by layer
    for (const node of nodes) {
      const layer = this.calculateLayer(node);
      if (!nodesByLayer.has(layer)) {
        nodesByLayer.set(layer, []);
      }
      nodesByLayer.get(layer)!.push(node);
    }
    
    // Generate positions
    const nodeData = [];
    let xOffset = 0;
    
    for (let layer = 0; layer <= layers; layer++) {
      const layerNodes = nodesByLayer.get(layer) || [];
      const layerHeight = 500 / (layerNodes.length + 1);
      
      for (let i = 0; i < layerNodes.length; i++) {
        const node = layerNodes[i];
        nodeData.push({
          id: node.id,
          type: node.type,
          status: node.status,
          x: xOffset,
          y: (i + 1) * layerHeight
        });
      }
      
      xOffset += 200;
    }
    
    return nodeData;
  }
  
  /**
   * Generate edge data for visualization
   */
  private generateEdgeData(nodes: DAGNode[]): Array<{
    source: string;
    target: string;
    type: string;
  }> {
    const edges = [];
    
    for (const node of nodes) {
      for (const depId of node.dependencies) {
        edges.push({
          source: depId,
          target: node.id,
          type: 'dependency'
        });
      }
    }
    
    return edges;
  }
  
  /**
   * Calculate layer for a node
   */
  private calculateLayer(node: DAGNode): number {
    if (node.dependencies.length === 0) return 0;
    
    let maxLayer = 0;
    for (const depId of node.dependencies) {
      const depNode = this.graph.getNode(depId);
      if (depNode) {
        const layer = this.calculateLayer(depNode);
        maxLayer = Math.max(maxLayer, layer);
      }
    }
    
    return maxLayer + 1;
  }
  
  /**
   * Calculate total number of layers
   */
  private calculateLayers(nodes: DAGNode[]): number {
    let maxLayer = 0;
    for (const node of nodes) {
      const layer = this.calculateLayer(node);
      maxLayer = Math.max(maxLayer, layer);
    }
    return maxLayer;
  }
  
  /**
   * Generate statistics report
   */
  generateStatisticsReport(): string {
    const stats = this.graph.getStatistics();
    
    return `
# Global DAG Statistics Report

## Overview
- Total Nodes: ${stats.totalNodes}
- Total Edges: ${stats.totalEdges}
- Average Compliance: ${stats.avgCompliance.toFixed(2)}%
- Completed: ${stats.completedNodes}
- Failed: ${stats.failedNodes}
- Currently Executing: ${stats.currentlyExecuting}

## Nodes by Type
${Object.entries(stats.nodesByType)
  .map(([type, count]) => `- ${type}: ${count}`)
  .join('\n')}

## Nodes by Organization
${Object.entries(stats.nodesByOrg)
  .map(([org, count]) => `- ${org}: ${count}`)
  .join('\n')}

## Execution Status
- Success Rate: ${stats.totalNodes > 0 
  ? ((stats.completedNodes / stats.totalNodes) * 100).toFixed(2) 
  : 0}%
`;
  }
}