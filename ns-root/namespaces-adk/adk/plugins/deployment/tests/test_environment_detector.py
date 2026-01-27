"""
Tests for Enhanced Environment Detector
"""

import pytest
from unittest.mock import patch

from ..detectors.environment_detector import EnvironmentDetector, EnvironmentInfo


class TestEnvironmentDetector:
    """Test EnvironmentDetector with enhanced functionality"""
    
    @pytest.fixture
    def mock_kubernetes_env(self):
        """Mock Kubernetes environment"""
        with patch.object(EnvironmentDetector, '_is_kubernetes', return_value=True):
            yield
    
    @pytest.fixture
    def mock_docker_env(self):
        """Mock Docker environment"""
        with patch.object(EnvironmentDetector, '_is_kubernetes', return_value=False), \
             patch.object(EnvironmentDetector, '_is_docker', return_value=True):
            yield
    
    @pytest.fixture
    def mock_aws_env(self):
        """Mock AWS environment"""
        with patch.object(EnvironmentDetector, '_is_kubernetes', return_value=False), \
             patch.object(EnvironmentDetector, '_is_docker', return_value=False), \
             patch.object(EnvironmentDetector, '_check_aws_metadata', return_value={
                 'instance_id': 'i-12345',
                 'instance_type': 't3.medium',
                 'availability_zone': 'us-east-1a',
                 'region': 'us-east-1',
                 'iam_role': 'test-role'
             }):
            yield
    
    @pytest.fixture
    def mock_gcp_env(self):
        """Mock GCP environment"""
        with patch.object(EnvironmentDetector, '_is_kubernetes', return_value=False), \
             patch.object(EnvironmentDetector, '_is_docker', return_value=False), \
             patch.object(EnvironmentDetector, '_check_gcp_metadata', return_value={
                 'instance_id': '123456789',
                 'machine_type': 'n1-standard-2',
                 'zone': 'us-central1-a',
                 'project_id': 'my-project'
             }):
            yield
    
    def test_detect_kubernetes(self, mock_kubernetes_env):
        """Test Kubernetes environment detection"""
        with patch.object(EnvironmentDetector, '_detect_kubernetes_environment', 
                         return_value=EnvironmentInfo(
                             type='kubernetes',
                             provider='aws-eks',
                             version='1.28.0',
                             cluster_name='my-cluster',
                             metadata={'kubernetes': True}
                         )):
            env_info = EnvironmentDetector.detect()
            
            assert env_info.type == 'kubernetes'
            assert env_info.provider == 'aws-eks'
            assert env_info.version == '1.28.0'
            assert env_info.cluster_name == 'my-cluster'
            assert env_info.is_cloud() == False
            assert env_info.is_container_platform() == True
    
    def test_detect_docker(self, mock_docker_env):
        """Test Docker environment detection"""
        with patch.object(EnvironmentDetector, '_detect_docker_environment',
                         return_value=EnvironmentInfo(
                             type='docker',
                             provider='docker',
                             version='20.10.0',
                             instance_id='container-123',
                             metadata={'docker': True}
                         )):
            env_info = EnvironmentDetector.detect()
            
            assert env_info.type == 'docker'
            assert env_info.provider == 'docker'
            assert env_info.version == '20.10.0'
            assert env_info.is_container_platform() == True
    
    def test_detect_aws(self, mock_aws_env):
        """Test AWS environment detection"""
        env_info = EnvironmentDetector.detect()
        
        assert env_info.type == 'aws'
        assert env_info.provider == 'aws'
        assert env_info.region == 'us-east-1'
        assert env_info.zone == 'us-east-1a'
        assert env_info.instance_id == 'i-12345'
        assert env_info.instance_type == 't3.medium'
        assert env_info.is_cloud() == True
    
    def test_detect_gcp(self, mock_gcp_env):
        """Test GCP environment detection"""
        env_info = EnvironmentDetector.detect()
        
        assert env_info.type == 'gcp'
        assert env_info.provider == 'gcp'
        assert env_info.region == 'us-central1'
        assert env_info.zone == 'us-central1-a'
        assert env_info.instance_id == '123456789'
        assert env_info.instance_type == 'n1-standard-2'
        assert env_info.is_cloud() == True
    
    def test_environment_info_to_dict(self):
        """Test EnvironmentInfo to_dict method"""
        env_info = EnvironmentInfo(
            type='aws',
            provider='aws',
            version='1.0.0',
            region='us-east-1',
            zone='us-east-1a',
            cluster_name='my-cluster',
            instance_id='i-12345',
            instance_type='t3.medium',
            metadata={'test': 'value'}
        )
        
        env_dict = env_info.to_dict()
        
        assert env_dict['type'] == 'aws'
        assert env_dict['provider'] == 'aws'
        assert env_dict['region'] == 'us-east-1'
        assert env_dict['zone'] == 'us-east-1a'
        assert env_dict['cluster_name'] == 'my-cluster'
        assert env_dict['instance_id'] == 'i-12345'
        assert env_dict['instance_type'] == 't3.medium'
        assert env_dict['metadata'] == {'test': 'value'}
    
    def test_zone_to_region(self):
        """Test zone to region conversion"""
        assert EnvironmentDetector._zone_to_region('us-central1-a') == 'us-central1'
        assert EnvironmentDetector._zone_to_region('europe-west2-b') == 'europe-west2'
        assert EnvironmentDetector._zone_to_region('simple') == 'simple'