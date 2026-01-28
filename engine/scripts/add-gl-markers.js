/**
 * @GL-governed
 * @GL-layer: scripts
 * @GL-semantic: automation-gl-marker-addition
 * @GL-audit-trail: ../governance/GL_SEMANTIC_ANCHOR.json
 * 
 * GL Unified Charter Activated - Automated GL Marker Addition Script
 */
const fs = require('fs');
const path = require('path');

const JS_TS_HEADER = `/**
 * @GL-governed
 * @GL-layer: {LAYER}
 * @GL-semantic: {SEMANTIC}
 * @GL-audit-trail: ../governance/GL_SEMANTIC_ANCHOR.json
 * 
 * GL Unified Charter Activated
 */\n\n`;

function getLayerFromFile(filePath) {
  const parts = filePath.split(path.sep);
  if (parts.includes('executor')) return 'executor';
  if (parts.includes('gl-gate')) return 'gl-gate';
  if (parts.includes('loader')) return 'loader';
  if (parts.includes('normalizer')) return 'normalizer';
  if (parts.includes('parser')) return 'parser';
  if (parts.includes('renderer')) return 'renderer';
  if (parts.includes('validator')) return 'validator';
  if (parts.includes('artifacts')) return 'artifacts';
  if (parts.includes('tests')) return 'tests';
  if (parts.includes('governance')) return 'governance';
  if (parts.includes('types')) return 'types';
  if (parts.includes('aep-engine-app')) return 'aep-engine-app';
  if (parts.includes('aep-engine-web')) return 'aep-engine-web';
  return 'core';
}

function getSemanticFromFile(filePath) {
  const basename = path.basename(filePath, path.extname(filePath));
  const dirname = path.dirname(filePath).split(path.sep).pop();
  return `${dirname}-${basename}`;
}

function addGLMarker(filePath) {
  const ext = path.extname(filePath);
  let content = fs.readFileSync(filePath, 'utf-8');
  
  const layer = getLayerFromFile(filePath);
  const semantic = getSemanticFromFile(filePath);
  
  let header;
  if (ext === '.ts' || ext === '.tsx' || ext === '.js' || ext === '.jsx') {
    header = JS_TS_HEADER.replace('{LAYER}', layer).replace('{SEMANTIC}', semantic);
  }
  
  if (header) {
    if (!content.includes('@GL-governed')) {
      content = header + content;
      fs.writeFileSync(filePath, content);
      return true;
    }
  }
  return false;
}

function walkDir(dir, callback) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      if (!filePath.includes('node_modules') && !filePath.includes('.git')) {
        walkDir(filePath, callback);
      }
    } else {
      callback(filePath);
    }
  }
}

const engineDir = path.join(__dirname, '..');
let count = 0;

walkDir(engineDir, (filePath) => {
  const ext = path.extname(filePath);
  if (['.ts', '.tsx', '.js', '.jsx'].includes(ext)) {
    if (addGLMarker(filePath)) {
      count++;
      console.log(`✓ ${filePath}`);
    }
  }
});

console.log(`\n✅ Added GL markers to ${count} files`);