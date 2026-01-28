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