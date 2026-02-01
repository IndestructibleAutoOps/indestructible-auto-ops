// @GL-governed
// @GL-layer: GL70-89
// @GL-semantic: engine-graph-management
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

import { SemanticAnalysis } from '../../governance/gl-semantic-graph';
export interface SRGRuntimeConfig {
    autoRefreshInterval: number;
    storagePath: string;
    enabled: boolean;
}
export interface SRGStatus {
    ready: boolean;
    lastUpdated: string;
    totalFilesAnalyzed: number;
    compliantFiles: number;
    nonCompliantFiles: number;
    autoRepairCandidateFiles: number;
}
export declare class SemanticGraphRuntime {
    private orchestrator;
    private config;
    private analyses;
    private status;
    private refreshTimer?;
    private storagePath;
    constructor(config?: Partial<SRGRuntimeConfig>);
    initialize(repositoryPath: string): Promise<void>;
    buildSemanticGraph(repositoryPath: string): Promise<void>;
    getFileAnalysis(filePath: string): Promise<SemanticAnalysis | null>;
    searchBySemanticAnchor(semanticAnchor: string): Promise<SemanticAnalysis[]>;
    searchByGLLayer(glLayer: string): Promise<SemanticAnalysis[]>;
    searchByRole(role: string): Promise<SemanticAnalysis[]>;
    getNonCompliantFiles(): Promise<SemanticAnalysis[]>;
    getAutoRepairCandidates(): Promise<SemanticAnalysis[]>;
    applyAutoRepair(): Promise<{
        applied: number;
        failed: number;
    }>;
    refreshGraph(): Promise<void>;
    getStatus(): SRGStatus;
    private persistAnalyses;
    private startAutoRefresh;
    shutdown(): Promise<void>;
}
//# sourceMappingURL=runtime.d.ts.map