"use strict";
// @GL-governed
// @GL-layer: engine
// @GL-semantic: semantic-graph-runtime
// @GL-charter-version: 2.0.0
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.SemanticGraphRuntime = void 0;
const gl_semantic_graph_1 = require("../../governance/gl-semantic-graph");
const promises_1 = __importDefault(require("fs/promises"));
const path_1 = __importDefault(require("path"));
class SemanticGraphRuntime {
    constructor(config = {}) {
        this.orchestrator = new gl_semantic_graph_1.SemanticGraphOrchestrator();
        this.config = {
            autoRefreshInterval: config.autoRefreshInterval || 300, // 5 minutes
            storagePath: config.storagePath || 'storage/gl-semantic-graph/',
            enabled: config.enabled !== false
        };
        this.analyses = new Map();
        this.storagePath = path_1.default.join(process.cwd(), this.config.storagePath);
        this.status = {
            ready: false,
            lastUpdated: '',
            totalFilesAnalyzed: 0,
            compliantFiles: 0,
            nonCompliantFiles: 0,
            autoRepairCandidateFiles: 0
        };
    }
    async initialize(repositoryPath) {
        if (!this.config.enabled) {
            console.log('Semantic Graph Runtime disabled');
            return;
        }
        console.log('Initializing Semantic Graph Runtime...');
        // Ensure storage directory exists
        await promises_1.default.mkdir(this.storagePath, { recursive: true });
        // Build initial semantic graph
        await this.buildSemanticGraph(repositoryPath);
        // Start auto-refresh
        this.startAutoRefresh(repositoryPath);
        this.status.ready = true;
        console.log('Semantic Graph Runtime initialized successfully');
    }
    async buildSemanticGraph(repositoryPath) {
        console.log('Building Semantic Resource Graph...');
        const startTime = Date.now();
        const analyses = await this.orchestrator.analyzeDirectory(repositoryPath, true);
        // Store analyses
        this.analyses.clear();
        for (const analysis of analyses) {
            this.analyses.set(analysis.filePath, analysis);
        }
        // Update status
        this.status.totalFilesAnalyzed = analyses.length;
        this.status.compliantFiles = analyses.filter(a => a.overallCompliance).length;
        this.status.nonCompliantFiles = analyses.filter(a => !a.overallCompliance).length;
        this.status.autoRepairCandidateFiles = analyses.filter(a => a.intentResolution.autoRepairCandidate).length;
        this.status.lastUpdated = new Date().toISOString();
        // Persist analyses
        await this.persistAnalyses();
        const duration = Date.now() - startTime;
        console.log(`Semantic Resource Graph built in ${duration}ms`);
        console.log(`- Total files analyzed: ${this.status.totalFilesAnalyzed}`);
        console.log(`- Compliant files: ${this.status.compliantFiles}`);
        console.log(`- Non-compliant files: ${this.status.nonCompliantFiles}`);
        console.log(`- Auto-repair candidates: ${this.status.autoRepairCandidateFiles}`);
    }
    async getFileAnalysis(filePath) {
        return this.analyses.get(filePath) || null;
    }
    async searchBySemanticAnchor(semanticAnchor) {
        const results = [];
        for (const analysis of this.analyses.values()) {
            if (analysis.mapping.glSemanticAnchor === semanticAnchor) {
                results.push(analysis);
            }
        }
        return results;
    }
    async searchByGLLayer(glLayer) {
        const results = [];
        for (const analysis of this.analyses.values()) {
            if (analysis.mapping.glLayer === glLayer) {
                results.push(analysis);
            }
        }
        return results;
    }
    async searchByRole(role) {
        const results = [];
        for (const analysis of this.analyses.values()) {
            if (analysis.classification.role === role) {
                results.push(analysis);
            }
        }
        return results;
    }
    async getNonCompliantFiles() {
        const results = [];
        for (const analysis of this.analyses.values()) {
            if (!analysis.overallCompliance) {
                results.push(analysis);
            }
        }
        return results;
    }
    async getAutoRepairCandidates() {
        const results = [];
        for (const analysis of this.analyses.values()) {
            if (analysis.intentResolution.autoRepairCandidate) {
                results.push(analysis);
            }
        }
        return results;
    }
    async applyAutoRepair() {
        const candidates = await this.getAutoRepairCandidates();
        let applied = 0;
        let failed = 0;
        for (const analysis of candidates) {
            try {
                const success = await this.orchestrator.applyAutoRepairPatch(analysis);
                if (success) {
                    applied++;
                    console.log(`Auto-repair applied to: ${analysis.filePath}`);
                }
            }
            catch (error) {
                failed++;
                console.error(`Auto-repair failed for ${analysis.filePath}:`, error);
            }
        }
        // Refresh graph after repairs
        if (applied > 0) {
            await this.refreshGraph();
        }
        return { applied, failed };
    }
    async refreshGraph() {
        console.log('Refreshing Semantic Resource Graph...');
        const repositoryPath = process.cwd();
        await this.buildSemanticGraph(repositoryPath);
    }
    getStatus() {
        return { ...this.status };
    }
    async persistAnalyses() {
        const analysesPath = path_1.default.join(this.storagePath, 'analyses.json');
        const data = Array.from(this.analyses.entries());
        await promises_1.default.writeFile(analysesPath, JSON.stringify(data, null, 2), 'utf-8');
    }
    startAutoRefresh(repositoryPath) {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        this.refreshTimer = setInterval(async () => {
            await this.refreshGraph();
        }, this.config.autoRefreshInterval * 1000);
    }
    async shutdown() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        this.status.ready = false;
        console.log('Semantic Graph Runtime shutdown');
    }
}
exports.SemanticGraphRuntime = SemanticGraphRuntime;
//# sourceMappingURL=runtime.js.map