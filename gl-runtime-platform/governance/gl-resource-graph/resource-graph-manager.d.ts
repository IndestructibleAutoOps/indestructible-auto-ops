// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-graph-management
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

import { ResourceGraphScanner } from './scanners/scanner';
import { ResourceGraphIndexer } from './indexers/indexer';
import { ResourceGraphModel } from './graph-model/graph-model';
import { ResourceGraphResolver } from './resolvers/resolver';
export interface GlobalResourceGraph {
    version: string;
    timestamp: string;
    nodes: any[];
    edges: any[];
    statistics: any;
    resolutions: any;
}
export declare class ResourceGraphManager {
    private scanner;
    private indexer;
    private graphModel;
    private resolver;
    private eventStream;
    private artifactStore;
    constructor();
    buildGlobalResourceGraph(rootPath: string): Promise<GlobalResourceGraph>;
    getScanner(): ResourceGraphScanner;
    getIndexer(): ResourceGraphIndexer;
    getGraphModel(): ResourceGraphModel;
    getResolver(): ResourceGraphResolver;
    loadGlobalResourceGraph(artifactId: string): Promise<GlobalResourceGraph | null>;
    checkGraphFreshness(rootPath: string): Promise<boolean>;
}
//# sourceMappingURL=resource-graph-manager.d.ts.map