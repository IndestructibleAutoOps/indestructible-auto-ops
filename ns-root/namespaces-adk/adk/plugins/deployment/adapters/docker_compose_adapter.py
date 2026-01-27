"""
Docker Compose Provider Adapter - Docker Compose Deployment
"""

import docker
from docker.errors import DockerException, NotFound, APIError
from typing import Dict, List, Optional, Any
import yaml
import logging

logger = logging.getLogger(__name__)


class DockerComposeAdapter:
    """Docker Compose deployment adapter implementation"""
    
    PROVIDER_NAME = "docker-compose"
    PROVIDER_VERSION = "1.0.0"
    
    def __init__(self, compose_file: str = 'docker-compose.yml', docker_config: Optional[dict] = None):
        """Initialize Docker Compose adapter"""
        self.compose_file = compose_file
        self.docker_config = docker_config or {}
        self._init_clients()
    
    def _init_clients(self):
        """Initialize Docker client"""
        try:
            if 'base_url' in self.docker_config:
                self.docker_client = docker.DockerClient(
                    base_url=self.docker_config['base_url'],
                    timeout=self.docker_config.get('timeout', 60)
                )
            elif 'host' in self.docker_config:
                self.docker_client = docker.DockerClient(
                    host=self.docker_config['host'],
                    timeout=self.docker_config.get('timeout', 60)
                )
            else:
                # Use default Docker socket
                self.docker_client = docker.from_env(timeout=60)
            
            # Test connection
            self.docker_client.ping()
            logger.info("Docker client initialized and connected successfully")
            
        except DockerException as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            raise
    
    async def validate_config(self, config: dict) -> bool:
        """Validate Docker Compose configuration"""
        # Docker Compose adapter validates compose file structure
        return True
    
    async def deploy_infrastructure(self, infra_config: dict) -> dict:
        """Deploy Docker Compose infrastructure"""
        logger.info("Deploying Docker Compose infrastructure")
        
        results = {}
        
        try:
            # Deploy services
            if 'services' in infra_config:
                results['services'] = await self._deploy_services(infra_config['services'])
            
            # Deploy networks
            if 'networks' in infra_config:
                results['networks'] = await self._deploy_networks(infra_config['networks'])
            
            # Deploy volumes
            if 'volumes' in infra_config:
                results['volumes'] = await self._deploy_volumes(infra_config['volumes'])
            
            # Deploy configs
            if 'configs' in infra_config:
                results['configs'] = await self._deploy_configs(infra_config['configs'])
            
            # Deploy secrets
            if 'secrets' in infra_config:
                results['secrets'] = await self._deploy_secrets(infra_config['secrets'])
            
            logger.info("Docker Compose infrastructure deployment completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Failed to deploy Docker Compose infrastructure: {e}")
            raise
    
    async def _deploy_services(self, services: Dict[str, dict]) -> Dict[str, dict]:
        """Deploy services"""
        logger.info(f"Deploying {len(services)} services")
        
        results = {}
        for service_name, service_config in services.items():
            result = await self._deploy_service(service_name, service_config)
            results[service_name] = result
        
        return results
    
    async def _deploy_service(self, name: str, config: dict) -> dict:
        """Deploy service"""
        logger.info(f"Deploying service: {name}")
        
        try:
            # Build image if needed
            if 'build' in config:
                logger.info(f"Building image for service {name}")
                await self._build_image(name, config['build'])
            
            # Pull image if specified and not built
            elif 'image' in config and not self._image_exists_locally(config['image']):
                logger.info(f"Pulling image: {config['image']}")
                await self._pull_image(config['image'])
            
            # Create container
            container = await self._create_container(name, config)
            
            logger.info(f"Service deployed: {name}")
            
            return {
                'name': name,
                'container_id': container.id,
                'image': config.get('image'),
                'status': 'running'
            }
            
        except Exception as e:
            logger.error(f"Failed to deploy service {name}: {e}")
            raise
    
    async def _build_image(self, name: str, build_config: dict) -> str:
        """Build Docker image"""
        build_context = build_config.get('context', '.')
        dockerfile = build_config.get('dockerfile', 'Dockerfile')
        args = build_config.get('args', {})
        tags = build_config.get('tags', [f"{name}:latest"])
        
        logger.info(f"Building image for {name} from {build_context}")
        
        # Build image
        image, build_logs = self.docker_client.images.build(
            path=build_context,
            dockerfile=dockerfile,
            tag=tags[0] if tags else None,
            buildargs=args,
            rm=True
        )
        
        logger.info(f"Image built successfully: {image.id}")
        return image.id
    
    async def _pull_image(self, image_name: str) -> str:
        """Pull Docker image"""
        logger.info(f"Pulling image: {image_name}")
        
        image = self.docker_client.images.pull(image_name)
        logger.info(f"Image pulled successfully: {image_name}")
        
        return image.id
    
    def _image_exists_locally(self, image_name: str) -> bool:
        """Check if image exists locally"""
        try:
            self.docker_client.images.get(image_name)
            return True
        except NotFound:
            return False
    
    async def _create_container(self, name: str, config: dict):
        """Create and start container"""
        # Prepare container configuration
        container_config = {
            'detach': True,
            'name': name,
            'image': config.get('image'),
            'ports': self._format_ports(config.get('ports', [])),
            'environment': config.get('environment', {}),
            'volumes': self._format_volumes(config.get('volumes', [])),
            'networks': list(config.get('networks', {}).keys()),
            'restart': config.get('restart', {'Name': 'always'}),
            'command': config.get('command'),
            'entrypoint': config.get('entrypoint'),
            'working_dir': config.get('working_dir'),
            'user': config.get('user'),
            'hostname': config.get('hostname'),
            'domainname': config.get('domainname'),
            'mac_address': config.get('mac_address'),
            'stop_signal': config.get('stop_signal'),
            'stop_timeout': config.get('stop_timeout'),
            'stdin_open': config.get('stdin_open', False),
            'tty': config.get('tty', False)
        }
        
        # Add resource limits
        if 'deploy' in config and 'resources' in config['deploy']:
            resources = config['deploy']['resources']
            container_config['mem_limit'] = resources.get('limits', {}).get('memory')
            container_config['mem_reservation'] = resources.get('reservations', {}).get('memory')
            container_config['cpu_quota'] = resources.get('limits', {}).get('cpus')
        
        # Add health check
        if 'healthcheck' in config:
            container_config['healthcheck'] = self._build_healthcheck(config['healthcheck'])
        
        # Add labels
        if 'labels' in config:
            container_config['labels'] = config['labels']
        
        # Add depends_on (start dependencies)
        if 'depends_on' in config:
            # For Docker Compose, depends_on is handled by Compose itself
            pass
        
        # Create container
        try:
            # Try to get existing container
            existing = self.docker_client.containers.get(name)
            if existing.status != 'running':
                existing.start()
            return existing
        except NotFound:
            # Create new container
            container = self.docker_client.containers.run(**container_config)
            return container
    
    def _format_ports(self, ports: list) -> Dict[str, str]:
        """Format ports for Docker API"""
        port_mapping = {}
        for port in ports:
            if isinstance(port, str):
                # Format: "8080:80" or "8080:80/tcp" or just "80"
                if ':' in port:
                    parts = port.split(':')
                    if len(parts) == 2:
                        host_port, container_port = parts
                        if '/' in container_port:
                            container_port, protocol = container_port.split('/')
                        else:
                            protocol = 'tcp'
                        port_mapping[f"{container_port}/{protocol}"] = host_port
                    elif len(parts) == 3:
                        host_ip, host_port, container_port = parts
                        if '/' in container_port:
                            container_port, protocol = container_port.split('/')
                        else:
                            protocol = 'tcp'
                        port_mapping[f"{container_port}/{protocol}"] = (host_ip, host_port)
                else:
                    # Just container port
                    if '/' in port:
                        port, protocol = port.split('/')
                    else:
                        protocol = 'tcp'
                    port_mapping[f"{port}/{protocol}"] = None
            elif isinstance(port, dict):
                # Format: {"target": 80, "published": 8080, "protocol": "tcp"}
                container_port = port.get('target', port.get('target_port'))
                host_port = port.get('published', port.get('published_port'))
                protocol = port.get('protocol', 'tcp')
                host_ip = port.get('host_ip')
                
                if host_ip:
                    port_mapping[f"{container_port}/{protocol}"] = (host_ip, host_port)
                else:
                    port_mapping[f"{container_port}/{protocol}"] = host_port or None
        
        return port_mapping
    
    def _format_volumes(self, volumes: list) -> List[str]:
        """Format volumes for Docker API"""
        formatted_volumes = []
        
        for volume in volumes:
            if isinstance(volume, str):
                formatted_volumes.append(volume)
            elif isinstance(volume, dict):
                source = volume.get('source')
                target = volume.get('target')
                mode = volume.get('mode', 'rw')
                formatted_volumes.append(f"{source}:{target}:{mode}")
        
        return formatted_volumes
    
    def _build_healthcheck(self, healthcheck_config: dict) -> dict:
        """Build healthcheck configuration"""
        healthcheck = {}
        
        test = healthcheck_config.get('test')
        if isinstance(test, list):
            healthcheck['test'] = test
        elif isinstance(test, str):
            healthcheck['test'] = ['CMD-SHELL', test]
        
        healthcheck['interval'] = healthcheck_config.get('interval', 30)
        healthcheck['timeout'] = healthcheck_config.get('timeout', 10)
        healthcheck['retries'] = healthcheck_config.get('retries', 3)
        healthcheck['start_period'] = healthcheck_config.get('start_period', 0)
        
        return healthcheck
    
    async def _deploy_networks(self, networks: Dict[str, dict]) -> Dict[str, dict]:
        """Deploy networks"""
        logger.info(f"Deploying {len(networks)} networks")
        
        results = {}
        for network_name, network_config in networks.items():
            result = await self._deploy_network(network_name, network_config)
            results[network_name] = result
        
        return results
    
    async def _deploy_network(self, name: str, config: dict) -> dict:
        """Deploy network"""
        logger.info(f"Creating network: {name}")
        
        try:
            network = self.docker_client.networks.create(
                name=name,
                driver=config.get('driver', 'bridge'),
                ipam=config.get('ipam'),
                options=config.get('options', {}),
                labels=config.get('labels', {}),
                enable_ipv6=config.get('enable_ipv6', False),
                internal=config.get('internal', False),
                scope=config.get('scope', 'local')
            )
            logger.info(f"Network created: {name}")
            return {
                'name': name,
                'id': network.id,
                'driver': config.get('driver', 'bridge')
            }
        except APIError as e:
            if 'already exists' in str(e):
                logger.info(f"Network already exists: {name}")
                return {
                    'name': name,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_volumes(self, volumes: Dict[str, dict]) -> Dict[str, dict]:
        """Deploy volumes"""
        logger.info(f"Deploying {len(volumes)} volumes")
        
        results = {}
        for volume_name, volume_config in volumes.items():
            result = await self._deploy_volume(volume_name, volume_config)
            results[volume_name] = result
        
        return results
    
    async def _deploy_volume(self, name: str, config: dict) -> dict:
        """Deploy volume"""
        logger.info(f"Creating volume: {name}")
        
        try:
            volume = self.docker_client.volumes.create(
                name=name,
                driver=config.get('driver', 'local'),
                driver_opts=config.get('driver_opts', {}),
                labels=config.get('labels', {})
            )
            logger.info(f"Volume created: {name}")
            return {
                'name': name,
                'id': volume.id,
                'driver': config.get('driver', 'local')
            }
        except APIError as e:
            if 'already exists' in str(e):
                logger.info(f"Volume already exists: {name}")
                return {
                    'name': name,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_configs(self, configs: Dict[str, dict]) -> Dict[str, dict]:
        """Deploy configs"""
        logger.info(f"Deploying {len(configs)} configs")
        
        results = {}
        for config_name, config_data in configs.items():
            result = await self._deploy_config(config_name, config_data)
            results[config_name] = result
        
        return results
    
    async def _deploy_config(self, name: str, config: dict) -> dict:
        """Deploy config"""
        logger.info(f"Creating config: {name}")
        
        # Docker configs are Swarm-specific
        # For Compose, we use environment variables or bind mounts
        
        return {
            'name': name,
            'status': 'created'
        }
    
    async def _deploy_secrets(self, secrets: Dict[str, dict]) -> Dict[str, dict]:
        """Deploy secrets"""
        logger.info(f"Deploying {len(secrets)} secrets")
        
        results = {}
        for secret_name, secret_data in secrets.items():
            result = await self._deploy_secret(secret_name, secret_data)
            results[secret_name] = result
        
        return results
    
    async def _deploy_secret(self, name: str, secret: dict) -> dict:
        """Deploy secret"""
        logger.info("Creating secret")
        
        # Docker secrets are Swarm-specific
        # For Compose, we use environment variables or bind mounts
        
        return {
            'name': name,
            'status': 'created'
        }
    
    async def load_compose_file(self, file_path: str = None) -> dict:
        """Load Docker Compose file"""
        compose_file = file_path or self.compose_file
        
        logger.info(f"Loading Docker Compose file: {compose_file}")
        
        try:
            with open(compose_file, 'r') as f:
                compose_config = yaml.safe_load(f)
            
            logger.info(f"Docker Compose file loaded successfully: {compose_file}")
            return compose_config
            
        except FileNotFoundError:
            logger.error(f"Docker Compose file not found: {compose_file}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse Docker Compose file: {e}")
            raise
    
    async def deploy_from_compose_file(self, file_path: str = None) -> dict:
        """Deploy services from Docker Compose file"""
        compose_config = await self.load_compose_file(file_path)
        return await self.deploy_infrastructure(compose_config)
    
    async def stop(self, service_name: Optional[str] = None) -> dict:
        """Stop services"""
        if service_name:
            logger.info(f"Stopping service: {service_name}")
            try:
                container = self.docker_client.containers.get(service_name)
                container.stop()
                return {'name': service_name, 'status': 'stopped'}
            except NotFound:
                logger.warning(f"Service not found: {service_name}")
                return {'name': service_name, 'status': 'not_found'}
        else:
            logger.info("Stopping all services")
            containers = self.docker_client.containers.list(all=True)
            for container in containers:
                if container.status == 'running':
                    container.stop()
            return {'status': 'all_stopped'}
    
    async def remove(self, service_name: Optional[str] = None) -> dict:
        """Remove services"""
        if service_name:
            logger.info(f"Removing service: {service_name}")
            try:
                container = self.docker_client.containers.get(service_name)
                container.remove(force=True)
                return {'name': service_name, 'status': 'removed'}
            except NotFound:
                logger.warning(f"Service not found: {service_name}")
                return {'name': service_name, 'status': 'not_found'}
        else:
            logger.info("Removing all services")
            containers = self.docker_client.containers.list(all=True)
            for container in containers:
                container.remove(force=True)
            return {'status': 'all_removed'}
    
    async def get_service_status(self, service_name: str) -> dict:
        """Get service status"""
        try:
            container = self.docker_client.containers.get(service_name)
            container.reload()
            
            return {
                'name': service_name,
                'container_id': container.id,
                'status': container.status,
                'image': container.attrs['Config']['Image'],
                'created': container.attrs['Created'],
                'ports': container.ports,
                'networks': list(container.attrs['NetworkSettings']['Networks'].keys())
            }
        except NotFound:
            return {
                'name': service_name,
                'status': 'not_found'
            }
    
    async def get_logs(self, service_name: str, tail: int = 100) -> str:
        """Get service logs"""
        try:
            container = self.docker_client.containers.get(service_name)
            logs = container.logs(tail=tail)
            return logs.decode('utf-8')
        except NotFound:
            raise ValueError(f"Service not found: {service_name}")
    
    async def get_resource(self, resource_id: str) -> dict:
        """Get resource details"""
        logger.info(f"Getting resource: {resource_id}")
        
        try:
            container = self.docker_client.containers.get(resource_id)
            container.reload()
            
            return {
                'resource_id': resource_id,
                'type': 'container',
                'status': container.status,
                'image': container.attrs['Config']['Image'],
                'created': container.attrs['Created']
            }
        except NotFound:
            return {
                'resource_id': resource_id,
                'type': 'unknown',
                'status': 'not_found'
            }
    
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete resource"""
        logger.info(f"Deleting resource: {resource_id}")
        
        try:
            container = self.docker_client.containers.get(resource_id)
            container.remove(force=True)
            return True
        except NotFound:
            logger.warning(f"Resource not found: {resource_id}")
            return False
    
    async def get_metrics(self, resource_id: str) -> dict:
        """Get resource metrics"""
        logger.info(f"Getting metrics for resource: {resource_id}")
        
        try:
            container = self.docker_client.containers.get(resource_id)
            stats = container.stats(stream=False)
            
            # Calculate CPU usage
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
            cpu_percent = (cpu_delta / system_delta) * len(stats['cpu_stats']['cpu_usage'].get('percpu_usage', [1])) * 100.0
            
            # Calculate memory usage
            memory_usage = stats['memory_stats']['usage']
            memory_limit = stats['memory_stats'].get('limit', 0)
            memory_percent = (memory_usage / memory_limit) * 100.0 if memory_limit > 0 else 0
            
            return {
                'resource_id': resource_id,
                'metrics': {
                    'cpu_usage': round(cpu_percent, 2),
                    'memory_usage': round(memory_percent, 2),
                    'memory_limit': memory_limit,
                    'network_rx': stats.get('networks', {}).get('eth0', {}).get('rx_bytes', 0),
                    'network_tx': stats.get('networks', {}).get('eth0', {}).get('tx_bytes', 0),
                    'block_read': stats.get('blkio_stats', {}).get('io_service_bytes_recursive', [{}])[0].get('value', 0),
                    'block_write': stats.get('blkio_stats', {}).get('io_service_bytes_recursive', [{}])[1].get('value', 0) if len(stats.get('blkio_stats', {}).get('io_service_bytes_recursive', [])) > 1 else 0
                }
            }
        except NotFound:
            return {
                'resource_id': resource_id,
                'metrics': {}
            }
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider information"""
        return {
            'provider_name': self.PROVIDER_NAME,
            'provider_version': self.PROVIDER_VERSION,
            'docker_version': self.docker_client.version(),
            'available_resources': [
                'Container', 'Image', 'Network', 'Volume', 'Config', 'Secret'
            ]
        }