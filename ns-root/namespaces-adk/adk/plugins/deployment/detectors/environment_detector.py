"""
Environment Detector - Auto-detect current deployment environment
Enhanced with comprehensive provider detection and detailed metadata
"""

import os
import requests
from typing import Dict, Optional, Any
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class EnvironmentInfo:
    """Enhanced environment information"""
    type: str  # kubernetes, docker, aws, gcp, azure, nomad, on-premise
    provider: str  # Specific provider name
    version: Optional[str] = None
    region: Optional[str] = None
    zone: Optional[str] = None
    cluster_name: Optional[str] = None
    instance_id: Optional[str] = None
    instance_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'type': self.type,
            'provider': self.provider,
            'version': self.version,
            'region': self.region,
            'zone': self.zone,
            'cluster_name': self.cluster_name,
            'instance_id': self.instance_id,
            'instance_type': self.instance_type,
            'metadata': self.metadata
        }
    
    def is_cloud(self) -> bool:
        """Check if running in cloud environment"""
        return self.type in ['aws', 'gcp', 'azure']
    
    def is_container_platform(self) -> bool:
        """Check if running in container platform"""
        return self.type in ['kubernetes', 'docker', 'nomad']
    
    def is_on_premise(self) -> bool:
        """Check if running on-premise"""
        return self.type == 'on-premise'


