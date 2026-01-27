"""
Tests for Enhanced Configuration Loader
"""

import pytest
import os
import tempfile

from ..loaders.config_loader import ConfigLoader


class TestConfigLoader:
    """Test ConfigLoader with hierarchical merging"""
    
    @pytest.fixture
    def temp_base_path(self):
        """Create temporary base path for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
    
    @pytest.fixture
    def config_loader(self, temp_base_path):
        """Create ConfigLoader instance"""
        return ConfigLoader(base_path=temp_base_path)
    
    def test_deep_merge_dicts(self, config_loader):
        """Test deep merge of dictionaries"""
        base = {
            'section1': {
                'key1': 'value1',
                'key2': 'value2'
            },
            'section2': {
                'key3': 'value3'
            }
        }
        
        override = {
            'section1': {
                'key2': 'new_value2',  # Override
                'key4': 'value4'       # New key
            },
            'section3': {               # New section
                'key5': 'value5'
            }
        }
        
        result = config_loader._deep_merge(base, override)
        
        # Check merged values
        assert result['section1']['key1'] == 'value1'  # Unchanged
        assert result['section1']['key2'] == 'new_value2'  # Overridden
        assert result['section1']['key4'] == 'value4'  # New
        assert result['section2']['key3'] == 'value3'  # Unchanged
        assert result['section3']['key5'] == 'value5'  # New section
    
    def test_deep_merge_lists(self, config_loader):
        """Test deep merge of lists"""
        base = {
            'items': ['a', 'b', 'c']
        }
        
        override = {
            'items': ['d', 'e']
        }
        
        result = config_loader._deep_merge(base, override)
        
        # Lists should be concatenated
        assert result['items'] == ['a', 'b', 'c', 'd', 'e']
    
    def test_deep_merge_mixed_types(self, config_loader):
        """Test deep merge with mixed types"""
        base = {
            'string': 'value1',
            'number': 100,
            'boolean': True
        }
        
        override = {
            'string': 'value2',  # Override
            'number': 200,       # Override
            'boolean': False     # Override
        }
        
        result = config_loader._deep_merge(base, override)
        
        assert result['string'] == 'value2'
        assert result['number'] == 200
        assert result['boolean'] == False
    
    def test_parse_env_value_boolean(self, config_loader):
        """Test parsing environment variable to boolean"""
        assert config_loader._parse_env_value('true') is True
        assert config_loader._parse_env_value('TRUE') is True
        assert config_loader._parse_env_value('yes') is True
        assert config_loader._parse_env_value('1') is True
        assert config_loader._parse_env_value('false') is False
        assert config_loader._parse_env_value('FALSE') is False
        assert config_loader._parse_env_value('no') is False
        assert config_loader._parse_env_value('0') is False
    
    def test_parse_env_value_number(self, config_loader):
        """Test parsing environment variable to number"""
        assert config_loader._parse_env_value('123') == 123
        assert config_loader._parse_env_value('-456') == -456
        assert config_loader._parse_env_value('3.14') == 3.14
        assert config_loader._parse_env_value('-2.71') == -2.71
    
    def test_parse_env_value_json(self, config_loader):
        """Test parsing environment variable to JSON"""
        result = config_loader._parse_env_value('["a", "b", "c"]')
        assert result == ['a', 'b', 'c']
        
        result = config_loader._parse_env_value('{"key": "value"}')
        assert result == {'key': 'value'}
    
    def test_parse_env_value_string(self, config_loader):
        """Test parsing environment variable to string"""
        assert config_loader._parse_env_value('hello') == 'hello'
        assert config_loader._parse_env_value('not-a-number') == 'not-a-number'
    
    def test_apply_env_overrides(self, config_loader):
        """Test applying environment variable overrides"""
        # Set environment variables
        os.environ['AWS__INFRASTRUCTURE__VPC__CIDR'] = '10.1.0.0/16'
        os.environ['KUBERNETES__DEPLOYMENT__REPLICAS'] = '5'
        os.environ['DOCKER_COMPOSE__SERVICES__API_SERVER__PORT'] = '8080'
        
        try:
            config = {
                'infrastructure': {
                    'vpc': {'cidr': '10.0.0.0/16'}
                },
                'deployment': {
                    'replicas': 3
                }
            }
            
            result = config_loader._apply_env_overrides(config)
            
            # Check overrides
            assert result['infrastructure']['vpc']['cidr'] == '10.1.0.0/16'
            assert result['deployment']['replicas'] == 5
            assert result['services']['api-server']['port'] == 8080
            
        finally:
            # Clean up
            del os.environ['AWS__INFRASTRUCTURE__VPC__CIDR']
            del os.environ['KUBERNETES__DEPLOYMENT__REPLICAS']
            del os.environ['DOCKER_COMPOSE__SERVICES__API_SERVER__PORT']
    
    def test_load_secrets_from_env(self, config_loader):
        """Test loading secrets from environment variables"""
        os.environ['SECRET__DATABASE_PASSWORD'] = 'secret123'
        os.environ['SECRET__API_KEY'] = 'key456'
        
        try:
            secrets = config_loader._load_secrets_from_env()
            
            assert secrets['database-password'] == 'secret123'
            assert secrets['api-key'] == 'key456'
            
        finally:
            del os.environ['SECRET__DATABASE_PASSWORD']
            del os.environ['SECRET__API_KEY']
    
    def test_validate_config_basic(self, config_loader):
        """Test basic configuration validation"""
        config = {
            'provider': 'aws',
            'environment': 'production',
            'infrastructure': {
                'vpc': {
                    'enabled': True,
                    'cidr': '10.0.0.0/16'
                }
            }
        }
        
        # Should not raise exception
        config_loader._validate_config(config)
    
    def test_validate_config_invalid(self, config_loader):
        """Test invalid configuration"""
        config = "not a dictionary"
        
        with pytest.raises(ValueError, match="Configuration must be a dictionary"):
            config_loader._validate_config(config)