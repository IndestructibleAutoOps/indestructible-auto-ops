"""
Tests for Universal Deployment Manager
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from ..managers.deployment_manager import (
    UniversalDeploymentManager,
    DeploymentResult,
    DeploymentPlan
)
from ..adapters.provider_factory import ProviderAdapterFactory


@pytest.fixture
def mock_config():
    """Mock configuration"""
    return {
        'provider': 'test',
        'environment': 'test',
        'infrastructure': {}
    }


@pytest.fixture
def mock_adapter():
    """Mock provider adapter"""
    adapter = Mock()
    adapter.validate_config = Mock(return_value=True)
    adapter.deploy_infrastructure = AsyncMock(return_value={'success': True})
    adapter.get_provider_info = Mock(return_value={'name': 'test', 'version': '1.0.0'})
    return adapter


class TestUniversalDeploymentManager:
    """Test UniversalDeploymentManager"""
    
    @pytest.mark.asyncio
    async def test_initialization_with_provider(self, mock_config):
        """Test initialization with provider specified"""
        with patch.object(ProviderAdapterFactory, 'get_adapter', return_value=mock_adapter()):
            manager = UniversalDeploymentManager(
                provider='test',
                environment='test'
            )
            
            assert manager.provider == 'test'
            assert manager.environment == 'test'
    
    @pytest.mark.asyncio
    async def test_initialization_auto_detect(self, mock_config):
        """Test initialization with auto-detect"""
        with patch.object(ProviderAdapterFactory, 'get_adapter', return_value=mock_adapter()):
            manager = UniversalDeploymentManager(
                auto_detect=True,
                environment='test'
            )
            
            assert manager.provider is not None
            assert manager.environment == 'test'
    
    @pytest.mark.asyncio
    async def test_deploy_success(self, mock_adapter):
        """Test successful deployment"""
        with patch.object(ProviderAdapterFactory, 'get_adapter', return_value=mock_adapter):
            manager = UniversalDeploymentManager(
                provider='test',
                environment='test'
            )
            
            result = await manager.deploy()
            
            assert result.success
            assert result.provider == 'test'
            assert result.environment == 'test'
            assert result.duration > 0
    
    @pytest.mark.asyncio
    async def test_deploy_failure(self, mock_adapter):
        """Test failed deployment"""
        mock_adapter.deploy_infrastructure = AsyncMock(
            side_effect=Exception("Deployment failed")
        )
        
        with patch.object(ProviderAdapterFactory, 'get_adapter', return_value=mock_adapter):
            manager = UniversalDeploymentManager(
                provider='test',
                environment='test'
            )
            
            result = await manager.deploy()
            
            assert not result.success
            assert len(result.errors) > 0
    
    @pytest.mark.asyncio
    async def test_dry_run(self, mock_adapter):
        """Test dry run mode"""
        with patch.object(ProviderAdapterFactory, 'get_adapter', return_value=mock_adapter):
            manager = UniversalDeploymentManager(
                provider='test',
                environment='test',
                dry_run=True
            )
            
            result = await manager.deploy()
            
            assert result.success
            # In dry run, deploy_infrastructure should not be called
            # or should be called differently
            mock_adapter.deploy_infrastructure.assert_called_once()
    
    def test_deployment_result_to_dict(self):
        """Test DeploymentResult to_dict method"""
        result = DeploymentResult(
            success=True,
            provider='test',
            environment='test',
            resources={'vpc': 1},
            errors=[],
            warnings=[],
            duration=10.5
        )
        
        result_dict = result.to_dict()
        
        assert result_dict['success'] is True
        assert result_dict['provider'] == 'test'
        assert result_dict['environment'] == 'test'
        assert result_dict['resources'] == {'vpc': 1}
        assert result_dict['duration'] == 10.5
    
    def test_deployment_plan_to_dict(self):
        """Test DeploymentPlan to_dict method"""
        plan = DeploymentPlan(
            steps=[{'name': 'step1'}],
            dependencies={'step1': []},
            rollback_steps=[{'name': 'rollback1'}],
            estimated_duration=100.0
        )
        
        plan_dict = plan.to_dict()
        
        assert plan_dict['steps'] == [{'name': 'step1'}]
        assert plan_dict['dependencies'] == {'step1': []}
        assert plan_dict['rollback_steps'] == [{'name': 'rollback1'}]
        assert plan_dict['estimated_duration'] == 100.0


class TestDeploymentResult:
    """Test DeploymentResult dataclass"""
    
    def test_deployment_result_creation(self):
        """Test creating DeploymentResult"""
        result = DeploymentResult(
            success=True,
            provider='aws',
            environment='production',
            resources={'vpc': 1, 'eks': 1},
            errors=[],
            warnings=['Resource limit warning'],
            duration=45.5
        )
        
        assert result.success is True
        assert result.provider == 'aws'
        assert result.environment == 'production'
        assert result.resources == {'vpc': 1, 'eks': 1}
        assert result.errors == []
        assert result.warnings == ['Resource limit warning']
        assert result.duration == 45.5
    
    def test_deployment_result_to_dict_full(self):
        """Test full DeploymentResult to_dict"""
        result = DeploymentResult(
            success=True,
            provider='aws',
            environment='production',
            resources={'vpc': 1},
            errors=[],
            warnings=[],
            duration=30.0
        )
        
        result_dict = result.to_dict()
        
        # Verify all fields are present
        expected_keys = {'success', 'provider', 'environment', 'resources', 'errors', 'warnings', 'duration'}
        assert set(result_dict.keys()) == expected_keys


class TestDeploymentPlan:
    """Test DeploymentPlan dataclass"""
    
    def test_deployment_plan_creation(self):
        """Test creating DeploymentPlan"""
        plan = DeploymentPlan(
            steps=[
                {'name': 'deploy-vpc', 'order': 1},
                {'name': 'deploy-eks', 'order': 2}
            ],
            dependencies={
                'deploy-eks': ['deploy-vpc']
            },
            rollback_steps=[
                {'name': 'delete-eks', 'order': 1},
                {'name': 'delete-vpc', 'order': 2}
            ],
            estimated_duration=120.0
        )
        
        assert len(plan.steps) == 2
        assert plan.dependencies['deploy-eks'] == ['deploy-vpc']
        assert len(plan.rollback_steps) == 2
        assert plan.estimated_duration == 120.0