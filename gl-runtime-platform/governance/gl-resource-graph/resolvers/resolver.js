"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ResourceGraphResolver = void 0;
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
resource - graph - resolver;
#;
-charter - version;
2.0;
.0;
const logger_1 = require("../../src/utils/logger");
const logger = (0, logger_1.createLogger)('ResourceGraphResolver');
class ResourceGraphResolver {
    constructor(graphData, indexEntries) {
        this.graphData = graphData;
        this.indexEntries = indexEntries;
    }
    resolveFile(path) {
        const node = this.graphData.nodes.find(n => n.path === path);
        if (!node) {
            logger.warn(`File not found in graph: ${path}`);
        }
        return node || null;
    }
    resolvePath(pattern) {
        const regex = new RegExp(pattern.replace('*', '.*'));
        const matchingNodes = this.graphData.nodes.filter(n => regex.test(n.path));
        return {
            found: matchingNodes.length > 0,
            nodes: matchingNodes.length > 0 ? matchingNodes : undefined,
            paths: matchingNodes.map(n => n.path)
        };
    }
    resolveDependency(fromPath, toPath) {
        const fromNode = this.resolveFile(fromPath);
        const toNode = this.resolveFile(toPath);
        if (!fromNode || !toNode) {
            return false;
        }
        const edge = this.graphData.edges.find(e => e.source === fromNode.id && e.target === toNode.id);
        return !!edge;
    }
    resolveMissingDependencies() {
        const missing = [];
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
    resolveMissingFiles(expectedPaths) {
        const missing = [];
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
    resolveOrphanNodes() {
        const nodesWithEdges = new Set();
        this.graphData.edges.forEach(edge => {
            nodesWithEdges.add(edge.source);
            nodesWithEdges.add(edge.target);
        });
        const orphans = this.graphData.nodes.filter(n => !nodesWithEdges.has(n.id));
        return orphans;
    }
    resolveCyclicDependencies() {
        const visited = new Set();
        const recursionStack = new Set();
        const cycles = [];
        const path = [];
        const dfs = (nodeId) => {
            visited.add(nodeId);
            recursionStack.add(nodeId);
            path.push(nodeId);
            const edges = this.graphData.edges.filter(e => e.source === nodeId);
            for (const edge of edges) {
                if (!visited.has(edge.target)) {
                    dfs(edge.target);
                }
                else if (recursionStack.has(edge.target)) {
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
    resolveGovernanceCompliance() {
        const nonCompliant = [];
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
    resolveBySemanticAnchor(semanticAnchor) {
        return this.graphData.nodes.filter(n => n.semanticAnchor === semanticAnchor);
    }
    resolveByType(type) {
        return this.graphData.nodes.filter(n => n.type === type);
    }
    resolveByLanguage(language) {
        return this.graphData.nodes.filter(n => n.language === language);
    }
    exportResolutions() {
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
exports.ResourceGraphResolver = ResourceGraphResolver;
//# sourceMappingURL=resolver.js.map