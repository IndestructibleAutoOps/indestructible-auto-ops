"""
Unit tests for Log Aggregation Manager (ELK Stack)
"""

import pytest
import asyncio
from datetime import datetime, timedelta

import sys
sys.path.insert(0, '/workspace/machine-native-ops')

from adk.plugins.deployment.infrastructure.log_aggregation import (
    LogAggregationManager,
    LogConfig,
    ElasticsearchConfig,
    LogstashConfig,
    KibanaConfig,
    LogEntry,
    LogQuery,
    LogAggregationResult,
    LogSource,
    LogLevel,
    LogFormat
)


class TestLogConfig:
    """Test LogConfig dataclass"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = LogConfig()
        
        assert config.elasticsearch.enabled is True
        assert config.logstash.enabled is True
        assert config.kibana.enabled is True
        assert config.index_retention_days == 30
        assert config.alerting_enabled is True
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = LogConfig(
            elasticsearch=ElasticsearchConfig(replicas=5),
            logstash=LogstashConfig(enabled=False),
            index_retention_days=90
        )
        
        assert config.elasticsearch.replicas == 5
        assert config.logstash.enabled is False
        assert config.index_retention_days == 90


class TestLogEntry:
    """Test LogEntry class"""
    
    def test_log_entry_creation(self):
        """Test creating log entry"""
        entry = LogEntry(
            timestamp=datetime.now(),
            level=LogLevel.INFO,
            message="Test log message",
            source="app-1",
            source_type=LogSource.APPLICATION,
            namespace="default",
            pod_name="pod-1"
        )
        
        assert entry.level == LogLevel.INFO
        assert entry.message == "Test log message"
        assert entry.source == "app-1"
        assert entry.source_type == LogSource.APPLICATION
    
    def test_log_entry_to_dict(self):
        """Test converting log entry to dictionary"""
        now = datetime.now()
        entry = LogEntry(
            timestamp=now,
            level=LogLevel.ERROR,
            message="Error occurred",
            source="web",
            source_type=LogSource.SERVICE
        )
        
        entry_dict = entry.to_dict()
        
        assert entry_dict["@timestamp"] == now.isoformat()
        assert entry_dict["level"] == "error"
        assert entry_dict["message"] == "Error occurred"


class TestLogQuery:
    """Test LogQuery class"""
    
    def test_log_query_creation(self):
        """Test creating log query"""
        query = LogQuery(
            query="error",
            start_time=datetime.now() - timedelta(hours=1),
            end_time=datetime.now(),
            level_filter=LogLevel.ERROR,
            size=50
        )
        
        assert query.query == "error"
        assert query.level_filter == LogLevel.ERROR
        assert query.size == 50
    
    def test_log_query_to_elasticsearch_query(self):
        """Test converting to Elasticsearch query"""
        now = datetime.now()
        query = LogQuery(
            query="error",
            start_time=now - timedelta(hours=1),
            end_time=now,
            level_filter=LogLevel.ERROR
        )
        
        es_query = query.to_elasticsearch_query()
        
        assert "query" in es_query
        assert "bool" in es_query["query"]
        assert "range" in es_query["query"]["bool"]["must"][0]
        assert es_query["size"] == 100


class TestLogAggregationManager:
    """Test LogAggregationManager class"""
    
    @pytest.fixture
    def config(self):
        """Create test configuration"""
        return LogConfig()
    
    @pytest.fixture
    def manager(self, config):
        """Create log aggregation manager instance"""
        return LogAggregationManager(config)
    
    def test_manager_initialization(self, manager):
        """Test manager initialization"""
        assert manager.config is not None
        assert manager._logs == []
        assert manager._indices == {}
        assert manager._alert_rules == {}
    
    @pytest.mark.asyncio
    async def test_deploy_elk_stack(self, manager):
        """Test deploying ELK stack"""
        result = await manager.deploy()
        
        assert isinstance(result, LogAggregationResult)
        assert result.success is True
        assert result.execution_time > 0
        assert result.data is not None
        assert "elasticsearch" in result.data
        assert "logstash" in result.data
        assert "kibana" in result.data
    
    @pytest.mark.asyncio
    async def test_deploy_without_logstash(self):
        """Test deploying without Logstash"""
        config = LogConfig(logstash=LogstashConfig(enabled=False))
        manager = LogAggregationManager(config)
        
        result = await manager.deploy()
        
        assert result.success is True
        assert result.data is not None
    
    @pytest.mark.asyncio
    async def test_ingest_log(self, manager):
        """Test ingesting log entry"""
        entry = LogEntry(
            timestamp=datetime.now(),
            level=LogLevel.INFO,
            message="Test log",
            source="test-app",
            source_type=LogSource.APPLICATION
        )
        
        result = await manager.ingest_log(entry)
        
        assert result.success is True
        assert len(manager._logs) == 1
    
    @pytest.mark.asyncio
    async def test_ingest_multiple_logs(self, manager):
        """Test ingesting multiple logs"""
        for i in range(10):
            entry = LogEntry(
                timestamp=datetime.now(),
                level=LogLevel.INFO,
                message=f"Log message {i}",
                source="app",
                source_type=LogSource.APPLICATION
            )
            await manager.ingest_log(entry)
        
        assert len(manager._logs) == 10
    
    @pytest.mark.asyncio
    async def test_search_logs(self, manager):
        """Test searching logs"""
        # Ingest some logs
        await manager.ingest_log(LogEntry(
            timestamp=datetime.now(),
            level=LogLevel.INFO,
            message="This is an info message",
            source="app",
            source_type=LogSource.APPLICATION
        ))
        
        await manager.ingest_log(LogEntry(
            timestamp=datetime.now(),
            level=LogLevel.ERROR,
            message="This is an error message",
            source="app",
            source_type=LogSource.APPLICATION
        ))
        
        # Search for "error"
        query = LogQuery(
            query="error",
            start_time=datetime.now() - timedelta(minutes=1),
            end_time=datetime.now()
        )
        
        result = await manager.search_logs(query)
        
        assert result.success is True
        assert result.total_count >= 1
    
    @pytest.mark.asyncio
    async def test_search_logs_with_level_filter(self, manager):
        """Test searching with level filter"""
        # Ingest logs with different levels
        for level in [LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR]:
            await manager.ingest_log(LogEntry(
                timestamp=datetime.now(),
                level=level,
                message=f"Log with level {level.value}",
                source="app",
                source_type=LogSource.APPLICATION
            ))
        
        # Search for ERROR level only
        query = LogQuery(
            query="log",
            start_time=datetime.now() - timedelta(minutes=1),
            end_time=datetime.now(),
            level_filter=LogLevel.ERROR
        )
        
        result = await manager.search_logs(query)
        
        assert result.success is True
        assert result.total_count == 1
    
    @pytest.mark.asyncio
    async def test_get_log_statistics(self, manager):
        """Test getting log statistics"""
        # Ingest some logs
        await manager.ingest_log(LogEntry(
            timestamp=datetime.now(),
            level=LogLevel.INFO,
            message="Info log",
            source="app1",
            source_type=LogSource.APPLICATION
        ))
        
        await manager.ingest_log(LogEntry(
            timestamp=datetime.now(),
            level=LogLevel.ERROR,
            message="Error log",
            source="app2",
            source_type=LogSource.APPLICATION
        ))
        
        # Get statistics
        stats = await manager.get_log_statistics()
        
        assert stats["total_logs"] == 2
        assert stats["level_distribution"]["info"] == 1
        assert stats["level_distribution"]["error"] == 1
        assert stats["source_distribution"]["app1"] == 1
        assert stats["source_distribution"]["app2"] == 1
    
    @pytest.mark.asyncio
    async def test_get_index_name(self, manager):
        """Test getting index name"""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        index_name = manager._get_index_name(timestamp)
        
        assert index_name == "logs-2024.01.15"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])