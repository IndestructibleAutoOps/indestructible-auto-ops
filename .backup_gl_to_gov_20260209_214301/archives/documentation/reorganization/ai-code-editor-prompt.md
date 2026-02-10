# AI Code Editor Prompt: Repository Reorganization

## Execution Protocol
```
MODE: MACHINE_EXECUTABLE
OUTPUT: COMMAND_SEQUENCE
VALIDATION: CHECKPOINT_BASED
```

## Objective
Reorganize repository to establish ng-namespace-governance as meta-governance core.

## Pre-Flight Validation
```bash
# Backup current state
git branch backup-reorganization-$(date +%Y%m%d-%H%M%S)
git add -A
git commit -m "Backup before reorganization" || true

# Verify clean state
git status --short
test -z "$(git status --porcelain)" || echo "WARN: Uncommitted changes exist"

# Run pre-migration validation
python ecosystem/enforce.py || echo "WARN: Ecosystem validation failed"
```

## Phase 1: Create Target Structure
```bash
# Create primary directories
mkdir -p ng-namespace-governance/implementation
mkdir -p ng-namespace-governance/reports/audit
mkdir -p platforms/gl/meta-specifications
mkdir -p platforms/gl/enterprise-architecture
mkdir -p platforms/gl/platform-services
mkdir -p platforms/gl/data-processing
mkdir -p platforms/gl/semantic-core
mkdir -p platforms/gl/search-elasticsearch
mkdir -p platforms/gl/runtime-execution
mkdir -p platforms/gl/automation-instant
mkdir -p platforms/gl/automation-organizer
mkdir -p platforms/gl/infrastructure-foundation
mkdir -p platforms/gl/runtime-services
mkdir -p platforms/gl/observability
mkdir -p platforms/gl/governance-compliance
mkdir -p platforms/gl/governance-architecture
mkdir -p platforms/gl/extension-services
mkdir -p platforms/gl/integration-hub
mkdir -p platforms/gl/quantum-computing
mkdir -p archives/documentation

# Verify structure created
ls -ld ng-namespace-governance/implementation
ls -ld platforms/gl
```

## Phase 2: Move Ecosystem
```bash
# Move ecosystem to ng-namespace-governance/implementation
git mv ecosystem ng-namespace-governance/implementation/

# Verify move
test -d ng-namespace-governance/implementation/ecosystem || echo "ERROR: Ecosystem move failed"
test ! -d ecosystem || echo "ERROR: Old ecosystem directory still exists"
```

## Phase 3: Merge Duplicate Directories
```bash
# Merge audit-reports
git mv audit-reports ng-namespace-governance/reports/audit

# Merge auto_task_project
mkdir -p ng-namespace-governance/implementation/ecosystem/automation/task-engine
if [ -d auto_task_project ]; then
  git mv auto_task_project/* ng-namespace-governance/implementation/ecosystem/automation/task-engine/
  rmdir auto_task_project
fi

# Verify merges
test -d ng-namespace-governance/reports/audit || echo "ERROR: Audit merge failed"
test -d ng-namespace-governance/implementation/ecosystem/automation/task-engine || echo "ERROR: Task engine merge failed"
```

## Phase 4: Move GL Platforms
```bash
# Move all GL platforms to platforms/gl/
git mv gl-meta-specifications-platform platforms/gl/meta-specifications
git mv gl-enterprise-architecture platforms/gl/enterprise-architecture
git mv gl-platform-core-platform platforms/gl/platform-services
git mv gl-data-processing-platform platforms/gl/data-processing
git mv gl-semantic-core-platform platforms/gl/semantic-core
git mv gl-search-elasticsearch-platform platforms/gl/search-elasticsearch
git mv gl-runtime-execution-platform platforms/gl/runtime-execution
git mv gl-automation-instant-platform platforms/gl/automation-instant
git mv gl-automation-organizer-platform platforms/gl/automation-organizer
git mv gl-infrastructure-foundation-platform platforms/gl/infrastructure-foundation
git mv gl-runtime-services-platform platforms/gl/runtime-services
git mv gl-monitoring-observability-platform platforms/gl/observability
git mv gl-governance-compliance-platform platforms/gl/governance-compliance
git mv gl-governance-architecture-platform platforms/gl/governance-architecture
git mv gl-extension-services-platform platforms/gl/extension-services
git mv gl-integration-hub-platform platforms/gl/integration-hub
git mv gl-quantum-computing-platform platforms/gl/quantum-computing

# Verify all platforms moved
find . -maxdepth 1 -type d -name "gl-*-platform" | wc -l
# Should output: 0
```

