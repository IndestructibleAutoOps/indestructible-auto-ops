"""
Configuration File Watcher - Enterprise Grade
==============================================

This module provides advanced file monitoring capabilities for configuration files
with enterprise-grade features including:
- Multiple file monitoring strategies
- Efficient debouncing and throttling
- Cross-platform compatibility
- Resource-efficient implementation
"""

import asyncio
import logging
import os
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set
import hashlib


logger = logging.getLogger(__name__)


class WatchEventType(Enum):
    """Types of file watch events."""
    MODIFIED = "modified"
    CREATED = "created"
    DELETED = "deleted"
    MOVED = "moved"


@dataclass
class WatchEvent:
    """Represents a file watch event."""
    event_type: WatchEventType
    path: Path
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    old_path: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class DebounceStrategy(Enum):
    """Debounce strategies for file events."""
    FIXED_DELAY = "fixed_delay"
    ADAPTIVE = "adaptive"
    AGGRESSIVE = "aggressive"
    CONSERVATIVE = "conservative"


@dataclass
class DebounceConfig:
    """Debounce configuration."""
    strategy: DebounceStrategy = DebounceStrategy.FIXED_DELAY
    base_delay: float = 1.0
    max_delay: float = 5.0
    adaptive_multiplier: float = 1.5


class ConfigFileWatcher:
    """
    Enterprise-grade configuration file watcher.
    
    Features:
    - Efficient file monitoring with minimal resource usage
    - Multiple debounce strategies
    - Event buffering and aggregation
    - Cross-platform support
    - Thread-safe operations
    
    Performance Targets:
    - CPU usage: <1%
    - Memory overhead: <5MB
    - Event latency: <1s
    """
    
    def __init__(
        self,
        watch_paths: List[Path],
        debounce_config: Optional[DebounceConfig] = None,
        enable_recursive: bool = True,
        max_buffer_size: int = 1000
    ):
        """
        Initialize the file watcher.
        
        Args:
            watch_paths: List of paths to watch
            debounce_config: Debounce configuration
            enable_recursive: Enable recursive directory watching
            max_buffer_size: Maximum event buffer size
        """
        self.watch_paths = [Path(p) for p in watch_paths]
        self.debounce_config = debounce_config or DebounceConfig()
        self.enable_recursive = enable_recursive
        self.max_buffer_size = max_buffer_size
        
        # State management
        self._is_running = False
        self._watcher_thread: Optional[threading.Thread] = None
        self._event_handlers: List[Callable[[WatchEvent], None]] = []
        
        # File tracking
        self._file_hashes: Dict[Path, str] = {}
        self._file_stats: Dict[Path, os.stat_result] = {}
        self._event_buffer: deque = deque(maxlen=max_buffer_size)
        
        # Debouncing
        self._pending_events: Dict[Path, float] = {}
        self._last_debounce_time: float = 0.0
        self._adaptive_delay: float = self.debounce_config.base_delay
        
        # Statistics
        self._total_events = 0
        self._buffered_events = 0
        self._debounced_events = 0
        
        # Thread safety
        self._lock = threading.RLock()
        
        logger.info(
            f"ConfigFileWatcher initialized for {len(watch_paths)} paths, "
            f"strategy={debounce_config.strategy.value}"
        )
    
    async def start(self) -> None:
        """Start the file watcher."""
        with self._lock:
            if self._is_running:
                logger.warning("ConfigFileWatcher already running")
                return
            
            self._is_running = True
            
            # Initialize file tracking
            self._initialize_file_tracking()
            
            # Start watcher thread
            self._watcher_thread = threading.Thread(
                target=self._watcher_loop,
                name="ConfigFileWatcher",
                daemon=True
            )
            self._watcher_thread.start()
            
            logger.info("ConfigFileWatcher started successfully")
    
    async def stop(self) -> None:
        """Stop the file watcher."""
        with self._lock:
            if not self._is_running:
                logger.warning("ConfigFileWatcher not running")
                return
            
            self._is_running = False
        
        # Wait for watcher thread to stop
        if self._watcher_thread:
            self._watcher_thread.join(timeout=5.0)
        
        logger.info("ConfigFileWatcher stopped")
    
    def _initialize_file_tracking(self) -> None:
        """Initialize file tracking for all watch paths."""
        logger.info("Initializing file tracking...")
        
        for path in self.watch_paths:
            if path.is_file():
                self._track_file(path)
            elif path.is_dir() and self.enable_recursive:
                self._track_directory(path)
            elif path.is_dir():
                self._track_file(path)
    
    def _track_file(self, path: Path) -> None:
        """Track a single file."""
        try:
            if path.exists():
                self._file_stats[path] = path.stat()
                self._file_hashes[path] = self._compute_file_hash(path)
                logger.debug(f"Tracking file: {path}")
        except Exception as e:
            logger.error(f"Failed to track file {path}: {e}")
    
    def _track_directory(self, path: Path) -> None:
        """Track all files in a directory."""
        try:
            for item in path.rglob('*'):
                if item.is_file():
                    self._track_file(item)
        except Exception as e:
            logger.error(f"Failed to track directory {path}: {e}")
    
    def _compute_file_hash(self, path: Path) -> str:
        """Compute hash of file content."""
        try:
            with open(path, 'rb') as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
        except Exception:
            return ""
    
    def _watcher_loop(self) -> None:
        """Main watcher loop - runs in background thread."""
        logger.info("Watcher loop started")
        
        while self._is_running:
            try:
                self._check_for_changes()
                time.sleep(0.5)  # Check every 500ms
            except Exception as e:
                logger.error(f"Error in watcher loop: {e}")
        
        logger.info("Watcher loop stopped")
    
    def _check_for_changes(self) -> None:
        """Check for file changes."""
        current_time = time.time()
        
        for path in self.watch_paths:
            try:
                if path.is_file():
                    self._check_file_change(path, current_time)
                elif path.is_dir() and self.enable_recursive:
                    self._check_directory_changes(path, current_time)
                elif path.is_dir():
                    self._check_file_change(path, current_time)
            except Exception as e:
                logger.error(f"Error checking {path}: {e}")
    
    def _check_file_change(self, path: Path, current_time: float) -> None:
        """Check for changes in a single file."""
        try:
            if not path.exists():
                # File deleted
                self._handle_file_deleted(path)
                return
            
            # Check if file modified
            current_stat = path.stat()
            last_stat = self._file_stats.get(path)
            
            if last_stat is None:
                # New file
                self._handle_file_created(path)
                self._file_stats[path] = current_stat
                return
            
            # Compare modification time and size
            if (current_stat.st_mtime != last_stat.st_mtime or
                current_stat.st_size != last_stat.st_size):
                
                # Check hash to confirm actual change
                current_hash = self._compute_file_hash(path)
                last_hash = self._file_hashes.get(path)
                
                if current_hash != last_hash:
                    self._handle_file_modified(path)
                    self._file_stats[path] = current_stat
                    self._file_hashes[path] = current_hash
        
        except Exception as e:
            logger.error(f"Error checking file {path}: {e}")
    
    def _check_directory_changes(self, path: Path, current_time: float) -> None:
        """Check for changes in a directory."""
        try:
            current_files = set()
            
            # Scan directory
            for item in path.rglob('*'):
                if item.is_file():
                    current_files.add(item)
                    
                    # Check if new file
                    if item not in self._file_stats:
                        self._handle_file_created(item)
                        self._track_file(item)
                    else:
                        self._check_file_change(item, current_time)
            
            # Check for deleted files
            tracked_files = set(self._file_stats.keys())
            deleted_files = tracked_files - current_files
            
            for deleted_file in deleted_files:
                self._handle_file_deleted(deleted_file)
                del self._file_stats[deleted_file]
                if deleted_file in self._file_hashes:
                    del self._file_hashes[deleted_file]
        
        except Exception as e:
            logger.error(f"Error checking directory {path}: {e}")
    
    def _handle_file_created(self, path: Path) -> None:
        """Handle file creation event."""
        event = WatchEvent(event_type=WatchEventType.CREATED, path=path)
        self._buffer_event(event, path)
    
    def _handle_file_modified(self, path: Path) -> None:
        """Handle file modification event."""
        event = WatchEvent(event_type=WatchEventType.MODIFIED, path=path)
        self._buffer_event(event, path)
    
    def _handle_file_deleted(self, path: Path) -> None:
        """Handle file deletion event."""
        event = WatchEvent(event_type=WatchEventType.DELETED, path=path)
        self._buffer_event(event, path)
    
    def _buffer_event(self, event: WatchEvent, path: Path) -> None:
        """Buffer an event with debouncing."""
        current_time = time.time()
        self._total_events += 1
        
        # Add to pending events for debouncing
        self._pending_events[path] = current_time
        
        # Determine debounce delay based on strategy
        delay = self._calculate_debounce_delay()
        
        # Check if debounce period has passed
        if current_time - self._last_debounce_time >= delay:
            # Flush pending events
            self._flush_pending_events()
            self._last_debounce_time = current_time
    
    def _calculate_debounce_delay(self) -> float:
        """Calculate debounce delay based on strategy."""
        strategy = self.debounce_config.strategy
        
        if strategy == DebounceStrategy.FIXED_DELAY:
            return self.debounce_config.base_delay
        
        elif strategy == DebounceStrategy.ADAPTIVE:
            # Adjust based on event frequency
            event_count = len(self._pending_events)
            if event_count > 10:
                return min(self.debounce_config.max_delay, 
                          self._adaptive_delay * self.debounce_config.adaptive_multiplier)
            else:
                return self.debounce_config.base_delay
        
        elif strategy == DebounceStrategy.AGGRESSIVE:
            # Longer debounce for high frequency
            return min(self.debounce_config.max_delay, 
                      self.debounce_config.base_delay * 2.0)
        
        elif strategy == DebounceStrategy.CONSERVATIVE:
            # Shorter debounce for quick response
            return self.debounce_config.base_delay * 0.5
        
        return self.debounce_config.base_delay
    
    def _flush_pending_events(self) -> None:
        """Flush all pending events to handlers."""
        if not self._pending_events:
            return
        
        current_time = time.time()
        
        for path, event_time in list(self._pending_events.items()):
            # Check if event is old enough to be considered stable
            delay = self._calculate_debounce_delay()
            if current_time - event_time >= delay:
                # Determine event type
                if not path.exists():
                    event = WatchEvent(event_type=WatchEventType.DELETED, path=path)
                elif path not in self._file_stats:
                    event = WatchEvent(event_type=WatchEventType.CREATED, path=path)
                else:
                    event = WatchEvent(event_type=WatchEventType.MODIFIED, path=path)
                
                # Add to buffer
                if len(self._event_buffer) < self.max_buffer_size:
                    self._event_buffer.append(event)
                    self._buffered_events += 1
                else:
                    logger.warning(f"Event buffer full, dropping event for {path}")
                
                # Remove from pending
                del self._pending_events[path]
                self._debounced_events += 1
                
                # Notify handlers
                self._notify_handlers(event)
    
    def _notify_handlers(self, event: WatchEvent) -> None:
        """Notify all registered event handlers."""
        for handler in self._event_handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error in event handler: {e}")
    
    def add_event_handler(self, handler: Callable[[WatchEvent], None]) -> None:
        """Add an event handler."""
        with self._lock:
            self._event_handlers.append(handler)
    
    def remove_event_handler(self, handler: Callable[[WatchEvent], None]) -> None:
        """Remove an event handler."""
        with self._lock:
            if handler in self._event_handlers:
                self._event_handlers.remove(handler)
    
    def get_statistics(self) -> Dict[str, int]:
        """Get watcher statistics."""
        return {
            "total_events": self._total_events,
            "buffered_events": self._buffered_events,
            "debounced_events": self._debounced_events,
            "tracked_files": len(self._file_stats),
            "pending_events": len(self._pending_events),
            "buffer_size": len(self._event_buffer)
        }
    
    def is_running(self) -> bool:
        """Check if watcher is running."""
        return self._is_running


def create_file_watcher(
    watch_paths: List[str],
    debounce_strategy: str = "fixed_delay",
    debounce_delay: float = 1.0
) -> ConfigFileWatcher:
    """
    Factory function to create a file watcher instance.
    
    Args:
        watch_paths: List of paths to watch
        debounce_strategy: Debounce strategy name
        debounce_delay: Base debounce delay in seconds
        
    Returns:
        Configured ConfigFileWatcher instance
    """
    strategy = DebounceStrategy(debounce_strategy)
    debounce_config = DebounceConfig(
        strategy=strategy,
        base_delay=debounce_delay
    )
    
    paths = [Path(p) for p in watch_paths]
    return ConfigFileWatcher(
        watch_paths=paths,
        debounce_config=debounce_config,
        enable_recursive=True
    )