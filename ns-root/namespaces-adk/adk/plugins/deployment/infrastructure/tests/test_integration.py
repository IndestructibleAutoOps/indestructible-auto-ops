"""
Integration tests for all infrastructure components
"""

import pytest
import asyncio
from datetime import datetime, timedelta

import sys
sys.path.insert(0, '/workspace/machine-native-ops')

from adk.plugins.deployment.infrastructure.monitoring_manager import (
    MonitoringStackManager, MonitoringConfig
)
from adk.plugins.deployment.infrastructure.secrets_manager import (
    SecretsManager, SecretConfig, SecretType
)
from adk.plugins.deployment.infrastructure.container_orchestration import (
    ContainerOrchestrationManager, ContainerConfig, DeploymentConfig
)
from adk.plugins.deployment.infrastructure.disaster_recovery import (
    DisasterRecoveryManager, DisasterRecoveryConfig
)
from adk.plugins.deployment.infrastructure.log_aggregation import (
    LogAggregationManager, LogConfig, LogEntry, LogLevel, LogSource
)
from adk.plugins.deployment.infrastructure.performance_monitoring import (
    PerformanceMonitoringManager, APMConfig, SpanKind
)


class TestInfrastructureIntegration:
    """Integration tests for all infrastructure components"""
    
    @pytest.mark.asyncio
    async def test_full_stack_deployment(self):
        """Test deploying full infrastructure stack"""
        
        # 1. Deploy Monitoring Stack
        monitoring_config = MonitoringConfig()
        monitoring_manager = MonitoringStackManager("kubernetes", monitoring_config)
        monitoring_result = await monitoring_manager.deploy()
        
        assert monitoring_result.success is True
        assert "prometheus" in monitoring_result.components_deployed
        assert "grafana" in monitoring_result.components_deployed
        
        # 2. Deploy Log Aggregation
        log_config = LogConfig()
        log_manager = LogAggregationManager(log_config)
        log_result = await log_manager.deploy()
        
        assert log_result.success is True
        assert "elasticsearch" in log_result.data
        
        # 3. Deploy Container Orchestration
        container_manager = ContainerOrchestrationManager("kubernetes")
        container_config = ContainerConfig(name="app", image="nginx", replicas=2)
        deployment_config = DeploymentConfig(
            name="app-deployment",
            containers=[container_config]
        )
        container_result = await container_manager.deploy(deployment_config)
        
        assert container_result.success is True
        
        # 4. Initialize Secrets Manager
        secrets_config = SecretConfig()
        secrets_manager = SecretsManager("kubernetes", secrets_config)
        
        # Create secrets for the application
        db_secret = await secrets_manager.create_secret(
            name="database-url",
            value="postgresql://user:pass@localhost:5432/db",
            secret_type=SecretType.DATABASE_URL
        )
        
        assert db_secret.success is True
        
        # 5. Initialize Disaster Recovery
        dr_config = DisasterRecoveryConfig()
        dr_manager = DisasterRecoveryManager(dr_config)
        
        # Create backup
        backup_result = await dr_manager.create_backup()
        
        assert backup_result.success is True
        
        # 6. Initialize Performance Monitoring
        apm_config = APMConfig()
        apm_manager = PerformanceMonitoringManager(apm_config)
        
        # Start a trace
        span = await apm_manager.start_trace(
            trace_id="test-trace",
            operation_name="GET /api/health",
            service_name="health-check",
            kind=SpanKind.SERVER
        )
        
        await apm_manager.end_trace(span, status_code=200)
        
        assert span.duration_ms > 0
        
        print("✅ Full stack deployment successful!")
        print(f"   Monitoring: {len(monitoring_result.components_deployed)} components")
        print(f"   Logs: {log_result.message}")
        print(f"   Containers: {container_result.message}")
        print(f"   Secrets: {db_secret.message}")
        print(f"   Backup: {backup_result.backup_id}")
        print(f"   APM: {span.duration_ms:.2f}ms")
    
    @pytest.mark.asyncio
    async def test_monitoring_and_logging_integration(self):
        """Test integration between monitoring and logging"""
        
        # Deploy both systems
        monitoring_config = MonitoringConfig(alerting_enabled=True)
        monitoring_manager = MonitoringStackManager("kubernetes", monitoring_config)
        await monitoring_manager.deploy()
        
        log_config = LogConfig(alerting_enabled=True)
        log_manager = LogAggregationManager(log_config)
        await log_manager.deploy()
        
        # Ingest logs
        await log_manager.ingest_log(LogEntry(
            timestamp=datetime.now(),
            level=LogLevel.INFO,
            message="Application started",
            source="app",
            source_type=LogSource.APPLICATION
        ))
        
        # Get statistics from both systems
        monitoring_stats = await monitoring_manager.get_metrics()
        log_stats = await log_manager.get_log_statistics()
        
        assert monitoring_stats["alert_rules_count"] > 0
        assert log_stats["total_logs"] == 1
        
        print("✅ Monitoring and logging integration successful!")
    
    @pytest.mark.asyncio
    async def test_secrets_and_container_integration(self):
        """Test integration between secrets management and container orchestration"""
        
        # Initialize Secrets Manager
        secrets_config = SecretConfig()
        secrets_manager = SecretsManager("kubernetes", secrets_config)
        
        # Create secrets
        api_key = await secrets_manager.create_secret(
            name="api-key",
            value="sk-test-123456",
            secret_type=SecretType.API_KEY
        )
        
        db_password = await secrets_manager.create_secret(
            name="db-password",
            value="secure-password-123",
            secret_type=SecretType.STRING
        )
        
        # Retrieve secrets
        retrieved_key = await secrets_manager.get_secret("api-key")
        retrieved_password = await secrets_manager.get_secret("db-password")
        
        # Deploy container with secrets
        container_manager = ContainerOrchestrationManager("kubernetes")
        container_config = ContainerConfig(
            name="app",
            image="app:latest",
            env_vars={
                "API_KEY": retrieved_key.data["value"],
                "DB_PASSWORD": retrieved_password.data["value"]
            }
        )
        
        deployment_config = DeploymentConfig(
            name="app-deployment",
            containers=[container_config]
        )
        
        container_result = await container_manager.deploy(deployment_config)
        
        assert container_result.success is True
        
        print("✅ Secrets and container integration successful!")
    
    @pytest.mark.asyncio
    async def test_disaster_recovery_with_all_components(self):
        """Test disaster recovery affecting all components"""
        
        # Initialize all components
        monitoring_manager = MonitoringStackManager("kubernetes", MonitoringConfig())
        secrets_manager = SecretsManager("kubernetes", SecretConfig())
        dr_manager = DisasterRecoveryManager(DisasterRecoveryConfig())
        
        # Deploy monitoring
        await monitoring_manager.deploy()
        
        # Create secrets
        await secrets_manager.create_secret(
            name="important-secret",
            value="secret-value",
            secret_type=SecretType.STRING
        )
        
        # Create backup
        backup_result = await dr_manager.create_backup()
        
        # Simulate failover
        failover_result = await dr_manager.initiate_failover(trigger_type="manual")
        
        # Restore from backup
        restore_result = await dr_manager.restore_backup(backup_result.backup_id)
        
        # Failback
        failback_result = await dr_manager.initiate_failback(trigger_type="manual")
        
        assert backup_result.success is True
        assert failover_result.success is True
        assert restore_result.success is True
        assert failback_result.success is True
        
        print("✅ Disaster recovery cycle successful!")
    
    @pytest.mark.asyncio
    async def test_performance_monitoring_across_services(self):
        """Test performance monitoring across multiple services"""
        
        apm_manager = PerformanceMonitoringManager(APMConfig())
        
        # Simulate requests across multiple services
        services = ["api-gateway", "user-service", "product-service", "order-service"]
        
        for service in services:
            # Simulate a request trace
            trace_id = f"trace-{service}"
            span = await apm_manager.start_trace(
                trace_id=trace_id,
                operation_name=f"GET /api/{service}",
                service_name=service,
                kind=SpanKind.SERVER
            )
            
            # Simulate some processing time
            await asyncio.sleep(0.01)
            
            await apm_manager.end_trace(span, status_code=200)
        
        # Record metrics
        for service in services:
            await apm_manager.record_metric(
                name="request_duration",
                value=50 + len(service) * 10,  # Variable duration
                metric_type="histogram",
                labels={"service": service}
            )
        
        # Get statistics
        stats = await apm_manager.get_statistics()
        
        # Each service creates 1 span, and end_trace creates 2-3 metrics per span
        # Plus we explicitly recorded 1 metric per service
        assert stats["total_spans"] == len(services)
        assert stats["total_metrics"] >= len(services)  # At minimum, one per service
        
        print("✅ Performance monitoring across services successful!")
        print(f"   Total spans: {stats['total_spans']}")
        print(f"   Avg duration: {stats['avg_span_duration_ms']:.2f}ms")
    
    @pytest.mark.asyncio
    async def test_complete_lifecycle(self):
        """Test complete lifecycle: deploy → monitor → backup → scale → backup → restore"""
        
        print("\n🚀 Starting complete lifecycle test...")
        
        # 1. Deploy application
        container_manager = ContainerOrchestrationManager("kubernetes")
        container_config = ContainerConfig(name="app", image="app:latest", replicas=2)
        deployment_config = DeploymentConfig(
            name="app-deployment",
            containers=[container_config]
        )
        
        deploy_result = await container_manager.deploy(deployment_config)
        print(f"   1. Deployed: {deploy_result.message}")
        assert deploy_result.success is True
        
        # 2. Deploy monitoring
        monitoring_manager = MonitoringStackManager("kubernetes", MonitoringConfig())
        monitoring_result = await monitoring_manager.deploy()
        print(f"   2. Monitoring: {len(monitoring_result.components_deployed)} components")
        assert monitoring_result.success is True
        
        # 3. Deploy logging
        log_manager = LogAggregationManager(LogConfig())
        await log_manager.deploy()
        print(f"   3. Logging: ELK stack deployed")
        
        # 4. Start APM
        apm_manager = PerformanceMonitoringManager(APMConfig())
        span = await apm_manager.start_trace(
            trace_id="lifecycle-trace",
            operation_name="startup",
            service_name="app",
            kind=SpanKind.SERVER
        )
        await apm_manager.end_trace(span)
        print(f"   4. APM: Tracing started")
        
        # 5. Create initial backup
        dr_manager = DisasterRecoveryManager(DisasterRecoveryConfig())
        backup1 = await dr_manager.create_backup()
        print(f"   5. Backup: {backup1.backup_id}")
        assert backup1.success is True
        
        # 6. Scale application
        scale_result = await container_manager.scale("app-deployment", replicas=5)
        print(f"   6. Scaled: {scale_result.message}")
        assert scale_result.success is True
        
        # 7. Create second backup after scaling
        backup2 = await dr_manager.create_backup()
        print(f"   7. Backup: {backup2.backup_id}")
        assert backup2.success is True
        
        # 8. Simulate failover
        failover_result = await dr_manager.initiate_failover()
        print(f"   8. Failover: {failover_result.failover_id}")
        assert failover_result.success is True
        
        # 9. Restore from first backup
        restore_result = await dr_manager.restore_backup(backup1.backup_id)
        print(f"   9. Restore: {restore_result.restore_id}")
        assert restore_result.success is True
        
        # 10. Failback
        failback_result = await dr_manager.initiate_failback()
        print(f"   10. Failback: {failback_result.failover_id}")
        assert failback_result.success is True
        
        print("\n✅ Complete lifecycle test passed!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])