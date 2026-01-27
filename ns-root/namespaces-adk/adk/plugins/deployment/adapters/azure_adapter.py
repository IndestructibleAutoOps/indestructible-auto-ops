"""
Azure Provider Adapter - Microsoft Azure Deployment
"""

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.core.exceptions import AzureError
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class AzureAdapter:
    """Azure cloud provider adapter implementation"""
    
    PROVIDER_NAME = "azure"
    PROVIDER_VERSION = "1.0.0"
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Azure adapter"""
        self.config = config
        
        # Initialize Azure clients
        self._init_clients()
    
    def _init_clients(self):
        """Initialize Azure clients"""
        try:
            credential = DefaultAzureCredential()
            
            self.resource_client = ResourceManagementClient(
                credential,
                self.config.get('subscription_id')
            )
            self.container_client = ContainerServiceClient(
                credential,
                self.config.get('subscription_id')
            )
            self.sql_client = SqlManagementClient(
                credential,
                self.config.get('subscription_id')
            )
            self.storage_client = StorageManagementClient(
                credential,
                self.config.get('subscription_id')
            )
            self.monitor_client = MonitorManagementClient(
                credential,
                self.config.get('subscription_id')
            )
            
            logger.info(f"Azure clients initialized for subscription: {self.config.get('subscription_id')}")
        except Exception as e:
            logger.error(f"Failed to initialize Azure clients: {e}")
            raise
    
    async def validate_config(self, config: dict) -> bool:
        """Validate Azure configuration"""
        required_fields = ['subscription_id', 'resource_group', 'location']
        
        for field in required_fields:
            if field not in config:
                logger.error(f"Missing required configuration field: {field}")
                return False
        
        return True
    
    async def deploy_infrastructure(self, infra_config: dict) -> dict:
        """Deploy Azure infrastructure"""
        logger.info(f"Deploying Azure infrastructure in {self.config.get('location')}")
        
        results = {}
        
        try:
            # Ensure resource group exists
            await self._ensure_resource_group()
            
            # Deploy VNet
            if 'vpc' in infra_config:
                results['vpc'] = await self._deploy_vnet(infra_config['vpc'])
            
            # Deploy AKS cluster
            if 'kubernetes' in infra_config:
                results['cluster'] = await self._deploy_aks_cluster(infra_config['kubernetes'])
            
            # Deploy databases
            if 'database' in infra_config:
                results['databases'] = await self._deploy_databases(infra_config['database'])
            
            # Deploy storage
            if 'storage' in infra_config:
                results['storage'] = await self._deploy_storage(infra_config['storage'])
            
            logger.info("Azure infrastructure deployment completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Failed to deploy Azure infrastructure: {e}")
            raise
    
    async def _ensure_resource_group(self) -> dict:
        """Ensure resource group exists"""
        rg_name = self.config.get('resource_group')
        location = self.config.get('location')
        
        logger.info(f"Ensuring resource group exists: {rg_name}")
        
        try:
            rg_result = self.resource_client.resource_groups.create_or_update(
                rg_name,
                {'location': location}
            )
            logger.info(f"Resource group ready: {rg_name}")
            return {
                'name': rg_name,
                'location': location,
                'id': rg_result.id
            }
        except AzureError as e:
            logger.error(f"Failed to create resource group: {e}")
            raise
    
    async def _deploy_vnet(self, vnet_config: dict) -> dict:
        """Deploy Virtual Network"""
        logger.info(f"Deploying Virtual Network: {vnet_config.get('name')}")
        
        vnet_name = vnet_config.get('name')
        rg_name = self.config.get('resource_group')
        location = self.config.get('location')
        
        # Build VNet parameters
        vnet_params = {
            'location': location,
            'address_space': {
                'address_prefixes': [vnet_config.get('address_space', '10.0.0.0/16')]
            },
            'subnets': [],
            'tags': vnet_config.get('tags', {})
        }
        
        # Create subnets
        for subnet_config in vnet_config.get('subnets', []):
            subnet = {
                'name': subnet_config['name'],
                'address_prefix': subnet_config['address_prefix']
            }
            vnet_params['subnets'].append(subnet)
        
        try:
            poller = self.resource_client.networks.begin_create_or_update(
                rg_name,
                vnet_name,
                vnet_params
            )
            vnet_result = poller.result()
            
            logger.info(f"Virtual Network deployed: {vnet_name}")
            
            return {
                'vnet_name': vnet_name,
                'vnet_id': vnet_result.id,
                'address_space': vnet_config.get('address_space'),
                'subnets': vnet_config.get('subnets', [])
            }
            
        except AzureError as e:
            logger.error(f"Failed to deploy Virtual Network: {e}")
            raise
    
    async def _deploy_aks_cluster(self, k8s_config: dict) -> dict:
        """Deploy AKS cluster"""
        logger.info(f"Deploying AKS cluster: {k8s_config.get('name')}")
        
        cluster_name = k8s_config['name']
        rg_name = self.config.get('resource_group')
        location = self.config.get('location')
        
        # Build cluster parameters
        cluster_params = {
            'location': location,
            'dns_prefix': k8s_config.get('name'),
            'kubernetes_version': k8s_config.get('version', '1.28'),
            'agent_pool_profiles': [],
            'identity': {
                'type': 'SystemAssigned'
            },
            'network_profile': {
                'network_plugin': k8s_config.get('network_plugin', 'kubenet'),
                'network_policy': k8s_config.get('network_policy', 'calico'),
                'load_balancer_sku': 'standard',
                'outbound_type': k8s_config.get('outbound_type', 'loadBalancer')
            },
            'tags': k8s_config.get('tags', {})
        }
        
        # Configure private cluster
        if k8s_config.get('private_cluster', False):
            cluster_params['api_server_access_profile'] = {
                'enable_private_cluster': True,
                'private_dns_zone': k8s_config.get('private_dns_zone', 'System')
            }
        
        # Create node pools
        for node_pool in k8s_config.get('node_pools', []):
            pool_profile = {
                'name': node_pool['name'],
                'count': node_pool.get('node_count', 3),
                'vm_size': node_pool.get('vm_size', 'Standard_DS2_v2'),
                'os_type': 'Linux',
                'mode': node_pool.get('mode', 'System'),
                'enable_auto_scaling': node_pool.get('enable_auto_scaling', False),
                'min_count': node_pool.get('min_count', 1),
                'max_count': node_pool.get('max_count', 10),
                'os_disk_size_gb': node_pool.get('disk_size_gb', 120),
                'type': 'VirtualMachineScaleSets'
            }
            
            # Add node taints
            if node_pool.get('taints'):
                pool_profile['taints'] = node_pool['taints']
            
            # Add node labels
            if node_pool.get('labels'):
                pool_profile['labels'] = node_pool['labels']
            
            cluster_params['agent_pool_profiles'].append(pool_profile)
        
        try:
            poller = self.container_client.managed_clusters.begin_create_or_update(
                rg_name,
                cluster_name,
                cluster_params
            )
            cluster_result = poller.result()
            
            logger.info(f"AKS cluster deployed: {cluster_name}")
            
            return {
                'cluster_name': cluster_name,
                'cluster_id': cluster_result.id,
                'fqdn': cluster_result.fqdn,
                'kubernetes_version': k8s_config.get('version', '1.28'),
                'node_count': sum(np['count'] for np in cluster_params['agent_pool_profiles'])
            }
            
        except AzureError as e:
            logger.error(f"Failed to deploy AKS cluster: {e}")
            raise
    
    async def _deploy_databases(self, db_config: dict) -> List[dict]:
        """Deploy Azure SQL instances"""
        logger.info("Deploying Azure SQL instances")
        
        databases = []
        for instance_config in db_config.get('instances', []):
            db = await self._create_azure_sql_instance(instance_config)
            databases.append(db)
        
        return databases
    
    async def _create_azure_sql_instance(self, db_config: dict) -> dict:
        """Create Azure SQL instance"""
        logger.info(f"Creating Azure SQL instance: {db_config['name']}")
        
        server_name = db_config['name']
        rg_name = self.config.get('resource_group')
        location = self.config.get('location')
        
        # Build server parameters
        server_params = {
            'location': location,
            'administrator_login': db_config['admin_username'],
            'administrator_login_password': db_config['admin_password'],
            'version': db_config.get('version', '12.0'),
            'tags': db_config.get('tags', {})
        }
        
        try:
            # Create SQL server
            poller = self.sql_client.servers.begin_create_or_update(
                rg_name,
                server_name,
                server_params
            )
            server_result = poller.result()
            
            # Create database
            db_params = {
                'location': location,
                'sku': {
                    'name': db_config.get('sku_name', 'GP_Gen5_2'),
                    'tier': db_config.get('tier', 'GeneralPurpose'),
                    'capacity': db_config.get('vcores', 2)
                },
                'max_size_bytes': db_config.get('max_size_bytes', 107374182400),
                'tags': db_config.get('tags', {})
            }
            
            db_poller = self.sql_client.databases.begin_create_or_update(
                rg_name,
                server_name,
                db_config.get('database_name', 'master'),
                db_params
            )
            db_result = db_poller.result()
            
            logger.info(f"Azure SQL instance deployed: {server_name}")
            
            return {
                'server_name': server_name,
                'database_name': db_config.get('database_name', 'master'),
                'server_id': server_result.id,
                'database_id': db_result.id,
                'endpoint': f"{server_name}.database.windows.net"
            }
            
        except AzureError as e:
            logger.error(f"Failed to create Azure SQL instance: {e}")
            raise
    
    async def _deploy_storage(self, storage_config: dict) -> List[dict]:
        """Deploy Storage Accounts"""
        logger.info("Deploying Storage Accounts")
        
        storage_accounts = []
        for account_config in storage_config.get('accounts', []):
            account = await self._create_storage_account(account_config)
            storage_accounts.append(account)
        
        return storage_accounts
    
    async def _create_storage_account(self, storage_config: dict) -> dict:
        """Create Storage Account"""
        logger.info(f"Creating Storage Account: {storage_config['name']}")
        
        account_name = storage_config['name']
        rg_name = self.config.get('resource_group')
        location = self.config.get('location')
        
        # Build storage account parameters
        account_params = {
            'location': location,
            'sku': {
                'name': storage_config.get('sku', 'Standard_LRS')
            },
            'kind': storage_config.get('kind', 'StorageV2'),
            'access_tier': storage_config.get('access_tier', 'Hot'),
            'tags': storage_config.get('tags', {}),
            'properties': {
                'allow_blob_public_access': storage_config.get('allow_public_access', False),
                'minimum_tls_version': storage_config.get('minimum_tls_version', 'TLS1_2')
            }
        }
        
        try:
            # Create storage account
            poller = self.storage_client.storage_accounts.begin_create(
                rg_name,
                account_name,
                account_params
            )
            account_result = poller.result()
            
            # Create blob containers
            containers = []
            for container_config in storage_config.get('containers', []):
                container = await self._create_blob_container(
                    account_name,
                    account_result.primary_endpoints.blob,
                    container_config
                )
                containers.append(container)
            
            logger.info(f"Storage Account deployed: {account_name}")
            
            return {
                'account_name': account_name,
                'account_id': account_result.id,
                'primary_endpoints': account_result.primary_endpoints,
                'containers': containers
            }
            
        except AzureError as e:
            logger.error(f"Failed to create Storage Account: {e}")
            raise
    
    async def _create_blob_container(self, account_name: str, endpoint: str, container_config: dict) -> dict:
        """Create blob container"""
        from azure.storage.blob import BlobServiceClient
        from azure.core.credentials import AzureNamedKeyCredential
        
        logger.info(f"Creating blob container: {container_config['name']}")
        
        # Create blob service client
        credential = DefaultAzureCredential()
        blob_service = BlobServiceClient(
            account_url=endpoint,
            credential=credential
        )
        
        # Create container
        container_client = blob_service.get_container_client(container_config['name'])
        container_client.create_container(
            metadata=container_config.get('metadata', {})
        )
        
        # Set access level
        if container_config.get('public_access'):
            container_client.set_container_access_policy(
                public_access=container_config.get('public_access')
            )
        
        return {
            'name': container_config['name'],
            'access_level': container_config.get('access_level', 'private')
        }
    
    async def get_resource(self, resource_id: str) -> dict:
        """Get resource details"""
        logger.info(f"Getting resource: {resource_id}")
        
        return {
            'resource_id': resource_id,
            'status': 'available'
        }
    
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete resource"""
        logger.info(f"Deleting resource: {resource_id}")
        
        return True
    
    async def get_metrics(self, resource_id: str) -> dict:
        """Get resource metrics"""
        logger.info(f"Getting metrics for resource: {resource_id}")
        
        return {
            'resource_id': resource_id,
            'metrics': {
                'cpu_utilization': 0.0,
                'memory_utilization': 0.0,
                'disk_io': 0.0,
                'network_io': 0.0
            }
        }
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider information"""
        return {
            'provider_name': self.PROVIDER_NAME,
            'provider_version': self.PROVIDER_VERSION,
            'subscription_id': self.config.get('subscription_id'),
            'resource_group': self.config.get('resource_group'),
            'location': self.config.get('location'),
            'available_services': [
                'aks', 'azure-sql', 'storage', 'monitor', 'functions',
                'cosmos-db', 'service-bus', 'event-hubs'
            ]
        }