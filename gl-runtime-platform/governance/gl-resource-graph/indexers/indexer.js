"use strict";
// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: resource-graph-indexer
// @GL-charter-version: 2.0.0
Object.defineProperty(exports, "__esModule", { value: true });
exports.ResourceGraphIndexer = void 0;
const logger_1 = require("../../src/utils/logger");
const logger = (0, logger_1.createLogger)('ResourceGraphIndexer');
class ResourceGraphIndexer {
    constructor() {
        this.pathIndex = new Map();
        this.typeIndex = new Map();
        this.languageIndex = new Map();
        this.semanticIndex = new Map();
    }
    buildIndex(scanResults) {
        logger.info(`Building index for ${scanResults.length} files`);
        for (const result of scanResults) {
            const entry = {
                path: result.path,
                type: result.type,
                language: result.language,
                dependencies: [],
                dependents: []
            };
            this.pathIndex.set(result.path, entry);
            // Build type index
            if (!this.typeIndex.has(result.type)) {
                this.typeIndex.set(result.type, new Set());
            }
            this.typeIndex.get(result.type).add(result.path);
            // Build language index
            if (!this.languageIndex.has(result.language)) {
                this.languageIndex.set(result.language, new Set());
            }
            this.languageIndex.get(result.language).add(result.path);
        }
        // Extract semantic anchors and metadata
        this.extractMetadata(scanResults);
        // Build dependency graph
        this.buildDependencyGraph(scanResults);
        logger.info(`Index built: ${this.pathIndex.size} entries`);
    }
    extractMetadata(scanResults) {
        for (const result of scanResults) {
            if (!result.hasSemanticAnchor)
                continue;
            // Extract semantic anchor (simplified)
            const semanticAnchor = this.extractSemanticAnchor(result.path);
            if (semanticAnchor) {
                const entry = this.pathIndex.get(result.path);
                if (entry) {
                    entry.semanticAnchor = semanticAnchor;
                    if (!this.semanticIndex.has(semanticAnchor)) {
                        this.semanticIndex.set(semanticAnchor, new Set());
                    }
                    this.semanticIndex.get(semanticAnchor).add(result.path);
                }
            }
        }
    }
    extractSemanticAnchor(filePath) {
        // Simplified semantic anchor extraction
        // In production, would parse file headers
        const parts = filePath.split('/');
        if (parts.includes('gl-runtime-platform')) {
            return 'GL-ROOT-GOVERNANCE';
        }
        return null;
    }
    buildDependencyGraph(scanResults) {
        // Simplified dependency detection
        // In production, would parse import statements, requires, etc.
        for (const result of scanResults) {
            const entry = this.pathIndex.get(result.path);
            if (!entry)
                continue;
            // Detect TypeScript/JavaScript imports
            if (result.language === 'typescript' || result.language === 'javascript') {
                const imports = this.detectImports(result.path);
                entry.dependencies = imports;
            }
            // Detect Python imports
            if (result.language === 'python') {
                const imports = this.detectPythonImports(result.path);
                entry.dependencies = imports;
            }
        }
        // Build reverse dependencies (dependents)
        for (const entry of this.pathIndex.values()) {
            for (const dep of entry.dependencies) {
                const depEntry = this.pathIndex.get(dep);
                if (depEntry) {
                    depEntry.dependents.push(entry.path);
                }
            }
        }
    }
    detectImports(filePath) {
        // Simplified import detection
        // In production, would use AST parsing
        const imports = [];
        const dir = filePath.substring(0, filePath.lastIndexOf('/'));
        // Common import patterns (would be more sophisticated)
        if (filePath.includes('/src/')) {
            imports.push(dir);
        }
        return imports;
    }
    detectPythonImports(filePath) {
        // Simplified Python import detection
        const imports = [];
        const dir = filePath.substring(0, filePath.lastIndexOf('/'));
        if (filePath.includes('/src/')) {
            imports.push(dir);
        }
        return imports;
    }
    getByPath(path) {
        return this.pathIndex.get(path);
    }
    getByType(type) {
        const paths = this.typeIndex.get(type) || [];
        return Array.from(paths).map(p => this.pathIndex.get(p)).filter(Boolean);
    }
    getByLanguage(language) {
        const paths = this.languageIndex.get(language) || [];
        return Array.from(paths).map(p => this.pathIndex.get(p)).filter(Boolean);
    }
    getBySemanticAnchor(semanticAnchor) {
        const paths = this.semanticIndex.get(semanticAnchor) || [];
        return Array.from(paths).map(p => this.pathIndex.get(p)).filter(Boolean);
    }
    getAllDependencies(path) {
        const entry = this.pathIndex.get(path);
        return entry?.dependencies || [];
    }
    getAllDependents(path) {
        const entry = this.pathIndex.get(path);
        return entry?.dependents || [];
    }
    getIndexSize() {
        return this.pathIndex.size;
    }
}
exports.ResourceGraphIndexer = ResourceGraphIndexer;
//# sourceMappingURL=indexer.js.map