// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: scanner-scanning
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

export interface FileScanResult {
    path: string;
    type: string;
    language: string;
    format: string;
    size: number;
    lastModified: string;
    hasGovernanceTags: boolean;
    hasSemanticAnchor: boolean;
    hasCharterVersion: boolean;
}
export declare class ResourceGraphScanner {
    private scanResults;
    scanRepository(rootPath: string): Promise<FileScanResult[]>;
    private getAllFiles;
    private scanFile;
    private detectFileType;
    private detectLanguage;
    private detectFormat;
    getScanResults(): Map<string, FileScanResult>;
    getFilesByType(type: string): FileScanResult[];
    getFilesByLanguage(language: string): FileScanResult[];
    getFilesWithoutGovernanceTags(): FileScanResult[];
}
//# sourceMappingURL=scanner.d.ts.map