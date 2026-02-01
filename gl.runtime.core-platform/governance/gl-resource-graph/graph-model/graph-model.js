"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ResourceGraphModel = void 0;
// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-graph-management
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

#;
-layer;
GL90 - 99;
#;
-semantic;
resource - graph - model;
#;
-charter - version;
2.0;
.0;
const logger_1 = require("../../src/utils/logger");
const logger = (0, logger_1.createLogger)('ResourceGraphModel');
class ResourceGraphModel {
    constructor() {
        this.graphData = {
            nodes: [],
            edges: []
        };
    }
    buildGraph(indexEntries) {
        logger.info(`Building graph with ${indexEntries.size} entries`);
        // Build nodes
        for (const [path, entry] of indexEntries.entries()) {
            const node = {
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
                    const edge = {
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
    generateNodeId(path) {
        // Generate a unique ID from path
        return path.replace(/[^a-zA-Z0-9]/g, '_');
    }
    getNodes() {
        return this.graphData.nodes;
    }
    getEdges() {
        return this.graphData.edges;
    }
    getNodeById(id) {
        return this.graphData.nodes.find(n => n.id === id);
    }
    getNodeByPath(path) {
        return this.graphData.nodes.find(n => n.path === path);
    }
    getDependencies(nodeId) {
        const edges = this.graphData.edges.filter(e => e.source === nodeId);
        return edges.map(e => this.getNodeById(e.target)).filter(Boolean);
    }
    getDependents(nodeId) {
        const edges = this.graphData.edges.filter(e => e.target === nodeId);
        return edges.map(e => this.getNodeById(e.source)).filter(Boolean);
    }
    getNodesByType(type) {
        return this.graphData.nodes.filter(n => n.type === type);
    }
    getNodesByLanguage(language) {
        return this.graphData.nodes.filter(n => n.language === language);
    }
    getNodesBySemanticAnchor(semanticAnchor) {
        return this.graphData.nodes.filter(n => n.semanticAnchor === semanticAnchor);
    }
    exportGraph() {
        return {
            nodes: [...this.graphData.nodes],
            edges: [...this.graphData.edges]
        };
    }
    importGraph(graphData) {
        this.graphData = {
            nodes: [...graphData.nodes],
            edges: [...graphData.edges]
        };
        logger.info(`Graph imported: ${this.graphData.nodes.length} nodes, ${this.graphData.edges.length} edges`);
    }
    getStatistics() {
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
exports.ResourceGraphModel = ResourceGraphModel;
//# sourceMappingURL=graph-model.js.map