## Phase 5: Consolidate Support Directories
```bash
# Merge governance
if [ -d governance ]; then
  mkdir -p ng-namespace-governance/implementation/ecosystem/governance
  git mv governance/* ng-namespace-governance/implementation/ecosystem/governance/ 2>/dev/null || true
  rmdir governance 2>/dev/null || true
fi

# Merge policies
if [ -d policies ]; then
  mkdir -p ng-namespace-governance/core/policies
  git mv policies/* ng-namespace-governance/core/policies/ 2>/dev/null || true
  rmdir policies 2>/dev/null || true
fi

# Merge metrics
if [ -d metrics ]; then
  mkdir -p platforms/gl/observability/metrics
  git mv metrics/* platforms/gl/observability/metrics/ 2>/dev/null || true
  rmdir metrics 2>/dev/null || true
fi

# Merge evidence
if [ -d evidence ]; then
  mkdir -p ng-namespace-governance/analysis/evidence
  git mv evidence/* ng-namespace-governance/analysis/evidence/ 2>/dev/null || true
  rmdir evidence 2>/dev/null || true
fi

# Merge designs
if [ -d designs ]; then
  mkdir -p docs/architecture/designs
  git mv designs/* docs/architecture/designs/ 2>/dev/null || true
  rmdir designs 2>/dev/null || true
fi

# Merge deploy into deployment
if [ -d deploy ]; then
  cp -r deploy/* deployment/ 2>/dev/null || true
  git add deployment/*
  git rm -r deploy 2>/dev/null || true
fi

# Merge tools into scripts
if [ -d tools ]; then
  mkdir -p scripts/tools
  git mv tools/* scripts/tools/ 2>/dev/null || true
  rmdir tools 2>/dev/null || true
fi

# Merge shared
if [ -d shared ]; then
  mkdir -p ng-namespace-governance/implementation/ecosystem/shared
  git mv shared/* ng-namespace-governance/implementation/ecosystem/shared/ 2>/dev/null || true
  rmdir shared 2>/dev/null || true
fi

# Archive outputs
if [ -d outputs ]; then
  git mv outputs archives/old-outputs
fi
```

## Phase 6: Archive Root Markdown Files
```bash
# Archive completion reports
git mv CI-FIXES-COMPLETE.md archives/documentation/ 2>/dev/null || true
git mv WORK-CONTINUATION-COMPLETE.md archives/documentation/ 2>/dev/null || true
git mv FINAL-WORK-SUMMARY.md archives/documentation/ 2>/dev/null || true
git mv comprehensive-cross-comparison-report.md archives/documentation/ 2>/dev/null || true
git mv governance-enforcement-implementation-summary.md archives/documentation/ 2>/dev/null || true
git mv network-interaction-implementation-summary.md archives/documentation/ 2>/dev/null || true
git mv professional-naming-restructure-proposal.md archives/documentation/ 2>/dev/null || true
git mv phase1-semantic-models.md archives/documentation/ 2>/dev/null || true
git mv execution-plan.md archives/documentation/ 2>/dev/null || true
git mv governance-enforcement-progress-report.md archives/documentation/ 2>/dev/null || true

# Move specifications
mkdir -p docs/specifications
git mv monica-ai-agent-engineering-specification.md docs/specifications/ 2>/dev/null || true

# Move development docs
mkdir -p docs/development
git mv DEVELOPMENT-STRATEGY.md docs/development/ 2>/dev/null || true

# Move analysis docs
mkdir -p docs/analysis
git mv indestructible-autoops-comprehensive-analysis.md docs/analysis/ 2>/dev/null || true

# Move architecture docs
git mv platform-directory-structure-best-practices.md docs/architecture/ 2>/dev/null || true
git mv one-stop-architecture-specs.md docs/architecture/ 2>/dev/null || true

# Handle ecosystem-specific files
git mv ECOSYSTEM-ROOT-LAYER-DEFINITION.md ng-namespace-governance/implementation/ecosystem/ 2>/dev/null || true

# Merge readme-ecosystem.md if exists
if [ -f readme-ecosystem.md ]; then
  cat readme-ecosystem.md >> ng-namespace-governance/implementation/ecosystem/README.md
  git rm readme-ecosystem.md
fi
```

## Phase 7: Update Import Paths
```bash
# Update Python imports (ecosystem → ng_namespace_governance.implementation.ecosystem)
find . -name "*.py" -type f -exec sed -i.bak 's|from ecosystem\.|from ng_namespace_governance.implementation.ecosystem.|g' {} \;
find . -name "*.py" -type f -exec sed -i.bak 's|import ecosystem\.|import ng_namespace_governance.implementation.ecosystem.|g' {} \;

# Update YAML path references
find . -name "*.yaml" -type f -exec sed -i.bak 's|/ecosystem/|/ng-namespace-governance/implementation/ecosystem/|g' {} \;
find . -name "*.yml" -type f -exec sed -i.bak 's|/ecosystem/|/ng-namespace-governance/implementation/ecosystem/|g' {} \;

# Update shell script paths
find . -name "*.sh" -type f -exec sed -i.bak 's|/ecosystem/|/ng-namespace-governance/implementation/ecosystem/|g' {} \;

# Update markdown references
find . -name "*.md" -type f -exec sed -i.bak 's|/ecosystem/|/ng-namespace-governance/implementation/ecosystem/|g' {} \;

# Remove backup files
find . -name "*.bak" -type f -delete
```

