<!-- @GL-governed -->
<!-- @GL-layer: GL90-99 -->
<!-- @GL-semantic: governed-documentation -->
<!-- @GL-audit-trail: engine/governance/GL_SEMANTIC_ANCHOR.json -->

# GL Unified Charter - Best Practice Migration Plan

**GL Unified Charter Activated**
**Report ID:** db58e146876fb8dd
**Generated:** 2026-01-24

---

## Executive Summary

The AEP Engine governance audit has completed successfully with **48 files processed** and **121 issues identified**. While no CRITICAL or HIGH severity issues were found, there are significant opportunities to improve governance compliance.

### Issue Distribution

| Severity | Count | Percentage |
|----------|-------|------------|
| CRITICAL | 0 | 0% |
| HIGH | 0 | 0% |
| MEDIUM | 70 | 57.9% |
| LOW | 51 | 42.1% |

### Issue Categories

| Category | Count | Priority |
|----------|-------|----------|
| GL Marker Missing | 47 | P1 - High |
| Semantic Manifest Missing | 43 | P2 - Medium |
| Type Errors (any usage) | 23 | P2 - Medium |
| Metadata Missing | 8 | P3 - Low |

---

## Best Practice Directory Structure

### Current Structure
```
engine/
├── artifacts/
├── executor/
├── governance/
├── loader/
├── normalizer/
├── parser/
├── renderer/
├── tests/
│   ├── artifacts/
│   ├── governance/
│   ├── loader/
│   ├── normalizer/
│   └── validator/
└── validator/
```

### Recommended Structure (GL-Compliant)
```
engine/
├── .gl/                          # GL governance metadata
│   ├── manifest.yaml             # Module manifest
│   ├── semantic-anchor.yaml      # Semantic anchors
│   └── evidence-chain.json       # Evidence chain
├── src/                          # Source code (GL-30-EXECUTION)
│   ├── artifacts/
│   ├── executor/
│   ├── governance/
│   ├── loader/
│   ├── normalizer/
│   ├── parser/
│   ├── renderer/
│   └── validator/
├── __tests__/                    # Tests (GL-50-OBSERVABILITY)
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/                         # Documentation (GL-90-META)
│   ├── api/
│   └── guides/
├── index.ts                      # Main entry point
├── package.json
├── tsconfig.json
└── readme.md
```

---

## Migration Actions

### Phase 1: Add GL Governance Markers (Priority: HIGH)

**Affected Files:** 47 files (see full list in `governance-audit-results/per-file-reports/`)

Add GL layer annotations to all source files:

```typescript
/**
 * @gl-layer GL-30-EXECUTION
 * @gl-module engine/artifacts
 * @gl-semantic-anchor GL-30-EXEC-TS
 * @gl-evidence-required true
 */
```

**Files requiring GL markers (partial list - example files):**
1. `engine/artifacts/artifact_manager.ts`
2. `engine/artifacts/evidence_chain.ts`
3. `engine/artifacts/manifest_generator.ts`
4. `engine/executor/local_executor.ts`
5. `engine/executor/remote_executor.ts`
6. `engine/executor/rollback.ts`
7. `engine/governance/anchor_resolver.ts`
8. `engine/governance/events_writer.ts`
9. `engine/governance/rule_evaluator.ts`
10. `engine/loader/fs_loader.ts`
11. `engine/loader/git_loader.ts`
12. `engine/loader/merge_index.ts`
13. `engine/normalizer/defaults_applier.ts`
14. `engine/normalizer/env_merger.ts`
15. `engine/normalizer/module_defaults.ts`
16. `engine/parser/anchor_resolver.ts`
17. `engine/parser/json_passthrough.ts`
18. `engine/parser/yaml_parser.ts`
19. `engine/renderer/artifact_writer.ts`
20. `engine/renderer/module_mapper.ts`
21. `engine/renderer/template_engine.ts`
22. `engine/validator/error_reporter.ts`
23. `engine/validator/module_validator.ts`
24. `engine/validator/schema_validator.ts`
25. All test files (6 files)
26. All README files (9 files)
27. Configuration files: `engine/index.ts`, `engine/interfaces-fix.d.ts`, `engine/interfaces.d.ts`, `engine/jest.config.js`, `engine/package.json`, `engine/package-lock.json`, `engine/tsconfig.json`, `engine/SPEC.md` (8 files)

**Note:** This list shows key examples. The complete list of all 47 files requiring GL markers can be found in the per-file audit reports at `governance-audit-results/per-file-reports/` (filter for files with `gl_marker_missing` issues).

### Phase 2: Add Semantic Manifests (Priority: MEDIUM)

**Affected Files:** 43 files

Create semantic manifest files for each module:

