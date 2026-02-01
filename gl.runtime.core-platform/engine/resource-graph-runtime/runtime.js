"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ResourceGraphRuntime = void 0;
// @GL-governed
// @GL-layer: GL70-89
// @GL-semantic: engine-graph-management
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

#;
-layer;
GL90 - 99;
#;
-semantic;
resource - graph - runtime;
#;
-charter - version;
2.0;
.0;
const resource_graph_manager_1 = require("../../governance/gl-resource-graph/resource-graph-manager");
const event_stream_manager_1 = require("../src/events/event-stream-manager");
const logger_1 = require("../src/utils/logger");
const logger = (0, logger_1.createLogger)('ResourceGraphRuntime');
class ResourceGraphRuntime {
    constructor(config) {
        this.currentGraph = null;
        this.resourceGraphManager = new resource_graph_manager_1.ResourceGraphManager();
        this.eventStream = new event_stream_manager_1.EventStreamManager();
        this.config = {
            autoRefresh: config?.autoRefresh ?? true,
            refreshIntervalMs: config?.refreshIntervalMs ?? 300000, // 5 minutes
            requireGraphForOperations: config?.requireGraphForOperations ?? true
        };
        if (this.config.autoRefresh) {
            this.startAutoRefresh();
        }
    }
    async initialize(rootPath) {
        logger.info(`Initializing Resource Graph Runtime for: ${rootPath}`);
        await this.eventStream.logEvent({
            eventType: 'runtime_init_started',
            layer: 'GL90-99',
            semanticAnchor: 'GL-ROOT-GOVERNANCE',
            timestamp: new Date().toISOString(),
            metadata: {
                rootPath,
                autoRefresh: this.config.autoRefresh
            }
        });
        // Build or load Global Resource Graph
        const isFresh = await this.resourceGraphManager.checkGraphFreshness(rootPath);
        if (isFresh) {
            // Load existing graph
            // In production, would load from artifact store
            logger.info('Loading existing Global Resource Graph');
        }
        else {
            // Build new graph
            logger.info('Building new Global Resource Graph');
            this.currentGraph = await this.resourceGraphManager.buildGlobalResourceGraph(rootPath);
        }
        await this.eventStream.logEvent({
            eventType: 'runtime_init_completed',
            layer: 'GL90-99',
            semanticAnchor: 'GL-ROOT-GOVERNANCE',
            timestamp: new Date().toISOString(),
            metadata: {
                nodeCount: this.currentGraph?.nodes.length || 0,
                edgeCount: this.currentGraph?.edges.length || 0
            }
        });
        logger.info('Resource Graph Runtime initialized successfully');
    }
    async ensureGraphReady(rootPath) {
        if (!this.currentGraph) {
            await this.initialize(rootPath);
        }
        else {
            const isFresh = await this.resourceGraphManager.checkGraphFreshness(rootPath);
            if (!isFresh) {
                logger.info('Refreshing Global Resource Graph');
                this.currentGraph = await this.resourceGraphManager.buildGlobalResourceGraph(rootPath);
            }
        }
    }
    getCurrentGraph() {
        return this.currentGraph;
    }
    async resolveFile(path) {
        if (this.config.requireGraphForOperations) {
            await this.ensureGraphReady('.');
        }
        const resolver = this.resourceGraphManager.getResolver();
        return resolver.resolveFile(path);
    }
    async resolveDependencies(path) {
        if (this.config.requireGraphForOperations) {
            await this.ensureGraphReady('.');
        }
        const resolver = this.resourceGraphManager.getResolver();
        const node = resolver.resolveFile(path);
        if (node) {
            return resolver.getDependencies(node.id);
        }
        return [];
    }
    async resolveMissingDependencies() {
        if (this.config.requireGraphForOperations) {
            await this.ensureGraphReady('.');
        }
        const resolver = this.resourceGraphManager.getResolver();
        const result = resolver.resolveMissingDependencies();
        return result.missing || [];
    }
    async resolveGovernanceCompliance() {
        if (this.config.requireGraphForOperations) {
            await this.ensureGraphReady('.');
        }
        const resolver = this.resourceGraphManager.getResolver();
        const result = resolver.resolveGovernanceCompliance();
        return result.missing || [];
    }
    async getCyclicDependencies() {
        if (this.config.requireGraphForOperations) {
            await this.ensureGraphReady('.');
        }
        const resolver = this.resourceGraphManager.getResolver();
        return resolver.resolveCyclicDependencies();
    }
    startAutoRefresh() {
        setInterval(async () => {
            try {
                logger.info('Auto-refreshing Global Resource Graph');
                this.currentGraph = await this.resourceGraphManager.buildGlobalResourceGraph('.');
                await this.eventStream.logEvent({
                    eventType: 'grg_auto_refreshed',
                    layer: 'GL90-99',
                    semanticAnchor: 'GL-ROOT-GOVERNANCE',
                    timestamp: new Date().toISOString(),
                    metadata: {
                        nodeCount: this.currentGraph?.nodes.length || 0,
                        edgeCount: this.currentGraph?.edges.length || 0
                    }
                });
            }
            catch (error) {
                logger.error(`Auto-refresh failed: ${error.message}`);
            }
        }, this.config.refreshIntervalMs);
    }
    async shutdown() {
        logger.info('Shutting down Resource Graph Runtime');
        // In production, would clean up resources
    }
}
exports.ResourceGraphRuntime = ResourceGraphRuntime;
//# sourceMappingURL=runtime.js.map