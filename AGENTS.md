# Agent System Documentation

[![GL Architecture](https://img.shields.io/badge/GL-Architecture-blue)](https://github.com/MachineNativeOps/machine-native-ops)
[![Agent System](https://img.shields.io/badge/Agent-System-success)](https://github.com/MachineNativeOps/machine-native-ops)

## Overview

The MachineNativeOps platform implements a comprehensive Multi-Agent System (MAS) designed to automate complex platform operations while maintaining strict governance compliance and architectural integrity. This document provides an overview of the agent ecosystem and references to detailed documentation.

## Agent System Architecture

Our agent system follows established Multi-Agent System principles:

- **Autonomy** - Each agent operates independently with its own decision-making logic
- **Cooperation** - Agents collaborate through defined communication protocols
- **Coordination** - Central orchestration ensures coherent system behavior
- **Scalability** - Agents can be added/removed without system disruption
- **Observability** - All agent actions are traceable and auditable

## Core Agent Types

### 1. Planner Agent
**Purpose:** Decompose complex tasks into executable sub-tasks

**Responsibilities:**
- Analyze incoming task requests
- Break down tasks into atomic operations
- Generate execution DAG (Directed Acyclic Graph)
- Identify dependencies and execution order
- Validate task feasibility

### 2. Executor Agent
**Purpose:** Execute atomic operations defined by the planner

**Responsibilities:**
- Execute individual tasks
- Handle errors and retries
- Collect execution metrics
- Report results to orchestrator
- Manage resource cleanup

### 3. Validator Agent
**Purpose:** Validate outputs and ensure compliance with governance policies

**Responsibilities:**
- Validate task outputs against schemas
- Check compliance with governance policies
- Verify security requirements
- Audit execution logs
- Generate compliance reports

### 4. Retriever Agent
**Purpose:** Retrieve context, data, and resources needed for task execution

**Responsibilities:**
- Query databases and APIs
- Retrieve configuration files
- Fetch historical data
- Access external services
- Cache frequently accessed data

### 5. Router Agent
**Purpose:** Route tasks to appropriate agents based on task type and capabilities

**Responsibilities:**
- Analyze task requirements
- Match tasks to capable agents
- Load balance across agent pools
- Handle agent failures
- Optimize routing decisions

## Agent Configurations

### Configuration Directory Structure

```
.github/config/agents/
├── profiles/           # Individual agent profiles
│   ├── custom_agent.yaml
│   └── recovery_expert.yaml
├── team/              # Team/multi-agent configurations
│   └── virtual-experts.yaml
├── schemas/           # JSON schemas for validation
│   └── virtual-experts.schema.json
└── README.md          # Configuration documentation
```

### Virtual Expert Team

The platform includes a virtual expert team for specialized domain knowledge:

- **AI Architect** - AI/ML architecture and model deployment
- **NLP Expert** - Natural language processing and text analysis
- **Security Architect** - Security best practices and threat modeling
- **Database Expert** - Database design and optimization
- **DevOps Specialist** - CI/CD and infrastructure automation
- **Cloud Architect** - Cloud-native architecture and services

See [Agent Configuration README](.github/config/agents/README.md) for detailed configuration instructions.

## Agent Orchestration

The orchestrator coordinates all agents and manages the overall system lifecycle:

```
┌─────────────────────────────────────────────────┐
│                 Task: Deploy Application         │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────▼─────────┐
        │   Planner Agent   │
        │  Decompose Task   │
        └─────────┬─────────┘
                  │
        ┌─────────▼─────────────────────────────┐
        │           Execution DAG               │
        │                                       │
        │  ┌─────────────┐     ┌─────────────┐ │
        │  │ Retriever   │────▶│   Executor  │ │
        │  │ (Config)    │     │ (Build)     │ │
        │  └─────────────┘     └──────┬──────┘ │
        │                             │        │
        │                             ▼        │
        │                      ┌─────────────┐ │
        │                      │   Executor  │ │
        │                      │ (Test)      │ │
        │                      └──────┬──────┘ │
        │                             │        │
        │                             ▼        │
        │                      ┌─────────────┐ │
        │                      │  Validator  │ │
        │                      │ (Compliance)│ │
        │                      └──────┬──────┘ │
        └─────────────────────────────┼────────┘
                                      │
                            ┌─────────▼─────────┐
                            │   Orchestrator    │
                            │  Aggregate Results│
                            └───────────────────┘
```

## Agent Communication

### Message Protocol

All agent communication uses a standardized message format with the following types:

1. **TASK_REQUEST** - Request to execute a task
2. **TASK_RESPONSE** - Task execution result
3. **VALIDATION_REQUEST** - Request to validate output
4. **VALIDATION_RESPONSE** - Validation result
5. **RETRIEVAL_REQUEST** - Request to retrieve data
6. **RETRIEVAL_RESPONSE** - Retrieved data
7. **ERROR_NOTIFICATION** - Error occurred
8. **HEARTBEAT** - Agent heartbeat
9. **STATUS_UPDATE** - Agent status update

### Message Structure

```python
@dataclass
class AgentMessage:
    id: str                    # Unique message ID
    sender: str               # Sender agent ID
    receiver: str             # Receiver agent ID
    timestamp: datetime       # Message timestamp
    type: MessageType         # REQUEST, RESPONSE, NOTIFICATION
    payload: Dict[str, Any]   # Message payload
    correlation_id: str       # Correlation for request/response
    priority: Priority        # LOW, MEDIUM, HIGH, CRITICAL
    ttl: int                  # Time-to-live in seconds
```

## Governance Integration

### GL Layer Compliance

Agents operate within the GL (Governance Layers) architecture and must comply with layer boundaries:

```
GL90-99 (Meta Specifications)
    ↓
GL00-09 (Enterprise Architecture) ← Pure Governance
    ↓
GL10-29 (Platform Services)
    ↓
GL20-29 (Data Processing)
    ↓
GL30-49 (Execution Runtime)
    ↓
GL50-59 (Observability) [Read-Only Monitor]
GL60-80 (Governance Compliance) [GL00-09 Only]
GL81-83 (Extension Services) [Can Extend All]
```

### Policy Enforcement

All agents enforce governance policies through the Validator agent using OPA (Open Policy Agent):

- Schema validation
- Policy compliance checking
- Security verification
- Boundary enforcement
- Audit trail generation

### Audit Trail

All agent actions are logged for auditability with:
- Timestamp and agent identification
- Action type and input/output data
- Duration and performance metrics
- Governance check results
- Redacted sensitive information

## Monitoring & Observability

### Agent Metrics

Each agent exposes metrics for monitoring:

- `agent_tasks_total` - Total tasks executed (by agent and status)
- `agent_task_duration_seconds` - Task execution time
- `agent_pool_size` - Current agent pool size
- `agent_success_rate` - Task success rate
- `agent_resource_usage` - CPU and memory usage

### Dashboards

Grafana dashboards monitor:
- Agent task throughput
- Task failure rates
- Execution latency
- Agent pool utilization
- Governance policy violations

## Security

### Security Measures

1. **Authentication** - Agents authenticate via mTLS or JWT tokens
2. **Authorization** - Agent capabilities restricted by policies
3. **Secrets Management** - Secrets stored in secure vault
4. **Network Isolation** - Agents communicate through secure channels
5. **Audit Logging** - All actions logged and auditable
6. **Boundary Enforcement** - Strict layer boundary compliance

### Zero External Dependencies

Consistent with the MachineNativeOps philosophy:
- No external package dependencies
- No external network calls (except configured integrations)
- Complete offline operation capability
- Local-only resources

## Agent Hooks

The platform includes pre-configured agent hooks for automated operations:

```
.agent_hooks/
├── *.py          # Python-based agent hooks
└── *.txt         # Hook configuration
```

These hooks integrate with Git workflows and CI/CD pipelines to ensure:
- Automated boundary checking
- Pre-commit validation
- Governance compliance enforcement
- Audit trail generation

## Getting Started

### Working with Agents

1. **View Agent Configurations**
   ```bash
   ls -la .github/config/agents/profiles/
   ```

2. **Validate Agent Configuration**
   ```bash
   python tools/scripts/validate-config.js
   ```

3. **Load Agent Configuration**
   ```python
   import yaml
   with open('.github/config/agents/profiles/recovery_expert.yaml') as f:
       agent_config = yaml.safe_load(f)
   ```

### Creating Custom Agents

See [Agent Configuration README](.github/config/agents/README.md) for detailed instructions on:
- Defining agent profiles
- Configuring agent capabilities
- Setting up domain mappings
- Implementing agent logic
- Testing and validation

## Documentation References

### Core Documentation

- **[Multi-Agent Architecture Design](designs/multi-agent-architecture.md)** - Detailed MAS design and implementation
- **[Agent Configuration README](.github/config/agents/README.md)** - Configuration guide and examples
- **[Main README](README.md)** - Platform overview and GL architecture
- **[GL Layer Documentation](gl-runtime-engine-platform/README.md)** - Runtime engine details

### Additional Resources

- **Governance Documentation** - `gl.governance.architecture-platform/`
- **Runtime Execution** - `gl.runtime.execution-platform/`
- **Service Platform** - `gl.runtime.services-platform/`
- **Monitoring & Observability** - `gl.monitoring.observability-platform/`

## Support & Contribution

### Getting Help

For questions about agents:
1. Review the documentation in `.github/config/agents/README.md`
2. Check the multi-agent architecture design in `designs/multi-agent-architecture.md`
3. Review AI Behavior Contract in `.github/AI-BEHAVIOR-CONTRACT.md`
4. Consult technical guidelines in `.github/copilot-instructions.md`

### Contributing

When contributing agent-related changes:
1. Follow the architectural principles defined in this document
2. Respect GL layer boundaries
3. Create interface contracts for cross-layer interactions
4. Run boundary checks before committing
5. Update documentation for all changes
6. Include appropriate tests

### Pre-Commit Process

```bash
# Make changes to agent code
git add .

# Boundary checker runs automatically via pre-commit hook
# Fix any violations

# Commit with descriptive message
git commit -m "feat: add new validator agent for security compliance"

# Push changes
git push
```

## Version Information

- **Platform Version**: 1.0.0
- **Agent System Version**: 1.0.0
- **Governance Level**: CONSTITUTIONAL
- **Compliance**: 100%
- **Last Updated**: 2026-02-03

---

**Maintained by**: MachineNativeOps Core Team  
**Status**: ✅ Active Development  
**License**: [Specify License Here]
