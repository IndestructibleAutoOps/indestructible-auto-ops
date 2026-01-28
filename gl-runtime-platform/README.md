// @GL-governed
// @GL-layer: GL70-89
// @GL-semantic: runtime-general-purpose
// @GL-charter-version: 2.0.0
// @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json

# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: runtime-platform-documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# GL Runtime Platform - Complete Governance & Repair Platform

## Overview

GL Runtime Platform is a production-grade, cross-module, cross-platform, cross-language, cross-format governance and repair platform. It provides comprehensive GL (Governance Layers) governance capabilities with automatic audit, repair, integration, and deployment functionalities.

## Architecture

### Core Components

- **Orchestration Engine** - Multi-agent parallel orchestration system
- **Sandbox Runner** - Isolated per-file execution environment
- **Scheduler** - Task scheduling and automation
- **GL Core** - Governance rule engine and semantic anchor management
- **GL Policy Engine** - Policy validation and compliance enforcement
- **GL Annotations** - Governance annotation management system

### Connectors

- **Git Connector** - Repository scanning, diff, patch, commit, push
- **GitHub CI Connector** - CI/CD workflow integration
- **JavaScript Connector** - JS/TS file processing and validation
- **Python Connector** - Python file processing and validation
- **Format Connector** - YAML/JSON/Markdown processing and validation

### Operations

- **Pipelines** - Directory audit and repo fix pipelines
- **Agents** - Multi-agent orchestration configuration
- **Auto-Bootstrap** - Automatic repair, integration, deployment, federation

### Storage

- **GL Artifacts Store** - Audit reports, patches, metadata storage
- **GL Events Stream** - Complete governance event tracking

### API

- **REST API** - Comprehensive API for audit, fix, integrate, deploy operations
- **gRPC API** - High-performance API for enterprise integration (planned)

### Deployment

- **Docker Compose** - Local development and testing
- **Kubernetes** - Production deployment with auto-scaling

## Installation

```bash
# Clone repository
git clone https://github.com/MachineNativeOps/machine-native-ops.git
cd machine-native-ops/gl-runtime-platform

# Install dependencies
npm install

# Build platform
npm run build
```

## Usage

### Start Platform

```bash
# Using Node.js
npm start

# Using Docker Compose
cd deployment
docker-compose up -d

# Using Kubernetes
kubectl apply -f deployment/k8s/
```

### API Endpoints

#### Audit Operations
- `POST /api/v1/audit` - Start audit
- `GET /api/v1/audit/:id` - Get audit results

#### Fix Operations
- `POST /api/v1/fix` - Apply fixes
- `GET /api/v1/fix/:id` - Get fix results

#### Integration Operations
- `POST /api/v1/integrate` - Start integration
- `GET /api/v1/integrate/:id` - Get integration results

#### Deployment Operations
- `POST /api/v1/deploy` - Start deployment
- `GET /api/v1/deploy/:id` - Get deployment results

#### Governance Operations
- `GET /api/v1/governance/status` - Get governance status
- `GET /api/v1/governance/rules` - Get governance rules
- `GET /api/v1/governance/policies` - Get governance policies

#### Sandbox Operations
- `POST /api/v1/sandbox/execute` - Execute in sandbox

#### Git Operations
- `GET /api/v1/git/status` - Get git status
- `POST /api/v1/git/commit` - Commit changes

## Configuration

### Environment Variables

- `GL_TOKEN` - GitHub token for git operations
- `GL_MODE` - Platform mode (orchestration/governance/connectors)
- `LOG_LEVEL` - Logging level (debug/info/warn/error)
- `NODE_ENV` - Environment (development/production)

### Configuration Files

- `ops/pipelines/` - Pipeline definitions
- `ops/agents/agent-orchestration.yaml` - Agent configuration
- `ops/auto-bootstrap/` - Auto-bootstrap configurations

## Governance Compliance

All components are GL-governed with:
- `@GL-governed` markers
- `@GL-semantic` anchors
- `@GL-layer` specifications
- `@GL-audit-trail` references
- Complete event stream tracking

## Monitoring

### Metrics

Platform exposes metrics on port 9090:
- Execution time
- Resource usage
- Compliance scores
- Event stream metrics

### Logging

All events are logged to `storage/gl-events-stream/`
- Separate log files per component
- JSONL format for easy parsing
- Complete audit trail

## Testing

```bash
# Run tests
npm test

# Run linting
npm run lint

# Run audit
npm run audit
```

## Development

### Project Structure

```
gl-runtime-platform/
├── engine/
│   ├── orchestration-engine/
│   ├── sandbox-runner/
│   └── scheduler/
├── governance/
│   ├── gl-core/
│   ├── gl-policy-engine/
│   └── gl-annotations/
├── connectors/
│   ├── connector-git/
│   ├── connector-ci-github/
│   ├── connector-lang-js/
│   ├── connector-lang-py/
│   └── connector-format-yaml-json-md/
├── ops/
│   ├── pipelines/
│   ├── agents/
│   └── auto-bootstrap/
├── storage/
│   ├── gl-artifacts-store/
│   └── gl-events-stream/
├── api/
│   ├── rest/
│   └── grpc/
└── deployment/
    ├── k8s/
    └── docker-compose.yaml
```

## License

MIT License - GL Unified Charter v2.0.0 Activated

## Support

For issues and questions, please contact the GL Governance Team.