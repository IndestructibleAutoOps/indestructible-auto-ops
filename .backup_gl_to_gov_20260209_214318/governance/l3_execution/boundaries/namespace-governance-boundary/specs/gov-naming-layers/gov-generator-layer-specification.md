# GL Generator Layer Specification

## Layer Overview

The GL Generator Layer defines naming conventions for code generators, scaffolding tools, template systems, and automation tools in a large-scale monorepo multi-platform architecture. This layer is critical for enabling consistent code generation, reducing boilerplate, and accelerating development.

**Layer ID**: L24-Generator  
**Priority**: LOW  
**Scope**: Code generators, scaffolding, templates, and automation

---

## Resource Naming Patterns

### 1. Code Generators

**Pattern**: `gl.gen.generator-{language/framework}-{scope}-{version}`

**Examples**:
- `gl.gen.generator-python-service-1.0.0` - Python service generator
- `gl.gen.generator-react-component-2.0.0` - React component generator
- `gl.gen.generator-go-grpc-1.0.0` - Go gRPC generator

**Validation**:
- Language/framework must be valid
- Scope must be clear (service, component, library, etc.)
- Version must follow semantic versioning
- Must include input/output schema

### 2. Scaffolding Tools

**Pattern**: `gl.gen.scaffold-{type}-{template}-{version}`

**Examples**:
- `gl.gen.scaffold-project-microservice-1.0.0` - Microservice project scaffold
- `gl.gen.scaffold-module-api-2.0.0` - API module scaffold
- `gl.gen.scaffold-package-library-1.0.0` - Library package scaffold

**Validation**:
- Type must be valid (project, module, package, etc.)
- Template must be descriptive
- Version must follow semantic versioning
- Must include structure definition

### 3. Template Definitions

**Pattern**: `gl.gen.template-{category}-{name}-{version}`

**Examples**:
- `gl.gen.template-service-rest-1.0.0` - REST service template
- `gl.gen.template-component-ui-2.0.0` - UI component template
- `gl.gen.template-script-cron-1.0.0` - Cron script template

**Validation**:
- Category must be valid (service, component, script, etc.)
- Name must be descriptive
- Version must follow semantic versioning
- Must include placeholder definitions

### 4. Boilerplate Generators

**Pattern**: `gl.gen.boilerplate-{framework}-{feature}-{version}`

**Examples**:
- `gl.gen.boilerplate-spring-boot-auth-1.0.0` - Spring Boot auth boilerplate
- `gl.gen.boilerplate-next-js-api-2.0.0` - Next.js API boilerplate
- `gl.gen.boilerplate-django-admin-1.0.0` - Django admin boilerplate

**Validation**:
- Framework must be valid
- Feature must be clear
- Version must follow semantic versioning
- Must be customizable

### 5. Code Templates

**Pattern**: `gl.gen.code-{language}-{pattern}-{version}`

**Examples**:
- `gl.gen.code-python-factory-1.0.0` - Python factory pattern template
- `gl.gen.code-typescript-repository-2.0.0` - TypeScript repository pattern template
- `gl.gen.code-java-strategy-1.0.0` - Java strategy pattern template

**Validation**:
- Language must be valid
- Pattern must be standard (factory, repository, strategy, etc.)
- Version must follow semantic versioning
- Must include documentation

### 6. Configuration Generators

**Pattern**: `gl.gen.config-{type}-{platform}-{version}`

**Examples**:
- `gl.gen.config-docker-compose-development-1.0.0` - Docker Compose config generator
- `gl.gen.config-kubernetes-production-2.0.0` - Kubernetes config generator
- `gl.gen.config-terraform-aws-1.0.0` - Terraform AWS config generator

**Validation**:
- Type must be valid (docker-compose, kubernetes, terraform, etc.)
- Platform must be valid
- Version must follow semantic versioning
- Must include validation schema

### 7. API Generators

**Pattern**: `gl.gen.api-{protocol}-{style}-{version}`

**Examples**:
- `gl.gen.api-rest-openapi-1.0.0` - REST OpenAPI generator
- `gl.gen.api-grpc-proto-2.0.0` - gRPC Protobuf generator
- `gl.gen.api-graphql-schema-1.0.0` - GraphQL schema generator

**Validation**:
- Protocol must be valid (rest, grpc, graphql, etc.)
- Style must be valid (openapi, proto, schema, etc.)
- Version must follow semantic versioning
- Must generate client/server code

### 8. Database Generators

**Pattern**: `gl.gen.database-{type}-{schema}-{version}`

**Examples**:
- `gl.gen.database-sql-migration-1.0.0` - SQL migration generator
- `gl.gen.database-nosql-collection-2.0.0` - NoSQL collection generator
- `gl.gen.database-orm-entity-1.0.0` - ORM entity generator

**Validation**:
- Type must be valid (sql, nosql, orm, etc.)
- Schema must be clear
- Version must follow semantic versioning
- Must support migrations

### 9. Test Generators

**Pattern**: `gl.gen.test-{framework}-{scope}-{version}`

