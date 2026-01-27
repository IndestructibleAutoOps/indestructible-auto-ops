"""
Unit tests for Monitoring Stack Manager
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch

import sys
sys.path.insert(0, '/workspace/machine-native-ops')

from adk.plugins.deployment.infrastructure.monitoring_manager import (
    MonitoringStackManager,
    MonitoringConfig,
    MonitoringProvider,
    StorageBackend,
    AlertRule,
    ScrapeConfig,
    DashboardConfig,
    MonitoringDeploymentResult
)


class TestMonitoringConfig:
    """Test MonitoringConfig dataclass"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = MonitoringConfig()
        
        assert config.provider == MonitoringProvider.PROMETHEUS
        assert config.storage_backend == StorageBackend.LOCAL
        assert config.prometheus_retention_days == 15
        assert config.grafana_replicas == 2
        assert config.alertmanager_replicas == 2
        assert config.ha_enabled is True
        assert config.ha_replicas == 2
        assert config.alerting_enabled is True
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = MonitoringConfig(
            provider=MonitoringProvider.CLOUDWATCH,
            storage_backend=StorageBackend.S3,
            prometheus_retention_days=30,
            grafana_replicas=3,
            alerting_enabled=False
        )
        
        assert config.provider == MonitoringProvider.CLOUDWATCH
        assert config.storage_backend == StorageBackend.S3
        assert config.prometheus_retention_days == 30
        assert config.grafana_replicas == 3
        assert config.alerting_enabled is False


class TestAlertRule:
    """Test AlertRule class"""
    
    def test_alert_rule_creation(self):
        """Test creating alert rule"""
        rule = AlertRule(
            name="HighCPUUsage",
            expr="cpu_usage > 80",
            for_duration="5m",
            labels={"severity": "warning"},
            annotations={"summary": "High CPU detected"},
            severity="warning"
        )
        
        assert rule.name == "HighCPUUsage"
        assert rule.expr == "cpu_usage > 80"
        assert rule.for_duration == "5m"
        assert rule.labels == {"severity": "warning"}
        assert rule.annotations == {"summary": "High CPU detected"}
        assert rule.severity == "warning"
    
    def test_alert_rule_to_dict(self):
        """Test converting alert rule to dictionary"""
        rule = AlertRule(
            name="HighMemoryUsage",
            expr="memory_usage > 85",
            for_duration="10m",
            labels={"severity": "critical"},
            annotations={"description": "Memory too high"},
            severity="critical"
        )
        
        rule_dict = rule.to_dict()
        
        assert rule_dict["alert"] == "HighMemoryUsage"
        assert rule_dict["expr"] == "memory_usage > 85"
        assert rule_dict["for"] == "10m"
        assert rule_dict["labels"] == {"severity": "critical"}
        assert rule_dict["annotations"] == {"description": "Memory too high"}


class TestScrapeConfig:
    """Test ScrapeConfig class"""
    
    def test_scrape_config_creation(self):
        """Test creating scrape configuration"""
        config = ScrapeConfig(
            job_name="prometheus",
            scrape_interval="15s",
            scrape_timeout="10s",
            metrics_path="/metrics",
            static_configs=[
                {"targets": ["localhost:9090"]}
            ]
        )
        
        assert config.job_name == "prometheus"
        assert config.scrape_interval == "15s"
        assert config.scrape_timeout == "10s"
        assert config.metrics_path == "/metrics"
        assert len(config.static_configs) == 1
    
    def test_scrape_config_to_dict(self):
        """Test converting scrape config to dictionary"""
        config = ScrapeConfig(
            job_name="kubernetes-pods",
            scrape_interval="30s",
            static_configs=[
                {"targets": ["pod1:9090", "pod2:9090"]},
                {"targets": ["pod3:9090"]}
            ]
        )
        
        config_dict = config.to_dict()
        
        assert config_dict["job_name"] == "kubernetes-pods"
        assert config_dict["scrape_interval"] == "30s"
        assert len(config_dict["static_configs"]) == 2


