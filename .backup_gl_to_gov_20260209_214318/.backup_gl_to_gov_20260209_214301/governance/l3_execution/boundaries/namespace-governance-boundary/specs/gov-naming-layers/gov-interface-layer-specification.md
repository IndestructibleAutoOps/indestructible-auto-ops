# GL Interface Layer Specification

## Interface Layer - 介面層

### Layer Overview

The Interface Layer defines naming conventions for interface resources including APIs, RPCs, GraphQL, and event interfaces. This layer ensures consistent interface definition across the platform, enabling effective service communication, contract management, and version control.

### 1. API Interface Naming

**Pattern**: `gl.interface.api`

**Format**: `gl.{service}.{resource}-api`

**Naming Rules**:
- Must use API identifier: `-api`
- Service identifies the service name
- Resource identifies the API resource

**Examples**:
```yaml
# Valid
gl.runtime.user-api
gl.data.product-api
gl.security.auth-api

# Invalid
user-api
runtime-api
api
```

**Purpose**: RESTful API interface definitions

### 2. RPC Interface Naming

**Pattern**: `gl.interface.rpc`

**Format**: `gl.{service}.{method}-rpc`

**Naming Rules**:
- Must use RPC identifier: `-rpc`
- Service identifies the service name
- Method identifies the RPC method

**Examples**:
```yaml
# Valid
gl.runtime.get-user-rpc
gl.data.create-product-rpc
gl.security.validate-token-rpc

# Invalid
get-user-rpc
runtime-rpc
rpc
```

**Purpose**: gRPC and other RPC interface definitions

### 3. GraphQL Interface Naming

**Pattern**: `gl.interface.graphql`

**Format**: `gl.{service}.{schema}-graphql`

**Naming Rules**:
- Must use GraphQL identifier: `-graphql`
- Service identifies the service name
- Schema identifies the GraphQL schema

**Examples**:
```yaml
# Valid
gl.runtime.user-schema-graphql
gl.data.product-schema-graphql
gl.security.auth-schema-graphql

# Invalid
user-schema-graphql
runtime-graphql
graphql
```

**Purpose**: GraphQL schema and interface definitions

### 4. Event Interface Naming

**Pattern**: `gl.interface.event`

**Format**: `gl.{domain}.{event}-event`

**Naming Rules**:
- Must use event identifier: `-event`
- Domain identifies the event domain
- Event identifies the event name

**Examples**:
```yaml
# Valid
gl.runtime.user-created-event
gl.data.product-updated-event
gl.security.auth-failed-event

# Invalid
user-created-event
runtime-event
event
```

**Purpose**: Event-driven interface definitions

### 5. WebSocket Interface Naming

**Pattern**: `gl.interface.websocket`

**Format**: `gl.{service}.{channel}-websocket`

**Naming Rules**:
- Must use WebSocket identifier: `-websocket`
- Service identifies the service name
- Channel identifies the WebSocket channel

**Examples**:
```yaml
# Valid
gl.runtime.notification-websocket
gl.data.realtime-websocket
gl.security.alert-websocket

# Invalid
notification-websocket
runtime-websocket
websocket
```

**Purpose**: WebSocket interface definitions

### 6. Stream Interface Naming

**Pattern**: `gl.interface.stream`

**Format**: `gl.{service}.{topic}-stream`

**Naming Rules**:
- Must use stream identifier: `-stream`
- Service identifies the service name
- Topic identifies the stream topic

**Examples**:
```yaml
# Valid
gl.runtime.data-stream
gl.data.log-stream
gl.security.metric-stream

# Invalid
data-stream
runtime-stream
stream
```

**Purpose**: Streaming interface definitions

### 7. Message Queue Interface Naming

**Pattern**: `gl.interface.queue`

**Format**: `gl.{service}.{type}-queue`

**Naming Rules**:
- Must use queue identifier: `-queue`
- Service identifies the service name
- Type identifies the queue type

**Examples**:
```yaml
# Valid
gl.runtime.task-queue
gl.data.event-queue
gl.security.notification-queue

# Invalid
task-queue
runtime-queue
queue
```

**Purpose**: Message queue interface definitions

### 8. Contract Interface Naming

**Pattern**: `gl.interface.contract`

**Format**: `gl.{service}.{version}-contract`

**Naming Rules**:
- Must use contract identifier: `-contract`
- Service identifies the service name
- Version identifies the contract version

**Examples**:
```yaml
# Valid
gl.runtime.v1-contract
gl.data.v2-contract
gl.security.v1-contract

# Invalid
v1-contract
runtime-contract
contract
```

**Purpose**: Interface contract definitions

### 9. Gateway Interface Naming

**Pattern**: `gl.interface.gateway`

**Format**: `gl.{platform}.{type}-gateway`

**Naming Rules**:
- Must use gateway identifier: `-gateway`
- Platform identifies the platform
- Type identifies the gateway type

**Examples**:
```yaml
# Valid
gl.runtime.api-gateway
gl.data.stream-gateway
gl.security.auth-gateway

# Invalid
api-gateway
runtime-gateway
gateway
```

**Purpose**: API gateway and interface routing

### 10. Interface Layer Integration

### Cross-Layer Dependencies
- **Depends on**: Contract Layer (for interface contracts)
- **Provides**: Interface conventions for communication
- **Works with**: Deployment Layer for interface deployment
- **Works with**: Security Layer for interface security

### Naming Hierarchy
```
gl.interface/
├── http/
│   ├── gl.interface.api
│   └── gl.interface.gateway
├── rpc/
│   └── gl.interface.rpc
├── graphql/
│   └── gl.interface.graphql
├── events/
│   ├── gl.interface.event
│   └── gl.interface.queue
├── realtime/
│   ├── gl.interface.websocket
│   └── gl.interface.stream
└── contracts/
    └── gl.interface.contract
```

