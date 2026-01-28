// @GL-governed
// GL-ROOT Global Governance Audit & Platform Build
// Unified Charter v2.0.0 - JavaScript Language Connector

const fs = require('fs').promises;
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: '../../storage/gl-events-stream/js-connector.log' }),
    new winston.transports.Console()
  ]
});

class JavaScriptConnector {
  constructor() {
    this.eventStream = [];
  }

  async parseFile(filePath) {
    const parseId = uuidv4();
    logger.info('JavaScript file parsing started', { parseId, filePath });
    this.logEvent('js_parse_started', { parseId, filePath });

    try {
      const content = await fs.readFile(filePath, 'utf8');
      const ast = this.parseAST(content);
      
      const result = {
        parseId,
        filePath,
        parsed: true,
        ast: ast,
        dependencies: this.extractDependencies(ast),
        exports: this.extractExports(ast),
        functions: this.extractFunctions(ast),
        parsedAt: new Date().toISOString()
      };

      this.logEvent('js_parse_completed', result);
      return result;
    } catch (error) {
      logger.error('JavaScript file parsing failed', { parseId, error: error.message });
      this.logEvent('js_parse_failed', { parseId, error: error.message });
      throw error;
    }
  }

  parseAST(content) {
    // Minimal AST parser - in production, use acorn or babel
    const ast = {
      type: 'Program',
      body: [],
      comments: [],
      tokens: []
    };

    // Extract function declarations
    const functionRegex = /function\s+(\w+)\s*\(([^)]*)\)/g;
    let match;
    while ((match = functionRegex.exec(content)) !== null) {
      ast.body.push({
        type: 'FunctionDeclaration',
        id: { type: 'Identifier', name: match[1] },
        params: match[2].split(',').map(p => p.trim()).filter(p => p)
      });
    }

    // Extract class declarations
    const classRegex = /class\s+(\w+)/g;
    while ((match = classRegex.exec(content)) !== null) {
      ast.body.push({
        type: 'ClassDeclaration',
        id: { type: 'Identifier', name: match[1] }
      });
    }

    // Extract require statements
    const requireRegex = /require\(['"]([^'"]+)['"]\)/g;
    while ((match = requireRegex.exec(content)) !== null) {
      ast.body.push({
        type: 'RequireStatement',
        source: match[1]
      });
    }

    return ast;
  }

  extractDependencies(ast) {
    return ast.body
      .filter(node => node.type === 'RequireStatement')
      .map(node => node.source);
  }

  extractExports(ast) {
    const exports = [];
    ast.body.forEach(node => {
      if (node.type === 'FunctionDeclaration' || node.type === 'ClassDeclaration') {
        exports.push(node.id.name);
      }
    });
    return exports;
  }

  extractFunctions(ast) {
    return ast.body
      .filter(node => node.type === 'FunctionDeclaration')
      .map(node => ({
        name: node.id.name,
        params: node.params
      }));
  }

  async validateGLCompliance(filePath) {
    const validationId = uuidv4();
    logger.info('GL compliance validation started', { validationId, filePath });
    this.logEvent('gl_validation_started', { validationId, filePath });

    try {
      const content = await fs.readFile(filePath, 'utf8');
      const violations = [];

      // Check for GL-governed marker
      if (!content.includes('@GL-governed')) {
        violations.push({
          type: 'missing_marker',
          severity: 'error',
          message: 'Missing @GL-governed marker'
        });
      }

      // Check for semantic anchoring
      if (!content.includes('@GL-semantic')) {
        violations.push({
          type: 'missing_semantic',
          severity: 'warning',
          message: 'Missing @GL-semantic anchor'
        });
      }

      // Check for layer specification
      if (!content.includes('@GL-layer')) {
        violations.push({
          type: 'missing_layer',
          severity: 'info',
          message: 'Missing @GL-layer specification'
        });
      }

      const result = {
        validationId,
        filePath,
        valid: violations.filter(v => v.severity === 'error').length === 0,
        violations,
        compliance: this.calculateCompliance(violations),
        validatedAt: new Date().toISOString()
      };

      this.logEvent('gl_validation_completed', result);
      return result;
    } catch (error) {
      logger.error('GL compliance validation failed', { validationId, error: error.message });
      this.logEvent('gl_validation_failed', { validationId, error: error.message });
      throw error;
    }
  }

  calculateCompliance(violations) {
    if (violations.length === 0) return 100;
    
    const errorWeight = 25;
    const warningWeight = 10;
    const infoWeight = 5;
    
    let penalty = 0;
    violations.forEach(v => {
      switch (v.severity) {
        case 'error':
          penalty += errorWeight;
          break;
        case 'warning':
          penalty += warningWeight;
          break;
        case 'info':
          penalty += infoWeight;
          break;
      }
    });
    
    return Math.max(0, 100 - penalty);
  }

  async transformToGLCompliant(filePath, transformations) {
    const transformId = uuidv4();
    logger.info('GL transformation started', { transformId, filePath });
    this.logEvent('gl_transform_started', { transformId, filePath });

    try {
      let content = await fs.readFile(filePath, 'utf8');
      const appliedTransformations = [];

      // Add GL-governed marker if requested
      if (transformations.addGLMarker && !content.includes('@GL-governed')) {
        const marker = '// @GL-governed\n// GL-ROOT Global Governance Audit & Platform Build\n';
        content = marker + content;
        appliedTransformations.push('added_gl_marker');
      }

      // Add semantic anchor if requested
      if (transformations.addSemanticAnchor && !content.includes('@GL-semantic')) {
        const anchor = `// @GL-semantic: ${transformations.semanticValue || 'javascript-module'}\n`;
        content = anchor + content;
        appliedTransformations.push('added_semantic_anchor');
      }

      await fs.writeFile(filePath, content, 'utf8');

      const result = {
        transformId,
        filePath,
        transformed: true,
        appliedTransformations,
        transformedAt: new Date().toISOString()
      };

      this.logEvent('gl_transform_completed', result);
      return result;
    } catch (error) {
      logger.error('GL transformation failed', { transformId, error: error.message });
      this.logEvent('gl_transform_failed', { transformId, error: error.message });
      throw error;
    }
  }

  logEvent(type, data) {
    const event = {
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      type,
      data,
      source: 'js-connector'
    };
    this.eventStream.push(event);
    logger.info('JavaScript connector event logged', event);

    fs.appendFile(
      './storage/gl-events-stream/js-events.jsonl',
      JSON.stringify(event) + '\n'
    ).catch(err => logger.error('Event stream write failed', { error: err.message }));
  }
}

module.exports = JavaScriptConnector;