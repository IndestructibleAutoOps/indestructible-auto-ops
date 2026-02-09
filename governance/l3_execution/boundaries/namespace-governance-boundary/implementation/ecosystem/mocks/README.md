# Mock Services

This directory contains mock services for local development and testing.

## Structure

```
mocks/
├── api/           # Mock API responses
├── data/          # Fake data generators
└── services/      # Mock service implementations
```

## Usage

Mock services are automatically loaded when `DEV_MOCK_EXTERNAL_SERVICES=true`
is set in `.env`.

## GL Layer

- **GL Layer**: GL30-49 (Execution Layer)
- **Purpose**: Development and testing support

## Quick Start

```python
from ecosystem.mocks.services.mock_service import get_mock_service

# Get mock service instance
service = get_mock_service()

# Check health
health = service.get_health()
print(health)

# Simulate API response
response = service.simulate_response("/api/v1/users", "GET")
print(response)
```

## Configuration

Set the following environment variables to control mock behavior:

```bash
# Enable mock services
DEV_MOCK_EXTERNAL_SERVICES=true

# Mock data directory (optional)
MOCK_DATA_DIR=/path/to/mock/data
```