### Validation Rules

### Rule IL-001: API Naming Convention
- **Severity**: CRITICAL
- **Check**: APIs must follow `gl.{service}.{resource}-api` pattern
- **Pattern**: `^gl\..+\.api$`

### Rule IL-002: RESTful Verb Usage
- **Severity**: HIGH
- **Check**: API paths must use RESTful conventions
- **Valid Verbs**: GET, POST, PUT, PATCH, DELETE

### Rule IL-003: Schema Versioning
- **Severity**: CRITICAL
- **Check**: GraphQL schemas must be versioned
- **Required**: Version in schema name or URL

### Rule IL-004: Event Naming Format
- **Severity**: HIGH
- **Check**: Events must use past-tense verbs
- **Format**: `{noun}-{verb-past-tense}-event`

### Rule IL-005: Contract Backward Compatibility
- **Severity**: HIGH
- **Check**: Contract changes must maintain backward compatibility
- **Required**: Version bumping and deprecation notice

### Rule IL-006: Interface Security
- **Severity**: CRITICAL
- **Check**: All interfaces must have security defined
- **Required**: Authentication, authorization, rate limiting

### Usage Examples

### Example 1: Complete Interface Stack
```yaml
# REST API
apiVersion: gl.io/v1
kind: API
metadata:
  name: gl.runtime.user-api
spec:
  type: rest
  version: "1.0.0"
  endpoints:
  - path: /api/v1/users
    method: GET
    handler: getUsers
    security:
    - gl.security.oauth-auth
  - path: /api/v1/users
    method: POST
    handler: createUser
    security:
    - gl.security.oauth-auth

# gRPC
apiVersion: gl.io/v1
kind: RPC
metadata:
  name: gl.runtime.get-user-rpc
spec:
  type: grpc
  version: "1.0.0"
  service: UserService
  method: GetUser
  request:
    message: GetUserRequest
    fields:
    - name: user_id
      type: string
  response:
    message: User
    fields:
    - name: id
      type: string
    - name: name
      type: string

# GraphQL
apiVersion: gl.io/v1
kind: GraphQL
metadata:
  name: gl.runtime.user-schema-graphql
spec:
  type: graphql
  version: "1.0.0"
  schema: |
    type User {
      id: ID!
      name: String!
      email: String!
    }
    
    type Query {
      user(id: ID!): User
    }
```

### Example 2: Event Interface
```yaml
apiVersion: gl.io/v1
kind: Event
metadata:
  name: gl.runtime.user-created-event
spec:
  type: event
  domain: gl.runtime
  version: "1.0.0"
  payload:
    type: object
    fields:
    - name: user_id
      type: string
    - name: name
      type: string
    - name: email
      type: string
    - name: created_at
      type: timestamp
  producer: gl.runtime.user-api
  consumers:
  - gl.data.analytics-service
  - gl.notification.email-service
```

### Example 3: WebSocket Interface
```yaml
apiVersion: gl.io/v1
kind: WebSocket
metadata:
  name: gl.runtime.notification-websocket
spec:
  type: websocket
  channel: notifications
  version: "1.0.0"
  authentication:
    required: true
    method: gl.security.jwt-auth
  rateLimiting:
    enabled: true
    maxConnections: 1000
    messagesPerSecond: 10
```

### Best Practices

### Interface Design
```yaml
# RESTful API design
apis:
  - gl.runtime.user-api
    endpoints:
    - GET /api/v1/users
    - POST /api/v1/users
    - GET /api/v1/users/:id
    - PUT /api/v1/users/:id
    - DELETE /api/v1/users/:id

# gRPC design
rpcs:
  - gl.runtime.get-user-rpc
  - gl.runtime.create-user-rpc
  - gl.runtime.update-user-rpc
  - gl.runtime.delete-user-rpc
```

### Event Naming
```yaml
# Standard event naming
events:
  - gl.runtime.user-created-event
  - gl.runtime.user-updated-event
  - gl.runtime.user-deleted-event
  - gl.data.product-created-event
  - gl.security.auth-failed-event
```

### Tool Integration

### API Documentation
```bash
# Generate API documentation
swagger generate spec -o gl.runtime.user-api.json
grpcurl -plaintext localhost:50051 list

# GraphQL introspection
curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name } } }"}'
```

### Interface Testing
```python
# Python API testing
import requests

response = requests.get('http://api.gl.runtime/v1/users')
assert response.status_code == 200
```

### Compliance Checklist

- [x] API naming follows `gl.{service}.{resource}-api` pattern
- [x] RPC naming includes `-rpc` identifier
- [x] GraphQL naming includes `-graphql` identifier
- [x] Event naming includes `-event` identifier
- [x] WebSocket naming includes `-websocket` identifier
- [x] Stream naming includes `-stream` identifier
- [x] Queue naming includes `-queue` identifier
- [x] Contract naming includes `-contract` identifier
- [x] Gateway naming includes `-gateway` identifier
- [x] All interfaces are versioned
- [x] RESTful verbs used correctly
- [x] Events use past-tense verbs
- [x] Contracts maintain backward compatibility
- [x] All interfaces have security defined

### References

- RESTful API Design: https://restfulapi.net/
- gRPC Best Practices: https://grpc.io/docs/guides/
- GraphQL Specification: https://graphql.github.io/graphql-spec/
- WebSocket API: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
- Naming Convention Principles: gl-prefix-principles-engineering.md