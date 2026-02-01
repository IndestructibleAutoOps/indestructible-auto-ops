// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-graph-management
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

import { IndexEntry } from '../indexers/indexer';
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
export declare class ResourceGraphModel {
    private graphData;
    buildGraph(indexEntries: Map<string, IndexEntry>): void;
    private generateNodeId;
    getNodes(): GraphNode[];
    getEdges(): GraphEdge[];
    getNodeById(id: string): GraphNode | undefined;
    getNodeByPath(path: string): GraphNode | undefined;
    getDependencies(nodeId: string): GraphNode[];
    getDependents(nodeId: string): GraphNode[];
    getNodesByType(type: string): GraphNode[];
    getNodesByLanguage(language: string): GraphNode[];
    getNodesBySemanticAnchor(semanticAnchor: string): GraphNode[];
    exportGraph(): GraphData;
    importGraph(graphData: GraphData): void;
    getStatistics(): {
        nodeCount: number;
        edgeCount: number;
        avgDegree: number;
    };
}
//# sourceMappingURL=graph-model.d.ts.map