# @GL-governed
# @GL-layer: GL20-29
# @GL-semantic: javascript-module
# @GL-audit-trail: ../../engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
#
# GL Unified Charter Activated
# GL Root Semantic Anchor: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/semantic/GL-ROOT-SEMANTIC-ANCHOR.yaml
# GL Unified Naming Charter: gl-platform-universe/governance/engine/governance/gl-artifacts/meta/naming-charter/gl-unified-naming-charter.yaml

/**
 * @GL-governed
 * @version 21.0.0
 * @priority 2
 * @stage complete
 */
const { CivilizationServer } = require('./dist/src/civilization-server');

const server = new CivilizationServer(3003);
server.start();

// Wait a moment then test the API
setTimeout(() => {
  console.log('\n=== Testing Civilization API ===\n');
  
  // Test health check
  fetch('http://localhost:3003/health')
    .then(res => res.json())
    .then(data => {
      console.log('✅ Health Check:', data);
      
      // Test civilization status
      return fetch('http://localhost:3003/api/v13/civilization/status');
    })
    .then(res => res.json())
    .then(data => {
      console.log('✅ Civilization Status:', JSON.stringify(data, null, 2));
      console.log('\n=== All Tests Passed ===\n');
      process.exit(0);
    })
    .catch(err => {
      console.error('❌ Error:', err);
      process.exit(1);
    });
}, 3000);