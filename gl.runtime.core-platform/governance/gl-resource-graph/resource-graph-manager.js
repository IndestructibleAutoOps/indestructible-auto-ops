"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ResourceGraphManager = void 0;
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
resource - graph - manager;
#;
-charter - version;
2.0;
.0;
const scanner_1 = require("./scanners/scanner");
const indexer_1 = require("./indexers/indexer");
const graph_model_1 = require("./graph-model/graph-model");
const resolver_1 = require("./resolvers/resolver");
const event_stream_manager_1 = require("../src/events/event-stream-manager");
const artifact_store_1 = require("../src/storage/artifact-store");
const logger_1 = require("../src/utils/logger");
const logger = (0, logger_1.createLogger)('ResourceGraphManager');
class ResourceGraphManager {
    constructor() {
        this.scanner = new scanner_1.ResourceGraphScanner();
        this.indexer = new indexer_1.ResourceGraphIndexer();
        this.graphModel = new graph_model_1.ResourceGraphModel();
        this.eventStream = new event_stream_manager_1.EventStreamManager();
        this.artifactStore = new artifact_store_1.ArtifactStore();
        // Initialize resolver after graph is built
        this.resolver = new resolver_1.ResourceGraphResolver({ nodes: [], edges: [] }, new Map());
    }
    async buildGlobalResourceGraph(rootPath) {
        logger.info(`Building Global Resource Graph for: ${rootPath}`);
        // Log governance event
        await this.eventStream.logEvent({
            eventType: 'grg_build_started',
            layer: 'GL90-99',
            semanticAnchor: 'GL-ROOT-GOVERNANCE',
            timestamp: new Date().toISOString(),
            metadata: {
                rootPath,
                version: '6.0.0'
            }
        });
        // Step 1: Scan repository
        const scanResults = await this.scanner.scanRepository(rootPath);
        logger.info(`Scanned ${scanResults.length} files`);
        // Step 2: Build index
        this.indexer.buildIndex(scanResults);
        logger.info(`Index built: ${this.indexer.getIndexSize()} entries`);
        // Step 3: Build graph model
        this.graphModel.buildGraph(this.indexer['pathIndex']);
        logger.info(`Graph built: ${this.graphModel.getStatistics().nodeCount} nodes`);
        // Step 4: Initialize resolver
        this.resolver = new resolver_1.ResourceGraphResolver(this.graphModel.exportGraph(), this.indexer['pathIndex']);
        // Step 5: Run resolutions
        const resolutions = this.resolver.exportResolutions();
        logger.info(`Resolutions: ${JSON.stringify(resolutions)}`);
        // Step 6: Build Global Resource Graph artifact
        const grg = {
            version: '6.0.0',
            timestamp: new Date().toISOString(),
            nodes: this.graphModel.getNodes(),
            edges: this.graphModel.getEdges(),
            statistics: this.graphModel.getStatistics(),
            resolutions: resolutions
        };
        // Step 7: Store artifact
        await this.artifactStore.storeArtifact({
            id: `global-resource-graph-${Date.now()}`,
            type: 'metadata',
            name: 'global-resource-graph',
            content: grg,
            timestamp: new Date().toISOString(),
            metadata: {
                version: '6.0.0',
                rootPath,
                charterVersion: '2.0.0'
            }
        });
        // Log governance event
        await this.eventStream.logEvent({
            eventType: 'grg_build_completed',
            layer: 'GL90-99',
            semanticAnchor: 'GL-ROOT-GOVERNANCE',
            timestamp: new Date().toISOString(),
            metadata: {
                version: '6.0.0',
                nodeCount: grg.nodes.length,
                edgeCount: grg.edges.length,
                missingDependencies: resolutions.missingDependencies.length,
                nonCompliantFiles: resolutions.nonCompliantFiles.length
            }
        });
        logger.info(`Global Resource Graph built successfully`);
        return grg;
    }
    getScanner() {
        return this.scanner;
    }
    getIndexer() {
        return this.indexer;
    }
    getGraphModel() {
        return this.graphModel;
    }
    getResolver() {
        return this.resolver;
    }
    async loadGlobalResourceGraph(artifactId) {
        const artifact = await this.artifactStore.loadArtifact(artifactId);
        if (artifact && artifact.type === 'metadata') {
            const grg = artifact.content;
            // Rebuild graph model from loaded data
            this.graphModel.importGraph({
                nodes: grg.nodes,
                edges: grg.edges
            });
            // Update resolver
            this.resolver = new resolver_1.ResourceGraphResolver(this.graphModel.exportGraph(), new Map());
            logger.info(`Global Resource Graph loaded: ${grg.nodes.length} nodes`);
            return grg;
        }
        return null;
    }
    async checkGraphFreshness(rootPath) {
        // Check if the graph is up to date
        // In production, would compare file timestamps
        const lastModified = new Date();
        // Simplified check - always return false for now
        return false;
    }
}
exports.ResourceGraphManager = ResourceGraphManager;
//# sourceMappingURL=resource-graph-manager.js.map