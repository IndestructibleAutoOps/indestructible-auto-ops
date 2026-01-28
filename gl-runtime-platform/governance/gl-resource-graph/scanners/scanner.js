"use strict";
// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: resource-graph-scanner
// @GL-charter-version: 2.0.0
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ResourceGraphScanner = void 0;
const promises_1 = __importDefault(require("fs/promises"));
const path_1 = __importDefault(require("path"));
const logger_1 = require("../../src/utils/logger");
const logger = (0, logger_1.createLogger)('ResourceGraphScanner');
class ResourceGraphScanner {
    constructor() {
        this.scanResults = new Map();
    }
    async scanRepository(rootPath) {
        logger.info(`Starting repository scan: ${rootPath}`);
        const files = await this.getAllFiles(rootPath);
        const results = [];
        for (const file of files) {
            const result = await this.scanFile(file);
            results.push(result);
            this.scanResults.set(file, result);
        }
        logger.info(`Scanned ${results.length} files`);
        return results;
    }
    async getAllFiles(dir) {
        const files = [];
        const entries = await promises_1.default.readdir(dir, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path_1.default.join(dir, entry.name);
            // Skip node_modules, .git, dist, build
            if (['node_modules', '.git', 'dist', 'build'].includes(entry.name)) {
                continue;
            }
            if (entry.isDirectory()) {
                const subFiles = await this.getAllFiles(fullPath);
                files.push(...subFiles);
            }
            else {
                files.push(fullPath);
            }
        }
        return files;
    }
    async scanFile(filePath) {
        try {
            const stats = await promises_1.default.stat(filePath);
            const content = await promises_1.default.readFile(filePath, 'utf-8');
            const ext = path_1.default.extname(filePath);
            const result = {
                path: filePath,
                type: this.detectFileType(filePath),
                language: this.detectLanguage(filePath),
                format: this.detectFormat(ext),
                size: stats.size,
                lastModified: stats.mtime.toISOString(),
                hasGovernanceTags: content.includes('@GL-governed'),
                hasSemanticAnchor: content.includes('@GL-semantic'),
                hasCharterVersion: content.includes('@GL-charter-version')
            };
            return result;
        }
        catch (error) {
            logger.error(`Failed to scan file ${filePath}: ${error.message}`);
            return {
                path: filePath,
                type: 'unknown',
                language: 'unknown',
                format: 'unknown',
                size: 0,
                lastModified: new Date().toISOString(),
                hasGovernanceTags: false,
                hasSemanticAnchor: false,
                hasCharterVersion: false
            };
        }
    }
    detectFileType(filePath) {
        const ext = path_1.default.extname(filePath);
        const fileTypes = {
            '.ts': 'typescript',
            '.js': 'javascript',
            '.py': 'python',
            '.java': 'java',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.md': 'markdown',
            '.txt': 'text',
            '.sh': 'shell'
        };
        return fileTypes[ext] || 'unknown';
    }
    detectLanguage(filePath) {
        const ext = path_1.default.extname(filePath);
        const languages = {
            '.ts': 'typescript',
            '.js': 'javascript',
            '.py': 'python',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c'
        };
        return languages[ext] || 'none';
    }
    detectFormat(ext) {
        const formats = {
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.xml': 'xml',
            '.toml': 'toml',
            '.md': 'markdown',
            '.txt': 'text'
        };
        return formats[ext] || 'binary';
    }
    getScanResults() {
        return this.scanResults;
    }
    getFilesByType(type) {
        return Array.from(this.scanResults.values()).filter(f => f.type === type);
    }
    getFilesByLanguage(language) {
        return Array.from(this.scanResults.values()).filter(f => f.language === language);
    }
    getFilesWithoutGovernanceTags() {
        return Array.from(this.scanResults.values()).filter(f => !f.hasGovernanceTags);
    }
}
exports.ResourceGraphScanner = ResourceGraphScanner;
//# sourceMappingURL=scanner.js.map