# FILE: tests/integration/test_kubernetes_deployment.py
# 集成測試：Kubernetes 部署驗證

import pytest
import yaml
import os


class TestKubernetesDeploymentValidation:
    """Test Kubernetes Deployment Validation"""
    
    def load_yaml_file(self, filepath: str) -> dict:
        """Load YAML file"""
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    
    @pytest.mark.skipif(
        not os.path.exists("infrastructure/kubernetes/namespaces/axiom-system.yaml"),
        reason="Kubernetes YAML file not found"
    )
    def test_namespace_yaml_validity(self):
        """Test namespace YAML validity"""
        yaml_file = "infrastructure/kubernetes/namespaces/axiom-system.yaml"
        
        data = self.load_yaml_file(yaml_file)
        assert data is not None
        assert "metadata" in data
        assert data["metadata"]["name"] == "axiom-system"
    
    @pytest.mark.skipif(
        not os.path.exists("infrastructure/kubernetes/rbac/axiom-rbac.yaml"),
        reason="Kubernetes RBAC YAML file not found"
    )
    def test_rbac_yaml_validity(self):
        """Test RBAC YAML validity"""
        yaml_file = "infrastructure/kubernetes/rbac/axiom-rbac.yaml"
        
        with open(yaml_file, 'r') as f:
            docs = yaml.safe_load_all(f)
            
            for doc in docs:
                if doc is None:
                    continue
                
                assert "kind" in doc
                assert "metadata" in doc
    
    @pytest.mark.skipif(
        not os.path.exists("infrastructure/kubernetes/deployments/ng-semantic-binding-service.yaml"),
        reason="Kubernetes deployment YAML file not found"
    )
    def test_deployment_yaml_validity(self):
        """Test deployment YAML validity"""
        yaml_file = "infrastructure/kubernetes/deployments/ng-semantic-binding-service.yaml"
        
        with open(yaml_file, 'r') as f:
            docs = yaml.safe_load_all(f)
            
            deployment_found = False
            for doc in docs:
                if doc is None:
                    continue
                
                if doc.get("kind") == "Deployment":
                    deployment_found = True
                    assert "spec" in doc
                    assert "template" in doc["spec"]
                    assert "containers" in doc["spec"]["template"]["spec"]
            
            assert deployment_found is True
    
    @pytest.mark.skipif(
        not os.path.exists("infrastructure/kubernetes/deployments/ng-semantic-binding-service.yaml"),
        reason="Kubernetes service YAML file not found"
    )
    def test_service_yaml_validity(self):
        """Test service YAML validity"""
        yaml_file = "infrastructure/kubernetes/deployments/ng-semantic-binding-service.yaml"
        
        with open(yaml_file, 'r') as f:
            docs = yaml.safe_load_all(f)
            
            service_found = False
            for doc in docs:
                if doc is None:
                    continue
                
                if doc.get("kind") == "Service":
                    service_found = True
                    assert "spec" in doc
                    assert "ports" in doc["spec"]
            
            assert service_found is True
    
    @pytest.mark.skipif(
        not os.path.exists("infrastructure/kubernetes/deployments/ng-semantic-binding-service.yaml"),
        reason="Kubernetes ConfigMap YAML file not found"
    )
    def test_configmap_yaml_validity(self):
        """Test ConfigMap YAML validity"""
        yaml_file = "infrastructure/kubernetes/deployments/ng-semantic-binding-service.yaml"
        
        with open(yaml_file, 'r') as f:
            docs = yaml.safe_load_all(f)
            
            configmap_found = False
            for doc in docs:
                if doc is None:
                    continue
                
                if doc.get("kind") == "ConfigMap":
                    configmap_found = True
                    assert "data" in doc
            
            assert configmap_found is True
    
    @pytest.mark.skipif(
        not os.path.exists("infrastructure/kubernetes/namespaces/axiom-system.yaml"),
        reason="Kubernetes resource quota YAML file not found"
    )
    def test_resource_quota_validity(self):
        """Test resource quota validity"""
        yaml_file = "infrastructure/kubernetes/namespaces/axiom-system.yaml"
        
        with open(yaml_file, 'r') as f:
            docs = yaml.safe_load_all(f)
            
            quota_found = False
            for doc in docs:
                if doc is None:
                    continue
                
                if doc.get("kind") == "ResourceQuota":
                    quota_found = True
                    assert "spec" in doc
                    assert "hard" in doc["spec"]
            
            assert quota_found is True
    
    @pytest.mark.skipif(
        not os.path.exists("infrastructure/kubernetes/namespaces/axiom-system.yaml"),
        reason="Kubernetes limit range YAML file not found"
    )
    def test_limit_range_validity(self):
        """Test limit range validity"""
        yaml_file = "infrastructure/kubernetes/namespaces/axiom-system.yaml"
        
        with open(yaml_file, 'r') as f:
            docs = yaml.safe_load_all(f)
            
            limit_found = False
            for doc in docs:
                if doc is None:
                    continue
                
                if doc.get("kind") == "LimitRange":
                    limit_found = True
                    assert "spec" in doc
                    assert "limits" in doc["spec"]
            
            assert limit_found is True