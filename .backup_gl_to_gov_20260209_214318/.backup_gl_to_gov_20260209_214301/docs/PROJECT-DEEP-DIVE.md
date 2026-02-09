# Project Deep Dive - Indestructible Auto Ops

## Scope
This document provides a focused technical deep dive of the repository and
highlights upgrade and restructure opportunities. It is grounded in the current
layout and enforcement code paths in this repo.

## High-Level Architecture
- GL governance architecture with multiple layers (GL00-GL99).
- Ecosystem governance enforcement implemented under `ecosystem/`.
- Platform-specific runtime and services in `gl-*-platform/` directories.
- Additional mirror of earlier structure in `machine-native-ops/`.

## Observed Structure (Key Facts)
- Root contains a large number of operational and report documents.
- Two parallel trees exist for similar components:
  - `ecosystem/` (active governance runtime)
  - `machine-native-ops/` (legacy/mirrored content)
- Multiple GL platform directories exist at root (e.g., `gl-runtime-engine-platform/`).
- Enforcement tooling is centralized in `ecosystem/enforce.py`.

## Enforcement and Governance Findings
1. **Duplicate method definitions in enforcement**
   - Prior to this upgrade, `ecosystem/enforce.py` contained duplicated method
     definitions for multiple checks, leading to overwrites and inconsistencies.
2. **Violation model misuse**
   - Several enforcement checks were constructing `Violation` objects with
     incorrect field names, causing runtime errors.
3. **Pipeline integration lacked a health check**
   - `ecosystem/enforcers/pipeline_integration.py` did not provide a `check()`
     method even though pipeline status is reported in governance summaries.

## Repository Risks
- **Documentation sprawl**: a large number of MD files in root makes navigation
  and discovery difficult.
- **Duplicate trees**: the `machine-native-ops/` mirror risks drift and
  inconsistencies versus `ecosystem/`.
- **Mixed naming conventions**: kebab-case, snake_case, and mixed styles appear
  across directories and files.
- **Zero-dependency policy risk**: a legacy subtree imports external packages
  (e.g., YAML), which could violate constraints if executed in production paths.

## Upgrade Actions Implemented (This Change Set)
- Consolidated governance checks in `ecosystem/enforce.py` into a single,
  non-duplicated block with consistent `Violation` construction.
- Added a basic `check()` method to the pipeline integration class to surface
  config availability and output directory readiness.

## Recommended Next Steps
1. **Document Indexing**
   - Create an indexed documentation map under `docs/` and reduce root clutter.
2. **Repository Structure Consolidation**
   - Decide on a single source of truth between `ecosystem/` and
     `machine-native-ops/` and plan a staged merge or deprecation path.
3. **Platform Registry Normalization**
   - Align `gl-*-platform/` directories with a single registry and entrypoint.
4. **Governance Test Harness**
   - Add a lightweight, zero-dependency test harness for enforcement checks.

## Evidence Paths
- Enforcement entrypoint: `ecosystem/enforce.py`
- Pipeline integration: `ecosystem/enforcers/pipeline_integration.py`
- Legacy mirror: `machine-native-ops/`
