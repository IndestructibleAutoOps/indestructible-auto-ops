// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-graph-management
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

import { GraphNode, GraphData } from '../graph-model/graph-model';
import { IndexEntry } from '../indexers/indexer';
export interface ResolutionResult {
    found: boolean;
    nodes?: GraphNode[];
    missing?: string[];
    paths?: string[];
}
export declare class ResourceGraphResolver {
    private graphData;
    private indexEntries;
    constructor(graphData: GraphData, indexEntries: Map<string, IndexEntry>);
    resolveFile(path: string): GraphNode | null;
    resolvePath(pattern: string): ResolutionResult;
    resolveDependency(fromPath: string, toPath: string): boolean;
    resolveMissingDependencies(): ResolutionResult;
    resolveMissingFiles(expectedPaths: string[]): ResolutionResult;
    resolveOrphanNodes(): GraphNode[];
    resolveCyclicDependencies(): string[][];
    resolveGovernanceCompliance(): ResolutionResult;
    resolveBySemanticAnchor(semanticAnchor: string): GraphNode[];
    resolveByType(type: string): GraphNode[];
    resolveByLanguage(language: string): GraphNode[];
    exportResolutions(): {
        missingDependencies: string[];
        orphanNodes: string[];
        cyclicDependencies: string[][];
        nonCompliantFiles: string[];
    };
}
//# sourceMappingURL=resolver.d.ts.map