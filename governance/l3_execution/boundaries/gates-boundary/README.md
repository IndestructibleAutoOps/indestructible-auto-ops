# Operation Control Gates

**Directory**: `gates-governance/`  
**GL Layer**: N/A  
**Purpose**: Operation checkpoints with enforcement rules

---

## Overview

This directory contains governance specifications for Operation Control Gates.

## Directory Structure

### `checkpoints/`

Operation checkpoint definitions

**Key Files:**
- `file-migration-gates.yaml`
- `code-commit-gates.yaml`

### `enforcement/`

Gate enforcement rules

**Key Files:**
- `enforcement-spec.yaml`
- `validators/`

### `policies/`

Gate policies and approval workflows

**Key Files:**
- `gate-policies.yaml`
- `approval-matrix.yaml`

## Governance Attributes

This governance domain covers the following attributes:

- `gates`
- `gate_fidelity`
- `gatekeeper`
- `gateway`
- `gateways`

## Migration Sources

Files migrated from:

- `ecosystem/gates/operation-gate.yaml`
- `ecosystem/gates/self-auditor-config.yaml`
- `governance/workflows/research-loop/gates.yaml`

## Usage

See individual files for specific governance specifications and requirements.

## Compliance

This governance directory follows:
- GL (Governance Layers) semantic boundaries
- MNGA (Machine Native Governance Architecture)
- FHS+GL directory mapping standards

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-07  
**Maintained by**: IndestructibleAutoOps
