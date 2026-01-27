"""
Kubernetes Provider Adapter - Kubernetes Cluster Deployment
"""

from kubernetes import client, config
from kubernetes.client.rest import ApiException
from typing import Dict, List, Optional, Any
import logging
import time

logger = logging.getLogger(__name__)


class KubernetesAdapter:
    """Kubernetes deployment adapter implementation"""
    
    PROVIDER_NAME = "kubernetes"
    PROVIDER_VERSION = "1.0.0"
    
    def __init__(self, kubeconfig_path: Optional[str] = None, kube_config: Optional[dict] = None):
        """Initialize Kubernetes adapter"""
        self._init_clients(kubeconfig_path, kube_config)
    
    def _init_clients(self, kubeconfig_path: Optional[str] = None, kube_config: Optional[dict] = None):
        """Initialize Kubernetes clients"""
        try:
            if kube_config:
                # Use inline kubeconfig
                config.load_kube_config_from_dict(config_dict=kube_config)
            elif kubeconfig_path:
                # Use kubeconfig file
                config.load_kube_config(config_file=kubeconfig_path)
            else:
                # Try in-cluster config first, then default kubeconfig
                try:
                    config.load_incluster_config()
                    logger.info("Loaded in-cluster Kubernetes config")
                except config.ConfigException:
                    config.load_kube_config()
                    logger.info("Loaded default kubeconfig")
            
            # Initialize API clients
            self.core_v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
            self.networking_v1 = client.NetworkingV1Api()
            self.rbac_v1 = client.RbacAuthorizationV1Api()
            self.batch_v1 = client.BatchV1Api()
            self.custom_objects = client.CustomObjectsApi()
            
            logger.info("Kubernetes clients initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Kubernetes clients: {e}")
            raise
    
    async def validate_config(self, config: dict) -> bool:
        """Validate Kubernetes configuration"""
        # Kubernetes adapter doesn't require specific config fields
        # kubeconfig can be loaded from file or environment
        
        return True
    
    async def deploy_infrastructure(self, infra_config: dict) -> dict:
        """Deploy Kubernetes infrastructure"""
        logger.info("Deploying Kubernetes infrastructure")
        
        results = {}
        
        try:
            # Deploy namespace
            if 'namespace' in infra_config:
                results['namespace'] = await self.deploy_namespace(infra_config['namespace'])
            
            # Deploy ConfigMaps
            if 'config_maps' in infra_config:
                results['config_maps'] = await self._deploy_config_maps(infra_config['config_maps'])
            
            # Deploy Secrets
            if 'secrets' in infra_config:
                results['secrets'] = await self._deploy_secrets(infra_config['secrets'])
            
            # Deploy PersistentVolumes and PersistentVolumeClaims
            if 'storage' in infra_config:
                results['storage'] = await self._deploy_storage(infra_config['storage'])
            
            # Deploy Deployments
            if 'deployments' in infra_config:
                results['deployments'] = await self._deploy_deployments(infra_config['deployments'])
            
            # Deploy StatefulSets
            if 'statefulsets' in infra_config:
                results['statefulsets'] = await self._deploy_statefulsets(infra_config['statefulsets'])
            
            # Deploy Services
            if 'services' in infra_config:
                results['services'] = await self._deploy_services(infra_config['services'])
            
            # Deploy Ingress
            if 'ingress' in infra_config:
                results['ingress'] = await self._deploy_ingress(infra_config['ingress'])
            
            # Deploy DaemonSets
            if 'daemonsets' in infra_config:
                results['daemonsets'] = await self._deploy_daemonsets(infra_config['daemonsets'])
            
            # Deploy Jobs
            if 'jobs' in infra_config:
                results['jobs'] = await self._deploy_jobs(infra_config['jobs'])
            
            # Deploy CronJobs
            if 'cronjobs' in infra_config:
                results['cronjobs'] = await self._deploy_cronjobs(infra_config['cronjobs'])
            
            # Deploy RBAC resources
            if 'rbac' in infra_config:
                results['rbac'] = await self._deploy_rbac(infra_config['rbac'])
            
            logger.info("Kubernetes infrastructure deployment completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Failed to deploy Kubernetes infrastructure: {e}")
            raise
    
    async def deploy_namespace(self, namespace: str) -> dict:
        """Deploy namespace"""
        logger.info(f"Creating namespace: {namespace}")
        
        namespace_obj = client.V1Namespace(
            metadata=client.V1ObjectMeta(
                name=namespace,
                labels={'name': namespace}
            )
        )
        
        try:
            result = self.core_v1.create_namespace(namespace_obj)
            logger.info(f"Namespace created: {namespace}")
            return {
                'name': namespace,
                'status': 'created',
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"Namespace already exists: {namespace}")
                return {
                    'name': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_config_maps(self, config_maps: List[dict]) -> List[dict]:
        """Deploy ConfigMaps"""
        logger.info(f"Deploying {len(config_maps)} ConfigMaps")
        
        results = []
        for cm_config in config_maps:
            result = await self.deploy_config_map(cm_config)
            results.append(result)
        
        return results
    
    async def deploy_config_map(self, config_map_config: dict) -> dict:
        """Deploy ConfigMap"""
        logger.info(f"Deploying ConfigMap: {config_map_config['name']}")
        
        namespace = config_map_config.get('namespace', 'default')
        
        config_map = client.V1ConfigMap(
            metadata=client.V1ObjectMeta(
                name=config_map_config['name'],
                namespace=namespace,
                labels=config_map_config.get('labels', {}),
                annotations=config_map_config.get('annotations', {})
            ),
            data=config_map_config.get('data', {}),
            binary_data=config_map_config.get('binary_data', {})
        )
        
        try:
            result = self.core_v1.create_namespaced_config_map(
                namespace=namespace,
                body=config_map
            )
            logger.info(f"ConfigMap created: {config_map_config['name']}")
            return {
                'name': config_map_config['name'],
                'namespace': namespace,
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"ConfigMap already exists: {config_map_config['name']}")
                return {
                    'name': config_map_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_secrets(self, secrets: List[dict]) -> List[dict]:
        """Deploy Secrets"""
        logger.info(f"Deploying {len(secrets)} Secrets")
        
        results = []
        for secret_config in secrets:
            result = await self.deploy_secret(secret_config)
            results.append(result)
        
        return results
    
    async def deploy_secret(self, secret_config: dict) -> dict:
        """Deploy secret"""
        logger.info("Deploying Kubernetes secret")
        
        namespace = secret_config.get('namespace', 'default')
        
        secret = client.V1Secret(
            metadata=client.V1ObjectMeta(
                name=secret_config['name'],
                namespace=namespace,
                labels=secret_config.get('labels', {}),
                annotations=secret_config.get('annotations', {})
            ),
            data=secret_config.get('data', {}),
            string_data=secret_config.get('string_data', {}),
            type=secret_config.get('type', 'Opaque')
        )
        
        try:
            self.core_v1.create_namespaced_secret(
                namespace=namespace,
                body=secret
            )
            logger.info("Secret created")
            return {
                'name': secret_config['name'],
                'namespace': namespace,
                'type': secret.type
            }
        except ApiException as e:
            if e.status == 409:
                logger.info("Secret already exists")
                return {
                    'name': secret_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_storage(self, storage_config: dict) -> dict:
        """Deploy storage resources"""
        logger.info("Deploying storage resources")
        
        results = {}
        
        # Deploy PersistentVolumes
        if 'persistent_volumes' in storage_config:
            results['persistent_volumes'] = await self._deploy_persistent_volumes(
                storage_config['persistent_volumes']
            )
        
        # Deploy PersistentVolumeClaims
        if 'persistent_volume_claims' in storage_config:
            results['persistent_volume_claims'] = await self._deploy_persistent_volume_claims(
                storage_config['persistent_volume_claims']
            )
        
        # Deploy StorageClasses
        if 'storage_classes' in storage_config:
            results['storage_classes'] = await self._deploy_storage_classes(
                storage_config['storage_classes']
            )
        
        return results
    
    async def _deploy_persistent_volumes(self, pvs: List[dict]) -> List[dict]:
        """Deploy PersistentVolumes"""
        results = []
        for pv_config in pvs:
            result = await self.deploy_persistent_volume(pv_config)
            results.append(result)
        return results
    
    async def deploy_persistent_volume(self, pv_config: dict) -> dict:
        """Deploy PersistentVolume"""
        logger.info(f"Deploying PersistentVolume: {pv_config['name']}")
        
        pv = client.V1PersistentVolume(
            metadata=client.V1ObjectMeta(
                name=pv_config['name'],
                labels=pv_config.get('labels', {})
            ),
            spec=client.V1PersistentVolumeSpec(
                capacity=pv_config['capacity'],
                access_modes=pv_config['access_modes'],
                persistent_volume_reclaim_policy=pv_config.get('reclaim_policy', 'Retain'),
                storage_class_name=pv_config.get('storage_class_name'),
                volume_mode=pv_config.get('volume_mode', 'Filesystem')
            )
        )
        
        try:
            result = self.core_v1.create_persistent_volume(pv)
            logger.info(f"PersistentVolume created: {pv_config['name']}")
            return {
                'name': pv_config['name'],
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"PersistentVolume already exists: {pv_config['name']}")
                return {'name': pv_config['name'], 'status': 'exists'}
            raise
    
    async def _deploy_persistent_volume_claims(self, pvcs: List[dict]) -> List[dict]:
        """Deploy PersistentVolumeClaims"""
        results = []
        for pvc_config in pvcs:
            result = await self.deploy_persistent_volume_claim(pvc_config)
            results.append(result)
        return results
    
    async def deploy_persistent_volume_claim(self, pvc_config: dict) -> dict:
        """Deploy PersistentVolumeClaim"""
        logger.info(f"Deploying PersistentVolumeClaim: {pvc_config['name']}")
        
        namespace = pvc_config.get('namespace', 'default')
        
        pvc = client.V1PersistentVolumeClaim(
            metadata=client.V1ObjectMeta(
                name=pvc_config['name'],
                namespace=namespace,
                labels=pvc_config.get('labels', {})
            ),
            spec=client.V1PersistentVolumeClaimSpec(
                access_modes=pvc_config['access_modes'],
                resources=pvc_config['resources'],
                storage_class_name=pvc_config.get('storage_class_name'),
                volume_name=pvc_config.get('volume_name')
            )
        )
        
        try:
            result = self.core_v1.create_namespaced_persistent_volume_claim(
                namespace=namespace,
                body=pvc
            )
            logger.info(f"PersistentVolumeClaim created: {pvc_config['name']}")
            return {
                'name': pvc_config['name'],
                'namespace': namespace,
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"PersistentVolumeClaim already exists: {pvc_config['name']}")
                return {'name': pvc_config['name'], 'status': 'exists'}
            raise
    
    async def _deploy_deployments(self, deployments: List[dict]) -> List[dict]:
        """Deploy Deployments"""
        logger.info(f"Deploying {len(deployments)} Deployments")
        
        results = []
        for deploy_config in deployments:
            result = await self.deploy_deployment(deploy_config)
            results.append(result)
        
        return results
    
    async def deploy_deployment(self, deployment_config: dict) -> dict:
        """Deploy deployment"""
        logger.info(f"Deploying deployment: {deployment_config['name']}")
        
        namespace = deployment_config.get('namespace', 'default')
        
        deployment = client.V1Deployment(
            metadata=client.V1ObjectMeta(
                name=deployment_config['name'],
                namespace=namespace,
                labels=deployment_config.get('labels', {}),
                annotations=deployment_config.get('annotations', {})
            ),
            spec=client.V1DeploymentSpec(
                replicas=deployment_config.get('replicas', 1),
                selector=client.V1LabelSelector(
                    match_labels=deployment_config.get('selector_labels', {})
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels=deployment_config.get('pod_labels', {}),
                        annotations=deployment_config.get('pod_annotations', {})
                    ),
                    spec=await self._build_pod_spec(deployment_config)
                ),
                strategy=deployment_config.get('strategy'),
                revision_history_limit=deployment_config.get('revision_history_limit', 10),
                progress_deadline_seconds=deployment_config.get('progress_deadline_seconds', 600)
            )
        )
        
        try:
            result = self.apps_v1.create_namespaced_deployment(
                namespace=namespace,
                body=deployment
            )
            logger.info(f"Deployment created: {deployment_config['name']}")
            return {
                'name': deployment_config['name'],
                'namespace': namespace,
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"Deployment already exists: {deployment_config['name']}")
                return {
                    'name': deployment_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _build_pod_spec(self, deployment_config: dict) -> client.V1PodSpec:
        """Build pod spec"""
        containers = []
        
        for container_config in deployment_config.get('containers', []):
            container = client.V1Container(
                name=container_config['name'],
                image=container_config['image'],
                ports=[
                    client.V1ContainerPort(
                        name=p.get('name', 'port'),
                        container_port=p['port'],
                        protocol=p.get('protocol', 'TCP')
                    )
                    for p in container_config.get('ports', [])
                ],
                env=[
                    client.V1EnvVar(
                        name=e['name'],
                        value=e.get('value'),
                        value_from=self._build_env_var_source(e.get('value_from'))
                    )
                    for e in container_config.get('env', [])
                ],
                env_from=[
                    client.V1EnvFromSource(
                        config_map_ref=client.V1ConfigMapEnvSource(
                            name=ef.get('config_map_name')
                        ) if 'config_map_name' in ef else None,
                        secret_ref=client.V1SecretEnvSource(
                            name=ef.get('secret_name')
                        ) if 'secret_name' in ef else None
                    )
                    for ef in container_config.get('env_from', [])
                ],
                resources=self._build_resource_requirements(
                    container_config.get('resources', {})
                ),
                volume_mounts=[
                    client.V1VolumeMount(
                        name=vm['name'],
                        mount_path=vm['mount_path'],
                        read_only=vm.get('read_only', False),
                        sub_path=vm.get('sub_path')
                    )
                    for vm in container_config.get('volume_mounts', [])
                ],
                image_pull_policy=container_config.get('image_pull_policy', 'IfNotPresent'),
                command=container_config.get('command'),
                args=container_config.get('args'),
                working_dir=container_config.get('working_dir'),
                lifecycle=container_config.get('lifecycle'),
                liveness_probe=self._build_probe(container_config.get('liveness_probe')),
                readiness_probe=self._build_probe(container_config.get('readiness_probe')),
                startup_probe=self._build_probe(container_config.get('startup_probe'))
            )
            containers.append(container)
        
        return client.V1PodSpec(
            containers=containers,
            init_containers=[
                client.V1Container(
                    name=ic['name'],
                    image=ic['image'],
                    command=ic.get('command'),
                    args=ic.get('args')
                )
                for ic in deployment_config.get('init_containers', [])
            ],
            service_account_name=deployment_config.get('service_account_name'),
            volumes=self._build_volumes(deployment_config.get('volumes', [])),
            dns_policy=deployment_config.get('dns_policy', 'ClusterFirst'),
            restart_policy=deployment_config.get('restart_policy', 'Always'),
            node_selector=deployment_config.get('node_selector'),
            affinity=deployment_config.get('affinity'),
            tolerations=deployment_config.get('tolerations'),
            priority_class_name=deployment_config.get('priority_class_name'),
            security_context=deployment_config.get('pod_security_context'),
            termination_grace_period_seconds=deployment_config.get('termination_grace_period_seconds')
        )
    
    def _build_env_var_source(self, value_from: Optional[dict]) -> Optional[client.V1EnvVarSource]:
        """Build environment variable source"""
        if not value_from:
            return None
        
        if 'secret_key_ref' in value_from:
            return client.V1EnvVarSource(
                secret_key_ref=client.V1SecretKeySelector(
                    name=value_from['secret_key_ref']['name'],
                    key=value_from['secret_key_ref']['key'],
                    optional=value_from['secret_key_ref'].get('optional', False)
                )
            )
        
        if 'config_map_key_ref' in value_from:
            return client.V1EnvVarSource(
                config_map_key_ref=client.V1ConfigMapKeySelector(
                    name=value_from['config_map_key_ref']['name'],
                    key=value_from['config_map_key_ref']['key'],
                    optional=value_from['config_map_key_ref'].get('optional', False)
                )
            )
        
        if 'field_ref' in value_from:
            return client.V1EnvVarSource(
                field_ref=client.V1ObjectFieldSelector(
                    field_path=value_from['field_ref']['field_path'],
                    api_version=value_from['field_ref'].get('api_version', 'v1')
                )
            )
        
        if 'resource_field_ref' in value_from:
            return client.V1EnvVarSource(
                resource_field_ref=client.V1ResourceFieldSelector(
                    container_name=value_from['resource_field_ref'].get('container_name'),
                    resource=value_from['resource_field_ref']['resource'],
                    divisor=value_from['resource_field_ref'].get('divisor')
                )
            )
        
        return None
    
    def _build_resource_requirements(self, resources: dict) -> Optional[client.V1ResourceRequirements]:
        """Build resource requirements"""
        if not resources:
            return None
        
        return client.V1ResourceRequirements(
            requests=resources.get('requests'),
            limits=resources.get('limits')
        )
    
    def _build_probe(self, probe_config: Optional[dict]) -> Optional[client.V1Probe]:
        """Build probe"""
        if not probe_config:
            return None
        
        probe = client.V1Probe(
            initial_delay_seconds=probe_config.get('initial_delay_seconds', 0),
            timeout_seconds=probe_config.get('timeout_seconds', 1),
            period_seconds=probe_config.get('period_seconds', 10),
            success_threshold=probe_config.get('success_threshold', 1),
            failure_threshold=probe_config.get('failure_threshold', 3)
        )
        
        if 'http_get' in probe_config:
            probe.http_get = client.V1HTTPGetAction(
                path=probe_config['http_get'].get('path', '/'),
                port=probe_config['http_get']['port'],
                scheme=probe_config['http_get'].get('scheme', 'HTTP'),
                http_headers=[
                    client.V1HTTPHeader(
                        name=h['name'],
                        value=h['value']
                    )
                    for h in probe_config['http_get'].get('headers', [])
                ]
            )
        
        if 'tcp_socket' in probe_config:
            probe.tcp_socket = client.V1TCPSocketAction(
                port=probe_config['tcp_socket']['port']
            )
        
        if 'exec' in probe_config:
            probe.exec = client.V1ExecAction(
                command=probe_config['exec']['command']
            )
        
        return probe
    
    def _build_volumes(self, volume_configs: List[dict]) -> List[client.V1Volume]:
        """Build volumes"""
        volumes = []
        
        for vol_config in volume_configs:
            volume = client.V1Volume(name=vol_config['name'])
            
            if 'persistent_volume_claim' in vol_config:
                volume.persistent_volume_claim = client.V1PersistentVolumeClaimVolumeSource(
                    claim_name=vol_config['persistent_volume_claim']['claim_name'],
                    read_only=vol_config['persistent_volume_claim'].get('read_only', False)
                )
            
            if 'config_map' in vol_config:
                volume.config_map = client.V1ConfigMapVolumeSource(
                    name=vol_config['config_map']['name'],
                    items=vol_config['config_map'].get('items', []),
                    default_mode=vol_config['config_map'].get('default_mode')
                )
            
            if 'secret' in vol_config:
                volume.secret = client.V1SecretVolumeSource(
                    secret_name=vol_config['secret']['name'],
                    optional=vol_config['secret'].get('optional', False),
                    default_mode=vol_config['secret'].get('default_mode')
                )
            
            if 'empty_dir' in vol_config:
                volume.empty_dir = client.V1EmptyDirVolumeSource(
                    medium=vol_config['empty_dir'].get('medium', ''),
                    size_limit=vol_config['empty_dir'].get('size_limit')
                )
            
            if 'host_path' in vol_config:
                volume.host_path = client.V1HostPathVolumeSource(
                    path=vol_config['host_path']['path'],
                    type=vol_config['host_path'].get('type')
                )
            
            if 'nfs' in vol_config:
                volume.nfs = client.V1NFSVolumeSource(
                    server=vol_config['nfs']['server'],
                    path=vol_config['nfs']['path'],
                    read_only=vol_config['nfs'].get('read_only', False)
                )
            
            volumes.append(volume)
        
        return volumes
    
    async def _deploy_statefulsets(self, statefulsets: List[dict]) -> List[dict]:
        """Deploy StatefulSets"""
        logger.info(f"Deploying {len(statefulsets)} StatefulSets")
        
        results = []
        for sts_config in statefulsets:
            result = await self.deploy_statefulset(sts_config)
            results.append(result)
        
        return results
    
    async def deploy_statefulset(self, statefulset_config: dict) -> dict:
        """Deploy StatefulSet"""
        logger.info(f"Deploying StatefulSet: {statefulset_config['name']}")
        
        namespace = statefulset_config.get('namespace', 'default')
        
        statefulset = client.V1StatefulSet(
            metadata=client.V1ObjectMeta(
                name=statefulset_config['name'],
                namespace=namespace,
                labels=statefulset_config.get('labels', {})
            ),
            spec=client.V1StatefulSetSpec(
                replicas=statefulset_config.get('replicas', 1),
                selector=client.V1LabelSelector(
                    match_labels=statefulset_config.get('selector_labels', {})
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels=statefulset_config.get('pod_labels', {})
                    ),
                    spec=await self._build_pod_spec(statefulset_config)
                ),
                volume_claim_templates=[
                    client.V1PersistentVolumeClaim(
                        metadata=client.V1ObjectMeta(name=pvt['name']),
                        spec=client.V1PersistentVolumeClaimSpec(
                            access_modes=pvt['access_modes'],
                            resources=pvt['resources']
                        )
                    )
                    for pvt in statefulset_config.get('volume_claim_templates', [])
                ],
                service_name=statefulset_config.get('service_name'),
                pod_management_policy=statefulset_config.get('pod_management_policy', 'OrderedReady'),
                update_strategy=statefulset_config.get('update_strategy'),
                revision_history_limit=statefulset_config.get('revision_history_limit', 10)
            )
        )
        
        try:
            result = self.apps_v1.create_namespaced_stateful_set(
                namespace=namespace,
                body=statefulset
            )
            logger.info(f"StatefulSet created: {statefulset_config['name']}")
            return {
                'name': statefulset_config['name'],
                'namespace': namespace,
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"StatefulSet already exists: {statefulset_config['name']}")
                return {
                    'name': statefulset_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_services(self, services: List[dict]) -> List[dict]:
        """Deploy Services"""
        logger.info(f"Deploying {len(services)} Services")
        
        results = []
        for service_config in services:
            result = await self.deploy_service(service_config)
            results.append(result)
        
        return results
    
    async def deploy_service(self, service_config: dict) -> dict:
        """Deploy service"""
        logger.info(f"Deploying service: {service_config['name']}")
        
        namespace = service_config.get('namespace', 'default')
        
        service = client.V1Service(
            metadata=client.V1ObjectMeta(
                name=service_config['name'],
                namespace=namespace,
                labels=service_config.get('labels', {}),
                annotations=service_config.get('annotations', {})
            ),
            spec=client.V1ServiceSpec(
                type=service_config.get('type', 'ClusterIP'),
                selector=service_config.get('selector', {}),
                ports=[
                    client.V1ServicePort(
                        name=p.get('name', 'http'),
                        protocol=p.get('protocol', 'TCP'),
                        port=p['port'],
                        target_port=p.get('target_port', p['port']),
                        node_port=p.get('node_port')
                    )
                    for p in service_config.get('ports', [])
                ],
                session_affinity=service_config.get('session_affinity', 'None'),
                external_i_ps=service_config.get('external_i_ps'),
                load_balancer_ip=service_config.get('load_balancer_ip'),
                external_name=service_config.get('external_name'),
                external_traffic_policy=service_config.get('external_traffic_policy'),
                health_check_node_port=service_config.get('health_check_node_port')
            )
        )
        
        try:
            result = self.core_v1.create_namespaced_service(
                namespace=namespace,
                body=service
            )
            logger.info(f"Service created: {service_config['name']}")
            return {
                'name': service_config['name'],
                'namespace': namespace,
                'cluster_ip': result.spec.cluster_ip
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"Service already exists: {service_config['name']}")
                return {
                    'name': service_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_ingress(self, ingress_configs: List[dict]) -> List[dict]:
        """Deploy Ingress resources"""
        logger.info(f"Deploying {len(ingress_configs)} Ingress resources")
        
        results = []
        for ingress_config in ingress_configs:
            result = await self.deploy_ingress(ingress_config)
            results.append(result)
        
        return results
    
    async def deploy_ingress(self, ingress_config: dict) -> dict:
        """Deploy ingress"""
        logger.info(f"Deploying ingress: {ingress_config['name']}")
        
        namespace = ingress_config.get('namespace', 'default')
        
        ingress = client.V1Ingress(
            metadata=client.V1ObjectMeta(
                name=ingress_config['name'],
                namespace=namespace,
                labels=ingress_config.get('labels', {}),
                annotations=ingress_config.get('annotations', {})
            ),
            spec=client.V1IngressSpec(
                rules=[
                    client.V1IngressRule(
                        host=rule.get('host'),
                        http=client.V1HTTPIngressRuleValue(
                            paths=[
                                client.V1HTTPIngressPath(
                                    path=path.get('path', '/'),
                                    path_type=path.get('path_type', 'Prefix'),
                                    backend=client.V1IngressBackend(
                                        service=client.V1IngressServiceBackend(
                                            name=path['service_name'],
                                            port=client.V1ServiceBackendPort(
                                                number=path['service_port']
                                            )
                                        )
                                    )
                                )
                                for path in rule.get('paths', [])
                            ]
                        )
                    )
                    for rule in ingress_config.get('rules', [])
                ],
                tls=[
                    client.V1IngressTLS(
                        hosts=tls.get('hosts', []),
                        secret_name=tls.get('secret_name')
                    )
                    for tls in ingress_config.get('tls', [])
                ],
                ingress_class_name=ingress_config.get('ingress_class_name')
            )
        )
        
        try:
            result = self.networking_v1.create_namespaced_ingress(
                namespace=namespace,
                body=ingress
            )
            logger.info(f"Ingress created: {ingress_config['name']}")
            return {
                'name': ingress_config['name'],
                'namespace': namespace,
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"Ingress already exists: {ingress_config['name']}")
                return {
                    'name': ingress_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_daemonsets(self, daemonsets: List[dict]) -> List[dict]:
        """Deploy DaemonSets"""
        logger.info(f"Deploying {len(daemonsets)} DaemonSets")
        
        results = []
        for ds_config in daemonsets:
            result = await self.deploy_daemonset(ds_config)
            results.append(result)
        
        return results
    
    async def deploy_daemonset(self, daemonset_config: dict) -> dict:
        """Deploy DaemonSet"""
        logger.info(f"Deploying DaemonSet: {daemonset_config['name']}")
        
        namespace = daemonset_config.get('namespace', 'default')
        
        daemonset = client.V1DaemonSet(
            metadata=client.V1ObjectMeta(
                name=daemonset_config['name'],
                namespace=namespace,
                labels=daemonset_config.get('labels', {})
            ),
            spec=client.V1DaemonSetSpec(
                selector=client.V1LabelSelector(
                    match_labels=daemonset_config.get('selector_labels', {})
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels=daemonset_config.get('pod_labels', {})
                    ),
                    spec=await self._build_pod_spec(daemonset_config)
                ),
                min_ready_seconds=daemonset_config.get('min_ready_seconds', 0),
                revision_history_limit=daemonset_config.get('revision_history_limit', 10)
            )
        )
        
        try:
            result = self.apps_v1.create_namespaced_daemon_set(
                namespace=namespace,
                body=daemonset
            )
            logger.info(f"DaemonSet created: {daemonset_config['name']}")
            return {
                'name': daemonset_config['name'],
                'namespace': namespace,
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"DaemonSet already exists: {daemonset_config['name']}")
                return {
                    'name': daemonset_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_jobs(self, jobs: List[dict]) -> List[dict]:
        """Deploy Jobs"""
        logger.info(f"Deploying {len(jobs)} Jobs")
        
        results = []
        for job_config in jobs:
            result = await self.deploy_job(job_config)
            results.append(result)
        
        return results
    
    async def deploy_job(self, job_config: dict) -> dict:
        """Deploy Job"""
        logger.info(f"Deploying Job: {job_config['name']}")
        
        namespace = job_config.get('namespace', 'default')
        
        job = client.V1Job(
            metadata=client.V1ObjectMeta(
                name=job_config['name'],
                namespace=namespace,
                labels=job_config.get('labels', {})
            ),
            spec=client.V1JobSpec(
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(
                        labels=job_config.get('pod_labels', {})
                    ),
                    spec=await self._build_pod_spec(job_config)
                ),
                backoff_limit=job_config.get('backoff_limit', 6),
                ttl_seconds_after_finished=job_config.get('ttl_seconds_after_finished', 3600),
                active_deadline_seconds=job_config.get('active_deadline_seconds'),
                completions=job_config.get('completions', 1),
                parallelism=job_config.get('parallelism', 1)
            )
        )
        
        try:
            result = self.batch_v1.create_namespaced_job(
                namespace=namespace,
                body=job
            )
            logger.info(f"Job created: {job_config['name']}")
            return {
                'name': job_config['name'],
                'namespace': namespace,
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"Job already exists: {job_config['name']}")
                return {
                    'name': job_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_cronjobs(self, cronjobs: List[dict]) -> List[dict]:
        """Deploy CronJobs"""
        logger.info(f"Deploying {len(cronjobs)} CronJobs")
        
        results = []
        for cj_config in cronjobs:
            result = await self.deploy_cronjob(cj_config)
            results.append(result)
        
        return results
    
    async def deploy_cronjob(self, cronjob_config: dict) -> dict:
        """Deploy CronJob"""
        logger.info(f"Deploying CronJob: {cronjob_config['name']}")
        
        namespace = cronjob_config.get('namespace', 'default')
        
        cronjob = client.V1CronJob(
            metadata=client.V1ObjectMeta(
                name=cronjob_config['name'],
                namespace=namespace,
                labels=cronjob_config.get('labels', {})
            ),
            spec=client.V1CronJobSpec(
                schedule=cronjob_config['schedule'],
                job_template=client.V1JobTemplateSpec(
                    spec=client.V1JobSpec(
                        template=client.V1PodTemplateSpec(
                            metadata=client.V1ObjectMeta(
                                labels=cronjob_config.get('pod_labels', {})
                            ),
                            spec=await self._build_pod_spec(cronjob_config)
                        )
                    )
                ),
                concurrency_policy=cronjob_config.get('concurrency_policy', 'Allow'),
                suspend=cronjob_config.get('suspend', False),
                successful_jobs_history_limit=cronjob_config.get('successful_jobs_history_limit', 3),
                failed_jobs_history_limit=cronjob_config.get('failed_jobs_history_limit', 1),
                starting_deadline_seconds=cronjob_config.get('starting_deadline_seconds')
            )
        )
        
        try:
            result = self.batch_v1.create_namespaced_cron_job(
                namespace=namespace,
                body=cronjob
            )
            logger.info(f"CronJob created: {cronjob_config['name']}")
            return {
                'name': cronjob_config['name'],
                'namespace': namespace,
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"CronJob already exists: {cronjob_config['name']}")
                return {
                    'name': cronjob_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_rbac(self, rbac_config: dict) -> dict:
        """Deploy RBAC resources"""
        logger.info("Deploying RBAC resources")
        
        results = {}
        
        # Deploy ServiceAccounts
        if 'service_accounts' in rbac_config:
            results['service_accounts'] = await self._deploy_service_accounts(
                rbac_config['service_accounts']
            )
        
        # Deploy Roles
        if 'roles' in rbac_config:
            results['roles'] = await self._deploy_roles(rbac_config['roles'])
        
        # Deploy RoleBindings
        if 'role_bindings' in rbac_config:
            results['role_bindings'] = await self._deploy_role_bindings(
                rbac_config['role_bindings']
            )
        
        # Deploy ClusterRoles
        if 'cluster_roles' in rbac_config:
            results['cluster_roles'] = await self._deploy_cluster_roles(
                rbac_config['cluster_roles']
            )
        
        # Deploy ClusterRoleBindings
        if 'cluster_role_bindings' in rbac_config:
            results['cluster_role_bindings'] = await self._deploy_cluster_role_bindings(
                rbac_config['cluster_role_bindings']
            )
        
        return results
    
    async def _deploy_service_accounts(self, sas: List[dict]) -> List[dict]:
        """Deploy ServiceAccounts"""
        results = []
        for sa_config in sas:
            result = await self.deploy_service_account(sa_config)
            results.append(result)
        return results
    
    async def deploy_service_account(self, sa_config: dict) -> dict:
        """Deploy ServiceAccount"""
        logger.info(f"Deploying ServiceAccount: {sa_config['name']}")
        
        namespace = sa_config.get('namespace', 'default')
        
        sa = client.V1ServiceAccount(
            metadata=client.V1ObjectMeta(
                name=sa_config['name'],
                namespace=namespace,
                labels=sa_config.get('labels', {}),
                annotations=sa_config.get('annotations', {})
            ),
            secrets=[client.V1ObjectReference(name=s) for s in sa_config.get('secrets', [])]
        )
        
        try:
            result = self.core_v1.create_namespaced_service_account(
                namespace=namespace,
                body=sa
            )
            logger.info(f"ServiceAccount created: {sa_config['name']}")
            return {
                'name': sa_config['name'],
                'namespace': namespace,
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"ServiceAccount already exists: {sa_config['name']}")
                return {
                    'name': sa_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_roles(self, roles: List[dict]) -> List[dict]:
        """Deploy Roles"""
        results = []
        for role_config in roles:
            result = await self.deploy_role(role_config)
            results.append(result)
        return results
    
    async def deploy_role(self, role_config: dict) -> dict:
        """Deploy Role"""
        logger.info(f"Deploying Role: {role_config['name']}")
        
        namespace = role_config.get('namespace', 'default')
        
        role = client.V1Role(
            metadata=client.V1ObjectMeta(
                name=role_config['name'],
                namespace=namespace,
                labels=role_config.get('labels', {})
            ),
            rules=[
                client.V1PolicyRule(
                    api_groups=rule['api_groups'],
                    resources=rule['resources'],
                    verbs=rule['verbs'],
                    resource_names=rule.get('resource_names')
                )
                for rule in role_config.get('rules', [])
            ]
        )
        
        try:
            result = self.rbac_v1.create_namespaced_role(
                namespace=namespace,
                body=role
            )
            logger.info(f"Role created: {role_config['name']}")
            return {
                'name': role_config['name'],
                'namespace': namespace,
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"Role already exists: {role_config['name']}")
                return {
                    'name': role_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_role_bindings(self, rbs: List[dict]) -> List[dict]:
        """Deploy RoleBindings"""
        results = []
        for rb_config in rbs:
            result = await self.deploy_role_binding(rb_config)
            results.append(result)
        return results
    
    async def deploy_role_binding(self, rb_config: dict) -> dict:
        """Deploy RoleBinding"""
        logger.info(f"Deploying RoleBinding: {rb_config['name']}")
        
        namespace = rb_config.get('namespace', 'default')
        
        role_binding = client.V1RoleBinding(
            metadata=client.V1ObjectMeta(
                name=rb_config['name'],
                namespace=namespace,
                labels=rb_config.get('labels', {})
            ),
            subjects=[
                client.V1Subject(
                    kind=s['kind'],
                    name=s['name'],
                    namespace=s.get('namespace')
                )
                for s in rb_config.get('subjects', [])
            ],
            role_ref=client.V1RoleRef(
                kind=rb_config['role_ref']['kind'],
                name=rb_config['role_ref']['name'],
                api_group=rb_config['role_ref'].get('api_group', 'rbac.authorization.k8s.io')
            )
        )
        
        try:
            result = self.rbac_v1.create_namespaced_role_binding(
                namespace=namespace,
                body=role_binding
            )
            logger.info(f"RoleBinding created: {rb_config['name']}")
            return {
                'name': rb_config['name'],
                'namespace': namespace,
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"RoleBinding already exists: {rb_config['name']}")
                return {
                    'name': rb_config['name'],
                    'namespace': namespace,
                    'status': 'exists'
                }
            raise
    
    async def _deploy_cluster_roles(self, crs: List[dict]) -> List[dict]:
        """Deploy ClusterRoles"""
        results = []
        for cr_config in crs:
            result = await self.deploy_cluster_role(cr_config)
            results.append(result)
        return results
    
    async def deploy_cluster_role(self, cr_config: dict) -> dict:
        """Deploy ClusterRole"""
        logger.info(f"Deploying ClusterRole: {cr_config['name']}")
        
        cluster_role = client.V1ClusterRole(
            metadata=client.V1ObjectMeta(
                name=cr_config['name'],
                labels=cr_config.get('labels', {})
            ),
            rules=[
                client.V1PolicyRule(
                    api_groups=rule['api_groups'],
                    resources=rule['resources'],
                    verbs=rule['verbs'],
                    resource_names=rule.get('resource_names'),
                    non_resource_urls=rule.get('non_resource_urls')
                )
                for rule in cr_config.get('rules', [])
            ]
        )
        
        try:
            result = self.rbac_v1.create_cluster_role(body=cluster_role)
            logger.info(f"ClusterRole created: {cr_config['name']}")
            return {
                'name': cr_config['name'],
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"ClusterRole already exists: {cr_config['name']}")
                return {
                    'name': cr_config['name'],
                    'status': 'exists'
                }
            raise
    
    async def _deploy_cluster_role_bindings(self, crbs: List[dict]) -> List[dict]:
        """Deploy ClusterRoleBindings"""
        results = []
        for crb_config in crbs:
            result = await self.deploy_cluster_role_binding(crb_config)
            results.append(result)
        return results
    
    async def deploy_cluster_role_binding(self, crb_config: dict) -> dict:
        """Deploy ClusterRoleBinding"""
        logger.info(f"Deploying ClusterRoleBinding: {crb_config['name']}")
        
        cluster_role_binding = client.V1ClusterRoleBinding(
            metadata=client.V1ObjectMeta(
                name=crb_config['name'],
                labels=crb_config.get('labels', {})
            ),
            subjects=[
                client.V1Subject(
                    kind=s['kind'],
                    name=s['name'],
                    namespace=s.get('namespace')
                )
                for s in crb_config.get('subjects', [])
            ],
            role_ref=client.V1RoleRef(
                kind=crb_config['role_ref']['kind'],
                name=crb_config['role_ref']['name'],
                api_group=crb_config['role_ref'].get('api_group', 'rbac.authorization.k8s.io')
            )
        )
        
        try:
            result = self.rbac_v1.create_cluster_role_binding(body=cluster_role_binding)
            logger.info(f"ClusterRoleBinding created: {crb_config['name']}")
            return {
                'name': crb_config['name'],
                'uid': result.metadata.uid
            }
        except ApiException as e:
            if e.status == 409:
                logger.info(f"ClusterRoleBinding already exists: {crb_config['name']}")
                return {
                    'name': crb_config['name'],
                    'status': 'exists'
                }
            raise
    
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
                'cpu_usage': 0.0,
                'memory_usage': 0.0,
                'pod_count': 0
            }
        }
    
    async def wait_for_deployment_ready(self, namespace: str, name: str, timeout: int = 300) -> bool:
        """Wait for deployment to be ready"""
        logger.info(f"Waiting for deployment {namespace}/{name} to be ready")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                deployment = self.apps_v1.read_namespaced_deployment(name, namespace)
                
                if deployment.status.ready_replicas == deployment.spec.replicas:
                    logger.info(f"Deployment {namespace}/{name} is ready")
                    return True
                
                ready = deployment.status.ready_replicas or 0
                desired = deployment.spec.replicas
                logger.info(f"Waiting for deployment {namespace}/{name}: {ready}/{desired} replicas ready")
                time.sleep(5)
            except ApiException as e:
                logger.error(f"Error checking deployment {namespace}/{name}: {e}")
                time.sleep(5)
        
        logger.error(f"Timeout waiting for deployment {namespace}/{name}")
        return False
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider information"""
        return {
            'provider_name': self.PROVIDER_NAME,
            'provider_version': self.PROVIDER_VERSION,
            'available_resources': [
                'Namespace', 'ConfigMap', 'Secret', 'Deployment', 'StatefulSet',
                'DaemonSet', 'Service', 'Ingress', 'Job', 'CronJob',
                'PersistentVolume', 'PersistentVolumeClaim', 'StorageClass',
                'ServiceAccount', 'Role', 'RoleBinding', 'ClusterRole', 'ClusterRoleBinding'
            ]
        }