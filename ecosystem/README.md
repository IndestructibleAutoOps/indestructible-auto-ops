# Ecosystem Core

The Ecosystem Core describes the governance-aligned layout for platform implementations, governance frameworks, tooling, documentation, and infrastructure for the MachineNativeOps GL Architecture.

## Structure (Planned / Proposed Consolidation)

> Note: The tree below describes the **planned consolidated `ecosystem/` layout**. The current `main` branch may still reflect the pre-consolidation directory structure until the migration is complete.

```
ecosystem/
├── platforms/                   # All GL Platform implementations
│   ├── runtime-engine/          # GL30-49: Execution Runtime Engine (AEP, ETL, etc.)
│   ├── runtime-services/        # GL30-49: Runtime Services
│   ├── governance-architecture/ # GL00-09: Governance Architecture
│   ├── governance-compliance/   # GL60-80: Governance Compliance
│   ├── enterprise-architecture/ # GL00-09: Enterprise Architecture
│   ├── infrastructure-foundation/ # Kubernetes, Redis, RKE2
│   ├── automation-instant/      # Instant Automation Platform
│   ├── automation-organizer/    # File Organizer Platform
│   ├── core/                    # Platform Core (TS)
│   ├── data-processing/         # GL20-29: Data Processing
│   ├── search-elasticsearch/    # GL20-29: Search System
│   ├── semantic-core/           # Semantic Computation
│   ├── quantum-computing/       # Quantum Computing
│   ├── integration-hub/         # GL10-29: Integration Hub
│   ├── monitoring-observability/ # GL50-59: Monitoring
│   ├── gl.platform-assistant/   # Platform Assistant API
│   ├── gl.platform-ide/         # IDE Plugin
│   └── registry/                # Platform Registry
├── governance/                  # Governance specifications & policies
│   ├── specs/                   # Architecture-to-code protocol specs
│   ├── workflows/               # Research loop & governance workflows
│   ├── kernel/                  # Self-governance kernel
│   ├── ng-namespace/            # NG Namespace Governance System
│   ├── policies/                # OPA/Rego policies
│   ├── closure/                 # Governance closure
│   └── ...                      # Enforcement rules, format layers, etc.
├── contracts/                   # GL interface contracts
│   ├── governance/              # Governance contracts
│   ├── naming-governance/       # Naming convention contracts
│   ├── verification/            # Verification contracts
│   ├── reasoning/               # Reasoning contracts
│   └── ...                      # Other contract definitions
├── coordination/                # Cross-platform coordination
│   ├── api-gateway/             # API Gateway (auth, rate limit, routing)
│   ├── communication/           # Message bus & event dispatcher
│   ├── data-synchronization/    # Data sync engine & connectors
│   └── service-discovery/       # Service registry & discovery
├── reasoning/                   # AI Reasoning engine
├── engines/                     # Core engines (sealing, repair, governance)
├── enforcers/                   # Governance enforcers
├── foundation/                  # Foundation schemas, formatters, DAG
├── auto-task/                   # Automated task scheduling system
├── config/                      # Platform configuration files
├── deploy/                      # Deployment configs & scripts
│   ├── scripts/                 # Deployment scripts (single-node, cluster, air-gapped)
│   └── platform/                # Platform deployment (alertmanager, etc.)
├── docs/                        # All documentation
│   ├── archive/                 # Historical docs & reports
│   ├── analysis/                # Architecture analysis
│   ├── plans/                   # Migration & restructure plans
│   ├── designs/                 # Multi-agent architecture designs
│   └── ...                      # Additional documentation
├── reports/                     # Audit & compliance reports
├── scripts/                     # Utility & automation scripts
├── tests/                       # Test suites
├── tools/                       # Development & governance tools
├── registry/                    # Service, data & platform registries
├── evidence/                    # Compliance evidence chain
├── metrics/                     # Current metrics
├── monitoring/                  # Alert rules
├── data/                        # Data files & legacy artifacts
├── archives/                    # Historical output archives
├── complements/                 # Templates (reports, checklists, etc.)
├── platform-templates/          # Platform deployment templates
│   ├── core-template/           # Core platform template
│   ├── cloud-template/          # Cloud platform template
│   └── on-premise-template/     # On-premise template
├── platform-cloud/              # Cloud platform configuration
├── ecosystem-cloud/             # Cloud ecosystem adapters & contracts
├── hooks/                       # Pre/post execution hooks
├── indexes/                     # Internal/external indexes
├── mocks/                       # Mock services & data
├── semantic/                    # Semantic context
├── utils/                       # Utility modules
├── validators/                  # Network & data validators
├── events/                      # Event emitter
├── gates/                       # Quality gates
├── shared/                      # Shared resources
├── __init__.py                  # Python package init
└── README.md                    # This file
```

> NOTE: The following `ecosystem/` directory tree describes a **planned / proposed consolidated layout** for the MachineNativeOps GL Architecture. It may not exactly match the current `main` branch filesystem. Use the root-level README (and the live repository tree) as the source of truth for the current on-main layout; treat this section as a migration / design reference until the consolidation lands.

## Purpose

The ecosystem provides:

1. **Centralized Governance**: All governance policies, enforcement rules, and compliance checking are managed centrally under `governance/` and `contracts/`.

2. **Platform Consolidation**: All GL platform implementations (formerly scattered as `gl-*` directories) are consolidated under `platforms/`.

3. **Cross-Platform Coordination**: Service discovery, data synchronization, API gateway, and communication are managed through `coordination/`.

4. **Unified Tooling**: All scripts, tools, deployment configurations, and test suites are organized in their respective directories.

5. **Comprehensive Documentation**: All docs, reports, and historical archives are consolidated under `docs/` and `reports/`.

## Quick Start

### Run Tests
```bash
python3 -m pytest ecosystem/tests/
```

### Run Governance Checks
```bash
python3 ecosystem/enforce.py
```

### Deploy Platform
```bash
# Single-node deployment
bash ecosystem/deploy/scripts/single-node/02-install-k3s.sh
bash ecosystem/deploy/scripts/single-node/03-deploy-gl-backend.sh
```

### Auto-Task System
```bash
cd ecosystem/auto-task
python3 main.py
```

## Governance

All platforms must comply with:
- GL naming conventions (`governance/ng-namespace/`)
- Interface contracts (`contracts/`)
- Boundary enforcement rules (`governance/enforcement-rules.yaml`)
- Quality gates (`gates/`)

## Key Modules

| Module | Description |
|--------|-------------|
| `platforms/runtime-engine/` | Core execution runtime with AEP engine app/web |
| `platforms/governance-architecture/` | GL layer governance specifications |
| `platforms/governance-compliance/` | Compliance checking & enforcement |
| `platforms/infrastructure-foundation/` | Kubernetes & infrastructure configs |
| `governance/` | Centralized governance framework |
| `contracts/` | GL interface contracts |
| `coordination/` | Cross-platform coordination services |
| `reasoning/` | AI reasoning engine |
| `auto-task/` | Automated task scheduling |