**Examples**:
- `gl.gen.test-jest-unit-1.0.0` - Jest unit test generator
- `gl.gen.test-pytest-integration-2.0.0` - Pytest integration test generator
- `gl.gen.test-cypress-e2e-1.0.0` - Cypress E2E test generator

**Validation**:
- Framework must be valid
- Scope must be valid (unit, integration, e2e)
- Version must follow semantic versioning
- Must include assertions

### 10. Documentation Generators

**Pattern**: `gl.gen.doc-{format}-{type}-{version}`

**Examples**:
- `gl.gen.doc-markdown-api-1.0.0` - Markdown API documentation generator
- `gl.gen.doc-openapi-spec-2.0.0` - OpenAPI specification generator
- `gl.gen.doc-swagger-ui-1.0.0` - Swagger UI generator

**Validation**:
- Format must be valid (markdown, openapi, swagger, etc.)
- Type must be clear
- Version must follow semantic versioning
- Must be readable

---

## Validation Rules

### GL-GEN-001: Generator Interface
**Severity**: HIGH  
**Rule**: All generators must have well-defined interfaces  
**Implementation**:
```yaml
generator_interface:
  name: gl.gen.generator-python-service-1.0.0
  input:
    type: object
    properties:
      service_name: string
      features: array
  output:
    type: directory
    structure: defined_template
  configuration: generator_config.yaml
```

### GL-GEN-002: Template Validation
**Severity**: MEDIUM  
**Rule**: All templates must be validated before use  
**Implementation**:
- Validate syntax
- Check placeholder completeness
- Verify template compatibility
- Test template rendering

### GL-GEN-003: Generated Code Quality
**Severity**: HIGH  
**Rule**: Generated code must meet quality standards  
**Implementation**:
```yaml
quality_standards:
  linting: must_pass_linter
  formatting: must_be_formatted
  documentation: must_include_comments
  testing: must_include_tests
  security: must_be_scanned
```

### GL-GEN-004: Generator Configuration
**Severity**: MEDIUM  
**Rule**: Generators must be configurable and extensible  
**Implementation**:
- Support configuration files
- Allow custom templates
- Enable plugin extensions
- Provide configuration validation

### GL-GEN-005: Output Consistency
**Severity**: HIGH  
**Rule**: Generators must produce consistent output  
**Implementation**:
- Deterministic generation
- Version-controlled templates
- Idempotent operations
- Output validation

### GL-GEN-006: Generator Documentation
**Severity**: MEDIUM  
**Rule**: All generators must be documented  
**Implementation**:
- Usage instructions
- Configuration options
- Input/output examples
- Troubleshooting guide

### GL-GEN-007: Template Security
**Severity**: CRITICAL  
**Rule**: Templates must be secure and sandboxed  
**Implementation**:
- Validate user input
- Sanitize template variables
- Prevent code injection
- Use secure rendering

---

## Usage Examples

### Complete Generator Stack
```yaml
generators/
  code-generators/
    gl.gen.generator-python-service-1.0.0/
      generator.yaml
      templates/
      configs/
    gl.gen.generator-react-component-2.0.0/
      generator.yaml
      templates/
      configs/
  scaffolding/
    gl.gen.scaffold-project-microservice-1.0.0/
      scaffold.yaml
      templates/
    gl.gen.scaffold-module-api-2.0.0/
      scaffold.yaml
      templates/
  templates/
    gl.gen.template-service-rest-1.0.0/
      template.yaml
      files/
    gl.gen.template-component-ui-2.0.0/
      template.yaml
      files/
  boilerplate/
    gl.gen.boilerplate-spring-boot-auth-1.0.0/
      boilerplate.yaml
      src/
    gl.gen.boilerplate-next-js-api-2.0.0/
      boilerplate.yaml
      src/
  code-templates/
    gl.gen.code-python-factory-1.0.0.py
    gl.gen.code-typescript-repository-2.0.0.ts
  config-generators/
    gl.gen.config-docker-compose-development-1.0.0/
      generator.yaml
      templates/
    gl.gen.config-kubernetes-production-2.0.0/
      generator.yaml
      templates/
  api-generators/
    gl.gen.api-rest-openapi-1.0.0/
      generator.yaml
      templates/
    gl.gen.api-grpc-proto-2.0.0/
      generator.yaml
      templates/
  database-generators/
    gl.gen.database-sql-migration-1.0.0/
      generator.yaml
      templates/
    gl.gen.database-nosql-collection-2.0.0/
      generator.yaml
      templates/
  test-generators/
    gl.gen.test-jest-unit-1.0.0/
      generator.yaml
      templates/
    gl.gen.test-pytest-integration-2.0.0/
      generator.yaml
      templates/
  doc-generators/
    gl.gen.doc-markdown-api-1.0.0/
      generator.yaml
      templates/
    gl.gen.doc-openapi-spec-2.0.0/
      generator.yaml
      templates/
```

