// @GL-governed
// @GL-layer: GL90-99
// @GL-semantic: runtime-indexing
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

// GL-ROOT Global Governance Audit & Platform Build
// Unified Charter v2.0.0 - GL Core Module

const fs = require('fs').promises;
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');
const yaml = require('js-yaml');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: '../../storage/gl-events-stream/gl-core.log' }),
    new winston.transports.Console()
  ]
});

class GLCore {
  constructor() {
    this.semanticAnchor = null;
    this.governanceRules = new Map();
    this.eventStream = [];
    this.loadSemanticAnchor();
    this.loadGovernanceRules();
  }

  async loadSemanticAnchor() {
    try {
      const anchorPath = path.join(__dirname, '../../../engine/governance/GL_SEMANTIC_ANCHOR.json');
      const content = await fs.readFile(anchorPath, 'utf8');
      this.semanticAnchor = JSON.parse(content);
      logger.info('Semantic anchor loaded', { version: this.semanticAnchor.version });
      this.logEvent('semantic_anchor_loaded', { path: anchorPath });
    } catch (error) {
      logger.warn('Semantic anchor not found, using defaults', { error: error.message });
      this.semanticAnchor = {
        version: '2.0.0',
        root: 'GL-ROOT',
        layers: ['GL00-10', 'GL10-30', 'GL30-60', 'GL60-90', 'GL90-99'],
        semantics: {}
      };
      this.logEvent('semantic_anchor_defaults_used', {});
    }
  }

  async loadGovernanceRules() {
    try {
      const rulesPath = path.join(__dirname, 'rules.yaml');
      const content = await fs.readFile(rulesPath, 'utf8');
      const rules = yaml.load(content);
      
      rules.forEach(rule => {
        this.governanceRules.set(rule.id, rule);
      });
      
      logger.info('Governance rules loaded', { count: this.governanceRules.size });
      this.logEvent('governance_rules_loaded', { count: this.governanceRules.size });
    } catch (error) {
      logger.warn('Governance rules not found, using defaults', { error: error.message });
      this.initializeDefaultRules();
    }
  }

  initializeDefaultRules() {
    const defaultRules = [
      {
        id: 'gl-001',
        name: 'GL Governed Marker Required',
        severity: 'error',
        scope: 'all',
        description: 'All files must have @GL-governed marker',
        enforcement: 'strict'
      },
      {
        id: 'gl-002',
        name: 'Semantic Anchor Required',
        severity: 'warning',
        scope: 'code',
        description: 'Code files must have @GL-semantic anchor',
        enforcement: 'strict'
      },
      {
        id: 'gl-003',
        name: 'Layer Compliance Required',
        severity: 'error',
        scope: 'architecture',
        description: 'Components must specify GL layer',
        enforcement: 'strict'
      },
      {
        id: 'gl-004',
        name: 'Naming Convention Compliance',
        severity: 'warning',
        scope: 'naming',
        description: 'Must follow GL naming conventions',
        enforcement: 'moderate'
      }
    ];

    defaultRules.forEach(rule => {
      this.governanceRules.set(rule.id, rule);
    });

    logger.info('Default governance rules initialized', { count: defaultRules.length });
    this.logEvent('default_rules_initialized', { count: defaultRules.length });
  }

  validateFile(file) {
    const violations = [];
    
    this.governanceRules.forEach((rule, ruleId) => {
      const violation = this.checkRule(file, rule);
      if (violation) {
        violations.push({
          ruleId,
          ruleName: rule.name,
          severity: rule.severity,
          description: rule.description,
          violation: violation
        });
      }
    });

    const compliance = this.calculateCompliance(violations);
    
    const result = {
      file,
      validated: true,
      violations,
      compliance,
      timestamp: new Date().toISOString()
    };

    this.logEvent('file_validated', result);
    return result;
  }

  checkRule(file, rule) {
    // Rule checking logic based on rule type
    switch (rule.scope) {
      case 'all':
        return this.checkAllFilesRule(file, rule);
      case 'code':
        return this.checkCodeRule(file, rule);
      case 'architecture':
        return this.checkArchitectureRule(file, rule);
      case 'naming':
        return this.checkNamingRule(file, rule);
      default:
        return null;
    }
  }

  async checkAllFilesRule(file, rule) {
    if (rule.id === 'gl-001') {
      try {
        const content = await fs.readFile(file, 'utf8');
        if (!content.includes('@GL-governed')) {
          return 'Missing @GL-governed marker';
        }
      } catch (error) {
        return `Cannot read file: ${error.message}`;
      }
    }
    return null;
  }

  async checkCodeRule(file, rule) {
    if (rule.id === 'gl-002') {
      const codeExtensions = ['.js', '.ts', '.py', '.go', '.java'];
      if (codeExtensions.some(ext => file.endsWith(ext))) {
        try {
          const content = await fs.readFile(file, 'utf8');
          if (!content.includes('@GL-semantic')) {
            return 'Missing @GL-semantic anchor';
          }
        } catch (error) {
          return `Cannot read file: ${error.message}`;
        }
      }
    }
    return null;
  }

  checkArchitectureRule(file, rule) {
    if (rule.id === 'gl-003') {
      // Check for GL layer specification in architecture files
      return null;
    }
    return null;
  }

  checkNamingRule(file, rule) {
    if (rule.id === 'gl-004') {
      const filename = path.basename(file);
      if (/[A-Z]/.test(filename) && !filename.includes('GL')) {
        return 'Non-GL uppercase characters detected';
      }
    }
    return null;
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

  getSemanticAnchor() {
    return this.semanticAnchor;
  }

  getGovernanceRules() {
    return Array.from(this.governanceRules.values());
  }

  logEvent(type, data) {
    const event = {
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      type,
      data,
      source: 'gl-core'
    };
    this.eventStream.push(event);
    logger.info('GL Core event logged', event);

    fs.appendFile(
      path.join(__dirname, '../../storage/gl-events-stream/gl-core-events.jsonl'),
      JSON.stringify(event) + '\n'
    ).catch(err => logger.error('Event stream write failed', { error: err.message }));
  }
}

module.exports = GLCore;