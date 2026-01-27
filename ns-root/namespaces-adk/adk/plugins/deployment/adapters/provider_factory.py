"""
Provider Adapter Factory - Creates provider-specific adapters
"""

from typing import Dict, Type, Any
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class ProviderAdapter(ABC):
    """Abstract base class for all provider adapters"""
    
    @abstractmethod
    async def deploy_infrastructure(self, config: dict) -> dict:
        """Deploy infrastructure resources"""
        pass
    
    @abstractmethod
    async def get_resource(self, resource_id: str) -> dict:
        """Get resource details"""
        pass
    
    @abstractmethod
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete resource"""
        pass
    
    @abstractmethod
    async def get_metrics(self, resource_id: str) -> dict:
        """Get resource metrics"""
        pass
    
    @abstractmethod
    async def validate_config(self, config: dict) -> bool:
        """Validate configuration"""
        pass
    
    @abstractmethod
    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider information"""
        pass


class ProviderAdapterFactory:
    """Factory for creating provider adapters"""
    
    _adapters: Dict[str, Type[ProviderAdapter]] = {}
    
    @classmethod
    def register_adapter(cls, provider_name: str, adapter_class: Type[ProviderAdapter]):
        """Register a provider adapter"""
        cls._adapters[provider_name] = adapter_class
        logger.info(f"Registered adapter for provider: {provider_name}")
    
    @classmethod
    def get_adapter(cls, provider_name: str, config: dict) -> ProviderAdapter:
        """Get adapter instance for provider"""
        adapter_class = cls._adapters.get(provider_name)
        
        if adapter_class is None:
            available = ', '.join(cls._adapters.keys())
            raise ValueError(
                f"Unknown provider: {provider_name}. "
                f"Available providers: {available}"
            )
        
        return adapter_class(config)
    
    @classmethod
    def list_providers(cls) -> list:
        """List all registered providers"""
        return list(cls._adapters.keys())
    
    @classmethod
    def is_provider_supported(cls, provider_name: str) -> bool:
        """Check if provider is supported"""
        return provider_name in cls._adapters


# Import and register adapters
def _register_adapters():
    """Register all available adapters"""
    try:
        from .aws_adapter import AWSAdapter
        ProviderAdapterFactory.register_adapter('aws', AWSAdapter)
        ProviderAdapterFactory.register_adapter('aws-eks', AWSAdapter)
    except ImportError:
        logger.debug("AWS adapter not available")
    
    try:
        from .gcp_adapter import GCPAdapter
        ProviderAdapterFactory.register_adapter('gcp', GCPAdapter)
        ProviderAdapterFactory.register_adapter('gcp-gke', GCPAdapter)
    except ImportError:
        logger.debug("GCP adapter not available")
    
    try:
        from .azure_adapter import AzureAdapter
        ProviderAdapterFactory.register_adapter('azure', AzureAdapter)
        ProviderAdapterFactory.register_adapter('azure-aks', AzureAdapter)
    except ImportError:
        logger.debug("Azure adapter not available")
    
    try:
        from .kubernetes_adapter import KubernetesAdapter
        ProviderAdapterFactory.register_adapter('kubernetes', KubernetesAdapter)
        ProviderAdapterFactory.register_adapter('k8s', KubernetesAdapter)
    except ImportError:
        logger.debug("Kubernetes adapter not available")
    
    try:
        from .docker_compose_adapter import DockerComposeAdapter
        ProviderAdapterFactory.register_adapter('docker-compose', DockerComposeAdapter)
        ProviderAdapterFactory.register_adapter('docker', DockerComposeAdapter)
    except ImportError:
        logger.debug("Docker Compose adapter not available")


# Register adapters on module import
_register_adapters()