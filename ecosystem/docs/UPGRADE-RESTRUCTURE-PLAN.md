# Upgrade & Restructure Plan

## Goals
- Reduce duplication and drift across parallel trees.
- Improve governance enforcement reliability.
- Make documentation discoverable and maintainable.
- Prepare for platform scaling with a clean registry and layout.

## Target Structure (Conceptual)
```
/ecosystem              # Governance core, contracts, enforcement
/platforms              # Platform runtimes and adapters
/shared                 # Shared utilities, templates, and specs
/docs                   # Single source of documentation
/gl-*-platform          # Legacy platform directories (to be merged or mapped)
```

## Phase 0 (Immediate)
1. **Stabilize enforcement**
   - Remove duplicate check implementations.
   - Ensure all checks construct `Violation` objects correctly.
2. **Add health checks**
   - Provide a `check()` method in pipeline integration for governance summaries.

## Phase 1 (Docs Restructure)
1. **Create a docs index**
   - Consolidate root MD files into `docs/`.
2. **Add a root "Docs Map"**
   - A single entrypoint linking plans, reports, and architecture.
3. **Enforce naming conventions**
   - Align files to consistent kebab-case or snake_case per policy.

## Phase 2 (Tree Consolidation)
1. **Define a source of truth**
   - Decide whether `ecosystem/` or `machine-native-ops/` is authoritative.
2. **Establish a migration map**
   - Use a mapping file for file moves and deprecations.
3. **Deprecate legacy paths**
   - Add deprecation notes and pointers for old paths.

## Phase 3 (Platform Registry Normalization)
1. **Registry spec**
   - Define a single platform registry under `platforms/registry/`.
2. **Entry points**
   - Add unified entrypoints for platform execution and deployment.

## Phase 4 (Quality Gates)
1. **Automated checks**
   - Ensure enforcement, naming, and evidence gates run consistently.
2. **Evidence coverage**
   - Report evidence coverage as a required output for governance runs.

## Success Criteria
- Single, authoritative governance tree.
- Documentation discoverable via a single docs index.
- No duplicated enforcement logic.
- Platform registry and entrypoints standardized.
