"""
Unit Tests for Configuration File Watcher
==========================================

Tests for the enterprise-grade configuration file watcher.
"""

import asyncio
import tempfile
import time
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from config_file_watcher import (
    ConfigFileWatcher,
    WatchEventType,
    WatchEvent,
    DebounceStrategy,
    DebounceConfig,
    create_file_watcher
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
async def file_watcher(temp_dir):
    """Create a file watcher instance."""
    watcher = ConfigFileWatcher(
        watch_paths=[temp_dir],
        debounce_config=DebounceConfig(
            strategy=DebounceStrategy.FIXED_DELAY,
            base_delay=0.5
        )
    )
    await watcher.start()
    yield watcher
    await watcher.stop()


class TestConfigFileWatcher:
    """Test suite for ConfigFileWatcher."""
    
    @pytest.mark.asyncio
    async def test_initialization(self, temp_dir):
        """Test file watcher initialization."""
        watcher = ConfigFileWatcher(
            watch_paths=[temp_dir],
            debounce_config=DebounceConfig(
                strategy=DebounceStrategy.FIXED_DELAY,
                base_delay=1.0
            )
        )
        
        assert len(watcher.watch_paths) == 1
        assert watcher.debounce_config.strategy == DebounceStrategy.FIXED_DELAY
        assert watcher.debounce_config.base_delay == 1.0
        assert watcher.enable_recursive is True
        assert watcher.max_buffer_size == 1000
        assert watcher._is_running is False
    
    @pytest.mark.asyncio
    async def test_start_and_stop(self, temp_dir):
        """Test starting and stopping the watcher."""
        watcher = ConfigFileWatcher(
            watch_paths=[temp_dir],
            debounce_config=DebounceConfig(base_delay=1.0)
        )
        
        await watcher.start()
        assert watcher.is_running() is True
        
        await watcher.stop()
        assert watcher.is_running() is False
    
    @pytest.mark.asyncio
    async def test_file_creation_detection(self, temp_dir, file_watcher):
        """Test detection of file creation."""
        events_received = []
        
        def event_handler(event):
            events_received.append(event)
        
        file_watcher.add_event_handler(event_handler)
        time.sleep(0.5)
        
        # Create a new file
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        
        # Wait for debounce
        time.sleep(1.5)
        
        # Verify event received
        assert len(events_received) > 0
        assert any(e.event_type == WatchEventType.CREATED for e in events_received)
        assert any(e.path == test_file for e in events_received)
    
    @pytest.mark.asyncio
    async def test_file_modification_detection(self, temp_dir, file_watcher):
        """Test detection of file modification."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("initial content")
        time.sleep(0.5)
        
        events_received = []
        
        def event_handler(event):
            events_received.append(event)
        
        file_watcher.add_event_handler(event_handler)
        time.sleep(0.5)
        
        # Modify file
        test_file.write_text("modified content")
        
        # Wait for debounce
        time.sleep(1.5)
        
        # Verify event received
        assert len(events_received) > 0
        assert any(e.event_type == WatchEventType.MODIFIED for e in events_received)
        assert any(e.path == test_file for e in events_received)
    
    @pytest.mark.asyncio
    async def test_file_deletion_detection(self, temp_dir, file_watcher):
        """Test detection of file deletion."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")
        time.sleep(0.5)
        
        events_received = []
        
        def event_handler(event):
            events_received.append(event)
        
        file_watcher.add_event_handler(event_handler)
        time.sleep(0.5)
        
        # Delete file
        test_file.unlink()
        
        # Wait for debounce
        time.sleep(1.5)
        
        # Verify event received
        assert len(events_received) > 0
        assert any(e.event_type == WatchEventType.DELETED for e in events_received)
        assert any(e.path == test_file for e in events_received)
    
    @pytest.mark.asyncio
    async def test_debounce_strategy_fixed_delay(self, temp_dir):
        """Test fixed delay debounce strategy."""
        watcher = ConfigFileWatcher(
            watch_paths=[temp_dir],
            debounce_config=DebounceConfig(
                strategy=DebounceStrategy.FIXED_DELAY,
                base_delay=1.0
            )
        )
        
        await watcher.start()
        time.sleep(0.5)
        
        events_received = []
        
        def event_handler(event):
            events_received.append(event)
        
        watcher.add_event_handler(event_handler)
        
        test_file = temp_dir / "test.txt"
        
        # Rapid modifications
        for i in range(5):
            test_file.write_text(f"content {i}")
            time.sleep(0.1)
        
        # Wait for debounce
        time.sleep(2.0)
        
        # Should receive fewer events due to debouncing
        assert len(events_received) < 5
        
        await watcher.stop()
    
    @pytest.mark.asyncio
    async def test_debounce_strategy_adaptive(self, temp_dir):
        """Test adaptive debounce strategy."""
        watcher = ConfigFileWatcher(
            watch_paths=[temp_dir],
            debounce_config=DebounceConfig(
                strategy=DebounceStrategy.ADAPTIVE,
                base_delay=0.5,
                adaptive_multiplier=1.5
            )
        )
        
        await watcher.start()
        time.sleep(0.5)
        
        events_received = []
        
        def event_handler(event):
            events_received.append(event)
        
        watcher.add_event_handler(event_handler)
        
        test_file = temp_dir / "test.txt"
        
        # Many rapid modifications
        for i in range(15):
            test_file.write_text(f"content {i}")
            time.sleep(0.05)
        
        # Wait for debounce
        time.sleep(3.0)
        
        # Adaptive strategy should handle high frequency better
        stats = watcher.get_statistics()
        assert stats["total_events"] > 0
        assert stats["debounced_events"] > 0
        
        await watcher.stop()
    
    @pytest.mark.asyncio
    async def test_multiple_watch_paths(self, temp_dir):
        """Test watching multiple paths."""
        dir1 = temp_dir / "dir1"
        dir2 = temp_dir / "dir2"
        dir1.mkdir()
        dir2.mkdir()
        
        watcher = ConfigFileWatcher(
            watch_paths=[dir1, dir2],
            debounce_config=DebounceConfig(base_delay=0.5)
        )
        
        await watcher.start()
        time.sleep(0.5)
        
        events_received = []
        
        def event_handler(event):
            events_received.append(event)
        
        watcher.add_event_handler(event_handler)
        
        # Create file in dir1
        file1 = dir1 / "test1.txt"
        file1.write_text("content 1")
        
        # Create file in dir2
        file2 = dir2 / "test2.txt"
        file2.write_text("content 2")
        
        # Wait for debounce
        time.sleep(1.5)
        
        # Verify both files detected
        assert any(e.path == file1 for e in events_received)
        assert any(e.path == file2 for e in events_received)
        
        await watcher.stop()
    
    @pytest.mark.asyncio
    async def test_recursive_directory_watching(self, temp_dir, file_watcher):
        """Test recursive directory watching."""
        events_received = []
        
        def event_handler(event):
            events_received.append(event)
        
        file_watcher.add_event_handler(event_handler)
        time.sleep(0.5)
        
        # Create nested directory
        nested_dir = temp_dir / "subdir" / "nested"
        nested_dir.mkdir(parents=True)
        
        # Create file in nested directory
        nested_file = nested_dir / "test.txt"
        nested_file.write_text("nested content")
        
        # Wait for debounce
        time.sleep(1.5)
        
        # Verify nested file detected
        assert any(e.path == nested_file for e in events_received)
    
    @pytest.mark.asyncio
    async def test_event_handler_management(self, temp_dir, file_watcher):
        """Test adding and removing event handlers."""
        handler1_called = []
        handler2_called = []
        
        def handler1(event):
            handler1_called.append(event)
        
        def handler2(event):
            handler2_called.append(event)
        
        # Add handlers
        file_watcher.add_event_handler(handler1)
        file_watcher.add_event_handler(handler2)
        
        time.sleep(0.5)
        
        # Create file
        test_file = temp_dir / "test.txt"
        test_file.write_text("content")
        
        time.sleep(1.5)
        
        # Verify both handlers called
        assert len(handler1_called) > 0
        assert len(handler2_called) > 0
        
        # Remove handler2
        file_watcher.remove_event_handler(handler2)
        
        # Create another file
        test_file2 = temp_dir / "test2.txt"
        test_file2.write_text("content2")
        
        time.sleep(1.5)
        
        # Verify only handler1 called
        assert len(handler1_called) > len(handler2_called)
    
    @pytest.mark.asyncio
    async def test_statistics_tracking(self, temp_dir, file_watcher):
        """Test statistics tracking."""
        time.sleep(0.5)
        
        # Create multiple files
        for i in range(5):
            test_file = temp_dir / f"test{i}.txt"
            test_file.write_text(f"content {i}")
        
        time.sleep(1.5)
        
        stats = watcher.get_statistics()
        assert stats["total_events"] > 0
        assert stats["buffered_events"] > 0
        assert stats["debounced_events"] > 0
        assert stats["tracked_files"] >= 5
    
    @pytest.mark.asyncio
    async def test_max_buffer_size(self, temp_dir):
        """Test event buffer size limit."""
        watcher = ConfigFileWatcher(
            watch_paths=[temp_dir],
            debounce_config=DebounceConfig(base_delay=0.5),
            max_buffer_size=10
        )
        
        await watcher.start()
        time.sleep(0.5)
        
        # Create many files rapidly
        for i in range(20):
            test_file = temp_dir / f"test{i}.txt"
            test_file.write_text(f"content {i}")
        
        time.sleep(2.0)
        
        stats = watcher.get_statistics()
        # Buffer should not exceed max size
        assert stats["buffer_size"] <= 10
        
        await watcher.stop()
    
    @pytest.mark.asyncio
    async def test_thread_safety(self, temp_dir, file_watcher):
        """Test thread-safe operations."""
        time.sleep(0.5)
        
        async def concurrent_operations():
            for i in range(10):
                # Concurrent get statistics
                stats = file_watcher.get_statistics()
                assert stats is not None
                
                # Concurrent file operations
                test_file = temp_dir / f"concurrent_{i}.txt"
                test_file.write_text(f"content {i}")
                
                await asyncio.sleep(0.01)
        
        # Run concurrent operations
        await asyncio.gather(
            concurrent_operations(),
            concurrent_operations()
        )
        
        # Verify no errors
        stats = file_watcher.get_statistics()
        assert stats["total_events"] >= 0