class TestDashboardConfig:
    """Test DashboardConfig class"""
    
    def test_dashboard_config_creation(self):
        """Test creating dashboard configuration"""
        config = DashboardConfig(
            title="Cluster Overview",
            tags=["kubernetes", "monitoring"],
            panels=[
                {
                    "title": "CPU Usage",
                    "type": "graph"
                },
                {
                    "title": "Memory Usage",
                    "type": "graph"
                }
            ]
        )
        
        assert config.title == "Cluster Overview"
        assert config.tags == ["kubernetes", "monitoring"]
        assert len(config.panels) == 2
    
    def test_dashboard_config_to_dict(self):
        """Test converting dashboard config to dictionary"""
        config = DashboardConfig(
            title="Application Metrics",
            panels=[
                {"title": "Request Rate", "type": "stat"},
                {"title": "Error Rate", "type": "gauge"}
            ],
            refresh="5s"
        )
        
        config_dict = config.to_dict()
        
        assert config_dict["title"] == "Application Metrics"
        assert len(config_dict["panels"]) == 2
        assert config_dict["refresh"] == "5s"


class TestMonitoringStackManager:
    """Test MonitoringStackManager class"""
    
    @pytest.fixture
    def config(self):
        """Create test configuration"""
        return MonitoringConfig()
    
    @pytest.fixture
    def manager(self, config):
        """Create monitoring stack manager instance"""
        return MonitoringStackManager("kubernetes", config)
    
    def test_manager_initialization(self, manager):
        """Test manager initialization"""
        assert manager.provider == "kubernetes"
        assert manager.config is not None
        assert manager._deployed_components == set()
        assert manager._alert_rules == []
        assert manager._scrape_configs == []
        assert manager._dashboards == []
    
    @pytest.mark.asyncio
    async def test_deploy_monitoring_stack(self, manager):
        """Test deploying monitoring stack"""
        result = await manager.deploy()
        
        assert isinstance(result, MonitoringDeploymentResult)
        assert result.success is True
        assert len(result.components_deployed) > 0
        assert result.deployment_time > 0
        assert "prometheus" in result.components_deployed
        assert "grafana" in result.components_deployed
        assert "alertmanager" in result.components_deployed
    
    @pytest.mark.asyncio
    async def test_deploy_with_alerting_disabled(self):
        """Test deploying without alerting"""
        config = MonitoringConfig(alerting_enabled=False)
        manager = MonitoringStackManager("kubernetes", config)
        
        result = await manager.deploy()
        
        assert result.success is True
        # AlertManager should not be deployed
        assert "alertmanager" not in result.components_deployed
    
    @pytest.mark.asyncio
    async def test_deploy_with_thanos_enabled(self):
        """Test deploying with Thanos for long-term storage"""
        config = MonitoringConfig(
            thanos_enabled=True,
            thanos_replicas=2
        )
        manager = MonitoringStackManager("kubernetes", config)
        
        result = await manager.deploy()
        
        assert result.success is True
        assert "thanos" in result.components_deployed
    
    @pytest.mark.asyncio
    async def test_add_alert_rule(self, manager):
        """Test adding custom alert rule"""
        rule = AlertRule(
            name="CustomAlert",
            expr="metric > 100",
            for_duration="1m",
            labels={"team": "devops"},
            annotations={"description": "Custom alert"}
        )
        
        manager.add_alert_rule(rule)
        
        assert len(manager._alert_rules) == 1
        assert manager._alert_rules[0].name == "CustomAlert"
    
    @pytest.mark.asyncio
    async def test_add_scrape_config(self, manager):
        """Test adding custom scrape configuration"""
        config = ScrapeConfig(
            job_name="custom-job",
            scrape_interval="10s",
            static_configs=[{"targets": ["localhost:8080"]}]
        )
        
        manager.add_scrape_config(config)
        
        assert len(manager._scrape_configs) == 1
        assert manager._scrape_configs[0].job_name == "custom-job"
    
    @pytest.mark.asyncio
    async def test_add_dashboard(self, manager):
        """Test adding custom dashboard"""
        dashboard = DashboardConfig(
            title="Custom Dashboard",
            panels=[{"title": "Test Panel", "type": "stat"}]
        )
        
        manager.add_dashboard(dashboard)
        
        assert len(manager._dashboards) == 1
        assert manager._dashboards[0].title == "Custom Dashboard"
    
    @pytest.mark.asyncio
    async def test_get_metrics(self, manager):
        """Test getting monitoring metrics"""
        metrics = await manager.get_metrics()
        
        assert isinstance(metrics, dict)
        assert "alert_rules_count" in metrics
        assert "scrape_configs_count" in metrics
        assert "dashboards_count" in metrics
        assert "deployed_components" in metrics
    
    @pytest.mark.asyncio
    async def test_export_config(self, manager):
        """Test exporting configuration"""
        config_dict = await manager.export_config()
        
        assert isinstance(config_dict, dict)
        assert "config" in config_dict
        assert "alert_rules" in config_dict
        assert "scrape_configs" in config_dict
        assert "dashboards" in config_dict
    
    @pytest.mark.asyncio
    async def test_build_prometheus_config(self, manager):
        """Test building Prometheus configuration"""
        prometheus_config = await manager._build_prometheus_config()
        
        assert isinstance(prometheus_config, dict)
        assert "global" in prometheus_config
        assert "scrape_configs" in prometheus_config
        assert "alerting" in prometheus_config
        assert "rule_files" in prometheus_config
    
    def test_get_default_scrape_configs(self, manager):
        """Test getting default scrape configurations"""
        configs = manager._get_default_scrape_configs()
        
        assert isinstance(configs, list)
        assert len(configs) > 0
        
        # Check for common scrape configs
        job_names = [config["job_name"] for config in configs]
        assert "prometheus" in job_names
        assert "kubernetes-apiservers" in job_names
        assert "kubernetes-pods" in job_names
    
    def test_get_default_alert_rules(self, manager):
        """Test getting default alert rules"""
        rules = manager._get_default_alert_rules()
        
        assert isinstance(rules, list)
        assert len(rules) > 0
        
        # Check for common alert rules
        rule_names = [rule.name for rule in rules]
        assert "HighCPUUsage" in rule_names
        assert "HighMemoryUsage" in rule_names
        assert "PodNotReady" in rule_names
    
    def test_get_default_dashboards(self, manager):
        """Test getting default dashboards"""
        dashboards = manager._get_default_dashboards()
        
        assert isinstance(dashboards, list)
        assert len(dashboards) > 0
        
        # Check for common dashboards
        dashboard_titles = [dashboard.title for dashboard in dashboards]
        assert "Kubernetes Cluster Overview" in dashboard_titles
        assert "Node Performance" in dashboard_titles
    
    @pytest.mark.asyncio
    async def test_verify_deployment(self, manager):
        """Test deployment verification"""
        result = await manager._verify_deployment()
        
        assert isinstance(result, dict)
        assert "success" in result
        assert "warnings" in result
    
    @pytest.mark.asyncio
    async def test_deploy_storage(self, manager):
        """Test deploying storage backend"""
        result = await manager._deploy_storage()
        
        assert isinstance(result, dict)
        assert result["success"] is True
        assert "storage_config" in result
        assert result["storage_config"]["backend"] == "local"


