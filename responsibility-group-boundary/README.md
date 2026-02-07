# Resource Grouping

**Directory**: `group-governance/`  
**GL Layer**: N/A  
**Purpose**: Resource grouping and organization

---

## Overview

This directory contains governance specifications for Resource Grouping.

## Directory Structure

### `policies/`

Grouping policies and rules

**Key Files:**
- `grouping-policies.yaml`
- `rules.yaml`

### `workflows/`

Workflow grouping configurations

**Key Files:**
- `workflow-groups.yaml`
- `concurrency.yaml`

### `monitoring/`

Monitoring group configurations

**Key Files:**
- `alert-groups.yaml`
- `metric-groups.yaml`

## Governance Attributes

This governance domain covers the following attributes:

- `group`
- `groups`
- `group_by`
- `group_wait`
- `group_interval`

## Migration Sources

Files migrated from:

- `.github/workflows-quantum/monitoring/workflow-monitor.yml`

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
