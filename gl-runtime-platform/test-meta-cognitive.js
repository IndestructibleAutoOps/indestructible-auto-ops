const { MetaCognitiveServer } = require('./dist/src/meta-cognitive-server');

const server = new MetaCognitiveServer(3004);
server.start();

// Wait a moment then test the API
setTimeout(() => {
  console.log('\n=== Testing Meta-Cognitive API ===\n');
  
  // Test health check
  fetch('http://localhost:3004/health')
    .then(res => res.json())
    .then(data => {
      console.log('✅ Health Check:', data);
      
      // Test meta-cognitive status
      return fetch('http://localhost:3004/api/v14/meta-cognitive/status');
    })
    .then(res => res.json())
    .then(data => {
      console.log('✅ Meta-Cognitive Status:', JSON.stringify(data, null, 2));
      console.log('\n=== All Tests Passed ===\n');
      process.exit(0);
    })
    .catch(err => {
      console.error('❌ Error:', err);
      process.exit(1);
    });
}, 3000);