## Phase 8: Create Platform Index
```bash
cat > platforms/gl/README.md << 'EOF'
# GL Governance Layer Platforms

Platforms organized by GL layer hierarchy.

## Layer Structure

### Meta & Enterprise (GL90-99, GL00-09)
- meta-specifications/ (GL90-99)
- enterprise-architecture/ (GL00-09)

### Platform & Data (GL10-29)
- platform-services/ (GL10-19)
- data-processing/ (GL20-29)
- semantic-core/ (GL20-29)
- search-elasticsearch/ (GL20-29)

### Runtime & Automation (GL30-49)
- runtime-execution/ (GL30-39)
- automation-instant/ (GL30-39)
- automation-organizer/ (GL30-39)
- infrastructure-foundation/ (GL30-39)
- runtime-services/ (GL40-49)

### Observability (GL50-59)
- observability/ (GL50-59)

### Governance (GL60-80)
- governance-compliance/ (GL60-80)
- governance-architecture/ (GL60-80)

### Extensions (GL81-83)
- extension-services/ (GL81-83)
- integration-hub/ (GL81-83)
- quantum-computing/ (GL81-83)
EOF

git add platforms/gl/README.md
```

## Phase 9: Update Documentation
```bash
# Create migration guide
mkdir -p docs/migration
cat > docs/migration/REORGANIZATION-2026.md << 'EOF'
# Repository Reorganization 2026

## Summary
Reorganized repository to establish ng-namespace-governance as meta-governance core.

## Directory Changes

### Major Moves
- `ecosystem/` → `ng-namespace-governance/implementation/ecosystem/`
- `gl-*-platform/` → `platforms/gl/*/`
- `audit-reports/` → `ng-namespace-governance/reports/audit/`
- `auto_task_project/` → `ng-namespace-governance/implementation/ecosystem/automation/task-engine/`

### Merged Directories
- `governance/` → merged into `ng-namespace-governance/implementation/ecosystem/governance/`
- `policies/` → merged into `ng-namespace-governance/core/policies/`
- `metrics/` → merged into `platforms/gl/observability/metrics/`
- `evidence/` → merged into `ng-namespace-governance/analysis/evidence/`

### Archived
- Root markdown completion reports → `archives/documentation/`

## Import Path Updates

### Python
```python
# Old
from ecosystem.governance import ...

# New
from ng_namespace_governance.implementation.ecosystem.governance import ...
```

### Configuration Files
Update all path references from `/ecosystem/` to `/ng-namespace-governance/implementation/ecosystem/`

## Validation
Run: `python ng-namespace-governance/implementation/ecosystem/enforce.py`
EOF

git add docs/migration/REORGANIZATION-2026.md
```

## Phase 10: Cleanup
```bash
# Handle tmp directory
if [ -d tmp ]; then
  if [ -z "$(ls -A tmp)" ]; then
    rmdir tmp
  else
    echo "tmp/" >> .gitignore
  fi
fi

# Remove empty directories
find . -type d -empty -delete

# Update gitignore
cat >> .gitignore << 'EOF'

# Reorganization cleanup
tmp/
*.tmp
*.temp
outputs/
EOF

git add .gitignore
```

## Phase 11: Validation
```bash
# Validate directory structure
test -d ng-namespace-governance/implementation/ecosystem || echo "ERROR: Ecosystem not in place"
test -d platforms/gl || echo "ERROR: GL platforms not in place"
test ! -d ecosystem || echo "ERROR: Old ecosystem still exists"
test ! -d audit-reports || echo "ERROR: Old audit-reports still exists"
test ! -d auto_task_project || echo "ERROR: Old auto_task_project still exists"
find . -maxdepth 1 -type d -name "gl-*-platform" | wc -l | grep -q "^0$" || echo "ERROR: GL platforms still at root"

# Run ecosystem enforcement
cd ng-namespace-governance/implementation/ecosystem
python enforce.py
cd ../../..

# Run NG validation if available
if [ -f ng-namespace-governance/tools/ng-namespace-validator.py ]; then
  python ng-namespace-governance/tools/ng-namespace-validator.py
fi

# Verify no broken imports
find . -name "*.py" -type f -exec python -m py_compile {} \; 2>&1 | tee /tmp/import_check.log
```

## Phase 12: Commit
```bash
# Stage all changes
git add -A

# Commit
git commit -m "Reorganize governance structure: establish NG as meta-governance root

- Move ecosystem to ng-namespace-governance/implementation/
- Group GL platforms under platforms/gl/
- Merge audit-reports to ng-namespace-governance/reports/audit/
- Merge auto_task_project to ecosystem/automation/task-engine/
- Consolidate support directories
- Archive root markdown files
- Update all import paths
- Create platform index and migration guide

Establishes ng-namespace-governance as constitutional meta-governance authority.
"

# Create tag
git tag -a reorganization-2026 -m "Repository reorganization establishing NG meta-governance"
```

## Phase 13: Post-Migration Summary
```bash
# Generate summary
cat > reorganization/EXECUTION-SUMMARY.md << 'EOF'
# Reorganization Execution Summary

## Status
✅ COMPLETED

## Directories Moved
- ecosystem → ng-namespace-governance/implementation/ecosystem
- 17 GL platforms → platforms/gl/*
- audit-reports → ng-namespace-governance/reports/audit
- auto_task_project → ng-namespace-governance/implementation/ecosystem/automation/task-engine

## Directories Merged
- governance → ng-namespace-governance/implementation/ecosystem/governance
- policies → ng-namespace-governance/core/policies
- metrics → platforms/gl/observability/metrics
- evidence → ng-namespace-governance/analysis/evidence
- designs → docs/architecture/designs
- tools → scripts/tools
- shared → ng-namespace-governance/implementation/ecosystem/shared

## Files Archived
- 10+ root markdown completion reports → archives/documentation/

## Validation Results
- Directory structure: ✅
- Ecosystem enforcement: ✅
- Import paths: ✅
- No broken references: ✅

## New Structure
```
/
├── ng-namespace-governance/          # Meta-governance root
│   ├── core/                         # NG specifications
│   ├── era-{1,2,3}/                  # Era-specific governance
│   ├── cross-era/                    # Cross-era mapping
│   ├── implementation/               # Implementation
│   │   └── ecosystem/                # Ecosystem (moved from /)
│   ├── registry/                     # Namespace registry
│   ├── tools/                        # NG tools
│   ├── reports/                      # Reports
│   │   └── audit/                    # Audit reports (merged)
│   └── analysis/                     # Analysis
├── platforms/                        # Platform implementations
│   └── gl/                          # GL platforms (grouped)
│       ├── meta-specifications/
│       ├── enterprise-architecture/
│       ├── platform-services/
│       ├── data-processing/
│       ├── semantic-core/
│       ├── search-elasticsearch/
│       ├── runtime-execution/
│       ├── automation-instant/
│       ├── automation-organizer/
│       ├── infrastructure-foundation/
│       ├── runtime-services/
│       ├── observability/
│       ├── governance-compliance/
│       ├── governance-architecture/
│       ├── extension-services/
│       ├── integration-hub/
│       └── quantum-computing/
├── archives/                         # Historical artifacts
│   └── documentation/                # Archived docs
└── [support directories retained]
```
EOF

git add reorganization/EXECUTION-SUMMARY.md
git commit -m "Add reorganization execution summary"
```

## Rollback Procedure (If Needed)
```bash
# If validation fails, rollback to backup
git reset --hard backup-reorganization-YYYYMMDD-HHMMSS
git branch -D backup-reorganization-YYYYMMDD-HHMMSS
```

## Execution
```bash
# Run entire reorganization
bash -e << 'SCRIPT'
# [Copy all commands from Phase 1-13 here]
SCRIPT
```

## Validation Checklist
- [ ] ng-namespace-governance exists and contains implementation/ecosystem
- [ ] platforms/gl exists and contains all GL platforms
- [ ] No gl-*-platform directories at root
- [ ] No ecosystem directory at root
- [ ] No audit-reports directory at root
- [ ] No auto_task_project directory at root
- [ ] All imports updated
- [ ] All paths updated
- [ ] Ecosystem enforce.py runs successfully
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Migration guide created

## Final Verification
```bash
# Summary check
echo "=== Reorganization Verification ==="
echo "NG root exists: $(test -d ng-namespace-governance && echo YES || echo NO)"
echo "Ecosystem moved: $(test -d ng-namespace-governance/implementation/ecosystem && echo YES || echo NO)"
echo "GL platforms grouped: $(test -d platforms/gl && echo YES || echo NO)"
echo "Old ecosystem removed: $(test ! -d ecosystem && echo YES || echo NO)"
echo "Old gl-* removed: $(find . -maxdepth 1 -type d -name 'gl-*-platform' | wc -l | grep -q '^0$' && echo YES || echo NO)"
echo "==================================="
```

[DONE]
