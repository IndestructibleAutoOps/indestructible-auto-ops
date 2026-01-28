# @GL-governed
# @GL-layer: GL90-99
# @GL-semantic: documentation
# @GL-audit-trail: ../../engine/governance/GL_SEMANTIC_ANCHOR.json
#
# GL Unified Charter Activated
# Frontend-Backend Separation Architecture Diagrams

> **GL Layer**: GL00-09 Strategic Layer  
> **Purpose**: Visual architecture documentation for frontend-backend separation

## System Architecture Overview

### High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Web[Web Application<br/>React/Vue/Angular]
        Mobile[Mobile App<br/>iOS/Android]
        Desktop[Desktop App<br/>Electron]
    end
    
    subgraph "API Layer"
        Gateway[API Gateway<br/>Authentication<br/>Rate Limiting<br/>Routing]
        LB[Load Balancer]
    end
    
    subgraph "Backend Services"
        API1[API Server 1<br/>Python/Node.js]
        API2[API Server 2<br/>Python/Node.js]
        API3[API Server 3<br/>Python/Node.js]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL<br/>Primary)]
        PG_R1[(PostgreSQL<br/>Replica 1)]
        PG_R2[(PostgreSQL<br/>Replica 2)]
        Redis[(Redis<br/>Cache/Session)]
        Mongo[(MongoDB<br/>Documents)]
        ES[(Elasticsearch<br/>Search)]
    end
    
    Web --> Gateway
    Mobile --> Gateway
    Desktop --> Gateway
    
    Gateway --> LB
    LB --> API1
    LB --> API2
    LB --> API3
    
    API1 --> PG
    API2 --> PG
    API3 --> PG
    
    PG --> PG_R1
    PG --> PG_R2
    
    API1 --> Redis
    API2 --> Redis
    API3 --> Redis
    
    API1 --> Mongo
    API2 --> Mongo
    
    API1 --> ES
    API2 --> ES
    
    style Web fill:#e1f5ff
    style Mobile fill:#e1f5ff
    style Desktop fill:#e1f5ff
    style Gateway fill:#fff4e6
    style API1 fill:#e8f5e9
    style API2 fill:#e8f5e9
    style API3 fill:#e8f5e9
    style PG fill:#f3e5f5
    style Redis fill:#f3e5f5
    style Mongo fill:#f3e5f5
    style ES fill:#f3e5f5
```

### API-First Development Workflow

```mermaid
graph LR
    subgraph "Phase 1: API Design"
        REQ[Requirements<br/>Analysis]
        API_SPEC[OpenAPI<br/>Specification]
        REVIEW[API<br/>Review]
    end
    
    subgraph "Phase 2: Parallel Development"
        FE_DEV[Frontend<br/>Development]
        BE_DEV[Backend<br/>Development]
        MOCK[Mock API<br/>Server]
    end
    
    subgraph "Phase 3: Integration"
        INTEGRATION[API<br/>Integration]
        CONTRACT[Contract<br/>Testing]
        E2E[E2E<br/>Testing]
    end
    
    subgraph "Phase 4: Deployment"
        DEPLOY[Deployment]
        MONITOR[Monitoring]
    end
    
    REQ --> API_SPEC
    API_SPEC --> REVIEW
    REVIEW --> FE_DEV
    REVIEW --> BE_DEV
    
    API_SPEC --> MOCK
    MOCK --> FE_DEV
    
    FE_DEV --> INTEGRATION
    BE_DEV --> INTEGRATION
    
    INTEGRATION --> CONTRACT
    CONTRACT --> E2E
    E2E --> DEPLOY
    DEPLOY --> MONITOR
    
    style REQ fill:#e3f2fd
    style API_SPEC fill:#fff9c4
    style REVIEW fill:#fff9c4
    style FE_DEV fill:#c8e6c9
    style BE_DEV fill:#c8e6c9
    style MOCK fill:#ffccbc
    style INTEGRATION fill:#f8bbd0
    style CONTRACT fill:#f8bbd0
    style E2E fill:#f8bbd0
    style DEPLOY fill:#d1c4e9
    style MONITOR fill:#d1c4e9
