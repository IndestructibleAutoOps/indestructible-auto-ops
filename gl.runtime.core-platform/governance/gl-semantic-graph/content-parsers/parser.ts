// @GL-governed
// @GL-layer: governance
// @GL-semantic: semantic-content-parser
// @GL-charter-version: 2.0.0

import fs from 'fs/promises';
import path from 'path';

export interface ParsedContent {
  type: string;
  language: string;
  format: string;
  content: any;
  metadata: any;
  functions?: string[];
  classes?: string[];
  imports?: string[];
  exports?: string[];
  schemas?: any[];
  apiEndpoints?: any[];
}

export class ContentParser {
  async parse(filePath: string): Promise<ParsedContent> {
    const ext = path.extname(filePath);
    const content = await fs.readFile(filePath, 'utf-8');
    
    switch (ext) {
      case '.ts':
      case '.js':
        return this.parseCode(filePath, content, ext === '.ts' ? 'typescript' : 'javascript');
      case '.py':
        return this.parseCode(filePath, content, 'python');
      case '.yaml':
      case '.yml':
        return this.parseYaml(filePath, content);
      case '.json':
        return this.parseJson(filePath, content);
      case '.md':
        return this.parseMarkdown(filePath, content);
      default:
        return this.parseText(filePath, content);
    }
  }

  private parseCode(filePath: string, content: string, language: string): ParsedContent {
    const functions = this.extractFunctions(content, language);
    const classes = this.extractClasses(content, language);
    const imports = this.extractImports(content, language);
    const exports = this.extractExports(content, language);

    return {
      type: 'code',
      language,
      format: 'source',
      content,
      metadata: { lineCount: content.split('\n').length },
      functions,
      classes,
      imports,
      exports
    };
  }

  private parseYaml(filePath: string, content: string): ParsedContent {
    try {
      // Simple YAML parsing for metadata
      const schemas = this.extractSchemas(content);
      const apiEndpoints = this.extractApiEndpoints(content);
      
      return {
        type: 'configuration',
        language: 'yaml',
        format: 'yaml',
        content,
        metadata: {},
        schemas,
        apiEndpoints
      };
    } catch {
      return {
        type: 'configuration',
        language: 'yaml',
        format: 'yaml',
        content,
        metadata: {}
      };
    }
  }

  private parseJson(filePath: string, content: string): ParsedContent {
    try {
      const json = JSON.parse(content);
      return {
        type: 'data',
        language: 'json',
        format: 'json',
        content: json,
        metadata: {}
      };
    } catch {
      return {
        type: 'data',
        language: 'json',
        format: 'json',
        content,
        metadata: {}
      };
    }
  }

  private parseMarkdown(filePath: string, content: string): ParsedContent {
    return {
      type: 'documentation',
      language: 'markdown',
      format: 'markdown',
      content,
      metadata: {
        sections: content.split(/^#+\s/m).length - 1,
        codeBlocks: (content.match(/```/g) || []).length / 2
      }
    };
  }

  private parseText(filePath: string, content: string): ParsedContent {
    return {
      type: 'text',
      language: 'plaintext',
      format: 'text',
      content,
      metadata: { lineCount: content.split('\n').length }
    };
  }

  private extractFunctions(content: string, language: string): string[] {
    const patterns: Record<string, RegExp> = {
      typescript: /(?:function|const|let|var)\s+(\w+)\s*(?:=\s*(?:async\s*)?\(|\()/g,
      javascript: /(?:function|const|let|var)\s+(\w+)\s*(?:=\s*(?:async\s*)?\(|\()/g,
      python: /def\s+(\w+)\s*\(/g
    };
    
    const pattern = patterns[language] || patterns.javascript;
    const functions: string[] = [];
    let match;
    while ((match = pattern.exec(content)) !== null) {
      functions.push(match[1]);
    }
    return functions;
  }

  private extractClasses(content: string, language: string): string[] {
    const patterns: Record<string, RegExp> = {
      typescript: /class\s+(\w+)/g,
      javascript: /class\s+(\w+)/g,
      python: /class\s+(\w+)/g
    };
    
    const pattern = patterns[language] || patterns.typescript;
    const classes: string[] = [];
    let match;
    while ((match = pattern.exec(content)) !== null) {
      classes.push(match[1]);
    }
    return classes;
  }

  private extractImports(content: string, language: string): string[] {
    const patterns: Record<string, RegExp> = {
      typescript: /import\s+.*\s+from\s+['"]([^'"]+)['"]/g,
      javascript: /import\s+.*\s+from\s+['"]([^'"]+)['"]/g,
      python: /from\s+(\S+)\s+import|import\s+(\S+)/g
    };
    
    const pattern = patterns[language] || patterns.typescript;
    const imports: string[] = [];
    let match;
    while ((match = pattern.exec(content)) !== null) {
      imports.push(match[1] || match[2]);
    }
    return [...new Set(imports)];
  }

  private extractExports(content: string, language: string): string[] {
    const patterns: Record<string, RegExp> = {
      typescript: /export\s+(?:default\s+)?(?:class|function|const|let|var|interface|type)\s+(\w+)/g,
      javascript: /export\s+(?:default\s+)?(?:class|function|const|let|var)\s+(\w+)/g,
      python: /__all__\s*=\s*\[([^\]]+)\]/g
    };
    
    const pattern = patterns[language] || patterns.typescript;
    const exports: string[] = [];
    let match;
    while ((match = pattern.exec(content)) !== null) {
      exports.push(match[1]);
    }
    return exports;
  }

  private extractSchemas(content: string): any[] {
    const schemas: any[] = [];
    const yamlSchemaMatch = content.match(/kind:\s*Schema/gi);
    if (yamlSchemaMatch) {
      schemas.push({ type: 'Schema', count: yamlSchemaMatch.length });
    }
    return schemas;
  }

  private extractApiEndpoints(content: string): any[] {
    const endpoints: any[] = [];
    const pathMatch = content.match(/path:\s*['"]([^'"]+)['"]/g);
    const methodMatch = content.match(/method:\s*['"]([^'"]+)['"]/gi);
    
    if (pathMatch && methodMatch) {
      for (let i = 0; i < pathMatch.length; i++) {
        endpoints.push({
          path: pathMatch[i].match(/['"]([^'"]+)['"]/)?.[1],
          method: methodMatch[i]?.match(/['"]([^'"]+)['"]/)?.[1]?.toUpperCase()
        });
      }
    }
    return endpoints;
  }
}