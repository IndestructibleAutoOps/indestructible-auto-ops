// @GL-governed
// @GL-layer: GL70-89
// @GL-semantic: engine-graph-management
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

import { GlobalResourceGraph } from '../../governance/gl-resource-graph/resource-graph-manager';
export interface RuntimeConfig {
    autoRefresh: boolean;
    refreshIntervalMs: number;
    requireGraphForOperations: boolean;
}
export declare class ResourceGraphRuntime {
    private resourceGraphManager;
    private eventStream;
    private currentGraph;
    private config;
    constructor(config?: Partial<RuntimeConfig>);
    initialize(rootPath: string): Promise<void>;
    ensureGraphReady(rootPath: string): Promise<void>;
    getCurrentGraph(): GlobalResourceGraph | null;
    resolveFile(path: string): Promise<any>;
    resolveDependencies(path: string): Promise<any[]>;
    resolveMissingDependencies(): Promise<string[]>;
    resolveGovernanceCompliance(): Promise<string[]>;
    getCyclicDependencies(): Promise<string[][]>;
    private startAutoRefresh;
    shutdown(): Promise<void>;
}
//# sourceMappingURL=runtime.d.ts.map