class TestWatchEvent:
    """Test suite for WatchEvent."""
    
    def test_event_creation(self):
        """Test creating a watch event."""
        event = WatchEvent(
            event_type=WatchEventType.CREATED,
            path=Path("test.txt")
        )
        
        assert event.event_type == WatchEventType.CREATED
        assert event.path == Path("test.txt")
        assert event.timestamp is not None
        assert event.old_path is None
        assert event.metadata == {}
    
    def test_event_with_metadata(self):
        """Test creating an event with metadata."""
        event = WatchEvent(
            event_type=WatchEventType.MODIFIED,
            path=Path("test.txt"),
            metadata={"size": 100, "mtime": 123456.0}
        )
        
        assert event.metadata["size"] == 100
        assert event.metadata["mtime"] == 123456.0


class TestDebounceConfig:
    """Test suite for DebounceConfig."""
    
    def test_default_config(self):
        """Test default debounce configuration."""
        config = DebounceConfig()
        
        assert config.strategy == DebounceStrategy.FIXED_DELAY
        assert config.base_delay == 1.0
        assert config.max_delay == 5.0
        assert config.adaptive_multiplier == 1.5
    
    def test_custom_config(self):
        """Test custom debounce configuration."""
        config = DebounceConfig(
            strategy=DebounceStrategy.ADAPTIVE,
            base_delay=0.5,
            max_delay=3.0,
            adaptive_multiplier=2.0
        )
        
        assert config.strategy == DebounceStrategy.ADAPTIVE
        assert config.base_delay == 0.5
        assert config.max_delay == 3.0
        assert config.adaptive_multiplier == 2.0


class TestFactoryFunction:
    """Test suite for factory functions."""
    
    @pytest.mark.asyncio
    async def test_create_file_watcher(self, temp_dir):
        """Test creating file watcher via factory function."""
        watcher = create_file_watcher(
            [str(temp_dir)],
            debounce_strategy="adaptive",
            debounce_delay=0.5
        )
        
        assert watcher.debounce_config.strategy == DebounceStrategy.ADAPTIVE
        assert watcher.debounce_config.base_delay == 0.5
        assert watcher.enable_recursive is True
        
        await watcher.start()
        await watcher.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])