```

### Request Flow Sequence

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API Gateway
    participant Backend
    participant Cache
    participant Database
    
    User->>Frontend: Interact with UI
    Frontend->>Frontend: Validate Input
    Frontend->>API Gateway: HTTP Request + JWT
    
    API Gateway->>API Gateway: Validate JWT
    API Gateway->>API Gateway: Rate Limit Check
    API Gateway->>Backend: Forward Request
    
    Backend->>Cache: Check Cache
    
    alt Cache Hit
        Cache-->>Backend: Return Cached Data
        Backend-->>API Gateway: Response
    else Cache Miss
        Backend->>Database: Query Data
        Database-->>Backend: Return Data
        Backend->>Cache: Update Cache
        Backend-->>API Gateway: Response
    end
    
    API Gateway-->>Frontend: HTTP Response (JSON)
    Frontend->>Frontend: Update UI State
    Frontend-->>User: Display Result
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant Auth Service
    participant Database
    participant Redis
    
    User->>Frontend: Enter Credentials
    Frontend->>API: POST /api/v1/auth/login
    API->>Auth Service: Validate Credentials
    Auth Service->>Database: Query User
    Database-->>Auth Service: User Data
    Auth Service->>Auth Service: Verify Password (bcrypt)
    
    alt Authentication Success
        Auth Service->>Auth Service: Generate JWT
        Auth Service->>Redis: Store Session
        Auth Service-->>API: Access + Refresh Tokens
        API-->>Frontend: Return Tokens
        Frontend->>Frontend: Store Tokens (HttpOnly Cookie)
        Frontend-->>User: Redirect to Dashboard
    else Authentication Failure
        Auth Service-->>API: 401 Unauthorized
        API-->>Frontend: Error Response
        Frontend-->>User: Display Error Message
    end
```

### Data Flow Architecture

```mermaid
graph TB
    subgraph "Write Path (CQRS)"
        FE_WRITE[Frontend Write Action]
        API_WRITE[POST/PUT/PATCH/DELETE]
        VALIDATE[Input Validation]
        BIZ_LOGIC[Business Logic]
        PG_PRIMARY[(PostgreSQL Primary)]
    end
    
    subgraph "Read Path (CQRS)"
        FE_READ[Frontend Read Action]
        API_READ[GET Request]
        CACHE_CHECK{Cache Available?}
        REDIS[(Redis Cache)]
        PG_REPLICA[(PostgreSQL Replica)]
    end
    
    FE_WRITE --> API_WRITE
    API_WRITE --> VALIDATE
    VALIDATE --> BIZ_LOGIC
    BIZ_LOGIC --> PG_PRIMARY
    
    FE_READ --> API_READ
    API_READ --> CACHE_CHECK
    CACHE_CHECK -->|Yes| REDIS
    REDIS --> FE_READ
    CACHE_CHECK -->|No| PG_REPLICA
    PG_REPLICA --> REDIS
    PG_REPLICA --> FE_READ
    
    PG_PRIMARY -.Replication.-> PG_REPLICA
    
    style FE_WRITE fill:#ffebee
    style API_WRITE fill:#ffebee
    style VALIDATE fill:#ffebee
    style BIZ_LOGIC fill:#ffebee
    style PG_PRIMARY fill:#ffebee
    
    style FE_READ fill:#e8f5e9
    style API_READ fill:#e8f5e9
    style CACHE_CHECK fill:#e8f5e9
    style REDIS fill:#e8f5e9
    style PG_REPLICA fill:#e8f5e9
```

### Deployment Architecture

