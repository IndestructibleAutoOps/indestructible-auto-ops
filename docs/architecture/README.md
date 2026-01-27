# Frontend-Backend Separation Architecture Guide

> **GL Layers**: GL00-09 (Strategic), GL20-29 (Data), GL30-49 (Execution)  
> **Status**: Active  
> **Last Updated**: 2026-01-27

## 📋 Overview

This guide provides comprehensive documentation for the **frontend-backend separation architecture** implemented in the MachineNativeOps project. The architecture follows an **API-first design** approach with **parallel development** of frontend and backend teams.

### Key Principles

1. **前後端分離 (Frontend-Backend Separation)** - Clear separation of concerns
2. **API優先設計 (API-First Design)** - API specification as the core contract
3. **並行開發 (Parallel Development)** - Simultaneous frontend and backend development
4. **獨立部署 (Independent Deployment)** - Separate deployment pipelines

## 🗂️ Documentation Structure

This architecture is documented across three GL (Governance Layers):

### GL00-09: Strategic Layer
**File**: [`gl/00-strategic/artifacts/frontend-backend-separation-architecture.yaml`](../gl/00-strategic/artifacts/frontend-backend-separation-architecture.yaml)

**Content**:
- ✅ Architecture principles (5 core principles)
- ✅ System boundaries (Frontend, Backend, API Layer)
- ✅ Communication patterns (RESTful, GraphQL, WebSocket)
- ✅ Development workflow (4-phase parallel development)
- ✅ Quality assurance strategy
- ✅ Deployment architecture
- ✅ API versioning strategy
- ✅ Security considerations
- ✅ Monitoring and observability
- ✅ Success metrics

### GL30-49: Execution Layer
**File**: [`gl/30-execution/artifacts/api-design-specification.yaml`](../gl/30-execution/artifacts/api-design-specification.yaml)

**Content**:
- ✅ API design principles (5 core principles)
- ✅ URL structure and naming conventions
- ✅ HTTP methods (GET, POST, PUT, PATCH, DELETE)
- ✅ Request/response formats (JSON schema)
- ✅ Authentication & authorization (JWT, OAuth2, RBAC)
- ✅ HTTP status codes (2xx, 4xx, 5xx)
- ✅ Error handling (comprehensive error codes)
- ✅ Rate limiting (token bucket algorithm)
- ✅ Caching strategies (ETags, Cache-Control)
- ✅ Pagination (offset-based and cursor-based)
- ✅ API documentation (OpenAPI 3.0 template)
- ✅ Testing (contract, integration, load testing)
- ✅ Monitoring & logging
- ✅ Deprecation policy

### GL20-29: Data Layer
**File**: [`gl/20-data/artifacts/database-architecture-specification.yaml`](../gl/20-data/artifacts/database-architecture-specification.yaml)

**Content**:
- ✅ Database strategy (polyglot persistence)
- ✅ Database types (PostgreSQL, MongoDB, Redis, Elasticsearch)
- ✅ Data models (User, Session entities with schemas)
- ✅ Data access patterns (CQRS, caching, sharding)
- ✅ Schema management (versioned migrations)
- ✅ Data governance (classification, retention, privacy)
- ✅ Backup and disaster recovery
- ✅ Performance optimization
- ✅ Monitoring and alerting
- ✅ Security (encryption, authentication, authorization)

### Architecture Diagrams
**File**: [`docs/architecture/frontend-backend-separation-diagrams.md`](frontend-backend-separation-diagrams.md)

**Content**:
- 🎨 High-level architecture diagram
- 🎨 API-first development workflow
- 🎨 Request flow sequence diagram
- 🎨 Authentication flow diagram
- 🎨 Data flow architecture (CQRS)
- 🎨 Deployment architecture
- 🎨 Technology stack diagram
- 🎨 Security architecture
- 🎨 Monitoring and observability
- 🎨 RESTful API design patterns
- 🎨 Error handling flow

## 🚀 Quick Start

### For Frontend Developers

1. **Read the API Specification**
   ```bash
   # View the API design specification
   cat gl/30-execution/artifacts/api-design-specification.yaml
   ```

2. **Set Up Mock API Server**
   ```bash
   # Install Prism (OpenAPI Mock Server)
   npm install -g @stoplight/prism-cli
   
   # Start mock server (create openapi.yaml first from template)
   prism mock openapi.yaml
   ```

3. **Develop Frontend**
   ```bash
   # Example: React application
   npx create-react-app my-app --template typescript
   cd my-app
   npm install axios
   
   # Configure API base URL
   echo "REACT_APP_API_URL=http://localhost:4010/api/v1" > .env.local
   ```

### For Backend Developers

1. **Read the API Specification**
   ```bash
   # View the API design specification
   cat gl/30-execution/artifacts/api-design-specification.yaml
   ```

2. **Set Up Backend Project**
   ```bash
   # Example: Python FastAPI
   mkdir backend && cd backend
   python -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn sqlalchemy pydantic
   ```

3. **Implement API Endpoints**
   ```python
   # main.py
   from fastapi import FastAPI
   
   app = FastAPI(
       title="MachineNativeOps API",
       version="1.0.0",
       openapi_url="/api/v1/openapi.json"
   )
   
   @app.get("/api/v1/users")
   def list_users():
       return {"data": [], "meta": {"total": 0}}
   ```

### For Database Administrators

1. **Review Database Architecture**
   ```bash
   # View the database specification
   cat gl/20-data/artifacts/database-architecture-specification.yaml
   ```

2. **Set Up Databases**
   ```bash
   # Using Docker Compose
   docker-compose up -d postgres redis mongodb elasticsearch
   ```

