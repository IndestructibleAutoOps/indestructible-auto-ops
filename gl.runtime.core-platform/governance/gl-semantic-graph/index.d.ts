// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-indexing
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

import { ParsedContent } from './content-parsers';
import { SemanticClassification } from './semantic-classifiers';
import { GLMapping } from './gl-mapping';
import { SchemaInference } from './schema-infer';
import { IntentResolution } from './intent-resolver';
export interface SemanticAnalysis {
    filePath: string;
    parsedContent: ParsedContent;
    classification: SemanticClassification;
    mapping: GLMapping;
    schemaInference: SchemaInference;
    intentResolution: IntentResolution;
    analysisTimestamp: string;
    overallCompliance: boolean;
    issues: string[];
    recommendations: string[];
}
export declare class SemanticGraphOrchestrator {
    private contentParser;
    private semanticClassifier;
    private glMapper;
    private schemaInferencer;
    private intentResolver;
    constructor();
    analyzeFile(filePath: string): Promise<SemanticAnalysis>;
    analyzeDirectory(directoryPath: string, recursive?: boolean): Promise<SemanticAnalysis[]>;
    private scanDirectory;
    private checkOverallCompliance;
    private compileIssues;
    private compileRecommendations;
    generateAutoRepairPatch(analysis: SemanticAnalysis): Promise<{
        patch: string;
        filePath: string;
    }>;
    applyAutoRepairPatch(analysis: SemanticAnalysis): Promise<boolean>;
}
//# sourceMappingURL=index.d.ts.map