"""
Unit tests for Container Orchestration Manager
"""

import pytest
import asyncio
from datetime import datetime

import sys
sys.path.insert(0, '/workspace/machine-native-ops')

from adk.plugins.deployment.infrastructure.container_orchestration import (
    ContainerOrchestrationManager,
    ContainerConfig,
    ServiceConfig,
    DeploymentConfig,
    OrchestratorType,
    DeploymentStrategy,
    ScalingStrategy,
    OrchestrationResult
)


class TestContainerConfig:
    """Test ContainerConfig dataclass"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = ContainerConfig(
            name="test-container",
            image="nginx"
        )
        
        assert config.name == "test-container"
        assert config.image == "nginx"
        assert config.tag == "latest"
        assert config.replicas == 1
        assert config.cpu_request == "100m"
        assert config.cpu_limit == "500m"
        assert config.memory_request == "256Mi"
        assert config.memory_limit == "512Mi"
        assert config.run_as_non_root is True
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = ContainerConfig(
            name="custom-container",
            image="redis",
            tag="7.0",
            replicas=3,
            cpu_request="500m",
            cpu_limit="2000m",
            memory_request="1Gi",
            memory_limit="4Gi",
            env_vars={"ENV": "production"},
            ports=[{"containerPort": 6379}]
        )
        
        assert config.name == "custom-container"
        assert config.image == "redis"
        assert config.tag == "7.0"
        assert config.replicas == 3
        assert config.env_vars == {"ENV": "production"}
        assert len(config.ports) == 1


class TestServiceConfig:
    """Test ServiceConfig dataclass"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = ServiceConfig(
            name="test-service",
            ports=[{"port": 80, "targetPort": 8080}]
        )
        
        assert config.name == "test-service"
        assert config.type == "ClusterIP"
        assert len(config.ports) == 1
    
    def test_load_balancer_service(self):
        """Test load balancer service"""
        config = ServiceConfig(
            name="lb-service",
            type="LoadBalancer",
            ports=[{"port": 443, "targetPort": 8443}],
            external_traffic_policy="Local"
        )
        
        assert config.type == "LoadBalancer"
        assert config.external_traffic_policy == "Local"