class TestMonitoringIntegration:
    """Integration tests for monitoring stack"""
    
    @pytest.mark.asyncio
    async def test_full_deployment_with_custom_configurations(self):
        """Test full deployment with custom configurations"""
        config = MonitoringConfig(
            ha_enabled=True,
            ha_replicas=3,
            alerting_enabled=True,
            pushgateway_enabled=True,
            node_exporter_enabled=True,
            kube_state_metrics_enabled=True
        )
        
        manager = MonitoringStackManager("kubernetes", config)
        
        # Add custom configurations
        manager.add_alert_rule(AlertRule(
            name="TestAlert",
            expr="test_metric > 0",
            for_duration="1m",
            labels={},
            annotations={}
        ))
        
        manager.add_scrape_config(ScrapeConfig(
            job_name="test-job",
            scrape_interval="5s",
            static_configs=[{"targets": ["test:9090"]}]
        ))
        
        manager.add_dashboard(DashboardConfig(
            title="Test Dashboard",
            panels=[{"title": "Test", "type": "stat"}]
        ))
        
        # Deploy
        result = await manager.deploy()
        
        assert result.success is True
        assert result.deployment_time > 0
        assert len(result.components_deployed) >= 6  # prometheus, grafana, alertmanager, pushgateway, node_exporter, kube_state_metrics


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])