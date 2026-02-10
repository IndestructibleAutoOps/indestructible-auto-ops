#!/bin/bash
# Root Environment Configuration
# GL Layer: Environment (GL90-99 Meta-Specification)
# Root layer environment configuration - initializes environment variables at startup

# ============================================================================
# Controlplane Paths (GL00-09 Strategic)
# ============================================================================
export CONTROLPLANE_PATH="./controlplane"
export CONTROLPLANE_CONFIG="${CONTROLPLANE_PATH}/config"
export CONTROLPLANE_SPECS="${CONTROLPLANE_PATH}/specifications"
export CONTROLPLANE_REGISTRIES="${CONTROLPLANE_PATH}/registries"
export CONTROLPLANE_VALIDATION="${CONTROLPLANE_PATH}/validation"

# ============================================================================
# Workspace Path (GL10-29 Operational)
# ============================================================================
export WORKSPACE_PATH="./workspace"

# ============================================================================
# FHS Paths (GL90-99 Meta-Specification)
# ============================================================================
export FHS_BIN="./bin"
export FHS_SBIN="./sbin"
export FHS_ETC="./etc"
export FHS_LIB="./lib"
export FHS_VAR="./var"
export FHS_USR="./usr"
export FHS_HOME="./home"
export FHS_TMP="./tmp"
export FHS_OPT="./opt"
export FHS_SRV="./srv"
export FHS_INITD="./init.d"

# ============================================================================
# Boot Mode (GL00-09 Strategic)
# ============================================================================
export BOOT_MODE="${BOOT_MODE:-production}"

# ============================================================================
# Version Information (GL90-99 Meta-Specification)
# ============================================================================
export MACHINENATIVEOPS_VERSION="v1.0.0"
export CONTROLPLANE_VERSION="v1.0.0"

# ============================================================================
# Environment Load Confirmation (GL50-59 Observability)
# ============================================================================
echo "✅ MachineNativeOps Taxonomy Root Layer environment loaded"
echo "   Controlplane: ${CONTROLPLANE_PATH}"
echo "   Workspace: ${WORKSPACE_PATH}"
echo "   Boot Mode: ${BOOT_MODE}"