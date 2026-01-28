// @GL-governed
// GL-ROOT Global Governance Audit & Platform Build
// Unified Charter v2.0.0 - Format Connector (YAML/JSON/Markdown)

const fs = require('fs').promises;
const yaml = require('js-yaml');
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: '../../storage/gl-events-stream/format-connector.log' }),
    new winston.transports.Console()
  ]
});

class FormatConnector {
  constructor() {
    this.eventStream = [];
    this.supportedFormats = ['yaml', 'yml', 'json', 'md', 'markdown'];
  }

  async parseFile(filePath) {
    const parseId = uuidv4();
    const format = this.getFormat(filePath);
    
    logger.info('File parsing started', { parseId, filePath, format });
    this.logEvent('file_parse_started', { parseId, filePath, format });

    try {
      const content = await fs.readFile(filePath, 'utf8');
      const result = await this.parseByFormat(content, format);
      
      const parseResult = {
        parseId,
        filePath,
        format,
        parsed: true,
        data: result,
        parsedAt: new Date().toISOString()
      };

      this.logEvent('file_parse_completed', parseResult);
      return parseResult;
    } catch (error) {
      logger.error('File parsing failed', { parseId, error: error.message });
      this.logEvent('file_parse_failed', { parseId, error: error.message });
      throw error;
    }
  }

  getFormat(filePath) {
    const ext = filePath.split('.').pop().toLowerCase();
    if (ext === 'markdown') return 'md';
    return ext;
  }

  async parseByFormat(content, format) {
    switch (format) {
      case 'yaml':
      case 'yml':
        return yaml.load(content);
      case 'json':
        return JSON.parse(content);
      case 'md':
      case 'markdown':
        return this.parseMarkdown(content);
      default:
        throw new Error(`Unsupported format: ${format}`);
    }
  }

