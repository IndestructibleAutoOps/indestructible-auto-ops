"""
Unit Tests for Configuration Hot Reloader
==========================================

Tests for the enterprise-grade configuration hot reload system.
"""

import asyncio
import json
import tempfile
import time
import yaml
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from config_hot_reloader import (
    ConfigHotReloader,
    ReloadEventType,
    ReloadEvent,
    ReloadStatistics,
    create_hot_reloader
)


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for config files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_yaml_config(temp_config_dir):
    """Create a sample YAML configuration file."""
    config_path = temp_config_dir / "config.yaml"
    config_data = {
        "version": "1.0",
        "settings": {
            "timeout": 30,
            "retries": 3
        }
    }
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)
    return config_path, config_data


@pytest.fixture
def sample_json_config(temp_config_dir):
    """Create a sample JSON configuration file."""
    config_path = temp_config_dir / "config.json"
    config_data = {
        "version": "1.0",
        "settings": {
            "timeout": 30,
            "retries": 3
        }
    }
    with open(config_path, 'w') as f:
        json.dump(config_data, f)
    return config_path, config_data


@pytest.fixture
async def hot_reloader(sample_yaml_config):
    """Create a hot reloader instance."""
    config_path, _ = sample_yaml_config
    reloader = create_hot_reloader([str(config_path)], debounce_interval=0.5)
    await reloader.start()
    yield reloader
    await reloader.stop()


