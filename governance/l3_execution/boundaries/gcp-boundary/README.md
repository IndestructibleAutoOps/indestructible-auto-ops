# Google Cloud Platform

**Directory**: `gcp-governance/`  
**GL Layer**: N/A  
**Purpose**: GCP infrastructure specifications and configurations

---

## Overview

This directory contains governance specifications for Google Cloud Platform.

## Directory Structure

### `infrastructure/`

GCP infrastructure specifications

**Key Files:**
- `gcp-infrastructure.yaml`
- `gke-spec.yaml`

### `monitoring/`

GCP monitoring configurations

**Key Files:**
- `monitoring-stack.yaml`
- `logging-spec.yaml`

### `security/`

GCP security specifications

**Key Files:**
- `security-spec.yaml`
- `iam-policies.yaml`

## Governance Attributes

This governance domain covers the following attributes:

- `gcp`
- `gcp_project`
- `gcp_bucket`
- `gcp_cloud_logging`
- `gcp_compute`
- `gcp_endpoint`
- `gcp_pubsub`
- `gcp_secret_manager`
- `gcp_service_account_key`
- `gcp_storage`
- `gke_cluster`
- `gcs`

## Migration Sources

Files migrated from:

- `.github/config/providers/gcp/`

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