class TestDeploymentConfig:
    """Test DeploymentConfig dataclass"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = DeploymentConfig(
            name="test-deployment",
            containers=[ContainerConfig(name="c1", image="nginx")]
        )
        
        assert config.name == "test-deployment"
        assert config.namespace == "default"
        assert config.strategy == DeploymentStrategy.ROLLING_UPDATE
        assert config.scaling_enabled is False
    
    def test_custom_config(self):
        """Test custom configuration with scaling"""
        container = ContainerConfig(name="c1", image="nginx")
        config = DeploymentConfig(
            name="scaled-deployment",
            containers=[container],
            strategy=DeploymentStrategy.CANARY,
            scaling_enabled=True,
            scaling_strategy=ScalingStrategy.HPA,
            min_replicas=2,
            max_replicas=10,
            target_cpu_utilization=70
        )
        
        assert config.strategy == DeploymentStrategy.CANARY
        assert config.scaling_enabled is True
        assert config.min_replicas == 2
        assert config.max_replicas == 10
        assert config.target_cpu_utilization == 70


class TestContainerOrchestrationManager:
    """Test ContainerOrchestrationManager class"""
    
    @pytest.fixture
    def manager_k8s(self):
        """Create Kubernetes manager"""
        return ContainerOrchestrationManager("kubernetes")
    
    @pytest.fixture
    def manager_docker(self):
        """Create Docker Compose manager"""
        return ContainerOrchestrationManager("docker_compose")
    
    def test_manager_initialization(self, manager_k8s):
        """Test manager initialization"""
        assert manager_k8s.orchestrator == "kubernetes"
        assert manager_k8s._deployments == {}
        assert manager_k8s._services == {}
        assert manager_k8s._pods == {}
    
    @pytest.mark.asyncio
    async def test_deploy_container(self, manager_k8s):
        """Test deploying a container"""
        container_config = ContainerConfig(
            name="nginx-container",
            image="nginx",
            replicas=2,
            ports=[{"containerPort": 80}]
        )
        
        deployment_config = DeploymentConfig(
            name="nginx-deployment",
            containers=[container_config]
        )
        
        result = await manager_k8s.deploy(deployment_config)
        
        assert isinstance(result, OrchestrationResult)
        assert result.success is True
        assert result.execution_time > 0
        assert "nginx-deployment completed successfully" in result.message
    
    @pytest.mark.asyncio
    async def test_deploy_with_services(self, manager_k8s):
        """Test deploying with services"""
        container_config = ContainerConfig(name="web", image="nginx")
        service_config = ServiceConfig(
            name="web-service",
            type="NodePort",
            ports=[{"port": 80, "targetPort": 80, "nodePort": 30080}]
        )
        
        deployment_config = DeploymentConfig(
            name="web-deployment",
            containers=[container_config],
            services=[service_config]
        )
        
        result = await manager_k8s.deploy(deployment_config)
        
        assert result.success is True
        assert result.data is not None
        assert "web" in result.data
        assert "web-service" in result.data
    
    @pytest.mark.asyncio
    async def test_deploy_with_scaling(self, manager_k8s):
        """Test deploying with auto-scaling"""
        container_config = ContainerConfig(
            name="app",
            image="app:latest",
            replicas=2
        )
        
        deployment_config = DeploymentConfig(
            name="app-deployment",
            containers=[container_config],
            scaling_enabled=True,
            scaling_strategy=ScalingStrategy.HPA,
            min_replicas=2,
            max_replicas=10,
            target_cpu_utilization=70
        )
        
        result = await manager_k8s.deploy(deployment_config)
        
        assert result.success is True
        assert result.data["scaling"] is not None
    
    @pytest.mark.asyncio
    async def test_deploy_dry_run(self, manager_k8s):
        """Test dry run deployment"""
        container_config = ContainerConfig(name="test", image="nginx")
        deployment_config = DeploymentConfig(
            name="test-deployment",
            containers=[container_config]
        )
        
        result = await manager_k8s.deploy(deployment_config, dry_run=True)
        
        assert result.success is True
        assert "Dry run completed successfully" in result.message
    
    @pytest.mark.asyncio
    async def test_scale_deployment(self, manager_k8s):
        """Test scaling deployment"""
        # First deploy
        container_config = ContainerConfig(name="app", image="nginx", replicas=2)
        deployment_config = DeploymentConfig(
            name="app-deployment",
            containers=[container_config]
        )
        await manager_k8s.deploy(deployment_config)
        
        # Scale up
        result = await manager_k8s.scale("app-deployment", replicas=5)
        
        assert result.success is True
        assert "Scaled app-deployment to 5 replicas" in result.message
        assert result.execution_time > 0
    
    @pytest.mark.asyncio
    async def test_rollback_deployment(self, manager_k8s):
        """Test rolling back deployment"""
        # Deploy
        container_config = ContainerConfig(name="app", image="nginx:1.20")
        deployment_config = DeploymentConfig(
            name="app-deployment",
            containers=[container_config]
        )
        await manager_k8s.deploy(deployment_config)
        
        # Rollback
        result = await manager_k8s.rollback("app-deployment", revision=1)
        
        assert result.success is True
        assert "Rollback of app-deployment completed" in result.message
    
    @pytest.mark.asyncio
    async def test_get_status(self, manager_k8s):
        """Test getting deployment status"""
        # Deploy
        container_config = ContainerConfig(name="app", image="nginx", replicas=3)
        deployment_config = DeploymentConfig(
            name="app-deployment",
            containers=[container_config]
        )
        await manager_k8s.deploy(deployment_config)
        
        # Get status
        result = await manager_k8s.get_status("app-deployment")
        
        assert result.success is True
        assert result.data is not None
        assert result.data["deployment_name"] == "app-deployment"
        assert result.data["status"] == "deployed"
        assert "pods" in result.data
    
    def test_validate_deployment(self, manager_k8s):
        """Test deployment validation"""
        # Valid deployment
        container = ContainerConfig(name="test", image="nginx", replicas=2)
        deployment = DeploymentConfig(
            name="test-deployment",
            containers=[container]
        )
        
        result = asyncio.run(manager_k8s._validate_deployment(deployment))
        assert result["success"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_deployment_no_containers(self, manager_k8s):
        """Test validation with no containers"""
        deployment = DeploymentConfig(
            name="empty-deployment",
            containers=[]
        )
        
        result = asyncio.run(manager_k8s._validate_deployment(deployment))
        assert result["success"] is False
        assert len(result["errors"]) > 0
    
    def test_validate_deployment_invalid_replicas(self, manager_k8s):
        """Test validation with invalid replicas"""
        container = ContainerConfig(name="test", image="nginx", replicas=-1)
        deployment = DeploymentConfig(
            name="test-deployment",
            containers=[container]
        )
        
        result = asyncio.run(manager_k8s._validate_deployment(deployment))
        assert result["success"] is False
        assert "invalid replicas" in result["errors"][0].lower()
    
    def test_validate_deployment_invalid_resources(self, manager_k8s):
        """Test validation with invalid resource specs"""
        container = ContainerConfig(
            name="test",
            image="nginx",
            cpu_request="invalid"
        )
        deployment = DeploymentConfig(
            name="test-deployment",
            containers=[container]
        )
        
        result = asyncio.run(manager_k8s._validate_deployment(deployment))
        assert result["success"] is False
        assert "invalid resource" in result["errors"][0].lower()
    
    def test_validate_deployment_scaling(self, manager_k8s):
        """Test scaling configuration validation"""
        container = ContainerConfig(name="test", image="nginx")
        deployment = DeploymentConfig(
            name="test-deployment",
            containers=[container],
            scaling_enabled=True,
            min_replicas=0,  # Invalid: must be >= 1
            max_replicas=5
        )
        
        result = asyncio.run(manager_k8s._validate_deployment(deployment))
        assert result["success"] is False
    
    def test_parse_resource(self, manager_k8s):
        """Test resource string parsing"""
        # Valid formats
        assert manager_k8s._parse_resource("100m") == "100m"
        assert manager_k8s._parse_resource("1Gi") == "1Gi"
        assert manager_k8s._parse_resource("512Mi") == "512Mi"
        
        # Invalid format
        with pytest.raises(ValueError):
            manager_k8s._parse_resource("invalid")
        
        with pytest.raises(ValueError):
            manager_k8s._parse_resource("")
    
    @pytest.mark.asyncio
    async def test_get_statistics(self, manager_k8s):
        """Test getting orchestration statistics"""
        # Deploy some containers
        container1 = ContainerConfig(name="app1", image="nginx")
        container2 = ContainerConfig(name="app2", image="redis")
        
        deployment1 = DeploymentConfig(
            name="deployment1",
            containers=[container1],
            namespace="default"
        )
        
        deployment2 = DeploymentConfig(
            name="deployment2",
            containers=[container2],
            namespace="staging"
        )
        
        await manager_k8s.deploy(deployment1)
        await manager_k8s.deploy(deployment2)
        
        # Get statistics
        stats = await manager_k8s.get_statistics()
        
        assert stats["orchestrator"] == "kubernetes"
        assert stats["total_deployments"] == 2
        assert stats["namespaces"] == 2
    
    @pytest.mark.asyncio
    async def test_deploy_with_health_checks(self, manager_k8s):
        """Test deploying with health checks"""
        container = ContainerConfig(
            name="app",
            image="app:latest",
            liveness_probe_path="/health",
            liveness_probe_port=8080,
            readiness_probe_path="/ready",
            readiness_probe_port=8080,
            startup_probe_path="/startup",
            startup_probe_port=8080
        )
        
        deployment = DeploymentConfig(
            name="app-deployment",
            containers=[container]
        )
        
        result = await manager_k8s.deploy(deployment)
        
        assert result.success is True
        container_spec = result.data["app"]["container_spec"]
        assert "livenessProbe" in container_spec
        assert "readinessProbe" in container_spec
        assert "startupProbe" in container_spec
    
    @pytest.mark.asyncio
    async def test_deploy_with_volumes(self, manager_k8s):
        """Test deploying with volumes"""
        container = ContainerConfig(
            name="app",
            image="app:latest",
            volumes=[
                {
                    "name": "data",
                    "persistentVolumeClaim": {"claimName": "pvc-data"}
                }
            ],
            volume_mounts=[
                {
                    "name": "data",
                    "mountPath": "/data"
                }
            ]
        )
        
        deployment = DeploymentConfig(
            name="app-deployment",
            containers=[container]
        )
        
        result = await manager_k8s.deploy(deployment)
        
        assert result.success is True
        container_spec = result.data["app"]["container_spec"]
        assert container_spec["volumes"] is not None
        assert container_spec["volumeMounts"] is not None
    
    @pytest.mark.asyncio
    async def test_deploy_with_service_mesh(self, manager_k8s):
        """Test deploying with service mesh"""
        container = ContainerConfig(name="app", image="app:latest")
        deployment = DeploymentConfig(
            name="app-deployment",
            containers=[container],
            service_mesh_enabled=True,
            service_mesh_config={
                "istio": {
                    "enabled": True
                }
            }
        )
        
        result = await manager_k8s.deploy(deployment)
        
        assert result.success is True
        assert result.data["service_mesh"] is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])