class TestConfigHotReloader:
    """Test suite for ConfigHotReloader."""
    
    @pytest.mark.asyncio
    async def test_initialization(self, sample_yaml_config):
        """Test hot reloader initialization."""
        config_path, _ = sample_yaml_config
        reloader = ConfigHotReloader(
            config_paths=[config_path],
            debounce_interval=0.5
        )
        
        assert len(reloader.config_paths) == 1
        assert reloader.debounce_interval == 0.5
        assert reloader.max_reload_attempts == 3
        assert reloader.enable_rollback is True
        assert reloader._is_running is False
    
    @pytest.mark.asyncio
    async def test_start_and_stop(self, sample_yaml_config):
        """Test starting and stopping the reloader."""
        config_path, _ = sample_yaml_config
        reloader = ConfigHotReloader(
            config_paths=[config_path],
            debounce_interval=0.5
        )
        
        await reloader.start()
        assert reloader.is_running() is True
        
        await reloader.stop()
        assert reloader.is_running() is False
    
    @pytest.mark.asyncio
    async def test_load_initial_config(self, sample_yaml_config):
        """Test loading initial configuration."""
        config_path, expected_config = sample_yaml_config
        reloader = ConfigHotReloader(
            config_paths=[config_path],
            debounce_interval=0.5
        )
        
        await reloader.start()
        
        loaded_config = reloader.get_config(config_path)
        assert loaded_config == expected_config
        
        await reloader.stop()
    
    @pytest.mark.asyncio
    async def test_hot_reload_on_file_change(self, sample_yaml_config):
        """Test hot reload when file changes."""
        config_path, _ = sample_yaml_config
        reloader = ConfigHotReloader(
            config_paths=[config_path],
            debounce_interval=0.5
        )
        
        # Track reload events
        reload_events = []
        
        def event_handler(event):
            reload_events.append(event)
        
        reloader.add_event_handler(event_handler)
        
        await reloader.start()
        time.sleep(0.5)  # Wait for initial load
        
        # Modify config file
        new_config = {
            "version": "2.0",
            "settings": {
                "timeout": 60,
                "retries": 5
            }
        }
        with open(config_path, 'w') as f:
            yaml.dump(new_config, f)
        
        # Wait for debounce and reload
        time.sleep(1.5)
        
        # Verify reload occurred
        assert len(reload_events) > 0
        assert any(e.event_type == ReloadEventType.RELOAD_SUCCESS for e in reload_events)
        
        # Verify config updated
        current_config = reloader.get_config(config_path)
        assert current_config["version"] == "2.0"
        assert current_config["settings"]["timeout"] == 60
        
        await reloader.stop()
    
    @pytest.mark.asyncio
    async def test_validation_failure(self, temp_config_dir):
        """Test handling of validation failures."""
        config_path = temp_config_dir / "config.yaml"
        initial_config = {"version": "1.0", "settings": {}}
        with open(config_path, 'w') as f:
            yaml.dump(initial_config, f)
        
        # Create validator that fails for version 2.0
        def validator(config):
            return config.get("version") != "2.0"
        
        reloader = ConfigHotReloader(
            config_paths=[config_path],
            validator=validator,
            debounce_interval=0.5
        )
        
        validation_failures = []
        
        def event_handler(event):
            if event.event_type == ReloadEventType.VALIDATION_FAILED:
                validation_failures.append(event)
        
        reloader.add_event_handler(event_handler)
        
        await reloader.start()
        time.sleep(0.5)
        
        # Try to load invalid config
        invalid_config = {"version": "2.0", "settings": {}}
        with open(config_path, 'w') as f:
            yaml.dump(invalid_config, f)
        
        time.sleep(1.5)
        
        # Verify validation failed
        assert len(validation_failures) > 0
        
        # Verify config not updated
        current_config = reloader.get_config(config_path)
        assert current_config["version"] == "1.0"
        
        await reloader.stop()
    
    @pytest.mark.asyncio
    async def test_rollback_on_failure(self, sample_yaml_config):
        """Test automatic rollback on reload failure."""
        config_path, initial_config = sample_yaml_config
        
        # Create validator that fails
        def always_fail(config):
            return False
        
        reloader = ConfigHotReloader(
            config_paths=[config_path],
            validator=always_fail,
            debounce_interval=0.5,
            enable_rollback=True
        )
        
        rollback_events = []
        
        def event_handler(event):
            if event.event_type == ReloadEventType.ROLLBACK_SUCCESS:
                rollback_events.append(event)
        
        reloader.add_event_handler(event_handler)
        
        await reloader.start()
        time.sleep(0.5)
        
        # Try to reload with invalid config
        new_config = {"version": "2.0", "settings": {}}
        with open(config_path, 'w') as f:
            yaml.dump(new_config, f)
        
        time.sleep(1.5)
        
        # Verify rollback occurred
        assert len(rollback_events) > 0
        
        # Verify config rolled back
        current_config = reloader.get_config(config_path)
        assert current_config == initial_config
        
        await reloader.stop()
    
    @pytest.mark.asyncio
    async def test_manual_reload(self, sample_yaml_config):
        """Test manual configuration reload."""
        config_path, _ = sample_yaml_config
        reloader = ConfigHotReloader(
            config_paths=[config_path],
            debounce_interval=0.5
        )
        
        await reloader.start()
        time.sleep(0.5)
        
        # Modify config file
        new_config = {"version": "2.0", "settings": {}}
        with open(config_path, 'w') as f:
            yaml.dump(new_config, f)
        
        # Trigger manual reload
        success = await reloader.manual_reload()
        
        # Verify reload successful
        assert success is True
        current_config = reloader.get_config(config_path)
        assert current_config["version"] == "2.0"
        
        await reloader.stop()
    
    @pytest.mark.asyncio
    async def test_statistics_tracking(self, sample_yaml_config):
        """Test statistics tracking."""
        config_path, _ = sample_yaml_config
        reloader = ConfigHotReloader(
            config_paths=[config_path],
            debounce_interval=0.5,
            stats_enabled=True
        )
        
        await reloader.start()
        time.sleep(0.5)
        
        # Trigger multiple reloads
        for i in range(3):
            new_config = {"version": f"{i+2}.0", "settings": {}}
            with open(config_path, 'w') as f:
                yaml.dump(new_config, f)
            time.sleep(1.0)
        
        stats = reloader.get_statistics()
        assert stats.total_reloads >= 3
        assert stats.successful_reloads >= 3
        assert stats.failed_reloads == 0
        assert stats.last_reload_time is not None
        
        await reloader.stop()
    
    @pytest.mark.asyncio
    async def test_event_handlers(self, sample_yaml_config):
        """Test event handler notifications."""
        config_path, _ = sample_yaml_config
        reloader = ConfigHotReloader(
            config_paths=[config_path],
            debounce_interval=0.5
        )
        
        events_received = []
        
        def event_handler(event):
            events_received.append(event)
        
        reloader.add_event_handler(event_handler)
        
        await reloader.start()
        time.sleep(0.5)
        
        # Trigger reload
        new_config = {"version": "2.0", "settings": {}}
        with open(config_path, 'w') as f:
            yaml.dump(new_config, f)
        
        time.sleep(1.5)
        
        # Verify events received
        assert len(events_received) > 0
        assert any(e.event_type == ReloadEventType.FILE_CHANGED for e in events_received)
        assert any(e.event_type == ReloadEventType.RELOAD_SUCCESS for e in events_received)
        
        # Test handler removal
        reloader.remove_event_handler(event_handler)
        event_count_before = len(events_received)
        
        # Trigger another reload
        new_config = {"version": "3.0", "settings": {}}
        with open(config_path, 'w') as f:
            yaml.dump(new_config, f)
        
        time.sleep(1.5)
        
        # Verify no new events
        assert len(events_received) == event_count_before
        
        await reloader.stop()
    
    @pytest.mark.asyncio
    async def test_multiple_config_files(self, temp_config_dir):
        """Test monitoring multiple configuration files."""
        config1_path = temp_config_dir / "config1.yaml"
        config2_path = temp_config_dir / "config2.yaml"
        
        with open(config1_path, 'w') as f:
            yaml.dump({"version": "1.0"}, f)
        
        with open(config2_path, 'w') as f:
            yaml.dump({"version": "1.0"}, f)
        
        reloader = ConfigHotReloader(
            config_paths=[config1_path, config2_path],
            debounce_interval=0.5
        )
        
        await reloader.start()
        time.sleep(0.5)
        
        # Verify both configs loaded
        assert reloader.get_config(config1_path) is not None
        assert reloader.get_config(config2_path) is not None
        
        # Modify first config
        with open(config1_path, 'w') as f:
            yaml.dump({"version": "2.0"}, f)
        
        time.sleep(1.5)
        
        # Verify only first config updated
        assert reloader.get_config(config1_path)["version"] == "2.0"
        assert reloader.get_config(config2_path)["version"] == "1.0"
        
        await reloader.stop()
    
    @pytest.mark.asyncio
    async def test_rollback_to_initial(self, sample_yaml_config):
        """Test rollback to initial configuration."""
        config_path, initial_config = sample_yaml_config
        reloader = ConfigHotReloader(
            config_paths=[config_path],
            debounce_interval=0.5
        )
        
        await reloader.start()
        time.sleep(0.5)
        
        # Modify config
        new_config = {"version": "2.0", "settings": {}}
        with open(config_path, 'w') as f:
            yaml.dump(new_config, f)
        
        time.sleep(1.5)
        assert reloader.get_config(config_path)["version"] == "2.0"
        
        # Rollback to initial
        reloader.rollback_to_initial()
        
        # Verify rolled back
        current_config = reloader.get_config(config_path)
        assert current_config == initial_config
        
        await reloader.stop()
    
    @pytest.mark.asyncio
    async def test_thread_safety(self, sample_yaml_config):
        """Test thread-safe operations."""
        config_path, _ = sample_yaml_config
        reloader = ConfigHotReloader(
            config_paths=[config_path],
            debounce_interval=0.5
        )
        
        await reloader.start()
        time.sleep(0.5)
        
        # Concurrent operations
        async def concurrent_get():
            for _ in range(10):
                reloader.get_config(config_path)
                await asyncio.sleep(0.01)
        
        async def concurrent_modify():
            for i in range(10):
                new_config = {"version": f"{i}.0", "settings": {}}
                with open(config_path, 'w') as f:
                    yaml.dump(new_config, f)
                await asyncio.sleep(0.01)
        
        # Run concurrent operations
        await asyncio.gather(concurrent_get(), concurrent_modify())
        
        # Verify no errors
        stats = reloader.get_statistics()
        assert stats.total_reloads >= 0
        
        await reloader.stop()


