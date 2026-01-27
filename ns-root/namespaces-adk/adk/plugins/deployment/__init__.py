"""
Deployment Plugin - Pluggable Architecture for Universal Deployment
"""

from .managers.deployment_manager import UniversalDeploymentManager
from .adapters.provider_factory import ProviderAdapterFactory
from .adapters.aws_adapter import AWSAdapter
from .adapters.gcp_adapter import GCPAdapter
from .adapters.azure_adapter import AzureAdapter
from .adapters.kubernetes_adapter import KubernetesAdapter
from .adapters.docker_compose_adapter import DockerComposeAdapter
from .detectors.environment_detector import EnvironmentDetector
from .loaders.config_loader import ConfigLoader

# Infrastructure components
from .infrastructure import (
    AutoScalingManager,
    DatabaseBackupManager,
    IaCManager,
    MonitoringStackManager,
    SecretsManager,
    ContainerOrchestrationManager,
    DisasterRecoveryManager,
    LogAggregationManager,
    PerformanceMonitoringManager
)

__all__ = [
    'UniversalDeploymentManager',
    'ProviderAdapterFactory',
    'AWSAdapter',
    'GCPAdapter',
    'AzureAdapter',
    'KubernetesAdapter',
    'DockerComposeAdapter',
    'EnvironmentDetector',
    'ConfigLoader',
    'AutoScalingManager',
    'DatabaseBackupManager',
    'IaCManager',
    'MonitoringStackManager',
    'SecretsManager',
    'ContainerOrchestrationManager',
    'DisasterRecoveryManager',
    'LogAggregationManager',
    'PerformanceMonitoringManager'
]