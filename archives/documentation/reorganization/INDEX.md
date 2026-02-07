=== path: reorganization/INDEX.md ===

# Reorganization Specification Index

## Overview
Complete machine-readable specification for repository governance structure reorganization.

## Artifacts

### 1. problem-analysis.yaml
**Purpose**: Root cause analysis and engineering patch specification

**Contains**:
- Problem identification
- Root cause analysis (RCA-01, RCA-02, RCA-03)
- Fix proposal
- Engineering patch
- Verification steps
- Governance compliance check

**Usage**: Understanding the why and what of reorganization

---

### 2. directory-structure.yaml
**Purpose**: Complete directory structure specification

**Contains**:
- Root level structure
- ng-namespace-governance hierarchy
- platforms/gl organization
- Support directory retention rules
- Deprecated directory handling

**Usage**: Reference for target directory structure

---

### 3. directory-mapping.yaml
**Purpose**: Source-to-target mapping for all directories

**Contains**:
- Governance migration mappings
- Duplicate resolution strategies
- GL platform migration mappings
- Support directory actions
- Root markdown file migration
- Migration sequence (6 phases)

**Usage**: Detailed migration execution mapping

---

### 4. file-classification.yaml
**Purpose**: File classification rules and patterns

**Contains**:
- Classification dimensions
- Pattern-based classification rules
- Meta-governance file rules
- Era-specific file rules
- GL platform file rules
- Ecosystem implementation rules
- Priority resolution algorithm

**Usage**: Automated file categorization and placement

---

### 5. execution-plan.yaml
**Purpose**: Phase-by-phase execution specification

**Contains**:
- Pre-execution validation
- 8 execution phases with checkpoints
- Post-execution summary
- Rollback plan
- Monitoring configuration

**Phases**:
1. Ecosystem migration
2. GL platform reorganization
3. Support directory consolidation
4. Root markdown migration
5. Cleanup
6. Documentation updates
7. Import path updates
8. Validation

**Usage**: Step-by-step execution guide

---

### 6. meta-governance-spec.yaml
**Purpose**: Constitutional governance specification

**Contains**:
- Meta-governance definition
- Directory responsibility matrix
- Governance mapping table
- Governance flow
- Authority hierarchy
- Compliance requirements
- Validation framework
- Enforcement mechanisms

**Usage**: Understanding governance structure and authority

---

### 7. directory-responsibility-matrix.yaml
**Purpose**: Comprehensive responsibility boundary definition

**Contains**:
- Tier-based responsibility matrix (T0-T3)
- Capability definitions
- Boundary specifications (can/cannot/must)
- Interface definitions
- Cross-cutting responsibilities
- Tier interaction rules
- Conflict resolution

**Usage**: Understanding directory roles and boundaries

---

### 8. governance-mapping-table.yaml
**Purpose**: Governance layer integration mapping

**Contains**:
- NG to GL mapping
- Governance flow mapping
- Directory to governance layer mapping
- NG to ecosystem contracts
- Ecosystem to platform contracts
- GL layer to NG era mapping
- Authority chain
- Validation chain
- Audit trail mapping

**Usage**: Understanding governance relationships and contracts

---

### 9. ai-code-editor-prompt.md
**Purpose**: Complete machine-executable reorganization script

**Contains**:
- Pre-flight validation commands
- 13 execution phases with bash commands
- Validation checkpoints
- Rollback procedure
- Final verification checklist

**Usage**: Copy-paste to AI code editor for execution

---

## Execution Workflow

### Understanding Phase
1. Read `problem-analysis.yaml` - understand the problem
2. Read `directory-structure.yaml` - understand target structure
3. Read `meta-governance-spec.yaml` - understand governance model

### Planning Phase
4. Read `directory-mapping.yaml` - understand migrations
5. Read `file-classification.yaml` - understand file handling
6. Read `directory-responsibility-matrix.yaml` - understand boundaries

### Execution Phase
7. Read `execution-plan.yaml` - understand phases
8. Read `governance-mapping-table.yaml` - understand integration
9. Use `ai-code-editor-prompt.md` - execute reorganization

## Machine Execution

### Option 1: Direct Execution
```bash
bash reorganization/ai-code-editor-prompt.md
```

### Option 2: AI Code Editor
1. Copy entire content of `ai-code-editor-prompt.md`
2. Paste into AI code editor
3. Execute phase by phase

### Option 3: Manual Execution
1. Follow `execution-plan.yaml` phase by phase
2. Use `directory-mapping.yaml` for reference
3. Apply `file-classification.yaml` rules
4. Validate with checkpoint commands

## Validation

### Pre-Execution
- Git status clean
- No uncommitted changes
- All tests passing
- Ecosystem enforce.py passes

### Post-Execution
- NG root exists with implementation/ecosystem
- GL platforms grouped under platforms/gl/
- No duplicate directories
- All imports updated
- All validations pass

### Continuous
- Run ecosystem enforce.py
- Run NG namespace validator
- Run test suite
- Check directory structure compliance

## Rollback

If validation fails:
```bash
git reset --hard backup-reorganization-YYYYMMDD-HHMMSS
```

## Compliance

All artifacts comply with:
- NG Charter (NG00000)
- NG Identifier Standards (NG00101)
- NG Lifecycle Standards (NG00201)
- NG Validation Rules (NG00301)
- GL Layer Boundaries
- Ecosystem Contracts

## Support

For issues or questions:
1. Review problem-analysis.yaml for rationale
2. Check directory-responsibility-matrix.yaml for boundaries
3. Consult governance-mapping-table.yaml for integration
4. Refer to meta-governance-spec.yaml for authority

---

**Version**: 1.0.0
**Status**: READY_FOR_EXECUTION
**Format**: MACHINE_READABLE
**Last Updated**: 2026-02-07

[DONE]