class TestReloadEvent:
    """Test suite for ReloadEvent."""
    
    def test_event_creation(self):
        """Test creating a reload event."""
        event = ReloadEvent(
            event_type=ReloadEventType.FILE_CHANGED,
            file_path=Path("config.yaml")
        )
        
        assert event.event_type == ReloadEventType.FILE_CHANGED
        assert event.file_path == Path("config.yaml")
        assert event.timestamp is not None
        assert event.old_config is None
        assert event.new_config is None
        assert event.error is None
        assert event.metadata == {}
    
    def test_event_with_data(self):
        """Test creating an event with data."""
        old_config = {"version": "1.0"}
        new_config = {"version": "2.0"}
        
        event = ReloadEvent(
            event_type=ReloadEventType.RELOAD_SUCCESS,
            file_path=Path("config.yaml"),
            old_config=old_config,
            new_config=new_config,
            metadata={"reload_time_ms": 50.5}
        )
        
        assert event.old_config == old_config
        assert event.new_config == new_config
        assert event.metadata["reload_time_ms"] == 50.5


class TestReloadStatistics:
    """Test suite for ReloadStatistics."""
    
    def test_statistics_initialization(self):
        """Test statistics initialization."""
        stats = ReloadStatistics()
        
        assert stats.total_reloads == 0
        assert stats.successful_reloads == 0
        assert stats.failed_reloads == 0
        assert stats.validation_failures == 0
        assert stats.rollbacks == 0
        assert stats.avg_reload_time_ms == 0.0
        assert stats.last_reload_time is None


class TestFactoryFunction:
    """Test suite for factory functions."""
    
    @pytest.mark.asyncio
    async def test_create_hot_reloader(self, sample_yaml_config):
        """Test creating hot reloader via factory function."""
        config_path, _ = sample_yaml_config
        reloader = create_hot_reloader(
            [str(config_path)],
            debounce_interval=0.5
        )
        
        assert reloader.debounce_interval == 0.5
        assert reloader.max_reload_attempts == 3
        assert reloader.enable_rollback is True
        assert reloader.stats_enabled is True
        
        await reloader.start()
        await reloader.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])