# Monitoring Dashboards

**Directory**: `grafana-governance/`  
**GL Layer**: N/A  
**Purpose**: Grafana dashboard and visualization specifications

---

## Overview

This directory contains governance specifications for Monitoring Dashboards.

## Directory Structure

### `core/grafana/dashboards/`

Dashboard specifications

**Key Files:**
- `core/grafana/dashboards/fallback-validation-dashboard.json`
- `core/grafana/dashboards/ng-governance-dashboard.json`
- `core/grafana/dashboards/parametric-convergence-dashboard.json`

### `core/grafana/provisioning/`

Provisioning configurations

**Key Files:**
- `core/grafana/provisioning/datasources.yaml`
- `core/grafana/provisioning/dashboards.yaml`

### `core/`

Monitoring stack configurations

**Key Files:**
- `core/monitoring-stack.yaml`
- `core/grafana/README.md`

## Governance Attributes

This governance domain covers the following attributes:

- `grafana`

## Migration Sources

Files migrated from:

- `monitoring/grafana/`
- `.github/config/providers/aws/infrastructure/monitoring-stack.yaml`

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