```mermaid
graph TB
    subgraph "Frontend Deployment"
        FE_BUILD[npm run build]
        FE_ASSETS[Static Assets<br/>HTML/CSS/JS]
        CDN[CDN<br/>CloudFront/Netlify]
        S3[S3 Bucket]
    end
    
    subgraph "Backend Deployment"
        BE_BUILD[Docker Build]
        BE_IMAGE[Container Image]
        ECR[Container Registry<br/>ECR/DockerHub]
        K8S[Kubernetes Cluster]
        POD1[Pod 1]
        POD2[Pod 2]
        POD3[Pod 3]
    end
    
    subgraph "Database Deployment"
        RDS[Amazon RDS<br/>PostgreSQL]
        RDS_R1[Read Replica 1]
        RDS_R2[Read Replica 2]
        ELASTICACHE[ElastiCache<br/>Redis]
    end
    
    FE_BUILD --> FE_ASSETS
    FE_ASSETS --> S3
    S3 --> CDN
    
    BE_BUILD --> BE_IMAGE
    BE_IMAGE --> ECR
    ECR --> K8S
    K8S --> POD1
    K8S --> POD2
    K8S --> POD3
    
    POD1 --> RDS
    POD2 --> RDS
    POD3 --> RDS
    
    RDS --> RDS_R1
    RDS --> RDS_R2
    
    POD1 --> ELASTICACHE
    POD2 --> ELASTICACHE
    POD3 --> ELASTICACHE
    
    style FE_BUILD fill:#e1f5ff
    style CDN fill:#e1f5ff
    style BE_BUILD fill:#e8f5e9
    style K8S fill:#e8f5e9
    style RDS fill:#f3e5f5
```

### Technology Stack

```mermaid
graph LR
    subgraph "Frontend Stack"
        FE_LANG[TypeScript]
        FE_FRAMEWORK[React/Vue/Angular]
        FE_STATE[Redux/Vuex/Pinia]
        FE_STYLE[Tailwind CSS]
        FE_BUILD[Vite/Webpack]
    end
    
    subgraph "Backend Stack"
        BE_LANG[Python/Node.js]
        BE_FRAMEWORK[FastAPI/NestJS]
        BE_ORM[SQLAlchemy/TypeORM]
        BE_VALIDATION[Pydantic/class-validator]
    end
    
    subgraph "API Layer"
        API_SPEC[OpenAPI 3.0]
        API_AUTH[JWT/OAuth2]
        API_DOCS[Swagger UI]
    end
    
    subgraph "Database"
        DB_RELATIONAL[PostgreSQL 15+]
        DB_CACHE[Redis 7+]
        DB_DOC[MongoDB 7+]
        DB_SEARCH[Elasticsearch 8+]
    end
    
    subgraph "DevOps"
        CI_CD[GitHub Actions]
        CONTAINER[Docker]
        ORCHESTRATION[Kubernetes]
        MONITORING[Prometheus + Grafana]
    end
    
    FE_FRAMEWORK --> API_SPEC
    BE_FRAMEWORK --> API_SPEC
    BE_ORM --> DB_RELATIONAL
    BE_FRAMEWORK --> DB_CACHE
    
    style FE_LANG fill:#61dafb
    style BE_LANG fill:#3776ab
    style DB_RELATIONAL fill:#336791
    style API_SPEC fill:#85ea2d
```

### Security Architecture

```mermaid
graph TB
    subgraph "Client Security"
        HTTPS[HTTPS/TLS]
        CSP[Content Security Policy]
        CORS_CLIENT[CORS Configuration]
    end
    
    subgraph "API Gateway Security"
        WAF[Web Application Firewall]
        RATE_LIMIT[Rate Limiting]
        JWT_VALIDATE[JWT Validation]
        API_KEY[API Key Management]
    end
    
    subgraph "Backend Security"
        INPUT_VAL[Input Validation]
        SQL_INJ[SQL Injection Prevention]
        XSS_PREVENT[XSS Prevention]
        AUTH_AUTHZ[Authentication & Authorization]
    end
    
    subgraph "Data Security"
        ENCRYPT_TRANSIT[Encryption in Transit<br/>TLS 1.2+]
        ENCRYPT_REST[Encryption at Rest<br/>AES-256]
        DATA_MASK[Data Masking]
        AUDIT_LOG[Audit Logging]
    end
    
    HTTPS --> WAF
    CSP --> WAF
    WAF --> RATE_LIMIT
    RATE_LIMIT --> JWT_VALIDATE
    JWT_VALIDATE --> AUTH_AUTHZ
    
    AUTH_AUTHZ --> INPUT_VAL
    INPUT_VAL --> SQL_INJ
    INPUT_VAL --> XSS_PREVENT
    
    SQL_INJ --> ENCRYPT_TRANSIT
    XSS_PREVENT --> ENCRYPT_TRANSIT
    ENCRYPT_TRANSIT --> ENCRYPT_REST
    ENCRYPT_REST --> AUDIT_LOG
    
    style HTTPS fill:#c8e6c9
    style WAF fill:#ffccbc
    style INPUT_VAL fill:#fff9c4
    style ENCRYPT_REST fill:#f8bbd0
```

