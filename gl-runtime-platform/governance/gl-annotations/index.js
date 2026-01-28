// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-indexing
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

// GL-ROOT Global Governance Audit & Platform Build
// Unified Charter v2.0.0 - GL Annotations Module

const fs = require('fs').promises;
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: '../../storage/gl-events-stream/gl-annotations.log' }),
    new winston.transports.Console()
  ]
});

class GLAnnotations {
  constructor() {
    this.annotations = new Map();
    this.eventStream = [];
  }

  async addAnnotation(file, annotation) {
    const annotationId = uuidv4();
    const annotationData = {
      id: annotationId,
      file,
      ...annotation,
      createdAt: new Date().toISOString()
    };

    this.annotations.set(annotationId, annotationData);
    logger.info('Annotation added', { annotationId, file });
    this.logEvent('annotation_added', annotationData);

    await this.writeAnnotationToFile(file, annotationData);
    
    return annotationId;
  }

  async writeAnnotationToFile(file, annotation) {
    try {
      const content = await fs.readFile(file, 'utf8');
      
      // Check if annotation already exists
      if (!content.includes('@GL-annotation')) {
        const annotationHeader = this.formatAnnotationHeader(annotation);
        const updatedContent = annotationHeader + '\n' + content;
        await fs.writeFile(file, updatedContent, 'utf8');
      }
    } catch (error) {
      logger.error('Failed to write annotation to file', { file, error: error.message });
    }
  }

  formatAnnotationHeader(annotation) {
    const lines = [
      '# @GL-annotation',
      `# @GL-layer: ${annotation.layer || 'GL00-10'}`,
      `# @GL-semantic: ${annotation.semantic || 'annotation'}`,
      `# @GL-type: ${annotation.type || 'metadata'}`,
      `# @GL-version: ${annotation.version || '2.0.0'}`,
      `# @GL-annotation-id: ${annotation.id}`
    ];
    
    if (annotation.description) {
      lines.push(`# @GL-description: ${annotation.description}`);
    }
    
    return lines.join('\n');
  }

  async extractAnnotations(file) {
    const annotations = [];
    
    try {
      const content = await fs.readFile(file, 'utf8');
      const lines = content.split('\n');
      
      let currentAnnotation = null;
      
      for (const line of lines) {
        if (line.includes('@GL-annotation')) {
          currentAnnotation = {
            id: uuidv4(),
            file,
            properties: {}
          };
          annotations.push(currentAnnotation);
        } else if (line.includes('@GL-') && currentAnnotation) {
          const match = line.match(/@GL-(\w+):\s*(.+)/);
          if (match) {
            const [, key, value] = match;
            currentAnnotation.properties[key] = value;
          }
        }
      }
    } catch (error) {
      logger.error('Failed to extract annotations', { file, error: error.message });
    }

    this.logEvent('annotations_extracted', { file, count: annotations.length });
    return annotations;
  }

  async validateAnnotations(file) {
    const annotations = await this.extractAnnotations(file);
    const violations = [];

    for (const annotation of annotations) {
      // Validate required properties
      if (!annotation.properties.layer) {
        violations.push({
          annotationId: annotation.id,
          severity: 'warning',
          message: 'Missing @GL-layer property'
        });
      }

      if (!annotation.properties.semantic) {
        violations.push({
          annotationId: annotation.id,
          severity: 'warning',
          message: 'Missing @GL-semantic property'
        });
      }

      // Validate layer format
      if (annotation.properties.layer && !/^GL[0-9]+-[0-9]+$/.test(annotation.properties.layer)) {
        violations.push({
          annotationId: annotation.id,
          severity: 'error',
          message: 'Invalid @GL-layer format (expected: GL##-##)'
        });
      }
    }

    const result = {
      valid: violations.filter(v => v.severity === 'error').length === 0,
      file,
      annotations,
      violations
    };

    this.logEvent('annotations_validated', result);
    return result;
  }

  getAnnotation(annotationId) {
    return this.annotations.get(annotationId);
  }

  getAnnotationsByFile(file) {
    return Array.from(this.annotations.values()).filter(a => a.file === file);
  }

  getAllAnnotations() {
    return Array.from(this.annotations.values());
  }

  logEvent(type, data) {
    const event = {
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      type,
      data,
      source: 'gl-annotations'
    };
    this.eventStream.push(event);
    logger.info('GL Annotations event logged', event);

    fs.appendFile(
      path.join(__dirname, '../../storage/gl-events-stream/annotation-events.jsonl'),
      JSON.stringify(event) + '\n'
    ).catch(err => logger.error('Event stream write failed', { error: err.message }));
  }
}

module.exports = GLAnnotations;