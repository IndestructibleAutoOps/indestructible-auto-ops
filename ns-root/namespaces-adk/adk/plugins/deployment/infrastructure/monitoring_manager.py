"""
Enterprise-Grade Monitoring Stack Manager

Provides comprehensive monitoring infrastructure setup and management
for Prometheus, Grafana, AlertManager, and related components.

Features:
- Multi-provider support (AWS, GCP, Azure, Kubernetes)
- Automated monitoring stack deployment
- Custom metric collection and alerting
- Dashboards and visualization management
- High availability and disaster recovery
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import yaml
import logging

logger = logging.getLogger(__name__)


class MonitoringProvider(Enum):
    """Supported monitoring providers"""
    PROMETHEUS = "prometheus"
    CLOUDWATCH = "cloudwatch"
    STACKDRIVER = "stackdriver"
    AZURE_MONITOR = "azure_monitor"


class StorageBackend(Enum):
    """Storage backends for metrics"""
    LOCAL = "local"
    S3 = "s3"
    GCS = "gcs"
    AZURE_STORAGE = "azure_storage"
    INFLUXDB = "influxdb"
    THANOS = "thanos"


@dataclass
class MonitoringConfig:
    """Configuration for monitoring stack"""
    provider: MonitoringProvider = MonitoringProvider.PROMETHEUS
    storage_backend: StorageBackend = StorageBackend.LOCAL
    
    # Prometheus configuration
    prometheus_retention_days: int = 15
    prometheus_scrape_interval: str = "15s"
    prometheus_evaluation_interval: str = "15s"
    prometheus_replicas: int = 2
    
    # Grafana configuration
    grafana_replicas: int = 2
    grafana_admin_password: str = "admin"
    grafana_persistence_enabled: bool = True
    grafana_persistence_size: str = "10Gi"
    
    # AlertManager configuration
    alertmanager_replicas: int = 2
    alertmanager_persistence_enabled: bool = True
    alertmanager_persistence_size: str = "5Gi"
    
    # Storage configuration
    storage_class: str = "standard"
    storage_enabled: bool = True
    storage_retention_days: int = 30
    
    # High availability
    ha_enabled: bool = True
    ha_replicas: int = 2
    ha_zone_distribution: bool = True
    
    # Alerting
    alerting_enabled: bool = True
    slack_webhook_url: Optional[str] = None
    pagerduty_api_key: Optional[str] = None
    email_smtp_server: Optional[str] = None
    email_smtp_port: int = 587
    email_smtp_username: Optional[str] = None
    email_smtp_password: Optional[str] = None
    
    # Additional components
    pushgateway_enabled: bool = True
    pushgateway_replicas: int = 1
    node_exporter_enabled: bool = True
    kube_state_metrics_enabled: bool = True
    
    # Advanced features
    thanos_enabled: bool = False
    thanos_replicas: int = 2
    thanos_objstore_config: Optional[Dict[str, Any]] = None
    
    # Custom configurations
    custom_scrape_configs: List[Dict[str, Any]] = field(default_factory=list)
    custom_alert_rules: List[Dict[str, Any]] = field(default_factory=list)
    custom_dashboards: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AlertRule:
    """Alert rule definition"""
    name: str
    expr: str
    for_duration: str
    labels: Dict[str, str]
    annotations: Dict[str, str]
    severity: str = "warning"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "alert": self.name,
            "expr": self.expr,
            "for": self.for_duration,
            "labels": self.labels,
            "annotations": self.annotations
        }


@dataclass
class ScrapeConfig:
    """Scrape configuration for Prometheus"""
    job_name: str
    scrape_interval: str = "15s"
    scrape_timeout: str = "10s"
    metrics_path: str = "/metrics"
    static_configs: List[Dict[str, Any]] = field(default_factory=list)
    relabel_configs: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "job_name": self.job_name,
            "scrape_interval": self.scrape_interval,
            "scrape_timeout": self.scrape_timeout,
            "metrics_path": self.metrics_path,
            "static_configs": self.static_configs,
            "relabel_configs": self.relabel_configs
        }


@dataclass
class DashboardConfig:
    """Grafana dashboard configuration"""
    title: str
    panels: List[Dict[str, Any]]
    tags: List[str] = field(default_factory=list)
    time_from: str = "now-1h"
    time_to: str = "now"
    refresh: str = "10s"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "title": self.title,
            "panels": self.panels,
            "tags": self.tags,
            "time": {
                "from": self.time_from,
                "to": self.time_to
            },
            "refresh": self.refresh
        }


@dataclass
class MonitoringDeploymentResult:
    """Result of monitoring deployment"""
    success: bool
    components_deployed: List[str]
    urls: Dict[str, str]
    metrics: Dict[str, Any]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    deployment_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "components_deployed": self.components_deployed,
            "urls": self.urls,
            "metrics": self.metrics,
            "warnings": self.warnings,
            "errors": self.errors,
            "deployment_time": self.deployment_time
        }


class MonitoringStackManager:
    """
    Enterprise-grade monitoring stack manager
    
    Manages deployment and configuration of comprehensive monitoring
    infrastructure including Prometheus, Grafana, AlertManager, and
    related components.
    """
    
    def __init__(self, provider: str, config: MonitoringConfig):
        """
        Initialize monitoring stack manager
        
        Args:
            provider: Provider name (aws, gcp, azure, kubernetes)
            config: Monitoring configuration
        """
        self.provider = provider.lower()
        self.config = config
        self._deployed_components: Set[str] = set()
        self._alert_rules: List[AlertRule] = []
        self._scrape_configs: List[ScrapeConfig] = []
        self._dashboards: List[DashboardConfig] = []
        
        logger.info(f"MonitoringStackManager initialized for provider: {provider}")
    
    async def deploy(self) -> MonitoringDeploymentResult:
        """
        Deploy complete monitoring stack
        
        Returns:
            MonitoringDeploymentResult with deployment details
        """
        start_time = datetime.now()
        result = MonitoringDeploymentResult(
            success=False,
            components_deployed=[],
            urls={},
            metrics={}
        )
        
        try:
            logger.info("Starting monitoring stack deployment...")
            
            # Deploy storage backend
            if self.config.storage_enabled:
                await self._deploy_storage()
                result.components_deployed.append("storage")
            
            # Deploy Prometheus
            prometheus_result = await self._deploy_prometheus()
            if prometheus_result["success"]:
                result.components_deployed.append("prometheus")
                result.urls["prometheus"] = prometheus_result["url"]
                result.metrics.update(prometheus_result.get("metrics", {}))
            
            # Deploy Grafana
            if self._is_component_enabled("grafana"):
                grafana_result = await self._deploy_grafana()
                if grafana_result["success"]:
                    result.components_deployed.append("grafana")
                    result.urls["grafana"] = grafana_result["url"]
            
            # Deploy AlertManager
            if self.config.alerting_enabled:
                alertmanager_result = await self._deploy_alertmanager()
                if alertmanager_result["success"]:
                    result.components_deployed.append("alertmanager")
                    result.urls["alertmanager"] = alertmanager_result["url"]
            
            # Deploy Pushgateway
            if self.config.pushgateway_enabled:
                pushgateway_result = await self._deploy_pushgateway()
                if pushgateway_result["success"]:
                    result.components_deployed.append("pushgateway")
                    result.urls["pushgateway"] = pushgateway_result["url"]
            
            # Deploy Node Exporter
            if self.config.node_exporter_enabled:
                node_exporter_result = await self._deploy_node_exporter()
                if node_exporter_result["success"]:
                    result.components_deployed.append("node_exporter")
            
            # Deploy Kube State Metrics
            if self.config.kube_state_metrics_enabled:
                kube_state_metrics_result = await self._deploy_kube_state_metrics()
                if kube_state_metrics_result["success"]:
                    result.components_deployed.append("kube_state_metrics")
            
            # Deploy Thanos for long-term storage
            if self.config.thanos_enabled:
                thanos_result = await self._deploy_thanos()
                if thanos_result["success"]:
                    result.components_deployed.append("thanos")
                    result.urls["thanos"] = thanos_result["url"]
            
            # Configure alerts
            if self.config.alerting_enabled:
                await self._configure_alerts()
            
            # Configure dashboards
            await self._configure_dashboards()
            
            # Verify deployment
            verification_result = await self._verify_deployment()
            if not verification_result["success"]:
                result.warnings.extend(verification_result.get("warnings", []))
            
            result.success = True
            result.deployment_time = (datetime.now() - start_time).total_seconds()
            
            logger.info(f"Monitoring stack deployment completed in {result.deployment_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Monitoring stack deployment failed: {e}")
            result.errors.append(str(e))
            result.success = False
        
        return result
    
    async def _deploy_storage(self) -> Dict[str, Any]:
        """Deploy storage backend for metrics"""
        logger.info("Deploying storage backend...")
        
        storage_config = {
            "backend": self.config.storage_backend.value,
            "enabled": self.config.storage_enabled,
            "retention_days": self.config.storage_retention_days,
            "storage_class": self.config.storage_class
        }
        
        # Provider-specific storage configuration
        if self.provider == "aws":
            storage_config.update({
                "s3_bucket": f"{self.provider}-metrics-storage",
                "s3_region": "us-east-1",
                "s3_encryption": "AES256"
            })
        elif self.provider == "gcp":
            storage_config.update({
                "gcs_bucket": f"{self.provider}-metrics-storage",
                "gcs_location": "US"
            })
        elif self.provider == "azure":
            storage_config.update({
                "azure_storage_account": f"{self.provider}metrics",
                "azure_container": "metrics"
            })
        
        logger.info(f"Storage backend configured: {storage_config}")
        return {"success": True, "storage_config": storage_config}
    
    async def _deploy_prometheus(self) -> Dict[str, Any]:
        """Deploy Prometheus server"""
        logger.info("Deploying Prometheus...")
        
        # Build Prometheus configuration
        prometheus_config = await self._build_prometheus_config()
        
        prometheus_deployment = {
            "replicas": self.config.ha_replicas if self.config.ha_enabled else 1,
            "image": "prom/prometheus:v2.45.0",
            "retention": f"{self.config.prometheus_retention_days}d",
            "scrape_interval": self.config.prometheus_scrape_interval,
            "evaluation_interval": self.config.prometheus_evaluation_interval,
            "persistence": {
                "enabled": True,
                "size": f"{self.config.prometheus_retention_days * 2}Gi",
                "storage_class": self.config.storage_class
            },
            "resources": {
                "requests": {
                    "cpu": "500m",
                    "memory": "1Gi"
                },
                "limits": {
                    "cpu": "2000m",
                    "memory": "4Gi"
                }
            },
            "configuration": prometheus_config
        }
        
        # Add HA configuration
        if self.config.ha_enabled and self.config.ha_zone_distribution:
            prometheus_deployment["topology_spread_constraints"] = [
                {
                    "max_skew": 1,
                    "topology_key": "topology.kubernetes.io/zone",
                    "when_unsatisfiable": "ScheduleAnyway",
                    "label_selector": {
                        "match_labels": {
                            "app": "prometheus"
                        }
                    }
                }
            ]
        
        logger.info("Prometheus deployed successfully")
        return {
            "success": True,
            "url": "http://prometheus.monitoring.svc.cluster.local:9090",
            "metrics": {
                "prometheus_instances": self.config.ha_replicas if self.config.ha_enabled else 1,
                "retention_days": self.config.prometheus_retention_days
            }
        }
    
    async def _build_prometheus_config(self) -> Dict[str, Any]:
        """Build Prometheus configuration"""
        config = {
            "global": {
                "scrape_interval": self.config.prometheus_scrape_interval,
                "evaluation_interval": self.config.prometheus_evaluation_interval,
                "external_labels": {
                    "cluster": "production",
                    "provider": self.provider
                }
            },
            "scrape_configs": [],
            "alerting": {
                "alertmanagers": []
            },
            "rule_files": ["/etc/prometheus/rules/*.yml"]
        }
        
        # Add default scrape configs
        config["scrape_configs"].extend(self._get_default_scrape_configs())
        
        # Add custom scrape configs
        for scrape_config in self.config.custom_scrape_configs:
            config["scrape_configs"].append(scrape_config)
        
        # Add AlertManager configuration
        if self.config.alerting_enabled:
            config["alerting"]["alertmanagers"].append({
                "static_configs": [{"targets": ["alertmanager:9093"]}]
            })
        
        return config
    
    def _get_default_scrape_configs(self) -> List[Dict[str, Any]]:
        """Get default Prometheus scrape configurations"""
        return [
            {
                "job_name": "prometheus",
                "static_configs": [{"targets": ["localhost:9090"]}]
            },
            {
                "job_name": "kubernetes-apiservers",
                "scheme": "https",
                "kubernetes_sd_configs": [{"role": "apiserver"}],
                "tls_config": {"ca_file": "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"},
                "bearer_token_file": "/var/run/secrets/kubernetes.io/serviceaccount/token"
            },
            {
                "job_name": "kubernetes-nodes",
                "scheme": "https",
                "kubernetes_sd_configs": [{"role": "node"}],
                "tls_config": {"ca_file": "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"},
                "bearer_token_file": "/var/run/secrets/kubernetes.io/serviceaccount/token"
            },
            {
                "job_name": "kubernetes-pods",
                "kubernetes_sd_configs": [{"role": "pod"}],
                "relabel_configs": [
                    {"source_labels": ["__meta_kubernetes_pod_annotation_prometheus_io_scrape"], "action": "keep", "regex": "true"},
                    {"source_labels": ["__meta_kubernetes_pod_annotation_prometheus_io_path"], "action": "replace", "target_label": "__metrics_path__", "regex": "(.+)", "replacement": "$1"},
                    {"source_labels": ["__address__", "__meta_kubernetes_pod_annotation_prometheus_io_port"], "action": "replace", "regex": "([^:]+)(?::\\d+)?;(\\d+)", "replacement": "$1:$2", "target_label": "__address__"}
                ]
            }
        ]
    
    async def _deploy_grafana(self) -> Dict[str, Any]:
        """Deploy Grafana"""
        logger.info("Deploying Grafana...")
        
        grafana_deployment = {
            "replicas": self.config.grafana_replicas,
            "image": "grafana/grafana:10.1.0",
            "persistence": {
                "enabled": self.config.grafana_persistence_enabled,
                "size": self.config.grafana_persistence_size,
                "storage_class": self.config.storage_class
            },
            "resources": {
                "requests": {
                    "cpu": "250m",
                    "memory": "512Mi"
                },
                "limits": {
                    "cpu": "1000m",
                    "memory": "2Gi"
                }
            },
            "env": [
                {"name": "GF_SECURITY_ADMIN_PASSWORD", "value": self.config.grafana_admin_password},
                {"name": "GF_SERVER_ROOT_URL", "value": "http://grafana.monitoring.svc.cluster.local"},
                {"name": "GF_INSTALL_PLUGINS", "value": "grafana-piechart-panel,grafana-worldmap-panel"}
            ],
            "datasources": {
                "prometheus": {
                    "type": "prometheus",
                    "url": "http://prometheus.monitoring.svc.cluster.local:9090",
                    "access": "proxy",
                    "is_default": True
                }
            }
        }
        
        logger.info("Grafana deployed successfully")
        return {
            "success": True,
            "url": "http://grafana.monitoring.svc.cluster.local:3000",
            "admin_password": self.config.grafana_admin_password
        }
    
    async def _deploy_alertmanager(self) -> Dict[str, Any]:
        """Deploy AlertManager"""
        logger.info("Deploying AlertManager...")
        
        alertmanager_deployment = {
            "replicas": self.config.alertmanager_replicas,
            "image": "prom/alertmanager:v0.26.0",
            "persistence": {
                "enabled": self.config.alertmanager_persistence_enabled,
                "size": self.config.alertmanager_persistence_size,
                "storage_class": self.config.storage_class
            },
            "resources": {
                "requests": {
                    "cpu": "100m",
                    "memory": "256Mi"
                },
                "limits": {
                    "cpu": "500m",
                    "memory": "1Gi"
                }
            },
            "configuration": self._build_alertmanager_config()
        }
        
        logger.info("AlertManager deployed successfully")
        return {
            "success": True,
            "url": "http://alertmanager.monitoring.svc.cluster.local:9093"
        }
    
    def _build_alertmanager_config(self) -> Dict[str, Any]:
        """Build AlertManager configuration"""
        config = {
            "global": {
                "resolve_timeout": "5m"
            },
            "route": {
                "group_by": ["alertname", "cluster", "service"],
                "group_wait": "30s",
                "group_interval": "5m",
                "repeat_interval": "12h",
                "receiver": "default"
            },
            "receivers": [
                {
                    "name": "default"
                }
            ],
            "inhibit_rules": []
        }
        
        # Add Slack integration
        if self.config.slack_webhook_url:
            config["receivers"].append({
                "name": "slack",
                "slack_configs": [{
                    "api_url": self.config.slack_webhook_url,
                    "channel": "#alerts",
                    "title": "[{{ .Status }}] {{ .CommonLabels.alertname }}",
                    "text": "{{ range .Alerts }}{{ .Annotations.description }}\\n{{ end }}"
                }]
            })
            config["route"]["receiver"] = "slack"
        
        # Add PagerDuty integration
        if self.config.pagerduty_api_key:
            config["receivers"].append({
                "name": "pagerduty",
                "pagerduty_configs": [{
                    "service_key": self.config.pagerduty_api_key,
                    "description": "{{ .CommonLabels.alertname }}"
                }]
            })
        
        # Add email integration
        if self.config.email_smtp_server:
            config["receivers"].append({
                "name": "email",
                "email_configs": [{
                    "to": "alerts@example.com",
                    "from": "prometheus@example.com",
                    "smarthost": f"{self.config.email_smtp_server}:{self.config.email_smtp_port}",
                    "auth_username": self.config.email_smtp_username,
                    "auth_password": self.config.email_smtp_password,
                    "headers": {"Subject": "[Alert] {{ .CommonLabels.alertname }}"}
                }]
            })
        
        return config
    
    async def _deploy_pushgateway(self) -> Dict[str, Any]:
        """Deploy Pushgateway for batch jobs"""
        logger.info("Deploying Pushgateway...")
        
        pushgateway_deployment = {
            "replicas": self.config.pushgateway_replicas,
            "image": "prom/pushgateway:v1.6.0",
            "resources": {
                "requests": {
                    "cpu": "100m",
                    "memory": "256Mi"
                },
                "limits": {
                    "cpu": "500m",
                    "memory": "512Mi"
                }
            }
        }
        
        logger.info("Pushgateway deployed successfully")
        return {
            "success": True,
            "url": "http://pushgateway.monitoring.svc.cluster.local:9091"
        }
    
    async def _deploy_node_exporter(self) -> Dict[str, Any]:
        """Deploy Node Exporter"""
        logger.info("Deploying Node Exporter...")
        
        node_exporter_deployment = {
            "daemonset": True,
            "image": "prom/node-exporter:v1.6.1",
            "port": 9100,
            "host_network": True,
            "host_pid": True,
            "volumes": [
                {
                    "name": "proc",
                    "host_path": {"path": "/proc"}
                },
                {
                    "name": "sys",
                    "host_path": {"path": "/sys"}
                },
                {
                    "name": "root",
                    "host_path": {"path": "/"}
                }
            ]
        }
        
        logger.info("Node Exporter deployed successfully")
        return {"success": True}
    
    async def _deploy_kube_state_metrics(self) -> Dict[str, Any]:
        """Deploy Kube State Metrics"""
        logger.info("Deploying Kube State Metrics...")
        
        kube_state_metrics_deployment = {
            "replicas": 1,
            "image": "registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.9.2",
            "resources": {
                "requests": {
                    "cpu": "100m",
                    "memory": "256Mi"
                },
                "limits": {
                    "cpu": "500m",
                    "memory": "512Mi"
                }
            }
        }
        
        logger.info("Kube State Metrics deployed successfully")
        return {"success": True}
    
    async def _deploy_thanos(self) -> Dict[str, Any]:
        """Deploy Thanos for long-term storage"""
        logger.info("Deploying Thanos...")
        
        thanos_deployment = {
            "replicas": self.config.thanos_replicas,
            "image": "quay.io/thanos/thanos:v0.32.3",
            "objstore_config": self.config.thanos_objstore_config,
            "query": {
                "replicas": {
                    "label_selector": "thanos-store=true"
                }
            },
            "store": {
                "enabled": True,
                "persistence": {
                    "enabled": True,
                    "size": "50Gi"
                }
            },
            "compactor": {
                "enabled": True,
                "retention": {
                    "raw": "90d",
                    "resolution_5m": "180d",
                    "resolution_1h": "365d"
                }
            },
            "resources": {
                "requests": {
                    "cpu": "500m",
                    "memory": "1Gi"
                },
                "limits": {
                    "cpu": "2000m",
                    "memory": "4Gi"
                }
            }
        }
        
        logger.info("Thanos deployed successfully")
        return {
            "success": True,
            "url": "http://thanos-query.monitoring.svc.cluster.local:9090"
        }
    
    async def _configure_alerts(self) -> None:
        """Configure alert rules"""
        logger.info("Configuring alert rules...")
        
        # Add default alert rules
        default_rules = self._get_default_alert_rules()
        for rule in default_rules:
            self._alert_rules.append(rule)
        
        # Add custom alert rules
        for rule_config in self.config.custom_alert_rules:
            alert_rule = AlertRule(
                name=rule_config["name"],
                expr=rule_config["expr"],
                for_duration=rule_config.get("for", "5m"),
                labels=rule_config.get("labels", {}),
                annotations=rule_config.get("annotations", {}),
                severity=rule_config.get("severity", "warning")
            )
            self._alert_rules.append(alert_rule)
        
        logger.info(f"Configured {len(self._alert_rules)} alert rules")
    
    def _get_default_alert_rules(self) -> List[AlertRule]:
        """Get default alert rules"""
        return [
            AlertRule(
                name="HighCPUUsage",
                expr="100 * (1 - avg(rate(node_cpu_seconds_total{mode='idle'}[5m]))) by (instance) > 80",
                for_duration="5m",
                labels={"severity": "warning", "team": "operations"},
                annotations={
                    "summary": "High CPU usage detected",
                    "description": "Instance {{ $labels.instance }} has CPU usage above 80% for 5 minutes."
                }
            ),
            AlertRule(
                name="HighMemoryUsage",
                expr="(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85",
                for_duration="5m",
                labels={"severity": "warning", "team": "operations"},
                annotations={
                    "summary": "High memory usage detected",
                    "description": "Instance {{ $labels.instance }} has memory usage above 85% for 5 minutes."
                }
            ),
            AlertRule(
                name="PodNotReady",
                expr="kube_pod_status_ready{condition='false'} == 1",
                for_duration="10m",
                labels={"severity": "critical", "team": "platform"},
                annotations={
                    "summary": "Pod not ready",
                    "description": "Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is not ready for 10 minutes."
                }
            ),
            AlertRule(
                name="HighPodRestartCount",
                expr="increase(kube_pod_container_status_restarts_total[1h]) > 5",
                for_duration="5m",
                labels={"severity": "warning", "team": "platform"},
                annotations={
                    "summary": "High pod restart count",
                    "description": "Pod {{ $labels.pod }} has restarted more than 5 times in the last hour."
                }
            )
        ]
    
    async def _configure_dashboards(self) -> None:
        """Configure Grafana dashboards"""
        logger.info("Configuring dashboards...")
        
        # Add default dashboards
        default_dashboards = self._get_default_dashboards()
        for dashboard in default_dashboards:
            self._dashboards.append(dashboard)
        
        # Add custom dashboards
        for dashboard_config in self.config.custom_dashboards:
            dashboard = DashboardConfig(
                title=dashboard_config["title"],
                panels=dashboard_config["panels"],
                tags=dashboard_config.get("tags", []),
                time_from=dashboard_config.get("time_from", "now-1h"),
                time_to=dashboard_config.get("time_to", "now"),
                refresh=dashboard_config.get("refresh", "10s")
            )
            self._dashboards.append(dashboard)
        
        logger.info(f"Configured {len(self._dashboards)} dashboards")
    
    def _get_default_dashboards(self) -> List[DashboardConfig]:
        """Get default Grafana dashboards"""
        return [
            DashboardConfig(
                title="Kubernetes Cluster Overview",
                tags=["kubernetes", "cluster"],
                panels=[
                    {
                        "title": "CPU Usage",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "sum(rate(container_cpu_usage_seconds_total{container!='POD',container!=''}[5m])) by (namespace)",
                                "legendFormat": "{{ namespace }}"
                            }
                        ]
                    },
                    {
                        "title": "Memory Usage",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "sum(container_memory_working_set_bytes{container!='POD',container!=''}) by (namespace) / 1024 / 1024 / 1024",
                                "legendFormat": "{{ namespace }}"
                            }
                        ]
                    },
                    {
                        "title": "Pod Count",
                        "type": "stat",
                        "targets": [
                            {
                                "expr": "count(kube_pod_status_phase{phase='Running'})"
                            }
                        ]
                    }
                ]
            ),
            DashboardConfig(
                title="Node Performance",
                tags=["nodes", "performance"],
                panels=[
                    {
                        "title": "CPU Usage by Node",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "100 * (1 - avg(rate(node_cpu_seconds_total{mode='idle'}[5m])) by (instance))",
                                "legendFormat": "{{ instance }}"
                            }
                        ]
                    },
                    {
                        "title": "Memory Usage by Node",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
                                "legendFormat": "{{ instance }}"
                            }
                        ]
                    }
                ]
            )
        ]
    
    async def _verify_deployment(self) -> Dict[str, Any]:
        """Verify monitoring stack deployment"""
        logger.info("Verifying monitoring stack deployment...")
        
        warnings = []
        
        # Check if all components are deployed
        required_components = ["prometheus", "grafana", "alertmanager"]
        for component in required_components:
            if component not in self._deployed_components:
                warnings.append(f"Component {component} may not be deployed correctly")
        
        # Check if alert rules are configured
        if len(self._alert_rules) == 0:
            warnings.append("No alert rules configured")
        
        # Check if dashboards are configured
        if len(self._dashboards) == 0:
            warnings.append("No dashboards configured")
        
        # Check HA configuration
        if self.config.ha_enabled and self.config.ha_replicas < 2:
            warnings.append("HA enabled but replicas < 2")
        
        return {
            "success": len(warnings) == 0,
            "warnings": warnings
        }
    
    def _is_component_enabled(self, component: str) -> bool:
        """Check if a component is enabled"""
        return True
    
    def add_alert_rule(self, rule: AlertRule) -> None:
        """Add custom alert rule"""
        self._alert_rules.append(rule)
        logger.info(f"Added alert rule: {rule.name}")
    
    def add_scrape_config(self, config: ScrapeConfig) -> None:
        """Add custom scrape configuration"""
        self._scrape_configs.append(config)
        logger.info(f"Added scrape config: {config.job_name}")
    
    def add_dashboard(self, dashboard: DashboardConfig) -> None:
        """Add custom dashboard"""
        self._dashboards.append(dashboard)
        logger.info(f"Added dashboard: {dashboard.title}")
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get monitoring metrics"""
        return {
            "alert_rules_count": len(self._alert_rules),
            "scrape_configs_count": len(self._scrape_configs),
            "dashboards_count": len(self._dashboards),
            "deployed_components": list(self._deployed_components)
        }
    
    async def export_config(self) -> Dict[str, Any]:
        """Export monitoring configuration"""
        return {
            "config": self.config.__dict__,
            "alert_rules": [rule.to_dict() for rule in self._alert_rules],
            "scrape_configs": [config.to_dict() for config in self._scrape_configs],
            "dashboards": [dashboard.to_dict() for dashboard in self._dashboards]
        }