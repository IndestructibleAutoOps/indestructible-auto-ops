<!--
GL Governance Markers
@gl-layer GL-00-NAMESPACE
@gl-module ns-root/namespaces-sdk
@gl-semantic-anchor GL-00-NAMESPAC_README
@gl-evidence-required false
GL Unified Charter Activated
-->

# namespace-sdk

A Machine-Native, Auditable Platform Integration Layer for MCP Tool Wrapping

## Overview

`namespace-sdk` is a comprehensive SDK designed to wrap external APIs, SDKs, and service interfaces (including GitHub, Cloudflare, OpenAI, and Google APIs) into standardized, MCP-compatible, and auditable tools. It provides a robust foundation for building machine-native governance systems with enterprise-grade security, observability, and extensibility.

## Features

### Core Capabilities

- **MCP Protocol Compliance**: Full support for Model Context Protocol (MCP) tool wrapping and invocation
- **Multi-Service Integration**: Built-in adapters for GitHub, Cloudflare, OpenAI, Google, and extensible for custom services
- **Schema Validation**: Comprehensive JSON Schema validation for all tool inputs and outputs
- **Credential Management**: Secure, multi-provider credential handling with rotation and expiration support
- **Observability**: Built-in logging, tracing, metrics, and audit trails
- **Plugin System**: Hot-pluggable architecture for dynamic tool and adapter registration
- **Type Safety**: Full TypeScript support with comprehensive type definitions

### Security & Governance

- **Audit Trails**: Tamper-evident logging of all sensitive operations
- **Credential Security**: Support for environment variables, files, HashiCorp Vault, and cloud secret managers
- **Input Validation**: Multi-layer validation to prevent injection and malformed data
- **Least Privilege**: Scoped credentials and minimal permission requirements
- **Compliance Ready**: Built-in support for GDPR, HIPAA, and SOC 2 requirements

### Developer Experience

- **Intuitive API**: Clean, fluent API design for easy integration
- **Comprehensive Documentation**: Detailed guides, API references, and examples
- **CLI Tools**: Command-line interface for tool discovery, invocation, and diagnostics
- **Testing Support**: Built-in testing utilities and contract testing support
- **Hot Reload**: Dynamic configuration and plugin loading without restarts

## Installation

```bash
npm install @mno-repository-understanding-system/namespaces-sdk
```

Or with yarn:

```bash
yarn add @mno-repository-understanding-system/namespaces-sdk
```

## Quick Start

### Basic Usage

```typescript
import { createSDK } from '@mno-repository-understanding-system/namespaces-sdk';

// Create and initialize SDK
const sdk = await createSDK({
  debug: true,
  credentials: {
    providers: ['env', 'file'],
    defaultProvider: 'env'
  }
});

// Register a tool
sdk.registerTool(myTool);

// List available tools
const tools = sdk.listTools();
console.log('Available tools:', tools);

// Invoke a tool
const result = await sdk.invokeTool('my_tool', {
  param1: 'value1',
  param2: 'value2'
});

console.log('Result:', result);

// Cleanup
await sdk.shutdown();
```

### Creating a Custom Tool

```typescript
import { createTool, CredentialType } from '@mno-repository-understanding-system/namespaces-sdk';

const myTool = createTool()
  .name('my_custom_tool')
  .title('My Custom Tool')
  .description('A custom tool that does something useful')
  .version('1.0.0')
  .adapter('my-service')
  .input({
    type: 'object',
    properties: {
      message: {
        type: 'string',
        description: 'Message to process'
      }
    },
    required: ['message']
  })
  .output({
    type: 'object',
    properties: {
      result: {
        type: 'string',
        description: 'Processed result'
      }
    }
  })
  .requireCredential('api_key', {
    scope: 'read',
    required: true,
    description: 'API key for authentication'
  })
  .handler(async (params, credentials) => {
    // Tool implementation
    const result = await processMessage(params.message, credentials.api_key);
    
    return {
      success: true,
      data: { result }
    };
  })
  .build();

// Register the tool
sdk.registerTool(myTool);
```

### Using Service Adapters

```typescript
import { createSDK } from '@mno-repository-understanding-system/namespaces-sdk';
import { GitHubAdapter } from '@mno-repository-understanding-system/namespaces-sdk/adapters/github';

const sdk = await createSDK();

// Initialize GitHub adapter
const github = new GitHubAdapter({
  token: process.env.GITHUB_TOKEN
});

await github.initialize(sdk);

// Use GitHub tools
const result = await sdk.invokeTool('github_create_issue', {
  repository: 'owner/repo',
  title: 'Issue title',
  body: 'Issue description'
});
```

## Configuration

### Environment Variables

```bash
# SDK Configuration
SDK_ENVIRONMENT=development
SDK_DEBUG=true

# Logging
SDK_LOG_LEVEL=info
SDK_LOG_FORMAT=json

# Credentials
SDK_GITHUB_TOKEN=your_token_here
SDK_OPENAI_API_KEY=your_key_here
```

### Configuration File

Create a `config.json` file:

```json
{
  "environment": "production",
  "logging": {
    "level": "info",
    "format": "json",
    "enabled": true
  },
  "tracing": {
    "enabled": true,
    "samplingRate": 1.0
  },
  "credentials": {
    "providers": ["env", "vault"],
    "defaultProvider": "vault"
  }
}
```

## Architecture

### Core Components

- **SDK Core**: Main orchestration and lifecycle management
- **Tool Registry**: Dynamic tool discovery and registration
- **Schema Validator**: JSON Schema validation engine
- **Credential Manager**: Secure credential storage and retrieval
- **Observability Layer**: Logging, tracing, metrics, and audit trails
- **Plugin System**: Hot-pluggable extension architecture

### Service Adapters

- **GitHub**: Repository management, issues, pull requests
- **Cloudflare**: DNS, Workers, KV, R2
- **OpenAI**: Chat completions, embeddings, assistants
- **Google**: Cloud services, APIs, authentication

## Documentation

- [Quick Start Guide](./src/docs/quickstart.md)
- [API Reference](./src/docs/api.md)
- [Service Adapters](./src/docs/adapters.md)
- [Plugin Development](./src/docs/plugins.md)
- [Security Best Practices](./src/docs/security.md)

## Development

### Setup

```bash
# Install dependencies
npm install

# Build the project
npm run build

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Lint code
npm run lint

# Format code
npm run format
```

### Project Structure

```
namespaces-sdk/
├── src/
│   ├── core/           # Core SDK logic
│   ├── adapters/       # Service adapters
│   ├── schema/         # Schema validation
│   ├── credentials/    # Credential management
│   ├── observability/  # Logging, tracing, metrics
│   ├── config/         # Configuration management
│   ├── plugins/        # Plugin system
│   └── index.ts        # Main entry point
├── docs/               # Documentation
├── examples/           # Usage examples
└── tests/              # Test suites
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](./LICENSE) file for details.

## Support

- GitHub Issues: [Report bugs or request features](https://github.com/your-org/mno-repository-understanding-system/issues)
- Documentation: [Full documentation](https://github.com/your-org/mno-repository-understanding-system/tree/main/ns-root/namespaces-sdk)
- Community: [Join our discussions](https://github.com/your-org/mno-repository-understanding-system/discussions)

## Roadmap

- [ ] Additional service adapters (AWS, Azure, Stripe, etc.)
- [ ] GraphQL API support
- [ ] WebSocket tool invocation
- [ ] Multi-language SDK generation
- [ ] Enhanced plugin marketplace
- [ ] Real-time collaboration features

## Acknowledgments

Built with ❤️ by the NinjaTech AI team as part of the machine-native-ops project.