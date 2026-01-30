@GL-governed
# CLI Generator

## Overview
Generates command-line interface tools for Code Intelligence & Security Layer capabilities.

## Features
- Auto-generates CLI tools from capability definitions
- Supports multiple command formats (npm, python, go)
- Includes help text and usage examples
- Integrated with pattern library

## Usage
```bash
gl-codeintel scan --source ./src --pattern security
gl-codeintel fix --vulnerability sql-injection --file app.js
gl-codeintel analyze --type performance --output report.json
```

## Generated Tools
1. `gl-codeintel`: Main CLI tool
2. `gl-security`: Security-focused CLI
3. `gl-perf`: Performance optimization CLI
4. `gl-arch`: Architecture analysis CLI