### Generator Definition
```yaml
# gl.gen.generator-python-service-1.0.0/generator.yaml
generator:
  id: gl.gen.generator-python-service-1.0.0
  name: Python Service Generator
  version: 1.0.0
  language: python
  
  input:
    type: object
    properties:
      service_name:
        type: string
        required: true
        pattern: "^[a-z][a-z0-9-]*$"
      features:
        type: array
        items:
          type: string
          enum: [api, database, cache, auth, logging, monitoring]
      framework:
        type: string
        enum: [fastapi, flask, django]
        default: fastapi
  
  output:
    type: directory
    structure:
      - src/
      - tests/
      - configs/
      - docs/
      - requirements.txt
      - Dockerfile
      - README.md
  
  templates:
    - service_main.py.j2
    - models.py.j2
    - api.py.j2
    - tests.py.j2
    - requirements.txt.j2
    - Dockerfile.j2
    - README.md.j2
  
  configuration:
    file: generator_config.yaml
    schema: config_schema.yaml
  
  post_generation:
    - format_code
    - install_dependencies
    - initialize_git
    - run_tests
```

### Template Definition
```yaml
# gl.gen.template-service-rest-1.0.0/template.yaml
template:
  id: gl.gen.template-service-rest-1.0.0
  name: REST Service Template
  version: 1.0.0
  category: service
  
  placeholders:
    service_name:
      type: string
      required: true
      description: Name of the service
    port:
      type: integer
      default: 8080
      description: Service port
    base_path:
      type: string
      default: "/api/v1"
      description: API base path
  
  files:
    - path: src/main.py
      template: main.py.j2
    - path: src/models.py
      template: models.py.j2
    - path: src/routes.py
      template: routes.py.j2
    - path: tests/test_api.py
      template: test_api.py.j2
    - path: README.md
      template: README.md.j2
  
  dependencies:
    - fastapi: "^0.104.0"
    - uvicorn: "^0.24.0"
    - pydantic: "^2.5.0"
  
  validation:
    - check_syntax
    - check_imports
    - lint_code
```

---

## Best Practices

### 1. Template Design
- Keep templates simple and readable
- Use standard template engines
- Document all placeholders
- Provide example outputs

### 2. Generator Usability
- Provide clear error messages
- Support interactive mode
- Include help documentation
- Validate inputs before generation

### 3. Code Quality
- Generate clean, idiomatic code
- Include comments and documentation
- Follow language-specific conventions
- Enable code formatting

### 4. Extensibility
- Support custom templates
- Allow plugin extensions
- Provide hooks for customization
- Enable configuration overrides

### 5. Testing
- Test generator output
- Validate generated code
- Include sample projects
- Document edge cases

---

## Tool Integration Examples

### Using Code Generator
```python
# Generate Python service
from gl.generator import GLCodeGenerator

generator = GLCodeGenerator('gl.gen.generator-python-service-1.0.0')

# Generate service
output = generator.generate(
    service_name='user-service',
    features=['api', 'database', 'auth'],
    framework='fastapi',
    output_dir='./generated/user-service'
)

# Output: generated/user-service/
#   ├── src/
#   ├── tests/
#   ├── configs/
#   ├── docs/
#   ├── requirements.txt
#   ├── Dockerfile
#   └── README.md
```

### Using Scaffolding Tool
```bash
# Scaffold new project
gov-scaffold \
  --template gl.gen.scaffold-project-microservice-1.0.0 \
  --name my-service \
  --type rest \
  --language python \
  --output ./my-service

# Or interactive mode
gov-scaffold interactive
```

### Generating API Code
```bash
# Generate REST API from OpenAPI spec
gov-gen-api \
  --generator gl.gen.api-rest-openapi-1.0.0 \
  --spec openapi.yaml \
  --output ./generated/api \
  --language python \
  --framework fastapi
```

### Generating Database Migrations
```python
# Generate SQL migration
from gl.generator import GLDatabaseGenerator

db_gen = GLDatabaseGenerator('gl.gen.database-sql-migration-1.0.0')

# Create migration
migration = db_gen.generate_migration(
    name='add_users_table',
    tables=[
        {
            'name': 'users',
            'columns': [
                {'name': 'id', 'type': 'SERIAL', 'primary_key': True},
                {'name': 'username', 'type': 'VARCHAR(255)', 'unique': True},
                {'name': 'email', 'type': 'VARCHAR(255)', 'unique': True},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'default': 'NOW()'}
            ]
        }
    ],
    output_dir='./migrations'
)
```

---

## Compliance Checklist

For each generator resource, verify:

- [ ] File name follows GL naming convention
- [ ] Generator interface defined
- [ ] Templates validated
- [ ] Output meets quality standards
- [ ] Documentation complete
- [ ] Configuration supported
- [ ] Security enforced
- [ ] Testing included
- [ ] Examples provided
- [ ] Version controlled

---

## References

- Yeoman Generators: https://yeoman.io/
- Cookiecutter: https://cookiecutter.readthedocs.io/
- Plop.js: https://plopjs.com/
- OpenAPI Generator: https://openapi-generator.tech/
- Hygen: https://www.hygen.io/

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-20  
**Maintained By**: Developer Experience Team