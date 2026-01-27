"""
Configuration Loader - Enhanced hierarchical configuration loading with deep merge and secret support
"""

import os
import yaml
import json
from typing import Dict, Optional, Any
from pathlib import Path
import logging
import re
from copy import deepcopy

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Enhanced configuration loader with hierarchical merging and secret support"""
    
    def __init__(self, base_path: Optional[str] = None):
        """Initialize config loader"""
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.config_cache = {}
        self.secrets_cache = {}
    
    def load_config(
        self,
        provider: str,
        environment: str = 'production',
        config_file: Optional[str] = None,
        include_secrets: bool = True
    ) -> Dict[str, Any]:
        """
        Load configuration for provider and environment with hierarchical merging
        
        Loading order (later configs override earlier ones):
        1. Base Configuration (provider-agnostic defaults)
        2. Provider Configuration (provider-specific settings)
        3. Environment Configuration (environment-specific settings)
        4. Provider + Environment Configuration (provider-specific environment settings)
        5. Custom Configuration (user-provided config file)
        6. Environment Variables (highest priority)
        """
        logger.info(f"Loading configuration for provider: {provider}, environment: {environment}")
        
        # Start with empty config
        config = {}
        
        # Step 1: Load base configuration
        logger.debug("Step 1: Loading base configuration")
        base_config = self._load_base_config()
        config = self._deep_merge(config, base_config)
        logger.debug(f"Base config keys: {list(config.keys())}")
        
        # Step 2: Load provider-specific configuration
        logger.debug("Step 2: Loading provider configuration")
        provider_config = self._load_provider_config(provider)
        config = self._deep_merge(config, provider_config)
        logger.debug(f"After provider merge keys: {list(config.keys())}")
        
        # Step 3: Load environment-specific configuration
        logger.debug("Step 3: Loading environment configuration")
        env_config = self._load_environment_config(environment)
        config = self._deep_merge(config, env_config)
        logger.debug(f"After environment merge keys: {list(config.keys())}")
        
        # Step 4: Load provider + environment configuration
        logger.debug("Step 4: Loading provider + environment configuration")
        provider_env_config = self._load_provider_environment_config(provider, environment)
        config = self._deep_merge(config, provider_env_config)
        logger.debug(f"After provider+env merge keys: {list(config.keys())}")
        
        # Step 5: Load custom config file if specified
        if config_file:
            logger.debug(f"Step 5: Loading custom config file: {config_file}")
            custom_config = self._load_config_file(config_file)
            config = self._deep_merge(config, custom_config)
            logger.debug(f"After custom config merge keys: {list(config.keys())}")
        
        # Step 6: Override with environment variables
        logger.debug("Step 6: Applying environment variable overrides")
        config = self._apply_env_overrides(config)
        
        # Step 7: Load secrets if enabled
        if include_secrets:
            logger.debug("Step 7: Loading secrets")
            secrets = self._load_secrets(provider, environment)
            config = self._deep_merge(config, secrets)
        
        # Add metadata
        config['_metadata'] = {
            'provider': provider,
            'environment': environment,
            'config_file': config_file
        }
        
        # Validate configuration
        logger.debug("Validating configuration")
        self._validate_config(config)
        
        logger.info(f"Configuration loaded successfully with {len(config)} top-level keys")
        return config
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries
        
        Strategy:
        - If both values are dicts, merge recursively
        - If both values are lists, concatenate (override takes precedence)
        - Otherwise, override value takes precedence
        """
        result = deepcopy(base)
        
        for key, value in override.items():
            if key in result:
                # Both have the key, need to merge
                base_value = result[key]
                
                if isinstance(base_value, dict) and isinstance(value, dict):
                    # Both are dicts, merge recursively
                    result[key] = self._deep_merge(base_value, value)
                elif isinstance(base_value, list) and isinstance(value, list):
                    # Both are lists, concatenate
                    result[key] = base_value + value
                else:
                    # Override with new value
                    result[key] = deepcopy(value)
            else:
                # New key, just add it
                result[key] = deepcopy(value)
        
        return result
    
    def _load_base_config(self) -> Dict[str, Any]:
        """Load base configuration"""
        config_paths = [
            self.base_path / 'config' / 'base' / 'application.yaml',
            self.base_path / 'config' / 'base' / 'services.yaml',
            self.base_path / 'config' / 'base' / 'monitoring.yaml',
            self.base_path / 'config' / 'base' / 'security.yaml',
            self.base_path / 'config' / 'base' / 'networking.yaml'
        ]
        
        config = {}
        for config_path in config_paths:
            if config_path.exists():
                logger.debug(f"Loading base config: {config_path}")
                file_config = self._load_yaml_file(config_path)
                config = self._deep_merge(config, file_config)
        
        return config
    
    def _load_provider_config(self, provider: str) -> Dict[str, Any]:
        """Load provider-specific configuration"""
        config_paths = [
            self.base_path / 'config' / 'providers' / provider / 'infrastructure.yaml',
            self.base_path / 'config' / 'providers' / provider / 'databases.yaml',
            self.base_path / 'config' / 'providers' / provider / 'storage.yaml',
            self.base_path / 'config' / 'providers' / provider / 'monitoring.yaml',
            self.base_path / 'config' / 'providers' / provider / 'networking.yaml',
            self.base_path / 'config' / 'providers' / provider / 'security.yaml'
        ]
        
        config = {}
        for config_path in config_paths:
            if config_path.exists():
                logger.debug(f"Loading provider config: {config_path}")
                file_config = self._load_yaml_file(config_path)
                config = self._deep_merge(config, file_config)
        
        return config
    
    def _load_environment_config(self, environment: str) -> Dict[str, Any]:
        """Load environment-specific configuration"""
        config_paths = [
            self.base_path / 'config' / 'environments' / f'{environment}.yaml',
            self.base_path / 'config' / 'environments' / environment / 'settings.yaml'
        ]
        
        config = {}
        for config_path in config_paths:
            if config_path.exists():
                logger.debug(f"Loading environment config: {config_path}")
                file_config = self._load_yaml_file(config_path)
                config = self._deep_merge(config, file_config)
        
        return config
    
    def _load_provider_environment_config(self, provider: str, environment: str) -> Dict[str, Any]:
        """Load provider-specific environment configuration"""
        config_paths = [
            self.base_path / 'config' / 'providers' / provider / 'environments' / f'{environment}.yaml',
            self.base_path / 'config' / 'providers' / provider / 'environments' / environment / 'settings.yaml'
        ]
        
        config = {}
        for config_path in config_paths:
            if config_path.exists():
                logger.debug(f"Loading provider+environment config: {config_path}")
                file_config = self._load_yaml_file(config_path)
                config = self._deep_merge(config, file_config)
        
        return config
    
    def _load_config_file(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from file"""
        config_path = Path(config_file)
        
        # If relative path, make it relative to base_path
        if not config_path.is_absolute():
            config_path = self.base_path / config_path
        
        if not config_path.exists():
            logger.warning(f"Config file not found: {config_path}")
            return {}
        
        logger.debug(f"Loading config file: {config_path}")
        
        if config_path.suffix in ['.yaml', '.yml']:
            return self._load_yaml_file(config_path)
        elif config_path.suffix == '.json':
            return self._load_json_file(config_path)
        else:
            logger.warning(f"Unsupported config file format: {config_path.suffix}")
            return {}
    
    def _load_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """Load YAML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as config_file:
                content = yaml.safe_load(config_file)
                return content if isinstance(content, dict) else {}
        except Exception as e:
            logger.error(f"Error loading YAML file {file_path}: {e}")
            return {}
    
    def _load_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as config_file:
                content = json.load(config_file)
                return content if isinstance(content, dict) else {}
        except Exception as e:
            logger.error(f"Error loading JSON file {file_path}: {e}")
            return {}
    
    def _apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply environment variable overrides
        
        Format: PROVIDER__SECTION__KEY=VALUE
        Examples:
          AWS__INFRASTRUCTURE__VPC__CIDR=10.1.0.0/16
          KUBERNETES__DEPLOYMENT__REPLICAS=5
          DOCKER_COMPOSE__SERVICES__API_SERVER__PORT=8080
        """
        overrides = {}
        
        # Pattern for env vars: PROVIDER__SECTION__KEY
        pattern = re.compile(r'^([A-Z_]+)__([A-Z_]+)__([A-Z_]+)$')
        
        for env_key, env_value in os.environ.items():
            match = pattern.match(env_key)
            if match:
                provider, section, key = match.groups()
                
                # Convert to lowercase and underscores to hyphens
                section = section.lower().replace('_', '-')
                key = key.lower().replace('_', '-')
                
                logger.debug(f"Applying env override: {env_key} -> {section}.{key}")
                
                # Try to convert to appropriate type
                parsed_value = self._parse_env_value(env_value)
                
                # Build nested structure
                if section not in overrides:
                    overrides[section] = {}
                overrides[section][key] = parsed_value
        
        # Merge overrides into config
        return self._deep_merge(config, overrides)
    
    def _parse_env_value(self, value: str) -> Any:
        """Parse environment variable value to appropriate type"""
        # Try boolean
        if value.lower() in ['true', 'yes', '1']:
            return True
        elif value.lower() in ['false', 'no', '0']:
            return False
        
        # Try integer
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Try JSON (for arrays and nested objects)
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
        
        # Default to string
        return value
    
    def _load_secrets(self, provider: str, environment: str) -> Dict[str, Any]:
        """
        Load secrets from various sources
        
        Priority:
        1. Secrets from secrets provider (e.g., AWS Secrets Manager, Vault)
        2. Secrets from environment variables (format: SECRET__KEY)
        3. Secrets from secrets file (config/providers/{provider}/secrets.yaml)
        """
        secrets = {}
        
        # 1. Load from environment variables (format: SECRET__KEY)
        env_secrets = self._load_secrets_from_env()
        secrets = self._deep_merge(secrets, env_secrets)
        
        # 2. Load from secrets file
        file_secrets = self._load_secrets_from_file(provider, environment)
        secrets = self._deep_merge(secrets, file_secrets)
        
        # 3. Load from secrets provider if available
        provider_secrets = self._load_secrets_from_provider(provider, environment)
        secrets = self._deep_merge(secrets, provider_secrets)
        
        return secrets
    
    def _load_secrets_from_env(self) -> Dict[str, Any]:
        """Load secrets from environment variables"""
        secrets = {}
        
        for env_key, env_value in os.environ.items():
            if env_key.startswith('SECRET__'):
                # Convert SECRET__KEY to secrets.key
                key = env_key[8:].lower().replace('_', '-')
                secrets[key] = env_value
                logger.debug(f"Loaded secret from env: {key}")
        
        return secrets
    
    def _load_secrets_from_file(self, provider: str, environment: str) -> Dict[str, Any]:
        """Load secrets from secrets file"""
        secrets_file = (
            self.base_path / 'config' / 'providers' / provider / 'secrets.yaml'
        )
        
        if secrets_file.exists():
            logger.debug(f"Loading secrets from file: {secrets_file}")
            return self._load_yaml_file(secrets_file)
        
        return {}
    
    def _load_secrets_from_provider(self, provider: str, environment: str) -> Dict[str, Any]:
        """
        Load secrets from secrets provider
        
        Supported providers:
        - AWS: AWS Secrets Manager
        - GCP: Secret Manager
        - Azure: Key Vault
        - Kubernetes: Kubernetes Secrets
        - Vault: HashiCorp Vault
        """
        secrets = {}
        
        try:
            if provider == 'aws':
                secrets = self._load_aws_secrets(environment)
            elif provider == 'gcp':
                secrets = self._load_gcp_secrets(environment)
            elif provider == 'azure':
                secrets = self._load_azure_secrets(environment)
            elif provider == 'kubernetes':
                secrets = self._load_kubernetes_secrets(environment)
            elif provider.startswith('aws-'):
                secrets = self._load_aws_secrets(environment)
            elif provider.startswith('gcp-'):
                secrets = self._load_gcp_secrets(environment)
            elif provider.startswith('azure-'):
                secrets = self._load_azure_secrets(environment)
        except Exception as e:
            logger.warning(f"Error loading secrets from provider: {e}")
        
        return secrets
    
    def _load_aws_secrets(self, environment: str) -> Dict[str, Any]:
        """Load secrets from AWS Secrets Manager"""
        try:
            import boto3
            
            client = boto3.client('secretsmanager')
            secret_name = f"machine-native-ops/{environment}"
            
            response = client.get_secret_value(SecretId=secret_name)
            secret_string = response.get('SecretString', '{}')
            
            secrets = json.loads(secret_string)
            logger.debug(f"Loaded {len(secrets)} secrets from AWS Secrets Manager")
            
            return secrets
            
        except ImportError:
            logger.debug("boto3 not available, skipping AWS Secrets Manager")
            return {}
        except Exception as e:
            logger.debug(f"Error loading AWS secrets: {e}")
            return {}
    
    def _load_gcp_secrets(self, environment: str) -> Dict[str, Any]:
        """Load secrets from GCP Secret Manager"""
        try:
            from google.cloud import secretmanager
            
            client = secretmanager.SecretManagerServiceClient()
            
            # List secrets with prefix
            project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', '')
            parent = f"projects/{project_id}"
            
            secrets = {}
            for secret in client.list_secrets(request={"parent": parent}):
                if environment in secret.name:
                    # Get secret version
                    secret_path = f"{secret.name}/versions/latest"
                    response = client.access_secret_version(request={"name": secret_path})
                    
                    # Parse secret name
                    secret_key = secret.name.split('/')[-1].lower().replace('_', '-')
                    secrets[secret_key] = response.payload.data.decode('UTF-8')
            
            logger.debug(f"Loaded {len(secrets)} secrets from GCP Secret Manager")
            return secrets
            
        except ImportError:
            logger.debug("google-cloud-secret-manager not available, skipping GCP Secret Manager")
            return {}
        except Exception as e:
            logger.debug(f"Error loading GCP secrets: {e}")
            return {}
    
    def _load_azure_secrets(self, environment: str) -> Dict[str, Any]:
        """Load secrets from Azure Key Vault"""
        try:
            from azure.keyvault.secrets import SecretClient
            from azure.identity import DefaultAzureCredential
            
            vault_url = os.environ.get('AZURE_KEYVAULT_URL')
            if not vault_url:
                return {}
            
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=vault_url, credential=credential)
            
            secrets = {}
            secret_properties = client.list_properties_of_secrets()
            
            for secret_prop in secret_properties:
                if environment in secret_prop.name:
                    secret = client.get_secret(secret_prop.name)
                    secret_key = secret_prop.name.lower().replace('_', '-')
                    secrets[secret_key] = secret.value
            
            logger.debug(f"Loaded {len(secrets)} secrets from Azure Key Vault")
            return secrets
            
        except ImportError:
            logger.debug("azure-identity or azure-keyvault-secrets not available")
            return {}
        except Exception as e:
            logger.debug(f"Error loading Azure secrets: {e}")
            return {}
    
    def _load_kubernetes_secrets(self, environment: str) -> Dict[str, Any]:
        """Load secrets from Kubernetes Secrets"""
        try:
            from kubernetes import client, config
            
            # Load config
            try:
                config.load_incluster_config()
            except config.ConfigException:
                config.load_kube_config()
            
            v1 = client.CoreV1Api()
            
            # Get namespace
            namespace = os.environ.get('POD_NAMESPACE', 'default')
            
            # List secrets
            secrets = {}
            secret_list = v1.list_namespaced_secret(namespace=namespace)
            
            for secret in secret_list.items:
                # Only load secrets with specific label or name pattern
                if environment in secret.metadata.name.lower():
                    secret_key = secret.metadata.name.lower().replace('_', '-')
                    secrets[secret_key] = {
                        'data': secret.data,
                        'type': secret.type
                    }
            
            logger.debug(f"Loaded {len(secrets)} secrets from Kubernetes")
            return secrets
            
        except ImportError:
            logger.debug("kubernetes not available")
            return {}
        except Exception as e:
            logger.debug(f"Error loading Kubernetes secrets: {e}")
            return {}
    
    def _validate_config(self, config: Dict[str, Any]):
        """Validate configuration"""
        # Basic validation
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")
        
        # Check for required fields based on provider
        provider = config.get('_metadata', {}).get('provider')
        if provider:
            self._validate_provider_config(provider, config)
    
    def _validate_provider_config(self, provider: str, config: Dict[str, Any]):
        """Validate provider-specific configuration"""
        # Add provider-specific validation rules
        if provider in ['aws', 'aws-eks']:
            # AWS validation
            infrastructure = config.get('infrastructure', {})
            if infrastructure.get('vpc', {}).get('enabled'):
                cidr = infrastructure.get('vpc', {}).get('cidr')
                if not cidr:
                    logger.warning("AWS VPC enabled but no CIDR specified")
        
        elif provider in ['gcp', 'gcp-gke']:
            # GCP validation
            infrastructure = config.get('infrastructure', {})
            if infrastructure.get('kubernetes', {}).get('enabled'):
                project = config.get('provider', {}).get('project')
                if not project:
                    logger.warning("GCP GKE enabled but no project specified")
        
        elif provider in ['azure', 'azure-aks']:
            # Azure validation
            infrastructure = config.get('infrastructure', {})
            if infrastructure.get('kubernetes', {}).get('enabled'):
                subscription_id = config.get('provider', {}).get('subscription_id')
                if not subscription_id:
                    logger.warning("Azure AKS enabled but no subscription_id specified")