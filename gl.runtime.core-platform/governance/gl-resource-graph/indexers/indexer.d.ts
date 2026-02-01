// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-indexing
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

import { FileScanResult } from '../scanners/scanner';
export interface IndexEntry {
    path: string;
    type: string;
    language: string;
    semanticAnchor?: string;
    layer?: string;
    charterVersion?: string;
    dependencies: string[];
    dependents: string[];
}
export declare class ResourceGraphIndexer {
    private pathIndex;
    private typeIndex;
    private languageIndex;
    private semanticIndex;
    buildIndex(scanResults: FileScanResult[]): void;
    private extractMetadata;
    private extractSemanticAnchor;
    private buildDependencyGraph;
    private detectImports;
    private detectPythonImports;
    getByPath(path: string): IndexEntry | undefined;
    getByType(type: string): IndexEntry[];
    getByLanguage(language: string): IndexEntry[];
    getBySemanticAnchor(semanticAnchor: string): IndexEntry[];
    getAllDependencies(path: string): string[];
    getAllDependents(path: string): string[];
    getIndexSize(): number;
}
//# sourceMappingURL=indexer.d.ts.map