```yaml
# engine/.gl/semantic-anchor.yaml
gl_version: "1.0"
module: "aep-engine"
layer: "GL-30-EXECUTION"
anchors:
  - id: "GL-30-EXEC-AEP-ENGINE"
    type: "execution"
    description: "Architecture Execution Pipeline Engine"
    dependencies:
      - "GL-10-CONFIG"
      - "GL-50-OBSERVABILITY"
```

### Phase 3: Fix Type Errors (Priority: MEDIUM)

**Affected Files:** 23 files with `any` type usage

Replace `any` types with specific types:

```typescript
// Before
function process(data: any): any {
  return data;
}

// After
interface ProcessInput {
  id: string;
  payload: Record<string, unknown>;
}

interface ProcessOutput {
  success: boolean;
  result: Record<string, unknown>;
}

function process(data: ProcessInput): ProcessOutput {
  return { success: true, result: data.payload };
}
```

### Phase 4: Improve Documentation (Priority: LOW)

**Affected Files:** 8 files

Add JSDoc documentation to all public APIs:

```typescript
/**
 * Manages artifact lifecycle in the AEP Engine.
 * 
 * @gl-layer GL-30-EXECUTION
 * @gl-module engine/artifacts
 * 
 * @example
 * ```typescript
 * const manager = new ArtifactManager();
 * await manager.create({ type: 'config', data: {} });
 * ```
 */
export class ArtifactManager {
  /**
   * Creates a new artifact.
   * @param artifact - The artifact configuration
   * @returns The created artifact with generated ID
   */
  async create(artifact: ArtifactConfig): Promise<Artifact> {
    // implementation
  }
}
```

---

## Naming Convention Standards

### File Naming
| Type | Convention | Example |
|------|------------|---------|
| TypeScript Source | snake_case | `artifact_manager.ts` |
| TypeScript Types | snake_case | `interfaces.d.ts` |
| Test Files | snake_case.test | `artifact_manager.test.ts` |
| Config Files | kebab-case | `tsconfig.json` |
| Documentation | UPPER_CASE | `readme.md` |

### Directory Naming
| Type | Convention | Example |
|------|------------|---------|
| Source Modules | lowercase | `artifacts/` |
| GL Metadata | dot-prefix | `.gl/` |
| Tests | double-underscore | `__tests__/` |

### GL Marker Naming
| Layer | Prefix | Example |
|-------|--------|---------|
| Strategic | GL-00 | `GL-00-STRATEGIC` |
| Operational | GL-10 | `GL-10-OPERATIONAL` |
| Execution | GL-30 | `GL-30-EXECUTION` |
| Observability | GL-50 | `GL-50-OBSERVABILITY` |
| Feedback | GL-60 | `GL-60-FEEDBACK` |
| Extended | GL-81 | `GL-81-EXTENDED` |
| Meta | GL-90 | `GL-90-META` |

---

## Governance Event Stream Integration

### Required Events
Each file operation must emit governance events:

```json
{
  "event_id": "unique-hash",
  "timestamp": "ISO-8601",
  "event_type": "FILE_MODIFIED",
  "source_file": "engine/artifacts/artifact_manager.ts",
  "gl_layer": "GL-30-EXECUTION",
  "semantic_anchor": "GL-30-EXEC-TS",
  "status": "SUCCESS",
  "evidence_hash": "sha256-hash"
}
```

### Event Types
- `FILE_CREATED` - New file added
- `FILE_MODIFIED` - Existing file changed
- `FILE_DELETED` - File removed
- `ETL_START` - ETL pipeline started
- `ETL_EXTRACT` - Data extraction complete
- `ETL_TRANSFORM` - Data transformation complete
- `ETL_LOAD` - Data loading complete
- `VALIDATION_PASSED` - Validation successful
- `VALIDATION_FAILED` - Validation failed

---

## Implementation Timeline

| Phase | Duration | Start | End |
|-------|----------|-------|-----|
| Phase 1: GL Markers | 2 days | Day 1 | Day 2 |
| Phase 2: Semantic Manifests | 1 day | Day 3 | Day 3 |
| Phase 3: Type Fixes | 3 days | Day 4 | Day 6 |
| Phase 4: Documentation | 2 days | Day 7 | Day 8 |

**Total Estimated Duration:** 8 days

---

## Verification Checklist

- [ ] All 47 files have GL markers
- [ ] All 43 files have semantic manifest references
- [ ] All 23 type errors resolved
- [ ] All 8 documentation gaps filled
- [ ] Governance event stream operational
- [ ] Evidence chain complete
- [ ] DAG integrity verified

---

**GL Unified Charter Activated**
**Document Hash:** `sha256:migration-plan-v1`