3. **Run Migrations**
   ```bash
   # Python/Alembic
   alembic upgrade head
   
   # Node.js/TypeORM
   npm run migration:run
   ```

## 📐 Development Workflow

### Phase 1: API Specification (1-2 weeks)

```mermaid
graph LR
    A[Requirements Analysis] --> B[API Design]
    B --> C[OpenAPI Specification]
    C --> D[Review & Approval]
    D --> E[Generate Mock Server]
```

**Deliverables**:
- ✅ OpenAPI 3.0 specification
- ✅ API design document
- ✅ Data model definitions

### Phase 2: Parallel Development (4-8 weeks)

**Frontend Team**:
- Develop UI components
- Implement state management
- Connect to Mock API
- Write unit tests

**Backend Team**:
- Implement business logic
- Set up database schema
- Implement API endpoints
- Write unit tests

**Collaboration**:
- Weekly sync meetings
- Shared API specification updates
- Common mock data

### Phase 3: Integration Testing (1-2 weeks)

```mermaid
graph LR
    A[Frontend + Backend] --> B[Contract Testing]
    B --> C[E2E Testing]
    C --> D[Performance Testing]
    D --> E[Security Testing]
```

### Phase 4: Deployment & Monitoring (Ongoing)

- CI/CD pipeline setup
- Environment deployment (Dev → Staging → Production)
- Monitoring and logging configuration
- Error tracking setup

## 🔧 Tools & Technologies

### Frontend
- **Framework**: React / Vue.js / Angular
- **Language**: TypeScript
- **State Management**: Redux / Vuex / Pinia
- **Testing**: Jest, Testing Library, Cypress
- **Build Tool**: Vite / Webpack

### Backend
- **Language**: Python 3.11+ / Node.js 18+
- **Framework**: FastAPI / NestJS / Express
- **ORM**: SQLAlchemy / TypeORM
- **Testing**: pytest / Jest
- **API Documentation**: Swagger UI / ReDoc

### Database
- **Relational**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Document**: MongoDB 7+
- **Search**: Elasticsearch 8+

### DevOps
- **CI/CD**: GitHub Actions
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Monitoring**: Prometheus + Grafana
- **Error Tracking**: Sentry

## 📊 API Example

### Request
```http
POST /api/v1/users HTTP/1.1
Host: api.machinenativeops.io
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user"
}
```

### Response (Success)
```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/users/123e4567-e89b-12d3-a456-426614174000

{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "status": "active",
    "emailVerified": false,
    "createdAt": "2026-01-27T10:00:00Z",
    "updatedAt": "2026-01-27T10:00:00Z"
  }
}
```

### Response (Error)
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Email already exists",
        "code": "DUPLICATE"
      }
    ],
    "requestId": "req-uuid-123",
    "timestamp": "2026-01-27T10:00:00Z"
  }
}
```

## 🔐 Security Best Practices

1. **Authentication**
   - Use JWT for API authentication
   - Store tokens in HttpOnly cookies
   - Implement refresh token rotation

2. **Authorization**
   - Implement RBAC (Role-Based Access Control)
   - Check permissions at API Gateway level
   - Enforce resource-level permissions

3. **Data Protection**
   - Always use HTTPS/TLS
   - Encrypt sensitive data at rest (AES-256)
   - Implement input validation and sanitization
   - Use parameterized queries to prevent SQL injection

4. **API Security**
   - Implement rate limiting
   - Configure CORS properly
   - Add security headers (HSTS, CSP, X-Frame-Options)
   - Monitor for suspicious activities

## 📈 Monitoring & Observability

### Frontend Metrics
- Page Load Time
- Core Web Vitals (LCP, FID, CLS)
- Error rate
- User engagement

### Backend Metrics
- API response time (p50, p95, p99)
- Error rate by endpoint
- Throughput (requests/second)
- Resource utilization (CPU, Memory)

### Database Metrics
- Connection pool utilization
- Query performance
- Replication lag
- Disk usage

## 🧪 Testing Strategy

### Frontend Testing
- **Unit Tests**: Jest + Testing Library (>80% coverage)
- **Component Tests**: Storybook
- **E2E Tests**: Cypress / Playwright

### Backend Testing
- **Unit Tests**: pytest / Jest (>80% coverage)
- **Integration Tests**: All API endpoints
- **Contract Tests**: Pact (100% API coverage)

### Database Testing
- **Migration Tests**: Test up and down migrations
- **Performance Tests**: Query performance benchmarks
- **Data Integrity Tests**: Constraint validation

## 📚 References

### Internal Documentation
- [Frontend-Backend Separation Architecture](../gl/00-strategic/artifacts/frontend-backend-separation-architecture.yaml)
- [API Design Specification](../gl/30-execution/artifacts/api-design-specification.yaml)
- [Database Architecture Specification](../gl/20-data/artifacts/database-architecture-specification.yaml)
- [Architecture Diagrams](frontend-backend-separation-diagrams.md)

### External Standards
- [OpenAPI Specification 3.0](https://swagger.io/specification/)
- [RESTful API Design Best Practices](https://restfulapi.net/)
- [12-Factor App](https://12factor.net/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

### Tools Documentation
- [OpenAPI Generator](https://openapi-generator.tech/)
- [Pact Contract Testing](https://docs.pact.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [NestJS Documentation](https://docs.nestjs.com/)

## 🤝 Contributing

When contributing to this architecture:

1. Follow the GL governance structure
2. Update relevant YAML specifications
3. Add/update Mermaid diagrams as needed
4. Ensure YAML validation passes
5. Update this README if adding new sections

## 📝 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-27 | Architecture Team | Initial frontend-backend separation architecture |

---

**Maintained by**: MachineNativeOps Architecture Team  
**Contact**: architecture-team@machinenativeops.io