  parseMarkdown(content) {
    // Minimal markdown parser
    const lines = content.split('\n');
    const result = {
      type: 'markdown',
      headers: [],
      codeBlocks: [],
      links: [],
      metadata: {}
    };

    lines.forEach((line, index) => {
      // Extract headers
      const headerMatch = line.match(/^(#{1,6})\s+(.+)$/);
      if (headerMatch) {
        result.headers.push({
          level: headerMatch[1].length,
          text: headerMatch[2],
          line: index
        });
      }

      // Extract code blocks
      if (line.startsWith('```')) {
        result.codeBlocks.push({
          startLine: index,
          language: line.substring(3).trim() || 'text'
        });
      }

      // Extract links
      const linkMatch = line.match(/\[([^\]]+)\]\(([^)]+)\)/g);
      if (linkMatch) {
        linkMatch.forEach(link => {
          const match = link.match(/\[([^\]]+)\]\(([^)]+)\)/);
          if (match) {
            result.links.push({
              text: match[1],
              url: match[2],
              line: index
            });
          }
        });
      }

      // Extract metadata (YAML front matter)
      if (line.startsWith('---') && result.metadataStarted === undefined) {
        result.metadataStarted = true;
        result.metadataEnd = index;
      }
    });

    return result;
  }

  async validateGLCompliance(filePath) {
    const validationId = uuidv4();
    const format = this.getFormat(filePath);
    
    logger.info('GL compliance validation started', { validationId, filePath, format });
    this.logEvent('gl_validation_started', { validationId, filePath, format });

    try {
      const content = await fs.readFile(filePath, 'utf8');
      const violations = [];

      // Check for GL-governed marker
      const marker = format === 'json' ? '"@GL-governed"' : '# @GL-governed';
      if (!content.includes(marker)) {
        violations.push({
          type: 'missing_marker',
          severity: 'error',
          message: `Missing @GL-governed marker for ${format}`
        });
      }

      // Check for semantic anchoring
      const semantic = format === 'json' ? '"@GL-semantic"' : '# @GL-semantic';
      if (!content.includes(semantic)) {
        violations.push({
          type: 'missing_semantic',
          severity: 'warning',
          message: `Missing @GL-semantic anchor for ${format}`
        });
      }

      // Format-specific validation
      if (format === 'yaml' || format === 'yml') {
        await this.validateYAMLStructure(content, violations);
      } else if (format === 'json') {
        await this.validateJSONStructure(content, violations);
      }

      const result = {
        validationId,
        filePath,
        format,
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

  async validateYAMLStructure(content, violations) {
    try {
      yaml.load(content);
    } catch (error) {
      violations.push({
        type: 'yaml_syntax',
        severity: 'error',
        message: `Invalid YAML syntax: ${error.message}`
      });
    }
  }

  async validateJSONStructure(content, violations) {
    try {
      JSON.parse(content);
    } catch (error) {
      violations.push({
        type: 'json_syntax',
        severity: 'error',
        message: `Invalid JSON syntax: ${error.message}`
      });
    }
  }

  calculateCompliance(violations) {
    if (violations.length === 0) return 100;
    
    const errorWeight = 25;
    const warningWeight = 10;
    
    let penalty = 0;
    violations.forEach(v => {
      penalty += v.severity === 'error' ? errorWeight : warningWeight;
    });
    
    return Math.max(0, 100 - penalty);
  }

  async transformToGLCompliant(filePath, transformations) {
    const transformId = uuidv4();
    const format = this.getFormat(filePath);
    
    logger.info('GL transformation started', { transformId, filePath, format });
    this.logEvent('gl_transform_started', { transformId, filePath, format });

    try {
      let content = await fs.readFile(filePath, 'utf8');
      const appliedTransformations = [];

      // Add GL-governed marker
      if (transformations.addGLMarker) {
        let marker;
        if (format === 'json') {
          if (content.startsWith('{')) {
            marker = '  "@GL-governed": true,\n  "@GL-description": "GL-ROOT Global Governance Audit & Platform Build",\n';
            content = content.slice(0, 1) + marker + content.slice(1);
            appliedTransformations.push('added_gl_marker');
          }
        } else {
          marker = '# @GL-governed\n# GL-ROOT Global Governance Audit & Platform Build\n';
          content = marker + content;
          appliedTransformations.push('added_gl_marker');
        }
      }

      // Add semantic anchor
      if (transformations.addSemanticAnchor) {
        if (format === 'json') {
          const anchor = `  "@GL-semantic": "${transformations.semanticValue || 'configuration'}",\n`;
          content = content.slice(0, 1) + anchor + content.slice(1);
          appliedTransformations.push('added_semantic_anchor');
        } else {
          const anchor = `# @GL-semantic: ${transformations.semanticValue || 'configuration'}\n`;
          content = anchor + content;
          appliedTransformations.push('added_semantic_anchor');
        }
      }

      await fs.writeFile(filePath, content, 'utf8');

      const result = {
        transformId,
        filePath,
        format,
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

  async convertFormat(filePath, targetFormat) {
    const convertId = uuidv4();
    const sourceFormat = this.getFormat(filePath);
    
    logger.info('Format conversion started', { convertId, filePath, sourceFormat, targetFormat });
    this.logEvent('format_conversion_started', { convertId, filePath, sourceFormat, targetFormat });

    try {
      const content = await fs.readFile(filePath, 'utf8');
      let convertedContent;

      // Parse source format
      let data;
      switch (sourceFormat) {
        case 'yaml':
        case 'yml':
          data = yaml.load(content);
          break;
        case 'json':
          data = JSON.parse(content);
          break;
        default:
          throw new Error(`Unsupported source format: ${sourceFormat}`);
      }

      // Convert to target format
      switch (targetFormat) {
        case 'yaml':
        case 'yml':
          convertedContent = yaml.dump(data, { indent: 2 });
          break;
        case 'json':
          convertedContent = JSON.stringify(data, null, 2);
          break;
        default:
          throw new Error(`Unsupported target format: ${targetFormat}`);
      }

      const result = {
        convertId,
        filePath,
        sourceFormat,
        targetFormat,
        converted: true,
        convertedContent,
        convertedAt: new Date().toISOString()
      };

      this.logEvent('format_conversion_completed', result);
      return result;
    } catch (error) {
      logger.error('Format conversion failed', { convertId, error: error.message });
      this.logEvent('format_conversion_failed', { convertId, error: error.message });
      throw error;
    }
  }

  logEvent(type, data) {
    const event = {
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      type,
      data,
      source: 'format-connector'
    };
    this.eventStream.push(event);
    logger.info('Format connector event logged', event);

    fs.appendFile(
      './storage/gl-events-stream/format-events.jsonl',
      JSON.stringify(event) + '\n'
    ).catch(err => logger.error('Event stream write failed', { error: err.message }));
  }
}

module.exports = FormatConnector;