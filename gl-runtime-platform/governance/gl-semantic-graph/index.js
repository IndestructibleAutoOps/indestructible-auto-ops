"use strict";
// @GL-governed
// @GL-layer: governance
// @GL-semantic: semantic-graph-orchestrator
// @GL-charter-version: 2.0.0
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.SemanticGraphOrchestrator = void 0;
const content_parsers_1 = require("./content-parsers");
const semantic_classifiers_1 = require("./semantic-classifiers");
const gl_mapping_1 = require("./gl-mapping");
const schema_infer_1 = require("./schema-infer");
const intent_resolver_1 = require("./intent-resolver");
const promises_1 = __importDefault(require("fs/promises"));
const path_1 = __importDefault(require("path"));
class SemanticGraphOrchestrator {
    constructor() {
        this.contentParser = new content_parsers_1.ContentParser();
        this.semanticClassifier = new semantic_classifiers_1.SemanticClassifier();
        this.glMapper = new gl_mapping_1.GLMapper();
        this.schemaInferencer = new schema_infer_1.SchemaInferencer();
        this.intentResolver = new intent_resolver_1.IntentResolver();
    }
    async analyzeFile(filePath) {
        const fileContent = await promises_1.default.readFile(filePath, 'utf-8');
        // Step 1: Parse content
        const parsedContent = await this.contentParser.parse(filePath);
        // Step 2: Classify semantics
        const classification = this.semanticClassifier.classify(filePath, parsedContent);
        // Step 3: Map to GL standards
        const mapping = this.glMapper.map(filePath, classification, fileContent);
        // Step 4: Infer schema
        const schemaInference = this.schemaInferencer.infer(filePath, parsedContent, classification);
        // Step 5: Resolve intent
        const intentResolution = this.intentResolver.resolve(filePath, parsedContent, classification, mapping);
        // Step 6: Compile overall analysis
        const overallCompliance = this.checkOverallCompliance(classification, mapping, schemaInference);
        const issues = this.compileIssues(classification, mapping, schemaInference);
        const recommendations = this.compileRecommendations(mapping, intentResolution);
        return {
            filePath,
            parsedContent,
            classification,
            mapping,
            schemaInference,
            intentResolution,
            analysisTimestamp: new Date().toISOString(),
            overallCompliance,
            issues,
            recommendations
        };
    }
    async analyzeDirectory(directoryPath, recursive = true) {
        const analyses = [];
        const files = await this.scanDirectory(directoryPath, recursive);
        for (const file of files) {
            try {
                const analysis = await this.analyzeFile(file);
                analyses.push(analysis);
            }
            catch (error) {
                console.error(`Error analyzing file ${file}:`, error);
            }
        }
        return analyses;
    }
    async scanDirectory(directoryPath, recursive) {
        const files = [];
        const entries = await promises_1.default.readdir(directoryPath, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path_1.default.join(directoryPath, entry.name);
            if (entry.isDirectory() && recursive) {
                // Skip node_modules and other common exclusions
                if (!entry.name.startsWith('.') && entry.name !== 'node_modules' && entry.name !== 'dist') {
                    const subFiles = await this.scanDirectory(fullPath, recursive);
                    files.push(...subFiles);
                }
            }
            else if (entry.isFile()) {
                // Include relevant file types
                const ext = path_1.default.extname(entry.name).toLowerCase();
                if (['.ts', '.js', '.py', '.yaml', '.yml', '.json', '.md'].includes(ext)) {
                    files.push(fullPath);
                }
            }
        }
        return files;
    }
    checkOverallCompliance(classification, mapping, schemaInference) {
        return mapping.governanceCompliant &&
            classification.governanceCompliance.hasGovernedTag &&
            classification.governanceCompliance.hasSemanticAnchor &&
            classification.governanceCompliance.hasGLLayer &&
            classification.governanceCompliance.hasCharterVersion &&
            mapping.issues.length === 0;
    }
    compileIssues(classification, mapping, schemaInference) {
        const issues = [];
        issues.push(...mapping.issues);
        if (schemaInference.missingMetadata.length > 0) {
            issues.push(`Missing metadata: ${schemaInference.missingMetadata.join(', ')}`);
        }
        return issues;
    }
    compileRecommendations(mapping, intentResolution) {
        const recommendations = [];
        recommendations.push(...intentResolution.recommendations);
        if (mapping.missingTags.length > 0) {
            recommendations.push(`Add missing tags: ${mapping.missingTags.join(', ')}`);
        }
        return recommendations;
    }
    async generateAutoRepairPatch(analysis) {
        const { filePath, mapping } = analysis;
        if (!mapping.governanceCompliant) {
            const fileContent = await promises_1.default.readFile(filePath, 'utf-8');
            const patchedContent = this.glMapper.applyGovernanceTags(fileContent, mapping);
            return {
                filePath,
                patch: patchedContent
            };
        }
        return {
            filePath,
            patch: ''
        };
    }
    async applyAutoRepairPatch(analysis) {
        const { patch, filePath } = await this.generateAutoRepairPatch(analysis);
        if (patch) {
            await promises_1.default.writeFile(filePath, patch, 'utf-8');
            return true;
        }
        return false;
    }
}
exports.SemanticGraphOrchestrator = SemanticGraphOrchestrator;
//# sourceMappingURL=index.js.map