class EnvironmentDetector:
    """Enhanced environment detector with comprehensive provider detection"""
    
    @staticmethod
    def detect(timeout: int = 5) -> EnvironmentInfo:
        """
        Detect environment with enhanced metadata
        Timeout in seconds for metadata requests
        """
        logger.info(f"Detecting deployment environment (timeout: {timeout}s)...")
        
        # Check for Kubernetes (highest priority)
        if EnvironmentDetector._is_kubernetes():
            return EnvironmentDetector._detect_kubernetes_environment(timeout)
        
        # Check for Docker
        if EnvironmentDetector._is_docker():
            return EnvironmentDetector._detect_docker_environment(timeout)
        
        # Check for cloud providers
        aws_metadata = EnvironmentDetector._check_aws_metadata(timeout)
        if aws_metadata:
            logger.info("Detected AWS environment")
            return EnvironmentDetector._create_aws_info(aws_metadata)
        
        gcp_metadata = EnvironmentDetector._check_gcp_metadata(timeout)
        if gcp_metadata:
            logger.info("Detected GCP environment")
            return EnvironmentDetector._create_gcp_info(gcp_metadata)
        
        azure_metadata = EnvironmentDetector._check_azure_metadata(timeout)
        if azure_metadata:
            logger.info("Detected Azure environment")
            return EnvironmentDetector._create_azure_info(azure_metadata)
        
        # Check for Nomad
        if EnvironmentDetector._is_nomad(timeout):
            logger.info("Detected Nomad environment")
            return EnvironmentDetector._detect_nomad_environment(timeout)
        
        # Default to on-premise
        logger.info("Defaulting to on-premise environment")
        return EnvironmentDetector._create_on_premise_info()
    
    @staticmethod
    def _is_kubernetes() -> bool:
        """Check if running in Kubernetes"""
        try:
            # Check for service account token
            if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/token'):
                logger.debug("Found Kubernetes service account token")
                return True
            
            # Check for KUBERNETES_SERVICE_HOST env var
            if os.environ.get('KUBERNETES_SERVICE_HOST'):
                logger.debug(f"Found KUBERNETES_SERVICE_HOST: {os.environ.get('KUBERNETES_SERVICE_HOST')}")
                return True
            
            # Check for kubeconfig
            if os.path.exists(os.path.expanduser('~/.kube/config')):
                logger.debug("Found kubeconfig file")
                return True
            
            return False
        except Exception as e:
            logger.debug(f"Error checking for Kubernetes: {e}")
            return False
    
    @staticmethod
    def _detect_kubernetes_environment(timeout: int) -> EnvironmentInfo:
        """Detect Kubernetes environment with detailed information"""
        logger.info("Detecting Kubernetes environment details...")
        
        try:
            # Read service account token
            token = None
            token_path = '/var/run/secrets/kubernetes.io/serviceaccount/token'
            if os.path.exists(token_path):
                with open(token_path, 'r') as f:
                    token = f.read().strip()
            
            # Read namespace
            namespace = 'default'
            namespace_path = '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
            if os.path.exists(namespace_path):
                with open(namespace_path, 'r') as f:
                    namespace = f.read().strip()
            
            # Get API server URL
            api_server = os.environ.get('KUBERNETES_SERVICE_HOST', '')
            api_port = os.environ.get('KUBERNETES_SERVICE_PORT', '443')
            api_url = f"https://{api_server}:{api_port}" if api_server else ''
            
            # Detect Kubernetes provider
            provider = EnvironmentDetector._detect_kubernetes_provider(timeout)
            
            # Get cluster name from environment or pod info
            cluster_name = os.environ.get('CLUSTER_NAME') or os.environ.get('KUBERNETES_CLUSTER_NAME')
            
            # Get pod name
            pod_name = os.environ.get('POD_NAME')
            pod_namespace = os.environ.get('POD_NAMESPACE', namespace)
            
            metadata = {
                'kubernetes': True,
                'api_server': api_url,
                'namespace': namespace,
                'pod_name': pod_name,
                'pod_namespace': pod_namespace,
                'has_service_account': token is not None
            }
            
            return EnvironmentInfo(
                type='kubernetes',
                provider=provider,
                version=EnvironmentDetector._get_kubernetes_version(timeout),
                cluster_name=cluster_name,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error detecting Kubernetes environment: {e}")
            return EnvironmentInfo(
                type='kubernetes',
                provider='kubernetes',
                metadata={'kubernetes': True, 'detection_error': str(e)}
            )
    
    @staticmethod
    def _detect_kubernetes_provider(timeout: int) -> str:
        """Detect Kubernetes provider (AWS EKS, GCP GKE, Azure AKS, etc.)"""
        try:
            # Check for AWS EKS
            if EnvironmentDetector._check_aws_metadata(timeout):
                return 'aws-eks'
            
            # Check for GCP GKE
            if EnvironmentDetector._check_gcp_metadata(timeout):
                return 'gcp-gke'
            
            # Check for Azure AKS
            if EnvironmentDetector._check_azure_metadata(timeout):
                return 'azure-aks'
            
            # Check for environment variables
            if os.environ.get('EKS_CLUSTER_NAME'):
                return 'aws-eks'
            if os.environ.get('GKE_CLUSTER'):
                return 'gcp-gke'
            if os.environ.get('AKS_CLUSTER_NAME'):
                return 'azure-aks'
            
            # Check for other providers
            if os.environ.get('DIGITALOCEAN_CLUSTER_NAME'):
                return 'digitalocean-doks'
            if os.environ.get('LINODE_CLUSTER_ID'):
                return 'linode-lke'
            
            # Default to generic Kubernetes
            return 'kubernetes'
            
        except Exception as e:
            logger.debug(f"Error detecting Kubernetes provider: {e}")
            return 'kubernetes'
    
    @staticmethod
    def _get_kubernetes_version(timeout: int) -> Optional[str]:
        """Get Kubernetes version"""
        try:
            import subprocess
            
            # Try kubectl
            result = subprocess.run(
                ['kubectl', 'version', '--short'],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                output = result.stdout
                for line in output.split('\n'):
                    if 'Server Version:' in line or 'Server' in line:
                        # Extract version (e.g., "v1.28.0")
                        parts = line.split()
                        for part in parts:
                            if part.startswith('v1.'):
                                return part
                return output.strip()
            
        except Exception as e:
            logger.debug(f"Error getting Kubernetes version: {e}")
        
        return None
    
    @staticmethod
    def _is_docker() -> bool:
        """Check if running in Docker"""
        try:
            # Check for .dockerenv file
            if os.path.exists('/.dockerenv'):
                logger.debug("Found .dockerenv file")
                return True
            
            # Check for cgroup information
            cgroup_path = '/proc/1/cgroup'
            if os.path.exists(cgroup_path):
                with open(cgroup_path, 'r') as f:
                    cgroup_content = f.read()
                    if 'docker' in cgroup_content.lower() or 'containerd' in cgroup_content.lower():
                        logger.debug("Found docker/containerd in cgroup")
                        return True
            
            # Check for Docker environment variables
            if os.environ.get('DOCKER_CONTAINER'):
                return True
            
            return False
        except Exception as e:
            logger.debug(f"Error checking for Docker: {e}")
            return False
    
    @staticmethod
    def _detect_docker_environment(timeout: int) -> EnvironmentInfo:
        """Detect Docker environment with detailed information"""
        logger.info("Detecting Docker environment details...")
        
        try:
            # Get container ID from cgroup
            container_id = None
            cgroup_path = '/proc/1/cgroup'
            if os.path.exists(cgroup_path):
                with open(cgroup_path, 'r') as f:
                    for line in f:
                        if 'docker' in line or 'containerd' in line:
                            # Extract container ID
                            parts = line.split('/')
                            if len(parts) > 0:
                                container_id = parts[-1].strip()
                                break
            
            # Get Docker host from environment
            docker_host = os.environ.get('DOCKER_HOST', 'unix:///var/run/docker.sock')
            
            # Get container name
            container_name = os.environ.get('CONTAINER_NAME') or os.environ.get('HOSTNAME')
            
            # Check if running in Docker Compose
            is_compose = 'COMPOSE_PROJECT_NAME' in os.environ
            
            # Get Docker version
            docker_version = None
            try:
                import subprocess
                result = subprocess.run(
                    ['docker', 'version', '--format', '{{.Server.Version}}'],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                if result.returncode == 0:
                    docker_version = result.stdout.strip()
            except Exception as e:
                logger.debug(f"Error getting Docker version: {e}")
            
            metadata = {
                'docker': True,
                'container_id': container_id,
                'container_name': container_name,
                'docker_host': docker_host,
                'docker_compose': is_compose,
                'compose_project': os.environ.get('COMPOSE_PROJECT_NAME') if is_compose else None
            }
            
            return EnvironmentInfo(
                type='docker',
                provider='docker',
                version=docker_version,
                instance_id=container_id,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error detecting Docker environment: {e}")
            return EnvironmentInfo(
                type='docker',
                provider='docker',
                metadata={'docker': True, 'detection_error': str(e)}
            )
    
    @staticmethod
    def _check_aws_metadata(timeout: int = 5) -> Optional[Dict[str, Any]]:
        """Check AWS instance metadata"""
        try:
            # AWS EC2 metadata endpoint
            metadata_url = "http://169.254.169.254/latest/meta-data/"
            
            try:
                response = requests.get(metadata_url, timeout=timeout)
                if response.status_code == 200:
                    # Get instance metadata
                    instance_id = requests.get(
                        f"{metadata_url}instance-id",
                        timeout=timeout
                    ).text
                    
                    instance_type = requests.get(
                        f"{metadata_url}instance-type",
                        timeout=timeout
                    ).text
                    
                    availability_zone = requests.get(
                        f"{metadata_url}placement/availability-zone",
                        timeout=timeout
                    ).text
                    
                    region = availability_zone[:-1]  # Remove zone letter
                    
                    # Get IAM role
                    iam_role = None
                    try:
                        iam_role = requests.get(
                            f"{metadata_url}iam/security-credentials/",
                            timeout=timeout
                        ).text
                    except requests.exceptions.RequestException as exc:
                        logger.debug(
                            "Failed to retrieve IAM role from AWS metadata service: %s",
                            exc,
                        )
                    
                    return {
                        'instance_id': instance_id,
                        'instance_type': instance_type,
                        'availability_zone': availability_zone,
                        'region': region,
                        'iam_role': iam_role
                    }
            except requests.exceptions.RequestException:
                logger.debug("AWS metadata endpoint request failed")
                pass
            
            return None
            
        except Exception as e:
            logger.debug(f"Error checking AWS metadata: {e}")
            return None
    
    @staticmethod
    def _create_aws_info(metadata: Dict[str, Any]) -> EnvironmentInfo:
        """Create AWS environment info"""
        return EnvironmentInfo(
            type='aws',
            provider='aws',
            region=metadata.get('region'),
            zone=metadata.get('availability_zone'),
            instance_id=metadata.get('instance_id'),
            instance_type=metadata.get('instance_type'),
            metadata={
                'aws': True,
                'availability_zone': metadata.get('availability_zone'),
                'iam_role': metadata.get('iam_role')
            }
        )
    
    @staticmethod
    def _check_gcp_metadata(timeout: int = 5) -> Optional[Dict[str, Any]]:
        """Check GCP instance metadata"""
        try:
            # GCP metadata endpoint
            metadata_url = "http://metadata.google.internal/computeMetadata/v1/"
            headers = {"Metadata-Flavor": "Google"}
            
            try:
                # Get instance metadata
                instance_id = requests.get(
                    f"{metadata_url}instance/id",
                    headers=headers,
                    timeout=timeout
                ).text
                
                machine_type = requests.get(
                    f"{metadata_url}instance/machine-type",
                    headers=headers,
                    timeout=timeout
                ).text.split('/')[-1]
                
                zone = requests.get(
                    f"{metadata_url}instance/zone",
                    headers=headers,
                    timeout=timeout
                ).text.split('/')[-1]
                
                project_id = requests.get(
                    f"{metadata_url}project/project-id",
                    headers=headers,
                    timeout=timeout
                ).text
                
                return {
                    'instance_id': instance_id,
                    'machine_type': machine_type,
                    'zone': zone,
                    'project_id': project_id
                }
            except requests.exceptions.RequestException:
                pass
            
            return None
            
        except Exception as e:
            logger.debug(f"Error checking GCP metadata: {e}")
            return None
    
    @staticmethod
    def _zone_to_region(zone: str) -> str:
        """Convert GCP zone to region"""
        if '-' in zone:
            parts = zone.split('-')
            if len(parts) >= 2:
                return '-'.join(parts[:-1])
        return zone
    
    @staticmethod
    def _create_gcp_info(metadata: Dict[str, Any]) -> EnvironmentInfo:
        """Create GCP environment info"""
        zone = metadata.get('zone')
        region = EnvironmentDetector._zone_to_region(zone) if zone else None
        
        return EnvironmentInfo(
            type='gcp',
            provider='gcp',
            region=region,
            zone=zone,
            instance_id=metadata.get('instance_id'),
            instance_type=metadata.get('machine_type'),
            metadata={
                'gcp': True,
                'project_id': metadata.get('project_id')
            }
        )
    
    @staticmethod
    def _check_azure_metadata(timeout: int = 5) -> Optional[Dict[str, Any]]:
        """Check Azure instance metadata"""
        try:
            # Azure metadata endpoint
            metadata_url = "http://169.254.169.254/metadata/instance?api-version=2021-02-01"
            headers = {"Metadata": "true"}
            
            try:
                response = requests.get(metadata_url, headers=headers, timeout=timeout)
                if response.status_code == 200:
                    metadata = response.json()
                    
                    compute = metadata.get('compute', {})
                    
                    location = compute.get('location')
                    zone = compute.get('zone')
                    vm_id = compute.get('vmId')
                    vm_size = compute.get('vmSize')
                    resource_group_name = compute.get('resourceGroupName')
                    
                    return {
                        'location': location,
                        'zone': zone,
                        'vm_id': vm_id,
                        'vm_size': vm_size,
                        'resource_group_name': resource_group_name
                    }
            except requests.exceptions.RequestException as exc:
                logger.debug("Azure metadata endpoint request failed: %s", exc)
            
            return None
            
        except Exception as e:
            logger.debug(f"Error checking Azure metadata: {e}")
            return None
    
    @staticmethod
    def _create_azure_info(metadata: Dict[str, Any]) -> EnvironmentInfo:
        """Create Azure environment info"""
        return EnvironmentInfo(
            type='azure',
            provider='azure',
            region=metadata.get('location'),
            zone=metadata.get('zone'),
            instance_id=metadata.get('vm_id'),
            instance_type=metadata.get('vm_size'),
            metadata={
                'azure': True,
                'resource_group_name': metadata.get('resource_group_name')
            }
        )
    
    @staticmethod
    def _is_nomad(timeout: int = 5) -> bool:
        """Check if running in Nomad"""
        try:
            # Check for Nomad environment variables
            if os.environ.get('NOMAD_ALLOC_ID'):
                logger.debug("Found NOMAD_ALLOC_ID")
                return True
            
            if os.environ.get('NOMAD_JOB_NAME'):
                logger.debug("Found NOMAD_JOB_NAME")
                return True
            
            # Check for Nomad API
            nomad_addr = os.environ.get('NOMAD_ADDR', 'http://127.0.0.1:4646')
            try:
                response = requests.get(
                    f"{nomad_addr}/v1/self",
                    timeout=timeout
                )
                if response.status_code == 200:
                    logger.debug("Successfully queried Nomad API")
                    return True
            except requests.exceptions.RequestException as e:
                logger.debug("Nomad API not available when checking environment: %s", e)
            
            return False
        except Exception as e:
            logger.debug(f"Error checking for Nomad: {e}")
            return False
    
    @staticmethod
    def _detect_nomad_environment(timeout: int) -> EnvironmentInfo:
        """Detect Nomad environment with detailed information"""
        logger.info("Detecting Nomad environment details...")
        
        try:
            # Get Nomad agent information
            nomad_addr = os.environ.get('NOMAD_ADDR', 'http://127.0.0.1:4646')
            
            # Get allocation info
            alloc_id = os.environ.get('NOMAD_ALLOC_ID')
            job_name = os.environ.get('NOMAD_JOB_NAME')
            task_name = os.environ.get('NOMAD_TASK_NAME')
            
            # Get Nomad version
            nomad_version = None
            try:
                response = requests.get(
                    f"{nomad_addr}/v1/self",
                    timeout=timeout
                )
                if response.status_code == 200:
                    self_info = response.json()
                    nomad_version = self_info.get('config', {}).get('Version')
            except Exception as e:
                logger.debug(f"Error getting Nomad version: {e}")
            
            metadata = {
                'nomad': True,
                'alloc_id': alloc_id,
                'job_name': job_name,
                'task_name': task_name,
                'nomad_addr': nomad_addr
            }
            
            return EnvironmentInfo(
                type='nomad',
                provider='nomad',
                version=nomad_version,
                instance_id=alloc_id,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error detecting Nomad environment: {e}")
            return EnvironmentInfo(
                type='nomad',
                provider='nomad',
                metadata={'nomad': True, 'detection_error': str(e)}
            )
    
    @staticmethod
    def _create_on_premise_info() -> EnvironmentInfo:
        """Create on-premise environment info"""
        try:
            import socket
            hostname = socket.gethostname()
        except Exception:
            hostname = None
        
        return EnvironmentInfo(
            type='on-premise',
            provider='bare-metal',
            metadata={
                'on-premise': True,
                'hostname': hostname
            }
        )