### Monitoring and Observability

```mermaid
graph TB
    subgraph "Frontend Monitoring"
        FE_METRICS[Core Web Vitals<br/>LCP, FID, CLS]
        FE_ERROR[Error Tracking<br/>Sentry]
        FE_ANALYTICS[User Analytics<br/>Google Analytics]
    end
    
    subgraph "Backend Monitoring"
        BE_METRICS[API Metrics<br/>Latency, Throughput]
        BE_LOGS[Structured Logging<br/>ELK Stack]
        BE_TRACES[Distributed Tracing<br/>Jaeger/Zipkin]
    end
    
    subgraph "Database Monitoring"
        DB_METRICS[Database Metrics<br/>Connections, Queries]
        DB_SLOW[Slow Query Log]
        DB_REPL[Replication Lag]
    end
    
    subgraph "Aggregation & Visualization"
        PROMETHEUS[Prometheus]
        GRAFANA[Grafana Dashboards]
        ALERTS[Alert Manager<br/>PagerDuty/Slack]
    end
    
    FE_METRICS --> PROMETHEUS
    FE_ERROR --> PROMETHEUS
    BE_METRICS --> PROMETHEUS
    BE_LOGS --> PROMETHEUS
    DB_METRICS --> PROMETHEUS
    
    PROMETHEUS --> GRAFANA
    PROMETHEUS --> ALERTS
    
    style FE_METRICS fill:#e1f5ff
    style BE_METRICS fill:#e8f5e9
    style DB_METRICS fill:#f3e5f5
    style GRAFANA fill:#fff4e6
    style ALERTS fill:#ffebee
```

## Component Interaction Patterns

### RESTful API Design Pattern

```mermaid
graph LR
    A[GET /api/v1/users] --> B[List Users]
    C[GET /api/v1/users/:id] --> D[Get User]
    E[POST /api/v1/users] --> F[Create User]
    G[PUT /api/v1/users/:id] --> H[Update User]
    I[PATCH /api/v1/users/:id] --> J[Partial Update]
    K[DELETE /api/v1/users/:id] --> L[Delete User]
    
    style A fill:#c8e6c9
    style C fill:#c8e6c9
    style E fill:#ffccbc
    style G fill:#fff9c4
    style I fill:#fff9c4
    style K fill:#ffebee
```

### Error Handling Flow

```mermaid
graph TB
    REQUEST[API Request]
    VALIDATE{Input Valid?}
    AUTH{Authenticated?}
    AUTHZ{Authorized?}
    BUSINESS{Business Logic OK?}
    SUCCESS[200 OK]
    
    ERROR_400[400 Bad Request<br/>Validation Error]
    ERROR_401[401 Unauthorized<br/>Auth Failed]
    ERROR_403[403 Forbidden<br/>No Permission]
    ERROR_422[422 Unprocessable<br/>Business Error]
    ERROR_500[500 Server Error<br/>Internal Error]
    
    REQUEST --> VALIDATE
    VALIDATE -->|No| ERROR_400
    VALIDATE -->|Yes| AUTH
    AUTH -->|No| ERROR_401
    AUTH -->|Yes| AUTHZ
    AUTHZ -->|No| ERROR_403
    AUTHZ -->|Yes| BUSINESS
    BUSINESS -->|Error| ERROR_422
    BUSINESS -->|Exception| ERROR_500
    BUSINESS -->|Success| SUCCESS
    
    style SUCCESS fill:#c8e6c9
    style ERROR_400 fill:#ffebee
    style ERROR_401 fill:#ffebee
    style ERROR_403 fill:#ffebee
    style ERROR_422 fill:#fff9c4
    style ERROR_500 fill:#ffccbc
```

---

## References

- **Frontend-Backend Separation Architecture**: `gl/00-strategic/artifacts/frontend-backend-separation-architecture.yaml`
- **API Design Specification**: `gl/30-execution/artifacts/api-design-specification.yaml`
- **Database Architecture Specification**: `gl/20-data/artifacts/database-architecture-specification.yaml`

---

**Last Updated**: 2026-01-27  
**Maintained by**: Architecture Team
