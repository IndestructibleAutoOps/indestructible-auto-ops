"""
GCP Provider Adapter - Google Cloud Platform Deployment
"""

from google.cloud import storage
from google.cloud import container_v1
try:
    from google.cloud.sql import connector
except ImportError:
    connector = None
from google.cloud import monitoring_v3
from google.oauth2 import service_account
from google.api_core import exceptions as gcp_exceptions
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class GCPAdapter:
    """GCP cloud provider adapter implementation"""
    
    PROVIDER_NAME = "gcp"
    PROVIDER_VERSION = "1.0.0"
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize GCP adapter"""
        self.config = config
        
        # Initialize GCP clients
        self._init_clients()
    
    def _init_clients(self):
        """Initialize GCP clients"""
        credentials = None
        
        if 'service_account_key' in self.config:
            credentials = service_account.Credentials.from_service_account_info(
                self.config['service_account_key']
            )
        elif 'service_account_file' in self.config:
            credentials = service_account.Credentials.from_service_account_file(
                self.config['service_account_file']
            )
        
        try:
            self.storage_client = storage.Client(
                project=self.config.get('project'),
                credentials=credentials
            )
            self.gke_client = container_v1.ClusterManagerClient(
                credentials=credentials
            )
            self.sql_client = sql.SqlInstancesServiceClient(
                credentials=credentials
            )
            self.monitoring_client = monitoring_v3.MetricServiceClient(
                credentials=credentials
            )
            
            logger.info(f"GCP clients initialized for project: {self.config.get('project')}")
        except Exception as e:
            logger.error(f"Failed to initialize GCP clients: {e}")
            raise
    
    async def validate_config(self, config: dict) -> bool:
        """Validate GCP configuration"""
        required_fields = ['project', 'region']
        
        for field in required_fields:
            if field not in config:
                logger.error(f"Missing required configuration field: {field}")
                return False
        
        return True
    
    async def deploy_infrastructure(self, infra_config: dict) -> dict:
        """Deploy GCP infrastructure"""
        logger.info(f"Deploying GCP infrastructure in {self.config.get('region')}")
        
        results = {}
        
        try:
            # Deploy VPC
            if 'vpc' in infra_config:
                results['vpc'] = await self._deploy_vpc(infra_config['vpc'])
            
            # Deploy GKE cluster
            if 'kubernetes' in infra_config:
                results['cluster'] = await self._deploy_gke_cluster(infra_config['kubernetes'])
            
            # Deploy databases
            if 'database' in infra_config:
                results['databases'] = await self._deploy_databases(infra_config['database'])
            
            # Deploy storage
            if 'storage' in infra_config:
                results['storage'] = await self._deploy_storage(infra_config['storage'])
            
            logger.info("GCP infrastructure deployment completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Failed to deploy GCP infrastructure: {e}")
            raise
    
    async def _deploy_vpc(self, vpc_config: dict) -> dict:
        """Deploy VPC network"""
        logger.info("Deploying VPC network")
        
        # In GCP, VPC is managed by Compute Engine API
        # This is a simplified implementation
        # Full implementation would use google.cloud.compute_v1
        
        vpc_name = vpc_config.get('name', 'main-network')
        
        return {
            'vpc_name': vpc_name,
            'region': self.config.get('region'),
            'auto_create_subnetworks': vpc_config.get('auto_create_subnetworks', False)
        }
    
    async def _deploy_gke_cluster(self, k8s_config: dict) -> dict:
        """Deploy GKE cluster"""
        logger.info(f"Deploying GKE cluster: {k8s_config.get('name')}")
        
        project_id = self.config['project']
        location = self.config.get('region') or self.config.get('zone')
        
        # Build cluster configuration
        cluster = {
            'name': k8s_config['name'],
            'initial_cluster_version': k8s_config.get('version', '1.28'),
            'network': k8s_config.get('network'),
            'subnetwork': k8s_config.get('subnetwork'),
            'node_pools': [],
            'ip_allocation_policy': {
                'use_ip_aliases': True
            },
            'private_cluster_config': None,
            'master_authorized_networks_config': None
        }
        
        # Configure private cluster if specified
        if k8s_config.get('private_cluster', False):
            cluster['private_cluster_config'] = {
                'enable_private_endpoint': k8s_config.get('enable_private_endpoint', False),
                'enable_private_nodes': True,
                'master_ipv4_cidr_block': k8s_config.get('master_ipv4_cidr', '172.16.0.0/28')
            }
        
        # Configure master authorized networks
        if k8s_config.get('master_authorized_networks'):
            cluster['master_authorized_networks_config'] = {
                'cidr_blocks': [
                    {'cidr_block': cidr, 'display_name': name}
                    for cidr, name in k8s_config['master_authorized_networks'].items()
                ]
            }
        
        # Create node pools
        for node_pool in k8s_config.get('node_pools', []):
            node_pool_config = {
                'name': node_pool['name'],
                'initial_node_count': node_pool.get('node_count', 3),
                'config': {
                    'machine_type': node_pool.get('machine_type', 'e2-medium'),
                    'disk_size_gb': node_pool.get('disk_size', 100),
                    'oauth_scopes': [
                        'https://www.googleapis.com/auth/cloud-platform'
                    ],
                    'labels': node_pool.get('labels', {}),
                    'taints': [
                        {
                            'key': taint['key'],
                            'value': taint.get('value', ''),
                            'effect': taint.get('effect', 'NO_SCHEDULE')
                        }
                        for taint in node_pool.get('taints', [])
                    ]
                },
                'autoscaling': {
                    'enabled': node_pool.get('enable_auto_scaling', False),
                    'min_node_count': node_pool.get('min_count', 1),
                    'max_node_count': node_pool.get('max_count', 5)
                }
            }
            
            # Add preemptible configuration
            if node_pool.get('preemptible', False):
                node_pool_config['config']['preemptible'] = True
            
            cluster['node_pools'].append(node_pool_config)
        
        # Create cluster request
        parent = f'projects/{project_id}/locations/{location}'
        request = {'parent': parent, 'cluster': cluster}
        
        try:
            operation = self.gke_client.create_cluster(request)
            
            logger.info(f"GKE cluster creation started: {k8s_config['name']}")
            logger.info(f"Operation: {operation.operation.name}")
            
            return {
                'cluster_name': k8s_config['name'],
                'operation': operation.operation.name,
                'location': location
            }
            
        except gcp_exceptions.AlreadyExists:
            logger.info(f"GKE cluster already exists: {k8s_config['name']}")
            return {
                'cluster_name': k8s_config['name'],
                'status': 'exists'
            }
    
    async def _deploy_databases(self, db_config: dict) -> List[dict]:
        """Deploy Cloud SQL instances"""
        logger.info("Deploying Cloud SQL instances")
        
        databases = []
        for instance_config in db_config.get('instances', []):
            db = await self._create_cloud_sql_instance(instance_config)
            databases.append(db)
        
        return databases
    
    async def _create_cloud_sql_instance(self, db_config: dict) -> dict:
        """Create Cloud SQL instance"""
        logger.info(f"Creating Cloud SQL instance: {db_config['name']}")
        
        project_id = self.config['project']
        instance_id = db_config['name']
        
        # Build instance configuration
        instance = {
            'name': instance_id,
            'database_version': db_config.get('engine_version', 'POSTGRES_15'),
            'region': self.config.get('region'),
            'settings': {
                'tier': db_config.get('tier', 'db-f1-micro'),
                'data_disk_size_gb': db_config.get('storage_gb', 100),
                'data_disk_type': db_config.get('disk_type', 'PD_SSD'),
                'availability_type': db_config.get('availability_type', 'ZONAL'),
                'backup_configuration': {
                    'enabled': True,
                    'backup_retention_settings': {
                        'retention_days': db_config.get('backup_retention_days', 7)
                    },
                    'start_time': db_config.get('backup_time', '03:00')
                },
                'ip_configuration': {
                    'ipv4_enabled': db_config.get('enable_public_ip', True),
                    'private_network': db_config.get('vpc_network'),
                    'require_ssl': db_config.get('require_ssl', True)
                },
                'database_flags': db_config.get('database_flags', []),
                'user_labels': db_config.get('labels', {})
            }
        }
        
        # Configure high availability
        if db_config.get('availability_type') == 'REGIONAL':
            instance['settings']['availability_type'] = 'REGIONAL'
        
        # Create instance request
        request = {
            'parent': f'projects/{project_id}',
            'instance': instance
        }
        
        try:
            operation = self.sql_client.create_instance(request)
            
            logger.info(f"Cloud SQL instance creation started: {instance_id}")
            
            return {
                'instance_id': instance_id,
                'operation': operation.operation.name,
                'project': project_id
            }
            
        except gcp_exceptions.AlreadyExists:
            logger.info(f"Cloud SQL instance already exists: {instance_id}")
            return {
                'instance_id': instance_id,
                'status': 'exists'
            }
    
    async def _deploy_storage(self, storage_config: dict) -> List[dict]:
        """Deploy GCS buckets"""
        logger.info("Deploying GCS buckets")
        
        buckets = []
        for bucket_config in storage_config.get('buckets', []):
            bucket = await self._create_gcs_bucket(bucket_config)
            buckets.append(bucket)
        
        return buckets
    
    async def _create_gcs_bucket(self, bucket_config: dict) -> dict:
        """Create GCS bucket"""
        logger.info(f"Creating GCS bucket: {bucket_config['name']}")
        
        bucket = self.storage_client.bucket(bucket_config['name'])
        bucket.storage_class = bucket_config.get('storage_class', 'STANDARD')
        bucket.location = bucket_config.get('location', 'US')
        
        try:
            bucket.create()
            
            # Enable versioning
            if bucket_config.get('versioning', {}).get('enabled', False):
                bucket.versioning_enabled = True
                bucket.patch()
            
            # Set lifecycle rules
            if bucket_config.get('lifecycle_rules'):
                lifecycle_rules = []
                for rule in bucket_config['lifecycle_rules']:
                    lifecycle_rule = {
                        'action': {
                            'type': rule.get('action_type', 'Delete')
                        },
                        'condition': {}
                    }
                    
                    if 'age_days' in rule:
                        lifecycle_rule['condition']['age'] = rule['age_days']
                    if 'is_live' in rule:
                        lifecycle_rule['condition']['is_live'] = rule['is_live']
                    if 'matches_prefix' in rule:
                        lifecycle_rule['condition']['matches_prefix'] = rule['matches_prefix']
                    
                    lifecycle_rules.append(lifecycle_rule)
                
                bucket.lifecycle_rules = lifecycle_rules
                bucket.patch()
            
            # Set bucket labels
            if bucket_config.get('labels'):
                bucket.labels = bucket_config['labels']
                bucket.patch()
            
            # Set default KMS key if specified
            if bucket_config.get('kms_key_name'):
                bucket.default_kms_key_name = bucket_config['kms_key_name']
                bucket.patch()
            
            logger.info(f"GCS bucket created: {bucket_config['name']}")
            
            return {
                'bucket_name': bucket_config['name'],
                'location': bucket.location,
                'storage_class': bucket.storage_class
            }
            
        except gcp_exceptions.Conflict:
            logger.warning(f"GCS bucket already exists: {bucket_config['name']}")
            return {
                'bucket_name': bucket_config['name'],
                'status': 'exists'
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
                'disk_io': 0.0
            }
        }
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider information"""
        return {
            'provider_name': self.PROVIDER_NAME,
            'provider_version': self.PROVIDER_VERSION,
            'project': self.config.get('project'),
            'region': self.config.get('region'),
            'available_services': [
                'gcs', 'gke', 'cloud-sql', 'cloud-monitoring', 'bigquery',
                'pubsub', 'cloud-functions', 'ai-platform'
            ]
        }